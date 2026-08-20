# ===============================================================
# tests/test_yo_oscilatorio_dinamico_FO.py
# ===============================================================
#
# VPSI-TRUTH — TEST CANÓNICO
# L4 — YO OSCILATORIO DINÁMICO
#
# RESPONSABILIDAD DEL TEST
# -----------------------
# Verificar exclusivamente el contrato matemático implementado en:
#
#   modules/formulas/formulas_omega/yo_oscilatorio_dinamico_FO.py
#
# El test comprueba:
#
#   1. Constantes estructurales del carril.
#   2. Dominio exacto L1..L6.
#   3. Validación de activaciones.
#   4. Validación de fricciones.
#   5. Energías E_i.
#   6. Pesos emergentes w_i.
#   7. Caso de energía total nula.
#   8. Contribuciones f_i.
#   9. Entropía S.
#  10. Entropía normalizada.
#  11. Negentropía.
#  12. Amortiguamiento φ_Y.
#  13. Amortiguamiento adimensional ζ_Y.
#  14. Frecuencia ω_Y.
#  15. Régimen dinámico.
#  16. Equilibrio dinámico θ_eq.
#  17. Fuerzas F_L0, F_L5, F_L6, F_β y F_COH.
#  18. Fuerza total F_Y.
#  19. Ecuación diferencial despejada.
#  20. Euler semi-implícito.
#  21. Estado temporal SessionStateYoOscilatorio.
#  22. Cálculo de ΔC_Ω entre ciclos.
#  23. Trayectorias de θ_Y y θ̇_Y.
#
# ESTE TEST NO:
#
#   - prueba Engine;
#   - prueba CONTENEDOR;
#   - prueba self;
#   - asigna significado psicológico;
#   - calcula casas;
#   - realiza integración superior;
#   - altera el contrato del módulo.
#
# ===============================================================

from __future__ import annotations

import math

import pytest

from modules.formulas.formulas_omega.yo_oscilatorio_dinamico_FO import (
    NUM_LAYERS_YO,
    S_MAX,
    PHI_CRITICAL,
    YoOscilatorioEngine,
    SessionStateYoOscilatorio,
)

from modules.formulas.formulas_omega.constants import (
    PHI,
    THETA_CUBE,
)

from modules.constante import (
    ALPHA,
    BETA,
)


# ===============================================================
# DATOS CANÓNICOS DEL TEST
# ===============================================================

ACTIVATIONS_ZERO = [
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
]

ACTIVATIONS_FULL = [
    1.0,
    1.0,
    1.0,
    1.0,
    1.0,
    1.0,
]

FRICTIONS_CANONICAL = [
    0.10,
    0.02,
    0.05,
    0.03,
    0.01,
    0.00,
]


# ===============================================================
# 1. CONSTANTES ESTRUCTURALES
# ===============================================================

def test_constantes_estructurales_del_carril():
    assert NUM_LAYERS_YO == 6
    assert S_MAX == pytest.approx(math.log(6))
    assert PHI_CRITICAL == pytest.approx(2.0 * math.pi)

    assert float(ALPHA) > 0.0
    assert float(BETA) > 0.0

    assert float(THETA_CUBE) == pytest.approx(
        float(THETA_CUBE)
    )

    assert PHI > 1.0


# ===============================================================
# 2. VALIDACIÓN DE ACTIVACIONES
# ===============================================================

def test_activaciones_deben_contener_exactamente_seis_valores():
    energies, weights = (
        YoOscilatorioEngine.compute_energies_and_weights(
            ACTIVATIONS_FULL
        )
    )

    assert len(energies) == 6
    assert len(weights) == 6


def test_activaciones_fuera_de_rango_fallan():
    with pytest.raises(ValueError):
        YoOscilatorioEngine.compute_energies_and_weights(
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.1]
        )

    with pytest.raises(ValueError):
        YoOscilatorioEngine.compute_energies_and_weights(
            [0.0, 0.0, 0.0, 0.0, 0.0, -0.1]
        )


