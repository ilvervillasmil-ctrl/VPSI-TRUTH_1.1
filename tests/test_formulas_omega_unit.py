# tests/test_formulas_omega_unit.py
# T12, T13, T17: fórmulas unitarias Omega
#
# Objetivo:
#   Verificar las invariantes matemáticas y contratos reales de las
#   fórmulas utilizadas por CoherenceEngine, sin duplicar la implementación
#   ni depender de valores arbitrarios.
#
# T12 = ResonanceLogic
# T13 = MetaconsciousnessCalculator
# T17 = ExternalInteraction

from __future__ import annotations

import math

import pytest

from modules.formulas.formulas_omega.resonance import ResonanceLogic
from modules.formulas.formulas_omega.metaconsciousness import (
    MetaconsciousnessCalculator,
)
from modules.formulas.formulas_omega.interaction import ExternalInteraction
from modules.formulas.constants import R_FIN


# ===============================================================
# T12 — RESONANCIA
# ===============================================================


def test_t12_resonancia_simetria():
    """T12 — la resonancia de un par no depende del orden."""
    casos = (
        (0.2, 0.7),
        (0.5, 0.5),
        (0.0, 1.0),
        (0.9, 0.3),
    )

    for a, b in casos:
        ab = ResonanceLogic.pair_resonance(a, b)
        ba = ResonanceLogic.pair_resonance(b, a)

        assert math.isfinite(float(ab))
        assert math.isfinite(float(ba))
        assert ab == pytest.approx(ba)


def test_t12_resonancia_identidad():
    """T12 — dos energías iguales producen alineación máxima."""
    for energy in (0.0, 0.1, 0.5, 1.0, 2.0):
        alignment = ResonanceLogic.calculate_phase_alignment(
            energy,
            energy,
        )

        assert alignment == pytest.approx(1.0)


def test_t12_resonancia_par_igual():
    """T12 — energías iguales producen resonancia máxima."""
    for energy in (0.1, 0.5, 1.0, 2.0):
        resonance = ResonanceLogic.pair_resonance(
            energy,
            energy,
            0.0,
        )

        assert resonance == pytest.approx(1.0)


def test_t12_resonancia_cero():
    """T12 — una energía nula elimina la resonancia del par."""
    assert ResonanceLogic.pair_resonance(0.0, 1.0) == pytest.approx(0.0)
    assert ResonanceLogic.pair_resonance(1.0, 0.0) == pytest.approx(0.0)


def test_t12_resonancia_todas_cero():
    """T12 — un sistema completamente sin energía tiene resonancia nula."""
    assert ResonanceLogic.compute([0.0, 0.0, 0.0]) == pytest.approx(0.0)


def test_t12_resonancia_resultado_acotado():
    """T12 — la resonancia global permanece en su dominio [0,1]."""
    casos = (
        [0.1, 0.2, 0.3],
        [1.0, 1.0, 1.0],
        [0.0, 1.0, 0.5],
        [2.0, 0.5, 3.0],
    )

    for energies in casos:
        value = float(ResonanceLogic.compute(energies))

        assert math.isfinite(value)
        assert 0.0 <= value <= 1.0 + 1e-9


def test_t12_resonancia_determinista():
    """T12 — la misma entrada produce exactamente la misma salida."""
    energies = [0.25, 0.5, 0.75, 1.0]

    a = ResonanceLogic.compute(energies)
    b = ResonanceLogic.compute(energies)

    assert a == pytest.approx(b)


# ===============================================================
# T13 — METACONCIENCIA
# ===============================================================


def test_t13_mc_l3_cero():
    """T13 — L3=0 elimina la metaconciencia."""
    activations = [1.0] * 7
    frictions = [0.0] * 7

    activations[3] = 0.0

    value = MetaconsciousnessCalculator.compute(
        activations,
        frictions,
    )

    assert value == pytest.approx(0.0)


def test_t13_mc_l4_cero():
    """T13 — L4=0 elimina la metaconciencia."""
    activations = [1.0] * 7
    frictions = [0.0] * 7

    activations[4] = 0.0

    value = MetaconsciousnessCalculator.compute(
        activations,
        frictions,
    )

    assert value == pytest.approx(0.0)


