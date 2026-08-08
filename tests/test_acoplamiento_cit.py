# ===============================================================
# VPSI-TRUTH — TEST DE ACOPLAMIENTO CIT ↔ ENGINE
# ===============================================================
#
# Objetivo:
#   Verificar que modules/citacion/__init__.py está acoplado
#   correctamente al core/engine.py REAL.
#
# Este test NO modifica Engine.
# Este test NO elimina "requiere".
# Este test NO completa artificialmente el contrato.
#
# Se prueba:
#   1. Importación real de core.engine.
#   2. Descubrimiento real del módulo CIT.
#   3. Validación completa del CONTENEDOR por Engine.
#   4. Registro de CIT.
#   5. Identidad contractual.
#   6. Dependencias declaradas.
#   7. Capacidades declaradas.
#   8. capacidades_meta.
#   9. permisos autoriza_engine.
#  10. reporting.
#  11. ejecución de capacidades compatibles con llamada directa.
#  12. reporte / diagnóstico / inventario.
#  13. resolución del módulo por ID, nombre y rol.
#
# ===============================================================

from __future__ import annotations

import shutil
import sys
from pathlib import Path


# ===============================================================
# 1. RAÍZ REAL DEL PROYECTO
# ===============================================================

ROOT = Path(__file__).resolve().parents[1]

# El test NO depende del cwd desde donde pytest sea ejecutado.
# Esto evita:
#
#   ModuleNotFoundError: No module named 'core'
#
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


# ===============================================================
# 2. IMPORTACIÓN DEL ENGINE REAL
# ===============================================================

from core.engine import (
    API_ENGINE_ACTUAL,
    ESQUEMA_CONTRATO_REQUERIDO,
    VERSION_CONTRATO_REQUERIDA,
    VERSION_ENGINE,
    Engine,
)


# ===============================================================
# 3. LOCALIZACIÓN DE CIT
# ===============================================================

MODULES_ROOT = ROOT / "modules"
CIT_ROOT = MODULES_ROOT / "citacion"


# ===============================================================
# 4. HELPERS
# ===============================================================

def _crear_entorno_cit_aislado(tmp_path: Path) -> Path:
    """
    Crea un árbol temporal:

        tmp/
          modules/
            __init__.py
            citacion/
              __init__.py
              fuentes/
              esquema/
              ...

    Así Engine descubre únicamente CIT.

    No se modifica el proyecto original.
    """
    if not CIT_ROOT.is_dir():
        raise AssertionError(
            f"No existe el módulo CIT esperado: {CIT_ROOT}"
        )

    destino_modules = tmp_path / "modules"
    destino_modules.mkdir(parents=True, exist_ok=True)

    init_modules = destino_modules / "__init__.py"
    init_modules.write_text(
        "# paquete temporal de prueba VPSI\n",
        encoding="utf-8",
    )

    destino_cit = destino_modules / "citacion"

    shutil.copytree(
        CIT_ROOT,
        destino_cit,
    )

    return destino_modules


def _engine_cit(tmp_path: Path) -> Engine:
    """
    Construye el Engine REAL contra un entorno donde únicamente
    existe CIT.
    """
    raiz = _crear_entorno_cit_aislado(tmp_path)

    # El paquete temporal debe ser importable porque CIT puede
    # resolver internamente:
    #
    #   modules.citacion.fuentes
    #
    tmp_root = raiz.parent

    if str(tmp_root) not in sys.path:
        sys.path.insert(0, str(tmp_root))

    return Engine(
        raiz_modulos=raiz,
        invocador_id="test_acoplamiento_cit",
        strict=True,
    )


# ===============================================================
# 5. TEST — ENGINE IMPORTABLE
# ===============================================================

def test_cit_importa_engine_real():
    assert Engine is not None
    assert VERSION_ENGINE == "18.3"
    assert ESQUEMA_CONTRATO_REQUERIDO == "VPSI-CONTRACT-1.0"
    assert VERSION_CONTRATO_REQUERIDA == "1.0"
    assert API_ENGINE_ACTUAL == "1.0"


