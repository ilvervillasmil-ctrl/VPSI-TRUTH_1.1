# ===============================================================
# tests/test_l5_metaconsciencia.py
# ===============================================================
"""
Auditoría contractual completa de L5 — Metaconsciencia / Mirador.

Ejecutar:
    pytest -q tests/test_l5_metaconsciencia.py

PRINCIPIO:
-----------
Este test verifica únicamente aquello que el módulo L5 declara como
contrato operativo, invariantes estructurales o comportamiento explícito.

No convierte mecanismos parametrizables en axiomas.
No exige comportamiento de novelty/loop que el módulo declara pendiente.
No confunde saturación numérica con movimiento observable.
No redefine constantes canónicas dentro del test.
"""

import math
import inspect
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

TODO_1 = (1.0,) * 7
CERO = (0.0,) * 7
MEDIO = (0.5,) * 7


# ===============================================================
# AUXILIARES
# ===============================================================

def _z(i: int) -> float:
    return TC * PHI ** ((i - L4) / 2.0)


def _frontera(a: int, b: int) -> float:
    return math.sqrt(_z(a) * _z(b))


def _assert_unit_interval(value: float) -> None:
    assert math.isfinite(value)
    assert 0.0 <= value <= 1.0


# ===============================================================
# A. ARRANQUE Y API
# ===============================================================

def test_a1_formula_maestra_arranca():
    """
    La API pública principal debe poder ejecutar el carril completo.
    """
    result = formula_maestra_l5(
        TODO_1,
        theta_y=TC,
        agency=1.0,
        autoreference=1.0,
    )

    assert result is not None


def test_a2_motor_l5_arranca():
    """
    La clase principal debe poder construirse con sus parámetros por defecto.
    """
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
# B. FUENTES CANÓNICAS
# ===============================================================

def test_b1_alpha_sale_de_la_fuente_canonica():
    """
    L5 importa ALPHA desde modules.constante.

    No se permite que el valor operativo se separe de esa fuente.
    """
    assert ALPHA == float(constante.ALPHA)


def test_b2_beta_sale_de_la_fuente_canonica():
    """
    L5 importa BETA desde modules.constante.
    """
    assert BETA == float(constante.BETA)


def test_b3_phi_sale_de_la_fuente_canonica():
    """
    PHI debe corresponder al valor canónico del stack de formulas_omega.
    """
    assert PHI == float(omega_constants.PHI)


def test_b4_theta_cube_operativo_sale_del_stack_canonico():
    """
    THETA_CUBE_DEFAULT debe coincidir con THETA_CUBE del stack canónico.
    """
    assert THETA_CUBE_DEFAULT == float(omega_constants.THETA_CUBE)


def test_b5_layer_count_sale_del_stack_canonico():
    """
    El número de capas no debe divergir del contrato del stack.
    """
    assert LAYER_COUNT == int(omega_constants.NUM_LAYERS)


def test_b6_fricciones_por_defecto_tienen_el_tamano_canonico():
    assert len(DEFAULT_FRICTIONS) == LAYER_COUNT
    assert len(DEFAULT_FRICTIONS) == int(omega_constants.NUM_LAYERS)


def test_b7_alpha_beta_conservan_el_cierre():
    assert abs(ALPHA + BETA - 1.0) < 1e-12


def test_b8_umbrales_se_derivan_de_alpha_beta():
    assert abs(
        THRESHOLD_N2 - (BETA / ALPHA) ** 0.5
    ) < 1e-12

    assert abs(
        THRESHOLD_N3 - (BETA / ALPHA) ** (1.0 / 3.0)
    ) < 1e-12


def test_b9_no_hay_redefinicion_local_de_constantes_canonicas():
    """
    Auditoría estructural del contrato:

        α, β ← modules.constante
        Φ, θ_cube, ... ← formulas_omega.constants

    El módulo no debe volver a declarar mediante asignación:

        ALPHA = ...
        BETA = ...
        PHI = ...

    Esta prueba no impone un estilo de implementación arbitrario:
    comprueba directamente que las constantes importadas no sean
    sobrescritas posteriormente en el código fuente.
    """
    source = inspect.getsource(
        inspect.getmodule(formula_maestra_l5)
    )

    forbidden = (
        "ALPHA: float =",
        "BETA: float =",
        "PHI: float =",
    )

    for assignment in forbidden:
        assert assignment not in source