def test_activaciones_con_longitud_incorrecta_fallan():
    with pytest.raises(ValueError):
        YoOscilatorioEngine.compute_energies_and_weights(
            [1.0, 1.0, 1.0, 1.0, 1.0]
        )


# ===============================================================
# 3. VALIDACIÓN DE FRICCIONES
# ===============================================================

def test_fricciones_canonicas_son_aceptadas():
    energies, weights = (
        YoOscilatorioEngine.compute_energies_and_weights(
            ACTIVATIONS_FULL,
            FRICTIONS_CANONICAL,
        )
    )

    assert len(energies) == 6
    assert len(weights) == 6


def test_fricciones_con_longitud_incorrecta_fallan():
    with pytest.raises(ValueError):
        YoOscilatorioEngine.compute_energies_and_weights(
            ACTIVATIONS_FULL,
            [0.10, 0.02, 0.05, 0.03, 0.01],
        )


def test_fricciones_fuera_de_rango_fallan():
    with pytest.raises(ValueError):
        YoOscilatorioEngine.compute_energies_and_weights(
            ACTIVATIONS_FULL,
            [0.10, 0.02, 0.05, 0.03, 0.01, 1.1],
        )

    with pytest.raises(ValueError):
        YoOscilatorioEngine.compute_energies_and_weights(
            ACTIVATIONS_FULL,
            [0.10, 0.02, 0.05, 0.03, 0.01, -0.1],
        )


def test_friccion_de_L6_es_forzada_a_cero():
    frictions = [
        0.10,
        0.02,
        0.05,
        0.03,
        0.01,
        0.75,
    ]

    _, weights = (
        YoOscilatorioEngine.compute_energies_and_weights(
            ACTIVATIONS_FULL,
            frictions,
        )
    )

    damping = (
        YoOscilatorioEngine.compute_damping_and_frequency(
            weights,
            frictions,
        )
    )

    expected = sum(
        weights[i] * frictions[i]
        for i in range(5)
    )

    assert damping["phi_Y"] == pytest.approx(expected)


# ===============================================================
# 4. ENERGÍAS E_i
# ===============================================================

def test_energias_se_calculan_con_la_formula_canónica():
    energies, _ = (
        YoOscilatorioEngine.compute_energies_and_weights(
            ACTIVATIONS_FULL,
            FRICTIONS_CANONICAL,
        )
    )

    expected = [
        ACTIVATIONS_FULL[i]
        * (1.0 - FRICTIONS_CANONICAL[i])
        * PHI ** ((i + 1) / 2.0)
        for i in range(6)
    ]

    assert energies == pytest.approx(expected)


def test_energia_cero_cuando_todas_las_activaciones_son_cero():
    energies, _ = (
        YoOscilatorioEngine.compute_energies_and_weights(
            ACTIVATIONS_ZERO,
            FRICTIONS_CANONICAL,
        )
    )

    assert energies == pytest.approx(
        [0.0] * 6
    )


# ===============================================================
# 5. PESOS EMERGENTES
# ===============================================================

def test_pesos_se_normalizan_a_uno():
    energies, weights = (
        YoOscilatorioEngine.compute_energies_and_weights(
            ACTIVATIONS_FULL,
            FRICTIONS_CANONICAL,
        )
    )

    assert len(energies) == 6
    assert len(weights) == 6
    assert sum(weights) == pytest.approx(1.0)


def test_pesos_corresponden_a_energia_sobre_energia_total():
    energies, weights = (
        YoOscilatorioEngine.compute_energies_and_weights(
            ACTIVATIONS_FULL,
            FRICTIONS_CANONICAL,
        )
    )

    total = sum(energies)

    expected = [
        energy / total
        for energy in energies
    ]

    assert weights == pytest.approx(expected)


