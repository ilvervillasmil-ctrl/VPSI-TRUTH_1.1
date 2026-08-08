# ===============================================================
# tests/test_proteccion_adversarial_demolicion.py
# VPSI-TRUTH — PROTECCION — batería unificada adversarial + demolición
#
# Cadena atacada:
# MANIFIESTO -> FORMA -> CUERPO -> CANONICALIZACIÓN -> ED25519
# -> IDENTIDAD -> NUCLEO/S/Q -> EVIDENCIA -> VEREDICTO
#
# Regla:
#   - Alteración de autoridad => rechazo.
#   - Referencia externa => nunca sustituye al cuerpo firmado.
#   - Artefacto alterado => nunca se salva con z/neutro/referencias.
#   - Entrada hostil => no debe producir crash no controlado.
#   - verificar() => no debe mutar la evidencia recibida.
#
# Se fusionan las dos baterías originales y se eliminan pruebas
# duplicadas o que imponían políticas no declaradas por el API actual
# (p. ej. expiración temporal/revocación externa).
# ===============================================================

from __future__ import annotations

import copy
import json
import threading
import time
from pathlib import Path

import pytest

from modules.spartaco_seguridad.proteccion import (
    ESQUEMA_MANIFIESTO,
    MODO_DIAGNOSTICO,
    MODO_PROTEGIDO,
    _fragmentos,
    build,
    firmar_bytes,
    generar_claves,
    nucleo,
    serializar,
    sellar,
    verificar,
    verificar_bytes,
    verificar_manifiesto,
    verificar_neutro,
)


# ===============================================================
# HELPERS
# ===============================================================

def blindado(fn, *args, **kwargs):
    """Ejecuta una entrada hostil: una excepción no controlada cuenta como fallo."""
    try:
        resultado = fn(*args, **kwargs)
    except Exception as exc:  # noqa: BLE001
        return False, exc

    if isinstance(resultado, dict):
        return bool(resultado.get("ok")), None

    return bool(resultado), None


def exige_rechazo_limpio(fn, *args, **kwargs):
    ok, exc = blindado(fn, *args, **kwargs)
    assert exc is None, (
        f"CRASH en lugar de rechazo: {type(exc).__name__}: {exc}"
    )
    assert ok is False


def remanifestar(cuerpo, priv):
    """Re-firma un cuerpo mutado: simula atacante con la clave legítima."""
    f = firmar_bytes(serializar(cuerpo), str(priv))
    assert f["ok"] is True
    return {"cuerpo": cuerpo, "firma": f["firma"]}


class DictMalo(dict):
    pass


class DictMutante(dict):
    """Cambia un campo después de la primera lectura."""

    def __init__(self, base, campo, malo):
        super().__init__(base)
        self.campo = campo
        self.malo = malo
        self.lecturas = 0

    def get(self, key, default=None):
        if key == self.campo:
            self.lecturas += 1
            if self.lecturas > 1:
                return self.malo
        return super().get(key, default)

    def __getitem__(self, key):
        if key == self.campo:
            self.lecturas += 1
            if self.lecturas > 1:
                return self.malo
        return super().__getitem__(key)


class SiempreIgual:
    """Ataca validaciones que dependan de == en vez de datos tipados/canónicos."""

    def __eq__(self, other):
        return True

    def __hash__(self):
        return 0

    def __str__(self):
        return "0" * 64


# ===============================================================
# FIXTURES
# ===============================================================

@pytest.fixture
def claves(tmp_path: Path):
    priv = tmp_path / "omega.key"
    pub = tmp_path / "omega.pub"

    r = generar_claves(str(priv), str(pub))

    assert r["ok"] is True
    assert priv.is_file()
    assert pub.is_file()
    assert len(pub.read_bytes()) == 32

    return priv, pub, pub.read_bytes()


@pytest.fixture
def build_valido(claves):
    priv, _, pub_bytes = claves

    datos = (
        b"VPSI-TRUTH::ARTEFACTO::ORIGINAL::"
        b"0123456789ABCDEF::SEGURIDAD"
    )

    r = build(
        datos,
        str(priv),
        n_neutro=3,
        artifact_id="TEST-001",
        version=3,
        clave_publica_id="OMEGA-ROOT-01",
    )

    assert r["ok"] is True
    assert set(r["manifiesto"]) == {"cuerpo", "firma"}
    assert isinstance(r["manifiesto"]["cuerpo"], dict)
    assert isinstance(r["manifiesto"]["firma"], str)
    assert r["manifiesto"]["firma"]
    assert r["manifiesto"]["cuerpo"]["n_neutro"] == 3
    assert r["manifiesto"]["cuerpo"]["esquema"] == ESQUEMA_MANIFIESTO

    return r, pub_bytes


CAMPOS_CUERPO = [
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
]

TIPOS_ADVERSARIOS = [
    True, False,
    0, 1, -1,
    1.0, 3.0, -0.0,
    float("inf"), float("-inf"), float("nan"),
    "", "3", "1", "0", "True",
    [], {}, None,
    b"3", (3,), {3},
]

HASH_HOSTIL = [
    123, None, True,
    b"\x00" * 32,
    ["a"], {"a": 1},
    "ñ" * 64, "\u00e9" * 64,
    "0" * 63, "0" * 65,
    "ZZ" * 32, " " * 64,
    "\x00" * 64, "0" * 64 + "\n",
]


# ===============================================================
# 1. CAMINO FELIZ / CONTRATO BÁSICO
# ===============================================================

def test_build_protegido_valido(build_valido):
    r, pub = build_valido
    v = verificar(
        r["datos"], manifiesto=r["manifiesto"],
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )
    assert v["ok"] is True
    assert v["fallos"] == []
    assert v["pasos"]["manifiesto"]["ok"] is True
    assert v["pasos"]["nucleo"]["ok"] is True
    assert v["pasos"]["canales"]["ok"] is True


def test_build_formato_unico(build_valido):
    r, _ = build_valido
    m = r["manifiesto"]
    assert set(m) == {"cuerpo", "firma"}
    assert isinstance(m["cuerpo"], dict)
    assert isinstance(m["firma"], str) and m["firma"]


def test_build_sella_y_cambia_bytes(claves):
    priv, _, _ = claves
    original = b"DATOS-SIN-SELLAR"
    r = build(original, str(priv), n_neutro=3)
    assert r["ok"] is True
    assert r["datos"] != original


def test_firma_build_es_del_cuerpo(build_valido):
    r, pub = build_valido
    v = verificar_bytes(
        serializar(r["manifiesto"]["cuerpo"]),
        r["manifiesto"]["firma"],
        pub_bytes=pub,
    )
    assert v["ok"] is True