# ===============================================================
# C. CARRIL L0..L6
# ===============================================================

def test_c1_existen_exactamente_siete_capas():
    assert LAYER_COUNT == 7


def test_c2_indices_del_carril_son_L0_a_L6():
    assert (L0, L1, L2, L3, L4, L5, L6) == (
        0, 1, 2, 3, 4, 5, 6
    )


def test_c3_L4_es_la_casa_del_yo():
    geometry = build_geometry()

    assert abs(geometry[L4].z - TC) < 1e-15


def test_c4_L5_es_mirador_y_no_octava_capa():
    geometry = build_geometry()

    assert len(geometry) == 7
    assert geometry[L5].index == 5
    assert geometry[L6].index == 6


def test_c5_geometria_tiene_siete_posiciones():
    geometry = build_geometry()

    assert tuple(p.index for p in geometry) == tuple(range(7))


def test_c6_geometria_es_monotona():
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

def test_d1_energias_tienen_siete_componentes():
    energies = calculate_energies(TODO_1)

    assert len(energies) == LAYER_COUNT


def test_d2_energia_respeta_formula_declarada():
    geometry = build_geometry()
    energies = calculate_energies(
        TODO_1,
        (0.0,) * LAYER_COUNT,
        geometry,
    )

    for i in range(LAYER_COUNT):
        expected = geometry[i].radius
        assert abs(energies[i] - expected) < 1e-12


def test_d3_friccion_reduce_energia():
    base = calculate_energies(
        TODO_1,
        (0.0,) * LAYER_COUNT,
    )

    friction = [0.0] * LAYER_COUNT
    friction[L3] = 0.5

    reduced = calculate_energies(
        TODO_1,
        friction,
    )

    assert reduced[L3] < base[L3]


def test_d4_pesos_suman_uno():
    weights = normalize_weights(
        calculate_energies(TODO_1)
    )

    assert abs(sum(weights) - 1.0) < 1e-12


def test_d5_sistema_apagado_produce_pesos_uniformes():
    weights = normalize_weights(
        calculate_energies(CERO)
    )

    assert all(
        abs(x - 1.0 / LAYER_COUNT) < 1e-12
        for x in weights
    )


def test_d6_activaciones_fuera_de_rango_se_rechazan():
    with pytest.raises(ValueError):
        calculate_energies(
            (1.2, 0, 0, 0, 0, 0, 0)
        )

    with pytest.raises(ValueError):
        calculate_energies(
            (0.5,) * 6
        )


def test_d7_fricciones_fuera_de_rango_se_rechazan():
    with pytest.raises(ValueError):
        calculate_energies(
            TODO_1,
            (1.2,) * 7,
        )

    with pytest.raises(ValueError):
        calculate_energies(
            TODO_1,
            (0.5,) * 6,
        )


# ===============================================================
# E. COHERENCIA DEL RECEPTOR L1..L4
# ===============================================================

def test_e1_receptor_usa_L1_a_L4():
    """
    Con activaciones uniformes, la coherencia interna debe ser máxima
    para el mecanismo operativo por defecto.
    """
    coherence = default_coherence(TODO_1)

    assert abs(coherence - 1.0) < 1e-12


def test_e2_desalineacion_reduce_coherencia():
    aligned = default_coherence(
        (0.5, 0.8, 0.8, 0.8, 0.8, 0.5, 0.5)
    )

    misaligned = default_coherence(
        (0.5, 1.0, 0.1, 1.0, 0.1, 0.5, 0.5)
    )

    assert aligned > misaligned


