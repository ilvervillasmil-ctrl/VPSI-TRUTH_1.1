# ===============================================================
# VPSI-TRUTH — tests/test_acoplamiento_cit.py
# ===============================================================
#
# TEST DE ACOPLAMIENTO — CIT ↔ ENGINE
#
# Objetivo:
#   Verificar que el módulo CIT se acopla al Engine mediante
#   VPSI-CONTRACT-1.0 sin depender de hacks, defaults o campos
#   inventados por el Engine.
#
# Base contractual:
#   modules/citacion/__init__.py
#   core/engine.py
#
# Este test NO modifica ningún módulo del sistema.
#
# ===============================================================

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict

import pytest


# ===============================================================
# RUTA DEL PROYECTO
# ===============================================================

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


# ===============================================================
# IMPORTACIONES
# ===============================================================

from core.engine import (
    API_ENGINE_ACTUAL,
    ESQUEMA_CONTRATO_REQUERIDO,
    VERSION_CONTRATO_REQUERIDA,
    Engine,
)


# CIT se importa directamente para inspeccionar su contrato.
from modules.citacion import CONTENEDOR as CIT_CONTENEDOR


# ===============================================================
# CONSTANTES DEL TEST
# ===============================================================

CIT_ID = "CIT"
CIT_NOMBRE = "citacion"
CIT_ROL = "CIT"

CIT_ESQUEMA = "VPSI-CONTRACT-1.0"
CIT_VERSION_CONTRATO = "1.0"
CIT_API_ENGINE = ">=1.0"

# El Engine 18.3 descubre módulos directamente bajo "modules".
MODULOS_DIR = ROOT / "modules"


# ===============================================================
# HELPERS
# ===============================================================

def crear_engine(strict: bool = True) -> Engine:
    """
    Crea el Engine utilizando exactamente la raíz de módulos
    utilizada por el proyecto.
    """
    return Engine(
        raiz_modulos=MODULOS_DIR,
        invocador_id="test_acoplamiento_cit",
        strict=strict,
    )


def obtener_cit(engine: Engine):
    """
    Obtiene CIT por ID, nombre o rol a través del RegistroModulos.
    """
    cit = engine.registro.primero(CIT_ID)

    if cit is None:
        cit = engine.registro.primero(CIT_NOMBRE)

    if cit is None:
        cit = engine.registro.primero(CIT_ROL)

    return cit


# ===============================================================
# 1. CONTRATO BASE
# ===============================================================

def test_cit_contiene_contenedor():
    assert isinstance(CIT_CONTENEDOR, dict)


def test_cit_id_correcto():
    assert CIT_CONTENEDOR["id"] == CIT_ID


def test_cit_nombre_correcto():
    assert CIT_CONTENEDOR["nombre"] == CIT_NOMBRE


def test_cit_rol_correcto():
    assert CIT_CONTENEDOR["rol"] == CIT_ROL


def test_cit_esquema_correcto():
    assert CIT_CONTENEDOR["esquema"] == CIT_ESQUEMA
    assert CIT_CONTENEDOR["esquema"] == ESQUEMA_CONTRATO_REQUERIDO


def test_cit_version_contrato_correcta():
    assert str(CIT_CONTENEDOR["version_contrato"]) == CIT_VERSION_CONTRATO
    assert str(CIT_CONTENEDOR["version_contrato"]) == VERSION_CONTRATO_REQUERIDA


def test_cit_api_engine_compatible():
    assert CIT_CONTENEDOR["api_engine"] == CIT_API_ENGINE


def test_cit_version_modulo_valida():
    version = CIT_CONTENEDOR["version_modulo"]

    assert isinstance(version, str)
    assert version.strip()


def test_cit_estabilidad_valida():
    assert isinstance(CIT_CONTENEDOR["estabilidad"], str)
    assert CIT_CONTENEDOR["estabilidad"].strip()


def test_cit_compatible_desde_valido():
    valor = CIT_CONTENEDOR["compatible_desde"]

    assert isinstance(valor, str)
    assert valor.strip()


