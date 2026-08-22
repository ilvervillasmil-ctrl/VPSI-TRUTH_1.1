"""
===============================================================================
TEST — VERDAD REAL MEDIANTE ENGINE
===============================================================================

El test presenta al Engine una conversación y su contexto.

La petición es determinar la VERDAD de la afirmación de Carlos
basándose en la conversación y en la evidencia presentada.

El Engine realiza todo el proceso matemático internamente.

El test no calcula la verdad.
El test no conoce los factores.
El test no introduce resultados.
El test no reproduce ninguna fórmula.
===============================================================================
"""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

import pytest

from core.engine import Engine


ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


# ============================================================================
# MATERIAL PARA DETERMINAR LA VERDAD
# ============================================================================

CONVERSACION = (
    "Carlos: Mana, voy a Miami.\n"
    "Maria: Genial, ¿qué harás?\n"
    "Carlos: Voy de vacaciones. Tengo 5 apartamentos.\n"
    "Maria: Carlos me dijo que tiene 5 apartamentos.\n"
    "Carla: Yo soy la hermana. Esta es la evidencia: aquí están los "
    "contratos y títulos de propiedad de esos 5 apartamentos y son míos, "
    "no de Carlos."
)

CONTEXTO = (
    "Determinar la verdad de la afirmación de Carlos "
    "basándose en la conversación y en la evidencia presentada."
)


# ============================================================================
# PETICIÓN
# ============================================================================

def _peticion_verdad() -> dict:
    return {
        "texto": CONVERSACION,
        "mensaje": CONVERSACION,
        "contexto": CONTEXTO,
        "O_context": CONTEXTO,
        "enunciado_O": CONTEXTO,
    }


# ============================================================================
# ENGINE
# ============================================================================

@pytest.fixture(scope="module")
def engine():
    eng = Engine(
        raiz_modulos=ROOT / "modules",
        invocador_id="test_engine_calculo_verdad_contractual",
        strict=True,
    )
    assert eng.estado == "OPERATIVO", (
        "Engine no operativo: {0!r}; errores={1!r}".format(
            eng.estado, eng.errores_arranque
        )
    )
    return eng


# ============================================================================
# TEST DE VERDAD
# ============================================================================

def test_engine_calcula_verdad_por_ciclo_real(engine):
    """
    El Engine recibe una petición de verdad basada en el contexto.

    Debe exponer C, L, K, tru_ri, tru_total como Fraction.
    El cálculo pertenece completamente al Engine.
    """
    peticion = _peticion_verdad()
    resultado = engine.ciclo_omega(capas=peticion)

    assert isinstance(resultado, dict)

    assert "C" in resultado
    assert "L" in resultado
    assert "K" in resultado
    assert "tru_ri" in resultado
    assert "tru_total" in resultado

    assert isinstance(resultado["C"], Fraction)
    assert isinstance(resultado["L"], Fraction)
    assert isinstance(resultado["K"], Fraction)
    assert isinstance(resultado["tru_ri"], Fraction)
    assert isinstance(resultado["tru_total"], Fraction)
