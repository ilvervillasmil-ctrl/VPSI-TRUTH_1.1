# ===============================================================
# VPSI-TRUTH — tests/test_acoplamiento_cit.py
# ===============================================================

from __future__ import annotations

import copy
import importlib
import sys
import textwrap
from pathlib import Path
from typing import Any, Dict

import pytest


# ===============================================================
# RAÍZ DEL PROYECTO
# ===============================================================
#
# IMPORTANTE:
# Se debe establecer sys.path ANTES de importar core.engine.
#
# Esto hace que el test sea independiente de cómo pytest
# haya configurado el directorio de ejecución.
#
# ===============================================================

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

MODULOS = ROOT / "modules"


# ===============================================================
# ENGINE REAL
# ===============================================================

from core.engine import (
    BANDERAS_REPORTING,
    CLAVES_META_CAPACIDAD,
    CLAVES_OBLIGATORIAS_CONTRATO,
    Engine,
    ArranqueError,
)


# ===============================================================
# CONFIGURACIÓN DEL TEST
# ===============================================================

CIT_ID = "CIT"


# ===============================================================
# HELPERS
# ===============================================================

def crear_engine(strict: bool = True) -> Engine:
    return Engine(
        raiz_modulos=MODULOS,
        invocador_id="test_acoplamiento_cit",
        strict=strict,
    )


def obtener_cit(engine: Engine):
    cit = engine.registro.primero(CIT_ID)

    assert cit is not None, (
        "CIT no fue registrado por Engine. "
        "El desacople está antes de la materialización del módulo."
    )

    return cit


def copiar_contrato_cit() -> Dict[str, Any]:
    modulo = importlib.import_module("modules.citacion")

    contrato = getattr(modulo, "CONTENEDOR", None)

    assert isinstance(contrato, dict), (
        "CIT no expone CONTENEDOR como dict."
    )

    return copy.deepcopy(contrato)


def escribir_modulo_sintetico(
    raiz: Path,
    nombre: str,
    contrato: Dict[str, Any],
) -> Path:

    modulo_dir = raiz / nombre
    modulo_dir.mkdir(parents=True, exist_ok=True)

    contenido = textwrap.dedent(
        f"""
        from __future__ import annotations

        def capacidad_prueba(*args, **kwargs):
            return {{
                "ok": True,
                "args": args,
                "kwargs": kwargs,
            }}

        CONTENEDOR = {repr(contrato)}
        """
    )

    (modulo_dir / "__init__.py").write_text(
        contenido,
        encoding="utf-8",
    )

    return modulo_dir


def contrato_base_sintetico(
    base: Dict[str, Any],
) -> Dict[str, Any]:

    contrato = copy.deepcopy(base)

    contrato["id"] = "TEST"
    contrato["nombre"] = "test_contract"
    contrato["rol"] = "TEST"
    contrato["version_modulo"] = "1.0"

    return contrato


def preparar_capacidad_sintetica(
    contrato: Dict[str, Any],
) -> Dict[str, Any]:

    contrato["capacidades"] = {
        "capacidad_prueba": "PLACEHOLDER"
    }

    contrato["capacidades_meta"] = {
        "capacidad_prueba": {
            "descripcion": "Capacidad sintética para prueba.",
            "entrada": "args, kwargs",
            "salida": "dict",
        }
    }

    return contrato


# ===============================================================
# 1 — DESCUBRIMIENTO
# ===============================================================

def test_cit_es_descubierto_por_engine():
    engine = crear_engine()

    cit = obtener_cit(engine)

    assert cit.id == CIT_ID
    assert cit.nombre
    assert cit.rol
    assert cit.modulo is not None
    assert cit.ruta.exists()


# ===============================================================
# 2 — MATERIALIZACIÓN CONTRACTUAL
# ===============================================================

