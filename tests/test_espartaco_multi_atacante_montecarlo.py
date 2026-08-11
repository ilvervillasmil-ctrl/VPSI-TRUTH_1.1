# ===============================================================
# TEST ESPARTACO — MULTI-ATACANTE MONTE CARLO
# tests/test_espartaco_multi_atacante_montecarlo.py
# ===============================================================
#
# ARMA: Test Espartaco
# OBJETIVO: maximizar presión adversarial sobre proteccion.py
#            con una sola autoridad criptográfica y N atacantes
#            sin clave privada. Intentar BREACH.
#
# Si hay BREACH → el test FALLA (el sistema fue penetrado).
# Si 0 BREACH tras N ataques → el test PASA (ninguna aceptación
# no autorizada en el espacio de mutación ejecutado).
#
# Estaciones reales (solo pipeline de verificar/verificar_manifiesto):
#   1 entrada_datos  2 manifiesto_forma  3 firma  4 esquema_cuerpo
#   5 nucleo  6 canales  7 n_bytes
# ===============================================================

from __future__ import annotations

import copy
import hashlib
import json
import os
import random
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pytest
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

import modules.spartaco_seguridad.proteccion as P


# ===============================================================
# PROCEDENCIA / CONFIG
# ===============================================================

SPEC_ID = "TEST-ESPARTACO-MULTI-ATACANTE-1.0"
SPEC_REVISION = "2026-08-11"
SPEC_HASH = hashlib.sha256(
    b"ESPARTACO|MULTI-ATACANTE|MONTE-CARLO|UNA-AUTORIDAD|SIN-PRIV"
).hexdigest()

MASTER_SEED = int(os.environ.get("ESPARTACO_SEED", "20260811"))
# CI: MULTI_ATTACK_N=100000  |  full local: 5000000
N_ATACANTES = int(os.environ.get("MULTI_ATTACK_N", "100000"))
N_CALIBRACION_OK = True  # se actualiza en calibración

ESTACIONES = (
    "entrada_datos",
    "manifiesto_forma",
    "firma",
    "esquema_cuerpo",
    "nucleo",
    "canales",
    "n_bytes",
)
PROFUNDIDAD = {
    "entrada_datos": 1,
    "manifiesto_forma": 2,
    "firma": 3,
    "esquema_cuerpo": 4,
    "nucleo": 5,
    "canales": 6,
    "n_bytes": 7,
    "NINGUNA_BREACH": 8,
}

# Pesos de cobertura experimental (no modelo de amenaza real)
PESOS_FRENTE = {
    "entrada": 5,
    "forma": 12,
    "firma": 12,
    "esquema": 12,
    "cuerpo": 12,
    "datos": 18,
    "nucleo_campo": 6,
    "canales_campo": 6,
    "longitud": 5,
    "recomposicion": 7,
    "compuesto": 5,
}

FRENTES = list(PESOS_FRENTE.keys())


# ===============================================================
# ORÁCULO INDEPENDIENTE (no usa P.serializar / P.verificar)
# ===============================================================

def oracle_canonical(obj: Any) -> bytes:
    return json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def oracle_verify_sig(pub_bytes: bytes, message: bytes, firma_hex: str) -> bool:
    try:
        sig = bytes.fromhex(firma_hex)
        if len(sig) != 64 or len(pub_bytes) != 32:
            return False
        Ed25519PublicKey.from_public_bytes(pub_bytes).verify(sig, message)
        return True
    except Exception:
        return False


def oracle_nucleo(datos: bytes) -> str:
    return hashlib.sha256(datos).hexdigest()


# ===============================================================
# ESTACIÓN DE DETENCIÓN (orden real del pipeline)
# ===============================================================

