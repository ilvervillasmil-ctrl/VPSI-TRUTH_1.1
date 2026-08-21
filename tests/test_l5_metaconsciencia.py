# ===============================================================
# tests/test_l5_metaconsciencia.py
# ===============================================================
"""
Auditoría contractual de L5 según el módulo real:

    modules/self/L5/metaconsciencia.py

Contrato de este archivo (no el idealizado):
    - Exporta ALPHA, BETA, PHI, THETA_CUBE_DEFAULT, LAYER_COUNT
    - ControlConfiguration.agency / autoreference / conscious son bool
    - gain de retorno = β · min(1, a·r) cuando a>0 y r>0
    - formula_maestra_l5 NO expone novelty (sí calcular)
    - sigma5 es parámetro de forma (default 0.029707)
    - DEFAULT_FRICTIONS = (0.0,) * 7 en este fuente

Ejecutar:
    pytest -q tests/test_l5_metaconsciencia.py
"""

from __future__ import annotations

import math

import pytest

import modules.constante as constante
import modules.formulas.formulas_omega.constants as omega_constants

from modules.self.L5.metaconsciencia import (
    ALPHA,
    BETA,
    PHI,
    THETA_CUBE_DEFAULT,
    LAYER_COUNT,
    N_MIN,
    N_MAX,
    THRESHOLD_N2,
    THRESHOLD_N3,
    DEFAULT_FRICTIONS,
    L0,
    L1,
    L2,
    L3,
    L4,
    L5,
    L6,
    build_geometry,
    calculate_energies,
    normalize_weights,
    default_coherence,
    receptor_quality,
    house_occupancy,
    layer_visibility,
    effective_visibility,
    calculate_i5,
    observation_intensity,
    determine_observation_level,
    control_configuration,
    yo_state,
    decode_downward_signal,
    describe_movement,
    L5Metaconsciencia,
    formula_maestra_l5,
)

TC = THETA_CUBE_DEFAULT
SIGMA5 = 0.029707

TODO_1 = (1.0,) * LAYER_COUNT
CERO = (0.0,) * LAYER_COUNT
MEDIO = (0.5,) * LAYER_COUNT


def _z(i: int) -> float:
    return TC * (PHI ** ((i - L4) / 2.0))


def _assert_unit_interval(value: float) -> None:
    assert math.isfinite(value)
    assert 0.0 <= value <= 1.0


def _assert_close(a: float, b: float, tol: float = 1e-12) -> None:
    assert abs(float(a) - float(b)) <= tol, (a, b)


# ===============================================================
# A. ARRANQUE Y API
# ===============================================================

def test_a1_formula_maestra_arranca():
    result = formula_maestra_l5(
        TODO_1,
        theta_y=TC,
        agency=1.0,
        autoreference=1.0,
    )
    assert result is not None


def test_a2_motor_l5_arranca():
    engine = L5Metaconsciencia()
    assert engine is not None
    assert len(engine.geometry) == LAYER_COUNT


def test_a3_resultado_carril_completo():
    result = formula_maestra_l5(TODO_1)
    assert len(result.activations_before) == LAYER_COUNT
    assert len(result.activations_after) == LAYER_COUNT
    assert len(result.energies) == LAYER_COUNT
    assert len(result.weights) == LAYER_COUNT
    assert len(result.geometry) == LAYER_COUNT


# ===============================================================
# B. VALORES Y UMBRALES (según este fuente)
# ===============================================================

def test_b1_alpha_beta_cierre():
    _assert_close(ALPHA + BETA, 1.0)


def test_b2_alpha_beta_coinciden_con_semilla_numerica():
    """Si el módulo redefine literales, al menos deben coincidir con la semilla."""
    _assert_close(ALPHA, float(constante.ALPHA))
    _assert_close(BETA, float(constante.BETA))


def test_b3_phi_coincide_con_constants():
    _assert_close(PHI, float(omega_constants.PHI))


