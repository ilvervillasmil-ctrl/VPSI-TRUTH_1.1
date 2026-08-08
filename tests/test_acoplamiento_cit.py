# ===============================================================
# VPSI-TRUTH — tests/test_acoplamiento_cit.py
# ===============================================================
#
# TEST DE ACOPLAMIENTO — CIT ↔ ENGINE
#
# Objetivo:
#   Verificar que modules/citacion/__init__.py se acopla al
#   core/engine.py mediante VPSI-CONTRACT-1.0 sin modificar
#   ni debilitar el contrato.
#
# Este test NO elimina "requiere".
# Este test NO modifica CONTENEDOR.
# Este test NO sustituye capacidades.
# Este test verifica el contrato real.
#
# ===============================================================

from pathlib import Path

import pytest

from core.engine import (
    Engine,
    VERSION_ENGINE,
    ESQUEMA_CONTRATO_REQUERIDO,
    VERSION_CONTRATO_REQUERIDA,
)


# ===============================================================
# RUTAS
# ===============================================================

ROOT = Path(__file__).resolve().parents[1]
MODULES_DIR = ROOT / "modules"
CIT_DIR = MODULES_DIR / "citacion"


# ===============================================================
# IMPORTACIÓN DEL CONTRATO REAL
# ===============================================================

def cargar_citacion():
    import importlib

    return importlib.import_module("modules.citacion")


# ===============================================================
# 1 — EXISTENCIA ESTRUCTURAL
# ===============================================================

def test_cit_existe_como_modulo():
    assert CIT_DIR.is_dir(), (
        f"No existe el directorio del módulo CIT: {CIT_DIR}"
    )

    assert (CIT_DIR / "__init__.py").is_file(), (
        "CIT no contiene modules/citacion/__init__.py"
    )


# ===============================================================
# 2 — CONTENEDOR
# ===============================================================

def test_cit_expone_contenedor():
    cit = cargar_citacion()

    assert hasattr(cit, "CONTENEDOR"), (
        "CIT no expone CONTENEDOR"
    )

    assert isinstance(cit.CONTENEDOR, dict), (
        "CIT.CONTENEDOR debe ser dict"
    )


# ===============================================================
# 3 — IDENTIDAD CONTRACTUAL
# ===============================================================

def test_cit_identidad_contractual():
    cit = cargar_citacion()
    c = cit.CONTENEDOR

    assert c["id"] == "CIT"
    assert c["nombre"] == "citacion"
    assert c["rol"] == "CIT"

    assert c["version_modulo"] == "2.0"
    assert c["version_contrato"] == VERSION_CONTRATO_REQUERIDA

    assert c["esquema"] == ESQUEMA_CONTRATO_REQUERIDO
    assert c["estabilidad"] == "ESTABLE"
    assert c["compatible_desde"] == "1.0"
    assert c["api_engine"] == ">=1.0"


# ===============================================================
# 4 — CONTRATO COMPLETO SEGÚN ENGINE
# ===============================================================

def test_cit_cumple_claves_obligatorias_del_engine():
    cit = cargar_citacion()
    c = cit.CONTENEDOR

    claves = (
        "esquema",
        "version_contrato",
        "version_modulo",
        "id",
        "nombre",
        "rol",
        "descripcion",
        "funcion",
        "no_hace",
        "autoridad",
        "conocimiento_exportable",
        "requiere",
        "autoriza_engine",
        "consultas_soportadas",
        "capacidades",
        "capacidades_meta",
        "reporting",
        "estados_validos",
        "invariantes",
        "estabilidad",
        "compatible_desde",
        "api_engine",
    )

    for clave in claves:
        assert clave in c, (
            f"CIT no cumple contrato Engine: falta '{clave}'"
        )


# ===============================================================
# 5 — REQUIERE
# ===============================================================
#
# Este punto es deliberadamente explícito.
#
# CIT declara que no requiere módulos:
#
#     "requiere": []
#
# No se elimina el campo.
# Se comprueba que existe y que su valor es una lista vacía.
# ===============================================================

