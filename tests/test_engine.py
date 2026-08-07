# ===============================================================
# VPSI-TRUTH
# tests/test_engine.py
# ===============================================================
#
# TEST:
#   Arranque del Engine
#
# Objetivo:
#   Garantizar que el Engine inicia correctamente y que la
#   infraestructura mínima del sistema queda operativa.
#
# Qué verifica:
#   - El Engine puede construirse.
#   - Estado OPERATIVO.
#   - Descubrimiento de módulos.
#   - Registro creado.
#   - Los contenedores poseen capacidades.
#   - No existen excepciones durante el arranque.
#
# ===============================================================


# ===============================================================
# IMPORTACIONES
# ===============================================================

import sys
from pathlib import Path

# Permite importar "core" desde GitHub Actions y pytest
sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent)
)

from core.engine import Engine

# ===============================================================
# FIN IMPORTACIONES
# ===============================================================


# ===============================================================
# CONFIGURACIÓN
# ===============================================================

MODULOS = Path("modules")

# ===============================================================
# FIN CONFIGURACIÓN
# ===============================================================


# ===============================================================
# TESTS
# ===============================================================

def test_engine_se_construye():
    """
    El Engine puede construirse.
    """
    eng = Engine(
        MODULOS,
        invocador_id="pytest",
        strict=False,
    )

    assert eng is not None


def test_estado_operativo():
    """
    El Engine termina en estado OPERATIVO.
    """
    eng = Engine(
        MODULOS,
        invocador_id="pytest",
        strict=False,
    )

    assert eng.estado == "OPERATIVO"


def test_descubre_modulos():
    """
    Debe descubrir al menos un módulo.
    """
    eng = Engine(
        MODULOS,
        invocador_id="pytest",
        strict=False,
    )

    assert eng.registro.total() > 0


def test_contenedores_tienen_capacidades():
    """
    Todo contenedor descubierto debe declarar capacidades.
    """
    eng = Engine(
        MODULOS,
        invocador_id="pytest",
        strict=False,
    )

    assert len(eng.registro.contenedores) > 0

    for contenedor in eng.registro.contenedores.values():

        assert hasattr(contenedor, "capacidades")

        assert isinstance(contenedor.capacidades, dict)

        assert len(contenedor.capacidades) > 0


def test_no_excepciones_arranque():
    """
    El arranque completo no debe producir excepciones.
    """
    try:

        Engine(
            MODULOS,
            invocador_id="pytest",
            strict=False,
        )

    except Exception as e:

        raise AssertionError(
            f"Engine produjo una excepción durante el arranque: {e}"
        )


# ===============================================================
# FIN TESTS
# ===============================================================
