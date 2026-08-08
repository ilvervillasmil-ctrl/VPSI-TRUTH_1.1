# ===============================================================
# VPSI-TRUTH — modules/spartaco_seguridad/proteccion.py
# ===============================================================
#
# CONTRATO DE IDENTIDAD (genealogía + autoridad)
#
#   LLAVE (clave_publica_id)
#           │
#           ▼
#   ARTEFACTO (artifact_id)
#           │
#           ▼
#   NÚCLEO  ← entidad arquitectónica
#   ├── digest = SHA-256(datos)     = cuerpo["nucleo"]
#   ├── root   = H(N|Z|S|Q)         = compromiso ZSQ (interno)
#   └── authority_id
#           │
#      ┌────┼────┐
#      ▼    ▼    ▼
#      Z    S    Q   cada uno: id, parent_id, role, depth, digest
#      │
#     hijos con la misma ficha de identidad…
#
# node_id = H(artifact_id | path)   path = "ROOT" | "ROOT/Z" | …
# parent_id = node_id del padre ("" en ROOT)
#
# DIAGNÓSTICO POR ENTIDAD (no por edificio):
#   datos ≠ nucleo  → fallos += "nucleo"
#   S/Q divergen    → fallos += "canales"
#   pasos: manifiesto, nucleo, canales, z, n_bytes, identidad_neutra
#
# CUERPO FIRMADO (CLAVES_CUERPO): nucleo, S, Q, valuaciones, …
# ROOT no sustituye a nucleo. valuaciones se deposita autenticada.
#
# serializar = frontera: valida tipo/rango ANTES de json.dumps.
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

# ---------------------------------------------------------------
# CONTRATO
# ---------------------------------------------------------------

ESQUEMA_MANIFIESTO: int = 1
VERSION_MINIMA_DEFAULT: int = 1
MAX_VERSION: int = 10_000_000

MODO_PROTEGIDO: str = "PROTEGIDO"
MODO_DIAGNOSTICO: str = "DIAGNOSTICO"

ALGORITMO_HASH: str = "SHA-256"
ALGORITMO_FIRMA: str = "Ed25519"

HOJA_MAX_BYTES: int = 32
PROFUNDIDAD_MAX: int = 12

CLAVES_CUERPO: frozenset = frozenset(
    {
        "esquema",
        "version",
        "emitido",
        "artifact_id",
        "clave_publica_id",
        "algoritmo_hash",
        "algoritmo_firma",
        "nucleo",
        "S",
        "Q",
        "n_bytes",
        "n_neutro",
        "valuaciones",
        "identidad_neutra",
    }
)