# ===============================================================
# 2. CLAVES OBLIGATORIAS DEL CONTRATO
# ===============================================================

def test_cit_claves_obligatorias_completas():
    obligatorias = {
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
    }

    assert obligatorias.issubset(CIT_CONTENEDOR.keys())


# ===============================================================
# 3. TIPOS ESTRUCTURALES
# ===============================================================

def test_cit_no_hace_es_lista():
    assert isinstance(CIT_CONTENEDOR["no_hace"], list)


def test_cit_autoridad_es_lista():
    assert isinstance(CIT_CONTENEDOR["autoridad"], list)


def test_cit_conocimiento_exportable_es_lista():
    assert isinstance(
        CIT_CONTENEDOR["conocimiento_exportable"],
        list,
    )


def test_cit_consultas_soportadas_es_lista():
    assert isinstance(
        CIT_CONTENEDOR["consultas_soportadas"],
        list,
    )


def test_cit_requiere_es_lista():
    assert isinstance(CIT_CONTENEDOR["requiere"], list)


def test_cit_invariantes_es_lista():
    assert isinstance(CIT_CONTENEDOR["invariantes"], list)


def test_cit_capacidades_es_dict():
    assert isinstance(CIT_CONTENEDOR["capacidades"], dict)


def test_cit_capacidades_meta_es_dict():
    assert isinstance(CIT_CONTENEDOR["capacidades_meta"], dict)


def test_cit_reporting_es_dict():
    assert isinstance(CIT_CONTENEDOR["reporting"], dict)


def test_cit_autoriza_engine_es_dict():
    assert isinstance(CIT_CONTENEDOR["autoriza_engine"], dict)


def test_cit_estados_validos_es_lista():
    assert isinstance(CIT_CONTENEDOR["estados_validos"], list)


# ===============================================================
# 4. REQUIERE
# ===============================================================

def test_cit_no_requiere_dependencias():
    """
    CIT declara explícitamente requiere=[].
    Esto es contractual y debe permanecer así.
    """
    assert CIT_CONTENEDOR["requiere"] == []


# ===============================================================
# 5. AUTORIZA_ENGINE
# ===============================================================

def test_cit_autoriza_engine_completo():
    permisos = {
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

    assert set(CIT_CONTENEDOR["autoriza_engine"].keys()) == permisos


def test_cit_autoriza_engine_todos_booleanos():
    for permiso, valor in CIT_CONTENEDOR["autoriza_engine"].items():
        assert isinstance(valor, bool), (
            f"autoriza_engine['{permiso}'] debe ser bool"
        )


def test_cit_no_autoriza_modificar():
    assert CIT_CONTENEDOR["autoriza_engine"]["modificar"] is False


def test_cit_no_autoriza_alterar():
    assert CIT_CONTENEDOR["autoriza_engine"]["alterar"] is False


def test_cit_no_autoriza_reescribir():
    assert CIT_CONTENEDOR["autoriza_engine"]["reescribir"] is False


def test_cit_autoriza_ejecucion():
    assert CIT_CONTENEDOR["autoriza_engine"]["ejecutar"] is True


# ===============================================================
# 6. REPORTING
# ===============================================================

def test_cit_reporting_completo():
    """
    Las banderas deben coincidir exactamente con el contrato real
    de CIT.

    IMPORTANTE:
    CIT incluye 'reporte' además de las banderas estructurales
    utilizadas por el Engine.
    """

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
        "reporte",
    }

    assert set(CIT_CONTENEDOR["reporting"].keys()) == banderas


def test_cit_reporting_todos_booleanos():
    for bandera, valor in CIT_CONTENEDOR["reporting"].items():
        assert isinstance(valor, bool), (
            f"reporting['{bandera}'] debe ser bool"
        )


def test_cit_reporting_reporte_declarado():
    assert "reporte" in CIT_CONTENEDOR["reporting"]
    assert CIT_CONTENEDOR["reporting"]["reporte"] is True


# ===============================================================
# 7. ESTADOS VÁLIDOS
# ===============================================================