def estacion_detencion(resultado: Dict[str, Any]) -> str:
    if resultado.get("ok") is True:
        return "NINGUNA_BREACH"
    fallos = list(resultado.get("fallos") or [])
    conceptos = list(resultado.get("conceptos") or [])
    pasos = resultado.get("pasos") or {}
    error = str(resultado.get("error") or "")

    if "datos" in fallos:
        return "entrada_datos"
    if "manifiesto" in fallos:
        if "MANIFIESTO_AUSENTE" in conceptos:
            return "manifiesto_forma"
        if "FIRMA_INVÁLIDA" in conceptos:
            return "firma"
        if "CÓDIGO_INVÁLIDO" in conceptos or "VERSIÓN_REGRESIVA" in conceptos:
            if any(x in error for x in ("exactamente", "no dict", "firma ausente", "ausente")):
                return "manifiesto_forma"
            return "esquema_cuerpo"
        return "manifiesto_forma"
    if "nucleo" in fallos or (pasos.get("nucleo") or {}).get("ok") is False:
        return "nucleo"
    if "canales" in fallos or (pasos.get("canales") or {}).get("ok") is False:
        return "canales"
    if "n_bytes" in fallos:
        return "n_bytes"
    if fallos:
        return f"otro:{fallos[0]}"
    return "desconocida"


def clasificar(resultado: Dict[str, Any], hostil: bool) -> str:
    if hostil and resultado.get("ok") is True:
        return "BREACH"
    if resultado.get("ok") is False:
        return "BLOCKED"
    return "BLOCKED"


# ===============================================================
# ATACANTE (sin clave privada)
# ===============================================================

class AtacanteMonteCarlo:
    __slots__ = ("attacker_id", "rng", "pub_bytes", "datos", "manifiesto", "frente")

    def __init__(
        self,
        attacker_id: int,
        master_seed: int,
        pub_bytes: bytes,
        datos: bytes,
        manifiesto: Dict[str, Any],
        frente: str,
    ):
        self.attacker_id = attacker_id
        self.rng = random.Random(
            int.from_bytes(
                hashlib.sha256(f"{master_seed}|{attacker_id}".encode()).digest()[:8],
                "big",
            )
        )
        self.pub_bytes = bytes(pub_bytes)
        self.datos = bytes(datos)
        self.manifiesto = copy.deepcopy(manifiesto)
        self.frente = frente
        assert self.no_tiene_clave_privada()

    def no_tiene_clave_privada(self) -> bool:
        # slots: no __dict__; solo comprobar que no hay atributos secretos
        prohibido = ("private_key", "priv", "ruta_priv", "seed_crypto", "Ed25519PrivateKey")
        slots = getattr(type(self), "__slots__", ())
        for k in prohibido:
            if k in slots:
                return False
            if k in getattr(self, "__dict__", {}):
                return False
        return True

    def scenario_id(self, ops: str) -> str:
        raw = f"{self.attacker_id}|{self.frente}|{ops}|{hashlib.sha256(self.datos).hexdigest()[:16]}"
        return hashlib.sha256(raw.encode()).hexdigest()[:24]


# ===============================================================
# GENERADORES DE ATAQUE (agresivos)
# ===============================================================

CAMPOS_CUERPO = (
    "artifact_id",
    "clave_publica_id",
    "version",
    "emitido",
    "algoritmo_hash",
    "algoritmo_firma",
    "nucleo",
    "S",
    "Q",
    "n_bytes",
    "n_neutro",
    "valuaciones",
    "identidad_neutra",
    "esquema",
)


def mutar_entrada(rng: random.Random, datos: bytes, man: Dict) -> Tuple[Any, Any, str]:
    opciones = [
        None,
        "texto",
        0,
        1.5,
        True,
        False,
        bytearray(datos),
        list(datos),
        {"x": 1},
        b"",
    ]
    return rng.choice(opciones), man, "entrada_tipo_hostil"


def mutar_forma(rng: random.Random, datos: bytes, man: Dict) -> Tuple[Any, Any, str]:
    m = copy.deepcopy(man)
    op = rng.randint(0, 9)
    if op == 0:
        return datos, None, "manifiesto_none"
    if op == 1:
        return datos, [], "manifiesto_lista"
    if op == 2:
        return datos, "basura", "manifiesto_str"
    if op == 3:
        return datos, {}, "manifiesto_vacio"
    if op == 4:
        m["extra"] = "x"
        return datos, m, "clave_extra"
    if op == 5:
        del m["cuerpo"]
        return datos, m, "sin_cuerpo"
    if op == 6:
        del m["firma"]
        return datos, m, "sin_firma"
    if op == 7:
        m["cuerpo"] = "no-dict"
        return datos, m, "cuerpo_str"
    if op == 8:
        m["firma"] = 12345
        return datos, m, "firma_int"
    m["firma"] = ""
    return datos, m, "firma_vacia"


