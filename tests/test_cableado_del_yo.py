# ===============================================================
# VPSI-TRUTH — tests/test_cableado_del_yo.py
# TEST DE CABLEADO — SELF — L4 — YO OSCILATORIO DINÁMICO
# ===============================================================
#
# RUTA DEL OBJETIVO:
#
#   modules/self/L4/yo_oscillador_dinamico.py
#
# RESPONSABILIDAD DEL TEST:
#
#   Verificar que el cableado dinámico de L4:
#
#       L1..L6
#          ↓
#       E_i
#          ↓
#       w_i
#          ↓
#       f_i
#          ↓
#       S
#          ↓
#       C_Ω
#          ↓
#       φ_Y
#          ↓
#       θ_eq
#          ↓
#       F_Y
#          ↓
#       θ̈_Y
#          ↓
#       θ̇_Y
#          ↓
#       θ_Y
#
#   está realmente conectado y ejecutable.
#
#   ESTE TEST NO MODIFICA EL CONTRATO DEL MÓDULO.
#
#   ESTE TEST NO SUPONE QUE modules.self.__init__ DEBA
#   REEXPORTAR LA CLASE.
#
#   LA IMPORTACIÓN SE REALIZA DESDE LA RUTA REAL DEL CABLEADO.
#
# ===============================================================

import math

import pytest

from modules.self.L4.yo_oscillador_dinamico import (
    ALPHA_F,
    BETA_F,
    ENTROPY_MAX,
    INTERNAL_LAYERS,
    LAYER_INDICES,
    PI2,
    YoOscillator,
    YoState,
    compute_contributions,
    compute_c_omega,
    compute_energies,
    compute_weights,
    dynamic_equilibrium,
    force_BETA,
    force_COH,
    force_L0,
    force_L5,
    force_L6,
    force_Y,
    negentropy,
    normalized_entropy,
    omega_Y,
    oscillator_solution_Y,
    phi_Y,
    read_rail,
    regime_Y,
    shannon_S,
    step_yo,
    zeta_Y,
)


# ===============================================================
# 1. EXISTENCIA Y ESTRUCTURA DEL MÓDULO
# ===============================================================

def test_l4_yo_oscillator_importa_desde_la_ruta_real():

    assert YoOscillator is not None
    assert YoState is not None


def test_l4_define_seis_capas_internas():

    assert INTERNAL_LAYERS == 6
    assert LAYER_INDICES == (1, 2, 3, 4, 5, 6)


def test_constantes_estructurales_estan_conectadas():

    assert math.isfinite(ALPHA_F)
    assert math.isfinite(BETA_F)
    assert ALPHA_F > 0.0
    assert BETA_F > 0.0
    assert math.isclose(
        ALPHA_F + BETA_F,
        1.0,
        rel_tol=0.0,
        abs_tol=1e-12,
    )


# ===============================================================
# 2. CABLEADO L1..L6 → ENERGÍAS
# ===============================================================

def test_l1_l6_alimentan_el_calculo_de_energias():

    activations = [
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
    ]

    frictions = [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
    ]

    energies = compute_energies(
        activations,
        frictions,
    )

    assert len(energies) == 6

    for i, energy in enumerate(energies, 1):

        expected = 1.0 * (
            1.0 - 0.0
        ) * (
            (1.0 + math.sqrt(5.0)) / 2.0
        ) ** (
            i / 2.0
        )

        assert math.isclose(
            energy,
            expected,
            rel_tol=1e-12,
            abs_tol=1e-12,
        )


def test_l6_conserva_fraccion_cero_de_friccion():

    activations = [1.0] * 6

    frictions = [
        0.10,
        0.02,
        0.05,
        0.03,
        0.01,
        0.00,
    ]

    energies = compute_energies(
        activations,
        frictions,
    )

    phi = (
        1.0 + math.sqrt(5.0)
    ) / 2.0

    expected_l6 = phi ** 3.0

    assert math.isclose(
        energies[5],
        expected_l6,
        rel_tol=1e-12,
        abs_tol=1e-12,
    )