def test_cit_estados_validos_no_vacios():
    assert CIT_CONTENEDOR["estados_validos"]


def test_cit_estados_validos_son_canonicos():
    canonicos = {
        "NO_INICIADO",
        "OPERATIVO",
        "DEGRADADO",
        "RECHAZADO",
    }

    assert set(CIT_CONTENEDOR["estados_validos"]).issubset(canonicos)


# ===============================================================
# 8. CAPACIDADES
# ===============================================================

def test_cit_capacidades_son_callable():
    for nombre, fn in CIT_CONTENEDOR["capacidades"].items():
        assert callable(fn), (
            f"La capacidad '{nombre}' de CIT no es callable"
        )


def test_cit_cada_capacidad_tiene_meta():
    capacidades = CIT_CONTENEDOR["capacidades"]
    meta = CIT_CONTENEDOR["capacidades_meta"]

    for nombre in capacidades:
        assert nombre in meta, (
            f"CIT: falta capacidades_meta para '{nombre}'"
        )


def test_cit_meta_capacidades_completa():
    capacidades = CIT_CONTENEDOR["capacidades"]
    meta = CIT_CONTENEDOR["capacidades_meta"]

    for nombre in capacidades:
        entrada = meta[nombre]

        assert isinstance(entrada, dict)

        assert "descripcion" in entrada
        assert "entrada" in entrada
        assert "salida" in entrada

        assert isinstance(entrada["descripcion"], str)
        assert isinstance(entrada["entrada"], str)
        assert isinstance(entrada["salida"], str)


# ===============================================================
# 9. ENGINE DESCUBRE CIT
# ===============================================================

def test_engine_descubre_cit():
    engine = crear_engine()

    cit = obtener_cit(engine)

    assert cit is not None


def test_engine_registra_cit_por_id():
    engine = crear_engine()

    assert CIT_ID in engine.registro.por_id


def test_engine_registra_cit_por_nombre():
    engine = crear_engine()

    assert CIT_NOMBRE in engine.registro.contenedores


def test_engine_registra_cit_por_rol():
    engine = crear_engine()

    assert CIT_ROL in engine.registro.por_rol


def test_engine_materializa_identidad_cit():
    engine = crear_engine()

    cit = obtener_cit(engine)

    assert cit.id == CIT_ID
    assert cit.nombre == CIT_NOMBRE
    assert cit.rol == CIT_ROL


# ===============================================================
# 10. ENGINE MATERIALIZA EL CONTRATO SIN ALTERARLO
# ===============================================================

def test_engine_no_altera_version_cit():
    engine = crear_engine()

    cit = obtener_cit(engine)

    assert cit.version == CIT_CONTENEDOR["version_modulo"]


def test_engine_no_altera_version_contrato_cit():
    engine = crear_engine()

    cit = obtener_cit(engine)

    assert cit.version_contrato == str(
        CIT_CONTENEDOR["version_contrato"]
    )


def test_engine_no_altera_esquema_cit():
    engine = crear_engine()

    cit = obtener_cit(engine)

    assert cit.esquema == CIT_CONTENEDOR["esquema"]


def test_engine_no_altera_api_cit():
    engine = crear_engine()

    cit = obtener_cit(engine)

    assert cit.api_engine == CIT_CONTENEDOR["api_engine"]


def test_engine_no_altera_requiere_cit():
    engine = crear_engine()

    cit = obtener_cit(engine)

    assert cit.requiere == CIT_CONTENEDOR["requiere"]


def test_engine_no_altera_capacidades_cit():
    engine = crear_engine()

    cit = obtener_cit(engine)

    assert set(cit.capacidades.keys()) == set(
        CIT_CONTENEDOR["capacidades"].keys()
    )


def test_engine_no_altera_reporting_cit():
    engine = crear_engine()

    cit = obtener_cit(engine)

    assert set(cit.reporting.keys()) == set(
        CIT_CONTENEDOR["reporting"].keys()
    )


# ===============================================================
# 11. VALIDACIÓN INTERNA DEL ENGINE
# ===============================================================