def test_b4_theta_cube_coincide_con_constants():
    _assert_close(THETA_CUBE_DEFAULT, float(omega_constants.THETA_CUBE))


def test_b5_layer_count():
    assert LAYER_COUNT == 7
    assert LAYER_COUNT == int(omega_constants.NUM_LAYERS)


def test_b6_umbrales_derivados():
    _assert_close(THRESHOLD_N2, (BETA / ALPHA) ** 0.5)
    _assert_close(THRESHOLD_N3, (BETA / ALPHA) ** (1.0 / 3.0))


def test_b7_default_frictions_longitud():
    assert len(DEFAULT_FRICTIONS) == LAYER_COUNT


# ===============================================================
# C. CARRIL L0..L6
# ===============================================================

def test_c1_indices():
    assert (L0, L1, L2, L3, L4, L5, L6) == (0, 1, 2, 3, 4, 5, 6)


def test_c2_L4_casa_del_yo():
    geometry = build_geometry()
    _assert_close(geometry[L4].z, TC)


def test_c3_siete_posiciones():
    geometry = build_geometry()
    assert len(geometry) == 7
    assert tuple(p.index for p in geometry) == tuple(range(7))


def test_c4_z_monotona():
    geometry = build_geometry()
    for i in range(LAYER_COUNT - 1):
        assert geometry[i].z < geometry[i + 1].z


def test_c5_theta_eq_no_cambia_geometria():
    a = L5Metaconsciencia(theta_eq=0.05).geometry
    b = L5Metaconsciencia(theta_eq=0.90).geometry
    assert [p.z for p in a] == [p.z for p in b]


# ===============================================================
# D. ENERGÍA Y PESOS
# ===============================================================

def test_d1_energias_longitud():
    assert len(calculate_energies(TODO_1)) == LAYER_COUNT


def test_d2_energia_con_friccion_cero():
    geometry = build_geometry()
    zero_phi = (0.0,) * LAYER_COUNT
    energies = calculate_energies(TODO_1, zero_phi, geometry)
    for i in range(LAYER_COUNT):
        _assert_close(energies[i], geometry[i].radius)


def test_d3_friccion_reduce_energia():
    zero_phi = (0.0,) * LAYER_COUNT
    base = calculate_energies(TODO_1, zero_phi)
    friction = [0.0] * LAYER_COUNT
    friction[L3] = 0.5
    reduced = calculate_energies(TODO_1, friction)
    assert reduced[L3] < base[L3]


def test_d4_pesos_suman_uno():
    _assert_close(sum(normalize_weights(calculate_energies(TODO_1))), 1.0)


def test_d5_apagado_uniforme():
    weights = normalize_weights(calculate_energies(CERO))
    for w in weights:
        _assert_close(w, 1.0 / LAYER_COUNT)


def test_d6_activaciones_invalidas():
    with pytest.raises(ValueError):
        calculate_energies((1.2, 0, 0, 0, 0, 0, 0))
    with pytest.raises(ValueError):
        calculate_energies((0.5,) * 6)


def test_d7_fricciones_invalidas():
    with pytest.raises(ValueError):
        calculate_energies(TODO_1, (1.2,) * 7)
    with pytest.raises(ValueError):
        calculate_energies(TODO_1, (0.5,) * 6)


# ===============================================================
# E. RECEPTOR
# ===============================================================

def test_e1_coherencia_uniforme():
    _assert_close(default_coherence(TODO_1), 1.0)


def test_e2_desalineacion_reduce():
    aligned = default_coherence((0.5, 0.8, 0.8, 0.8, 0.8, 0.5, 0.5))
    misaligned = default_coherence((0.5, 1.0, 0.1, 1.0, 0.1, 0.5, 0.5))
    assert aligned > misaligned


def test_e3_calibracion_L1_L4():
    frictions = (0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6)
    _, q5, _ = receptor_quality(TODO_1, frictions)
    expected = (
        (1.0 - frictions[L1])
        * (1.0 - frictions[L2])
        * (1.0 - frictions[L3])
        * (1.0 - frictions[L4])
    )
    _assert_close(q5, expected)