def test_t13_mc_l5_cero():
    """T13 — L5=0 elimina la metaconciencia."""
    activations = [1.0] * 7
    frictions = [0.0] * 7

    activations[5] = 0.0

    value = MetaconsciousnessCalculator.compute(
        activations,
        frictions,
    )

    assert value == pytest.approx(0.0)


def test_t13_mc_l6_cero():
    """T13 — L6=0 elimina la metaconciencia."""
    activations = [1.0] * 7
    frictions = [0.0] * 7

    activations[6] = 0.0

    value = MetaconsciousnessCalculator.compute(
        activations,
        frictions,
    )

    assert value == pytest.approx(0.0)


def test_t13_mc_producto_real():
    """T13 — la fórmula corresponde al producto L3..L6 por R_FIN."""
    activations = [0.0, 0.0, 0.0, 0.8, 0.7, 0.6, 0.9]
    frictions = [0.0, 0.0, 0.0, 0.1, 0.2, 0.3, 0.4]

    expected = (
        activations[3] * (1.0 - frictions[3])
        * activations[4] * (1.0 - frictions[4])
        * activations[5] * (1.0 - frictions[5])
        * activations[6] * (1.0 - frictions[6])
        * R_FIN
    )

    value = MetaconsciousnessCalculator.compute(
        activations,
        frictions,
    )

    assert value == pytest.approx(expected)


def test_t13_mc_fraccion_cero():
    """T13 — fricción total en cualquier capa L3-L6 anula su contribución."""
    activations = [1.0] * 7
    frictions = [0.0] * 7

    for index in range(3, 7):
        local_frictions = list(frictions)
        local_frictions[index] = 1.0

        value = MetaconsciousnessCalculator.compute(
            activations,
            local_frictions,
        )

        assert value == pytest.approx(0.0)


def test_t13_mc_no_depende_de_l0_l1_l2():
    """T13 — L0-L2 no forman parte del producto de metaconciencia."""
    activations_a = [0.1, 0.2, 0.3, 0.8, 0.7, 0.6, 0.9]
    activations_b = [0.9, 0.8, 0.7, 0.8, 0.7, 0.6, 0.9]

    frictions = [0.1] * 7

    a = MetaconsciousnessCalculator.compute(
        activations_a,
        frictions,
    )

    b = MetaconsciousnessCalculator.compute(
        activations_b,
        frictions,
    )

    assert a == pytest.approx(b)


def test_t13_mc_determinismo():
    """T13 — la misma entrada produce el mismo resultado."""
    activations = [0.2, 0.4, 0.6, 0.8, 0.7, 0.5, 0.9]
    frictions = [0.1, 0.1, 0.2, 0.1, 0.2, 0.3, 0.1]

    a = MetaconsciousnessCalculator.compute(
        activations,
        frictions,
    )

    b = MetaconsciousnessCalculator.compute(
        activations,
        frictions,
    )

    assert a == pytest.approx(b)


def test_t13_mc_niveles_coherentes():
    """T13 — level y level_name son consistentes con el valor calculado."""
    casos = (
        0.0,
        0.1,
        0.3,
        0.5,
        0.7,
        1.0,
    )

    for value in casos:
        level = MetaconsciousnessCalculator.level(value)
        name = MetaconsciousnessCalculator.level_name(value)

        assert level in (0, 1, 2, 3)
        assert isinstance(name, str)
        assert name


# ===============================================================
# T17 — INTERACCIÓN EXTERNA
# ===============================================================


def test_t17_love_es_suma():
    """T17 — θ=0 equivale a suma directa."""
    casos = (
        (0.3, 0.4),
        (0.0, 1.0),
        (0.75, 0.25),
        (1.2, 0.8),
    )

    for c1, c2 in casos:
        assert ExternalInteraction.love(c1, c2) == pytest.approx(
            c1 + c2
        )


def test_t17_conflict_es_diferencia_absoluta():
    """T17 — θ=π equivale a diferencia absoluta."""
    casos = (
        (0.3, 0.4),
        (0.8, 0.2),
        (0.2, 0.8),
        (1.0, 1.0),
    )

    for c1, c2 in casos:
        assert ExternalInteraction.conflict(c1, c2) == pytest.approx(
            abs(c1 - c2)
        )