# ===============================================================
# 6. TEST — ENGINE DESCUBRE CIT
# ===============================================================

def test_engine_descubre_cit(tmp_path):
    engine = _engine_cit(tmp_path)

    assert engine.estado == "OPERATIVO"
    assert engine.registro.total() == 1

    assert "citacion" in engine.registro.contenedores

    cit = engine.registro.primero("citacion")

    assert cit is not None
    assert cit.id == "CIT"
    assert cit.nombre == "citacion"
    assert cit.rol == "CIT"


# ===============================================================
# 7. TEST — IDENTIDAD CONTRACTUAL
# ===============================================================

def test_cit_identidad_contractual(tmp_path):
    engine = _engine_cit(tmp_path)

    cit = engine.registro.primero("CIT")

    assert cit is not None

    assert cit.id == "CIT"
    assert cit.nombre == "citacion"
    assert cit.rol == "CIT"

    assert cit.version == "2.0"
    assert cit.version_contrato == "1.0"

    assert cit.esquema == "VPSI-CONTRACT-1.0"
    assert cit.estabilidad == "ESTABLE"
    assert cit.compatible_desde == "1.0"
    assert cit.api_engine == ">=1.0"


# ===============================================================
# 8. TEST — CIT NO TIENE REQUERIMIENTOS OCULTOS
# ===============================================================

def test_cit_requiere_es_exactamente_el_contrato(tmp_path):
    engine = _engine_cit(tmp_path)

    cit = engine.registro.primero("CIT")

    assert cit is not None

    # Según el contrato proporcionado:
    #
    #     "requiere": []
    #
    assert cit.requiere == []

    # Engine debe haber construido el grafo sin dependencias.
    deps = engine.estado_global()["dependencias"]

    assert deps["faltantes"] == {}
    assert deps["ciclos"] == []


# ===============================================================
# 9. TEST — VALIDACIÓN COMPLETA DEL CONTRATO
# ===============================================================

def test_cit_pasa_validacion_completa_del_engine(tmp_path):
    engine = _engine_cit(tmp_path)

    assert engine.errores_arranque == []
    assert engine.estado == "OPERATIVO"

    cit = engine.registro.primero("CIT")
    assert cit is not None

    errores = engine._validar_esquema(
        cit.meta,
        cit.nombre,
    )

    assert errores == []


# ===============================================================
# 10. TEST — CAPACIDADES DECLARADAS SON CALLABLES
# ===============================================================

def test_todas_las_capacidades_cit_son_callables(tmp_path):
    engine = _engine_cit(tmp_path)

    cit = engine.registro.primero("CIT")

    assert cit is not None
    assert cit.capacidades

    for nombre, capacidad in cit.capacidades.items():
        assert callable(capacidad), (
            f"CIT declara '{nombre}' pero no es callable"
        )


# ===============================================================
# 11. TEST — TODA CAPACIDAD TIENE META
# ===============================================================

def test_todas_las_capacidades_cit_tienen_meta(tmp_path):
    engine = _engine_cit(tmp_path)

    cit = engine.registro.primero("CIT")

    assert cit is not None

    for nombre in cit.capacidades:
        assert nombre in cit.capacidades_meta, (
            f"CIT.capacidades['{nombre}'] "
            f"no tiene entrada en capacidades_meta"
        )

        meta = cit.capacidades_meta[nombre]

        assert isinstance(meta, dict)

        assert "descripcion" in meta
        assert "entrada" in meta
        assert "salida" in meta

        assert isinstance(meta["descripcion"], str)
        assert isinstance(meta["entrada"], str)
        assert isinstance(meta["salida"], str)


# ===============================================================
# 12. TEST — PERMISOS COMPLETOS DEL ENGINE
# ===============================================================