def test_e3_calibracion_usa_L1_a_L4():
    frictions = (0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6)

    _, q5, _ = receptor_quality(
        TODO_1,
        frictions,
    )

    expected = (
        (1.0 - frictions[L1])
        * (1.0 - frictions[L2])
        * (1.0 - frictions[L3])
        * (1.0 - frictions[L4])
    )

    assert abs(q5 - expected) < 1e-12


def test_e4_distorsion_es_complemento_de_q5():
    _, q5, distortion = receptor_quality(
        TODO_1,
        DEFAULT_FRICTIONS,
    )

    assert abs(q5 + distortion - 1.0) < 1e-12


def test_e5_receptor_esta_en_rango():
    _, q5, distortion = receptor_quality(
        TODO_1,
        DEFAULT_FRICTIONS,
    )

    _assert_unit_interval(q5)
    _assert_unit_interval(distortion)


def test_e6_sistema_apagado_no_debe_producir_coherencia_perfecta():
    """
    Falla semántica real del mecanismo actual.

    Con L1..L4 = 0, la implementación actual asigna pares = 1.0
    cuando ambos valores son cero. Eso produce coherencia perfecta
    para un receptor completamente apagado.

    El estado muerto no debe confundirse con alineación funcional.
    """
    coherence, q5, _ = receptor_quality(
        CERO,
        DEFAULT_FRICTIONS,
    )

    assert coherence < 1.0
    assert q5 < 1.0


# ===============================================================
# F. OCUPACIÓN DEL MIRADOR
# ===============================================================

def test_f1_sigma5_debe_ser_positivo():
    with pytest.raises(ValueError):
        house_occupancy(
            TC,
            _z(L5),
            0.0,
        )


def test_f2_ocupacion_maxima_en_misma_posicion():
    occupancy = house_occupancy(
        _z(L5),
        _z(L5),
        SIGMA5,
    )

    assert abs(occupancy - 1.0) < 1e-12


def test_f3_ocupacion_es_simetrica():
    delta = 0.01

    left = house_occupancy(
        _z(L5) - delta,
        _z(L5),
        SIGMA5,
    )

    right = house_occupancy(
        _z(L5) + delta,
        _z(L5),
        SIGMA5,
    )

    assert abs(left - right) < 1e-12


def test_f4_ocupacion_disminuye_al_alejarse():
    center = house_occupancy(
        _z(L5),
        _z(L5),
        SIGMA5,
    )

    nearby = house_occupancy(
        _z(L5) + 0.01,
        _z(L5),
        SIGMA5,
    )

    far = house_occupancy(
        _z(L5) + 0.05,
        _z(L5),
        SIGMA5,
    )

    assert center > nearby > far


def test_f5_ocupacion_esta_en_rango():
    for delta in (0.0, 0.01, 0.05, 1.0):
        value = house_occupancy(
            _z(L5) + delta,
            _z(L5),
            SIGMA5,
        )

        _assert_unit_interval(value)


# ===============================================================
# G. VISIBILIDAD
# ===============================================================

def test_g1_visibilidad_de_L5_sobre_si_mismo_es_uno():
    value = layer_visibility(
        _z(L5),
        _z(L5),
        TC,
    )

    assert abs(value - 1.0) < 1e-12


def test_g2_visibilidad_decrece_con_distancia():
    values = [
        layer_visibility(
            _z(L5),
            _z(i),
            TC,
        )
        for i in range(LAYER_COUNT)
    ]

    assert values[L0] < values[L1]
    assert values[L1] < values[L2]
    assert values[L2] < values[L3]
    assert values[L3] < values[L4]
    assert values[L4] < values[L5]


def test_g3_visibilidad_es_positiva():
    for i in range(LAYER_COUNT):
        value = layer_visibility(
            _z(L5),
            _z(i),
            TC,
        )

        assert value > 0.0


def test_g4_theta_cube_cero_se_rechaza():
    with pytest.raises(ValueError):
        layer_visibility(
            _z(L5),
            _z(L4),
            0.0,
        )