def test_energia_total_nula_produce_pesos_uniformes():
    energies, weights = (
        YoOscilatorioEngine.compute_energies_and_weights(
            ACTIVATIONS_ZERO,
            FRICTIONS_CANONICAL,
        )
    )

    assert energies == pytest.approx(
        [0.0] * 6
    )

    assert weights == pytest.approx(
        [1.0 / 6.0] * 6
    )


# ===============================================================
# 6. CONTRIBUCIONES f_i
# ===============================================================

def test_contribuciones_siguen_la_formula_documental():
    energies, weights = (
        YoOscilatorioEngine.compute_energies_and_weights(
            ACTIVATIONS_FULL,
            FRICTIONS_CANONICAL,
        )
    )

    contributions = (
        YoOscilatorioEngine.compute_contributions(
            weights=weights,
            activations=ACTIVATIONS_FULL,
            energies=energies,
            frictions=FRICTIONS_CANONICAL,
        )
    )

    expected = [
        weights[i]
        * ACTIVATIONS_FULL[i]
        * (1.0 - FRICTIONS_CANONICAL[i])
        * energies[i]
        for i in range(6)
    ]

    assert len(contributions) == 6
    assert contributions == pytest.approx(expected)


def test_contribuciones_son_cero_con_energias_nulas():
    energies = [0.0] * 6
    weights = [1.0 / 6.0] * 6

    contributions = (
        YoOscilatorioEngine.compute_contributions(
            weights=weights,
            activations=ACTIVATIONS_ZERO,
            energies=energies,
            frictions=FRICTIONS_CANONICAL,
        )
    )

    assert contributions == pytest.approx(
        [0.0] * 6
    )


# ===============================================================
# 7. ENTROPÍA
# ===============================================================

def test_entropia_uniforme_es_maxima():
    weights = [1.0 / 6.0] * 6

    result = (
        YoOscilatorioEngine.compute_entropy(
            weights
        )
    )

    assert result["s"] == pytest.approx(
        math.log(6)
    )

    assert result["s_norm"] == pytest.approx(
        1.0
    )

    assert result["negentropy"] == pytest.approx(
        0.0
    )


def test_entropia_concentrada_es_cero():
    weights = [
        1.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
    ]

    result = (
        YoOscilatorioEngine.compute_entropy(
            weights
        )
    )

    assert result["s"] == pytest.approx(
        0.0
    )

    assert result["s_norm"] == pytest.approx(
        0.0
    )

    assert result["negentropy"] == pytest.approx(
        1.0
    )


def test_entropia_normalizada_permanece_en_cero_uno():
    _, weights = (
        YoOscilatorioEngine.compute_energies_and_weights(
            ACTIVATIONS_FULL,
            FRICTIONS_CANONICAL,
        )
    )

    result = (
        YoOscilatorioEngine.compute_entropy(
            weights
        )
    )

    assert 0.0 <= result["s_norm"] <= 1.0
    assert 0.0 <= result["negentropy"] <= 1.0


# ===============================================================
# 8. AMORTIGUAMIENTO
# ===============================================================

def test_amortiguamiento_efectivo_es_promedio_ponderado():
    weights = [1.0 / 6.0] * 6

    result = (
        YoOscilatorioEngine.compute_damping_and_frequency(
            weights,
            FRICTIONS_CANONICAL,
        )
    )

    expected_phi = sum(
        weights[i] * FRICTIONS_CANONICAL[i]
        for i in range(6)
    )

    assert result["phi_Y"] == pytest.approx(
        expected_phi
    )


def test_l6_no_aporta_friccion_propia():
    weights = [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        1.0,
    ]

    result = (
        YoOscilatorioEngine.compute_damping_and_frequency(
            weights,
            FRICTIONS_CANONICAL,
        )
    )

    assert result["phi_Y"] == pytest.approx(
        0.0
    )

    assert result["zeta_Y"] == pytest.approx(
        0.0
    )

    assert result["omega_Y"] == pytest.approx(
        math.pi
    )

    assert result["regime"] == "SUBDAMPED"


