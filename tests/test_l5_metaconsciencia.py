# -*- coding: utf-8 -*-
"""
VPSI-TRUTH — TEST DL5
modules/self/L5/metaconsciencia.py

Propósito
---------
Validar el contrato matemático y causal del mirador L5.

Este test NO hardcodea resultados derivados de la fórmula.
Las propiedades se comprueban por invariancia, causalidad y
consistencia entre ejecuciones.

Contrato DL5 relevante
----------------------
    activations[0..6]       → carril L0..L6
    theta_y                 → posición del Yo
    theta_eq                → equilibrio del Yo
    agency                  → agencia
    autoreference           → autoreferencia
    novelty                 → entrada reservada; no altera N ni I5
    loop_detected           → lectura de estado del loop

Cadena principal
----------------
    activations
        ↓
    energies / weights
        ↓
    coherence / receptor_quality
        ↓
    h5 / V5
        ↓
    I5
        ↓
    observation_level N
        ↓
    control
        ↓
    retorno opcional
"""

from __future__ import annotations

import pytest

from modules.self.L5.metaconsciencia import (
    ALPHA_F,
    BETA_F,
    THETA_CUBE_F,
    THRESHOLD_N2,
    THRESHOLD_N3,
    LAYER_COUNT,
    L0,
    L1,
    L2,
    L3,
    L4,
    L5,
    L6,
    DEFAULT_FRICTIONS,
    LayerGeometry,
    ControlConfiguration,
    LayerMovement,
    L5Result,
    L5Metaconsciencia,
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
    level_description,
    yo_state,
    decode_downward_signal,
    describe_movement,
    formula_maestra_l5,
)


# ===============================================================
# DATOS BASE DEL TEST
# ===============================================================

CAPAS = (
    0.10,
    0.20,
    0.30,
    0.40,
    0.50,
    0.60,
    0.70,
)

FRICCIONES = tuple(DEFAULT_FRICTIONS)

THETA_Y = 0.50
THETA_EQ = 0.50

AGENCY = 0.80
AUTOREFERENCE = 0.80

SIGMA5 = 0.029707


def _resultado_base(**overrides) -> L5Result:
    parametros = dict(
        activations=CAPAS,
        theta_y=THETA_Y,
        theta_eq=THETA_EQ,
        agency=AGENCY,
        autoreference=AUTOREFERENCE,
        novelty=0.0,
        frictions=FRICCIONES,
        sigma5=SIGMA5,
        loop_detected=False,
    )
    parametros.update(overrides)
    return formula_maestra_l5(**parametros)


# ===============================================================
# DL5 — ESTRUCTURA BÁSICA
# ===============================================================

def test_dl5_formula_maestra_produce_resultado_l5():
    resultado = _resultado_base()

    assert isinstance(resultado, L5Result)


def test_dl5_carril_tiene_siete_posiciones():
    resultado = _resultado_base()

    assert len(resultado.activations_before) == LAYER_COUNT
    assert len(resultado.activations_after) == LAYER_COUNT


def test_dl5_indices_corresponden_al_carril_l0_l6():
    assert (L0, L1, L2, L3, L4, L5, L6) == tuple(range(LAYER_COUNT))


def test_dl5_activaciones_de_entrada_se_conservan():
    resultado = _resultado_base()

    assert resultado.activations_before == CAPAS


# ===============================================================
# DL5 — GEOMETRÍA
# ===============================================================

def test_dl5_geometria_tiene_siete_capas():
    geometry = build_geometry()

    assert len(geometry) == LAYER_COUNT


def test_dl5_geometria_contiene_layer_geometry():
    geometry = build_geometry()

    assert all(isinstance(item, LayerGeometry) for item in geometry)


def test_dl5_geometria_indices_son_l0_a_l6():
    geometry = build_geometry()

    assert tuple(item.index for item in geometry) == tuple(range(LAYER_COUNT))


def test_dl5_geometria_l5_existe():
    geometry = build_geometry()

    assert geometry[L5].index == L5


