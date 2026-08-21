
"""
===============================================================================
TEST — ENGINE / CÁLCULO REAL DE VERDAD
===============================================================================

OBJETIVO
--------
Comprobar la cadena real de cálculo de verdad desde una petición semántica.

El test solamente proporciona:

    X = conversación
    O = contexto

El cálculo pertenece exclusivamente al Engine y a las capacidades que éste
resuelva contractualmente.

Este test NO:

    - calcula C
    - calcula L
    - calcula K
    - calcula α
    - calcula β
    - calcula Tru_Ri
    - calcula Tru_total
    - reconstruye ninguna fórmula
    - importa Calculator
    - importa truth.py
    - construye argumentos internos de FO
    - introduce la clave L manualmente
    - conoce qué capacidades internas debe ejecutar Engine
    - sustituye una interfaz del Engine por una interfaz de FO

La prueba únicamente observa la salida publicada por Engine.
===============================================================================
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest


# ===========================================================================
# REPOSITORIO
# ===========================================================================

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


# ===========================================================================
# ENGINE REAL
# ===========================================================================

from core.engine import Engine


# ===========================================================================
# MATERIAL SEMÁNTICO
# ===========================================================================

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
    "Afirmación a evaluar: Carlos afirma 'Tengo 5 apartamentos'. "
    "Evidencia aportada por Carla: los contratos y títulos de propiedad "
    "de esos 5 apartamentos están a su nombre y no a nombre de Carlos."
)


# ===========================================================================
# PETICIÓN
# ===========================================================================

def _peticion_verdad() -> dict:
    """
    Construye exclusivamente la entrada semántica.

    No contiene ningún resultado ni factor matemático.
    """
    return {
        "texto": CONVERSACION,
        "mensaje": CONVERSACION,
        "contexto": CONTEXTO,
        "O_context": CONTEXTO,
        "enunciado_O": CONTEXTO,
    }


# ===========================================================================
# FIXTURE — ENGINE REAL
# ===========================================================================

@pytest.fixture(scope="module")
def engine():
    """
    Engine real del repositorio.

    El test no modifica ni sustituye ninguna capacidad.
    """
    eng = Engine(
        ROOT / "modules",
        invocador_id="test_engine_calculo_verdad_contractual",
        strict=True,
    )

    assert eng.estado == "OPERATIVO", (
        "ENGINE NO OPERATIVO\n"
        f"estado={eng.estado!r}\n"
        f"errores={eng.errores_arranque!r}"
    )

    return eng


# ===========================================================================
# TEST — PETICIÓN REAL DE VERDAD
# ===========================================================================

def test_engine_calcula_verdad_por_ciclo_real(engine):
    """
    El test entrega X + O.

    A partir de ahí, el Engine debe ejecutar su propia cadena contractual.

    El test no conoce ni reproduce los pasos internos.
    """

    peticion = _peticion_verdad()

    resultado = engine.ciclo_omega(
        meta=peticion,
    )

    assert isinstance(resultado, dict), (
        "Engine no devolvió una estructura contractual tipo dict.\n"
        f"Resultado: {resultado!r}"
    )

    assert resultado.get("estado") == "EXITO", (
        "El Engine no completó el ciclo de verdad.\n"
        f"Resultado: {resultado!r}"
    )

    assert "verdad" in resultado, (
        "El Engine completó el ciclo pero no publicó el bloque de verdad.\n"
        f"Resultado: {resultado!r}"
    )


# ===========================================================================
# TEST — DETERMINISMO
# ===========================================================================

def test_engine_verdad_es_determinista(engine):
    """
    La misma petición semántica debe producir la misma salida observable.

    No se inspeccionan ni reproducen los cálculos internos.
    """

    peticion = _peticion_verdad()

    primero = engine.ciclo_omega(meta=peticion)
    segundo = engine.ciclo_omega(meta=peticion)

    assert isinstance(primero, dict)
    assert isinstance(segundo, dict)

    assert primero == segundo