def test_cit_requiere_es_lista_y_no_tiene_dependencias():
    cit = cargar_citacion()
    c = cit.CONTENEDOR

    assert "requiere" in c

    assert isinstance(c["requiere"], list), (
        "CIT.requiere debe ser list"
    )

    assert c["requiere"] == [], (
        "CIT declara dependencias inesperadas: "
        f"{c['requiere']}"
    )


# ===============================================================
# 6 — AUTORIZACIÓN ENGINE
# ===============================================================

def test_cit_autoriza_engine_tiene_esquema_completo():
    cit = cargar_citacion()
    auth = cit.CONTENEDOR["autoriza_engine"]

    permisos = (
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
    )

    assert isinstance(auth, dict)

    for permiso in permisos:
        assert permiso in auth, (
            f"CIT.autoriza_engine no declara '{permiso}'"
        )
        assert isinstance(auth[permiso], bool), (
            f"CIT.autoriza_engine['{permiso}'] no es bool"
        )

    assert auth["ejecutar"] is True

    assert auth["modificar"] is False
    assert auth["alterar"] is False
    assert auth["reescribir"] is False


# ===============================================================
# 7 — CAPACIDADES
# ===============================================================

def test_cit_capacidades_son_callables():
    cit = cargar_citacion()
    capacidades = cit.CONTENEDOR["capacidades"]

    assert isinstance(capacidades, dict)
    assert capacidades, "CIT no declara capacidades"

    for nombre, fn in capacidades.items():
        assert callable(fn), (
            f"CIT.capacidades['{nombre}'] no es callable"
        )


# ===============================================================
# 8 — CAPACIDADES_META
# ===============================================================

def test_cit_capacidades_meta_acopla_una_a_una():
    cit = cargar_citacion()
    c = cit.CONTENEDOR

    capacidades = c["capacidades"]
    meta = c["capacidades_meta"]

    assert isinstance(meta, dict)

    for nombre in capacidades:
        assert nombre in meta, (
            f"CIT declara capacidad '{nombre}' "
            "pero no tiene capacidades_meta correspondiente"
        )

        descripcion = meta[nombre]

        assert isinstance(descripcion, dict)

        for campo in ("descripcion", "entrada", "salida"):
            assert campo in descripcion, (
                f"CIT.capacidades_meta['{nombre}'] "
                f"no contiene '{campo}'"
            )

            assert isinstance(descripcion[campo], str), (
                f"CIT.capacidades_meta['{nombre}']['{campo}'] "
                "debe ser str"
            )


# ===============================================================
# 9 — REPORTING
# ===============================================================

def test_cit_reporting_cumple_banderas_engine():
    cit = cargar_citacion()
    reporting = cit.CONTENEDOR["reporting"]

    banderas = (
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
    )

    assert isinstance(reporting, dict)

    for bandera in banderas:
        assert bandera in reporting, (
            f"CIT.reporting no declara '{bandera}'"
        )
        assert isinstance(reporting[bandera], bool), (
            f"CIT.reporting['{bandera}'] debe ser bool"
        )


# ===============================================================
# 10 — ESTADOS
# ===============================================================

def test_cit_estados_validos_son_compatibles_con_engine():
    cit = cargar_citacion()
    estados = cit.CONTENEDOR["estados_validos"]

    assert isinstance(estados, list)
    assert estados

    estados_engine = {
        "NO_INICIADO",
        "OPERATIVO",
        "DEGRADADO",
        "RECHAZADO",
    }

    for estado in estados:
        assert estado in estados_engine, (
            f"CIT declara estado no reconocido por Engine: {estado}"
        )


# ===============================================================
# 11 — ENGINE DESCUBRE CIT
# ===============================================================

def test_engine_descubre_cit():
    engine = Engine(MODULES_DIR, strict=False)

    nombres = set(engine.registro.contenedores.keys())

    assert "citacion" in nombres, (
        "Engine no descubrió el módulo citacion"
    )


# ===============================================================
# 12 — ENGINE MATERIALIZA EL CONTENEDOR CIT
# ===============================================================

def test_engine_materializa_cit_sin_alterar_identidad():
    engine = Engine(MODULES_DIR, strict=False)

    cit = engine.registro.primero("CIT")

    assert cit is not None, (
        "Engine no registró CIT por id"
    )

    assert cit.id == "CIT"
    assert cit.nombre == "citacion"
    assert cit.rol == "CIT"

    assert cit.version == "2.0"
    assert cit.version_contrato == "1.0"
    assert cit.esquema == "VPSI-CONTRACT-1.0"
    assert cit.api_engine == ">=1.0"


