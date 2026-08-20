# ===============================================================
# VPSI-TRUTH — tests/test_yo_oscilatorio_dinamico_FO.py
# ===============================================================

import math
import pytest

from modules.formulas.formulas_omega.yo_oscilatorio_dinamico_FO import (
    NUM_LAYERS_YO,
    S_MAX,
    YoOscilatorioEngine,
    SessionStateYoOscilatorio,
)


def test_l4_yo_oscilatorio_contrato_completo():
    """Auditoría compacta del contrato matemático L4: L1..L6 internas, L0 externo y L7 emergente."""

    # -----------------------------------------------------------
    # DOMINIO
    # -----------------------------------------------------------
    assert NUM_LAYERS_YO == 6
    assert math.isclose(S_MAX, math.log(6), rel_tol=1e-12)

    activations = [0.20, 0.30, 0.40, 0.50, 0.60, 0.70]
    frictions = [0.10, 0.02, 0.05, 0.03, 0.01, 0.90]

    # φ6 debe quedar forzada a cero aunque entre otro valor.
    energies, weights = YoOscilatorioEngine.compute_energies_and_weights(
        activations, frictions
    )

    assert len(energies) == 6
    assert len(weights) == 6
    assert math.isclose(sum(weights), 1.0, rel_tol=1e-12)
    assert weights[5] > 0.0

    # -----------------------------------------------------------
    # f_i DOCUMENTAL
    # -----------------------------------------------------------
    contributions = YoOscilatorioEngine.compute_contributions(
        weights, activations, energies, frictions
    )

    assert len(contributions) == 6
    assert all(x >= 0.0 for x in contributions)

    # -----------------------------------------------------------
    # ENTROPÍA Y AMORTIGUAMIENTO
    # -----------------------------------------------------------
    entropy = YoOscilatorioEngine.compute_entropy(weights)
    damping = YoOscilatorioEngine.compute_damping_and_frequency(
        weights, frictions
    )

    assert 0.0 <= entropy["s"] <= math.log(6)
    assert 0.0 <= entropy["s_norm"] <= 1.0
    assert math.isclose(
        entropy["negentropy"], 1.0 - entropy["s_norm"], rel_tol=1e-12
    )

    # φ6 = 0: cambiar únicamente la fricción suministrada de L6
    # no puede modificar φY.
    frictions_l6_alt = frictions.copy()
    frictions_l6_alt[5] = 999.0

    damping_alt = YoOscilatorioEngine.compute_damping_and_frequency(
        weights, frictions_l6_alt
    )

    assert math.isclose(
        damping["phi_Y"], damping_alt["phi_Y"], rel_tol=1e-12
    )

    assert damping["zeta_Y"] >= 0.0
    assert damping["omega_Y"] >= 0.0
    assert damping["regime"] in {"SUBDAMPED", "CRITICAL", "OVERDAMPED"}

    # -----------------------------------------------------------
    # EQUILIBRIO DINÁMICO
    # -----------------------------------------------------------
    geometry = YoOscilatorioEngine.compute_theta_eq(
        c_omega=0.5,
        weights=weights,
    )

    assert "theta_eq" in geometry
    assert "delta_theta_coh" in geometry
    assert "delta_theta_w" in geometry
    assert "theta_cube" in geometry

    # -----------------------------------------------------------
    # FUERZAS
    # L0 entra como escalar independiente, nunca como activación.
    # -----------------------------------------------------------
    forces = YoOscilatorioEngine.compute_forces(
        l0_input=0.25,
        weights=weights,
        c_omega=0.5,
        delta_c_omega=0.1,
        entropy_s=entropy["s"],
        purpose_p=0.8,
        novelty=1.0,
    )

    assert set(
        ["f_total", "f_l0", "f_l5", "f_l6", "f_beta", "f_coh"]
    ).issubset(forces)

    assert math.isclose(forces["f_l0"], 0.25, rel_tol=1e-12)
    assert forces["f_l6"] >= 0.0

    # -----------------------------------------------------------
    # PASO EULER SEMI-IMPLÍCITO
    # -----------------------------------------------------------
    result = YoOscilatorioEngine.step(
        theta_Y=0.0,
        theta_dot_Y=0.0,
        activations=activations,
        l0_input=0.25,
        c_omega=0.5,
        delta_c_omega=0.1,
        frictions=frictions,
        purpose_p=0.8,
        novelty=1.0,
        dt=0.01,
    )

    for key in (
        "theta_Y",
        "theta_dot_Y",
        "theta_ddot_Y",
        "energies",
        "weights",
        "contributions_f_i",
        "entropy",
        "damping",
        "geometry",
        "forces",
    ):
        assert key in result

    assert len(result["energies"]) == 6
    assert len(result["weights"]) == 6
    assert len(result["contributions_f_i"]) == 6

    expected_velocity = result["theta_ddot_Y"] * 0.01
    expected_theta = expected_velocity * 0.01

    assert math.isclose(
        result["theta_dot_Y"], expected_velocity, rel_tol=1e-12
    )
    assert math.isclose(
        result["theta_Y"], expected_theta, rel_tol=1e-12
    )

    # -----------------------------------------------------------
    # VECTOR CERO → PESOS UNIFORMES
    # -----------------------------------------------------------
    zero_energies, zero_weights = YoOscilatorioEngine.compute_energies_and_weights(
        [0.0] * 6
    )

    assert zero_energies == [0.0] * 6
    assert zero_weights == [1.0 / 6.0] * 6

    # -----------------------------------------------------------
    # L6: purpose_p actúa mediante w6
    # -----------------------------------------------------------
    no_purpose = YoOscilatorioEngine.compute_forces(
        l0_input=0.0,
        weights=weights,
        c_omega=0.0,
        delta_c_omega=0.0,
        entropy_s=entropy["s"],
        purpose_p=0.0,
        novelty=0.0,
    )

    with_purpose = YoOscilatorioEngine.compute_forces(
        l0_input=0.0,
        weights=weights,
        c_omega=0.0,
        delta_c_omega=0.0,
        entropy_s=entropy["s"],
        purpose_p=1.0,
        novelty=0.0,
    )

    assert math.isclose(
        with_purpose["f_l6"] - no_purpose["f_l6"],
        weights[5],
        rel_tol=1e-12,
    )

    # -----------------------------------------------------------
    # VALIDACIONES DE CONTRATO
    # -----------------------------------------------------------
    with pytest.raises(ValueError):
        YoOscilatorioEngine.step(
            theta_Y=0.0,
            theta_dot_Y=0.0,
            activations=[0.0] * 7,
            l0_input=0.0,
            c_omega=0.0,
            delta_c_omega=0.0,
        )

    with pytest.raises(ValueError):
        YoOscilatorioEngine.step(
            theta_Y=0.0,
            theta_dot_Y=0.0,
            activations=[0.0] * 6,
            l0_input=0.0,
            c_omega=0.0,
            delta_c_omega=0.0,
            dt=0.0,
        )

    # -----------------------------------------------------------
    # SESIÓN: ΔCΩ se calcula temporalmente
    # -----------------------------------------------------------
    session = SessionStateYoOscilatorio()

    first = session.update(
        activations=[0.0] * 6,
        l0_input=0.0,
        c_omega=0.4,
        dt=0.01,
    )

    second = session.update(
        activations=[0.0] * 6,
        l0_input=0.0,
        c_omega=0.6,
        dt=0.01,
    )

    assert first["forces"]["f_coh"] == 0.0
    assert second["forces"]["f_coh"] != 0.0
    assert len(session.history) == 2
    assert len(session.trajectory()) == 2
    assert len(session.velocity_trajectory()) == 2