def test_t17_independence_es_norma_euclidiana():
    """T17 — θ=π/2 equivale a √(c1²+c2²)."""
    casos = (
        (3.0, 4.0),
        (0.0, 1.0),
        (1.0, 0.0),
        (0.5, 0.5),
    )

    for c1, c2 in casos:
        expected = math.sqrt(c1 ** 2 + c2 ** 2)

        assert ExternalInteraction.independence(c1, c2) == pytest.approx(
            expected
        )


def test_t17_compute_pair_reproduce_casos_especiales():
    """T17 — compute_pair respeta los tres ángulos fundamentales."""
    c1, c2 = 0.3, 0.4

    assert ExternalInteraction.compute_pair(
        c1,
        c2,
        0.0,
    ) == pytest.approx(
        ExternalInteraction.love(c1, c2)
    )

    assert ExternalInteraction.compute_pair(
        c1,
        c2,
        math.pi,
    ) == pytest.approx(
        ExternalInteraction.conflict(c1, c2)
    )

    assert ExternalInteraction.compute_pair(
        c1,
        c2,
        math.pi / 2,
    ) == pytest.approx(
        ExternalInteraction.independence(c1, c2)
    )


def test_t17_compute_pair_ley_del_coseno():
    """T17 — compute_pair satisface la ley general del coseno."""
    casos = (
        (0.2, 0.7, 0.3),
        (0.5, 0.4, 1.1),
        (1.0, 0.3, 2.0),
        (0.8, 0.6, math.pi / 3),
    )

    for c1, c2, theta in casos:
        expected = math.sqrt(
            c1 ** 2
            + c2 ** 2
            + 2.0 * c1 * c2 * math.cos(theta)
        )

        value = ExternalInteraction.compute_pair(
            c1,
            c2,
            theta,
        )

        assert value == pytest.approx(expected)


def test_t17_compute_pair_simetria():
    """T17 — intercambiar las coherencias no cambia el resultado."""
    casos = (
        (0.2, 0.7, 0.2),
        (0.5, 0.3, 1.0),
        (0.9, 0.1, math.pi / 3),
    )

    for c1, c2, theta in casos:
        a = ExternalInteraction.compute_pair(c1, c2, theta)
        b = ExternalInteraction.compute_pair(c2, c1, theta)

        assert a == pytest.approx(b)


def test_t17_compute_multi_vacio():
    """T17 — colección vacía produce ausencia de interacción."""
    assert ExternalInteraction.compute_multi([]) == pytest.approx(0.0)


def test_t17_compute_multi_escalar_unico():
    """T17 — un escalar conserva su valor."""
    for value in (0.0, 0.2, 0.75, 1.0):
        assert ExternalInteraction.compute_multi([value]) == pytest.approx(
            value
        )


def test_t17_compute_multi_suma_acumulativa():
    """T17 — múltiples escalares se combinan mediante θ=0."""
    values = [0.2, 0.3, 0.5]

    result = ExternalInteraction.compute_multi(values)

    assert result == pytest.approx(sum(values))


def test_t17_compute_multi_determinismo():
    """T17 — misma colección produce mismo resultado."""
    values = [
        (0.3, 0.4),
        (0.2, 0.1, math.pi / 3),
        0.25,
    ]

    a = ExternalInteraction.compute_multi(values)
    b = ExternalInteraction.compute_multi(values)

    assert a == pytest.approx(b)


# ===============================================================
# INTEGRIDAD NUMÉRICA TRANSVERSAL
# ===============================================================


@pytest.mark.parametrize(
    "fn,args",
    [
        (
            ResonanceLogic.compute,
            ([0.2, 0.4, 0.6, 0.8],),
        ),
        (
            MetaconsciousnessCalculator.compute,
            (
                [0.2, 0.4, 0.6, 0.8, 0.7, 0.5, 0.9],
                [0.1, 0.1, 0.2, 0.1, 0.2, 0.3, 0.1],
            ),
        ),
        (
            ExternalInteraction.compute_multi,
            ([0.2, 0.3, 0.4],),
        ),
    ],
)
def test_formulas_omega_resultados_finitos(fn, args):
    """Todas las fórmulas unitarias producen resultados numéricos finitos."""
    value = fn(*args)

    assert isinstance(value, (int, float))
    assert math.isfinite(float(value))