def test_energia_cambia_si_cambia_una_activacion():

    base = [
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
    ]

    altered = [
        1.0,
        1.0,
        1.0,
        0.5,
        1.0,
        1.0,
    ]

    frictions = [0.0] * 6

    energies_base = compute_energies(
        base,
        frictions,
    )

    energies_altered = compute_energies(
        altered,
        frictions,
    )

    assert energies_base[3] != energies_altered[3]

    assert math.isclose(
        energies_altered[3],
        energies_base[3] * 0.5,
        rel_tol=1e-12,
        abs_tol=1e-12,
    )

    for i in [0, 1, 2, 4, 5]:

        assert math.isclose(
            energies_base[i],
            energies_altered[i],
            rel_tol=1e-12,
            abs_tol=1e-12,
        )


# ===============================================================
# 3. CABLEADO ENERGÍAS → PESOS
# ===============================================================

def test_energias_alimentan_pesos_emergentes():

    energies = [
        1.0,
        2.0,
        3.0,
        4.0,
        5.0,
        6.0,
    ]

    weights = compute_weights(
        energies
    )

    assert len(weights) == 6

    assert math.isclose(
        sum(weights),
        1.0,
        rel_tol=0.0,
        abs_tol=1e-12,
    )

    total = sum(energies)

    for energy, weight in zip(
        energies,
        weights,
    ):

        assert math.isclose(
            weight,
            energy / total,
            rel_tol=1e-12,
            abs_tol=1e-12,
        )


def test_pesos_uniformes_si_no_hay_energia():

    weights = compute_weights(
        [0.0] * 6
    )

    assert len(weights) == 6

    for weight in weights:

        assert math.isclose(
            weight,
            1.0 / 6.0,
            rel_tol=0.0,
            abs_tol=1e-12,
        )


# ===============================================================
# 4. CABLEADO PESOS → CONTRIBUCIONES
# ===============================================================

def test_pesos_alimentan_contribuciones():

    activations = [1.0] * 6
    energies = [1.0] * 6
    weights = [1.0 / 6.0] * 6
    frictions = [0.0] * 6

    contributions = compute_contributions(
        weights,
        activations,
        energies,
        frictions,
    )

    assert len(contributions) == 6

    for contribution in contributions:

        assert math.isclose(
            contribution,
            1.0 / 6.0,
            rel_tol=1e-12,
            abs_tol=1e-12,
        )


# ===============================================================
# 5. CABLEADO PESOS → ENTROPÍA
# ===============================================================

def test_entropia_de_distribucion_uniforme():

    weights = [1.0 / 6.0] * 6

    S = shannon_S(weights)

    assert math.isclose(
        S,
        math.log(6.0),
        rel_tol=1e-12,
        abs_tol=1e-12,
    )


def test_entropia_normalizada_maxima():

    weights = [1.0 / 6.0] * 6

    S = shannon_S(weights)

    normalized = normalized_entropy(S)

    assert math.isclose(
        normalized,
        1.0,
        rel_tol=0.0,
        abs_tol=1e-12,
    )


def test_negentropia_uniforme_es_cero():

    weights = [1.0 / 6.0] * 6

    assert math.isclose(
        negentropy(weights),
        0.0,
        rel_tol=0.0,
        abs_tol=1e-12,
    )


def test_entropia_de_distribucion_concentrada():

    weights = [
        1.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
    ]

    S = shannon_S(weights)

    assert math.isclose(
        S,
        0.0,
        rel_tol=0.0,
        abs_tol=1e-12,
    )


# ===============================================================
# 6. CABLEADO CONTRIBUCIONES → C_Ω
# ===============================================================

def test_contribuciones_alimentan_c_omega():

    contributions = [
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
    ]

    C = compute_c_omega(
        contributions
    )

    assert math.isfinite(C)

    assert 0.0 <= C <= ALPHA_F


def test_c_omega_no_excede_alpha():

    contributions = [
        10.0,
        10.0,
        10.0,
        10.0,
        10.0,
        10.0,
    ]

    C = compute_c_omega(
        contributions,
        rho=100.0,
        P_t=100.0,
        A=100.0,
        I_ext=100.0,
    )

    assert C <= ALPHA_F


# ===============================================================
# 7. CABLEADO PESOS → AMORTIGUAMIENTO
# ===============================================================

def test_phi_y_es_promedio_ponderado_de_fricciones():

    weights = [1.0 / 6.0] * 6

    frictions = [
        0.10,
        0.02,
        0.05,
        0.03,
        0.01,
        0.00,
    ]

    expected = sum(
        weights[i] * frictions[i]
        for i in range(6)
    )

    result = phi_Y(
        weights,
        frictions,
    )

    assert math.isclose(
        result,
        expected,
        rel_tol=1e-12,
        abs_tol=1e-12,
    )