# ===============================================================
# 13 — ENGINE CONSERVA REQUIERE
# ===============================================================

def test_engine_conserva_requiere_de_cit():
    engine = Engine(MODULES_DIR, strict=False)

    cit = engine.registro.primero("CIT")

    assert cit is not None

    assert isinstance(cit.requiere, list)
    assert cit.requiere == []


# ===============================================================
# 14 — ENGINE RESUELVE CAPACIDADES DE CIT
# ===============================================================

def test_engine_resuelve_todas_las_capacidades_de_cit():
    engine = Engine(MODULES_DIR, strict=False)

    cit = engine.registro.primero("CIT")

    assert cit is not None

    for nombre in cit.capacidades:
        fn = cit.fn(nombre)

        assert fn is not None, (
            f"Engine no pudo resolver capacidad CIT: {nombre}"
        )

        assert callable(fn), (
            f"Engine resolvió una capacidad no callable: {nombre}"
        )


# ===============================================================
# 15 — ENGINE PUEDE EJECUTAR INVENTARIO
# ===============================================================

def test_engine_ejecuta_inventario_cit():
    engine = Engine(MODULES_DIR, strict=False)

    resultado = engine.ejecutar_inventario("CIT")

    assert resultado["estado"] == "EXITO"
    assert resultado["modulo"] == "citacion"
    assert resultado["capacidad"] == "inventario"

    inventario = resultado["resultado"]

    assert isinstance(inventario, dict)
    assert inventario["id"] == "CIT"
    assert inventario["nombre"] == "citacion"
    assert inventario["rol"] == "CIT"


# ===============================================================
# 16 — ENGINE PUEDE EJECUTAR REPORTE
# ===============================================================

def test_engine_ejecuta_reporte_cit():
    engine = Engine(MODULES_DIR, strict=False)

    resultado = engine.ejecutar_reporte("CIT")

    assert resultado["estado"] == "EXITO"
    assert resultado["modulo"] == "citacion"
    assert resultado["capacidad"] == "reporte"

    reporte = resultado["resultado"]

    assert isinstance(reporte, dict)
    assert reporte["id"] == "CIT"
    assert reporte["estado"] == "OPERATIVO"


# ===============================================================
# 17 — ENGINE PUEDE EJECUTAR DIAGNÓSTICO
# ===============================================================

def test_engine_ejecuta_diagnostico_cit():
    engine = Engine(MODULES_DIR, strict=False)

    resultado = engine.ejecutar_diagnostico("CIT")

    assert resultado["estado"] == "EXITO"
    assert resultado["modulo"] == "citacion"
    assert resultado["capacidad"] == "diagnostico"

    diagnostico = resultado["resultado"]

    assert isinstance(diagnostico, dict)
    assert diagnostico["id"] == "CIT"
    assert diagnostico["coherente"] is True


# ===============================================================
# 18 — GRAFO
# ===============================================================

def test_engine_grafo_contiene_cit_y_sus_capacidades():
    engine = Engine(MODULES_DIR, strict=False)

    grafo = engine._grafo

    assert isinstance(grafo, dict)
    assert "nodos" in grafo
    assert "aristas" in grafo

    nodos = grafo["nodos"]

    nodo_cit = [
        n for n in nodos
        if n.get("id") == "CIT"
    ]

    assert nodo_cit, "CIT no aparece como nodo del grafo"

    capacidades_cit = engine.registro.primero("CIT").capacidades

    for capacidad in capacidades_cit:
        cap_id = f"citacion.{capacidad}"

        assert any(
            n.get("id") == cap_id
            for n in nodos
        ), (
            f"Capacidad CIT no aparece en grafo: {cap_id}"
        )


# ===============================================================
# 19 — DEPENDENCIAS
# ===============================================================

