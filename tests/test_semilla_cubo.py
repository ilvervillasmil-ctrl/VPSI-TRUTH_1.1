# tests/test_semilla_cubo.py
# T03, T07, T08: semilla estructural y Fórmula de la Verdad

from __future__ import annotations

from fractions import Fraction

import pytest

from modules.constante import ALPHA, BETA
from modules.formulas.truth import tru_ri, tru_total


def test_t03_alpha_beta_suman_uno():
    """T03 — α + β = 1: conservación completa del cubo."""
    assert isinstance(ALPHA, Fraction)
    assert isinstance(BETA, Fraction)
    assert ALPHA + BETA == Fraction(1, 1)


def test_t03_alpha_beta_valores_cubo():
    """T03 — α = 26/27 y β = 1/27."""
    assert ALPHA == Fraction(26, 27)
    assert BETA == Fraction(1, 27)


def test_t08_truth_formula_piso():
    """T08 — C=L=K=0 produce exactamente β."""
    resultado = tru_total(
        Fraction(0),
        Fraction(0),
        Fraction(0),
    )

    assert resultado == BETA


def test_t08_truth_formula_techo():
    """T08 — C=L=K=1 produce exactamente 1."""
    resultado = tru_total(
        Fraction(1),
        Fraction(1),
        Fraction(1),
    )

    assert resultado == Fraction(1, 1)


def test_t08_truth_ri():
    """T08 — Tru_Ri = C × L × K."""
    resultado = tru_ri(
        Fraction(1, 2),
        Fraction(3, 4),
        Fraction(2, 3),
    )

    assert resultado == Fraction(1, 4)


def test_t08_truth_formula_completa():
    """T08 — Tru_total = (C × L × K × α) + β."""
    C = Fraction(1, 2)
    L = Fraction(3, 4)
    K = Fraction(2, 3)

    esperado = (
        C * L * K * ALPHA
    ) + BETA

    resultado = tru_total(C, L, K)

    assert resultado == esperado


def test_t08_truth_dentro_del_rango():
    """T08 — para C,L,K ∈ [0,1], Truth permanece en [β,1]."""
    casos = [
        (Fraction(0), Fraction(0), Fraction(0)),
        (Fraction(1, 2), Fraction(1), Fraction(1)),
        (Fraction(1), Fraction(1, 2), Fraction(1)),
        (Fraction(1), Fraction(1), Fraction(1, 2)),
        (Fraction(1), Fraction(1), Fraction(1)),
    ]

    for C, L, K in casos:
        resultado = tru_total(C, L, K)

        assert BETA <= resultado <= Fraction(1, 1)
