# ===============================================================
# modules/seguridad/proteccion.py
# Herramienta única: PROTECCION
# Integridad + autenticidad (Ed25519) + evidencia estructural
# ===============================================================
#
# BUILD (orden obligatorio):
#   datos → sellar() → firmar() → manifiesto
#
# RUNTIME:
#   datos + manifiesto + clave pública → verificar()
#
# MODO_PROTEGIDO  → firma obligatoria (fail-closed)
# MODO_DIAGNOSTICO → firma opcional
#
# La clave pública debe provenir de una raíz de confianza
# (embebida / pinneada). No basta un .pub intercambiable
# al lado del artefacto si el atacante puede sustituirlo.
# ===============================================================

from __future__ import annotations

import hashlib
import json
from math import gcd
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)

# ---------------------------------------------------------------
# Declaración descubrible por SC
# ---------------------------------------------------------------
SEGURIDAD = {
    "id": "proteccion",
    "nombre": "Protección criptográfica unificada",
    "hace": (
        "Sella, firma (Ed25519) y verifica un artefacto. "
        "Hash = integridad. Firma = autenticidad. "
        "Canales / z / residuo = evidencia estructural, no autoridad."
    ),
    "herramienta": "PROTECCION",
    "version": "2.0",
    "conceptos": [
        "FIRMA_INVÁLIDA",
        "INTEGRIDAD_COMPROMETIDA",
        "CÓDIGO_COMPROMETIDO",
        "ALTERACIÓN",
        "MANIPULACIÓN",
        "AMENAZA",
        "CÓDIGO_INVÁLIDO",
        "ALERTA",
    ],
}

MODO_PROTEGIDO = "PROTEGIDO"
MODO_DIAGNOSTICO = "DIAGNOSTICO"
MARCA_NEUTRA = b"\n# OMEGA_NEUTRO:"
ALG_HASH = "SHA-256"
ALG_FIRMA = "Ed25519"


# ===============================================================
# Núcleo C — huella (integridad, no autoridad)
# ===============================================================

def nucleo(datos: bytes) -> str:
    return hashlib.sha256(datos).hexdigest()


def nucleo_digest(datos: bytes) -> bytes:
    return hashlib.sha256(datos).digest()


# ===============================================================
# Canales S · Q — dualidad de observación (no dualidad algebraica)
# ===============================================================

def canales(datos: bytes) -> Dict[str, str]:
    mid = len(datos) // 2
    s, q = datos[:mid], datos[mid:]
    return {
        "S": hashlib.sha256(s).hexdigest(),
        "Q": hashlib.sha256(q).hexdigest(),
        "n_S": len(s),
        "n_Q": len(q),
    }


# ===============================================================
# Fragmentos exactos (sin huecos) + z estructural
# z=1 normal · z=2 permitido · z>=3 obstrucción semántica
# No es detector de manipulación por sí solo.
# ===============================================================