def test_engine_registra_dependencias_de_cit_sin_falsificarlas():
    engine = Engine(MODULES_DIR, strict=False)

    dep = engine._dependencias

    assert isinstance(dep, dict)

    grafo_dep = dep["grafo"]
    faltantes = dep["faltantes"]

    assert "citacion" in grafo_dep
    assert grafo_dep["citacion"] == []

    assert "citacion" not in faltantes


# ===============================================================
# 20 — CONSOLIDACIÓN
# ===============================================================

def test_engine_consolida_cit():
    engine = Engine(MODULES_DIR, strict=False)

    consolidado = engine.consolidar_reportes()

    assert "reportes" in consolidado
    assert "diagnosticos" in consolidado
    assert "inventarios" in consolidado

    assert "citacion" in consolidado["reportes"]
    assert "citacion" in consolidado["diagnosticos"]
    assert "citacion" in consolidado["inventarios"]


# ===============================================================
# 21 — PAQUETE OMEGA
# ===============================================================

def test_engine_paquete_omega_contiene_cit():
    engine = Engine(MODULES_DIR, strict=False)

    paquete = engine.paquete_omega()

    assert isinstance(paquete, dict)
    assert "metadata" in paquete
    assert "reportes" in paquete

    reportes = paquete["reportes"]

    cit_reportes = [
        r for r in reportes
        if r.get("id") == "CIT"
    ]

    assert cit_reportes, (
        "paquete_omega() no contiene reporte del módulo CIT"
    )

    contenido = cit_reportes[0]["contenido"]

    assert contenido["id"] == "CIT"
    assert contenido["nombre"] == "citacion"
    assert contenido["rol"] == "CIT"
    assert contenido["requiere"] == []


# ===============================================================
# 22 — TRAZA DE EJECUCIÓN
# ===============================================================

def test_engine_deja_traza_de_ejecucion_de_cit():
    engine = Engine(MODULES_DIR, strict=False)

    resultado = engine.ejecutar_inventario("CIT")

    assert resultado["estado"] == "EXITO"

    trazas = engine.obtener_trazas()

    assert trazas

    trazas_cit = [
        t for t in trazas
        if t.get("modulo") == "citacion"
        and t.get("capacidad") == "inventario"
    ]

    assert trazas_cit

    assert trazas_cit[-1]["estado"] == "EXITO"


# ===============================================================
# 23 — ACOPLAMIENTO DIRECTO CIT ↔ ENGINE
# ===============================================================

def test_acoplamiento_cit_engine_completo():
    """
    Prueba de integración estructural:

        CIT.CONTENEDOR
              ↓
        Engine
              ↓
        RegistroModulos
              ↓
        Contenedor CIT
              ↓
        capacidad
              ↓
        ejecución
              ↓
        resultado
              ↓
        traza
    """

    cit = cargar_citacion()
    contrato = cit.CONTENEDOR

    engine = Engine(MODULES_DIR, strict=False)

    cont = engine.registro.primero("CIT")

    assert cont is not None

    # Identidad
    assert cont.id == contrato["id"]
    assert cont.nombre == contrato["nombre"]
    assert cont.rol == contrato["rol"]

    # Versionado
    assert cont.version == contrato["version_modulo"]
    assert cont.version_contrato == contrato["version_contrato"]
    assert cont.esquema == contrato["esquema"]
    assert cont.api_engine == contrato["api_engine"]

    # Dependencias
    assert cont.requiere == contrato["requiere"]

    # Capacidades
    assert set(cont.capacidades) == set(
        contrato["capacidades"]
    )

    # Autorización
    assert cont.autoriza_engine == contrato["autoriza_engine"]

    # Ejecución real de una capacidad declarada
    assert "inventario" in cont.capacidades

    salida = engine.ejecutar_capacidad(
        "CIT",
        "inventario",
    )

    assert salida["estado"] == "EXITO"

    resultado = salida["resultado"]

    assert isinstance(resultado, dict)
    assert resultado["id"] == "CIT"
    assert resultado["nombre"] == "citacion"

    # Evidencia de ejecución
    trazas = engine.obtener_trazas()

    assert any(
        t.get("modulo") == "citacion"
        and t.get("capacidad") == "inventario"
        and t.get("estado") == "EXITO"
        for t in trazas
    )


# ===============================================================
# FIN DEL TEST
# ===============================================================
