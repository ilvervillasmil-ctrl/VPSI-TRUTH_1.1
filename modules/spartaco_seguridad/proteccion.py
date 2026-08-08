# ===============================================================
# VPSI-TRUTH — modules/spartaco_seguridad/proteccion.py
# ===============================================================
#
# ARQUITECTURA DE CIERRE RECURSIVO (compromiso fractal)
#
#   ENTRADA EXTERNA
#        │
#        ▼
#   [TIPO] → [FORMA] → [CANÓNICO] → [Ed25519] → [CONGELAR]
#        │
#        ▼
#   [ESQUEMA] → [ÁRBOL DE COMPROMISO] → [INVARIANTES] → [VEREDICTO]
#
# COMPROMISO FRACTAL:
#   Cada hoja = H("HOJA|tag|valor_canónico")
#   Cada nodo = H("NODO|tag|hijo1|hijo2|...")
#   Raíz = compromiso del estado completo.
#
#   Hoja modificada → padre cambia → ancestro cambia → raíz diverge.
#   No hace falta un detector por campo: la divergencia es estructural.
#
# RESPONSABILIDADES:
#   Ed25519     = autoridad / autenticidad sobre el cuerpo canónico
#   SHA-256     = compromiso / integridad (hojas, nodos, núcleo, S, Q)
#   Árbol       = contaminación jerárquica de cualquier cambio local
#   Esquema     = semántica estructural exacta
#   Congelación = eliminación de comportamiento Python arbitrario
#   Invariantes = coherencia cuerpo autenticado ↔ bytes reales
#   Veredicto   = cierre lógico del modo
#
# artifact_id = identificador lógico externo (firmado, no es digest).
# nucleo      = identidad criptográfica de los bytes del artefacto.
#
# FRONTERA DE CONFIANZA: todo lo externo es NO CONFIABLE.
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
# CONSTANTES DE CONTRATO
# ===============================================================

ESQUEMA_MANIFIESTO: int = 1
VERSION_MINIMA_DEFAULT: int = 1
MAX_VERSION: int = 10_000_000

MODO_PROTEGIDO: str = "PROTEGIDO"
MODO_DIAGNOSTICO: str = "DIAGNOSTICO"

ALGORITMO_HASH: str = "SHA-256"
ALGORITMO_FIRMA: str = "Ed25519"

# Orden canónico de hojas del árbol (estable, documentado).
# Cualquier cambio de valor en una hoja → nueva raíz.
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
    HOJAS_META + HOJAS_INTEGRIDAD + HOJAS_EVIDENCIA + ("compromiso_raiz",)
)