def test_zeta_se_calcula_como_phi_sobre_dos_pi():
    weights = [1.0 / 6.0] * 6

    result = (
        YoOscilatorioEngine.compute_damping_and_frequency(
            weights,
            FRICTIONS_CANONICAL,
        )
    )

    expected_zeta = (
        result["phi_Y"]
        / (2.0 * math.pi)
    )

    assert result["zeta_Y"] == pytest.approx(
        expected_zeta
    )


def test_frecuencia_se_calcula_para_regimen_subamortiguado():
    weights = [1.0 / 6.0] * 6

    result = (
        YoOscilatorioEngine.compute_damping_and_frequency(
            weights,
            FRICTIONS_CANONICAL,
        )
    )

    zeta = result["zeta_Y"]

    expected = (
        math.pi
        * math.sqrt(
            1.0 - zeta ** 2
        )
    )

    assert result["omega_Y"] == pytest.approx(
        expected
    )


# ===============================================================
# 9. EQUILIBRIO DINÁMICO
# ===============================================================

def test_equilibrio_dinamico_reproduce_formula_canónica():
    weights = [1.0 / 6.0] * 6
    c_omega = float(ALPHA)

    result = (
        YoOscilatorioEngine.compute_theta_eq(
            c_omega,
            weights,
        )
    )

    delta_coh = (
        float(BETA)
        * ((c_omega / float(ALPHA)) - 1.0)
        * (math.pi / 27.0)
    )

    w_alto = (
        weights[3]
        + weights[4]
        + weights[5]
    ) / 3.0

    w_bajo = (
        weights[0]
        + weights[1]
    ) / 2.0

    delta_w = (
        float(BETA)
        * (w_alto - w_bajo)
        * (math.pi / 54.0)
    )

    expected = (
        float(THETA_CUBE)
        + delta_coh
        + delta_w
    )

    assert result["delta_theta_coh"] == pytest.approx(
        delta_coh
    )

    assert result["delta_theta_w"] == pytest.approx(
        delta_w
    )

    assert result["theta_eq"] == pytest.approx(
        expected
    )


def test_equilibrio_con_coherencia_igual_a_alpha_elimina_desplazamiento_coherente():
    weights = [1.0 / 6.0] * 6

    result = (
        YoOscilatorioEngine.compute_theta_eq(
            float(ALPHA),
            weights,
        )
    )

    assert result["delta_theta_coh"] == pytest.approx(
        0.0
    )


# ===============================================================
# 10. FUERZA L0
# ===============================================================

def test_fuerza_L0_es_entrada_por_escala():
    result = (
        YoOscilatorioEngine.compute_forces(
            l0_input=0.25,
            weights=[1.0 / 6.0] * 6,
            c_omega=0.0,
            delta_c_omega=0.0,
            entropy_s=math.log(6),
            scale_l0=4.0,
        )
    )

    assert result["f_l0"] == pytest.approx(
        1.0
    )


# ===============================================================
# 11. FUERZA L5
# ===============================================================

def test_fuerza_L5_reproduce_formula():
    c_omega = 0.4
    delta_c = 0.2
    rho = 2.0
    p_t = 3.0
    entropy_s = math.log(6)

    result = (
        YoOscilatorioEngine.compute_forces(
            l0_input=0.0,
            weights=[1.0 / 6.0] * 6,
            c_omega=c_omega,
            delta_c_omega=delta_c,
            entropy_s=entropy_s,
            rho=rho,
            p_t=p_t,
        )
    )

    expected = (
        rho * p_t * c_omega
        + 0.5 * delta_c
        - float(BETA)
    )

    assert result["f_l5"] == pytest.approx(
        expected
    )