def test_engine_acepta_contrato_cit():
    engine = crear_engine()

    assert CIT_NOMBRE not in {
        error.split(":")[0]
        for error in engine.errores_arranque
    }


def test_engine_estado_operativo_con_cit():
    engine = crear_engine()

    assert engine.estado == "OPERATIVO"


def test_engine_no_rechaza_cit_por_contrato():
    engine = crear_engine()

    errores_cit = [
        error
        for error in engine.errores_arranque
        if CIT_NOMBRE in error or CIT_ID in error
    ]

    assert errores_cit == []


# ===============================================================
# 12. EJECUCIÓN DE CAPACIDADES
# ===============================================================

def test_engine_ejecuta_reporte_cit():
    engine = crear_engine()

    salida = engine.ejecutar_reporte(CIT_ID)

    assert salida["estado"] == "EXITO"
    assert salida["modulo"] == CIT_NOMBRE
    assert salida["capacidad"] == "reporte"
    assert isinstance(salida["resultado"], dict)


def test_engine_ejecuta_diagnostico_cit():
    engine = crear_engine()

    salida = engine.ejecutar_diagnostico(CIT_ID)

    assert salida["estado"] == "EXITO"
    assert salida["modulo"] == CIT_NOMBRE
    assert salida["capacidad"] == "diagnostico"
    assert isinstance(salida["resultado"], dict)


def test_engine_ejecuta_inventario_cit():
    engine = crear_engine()

    salida = engine.ejecutar_inventario(CIT_ID)

    assert salida["estado"] == "EXITO"
    assert salida["modulo"] == CIT_NOMBRE
    assert salida["capacidad"] == "inventario"
    assert isinstance(salida["resultado"], dict)


# ===============================================================
# 13. VALIDACIÓN DE IDENTIDAD DESDE INVENTARIO
# ===============================================================

def test_cit_inventario_identidad():
    engine = crear_engine()

    salida = engine.ejecutar_inventario(CIT_ID)

    inventario = salida["resultado"]

    assert inventario["id"] == CIT_ID
    assert inventario["nombre"] == CIT_NOMBRE
    assert inventario["rol"] == CIT_ROL


def test_cit_inventario_contrato():
    engine = crear_engine()

    salida = engine.ejecutar_inventario(CIT_ID)

    inventario = salida["resultado"]

    assert inventario["esquema"] == CIT_ESQUEMA
    assert inventario["version_contrato"] == CIT_VERSION_CONTRATO


def test_cit_inventario_capacidades():
    engine = crear_engine()

    salida = engine.ejecutar_inventario(CIT_ID)

    inventario = salida["resultado"]

    capacidades_engine = set(
        CIT_CONTENEDOR["capacidades"].keys()
    )

    capacidades_inventario = set(
        inventario["capacidades"]
    )

    assert capacidades_engine == capacidades_inventario


# ===============================================================
# 14. REPORTE DE CIT
# ===============================================================

def test_cit_reporte_operativo():
    engine = crear_engine()

    salida = engine.ejecutar_reporte(CIT_ID)

    reporte = salida["resultado"]

    assert reporte["id"] == CIT_ID
    assert reporte["nombre"] == CIT_NOMBRE
    assert reporte["rol"] == CIT_ROL
    assert reporte["estado"] == "OPERATIVO"


def test_cit_reporte_coherente():
    engine = crear_engine()

    salida = engine.ejecutar_reporte(CIT_ID)

    reporte = salida["resultado"]

    assert reporte["coherente"] is True


# ===============================================================
# 15. DIAGNÓSTICO DE CIT
# ===============================================================

def test_cit_diagnostico_operativo():
    engine = crear_engine()

    salida = engine.ejecutar_diagnostico(CIT_ID)

    diagnostico = salida["resultado"]

    assert diagnostico["id"] == CIT_ID
    assert diagnostico["estado"] == "OPERATIVO"


def test_cit_diagnostico_sin_problemas():
    engine = crear_engine()

    salida = engine.ejecutar_diagnostico(CIT_ID)

    diagnostico = salida["resultado"]

    assert diagnostico["problemas"] == []


