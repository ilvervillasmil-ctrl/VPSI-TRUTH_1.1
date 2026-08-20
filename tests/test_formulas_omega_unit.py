# ===============================================================
# VPSI-TRUTH — tests/test_formulas_omega_unit.py
# T12, T13, T17 — fórmulas Omega
#
# PRINCIPIO:
#   Los valores de entrada son datos base de prueba.
#   Las salidas son producidas por las fórmulas reales.
#   El test no importa constants.py ni duplica constantes del
#   otro repositorio.
#   Las comprobaciones se basan en invariantes matemáticos,
#   relaciones entre ejecuciones y propiedades estructurales.
# ===============================================================

from __future__ import annotations

import math

import pytest

from modules.formulas.formulas_omega.resonance import ResonanceLogic
from modules.formulas.formulas_omega.metaconsciousness import (
    MetaconsciousnessCalculator,
)
from modules.formulas.formulas_omega.interaction import ExternalInteraction


# ===============================================================
# DATOS BASE
# ===============================================================

ENERGIA_A = 0.70
ENERGIA_B = 0.70
ENERGIA_C = 0.40

FASE_IGUAL = 0.0
FASE_OPUESTA = math.pi
FASE_INDEPENDIENTE = math.pi / 2

ACTIVACIONES_BASE = [
    0.80,
    0.75,
    0.90,
    0.80,
    0.70,
    0.85,
    0.95,
]

FRICCIONES_BASE = [
    0.10,
    0.10,
    0.10,
    0.10,
    0.10,
    0.10,
    0.10,
]


# ===============================================================
# T12 — RESONANCIA
# ===============================================================

def test_t12_resonancia_energia_igual():
    """T12 — energías iguales producen alineación máxima."""

    resultado = ResonanceLogic.calculate_phase_alignment(
        ENERGIA_A,
        ENERGIA_B,
    )

    assert math.isfinite(float(resultado))
    assert 0.0 <= float(resultado) <= 1.0
    assert float(resultado) == pytest.approx(1.0)


def test_t12_resonancia_par_fase_igual():
    """T12 — energías iguales y fase igual producen resonancia máxima."""

    resultado = ResonanceLogic.pair_resonance(
        ENERGIA_A,
        ENERGIA_B,
        FASE_IGUAL,
    )

    assert math.isfinite(float(resultado))
    assert 0.0 <= float(resultado) <= 1.0
    assert float(resultado) == pytest.approx(1.0)


def test_t12_resonancia_fase_opuesta_reduce_resultado():
    """T12 — la fase opuesta no puede superar la fase alineada."""

    alineada = ResonanceLogic.pair_resonance(
        ENERGIA_A,
        ENERGIA_B,
        FASE_IGUAL,
    )

    opuesta = ResonanceLogic.pair_resonance(
        ENERGIA_A,
        ENERGIA_B,
        FASE_OPUESTA,
    )

    assert math.isfinite(float(alineada))
    assert math.isfinite(float(opuesta))
    assert float(opuesta) <= float(alineada)
    assert float(opuesta) == pytest.approx(0.0)


def test_t12_resonancia_fase_independiente_intermedia():
    """T12 — fase π/2 produce un valor entre alineación y oposición."""

    alineada = ResonanceLogic.pair_resonance(
        ENERGIA_A,
        ENERGIA_B,
        FASE_IGUAL,
    )

    independiente = ResonanceLogic.pair_resonance(
        ENERGIA_A,
        ENERGIA_B,
        FASE_INDEPENDIENTE,
    )

    opuesta = ResonanceLogic.pair_resonance(
        ENERGIA_A,
        ENERGIA_B,
        FASE_OPUESTA,
    )

    assert float(opuesta) <= float(independiente)
    assert float(independiente) <= float(alineada)


def test_t12_resonancia_energia_cero():
    """T12 — una energía nula elimina la magnitud de resonancia."""

    resultado = ResonanceLogic.pair_resonance(
        0.0,
        ENERGIA_A,
        FASE_IGUAL,
    )

    assert math.isfinite(float(resultado))
    assert float(resultado) == pytest.approx(0.0)