def test_e4_distorsion_complemento():
    _, q5, distortion = receptor_quality(TODO_1, DEFAULT_FRICTIONS)
    _assert_close(q5 + distortion, 1.0)


def test_e5_receptor_en_rango():
    _, q5, distortion = receptor_quality(TODO_1, DEFAULT_FRICTIONS)
    _assert_unit_interval(q5)
    _assert_unit_interval(distortion)


# ===============================================================
# F. OCUPACIÓN h5
# ===============================================================

def test_f1_sigma5_positivo():
    with pytest.raises(ValueError):
        house_occupancy(TC, _z(L5), 0.0)


def test_f2_maxima_en_z5():
    _assert_close(house_occupancy(_z(L5), _z(L5), SIGMA5), 1.0)


def test_f3_simetrica():
    delta = 0.01
    left = house_occupancy(_z(L5) - delta, _z(L5), SIGMA5)
    right = house_occupancy(_z(L5) + delta, _z(L5), SIGMA5)
    _assert_close(left, right)


def test_f4_decrece_con_distancia():
    center = house_occupancy(_z(L5), _z(L5), SIGMA5)
    nearby = house_occupancy(_z(L5) + 0.01, _z(L5), SIGMA5)
    far = house_occupancy(_z(L5) + 0.05, _z(L5), SIGMA5)
    assert center > nearby > far


def test_f5_en_rango():
    for delta in (0.0, 0.01, 0.05, 1.0):
        _assert_unit_interval(house_occupancy(_z(L5) + delta, _z(L5), SIGMA5))


# ===============================================================
# G. VISIBILIDAD
# ===============================================================

def test_g1_sobre_si_mismo():
    _assert_close(layer_visibility(_z(L5), _z(L5), TC), 1.0)


def test_g2_crece_hacia_L5():
    values = [layer_visibility(_z(L5), _z(i), TC) for i in range(L0, L5 + 1)]
    for i in range(len(values) - 1):
        assert values[i] < values[i + 1]


def test_g3_positiva():
    for i in range(LAYER_COUNT):
        assert layer_visibility(_z(L5), _z(i), TC) > 0.0


def test_g4_theta_cube_cero():
    with pytest.raises(ValueError):
        layer_visibility(_z(L5), _z(L4), 0.0)


def test_g5_efectiva_en_rango():
    geometry = build_geometry()
    weights = normalize_weights(calculate_energies(TODO_1))
    _assert_unit_interval(
        effective_visibility(weights, geometry, theta_cube=TC)
    )


# ===============================================================
# H. I5
# ===============================================================

def test_h1_techo_alpha():
    value = calculate_i5(q5=1.0, h5=1.0, v5=1.0)
    _assert_close(value, ALPHA)
    assert value <= ALPHA + 1e-12


def test_h2_monotona_q5():
    assert calculate_i5(q5=0.6, h5=0.8, v5=0.8) > calculate_i5(
        q5=0.4, h5=0.8, v5=0.8
    )


def test_h3_monotona_h5():
    assert calculate_i5(q5=0.8, h5=0.6, v5=0.8) > calculate_i5(
        q5=0.8, h5=0.4, v5=0.8
    )


def test_h4_monotona_v5():
    assert calculate_i5(q5=0.8, h5=0.8, v5=0.6) > calculate_i5(
        q5=0.8, h5=0.8, v5=0.4
    )


def test_h5_en_rango():
    for q5 in (0.0, 0.5, 1.0):
        for h5 in (0.0, 0.5, 1.0):
            for v5 in (0.0, 0.5, 1.0):
                value = calculate_i5(q5=q5, h5=h5, v5=v5)
                assert 0.0 <= value <= ALPHA + 1e-12


# ===============================================================
# I. INTENSIDAD DE OBSERVACIÓN
# ===============================================================