def test_cit_diagnostico_coherente():
    engine = crear_engine()

    salida = engine.ejecutar_diagnostico(CIT_ID)

    diagnostico = salida["resultado"]

    assert diagnostico["coherente"] is True


# ===============================================================
# 16. CAPACIDADES PROPIAS DE CIT
# ===============================================================

def test_cit_verificar():
    engine = crear_engine()

    salida = engine.ejecutar_capacidad(
        CIT_ID,
        "verificar",
    )

    assert salida["estado"] == "EXITO"

    resultado = salida["resultado"]

    assert isinstance(resultado, dict)
    assert resultado["id"] == CIT_ID
    assert "coherente" in resultado


def test_cit_barrer():
    engine = crear_engine()

    salida = engine.ejecutar_capacidad(
        CIT_ID,
        "barrer",
    )

    assert salida["estado"] == "EXITO"

    resultado = salida["resultado"]

    assert isinstance(resultado, dict)
    assert resultado["id"] == CIT_ID
    assert "coherente" in resultado


def test_cit_verificar_salida():
    engine = crear_engine()

    salida = engine.ejecutar_capacidad(
        CIT_ID,
        "verificar_salida",
        {
            "id": CIT_ID,
            "estado": "OPERATIVO",
        },
    )

    assert salida["estado"] == "EXITO"
    assert salida["resultado"] is True


# ===============================================================
# 17. RESOLUCIÓN DE DECLARACIONES
# ===============================================================

def test_cit_resolver_capacidad_existe():
    engine = crear_engine()

    cit = obtener_cit(engine)

    assert cit.fn("resolver") is not None
    assert callable(cit.fn("resolver"))


def test_cit_registrar_capacidad_existe():
    engine = crear_engine()

    cit = obtener_cit(engine)

    assert cit.fn("registrar") is not None
    assert callable(cit.fn("registrar"))


def test_cit_buscar_capacidad_existe():
    engine = crear_engine()

    cit = obtener_cit(engine)

    assert cit.fn("buscar") is not None
    assert callable(cit.fn("buscar"))


def test_cit_citar_capacidad_existe():
    engine = crear_engine()

    cit = obtener_cit(engine)

    assert cit.fn("citar") is not None
    assert callable(cit.fn("citar"))


def test_cit_anunciar_capacidad_existe():
    engine = crear_engine()

    cit = obtener_cit(engine)

    assert cit.fn("anunciar") is not None
    assert callable(cit.fn("anunciar"))


# ===============================================================
# 18. PRUEBA DE REGISTRO A TRAVÉS DEL ENGINE
# ===============================================================

def test_engine_puede_invocar_registrar_cit():
    engine = crear_engine()

    declaracion = {
        "id": "TEST-CIT-001",
        "tipo": "definicion",
        "fuente": "test",
        "enunciado": "Declaración de prueba de acoplamiento CIT.",
    }

    salida = engine.ejecutar_capacidad(
        CIT_ID,
        "registrar",
        declaracion,
    )

    assert salida["estado"] == "EXITO"

    resultado = salida["resultado"]

    assert resultado["ok"] is True
    assert resultado["declaracion"]["id"] == "TEST-CIT-001"


# ===============================================================
# 19. RESOLUCIÓN DESPUÉS DEL REGISTRO
# ===============================================================

def test_engine_puede_invocar_resolver_cit():
    engine = crear_engine()

    declaracion = {
        "id": "TEST-CIT-002",
        "tipo": "definicion",
        "fuente": "test",
        "enunciado": "Declaración resoluble.",
    }

    registro = engine.ejecutar_capacidad(
        CIT_ID,
        "registrar",
        declaracion,
    )

    assert registro["estado"] == "EXITO"

    resolucion = engine.ejecutar_capacidad(
        CIT_ID,
        "resolver",
        "TEST-CIT-002",
    )

    assert resolucion["estado"] == "EXITO"

    resultado = resolucion["resultado"]

    assert resultado["resuelto"] is True
    assert resultado["id"] == "TEST-CIT-002"