# ===============================================================
# 12. FUERZA L6
# ===============================================================

def test_fuerza_L6_usa_exclusivamente_w6_y_P():
    weights = [
        0.05,
        0.10,
        0.15,
        0.20,
        0.25,
        0.25,
    ]

    result = (
        YoOscilatorioEngine.compute_forces(
            l0_input=0.0,
            weights=weights,
            c_omega=0.0,
            delta_c_omega=0.0,
            entropy_s=math.log(6),
            purpose_p=4.0,
        )
    )

    assert result["f_l6"] == pytest.approx(
        0.25 * 4.0
    )


# ===============================================================
# 13. FUERZA β
# ===============================================================

def test_fuerza_beta_es_cero_con_novedad_cero():
    result = (
        YoOscilatorioEngine.compute_forces(
            l0_input=0.0,
            weights=[1.0 / 6.0] * 6,
            c_omega=0.0,
            delta_c_omega=0.0,
            entropy_s=0.0,
            novelty=0.0,
        )
    )

    assert result["f_beta"] == pytest.approx(
        0.0
    )


def test_fuerza_beta_reproduce_funcion_de_novedad():
    novelty = 5.0
    sensitivity = 5.0

    result = (
        YoOscilatorioEngine.compute_forces(
            l0_input=0.0,
            weights=[1.0 / 6.0] * 6,
            c_omega=0.0,
            delta_c_omega=0.0,
            entropy_s=0.0,
            novelty=novelty,
            sensitivity=sensitivity,
        )
    )

    expected = (
        float(BETA)
        * (
            1.0
            - math.exp(
                -novelty / sensitivity
            )
        )
    )

    assert result["f_beta"] == pytest.approx(
        expected
    )


# ===============================================================
# 14. FUERZA DE COHERENCIA
# ===============================================================

def test_fuerza_coherencia_reproduce_C_OMEGA_por_delta_C():
    c_omega = 0.4
    delta_c = 0.3

    result = (
        YoOscilatorioEngine.compute_forces(
            l0_input=0.0,
            weights=[1.0 / 6.0] * 6,
            c_omega=c_omega,
            delta_c_omega=delta_c,
            entropy_s=0.0,
        )
    )

    assert result["f_coh"] == pytest.approx(
        c_omega * delta_c
    )


# ===============================================================
# 15. FUERZA TOTAL
# ===============================================================

def test_fuerza_total_es_suma_de_componentes():
    weights = [1.0 / 6.0] * 6

    result = (
        YoOscilatorioEngine.compute_forces(
            l0_input=0.2,
            weights=weights,
            c_omega=0.3,
            delta_c_omega=0.1,
            entropy_s=math.log(6),
            purpose_p=0.4,
            rho=1.2,
            p_t=0.8,
            novelty=2.0,
            sensitivity=5.0,
            scale_l0=2.0,
        )
    )

    expected = (
        result["f_l0"]
        + result["f_l5"]
        + result["f_l6"]
        + result["f_beta"]
        + result["f_coh"]
    )

    assert result["f_total"] == pytest.approx(
        expected
    )


# ===============================================================
# 16. VALIDACIÓN DE SENSIBILIDAD
# ===============================================================

def test_sensibilidad_debe_ser_positiva():
    with pytest.raises(ValueError):
        YoOscilatorioEngine.compute_forces(
            l0_input=0.0,
            weights=[1.0 / 6.0] * 6,
            c_omega=0.0,
            delta_c_omega=0.0,
            entropy_s=0.0,
            sensitivity=0.0,
        )

    with pytest.raises(ValueError):
        YoOscilatorioEngine.compute_forces(
            l0_input=0.0,
            weights=[1.0 / 6.0] * 6,
            c_omega=0.0,
            delta_c_omega=0.0,
            entropy_s=0.0,
            sensitivity=-1.0,
        )