def test_cit_engine_materializa_el_contrato_sin_reconstruirlo():
    engine = crear_engine()
    cit = obtener_cit(engine)

    contrato = cit.meta

    assert isinstance(contrato, dict)

    for clave in CLAVES_OBLIGATORIAS_CONTRATO:
        assert clave in contrato, (
            f"CIT declara contrato incompleto: falta '{clave}'."
        )

    assert cit.id == str(contrato["id"])
    assert cit.nombre == str(contrato["nombre"])
    assert cit.rol == str(contrato["rol"])
    assert cit.version == str(contrato["version_modulo"])
    assert cit.version_contrato == str(contrato["version_contrato"])
    assert cit.esquema == str(contrato["esquema"])
    assert cit.estabilidad == str(contrato["estabilidad"])
    assert cit.descripcion == str(contrato["descripcion"])
    assert cit.compatible_desde == str(contrato["compatible_desde"])
    assert cit.api_engine == str(contrato["api_engine"])

    assert cit.funcion == contrato["funcion"]
    assert cit.no_hace == contrato["no_hace"]
    assert cit.autoridad == contrato["autoridad"]
    assert cit.conocimiento_exportable == contrato["conocimiento_exportable"]
    assert cit.consultas_soportadas == contrato["consultas_soportadas"]
    assert cit.invariantes == contrato["invariantes"]

    assert cit.requiere == contrato["requiere"]
    assert cit.autoriza_engine == contrato["autoriza_engine"]
    assert cit.capacidades == contrato["capacidades"]
    assert cit.capacidades_meta == contrato["capacidades_meta"]
    assert cit.reporting == contrato["reporting"]
    assert cit.estados_validos == contrato["estados_validos"]


# ===============================================================
# 3 — CAPACIDADES DINÁMICAS
# ===============================================================

def test_cit_capacidades_se_descubren_desde_el_contrato():
    engine = crear_engine()
    cit = obtener_cit(engine)

    capacidades = cit.meta["capacidades"]

    assert isinstance(capacidades, dict)

    for nombre, referencia in capacidades.items():
        assert nombre
        assert callable(referencia), (
            f"CIT declara '{nombre}', pero no es callable."
        )

        assert cit.fn(nombre) is referencia, (
            f"Desacople en capacidad '{nombre}'."
        )


# ===============================================================
# 4 — METADATA DE CAPACIDADES
# ===============================================================

def test_cit_toda_capacidad_tiene_metadata_contractual():
    engine = crear_engine()
    cit = obtener_cit(engine)

    for capacidad in cit.capacidades:
        assert capacidad in cit.capacidades_meta, (
            f"La capacidad '{capacidad}' no tiene capacidades_meta."
        )

        definicion = cit.capacidades_meta[capacidad]

        assert isinstance(definicion, dict)

        for campo in CLAVES_META_CAPACIDAD:
            assert campo in definicion, (
                f"'{capacidad}' carece de '{campo}'."
            )

            assert isinstance(definicion[campo], str), (
                f"'{capacidad}.{campo}' debe ser str."
            )


# ===============================================================
# 5 — AUTORIZACIÓN ENGINE
# ===============================================================

def test_cit_autorizacion_engine_es_compatible_con_engine():
    engine = crear_engine()
    cit = obtener_cit(engine)

    from core.engine import PERMISOS_AUTORIZA_ENGINE

    for permiso in PERMISOS_AUTORIZA_ENGINE:
        assert permiso in cit.autoriza_engine

        assert isinstance(
            cit.autoriza_engine[permiso],
            bool,
        )

    extras = (
        set(cit.autoriza_engine)
        - set(PERMISOS_AUTORIZA_ENGINE)
    )

    assert not extras, (
        f"CIT declara permisos Engine desconocidos: {sorted(extras)}"
    )


# ===============================================================
# 6 — REPORTING
# ===============================================================

def test_cit_reporting_es_compatible_con_engine():
    engine = crear_engine()
    cit = obtener_cit(engine)

    assert isinstance(cit.reporting, dict)

    # IMPORTANTE:
    # NO se compara igualdad exacta.
    #
    # CIT puede tener extensiones propias.
    #
    # Solo verificamos que contiene el contrato mínimo que
    # el Engine exige.

    for bandera in BANDERAS_REPORTING:
        assert bandera in cit.reporting

        assert isinstance(
            cit.reporting[bandera],
            bool,
        )