# ===============================================================
# DL5 — ENERGÍA Y PESOS
# ===============================================================

def test_dl5_energias_tienen_siete_posiciones():
    geometry = build_geometry()

    energies = calculate_energies(
        CAPAS,
        FRICCIONES,
        geometry,
    )

    assert len(energies) == LAYER_COUNT


def test_dl5_pesos_tienen_siete_posiciones():
    geometry = build_geometry()

    energies = calculate_energies(
        CAPAS,
        FRICCIONES,
        geometry,
    )

    weights = normalize_weights(energies)

    assert len(weights) == LAYER_COUNT


def test_dl5_pesos_normalizados_suman_uno():
    geometry = build_geometry()

    energies = calculate_energies(
        CAPAS,
        FRICCIONES,
        geometry,
    )

    weights = normalize_weights(energies)

    assert sum(weights) == pytest.approx(1.0)


def test_dl5_energias_son_no_negativas():
    geometry = build_geometry()

    energies = calculate_energies(
        CAPAS,
        FRICCIONES,
        geometry,
    )

    assert all(value >= 0.0 for value in energies)


def test_dl5_pesos_son_no_negativos():
    geometry = build_geometry()

    energies = calculate_energies(
        CAPAS,
        FRICCIONES,
        geometry,
    )

    weights = normalize_weights(energies)

    assert all(value >= 0.0 for value in weights)


def test_dl5_cero_energias_produce_peso_uniforme():
    energies = tuple(0.0 for _ in range(LAYER_COUNT))

    weights = normalize_weights(energies)

    assert len(weights) == LAYER_COUNT
    assert all(
        value == pytest.approx(1.0 / LAYER_COUNT)
        for value in weights
    )


# ===============================================================
# DL5 — COHERENCIA Y RECEPTOR
# ===============================================================

def test_dl5_coherencia_esta_en_rango():
    coherence = default_coherence(CAPAS)

    assert 0.0 <= coherence <= 1.0


def test_dl5_coherencia_de_capas_identicas_es_uno():
    capas = tuple(0.5 for _ in range(LAYER_COUNT))

    coherence = default_coherence(capas)

    assert coherence == pytest.approx(1.0)


def test_dl5_receptor_devuelve_coherencia_calidad_y_distorsion():
    coherence, quality, distortion = receptor_quality(
        CAPAS,
        FRICCIONES,
    )

    assert 0.0 <= coherence <= 1.0
    assert 0.0 <= quality <= 1.0
    assert 0.0 <= distortion <= 1.0


def test_dl5_receptor_quality_y_distorsion_son_complementarios():
    _, quality, distortion = receptor_quality(
        CAPAS,
        FRICCIONES,
    )

    assert distortion == pytest.approx(1.0 - quality)


# ===============================================================
# DL5 — OCUPACIÓN H5
# ===============================================================

def test_dl5_h5_esta_en_rango():
    geometry = build_geometry()
    z5 = geometry[L5].z

    h5 = house_occupancy(
        THETA_Y,
        z5,
        SIGMA5,
    )

    assert 0.0 <= h5 <= 1.0


def test_dl5_h5_en_su_centro_es_uno():
    h5 = house_occupancy(
        THETA_Y,
        THETA_Y,
        SIGMA5,
    )

    assert h5 == pytest.approx(1.0)


def test_dl5_h5_decrece_al_aumentar_distancia():
    centro = house_occupancy(
        THETA_Y,
        THETA_Y,
        SIGMA5,
    )

    distancia_pequena = house_occupancy(
        THETA_Y,
        THETA_Y + SIGMA5,
        SIGMA5,
    )

    distancia_grande = house_occupancy(
        THETA_Y,
        THETA_Y + 2.0 * SIGMA5,
        SIGMA5,
    )

    assert centro > distancia_pequena > distancia_grande


# ===============================================================
# DL5 — VISIBILIDAD
# ===============================================================