def test_t12_resonancia_global_datos_base():
    """T12 — compute() produce una resonancia global válida."""

    energias = [
        ENERGIA_A,
        ENERGIA_B,
        ENERGIA_C,
    ]

    resultado = ResonanceLogic.compute(energias)

    assert math.isfinite(float(resultado))
    assert 0.0 <= float(resultado) <= 1.0


def test_t12_resonancia_global_cero():
    """T12 — un conjunto completamente nulo no produce resonancia."""

    resultado = ResonanceLogic.compute(
        [0.0, 0.0, 0.0],
    )

    assert math.isfinite(float(resultado))
    assert float(resultado) == pytest.approx(0.0)


# ===============================================================
# T13 — METACONSCIENCIA
# ===============================================================

def test_t13_mc_datos_base():
    """T13 — datos base producen MC finita y no negativa."""

    resultado = MetaconsciousnessCalculator.compute(
        ACTIVACIONES_BASE,
        FRICCIONES_BASE,
    )

    assert math.isfinite(float(resultado))
    assert float(resultado) >= 0.0


def test_t13_mc_capa_l3_cero():
    """T13 — L3=0 anula el producto L3-L6."""

    activaciones = list(ACTIVACIONES_BASE)
    activaciones[3] = 0.0

    resultado = MetaconsciousnessCalculator.compute(
        activaciones,
        FRICCIONES_BASE,
    )

    assert float(resultado) == pytest.approx(0.0)


def test_t13_mc_capa_l4_cero():
    """T13 — L4=0 anula el producto L3-L6."""

    activaciones = list(ACTIVACIONES_BASE)
    activaciones[4] = 0.0

    resultado = MetaconsciousnessCalculator.compute(
        activaciones,
        FRICCIONES_BASE,
    )

    assert float(resultado) == pytest.approx(0.0)


def test_t13_mc_capa_l5_cero():
    """T13 — L5=0 anula el producto L3-L6."""

    activaciones = list(ACTIVACIONES_BASE)
    activaciones[5] = 0.0

    resultado = MetaconsciousnessCalculator.compute(
        activaciones,
        FRICCIONES_BASE,
    )

    assert float(resultado) == pytest.approx(0.0)


def test_t13_mc_capa_l6_cero():
    """T13 — L6=0 anula el producto L3-L6."""

    activaciones = list(ACTIVACIONES_BASE)
    activaciones[6] = 0.0

    resultado = MetaconsciousnessCalculator.compute(
        activaciones,
        FRICCIONES_BASE,
    )

    assert float(resultado) == pytest.approx(0.0)


def test_t13_mc_frictions_reduce_resultado():
    """T13 — aumentar fricción en una capa activa no aumenta MC."""

    fricciones_bajas = list(FRICCIONES_BASE)
    fricciones_altas = list(FRICCIONES_BASE)

    fricciones_altas[3] = 0.40

    mc_bajo = MetaconsciousnessCalculator.compute(
        ACTIVACIONES_BASE,
        fricciones_bajas,
    )

    mc_alto = MetaconsciousnessCalculator.compute(
        ACTIVACIONES_BASE,
        fricciones_altas,
    )

    assert float(mc_alto) <= float(mc_bajo)


def test_t13_mc_level_consistente_con_resultado():
    """T13 — level_name corresponde al nivel calculado por la propia fórmula."""

    resultado = MetaconsciousnessCalculator.compute(
        ACTIVACIONES_BASE,
        FRICCIONES_BASE,
    )

    nivel = MetaconsciousnessCalculator.level(resultado)
    nombre = MetaconsciousnessCalculator.level_name(resultado)

    assert nivel in (0, 1, 2, 3)
    assert isinstance(nombre, str)
    assert nombre


# ===============================================================
# T17 — INTERACCIÓN EXTERNA
# ===============================================================