def test_g5_visibilidad_efectiva_usa_L0_a_L4():
    geometry = build_geometry()
    weights = normalize_weights(
        calculate_energies(TODO_1)
    )

    visibility = effective_visibility(
        weights,
        geometry,
        theta_cube=TC,
    )

    _assert_unit_interval(visibility)


# ===============================================================
# H. SEÑAL I5
# ===============================================================

def test_h1_i5_tiene_techo_alpha():
    value = calculate_i5(
        q5=1.0,
        h5=1.0,
        v5=1.0,
    )

    assert value <= ALPHA + 1e-12


def test_h2_i5_es_monotona_en_q5():
    a = calculate_i5(
        q5=0.4,
        h5=0.8,
        v5=0.8,
    )

    b = calculate_i5(
        q5=0.6,
        h5=0.8,
        v5=0.8,
    )

    assert b > a


def test_h3_i5_es_monotona_en_h5():
    a = calculate_i5(
        q5=0.8,
        h5=0.4,
        v5=0.8,
    )

    b = calculate_i5(
        q5=0.8,
        h5=0.6,
        v5=0.8,
    )

    assert b > a


def test_h4_i5_es_monotona_en_v5():
    a = calculate_i5(
        q5=0.8,
        h5=0.8,
        v5=0.4,
    )

    b = calculate_i5(
        q5=0.8,
        h5=0.8,
        v5=0.6,
    )

    assert b > a


def test_h5_i5_esta_en_rango():
    for q5 in (0.0, 0.5, 1.0):
        for h5 in (0.0, 0.5, 1.0):
            for v5 in (0.0, 0.5, 1.0):
                value = calculate_i5(
                    q5=q5,
                    h5=h5,
                    v5=v5,
                )

                assert 0.0 <= value <= ALPHA + 1e-12


# ===============================================================
# I. OBSERVACIÓN RECURSIVA
# ===============================================================

def test_i1_orden_uno_reproduce_i5():
    for i5 in (0.05, 0.2, 0.5, 0.9):
        assert abs(
            observation_intensity(i5, 1) - i5
        ) < 1e-12


def test_i2_recursion_disminuye_para_i5_normalizado_menor_que_uno():
    i5 = 0.5

    i1 = observation_intensity(i5, 1)
    i2 = observation_intensity(i5, 2)
    i3 = observation_intensity(i5, 3)

    assert i1 > i2 > i3


def test_i3_orden_invalido_se_rechaza():
    with pytest.raises(ValueError):
        observation_intensity(0.5, 0)


def test_i4_intensidades_estan_en_rango():
    for i5 in (0.0, 0.1, 0.5, ALPHA):
        for k in (1, 2, 3):
            value = observation_intensity(i5, k)

            assert 0.0 <= value <= ALPHA + 1e-12


# ===============================================================
# J. EJE N
# ===============================================================

def test_j1_sin_autoreferencia_minima_n_es_N1():
    assert determine_observation_level(
        0.9,
        autoreference=BETA - 1e-9,
    ) == N_MIN

    assert determine_observation_level(
        0.9,
        autoreference=0.0,
    ) == N_MIN


def test_j2_N1_es_el_piso():
    assert determine_observation_level(
        0.0,
        autoreference=1.0,
    ) == N_MIN


def test_j3_umbral_N2_es_inclusivo():
    value = ALPHA * THRESHOLD_N2

    assert determine_observation_level(
        value,
        autoreference=1.0,
    ) == 2


def test_j4_por_debajo_de_N2_se_permanece_en_N1():
    value = ALPHA * THRESHOLD_N2 * 0.999

    assert determine_observation_level(
        value,
        autoreference=1.0,
    ) == 1


def test_j5_umbral_N3_es_inclusivo():
    value = ALPHA * THRESHOLD_N3

    assert determine_observation_level(
        value,
        autoreference=1.0,
    ) == 3


def test_j6_por_debajo_de_N3_se_permanece_en_N2():
    value = ALPHA * THRESHOLD_N3 * 0.999

    assert determine_observation_level(
        value,
        autoreference=1.0,
    ) == 2


