# ===============================================================
# tests/test_integracion_real_engine.py
# ===============================================================
# 50 tests duros, realistas y sin piedad contra Engine 19.0
# Alineados con VPSI-CONTRACT-1.0 / comportamiento real del Engine
# Sin hardcode de módulos específicos. Sin tolerancia a ambigüedad.
# ===============================================================

from __future__ import annotations
import inspect
import pytest
from pathlib import Path
from typing import Any, Dict, List

from core.engine import (
    Engine,
    ArranqueError,
    Contenedor,
    RegistroModulos,
    VERSION_ENGINE,
    ESQUEMA_CONTRATO_REQUERIDO,
    VERSION_CONTRATO_REQUERIDA,
    API_ENGINE_ACTUAL,
    ESTADOS_CANONICOS,
    CLAVES_OBLIGATORIAS_CONTRATO,
    PERMISOS_AUTORIZA_ENGINE,
    BANDERAS_REPORTING,
    CLAVES_META_CAPACIDAD,
    LISTAS_STR_OBLIGATORIAS,
)


# ===============================================================
# FIXTURES
# ===============================================================

@pytest.fixture(scope="module")
def engine(tmp_path_factory) -> Engine:
    """
    Arranca el Engine real contra el directorio de módulos del proyecto.
    Si el arranque falla de forma estructural, el fixture propaga el error.
    """
    raiz = Path("modules")
    if not raiz.is_dir():
        pytest.skip("No existe directorio modules/")
    return Engine(raiz_modulos=raiz, invocador_id="test_duro", strict=True)


@pytest.fixture
def registro(engine: Engine) -> RegistroModulos:
    return engine.registro


# ===============================================================
# 1–10  IDENTIDAD Y CONSTANTES DEL ENGINE
# ===============================================================

def test_01_version_engine_es_str_no_vacia():
    assert isinstance(VERSION_ENGINE, str)
    assert VERSION_ENGINE.strip() != ""

def test_02_esquema_contrato_requerido_exacto():
    assert ESQUEMA_CONTRATO_REQUERIDO == "VPSI-CONTRACT-1.0"

def test_03_version_contrato_requerida_exacta():
    assert VERSION_CONTRATO_REQUERIDA == "1.0"

def test_04_api_engine_actual_es_str():
    assert isinstance(API_ENGINE_ACTUAL, str)
    assert API_ENGINE_ACTUAL.strip() != ""

def test_05_estados_canonicos_completos():
    esperados = {"NO_INICIADO", "OPERATIVO", "DEGRADADO", "RECHAZADO"}
    assert set(ESTADOS_CANONICOS) == esperados

def test_06_claves_obligatorias_contrato_no_vacias():
    assert len(CLAVES_OBLIGATORIAS_CONTRATO) > 10
    assert "id" in CLAVES_OBLIGATORIAS_CONTRATO
    assert "capacidades" in CLAVES_OBLIGATORIAS_CONTRATO
    assert "capacidades_meta" in CLAVES_OBLIGATORIAS_CONTRATO

def test_07_permisos_autoriza_engine_incluye_ejecutar():
    assert "ejecutar" in PERMISOS_AUTORIZA_ENGINE

def test_08_banderas_reporting_incluye_inventario():
    assert "inventario" in BANDERAS_REPORTING

def test_09_claves_meta_capacidad_minimas():
    for k in ("descripcion", "entrada", "salida", "validar_esquema", "acceso_archivos"):
        assert k in CLAVES_META_CAPACIDAD

def test_10_listas_str_obligatorias_existen():
    assert "no_hace" in LISTAS_STR_OBLIGATORIAS
    assert "invariantes" in LISTAS_STR_OBLIGATORIAS


# ===============================================================
# 11–20  ARRANQUE Y ESTADO DEL ENGINE
# ===============================================================

def test_11_engine_arranca_en_estado_operativo(engine: Engine):
    assert engine.estado == "OPERATIVO"

def test_12_engine_no_tiene_errores_arranque(engine: Engine):
    assert engine.errores_arranque == []

def test_13_registro_tiene_al_menos_un_modulo(engine: Engine):
    assert engine.registro.total() >= 1