SEGURIDAD: Dict[str, Any] = {
    "id": "PROTECCION",
    "nombre": "proteccion",
    "hace": (
        "Autentica artefactos con identidad genealógica: nucleo, canales S/Q, "
        "valuaciones y árbol ZSQ con node_id/parent_id; autoridad Ed25519."
    ),
    "herramienta": "Ed25519 + SHA-256 + NodoZSQ(id) + manifiesto {cuerpo, firma}",
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


# ---------------------------------------------------------------
# TIPO
# ---------------------------------------------------------------

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


# ---------------------------------------------------------------
# CANÓNICO — frontera segura
# ---------------------------------------------------------------
# Rechaza tipo/rango ANTES de json.dumps.
# No deja que bytes / objetos / int gigante lleguen al encoder.

def _prevalidar_json(obj: Any, _depth: int = 0) -> None:
    if _depth > 64:
        raise ValueError("profundidad JSON excesiva")
    if obj is None or _es_bool(obj) or _es_str(obj):
        return
    if _es_int(obj):
        # evita conversion overflow (version gigante, etc.)
        if obj.bit_length() > 256:
            raise ValueError("entero fuera de rango contractual")
        return
    if type(obj) is float:
        if obj != obj or obj in (float("inf"), float("-inf")):
            raise ValueError("float no finito")
        return
    if type(obj) is list:
        for x in obj:
            _prevalidar_json(x, _depth + 1)
        return
    if type(obj) is dict:
        for k, v in obj.items():
            if not _es_str(k):
                raise ValueError("clave JSON no str")
            _prevalidar_json(v, _depth + 1)
        return
    raise ValueError(f"tipo no JSON: {type(obj).__name__}")


def serializar(obj: Any) -> bytes:
    """
    Frontera canónica. Valida dominio JSON contractual y luego codifica.
    Lanza ValueError clasificado (no TypeError crudo del encoder).
    """
    try:
        _prevalidar_json(obj)
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


# ---------------------------------------------------------------
# IDENTIDAD DE NODO (genealogía)
# ---------------------------------------------------------------

def node_id(artifact_id: str, path: str) -> str:
    """ID determinista: H(artifact_id | path)."""
    if not _es_str(artifact_id) or not _es_str(path):
        raise ValueError("artifact_id/path inválidos")
    return _sha(f"{artifact_id}|{path}".encode("utf-8"))


def _partir3(data: bytes) -> Tuple[bytes, bytes, bytes]:
    n = len(data)
    a = n // 3
    b = n // 3
    return data[:a], data[a : a + b], data[a + b :]


class NodoZSQ:
    """
    Nodo inmutable con ficha de identidad.

    id, parent_id, role, depth, path, digest, authority_id, artifact_id
    """

    __slots__ = (
        "id",
        "parent_id",
        "role",
        "depth",
        "path",
        "digest",
        "authority_id",
        "artifact_id",
        "z",
        "s",
        "q",
        "_hijo_z",
        "_hijo_s",
        "_hijo_q",
    )

    def __init__(
        self,
        data: bytes,
        *,
        artifact_id: str,
        authority_id: str,
        role: str = "ROOT",
        path: str = "ROOT",
        parent_id: str = "",
        depth: int = 0,
    ) -> None:
        if not _es_bytes(data):
            raise TypeError("data debe ser bytes")
        if role not in ("ROOT", "Z", "S", "Q"):
            raise ValueError("role inválido")
        data = bytes(data)
        self.artifact_id = artifact_id
        self.authority_id = authority_id
        self.role = role
        self.path = path
        self.parent_id = parent_id
        self.depth = depth
        self.id = node_id(artifact_id, path)
        self._hijo_z = self._hijo_s = self._hijo_q = None

        z_b, s_b, q_b = _partir3(data)
        if len(data) <= HOJA_MAX_BYTES or depth >= PROFUNDIDAD_MAX:
            self.z = _sha(b"Z|" + z_b)
            self.s = _sha(b"S|" + s_b)
            self.q = _sha(b"Q|" + q_b)
        else:
            self._hijo_z = NodoZSQ(
                z_b,
                artifact_id=artifact_id,
                authority_id=authority_id,
                role="Z",
                path=f"{path}/Z",
                parent_id=self.id,
                depth=depth + 1,
            )
            self._hijo_s = NodoZSQ(
                s_b,
                artifact_id=artifact_id,
                authority_id=authority_id,
                role="S",
                path=f"{path}/S",
                parent_id=self.id,
                depth=depth + 1,
            )
            self._hijo_q = NodoZSQ(
                q_b,
                artifact_id=artifact_id,
                authority_id=authority_id,
                role="Q",
                path=f"{path}/Q",
                parent_id=self.id,
                depth=depth + 1,
            )
            self.z = self._hijo_z.digest
            self.s = self._hijo_s.digest
            self.q = self._hijo_q.digest

        self.digest = _sha(
            b"N|"
            + self.z.encode("ascii")
            + b"|"
            + self.s.encode("ascii")
            + b"|"
            + self.q.encode("ascii")
        )

    def ficha(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "parent_id": self.parent_id,
            "role": self.role,
            "depth": self.depth,
            "path": self.path,
            "digest": self.digest,
            "z": self.z,
            "s": self.s,
            "q": self.q,
            "authority_id": self.authority_id,
            "artifact_id": self.artifact_id,
        }

    def snapshot(self) -> Dict[str, Any]:
        out = self.ficha()
        if self._hijo_z is not None:
            out["hijos"] = {
                "Z": self._hijo_z.snapshot(),
                "S": self._hijo_s.snapshot() if self._hijo_s else None,
                "Q": self._hijo_q.snapshot() if self._hijo_q else None,
            }
        return out


def construir_arbol(
    datos: bytes,
    *,
    artifact_id: str = "",
    authority_id: str = "",
) -> Dict[str, Any]:
    if not _es_bytes(datos):
        return _rechazo("CÓDIGO_INVÁLIDO", error="datos no bytes")
    try:
        root = NodoZSQ(
            bytes(datos),
            artifact_id=artifact_id,
            authority_id=authority_id,
            role="ROOT",
            path="ROOT",
            parent_id="",
            depth=0,
        )
    except (TypeError, ValueError) as e:
        return _rechazo("CÓDIGO_INVÁLIDO", error=str(e))
    return {
        "ok": True,
        "root_digest": root.digest,
        "nucleo_id": root.id,
        "Z": root.z,
        "S": root.s,
        "Q": root.q,
        "ficha": root.ficha(),
        "arbol": root.snapshot(),
        "conceptos": [],
    }


# ---------------------------------------------------------------
# INTEGRIDAD CONTRACTUAL (nombres públicos)
# ---------------------------------------------------------------

def nucleo(datos: bytes) -> str:
    """Digest contractual del artefacto = SHA-256(datos). Entidad: nucleo."""
    if not _es_bytes(datos):
        raise TypeError("datos debe ser bytes")
    return hashlib.sha256(bytes(datos)).hexdigest()


def nucleo_digest(datos: bytes) -> bytes:
    if not _es_bytes(datos):
        raise TypeError("datos debe ser bytes")
    return hashlib.sha256(bytes(datos)).digest()


def canales(datos: bytes) -> Tuple[str, str]:
    if not _es_bytes(datos):
        raise TypeError("datos debe ser bytes")
    datos = bytes(datos)
    mid = len(datos) // 2
    return (
        hashlib.sha256(datos[:mid]).hexdigest(),
        hashlib.sha256(datos[mid:]).hexdigest(),
    )


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


# ---------------------------------------------------------------
# NEUTRO
# ---------------------------------------------------------------

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


# ---------------------------------------------------------------
# Ed25519
# ---------------------------------------------------------------

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


# ---------------------------------------------------------------
# ESQUEMA / CUERPO
# ---------------------------------------------------------------

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

    for campo in ("nucleo", "S", "Q"):
        if not _es_hex64(cuerpo[campo]):
            return _rechazo("CÓDIGO_INVÁLIDO", error=f"{campo} no hex64")

    if not _es_int(cuerpo["n_bytes"]) or cuerpo["n_bytes"] < 0:
        return _rechazo("CÓDIGO_INVÁLIDO", error="n_bytes")
    if not _es_int(cuerpo["n_neutro"]) or cuerpo["n_neutro"] < 2:
        return _rechazo("CÓDIGO_INVÁLIDO", error="n_neutro")

    # Cada valuación es un conteo de bits nulos iniciales de un SHA-256
    # (0..256), y _fragmentos emite a lo sumo 64 tramos.
    vals = cuerpo["valuaciones"]
    if type(vals) is not list or len(vals) > 64:
        return _rechazo("CÓDIGO_INVÁLIDO", error="valuaciones")
    for x in vals:
        if not _es_int(x) or x < 0 or x > 256:
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

    # genealogía (depositable como evidencia de pasos; no sustituye nucleo)
    arbol = construir_arbol(
        datos, artifact_id=artifact_id, authority_id=clave_publica_id
    )

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
        "nucleo": nucleo(datos),
        "S": s_chan,
        "Q": q_chan,
        "n_bytes": len(datos),
        "n_neutro": n_neutro,
        "valuaciones": zinfo["valuaciones"],
        "identidad_neutra": bool(neutro.get("ok")),
    }

    val = _validar_cuerpo_esquema(cuerpo, version_minima=1)
    if not val["ok"]:
        return val
    return {
        "ok": True,
        "cuerpo": cuerpo,
        "genealogia": arbol if arbol.get("ok") else None,
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


# ---------------------------------------------------------------
# VERIFICAR MANIFIESTO
# ---------------------------------------------------------------

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

    return {"ok": True, "cuerpo": sem["cuerpo"], "conceptos": []}


# ---------------------------------------------------------------
# BUILD
# ---------------------------------------------------------------

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

    firma = firmar_bytes(ser["bytes"], ruta_priv)
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
        "genealogia": cb.get("genealogia"),
        "conceptos": [],
    }