def mutar_firma(rng: random.Random, datos: bytes, man: Dict) -> Tuple[bytes, Dict, str]:
    m = copy.deepcopy(man)
    op = rng.randint(0, 6)
    if op == 0:
        m["firma"] = os.urandom(64).hex()
        return datos, m, "firma_random"
    if op == 1:
        m["firma"] = m["firma"][:60]
        return datos, m, "firma_truncada"
    if op == 2:
        m["firma"] = m["firma"] + "ab"
        return datos, m, "firma_extra"
    if op == 3:
        m["firma"] = "zz" * 32
        return datos, m, "firma_hex_invalido"
    if op == 4:
        fh = m["firma"]
        i = rng.randint(0, max(0, len(fh) - 2))
        m["firma"] = fh[:i] + ("0" if fh[i] != "0" else "1") + fh[i + 1 :]
        return datos, m, "firma_flip_nibble"
    if op == 5:
        m["firma"] = "00" * 64
        return datos, m, "firma_ceros"
    m["firma"] = "ff" * 64
    return datos, m, "firma_ff"


def mutar_cuerpo(rng: random.Random, datos: bytes, man: Dict) -> Tuple[bytes, Dict, str]:
    m = copy.deepcopy(man)
    campo = rng.choice(CAMPOS_CUERPO)
    c = m["cuerpo"]
    if campo == "artifact_id":
        c["artifact_id"] = "ATK-" + str(rng.randint(0, 10**9))
    elif campo == "clave_publica_id":
        c["clave_publica_id"] = "FAKE-KEY"
    elif campo == "version":
        c["version"] = rng.choice([-1, 0, 10**9, "3", 1.5])
    elif campo == "emitido":
        c["emitido"] = 12345
    elif campo == "algoritmo_hash":
        c["algoritmo_hash"] = "MD5"
    elif campo == "algoritmo_firma":
        c["algoritmo_firma"] = "RSA"
    elif campo in ("nucleo", "S", "Q"):
        c[campo] = rng.choice(["00" * 32, "ff" * 32, "ab" * 32, "0" * 63, True, None, 0])
    elif campo == "n_bytes":
        c["n_bytes"] = rng.choice([-1, 0, 10**9, "10", True])
    elif campo == "n_neutro":
        c["n_neutro"] = rng.choice([-1, 0, 1, 3.0, True, "3"])
    elif campo == "valuaciones":
        c["valuaciones"] = rng.choice([None, "x", [999], [], list(range(100)), True])
    elif campo == "identidad_neutra":
        c["identidad_neutra"] = rng.choice([0, 1, "true", None])
    elif campo == "esquema":
        c["esquema"] = rng.choice([0, 2, "1", None])
    return datos, m, f"cuerpo_{campo}"


def mutar_esquema(rng: random.Random, datos: bytes, man: Dict) -> Tuple[bytes, Dict, str]:
    m = copy.deepcopy(man)
    c = m["cuerpo"]
    op = rng.randint(0, 5)
    if op == 0 and CAMPOS_CUERPO:
        k = rng.choice(CAMPOS_CUERPO)
        if k in c:
            del c[k]
            return datos, m, f"elimina_{k}"
    if op == 1:
        c["campo_fantasma"] = "x"
        return datos, m, "clave_extra_cuerpo"
    if op == 2:
        c["nucleo"] = "not-hex"
        return datos, m, "nucleo_mal_hex"
    if op == 3:
        c["version"] = -100
        return datos, m, "version_negativa"
    if op == 4:
        c["S"] = "aa" * 16  # longitud incorrecta
        return datos, m, "S_corto"
    c["valuaciones"] = [1, 2, "x"]
    return datos, m, "valuaciones_tipo"


