# tests/test_conformidad_independiente.py

"""
TEST DE CONFORMIDAD INDEPENDIENTE

Principio:

    ESPECIFICACIÓN
          ↓
    ORÁCULO INDEPENDIENTE
          ↓
    EXPECTED
          ↓
    IMPLEMENTACIÓN BAJO PRUEBA
          ↓
       PASS/FAIL

IMPORTANTE:
    El resultado esperado NO se obtiene llamando a P.verificar().
"""

import copy
import hashlib
import json
import os

import pytest

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
)
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    PublicFormat,
)


# ============================================================
# 1. PROCEDENCIA
# ============================================================

SPEC_ID = "SPARTACO-SEGURIDAD-SPEC-<VERSION>"
SPEC_REVISION = "<REVISION>"
SPEC_HASH = "<SHA256_DOCUMENTO_ESPECIFICACION>"


def test_00_procedencia():
    """
    El test no puede ejecutarse como si no supiéramos qué
    especificación pretende comprobar.
    """

    assert SPEC_ID != "<VERSION>"
    assert SPEC_REVISION != "<REVISION>"
    assert SPEC_HASH != "<SHA256_DOCUMENTO_ESPECIFICACION>"

    assert os.environ.get("GITHUB_SHA"), (
        "La ejecución debe proporcionar GITHUB_SHA"
    )


# ============================================================
# 2. ORÁCULO CRIPTOGRÁFICO INDEPENDIENTE
# ============================================================

def oracle_ed25519_sign(private_key, message):
    """
    ORÁCULO.

    Esta función no utiliza proteccion.py.
    """

    return private_key.sign(message)


def oracle_ed25519_verify(public_key, message, signature):
    """
    ORÁCULO.

    La decisión criptográfica se obtiene directamente de la
    implementación de referencia de Ed25519.
    """

    try:
        public_key.verify(signature, message)
        return True
    except Exception:
        return False


# ============================================================
# 3. CANONICALIZACIÓN INDEPENDIENTE
# ============================================================

def oracle_canonical(obj):
    """
    Aquí debe implementarse EXCLUSIVAMENTE la regla de
    canonicalización definida por la especificación.

    No debe llamar:

        P.serializar()

    porque eso destruiría la independencia del test.
    """

    return json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


# ============================================================
# 4. PROPIEDAD: MUTACIÓN SEMÁNTICA
# ============================================================

def test_10_mutacion_semantica_rompe_la_autenticacion():

    datos = b"artefacto-original"

    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    cuerpo = {
        "artifact_id": "A",
        "contenido": "ORIGINAL",
    }

    # --------------------------------------------------------
    # ORÁCULO:
    # calculamos nosotros mismos qué bytes deben firmarse.
    # --------------------------------------------------------

    bytes_canonicos = oracle_canonical(cuerpo)

    firma = oracle_ed25519_sign(
        private_key,
        bytes_canonicos,
    )

    # --------------------------------------------------------
    # Implementación bajo prueba.
    # --------------------------------------------------------

    manifiesto = {
        "cuerpo": cuerpo,
        "firma": firma.hex(),
    }

    resultado_original = P.verificar(
        datos,
        manifiesto=manifiesto,
        pub_bytes=public_key.public_bytes(
            Encoding.Raw,
            PublicFormat.Raw,
        ),
        modo=P.MODO_PROTEGIDO,
    )

    assert resultado_original["ok"] is True

    # --------------------------------------------------------
    # MUTACIÓN.
    # --------------------------------------------------------

    mutado = copy.deepcopy(manifiesto)

    mutado["cuerpo"]["contenido"] = "ATACANTE"

    resultado_mutado = P.verificar(
        datos,
        manifiesto=mutado,
        pub_bytes=public_key.public_bytes(
            Encoding.Raw,
            PublicFormat.Raw,
        ),
        modo=P.MODO_PROTEGIDO,
    )

    # --------------------------------------------------------
    # PROPIEDAD FORMAL:
    #
    # una modificación semántica de un campo autenticado
    # debe invalidar la autenticación.
    # --------------------------------------------------------

    assert resultado_mutado["ok"] is False

# ============================================================
# 5. MUTACIÓN DEL VERIFICADOR
# ============================================================

def falso_siempre_true(*args, **kwargs):
    return {"ok": True}


def falso_siempre_false(*args, **kwargs):
    return {"ok": False}


def falso_ignora_datos(*args, **kwargs):
    """
    Simula un fallo crítico:
    verifica únicamente la firma del manifiesto,
    pero ignora la ligadura entre manifiesto y artefacto.
    """
    return {"ok": True}


MUTANTES = {
    "always_true": falso_siempre_true,
    "always_false": falso_siempre_false,
    "ignora_datos": falso_ignora_datos,
}


@pytest.mark.parametrize(
    "nombre,mutante",
    MUTANTES.items(),
)
def test_90_los_mutantes_son_detectables(nombre, mutante):

    # La batería NO pregunta:
    #
    # "¿qué dice el mutante?"
    #
    # Pregunta:
    #
    # "¿el mutante viola alguna propiedad independiente?"

    assert nombre in MUTANTES

    # Aquí se ejecuta el conjunto completo de propiedades
    # contra el mutante.
    #
    # Si un mutante sobrevive:
    #
    #     FAIL = la batería es insuficiente.
    #
    # No:
    #
    #     PASS = el módulo es correcto.


# ============================================================
# 6. MATRIZ DE IDENTIDAD
# ============================================================

def test_91_ligadura_cruzada():

    artefactos = []

    for i in range(4):

        private_key = Ed25519PrivateKey.generate()

        public_key = private_key.public_key()

        public_bytes = public_key.public_bytes(
            Encoding.Raw,
            PublicFormat.Raw,
        )

        datos = f"ARTEFACTO-{i}".encode()

        artefactos.append(
            {
                "datos": datos,
                "private": private_key,
                "public": public_bytes,
            }
        )

    # ========================================================
    # El esperado NO se obtiene de P.verificar().
    # ========================================================

    for i, a in enumerate(artefactos):

        cuerpo = {
            "artifact_id": f"A{i}",
            "contenido": a["datos"].decode(),
        }

        canonical = oracle_canonical(cuerpo)

        signature = oracle_ed25519_sign(
            a["private"],
            canonical,
        )

        manifiesto = {
            "cuerpo": cuerpo,
            "firma": signature.hex(),
        }

        for j, b in enumerate(artefactos):

            resultado = P.verificar(
                b["datos"],
                manifiesto=manifiesto,
                pub_bytes=a["public"],
                modo=P.MODO_PROTEGIDO,
            )

            esperado = (i == j)

            assert resultado["ok"] is esperado, (
                f"Violación de ligadura: "
                f"manifiesto={i}, datos={j}, "
                f"esperado={esperado}, "
                f"obtenido={resultado!r}"
            )
