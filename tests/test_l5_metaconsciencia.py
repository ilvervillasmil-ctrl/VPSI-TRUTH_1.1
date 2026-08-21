# ===============================================================
# tests/test_l5_metaconsciencia.py
# ===============================================================
"""
Auditoría contractual de L5 — Metaconsciencia / Mirador.

Alineado al módulo real:
    modules/self/L5/metaconsciencia.py

Semilla / derivadas:
    ALPHA_F, BETA_F  ← modules.constante
    PHI_F, THETA_CUBE_F, LAYER_COUNT, DEFAULT_FRICTIONS
                     ← formulas_omega.constants

Matemática continua:
    C = a · r ∈ [0,1]
    gain = β · (a · r)
    conscious = product (float), no bool

Ejecutar:
    pytest -q tests/test_l5_metaconsciencia.py
"""

from __future__ import annotations

import inspect
import math

import pytest

import modules.constante as constante
import modules.formulas.formulas_omega.constants as omega_constants

from modules.self.L5.metaconsciencia import (
    ALPHA_F,
    BETA_F,
    PHI_F,
    THETA_CUBE_F,
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

TC = THETA_CUBE_F
SIGMA5 = 0.029707

TODO_1 = (1.0,) * LAYER_COUNT
CERO = (0.0,) * LAYER_COUNT
MEDIO = (0.5,) * LAYER_COUNT


# ===============================================================
# AUXILIARES
# ===============================================================

def _z(i: int) -> float:
    return TC * (PHI_F ** ((i - L4) / 2.0))


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


def test_a3_resultado_contiene_el_carril_completo():
    result = formula_maestra_l5(TODO_1)
    assert len(result.activations_before) == LAYER_COUNT
    assert len(result.activations_after) == LAYER_COUNT
    assert len(result.energies) == LAYER_COUNT
    assert len(result.weights) == LAYER_COUNT
    assert len(result.geometry) == LAYER_COUNT


# ===============================================================
# B. FUENTES CANÓNICAS (anti-hardcode)
# ===============================================================

def test_b1_alpha_sale_de_la_fuente_canonica():
    _assert_close(ALPHA_F, float(constante.ALPHA))


def test_b2_beta_sale_de_la_fuente_canonica():
    _assert_close(BETA_F, float(constante.BETA))


def test_b3_phi_sale_de_la_fuente_canonica():
    _assert_close(PHI_F, float(omega_constants.PHI))


def test_b4_theta_cube_sale_del_stack_canonico():
    _assert_close(THETA_CUBE_F, float(omega_constants.THETA_CUBE))


def test_b5_layer_count_sale_del_stack_canonico():
    assert LAYER_COUNT == int(omega_constants.NUM_LAYERS)


def test_b6_fricciones_por_defecto_alineadas():
    assert len(DEFAULT_FRICTIONS) == LAYER_COUNT
    assert len(DEFAULT_FRICTIONS) == int(omega_constants.NUM_LAYERS)
    for a, b in zip(DEFAULT_FRICTIONS, omega_constants.LAYER_FRICTION):
        _assert_close(a, float(b))


def test_b7_alpha_beta_conservan_el_cierre():
    _assert_close(ALPHA_F + BETA_F, 1.0)


def test_b8_umbrales_se_derivan_de_alpha_beta():
    _assert_close(THRESHOLD_N2, (BETA_F / ALPHA_F) ** 0.5)
    _assert_close(THRESHOLD_N3, (BETA_F / ALPHA_F) ** (1.0 / 3.0))


def test_b9_no_redefinicion_local_de_semilla():
    """
    El fuente no debe reasignar ALPHA/BETA/PHI como literales locales.
    """
    source = inspect.getsource(inspect.getmodule(formula_maestra_l5))
    for forbidden in (
        "ALPHA: float =",
        "BETA: float =",
        "PHI: float =",
        "ALPHA = 26",
        "BETA = 1",
    ):
        assert forbidden not in source


# ===============================================================
# C. CARRIL L0..L6
# ===============================================================

def test_c1_layer_count_coincide_con_num_layers():
    assert LAYER_COUNT == int(omega_constants.NUM_LAYERS)


def test_c2_indices_del_carril():
    assert (L0, L1, L2, L3, L4, L5, L6) == tuple(range(LAYER_COUNT))


def test_c3_L4_es_la_casa_del_yo():
    geometry = build_geometry()
    _assert_close(geometry[L4].z, TC)


def test_c4_L5_es_mirador_no_octava_capa():
    geometry = build_geometry()
    assert len(geometry) == LAYER_COUNT
    assert geometry[L5].index == L5
    assert geometry[L6].index == L6


def test_c5_geometria_indices():
    geometry = build_geometry()
    assert tuple(p.index for p in geometry) == tuple(range(LAYER_COUNT))


def test_c6_geometria_z_monotona():
    geometry = build_geometry()
    for i in range(LAYER_COUNT - 1):
        assert geometry[i].z < geometry[i + 1].z


def test_c7_theta_eq_no_modifica_geometria():
    a = L5Metaconsciencia(theta_eq=0.05).geometry
    b = L5Metaconsciencia(theta_eq=0.90).geometry
    assert [p.z for p in a] == [p.z for p in b]


# ===============================================================
# D. ENERGÍA Y PESOS
# ===============================================================

def test_d1_energias_longitud():
    assert len(calculate_energies(TODO_1)) == LAYER_COUNT


def test_d2_energia_formula():
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
    weights = normalize_weights(calculate_energies(TODO_1))
    _assert_close(sum(weights), 1.0)


def test_d5_sistema_apagado_pesos_uniformes():
    weights = normalize_weights(calculate_energies(CERO))
    for w in weights:
        _assert_close(w, 1.0 / LAYER_COUNT)


def test_d6_activaciones_invalidas():
    with pytest.raises(ValueError):
        calculate_energies((1.2,) + (0.0,) * (LAYER_COUNT - 1))
    with pytest.raises(ValueError):
        calculate_energies((0.5,) * (LAYER_COUNT - 1))


def test_d7_fricciones_invalidas():
    with pytest.raises(ValueError):
        calculate_energies(TODO_1, (1.2,) * LAYER_COUNT)
    with pytest.raises(ValueError):
        calculate_energies(TODO_1, (0.5,) * (LAYER_COUNT - 1))


# ===============================================================
# E. RECEPTOR L1..L4
# ===============================================================

def test_e1_coherencia_uniforme_maxima():
    _assert_close(default_coherence(TODO_1), 1.0)


def test_e2_desalineacion_reduce_coherencia():
    aligned = default_coherence((0.5, 0.8, 0.8, 0.8, 0.8, 0.5, 0.5))
    misaligned = default_coherence((0.5, 1.0, 0.1, 1.0, 0.1, 0.5, 0.5))
    assert aligned > misaligned


def test_e3_calibracion_L1_a_L4():
    frictions = (0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6)
    _, q5, _ = receptor_quality(TODO_1, frictions)
    expected = (
        (1.0 - frictions[L1])
        * (1.0 - frictions[L2])
        * (1.0 - frictions[L3])
        * (1.0 - frictions[L4])
    )
    # coh4 de TODO_1 = 1 → q5 = calibration
    _assert_close(q5, expected)


def test_e4_distorsion_complemento_q5():
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


def test_f2_ocupacion_maxima_en_z5():
    _assert_close(house_occupancy(_z(L5), _z(L5), SIGMA5), 1.0)


def test_f3_ocupacion_simetrica():
    delta = 0.01
    left = house_occupancy(_z(L5) - delta, _z(L5), SIGMA5)
    right = house_occupancy(_z(L5) + delta, _z(L5), SIGMA5)
    _assert_close(left, right)


def test_f4_ocupacion_decrece_con_distancia():
    center = house_occupancy(_z(L5), _z(L5), SIGMA5)
    nearby = house_occupancy(_z(L5) + 0.01, _z(L5), SIGMA5)
    far = house_occupancy(_z(L5) + 0.05, _z(L5), SIGMA5)
    assert center > nearby > far


def test_f5_ocupacion_en_rango():
    for delta in (0.0, 0.01, 0.05, 1.0):
        _assert_unit_interval(house_occupancy(_z(L5) + delta, _z(L5), SIGMA5))


# ===============================================================
# G. VISIBILIDAD
# ===============================================================

def test_g1_visibilidad_sobre_si_mismo():
    _assert_close(layer_visibility(_z(L5), _z(L5), TC), 1.0)


def test_g2_visibilidad_crece_hacia_L5():
    values = [layer_visibility(_z(L5), _z(i), TC) for i in range(L0, L5 + 1)]
    for i in range(len(values) - 1):
        assert values[i] < values[i + 1]


def test_g3_visibilidad_positiva():
    for i in range(LAYER_COUNT):
        assert layer_visibility(_z(L5), _z(i), TC) > 0.0


def test_g4_theta_cube_cero_rechazado():
    with pytest.raises(ValueError):
        layer_visibility(_z(L5), _z(L4), 0.0)


def test_g5_visibilidad_efectiva_en_rango():
    geometry = build_geometry()
    weights = normalize_weights(calculate_energies(TODO_1))
    v = effective_visibility(weights, geometry, theta_cube=TC)
    _assert_unit_interval(v)


# ===============================================================
# H. SEÑAL I5
# ===============================================================

def test_h1_i5_techo_alpha():
    value = calculate_i5(q5=1.0, h5=1.0, v5=1.0)
    _assert_close(value, ALPHA_F)
    assert value <= ALPHA_F + 1e-12


def test_h2_i5_monotona_q5():
    assert calculate_i5(q5=0.6, h5=0.8, v5=0.8) > calculate_i5(
        q5=0.4, h5=0.8, v5=0.8
    )


def test_h3_i5_monotona_h5():
    assert calculate_i5(q5=0.8, h5=0.6, v5=0.8) > calculate_i5(
        q5=0.8, h5=0.4, v5=0.8
    )


def test_h4_i5_monotona_v5():
    assert calculate_i5(q5=0.8, h5=0.8, v5=0.6) > calculate_i5(
        q5=0.8, h5=0.8, v5=0.4
    )


def test_h5_i5_en_rango():
    for q5 in (0.0, 0.5, 1.0):
        for h5 in (0.0, 0.5, 1.0):
            for v5 in (0.0, 0.5, 1.0):
                value = calculate_i5(q5=q5, h5=h5, v5=v5)
                assert 0.0 <= value <= ALPHA_F + 1e-12


# ===============================================================
# I. OBSERVACIÓN RECURSIVA
# ===============================================================

def test_i1_orden_uno_reproduce_i5():
    for i5 in (0.05, 0.2, 0.5, min(0.9, ALPHA_F)):
        _assert_close(observation_intensity(i5, 1), i5)


def test_i2_recursion_disminuye():
    i5 = 0.5 * ALPHA_F
    assert observation_intensity(i5, 1) > observation_intensity(i5, 2)
    assert observation_intensity(i5, 2) > observation_intensity(i5, 3)


def test_i3_orden_invalido():
    with pytest.raises(ValueError):
        observation_intensity(0.5, 0)


def test_i4_intensidades_en_rango():
    for i5 in (0.0, 0.1, 0.5 * ALPHA_F, ALPHA_F):
        for k in (1, 2, 3):
            value = observation_intensity(i5, k)
            assert 0.0 <= value <= ALPHA_F + 1e-12


# ===============================================================
# J. EJE N
# ===============================================================

def test_j1_sin_autoreferencia_minima_es_N1():
    assert determine_observation_level(0.9, autoreference=BETA_F * 0.5) == N_MIN
    assert determine_observation_level(0.9, autoreference=0.0) == N_MIN


def test_j2_N1_piso():
    assert determine_observation_level(0.0, autoreference=1.0) == N_MIN


def test_j3_umbral_N2_inclusivo():
    value = ALPHA_F * THRESHOLD_N2
    assert determine_observation_level(value, autoreference=1.0) == 2


def test_j4_bajo_N2_permanece_N1():
    value = ALPHA_F * THRESHOLD_N2 * 0.999
    assert determine_observation_level(value, autoreference=1.0) == 1


def test_j5_umbral_N3_inclusivo():
    value = ALPHA_F * THRESHOLD_N3
    assert determine_observation_level(value, autoreference=1.0) == 3


def test_j6_bajo_N3_permanece_N2():
    value = ALPHA_F * THRESHOLD_N3 * 0.999
    assert determine_observation_level(value, autoreference=1.0) == 2


def test_j7_eje_acotado_N1_N3():
    for i5 in (0.0, 0.1, 0.5, 0.9, ALPHA_F):
        for ar in (0.0, BETA_F, 0.5, 1.0):
            level = determine_observation_level(i5, autoreference=ar)
            assert N_MIN <= level <= N_MAX


# ===============================================================
# K. CONTROL CONTINUO  C = a · r
# ===============================================================

def test_k1_producto_continuo_y_codigos():
    cases = (
        (0.0, 0.0, "2.1", 0.0),
        (0.0, 1.0, "2.2", 0.0),
        (1.0, 0.0, "2.3", 0.0),
        (1.0, 1.0, "2.4", 1.0),
        (0.5, 0.4, "2.4", 0.2),
    )
    for agency, autoreference, code, product in cases:
        cfg = control_configuration(2, agency=agency, autoreference=autoreference)
        assert cfg.code == code
        _assert_close(cfg.agency, agency)
        _assert_close(cfg.autoreference, autoreference)
        _assert_close(cfg.product, product)
        _assert_close(cfg.conscious, product)
        assert isinstance(cfg.conscious, float)


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
    _assert_close(cfg1.product, 0.0)
    _assert_close(cfg2.product, 0.0)


def test_k4_producto_parcial_no_es_bool():
    cfg = control_configuration(2, agency=0.3, autoreference=0.5)
    _assert_close(cfg.product, 0.15)
    _assert_close(cfg.conscious, 0.15)
    assert cfg.conscious != 0.0
    assert cfg.conscious != 1.0


# ===============================================================
# L. CASA DEL YO = L4
# ===============================================================

def test_l1_casa_en_L4():
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


def test_l3_yo_state_no_declara_L5_como_casa():
    for level in (1, 2, 3):
        state = yo_state(level, agency=1.0, autoreference=1.0)
        assert "L5" not in state


# ===============================================================
# M. RETORNO  gain = β · (a · r)
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


def test_m3_retorno_reduce_L1_L2_L3():
    after = decode_downward_signal(
        MEDIO, observation_level=2, agency=1.0, autoreference=1.0
    )
    assert after[L1] < MEDIO[L1]
    assert after[L2] < MEDIO[L2]
    assert after[L3] < MEDIO[L3]


def test_m4_retorno_refuerza_L4():
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
    gain = BETA_F * agency * autoreference
    _assert_close(after[L1], MEDIO[L1] * (1.0 - gain))
    _assert_close(after[L4], min(1.0, MEDIO[L4] * (1.0 + gain)))


def test_m7_entrada_no_se_muta():
    before = [0.5] * LAYER_COUNT
    copy_before = list(before)
    decode_downward_signal(
        before, observation_level=2, agency=1.0, autoreference=1.0
    )
    assert before == copy_before


def test_m8_salida_en_rango():
    after = decode_downward_signal(
        MEDIO, observation_level=3, agency=1.0, autoreference=1.0
    )
    for value in after:
        _assert_unit_interval(value)


def test_m9_L4_saturado_no_supera_uno():
    before = (0.5, 0.5, 0.5, 0.5, 1.0, 0.5, 0.5)
    after = decode_downward_signal(
        before, observation_level=2, agency=1.0, autoreference=1.0
    )
    _assert_close(after[L4], 1.0)


# ===============================================================
# N. TRAZAS DE MOVIMIENTO
# ===============================================================

def test_n1_movimientos_solo_cambios_reales():
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


def test_n3_L4_saturado_sin_movimiento_reportado():
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
    _assert_close(result.control.product, 1.0)
    _assert_close(result.control.conscious, 1.0)


def test_o2_i5_en_rango():
    result = formula_maestra_l5(TODO_1, theta_y=TC, agency=1.0, autoreference=1.0)
    assert 0.0 <= result.i5 <= ALPHA_F + 1e-12


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
        for autoreference in (0.0, BETA_F, 0.5, 1.0):
            result = formula_maestra_l5(
                TODO_1,
                theta_y=theta,
                agency=0.5,
                autoreference=autoreference,
            )
            assert math.isfinite(result.i5)
            assert math.isfinite(result.occupancy)
            assert math.isfinite(result.visibility)
            assert 0.0 <= result.i5 <= ALPHA_F + 1e-12
            assert result.observation_level in (1, 2, 3)


# ===============================================================
# Q. FLAGS / NOVELTY (contrato actual)
# ===============================================================

def test_q1_loop_detected_se_propaga():
    assert formula_maestra_l5(TODO_1, loop_detected=True).loop_detected is True


def test_q2_loop_no_cambia_activaciones():
    a = formula_maestra_l5(TODO_1, loop_detected=False)
    b = formula_maestra_l5(TODO_1, loop_detected=True)
    assert a.activations_after == b.activations_after


def test_r1_novelty_no_modifica_N_ni_I5():
    a = formula_maestra_l5(
        TODO_1, theta_y=0.22, agency=1.0, autoreference=1.0, novelty=0.0
    )
    b = formula_maestra_l5(
        TODO_1, theta_y=0.22, agency=1.0, autoreference=1.0, novelty=1.0
    )
    assert a.observation_level == b.observation_level
    _assert_close(a.i5, b.i5)


# ===============================================================
# S. INVARIANTES DE MODELO
# ===============================================================

def test_s1_no_octava_capa():
    result = formula_maestra_l5(TODO_1, theta_y=0.22)
    assert len(result.activations_before) == LAYER_COUNT
    assert len(result.activations_after) == LAYER_COUNT
    assert len(result.geometry) == LAYER_COUNT


def test_s2_L4_sigue_siendo_casa():
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