def test_j7_nunca_sale_del_eje_N1_N3():
    for i5 in (0.0, 0.1, 0.5, 0.9, ALPHA):
        for ar in (0.0, BETA, 0.5, 1.0):
            level = determine_observation_level(
                i5,
                autoreference=ar,
            )

            assert N_MIN <= level <= N_MAX


# ===============================================================
# K. CONFIGURACIONES DE CONTROL
# ===============================================================

def test_k1_existen_las_cuatro_configuraciones():
    cases = (
        (0.0, 0.0, "2.1", False),
        (0.0, 1.0, "2.2", False),
        (1.0, 0.0, "2.3", False),
        (1.0, 1.0, "2.4", True),
    )

    for agency, autoreference, expected_code, conscious in cases:
        cfg = control_configuration(
            2,
            agency=agency,
            autoreference=autoreference,
        )

        assert cfg.code == expected_code
        assert cfg.conscious is conscious


def test_k2_nivel_invalido_se_rechaza():
    with pytest.raises(ValueError):
        control_configuration(
            0,
            agency=1.0,
            autoreference=1.0,
        )

    with pytest.raises(ValueError):
        control_configuration(
            4,
            agency=1.0,
            autoreference=1.0,
        )


def test_k3_agencia_y_autoreferencia_son_dimensiones_independientes():
    cfg1 = control_configuration(
        2,
        agency=1.0,
        autoreference=0.0,
    )

    cfg2 = control_configuration(
        2,
        agency=0.0,
        autoreference=1.0,
    )

    assert cfg1.code == "2.3"
    assert cfg2.code == "2.2"
    assert cfg1.conscious is False
    assert cfg2.conscious is False


def test_k4_consciencia_requiere_agencia_y_autoreferencia():
    cfg = control_configuration(
        2,
        agency=1.0,
        autoreference=1.0,
    )

    assert cfg.conscious is True


# ===============================================================
# L. CASA DEL YO
# ===============================================================

def test_l1_la_casa_del_yo_permanece_en_L4():
    engine = L5Metaconsciencia()

    assert engine.geometry[L4].index == L4


def test_l2_theta_eq_no_transfiere_el_yo_a_L5():
    result = formula_maestra_l5(
        TODO_1,
        theta_y=0.22,
        theta_eq=TC,
        agency=1.0,
        autoreference=1.0,
    )

    assert result.theta_eq == TC
    assert result.geometry[L4].z == TC


def test_l3_yo_state_no_declara_L5_como_casa():
    for level in (1, 2, 3):
        state = yo_state(
            level,
            agency=1.0,
            autoreference=1.0,
        )

        assert "L5" not in state


# ===============================================================
# M. RETORNO DESCENDENTE
# ===============================================================

def test_m1_sin_agencia_no_hay_retorno():
    before = MEDIO

    after = decode_downward_signal(
        before,
        observation_level=3,
        agency=0.0,
        autoreference=1.0,
    )

    assert after == before


def test_m2_sin_autoreferencia_no_hay_retorno():
    before = MEDIO

    after = decode_downward_signal(
        before,
        observation_level=3,
        agency=1.0,
        autoreference=0.0,
    )

    assert after == before


def test_m3_retorno_reduce_L1_L2_L3():
    before = MEDIO

    after = decode_downward_signal(
        before,
        observation_level=2,
        agency=1.0,
        autoreference=1.0,
    )

    assert after[L1] < before[L1]
    assert after[L2] < before[L2]
    assert after[L3] < before[L3]


def test_m4_retorno_refuerza_L4_si_no_esta_saturado():
    before = (
        0.5,
        0.5,
        0.5,
        0.5,
        0.5,
        0.5,
        0.5,
    )

    after = decode_downward_signal(
        before,
        observation_level=2,
        agency=1.0,
        autoreference=1.0,
    )

    assert after[L4] > before[L4]