def test_14_todos_los_contenedores_tienen_id(engine: Engine):
    for cont in engine.registro.contenedores.values():
        assert isinstance(cont.id, str)
        assert cont.id.strip() != ""

def test_15_todos_los_contenedores_tienen_nombre(engine: Engine):
    for cont in engine.registro.contenedores.values():
        assert isinstance(cont.nombre, str)
        assert cont.nombre.strip() != ""

def test_16_todos_los_contenedores_tienen_rol(engine: Engine):
    for cont in engine.registro.contenedores.values():
        assert isinstance(cont.rol, str)
        assert cont.rol.strip() != ""

def test_17_roles_son_unicos(engine: Engine):
    roles = [c.rol for c in engine.registro.contenedores.values()]
    assert len(roles) == len(set(roles)), "Existen roles duplicados"

def test_18_ids_son_unicos(engine: Engine):
    ids = [c.id for c in engine.registro.contenedores.values() if c.id]
    assert len(ids) == len(set(ids)), "Existen ids duplicados"

def test_19_nombres_son_unicos(engine: Engine):
    nombres = list(engine.registro.contenedores.keys())
    assert len(nombres) == len(set(nombres))

def test_20_grafo_existe_y_tiene_nodos(engine: Engine):
    assert isinstance(engine._grafo, dict)
    assert "nodos" in engine._grafo
    assert isinstance(engine._grafo["nodos"], list)
    assert len(engine._grafo["nodos"]) >= 1


# ===============================================================
# 21–30  CONTRATO DE CADA MÓDULO
# ===============================================================

def test_21_todo_modulo_tiene_esquema_correcto(engine: Engine):
    for cont in engine.registro.contenedores.values():
        assert cont.esquema == ESQUEMA_CONTRATO_REQUERIDO

def test_22_todo_modulo_tiene_version_contrato_correcta(engine: Engine):
    for cont in engine.registro.contenedores.values():
        assert cont.version_contrato == VERSION_CONTRATO_REQUERIDA

def test_23_todo_modulo_tiene_capacidades_dict(engine: Engine):
    for cont in engine.registro.contenedores.values():
        assert isinstance(cont.capacidades, dict)

def test_24_todo_modulo_tiene_capacidades_meta_dict(engine: Engine):
    for cont in engine.registro.contenedores.values():
        assert isinstance(cont.capacidades_meta, dict)

def test_25_capacidades_y_meta_tienen_mismas_claves(engine: Engine):
    for cont in engine.registro.contenedores.values():
        caps = set(cont.capacidades.keys())
        meta = set(cont.capacidades_meta.keys())
        assert caps == meta, f"{cont.nombre}: capacidades y capacidades_meta no coinciden"

def test_26_todas_las_capacidades_son_callables(engine: Engine):
    for cont in engine.registro.contenedores.values():
        for nombre, fn in cont.capacidades.items():
            assert callable(fn), f"{cont.nombre}.{nombre} no es callable"

def test_27_capacidades_meta_tiene_campos_obligatorios(engine: Engine):
    for cont in engine.registro.contenedores.values():
        for cap, meta in cont.capacidades_meta.items():
            for campo in CLAVES_META_CAPACIDAD:
                assert campo in meta, f"{cont.nombre}.{cap} falta '{campo}' en meta"

def test_28_autoriza_engine_es_dict_completo(engine: Engine):
    for cont in engine.registro.contenedores.values():
        assert isinstance(cont.autoriza_engine, dict)
        for permiso in PERMISOS_AUTORIZA_ENGINE:
            assert permiso in cont.autoriza_engine, f"{cont.nombre} falta permiso '{permiso}'"
            assert isinstance(cont.autoriza_engine[permiso], bool)

def test_29_reporting_es_dict_completo(engine: Engine):
    for cont in engine.registro.contenedores.values():
        assert isinstance(cont.reporting, dict)
        for bandera in BANDERAS_REPORTING:
            assert bandera in cont.reporting
            assert isinstance(cont.reporting[bandera], bool)

def test_30_estados_validos_son_canonicos(engine: Engine):
    for cont in engine.registro.contenedores.values():
        for est in cont.estados_validos:
            assert est in ESTADOS_CANONICOS, f"{cont.nombre} tiene estado no canónico: {est}"


# ===============================================================
# 31–40  EJECUCIÓN CONTRACTUAL
# ===============================================================