def _fragmentos(datos: bytes, k: int = 8) -> List[bytes]:
    if not datos:
        return [b""]
    n = len(datos)
    cortes = [(n * i) // k for i in range(k + 1)]
    out = [
        datos[cortes[i] : cortes[i + 1]]
        for i in range(k)
        if cortes[i] < cortes[i + 1]
    ]
    return out or [datos]


def _val_efectiva(h: str) -> int:
    c = 0
    for ch in h:
        if ch == "0":
            c += 1
        else:
            break
    return c + 1


def z_invariante(datos: bytes, k: int = 8) -> Dict[str, Any]:
    vals = [
        _val_efectiva(hashlib.sha256(f).hexdigest())
        for f in _fragmentos(datos, k=k)
    ]
    z = vals[0]
    for v in vals[1:]:
        z = gcd(z, v)
    return {
        "z": z,
        "valuaciones": vals,
        "regimen": (
            "normal" if z == 1 else ("cuadrado" if z == 2 else "obstruccion")
        ),
        "nota": (
            "Marcador estructural de hashes de fragmentos. "
            "No sustituye firma ni es control de manipulación."
        ),
    }


# ===============================================================
# Identidad neutra — marca de BUILD (no autenticación)
# Condición real: SHA256(datos) ≡ 0 (mod n)
# Representación reportada: residuo = 1 ⇔ h % n == 0
# ===============================================================

def _es_neutro(datos: bytes, n: int = 3) -> bool:
    return int(hashlib.sha256(datos).hexdigest(), 16) % n == 0


def sellar(
    datos: bytes,
    n: int = 3,
    max_intentos: int = 8192,
) -> Dict[str, Any]:
    """Build: padding mínimo hasta h ≡ 0 (mod n)."""
    if n < 2:
        return {
            "ok": False,
            "error": "n debe ser ≥ 2",
            "conceptos": ["CÓDIGO_INVÁLIDO"],
        }
    for i in range(max_intentos):
        cand = datos + MARCA_NEUTRA + str(i).encode("ascii")
        if _es_neutro(cand, n=n):
            return {
                "ok": True,
                "datos": cand,
                "intentos": i + 1,
                "n": n,
                "neutro": True,
                "conceptos": [],
            }
    return {
        "ok": False,
        "error": "no se pudo sellar",
        "conceptos": ["CÓDIGO_INVÁLIDO"],
    }


def verificar_neutro(datos: bytes, n: int = 3) -> Dict[str, Any]:
    ok = _es_neutro(datos, n=n)
    return {
        "ok": ok,
        "n": n,
        "neutro": ok,
        "conceptos": [] if ok else ["FIRMA_INVÁLIDA"],
        "nota": "Marca de build, no autenticación.",
    }


# ===============================================================
# FIRMA Ed25519 — autoridad criptográfica
# ===============================================================

def generar_claves(ruta_priv: str, ruta_pub: str) -> Dict[str, Any]:
    """La privada no se distribuye. La pública requiere raíz de confianza."""
    priv = Ed25519PrivateKey.generate()
    Path(ruta_priv).write_bytes(
        priv.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
    Path(ruta_pub).write_bytes(
        priv.public_key().public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )
    )
    return {"ok": True, "priv": ruta_priv, "pub": ruta_pub}


def _cargar_priv(ruta_priv: str) -> Ed25519PrivateKey:
    return Ed25519PrivateKey.from_private_bytes(Path(ruta_priv).read_bytes())


def _cargar_pub(
    ruta_pub: Optional[str] = None,
    pub_bytes: Optional[bytes] = None,
) -> Ed25519PublicKey:
    raw = pub_bytes
    if raw is None and ruta_pub is not None:
        raw = Path(ruta_pub).read_bytes()
    if raw is None:
        raise ValueError("sin clave pública")
    return Ed25519PublicKey.from_public_bytes(raw)


def firmar(datos: bytes, ruta_priv: str) -> Dict[str, Any]:
    """Firma el digest del artefacto final (post-sellar)."""
    priv = _cargar_priv(ruta_priv)
    dig = nucleo_digest(datos)
    return {
        "ok": True,
        "nucleo": dig.hex(),
        "firma": priv.sign(dig).hex(),
        "algoritmo": ALG_FIRMA,
        "hash": ALG_HASH,
        "conceptos": [],
    }


def verificar_firma(
    datos: bytes,
    firma_hex: str,
    ruta_pub: Optional[str] = None,
    pub_bytes: Optional[bytes] = None,
) -> Dict[str, Any]:
    try:
        pub = _cargar_pub(ruta_pub=ruta_pub, pub_bytes=pub_bytes)
    except (ValueError, Exception) as e:
        return {
            "ok": False,
            "error": str(e),
            "conceptos": ["CÓDIGO_INVÁLIDO", "FIRMA_INVÁLIDA"],
        }
    dig = nucleo_digest(datos)
    try:
        pub.verify(bytes.fromhex(firma_hex), dig)
        valida = True
    except (InvalidSignature, ValueError):
        valida = False
    return {
        "ok": valida,
        "nucleo": dig.hex(),
        "valida": valida,
        "conceptos": (
            []
            if valida
            else ["FIRMA_INVÁLIDA", "INTEGRIDAD_COMPROMETIDA", "ALTERACIÓN"]
        ),
    }


# ===============================================================
# Manifiesto canónico (lo que la firma autentica en bloque)
# ===============================================================

def construir_manifiesto(
    datos: bytes,
    firma_hex: str,
    *,
    artifact_id: str = "",
    version: str = "1.0",
    clave_publica_id: str = "",
) -> Dict[str, Any]:
    ch = canales(datos)
    return {
        "artifact_id": artifact_id,
        "version": version,
        "algoritmo_hash": ALG_HASH,
        "algoritmo_firma": ALG_FIRMA,
        "nucleo": nucleo(datos),
        "S": ch["S"],
        "Q": ch["Q"],
        "identidad_neutra": _es_neutro(datos),
        "firma": firma_hex,
        "clave_publica_id": clave_publica_id,
        "version_contrato": "1.0",
    }


def manifiesto_canonico(m: Dict[str, Any]) -> bytes:
    """Serialización estable para re-firma futura del manifiesto completo."""
    return json.dumps(m, sort_keys=True, separators=(",", ":")).encode("utf-8")


# ===============================================================
# BUILD: sellar → firmar → manifiesto
# ===============================================================

def build(
    datos: bytes,
    ruta_priv: str,
    *,
    n_neutro: int = 3,
    artifact_id: str = "",
    version: str = "1.0",
    clave_publica_id: str = "",
) -> Dict[str, Any]:
    s = sellar(datos, n=n_neutro)
    if not s.get("ok"):
        return {
            "ok": False,
            "fase": "sellar",
            "error": s.get("error"),
            "conceptos": s.get("conceptos") or ["CÓDIGO_INVÁLIDO"],
        }
    artefacto = s["datos"]
    f = firmar(artefacto, ruta_priv)
    if not f.get("ok"):
        return {
            "ok": False,
            "fase": "firmar",
            "error": "fallo al firmar",
            "conceptos": ["FIRMA_INVÁLIDA"],
        }
    man = construir_manifiesto(
        artefacto,
        f["firma"],
        artifact_id=artifact_id,
        version=version,
        clave_publica_id=clave_publica_id,
    )
    return {
        "ok": True,
        "datos": artefacto,
        "manifiesto": man,
        "firma": f["firma"],
        "nucleo": f["nucleo"],
        "conceptos": [],
    }


# ===============================================================
# RUNTIME: verificar (fail-closed en MODO_PROTEGIDO)
# ===============================================================

def verificar(
    datos: bytes,
    *,
    firma_hex: Optional[str] = None,
    ruta_pub: Optional[str] = None,
    pub_bytes: Optional[bytes] = None,
    nucleo_esperado: Optional[str] = None,
    S_esperado: Optional[str] = None,
    Q_esperado: Optional[str] = None,
    n_neutro: int = 3,
    modo: str = MODO_PROTEGIDO,
    manifiesto: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    MODO_PROTEGIDO  → sin firma válida = FAIL
    MODO_DIAGNOSTICO → firma opcional; reporta evidencia
    """
    conceptos: List[str] = []
    pasos: Dict[str, Any] = {}

    # --- Manifiesto opcional: rellena esperados si no se pasaron ---
    if manifiesto:
        firma_hex = firma_hex or manifiesto.get("firma")
        nucleo_esperado = nucleo_esperado or manifiesto.get("nucleo")
        S_esperado = S_esperado or manifiesto.get("S")
        Q_esperado = Q_esperado or manifiesto.get("Q")

    # --- FIRMA (autoridad) ---
    if modo == MODO_PROTEGIDO:
        if not firma_hex or (ruta_pub is None and pub_bytes is None):
            return {
                "herramienta": "PROTECCION",
                "ok": False,
                "modo": modo,
                "error": "firma obligatoria ausente",
                "conceptos": ["FIRMA_INVÁLIDA", "ALERTA"],
                "pasos": {},
            }
        fir = verificar_firma(
            datos, firma_hex, ruta_pub=ruta_pub, pub_bytes=pub_bytes
        )
        pasos["firma"] = fir
        conceptos.extend(fir.get("conceptos") or [])
        if not fir.get("ok"):
            return {
                "herramienta": "PROTECCION",
                "ok": False,
                "modo": modo,
                "conceptos": sorted(set(conceptos)),
                "pasos": pasos,
            }
    elif firma_hex and (ruta_pub is not None or pub_bytes is not None):
        fir = verificar_firma(
            datos, firma_hex, ruta_pub=ruta_pub, pub_bytes=pub_bytes
        )
        pasos["firma"] = fir
        conceptos.extend(fir.get("conceptos") or [])

    # --- Núcleo (integridad vs esperado independiente) ---
    h = nucleo(datos)
    pasos["nucleo"] = {"nucleo": h, "ok": True}
    if nucleo_esperado is not None:
        ok_n = h == nucleo_esperado
        pasos["nucleo"]["ok"] = ok_n
        pasos["nucleo"]["esperado"] = nucleo_esperado
        if not ok_n:
            conceptos.extend(
                ["INTEGRIDAD_COMPROMETIDA", "ALTERACIÓN", "CÓDIGO_COMPROMETIDO"]
            )

    # --- Canales (evidencia; solo si hay esperados) ---
    ch = canales(datos)
    pasos["canales"] = {**ch, "ok": True}
    if S_esperado is not None and Q_esperado is not None:
        ok_c = ch["S"] == S_esperado and ch["Q"] == Q_esperado
        pasos["canales"]["ok"] = ok_c
        if not ok_c:
            conceptos.extend(
                ["INTEGRIDAD_COMPROMETIDA", "ALTERACIÓN", "MANIPULACIÓN"]
            )

    # --- Neutro (marca de build) ---
    neu = verificar_neutro(datos, n=n_neutro)
    pasos["identidad_neutra"] = neu
    # En protegido la marca es evidencia, no autoridad; no tumba sola
    if modo == MODO_DIAGNOSTICO and not neu.get("ok"):
        conceptos.extend(neu.get("conceptos") or [])

    # --- z estructural (evidencia, no control) ---
    z = z_invariante(datos)
    pasos["z"] = z

    ok = not conceptos or (
        modo == MODO_PROTEGIDO
        and pasos.get("firma", {}).get("ok") is True
        and pasos.get("nucleo", {}).get("ok") is True
        and pasos.get("canales", {}).get("ok") is True
        and not any(
            c in conceptos
            for c in (
                "FIRMA_INVÁLIDA",
                "INTEGRIDAD_COMPROMETIDA",
                "ALTERACIÓN",
                "MANIPULACIÓN",
                "CÓDIGO_COMPROMETIDO",
            )
        )
    )
    # Recalcular ok de forma explícita
    fallos_duros = []
    if modo == MODO_PROTEGIDO:
        if not pasos.get("firma", {}).get("ok"):
            fallos_duros.append("firma")
        if nucleo_esperado is not None and not pasos["nucleo"]["ok"]:
            fallos_duros.append("nucleo")
        if (
            S_esperado is not None
            and Q_esperado is not None
            and not pasos["canales"]["ok"]
        ):
            fallos_duros.append("canales")
    else:
        if "firma" in pasos and not pasos["firma"].get("ok"):
            fallos_duros.append("firma")
        if nucleo_esperado is not None and not pasos["nucleo"]["ok"]:
            fallos_duros.append("nucleo")
        if (
            S_esperado is not None
            and Q_esperado is not None
            and not pasos["canales"]["ok"]
        ):
            fallos_duros.append("canales")

    ok = len(fallos_duros) == 0

    return {
        "herramienta": "PROTECCION",
        "ok": ok,
        "modo": modo,
        "nucleo": h,
        "conceptos": sorted(set(conceptos)),
        "fallos": fallos_duros,
        "pasos": pasos,
        "nota": (
            "Firma = autoridad. Hash/canales/z/neutro = evidencia. "
            "Clave pública requiere raíz de confianza."
        ),
    }


# ===============================================================
# API pública
# ===============================================================

__all__ = [
    "SEGURIDAD",
    "MODO_PROTEGIDO",
    "MODO_DIAGNOSTICO",
    "nucleo",
    "canales",
    "z_invariante",
    "sellar",
    "verificar_neutro",
    "generar_claves",
    "firmar",
    "verificar_firma",
    "construir_manifiesto",
    "build",
    "verificar",
]