def test_t17_interaction_love():
    """T17 — θ=0 equivale a suma."""

    c1 = 0.30
    c2 = 0.40

    resultado = ExternalInteraction.love(c1, c2)

    assert math.isfinite(resultado)
    assert resultado == pytest.approx(c1 + c2)


def test_t17_interaction_conflict():
    """T17 — θ=π equivale a diferencia absoluta."""

    c1 = 0.50
    c2 = 0.20

    resultado = ExternalInteraction.conflict(c1, c2)

    assert math.isfinite(resultado)
    assert resultado == pytest.approx(abs(c1 - c2))


def test_t17_interaction_independence():
    """T17 — θ=π/2 equivale a norma euclidiana."""

    c1 = 0.30
    c2 = 0.40

    resultado = ExternalInteraction.independence(c1, c2)

    esperado = math.hypot(c1, c2)

    assert math.isfinite(resultado)
    assert resultado == pytest.approx(esperado)


def test_t17_interaction_compute_pair_datos_base():
    """T17 — compute_pair ejecuta la ley del coseno con datos base."""

    c1 = 0.30
    c2 = 0.40
    theta = math.pi / 3

    resultado = ExternalInteraction.compute_pair(
        c1,
        c2,
        theta,
    )

    esperado = math.sqrt(
        c1 ** 2
        + c2 ** 2
        + 2.0 * c1 * c2 * math.cos(theta)
    )

    assert math.isfinite(resultado)
    assert resultado == pytest.approx(esperado)


def test_t17_interaction_compute_pair_conecta_casos_limite():
    """T17 — compute_pair coincide con las tres especializaciones."""

    c1 = 0.30
    c2 = 0.40

    love = ExternalInteraction.compute_pair(
        c1,
        c2,
        0.0,
    )

    conflict = ExternalInteraction.compute_pair(
        c1,
        c2,
        math.pi,
    )

    independence = ExternalInteraction.compute_pair(
        c1,
        c2,
        math.pi / 2,
    )

    assert love == pytest.approx(
        ExternalInteraction.love(c1, c2)
    )

    assert conflict == pytest.approx(
        ExternalInteraction.conflict(c1, c2)
    )

    assert independence == pytest.approx(
        ExternalInteraction.independence(c1, c2)
    )


def test_t17_interaction_multi_datos_base():
    """T17 — compute_multi reduce múltiples coherencias."""

    valores = [
        0.20,
        0.30,
        0.40,
    ]

    resultado = ExternalInteraction.compute_multi(valores)

    esperado = sum(valores)

    assert math.isfinite(resultado)
    assert resultado == pytest.approx(esperado)


def test_t17_interaction_multi_vacio():
    """T17 — colección vacía produce el caso nulo definido."""

    resultado = ExternalInteraction.compute_multi([])

    assert resultado == pytest.approx(0.0)


def test_t17_interaction_multi_un_elemento():
    """T17 — un escalar conserva su valor."""

    valor = 0.75

    resultado = ExternalInteraction.compute_multi([valor])

    assert resultado == pytest.approx(valor)


# ===============================================================
# T12/T13/T17 — DETERMINISMO
# ===============================================================

def test_formulas_omega_determinismo():
    """Mismo input → mismo resultado."""

    energias = [
        ENERGIA_A,
        ENERGIA_B,
        ENERGIA_C,
    ]

    r1 = ResonanceLogic.compute(energias)
    r2 = ResonanceLogic.compute(energias)

    assert r1 == pytest.approx(r2)

    mc1 = MetaconsciousnessCalculator.compute(
        ACTIVACIONES_BASE,
        FRICCIONES_BASE,
    )

    mc2 = MetaconsciousnessCalculator.compute(
        ACTIVACIONES_BASE,
        FRICCIONES_BASE,
    )

    assert mc1 == pytest.approx(mc2)

    i1 = ExternalInteraction.compute_pair(
        0.30,
        0.40,
        math.pi / 3,
    )

    i2 = ExternalInteraction.compute_pair(
        0.30,
        0.40,
        math.pi / 3,
    )

    assert i1 == pytest.approx(i2)


# ===============================================================
# FIN
# ===============================================================