def test_m5_L0_L5_L6_no_son_modificados():
    before = MEDIO

    after = decode_downward_signal(
        before,
        observation_level=3,
        agency=1.0,
        autoreference=1.0,
    )

    for index in (L0, L5, L6):
        assert after[index] == before[index]


def test_m6_ganancia_es_beta_por_producto_agencia_autoreferencia():
    before = MEDIO

    agency = 0.8
    autoreference = 0.6

    after = decode_downward_signal(
        before,
        observation_level=2,
        agency=agency,
        autoreference=autoreference,
    )

    gain = BETA * agency * autoreference

    expected = before[L1] * (1.0 - gain)

    assert abs(after[L1] - expected) < 1e-12


def test_m7_entrada_no_se_muta():
    before = [0.5] * 7
    copy_before = list(before)

    decode_downward_signal(
        before,
        observation_level=2,
        agency=1.0,
        autoreference=1.0,
    )

    assert before == copy_before


def test_m8_salida_permanece_en_rango():
    after = decode_downward_signal(
        MEDIO,
        observation_level=3,
        agency=1.0,
        autoreference=1.0,
    )

    for value in after:
        _assert_unit_interval(value)


def test_m9_L4_saturado_no_debe_superar_uno():
    """
    Saturación válida: el clamp protege el dominio [0,1].

    No se exige un movimiento observable porque 1.0 ya es el máximo
    permitido. Esto sustituye al falso supuesto del test Z3 anterior.
    """
    before = (
        0.5,
        0.5,
        0.5,
        0.5,
        1.0,
        0.5,
        0.5,
    )

    after = decode_downward_signal(
        before,
        observation_level=2,
        agency=1.0,
        autoreference=1.0,
    )

    assert after[L4] == 1.0


# ===============================================================
# N. TRAZAS DE MOVIMIENTO
# ===============================================================

def test_n1_movimientos_solo_registran_cambios_reales():
    before = MEDIO

    after = decode_downward_signal(
        before,
        observation_level=2,
        agency=1.0,
        autoreference=1.0,
    )

    movements = describe_movement(
        before,
        after,
    )

    targets = {
        movement.target_layer
        for movement in movements
    }

    assert targets == {
        L1,
        L2,
        L3,
        L4,
    }


def test_n2_movimiento_tiene_origen_L5():
    before = MEDIO

    after = decode_downward_signal(
        before,
        observation_level=2,
        agency=1.0,
        autoreference=1.0,
    )

    movements = describe_movement(
        before,
        after,
    )

    assert all(
        movement.source_layer == L5
        for movement in movements
    )


def test_n3_L4_saturado_no_se_reporta_como_movimiento():
    before = (
        0.5,
        0.5,
        0.5,
        0.5,
        1.0,
        0.5,
        0.5,
    )

    after = decode_downward_signal(
        before,
        observation_level=2,
        agency=1.0,
        autoreference=1.0,
    )

    movements = describe_movement(
        before,
        after,
    )

    targets = {
        movement.target_layer
        for movement in movements
    }

    assert L4 not in targets


# ===============================================================
# O. RESULTADO INTEGRAL
# ===============================================================

def test_o1_formula_maestra_produce_resultado_coherente():
    result = formula_maestra_l5(
        TODO_1,
        theta_y=TC,
        agency=1.0,
        autoreference=1.0,
    )

    assert len(result.observation_intensities) == 3
    assert result.observation_level in (1, 2, 3)
    assert result.control.level == result.observation_level
    assert result.loop_detected is False


def test_o2_i5_resultado_esta_en_rango():
    result = formula_maestra_l5(
        TODO_1,
        theta_y=TC,
        agency=1.0,
        autoreference=1.0,
    )

    assert 0.0 <= result.i5 <= ALPHA + 1e-12


def test_o3_ocupacion_resultado_esta_en_rango():
    result = formula_maestra_l5(
        TODO_1,
        theta_y=TC,
    )

    _assert_unit_interval(result.occupancy)


def test_o4_visibilidad_resultado_esta_en_rango():
    result = formula_maestra_l5(
        TODO_1,
        theta_y=TC,
    )

    _assert_unit_interval(result.visibility)