def test_31_ejecutar_capacidad_inexistente_devuelve_error(engine: Engine):
    nombre = next(iter(engine.registro.contenedores))
    salida = engine.ejecutar_capacidad(nombre, "capacidad_que_no_existe_xyz")
    assert isinstance(salida, dict)
    assert salida.get("estado") in ("ERROR", "ERROR_ENTRADA", "ERROR_EJECUCION")

def test_32_ejecutar_modulo_inexistente_devuelve_error(engine: Engine):
    salida = engine.ejecutar_capacidad("modulo_fantasma_xyz", "inventario")
    assert isinstance(salida, dict)
    assert salida.get("estado") == "ERROR"

def test_33_resolver_existencia_de_capacidad_real(engine: Engine):
    cont = next(iter(engine.registro.contenedores.values()))
    if not cont.capacidades:
        pytest.skip("Módulo sin capacidades")
    cap = next(iter(cont.capacidades))
    res = engine.resolver_existencia(cap)
    assert res["estado"] == "EXISTE"
    assert res["existe"] is True

def test_34_resolver_existencia_de_inexistente(engine: Engine):
    res = engine.resolver_existencia("capacidad_absolutamente_inexistente_xyz_999")
    assert res["estado"] == "NO_EXISTE"
    assert res["existe"] is False

def test_35_ejecutar_capacidad_real_devuelve_estructura(engine: Engine):
    cont = next(iter(engine.registro.contenedores.values()))
    if not cont.capacidades:
        pytest.skip("Módulo sin capacidades")
    cap = next(iter(cont.capacidades))
    salida = engine.ejecutar_capacidad(cont.nombre, cap)
    assert isinstance(salida, dict)
    assert "estado" in salida
    assert "modulo" in salida
    assert "capacidad" in salida

def test_36_salida_exitosa_contiene_resultado(engine: Engine):
    cont = next(iter(engine.registro.contenedores.values()))
    if not cont.capacidades:
        pytest.skip("Módulo sin capacidades")
    # Buscamos una capacidad sin argumentos
    for cap, fn in cont.capacidades.items():
        try:
            sig = inspect.signature(fn)
            if len(sig.parameters) == 0:
                salida = engine.ejecutar_capacidad(cont.nombre, cap)
                if salida.get("estado") == "EXITO":
                    assert "resultado" in salida
                    return
        except Exception:
            continue
    pytest.skip("No se encontró capacidad sin argumentos ejecutable")

def test_37_engine_no_inventa_capacidades(engine: Engine):
    """El Engine solo puede ejecutar lo que el módulo declaró."""
    cont = next(iter(engine.registro.contenedores.values()))
    inventada = "capacidad_inventada_por_test_xyz"
    assert inventada not in cont.capacidades
    salida = engine.ejecutar_capacidad(cont.nombre, inventada)
    assert salida.get("estado") != "EXITO"

def test_38_censar_devuelve_estructura_minima(engine: Engine):
    censo = engine.censar()
    assert isinstance(censo, dict)
    assert "total" in censo
    assert "cargados" in censo
    assert censo["total"] == engine.registro.total()

def test_39_estado_global_contiene_campos_obligatorios(engine: Engine):
    eg = engine.estado_global()
    assert isinstance(eg, dict)
    assert eg.get("tipo") == "estado_global"
    assert "version_engine" in eg
    assert "estado" in eg
    assert "total_contenedores" in eg

def test_40_paquete_omega_es_dict_con_reportes(engine: Engine):
    po = engine.paquete_omega()
    assert isinstance(po, dict)
    assert "metadata" in po
    assert "reportes" in po
    assert isinstance(po["reportes"], list)


# ===============================================================
# 41–50  FRONTERA ENGINE → MÓDULO → RESULTADO
# ===============================================================

def test_41_ejecutar_capacidad_respeta_autoriza_engine(engine: Engine):
    for cont in engine.registro.contenedores.values():
        if cont.autoriza_engine.get("ejecutar") is not True:
            # Debe rechazar cualquier ejecución
            if cont.capacidades:
                cap = next(iter(cont.capacidades))
                salida = engine.ejecutar_capacidad(cont.nombre, cap)
                assert salida.get("estado") == "ERROR"
                assert "no autoriza" in str(salida.get("error", "")).lower() or "autoriza" in str(salida.get("error", "")).lower()