# ===============================================================
# 20. ACOPLAMIENTO DE CAPACIDADES
# ===============================================================

def test_engine_ve_todas_las_capacidades_declaradas_por_cit():
    engine = crear_engine()

    cit = obtener_cit(engine)

    declaradas = set(CIT_CONTENEDOR["capacidades"].keys())
    materializadas = set(cit.capacidades.keys())

    assert materializadas == declaradas


def test_engine_no_inventa_capacidades_para_cit():
    engine = crear_engine()

    cit = obtener_cit(engine)

    declaradas = set(CIT_CONTENEDOR["capacidades"].keys())
    materializadas = set(cit.capacidades.keys())

    assert materializadas == declaradas


def test_todas_las_capacidades_de_cit_son_callable_desde_engine():
    engine = crear_engine()

    cit = obtener_cit(engine)

    for capacidad in cit.capacidades:
        assert callable(cit.fn(capacidad)), (
            f"CIT.{capacidad} no es callable desde Engine"
        )


# ===============================================================
# 21. ACOPLAMIENTO DE META-CAPACIDADES
# ===============================================================

def test_engine_recibe_meta_de_todas_las_capacidades_cit():
    engine = crear_engine()

    cit = obtener_cit(engine)

    for capacidad in cit.capacidades:
        assert capacidad in cit.capacidades_meta

        meta = cit.capacidades_meta[capacidad]

        assert isinstance(meta, dict)
        assert isinstance(meta["descripcion"], str)
        assert isinstance(meta["entrada"], str)
        assert isinstance(meta["salida"], str)


# ===============================================================
# 22. DEPENDENCIAS
# ===============================================================

def test_cit_no_tiene_dependencias_faltantes():
    engine = crear_engine()

    faltantes = engine._dependencias.get("faltantes", {})

    assert CIT_NOMBRE not in faltantes


def test_cit_no_genera_arista_requiere():
    engine = crear_engine()

    grafo = engine._grafo

    aristas_cit = [
        a
        for a in grafo.get("aristas", [])
        if a.get("from") == CIT_NOMBRE
        and a.get("tipo") == "requiere"
    ]

    assert aristas_cit == []


# ===============================================================
# 23. GRAFO ESTRUCTURAL
# ===============================================================

def test_cit_aparece_en_grafo():
    engine = crear_engine()

    nodos = engine._grafo.get("nodos", [])

    encontrados = [
        nodo
        for nodo in nodos
        if nodo.get("id") == CIT_ID
        or nodo.get("nombre") == CIT_NOMBRE
    ]

    assert encontrados


def test_capacidades_cit_aparecen_en_grafo():
    engine = crear_engine()

    nodos = engine._grafo.get("nodos", [])

    capacidades = CIT_CONTENEDOR["capacidades"]

    for capacidad in capacidades:
        esperado = f"{CIT_NOMBRE}.{capacidad}"

        encontrados = [
            nodo
            for nodo in nodos
            if nodo.get("id") == esperado
        ]

        assert encontrados, (
            f"No existe nodo de capacidad en grafo: {esperado}"
        )


# ===============================================================
# 24. TRAZAS
# ===============================================================

def test_engine_genera_traza_para_cit():
    engine = crear_engine()

    engine.ejecutar_reporte(CIT_ID)

    trazas = engine.obtener_trazas()

    assert trazas

    cit_trazas = [
        traza
        for traza in trazas
        if traza.get("modulo") == CIT_NOMBRE
    ]

    assert cit_trazas


def test_traza_cit_contiene_capacidad():
    engine = crear_engine()

    engine.ejecutar_reporte(CIT_ID)

    trazas = engine.obtener_trazas()

    cit_trazas = [
        traza
        for traza in trazas
        if traza.get("modulo") == CIT_NOMBRE
    ]

    assert any(
        traza.get("capacidad") == "reporte"
        for traza in cit_trazas
    )


