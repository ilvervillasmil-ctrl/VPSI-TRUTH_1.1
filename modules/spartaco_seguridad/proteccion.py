# ===============================================================
# VPSI-TRUTH — modules/spartaco_seguridad/proteccion.py
# ===============================================================
#
# ESTRUCTURA GENERATIVA: nodo Z/S/Q recursivo
#
#                    ED25519
#                 AUTORIDAD RAÍZ
#                       │
#                       ▼
#                     ROOT
#                       │
#                ┌──────┼──────┐
#                ▼      ▼      ▼
#                Z      S      Q
#                │      │      │
#             hijos   hijos   hijos
#                │      │      │
#              ZSQ    ZSQ     ZSQ
#
# INVARIANTE DE CIERRE (para todo nodo N):
#   válido(N) ⇔ estructura(N) ∧ Z(N) ∧ S(N) ∧ Q(N)
#              ∧ compromisos_hijos(N) ∧ autorización(N)
#
#   N - Z → inválido
#   N - S → inválido
#   N - Q → inválido
#   N - hijo → inválido
#   N + hijo extraño → inválido
#   N alterado → inválido
#
# División / recomposición:
#   válido(N) → N1,N2,N3 con válido(Ni) → recomponer → válido(N)
#   La misma ley se aplica a cada Ni (recursión).
#
# RESPONSABILIDADES:
#   Z/S/Q     = integridad / invarianza estructural (recursiva)
#   Ed25519   = autoridad criptográfica sobre la raíz
#   Esquema   = semántica del cuerpo contractual
#   Congelar  = eliminar comportamiento Python arbitrario
#
# FRONTERA: todo lo externo es NO CONFIABLE.
# Ninguna ruta a ok=True sin atravesar todas las fronteras del modo.
# ===============================================================

from __future__ import annotations

import hashlib
import hmac
import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

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

# Campos del cuerpo (hojas del árbol contractual)
HOJAS_META: Tuple[str, ...] = (
    "esquema",
    "version",
    "emitido",
    "artifact_id",
    "clave_publica_id",
    "algoritmo_hash",
    "algoritmo_firma",
)
HOJAS_INTEGRIDAD: Tuple[str, ...] = (
    "nucleo",
    "S",
    "Q",
    "n_bytes",
)
HOJAS_EVIDENCIA: Tuple[str, ...] = (
    "n_neutro",
    "valuaciones",
    "identidad_neutra",
)

CLAVES_CUERPO: frozenset = frozenset(
    HOJAS_META + HOJAS_INTEGRIDAD + HOJAS_EVIDENCIA + ("zsq_raiz",)
)