def test_dl5_visibilidad_de_capa_esta_en_rango():
    geometry = build_geometry()

    z5 = geometry[L5].z
    zi = geometry[L4].z

    visibility = layer_visibility(
        z5,
        zi,
        THETA_CUBE_F,
    )

    assert 0.0 <= visibility <= 1.0


def test_dl5_visibilidad_maxima_en_misma_posicion():
    visibility = layer_visibility(
        1.0,
        1.0,
        THETA_CUBE_F,
    )

    assert visibility == pytest.approx(1.0)


def test_dl5_visibilidad_disminuye_con_distancia():
    cercana = layer_visibility(
        1.0,
        1.1,
        THETA_CUBE_F,
    )

    lejana = layer_visibility(
        1.0,
        2.0,
        THETA_CUBE_F,
    )

    assert cercana > lejana


def test_dl5_visibilidad_efectiva_esta_en_rango():
    geometry = build_geometry()

    energies = calculate_energies(
        CAPAS,
        FRICCIONES,
        geometry,
    )

    weights = normalize_weights(energies)

    visibility = effective_visibility(
        weights,
        geometry,
        theta_cube=THETA_CUBE_F,
    )

    assert 0.0 <= visibility <= 1.0


# ===============================================================
# DL5 — I5
# ===============================================================

def test_dl5_i5_esta_limitado_por_alpha():
    resultado = _resultado_base()

    assert 0.0 <= resultado.i5 <= ALPHA_F


def test_dl5_i5_es_consistente_con_q5_h5_v5():
    resultado = _resultado_base()

    esperado = calculate_i5(
        q5=resultado.receptor_quality,
        h5=resultado.occupancy,
        v5=resultado.visibility,
    )

    assert resultado.i5 == pytest.approx(esperado)


def test_dl5_i5_no_supera_alpha():
    resultado = _resultado_base()

    assert resultado.i5 <= ALPHA_F


# ===============================================================
# DL5 — INTENSIDADES DE OBSERVACIÓN
# ===============================================================

def test_dl5_produce_tres_intensidades_de_observacion():
    resultado = _resultado_base()

    assert len(resultado.observation_intensities) == 3


def test_dl5_intensidades_corresponden_a_k_1_2_3():
    resultado = _resultado_base()

    esperadas = tuple(
        observation_intensity(resultado.i5, k)
        for k in range(1, 4)
    )

    assert resultado.observation_intensities == pytest.approx(esperadas)


# ===============================================================
# DL5 — EJE N
# ===============================================================

def test_dl5_n_siempre_pertenece_a_1_2_3():
    resultado = _resultado_base()

    assert resultado.observation_level in (1, 2, 3)


def test_dl5_autoreferencia_menor_que_beta_fija_n1():
    nivel = determine_observation_level(
        i5=ALPHA_F,
        autoreference=max(0.0, BETA_F - 1e-12),
    )

    assert nivel == 1


def test_dl5_n2_y_n3_son_umbralizados_desde_i5_normalizado():
    autoreference = BETA_F

    nivel_n2 = determine_observation_level(
        i5=ALPHA_F * THRESHOLD_N2,
        autoreference=autoreference,
    )

    nivel_n3 = determine_observation_level(
        i5=ALPHA_F * THRESHOLD_N3,
        autoreference=autoreference,
    )

    assert nivel_n2 in (2, 3)
    assert nivel_n3 == 3


# ===============================================================
# DL5 — CONFIGURACIÓN DE CONTROL
# ===============================================================

def test_dl5_control_es_configuration():
    resultado = _resultado_base()

    assert isinstance(resultado.control, ControlConfiguration)


def test_dl5_producto_control_es_agencia_por_autoreferencia():
    resultado = _resultado_base()

    assert resultado.control.product == pytest.approx(
        AGENCY * AUTOREFERENCE
    )


def test_dl5_producto_control_esta_en_rango():
    resultado = _resultado_base()

    assert 0.0 <= resultado.control.product <= 1.0


