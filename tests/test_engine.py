# ===============================================================
# VPSI-TRUTH
# tests/test_01_arranque_engine.py
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
#   - No existen excepciones durante el arranque.
#
# ===============================================================


# ===============================================================
# IMPORTACIONES
# ===============================================================

from pathlib import Path

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
    Engine puede instanciarse.
    """
    eng = Engine(
        MODULOS,
        invocador_id="pytest",
        strict=False,
    )

    assert eng is not None


def test_estado_operativo():
    """
    Engine termina en estado OPERATIVO.
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


def test_contenedores_cargados():
    """
    Todo módulo descubierto debe tener CONTENEDOR.
    """
    eng = Engine(
        MODULOS,
        invocador_id="pytest",
        strict=False,
    )

    for contenedor in eng.registro.contenedores.values():
        assert hasattr(contenedor, "capacidades")


def test_no_excepciones_arranque():
    """
    El arranque completo no debe producir excepción.
    """
    try:
        Engine(
            MODULOS,
            invocador_id="pytest",
            strict=False,
        )
    except Exception as e:
        raise AssertionError(
            f"Engine produjo excepción durante el arranque: {e}"
        )


# ===============================================================
# FIN TESTS
# ===============================================================