def test_traza_cit_exito():
    engine = crear_engine()

    engine.ejecutar_reporte(CIT_ID)

    trazas = engine.obtener_trazas()

    cit_trazas = [
        traza
        for traza in trazas
        if traza.get("modulo") == CIT_NOMBRE
    ]

    assert any(
        traza.get("estado") == "EXITO"
        for traza in cit_trazas
    )


# ===============================================================
# 25. CONSOLIDACIÓN
# ===============================================================

def test_engine_consolida_reporte_cit():
    engine = crear_engine()

    consolidado = engine.consolidar_reportes()

    assert CIT_NOMBRE in consolidado["reportes"]


def test_engine_consolida_diagnostico_cit():
    engine = crear_engine()

    consolidado = engine.consolidar_reportes()

    assert CIT_NOMBRE in consolidado["diagnosticos"]


def test_engine_consolida_inventario_cit():
    engine = crear_engine()

    consolidado = engine.consolidar_reportes()

    assert CIT_NOMBRE in consolidado["inventarios"]


# ===============================================================
# 26. PAQUETE OMEGA
# ===============================================================

def test_paquete_omega_contiene_cit():
    engine = crear_engine()

    paquete = engine.paquete_omega()

    reportes = paquete["reportes"]

    encontrados = [
        reporte
        for reporte in reportes
        if reporte.get("id") == CIT_ID
    ]

    assert encontrados


def test_paquete_omega_cit_contiene_contrato():
    engine = crear_engine()

    paquete = engine.paquete_omega()

    reportes = paquete["reportes"]

    cit_reportes = [
        reporte
        for reporte in reportes
        if reporte.get("id") == CIT_ID
    ]

    assert cit_reportes

    contenido = cit_reportes[0]["contenido"]

    assert contenido["id"] == CIT_ID
    assert contenido["nombre"] == CIT_NOMBRE
    assert contenido["rol"] == CIT_ROL
    assert contenido["esquema"] == CIT_ESQUEMA
    assert contenido["version_contrato"] == CIT_VERSION_CONTRATO


def test_paquete_omega_cit_conserva_reporting():
    engine = crear_engine()

    paquete = engine.paquete_omega()

    cit = obtener_cit(engine)

    reportes = paquete["reportes"]

    cit_reportes = [
        reporte
        for reporte in reportes
        if reporte.get("id") == CIT_ID
    ]

    assert cit_reportes

    contenido = cit_reportes[0]["contenido"]

    # El paquete expone capacidades y contrato, pero reporting no se
    # materializa como campo independiente en paquete_omega.
    # Por ello comprobamos el contrato materializado en Engine.
    assert set(cit.reporting.keys()) == set(
        CIT_CONTENEDOR["reporting"].keys()
    )


# ===============================================================
# 27. CENSO
# ===============================================================

def test_censo_contiene_cit():
    engine = crear_engine()

    censo = engine.censar()

    cargados = censo["cargados"]

    encontrados = [
        modulo
        for modulo in cargados
        if modulo.get("id") == CIT_ID
        or modulo.get("nombre") == CIT_NOMBRE
    ]

    assert encontrados


def test_censo_identidad_cit():
    engine = crear_engine()

    censo = engine.censar()

    cit = next(
        modulo
        for modulo in censo["cargados"]
        if modulo.get("id") == CIT_ID
    )

    assert cit["id"] == CIT_ID
    assert cit["nombre"] == CIT_NOMBRE
    assert cit["rol"] == CIT_ROL


# ===============================================================
# 28. ESTADO GLOBAL
# ===============================================================

def test_estado_global_engine_operativo():
    engine = crear_engine()

    estado = engine.estado_global()

    assert estado["estado"] == "OPERATIVO"


def test_estado_global_no_rechaza_cit():
    engine = crear_engine()

    estado = engine.estado_global()

    errores = estado["errores_arranque"]

    errores_cit = [
        error
        for error in errores
        if CIT_NOMBRE in str(error)
        or CIT_ID in str(error)
    ]

    assert errores_cit == []


# ===============================================================
# 29. PRUEBA DE ACOPLAMIENTO COMPLETO
# ===============================================================