def test_dl5_configuracion_x1():
    cfg = control_configuration(
        1,
        agency=0.0,
        autoreference=0.0,
    )

    assert cfg.code == "1.1"
    assert cfg.product == pytest.approx(0.0)
    assert cfg.conscious == pytest.approx(0.0)


def test_dl5_configuracion_x2():
    cfg = control_configuration(
        1,
        agency=0.0,
        autoreference=1.0,
    )

    assert cfg.code == "1.2"
    assert cfg.product == pytest.approx(0.0)


def test_dl5_configuracion_x3():
    cfg = control_configuration(
        1,
        agency=1.0,
        autoreference=0.0,
    )

    assert cfg.code == "1.3"
    assert cfg.product == pytest.approx(0.0)


def test_dl5_configuracion_x4():
    cfg = control_configuration(
        1,
        agency=1.0,
        autoreference=1.0,
    )

    assert cfg.code == "1.4"
    assert cfg.product == pytest.approx(1.0)
    assert cfg.conscious == pytest.approx(1.0)


# ===============================================================
# DL5 — CASA DEL YO
# ===============================================================

def test_dl5_casa_del_yo_permanece_en_l4():
    resultado = _resultado_base()

    assert resultado.geometry[L4].index == L4
    assert L4 == 4


def test_dl5_yo_state_no_mueve_la_casa_del_yo():
    for nivel in (1, 2, 3):
        estado = yo_state(
            nivel,
            agency=AGENCY,
            autoreference=AUTOREFERENCE,
        )

        assert isinstance(estado, str)


# ===============================================================
# DL5 — RETORNO HACIA ABAJO
# ===============================================================

def test_dl5_sin_agencia_no_hay_retorno():
    resultado = _resultado_base(
        agency=0.0,
        autoreference=AUTOREFERENCE,
    )

    assert resultado.activations_after == resultado.activations_before
    assert resultado.movements == ()


def test_dl5_sin_autoreferencia_no_hay_retorno():
    resultado = _resultado_base(
        agency=AGENCY,
        autoreference=0.0,
    )

    assert resultado.activations_after == resultado.activations_before
    assert resultado.movements == ()


def test_dl5_sin_producto_no_hay_retorno():
    before = CAPAS

    after = decode_downward_signal(
        before,
        observation_level=2,
        agency=0.0,
        autoreference=1.0,
    )

    assert after == before


def test_dl5_retorno_atenúa_l1_l2_l3():
    before = CAPAS

    after = decode_downward_signal(
        before,
        observation_level=2,
        agency=AGENCY,
        autoreference=AUTOREFERENCE,
    )

    assert after[L1] < before[L1]
    assert after[L2] < before[L2]
    assert after[L3] < before[L3]


def test_dl5_retorno_refuerza_l4():
    before = CAPAS

    after = decode_downward_signal(
        before,
        observation_level=2,
        agency=AGENCY,
        autoreference=AUTOREFERENCE,
    )

    assert after[L4] > before[L4]


def test_dl5_retorno_no_altera_l0_l5_l6():
    before = CAPAS

    after = decode_downward_signal(
        before,
        observation_level=2,
        agency=AGENCY,
        autoreference=AUTOREFERENCE,
    )

    assert after[L0] == before[L0]
    assert after[L5] == before[L5]
    assert after[L6] == before[L6]


def test_dl5_movements_describen_las_variaciones_reales():
    resultado = _resultado_base()

    movimientos = describe_movement(
        resultado.activations_before,
        resultado.activations_after,
    )

    assert movimientos == resultado.movements

    for movement in movimientos:
        assert isinstance(movement, LayerMovement)
        assert movement.source_layer == L5
        assert movement.amount >= 0.0


# ===============================================================
# DL5 — NOVELTY
# ===============================================================
#
# Esta es la prueba correspondiente al fallo:
#
#     test_r1_novelty_no_modifica_N_ni_I5
#
# novelty es una entrada reservada.
# El contrato actual indica explícitamente:
#
#     novelty → reservada; no mueve N
#
# Por tanto no se fija un I5 ni un N concreto.
# Se ejecuta la misma fórmula dos veces cambiando ÚNICAMENTE novelty.
# ===============================================================

