# ===============================================================
# modules/seguridad/proteccion.py
# PROTECCION unificada — integridad + autenticidad + evidencia
# ===============================================================
#
# BUILD (orden fijo):
#   datos → sellar → cuerpo → firmar(cuerpo) → {cuerpo, firma}
#
# RUNTIME (MODO_PROTEGIDO):
#   datos + manifiesto{cuerpo,firma} + pub → verificar()
#   Sin manifiesto = FAIL.
#
# Autoridad: firma Ed25519 sobre serializar(cuerpo).
# Evidencia: canales / z / neutro (no invalidan autorización).
#
# Clave pública: raíz de confianza externa (pin / TPM / build).
# ===============================================================

from __future__ import annotations

import hashlib
import hmac
import json
import time
from math import gcd
from pathlib import Path
from typing import Any, Dict, List, Optional

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)

# ---------------------------------------------------------------
SEGURIDAD = {
    "id": "proteccion",
    "nombre": "Protección criptográfica unificada",
    "hace": (
        "Sella el artefacto, firma el cuerpo canónico del manifiesto "
        "(Ed25519) y verifica datos contra ese cuerpo. "
        "Firma = autoridad. Hash/canales/z/neutro = evidencia."
    ),
    "herramienta": "PROTECCION",
    "version": "3.1",
    "conceptos": [
        "FIRMA_INVÁLIDA",
        "INTEGRIDAD_COMPROMETIDA",
        "CÓDIGO_COMPROMETIDO",
        "ALTERACIÓN",
        "MANIPULACIÓN",
        "AMENAZA",
        "CÓDIGO_INVÁLIDO",
        "ALERTA",
        "MANIFIESTO_AUSENTE",
        "VERSIÓN_REGRESIVA",
    ],
}

MODO_PROTEGIDO = "PROTEGIDO"
MODO_DIAGNOSTICO = "DIAGNOSTICO"
MARCA_NEUTRA = b"\n# OMEGA_NEUTRO:"
ALG_HASH = "SHA-256"
ALG_FIRMA = "Ed25519"
ESQUEMA_MANIFIESTO = 1


# ===============================================================
# Integridad
# ===============================================================

def nucleo(datos: bytes) -> str:
    return hashlib.sha256(datos).hexdigest()


def nucleo_digest(datos: bytes) -> bytes:
    return hashlib.sha256(datos).digest()


def canales(datos: bytes) -> Dict[str, Any]:
    mid = len(datos) // 2
    s, q = datos[:mid], datos[mid:]
    assert len(s) + len(q) == len(datos)
    return {
        "S": hashlib.sha256(s).hexdigest(),
        "Q": hashlib.sha256(q).hexdigest(),
        "n_S": len(s),
        "n_Q": len(q),
        "n_total": len(datos),
    }


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
    frags = _fragmentos(datos, k=k)
    vals = [_val_efectiva(hashlib.sha256(f).hexdigest()) for f in frags]
    z = vals[0]
    for v in vals[1:]:
        z = gcd(z, v)
    cubierto = sum(len(f) for f in frags)
    return {
        "z": z,
        "valuaciones": vals,
        "n_fragmentos": len(frags),
        "bytes_cubiertos": cubierto,
        "cobertura_total": cubierto == len(datos),
        "regimen": (
            "normal" if z == 1 else ("cuadrado" if z == 2 else "obstruccion")
        ),
        "nota": (
            "Evidencia estructural. No es autoridad. "
            "La autoridad es la firma del cuerpo del manifiesto."
        ),
    }


def comparar_z(
    datos: bytes, vals_esperadas: List[int], k: int = 8
) -> Dict[str, Any]:
    r = z_invariante(datos, k=k)
    coincide = r["valuaciones"] == list(vals_esperadas)
    return {
        "ok": coincide,
        "z": r["z"],
        "valuaciones": r["valuaciones"],
        "esperadas": list(vals_esperadas),
        "conceptos": (
            [] if coincide else ["ALTERACIÓN", "INTEGRIDAD_COMPROMETIDA"]
        ),
        "nota": "Diagnóstico. No invalida autorización.",
    }