def test_o5_receptor_resultado_esta_en_rango():
    result = formula_maestra_l5(
        TODO_1,
        theta_y=TC,
    )

    _assert_unit_interval(result.coherence)
    _assert_unit_interval(result.receptor_quality)
    _assert_unit_interval(result.distortion)


# ===============================================================
# P. DETERMINISMO
# ===============================================================

def test_p1_determinismo():
    a = formula_maestra_l5(
        TODO_1,
        theta_y=0.22,
        agency=0.7,
        autoreference=0.6,
    )

    b = formula_maestra_l5(
        TODO_1,
        theta_y=0.22,
        agency=0.7,
        autoreference=0.6,
    )

    assert a == b


def test_p2_barrido_finito():
    for theta in (
        0.01,
        0.05,
        0.10,
        0.15,
        0.20,
        0.25,
        0.30,
        0.50,
    ):
        for autoreference in (
            0.0,
            BETA,
            0.5,
            1.0,
        ):
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
            assert 0.0 <= result.occupancy <= 1.0
            assert 0.0 <= result.visibility <= 1.0
            assert result.observation_level in (1, 2, 3)


# ===============================================================
# Q. PROPAGACIÓN DE FLAGS
# ===============================================================

def test_q1_loop_detected_se_propaga():
    result = formula_maestra_l5(
        TODO_1,
        loop_detected=True,
    )

    assert result.loop_detected is True


def test_q2_loop_detected_no_modifica_por_si_solo_el_resultado_actual():
    """
    El propio módulo declara loop_detected como lectura y no implementa
    todavía una transición F_beta.

    Por tanto, no se exige aquí que cambie activations_after.
    """
    a = formula_maestra_l5(
        TODO_1,
        loop_detected=False,
    )

    b = formula_maestra_l5(
        TODO_1,
        loop_detected=True,
    )

    assert a.loop_detected is False
    assert b.loop_detected is True
    assert a.activations_after == b.activations_after


# ===============================================================
# R. NOVELTY: CONTRATO ACTUAL, NO FUTURO
# ===============================================================

def test_r1_novelty_no_modifica_N_en_la_implementacion_actual():
    """
    novelty está declarada como reservada y el módulo explícitamente
    descarta su efecto operativo actual.

    No se inventa aquí una dinámica que todavía no existe.
    """
    a = formula_maestra_l5(
        TODO_1,
        theta_y=0.22,
        agency=1.0,
        autoreference=1.0,
        novelty=0.0,
    )

    b = formula_maestra_l5(
        TODO_1,
        theta_y=0.22,
        agency=1.0,
        autoreference=1.0,
        novelty=1.0,
    )

    assert a.observation_level == b.observation_level
    assert a.i5 == b.i5


# ===============================================================
# S. INVARIANTE FUNDAMENTAL DEL MODELO
# ===============================================================

def test_s1_L5_no_se_convierte_en_octava_capa():
    """
    La existencia de L5 es una posición del carril L0..L6 y un mirador
    semántico; el módulo no puede producir una octava posición.
    """
    result = formula_maestra_l5(
        TODO_1,
        theta_y=0.22,
    )

    assert len(result.activations_before) == 7
    assert len(result.activations_after) == 7
    assert len(result.geometry) == 7


def test_s2_L4_sigue_siendola_casa_del_yo():
    result = formula_maestra_l5(
        TODO_1,
        theta_y=0.22,
        theta_eq=TC,
        agency=1.0,
        autoreference=1.0,
    )

    assert result.geometry[L4].index == L4
    assert result.geometry[L4].z == TC
    assert result.theta_eq == TC


def test_s3_L5_observa_sin_reemplazar_L4():
    result = formula_maestra_l5(
        TODO_1,
        theta_y=0.22,
        theta_eq=TC,
        agency=1.0,
        autoreference=1.0,
    )

    assert result.geometry[L5].index == L5
    assert result.geometry[L4].index == L4
    assert result.geometry[L4].z == TC