def test_r1_novelty_no_modifica_N_ni_I5():
    resultado_sin_novedad = _resultado_base(
        novelty=0.0,
    )

    resultado_con_novedad = _resultado_base(
        novelty=1.0,
    )

    assert (
        resultado_sin_novedad.i5
        == pytest.approx(resultado_con_novedad.i5)
    )

    assert (
        resultado_sin_novedad.observation_level
        == resultado_con_novedad.observation_level
    )


def test_r1_novelty_no_modifica_receptor():
    resultado_sin_novedad = _resultado_base(
        novelty=0.0,
    )

    resultado_con_novedad = _resultado_base(
        novelty=1.0,
    )

    assert (
        resultado_sin_novedad.coherence
        == pytest.approx(resultado_con_novedad.coherence)
    )

    assert (
        resultado_sin_novedad.receptor_quality
        == pytest.approx(resultado_con_novedad.receptor_quality)
    )

    assert (
        resultado_sin_novedad.distortion
        == pytest.approx(resultado_con_novedad.distortion)
    )


def test_r1_novelty_no_modifica_h5_ni_v5():
    resultado_sin_novedad = _resultado_base(
        novelty=0.0,
    )

    resultado_con_novedad = _resultado_base(
        novelty=1.0,
    )

    assert (
        resultado_sin_novedad.occupancy
        == pytest.approx(resultado_con_novedad.occupancy)
    )

    assert (
        resultado_sin_novedad.visibility
        == pytest.approx(resultado_con_novedad.visibility)
    )


def test_r1_novelty_no_modifica_intensidades_de_observacion():
    resultado_sin_novedad = _resultado_base(
        novelty=0.0,
    )

    resultado_con_novedad = _resultado_base(
        novelty=1.0,
    )

    assert (
        resultado_sin_novedad.observation_intensities
        == pytest.approx(
            resultado_con_novedad.observation_intensities
        )
    )


def test_r1_novelty_no_modifica_control():
    resultado_sin_novedad = _resultado_base(
        novelty=0.0,
    )

    resultado_con_novedad = _resultado_base(
        novelty=1.0,
    )

    assert resultado_sin_novedad.control == resultado_con_novedad.control


def test_r1_novelty_no_modifica_retorno():
    resultado_sin_novedad = _resultado_base(
        novelty=0.0,
    )

    resultado_con_novedad = _resultado_base(
        novelty=1.0,
    )

    assert (
        resultado_sin_novedad.activations_after
        == pytest.approx(resultado_con_novedad.activations_after)
    )


# ===============================================================
# DL5 — NOVELTY CONTINUA
# ===============================================================
#
# No se asume que novelty sea booleano.
# Se comprueba que diferentes valores reservados no introducen
# causalidad en la salida actual.
# ===============================================================

def test_r1_novelty_es_invariante_para_varios_valores():
    resultados = [
        _resultado_base(novelty=value)
        for value in (
            0.0,
            0.25,
            0.5,
            0.75,
            1.0,
        )
    ]

    referencia = resultados[0]

    for resultado in resultados[1:]:
        assert resultado.i5 == pytest.approx(referencia.i5)
        assert (
            resultado.observation_level
            == referencia.observation_level
        )


# ===============================================================
# DL5 — LOOP DETECTED
# ===============================================================

def test_dl5_loop_detected_es_lectura_y_no_modifica_i5():
    sin_loop = _resultado_base(
        loop_detected=False,
    )

    con_loop = _resultado_base(
        loop_detected=True,
    )

    assert con_loop.i5 == pytest.approx(sin_loop.i5)


def test_dl5_loop_detected_es_conservado_en_resultado():
    sin_loop = _resultado_base(
        loop_detected=False,
    )

    con_loop = _resultado_base(
        loop_detected=True,
    )

    assert sin_loop.loop_detected is False
    assert con_loop.loop_detected is True