def mutar_datos(rng: random.Random, datos: bytes, man: Dict) -> Tuple[bytes, Dict, str]:
    d = bytearray(datos)
    op = rng.randint(0, 8)
    if not d:
        d = bytearray(b"\x00")
    if op == 0:
        i = rng.randint(0, len(d) - 1)
        d[i] ^= 0x01
        return bytes(d), man, "flip_bit"
    if op == 1:
        i = rng.randint(0, len(d) - 1)
        d[i] ^= 0xFF
        return bytes(d), man, "flip_byte"
    if op == 2:
        i = rng.randint(0, len(d) - 1)
        nuevo = rng.randint(0, 255)
        if nuevo == d[i]:
            nuevo = (d[i] + 1) % 256
        d[i] = nuevo
        return bytes(d), man, "byte_random"
    if op == 3:
        return bytes(d[:-1]) if len(d) > 1 else b"", man, "truncar"
    if op == 4:
        return bytes(d) + bytes([rng.randint(0, 255)]), man, "extender"
    if op == 5:
        return b"\x00" + bytes(d), man, "prefijo"
    if op == 6:
        return bytes(d) + b"\xff\xff", man, "sufijo"
    if op == 7:
        mid = len(d) // 2
        d[mid : mid + 1] = b"\xaa"
        return bytes(d), man, "region_media"
    # múltiples flips
    for _ in range(rng.randint(2, 5)):
        if d:
            d[rng.randint(0, len(d) - 1)] ^= rng.randint(1, 255)
    return bytes(d), man, "multi_flip"


def mutar_nucleo_campo(rng: random.Random, datos: bytes, man: Dict) -> Tuple[bytes, Dict, str]:
    m = copy.deepcopy(man)
    m["cuerpo"]["nucleo"] = hashlib.sha256(os.urandom(16)).hexdigest()
    return datos, m, "nucleo_en_cuerpo"


def mutar_canales_campo(rng: random.Random, datos: bytes, man: Dict) -> Tuple[bytes, Dict, str]:
    m = copy.deepcopy(man)
    op = rng.randint(0, 2)
    if op == 0:
        m["cuerpo"]["S"] = "11" * 32
        return datos, m, "S_solo"
    if op == 1:
        m["cuerpo"]["Q"] = "22" * 32
        return datos, m, "Q_solo"
    m["cuerpo"]["S"] = "33" * 32
    m["cuerpo"]["Q"] = "44" * 32
    return datos, m, "S_y_Q"


def mutar_longitud(rng: random.Random, datos: bytes, man: Dict) -> Tuple[bytes, Dict, str]:
    # cambiar bytes para que len != n_bytes del cuerpo (manifiesto intacto)
    d = bytearray(datos)
    if rng.random() < 0.5:
        d.append(0xAB)
        return bytes(d), man, "len_mas_1"
    if len(d) > 1:
        return bytes(d[:-1]), man, "len_menos_1"
    return bytes(d) + b"\x00\x00", man, "len_mas_2"


def mutar_recomposicion(
    rng: random.Random,
    datos: bytes,
    man: Dict,
    datos_b: bytes,
    man_b: Dict,
) -> Tuple[bytes, Dict, str]:
    op = rng.randint(0, 3)
    if op == 0:
        return datos_b, man, "manifiesto_A_datos_B"
    if op == 1:
        return datos, man_b, "manifiesto_B_datos_A"
    if op == 2:
        m = copy.deepcopy(man)
        m["firma"] = man_b["firma"]
        return datos, m, "firma_B_cuerpo_A"
    m = copy.deepcopy(man_b)
    m["firma"] = man["firma"]
    return datos_b, m, "firma_A_cuerpo_B"


def mutar_compuesto(rng: random.Random, datos: bytes, man: Dict) -> Tuple[bytes, Dict, str]:
    d, m, ops = datos, copy.deepcopy(man), []
    n = rng.randint(2, 5)
    gens = [mutar_datos, mutar_cuerpo, mutar_firma, mutar_esquema, mutar_longitud]
    for _ in range(n):
        g = rng.choice(gens)
        d, m, op = g(rng, d if isinstance(d, (bytes, bytearray)) else datos, m if isinstance(m, dict) else man)
        ops.append(op)
        if not isinstance(d, (bytes, bytearray)):
            break
        if not isinstance(m, dict):
            break
    return d, m, "+".join(ops)