def test_i1_orden_uno():
    for i5 in (0.05, 0.2, 0.5, min(0.9, ALPHA)):
        _assert_close(observation_intensity(i5, 1), i5)


def test_i2_recursion_disminuye():
    i5 = 0.5 * ALPHA
    assert observation_intensity(i5, 1) > observation_intensity(i5, 2)
    assert observation_intensity(i5, 2) > observation_intensity(i5, 3)


def test_i3_orden_invalido():
    with pytest.raises(ValueError):
        observation_intensity(0.5, 0)


def test_i4_en_rango():
    for i5 in (0.0, 0.1, 0.5 * ALPHA, ALPHA):
        for k in (1, 2, 3):
            value = observation_intensity(i5, k)
            assert 0.0 <= value <= ALPHA + 1e-12


# ===============================================================
# J. EJE N
# ===============================================================

def test_j1_sin_ar_minima_N1():
    assert determine_observation_level(0.9, autoreference=BETA * 0.5) == N_MIN
    assert determine_observation_level(0.9, autoreference=0.0) == N_MIN


def test_j2_piso_N1():
    assert determine_observation_level(0.0, autoreference=1.0) == N_MIN


def test_j3_umbral_N2_inclusivo():
    assert determine_observation_level(
        ALPHA * THRESHOLD_N2, autoreference=1.0
    ) == 2


def test_j4_bajo_N2():
    assert determine_observation_level(
        ALPHA * THRESHOLD_N2 * 0.999, autoreference=1.0
    ) == 1


def test_j5_umbral_N3_inclusivo():
    assert determine_observation_level(
        ALPHA * THRESHOLD_N3, autoreference=1.0
    ) == 3


def test_j6_bajo_N3():
    assert determine_observation_level(
        ALPHA * THRESHOLD_N3 * 0.999, autoreference=1.0
    ) == 2


def test_j7_acotado():
    for i5 in (0.0, 0.1, 0.5, 0.9, ALPHA):
        for ar in (0.0, BETA, 0.5, 1.0):
            level = determine_observation_level(i5, autoreference=ar)
            assert N_MIN <= level <= N_MAX


# ===============================================================
# K. CONTROL (bool en este fuente)
# ===============================================================

def test_k1_cuatro_configuraciones():
    cases = (
        (0.0, 0.0, "2.1", False),
        (0.0, 1.0, "2.2", False),
        (1.0, 0.0, "2.3", False),
        (1.0, 1.0, "2.4", True),
    )
    for agency, autoreference, code, conscious in cases:
        cfg = control_configuration(2, agency=agency, autoreference=autoreference)
        assert cfg.code == code
        assert cfg.conscious is conscious
        assert isinstance(cfg.agency, bool)
        assert isinstance(cfg.autoreference, bool)
        assert isinstance(cfg.conscious, bool)


def test_k2_nivel_invalido():
    with pytest.raises(ValueError):
        control_configuration(0, agency=1.0, autoreference=1.0)
    with pytest.raises(ValueError):
        control_configuration(4, agency=1.0, autoreference=1.0)


def test_k3_dimensiones_independientes():
    cfg1 = control_configuration(2, agency=1.0, autoreference=0.0)
    cfg2 = control_configuration(2, agency=0.0, autoreference=1.0)
    assert cfg1.code == "2.3"
    assert cfg2.code == "2.2"
    assert cfg1.conscious is False
    assert cfg2.conscious is False


def test_k4_conscious_requiere_ambos():
    cfg = control_configuration(2, agency=1.0, autoreference=1.0)
    assert cfg.conscious is True


# ===============================================================
# L. CASA DEL YO = L4
# ===============================================================

def test_l1_casa_L4():
    assert L5Metaconsciencia().geometry[L4].index == L4


def test_l2_theta_eq_no_transfiere_a_L5():
    result = formula_maestra_l5(
        TODO_1,
        theta_y=0.22,
        theta_eq=TC,
        agency=1.0,
        autoreference=1.0,
    )
    _assert_close(result.theta_eq, TC)
    _assert_close(result.geometry[L4].z, TC)


