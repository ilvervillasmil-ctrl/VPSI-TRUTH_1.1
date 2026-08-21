# tests/test_engine_calculo_verdad_contractual.py
# ===============================================================
# TEST — FÓRMULA 2 — VERDAD CONTRACTUAL
# ===============================================================
#
# OBJETIVO
# --------
# Verificar que Engine.evaluar() recibe una conversación y un contexto
# semántico y produce el resultado de verdad mediante su cadena real.
#
# EL TEST NO:
#   - calcula C
#   - calcula L
#   - calcula K
#   - calcula α
#   - calcula β
#   - calcula Tru_Ri
#   - calcula Tru_total
#   - importa Calculator
#   - importa truth.py
#   - reproduce ninguna fórmula
#
# TODO cálculo pertenece al Engine y a las capacidades contractuales
# que éste resuelva.
# ===============================================================

from __future__ import annotations

import sys
from pathlib import Path

import pytest


# ===============================================================
# REPOSITORIO
# ===============================================================

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


# ===============================================================
# ÚNICO IMPORT PRODUCTIVO
# ===============================================================

from core.engine import Engine


# ===============================================================
# MATERIAL SEMÁNTICO
# ===============================================================

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


# ===============================================================
# PETICIÓN SEMÁNTICA
# ===============================================================

def _peticion(conversacion: str, contexto: str) -> dict:
    """
    Construye exclusivamente la entrada semántica.

    No contiene factores matemáticos ni resultados esperados.
    """
    return {
        "texto": conversacion,
        "mensaje": conversacion,
        "contexto": contexto,
        "O_context": contexto,
        "enunciado_O": contexto,
    }


# ===============================================================
# ENGINE REAL
# ===============================================================

@pytest.fixture(scope="module")
def engine():
    """
    Engine real del repositorio.

    Se utiliza únicamente el contrato actual de Engine.__init__().
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


# ===============================================================
# TEST — VERDAD REAL
# ===============================================================

def test_engine_evaluar_verdad_real(engine):
    """
    El Engine debe realizar el cálculo completo.

    El test no conoce de antemano el resultado.

    Flujo esperado:

        conversación + contexto
                    ↓
                 Engine
                    ↓
             resolución real
                    ↓
              Tru_Ri / Tru_total
    """
    peticion = _peticion(
        CONVERSACION_A,
        CONTEXTO_A,
    )

    resultado = engine.evaluar(peticion)

    assert isinstance(resultado, dict), (
        "Engine.evaluar() debe devolver un dict.\n"
        f"Resultado recibido: {resultado!r}"
    )

    assert "tru_ri" in resultado, (
        "Engine no publicó 'tru_ri'.\n"
        f"Resultado recibido: {resultado!r}"
    )

    assert "tru_total" in resultado, (
        "Engine no publicó 'tru_total'.\n"
        f"Resultado recibido: {resultado!r}"
    )

    print("\n===============================================================")
    print("RESULTADO REAL PRODUCIDO POR ENGINE")
    print("===============================================================")
    print(f"tru_ri    = {resultado['tru_ri']!r}")
    print(f"tru_total = {resultado['tru_total']!r}")
    print("===============================================================")

    # No se compara contra ningún valor calculado por el test.
    # El Engine es la única autoridad del cálculo.
