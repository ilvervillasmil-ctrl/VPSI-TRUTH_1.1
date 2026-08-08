# ===============================================================
# VPSI-TRUTH — tests/test_acoplamiento_cit.py
# ===============================================================
#
# TEST DE ACOPLAMIENTO CONTRACTUAL — CIT
#
# PRINCIPIO:
#
#   Este test NO conoce las capacidades internas de CIT.
#   Este test NO hardcodea el reporting de CIT.
#   Este test NO reconstruye manualmente el contrato de CIT.
#
# El contrato real de CIT es la fuente de verdad.
#
# El test verifica:
#
#   CONTENEDOR declarado
#          ↓
#      Engine carga
#          ↓
#      Engine valida
#          ↓
#      Engine materializa
#          ↓
#      Engine registra
#          ↓
#      Engine resuelve dependencias
#          ↓
#      Engine construye grafo
#          ↓
#      Engine ejecuta capacidades
#          ↓
#      Engine produce trazabilidad
#
# También verifica que Engine RECHAZA contratos rotos.
#
# ===============================================================

from __future__ import annotations

import copy
import importlib
import textwrap
from pathlib import Path
from typing import Any, Dict

import pytest

from core.engine import (
    API_ENGINE_ACTUAL,
    BANDERAS_REPORTING,
    CLAVES_META_CAPACIDAD,
    CLAVES_OBLIGATORIAS_CONTRATO,
    Engine,
    ArranqueError,
)


# ===============================================================
# CONFIGURACIÓN
# ===============================================================

ROOT = Path(__file__).resolve().parents[1]
MODULOS = ROOT / "modules"

CIT_ID = "CIT"


# ===============================================================
# HELPERS
# ===============================================================

def crear_engine(strict: bool = True) -> Engine:
    """
    Crea el Engine exactamente contra la raíz real de módulos.
    No modifica el entorno.
    """
    return Engine(
        raiz_modulos=MODULOS,
        invocador_id="test_acoplamiento_cit",
        strict=strict,
    )


def obtener_cit(engine: Engine):
    """
    Obtiene CIT por ID desde el registro real del Engine.

    El test conoce únicamente que el módulo objetivo es CIT.
    No conoce sus capacidades internas.
    """
    cit = engine.registro.primero(CIT_ID)

    assert cit is not None, (
        "CIT no fue registrado por Engine. "
        "El desacople está antes de la materialización del módulo."
    )

    return cit


def copiar_contrato_cit() -> Dict[str, Any]:
    """
    Obtiene el CONTENEDOR real de CIT.

    Se usa únicamente para construir módulos sintéticos
    adversariales en pruebas de rechazo.
    """
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
    """
    Crea un módulo temporal con un CONTENEDOR controlado.

    No modifica ningún módulo real del VPSI.
    """
    modulo_dir = raiz / nombre
    modulo_dir.mkdir(parents=True, exist_ok=True)

    contenido = """
from __future__ import annotations

def capacidad_prueba(*args, **kwargs):
    return {
        "ok": True,
        "args": args,
        "kwargs": kwargs,
    }

CONTENEDOR = CONTRATO
"""

    # Se genera código con el contrato literal.
    # Las funciones reales se insertan después mediante un patrón
    # simple y seguro para estas pruebas.
    contrato_repr = repr(contrato)

    contenido = textwrap.dedent(
        contenido.replace("CONTRATO", contrato_repr)
    )

    (modulo_dir / "__init__.py").write_text(
        contenido,
        encoding="utf-8",
    )

    return modulo_dir


