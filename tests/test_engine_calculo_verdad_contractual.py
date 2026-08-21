# -*- coding: utf-8 -*-
# tests/test_engine_calculo_verdad_contractual.py
# ===============================================================
# TEST — FÓRMULA 2 — VERDAD CONTRACTUAL
# ===============================================================
#
# OBJETIVO
# --------
# Verificar la cadena real:
#
#     SF
#      ↓
#   capas L0..L6
#      ↓
#   Engine.calcular_coherencia()
#      ↓
#   FO.evaluar_coherencia()
#      ↓
#   Engine.aplicar_verdad()
#      ↓
#   FO.tru_total
#      ↓
#   verdad cuantificada
#
# El test NO calcula:
#   C
#   L
#   K
#   α
#   β
#   Tru_Ri
#   Tru_total
#
# El test únicamente entrega una situación semántica como contexto
# auxiliar y deja que el Engine ejecute su cadena contractual real.
#
# No se hardcodea ningún resultado matemático.
# ===============================================================

from __future__ import annotations

import math
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
# PETICIÓN / CONTEXTO SEMÁNTICO
# ===============================================================

def _contexto_verdad() -> dict:
    """
    Contexto semántico auxiliar.

    No contiene C, L, K ni ningún resultado matemático.
    """
    return {
        "texto": CONVERSACION_A,
        "mensaje": CONVERSACION_A,
        "contexto": CONTEXTO_A,
        "O_context": CONTEXTO_A,
        "enunciado_O": CONTEXTO_A,
    }


# ===============================================================
# ENGINE REAL
# ===============================================================

@pytest.fixture(scope="module")
def engine():
    """
    Engine real del repositorio.

    Se utiliza exclusivamente la firma actual del constructor.
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

def test_engine_calcula_verdad_por_ciclo_real(engine):
    """
    El Engine debe ejecutar su cadena contractual real.

    El test no proporciona C, L ni K.

    El Engine debe:
        1. obtener las capas de SF;
        2. calcular CΩ mediante FO;
        3. pasar el resultado a la pared de verdad;
        4. ejecutar FO.tru_total;
        5. devolver la verdad resultante.
    """

    contexto = _contexto_verdad()

    capas = engine.obtener_capas_self()

    assert capas is not None, (
        "SF no proporcionó las capas necesarias para el ciclo."
    )

    resultado = engine.ciclo_omega(
        capas=capas,
        meta=contexto,
    )

    assert isinstance(resultado, dict), (
        "Engine.ciclo_omega() debe devolver un dict.\n"
        f"Resultado recibido: {resultado!r}"
    )

    assert resultado.get("estado") == "EXITO", (
        "El ciclo de verdad no terminó correctamente.\n"
        f"Resultado: {resultado!r}"
    )

    assert resultado.get("operacion") == "ciclo_omega"

    assert "coherencia" in resultado, (
        "El ciclo no publicó la coherencia producida por FO."
    )

    assert "verdad" in resultado, (
        "El ciclo no publicó el resultado de verdad."
    )

    coherencia = resultado["coherencia"]
    verdad = resultado["verdad"]

    assert isinstance(coherencia, (int, float))
    assert not isinstance(coherencia, bool)
    assert math.isfinite(float(coherencia))

    assert isinstance(verdad, (int, float))
    assert not isinstance(verdad, bool)
    assert math.isfinite(float(verdad))

    assert 0.0 <= float(coherencia) <= 1.0
    assert 0.0 <= float(verdad) <= 1.0

    assert resultado["detalle_coherencia"]["capacidad"] == (
        "evaluar_coherencia"
    )

    assert resultado["detalle_verdad"]["capacidad"] in (
        "tru_total",
        engine.clave_proposito,
    )

    print("\n===============================================================")
    print("RESULTADO REAL DEL ENGINE")
    print("===============================================================")
    print(f"coherencia = {coherencia!r}")
    print(f"verdad     = {verdad!r}")
    print("===============================================================")