def test_cit_autoriza_engine_completo(tmp_path):
    engine = _engine_cit(tmp_path)

    cit = engine.registro.primero("CIT")

    assert cit is not None

    permisos_esperados = {
        "leer",
        "ejecutar",
        "consultar",
        "recombinar",
        "reportar",
        "auditar",
        "inventariar",
        "modificar",
        "alterar",
        "reescribir",
    }

    assert set(cit.autoriza_engine.keys()) == permisos_esperados

    # Según el contrato de CIT:
    #
    # leer=True
    # ejecutar=True
    # consultar=True
    # recombinar=True
    # reportar=True
    # auditar=True
    # inventariar=True
    # modificar=False
    # alterar=False
    # reescribir=False

    assert cit.autoriza_engine["leer"] is True
    assert cit.autoriza_engine["ejecutar"] is True
    assert cit.autoriza_engine["consultar"] is True
    assert cit.autoriza_engine["recombinar"] is True
    assert cit.autoriza_engine["reportar"] is True
    assert cit.autoriza_engine["auditar"] is True
    assert cit.autoriza_engine["inventariar"] is True

    assert cit.autoriza_engine["modificar"] is False
    assert cit.autoriza_engine["alterar"] is False
    assert cit.autoriza_engine["reescribir"] is False


# ===============================================================
# 13. TEST — REPORTING CONTRACTUAL
# ===============================================================

def test_cit_reporting_completo(tmp_path):
    engine = _engine_cit(tmp_path)

    cit = engine.registro.primero("CIT")

    assert cit is not None

    banderas = {
        "estado",
        "salud",
        "inventario",
        "capacidades",
        "errores",
        "advertencias",
        "dependencias",
        "version",
        "contrato",
        "conocimiento",
        "metricas",
        "diagnostico",
    }

    assert set(cit.reporting.keys()) == banderas

    for bandera in banderas:
        assert isinstance(
            cit.reporting[bandera],
            bool,
        )


# ===============================================================
# 14. TEST — INVENTARIO
# ===============================================================

def test_cit_inventario_por_engine(tmp_path):
    engine = _engine_cit(tmp_path)

    salida = engine.ejecutar_inventario("CIT")

    assert salida["estado"] == "EXITO"

    inventario = salida["resultado"]

    assert inventario["id"] == "CIT"
    assert inventario["nombre"] == "citacion"
    assert inventario["rol"] == "CIT"
    assert inventario["version"] == "2.0"
    assert inventario["version_contrato"] == "1.0"
    assert inventario["esquema"] == "VPSI-CONTRACT-1.0"


# ===============================================================
# 15. TEST — REPORTE
# ===============================================================

def test_cit_reporte_por_engine(tmp_path):
    engine = _engine_cit(tmp_path)

    salida = engine.ejecutar_reporte("CIT")

    assert salida["estado"] == "EXITO"

    reporte = salida["resultado"]

    assert reporte["id"] == "CIT"
    assert reporte["nombre"] == "citacion"
    assert reporte["rol"] == "CIT"
    assert reporte["estado"] == "OPERATIVO"
    assert reporte["coherente"] is True


# ===============================================================
# 16. TEST — DIAGNÓSTICO
# ===============================================================

def test_cit_diagnostico_por_engine(tmp_path):
    engine = _engine_cit(tmp_path)

    salida = engine.ejecutar_diagnostico("CIT")

    assert salida["estado"] == "EXITO"

    diagnostico = salida["resultado"]

    assert diagnostico["id"] == "CIT"
    assert diagnostico["nombre"] == "citacion"
    assert diagnostico["rol"] == "CIT"
    assert diagnostico["estado"] == "OPERATIVO"
    assert diagnostico["coherente"] is True
    assert diagnostico["problemas"] == []


# ===============================================================
# 17. TEST — BARRER
# ===============================================================