def test_dl5_loop_detected_no_modifica_n():
    sin_loop = _resultado_base(
        loop_detected=False,
    )

    con_loop = _resultado_base(
        loop_detected=True,
    )

    assert (
        sin_loop.observation_level
        == con_loop.observation_level
    )


# ===============================================================
# DL5 — DETERMINISMO
# ===============================================================

def test_dl5_misma_entrada_produce_mismo_resultado():
    primero = _resultado_base()
    segundo = _resultado_base()

    assert primero == segundo


def test_dl5_misma_entrada_produce_mismo_i5():
    primero = _resultado_base()
    segundo = _resultado_base()

    assert primero.i5 == pytest.approx(segundo.i5)


def test_dl5_misma_entrada_produce_mismo_n():
    primero = _resultado_base()
    segundo = _resultado_base()

    assert primero.observation_level == segundo.observation_level


# ===============================================================
# DL5 — RESULTADO COMPLETO
# ===============================================================

def test_dl5_resultado_expone_la_cadena_completa():
    resultado = _resultado_base()

    assert len(resultado.activations_before) == LAYER_COUNT
    assert len(resultado.activations_after) == LAYER_COUNT
    assert len(resultado.energies) == LAYER_COUNT
    assert len(resultado.weights) == LAYER_COUNT
    assert len(resultado.geometry) == LAYER_COUNT

    assert 0.0 <= resultado.coherence <= 1.0
    assert 0.0 <= resultado.receptor_quality <= 1.0
    assert 0.0 <= resultado.distortion <= 1.0
    assert 0.0 <= resultado.occupancy <= 1.0
    assert 0.0 <= resultado.visibility <= 1.0
    assert 0.0 <= resultado.i5 <= ALPHA_F

    assert resultado.observation_level in (1, 2, 3)
    assert isinstance(resultado.level_description, str)
    assert isinstance(resultado.control, ControlConfiguration)
    assert isinstance(resultado.yo_state, str)
    assert isinstance(resultado.movements, tuple)
    assert isinstance(resultado.loop_detected, bool)


# ===============================================================
# DL5 — NO SE MUEVE LA CASA DEL YO
# ===============================================================

def test_dl5_theta_y_no_reubica_la_casa_del_yo():
    resultado = _resultado_base(
        theta_y=THETA_Y,
    )

    assert resultado.geometry[L4].index == L4
    assert resultado.theta_y == pytest.approx(THETA_Y)
    assert resultado.theta_eq == pytest.approx(THETA_EQ)


# ===============================================================
# DL5 — CONSISTENCIA DE LA FORMULA MAESTRA
# ===============================================================

def test_dl5_formula_maestra_y_motor_producen_mismo_i5():
    resultado_maestro = _resultado_base()

    motor = L5Metaconsciencia(
        theta_eq=THETA_EQ,
        theta_cube=THETA_CUBE_F,
        frictions=FRICCIONES,
        sigma5=SIGMA5,
    )

    resultado_motor = motor.calcular(
        activations=CAPAS,
        theta_y=THETA_Y,
        agency=AGENCY,
        autoreference=AUTOREFERENCE,
        novelty=0.0,
        loop_detected=False,
    )

    assert resultado_maestro.i5 == pytest.approx(
        resultado_motor.i5
    )


def test_dl5_formula_maestra_y_motor_producen_mismo_n():
    resultado_maestro = _resultado_base()

    motor = L5Metaconsciencia(
        theta_eq=THETA_EQ,
        theta_cube=THETA_CUBE_F,
        frictions=FRICCIONES,
        sigma5=SIGMA5,
    )

    resultado_motor = motor.calcular(
        activations=CAPAS,
        theta_y=THETA_Y,
        agency=AGENCY,
        autoreference=AUTOREFERENCE,
        novelty=0.0,
        loop_detected=False,
    )

    assert (
        resultado_maestro.observation_level
        == resultado_motor.observation_level
    )


# ===============================================================
# FIN DL5
# ===============================================================
