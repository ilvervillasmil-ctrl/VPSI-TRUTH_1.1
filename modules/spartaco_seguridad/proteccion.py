# ===============================================================
# VPSI-TRUTH — modules/spartaco_seguridad/proteccion.py
# ===============================================================
#
# UNA SOLA REGLA GENERATIVA
#
#   DATOS
#     │
#     ▼
#   PARTIR en 3  (Z_bytes, S_bytes, Q_bytes)
#     │
#     ├── Nodo(Z_bytes)  → compromiso_Z
#     ├── Nodo(S_bytes)  → compromiso_S
#     └── Nodo(Q_bytes)  → compromiso_Q
#             │
#             ▼
#   compromiso(N) = H("N" | Z | S | Q)
#             │
#             ▼  (recursión hasta hoja)
#           ROOT
#             │
#             ▼
#          Ed25519
#
# INVARIANTE DE CIERRE (todo nodo N):
#   válido(N) ⇔ Z(N) ∧ S(N) ∧ Q(N) ∧ hijos_válidos ∧ ROOT autenticado
#
#   Quitar / añadir / alterar / reordenar una pieza
#   → compromiso del ancestro diverge
#   → ROOT diverge
#   → firma inválida o raíz no coincide
#   → ok=False
#
# NODOS INMUTABLES: no se mutan. Cambio ⇒ nodo nuevo ⇒ padre nuevo ⇒ ROOT nuevo.
#
# Z/S/Q son tres ramas equivalentes (ternaria), no "hash total + dos mitades".
# Nucleo del artefacto = ROOT. Canales del artefacto = (Z,S,Q) de la raíz.
#
# FRONTERA: todo lo externo es NO CONFIABLE.
# ===============================================================

from __future__ import annotations

import hashlib
import hmac
import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    PublicFormat,
)

# ===============================================================
# CONTRATO
# ===============================================================

ESQUEMA_MANIFIESTO: int = 1
VERSION_MINIMA_DEFAULT: int = 1
MAX_VERSION: int = 10_000_000

MODO_PROTEGIDO: str = "PROTEGIDO"
MODO_DIAGNOSTICO: str = "DIAGNOSTICO"

ALGORITMO_HASH: str = "SHA-256"
ALGORITMO_FIRMA: str = "Ed25519"

# Partición ternaria recursiva
HOJA_MAX_BYTES: int = 32          # bajo este tamaño (o profundidad máx) → hoja
PROFUNDIDAD_MAX: int = 12

# Campos del cuerpo autenticado (metadatos + raíz ZSQ de los DATOS)
CLAVES_CUERPO: frozenset = frozenset(
    {
        "esquema",
        "version",
        "emitido",
        "artifact_id",
        "clave_publica_id",
        "algoritmo_hash",
        "algoritmo_firma",
        "n_bytes",
        "n_neutro",
        "identidad_neutra",
        # raíz y ramas del árbol de DATOS
        "root",   # compromiso(Nodo(datos))
        "Z",      # rama Z de la raíz
        "S",      # rama S de la raíz
        "Q",      # rama Q de la raíz
    }
)

SEGURIDAD: Dict[str, Any] = {
    "id": "PROTECCION",
    "nombre": "proteccion",
    "hace": (
        "Integridad recursiva Z/S/Q del artefacto + autoridad Ed25519 sobre la raíz. "
        "Una sola regla generativa: partir datos en Z/S/Q, comprometer, repetir."
    ),
    "herramienta": "NodoZSQ ternario recursivo + Ed25519 + manifiesto {cuerpo, firma}",
    "conceptos": [
        "FIRMA_INVÁLIDA",
        "INTEGRIDAD_COMPROMETIDA",
        "MANIFIESTO_AUSENTE",
        "CÓDIGO_INVÁLIDO",
        "VERSIÓN_REGRESIVA",
        "ALTERACIÓN",
        "MANIPULACIÓN",
        "CÓDIGO_COMPROMETIDO",
    ],
}


# ===============================================================
# TIPO (sin coerción)
# ===============================================================

def _es_int(x: Any) -> bool:
    return type(x) is int


def _es_bool(x: Any) -> bool:
    return type(x) is bool


def _es_str(x: Any) -> bool:
    return type(x) is str


def _es_bytes(x: Any) -> bool:
    return isinstance(x, (bytes, bytearray))


def _es_hex64(x: Any) -> bool:
    if not _es_str(x) or len(x) != 64:
        return False
    return all(c in "0123456789abcdef" for c in x)


def _rechazo(*conceptos: str, error: str = "", **extra: Any) -> Dict[str, Any]:
    out: Dict[str, Any] = {"ok": False, "conceptos": list(conceptos), "error": error}
    out.update(extra)
    return out


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# ===============================================================
# CANÓNICO / CONGELACIÓN
# ===============================================================