def test_cit_barrer_por_engine(tmp_path):
    engine = _engine_cit(tmp_path)

    salida = engine.ejecutar_capacidad(
        "CIT",
        "barrer",
    )

    assert salida["estado"] == "EXITO"

    resultado = salida["resultado"]

    assert resultado["id"] == "CIT"
    assert resultado["coherente"] is True
    assert resultado["errores"] == []
    assert resultado["choques"] == []


# ===============================================================
# 18. TEST — VERIFICAR
# ===============================================================

def test_cit_verificar_por_engine(tmp_path):
    engine = _engine_cit(tmp_path)

    salida = engine.ejecutar_capacidad(
        "CIT",
        "verificar",
    )

    assert salida["estado"] == "EXITO"

    resultado = salida["resultado"]

    assert resultado["id"] == "CIT"
    assert resultado["coherente"] is True


# ===============================================================
# 19. TEST — ANUNCIAR
# ===============================================================

def test_cit_anunciar_por_engine(tmp_path):
    engine = _engine_cit(tmp_path)

    salida = engine.ejecutar_capacidad(
        "CIT",
        "anunciar",
    )

    assert salida["estado"] == "EXITO"

    resultado = salida["resultado"]

    assert isinstance(resultado, dict)
    assert resultado["id"] == "CIT"


# ===============================================================
# 20. TEST — ANUNCIAR_TODO
# ===============================================================

def test_cit_anunciar_todo_por_engine(tmp_path):
    engine = _engine_cit(tmp_path)

    salida = engine.ejecutar_capacidad(
        "CIT",
        "anunciar_todo",
    )

    assert salida["estado"] == "EXITO"

    resultado = salida["resultado"]

    assert resultado["id"] == "CIT"
    assert "anuncios" in resultado
    assert "n" in resultado


# ===============================================================
# 21. TEST — BUSCAR
# ===============================================================

def test_cit_buscar_por_engine(tmp_path):
    engine = _engine_cit(tmp_path)

    salida = engine.ejecutar_capacidad(
        "CIT",
        "buscar",
    )

    assert salida["estado"] == "EXITO"

    resultado = salida["resultado"]

    assert resultado["id"] == "CIT"
    assert "declaraciones" in resultado
    assert "n" in resultado


# ===============================================================
# 22. TEST — CITAR
# ===============================================================

def test_cit_citar_por_engine(tmp_path):
    engine = _engine_cit(tmp_path)

    salida = engine.ejecutar_capacidad(
        "CIT",
        "citar",
    )

    assert salida["estado"] == "EXITO"

    resultado = salida["resultado"]

    assert resultado["id"] == "CIT"
    assert "citas" in resultado
    assert "n" in resultado


# ===============================================================
# 23. TEST — LIMPIAR CICLO
# ===============================================================

def test_cit_limpiar_ciclo_por_engine(tmp_path):
    engine = _engine_cit(tmp_path)

    salida = engine.ejecutar_capacidad(
        "CIT",
        "limpiar_ciclo",
    )

    assert salida["estado"] == "EXITO"

    resultado = salida["resultado"]

    assert resultado["ok"] is True
    assert resultado["id"] == "CIT"


# ===============================================================
# 24. TEST — RESOLUCIÓN POR ID / NOMBRE / ROL
# ===============================================================

def test_engine_resuelve_cit_por_tres_identificadores(tmp_path):
    engine = _engine_cit(tmp_path)

    por_nombre = engine.registro.primero("citacion")
    por_id = engine.registro.primero("CIT")
    por_rol = engine.registro.primero("CIT")

    assert por_nombre is not None
    assert por_id is not None
    assert por_rol is not None

    assert por_nombre is por_id
    assert por_id is por_rol


# ===============================================================
# 25. TEST — GRAFO ESTRUCTURAL
# ===============================================================