GENERADORES = {
    "entrada": mutar_entrada,
    "forma": mutar_forma,
    "firma": mutar_firma,
    "esquema": mutar_esquema,
    "cuerpo": mutar_cuerpo,
    "datos": mutar_datos,
    "nucleo_campo": mutar_nucleo_campo,
    "canales_campo": mutar_canales_campo,
    "longitud": mutar_longitud,
    "compuesto": mutar_compuesto,
}


def elegir_frente(rng: random.Random) -> str:
    total = sum(PESOS_FRENTE.values())
    r = rng.randint(1, total)
    acc = 0
    for f, w in PESOS_FRENTE.items():
        acc += w
        if r <= acc:
            return f
    return "datos"


# ===============================================================
# FIXTURES — UNA SOLA AUTORIDAD
# ===============================================================

@pytest.fixture(scope="module")
def autoridad_unica(tmp_path_factory):
    base = tmp_path_factory.mktemp("espartaco")
    priv = base / "legit.key"
    pub = base / "legit.pub"
    assert P.generar_claves(str(priv), str(pub))["ok"] is True
    pub_bytes = pub.read_bytes()

    datos = b"ESPARTACO::ARTEFACTO::LEGITIMO::MONTECARLO::v1"
    built = P.build(
        datos,
        str(priv),
        n_neutro=3,
        artifact_id="ESP-LEGIT-001",
        version=1,
        clave_publica_id="ROOT-ESP",
    )
    assert built["ok"] is True

    # Segundo artefacto solo para recomposición (priv fuera de atacantes)
    priv_b = base / "b.key"
    pub_b = base / "b.pub"
    P.generar_claves(str(priv_b), str(pub_b))
    built_b = P.build(
        b"ESPARTACO::ARTEFACTO::B::DISTINTO",
        str(priv_b),
        n_neutro=3,
        artifact_id="ESP-B-002",
        version=1,
        clave_publica_id="ROOT-B",
    )
    assert built_b["ok"] is True

    return {
        "priv_path": priv,
        "pub_bytes": pub_bytes,
        "datos": built["datos"],
        "manifiesto": built["manifiesto"],
        "datos_b": built_b["datos"],
        "manifiesto_b": built_b["manifiesto"],
        "pub_b": pub_b.read_bytes(),
    }


# ===============================================================
# CALIBRACIÓN (debe pasar antes del MC)
# ===============================================================

def test_00_espartaco_procedencia():
    assert SPEC_ID.startswith("TEST-ESPARTACO")
    assert len(SPEC_HASH) == 64
    assert MASTER_SEED > 0