# ===============================================================
# 7 — ESTADOS
# ===============================================================

def test_cit_estados_son_compatibles_con_engine():
    engine = crear_engine()
    cit = obtener_cit(engine)

    from core.engine import ESTADOS_CANONICOS

    assert cit.estados_validos

    for estado in cit.estados_validos:
        assert estado in ESTADOS_CANONICOS


# ===============================================================
# 8 — DEPENDENCIAS
# ===============================================================

def test_cit_dependencias_estan_resueltas():
    engine = crear_engine()
    cit = obtener_cit(engine)

    assert isinstance(cit.requiere, list)

    faltantes = engine._dependencias.get(
        "faltantes",
        {},
    )

    assert cit.nombre not in faltantes, (
        f"CIT tiene dependencias no resueltas: "
        f"{faltantes.get(cit.nombre)}"
    )


# ===============================================================
# 9 — GRAFO
# ===============================================================

def test_cit_aparece_en_grafo_engine():
    engine = crear_engine()
    cit = obtener_cit(engine)

    nodos = engine._grafo.get("nodos", [])

    assert any(
        nodo.get("tipo") == "modulo"
        and (
            nodo.get("id") == cit.id
            or nodo.get("nombre") == cit.nombre
        )
        for nodo in nodos
    )


def test_cit_capacidades_aparecen_en_grafo_dinamicamente():
    engine = crear_engine()
    cit = obtener_cit(engine)

    nodos = engine._grafo.get("nodos", [])

    encontradas = {
        nodo.get("id")
        for nodo in nodos
        if nodo.get("tipo") == "capacidad"
        and nodo.get("modulo") == cit.nombre
    }

    esperadas = {
        f"{cit.nombre}.{capacidad}"
        for capacidad in cit.capacidades
    }

    assert encontradas == esperadas, (
        "Desacople CIT → grafo.\n"
        f"Esperadas: {sorted(esperadas)}\n"
        f"Encontradas: {sorted(encontradas)}"
    )


# ===============================================================
# 10 — REPORTING OPERATIVO
# ===============================================================

@pytest.mark.parametrize(
    "capacidad",
    [
        "reporte",
        "diagnostico",
        "inventario",
    ],
)
def test_cit_reporting_operativo_si_declara_capacidad(
    capacidad: str,
):
    engine = crear_engine()
    cit = obtener_cit(engine)

    if capacidad not in cit.capacidades:
        pytest.skip(
            f"CIT no declara '{capacidad}'."
        )

    salida = engine.ejecutar_capacidad(
        cit.nombre,
        capacidad,
    )

    assert salida.get("estado") == "EXITO", (
        f"CIT declara '{capacidad}', "
        f"pero Engine no pudo ejecutarla: {salida}"
    )


# ===============================================================
# 11 — OMEGA
# ===============================================================

def test_cit_se_consolida_en_paquete_omega():
    engine = crear_engine()

    paquete = engine.paquete_omega()

    assert isinstance(paquete, dict)
    assert "metadata" in paquete
    assert "reportes" in paquete

    assert any(
        reporte.get("id") == CIT_ID
        for reporte in paquete["reportes"]
    )


# ===============================================================
# 12 — INMUTABILIDAD DEL CONTRATO
# ===============================================================

def test_engine_no_muta_contrato_de_cit():
    engine = crear_engine()
    cit = obtener_cit(engine)

    original = copy.deepcopy(cit.meta)

    engine.censar()
    engine.estado_global()
    engine.paquete_omega()

    assert cit.meta == original, (
        "Engine modificó el CONTENEDOR de CIT."
    )


# ===============================================================
# 13 — NO HARDCODE
# ===============================================================

def test_acoplamiento_cit_no_hardcodea_capacidades():
    engine = crear_engine()
    cit = obtener_cit(engine)

    capacidades_contrato = set(
        cit.meta["capacidades"].keys()
    )

    capacidades_engine = set(
        cit.capacidades.keys()
    )

    assert capacidades_engine == capacidades_contrato


# ===============================================================
# FIN
# ===============================================================