def serializar(obj: Any) -> bytes:
    try:
        texto = json.dumps(
            obj,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    except (TypeError, ValueError, OverflowError) as e:
        raise ValueError(f"no canónico: {e}") from e
    return texto.encode("ascii")


def serializar_seguro(obj: Any) -> Dict[str, Any]:
    try:
        return {"ok": True, "bytes": serializar(obj), "conceptos": []}
    except ValueError as e:
        return _rechazo("CÓDIGO_INVÁLIDO", error=str(e))


def _descongelar_json(canonico: bytes) -> Any:
    if not _es_bytes(canonico):
        raise ValueError("canonico no es bytes")
    try:
        texto = bytes(canonico).decode("ascii")
    except UnicodeDecodeError as e:
        raise ValueError("canonico no ASCII") from e
    try:
        return json.loads(texto)
    except (ValueError, TypeError) as e:
        raise ValueError(f"JSON inválido: {e}") from e


# ===============================================================
# PARTICIÓN TERNARIA (regla generativa única)
# ===============================================================

def _partir3(data: bytes) -> Tuple[bytes, bytes, bytes]:
    """
    Parte en tres trozos lo más iguales posible.
    Z = primer tercio, S = segundo, Q = resto.
    Conserva todos los bytes; es invertible por concatenación.
    """
    n = len(data)
    a = n // 3
    b = n // 3
    # c = n - a - b  (puede ser a o a+1)
    return data[:a], data[a : a + b], data[a + b :]


def _es_hoja(data: bytes, profundidad: int) -> bool:
    return len(data) <= HOJA_MAX_BYTES or profundidad >= PROFUNDIDAD_MAX


# ===============================================================
# NODO Z/S/Q INMUTABLE
# ===============================================================
#
# Construcción:
#   hoja:   Z=H(Z_bytes), S=H(S_bytes), Q=H(Q_bytes)
#           compromiso = H("N"|Z|S|Q)
#   interior:
#           hijo_Z = Nodo(Z_bytes), hijo_S = Nodo(S_bytes), hijo_Q = Nodo(Q_bytes)
#           Z = hijo_Z.compromiso, S = hijo_S.compromiso, Q = hijo_Q.compromiso
#           compromiso = H("N"|Z|S|Q)
#
# No hay setters. Cambio de datos ⇒ construir nodo nuevo.
#

class NodoZSQ:
    __slots__ = ("_data", "_prof", "_z", "_s", "_q", "_c", "_hijo_z", "_hijo_s", "_hijo_q")

    def __init__(self, data: bytes, profundidad: int = 0) -> None:
        if not _es_bytes(data):
            raise TypeError("data debe ser bytes")
        if not _es_int(profundidad) or profundidad < 0:
            raise ValueError("profundidad inválida")
        self._data = bytes(data)
        self._prof = profundidad
        self._z: str
        self._s: str
        self._q: str
        self._c: str
        self._hijo_z: Optional["NodoZSQ"] = None
        self._hijo_s: Optional["NodoZSQ"] = None
        self._hijo_q: Optional["NodoZSQ"] = None
        self._construir()

    def _construir(self) -> None:
        z_b, s_b, q_b = _partir3(self._data)
        if _es_hoja(self._data, self._prof):
            self._z = _sha(b"Z|" + z_b)
            self._s = _sha(b"S|" + s_b)
            self._q = _sha(b"Q|" + q_b)
        else:
            self._hijo_z = NodoZSQ(z_b, self._prof + 1)
            self._hijo_s = NodoZSQ(s_b, self._prof + 1)
            self._hijo_q = NodoZSQ(q_b, self._prof + 1)
            self._z = self._hijo_z.compromiso
            self._s = self._hijo_s.compromiso
            self._q = self._hijo_q.compromiso
        self._c = _sha(
            b"N|"
            + self._z.encode("ascii")
            + b"|"
            + self._s.encode("ascii")
            + b"|"
            + self._q.encode("ascii")
        )

    # --- API de solo lectura ---

    @property
    def z(self) -> str:
        return self._z

    @property
    def s(self) -> str:
        return self._s

    @property
    def q(self) -> str:
        return self._q

    @property
    def compromiso(self) -> str:
        return self._c

    @property
    def es_hoja(self) -> bool:
        return self._hijo_z is None

    @property
    def n_bytes(self) -> int:
        return len(self._data)

    def snapshot(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {
            "z": self._z,
            "s": self._s,
            "q": self._q,
            "compromiso": self._c,
            "n_bytes": len(self._data),
            "profundidad": self._prof,
            "hoja": self.es_hoja,
        }
        if not self.es_hoja:
            out["hijos"] = {
                "Z": self._hijo_z.snapshot() if self._hijo_z else None,
                "S": self._hijo_s.snapshot() if self._hijo_s else None,
                "Q": self._hijo_q.snapshot() if self._hijo_q else None,
            }
        return out


def construir_raiz(datos: bytes) -> Dict[str, Any]:
    """
    DATOS → NodoZSQ → {root, Z, S, Q, arbol}.
    Frontera de tipo: datos debe ser bytes.
    """
    if not _es_bytes(datos):
        return _rechazo("CÓDIGO_INVÁLIDO", error="datos no bytes")
    try:
        nodo = NodoZSQ(bytes(datos), 0)
    except (TypeError, ValueError, OverflowError) as e:
        return _rechazo("CÓDIGO_INVÁLIDO", error=str(e))
    return {
        "ok": True,
        "root": nodo.compromiso,
        "Z": nodo.z,
        "S": nodo.s,
        "Q": nodo.q,
        "n_bytes": nodo.n_bytes,
        "arbol": nodo.snapshot(),
        "conceptos": [],
    }


def verificar_raiz(datos: bytes, root: str, Z: str, S: str, Q: str) -> Dict[str, Any]:
    """
    Reconstruye el árbol desde datos y exige igualdad exacta de root/Z/S/Q.
    Cualquier byte distinto → diverge.
    """
    if not _es_bytes(datos):
        return _rechazo("CÓDIGO_INVÁLIDO", error="datos no bytes")
    for nombre, val in (("root", root), ("Z", Z), ("S", S), ("Q", Q)):
        if not _es_hex64(val):
            return _rechazo("CÓDIGO_INVÁLIDO", error=f"{nombre} no hex64")

    calc = construir_raiz(datos)
    if not calc.get("ok"):
        return calc

    if not hmac.compare_digest(calc["root"], root):
        return _rechazo(
            "INTEGRIDAD_COMPROMETIDA",
            "ALTERACIÓN",
            error="root diverge",
            root_real=calc["root"],
            root_declarado=root,
        )
    if not (
        hmac.compare_digest(calc["Z"], Z)
        and hmac.compare_digest(calc["S"], S)
        and hmac.compare_digest(calc["Q"], Q)
    ):
        return _rechazo(
            "INTEGRIDAD_COMPROMETIDA",
            "ALTERACIÓN",
            error="ramas Z/S/Q divergen",
        )
    return {
        "ok": True,
        "root": calc["root"],
        "Z": calc["Z"],
        "S": calc["S"],
        "Q": calc["Q"],
        "arbol": calc["arbol"],
        "conceptos": [],
    }


# ===============================================================
# COMPATIBILIDAD: nucleo / canales / z_invariante
# (derivados de la misma regla, no un sistema paralelo)
# ===============================================================

def nucleo(datos: bytes) -> str:
    """Identidad criptográfica del artefacto = ROOT del árbol ZSQ."""
    r = construir_raiz(datos)
    if not r.get("ok"):
        raise TypeError(r.get("error", "nucleo"))
    return r["root"]


def nucleo_digest(datos: bytes) -> bytes:
    return bytes.fromhex(nucleo(datos))


def canales(datos: bytes) -> Tuple[str, str]:
    """S y Q de la raíz del árbol (ramas estructurales)."""
    r = construir_raiz(datos)
    if not r.get("ok"):
        raise TypeError(r.get("error", "canales"))
    return r["S"], r["Q"]


def z_invariante(datos: bytes, k: int = 8) -> Dict[str, Any]:
    """
    Evidencia: Z de la raíz + profundidad efectiva.
    k se ignora como parámetro de fragmentación fija (la partición es ternaria recursiva).
    """
    if not _es_bytes(datos):
        return _rechazo("CÓDIGO_INVÁLIDO", error="datos no bytes", z=None, valuaciones=[])
    r = construir_raiz(datos)
    if not r.get("ok"):
        return _rechazo("CÓDIGO_INVÁLIDO", error=r.get("error", "z"), z=None, valuaciones=[])
    # valuaciones: compromisos de las tres ramas (evidencia, no autoridad extra)
    return {
        "ok": True,
        "z": r["Z"],
        "valuaciones": [r["Z"], r["S"], r["Q"]],
        "root": r["root"],
        "conceptos": [],
    }


def comparar_z(z_a: Any, z_b: Any) -> Dict[str, Any]:
    if not _es_str(z_a) or not _es_str(z_b):
        # también acepta int legacy
        if not (_es_int(z_a) and _es_int(z_b)):
            return _rechazo("CÓDIGO_INVÁLIDO", error="z tipo inválido")
        return {"ok": True, "igual": z_a == z_b, "conceptos": []}
    return {"ok": True, "igual": hmac.compare_digest(z_a, z_b), "conceptos": []}


def _fragmentos(datos: bytes, k: int = 8) -> List[bytes]:
    """
    Compatibilidad residual. La partición canónica es ternaria recursiva (_partir3).
    Esta función solo se conserva para callers antiguos; no define la invariante.
    """
    if not _es_bytes(datos):
        raise TypeError("datos debe ser bytes")
    if not _es_int(k) or k < 1:
        raise ValueError("k inválido")
    datos = bytes(datos)
    n = len(datos)
    if n == 0:
        return []
    if n < k:
        return [datos[i : i + 1] for i in range(n)]
    base, extra = divmod(n, k)
    out: List[bytes] = []
    ini = 0
    for i in range(k):
        tam = base + (1 if i < extra else 0)
        out.append(datos[ini : ini + tam])
        ini += tam
    return out


# ===============================================================
# IDENTIDAD NEUTRA
# ===============================================================

MARCA_NEUTRA = b"\n#VPSI-NEUTRO:"


def sellar(datos: bytes, n: int = 3, max_intentos: int = 100_000) -> Dict[str, Any]:
    if not _es_bytes(datos):
        return _rechazo("CÓDIGO_INVÁLIDO", error="datos no bytes")
    if not _es_int(n) or n < 2:
        return _rechazo("CÓDIGO_INVÁLIDO", error="n_neutro inválido")
    if not _es_int(max_intentos) or max_intentos < 1:
        return _rechazo("CÓDIGO_INVÁLIDO", error="max_intentos inválido")
    datos = bytes(datos)
    for i in range(max_intentos):
        candidato = datos + MARCA_NEUTRA + str(i).encode("ascii")
        if int(hashlib.sha256(candidato).hexdigest(), 16) % n == 0:
            return {
                "ok": True,
                "datos": candidato,
                "n": n,
                "intentos": i + 1,
                "conceptos": [],
            }
    return _rechazo("CÓDIGO_INVÁLIDO", error="no se alcanzó neutro")


def verificar_neutro(datos: bytes, n: int = 3) -> Dict[str, Any]:
    if not _es_bytes(datos):
        return _rechazo("CÓDIGO_INVÁLIDO", error="datos no bytes")
    if not _es_int(n) or n < 2:
        return _rechazo("CÓDIGO_INVÁLIDO", error="n_neutro inválido")
    ok = int(hashlib.sha256(bytes(datos)).hexdigest(), 16) % n == 0
    return {"ok": ok, "n": n, "conceptos": [] if ok else ["CÓDIGO_INVÁLIDO"]}


# ===============================================================
# Ed25519
# ===============================================================

def generar_claves(ruta_priv: str, ruta_pub: str) -> Dict[str, Any]:
    if not _es_str(ruta_priv) or not _es_str(ruta_pub):
        return _rechazo("CÓDIGO_INVÁLIDO", error="rutas inválidas")
    try:
        priv = Ed25519PrivateKey.generate()
        pub = priv.public_key()
        Path(ruta_priv).write_bytes(
            priv.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())
        )
        Path(ruta_pub).write_bytes(
            pub.public_bytes(Encoding.Raw, PublicFormat.Raw)
        )
    except (OSError, TypeError, ValueError) as e:
        return _rechazo("CÓDIGO_INVÁLIDO", error=str(e))
    return {"ok": True, "conceptos": []}


def firmar_bytes(datos: bytes, ruta_priv: str) -> Dict[str, Any]:
    if not _es_bytes(datos):
        return _rechazo("CÓDIGO_INVÁLIDO", error="datos no bytes")
    if not _es_str(ruta_priv):
        return _rechazo("CÓDIGO_INVÁLIDO", error="ruta_priv inválida")
    try:
        raw = Path(ruta_priv).read_bytes()
        if len(raw) != 32:
            return _rechazo("CÓDIGO_INVÁLIDO", error="clave privada longitud inválida")
        sig = Ed25519PrivateKey.from_private_bytes(raw).sign(bytes(datos))
    except (OSError, TypeError, ValueError) as e:
        return _rechazo("CÓDIGO_INVÁLIDO", error=str(e))
    return {"ok": True, "firma": sig.hex(), "conceptos": []}


def verificar_bytes(
    datos: bytes,
    firma_hex: str,
    *,
    pub_bytes: bytes,
) -> Dict[str, Any]:
    if not _es_bytes(datos):
        return _rechazo("FIRMA_INVÁLIDA", error="datos no bytes")
    if not _es_str(firma_hex):
        return _rechazo("FIRMA_INVÁLIDA", error="firma no str")
    if not _es_bytes(pub_bytes):
        return _rechazo("FIRMA_INVÁLIDA", error="pub_bytes tipo inválido")
    pub_bytes = bytes(pub_bytes)
    if len(pub_bytes) != 32:
        return _rechazo("FIRMA_INVÁLIDA", error="pub_bytes longitud inválida")
    try:
        sig = bytes.fromhex(firma_hex)
    except (ValueError, TypeError):
        return _rechazo("FIRMA_INVÁLIDA", error="firma hex inválida")
    if len(sig) != 64:
        return _rechazo("FIRMA_INVÁLIDA", error="firma longitud inválida")
    try:
        Ed25519PublicKey.from_public_bytes(pub_bytes).verify(sig, bytes(datos))
    except (InvalidSignature, TypeError, ValueError):
        return _rechazo("FIRMA_INVÁLIDA", error="firma inválida")
    return {"ok": True, "conceptos": []}


def firmar(datos: bytes, ruta_priv: str) -> Dict[str, Any]:
    return firmar_bytes(datos, ruta_priv)


def verificar_firma(
    datos: bytes, firma_hex: str, *, pub_bytes: bytes
) -> Dict[str, Any]:
    return verificar_bytes(datos, firma_hex, pub_bytes=pub_bytes)


# ===============================================================
# ESQUEMA DEL CUERPO
# ===============================================================

def _validar_cuerpo_esquema(
    cuerpo: Any,
    *,
    version_minima: int = VERSION_MINIMA_DEFAULT,
) -> Dict[str, Any]:
    if type(cuerpo) is not dict:
        return _rechazo("CÓDIGO_INVÁLIDO", error="cuerpo no dict ordinario")

    claves = set(cuerpo.keys())
    if claves != set(CLAVES_CUERPO):
        return _rechazo(
            "CÓDIGO_INVÁLIDO",
            error=(
                f"claves inválidas extra={claves - set(CLAVES_CUERPO)} "
                f"faltan={set(CLAVES_CUERPO) - claves}"
            ),
        )

    if cuerpo["esquema"] != ESQUEMA_MANIFIESTO:
        return _rechazo("CÓDIGO_INVÁLIDO", error="esquema desconocido")

    ver = cuerpo["version"]
    if not _es_int(ver) or ver < int(version_minima) or ver > MAX_VERSION:
        return _rechazo("VERSIÓN_REGRESIVA", error=f"versión {ver!r}")

    for campo in ("emitido", "artifact_id", "clave_publica_id"):
        if not _es_str(cuerpo[campo]):
            return _rechazo("CÓDIGO_INVÁLIDO", error=f"{campo} no str")

    if cuerpo["algoritmo_hash"] != ALGORITMO_HASH:
        return _rechazo("CÓDIGO_INVÁLIDO", error="algoritmo_hash")
    if cuerpo["algoritmo_firma"] != ALGORITMO_FIRMA:
        return _rechazo("CÓDIGO_INVÁLIDO", error="algoritmo_firma")

    for campo in ("root", "Z", "S", "Q"):
        if not _es_hex64(cuerpo[campo]):
            return _rechazo("CÓDIGO_INVÁLIDO", error=f"{campo} no hex64")

    if not _es_int(cuerpo["n_bytes"]) or cuerpo["n_bytes"] < 0:
        return _rechazo("CÓDIGO_INVÁLIDO", error="n_bytes")
    if not _es_int(cuerpo["n_neutro"]) or cuerpo["n_neutro"] < 2:
        return _rechazo("CÓDIGO_INVÁLIDO", error="n_neutro")
    if not _es_bool(cuerpo["identidad_neutra"]):
        return _rechazo("CÓDIGO_INVÁLIDO", error="identidad_neutra")

    return {"ok": True, "cuerpo": cuerpo, "conceptos": []}


def construir_cuerpo(
    datos: bytes,
    *,
    n_neutro: int = 3,
    artifact_id: str = "",
    version: int = 1,
    clave_publica_id: str = "",
    emitido: Optional[str] = None,
) -> Dict[str, Any]:
    if not _es_bytes(datos):
        return _rechazo("CÓDIGO_INVÁLIDO", error="datos no bytes")
    if not _es_int(n_neutro) or n_neutro < 2:
        return _rechazo("CÓDIGO_INVÁLIDO", error="n_neutro")
    if not _es_int(version) or version < 1 or version > MAX_VERSION:
        return _rechazo("CÓDIGO_INVÁLIDO", error="version")
    if not _es_str(artifact_id) or not _es_str(clave_publica_id):
        return _rechazo("CÓDIGO_INVÁLIDO", error="ids no str")

    datos = bytes(datos)
    raiz = construir_raiz(datos)
    if not raiz.get("ok"):
        return raiz

    neutro = verificar_neutro(datos, n=n_neutro)

    cuerpo: Dict[str, Any] = {
        "esquema": ESQUEMA_MANIFIESTO,
        "version": version,
        "emitido": (
            emitido
            if _es_str(emitido)
            else time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        ),
        "artifact_id": artifact_id,
        "clave_publica_id": clave_publica_id,
        "algoritmo_hash": ALGORITMO_HASH,
        "algoritmo_firma": ALGORITMO_FIRMA,
        "n_bytes": len(datos),
        "n_neutro": n_neutro,
        "identidad_neutra": bool(neutro.get("ok")),
        "root": raiz["root"],
        "Z": raiz["Z"],
        "S": raiz["S"],
        "Q": raiz["Q"],
    }

    val = _validar_cuerpo_esquema(cuerpo, version_minima=1)
    if not val["ok"]:
        return val
    return {
        "ok": True,
        "cuerpo": cuerpo,
        "arbol": raiz["arbol"],
        "conceptos": [],
    }


def construir_manifiesto(cuerpo: Dict[str, Any], firma_hex: str) -> Dict[str, Any]:
    if type(cuerpo) is not dict or not _es_str(firma_hex) or not firma_hex:
        return _rechazo("CÓDIGO_INVÁLIDO", error="manifiesto inválido")
    return {
        "ok": True,
        "manifiesto": {"cuerpo": cuerpo, "firma": firma_hex},
        "conceptos": [],
    }


# ===============================================================
# VERIFICAR MANIFIESTO
# ===============================================================

def verificar_manifiesto(
    manifiesto: Any,
    *,
    pub_bytes: Any = None,
    version_minima: int = VERSION_MINIMA_DEFAULT,
) -> Dict[str, Any]:
    if type(manifiesto) is not dict:
        return _rechazo("MANIFIESTO_AUSENTE", error="manifiesto no dict")
    if set(manifiesto.keys()) != {"cuerpo", "firma"}:
        return _rechazo(
            "CÓDIGO_INVÁLIDO",
            error="manifiesto debe ser exactamente {cuerpo, firma}",
        )

    cuerpo_raw = manifiesto["cuerpo"]
    firma_hex = manifiesto["firma"]

    if type(cuerpo_raw) is not dict:
        return _rechazo("CÓDIGO_INVÁLIDO", error="cuerpo no dict")
    if not _es_str(firma_hex) or not firma_hex:
        return _rechazo("FIRMA_INVÁLIDA", error="firma ausente o tipo inválido")

    ser = serializar_seguro(cuerpo_raw)
    if not ser.get("ok"):
        return ser
    canonico = ser["bytes"]

    if pub_bytes is None:
        return _rechazo("FIRMA_INVÁLIDA", error="clave pública ausente")
    vf = verificar_bytes(canonico, firma_hex, pub_bytes=pub_bytes)
    if not vf.get("ok"):
        return _rechazo("FIRMA_INVÁLIDA", error="firma inválida")

    try:
        cuerpo = _descongelar_json(canonico)
    except ValueError as e:
        return _rechazo("CÓDIGO_INVÁLIDO", error=str(e))

    if not _es_int(version_minima):
        version_minima = VERSION_MINIMA_DEFAULT
    sem = _validar_cuerpo_esquema(cuerpo, version_minima=version_minima)
    if not sem.get("ok"):
        return sem
    cuerpo = sem["cuerpo"]

    return {
        "ok": True,
        "cuerpo": cuerpo,
        "conceptos": [],
    }


# ===============================================================
# BUILD
# ===============================================================

def build(
    datos: bytes,
    ruta_priv: str,
    *,
    n_neutro: int = 3,
    artifact_id: str = "",
    version: int = 1,
    clave_publica_id: str = "",
) -> Dict[str, Any]:
    if not _es_bytes(datos):
        return _rechazo("CÓDIGO_INVÁLIDO", error="datos no bytes", fallos=["entrada"])
    if not _es_str(ruta_priv):
        return _rechazo("CÓDIGO_INVÁLIDO", error="ruta_priv", fallos=["entrada"])
    if not _es_int(n_neutro) or n_neutro < 2:
        return _rechazo("CÓDIGO_INVÁLIDO", error="n_neutro", fallos=["entrada"])
    if not _es_int(version) or version < 1 or version > MAX_VERSION:
        return _rechazo("CÓDIGO_INVÁLIDO", error="version", fallos=["entrada"])
    if not _es_str(artifact_id) or not _es_str(clave_publica_id):
        return _rechazo("CÓDIGO_INVÁLIDO", error="ids", fallos=["entrada"])

    sello = sellar(bytes(datos), n=n_neutro)
    if not sello.get("ok"):
        return _rechazo("CÓDIGO_INVÁLIDO", error="sellar", fallos=["neutro"])

    datos_s = sello["datos"]
    cb = construir_cuerpo(
        datos_s,
        n_neutro=n_neutro,
        artifact_id=artifact_id,
        version=version,
        clave_publica_id=clave_publica_id,
    )
    if not cb.get("ok"):
        return _rechazo("CÓDIGO_INVÁLIDO", error=cb.get("error", "cuerpo"), fallos=["cuerpo"])

    cuerpo = cb["cuerpo"]
    ser = serializar_seguro(cuerpo)
    if not ser.get("ok"):
        return _rechazo(
            "CÓDIGO_INVÁLIDO",
            error=ser.get("error", "canónico"),
            fallos=["canonicalización"],
        )
    canonico = ser["bytes"]

    firma = firmar_bytes(canonico, ruta_priv)
    if not firma.get("ok"):
        return _rechazo("CÓDIGO_INVÁLIDO", error=firma.get("error", "firma"), fallos=["firma"])

    man = {"cuerpo": cuerpo, "firma": firma["firma"]}

    try:
        priv_raw = Path(ruta_priv).read_bytes()
        priv = Ed25519PrivateKey.from_private_bytes(priv_raw)
        pub_bytes = priv.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
    except (OSError, TypeError, ValueError) as e:
        return _rechazo("CÓDIGO_INVÁLIDO", error=str(e), fallos=["clave"])

    check = verificar_manifiesto(man, pub_bytes=pub_bytes, version_minima=1)
    if not check.get("ok"):
        return _rechazo(
            "CÓDIGO_INVÁLIDO",
            error=f"build no auto-valida: {check.get('error')}",
            fallos=["cierre"],
        )

    return {
        "ok": True,
        "datos": datos_s,
        "manifiesto": man,
        "arbol": cb.get("arbol"),
        "conceptos": [],
    }


# ===============================================================
# RUNTIME verificar()
# ===============================================================
#
# UNA pregunta estructural:
#   ¿Los datos reconstruyen exactamente root/Z/S/Q del cuerpo
#    y ese cuerpo está autorizado por Ed25519?
#

def verificar(
    datos: Any,
    *,
    manifiesto: Any = None,
    pub_bytes: Any = None,
    modo: Any = MODO_PROTEGIDO,
    n_neutro: Any = None,
    nucleo_esperado: Any = None,
    S_esperado: Any = None,
    Q_esperado: Any = None,
    firma_hex: Any = None,
    version_minima: int = VERSION_MINIMA_DEFAULT,
) -> Dict[str, Any]:
    pasos: Dict[str, Any] = {}
    fallos: List[str] = []
    conceptos: List[str] = []

    if not _es_bytes(datos):
        return {
            "ok": False,
            "fallos": ["datos"],
            "conceptos": ["CÓDIGO_INVÁLIDO"],
            "pasos": {},
            "error": "datos no bytes",
        }
    datos = bytes(datos)

    if modo not in (MODO_PROTEGIDO, MODO_DIAGNOSTICO):
        modo = MODO_PROTEGIDO

    cuerpo: Optional[Dict[str, Any]] = None

    # --- autoridad del manifiesto ---
    if modo == MODO_PROTEGIDO:
        if manifiesto is None:
            return {
                "ok": False,
                "fallos": ["manifiesto"],
                "conceptos": ["MANIFIESTO_AUSENTE"],
                "pasos": {"manifiesto": {"ok": False}},
                "error": "manifiesto ausente",
            }
        man = verificar_manifiesto(
            manifiesto, pub_bytes=pub_bytes, version_minima=version_minima
        )
        pasos["manifiesto"] = {"ok": bool(man.get("ok"))}
        if not man.get("ok"):
            fallos.append("manifiesto")
            conceptos.extend(man.get("conceptos") or ["FIRMA_INVÁLIDA"])
            return {
                "ok": False,
                "fallos": fallos,
                "conceptos": conceptos,
                "pasos": pasos,
                "error": man.get("error", ""),
            }
        cuerpo = man["cuerpo"]
    else:
        if manifiesto is not None:
            man = verificar_manifiesto(
                manifiesto, pub_bytes=pub_bytes, version_minima=version_minima
            )
            pasos["manifiesto"] = {"ok": bool(man.get("ok"))}
            if not man.get("ok"):
                fallos.append("manifiesto")
                conceptos.extend(man.get("conceptos") or ["FIRMA_INVÁLIDA"])
                return {
                    "ok": False,
                    "fallos": fallos,
                    "conceptos": conceptos,
                    "pasos": pasos,
                    "error": man.get("error", ""),
                }
            cuerpo = man["cuerpo"]
        else:
            pasos["manifiesto"] = {"ok": None, "nota": "ausente en diagnóstico"}

    # --- referencias: cuerpo firmado manda en PROTEGIDO ---
    if cuerpo is not None:
        root_ref = cuerpo["root"]
        z_ref = cuerpo["Z"]
        s_ref = cuerpo["S"]
        q_ref = cuerpo["Q"]
        n_bytes_ref = cuerpo["n_bytes"]
        n_uso = cuerpo["n_neutro"]
        neutro_ref = cuerpo["identidad_neutra"]
    else:
        if n_neutro is not None and (not _es_int(n_neutro) or n_neutro < 2):
            return {
                "ok": False,
                "fallos": ["n_neutro"],
                "conceptos": ["CÓDIGO_INVÁLIDO"],
                "pasos": pasos,
            }
        n_uso = n_neutro if _es_int(n_neutro) else 3
        root_ref = nucleo_esperado if _es_hex64(nucleo_esperado) else None
        z_ref = None
        s_ref = S_esperado if _es_hex64(S_esperado) else None
        q_ref = Q_esperado if _es_hex64(Q_esperado) else None
        n_bytes_ref = None
        neutro_ref = None

    # --- UNA pregunta: datos → árbol ¿coincide con root/Z/S/Q autorizados? ---
    if root_ref is not None and z_ref is not None and s_ref is not None and q_ref is not None:
        vr = verificar_raiz(datos, root_ref, z_ref, s_ref, q_ref)
        pasos["zsq"] = {
            "ok": bool(vr.get("ok")),
            "root": vr.get("root_real", vr.get("root")),
            "error": vr.get("error"),
        }
        if not vr.get("ok"):
            fallos.append("zsq")
            conceptos.extend(vr.get("conceptos") or ["INTEGRIDAD_COMPROMETIDA"])
    else:
        # diagnóstico parcial
        calc = construir_raiz(datos)
        pasos["zsq"] = {
            "ok": None,
            "root": calc.get("root"),
            "Z": calc.get("Z"),
            "S": calc.get("S"),
            "Q": calc.get("Q"),
        }
        if root_ref is not None and calc.get("ok"):
            if not hmac.compare_digest(calc["root"], root_ref):
                fallos.append("root")
                conceptos.append("INTEGRIDAD_COMPROMETIDA")
                pasos["zsq"]["ok"] = False

    if n_bytes_ref is not None and n_bytes_ref != len(datos):
        fallos.append("n_bytes")
        conceptos.append("INTEGRIDAD_COMPROMETIDA")
        pasos["n_bytes"] = {"ok": False, "real": len(datos), "ref": n_bytes_ref}
    else:
        pasos["n_bytes"] = {
            "ok": True if n_bytes_ref is not None else None,
            "real": len(datos),
        }

    # neutro: si el cuerpo lo declara, debe coincidir
    neutro = verificar_neutro(datos, n=n_uso)
    coherente_neutro = (
        bool(neutro.get("ok")) == bool(neutro_ref) if neutro_ref is not None else None
    )
    pasos["identidad_neutra"] = {
        "ok": bool(neutro.get("ok")),
        "n": n_uso,
        "coherente_con_cuerpo": coherente_neutro,
    }
    if coherente_neutro is False:
        fallos.append("identidad_neutra")
        conceptos.append("INTEGRIDAD_COMPROMETIDA")

    # --- veredicto ---
    if modo == MODO_PROTEGIDO:
        ok = (
            pasos.get("manifiesto", {}).get("ok") is True
            and pasos.get("zsq", {}).get("ok") is True
            and len(fallos) == 0
        )
    else:
        ok = len(fallos) == 0

    return {
        "ok": ok,
        "fallos": fallos,
        "conceptos": conceptos,
        "pasos": pasos,
    }


# ===============================================================
# EXPORTS
# ===============================================================

__all__ = [
    "SEGURIDAD",
    "ESQUEMA_MANIFIESTO",
    "MODO_PROTEGIDO",
    "MODO_DIAGNOSTICO",
    "NodoZSQ",
    "construir_raiz",
    "verificar_raiz",
    "nucleo",
    "nucleo_digest",
    "canales",
    "z_invariante",
    "comparar_z",
    "sellar",
    "verificar_neutro",
    "generar_claves",
    "firmar",
    "firmar_bytes",
    "verificar_firma",
    "verificar_bytes",
    "serializar",
    "serializar_seguro",
    "construir_cuerpo",
    "construir_manifiesto",
    "verificar_manifiesto",
    "build",
    "verificar",
    "_fragmentos",
    "_partir3",
]