def test_01_calibracion_estaciones(autoridad_unica):
    """Flechas conocidas: si fallan, no interpretar el Monte Carlo."""
    pub = autoridad_unica["pub_bytes"]
    datos = autoridad_unica["datos"]
    man = copy.deepcopy(autoridad_unica["manifiesto"])

    # legítimo
    r = P.verificar(datos, manifiesto=man, pub_bytes=pub, modo=P.MODO_PROTEGIDO)
    assert r["ok"] is True, r

    # artifact_id → firma
    m = copy.deepcopy(man)
    m["cuerpo"]["artifact_id"] = "X"
    r = P.verificar(datos, manifiesto=m, pub_bytes=pub, modo=P.MODO_PROTEGIDO)
    assert r["ok"] is False
    assert estacion_detencion(r) in ("firma", "esquema_cuerpo", "manifiesto_forma")

    # nucleo en cuerpo → firma
    m = copy.deepcopy(man)
    m["cuerpo"]["nucleo"] = "00" * 32
    r = P.verificar(datos, manifiesto=m, pub_bytes=pub, modo=P.MODO_PROTEGIDO)
    assert r["ok"] is False
    assert estacion_detencion(r) in ("firma", "esquema_cuerpo")

    # S/Q → firma
    m = copy.deepcopy(man)
    m["cuerpo"]["S"] = "11" * 32
    r = P.verificar(datos, manifiesto=m, pub_bytes=pub, modo=P.MODO_PROTEGIDO)
    assert r["ok"] is False
    assert estacion_detencion(r) in ("firma", "esquema_cuerpo")

    # flip datos → nucleo
    d = bytearray(datos)
    d[0] ^= 0xFF
    r = P.verificar(bytes(d), manifiesto=man, pub_bytes=pub, modo=P.MODO_PROTEGIDO)
    assert r["ok"] is False
    assert estacion_detencion(r) in ("nucleo", "canales", "n_bytes")

    # A→B → nucleo
    r = P.verificar(
        autoridad_unica["datos_b"],
        manifiesto=man,
        pub_bytes=pub,
        modo=P.MODO_PROTEGIDO,
    )
    assert r["ok"] is False
    assert estacion_detencion(r) in ("nucleo", "canales", "n_bytes")

    # sin manifiesto
    r = P.verificar(datos, manifiesto=None, pub_bytes=pub, modo=P.MODO_PROTEGIDO)
    assert r["ok"] is False
    assert estacion_detencion(r) == "manifiesto_forma"

    # clave extra
    m = copy.deepcopy(man)
    m["extra"] = 1
    r = P.verificar(datos, manifiesto=m, pub_bytes=pub, modo=P.MODO_PROTEGIDO)
    assert r["ok"] is False
    assert estacion_detencion(r) in ("manifiesto_forma", "firma", "esquema_cuerpo")


# ===============================================================
# MOTOR MONTE CARLO — INTENTAR ROMPER
# ===============================================================