def test_l6_no_aporta_friccion():

    weights = [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        1.0,
    ]

    frictions = [
        0.10,
        0.02,
        0.05,
        0.03,
        0.01,
        0.90,
    ]

    assert math.isclose(
        phi_Y(
            weights,
            frictions,
        ),
        0.0,
        rel_tol=0.0,
        abs_tol=1e-12,
    )


# ===============================================================
# 8. CABLEADO φ_Y → ζ_Y → ω_Y → RÉGIMEN
# ===============================================================

def test_cadena_de_amortiguamiento():

    phi = 0.05

    zeta = zeta_Y(phi)

    omega = omega_Y(phi)

    regime = regime_Y(phi)

    assert zeta >= 0.0
    assert omega >= 0.0
    assert regime == "SUBAMORTIGUADO"


def test_omega_se_anula_en_sobre_amortiguamiento():

    phi = 2.0 * math.pi

    assert math.isclose(
        zeta_Y(phi),
        1.0,
        rel_tol=0.0,
        abs_tol=1e-12,
    )

    assert math.isclose(
        omega_Y(phi),
        0.0,
        rel_tol=0.0,
        abs_tol=1e-12,
    )

    assert regime_Y(phi) == "CRITICO"


# ===============================================================
# 9. CABLEADO C_Ω + PESOS → θ_eq
# ===============================================================

def test_c_omega_y_pesos_alimentan_equilibrio():

    weights = [1.0 / 6.0] * 6

    theta_eq = dynamic_equilibrium(
        c_omega=0.0,
        weights=weights,
    )

    assert math.isfinite(theta_eq)


def test_equilibrio_responde_a_cambio_de_pesos():

    weights_a = [
        1.0 / 6.0,
        1.0 / 6.0,
        1.0 / 6.0,
        1.0 / 6.0,
        1.0 / 6.0,
        1.0 / 6.0,
    ]

    weights_b = [
        0.0,
        0.0,
        0.0,
        0.0,
        0.5,
        0.5,
    ]

    theta_a = dynamic_equilibrium(
        0.5 * ALPHA_F,
        weights_a,
    )

    theta_b = dynamic_equilibrium(
        0.5 * ALPHA_F,
        weights_b,
    )

    assert theta_a != theta_b


# ===============================================================
# 10. CABLEADO DE FUERZAS
# ===============================================================

def test_force_l0_es_entrada_externa():

    assert math.isclose(
        force_L0(3.0),
        3.0,
        rel_tol=0.0,
        abs_tol=1e-12,
    )


def test_force_l6_usa_w6_como_direccion():

    assert math.isclose(
        force_L6(
            w6=0.25,
            purpose_magnitude=4.0,
        ),
        1.0,
        rel_tol=0.0,
        abs_tol=1e-12,
    )


def test_force_beta_responde_a_novedad():

    zero = force_BETA(0.0)
    positive = force_BETA(10.0)

    assert zero == 0.0
    assert positive > zero


def test_force_coh_responde_a_delta_c():

    assert math.isclose(
        force_COH(
            c_omega=0.5,
            delta_c=0.2,
        ),
        0.1,
        rel_tol=0.0,
        abs_tol=1e-12,
    )