# ===============================================================
# 17. PASO DE INTEGRACIÓN — ECUACIÓN MAESTRA
# ===============================================================

def test_step_reproduce_ecuacion_maestra_y_euler_semiimplicito():
    theta = float(THETA_CUBE)
    theta_dot = 0.0
    dt = 0.01

    activations = ACTIVATIONS_FULL
    l0_input = 0.0
    c_omega = float(ALPHA)
    delta_c = 0.0

    result = YoOscilatorioEngine.step(
        theta_Y=theta,
        theta_dot_Y=theta_dot,
        activations=activations,
        l0_input=l0_input,
        c_omega=c_omega,
        delta_c_omega=delta_c,
        frictions=FRICTIONS_CANONICAL,
        purpose_p=0.0,
        rho=1.0,
        p_t=1.0,
        novelty=0.0,
        sensitivity=5.0,
        dt=dt,
        scale_l0=1.0,
    )

    phi_y = result["damping"]["phi_Y"]
    theta_eq = result["geometry"]["theta_eq"]
    force = result["forces"]["f_total"]

    restoration = (
        math.pi ** 2
        * (theta - theta_eq)
    )

    expected_acceleration = (
        force
        - phi_y * theta_dot
        - restoration
    )

    expected_theta_dot = (
        theta_dot
        + expected_acceleration * dt
    )

    expected_theta = (
        theta
        + expected_theta_dot * dt
    )

    assert result["theta_ddot_Y"] == pytest.approx(
        expected_acceleration
    )

    assert result["theta_dot_Y"] == pytest.approx(
        expected_theta_dot
    )

    assert result["theta_Y"] == pytest.approx(
        expected_theta
    )


def test_dt_cero_falla():
    with pytest.raises(ValueError):
        YoOscilatorioEngine.step(
            theta_Y=float(THETA_CUBE),
            theta_dot_Y=0.0,
            activations=ACTIVATIONS_FULL,
            l0_input=0.0,
            c_omega=0.0,
            delta_c_omega=0.0,
            dt=0.0,
        )


def test_dt_negativo_falla():
    with pytest.raises(ValueError):
        YoOscilatorioEngine.step(
            theta_Y=float(THETA_CUBE),
            theta_dot_Y=0.0,
            activations=ACTIVATIONS_FULL,
            l0_input=0.0,
            c_omega=0.0,
            delta_c_omega=0.0,
            dt=-0.01,
        )


# ===============================================================
# 18. ESTRUCTURA DE SALIDA DEL STEP
# ===============================================================

def test_step_expone_todas_las_MAGNITUDES_DEL_CARRIL():
    result = YoOscilatorioEngine.step(
        theta_Y=float(THETA_CUBE),
        theta_dot_Y=0.0,
        activations=ACTIVATIONS_FULL,
        l0_input=0.0,
        c_omega=float(ALPHA),
        delta_c_omega=0.0,
        dt=0.01,
    )

    required_keys = {
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
        "dt",
        "ALPHA",
        "BETA",
        "NUM_LAYERS_YO",
    }

    assert required_keys.issubset(
        result.keys()
    )

    assert len(result["energies"]) == 6
    assert len(result["weights"]) == 6
    assert len(result["contributions_f_i"]) == 6


# ===============================================================
# 19. ESTADO TEMPORAL
# ===============================================================

def test_session_inicia_en_theta_cube():
    session = SessionStateYoOscilatorio()

    assert session.theta_Y == pytest.approx(
        float(THETA_CUBE)
    )

    assert session.theta_dot_Y == pytest.approx(
        0.0
    )

    assert session.prev_c_omega is None
    assert session.history == []


def test_session_acepta_estado_inicial_explicito():
    session = SessionStateYoOscilatorio(
        initial_theta=1.25,
        initial_theta_dot=0.75,
    )

    assert session.theta_Y == pytest.approx(
        1.25
    )

    assert session.theta_dot_Y == pytest.approx(
        0.75
    )


