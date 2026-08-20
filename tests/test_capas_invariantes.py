# tests/test_capas_invariantes.py
# T04–T06, T09: capas e integridad anti-circularidad

from __future__ import annotations

import pytest

from core.engine import (
    AntiHackValidation,
    PurposeAlignmentError,
    StructuralIntegrityError,
    CircularityDetectedError,
)


def _capas_ok(phi6: float = 0.0):
    return [
        {"L": 0.8, "phi": 0.1}
        for _ in range(6)
    ] + [
        {"L": 0.9, "phi": phi6}
    ]


def test_t04_exige_numero_de_capas():
    """T04 — número de capas distinto del canónico → error."""
    from core.engine import AntiHackValidation, StructuralIntegrityError

    try:
        from modules.formulas.formulas_omega.constants import NUM_LAYERS
        n = int(NUM_LAYERS)
    except Exception:
        n = 7

    capas_cortas = [{"L": 1.0, "phi": 0.0} for _ in range(max(1, n - 1))]

    with pytest.raises((ValueError, StructuralIntegrityError, TypeError, KeyError)):
        AntiHackValidation.validate_layer_data(capas_cortas)


def test_t05_L_fuera_de_dominio():
    """T05 — L fuera de [0,1] debe rechazarse."""
    for valor in (-0.1, 1.1):
        mal = _capas_ok()
        mal[0]["L"] = valor

        with pytest.raises(StructuralIntegrityError):
            AntiHackValidation.validate_layer_data(mal)


def test_t05_phi_fuera_de_dominio():
    """T05 — phi fuera de [0,1] debe rechazarse."""
    for valor in (-0.1, 1.1):
        mal = _capas_ok()
        mal[0]["phi"] = valor

        with pytest.raises(StructuralIntegrityError):
            AntiHackValidation.validate_layer_data(mal)


def test_t06_l6_phi_cero():
    """T06 — L6 con phi != 0 debe rechazarse."""
    mal = _capas_ok(phi6=0.2)

    with pytest.raises(PurposeAlignmentError):
        AntiHackValidation.validate_layer_data(mal)


def test_t06_l6_phi_cero_ok():
    """T06 — L6 con phi = 0 debe aceptarse."""
    AntiHackValidation.validate_layer_data(
        _capas_ok(phi6=0.0)
    )


def test_t09_circularidad_c_omega_truth():
    """T09 — C_Ω ≈ Truth en estado intermedio debe rechazarse."""
    with pytest.raises(CircularityDetectedError):
        AntiHackValidation.detect_formula_circularity(
            0.55,
            0.55,
        )