SEGURIDAD: Dict[str, Any] = {
    "id": "PROTECCION",
    "nombre": "proteccion",
    "hace": (
        "Cierre criptográfico fractal de artefactos: compromiso jerárquico "
        "SHA-256 + firma Ed25519 del cuerpo canónico; verificación por "
        "fronteras composables (tipo, forma, canónico, autoridad, "
        "congelación, esquema, árbol, invariantes, veredicto)."
    ),
    "herramienta": "Ed25519 + SHA-256 fractal + manifiesto {cuerpo, firma}",
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
# NIVEL 0 — TIPO (sin coerción)
# ===============================================================
# Invariante: type(x) is T. bool no es int contractual.
# Ataques: None, str, list, dict, float, bool-como-int, objetos custom.

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
# NIVEL 1 — CANÓNICO / CONGELACIÓN
# ===============================================================
# Invariante: un encoding determinista; tras autenticar, solo JSON nuevo.
# Ataques: orden de claves, NaN, subclases, __eq__, bytes/set en valores.

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


def _descongelar_json(canonico: bytes) -> Any:
    """
    CONGELACIÓN: bytes autenticados → estructuras JSON ordinarias nuevas.
    No reutiliza el objeto Python original.
    """
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


def _valor_hoja(valor: Any) -> bytes:
    """Representación canónica de un valor de hoja para el árbol."""
    return serializar(valor)


# ===============================================================
# NIVEL 2 — COMPROMISO FRACTAL (árbol de hashes)
# ===============================================================
#
#          ROOT
#           │
#    ┌──────┼──────┐
#    │      │      │
#   META  INTEG  EVID
#    │      │      │
#  hojas  hojas  hojas
#
# Invariante: raíz = f(todas las hojas). Cualquier hoja distinta → raíz distinta.
# No sustituye a Ed25519: Ed25519 autentica el cuerpo (que incluye la raíz).
# El árbol hace explícita la contaminación jerárquica.
#

def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _hoja(tag: str, valor: Any) -> str:
    return _sha256_hex(b"HOJA|" + tag.encode("ascii") + b"|" + _valor_hoja(valor))


def _nodo(tag: str, hijos: Sequence[str]) -> str:
    payload = b"NODO|" + tag.encode("ascii") + b"|" + "|".join(hijos).encode("ascii")
    return _sha256_hex(payload)


def compromiso_fractal(campos: Dict[str, Any]) -> Dict[str, Any]:
    """
    Construye el árbol de compromiso a partir de los campos del cuerpo
    (sin incluir compromiso_raiz a sí mismo).

    Devuelve:
      {
        ok, raiz, meta, integridad, evidencia,
        hojas: {tag: hash_hoja},
      }
    """
    try:
        hojas_meta = [_hoja(t, campos[t]) for t in HOJAS_META]
        hojas_int = [_hoja(t, campos[t]) for t in HOJAS_INTEGRIDAD]
        hojas_ev = [_hoja(t, campos[t]) for t in HOJAS_EVIDENCIA]
    except (KeyError, ValueError, TypeError) as e:
        return _rechazo("CÓDIGO_INVÁLIDO", error=f"hoja: {e}")

    meta = _nodo("meta", hojas_meta)
    integridad = _nodo("integridad", hojas_int)
    evidencia = _nodo("evidencia", hojas_ev)
    raiz = _nodo("raiz", [meta, integridad, evidencia])

    hojas_map = {}
    for t, h in zip(HOJAS_META, hojas_meta):
        hojas_map[t] = h
    for t, h in zip(HOJAS_INTEGRIDAD, hojas_int):
        hojas_map[t] = h
    for t, h in zip(HOJAS_EVIDENCIA, hojas_ev):
        hojas_map[t] = h

    return {
        "ok": True,
        "raiz": raiz,
        "meta": meta,
        "integridad": integridad,
        "evidencia": evidencia,
        "hojas": hojas_map,
        "conceptos": [],
    }


def verificar_compromiso(cuerpo: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recalcula el árbol desde las hojas del cuerpo y compara con compromiso_raiz.
    Divergencia ⇒ ALTERACIÓN estructural.
    """
    if "compromiso_raiz" not in cuerpo:
        return _rechazo("CÓDIGO_INVÁLIDO", error="falta compromiso_raiz")

    campos = {k: cuerpo[k] for k in (HOJAS_META + HOJAS_INTEGRIDAD + HOJAS_EVIDENCIA)}
    arbol = compromiso_fractal(campos)
    if not arbol.get("ok"):
        return arbol

    raiz_declarada = cuerpo["compromiso_raiz"]
    if not _es_hex64(raiz_declarada):
        return _rechazo("CÓDIGO_INVÁLIDO", error="compromiso_raiz no hex64")

    if not hmac.compare_digest(arbol["raiz"], raiz_declarada):
        return _rechazo(
            "INTEGRIDAD_COMPROMETIDA",
            "ALTERACIÓN",
            error="raíz fractal diverge",
            raiz_real=arbol["raiz"],
            raiz_declarada=raiz_declarada,
        )

    return {
        "ok": True,
        "raiz": arbol["raiz"],
        "meta": arbol["meta"],
        "integridad": arbol["integridad"],
        "evidencia": arbol["evidencia"],
        "conceptos": [],
    }


# ===============================================================
# NIVEL 3 — INTEGRIDAD DE BYTES (núcleo / canales / z)
# ===============================================================
# Invariante: digest determinista de bytes reales. No autorizan.

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
    s = hashlib.sha256(datos[:mid]).hexdigest()
    q = hashlib.sha256(datos[mid:]).hexdigest()
    return s, q


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
# NIVEL 4 — IDENTIDAD NEUTRA
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
# NIVEL 5 — Ed25519 (autoridad)
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
# NIVEL 6 — ESQUEMA DEL CUERPO
# ===============================================================
# Invariante: claves exactas + tipos + rangos + formatos.
# Se aplica solo sobre datos YA congelados.

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

    for campo in ("nucleo", "S", "Q", "compromiso_raiz"):
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
    s, q = canales(datos)
    zinfo = z_invariante(datos)
    if not zinfo.get("ok"):
        return _rechazo("CÓDIGO_INVÁLIDO", error="z")
    neutro = verificar_neutro(datos, n=n_neutro)

    base = {
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
        "S": s,
        "Q": q,
        "n_bytes": len(datos),
        "n_neutro": n_neutro,
        "valuaciones": zinfo["valuaciones"],
        "identidad_neutra": bool(neutro.get("ok")),
    }

    arbol = compromiso_fractal(base)
    if not arbol.get("ok"):
        return arbol
    base["compromiso_raiz"] = arbol["raiz"]

    val = _validar_cuerpo_esquema(base, version_minima=1)
    if not val["ok"]:
        return val
    return {"ok": True, "cuerpo": base, "arbol": arbol, "conceptos": []}


def construir_manifiesto(cuerpo: Dict[str, Any], firma_hex: str) -> Dict[str, Any]:
    if type(cuerpo) is not dict or not _es_str(firma_hex) or not firma_hex:
        return _rechazo("CÓDIGO_INVÁLIDO", error="manifiesto inválido")
    return {
        "ok": True,
        "manifiesto": {"cuerpo": cuerpo, "firma": firma_hex},
        "conceptos": [],
    }


# ===============================================================
# NIVEL 7 — VERIFICAR MANIFIESTO (puerta única del sobre)
# ===============================================================
# Flujo: forma → canónico → Ed25519 → congelar → esquema → árbol

def verificar_manifiesto(
    manifiesto: Any,
    *,
    pub_bytes: Any = None,
    version_minima: int = VERSION_MINIMA_DEFAULT,
) -> Dict[str, Any]:
    # FORMA del sobre
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

    # CANÓNICO
    try:
        canonico = serializar(cuerpo_raw)
    except ValueError as e:
        return _rechazo("CÓDIGO_INVÁLIDO", error=str(e))

    # AUTORIDAD (antes de semántica)
    if pub_bytes is None:
        return _rechazo("FIRMA_INVÁLIDA", error="clave pública ausente")
    vf = verificar_bytes(canonico, firma_hex, pub_bytes=pub_bytes)
    if not vf.get("ok"):
        return _rechazo("FIRMA_INVÁLIDA", error="firma inválida")

    # CONGELACIÓN
    try:
        cuerpo = _descongelar_json(canonico)
    except ValueError as e:
        return _rechazo("CÓDIGO_INVÁLIDO", error=str(e))

    # ESQUEMA
    if not _es_int(version_minima):
        version_minima = VERSION_MINIMA_DEFAULT
    sem = _validar_cuerpo_esquema(cuerpo, version_minima=version_minima)
    if not sem.get("ok"):
        return sem
    cuerpo = sem["cuerpo"]

    # ÁRBOL FRACTAL (recomputar y comparar raíz)
    arb = verificar_compromiso(cuerpo)
    if not arb.get("ok"):
        return arb

    return {
        "ok": True,
        "cuerpo": cuerpo,
        "arbol": {
            "raiz": arb["raiz"],
            "meta": arb["meta"],
            "integridad": arb["integridad"],
            "evidencia": arb["evidencia"],
        },
        "conceptos": [],
    }


# ===============================================================
# NIVEL 8 — BUILD (cierra su círculo)
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
    try:
        canonico = serializar(cuerpo)
    except ValueError as e:
        return _rechazo("CÓDIGO_INVÁLIDO", error=str(e), fallos=["canonicalización"])

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
        "conceptos": [],
    }


# ===============================================================
# NIVEL 9 — RUNTIME verificar()
# ===============================================================
# PROTEGIDO: cuerpo firmado es la única autoridad.
# Parámetros externos no pisan nucleo/S/Q/n_neutro autenticados.

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
            if man.get("arbol"):
                pasos["arbol"] = man["arbol"]
        else:
            pasos["manifiesto"] = {"ok": None, "nota": "ausente en diagnóstico"}

    # Autoridad de parámetros
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

    # Integridad real
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

    # Evidencia (no autoriza; si el cuerpo la declara, debe coincidir)
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

    # VEREDICTO
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
    "construir_cuerpo",
    "construir_manifiesto",
    "verificar_manifiesto",
    "build",
    "verificar",
    "compromiso_fractal",
    "verificar_compromiso",
    "_fragmentos",
]