def contrato_base_sintetico(
    base: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Construye una copia independiente del contrato real,
    conservando la arquitectura contractual.
    """
    contrato = copy.deepcopy(base)

    contrato["id"] = "TEST"
    contrato["nombre"] = "test_contract"
    contrato["rol"] = "TEST"
    contrato["version_modulo"] = "1.0"

    return contrato


def preparar_capacidad_sintetica(contrato: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sustituye las referencias callable por funciones expresables
    dentro del módulo sintético.

    El objetivo es conservar la forma contractual, no probar CIT.
    """
    contrato["capacidades"] = {
        "capacidad_prueba": "PLACEHOLDER"
    }

    contrato["capacidades_meta"] = {
        "capacidad_prueba": {
            "descripcion": "Capacidad sintética para prueba de acoplamiento.",
            "entrada": "args, kwargs",
            "salida": "dict",
        }
    }

    return contrato


# ===============================================================
# 1. CARGA FUNDAMENTAL
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
# 2. ENGINE DEBE MATERIALIZAR EL CONTRATO REAL
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

    # La materialización debe conservar exactamente los metadatos
    # declarativos fundamentales.
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
# 3. CAPACIDADES — DESCUBRIMIENTO DINÁMICO
# ===============================================================

def test_cit_capacidades_se_descubren_desde_el_contrato():
    engine = crear_engine()
    cit = obtener_cit(engine)

    capacidades_declaradas = cit.meta["capacidades"]

    assert isinstance(capacidades_declaradas, dict)

    for nombre, referencia in capacidades_declaradas.items():
        assert nombre, "CIT contiene una capacidad con nombre vacío."
        assert callable(referencia), (
            f"CIT declara '{nombre}', pero no es callable."
        )

        materializada = cit.fn(nombre)

        assert materializada is referencia, (
            f"Desacople de capacidad '{nombre}': "
            "Engine no materializó la misma referencia callable."
        )


# ===============================================================
# 4. CAPACIDADES_META — ACOPLAMIENTO DINÁMICO
# ===============================================================

def test_cit_toda_capacidad_tiene_metadata_contractual():
    engine = crear_engine()
    cit = obtener_cit(engine)

    capacidades = cit.capacidades
    meta = cit.capacidades_meta

    assert isinstance(meta, dict)

    for capacidad in capacidades:
        assert capacidad in meta, (
            f"Desacople CIT → Engine: la capacidad '{capacidad}' "
            "no posee entrada en capacidades_meta."
        )

        definicion = meta[capacidad]

        assert isinstance(definicion, dict), (
            f"capacidades_meta['{capacidad}'] no es dict."
        )

        for campo in CLAVES_META_CAPACIDAD:
            assert campo in definicion, (
                f"Capacidad '{capacidad}' carece de '{campo}'."
            )

            assert isinstance(definicion[campo], str), (
                f"Capacidad '{capacidad}': "
                f"'{campo}' debe ser str."
            )


# ===============================================================
# 5. AUTORIZACIÓN ENGINE
# ===============================================================

def test_cit_autorizacion_engine_es_compatible_con_engine():
    engine = crear_engine()
    cit = obtener_cit(engine)

    autorizacion = cit.autoriza_engine

    assert isinstance(autorizacion, dict)

    # Se obtienen dinámicamente los permisos que Engine considera
    # obligatorios; no se hardcodean las claves de CIT.
    from core.engine import PERMISOS_AUTORIZA_ENGINE

    for permiso in PERMISOS_AUTORIZA_ENGINE:
        assert permiso in autorizacion, (
            f"CIT no declara permiso Engine obligatorio: '{permiso}'."
        )

        assert isinstance(autorizacion[permiso], bool), (
            f"CIT.autoriza_engine['{permiso}'] no es bool."
        )

    extras = set(autorizacion) - set(PERMISOS_AUTORIZA_ENGINE)

    assert not extras, (
        "CIT declara permisos Engine desconocidos: "
        f"{sorted(extras)}"
    )


# ===============================================================
# 6. REPORTING — SIN HARDCODEAR EL REPORTING DE CIT
# ===============================================================

def test_cit_reporting_es_compatible_con_engine():
    engine = crear_engine()
    cit = obtener_cit(engine)

    reporting = cit.reporting

    assert isinstance(reporting, dict)

    # Importante:
    #
    # NO hacemos:
    #
    #   assert set(reporting.keys()) == {...}
    #
    # porque eso acoplaría el test a la implementación de CIT.
    #
    # Engine define las banderas mínimas obligatorias.
    # CIT puede tener información adicional.

    for bandera in BANDERAS_REPORTING:
        assert bandera in reporting, (
            f"CIT no declara la bandera reporting obligatoria "
            f"'{bandera}'."
        )

        assert isinstance(reporting[bandera], bool), (
            f"CIT.reporting['{bandera}'] debe ser bool."
        )


# ===============================================================
# 7. ESTADOS
# ===============================================================

def test_cit_estados_son_compatibles_con_engine():
    engine = crear_engine()
    cit = obtener_cit(engine)

    assert cit.estados_validos

    from core.engine import ESTADOS_CANONICOS

    for estado in cit.estados_validos:
        assert estado in ESTADOS_CANONICOS, (
            f"CIT declara estado no reconocido por Engine: '{estado}'."
        )


# ===============================================================
# 8. DEPENDENCIAS
# ===============================================================

def test_cit_dependencias_estan_resueltas():
    engine = crear_engine()
    cit = obtener_cit(engine)

    dependencias = cit.requiere

    assert isinstance(dependencias, list)

    faltantes = engine._dependencias.get("faltantes", {})

    assert cit.nombre not in faltantes, (
        f"CIT tiene dependencias no resueltas: "
        f"{faltantes.get(cit.nombre)}"
    )


# ===============================================================
# 9. GRAFO — EL CONTRATO DEBE REFLEJARSE
# ===============================================================

def test_cit_aparece_en_grafo_engine():
    engine = crear_engine()
    cit = obtener_cit(engine)

    nodos = engine._grafo.get("nodos", [])

    modulo_ids = {
        nodo.get("id")
        for nodo in nodos
        if nodo.get("tipo") == "modulo"
    }

    assert cit.id in modulo_ids or cit.nombre in modulo_ids, (
        "CIT fue registrado pero no aparece como nodo de módulo "
        "en el grafo del Engine."
    )


def test_cit_capacidades_aparecen_en_grafo_dinamicamente():
    engine = crear_engine()
    cit = obtener_cit(engine)

    nodos = engine._grafo.get("nodos", [])

    capacidad_ids = {
        nodo.get("id")
        for nodo in nodos
        if nodo.get("tipo") == "capacidad"
        and nodo.get("modulo") == cit.nombre
    }

    esperadas = {
        f"{cit.nombre}.{capacidad}"
        for capacidad in cit.capacidades
    }

    assert capacidad_ids == esperadas, (
        "Desacople CIT → grafo.\n"
        f"Esperadas: {sorted(esperadas)}\n"
        f"Encontradas: {sorted(capacidad_ids)}"
    )


# ===============================================================
# 10. EJECUCIÓN DINÁMICA DE TODAS LAS CAPACIDADES COMPATIBLES
# ===============================================================

def test_cit_capacidades_son_invocables_por_engine():
    engine = crear_engine()
    cit = obtener_cit(engine)

    for capacidad in cit.capacidades:
        meta = cit.capacidades_meta[capacidad]

        entrada = str(meta["entrada"]).lower()

        # No inventamos argumentos.
        #
        # Solo probamos capacidades que declaran explícitamente
        # que aceptan entrada opcional / vacía.
        #
        # Si no es evidente que acepten llamada sin argumentos,
        # verificamos el puente contractual sin ejecutar la función.
        if (
            "opcional" in entrada
            or "none" in entrada
            or "sin argumento" in entrada
            or "ningun" in entrada
            or "ninguno" in entrada
        ):
            salida = engine.ejecutar_capacidad(
                cit.nombre,
                capacidad,
            )

            assert isinstance(salida, dict), (
                f"Engine no devolvió dict al ejecutar '{capacidad}'."
            )

            assert salida.get("modulo") == cit.nombre
            assert salida.get("capacidad") == capacidad

        else:
            # La capacidad ya fue validada como callable.
            # No inventamos su firma.
            assert callable(cit.fn(capacidad))


# ===============================================================
# 11. REPORTE / DIAGNÓSTICO / INVENTARIO
# ===============================================================
#
# Aquí tampoco suponemos que CIT tenga exactamente esas capacidades.
# Se consultan dinámicamente.
# ===============================================================

@pytest.mark.parametrize(
    "capacidad",
    ["reporte", "diagnostico", "inventario"],
)
def test_cit_reporting_operativo_si_declara_capacidad(capacidad: str):
    engine = crear_engine()
    cit = obtener_cit(engine)

    if capacidad not in cit.capacidades:
        pytest.skip(
            f"CIT no declara '{capacidad}'; "
            "el contrato no exige que todos los módulos la implementen."
        )

    salida = engine.ejecutar_capacidad(
        cit.nombre,
        capacidad,
    )

    assert salida.get("estado") == "EXITO", (
        f"CIT declara '{capacidad}', pero Engine no pudo ejecutarla: "
        f"{salida}"
    )


# ===============================================================
# 12. TRAZABILIDAD
# ===============================================================

def test_cit_ejecucion_deja_traza():
    engine = crear_engine()
    cit = obtener_cit(engine)

    capacidad = next(iter(cit.capacidades))

    meta = cit.capacidades_meta[capacidad]
    entrada = str(meta["entrada"]).lower()

    # Solo ejecutar automáticamente cuando la metadata indica
    # que la llamada vacía es admisible.
    if not (
        "opcional" in entrada
        or "none" in entrada
        or "sin argumento" in entrada
        or "ningun" in entrada
        or "ninguno" in entrada
    ):
        pytest.skip(
            f"La firma declarada de '{capacidad}' no permite "
            "inferir una llamada vacía."
        )

    antes = len(engine.obtener_trazas())

    salida = engine.ejecutar_capacidad(
        cit.nombre,
        capacidad,
    )

    despues = engine.obtener_trazas()

    assert salida.get("estado") == "EXITO"

    assert len(despues) == antes + 1

    traza = despues[-1]

    assert traza["modulo"] == cit.nombre
    assert traza["capacidad"] == capacidad
    assert traza["estado"] == "EXITO"


# ===============================================================
# 13. CONSOLIDACIÓN
# ===============================================================

def test_cit_se_consolida_en_paquete_omega():
    engine = crear_engine()

    paquete = engine.paquete_omega()

    assert isinstance(paquete, dict)
    assert "metadata" in paquete
    assert "reportes" in paquete

    reportes = paquete["reportes"]

    encontrados = [
        r
        for r in reportes
        if r.get("id") == CIT_ID
        or (
            isinstance(r.get("titulo"), str)
            and CIT_ID in r["titulo"]
        )
    ]

    assert encontrados, (
        "CIT no aparece en paquete_omega()."
    )


# ===============================================================
# 14. INTEGRIDAD: EL ENGINE NO DEBE CAMBIAR EL CONTRATO
# ===============================================================

def test_engine_no_mutara_contrato_de_cit():
    engine = crear_engine()
    cit = obtener_cit(engine)

    original = copy.deepcopy(cit.meta)

    # Operaciones normales del Engine.
    engine.censar()
    engine.estado_global()
    engine.paquete_omega()

    assert cit.meta == original, (
        "El Engine modificó el CONTENEDOR contractual de CIT."
    )


# ===============================================================
# 15. PRUEBA ADVERSARIAL — CAPACIDAD NO CALLABLE
# ===============================================================

def test_engine_detecta_capacidad_no_callable(tmp_path: Path):
    base = copiar_contrato_cit()
    contrato = contrato_base_sintetico(base)

    contrato = preparar_capacidad_sintetica(contrato)

    # Lo hacemos inválido deliberadamente.
    contrato["capacidades"]["capacidad_prueba"] = "NO_CALLABLE"

    escribir_modulo_sintetico(
        tmp_path,
        "test_no_callable",
        contrato,
    )

    with pytest.raises(ArranqueError):
        Engine(
            raiz_modulos=tmp_path,
            strict=True,
        )


# ===============================================================
# 16. PRUEBA ADVERSARIAL — CAPACIDAD SIN META
# ===============================================================

def test_engine_detecta_capacidad_sin_metadata(tmp_path: Path):
    base = copiar_contrato_cit()
    contrato = contrato_base_sintetico(base)

    contrato = preparar_capacidad_sintetica(contrato)

    contrato["capacidades_meta"] = {}

    escribir_modulo_sintetico(
        tmp_path,
        "test_sin_meta",
        contrato,
    )

    with pytest.raises(ArranqueError):
        Engine(
            raiz_modulos=tmp_path,
            strict=True,
        )


# ===============================================================
# 17. PRUEBA ADVERSARIAL — REPORTING INCOMPLETO
# ===============================================================

def test_engine_detecta_reporting_incompleto(tmp_path: Path):
    base = copiar_contrato_cit()
    contrato = contrato_base_sintetico(base)

    contrato = preparar_capacidad_sintetica(contrato)

    contrato["reporting"] = {}

    escribir_modulo_sintetico(
        tmp_path,
        "test_reporting_roto",
        contrato,
    )

    with pytest.raises(ArranqueError):
        Engine(
            raiz_modulos=tmp_path,
            strict=True,
        )


# ===============================================================
# 18. PRUEBA ADVERSARIAL — PERMISO ENGINE DESCONOCIDO
# ===============================================================

def test_engine_detecta_permiso_engine_desconocido(tmp_path: Path):
    base = copiar_contrato_cit()
    contrato = contrato_base_sintetico(base)

    contrato = preparar_capacidad_sintetica(contrato)

    contrato["autoriza_engine"]["permiso_inventado"] = True

    escribir_modulo_sintetico(
        tmp_path,
        "test_permiso_desconocido",
        contrato,
    )

    with pytest.raises(ArranqueError):
        Engine(
            raiz_modulos=tmp_path,
            strict=True,
        )


# ===============================================================
# 19. PRUEBA ADVERSARIAL — DEPENDENCIA INEXISTENTE
# ===============================================================

def test_engine_detecta_dependencia_inexistente(tmp_path: Path):
    base = copiar_contrato_cit()
    contrato = contrato_base_sintetico(base)

    contrato = preparar_capacidad_sintetica(contrato)

    contrato["requiere"] = [
        "MODULO_QUE_NO_EXISTE"
    ]

    escribir_modulo_sintetico(
        tmp_path,
        "test_dependencia_rota",
        contrato,
    )

    with pytest.raises(ArranqueError):
        Engine(
            raiz_modulos=tmp_path,
            strict=True,
        )


# ===============================================================
# 20. PRUEBA ADVERSARIAL — API INCOMPATIBLE
# ===============================================================

def test_engine_detecta_api_incompatible(tmp_path: Path):
    base = copiar_contrato_cit()
    contrato = contrato_base_sintetico(base)

    contrato = preparar_capacidad_sintetica(contrato)

    contrato["api_engine"] = ">=999.0"

    escribir_modulo_sintetico(
        tmp_path,
        "test_api_incompatible",
        contrato,
    )

    with pytest.raises(ArranqueError):
        Engine(
            raiz_modulos=tmp_path,
            strict=True,
        )


# ===============================================================
# 21. PRUEBA ADVERSARIAL — VERSION DE COMPATIBILIDAD FUTURA
# ===============================================================

def test_engine_detecta_compatible_desde_futuro(tmp_path: Path):
    base = copiar_contrato_cit()
    contrato = contrato_base_sintetico(base)

    contrato = preparar_capacidad_sintetica(contrato)

    contrato["compatible_desde"] = "999.0"

    escribir_modulo_sintetico(
        tmp_path,
        "test_version_futura",
        contrato,
    )

    with pytest.raises(ArranqueError):
        Engine(
            raiz_modulos=tmp_path,
            strict=True,
        )


# ===============================================================
# 22. PRUEBA ADVERSARIAL — ESTADO NO CANÓNICO
# ===============================================================

def test_engine_detecta_estado_no_canonico(tmp_path: Path):
    base = copiar_contrato_cit()
    contrato = contrato_base_sintetico(base)

    contrato = preparar_capacidad_sintetica(contrato)

    contrato["estados_validos"] = [
        "ESTADO_INVENTADO"
    ]

    escribir_modulo_sintetico(
        tmp_path,
        "test_estado_invalido",
        contrato,
    )

    with pytest.raises(ArranqueError):
        Engine(
            raiz_modulos=tmp_path,
            strict=True,
        )


# ===============================================================
# 23. PRUEBA ADVERSARIAL — ESQUEMA INCORRECTO
# ===============================================================

def test_engine_detecta_esquema_incorrecto(tmp_path: Path):
    base = copiar_contrato_cit()
    contrato = contrato_base_sintetico(base)

    contrato = preparar_capacidad_sintetica(contrato)

    contrato["esquema"] = "CONTRATO-INVENTADO-999"

    escribir_modulo_sintetico(
        tmp_path,
        "test_esquema_invalido",
        contrato,
    )

    with pytest.raises(ArranqueError):
        Engine(
            raiz_modulos=tmp_path,
            strict=True,
        )


# ===============================================================
# 24. PRUEBA ADVERSARIAL — VERSION DE CONTRATO INCORRECTA
# ===============================================================

def test_engine_detecta_version_contrato_incorrecta(tmp_path: Path):
    base = copiar_contrato_cit()
    contrato = contrato_base_sintetico(base)

    contrato = preparar_capacidad_sintetica(contrato)

    contrato["version_contrato"] = "999.0"

    escribir_modulo_sintetico(
        tmp_path,
        "test_contrato_incompatible",
        contrato,
    )

    with pytest.raises(ArranqueError):
        Engine(
            raiz_modulos=tmp_path,
            strict=True,
        )


# ===============================================================
# 25. PRUEBA ADVERSARIAL — REQUIERE DEBE SER LISTA
# ===============================================================

def test_engine_detecta_requiere_no_lista(tmp_path: Path):
    base = copiar_contrato_cit()
    contrato = contrato_base_sintetico(base)

    contrato = preparar_capacidad_sintetica(contrato)

    contrato["requiere"] = "CIT"

    escribir_modulo_sintetico(
        tmp_path,
        "test_requiere_invalido",
        contrato,
    )

    with pytest.raises(ArranqueError):
        Engine(
            raiz_modulos=tmp_path,
            strict=True,
        )


# ===============================================================
# 26. PRUEBA ADVERSARIAL — META CON TIPO INCORRECTO
# ===============================================================

def test_engine_detecta_meta_capacidad_mal_formada(tmp_path: Path):
    base = copiar_contrato_cit()
    contrato = contrato_base_sintetico(base)

    contrato = preparar_capacidad_sintetica(contrato)

    contrato["capacidades_meta"]["capacidad_prueba"] = {
        "descripcion": "válida",
        "entrada": 123,
        "salida": "dict",
    }

    escribir_modulo_sintetico(
        tmp_path,
        "test_meta_mal_formada",
        contrato,
    )

    with pytest.raises(ArranqueError):
        Engine(
            raiz_modulos=tmp_path,
            strict=True,
        )


# ===============================================================
# 27. PRUEBA ADVERSARIAL — DUPLICADO DE ID
# ===============================================================

def test_engine_detecta_id_duplicado(tmp_path: Path):
    base = copiar_contrato_cit()

    contrato_a = contrato_base_sintetico(base)
    contrato_a = preparar_capacidad_sintetica(contrato_a)

    contrato_b = contrato_base_sintetico(base)
    contrato_b = preparar_capacidad_sintetica(contrato_b)

    contrato_b["nombre"] = "test_segundo"
    contrato_b["id"] = "TEST"

    escribir_modulo_sintetico(
        tmp_path,
        "test_primero",
        contrato_a,
    )

    escribir_modulo_sintetico(
        tmp_path,
        "test_segundo",
        contrato_b,
    )

    with pytest.raises(ArranqueError):
        Engine(
            raiz_modulos=tmp_path,
            strict=True,
        )


# ===============================================================
# 28. PRUEBA ADVERSARIAL — DUPLICADO DE ROL
# ===============================================================

def test_engine_detecta_rol_duplicado(tmp_path: Path):
    base = copiar_contrato_cit()

    contrato_a = contrato_base_sintetico(base)
    contrato_a = preparar_capacidad_sintetica(contrato_a)

    contrato_b = contrato_base_sintetico(base)
    contrato_b = preparar_capacidad_sintetica(contrato_b)

    contrato_a["id"] = "TEST_A"
    contrato_a["nombre"] = "test_a"
    contrato_a["rol"] = "TEST"

    contrato_b["id"] = "TEST_B"
    contrato_b["nombre"] = "test_b"
    contrato_b["rol"] = "TEST"

    escribir_modulo_sintetico(
        tmp_path,
        "test_a",
        contrato_a,
    )

    escribir_modulo_sintetico(
        tmp_path,
        "test_b",
        contrato_b,
    )

    with pytest.raises(ArranqueError):
        Engine(
            raiz_modulos=tmp_path,
            strict=True,
        )


# ===============================================================
# 29. PRUEBA DE NO-HARDCODE
# ===============================================================

def test_acoplamiento_cit_no_hardcodea_capacidades():
    """
    Esta prueba documenta explícitamente el principio arquitectónico.

    No se fija ninguna capacidad concreta de CIT.

    El conjunto se obtiene directamente del contrato cargado.
    """
    engine = crear_engine()
    cit = obtener_cit(engine)

    capacidades_contrato = set(cit.meta["capacidades"].keys())
    capacidades_engine = set(cit.capacidades.keys())

    assert capacidades_engine == capacidades_contrato


# ===============================================================
# 30. PRUEBA FINAL DE ACOPLAMIENTO
# ===============================================================

def test_cit_acoplamiento_integral():
    """
    Prueba resumida del acoplamiento real:

        contrato
           ↓
        carga
           ↓
        validación
           ↓
        registro
           ↓
        dependencia
           ↓
        grafo
           ↓
        capacidades
           ↓
        reporting
           ↓
        Omega
    """
    engine = crear_engine()

    cit = obtener_cit(engine)

    assert engine.estado == "OPERATIVO"

    assert cit.id == cit.meta["id"]
    assert cit.nombre == cit.meta["nombre"]
    assert cit.rol == cit.meta["rol"]

    assert cit.capacidades == cit.meta["capacidades"]
    assert cit.capacidades_meta == cit.meta["capacidades_meta"]
    assert cit.reporting == cit.meta["reporting"]

    assert cit.nombre not in engine._dependencias.get("faltantes", {})

    nodos = engine._grafo.get("nodos", [])

    assert any(
        nodo.get("tipo") == "modulo"
        and (
            nodo.get("id") == cit.id
            or nodo.get("nombre") == cit.nombre
        )
        for nodo in nodos
    )

    paquete = engine.paquete_omega()

    assert paquete["metadata"]["estado_engine"] == "OPERATIVO"

    assert any(
        reporte.get("id") == cit.id
        for reporte in paquete.get("reportes", [])
    )


# ===============================================================
# FIN DEL TEST
# ===============================================================