def test_firma_cuerpo_no_valida_digest_artefacto(build_valido):
    r, pub = build_valido
    digest = bytes.fromhex(r["manifiesto"]["cuerpo"]["nucleo"])
    assert verificar_bytes(
        digest, r["manifiesto"]["firma"], pub_bytes=pub
    )["ok"] is False


# ===============================================================
# 2. FAIL-CLOSED
# ===============================================================

def test_protegido_sin_manifiesto_falla(build_valido):
    r, pub = build_valido
    v = verificar(r["datos"], pub_bytes=pub, modo=MODO_PROTEGIDO)
    assert v["ok"] is False
    assert "manifiesto" in v["fallos"]
    assert "MANIFIESTO_AUSENTE" in v["conceptos"]


def test_protegido_none_falla(build_valido):
    r, pub = build_valido
    v = verificar(
        r["datos"], manifiesto=None,
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )
    assert v["ok"] is False
    assert "manifiesto" in v["fallos"]


@pytest.mark.parametrize(
    "manifiesto",
    [
        {}, {"firma": "00"}, {"cuerpo": {}},
        {"cuerpo": {}, "firma": ""},
        {"cuerpo": "x", "firma": "00"},
        {"cuerpo": {}, "firma": None},
        {"cuerpo": None, "firma": "00"},
        {"cuerpo": [], "firma": "00"},
        {"cuerpo": {}, "firma": []},
        {"cuerpo": {}, "firma": 0},
        {"cuerpo": 1, "firma": "ab"},
        [], "texto", 123, b"bytes", True, False,
        0.0, float("nan"),
    ],
)
def test_protegido_manifiesto_basura_falla(build_valido, manifiesto):
    r, pub = build_valido
    v = verificar(
        r["datos"], manifiesto=manifiesto,
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )
    assert v["ok"] is False


def test_protegido_sin_clave_publica_falla(build_valido):
    r, _ = build_valido
    v = verificar(
        r["datos"], manifiesto=r["manifiesto"],
        modo=MODO_PROTEGIDO,
    )
    assert v["ok"] is False
    assert "manifiesto" in v["fallos"]
    assert "FIRMA_INVÁLIDA" in v["conceptos"]


def test_firma_hex_suelta_no_bypassea(build_valido):
    r, pub = build_valido
    v = verificar(
        r["datos"],
        firma_hex=r["manifiesto"]["firma"],
        pub_bytes=pub,
        modo=MODO_PROTEGIDO,
    )
    assert v["ok"] is False
    assert "manifiesto" in v["fallos"]


@pytest.mark.parametrize(
    "man",
    [None, {}, {"cuerpo": {}}, {"firma": "00"},
     {"cuerpo": None}, {"firma": None}],
)
def test_fail_closed_casos_minimos(build_valido, man):
    r, pub = build_valido
    assert verificar(
        r["datos"], manifiesto=man,
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )["ok"] is False


# ===============================================================
# 3. FORMA ESTRICTA
# ===============================================================

@pytest.mark.parametrize(
    "extra_key,extra_val",
    [
        ("campo_extra", "X"),
        ("firma_extra", "00" * 64),
        ("cuerpo_extra", {"a": 1}),
        ("nucleo", "00" * 32),
        ("version", 1), ("S", "00"), ("Q", "00"),
        ("", ""), ("cuerpo ", {}), ("firma ", "x"),
        ("Cuerpo", {}), ("FIRMA", "x"), ("cuerpo\x00", {}),
    ],
)
def test_clave_extra_rechazada(
    build_valido, extra_key, extra_val
):
    r, pub = build_valido
    m = copy.deepcopy(r["manifiesto"])
    m[extra_key] = extra_val

    assert verificar_manifiesto(m, pub_bytes=pub)["ok"] is False

    v = verificar(
        r["datos"], manifiesto=m,
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )
    assert v["ok"] is False
    assert "manifiesto" in v["fallos"]


def test_campo_plano_rechazado(build_valido):
    r, pub = build_valido
    m = copy.deepcopy(r["manifiesto"])
    m["artifact_id"] = "PLANO"
    assert verificar_manifiesto(m, pub_bytes=pub)["ok"] is False
    assert verificar(
        r["datos"], manifiesto=m,
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )["ok"] is False


def test_solo_cuerpo_falla(build_valido):
    r, pub = build_valido
    assert verificar(
        r["datos"],
        manifiesto={"cuerpo": r["manifiesto"]["cuerpo"]},
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )["ok"] is False


def test_solo_firma_falla(build_valido):
    r, pub = build_valido
    assert verificar(
        r["datos"],
        manifiesto={"firma": r["manifiesto"]["firma"]},
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )["ok"] is False


def test_dict_subclass_no_crashea(build_valido):
    r, pub = build_valido
    m = DictMalo(
        cuerpo=r["manifiesto"]["cuerpo"],
        firma=r["manifiesto"]["firma"],
    )
    ok, exc = blindado(
        verificar, r["datos"],
        manifiesto=m, pub_bytes=pub,
        modo=MODO_PROTEGIDO,
    )
    assert exc is None
    assert isinstance(ok, bool)


# ===============================================================
# 4. MUTACIÓN / BORRADO DEL CUERPO
# ===============================================================

@pytest.mark.parametrize("campo", CAMPOS_CUERPO)
def test_mutar_campo_cuerpo_rompe(build_valido, campo):
    r, pub = build_valido
    m = copy.deepcopy(r["manifiesto"])
    original = m["cuerpo"][campo]

    if isinstance(original, bool):
        m["cuerpo"][campo] = not original
    elif isinstance(original, int):
        m["cuerpo"][campo] = original + 7919
    elif isinstance(original, list):
        m["cuerpo"][campo] = list(original) + [-1]
    elif isinstance(original, str):
        m["cuerpo"][campo] = original + "|ATAQUE"
    else:
        m["cuerpo"][campo] = "ATAQUE"

    v = verificar(
        r["datos"], manifiesto=m,
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )
    assert v["ok"] is False
    assert "manifiesto" in v["fallos"]


@pytest.mark.parametrize("campo", CAMPOS_CUERPO)
def test_borrar_campo_cuerpo_rompe(build_valido, campo):
    r, pub = build_valido
    cuerpo = copy.deepcopy(r["manifiesto"]["cuerpo"])
    del cuerpo[campo]

    v = verificar(
        r["datos"],
        manifiesto={"cuerpo": cuerpo,
                    "firma": r["manifiesto"]["firma"]},
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )
    assert v["ok"] is False


def test_cuerpo_vacio_falla(build_valido):
    r, pub = build_valido
    assert verificar(
        r["datos"],
        manifiesto={"cuerpo": {},
                    "firma": r["manifiesto"]["firma"]},
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )["ok"] is False