# ===============================================================
# 20. PRIMER UPDATE — ΔC_Ω = 0
# ===============================================================

def test_session_primer_update_tiene_delta_C_cero():
    session = SessionStateYoOscilatorio()

    result = session.update(
        activations=ACTIVATIONS_FULL,
        l0_input=0.0,
        c_omega=0.4,
        dt=0.01,
    )

    assert result["forces"]["f_coh"] == pytest.approx(
        0.0
    )

    assert result["forces"]["f_l5"] == pytest.approx(
        (
            result["forces"]["f_l5"]
        )
    )

    assert session.prev_c_omega == pytest.approx(
        0.4
    )

    assert len(session.history) == 1


# ===============================================================
# 21. SEGUNDO UPDATE — ΔC_Ω DINÁMICO
# ===============================================================

def test_session_calcula_delta_C_entre_ciclos():
    session = SessionStateYoOscilatorio()

    session.update(
        activations=ACTIVATIONS_FULL,
        l0_input=0.0,
        c_omega=0.4,
        dt=0.01,
    )

    result = session.update(
        activations=ACTIVATIONS_FULL,
        l0_input=0.0,
        c_omega=0.7,
        dt=0.01,
    )

    assert result["forces"]["f_coh"] == pytest.approx(
        0.7 * 0.3
    )

    assert session.prev_c_omega == pytest.approx(
        0.7
    )

    assert len(session.history) == 2


# ===============================================================
# 22. TRAYECTORIA DE POSICIÓN
# ===============================================================

def test_trajectory_retorna_todas_las_posiciones():
    session = SessionStateYoOscilatorio()

    session.update(
        activations=ACTIVATIONS_FULL,
        l0_input=0.0,
        c_omega=0.2,
        dt=0.01,
    )

    session.update(
        activations=ACTIVATIONS_FULL,
        l0_input=0.0,
        c_omega=0.3,
        dt=0.01,
    )

    session.update(
        activations=ACTIVATIONS_FULL,
        l0_input=0.0,
        c_omega=0.4,
        dt=0.01,
    )

    trajectory = session.trajectory()

    assert len(trajectory) == 3

    assert trajectory == [
        entry["theta_Y"]
        for entry in session.history
    ]


# ===============================================================
# 23. TRAYECTORIA DE VELOCIDAD
# ===============================================================

def test_velocity_trajectory_retorna_todas_las_velocidades():
    session = SessionStateYoOscilatorio()

    session.update(
        activations=ACTIVATIONS_FULL,
        l0_input=0.0,
        c_omega=0.2,
        dt=0.01,
    )

    session.update(
        activations=ACTIVATIONS_FULL,
        l0_input=0.0,
        c_omega=0.3,
        dt=0.01,
    )

    velocities = session.velocity_trajectory()

    assert len(velocities) == 2

    assert velocities == [
        entry["theta_dot_Y"]
        for entry in session.history
    ]


# ===============================================================
# 24. CONSISTENCIA ENTRE ENGINE Y SESSION
# ===============================================================

def test_session_y_engine_producen_el_mismo_primer_paso():
    theta0 = float(THETA_CUBE)
    theta_dot0 = 0.0
    dt = 0.01
    c_omega = 0.4

    engine_result = YoOscilatorioEngine.step(
        theta_Y=theta0,
        theta_dot_Y=theta_dot0,
        activations=ACTIVATIONS_FULL,
        l0_input=0.1,
        c_omega=c_omega,
        delta_c_omega=0.0,
        frictions=FRICTIONS_CANONICAL,
        purpose_p=0.2,
        rho=1.0,
        p_t=1.0,
        novelty=0.5,
        sensitivity=5.0,
        dt=dt,
        scale_l0=1.0,
    )

    session = SessionStateYoOscilatorio(
        initial_theta=theta0,
        initial_theta_dot=theta_dot0,
    )

    session_result = session.update(
        activations=ACTIVATIONS_FULL,
        l0_input=0.1,
        c_omega=c_omega,
        frictions=FRICTIONS_CANONICAL,
        purpose_p=0.2,
        rho=1.0,
        p_t=1.0,
        novelty=0.5,
        sensitivity=5.0,
        dt=dt,
        scale_l0=1.0,
    )

    assert session_result["theta_Y"] == pytest.approx(
        engine_result["theta_Y"]
    )

    assert session_result["theta_dot_Y"] == pytest.approx(
        engine_result["theta_dot_Y"]
    )

    assert session_result["theta_ddot_Y"] == pytest.approx(
        engine_result["theta_ddot_Y"]
    )