def test_cit_grafo_estructural(tmp_path):
    engine = _engine_cit(tmp_path)

    grafo = engine.estado_global()["grafo"]

    nodos = grafo["nodos"]
    aristas = grafo["aristas"]

    modulo = next(
        n for n in nodos
        if n["tipo"] == "modulo"
        and n["id"] == "CIT"
    )

    assert modulo["nombre"] == "citacion"
    assert modulo["rol"] == "CIT"

    # CIT no declara dependencias.
    dependencias = [
        a for a in aristas
        if a["tipo"] == "requiere"
    ]

    assert dependencias == []


# ===============================================================
# 26. TEST — CAPACIDADES DEL GRAFO
# ===============================================================

def test_cit_capacidades_aparecen_en_grafo(tmp_path):
    engine = _engine_cit(tmp_path)

    cit = engine.registro.primero("CIT")
    assert cit is not None

    grafo = engine.estado_global()["grafo"]

    nodos_capacidad = {
        n["nombre"]
        for n in grafo["nodos"]
        if n["tipo"] == "capacidad"
        and n.get("modulo") == "citacion"
    }

    assert nodos_capacidad == set(cit.capacidades.keys())


# ===============================================================
# 27. TEST — CONSOLIDACIÓN DE REPORTES
# ===============================================================

def test_cit_consolidacion_de_reportes(tmp_path):
    engine = _engine_cit(tmp_path)

    consolidado = engine.consolidar_reportes()

    assert "citacion" in consolidado["reportes"]
    assert "citacion" in consolidado["diagnosticos"]
    assert "citacion" in consolidado["inventarios"]

    assert consolidado["reportes"]["citacion"]["id"] == "CIT"
    assert consolidado["diagnosticos"]["citacion"]["id"] == "CIT"
    assert consolidado["inventarios"]["citacion"]["id"] == "CIT"


# ===============================================================
# 28. TEST — PAQUETE OMEGA
# ===============================================================

def test_cit_aparece_en_paquete_omega(tmp_path):
    engine = _engine_cit(tmp_path)

    omega = engine.paquete_omega()

    assert omega["metadata"]["estado_engine"] == "OPERATIVO"
    assert omega["metadata"]["total_modulos"] == 1

    reportes = omega["reportes"]

    modulo_cit = next(
        r for r in reportes
        if r["id"] == "CIT"
    )

    contenido = modulo_cit["contenido"]

    assert contenido["id"] == "CIT"
    assert contenido["nombre"] == "citacion"
    assert contenido["rol"] == "CIT"

    assert contenido["requiere"] == []

    assert contenido["reporte"]["estado"] == "OPERATIVO"
    assert contenido["diagnostico"]["coherente"] is True
    assert contenido["inventario"]["id"] == "CIT"


# ===============================================================
# 29. TEST — TRAZA DE EJECUCIÓN
# ===============================================================

def test_cit_deja_traza_al_ser_ejecutado(tmp_path):
    engine = _engine_cit(tmp_path)

    antes = len(engine.obtener_trazas())

    salida = engine.ejecutar_reporte("CIT")

    assert salida["estado"] == "EXITO"

    despues = engine.obtener_trazas()

    assert len(despues) == antes + 1

    ultima = despues[-1]

    assert ultima["modulo"] == "citacion"
    assert ultima["capacidad"] == "reporte"
    assert ultima["estado"] == "EXITO"


# ===============================================================
# 30. TEST — NO HAY ERRORES DE ARRANQUE
# ===============================================================

def test_cit_acoplamiento_final_sin_errores(tmp_path):
    engine = _engine_cit(tmp_path)

    assert engine.estado == "OPERATIVO"
    assert engine.errores_arranque == []

    cit = engine.registro.primero("CIT")

    assert cit is not None
    assert cit.id == "CIT"
    assert cit.nombre == "citacion"
    assert cit.rol == "CIT"
    assert cit.requiere == []


# ===============================================================
# FIN DEL TEST
# ===============================================================