SEGURIDAD: Dict[str, Any] = {
    "id": "PROTECCION",
    "nombre": "proteccion",
    "hace": (
        "Cierre criptográfico por nodo Z/S/Q recursivo + Ed25519 sobre la raíz. "
        "Toda división válida conserva la invariante; toda recomposición válida "
        "reconstruye la invariante del nivel superior."
    ),
    "herramienta": "ZSQ-recursivo + Ed25519 + manifiesto {cuerpo, firma}",
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
# FRONTERA TIPO (sin coerción)
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


# ===============================================================
# CANÓNICO / CONGELACIÓN
# ===============================================================

def serializar(obj: Any) -> bytes:
    """
    Encoding determinista. Lanza ValueError si no es JSON seguro.
    En fronteras de entrada hostil usar serializar_seguro().
    """
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
    """Nunca lanza. Frontera para datos externos."""
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
# NODO Z/S/Q RECURSIVO  (abstracción única)
# ===============================================================
#
# Nodo
#  ├── tag
#  ├── payload   (hoja)  XOR  hijos (interior)
#  ├── Z, S, Q
#  └── compromiso = H(N|tag|Z|S|Q)
#
# Misma ley en cada nivel. No se agregan funciones por capa.
#

def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class NodoZSQ:
    """
    Contrato recursivo de integridad.

    Hoja:  payload canónico → Z/S/Q sobre ese payload.
    Interior: hijos → Z/S/Q sobre los compromisos de los hijos.

    compromiso(N) depende de Z,S,Q; Z,S,Q dependen del contenido.
    Alterar un descendiente altera el compromiso de todos los ancestros.
    """

    __slots__ = ("tag", "payload", "hijos", "_z", "_s", "_q", "_c")

    def __init__(
        self,
        tag: str,
        *,
        payload: Any = None,
        hijos: Optional[Sequence["NodoZSQ"]] = None,
    ) -> None:
        if not _es_str(tag) or not tag:
            raise ValueError("tag inválido")
        self.tag = tag
        self.payload = payload
        self.hijos: List[NodoZSQ] = list(hijos) if hijos else []
        if self.hijos and payload is not None:
            raise ValueError("nodo no puede ser hoja e interior a la vez")
        self._z: Optional[str] = None
        self._s: Optional[str] = None
        self._q: Optional[str] = None
        self._c: Optional[str] = None

    # --- Z / S / Q ---

    def z(self) -> str:
        if self._z is not None:
            return self._z
        if self.hijos:
            # Z = digest estructural de (tag + compromisos ordenados de hijos)
            mat = "|".join(h.compromiso() for h in self.hijos)
            self._z = _sha(b"Z|" + self.tag.encode("ascii") + b"|" + mat.encode("ascii"))
        else:
            raw = serializar(self.payload)
            self._z = _sha(b"Z|" + self.tag.encode("ascii") + b"|" + raw)
        return self._z

    def s(self) -> str:
        if self._s is not None:
            return self._s
        if self.hijos:
            cs = [h.compromiso() for h in self.hijos]
            mid = len(cs) // 2
            self._s = _sha(b"S|" + "|".join(cs[:mid]).encode("ascii"))
        else:
            raw = serializar(self.payload)
            mid = len(raw) // 2
            self._s = _sha(b"S|" + raw[:mid])
        return self._s

    def q(self) -> str:
        if self._q is not None:
            return self._q
        if self.hijos:
            cs = [h.compromiso() for h in self.hijos]
            mid = len(cs) // 2
            self._q = _sha(b"Q|" + "|".join(cs[mid:]).encode("ascii"))
        else:
            raw = serializar(self.payload)
            mid = len(raw) // 2
            self._q = _sha(b"Q|" + raw[mid:])
        return self._q

    def compromiso(self) -> str:
        if self._c is not None:
            return self._c
        self._c = _sha(
            b"N|"
            + self.tag.encode("ascii")
            + b"|"
            + self.z().encode("ascii")
            + b"|"
            + self.s().encode("ascii")
            + b"|"
            + self.q().encode("ascii")
        )
        return self._c

    def invalido(self) -> bool:
        """
        INVARIANTE DE CIERRE local:
        - Z, S, Q calculables
        - si hay hijos: todos válidos
        - compromiso estable (recomputar coincide)
        """
        try:
            z1, s1, q1, c1 = self.z(), self.s(), self.q(), self.compromiso()
            # forzar recálculo
            self._z = self._s = self._q = self._c = None
            z2, s2, q2, c2 = self.z(), self.s(), self.q(), self.compromiso()
            if not (z1 == z2 and s1 == s2 and q1 == q2 and c1 == c2):
                return True
            for h in self.hijos:
                if h.invalido():
                    return True
            return False
        except (ValueError, TypeError, OverflowError):
            return True

    def snapshot(self) -> Dict[str, Any]:
        return {
            "tag": self.tag,
            "z": self.z(),
            "s": self.s(),
            "q": self.q(),
            "compromiso": self.compromiso(),
            "hijos": [h.snapshot() for h in self.hijos],
        }


def construir_arbol_cuerpo(campos: Dict[str, Any]) -> NodoZSQ:
    """
    ROOT
    ├── meta        (hojas HOJAS_META)
    ├── integridad  (hojas HOJAS_INTEGRIDAD)
    └── evidencia   (hojas HOJAS_EVIDENCIA)

    Cada hoja = NodoZSQ(tag, payload=valor del campo).
    """
    def hojas(tags: Tuple[str, ...]) -> List[NodoZSQ]:
        out: List[NodoZSQ] = []
        for t in tags:
            if t not in campos:
                raise ValueError(f"falta hoja {t}")
            out.append(NodoZSQ(t, payload=campos[t]))
        return out

    meta = NodoZSQ("meta", hijos=hojas(HOJAS_META))
    integ = NodoZSQ("integridad", hijos=hojas(HOJAS_INTEGRIDAD))
    evid = NodoZSQ("evidencia", hijos=hojas(HOJAS_EVIDENCIA))
    return NodoZSQ("raiz", hijos=[meta, integ, evid])


def zsq_de_cuerpo(campos: Dict[str, Any]) -> Dict[str, Any]:
    """
    Construye el árbol y devuelve la raíz Z/S/Q + compromiso.
    Si cualquier hoja es hostil (no serializable), ok=False.
    """
    try:
        root = construir_arbol_cuerpo(campos)
        if root.invalido():
            return _rechazo("INTEGRIDAD_COMPROMETIDA", error="nodo inválido")
        return {
            "ok": True,
            "zsq_raiz": root.compromiso(),
            "z": root.z(),
            "s": root.s(),
            "q": root.q(),
            "arbol": root.snapshot(),
            "conceptos": [],
        }
    except (ValueError, TypeError, OverflowError, KeyError) as e:
        return _rechazo("CÓDIGO_INVÁLIDO", error=str(e))


def verificar_zsq_cuerpo(cuerpo: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recalcula el árbol desde las hojas y exige:
      cuerpo['zsq_raiz'] == root.compromiso()
    Cualquier campo alterado → raíz distinta → FAIL.
    """
    if "zsq_raiz" not in cuerpo:
        return _rechazo("CÓDIGO_INVÁLIDO", error="falta zsq_raiz")
    declarada = cuerpo["zsq_raiz"]
    if not _es_hex64(declarada):
        return _rechazo("CÓDIGO_INVÁLIDO", error="zsq_raiz no hex64")

    campos = {
        k: cuerpo[k]
        for k in (HOJAS_META + HOJAS_INTEGRIDAD + HOJAS_EVIDENCIA)
    }
    calc = zsq_de_cuerpo(campos)
    if not calc.get("ok"):
        return calc

    if not hmac.compare_digest(calc["zsq_raiz"], declarada):
        return _rechazo(
            "INTEGRIDAD_COMPROMETIDA",
            "ALTERACIÓN",
            error="zsq_raiz diverge",
            raiz_real=calc["zsq_raiz"],
            raiz_declarada=declarada,
        )
    return {
        "ok": True,
        "zsq_raiz": calc["zsq_raiz"],
        "z": calc["z"],
        "s": calc["s"],
        "q": calc["q"],
        "arbol": calc["arbol"],
        "conceptos": [],
    }


def fijar_zsq(cuerpo: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recalcula y escribe cuerpo['zsq_raiz'] desde las hojas actuales.
    Obligatorio tras cualquier mutación legítima de campos antes de firmar.
    """
    if type(cuerpo) is not dict:
        return _rechazo("CÓDIGO_INVÁLIDO", error="cuerpo no dict")
    campos = {
        k: cuerpo[k]
        for k in (HOJAS_META + HOJAS_INTEGRIDAD + HOJAS_EVIDENCIA)
        if k in cuerpo
    }
    calc = zsq_de_cuerpo(campos)
    if not calc.get("ok"):
        return calc
    cuerpo["zsq_raiz"] = calc["zsq_raiz"]
    return {"ok": True, "cuerpo": cuerpo, "arbol": calc["arbol"], "conceptos": []}


# ===============================================================
# INTEGRIDAD DE BYTES (artefacto)
# ===============================================================

def nucleo(datos: bytes) -> str:
    if not _es_bytes(datos):
        raise TypeError("datos debe ser bytes")
    return hashlib.sha256(bytes(datos)).hexdigest()


def nucleo_digest(datos: bytes) -> bytes:
    if not _es_bytes(datos):
        raise TypeError("datos debe ser bytes")
    return hashlib.sha256(bytes(datos)).digest()


def _fragmentos(datos: bytes, k: int = 8) -> List[bytes]:
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


def canales(datos: bytes) -> Tuple[str, str]:
    if not _es_bytes(datos):
        raise TypeError("datos debe ser bytes")
    datos = bytes(datos)
    mid = len(datos) // 2
    return (
        hashlib.sha256(datos[:mid]).hexdigest(),
        hashlib.sha256(datos[mid:]).hexdigest(),
    )


def z_invariante(datos: bytes, k: int = 8) -> Dict[str, Any]:
    if not _es_bytes(datos):
        return _rechazo("CÓDIGO_INVÁLIDO", error="datos no bytes", z=None, valuaciones=[])
    try:
        frags = _fragmentos(bytes(datos), k=k)
    except (TypeError, ValueError) as e:
        return _rechazo("CÓDIGO_INVÁLIDO", error=str(e), z=None, valuaciones=[])
    vals: List[int] = []
    for f in frags:
        h = hashlib.sha256(f).digest()
        z = 0
        for b in h:
            if b == 0:
                z += 8
            else:
                z += 8 - b.bit_length()
                break
        vals.append(z)
    return {
        "ok": True,
        "z": min(vals) if vals else 0,
        "valuaciones": vals,
        "conceptos": [],
    }


def comparar_z(z_a: Any, z_b: Any) -> Dict[str, Any]:
    if not _es_int(z_a) or not _es_int(z_b):
        return _rechazo("CÓDIGO_INVÁLIDO", error="z no int")
    return {"ok": True, "igual": z_a == z_b, "conceptos": []}


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

    for campo in ("nucleo", "S", "Q", "zsq_raiz"):
        if not _es_hex64(cuerpo[campo]):
            return _rechazo("CÓDIGO_INVÁLIDO", error=f"{campo} no hex64")

    if not _es_int(cuerpo["n_bytes"]) or cuerpo["n_bytes"] < 0:
        return _rechazo("CÓDIGO_INVÁLIDO", error="n_bytes")
    if not _es_int(cuerpo["n_neutro"]) or cuerpo["n_neutro"] < 2:
        return _rechazo("CÓDIGO_INVÁLIDO", error="n_neutro")

    vals = cuerpo["valuaciones"]
    if type(vals) is not list or not all(_es_int(x) for x in vals):
        return _rechazo("CÓDIGO_INVÁLIDO", error="valuaciones")

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
    s_chan, q_chan = canales(datos)
    zinfo = z_invariante(datos)
    if not zinfo.get("ok"):
        return _rechazo("CÓDIGO_INVÁLIDO", error="z")
    neutro = verificar_neutro(datos, n=n_neutro)

    base: Dict[str, Any] = {
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
        "nucleo": nucleo(datos),
        "S": s_chan,
        "Q": q_chan,
        "n_bytes": len(datos),
        "n_neutro": n_neutro,
        "valuaciones": zinfo["valuaciones"],
        "identidad_neutra": bool(neutro.get("ok")),
    }

    # Fijar ZSQ raíz desde las hojas (regla generativa)
    fz = fijar_zsq(base)
    if not fz.get("ok"):
        return fz

    val = _validar_cuerpo_esquema(base, version_minima=1)
    if not val["ok"]:
        return val
    return {
        "ok": True,
        "cuerpo": base,
        "arbol": fz.get("arbol"),
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
# forma → canónico → Ed25519 → congelar → esquema → ZSQ

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

    # ZSQ: recalcular árbol y exigir igualdad con zsq_raiz firmada
    zsq = verificar_zsq_cuerpo(cuerpo)
    if not zsq.get("ok"):
        return zsq

    return {
        "ok": True,
        "cuerpo": cuerpo,
        "arbol": zsq.get("arbol"),
        "zsq": {"z": zsq["z"], "s": zsq["s"], "q": zsq["q"], "raiz": zsq["zsq_raiz"]},
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
        return _rechazo("CÓDIGO_INVÁLIDO", error=ser.get("error", "canónico"), fallos=["canonicalización"])
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
        "arbol": check.get("arbol"),
        "zsq": check.get("zsq"),
        "conceptos": [],
    }


# ===============================================================
# RUNTIME verificar()
# ===============================================================

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
        if man.get("zsq"):
            pasos["zsq"] = man["zsq"]
        if man.get("arbol"):
            pasos["arbol"] = man["arbol"]
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
            if man.get("zsq"):
                pasos["zsq"] = man["zsq"]
        else:
            pasos["manifiesto"] = {"ok": None, "nota": "ausente en diagnóstico"}

    if cuerpo is not None:
        n_uso = cuerpo["n_neutro"]
        nucleo_ref = cuerpo["nucleo"]
        s_ref = cuerpo["S"]
        q_ref = cuerpo["Q"]
        n_bytes_ref = cuerpo["n_bytes"]
        vals_ref = cuerpo["valuaciones"]
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
        nucleo_ref = nucleo_esperado if _es_hex64(nucleo_esperado) else None
        s_ref = S_esperado if _es_hex64(S_esperado) else None
        q_ref = Q_esperado if _es_hex64(Q_esperado) else None
        n_bytes_ref = None
        vals_ref = None
        neutro_ref = None

    h = nucleo(datos)
    s_real, q_real = canales(datos)

    if nucleo_ref is not None:
        ok_n = hmac.compare_digest(h, nucleo_ref)
        pasos["nucleo"] = {"ok": ok_n, "real": h}
        if not ok_n:
            fallos.append("nucleo")
            conceptos.append("INTEGRIDAD_COMPROMETIDA")
    else:
        pasos["nucleo"] = {"ok": None, "real": h}

    if s_ref is not None and q_ref is not None:
        ok_c = hmac.compare_digest(s_real, s_ref) and hmac.compare_digest(q_real, q_ref)
        pasos["canales"] = {"ok": ok_c, "S": s_real, "Q": q_real}
        if not ok_c:
            fallos.append("canales")
            if "INTEGRIDAD_COMPROMETIDA" not in conceptos:
                conceptos.append("INTEGRIDAD_COMPROMETIDA")
    else:
        pasos["canales"] = {"ok": None, "S": s_real, "Q": q_real}

    if n_bytes_ref is not None and n_bytes_ref != len(datos):
        fallos.append("n_bytes")
        conceptos.append("INTEGRIDAD_COMPROMETIDA")
        pasos["n_bytes"] = {"ok": False, "real": len(datos), "ref": n_bytes_ref}
    else:
        pasos["n_bytes"] = {
            "ok": True if n_bytes_ref is not None else None,
            "real": len(datos),
        }

    zinfo = z_invariante(datos)
    pasos["z"] = {
        "ok": True,
        "z": zinfo.get("z"),
        "valuaciones": zinfo.get("valuaciones"),
        "coherente_con_cuerpo": (
            zinfo.get("valuaciones") == vals_ref if vals_ref is not None else None
        ),
    }

    neutro = verificar_neutro(datos, n=n_uso)
    pasos["identidad_neutra"] = {
        "ok": bool(neutro.get("ok")),
        "n": n_uso,
        "coherente_con_cuerpo": (
            bool(neutro.get("ok")) == bool(neutro_ref) if neutro_ref is not None else None
        ),
    }

    if modo == MODO_PROTEGIDO:
        ok = all(
            [
                pasos.get("manifiesto", {}).get("ok") is True,
                pasos.get("nucleo", {}).get("ok") is True,
                pasos.get("canales", {}).get("ok") is True,
                len(fallos) == 0,
            ]
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
    "zsq_de_cuerpo",
    "verificar_zsq_cuerpo",
    "fijar_zsq",
    "construir_arbol_cuerpo",
    "_fragmentos",
]