# ---------------------------------------------------------------
# RUNTIME verificar()  — diagnóstico por entidad
# ---------------------------------------------------------------

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

    if cuerpo is not None:
        nucleo_ref = cuerpo["nucleo"]
        s_ref = cuerpo["S"]
        q_ref = cuerpo["Q"]
        n_bytes_ref = cuerpo["n_bytes"]
        n_uso = cuerpo["n_neutro"]
        vals_ref = cuerpo["valuaciones"]
        neutro_ref = cuerpo["identidad_neutra"]
        artifact_id = cuerpo["artifact_id"]
        authority_id = cuerpo["clave_publica_id"]
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
        artifact_id = ""
        authority_id = ""

    # --- entidad NÚCLEO ---
    h = nucleo(datos)
    if nucleo_ref is not None:
        ok_n = hmac.compare_digest(h, nucleo_ref)
        pasos["nucleo"] = {
            "ok": ok_n,
            "real": h,
            "esperado": nucleo_ref,
            "id": node_id(artifact_id, "ROOT") if artifact_id else None,
            "authority_id": authority_id or None,
        }
        if not ok_n:
            fallos.append("nucleo")
            conceptos.append("INTEGRIDAD_COMPROMETIDA")
    else:
        pasos["nucleo"] = {"ok": None, "real": h}

    # --- entidades S / Q (canales) ---
    s_real, q_real = canales(datos)
    if s_ref is not None and q_ref is not None:
        ok_c = hmac.compare_digest(s_real, s_ref) and hmac.compare_digest(q_real, q_ref)
        pasos["canales"] = {
            "ok": ok_c,
            "S": s_real,
            "Q": q_real,
            "S_id": node_id(artifact_id, "ROOT/S") if artifact_id else None,
            "Q_id": node_id(artifact_id, "ROOT/Q") if artifact_id else None,
        }
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

    # --- evidencia Z (no autoridad; no entra en fallos) ---
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
        ok = (
            pasos.get("manifiesto", {}).get("ok") is True
            and pasos.get("nucleo", {}).get("ok") is True
            and pasos.get("canales", {}).get("ok") is True
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

# ---------------------------------------------------------------
# CONTRATO
# ---------------------------------------------------------------

ESQUEMA_MANIFIESTO: int = 1
VERSION_MINIMA_DEFAULT: int = 1
MAX_VERSION: int = 10_000_000

MODO_PROTEGIDO: str = "PROTEGIDO"
MODO_DIAGNOSTICO: str = "DIAGNOSTICO"

ALGORITMO_HASH: str = "SHA-256"
ALGORITMO_FIRMA: str = "Ed25519"

HOJA_MAX_BYTES: int = 32
PROFUNDIDAD_MAX: int = 12

CLAVES_CUERPO: frozenset = frozenset(
    {
        "esquema",
        "version",
        "emitido",
        "artifact_id",
        "clave_publica_id",
        "algoritmo_hash",
        "algoritmo_firma",
        "nucleo",
        "S",
        "Q",
        "n_bytes",
        "n_neutro",
        "valuaciones",
        "identidad_neutra",
    }
)

SEGURIDAD: Dict[str, Any] = {
    "id": "PROTECCION",
    "nombre": "proteccion",
    "hace": (
        "Autentica artefactos con identidad genealógica: nucleo, canales S/Q, "
        "valuaciones y árbol ZSQ con node_id/parent_id; autoridad Ed25519."
    ),
    "herramienta": "Ed25519 + SHA-256 + NodoZSQ(id) + manifiesto {cuerpo, firma}",
    "version": "1.0",
    "clave_declaracion": "capacidades_recurso",
    "capacidades_recurso": [
        # identidad / núcleo
        "nucleo",
        "nucleo_digest",
        "canales",
        "z_invariante",
        "comparar_z",
        # genealogía ZSQ
        "node_id",
        "construir_arbol",
        "NodoZSQ",
        # neutro
        "sellar",
        "verificar_neutro",
        # Ed25519
        "generar_claves",
        "firmar",
        "firmar_bytes",
        "verificar_firma",
        "verificar_bytes",
        # canónico
        "serializar",
        "serializar_seguro",
        # cuerpo / manifiesto
        "construir_cuerpo",
        "construir_manifiesto",
        "verificar_manifiesto",
        # pipeline
        "build",
        "verificar",
    ],
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

# ---------------------------------------------------------------
# EXPORTS
# ---------------------------------------------------------------

__all__ = [
    "SEGURIDAD",
    "ESQUEMA_MANIFIESTO",
    "MODO_PROTEGIDO",
    "MODO_DIAGNOSTICO",
    "NodoZSQ",
    "node_id",
    "construir_arbol",
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