def test_force_y_integra_los_canales():

    result = force_Y(
        L0_input=1.0,
        weights=[0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
        purpose_magnitude=2.0,
        c_omega=0.0,
        rho=1.0,
        P_t=1.0,
        S=0.0,
        delta_c=0.0,
        novelty=0.0,
    )

    assert math.isfinite(result)

    assert result >= 3.0


# ===============================================================
# 11. INTEGRACIÓN COMPLETA DEL CARRIL
# ===============================================================

def test_step_yo_ejecuta_el_circuito_completo():

    state = YoState()

    activations = [
        1.0,
        0.8,
        0.6,
        0.7,
        0.9,
        1.0,
    ]

    new_state = step_yo(
        state,
        activations=activations,
        dt=0.01,
    )

    assert new_state.t == 0.01

    assert len(new_state.energies) == 6
    assert len(new_state.weights) == 6
    assert len(new_state.contributions) == 6

    assert math.isfinite(new_state.theta)
    assert math.isfinite(new_state.theta_dot)
    assert math.isfinite(new_state.theta_eq)
    assert math.isfinite(new_state.force_y)
    assert math.isfinite(new_state.c_omega)
    assert math.isfinite(new_state.phi_y)
    assert math.isfinite(new_state.zeta_y)
    assert math.isfinite(new_state.omega_y)
    assert math.isfinite(new_state.S)


def test_step_yo_realmente_mueve_el_estado():

    oscillator = YoOscillator()

    before = oscillator.snapshot()

    after = oscillator.step(
        activations=[
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
        ],
        dt=0.01,
        L0_input=1.0,
        purpose_magnitude=1.0,
    )

    assert after["t"] > before["t"]

    assert (
        after["theta_Y"]
        != before["theta_Y"]
        or
        after["theta_dot_Y"]
        != before["theta_dot_Y"]
    )


# ===============================================================
# 12. VERIFICACIÓN DE LA CADENA ENERGÉTICA COMPLETA
# ===============================================================

def test_cadena_l1_l6_hasta_estado_l4():

    activations = [
        0.90,
        0.80,
        0.70,
        0.60,
        0.50,
        0.40,
    ]

    oscillator = YoOscillator()

    result = oscillator.step(
        activations=activations,
        dt=0.001,
    )

    energies = result[
        "energies_L1_L6"
    ]

    weights = result[
        "weights_L1_L6"
    ]

    contributions = result[
        "contributions_f1_f6"
    ]

    assert len(energies) == 6
    assert len(weights) == 6
    assert len(contributions) == 6

    assert math.isclose(
        sum(weights),
        1.0,
        rel_tol=0.0,
        abs_tol=1e-12,
    )

    assert result["C_OMEGA"] >= 0.0
    assert result["C_OMEGA"] <= ALPHA_F

    assert math.isfinite(
        result["theta_Y"]
    )

    assert math.isfinite(
        result["theta_dot_Y"]
    )

    assert result["L0_ROLE"] == (
        "INPUT_EXTERNAL"
    )


# ===============================================================
# 13. L0 NO DEBE CONVERTIRSE EN PESO INTERNO
# ===============================================================

def test_l0_no_forma_parte_de_los_seis_pesos():

    oscillator = YoOscillator()

    result = oscillator.step(
        activations=[1.0] * 6,
        dt=0.001,
        L0_input=100.0,
    )

    assert len(
        result["weights_L1_L6"]
    ) == 6

    assert "w0" not in result


# ===============================================================
# 14. VALIDACIONES DE CONTRATO
# ===============================================================

def test_rechaza_menos_de_seis_activaciones():

    with pytest.raises(ValueError):

        compute_energies(
            [1.0] * 5,
            [0.0] * 6,
        )


def test_rechaza_mas_de_seis_activaciones():

    with pytest.raises(ValueError):

        compute_energies(
            [1.0] * 7,
            [0.0] * 6,
        )


def test_rechaza_activacion_fuera_de_rango():

    with pytest.raises(ValueError):

        compute_energies(
            [1.0, 1.0, 1.0, 1.0, 1.0, 2.0],
            [0.0] * 6,
        )


def test_rechaza_dt_cero():

    with pytest.raises(ValueError):

        step_yo(
            YoState(),
            activations=[1.0] * 6,
            dt=0.0,
        )


def test_rechaza_dt_negativo():

    with pytest.raises(ValueError):

        step_yo(
            YoState(),
            activations=[1.0] * 6,
            dt=-0.01,
        )


# ===============================================================
# 15. LECTURA DEL CARRIL
# ===============================================================

def test_read_rail_expone_el_estado_COMPLETO():

    state = YoState()

    rail = read_rail(state)

    required = {
        "theta_Y",
        "theta_dot_Y",
        "t",
        "theta_eq",
        "phi_Y",
        "zeta_Y",
        "omega_Y",
        "regime",
        "force_Y",
        "C_OMEGA",
        "C_OMEGA_RAW",
        "delta_C_OMEGA",
        "S",
        "weights_L1_L6",
        "energies_L1_L6",
        "contributions_f1_f6",
        "ALPHA",
        "BETA",
        "THETA_CUBE",
        "L0_ROLE",
    }

    assert required.issubset(
        rail.keys()
    )


# ===============================================================
# 16. SOLUCIÓN ANALÍTICA
# ===============================================================

def test_solucion_analitica_es_finita():

    result = oscillator_solution_Y(
        t=1.0,
        amplitude=0.5,
        delta=0.0,
        phi_y=0.05,
    )

    assert math.isfinite(result)


# ===============================================================
# FIN DEL TEST
# ===============================================================