def test_l3_yo_state_sin_L5_como_casa():
    for level in (1, 2, 3):
        state = yo_state(level, agency=1.0, autoreference=1.0)
        assert "L5" not in state


# ===============================================================
# M. RETORNO
#   gate: a>0 y r>0
#   gain = β · min(1, a·r)   (magnitud continua)
# ===============================================================

def test_m1_sin_agencia_sin_retorno():
    after = decode_downward_signal(
        MEDIO, observation_level=3, agency=0.0, autoreference=1.0
    )
    assert after == MEDIO


def test_m2_sin_autoreferencia_sin_retorno():
    after = decode_downward_signal(
        MEDIO, observation_level=3, agency=1.0, autoreference=0.0
    )
    assert after == MEDIO


def test_m3_reduce_L1_L2_L3():
    after = decode_downward_signal(
        MEDIO, observation_level=2, agency=1.0, autoreference=1.0
    )
    assert after[L1] < MEDIO[L1]
    assert after[L2] < MEDIO[L2]
    assert after[L3] < MEDIO[L3]


def test_m4_refuerza_L4():
    after = decode_downward_signal(
        MEDIO, observation_level=2, agency=1.0, autoreference=1.0
    )
    assert after[L4] > MEDIO[L4]


def test_m5_L0_L5_L6_invariantes():
    after = decode_downward_signal(
        MEDIO, observation_level=3, agency=1.0, autoreference=1.0
    )
    for index in (L0, L5, L6):
        _assert_close(after[index], MEDIO[index])


def test_m6_ganancia_beta_por_producto():
    agency = 0.8
    autoreference = 0.6
    after = decode_downward_signal(
        MEDIO,
        observation_level=2,
        agency=agency,
        autoreference=autoreference,
    )
    gain = BETA * min(1.0, agency * autoreference)
    _assert_close(after[L1], MEDIO[L1] * (1.0 - gain))
    _assert_close(after[L4], min(1.0, MEDIO[L4] * (1.0 + gain)))


def test_m7_entrada_no_se_muta():
    before = [0.5] * LAYER_COUNT
    snapshot = list(before)
    decode_downward_signal(
        before, observation_level=2, agency=1.0, autoreference=1.0
    )
    assert before == snapshot


def test_m8_salida_en_rango():
    after = decode_downward_signal(
        MEDIO, observation_level=3, agency=1.0, autoreference=1.0
    )
    for value in after:
        _assert_unit_interval(value)


def test_m9_L4_saturado_queda_en_uno():
    before = (0.5, 0.5, 0.5, 0.5, 1.0, 0.5, 0.5)
    after = decode_downward_signal(
        before, observation_level=2, agency=1.0, autoreference=1.0
    )
    _assert_close(after[L4], 1.0)


# ===============================================================
# N. MOVIMIENTOS
# ===============================================================

def test_n1_targets_cambio():
    after = decode_downward_signal(
        MEDIO, observation_level=2, agency=1.0, autoreference=1.0
    )
    targets = {m.target_layer for m in describe_movement(MEDIO, after)}
    assert targets == {L1, L2, L3, L4}


def test_n2_origen_L5():
    after = decode_downward_signal(
        MEDIO, observation_level=2, agency=1.0, autoreference=1.0
    )
    assert all(m.source_layer == L5 for m in describe_movement(MEDIO, after))


def test_n3_L4_saturado_sin_traza():
    before = (0.5, 0.5, 0.5, 0.5, 1.0, 0.5, 0.5)
    after = decode_downward_signal(
        before, observation_level=2, agency=1.0, autoreference=1.0
    )
    targets = {m.target_layer for m in describe_movement(before, after)}
    assert L4 not in targets


# ===============================================================
# O. RESULTADO INTEGRAL
# ===============================================================

def test_o1_resultado_coherente():
    result = formula_maestra_l5(
        TODO_1, theta_y=TC, agency=1.0, autoreference=1.0
    )
    assert len(result.observation_intensities) == 3
    assert result.observation_level in (1, 2, 3)
    assert result.control.level == result.observation_level
    assert result.loop_detected is False
    assert result.control.conscious is True