def test_firma_otro_cuerpo_no_reutilizable(build_valido, claves):
    r, _ = build_valido
    priv, _, pub = claves

    otro = copy.deepcopy(r["manifiesto"]["cuerpo"])
    otro["artifact_id"] = "OTRO-ID"
    f = firmar_bytes(serializar(otro), str(priv))
    assert f["ok"] is True

    v = verificar(
        r["datos"],
        manifiesto={
            "cuerpo": r["manifiesto"]["cuerpo"],
            "firma": f["firma"],
        },
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )
    assert v["ok"] is False


def test_trasplante_firma_A_sobre_cuerpo_B(claves):
    priv, _, pub = claves
    a = {"esquema": 1, "version": 1, "artifact_id": "A"}
    b = {"esquema": 1, "version": 1, "artifact_id": "B"}

    fa = firmar_bytes(serializar(a), str(priv))
    assert fa["ok"] is True

    assert verificar_bytes(
        serializar(b), fa["firma"], pub_bytes=pub
    )["ok"] is False


# ===============================================================
# 5. ARTEFACTO / INTEGRIDAD
# ===============================================================

def test_flip_byte_0(build_valido):
    r, pub = build_valido
    d = bytearray(r["datos"])
    d[0] ^= 0x01

    v = verificar(
        bytes(d), manifiesto=r["manifiesto"],
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )

    assert v["ok"] is False
    assert "nucleo" in v["fallos"]
    assert "canales" in v["fallos"]
    assert "INTEGRIDAD_COMPROMETIDA" in v["conceptos"]