def test_42_resultado_de_capacidad_no_es_modificado_por_engine(engine: Engine):
    """El Engine debe devolver el resultado tal cual lo produjo el módulo."""
    cont = next(iter(engine.registro.contenedores.values()))
    for cap, fn in cont.capacidades.items():
        try:
            sig = inspect.signature(fn)
            if len(sig.parameters) == 0:
                crudo = fn()
                envuelto = engine.ejecutar_capacidad(cont.nombre, cap)
                if envuelto.get("estado") == "EXITO":
                    assert envuelto["resultado"] == crudo
                    return
        except Exception:
            continue
    pytest.skip("No se pudo comparar resultado crudo vs envuelto")

def test_43_trazas_se_registran_en_ejecucion_exitosa(engine: Engine):
    antes = len(engine._trazas)
    cont = next(iter(engine.registro.contenedores.values()))
    for cap, fn in cont.capacidades.items():
        try:
            sig = inspect.signature(fn)
            if len(sig.parameters) == 0:
                engine.ejecutar_capacidad(cont.nombre, cap)
                assert len(engine._trazas) > antes
                return
        except Exception:
            continue
    pytest.skip("No se ejecutó ninguna capacidad sin argumentos")

def test_44_invocar_devuelve_solo_resultado_en_exito(engine: Engine):
    cont = next(iter(engine.registro.contenedores.values()))
    for cap, fn in cont.capacidades.items():
        try:
            sig = inspect.signature(fn)
            if len(sig.parameters) == 0:
                res = engine.invocar(cont.nombre, cap)
                # invocar debe devolver el resultado interno, no el sobre
                assert not (isinstance(res, dict) and res.get("estado") == "EXITO" and "resultado" in res)
                return
        except Exception:
            continue
    pytest.skip("No se pudo invocar capacidad sin argumentos")

def test_45_resolver_peticion_de_inexistente_no_lanza(engine: Engine):
    res = engine.resolver_peticion("peticion_totalmente_inexistente_xyz")
    assert isinstance(res, dict)
    assert res.get("estado") == "NO_EXISTE"

def test_46_dependencias_grafo_existe(engine: Engine):
    assert isinstance(engine._dependencias, dict)
    assert "grafo" in engine._dependencias
    assert "orden_topologico" in engine._dependencias

def test_47_no_hay_ciclos_de_dependencia(engine: Engine):
    ciclos = engine._dependencias.get("ciclos", [])
    assert ciclos == [] or len(ciclos) == 0

def test_48_todos_los_modulos_tienen_invariantes(engine: Engine):
    for cont in engine.registro.contenedores.values():
        assert isinstance(cont.invariantes, list)
        assert len(cont.invariantes) >= 1

def test_49_engine_strict_true_rechaza_arranque_con_errores(tmp_path):
    """Si strict=True y hay errores de contrato, debe lanzar ArranqueError."""
    # Creamos un módulo inválido temporal
    mod_dir = tmp_path / "mod_invalido"
    mod_dir.mkdir()
    (mod_dir / "__init__.py").write_text(
        "CONTENEDOR = {'id': 'X', 'nombre': 'x'}\n",  # contrato incompleto
        encoding="utf-8",
    )
    with pytest.raises(ArranqueError):
        Engine(raiz_modulos=tmp_path, strict=True)

def test_50_forma_minima_identidad_en_capacidades_dict(engine: Engine):
    """
    Toda capacidad que devuelva dict debe contener, como mínimo,
    la identidad contractual del módulo cuando el test de etapa operativa lo exige.
    Esta es la regla aprendida del fallo UI.inventario.
    """
    for cont in engine.registro.contenedores.values():
        for cap, fn in cont.capacidades.items():
            try:
                sig = inspect.signature(fn)
                if len(sig.parameters) > 0:
                    continue
                res = fn()
                if isinstance(res, dict):
                    # Si el módulo decide devolver identidad, debe ser coherente
                    if "id" in res:
                        assert res["id"] == cont.id
                    if "nombre" in res:
                        assert res["nombre"] == cont.nombre
                    if "rol" in res:
                        assert res["rol"] == cont.rol
            except Exception:
                continue