# ===============================================================
# Identidad neutra (marca de BUILD)
# ===============================================================

def _es_neutro(datos: bytes, n: int) -> bool:
    if n < 2:
        return False
    return int(hashlib.sha256(datos).hexdigest(), 16) % n == 0


def sellar(
    datos: bytes,
    n: int = 3,
    max_intentos: int = 8192,
) -> Dict[str, Any]:
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
        "error": f"no se pudo sellar en {max_intentos} intentos",
        "conceptos": ["CÓDIGO_INVÁLIDO"],
    }


def verificar_neutro(datos: bytes, n: int = 3) -> Dict[str, Any]:
    if n < 2:
        return {
            "ok": False,
            "n": n,
            "neutro": False,
            "error": "n debe ser ≥ 2",
            "conceptos": ["CÓDIGO_INVÁLIDO"],
        }
    ok = _es_neutro(datos, n=n)
    return {
        "ok": ok,
        "n": n,
        "neutro": ok,
        "conceptos": (
            [] if ok else ["ALTERACIÓN", "INTEGRIDAD_COMPROMETIDA"]
        ),
        "nota": "Marca de build, no autenticación.",
    }


# ===============================================================
# Claves y Ed25519
# ===============================================================

def generar_claves(ruta_priv: str, ruta_pub: str) -> Dict[str, Any]:
    priv = Ed25519PrivateKey.generate()
    p = Path(ruta_priv)
    p.write_bytes(
        priv.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
    try:
        p.chmod(0o600)
    except OSError:
        pass
    pub_raw = priv.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    Path(ruta_pub).write_bytes(pub_raw)
    return {
        "ok": True,
        "priv": ruta_priv,
        "pub": ruta_pub,
        "pub_hex": pub_raw.hex(),
        "conceptos": [],
    }


def _cargar_priv(ruta_priv: str) -> Ed25519PrivateKey:
    return Ed25519PrivateKey.from_private_bytes(Path(ruta_priv).read_bytes())


def _cargar_pub_raw(
    ruta_pub: Optional[str] = None,
    pub_bytes: Optional[bytes] = None,
) -> Optional[bytes]:
    if pub_bytes is not None:
        return pub_bytes
    if ruta_pub is not None:
        try:
            return Path(ruta_pub).read_bytes()
        except OSError:
            return None
    return None


def firmar_bytes(mensaje: bytes, ruta_priv: str) -> Dict[str, Any]:
    try:
        priv = _cargar_priv(ruta_priv)
    except (OSError, ValueError) as e:
        return {
            "ok": False,
            "error": f"clave privada ilegible: {e}",
            "conceptos": ["CÓDIGO_INVÁLIDO"],
        }
    return {
        "ok": True,
        "firma": priv.sign(mensaje).hex(),
        "conceptos": [],
    }


def verificar_bytes(
    mensaje: bytes,
    firma_hex: str,
    ruta_pub: Optional[str] = None,
    pub_bytes: Optional[bytes] = None,
) -> Dict[str, Any]:
    raw = _cargar_pub_raw(ruta_pub=ruta_pub, pub_bytes=pub_bytes)
    if raw is None or len(raw) != 32:
        return {
            "ok": False,
            "error": "clave pública ausente o inválida",
            "conceptos": ["CÓDIGO_INVÁLIDO", "FIRMA_INVÁLIDA"],
        }
    try:
        Ed25519PublicKey.from_public_bytes(raw).verify(
            bytes.fromhex(firma_hex), mensaje
        )
        valida = True
    except (InvalidSignature, ValueError, TypeError):
        valida = False
    return {
        "ok": valida,
        "valida": valida,
        "conceptos": (
            []
            if valida
            else [
                "FIRMA_INVÁLIDA",
                "INTEGRIDAD_COMPROMETIDA",
                "ALTERACIÓN",
            ]
        ),
    }


def firmar(datos: bytes, ruta_priv: str) -> Dict[str, Any]:
    """Auxiliar: firma el digest del artefacto. Preferir build()."""
    dig = nucleo_digest(datos)
    r = firmar_bytes(dig, ruta_priv)
    if r.get("ok"):
        r["nucleo"] = dig.hex()
    return r


def verificar_firma(
    datos: bytes,
    firma_hex: str,
    ruta_pub: Optional[str] = None,
    pub_bytes: Optional[bytes] = None,
) -> Dict[str, Any]:
    dig = nucleo_digest(datos)
    r = verificar_bytes(dig, firma_hex, ruta_pub=ruta_pub, pub_bytes=pub_bytes)
    r["nucleo"] = dig.hex()
    return r


# ===============================================================
# Manifiesto: SOLO {cuerpo, firma} — sin campos planos duplicados
# ===============================================================

def serializar(cuerpo: Dict[str, Any]) -> bytes:
    return json.dumps(
        cuerpo, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")


def construir_cuerpo(
    datos: bytes,
    *,
    artifact_id: str = "",
    version: int = 1,
    clave_publica_id: str = "",
    n_neutro: int = 3,
) -> Dict[str, Any]:
    ch = canales(datos)
    z = z_invariante(datos)
    return {
        "esquema": ESQUEMA_MANIFIESTO,
        "version": int(version),
        "emitido": int(time.time()),
        "artifact_id": artifact_id,
        "clave_publica_id": clave_publica_id,
        "algoritmo_hash": ALG_HASH,
        "algoritmo_firma": ALG_FIRMA,
        "nucleo": nucleo(datos),
        "S": ch["S"],
        "Q": ch["Q"],
        "n_bytes": len(datos),
        "n_neutro": int(n_neutro),
        "valuaciones": z["valuaciones"],
        "identidad_neutra": _es_neutro(datos, n=n_neutro),
    }


def construir_manifiesto(
    datos: bytes,
    firma_hex: str,
    *,
    artifact_id: str = "",
    version: int = 1,
    clave_publica_id: str = "",
    n_neutro: int = 3,
) -> Dict[str, Any]:
    """Formato único: {cuerpo, firma}."""
    cuerpo = construir_cuerpo(
        datos,
        artifact_id=artifact_id,
        version=version,
        clave_publica_id=clave_publica_id,
        n_neutro=n_neutro,
    )
    return {"cuerpo": cuerpo, "firma": firma_hex}


def verificar_manifiesto(
    manifiesto: Optional[Dict[str, Any]],
    ruta_pub: Optional[str] = None,
    pub_bytes: Optional[bytes] = None,
    version_minima: int = 1,
) -> Dict[str, Any]:
    if not isinstance(manifiesto, dict):
        return {
            "ok": False,
            "error": "manifiesto ausente",
            "conceptos": ["MANIFIESTO_AUSENTE", "INTEGRIDAD_COMPROMETIDA"],
        }

    cuerpo = manifiesto.get("cuerpo")
    firma_hex = manifiesto.get("firma")
    if not isinstance(cuerpo, dict) or not isinstance(firma_hex, str) or not firma_hex:
        return {
            "ok": False,
            "error": "manifiesto mal formado (exige cuerpo + firma)",
            "conceptos": ["MANIFIESTO_AUSENTE", "CÓDIGO_INVÁLIDO"],
        }

    if cuerpo.get("esquema") != ESQUEMA_MANIFIESTO:
        return {
            "ok": False,
            "error": f"esquema {cuerpo.get('esquema')!r} desconocido",
            "conceptos": ["CÓDIGO_INVÁLIDO"],
        }

    f = verificar_bytes(
        serializar(cuerpo),
        firma_hex,
        ruta_pub=ruta_pub,
        pub_bytes=pub_bytes,
    )
    if not f.get("ok"):
        return {
            "ok": False,
            "error": "firma del manifiesto inválida",
            "conceptos": f.get("conceptos")
            or ["FIRMA_INVÁLIDA", "INTEGRIDAD_COMPROMETIDA"],
        }

    v = cuerpo.get("version")
    if not isinstance(v, int) or v < version_minima:
        return {
            "ok": False,
            "error": f"versión {v!r} < mínima {version_minima}",
            "version": v,
            "conceptos": ["VERSIÓN_REGRESIVA", "INTEGRIDAD_COMPROMETIDA"],
        }

    return {
        "ok": True,
        "cuerpo": cuerpo,
        "firma": firma_hex,
        "version": v,
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
    s = sellar(datos, n=n_neutro)
    if not s.get("ok"):
        return {
            "ok": False,
            "fase": "sellar",
            "error": s.get("error"),
            "conceptos": s.get("conceptos") or ["CÓDIGO_INVÁLIDO"],
        }
    artefacto = s["datos"]

    cuerpo = construir_cuerpo(
        artefacto,
        artifact_id=artifact_id,
        version=version,
        clave_publica_id=clave_publica_id,
        n_neutro=n_neutro,
    )
    f = firmar_bytes(serializar(cuerpo), ruta_priv)
    if not f.get("ok"):
        return {
            "ok": False,
            "fase": "firmar",
            "error": f.get("error") or "fallo al firmar cuerpo",
            "conceptos": f.get("conceptos") or ["FIRMA_INVÁLIDA"],
        }

    # Única representación: cuerpo + firma
    manifiesto = {"cuerpo": cuerpo, "firma": f["firma"]}
    return {
        "ok": True,
        "datos": artefacto,
        "manifiesto": manifiesto,
        "firma": f["firma"],
        "nucleo": cuerpo["nucleo"],
        "conceptos": [],
    }


# ===============================================================
# RUNTIME
# ===============================================================

def verificar(
    datos: bytes,
    *,
    ruta_pub: Optional[str] = None,
    pub_bytes: Optional[bytes] = None,
    manifiesto: Optional[Dict[str, Any]] = None,
    n_neutro: Optional[int] = None,
    modo: str = MODO_PROTEGIDO,
    version_minima: int = 1,
    # Compatibilidad residual (DIAGNOSTICO / tests de evidencia):
    firma_hex: Optional[str] = None,
    nucleo_esperado: Optional[str] = None,
    S_esperado: Optional[str] = None,
    Q_esperado: Optional[str] = None,
) -> Dict[str, Any]:
    conceptos: List[str] = []
    fallos: List[str] = []
    pasos: Dict[str, Any] = {}
    cuerpo: Optional[Dict[str, Any]] = None

    # ---------- AUTORIDAD ----------
    if modo == MODO_PROTEGIDO:
        if manifiesto is None:
            return {
                "herramienta": "PROTECCION",
                "ok": False,
                "modo": modo,
                "error": "manifiesto obligatorio en MODO_PROTEGIDO",
                "conceptos": [
                    "MANIFIESTO_AUSENTE",
                    "FIRMA_INVÁLIDA",
                    "ALERTA",
                ],
                "fallos": ["manifiesto"],
                "pasos": {},
            }

        man = verificar_manifiesto(
            manifiesto,
            ruta_pub=ruta_pub,
            pub_bytes=pub_bytes,
            version_minima=version_minima,
        )
        pasos["manifiesto"] = man
        conceptos.extend(man.get("conceptos") or [])
        if not man.get("ok"):
            fallos.append("manifiesto")
            return {
                "herramienta": "PROTECCION",
                "ok": False,
                "modo": modo,
                "conceptos": sorted(set(conceptos)),
                "fallos": fallos,
                "pasos": pasos,
                "nota": "Sin manifiesto válido no hay referencia autenticada.",
            }
        cuerpo = man["cuerpo"]
        nucleo_esperado = cuerpo["nucleo"]
        S_esperado = cuerpo["S"]
        Q_esperado = cuerpo["Q"]
        if n_neutro is None:
            n_neutro = int(cuerpo.get("n_neutro") or 3)

    else:
        # DIAGNOSTICO: manifiesto opcional; firma-digest opcional
        if manifiesto is not None:
            man = verificar_manifiesto(
                manifiesto,
                ruta_pub=ruta_pub,
                pub_bytes=pub_bytes,
                version_minima=version_minima,
            )
            pasos["manifiesto"] = man
            conceptos.extend(man.get("conceptos") or [])
            if man.get("ok"):
                cuerpo = man["cuerpo"]
                nucleo_esperado = nucleo_esperado or cuerpo.get("nucleo")
                S_esperado = S_esperado or cuerpo.get("S")
                Q_esperado = Q_esperado or cuerpo.get("Q")
                if n_neutro is None:
                    n_neutro = int(cuerpo.get("n_neutro") or 3)
            else:
                fallos.append("manifiesto")
        elif firma_hex and (ruta_pub is not None or pub_bytes is not None):
            fir = verificar_firma(
                datos, firma_hex, ruta_pub=ruta_pub, pub_bytes=pub_bytes
            )
            pasos["firma"] = fir
            conceptos.extend(fir.get("conceptos") or [])
            if not fir.get("ok"):
                fallos.append("firma")

        if n_neutro is None:
            n_neutro = 3

    # ---------- Núcleo (autoridad vía cuerpo autenticado) ----------
    h = nucleo(datos)
    pasos["nucleo"] = {"nucleo": h, "ok": True}
    if nucleo_esperado is not None:
        ok_n = hmac.compare_digest(h, str(nucleo_esperado))
        pasos["nucleo"]["ok"] = ok_n
        pasos["nucleo"]["esperado"] = nucleo_esperado
        if not ok_n:
            fallos.append("nucleo")
            conceptos.extend(
                [
                    "INTEGRIDAD_COMPROMETIDA",
                    "ALTERACIÓN",
                    "CÓDIGO_COMPROMETIDO",
                ]
            )

    # ---------- Canales (autoridad vía cuerpo autenticado) ----------
    ch = canales(datos)
    pasos["canales"] = {**ch, "ok": True}
    if S_esperado is not None and Q_esperado is not None:
        ok_c = hmac.compare_digest(
            ch["S"], str(S_esperado)
        ) and hmac.compare_digest(ch["Q"], str(Q_esperado))
        pasos["canales"]["ok"] = ok_c
        if not ok_c:
            fallos.append("canales")
            conceptos.extend(
                ["INTEGRIDAD_COMPROMETIDA", "ALTERACIÓN", "MANIPULACIÓN"]
            )

    # ---------- Neutro (EVIDENCIA — no añade fallos de autoridad) ----------
    neu = verificar_neutro(datos, n=int(n_neutro))
    pasos["identidad_neutra"] = neu
    if not neu.get("ok"):
        conceptos.extend(neu.get("conceptos") or [])

    # ---------- z (EVIDENCIA — no añade fallos de autoridad) ----------
    z = z_invariante(datos)
    pasos["z"] = z
    if cuerpo and isinstance(cuerpo.get("valuaciones"), list):
        cz = comparar_z(datos, cuerpo["valuaciones"])
        pasos["z_compare"] = cz
        if not cz.get("ok"):
            conceptos.extend(cz.get("conceptos") or [])

    ok = len(fallos) == 0
    return {
        "herramienta": "PROTECCION",
        "ok": ok,
        "modo": modo,
        "nucleo": h,
        "conceptos": sorted(set(conceptos)),
        "fallos": fallos,
        "pasos": pasos,
        "nota": (
            "Autoridad = firma del cuerpo + match nucleo/S/Q. "
            "z/neutro = evidencia (no invalidan ok). "
            "Clave pública requiere raíz de confianza externa."
        ),
    }


# ===============================================================
__all__ = [
    "SEGURIDAD",
    "MODO_PROTEGIDO",
    "MODO_DIAGNOSTICO",
    "nucleo",
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
]