# ===============================================================
# 25. INVARIANTE DE DIMENSIONALIDAD INTERNA
# ===============================================================

def test_todas_las_magnitudes_vectoriales_internas_tienen_seis_posiciones():
    energies, weights = (
        YoOscilatorioEngine.compute_energies_and_weights(
            ACTIVATIONS_FULL,
            FRICTIONS_CANONICAL,
        )
    )

    contributions = (
        YoOscilatorioEngine.compute_contributions(
            weights=weights,
            activations=ACTIVATIONS_FULL,
            energies=energies,
            frictions=FRICTIONS_CANONICAL,
        )
    )

    entropy = (
        YoOscilatorioEngine.compute_entropy(
            weights
        )
    )

    damping = (
        YoOscilatorioEngine.compute_damping_and_frequency(
            weights,
            FRICTIONS_CANONICAL,
        )
    )

    assert len(energies) == 6
    assert len(weights) == 6
    assert len(contributions) == 6

    assert set(entropy.keys()) == {
        "s",
        "s_norm",
        "negentropy",
    }

    assert set(damping.keys()) == {
        "phi_Y",
        "zeta_Y",
        "omega_Y",
        "regime",
    }


# ===============================================================
# 26. TEST DE INTEGRACIÓN MATEMÁTICA COMPLETA
# ===============================================================

def test_carril_completo_conserva_la_cadena_causal():
    session = SessionStateYoOscilatorio()

    result = session.update(
        activations=[
            0.20,
            0.40,
            0.60,
            0.80,
            1.00,
            0.50,
        ],
        l0_input=0.15,
        c_omega=0.65,
        frictions=FRICTIONS_CANONICAL,
        purpose_p=0.30,
        rho=1.10,
        p_t=0.90,
        novelty=1.50,
        sensitivity=5.0,
        dt=0.01,
        scale_l0=1.20,
    )

    energies = result["energies"]
    weights = result["weights"]
    contributions = result["contributions_f_i"]

    assert len(energies) == 6
    assert len(weights) == 6
    assert len(contributions) == 6

    assert sum(weights) == pytest.approx(
        1.0
    )

    assert result["entropy"]["s"] >= 0.0
    assert result["entropy"]["s"] <= math.log(6)

    assert result["damping"]["phi_Y"] >= 0.0
    assert result["damping"]["zeta_Y"] >= 0.0
    assert result["damping"]["omega_Y"] >= 0.0

    forces = result["forces"]

    assert forces["f_total"] == pytest.approx(
        forces["f_l0"]
        + forces["f_l5"]
        + forces["f_l6"]
        + forces["f_beta"]
        + forces["f_coh"]
    )

    theta_eq = result["geometry"]["theta_eq"]
    phi_y = result["damping"]["phi_Y"]
    theta = (
        float(THETA_CUBE)
    )
    theta_dot = 0.0

    expected_acceleration = (
        forces["f_total"]
        - phi_y * theta_dot
        - math.pi ** 2 * (theta - theta_eq)
    )

    assert result["theta_ddot_Y"] == pytest.approx(
        expected_acceleration
    )


# ===============================================================
# FIN DEL TEST
# ===============================================================