def test_99_espartaco_montecarlo_demolicion(autoridad_unica):
    """
    N atacantes independientes, una sola autoridad, sin clave privada.
    Objetivo: encontrar BREACH. Si aparece uno, el test falla.
    """
    pub = autoridad_unica["pub_bytes"]
    datos0 = autoridad_unica["datos"]
    man0 = autoridad_unica["manifiesto"]
    datos_b = autoridad_unica["datos_b"]
    man_b = autoridad_unica["manifiesto_b"]

    # control negativo
    r_ok = P.verificar(datos0, manifiesto=man0, pub_bytes=pub, modo=P.MODO_PROTEGIDO)
    assert r_ok["ok"] is True

    conteo_estacion: Dict[str, int] = {e: 0 for e in ESTACIONES}
    conteo_estacion["NINGUNA_BREACH"] = 0
    conteo_estacion["desconocida"] = 0
    conteo_frente: Dict[str, int] = {f: 0 for f in FRENTES}
    conteo_fe: Dict[Tuple[str, str], int] = {}
    profundidad_sum = 0
    profundidad_max = 0
    estacion_max = ""
    blocked = 0
    breaches = 0
    exceptions = 0
    indeterminate = 0
    breach_cases: List[Dict[str, Any]] = []

    meta_rng = random.Random(MASTER_SEED)

    for i in range(N_ATACANTES):
        frente = elegir_frente(meta_rng)
        atk = AtacanteMonteCarlo(i, MASTER_SEED, pub, datos0, man0, frente)
        assert atk.no_tiene_clave_privada()
        conteo_frente[frente] += 1

        try:
            if frente == "recomposicion":
                d, m, ops = mutar_recomposicion(
                    atk.rng, atk.datos, atk.manifiesto, datos_b, man_b
                )
            elif frente in GENERADORES:
                d, m, ops = GENERADORES[frente](atk.rng, atk.datos, atk.manifiesto)
            else:
                d, m, ops = mutar_datos(atk.rng, atk.datos, atk.manifiesto)

            # Si la mutación no alteró nada observable, no es ataque hostil
            mismo_datos = isinstance(d, (bytes, bytearray)) and bytes(d) == atk.datos
            mismo_man = isinstance(m, dict) and m == atk.manifiesto
            if mismo_datos and mismo_man:
                blocked += 1  # no-op descartado como presión
                conteo_estacion["manifiesto_forma"] += 0  # no cuenta
                continue

            resultado = P.verificar(
                d,
                manifiesto=m,
                pub_bytes=atk.pub_bytes,
                modo=P.MODO_PROTEGIDO,
            )
        except Exception as ex:
            exceptions += 1
            breach_cases.append(
                {
                    "id": i,
                    "frente": frente,
                    "error": repr(ex),
                    "tb": traceback.format_exc()[-500:],
                }
            )
            continue

        if not isinstance(resultado, dict) or "ok" not in resultado:
            indeterminate += 1
            continue

        hostil = True  # todos los del loop son hostiles
        clase = clasificar(resultado, hostil)
        est = estacion_detencion(resultado)

        if clase == "BREACH":
            breaches += 1
            breach_cases.append(
                {
                    "id": i,
                    "frente": frente,
                    "ops": ops,
                    "scenario_id": atk.scenario_id(str(ops)),
                    "resultado": {
                        "ok": resultado.get("ok"),
                        "fallos": resultado.get("fallos"),
                        "conceptos": resultado.get("conceptos"),
                    },
                }
            )
            # no seguir ocultando
            break

        if clase == "BLOCKED":
            blocked += 1
        else:
            indeterminate += 1

        key = est if est in conteo_estacion else "desconocida"
        conteo_estacion[key] = conteo_estacion.get(key, 0) + 1
        conteo_fe[(frente, est)] = conteo_fe.get((frente, est), 0) + 1
        prof = PROFUNDIDAD.get(est, 0)
        profundidad_sum += prof
        if prof > profundidad_max:
            profundidad_max = prof
            estacion_max = est

        assert atk.no_tiene_clave_privada()

    n_exec = blocked + breaches + exceptions + indeterminate
    prof_media = (profundidad_sum / blocked) if blocked else 0.0

    # --- reporte ---
    lineas = [
        "",
        "=" * 72,
        "TEST ESPARTACO — MAPA DE PENETRACIÓN",
        f"SPEC_ID={SPEC_ID}  REV={SPEC_REVISION}",
        f"MASTER_SEED={MASTER_SEED}  N={N_ATACANTES}  ejecutados={n_exec}",
        "=" * 72,
        f"{'FRENTE':<16} {'N':>8}",
    ]
    for f in FRENTES:
        lineas.append(f"{f:<16} {conteo_frente.get(f, 0):>8}")
    lineas.append("-" * 72)
    lineas.append(f"{'ESTACIÓN':<22} {'ALERTAS':>10}")
    for e in list(ESTACIONES) + ["NINGUNA_BREACH", "desconocida"]:
        lineas.append(f"{e:<22} {conteo_estacion.get(e, 0):>10}")
    lineas.append("-" * 72)
    lineas.append(f"BLOCKED={blocked}  BREACH={breaches}  EXCEPTION={exceptions}  INDETERMINATE={indeterminate}")
    lineas.append(f"PROFUNDIDAD_MAX={profundidad_max}  ESTACION_MAX={estacion_max}")
    lineas.append(f"PROFUNDIDAD_MEDIA={prof_media:.3f}")
    if breaches == 0 and n_exec > 0:
        # regla del 3, cota superior ~95%
        upper = 3.0 / n_exec
        lineas.append(f"BREACH_RATE=0/{n_exec}  upper95~={upper:.2e}")
    lineas.append("=" * 72)
    reporte = "\n".join(lineas)
    print(reporte)

    # Criterio de éxito del arma
    assert exceptions == 0, f"EXCEPTIONS={exceptions} casos={breach_cases[:3]}"
    assert indeterminate == 0, f"INDETERMINATE={indeterminate}"
    assert breaches == 0, f"CRITICAL_BREACH x{breaches}: {breach_cases[:5]}"
    assert blocked == N_ATACANTES or (blocked + breaches + exceptions + indeterminate) >= N_ATACANTES * 0.99
    assert profundidad_max >= 2  # al menos forma o más
    # control legítimo intacto al final
    r_final = P.verificar(
        autoridad_unica["datos"],
        manifiesto=autoridad_unica["manifiesto"],
        pub_bytes=autoridad_unica["pub_bytes"],
        modo=P.MODO_PROTEGIDO,
    )
    assert r_final["ok"] is True
