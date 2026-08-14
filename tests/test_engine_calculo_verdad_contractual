# -*- coding: utf-8 -*-
"""
===============================================================================
TEST SONDA — test_engine_calculo_verdad_blackbox_probe
===============================================================================

OBJETIVO
--------
Sonda diagnóstica de caja negra sobre Engine.evaluar().

Este Test NO calcula la verdad.
Este Test NO calcula C, L, K.
Este Test NO calcula α ni β.
Este Test NO importa Calculator.
Este Test NO importa truth.py.
Este Test NO reconstruye Tru_Ri.
Este Test NO reconstruye Tru_total.
Este Test NO conoce los valores correctos.

El único cálculo autorizado es el que realiza:

    Engine.evaluar(peticion)

La sonda entrega X + O al Engine y posteriormente compara los valores
publicados por Engine contra valores señuelo deliberadamente incorrectos.

Los señuelos NO representan valores esperados.
Su única finalidad es provocar un fallo controlado de pytest.

El valor ACTUAL mostrado por pytest corresponde al valor publicado
por Engine para esa ejecución.

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
# ÚNICO IMPORT PRODUCTIVO
# ===========================================================================

from core.engine import Engine


# ===========================================================================
# MATERIAL SEMÁNTICO
# ===========================================================================

CONVERSACION_A = (
    "Carlos: Mana, voy a Miami.\n"
    "Maria: Genial, ¿qué harás?\n"
    "Carlos: Voy de vacaciones. Tengo 5 apartamentos.\n"
    "Maria: Carlos me dijo que tiene 5 apartamentos.\n"
    "Carla: Yo soy la hermana. Esta es la evidencia: aquí están los "
    "contratos y títulos de propiedad de esos 5 apartamentos y son míos, "
    "no de Carlos."
)

CONTEXTO_A = (
    "Afirmación a evaluar: Carlos afirma 'Tengo 5 apartamentos'. "
    "Evidencia aportada por Carla: los contratos y títulos de propiedad "
    "de esos 5 apartamentos están a su nombre y no a nombre de Carlos."
)


# ===========================================================================
# CONSTRUCCIÓN DE PETICIÓN
# ===========================================================================

def _peticion(conversacion: str, contexto: str) -> dict:
    """
    Entrada semántica.

    No contiene resultados, factores ni parámetros del cálculo.
    """

    return {
        "texto": conversacion,
        "mensaje": conversacion,
        "contexto": contexto,
        "O_context": contexto,
        "enunciado_O": contexto,
    }


# ===========================================================================
# FIXTURE — ENGINE REAL
# ===========================================================================

@pytest.fixture(scope="module")
def engine():
    """
    Instancia real del Engine.

    Si el Engine no arranca, la prueba falla.
    """

    eng = Engine(
        raiz_modulos=ROOT / "modules",
        invocador_id="test_engine_calculo_verdad_blackbox_probe",
        verificar_axiomas=True,
        strict=True,
    )

    assert eng.estado == "OPERATIVO", (
        "ENGINE NO OPERATIVO\n"
        f"estado={eng.estado!r}\n"
        f"errores={eng.errores_arranque!r}"
    )

    return eng


# ===========================================================================
# SONDA
# ===========================================================================

class TestEngineBlackBoxProbe:
    """
    Sonda deliberadamente falsificada.

    La prueba NO busca pasar.

    La finalidad es que pytest revele el valor producido por Engine.
    """

    def test_sonda_tru_ri(self, engine):
        """
        Ejecuta Engine y fuerza una discrepancia contra un valor señuelo.

        Si Engine publica, por ejemplo:

            1/6

        pytest mostrará la discrepancia entre el valor actual y el señuelo.
        """

        resultado = engine.evaluar(
            _peticion(CONVERSACION_A, CONTEXTO_A)
        )

        assert isinstance(resultado, dict), (
            f"Engine no devolvió dict: {resultado!r}"
        )

        assert "tru_ri" in resultado, (
            f"Engine no publicó 'tru_ri'. Resultado: {resultado!r}"
        )

        # SEÑUELO DELIBERADAMENTE INCORRECTO.
        # NO calcular.
        # NO sustituir por el valor real.
        tru_ri_señuelo = "999999999/999999998"

        assert str(resultado["tru_ri"]) == tru_ri_señuelo


    def test_sonda_tru_total(self, engine):
        """
        Ejecuta nuevamente Engine y fuerza una discrepancia contra un
        valor señuelo independiente.

        Si Engine publica, por ejemplo:

            11/162

        pytest mostrará ese valor como ACTUAL.
        """

        resultado = engine.evaluar(
            _peticion(CONVERSACION_A, CONTEXTO_A)
        )

        assert isinstance(resultado, dict), (
            f"Engine no devolvió dict: {resultado!r}"
        )

        assert "tru_total" in resultado, (
            f"Engine no publicó 'tru_total'. Resultado: {resultado!r}"
        )

        # SEÑUELO DELIBERADAMENTE INCORRECTO.
        # NO calcular.
        # NO sustituir por el valor real.
        tru_total_señuelo = "888888887/888888886"

        assert str(resultado["tru_total"]) == tru_total_señuelo