def test_flip_mitad(build_valido):
    r, pub = build_valido
    d = bytearray(r["datos"])
    d[len(d) // 2] ^= 0x80

    v = verificar(
        bytes(d), manifiesto=r["manifiesto"],
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )

    assert v["ok"] is False
    assert "nucleo" in v["fallos"]


def test_append_byte(build_valido):
    r, pub = build_valido
    v = verificar(
        r["datos"] + b"\x00",
        manifiesto=r["manifiesto"],
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )
    assert v["ok"] is False
    assert "nucleo" in v["fallos"]


def test_pop_byte(build_valido):
    r, pub = build_valido
    v = verificar(
        r["datos"][:-1],
        manifiesto=r["manifiesto"],
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )
    assert v["ok"] is False
    assert "nucleo" in v["fallos"]


@pytest.mark.parametrize("pos", [0, 1, 2, -3, -2, -1])
def test_flip_en_borde(build_valido, pos):
    r, pub = build_valido
    d = bytearray(r["datos"])
    d[pos] ^= 0xFF

    v = verificar(
        bytes(d), manifiesto=r["manifiesto"],
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )
    assert v["ok"] is False
    assert "nucleo" in v["fallos"]


def test_flip_posiciones_criticas(build_valido):
    r, pub = build_valido
    n = len(r["datos"])

    for pos in {
        0, min(1, n - 1), n // 4, n // 2,
        (3 * n) // 4, max(0, n - 2), n - 1,
    }:
        d = bytearray(r["datos"])
        d[pos] ^= 0xFF

        v = verificar(
            bytes(d), manifiesto=r["manifiesto"],
            pub_bytes=pub, modo=MODO_PROTEGIDO,
        )
        assert v["ok"] is False, f"byte {pos} no detectado"
        assert "nucleo" in v["fallos"]


def test_manifiesto_no_autentica_artefacto_B(build_valido):
    r, pub = build_valido
    v = verificar(
        r["datos"] + b"::B",
        manifiesto=r["manifiesto"],
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )
    assert v["ok"] is False
    assert "nucleo" in v["fallos"]


def test_dos_builds_no_cruzan_autorizacion(claves):
    priv, _, pub = claves

    a = build(b"ARTEFACTO-A", str(priv),
              artifact_id="A", version=1)
    b = build(b"ARTEFACTO-B", str(priv),
              artifact_id="B", version=1)

    assert a["ok"] and b["ok"]

    assert verificar(
        a["datos"], manifiesto=a["manifiesto"],
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )["ok"]

    assert verificar(
        b["datos"], manifiesto=b["manifiesto"],
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )["ok"]

    cruz = verificar(
        a["datos"], manifiesto=b["manifiesto"],
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )
    assert cruz["ok"] is False
    assert "nucleo" in cruz["fallos"]


# ===============================================================
# 6. FIRMA / PARSING / MALEABILIDAD
# ===============================================================

def test_firma_alterada_un_nibble(build_valido):
    r, pub = build_valido
    firma = r["manifiesto"]["firma"]
    alterada = ("0" if firma[0] != "0" else "1") + firma[1:]

    m = copy.deepcopy(r["manifiesto"])
    m["firma"] = alterada

    v = verificar(
        r["datos"], manifiesto=m,
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )
    assert v["ok"] is False
    assert "manifiesto" in v["fallos"]
    assert "FIRMA_INVÁLIDA" in v["conceptos"]


@pytest.mark.parametrize(
    "firma",
    [
        "", "00", "zz", "0" * 128,
        "a" * 130, "a", "deadbeef", "gg",
        " " * 64, "\x00",
        "0x" + "00" * 64,
        "\n" + "00" * 64,
        "00 " * 64,
    ],
)
def test_firma_malformada(build_valido, firma):
    r, pub = build_valido
    m = copy.deepcopy(r["manifiesto"])
    m["firma"] = firma

    ok, exc = blindado(
        verificar,
        r["datos"], manifiesto=m,
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )
    assert exc is None
    assert ok is False


@pytest.mark.parametrize(
    "firma",
    [
        b"00" * 64, bytearray(b"0" * 128),
        0, None, [], {}, 1.5, True,
    ],
)
def test_firma_tipo_no_str(build_valido, firma):
    r, pub = build_valido
    m = {
        "cuerpo": r["manifiesto"]["cuerpo"],
        "firma": firma,
    }

    ok, exc = blindado(
        verificar,
        r["datos"], manifiesto=m,
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )
    assert exc is None
    assert ok is False


def test_mutar_cada_par_hex_firma(build_valido):
    r, pub = build_valido
    firma = r["manifiesto"]["firma"]

    for i in range(0, min(len(firma), 128), 2):
        chars = list(firma)
        chars[i] = "0" if chars[i] != "0" else "1"

        m = copy.deepcopy(r["manifiesto"])
        m["firma"] = "".join(chars)

        v = verificar(
            r["datos"], manifiesto=m,
            pub_bytes=pub, modo=MODO_PROTEGIDO,
        )
        assert v["ok"] is False, f"nibble {i} no invalidó"


def test_firma_maleable_S_mas_L(build_valido):
    """
    Ed25519: una codificación no canónica de S no debe convertirse
    en una firma aceptada.
    """
    r, pub = build_valido

    L = (
        2 ** 252
        + 27742317777372353535851937790883648493
    )

    raw = bytes.fromhex(r["manifiesto"]["firma"])
    R = raw[:32]
    S = int.from_bytes(raw[32:], "little")
    S_mal = S + L

    if S_mal >= 2 ** 256:
        pytest.skip("S+L no cabe en 32 bytes")

    mal = R + S_mal.to_bytes(32, "little")

    m = {
        "cuerpo": r["manifiesto"]["cuerpo"],
        "firma": mal.hex(),
    }

    ok, exc = blindado(
        verificar,
        r["datos"], manifiesto=m,
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )
    assert exc is None
    assert ok is False


# ===============================================================
# 7. CLAVE PÚBLICA
# ===============================================================

@pytest.mark.parametrize(
    "pub",
    [
        b"", b"x", b"x" * 31, b"x" * 33,
        b"\x00" * 32, b"\xff" * 32, bytes(range(32)),
    ],
)
def test_clave_publica_invalida(build_valido, pub):
    r, _ = build_valido
    v = verificar(
        r["datos"], manifiesto=r["manifiesto"],
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )
    assert v["ok"] is False
    assert (
        "FIRMA_INVÁLIDA" in v["conceptos"]
        or "CÓDIGO_INVÁLIDO" in v["conceptos"]
    )


def test_clave_atacante_no_valida(build_valido, tmp_path):
    r, _ = build_valido
    priv = tmp_path / "atk.key"
    pub = tmp_path / "atk.pub"

    generar_claves(str(priv), str(pub))

    v = verificar(
        r["datos"], manifiesto=r["manifiesto"],
        pub_bytes=pub.read_bytes(),
        modo=MODO_PROTEGIDO,
    )
    assert v["ok"] is False
    assert "FIRMA_INVÁLIDA" in v["conceptos"]


@pytest.mark.parametrize(
    "pub",
    [None, "", "abc", 0, [], {}, 1.5, True, bytearray(32)],
)
def test_pub_bytes_tipo_hostil_no_crashea(build_valido, pub):
    r, _ = build_valido
    ok, exc = blindado(
        verificar,
        r["datos"], manifiesto=r["manifiesto"],
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )
    assert exc is None
    assert ok is False


def test_firmar_clave_inexistente_falla(tmp_path):
    r = firmar_bytes(
        b"msg", str(tmp_path / "no.key")
    )
    assert r["ok"] is False
    assert "CÓDIGO_INVÁLIDO" in r["conceptos"]


def test_firmar_clave_basura_falla(tmp_path):
    p = tmp_path / "fake.key"
    p.write_bytes(b"no-es-ed25519-seed-valida!!!!!")

    ok, exc = blindado(
        firmar_bytes, b"msg", str(p)
    )
    assert exc is None
    assert ok is False


# ===============================================================
# 8. CANONICALIZACIÓN / SERIALIZACIÓN
# ===============================================================

def test_reordenar_claves_no_rompe(build_valido):
    r, pub = build_valido
    cuerpo = r["manifiesto"]["cuerpo"]

    inverso = {
        k: cuerpo[k] for k in reversed(list(cuerpo))
    }

    assert serializar(cuerpo) == serializar(inverso)

    v = verificar(
        r["datos"],
        manifiesto={
            "cuerpo": inverso,
            "firma": r["manifiesto"]["firma"],
        },
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )
    assert v["ok"] is True


def test_serializar_determinista(build_valido):
    r, _ = build_valido
    c = r["manifiesto"]["cuerpo"]
    assert serializar(c) == serializar(
        dict(reversed(list(c.items())))
    )


def test_cambio_semantico_cambia_serializacion(build_valido):
    r, _ = build_valido
    c = copy.deepcopy(r["manifiesto"]["cuerpo"])
    antes = serializar(c)
    c["artifact_id"] = "CAMBIO"
    assert antes != serializar(c)


@pytest.mark.parametrize(
    "a,b",
    [
        ("café", "cafe\u0301"),
        ("A", "\u0410"),
        ("ID", "I\u200bD"),
        ("x", "x\ufeff"),
        ("x", "x "),
    ],
)
def test_formas_textuales_distintas_no_colisionan(a, b):
    assert serializar({"artifact_id": a}) != serializar(
        {"artifact_id": b}
    )


def test_serializar_claves_mixtas_no_acepta_silenciosamente():
    ok, exc = blindado(
        serializar, {1: "a", "b": 2}
    )
    assert exc is None or isinstance(
        exc, (TypeError, ValueError)
    )


def test_serializar_referencia_circular_no_cuelga():
    c = {"esquema": 1}
    c["yo"] = c

    t0 = time.monotonic()
    ok, exc = blindado(serializar, c)

    assert time.monotonic() - t0 < 5
    assert exc is None or isinstance(
        exc, (ValueError, RecursionError)
    )


def test_serializar_surrogate_no_cuelga():
    ok, exc = blindado(
        serializar,
        {"esquema": 1, "artifact_id": "\ud800"},
    )
    assert exc is None or isinstance(
        exc, (UnicodeEncodeError, ValueError, TypeError)
    )


def test_serializar_anidamiento_profundo_no_cuelga():
    c = {"esquema": 1}
    nodo = c

    for _ in range(2000):
        nodo["n"] = {}
        nodo = nodo["n"]

    t0 = time.monotonic()
    ok, exc = blindado(serializar, c)

    assert time.monotonic() - t0 < 5
    assert exc is None or isinstance(
        exc, (RecursionError, ValueError)
    )


def test_roundtrip_json_no_cambia_veredicto(build_valido):
    r, pub = build_valido
    vuelta = json.loads(json.dumps(r["manifiesto"]))

    v = verificar(
        r["datos"], manifiesto=vuelta,
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )
    assert v["ok"] is True


def test_inyeccion_string_no_escapa(build_valido):
    r, pub = build_valido
    m = copy.deepcopy(r["manifiesto"])
    ataque = '","firma":"deadbeef","x":"'
    m["cuerpo"]["artifact_id"] = ataque

    vuelta = json.loads(json.dumps(m))
    assert vuelta["cuerpo"]["artifact_id"] == ataque

    v = verificar(
        r["datos"], manifiesto=vuelta,
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )
    assert v["ok"] is False


# ===============================================================
# 9. VERSIÓN / ESQUEMA
# ===============================================================

def test_version_regresiva_rechazada(build_valido, claves):
    r, _ = build_valido
    priv, _, pub = claves

    c = copy.deepcopy(r["manifiesto"]["cuerpo"])
    c["version"] = 0
    f = firmar_bytes(serializar(c), str(priv))
    assert f["ok"] is True

    vm = verificar_manifiesto(
        {"cuerpo": c, "firma": f["firma"]},
        pub_bytes=pub, version_minima=1,
    )
    assert vm["ok"] is False
    assert "VERSIÓN_REGRESIVA" in vm["conceptos"]


def test_version_alta_aceptada(build_valido, claves):
    r, _ = build_valido
    priv, _, pub = claves

    c = copy.deepcopy(r["manifiesto"]["cuerpo"])
    c["version"] = 999
    f = firmar_bytes(serializar(c), str(priv))
    assert f["ok"] is True

    vm = verificar_manifiesto(
        {"cuerpo": c, "firma": f["firma"]},
        pub_bytes=pub, version_minima=1,
    )
    assert vm["ok"] is True


def test_esquema_incompatible_falla(build_valido):
    r, pub = build_valido
    m = copy.deepcopy(r["manifiesto"])
    m["cuerpo"]["esquema"] = 999

    v = verificar(
        r["datos"], manifiesto=m,
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )
    assert v["ok"] is False
    assert "manifiesto" in v["fallos"]


def test_esquema_firmado_pero_no_autorizado(build_valido, claves):
    r, _ = build_valido
    priv, _, pub = claves

    c = copy.deepcopy(r["manifiesto"]["cuerpo"])
    c["esquema"] = ESQUEMA_MANIFIESTO + 1
    f = firmar_bytes(serializar(c), str(priv))
    assert f["ok"] is True

    vm = verificar_manifiesto(
        {"cuerpo": c, "firma": f["firma"]},
        pub_bytes=pub,
    )
    assert vm["ok"] is False


# ===============================================================
# 10. n_neutro — EL CUERPO MANDA
# ===============================================================

def test_n_neutro_externo_no_pisa_cuerpo(build_valido):
    r, pub = build_valido

    v = verificar(
        r["datos"], manifiesto=r["manifiesto"],
        pub_bytes=pub, n_neutro=999,
        modo=MODO_PROTEGIDO,
    )

    assert (
        v["pasos"]["identidad_neutra"]["n"]
        == r["manifiesto"]["cuerpo"]["n_neutro"]
    )


def test_n_neutro_cuerpo_conservado(build_valido):
    r, pub = build_valido
    esperado = r["manifiesto"]["cuerpo"]["n_neutro"]

    v = verificar(
        r["datos"], manifiesto=r["manifiesto"],
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )
    assert v["pasos"]["identidad_neutra"]["n"] == esperado


def test_mutar_n_neutro_rompe(build_valido):
    r, pub = build_valido
    m = copy.deepcopy(r["manifiesto"])
    m["cuerpo"]["n_neutro"] = 999

    v = verificar(
        r["datos"], manifiesto=m,
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )
    assert v["ok"] is False
    assert "manifiesto" in v["fallos"]


@pytest.mark.parametrize("n", [-100, -1, 0, 1])
def test_sellar_n_invalido(n):
    r = sellar(b"datos", n=n)
    assert r["ok"] is False
    assert "CÓDIGO_INVÁLIDO" in r["conceptos"]


@pytest.mark.parametrize("n", [-1, 0, 1])
def test_verificar_neutro_n_invalido(n):
    r = verificar_neutro(b"x", n=n)
    assert r["ok"] is False
    assert "CÓDIGO_INVÁLIDO" in r["conceptos"]


@pytest.mark.parametrize(
    "n", [None, "3", 1.5, True, False, [], {}, 10 ** 20]
)
def test_sellar_n_hostil_no_crashea(n):
    ok, exc = blindado(sellar, b"datos", n=n)
    assert exc is None
    assert ok is False


# ===============================================================
# 11. z / NEUTRO = EVIDENCIA
# ===============================================================

def test_z_no_en_fallos(build_valido):
    r, pub = build_valido
    v = verificar(
        r["datos"], manifiesto=r["manifiesto"],
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )
    assert "z" in v["pasos"]
    assert "z" not in v["fallos"]


def test_neutro_no_en_fallos(build_valido):
    r, pub = build_valido
    v = verificar(
        r["datos"], manifiesto=r["manifiesto"],
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )
    assert "identidad_neutra" in v["pasos"]
    assert "identidad_neutra" not in v["fallos"]


def test_mutar_valuaciones_rompe_firma(build_valido):
    r, pub = build_valido
    m = copy.deepcopy(r["manifiesto"])
    m["cuerpo"]["valuaciones"] = [999999]

    v = verificar(
        r["datos"], manifiesto=m,
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )
    assert v["ok"] is False
    assert "manifiesto" in v["fallos"]


# ===============================================================
# 12. DIAGNÓSTICO
# ===============================================================

def test_diagnostico_sin_manifiesto_ok(build_valido):
    r, _ = build_valido
    assert verificar(
        r["datos"], modo=MODO_DIAGNOSTICO
    )["ok"] is True


def test_diagnostico_manifiesto_valido(build_valido):
    r, pub = build_valido
    assert verificar(
        r["datos"], manifiesto=r["manifiesto"],
        pub_bytes=pub, modo=MODO_DIAGNOSTICO,
    )["ok"] is True


def test_diagnostico_detecta_manifiesto_falso(build_valido):
    r, pub = build_valido
    m = copy.deepcopy(r["manifiesto"])
    m["cuerpo"]["artifact_id"] = "ATACANTE"

    v = verificar(
        r["datos"], manifiesto=m,
        pub_bytes=pub, modo=MODO_DIAGNOSTICO,
    )
    assert v["ok"] is False
    assert "manifiesto" in v["fallos"]


# ===============================================================
# 13. FRAGMENTOS
# ===============================================================

@pytest.mark.parametrize(
    "n",
    list(range(80)) + [
        81, 97, 99, 100, 101, 127, 128, 129,
        255, 256, 257, 512, 1024,
    ],
)
def test_fragmentos_cobertura_exacta(n):
    datos = bytes(i % 256 for i in range(n))
    frags = _fragmentos(datos, k=8)

    assert b"".join(frags) == datos
    assert sum(len(f) for f in frags) == len(datos)


@pytest.mark.parametrize(
    "k", [1, 2, 3, 4, 5, 7, 8, 9, 16, 32, 64, 1000, 100000]
)
def test_fragmentos_varios_k(k):
    datos = b"0123456789" * 37
    assert b"".join(_fragmentos(datos, k=k)) == datos


@pytest.mark.parametrize(
    "k", [None, "8", 1.5, True, [], {}, 0, -1, -8]
)
def test_fragmentos_k_hostil_no_cuelga(k):
    t0 = time.monotonic()
    ok, exc = blindado(_fragmentos, b"abc", k=k)
    assert time.monotonic() - t0 < 5
    assert exc is None or isinstance(
        exc, (TypeError, ValueError, ZeroDivisionError)
    )


# ===============================================================
# 14. API CRIPTO DIRECTA
# ===============================================================

def test_firmar_verificar_bytes(claves):
    priv, _, pub = claves
    f = firmar_bytes(b"mensaje protegido", str(priv))
    assert f["ok"] is True

    assert verificar_bytes(
        b"mensaje protegido",
        f["firma"],
        pub_bytes=pub,
    )["ok"] is True


def test_firma_no_reutilizable_otro_mensaje(claves):
    priv, _, pub = claves
    f = firmar_bytes(b"A", str(priv))
    assert f["ok"] is True

    assert verificar_bytes(
        b"B", f["firma"], pub_bytes=pub
    )["ok"] is False


@pytest.mark.parametrize(
    "datos",
    [None, "texto", 0, 1.5, True, [], {}, bytearray(b"abc")]
)
def test_firmar_datos_hostiles_no_crashea(claves, datos):
    priv, _, _ = claves
    ok, exc = blindado(
        firmar_bytes, datos, str(priv)
    )
    assert exc is None


@pytest.mark.parametrize(
    "firma",
    [None, "", 0, True, [], {}, b"\x00" * 64,
     bytearray(64), "zz"]
)
def test_verificar_firma_hostil_no_crashea(claves, firma):
    _, _, pub = claves
    ok, exc = blindado(
        verificar_bytes, b"mensaje",
        firma, pub_bytes=pub,
    )
    assert exc is None
    assert ok is False


# ===============================================================
# 15. REFERENCIAS EXTERNAS — NUNCA TOMAN AUTORIDAD
# ===============================================================

def test_nucleo_S_Q_externos_ignorados(build_valido):
    r, pub = build_valido
    v = verificar(
        r["datos"], manifiesto=r["manifiesto"],
        pub_bytes=pub,
        nucleo_esperado="00" * 32,
        S_esperado="00" * 32,
        Q_esperado="00" * 32,
        modo=MODO_PROTEGIDO,
    )
    assert v["ok"] is True


def test_cuatro_referencias_externas_simultaneas(build_valido):
    r, pub = build_valido
    cuerpo = r["manifiesto"]["cuerpo"]

    v = verificar(
        r["datos"], manifiesto=r["manifiesto"],
        pub_bytes=pub,
        nucleo_esperado="AA" * 32,
        S_esperado="BB" * 32,
        Q_esperado="CC" * 32,
        n_neutro=999999,
        modo=MODO_PROTEGIDO,
    )

    assert v["ok"] is True
    assert (
        v["pasos"]["identidad_neutra"]["n"]
        == cuerpo["n_neutro"]
    )


def test_externos_no_salvan_artefacto_roto(build_valido):
    r, pub = build_valido

    d = bytearray(r["datos"])
    d[0] ^= 1
    roto = bytes(d)

    v = verificar(
        roto,
        manifiesto=r["manifiesto"],
        pub_bytes=pub,
        nucleo_esperado=nucleo(roto),
        S_esperado="00" * 32,
        Q_esperado="00" * 32,
        n_neutro=3,
        modo=MODO_PROTEGIDO,
    )

    assert v["ok"] is False
    assert "nucleo" in v["fallos"]


# ===============================================================
# 16. ALGORITMOS / IDENTIDAD / LONGITUD
# ===============================================================

@pytest.mark.parametrize(
    "campo,valor",
    [
        ("algoritmo_hash", "MD5"),
        ("algoritmo_firma", "RSA"),
        ("artifact_id", "OTRO"),
        ("clave_publica_id", "CLAVE-ATACANTE"),
    ],
)
def test_identidad_algoritmo_mutado_rompe(
    build_valido, campo, valor
):
    r, pub = build_valido
    m = copy.deepcopy(r["manifiesto"])
    m["cuerpo"][campo] = valor

    v = verificar(
        r["datos"], manifiesto=m,
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )
    assert v["ok"] is False


def test_n_bytes_mutado_rompe(build_valido):
    r, pub = build_valido
    m = copy.deepcopy(r["manifiesto"])
    m["cuerpo"]["n_bytes"] += 1

    v = verificar(
        r["datos"], manifiesto=m,
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )
    assert v["ok"] is False
    assert "manifiesto" in v["fallos"]


# ===============================================================
# 17. TIPOS ADVERSARIALES
# ===============================================================

@pytest.mark.parametrize("valor", TIPOS_ADVERSARIOS)
def test_n_neutro_tipo_adversarial(build_valido, valor):
    r, pub = build_valido

    if valor == r["manifiesto"]["cuerpo"]["n_neutro"]:
        pytest.skip("mismo valor legítimo")

    m = copy.deepcopy(r["manifiesto"])
    m["cuerpo"]["n_neutro"] = valor

    v = verificar(
        r["datos"], manifiesto=m,
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )
    assert v["ok"] is False


@pytest.mark.parametrize(
    "campo,valor",
    [
        ("nucleo", True), ("nucleo", 0), ("nucleo", None),
        ("nucleo", []), ("nucleo", {}),
        ("S", True), ("S", 0), ("S", None), ("S", []),
        ("Q", False), ("Q", {}), ("Q", None),
        ("artifact_id", True), ("artifact_id", 0),
        ("artifact_id", None),
        ("identidad_neutra", 0), ("identidad_neutra", 1),
        ("identidad_neutra", "True"),
        ("identidad_neutra", None),
        ("n_bytes", True), ("n_bytes", False),
        ("n_bytes", 1.5), ("n_bytes", "10"),
        ("n_bytes", None),
    ],
)
def test_campo_cuerpo_tipo_adversarial(
    build_valido, campo, valor
):
    r, pub = build_valido
    m = copy.deepcopy(r["manifiesto"])
    m["cuerpo"][campo] = valor

    v = verificar(
        r["datos"], manifiesto=m,
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )
    assert v["ok"] is False


@pytest.mark.parametrize("campo", ["nucleo", "S", "Q"])
@pytest.mark.parametrize("valor", HASH_HOSTIL)
def test_hash_hostil_no_crashea(
    build_valido, claves, campo, valor
):
    r, _ = build_valido
    priv, _, pub = claves

    c = copy.deepcopy(r["manifiesto"]["cuerpo"])
    c[campo] = valor

    ok, exc = blindado(
        firmar_bytes, serializar(c), str(priv)
    )
    if exc is not None or not ok:
        return

    f = firmar_bytes(serializar(c), str(priv))
    ok, exc = blindado(
        verificar,
        r["datos"],
        manifiesto={"cuerpo": c, "firma": f["firma"]},
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )

    assert exc is None
    assert ok is False


@pytest.mark.parametrize(
    "valor",
    [
        None, "abc", 1, {"a": 1},
        [None], ["x"], [1.5], [True],
        [-1], [10 ** 40], list(range(100000)),
    ],
)
def test_valuaciones_hostiles_no_crashean(
    build_valido, claves, valor
):
    r, _ = build_valido
    priv, _, pub = claves

    c = copy.deepcopy(r["manifiesto"]["cuerpo"])
    c["valuaciones"] = valor

    ok, exc = blindado(
        firmar_bytes, serializar(c), str(priv)
    )
    if exc is not None or not ok:
        return

    f = firmar_bytes(serializar(c), str(priv))
    ok, exc = blindado(
        verificar,
        r["datos"],
        manifiesto={"cuerpo": c, "firma": f["firma"]},
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )

    assert exc is None
    assert ok is False


# ===============================================================
# 18. MUTACIÓN PROFUNDA / ALIASING
# ===============================================================

def test_valuaciones_elemento_mutado_rompe(build_valido):
    r, pub = build_valido
    m = copy.deepcopy(r["manifiesto"])
    vals = m["cuerpo"]["valuaciones"]

    assert isinstance(vals, list) and vals
    original = copy.deepcopy(vals)

    vals[0] = "ATAQUE"
    assert vals != original

    v = verificar(
        r["datos"], manifiesto=m,
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )
    assert v["ok"] is False


def test_valuaciones_append_rompe(build_valido):
    r, pub = build_valido
    m = copy.deepcopy(r["manifiesto"])
    m["cuerpo"]["valuaciones"] = (
        list(m["cuerpo"]["valuaciones"]) + [0]
    )

    assert verificar(
        r["datos"], manifiesto=m,
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )["ok"] is False


def test_valuaciones_pop_rompe(build_valido):
    r, pub = build_valido
    m = copy.deepcopy(r["manifiesto"])
    vals = list(m["cuerpo"]["valuaciones"])

    if not vals:
        pytest.skip("sin valuaciones")

    vals.pop()
    m["cuerpo"]["valuaciones"] = vals

    assert verificar(
        r["datos"], manifiesto=m,
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )["ok"] is False


def test_mutacion_posterior_no_recalcula_firma(build_valido):
    r, pub = build_valido
    m = r["manifiesto"]
    firma_original = m["firma"]

    m["cuerpo"]["artifact_id"] = "ATAQUE"

    assert m["firma"] == firma_original

    v = verificar(
        r["datos"], manifiesto=m,
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )
    assert v["ok"] is False


def test_verificar_no_muta_manifiesto(build_valido):
    r, pub = build_valido
    m = copy.deepcopy(r["manifiesto"])
    antes = copy.deepcopy(m)

    verificar(
        r["datos"], manifiesto=m,
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )

    assert m == antes


def test_verificar_no_muta_manifiesto_rechazado(build_valido):
    r, pub = build_valido
    m = copy.deepcopy(r["manifiesto"])
    m["cuerpo"]["artifact_id"] = "X"
    antes = copy.deepcopy(m)

    verificar(
        r["datos"], manifiesto=m,
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )

    assert m == antes


# ===============================================================
# 19. TOCTOU / MAPPINGS HOSTILES
# ===============================================================

@pytest.mark.parametrize(
    "campo",
    ["version", "nucleo", "S", "Q", "n_neutro", "esquema"],
)
def test_toctou_no_debe_producir_aceptacion(
    build_valido, campo
):
    r, pub = build_valido

    mutante = DictMutante(
        r["manifiesto"]["cuerpo"],
        campo,
        "MALO",
    )

    m = {
        "cuerpo": mutante,
        "firma": r["manifiesto"]["firma"],
    }

    ok, exc = blindado(
        verificar,
        r["datos"], manifiesto=m,
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )

    assert exc is None
    if ok:
        assert mutante.lecturas <= 1, (
            f"TOCTOU potencial en {campo}: "
            f"{mutante.lecturas} lecturas"
        )


@pytest.mark.parametrize("campo", ["nucleo", "S", "Q"])
def test_objeto_eq_siempre_true_no_pasa(
    build_valido, claves, campo
):
    r, _ = build_valido
    priv, _, pub = claves

    c = dict(r["manifiesto"]["cuerpo"])
    c[campo] = SiempreIgual()

    ok, exc = blindado(
        firmar_bytes, serializar(c), str(priv)
    )
    if exc is not None or not ok:
        return

    f = firmar_bytes(serializar(c), str(priv))
    ok, exc = blindado(
        verificar,
        r["datos"],
        manifiesto={"cuerpo": c, "firma": f["firma"]},
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )

    assert exc is None
    assert ok is False


# ===============================================================
# 20. SELLADO / RESELLADO
# ===============================================================

def test_sellar_n_grande_no_cuelga():
    t0 = time.monotonic()
    ok, exc = blindado(
        sellar, b"datos", n=2 ** 40
    )
    assert exc is None
    assert time.monotonic() - t0 < 10


def test_sellar_idempotencia_veredicto():
    s1 = sellar(b"payload", n=3)
    assert s1["ok"] is True

    s2 = sellar(s1["datos"], n=3)
    assert s2["ok"] is True

    assert verificar_neutro(
        s2["datos"], n=3
    )["ok"] is True


def test_resellado_no_salva_autorizacion(claves):
    priv, _, pub = claves

    original = build(
        b"ORIGINAL", str(priv), n_neutro=3
    )
    assert original["ok"] is True

    d = bytearray(original["datos"])
    d[0] ^= 0xFF

    regrindado = sellar(bytes(d), n=3)
    assert regrindado["ok"] is True
    assert verificar_neutro(
        regrindado["datos"], n=3
    )["ok"] is True

    v = verificar(
        regrindado["datos"],
        manifiesto=original["manifiesto"],
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )

    assert v["ok"] is False
    assert "nucleo" in v["fallos"]


# ===============================================================
# 21. DATOS EXTREMOS / DoS
# ===============================================================

@pytest.mark.parametrize(
    "datos",
    [
        b"", b"\x00", b"\xff", b"X", b"AB",
        b"A" * 3, b"A" * 7, b"A" * 8, b"A" * 9,
        b"A" * 100, b"A" * 1000, b"A" * 10000,
        bytes(range(256)),
        b"\x00" * 4096,
        b"\xff" * 4096,
    ],
)
def test_datos_extremos_build_y_verify(claves, datos):
    priv, _, pub = claves

    r = build(
        datos, str(priv),
        n_neutro=3, artifact_id="EDGE", version=1,
    )
    assert r["ok"] is True

    v = verificar(
        r["datos"], manifiesto=r["manifiesto"],
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )
    assert v["ok"] is True


@pytest.mark.parametrize(
    "datos",
    [None, "texto", 0, [], {}, 1.5, True, bytearray(b"ab")]
)
def test_datos_tipo_hostil_no_crashea(build_valido, datos):
    r, pub = build_valido
    ok, exc = blindado(
        verificar,
        datos, manifiesto=r["manifiesto"],
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )
    assert exc is None


def test_version_gigante_no_cuelga(build_valido, claves):
    r, _ = build_valido
    priv, _, pub = claves

    c = copy.deepcopy(r["manifiesto"]["cuerpo"])
    c["version"] = 10 ** 5000

    t0 = time.monotonic()
    ok, exc = blindado(
        firmar_bytes, serializar(c), str(priv)
    )

    assert time.monotonic() - t0 < 5
    assert exc is None or isinstance(
        exc, (ValueError, OverflowError)
    )

    if exc is None and ok:
        f = firmar_bytes(serializar(c), str(priv))
        ok2, exc2 = blindado(
            verificar_manifiesto,
            {"cuerpo": c, "firma": f["firma"]},
            pub_bytes=pub,
        )
        assert exc2 is None


def test_cuerpo_grande_no_cuelga(build_valido, claves):
    r, _ = build_valido
    priv, _, pub = claves

    c = copy.deepcopy(r["manifiesto"]["cuerpo"])
    c["artifact_id"] = "A" * (5 * 1024 * 1024)

    t0 = time.monotonic()
    ok, exc = blindado(
        firmar_bytes, serializar(c), str(priv)
    )

    assert time.monotonic() - t0 < 15
    assert exc is None or isinstance(
        exc, (ValueError, OverflowError, MemoryError)
    )

    if exc is None and ok:
        f = firmar_bytes(serializar(c), str(priv))
        ok2, exc2 = blindado(
            verificar,
            r["datos"],
            manifiesto={"cuerpo": c, "firma": f["firma"]},
            pub_bytes=pub, modo=MODO_PROTEGIDO,
        )
        assert exc2 is None


def test_artefacto_grande_no_cuelga(claves):
    priv, _, pub = claves

    r = build(
        b"\x5a" * (2 * 1024 * 1024),
        str(priv), version=1,
    )
    assert r["ok"] is True

    t0 = time.monotonic()
    v = verificar(
        r["datos"], manifiesto=r["manifiesto"],
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )

    assert v["ok"] is True
    assert time.monotonic() - t0 < 10


# ===============================================================
# 22. CONCURRENCIA
# ===============================================================

def test_verificacion_concurrente_sin_estado_compartido(
    build_valido,
):
    r, pub = build_valido
    resultados = []
    lock = threading.Lock()

    def correr():
        locales = []

        for _ in range(30):
            locales.append(
                verificar(
                    r["datos"],
                    manifiesto=r["manifiesto"],
                    pub_bytes=pub,
                    modo=MODO_PROTEGIDO,
                )
            )

        with lock:
            resultados.extend(locales)

    hilos = [
        threading.Thread(target=correr)
        for _ in range(8)
    ]

    for h in hilos:
        h.start()
    for h in hilos:
        h.join()

    assert len(resultados) == 240
    assert all(v["ok"] is True for v in resultados)
    assert all(v["fallos"] == [] for v in resultados)


# ===============================================================
# 23. INVARIANTES DE CONTRATO
# ===============================================================

def test_verificar_nunca_lanza_sobre_entrada_arbitraria(
    build_valido,
):
    r, pub = build_valido

    basura = [
        None, 0, "", b"", [], {}, set(), object(),
        1.5, True,
        {
            "cuerpo": {
                "a": {"b": {"c": [1, {"d": None}]}}
            },
            "firma": "0" * 128,
        },
    ]

    for m in basura:
        ok, exc = blindado(
            verificar,
            r["datos"], manifiesto=m,
            pub_bytes=pub, modo=MODO_PROTEGIDO,
        )
        assert exc is None, (
            f"manifiesto={m!r} "
            f"lanza {type(exc).__name__}: {exc}"
        )


@pytest.mark.parametrize(
    "modo",
    [
        None, "", "protegido", "PROTEGIDO",
        0, 1, -1, [], {}, True,
    ],
)
def test_modo_desconocido_no_relaja_seguridad(
    build_valido, modo
):
    r, pub = build_valido
    m = copy.deepcopy(r["manifiesto"])
    m["cuerpo"]["artifact_id"] = "ATACANTE"

    ok, exc = blindado(
        verificar,
        r["datos"], manifiesto=m,
        pub_bytes=pub, modo=modo,
    )

    assert exc is None
    assert ok is False


def test_fallos_y_conceptos_siempre_presentes(build_valido):
    r, pub = build_valido

    for m in (None, {}, r["manifiesto"]):
        v = verificar(
            r["datos"], manifiesto=m,
            pub_bytes=pub, modo=MODO_PROTEGIDO,
        )
        assert isinstance(v.get("fallos"), list)
        assert isinstance(v.get("conceptos"), list)
        assert isinstance(v.get("ok"), bool)


def test_ok_true_implica_fallos_vacios(build_valido):
    r, pub = build_valido
    v = verificar(
        r["datos"], manifiesto=r["manifiesto"],
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )
    assert (v["ok"] is True) == (v["fallos"] == [])


# ===============================================================
# 24. CADENA COMPLETA
# ===============================================================

def test_cadena_ok_luego_tamper(build_valido):
    r, pub = build_valido

    ok = verificar(
        r["datos"], manifiesto=r["manifiesto"],
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )
    assert ok["ok"] is True
    assert ok["fallos"] == []

    d = bytearray(r["datos"])
    d[-1] ^= 1

    bad = verificar(
        bytes(d), manifiesto=r["manifiesto"],
        pub_bytes=pub, modo=MODO_PROTEGIDO,
    )

    assert bad["ok"] is False
    assert "nucleo" in bad["fallos"]


def test_nucleo_cambia_si_cambia_artefacto(build_valido):
    r, _ = build_valido
    h0 = nucleo(r["datos"])

    d = bytearray(r["datos"])
    d[0] ^= 1

    assert nucleo(bytes(d)) != h0


# ===============================================================
# FIN — batería unificada sin clemencia
# ===============================================================