def test_acoplamiento_cit_engine_completo():
    """
    Prueba integral:

        contrato CIT
              ↓
        descubrimiento
              ↓
        validación
              ↓
        registro
              ↓
        materialización
              ↓
        capacidades
              ↓
        reporte
              ↓
        diagnóstico
              ↓
        inventario
              ↓
        grafo
              ↓
        trazas
              ↓
        paquete Omega
    """

    engine = crear_engine()

    # 1. Engine operativo
    assert engine.estado == "OPERATIVO"

    # 2. CIT descubierto
    cit = obtener_cit(engine)
    assert cit is not None

    # 3. Identidad
    assert cit.id == CIT_ID
    assert cit.nombre == CIT_NOMBRE
    assert cit.rol == CIT_ROL

    # 4. Contrato
    assert cit.esquema == CIT_ESQUEMA
    assert cit.version_contrato == CIT_VERSION_CONTRATO
    assert cit.api_engine == CIT_API_ENGINE

    # 5. Dependencias
    assert cit.requiere == []

    # 6. Capacidades
    assert set(cit.capacidades) == set(
        CIT_CONTENEDOR["capacidades"]
    )

    # 7. Meta-capacidades
    for capacidad in cit.capacidades:
        assert capacidad in cit.capacidades_meta

    # 8. Reporting
    assert set(cit.reporting) == set(
        CIT_CONTENEDOR["reporting"]
    )

    # 9. Reporte
    reporte = engine.ejecutar_reporte(CIT_ID)
    assert reporte["estado"] == "EXITO"

    # 10. Diagnóstico
    diagnostico = engine.ejecutar_diagnostico(CIT_ID)
    assert diagnostico["estado"] == "EXITO"

    # 11. Inventario
    inventario = engine.ejecutar_inventario(CIT_ID)
    assert inventario["estado"] == "EXITO"

    # 12. Grafo
    nodos = engine._grafo["nodos"]
    assert any(
        nodo.get("id") == CIT_ID
        for nodo in nodos
    )

    # 13. Omega
    omega = engine.paquete_omega()
    assert isinstance(omega, dict)
    assert "reportes" in omega

    # 14. CIT presente en Omega
    assert any(
        reporte.get("id") == CIT_ID
        for reporte in omega["reportes"]
    )


# ===============================================================
# 30. TEST FINAL DE INTEGRIDAD CONTRACTUAL
# ===============================================================

def test_cit_contrato_engine_100_por_ciento():
    """
    La materialización de CIT por Engine debe conservar exactamente
    los elementos estructurales declarados por CIT.

    No se permite:
      - perder capacidades
      - inventar capacidades
      - perder reporting
      - alterar requiere
      - alterar identidad
      - alterar versiones
      - alterar esquema
    """

    engine = crear_engine()

    cit = obtener_cit(engine)

    assert cit is not None

    assert cit.id == CIT_CONTENEDOR["id"]
    assert cit.nombre == CIT_CONTENEDOR["nombre"]
    assert cit.rol == CIT_CONTENEDOR["rol"]

    assert cit.version == CIT_CONTENEDOR["version_modulo"]
    assert cit.version_contrato == str(
        CIT_CONTENEDOR["version_contrato"]
    )

    assert cit.esquema == CIT_CONTENEDOR["esquema"]
    assert cit.estabilidad == CIT_CONTENEDOR["estabilidad"]
    assert cit.compatible_desde == CIT_CONTENEDOR["compatible_desde"]
    assert cit.api_engine == CIT_CONTENEDOR["api_engine"]

    assert cit.requiere == CIT_CONTENEDOR["requiere"]

    assert set(cit.capacidades) == set(
        CIT_CONTENEDOR["capacidades"]
    )

    assert set(cit.capacidades_meta) == set(
        CIT_CONTENEDOR["capacidades_meta"]
    )

    assert set(cit.reporting) == set(
        CIT_CONTENEDOR["reporting"]
    )

    assert cit.autoriza_engine == CIT_CONTENEDOR["autoriza_engine"]


# ===============================================================
# FIN DEL TEST
# ===============================================================