def test_o2_i5_en_rango():
    result = formula_maestra_l5(TODO_1, theta_y=TC, agency=1.0, autoreference=1.0)
    assert 0.0 <= result.i5 <= ALPHA + 1e-12


def test_o3_ocupacion_en_rango():
    _assert_unit_interval(formula_maestra_l5(TODO_1, theta_y=TC).occupancy)


def test_o4_visibilidad_en_rango():
    _assert_unit_interval(formula_maestra_l5(TODO_1, theta_y=TC).visibility)


def test_o5_receptor_en_rango():
    r = formula_maestra_l5(TODO_1, theta_y=TC)
    _assert_unit_interval(r.coherence)
    _assert_unit_interval(r.receptor_quality)
    _assert_unit_interval(r.distortion)


# ===============================================================
# P. DETERMINISMO
# ===============================================================

def test_p1_determinismo():
    a = formula_maestra_l5(
        TODO_1, theta_y=0.22, agency=0.7, autoreference=0.6
    )
    b = formula_maestra_l5(
        TODO_1, theta_y=0.22, agency=0.7, autoreference=0.6
    )
    assert a == b


def test_p2_barrido_finito():
    for theta in (0.01, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.50):
        for autoreference in (0.0, BETA, 0.5, 1.0):
            result = formula_maestra_l5(
                TODO_1,
                theta_y=theta,
                agency=0.5,
                autoreference=autoreference,
            )
            assert math.isfinite(result.i5)
            assert math.isfinite(result.occupancy)
            assert math.isfinite(result.visibility)
            assert 0.0 <= result.i5 <= ALPHA + 1e-12
            assert result.observation_level in (1, 2, 3)


# ===============================================================
# Q. FLAGS / novelty vía calcular (no vía formula_maestra_l5)
# ===============================================================

def test_q1_loop_detected_se_propaga():
    assert formula_maestra_l5(TODO_1, loop_detected=True).loop_detected is True


def test_q2_loop_no_cambia_activaciones():
    a = formula_maestra_l5(TODO_1, loop_detected=False)
    b = formula_maestra_l5(TODO_1, loop_detected=True)
    assert a.activations_after == b.activations_after


def test_r1_novelty_en_calcular_no_modifica_N_ni_I5():
    """novelty está en calcular; formula_maestra_l5 de este fuente no lo expone."""
    engine = L5Metaconsciencia()
    a = engine.calcular(
        activations=TODO_1,
        theta_y=0.22,
        agency=1.0,
        autoreference=1.0,
        novelty=0.0,
    )
    b = engine.calcular(
        activations=TODO_1,
        theta_y=0.22,
        agency=1.0,
        autoreference=1.0,
        novelty=1.0,
    )
    assert a.observation_level == b.observation_level
    _assert_close(a.i5, b.i5)


# ===============================================================
# S. INVARIANTES DE MODELO
# ===============================================================

def test_s1_no_octava_capa():
    result = formula_maestra_l5(TODO_1, theta_y=0.22)
    assert len(result.activations_before) == 7
    assert len(result.activations_after) == 7
    assert len(result.geometry) == 7


def test_s2_L4_sigue_casa():
    result = formula_maestra_l5(
        TODO_1, theta_y=0.22, theta_eq=TC, agency=1.0, autoreference=1.0
    )
    assert result.geometry[L4].index == L4
    _assert_close(result.geometry[L4].z, TC)
    _assert_close(result.theta_eq, TC)


def test_s3_L5_observa_sin_reemplazar_L4():
    result = formula_maestra_l5(
        TODO_1, theta_y=0.22, theta_eq=TC, agency=1.0, autoreference=1.0
    )
    assert result.geometry[L5].index == L5
    assert result.geometry[L4].index == L4
    _assert_close(result.geometry[L4].z, TC)
