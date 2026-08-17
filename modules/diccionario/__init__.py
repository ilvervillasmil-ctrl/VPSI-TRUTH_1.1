# ===============================================================
# VPSI-TRUTH — modules/diccionario/__init__.py
# ===============================================================
#
# MÓDULO:              diccionario
# ID:                  DI
# Rol:                 DI
# Versión módulo:      1.0
# Versión contrato:    1.0
# Esquema contrato:    VPSI-CONTRACT-1.0
# Estabilidad:         ESTABLE
# Compatible desde:    1.0
# API Engine:          >=1.0
#
# Función:
#   Biblioteca de definiciones (materia prima léxica).
#   Herramienta para contrastar y correlacionar a nivel de significado.
#
# Qué hace:
#   - Auto-carga todos los archivos que declaren DICCIONARIO
#   - Expone definiciones y significados por palabra, idioma o fuente
#   - Entrega materia prima léxica a Engine y otros módulos
#   - Expone inventario, reporte, diagnóstico
#
# Responsabilidad:
#   Ser la fuente de definiciones del sistema.
#
# Autoridad:
#   - Exponer definiciones y significados
#   - Auto-cargar todos los archivos que declaren DICCIONARIO
#   - Entregar materia prima léxica a Engine y otros módulos
#   - Reportar el estado estructural del módulo.
#
# Conocimiento exportable:
#   - inventario
#   - reporte
#   - diagnostico
#   - listar, cargar, cargar_todos
#   - definir, significado, palabras
#   - inyectar_en_peticion
#   - verificar, barrer
#
# Relación con Engine:
#   Engine descubre este CONTENEDOR, ejecuta únicamente las
#   capacidades declaradas, puede inspeccionar todos los archivos
#   del módulo y consolida el reporte producido por este.
#
# Relación con Omega:
#   Omega no calcula información de este módulo.
#   Solo presenta los resultados entregados por Engine.
#
# Observaciones:
#   Todo archivo *.py del directorio o fuentes/ que declare DICCIONARIO
#   se carga automáticamente. No hace falta editar el init.
#
# NOTAS DE ARQUITECTURA (leer antes de editar):
#   1. El CONTENEDOR es la ÚNICA interfaz pública del módulo.
#   2. Engine solo lee CONTENEDOR; no lee constantes sueltas del código.
#   3. Toda capacidad en "capacidades" DEBE tener entrada 1:1 en
#      "capacidades_meta" con descripcion, entrada y salida (str).
#   4. "requiere" y "no_hace" son claves OBLIGATORIAS del esquema
#      (pueden ser listas vacías []).
#   5. El módulo no importa ni invoca otros módulos de dominio.
#      Si necesita algo, lo declara en "requiere"; Engine resuelve.
#   6. El contrato es positivo: describe qué ES y qué GARANTIZA.
#      "no_hace" existe por esquema; usar límites de oficio, no nombres
#      de otros módulos.
#   7. Al agregar capacidad nueva: capacidades + capacidades_meta +
#      _CAP_MAP + VERSION_MODULO.
#   8. Tras _resolver_capacidades, CONTENEDOR se considera inmutable.
#
# ===============================================================

# ===============================================================
# IMPORTACIONES
# ===============================================================

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, 
# --- Importación exacta desde la ubicación real del módulo ---
from modules.diagnosticoD import (
    DiagnosticoGlobal,
    DiagnosticoError,
    PESOS,
    barrer_diagnostico,
)


# ===============================================================
# FIN IMPORTACIONES
# ===============================================================

# ===============================================================
# PARTE 1 — PRINCIPIOS, BANDERAS Y ESPECIFICACIONES PRECISAS
# ===============================================================

# ===============================================================
# 1.1 — IDENTIDAD
# ===============================================================

ID_MODULO = "DI"
NOMBRE_MODULO = "diccionario"
ROL_MODULO = "DI"

# ===============================================================
# FIN 1.1
# ===============================================================


# ===============================================================
# 1.2 — VERSIONES Y ESTABILIDAD
# ===============================================================

VERSION_MODULO = "1.0"
VERSION_CONTRATO = "1.0"
ESQUEMA_CONTRATO = "VPSI-CONTRACT-1.0"
COMPATIBLE_DESDE = "1.0"
API_ENGINE = ">=1.0"
ESTABILIDAD = "ESTABLE"

# ===============================================================
# FIN 1.2
# ===============================================================


# ===============================================================
# 1.3 — BANDERAS DE ESTADO
# ===============================================================

ESTADO_NO_INICIADO = "NO_INICIADO"
ESTADO_OPERATIVO = "OPERATIVO"
ESTADO_DEGRADADO = "DEGRADADO"
ESTADO_RECHAZADO = "RECHAZADO"
ESTADOS_VALIDOS = (
    ESTADO_NO_INICIADO,
    ESTADO_OPERATIVO,
    ESTADO_DEGRADADO,
    ESTADO_RECHAZADO,
)

# ===============================================================
# FIN 1.3
# ===============================================================


# ===============================================================
# 1.4 — INVARIANTES
# ===============================================================

INVARIANTES = (
    "el id del módulo nunca cambia",
    "el rol nunca cambia",
    "DI es una herramienta de definiciones, no calcula Tru",
    "DI no clasifica O_context (eso es CX)",
    "DI auto-carga todo lo que está debajo del módulo",
    "las capacidades declaradas son siempre callables tras la resolución",
    "este módulo no modifica el estado de otros módulos",
    "este módulo no inventa capacidades no declaradas en CONTENEDOR",
    "este módulo siempre puede reportar su propio estado",
)

# ===============================================================
# FIN 1.4
# ===============================================================


# ===============================================================
# 1.5 — CONFIGURACIÓN
# ===============================================================

_DIR = Path(__file__).parent
_FUENTES = _DIR / "fuentes"

# ===============================================================
# FIN 1.5
# ===============================================================

# ===============================================================
# FIN PARTE 1
# ===============================================================


# ===============================================================
# PARTE 4 — DEFINICIONES
# ===============================================================

# ===============================================================
# 4.1 — EXCEPCIONES
# ===============================================================

class ContratoInvalido(Exception):
    """El CONTENEDOR no cumple el esquema o la resolución falló."""
    pass

# ===============================================================
# FIN 4.1
# ===============================================================

# ===============================================================
# FIN PARTE 4
# ===============================================================

# ===============================================================
# ESTADO INTERNO
# ===============================================================

_REGISTRO: Dict[str, Any] = {}
_META: Dict[str, Dict[str, Any]] = {}
_CARGADO = False

# ===============================================================
# FIN ESTADO INTERNO
# ===============================================================

# ===============================================================
# PARTE 5 — CONTRATO OFICIAL (CONTENEDOR)
# ===============================================================

CONTENEDOR: Dict[str, Any] = {

    # ============================================================
    # 5.1 — ESQUEMA
    # ============================================================
    "esquema": ESQUEMA_CONTRATO,
    "version_contrato": VERSION_CONTRATO,
    "version_modulo": VERSION_MODULO,
    "estabilidad": ESTABILIDAD,
    "compatible_desde": COMPATIBLE_DESDE,
    "api_engine": API_ENGINE,

    # ============================================================
    # 5.2 — IDENTIDAD
    # ============================================================
    "id": ID_MODULO,
    "nombre": NOMBRE_MODULO,
    "rol": ROL_MODULO,
    "descripcion": (
        "Biblioteca de definiciones. Rol DI. "
        "Materia prima léxica: palabra → definición → significado. "
        "Herramienta para contrastar y correlacionar a nivel de significado. "
        "Auto-carga todos los archivos debajo del módulo. "
        "Engine puede solicitar y distribuir definiciones según contexto. "
        "No calcula Tru. No clasifica O. No trae dominios externos."
    ),

    # ============================================================
    # 5.3 — PROPÓSITO
    # ============================================================
    "funcion": (
        "Biblioteca de definiciones para contrastar y correlacionar a nivel "
        "léxico-significado. Materia prima: palabra → definición → significado. "
        "Auto-carga todo lo que está debajo del módulo."
    ),
    "no_hace": [
        "No calcula C, L, K, Tru_Ri ni Tru_total",
        "No clasifica O_context (eso es CX)",
        "No trae material externo de dominios (eso es RE)",
        "No orquesta el ciclo (eso es Engine)",
        "No sustituye AX, MC, CA, FO, CIT",
    ],

    # ============================================================
    # 5.4 — AUTORIDAD
    # ============================================================
    "autoridad": [
        "Exponer definiciones y significados",
        "Auto-cargar todos los archivos que declaren DICCIONARIO",
        "Entregar materia prima léxica a Engine y otros módulos",
        "Reportar estado, inventario y diagnóstico propios",
    ],

    # ============================================================
    # 5.5 — CONOCIMIENTO EXPORTABLE
    # ============================================================
    "conocimiento_exportable": [
        "inventario",
        "reporte",
        "diagnostico",
        "listar",
        "cargar",
        "cargar_todos",
        "definir",
        "significado",
        "palabras",
        "inyectar_en_peticion",
        "verificar",
        "barrer",
        "resolver",
        "axiomas",
        "ejecutar_total",
        "inspeccionar",
        "registrar_inventario",
    ],

    # ============================================================
    # 5.6 — ACCESO
    # ============================================================
    "acceso": {
        "nivel": "completo",
        "descripcion": "Acceso total a recursos del módulo",
    },

    # ============================================================
    # 5.7 — DEPENDENCIAS
    # ============================================================
    "requiere": [
        "CT", "AX", "FO", "MC", "SF", "CA", "CX",
        "RE", "VX", "TX", "CH", "CIT", "TT",
        "CE", "CC",
    ],

    # ============================================================
    # 5.8 — ACCESO A ARCHIVOS
    # ============================================================
    "acceso_archivos": ["*"],

    # ============================================================
    # 5.9 — VALIDAR ESQUEMA
    # ============================================================
    "validar_esquema": ["*"],

    # ============================================================
    # 5.10 — AUTORIZACIÓN AL ENGINE
    # ============================================================
    "autoriza_engine": {
        # --- PERMISOS BASE ---
        "leer": True,
        "ejecutar": True,
        "consultar": True,
        "recombinar": True,
        "reportar": True,
        "auditar": True,
        "inventariar": True,

        # --- PERMISOS DE ESCRITURA ---
        "alterar": False,
        "crear": True,
        "actualizar": False,

        # --- PERMISOS DE PROCESAMIENTO ---
        "validar": True,
        "procesar": True,
        "analizar": True,
        "generar": True,

        # --- PERMISOS DE DATOS ---
        "exportar": True,
        "importar": True,
        "respaldar": True,
        "recuperar": True,
        "sincronizar": True,

        # --- PERMISOS DE MONITOREO ---
        "monitorear": True,
        "metricas": True,
        "diagnostico": True,

        # --- PERMISOS DE ESTADO ---
        "estado": True,
        "version": True,
        "salud": True,
        "inventario": True,
        "capacidades": True,
        "errores": True,
        "advertencias": True,
        "dependencias": True,
        "contrato": True,
        "conocimiento": True,
        "reporte": True,

        # --- PERMISOS AGREGADOS (OBLIGATORIOS) ---
        "validar_esquema": True,
        "acceso_archivos": True,

        # --- BANDERAS NUEVAS (OBLIGATORIAS ENGINE) ---
        "ejecutar_total": True,
        "inspeccionar": True,
        "registrar_inventario": True,
    },
    

        # ============================================================
    # 5.11 — CONSULTAS SOPORTADAS
    # ============================================================
    "consultas_soportadas": [
        # --- CONSULTAS LÉXICAS ---
        "listar",
        "cargar",
        "cargar_todos",
        "definir",
        "significado",
        "palabras",
        "inyectar_en_peticion",

        # --- CONSULTAS DE ESTADO ---
        "inventario",
        "reporte",
        "diagnostico",
        "verificar",
        "barrer",

        # --- CONSULTAS DE RESOLUCIÓN ---
        "resolver",
        "axiomas",

        # --- CONSULTAS ARQUITECTÓNICAS (OBLIGATORIAS ENGINE) ---
        "ejecutar_total",
        "inspeccionar",
        "registrar_inventario",
    ],

    # ============================================================
    # 5.12 — CAPACIDADES
    # ============================================================
    "capacidades": {
        # --- CENTINELA ---
        "verificar": "verificar",
        "barrer": "barrer",
        "verificar_salida": "verificar_salida",

        # --- INVENTARIO Y REPORTING ---
        "inventario": "inventario",
        "reporte": "reporte",
        "diagnostico": "diagnostico",

        # --- CONOCIMIENTO ---
        "axiomas": "axiomas",
        "resolver": "resolver",

        # --- OPERACIONES LÉXICAS ---
        "listar": "listar",
        "cargar": "cargar",
        "cargar_todos": "cargar_todos",
        "definir": "definir",
        "significado": "significado",
        "palabras": "palabras",
        "inyectar_en_peticion": "inyectar_en_peticion",

        # --- CAPACIDADES ARQUITECTÓNICAS (OBLIGATORIAS ENGINE) ---
        "ejecutar_total": "ejecutar_total",
        "inspeccionar": "inspeccionar",
        "registrar_inventario": "registrar_inventario",
    },
    
    # ============================================================
    # 6 — METADATOS DE CAPACIDADES (1:1 OBLIGATORIO)
    # ============================================================
    "capacidades_meta": {

        # ============================================================
        # 6.1 — VERIFICAR
        # ============================================================
        "verificar": {
            "descripcion": (
                "Alias de barrer. Verifica coherencia del diccionario."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con coherente, errores, diccionarios, total"
            ),
            "acceso_archivos": ["*"],
        },

        # ============================================================
        # 6.2 — BARRER
        # ============================================================
        "barrer": {
            "descripcion": (
                "Centinela de DI: valida forma de las fuentes, "
                "reporta errores de carga. No calcula Tru."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con coherente, errores, diccionarios, "
                "total, por_idioma"
            ),
            "acceso_archivos": ["*"],
        },

        # ============================================================
        # 6.3 — INVENTARIO
        # ============================================================
        "inventario": {
            "descripcion": (
                "Inventario de diccionarios descubiertos."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con id, version, total, diccionarios, por_idioma"
            ),
            "acceso_archivos": ["*"],
        },

        # ============================================================
        # 6.4 — REPORTE
        # ============================================================
        "reporte": {
            "descripcion": (
                "Reporte interno de estado del módulo DI."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con id, estado, coherente, diccionarios, capacidades"
            ),
            "acceso_archivos": ["*"],
        },

        # ============================================================
        # 6.5 — DIAGNÓSTICO
        # ============================================================
        "diagnostico": {
            "descripcion": (
                "Diagnóstico del módulo DI."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con id, estado, problemas, advertencias, "
                "recomendaciones"
            ),
            "acceso_archivos": ["*"],
        },

        # ============================================================
        # 6.6 — AXIOMAS
        # ============================================================
        "axiomas": {
            "descripcion": (
                "Declaraciones axiomáticas del módulo DI."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "list[dict] de declaraciones",
            "acceso_archivos": ["*"],
        },

        # ============================================================
        # 6.7 — RESOLVER
        # ============================================================
        "resolver": {
            "descripcion": (
                "Entrega definiciones según palabra, idioma o fuente."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con definiciones o materia prima"
            ),
            "acceso_archivos": ["*"],
        },

        # ============================================================
        # 6.8 — LISTAR
        # ============================================================
        "listar": {
            "descripcion": (
                "Nombres de todos los diccionarios descubiertos."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "list[str]",
            "acceso_archivos": ["*"],
        },

        # ============================================================
        # 6.9 — CARGAR
        # ============================================================
        "cargar": {
            "descripcion": (
                "Carga un diccionario por nombre."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con el DICCIONARIO",
            "acceso_archivos": ["*"],
        },

        # ============================================================
        # 6.10 — CARGAR TODOS
        # ============================================================
        "cargar_todos": {
            "descripcion": (
                "Carga todos los diccionarios descubiertos."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict nombre → datos",
            "acceso_archivos": ["*"],
        },

        # ============================================================
        # 6.11 — DEFINIR
        # ============================================================
        "definir": {
            "descripcion": (
                "Busca definición de una palabra en fuentes."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con definicion, significado, fuente o None"
            ),
            "acceso_archivos": ["*"],
        },

        # ============================================================
        # 6.12 — SIGNIFICADO
        # ============================================================
        "significado": {
            "descripcion": (
                "Atajo para obtener significado/definición de una palabra."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "str o None",
            "acceso_archivos": ["*"],
        },

        # ============================================================
        # 6.13 — PALABRAS
        # ============================================================
        "palabras": {
            "descripcion": (
                "Conjunto de lemas de las fuentes indicadas."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "set[str]",
            "acceso_archivos": ["*"],
        },

        # ============================================================
        # 6.14 — INYECTAR EN PETICIÓN
        # ============================================================
        "inyectar_en_peticion": {
            "descripcion": (
                "Entrega lemas a una petición para el ciclo."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "peticion con lemas inyectados",
            "acceso_archivos": ["*"],
        },

        # ============================================================
        # 6.15 — VERIFICAR SALIDA
        # ============================================================
        "verificar_salida": {
            "descripcion": (
                "Comprueba forma mínima de una salida de DI."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "bool",
            "acceso_archivos": ["*"],
        },

        # ============================================================
        # 6.16 — EJECUTAR TOTAL
        # ============================================================
        "ejecutar_total": {
            "descripcion": (
                "Autoridad total de ENGINE sobre DI. "
                "Ejerce TODAS las unidades operativamente ejecutables "
                "del módulo conforme a su contrato e inventario. "
                "Todo es callable real. No inventa capacidades."
            ),
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["*"],
            "salida": "dict con resultados de todas las unidades ejecutadas",
            "acceso_archivos": ["*"],
        },

        # ============================================================
        # 6.17 — INSPECCIONAR
        # ============================================================
        "inspeccionar": {
            "descripcion": (
                "Capacidad meta de inspeccion estructural de DI. "
                "Expone constantes, capacidades, diccionarios y estado "
                "sin alterar el contrato ni calcular."
            ),
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["acceso_archivos"],
            "salida": "dict con estructura, capacidades y estado del modulo",
            "acceso_archivos": ["acceso_archivos"],
        },

        # ============================================================
        # 6.18 — REGISTRAR INVENTARIO
        # ============================================================
        "registrar_inventario": {
            "descripcion": (
                "Registra el inventario estructural de DI "
                "como instantanea determinista. No altera evidencia."
            ),
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["acceso_archivos"],
            "salida": "dict con inventario registrado",
            "acceso_archivos": ["acceso_archivos"],
        },
    },
    
    # ============================================================
    # REPORTING (OBLIGATORIO EN EL ESQUEMA)
    # ============================================================
    "reporting": {
        # --- BANDERAS DE ESTADO Y SALUD ---
        "estado": True,
        "salud": True,

        # --- BANDERAS DE INVENTARIO Y CAPACIDADES ---
        "inventario": True,
        "capacidades": True,

        # --- BANDERAS DE ERRORES Y ADVERTENCIAS ---
        "errores": True,
        "advertencias": True,

        # --- BANDERAS DE DEPENDENCIAS Y VERSION ---
        "dependencias": True,
        "version": True,

        # --- BANDERAS DE CONTRATO Y CONOCIMIENTO ---
        "contrato": True,
        "conocimiento": True,

        # --- BANDERAS DE METRICAS Y DIAGNOSTICO ---
        "metricas": True,
        "diagnostico": True,

        # --- BANDERA DE REPORTE ---
        "reporte": True,

                # --- BANDERAS OBLIGATORIAS SEGÚN ENGINE ---
        "acceso_archivos": True,
        "validar_esquema": True,

        # --- BANDERAS NUEVAS (OBLIGATORIAS ENGINE) ---
        "ejecutar_total": True,
        "inspeccionar": True,
        "registrar_inventario": True,
    },

    # ============================================================
    # ESTADOS VÁLIDOS
    # ============================================================
    "estados_validos": list(ESTADOS_VALIDOS),

    # ============================================================
    # INVARIANTES
    # ============================================================
    "invariantes": list(INVARIANTES),

}  # <--- CIERRE FINAL

# ===============================================================
# FIN CONTRATO
# ===============================================================

# ===============================================================
# PARTE 7 — FUNCIONES PRIVADAS
# ===============================================================

# ===============================================================
# 7.1 — NORMALIZACIÓN
# ===============================================================

def _norm_nombre(nombre: str) -> str:
    return (nombre or "").strip().lower().replace("-", "_").replace(" ", "_")


def _norm_palabra(p: str) -> str:
    return (p or "").strip().lower()

# ===============================================================
# FIN 7.1
# ===============================================================


# ===============================================================
# 7.2 — EXTRACCIÓN LÉXICA
# ===============================================================

def _extraer_definicion(entrada: Any) -> Optional[str]:
    if entrada is None:
        return None
    if isinstance(entrada, str):
        return entrada.strip() or None
    if isinstance(entrada, dict):
        for k in ("definicion", "definición", "def", "meaning", "significado"):
            v = entrada.get(k)
            if v is not None and str(v).strip():
                return str(v).strip()
    return None


def _extraer_significado(entrada: Any) -> Optional[str]:
    if not isinstance(entrada, dict):
        return _extraer_definicion(entrada)
    for k in ("significado", "meaning", "interpretacion", "interpretación"):
        v = entrada.get(k)
        if v is not None and str(v).strip():
            return str(v).strip()
    return _extraer_definicion(entrada)

# ===============================================================
# FIN 7.2
# ===============================================================


# ===============================================================
# 7.3 — CARGA DE MÓDULO
# ===============================================================

def _cargar_modulo(path: Path, clave: str) -> Optional[Any]:
    spec = importlib.util.spec_from_file_location(clave, path)
    if spec is None or spec.loader is None:
        return None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[clave] = mod
    try:
        spec.loader.exec_module(mod)
    except Exception:
        return None
    return mod

# ===============================================================
# FIN 7.3
# ===============================================================


# ===============================================================
# 7.4 — DESCUBRIMIENTO
# ===============================================================

def _descubrir() -> None:
    global _CARGADO
    if _CARGADO:
        return

    candidatos: List[Path] = []
    if _FUENTES.is_dir():
        candidatos.extend(sorted(_FUENTES.glob("*.py")))
    candidatos.extend(sorted(_DIR.glob("*.py")))

    vistos: Set[Path] = set()
    for f in candidatos:
        if f.name == "__init__.py" or f.name.startswith("_"):
            continue
        resolved = f.resolve()
        if resolved in vistos:
            continue
        vistos.add(resolved)

        clave = "diccionario_{0}".format(f.stem)
        mod = _cargar_modulo(f, clave)
        if mod is None:
            _META[f.stem] = {"error": "carga fallida", "archivo": f.name}
            continue

        datos = getattr(mod, "DICCIONARIO", None)
        if datos is None:
            continue

        meta = getattr(mod, "META", None)
        nombre = None
        if isinstance(meta, dict):
            nombre = meta.get("nombre")
        if not nombre:
            nombre = f.stem
        key = _norm_nombre(str(nombre))

        _REGISTRO[key] = datos
        if isinstance(meta, dict):
            _META[key] = dict(meta)
            _META[key]["archivo"] = f.name
        else:
            _META[key] = {"nombre": key, "archivo": f.name}

    _CARGADO = True


def _asegurar() -> None:
    _descubrir()

# ===============================================================
# FIN 7.4
# ===============================================================


# ===============================================================
# 7.5 — VALIDACIÓN DE CONTRATO
# ===============================================================

def _validar_contrato(cont: Dict[str, Any]) -> None:
    obligatorias = (
        "esquema", "version_contrato", "version_modulo",
        "id", "nombre", "rol", "descripcion",
        "funcion", "no_hace", "autoridad",
        "conocimiento_exportable", "requiere",
        "autoriza_engine", "consultas_soportadas",
        "capacidades", "capacidades_meta",
        "reporting", "estados_validos", "invariantes",
        "estabilidad", "compatible_desde", "api_engine",
    )
    faltantes = [k for k in obligatorias if k not in cont]
    if faltantes:
        raise ContratoInvalido(
            "{0}: CONTENEDOR incompleto. Faltan: {1}".format(
                NOMBRE_MODULO, faltantes
            )
        )
    if cont.get("esquema") != ESQUEMA_CONTRATO:
        raise ContratoInvalido(
            "{0}: esquema incompatible: {1}".format(
                NOMBRE_MODULO, cont.get("esquema")
            )
        )
    if str(cont.get("version_contrato")) != VERSION_CONTRATO:
        raise ContratoInvalido(
            "{0}: version_contrato inválida: {1}".format(
                NOMBRE_MODULO, cont.get("version_contrato")
            )
        )
    meta_caps = cont.get("capacidades_meta") or {}
    for nombre_cap in cont.get("capacidades") or {}:
        if nombre_cap not in meta_caps:
            raise ContratoInvalido(
                "{0}: capacidad '{1}' sin capacidades_meta".format(
                    NOMBRE_MODULO, nombre_cap
                )
            )
        entrada = meta_caps[nombre_cap]
        if not isinstance(entrada, dict):
            raise ContratoInvalido(
                "{0}: capacidades_meta['{1}'] debe ser dict".format(
                    NOMBRE_MODULO, nombre_cap
                )
            )
        for campo in ("descripcion", "entrada", "salida"):
            if campo not in entrada or not isinstance(entrada[campo], str):
                raise ContratoInvalido(
                    "{0}: capacidades_meta['{1}'] requiere '{2}: str'".format(
                        NOMBRE_MODULO, nombre_cap, campo
                    )
                )

# ===============================================================
# FIN 7.5
# ===============================================================


# ===============================================================
# 7.6 — RESOLUCIÓN DE CAPACIDAD INDIVIDUAL
# ===============================================================

def _resolver_capacidad(
    nombre: str,
    referencia: Any,
) -> Callable[..., Any]:
    """
    Resuelve una capacidad contractual hasta una función callable real.
    No crea funciones ni sustituye referencias inexistentes.
    """
    if callable(referencia):
        return referencia

    if isinstance(referencia, str):
        funcion = globals().get(referencia)
        if callable(funcion):
            return funcion

    raise ContratoInvalido(
        f"{NOMBRE_MODULO}: capacidad '{nombre}' "
        "no resuelve a una función callable real"
    )

# ===============================================================
# FIN 7.6
# ===============================================================


# ===============================================================
# 7.7 — EJECUCIÓN DE CAPACIDAD INDIVIDUAL
# ===============================================================

def _ejecutar_capacidad(
    nombre: str,
    referencia: Any,
    peticion: Any,
) -> Any:
    """
    Ejecuta una capacidad contractual real según su firma.
    No inventa argumentos.
    """
    funcion = _resolver_capacidad(
        nombre=nombre,
        referencia=referencia,
    )

    firma = inspect.signature(funcion)
    parametros = list(firma.parameters.values())

    obligatorios = [
        parametro
        for parametro in parametros
        if parametro.kind in (
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
        )
        and parametro.default is inspect.Parameter.empty
    ]

    if not obligatorios:
        return funcion()

    if len(obligatorios) == 1 and len(parametros) == 1:
        return funcion(peticion)

    raise ContratoInvalido(
        f"{NOMBRE_MODULO}: capacidad '{nombre}' "
        "no posee una firma compatible con la interfaz contractual"
    )

# ===============================================================
# FIN 7.7
# ===============================================================

# ===============================================================
# FIN PARTE 7
# ===============================================================

# ===============================================================
# 8 — FUNCIONES PRIVADAS
# ===============================================================

# ===============================================================
# 8.1 — NORMALIZACIÓN
# ===============================================================

def _norm_nombre(nombre: str) -> str:
    return (nombre or "").strip().lower().replace("-", "_").replace(" ", "_")


def _norm_palabra(p: str) -> str:
    return (p or "").strip().lower()

# ===============================================================
# FIN 8.1
# ===============================================================


# ===============================================================
# 8.2 — EXTRACCIÓN LÉXICA
# ===============================================================

def _extraer_definicion(entrada: Any) -> Optional[str]:
    if entrada is None:
        return None
    if isinstance(entrada, str):
        return entrada.strip() or None
    if isinstance(entrada, dict):
        for k in ("definicion", "definición", "def", "meaning", "significado"):
            v = entrada.get(k)
            if v is not None and str(v).strip():
                return str(v).strip()
    return None


def _extraer_significado(entrada: Any) -> Optional[str]:
    if not isinstance(entrada, dict):
        return _extraer_definicion(entrada)
    for k in ("significado", "meaning", "interpretacion", "interpretación"):
        v = entrada.get(k)
        if v is not None and str(v).strip():
            return str(v).strip()
    return _extraer_definicion(entrada)

# ===============================================================
# FIN 8.2
# ===============================================================


# ===============================================================
# 8.3 — CARGA DE MÓDULO
# ===============================================================

def _cargar_modulo(path: Path, clave: str) -> Optional[Any]:
    spec = importlib.util.spec_from_file_location(clave, path)
    if spec is None or spec.loader is None:
        return None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[clave] = mod
    try:
        spec.loader.exec_module(mod)
    except Exception:
        return None
    return mod

# ===============================================================
# FIN 8.3
# ===============================================================


# ===============================================================
# 8.4 — DESCUBRIMIENTO
# ===============================================================

def _descubrir() -> None:
    global _CARGADO
    if _CARGADO:
        return

    candidatos: List[Path] = []
    if _FUENTES.is_dir():
        candidatos.extend(sorted(_FUENTES.glob("*.py")))
    candidatos.extend(sorted(_DIR.glob("*.py")))

    vistos: Set[Path] = set()
    for f in candidatos:
        if f.name == "__init__.py" or f.name.startswith("_"):
            continue
        resolved = f.resolve()
        if resolved in vistos:
            continue
        vistos.add(resolved)

        clave = "diccionario_{0}".format(f.stem)
        mod = _cargar_modulo(f, clave)
        if mod is None:
            _META[f.stem] = {"error": "carga fallida", "archivo": f.name}
            continue

        datos = getattr(mod, "DICCIONARIO", None)
        if datos is None:
            continue

        meta = getattr(mod, "META", None)
        nombre = None
        if isinstance(meta, dict):
            nombre = meta.get("nombre")
        if not nombre:
            nombre = f.stem
        key = _norm_nombre(str(nombre))

        _REGISTRO[key] = datos
        if isinstance(meta, dict):
            _META[key] = dict(meta)
            _META[key]["archivo"] = f.name
        else:
            _META[key] = {"nombre": key, "archivo": f.name}

    _CARGADO = True


def _asegurar() -> None:
    _descubrir()

# ===============================================================
# FIN 8.4
# ===============================================================

# ===============================================================
# FIN 8 — FUNCIONES PRIVADAS
# ===============================================================

# ===============================================================
# 9 — CAPACIDADES PÚBLICAS
# ===============================================================

# ===============================================================
# 9.1 — LISTAR
# ===============================================================

def listar() -> List[str]:
    _asegurar()
    return sorted(_REGISTRO.keys())

# ===============================================================
# FIN 9.1
# ===============================================================


# ===============================================================
# 9.2 — LISTAR POR IDIOMA
# ===============================================================

def listar_por_idioma(idioma: str) -> List[str]:
    _asegurar()
    idioma = (idioma or "").strip().lower()
    out = []
    for k, m in _META.items():
        if k in _REGISTRO and str(m.get("idioma", "")).lower() == idioma:
            out.append(k)
    return sorted(out)

# ===============================================================
# FIN 9.2
# ===============================================================


# ===============================================================
# 9.3 — META
# ===============================================================

def meta(nombre: str) -> Optional[Dict[str, Any]]:
    _asegurar()
    return _META.get(_norm_nombre(nombre))

# ===============================================================
# FIN 9.3
# ===============================================================


# ===============================================================
# 9.4 — CARGAR
# ===============================================================

def cargar(nombre: str) -> Any:
    _asegurar()
    key = _norm_nombre(nombre)
    if key not in _REGISTRO:
        raise KeyError(
            "diccionario no encontrado: {0!r}. Disponibles: {1}".format(
                nombre, listar()
            )
        )
    return _REGISTRO[key]

# ===============================================================
# FIN 9.4
# ===============================================================


# ===============================================================
# 9.5 — CARGAR TODOS
# ===============================================================

def cargar_todos() -> Dict[str, Any]:
    _asegurar()
    return {k: _REGISTRO[k] for k in sorted(_REGISTRO)}

# ===============================================================
# FIN 9.5
# ===============================================================


# ===============================================================
# 9.6 — CARGAR IDIOMA
# ===============================================================

def cargar_idioma(idioma: str) -> Dict[str, Any]:
    return {n: cargar(n) for n in listar_por_idioma(idioma)}

# ===============================================================
# FIN 9.6
# ===============================================================


# ===============================================================
# 9.7 — DEFINIR
# ===============================================================

def definir(palabra: str, *nombres: str) -> Optional[Dict[str, Any]]:
    _asegurar()
    p = _norm_palabra(palabra)
    if not p:
        return None

    fuentes = list(nombres) if nombres else listar()
    for nombre in fuentes:
        try:
            datos = cargar(nombre)
        except KeyError:
            continue

        if isinstance(datos, dict):
            for k, v in datos.items():
                if _norm_palabra(str(k)) == p:
                    return {
                        "palabra": p,
                        "definicion": _extraer_definicion(v),
                        "significado": _extraer_significado(v),
                        "fuente": _norm_nombre(nombre),
                        "entrada": v,
                    }
        elif isinstance(datos, (set, frozenset, list, tuple)):
            if p in {_norm_palabra(str(x)) for x in datos}:
                return {
                    "palabra": p,
                    "definicion": None,
                    "significado": None,
                    "fuente": _norm_nombre(nombre),
                    "entrada": p,
                    "nota": "término presente sin definición textual",
                }
    return None

# ===============================================================
# FIN 9.7
# ===============================================================


# ===============================================================
# 9.8 — SIGNIFICADO
# ===============================================================

def significado(palabra: str, *nombres: str) -> Optional[str]:
    r = definir(palabra, *nombres)
    if r is None:
        return None
    return r.get("significado") or r.get("definicion")

# ===============================================================
# FIN 9.8
# ===============================================================


# ===============================================================
# 9.9 — PALABRAS
# ===============================================================

def palabras(*nombres: str) -> Set[str]:
    _asegurar()
    fuentes = list(nombres) if nombres else listar()
    out: Set[str] = set()
    for nombre in fuentes:
        try:
            datos = cargar(nombre)
        except KeyError:
            continue
        if isinstance(datos, dict):
            out |= {_norm_palabra(str(k)) for k in datos if k}
        elif isinstance(datos, (set, frozenset, list, tuple)):
            out |= {_norm_palabra(str(x)) for x in datos if x}
    return out

# ===============================================================
# FIN 9.9
# ===============================================================


# ===============================================================
# 9.10 — INYECTAR EN PETICIÓN
# ===============================================================

def inyectar_en_peticion(
    peticion: Optional[Dict[str, Any]] = None,
    *nombres: str,
    clave: str = "diccionario",
) -> Dict[str, Any]:
    base = dict(peticion or {})
    lemas = sorted(palabras(*nombres))
    base[clave] = lemas
    base["_diccionario_meta"] = {
        "nombres": list(nombres) if nombres else listar(),
        "size": len(lemas),
        "version": VERSION_MODULO,
        "modulo": "diccionario",
        "rol": "DI",
    }
    return base

# ===============================================================
# FIN 9.10
# ===============================================================


# ===============================================================
# 9.11 — RESOLVER
# ===============================================================

def resolver(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    _asegurar()
    peticion = dict(peticion or {})
    palabra = peticion.get("palabra") or peticion.get("termino")
    idioma = peticion.get("idioma")
    nombres = peticion.get("diccionarios") or peticion.get("nombres")

    if palabra:
        if nombres:
            if isinstance(nombres, str):
                nombres = [nombres]
            r = definir(str(palabra), *nombres)
        elif idioma:
            r = definir(str(palabra), *listar_por_idioma(str(idioma)))
        else:
            r = definir(str(palabra))
        return {
            "ok": r is not None,
            "modulo": "diccionario",
            "rol": "DI",
            "resultado": r,
            "coherente": True,
            "notas": [
                "Definición entregada. No se calculó Tru ni se clasificó O."
            ],
        }

    if idioma and not nombres:
        datos = cargar_idioma(str(idioma))
        usados = list(datos.keys())
    elif nombres:
        if isinstance(nombres, str):
            nombres = [nombres]
        datos = {n: cargar(n) for n in nombres}
        usados = list(nombres)
    else:
        datos = cargar_todos()
        usados = list(datos.keys())

    return {
        "ok": True,
        "modulo": "diccionario",
        "rol": "DI",
        "diccionarios_usados": usados,
        "palabras_n": len(palabras(*usados)),
        "coherente": True,
        "notas": [
            "Materia prima entregada. No se calculó Tru ni se clasificó O."
        ],
    }

# ===============================================================
# FIN 9.11
# ===============================================================


# ===============================================================
# 9.12 — BARRER
# ===============================================================

def barrer() -> Dict[str, Any]:
    _asegurar()
    errores: List[str] = []
    notas: List[str] = []
    por_idioma: Dict[str, List[str]] = {}

    for k, m in sorted(_META.items()):
        if m.get("error"):
            errores.append("{0}: {1}".format(k, m["error"]))
            continue
        if k not in _REGISTRO:
            continue
        idioma = str(m.get("idioma") or "?").lower()
        por_idioma.setdefault(idioma, []).append(k)
        datos = _REGISTRO[k]
        if not isinstance(datos, (dict, set, frozenset, list, tuple)):
            errores.append(
                "{0}: DICCIONARIO debe ser dict (definiciones) "
                "o set/list (términos)".format(k)
            )

    if not _REGISTRO:
        notas.append(
            "ningún diccionario declarado todavía "
            "(vacío legítimo hasta montar fuentes)"
        )

    if errores:
        try:
            DiagnosticoGlobal.recibir_reporte(
                modulo="diccionario",
                errores=[{"tipo": "error", "detalle": e} for e in errores],
            )
        except Exception:
            pass

    return {
        "contenedor": "diccionario",
        "rol": "DI",
        "coherente": not errores,
        "errores": errores,
        "diccionarios": listar(),
        "total": len(_REGISTRO),
        "por_idioma": por_idioma,
        "notas": notas,
    }

# ===============================================================
# FIN 9.12
# ===============================================================


# ===============================================================
# 9.13 — VERIFICAR
# ===============================================================

def verificar() -> Dict[str, Any]:
    """Alias contractual real de barrer."""
    return barrer()

# ===============================================================
# FIN 9.13
# ===============================================================


# ===============================================================
# 9.14 — VERIFICAR SALIDA
# ===============================================================

def verificar_salida(salida: Dict[str, Any]) -> bool:
    if not isinstance(salida, dict):
        return False
    if "coherente" not in salida:
        return False
    if not isinstance(salida["coherente"], bool):
        return False
    return True

# ===============================================================
# FIN 9.14
# ===============================================================


# ===============================================================
# 9.15 — AXIOMAS
# ===============================================================

def axiomas() -> List[Dict[str, Any]]:
    return [
        {
            "id": "DI-OP-1",
            "tipo": "axioma",
            "sujeto": "diccionario",
            "relacion": "es",
            "objeto": "herramienta_de_definiciones",
            "polaridad": True,
            "enunciado": (
                "DI es la herramienta de definiciones para contrastar y "
                "correlacionar a nivel léxico-significado."
            ),
            "depende_de": [],
            "gobierna": ["diccionario"],
        },
        {
            "id": "DI-OP-2",
            "tipo": "axioma",
            "sujeto": "diccionario",
            "relacion": "no_calcula",
            "objeto": "Tru_ni_C_L_K",
            "polaridad": True,
            "enunciado": (
                "DI no calcula Tru_Ri, Tru_total, C, L ni K."
            ),
            "depende_de": [],
            "gobierna": ["diccionario"],
        },
        {
            "id": "DI-OP-3",
            "tipo": "axioma",
            "sujeto": "diccionario",
            "relacion": "no_clasifica",
            "objeto": "O_context",
            "polaridad": True,
            "enunciado": (
                "DI no clasifica O_context (oficio CX)."
            ),
            "depende_de": [],
            "gobierna": ["diccionario", "contexto"],
        },
        {
            "id": "DI-OP-4",
            "tipo": "axioma",
            "sujeto": "fuentes_de_diccionario",
            "relacion": "se_leen",
            "objeto": "automaticamente",
            "polaridad": True,
            "enunciado": (
                "Todo archivo bajo el módulo que declare DICCIONARIO se carga solo."
            ),
            "depende_de": [],
            "gobierna": ["diccionario"],
        },
    ]

# ===============================================================
# FIN 9.15
# ===============================================================


# ===============================================================
# 9.16 — INVENTARIO
# ===============================================================

def inventario(peticion: Any = None) -> Dict[str, Any]:
    b = barrer()
    detalle = []
    for n in listar():
        m = meta(n) or {}
        datos = _REGISTRO.get(n)
        if isinstance(datos, dict):
            size = len(datos)
            tipo = m.get("tipo") or "definiciones"
        elif isinstance(datos, (set, frozenset, list, tuple)):
            size = len(datos)
            tipo = m.get("tipo") or "terminos"
        else:
            size = None
            tipo = m.get("tipo")
        detalle.append({
            "nombre": n,
            "idioma": m.get("idioma"),
            "tipo": tipo,
            "size": size,
            "version": m.get("version"),
            "archivo": m.get("archivo"),
        })
    return {
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "total": b.get("total"),
        "diccionarios": detalle,
        "por_idioma": b.get("por_idioma"),
        "coherente": b.get("coherente"),
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "autoridad": CONTENEDOR.get("autoridad"),
        "conocimiento_exportable": CONTENEDOR.get("conocimiento_exportable"),
        "consultas_soportadas": CONTENEDOR.get("consultas_soportadas"),
        "invariantes": CONTENEDOR.get("invariantes"),
    }

# ===============================================================
# FIN 9.16
# ===============================================================


# ===============================================================
# 9.17 — REPORTE
# ===============================================================

def reporte() -> Dict[str, Any]:
    b = barrer()
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "estado": (
            ESTADO_OPERATIVO if b.get("coherente") else ESTADO_DEGRADADO
        ),
        "coherente": b.get("coherente"),
        "diccionarios": b.get("total"),
        "errores": len(b.get("errores") or []),
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "operaciones_arquitectonicas": {
            "ejecutar_total": True,
            "inspeccionar": True,
            "registrar_inventario": True,
        },
    }

# ===============================================================
# FIN 9.17
# ===============================================================


# ===============================================================
# 9.18 — DIAGNÓSTICO
# ===============================================================

def diagnostico() -> Dict[str, Any]:
    b = barrer()
    problemas: List[Dict[str, Any]] = []
    advertencias: List[str] = []
    recomendaciones: List[str] = []

    if b.get("errores"):
        problemas.append({"tipo": "errores_carga", "detalle": b["errores"]})
        recomendaciones.append(
            "Revisar archivos de fuentes con error de carga"
        )

    if not b.get("diccionarios"):
        advertencias.append("No hay diccionarios cargados")
        recomendaciones.append(
            "Agregar archivos con DICCIONARIO en fuentes/"
        )

    estado = ESTADO_OPERATIVO
    if problemas:
        estado = ESTADO_DEGRADADO
    if not b.get("diccionarios") and not problemas:
        estado = ESTADO_NO_INICIADO

    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "estado": estado,
        "coherente": b.get("coherente"),
        "problemas": problemas,
        "advertencias": advertencias,
        "recomendaciones": recomendaciones,
        "diccionarios": b.get("total"),
        "errores_n": len(b.get("errores") or []),
    }

# ===============================================================
# FIN 9.18
# ===============================================================


# ===============================================================
# 9.19 — EJECUTAR TOTAL
# ===============================================================

def ejecutar_total(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Autoridad total de ENGINE sobre DI.
    Fuente única: CONTENEDOR["capacidades"].
    No inventa. No autoinvoca. Todo callable real.
    """
    peticion_normalizada = (
        dict(peticion) if isinstance(peticion, dict) else {}
    )
    resultados: Dict[str, Any] = {}
    errores_ejecucion: List[str] = []

    capacidades = CONTENEDOR.get("capacidades", {})
    if not isinstance(capacidades, dict):
        return {
            "id": ID_MODULO,
            "modulo": NOMBRE_MODULO,
            "rol": ROL_MODULO,
            "version": VERSION_MODULO,
            "operacion": "ejecutar_total",
            "estado": ESTADO_DEGRADADO,
            "coherente": False,
            "capacidades_ejecutadas": [],
            "errores_ejecucion": [
                f"{NOMBRE_MODULO}: CONTENEDOR['capacidades'] no es dict"
            ],
            "resultados": {},
            "capacidades_declaradas": [],
        }

    for nombre in sorted(capacidades):
        if nombre == "ejecutar_total":
            continue
        referencia = capacidades[nombre]
        try:
            if callable(referencia):
                firma = inspect.signature(referencia)
                params = list(firma.parameters.values())
                obligatorios = [
                    p for p in params
                    if p.kind in (
                        inspect.Parameter.POSITIONAL_ONLY,
                        inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    )
                    and p.default is inspect.Parameter.empty
                ]
                if not obligatorios:
                    resultados[nombre] = referencia()
                elif len(obligatorios) == 1:
                    resultados[nombre] = referencia(peticion_normalizada)
                else:
                    resultados[nombre] = referencia()
            elif isinstance(referencia, str):
                fn = globals().get(referencia)
                if not callable(fn):
                    raise ContratoInvalido(
                        f"'{referencia}' no es callable"
                    )
                firma = inspect.signature(fn)
                params = list(firma.parameters.values())
                obligatorios = [
                    p for p in params
                    if p.kind in (
                        inspect.Parameter.POSITIONAL_ONLY,
                        inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    )
                    and p.default is inspect.Parameter.empty
                ]
                if not obligatorios:
                    resultados[nombre] = fn()
                elif len(obligatorios) == 1:
                    resultados[nombre] = fn(peticion_normalizada)
                else:
                    resultados[nombre] = fn()
            else:
                raise ContratoInvalido(
                    f"tipo inválido: {type(referencia).__name__}"
                )
        except Exception as exc:
            errores_ejecucion.append(f"{nombre}: {exc}")
            resultados[nombre] = None

    barrido = resultados.get("barrer")
    coherente = (
        isinstance(barrido, dict) and bool(barrido.get("coherente"))
    )
    ejecutadas = sorted(
        n for n, r in resultados.items() if r is not None
    )

    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "operacion": "ejecutar_total",
        "estado": (
            ESTADO_OPERATIVO
            if coherente and not errores_ejecucion
            else ESTADO_DEGRADADO
        ),
        "coherente": coherente and not errores_ejecucion,
        "capacidades_ejecutadas": ejecutadas,
        "errores_ejecucion": errores_ejecucion,
        "resultados": resultados,
        "capacidades_declaradas": sorted(capacidades.keys()),
    }

# ===============================================================
# FIN 9.19
# ===============================================================


# ===============================================================
# 9.20 — INSPECCIONAR
# ===============================================================

def inspeccionar(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Inspección estructural de DI.
    Expone contrato y estado sin calcular ni alterar.
    """
    b = barrer()
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "operacion": "inspeccionar",
        "constantes": {
            "ID_MODULO": ID_MODULO,
            "NOMBRE_MODULO": NOMBRE_MODULO,
            "ROL_MODULO": ROL_MODULO,
            "VERSION_MODULO": VERSION_MODULO,
            "VERSION_CONTRATO": VERSION_CONTRATO,
            "ESQUEMA_CONTRATO": ESQUEMA_CONTRATO,
            "ESTABILIDAD": ESTABILIDAD,
        },
        "capacidades_contractuales": sorted(
            CONTENEDOR.get("capacidades", {}).keys()
        ),
        "capacidades_meta": sorted(
            CONTENEDOR.get("capacidades_meta", {}).keys()
        ),
        "integridad": {
            "coherente": b.get("coherente"),
            "errores": b.get("errores"),
            "diccionarios": b.get("diccionarios"),
            "total": b.get("total"),
            "por_idioma": b.get("por_idioma"),
        },
        "autoriza_engine": CONTENEDOR.get("autoriza_engine"),
        "reporting": CONTENEDOR.get("reporting"),
        "invariantes": list(INVARIANTES),
        "nota": (
            "inspeccionar expone estructura de DI sin calcular "
            "ni alterar el contrato."
        ),
    }

# ===============================================================
# FIN 9.20
# ===============================================================


# ===============================================================
# 9.21 — REGISTRAR INVENTARIO
# ===============================================================

def registrar_inventario(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Instantánea determinista del inventario de DI.
    No altera evidencia.
    """
    inv = inventario(peticion)
    return {
        "id": ID_MODULO,
        "operacion": "registrar_inventario",
        "registrado": True,
        "inventario": inv,
        "nota": (
            "Instantánea determinista del inventario de DI. "
            "No modifica fuentes ni evidencia."
        ),
    }

# ===============================================================
# FIN 9.21
# ===============================================================

# ===============================================================
# FIN 9 — CAPACIDADES PÚBLICAS
# ===============================================================

# ===============================================================
# 10 — VALIDACIÓN, RESOLUCIÓN Y EXPORTACIONES
# ===============================================================

# ===============================================================
# 10.1 — VALIDACIÓN DE CONTRATO
# ===============================================================

def _validar_contrato(cont: Dict[str, Any]) -> None:
    obligatorias = (
        "esquema", "version_contrato", "version_modulo",
        "id", "nombre", "rol", "descripcion",
        "funcion", "no_hace", "autoridad",
        "conocimiento_exportable", "requiere",
        "autoriza_engine", "consultas_soportadas",
        "capacidades", "capacidades_meta",
        "reporting", "estados_validos", "invariantes",
        "estabilidad", "compatible_desde", "api_engine",
    )
    faltantes = [k for k in obligatorias if k not in cont]
    if faltantes:
        raise ContratoInvalido(
            "{0}: CONTENEDOR incompleto. Faltan: {1}".format(
                NOMBRE_MODULO, faltantes
            )
        )
    if cont.get("esquema") != ESQUEMA_CONTRATO:
        raise ContratoInvalido(
            "{0}: esquema incompatible: {1}".format(
                NOMBRE_MODULO, cont.get("esquema")
            )
        )
    if str(cont.get("version_contrato")) != VERSION_CONTRATO:
        raise ContratoInvalido(
            "{0}: version_contrato inválida: {1}".format(
                NOMBRE_MODULO, cont.get("version_contrato")
            )
        )
    meta_caps = cont.get("capacidades_meta") or {}
    for nombre_cap in cont.get("capacidades") or {}:
        if nombre_cap not in meta_caps:
            raise ContratoInvalido(
                "{0}: capacidad '{1}' sin capacidades_meta".format(
                    NOMBRE_MODULO, nombre_cap
                )
            )
        entrada = meta_caps[nombre_cap]
        if not isinstance(entrada, dict):
            raise ContratoInvalido(
                "{0}: capacidades_meta['{1}'] debe ser dict".format(
                    NOMBRE_MODULO, nombre_cap
                )
            )
        for campo in ("descripcion", "entrada", "salida"):
            if campo not in entrada or not isinstance(entrada[campo], str):
                raise ContratoInvalido(
                    "{0}: capacidades_meta['{1}'] requiere '{2}: str'".format(
                        NOMBRE_MODULO, nombre_cap, campo
                    )
                )

# ===============================================================
# FIN 10.1
# ===============================================================


# ===============================================================
# 10.2 — MAPA DE CAPACIDADES
# ===============================================================

_CAP_MAP = {
    # --- CENTINELA ---
    "verificar": verificar,
    "barrer": barrer,
    "verificar_salida": verificar_salida,

    # --- INVENTARIO Y REPORTING ---
    "inventario": inventario,
    "reporte": reporte,
    "diagnostico": diagnostico,

    # --- CONOCIMIENTO ---
    "axiomas": axiomas,
    "resolver": resolver,

    # --- OPERACIONES LÉXICAS ---
    "listar": listar,
    "cargar": cargar,
    "cargar_todos": cargar_todos,
    "definir": definir,
    "significado": significado,
    "palabras": palabras,
    "inyectar_en_peticion": inyectar_en_peticion,

    # --- CAPACIDADES ARQUITECTÓNICAS (OBLIGATORIAS ENGINE) ---
    "ejecutar_total": ejecutar_total,
    "inspeccionar": inspeccionar,
    "registrar_inventario": registrar_inventario,
}

# ===============================================================
# FIN 10.2
# ===============================================================


# ===============================================================
# 10.3 — RESOLUCIÓN DE CAPACIDADES
# ===============================================================

def _resolver_capacidades(cont: Dict[str, Any]) -> None:
    """
    Resuelve referencias str → callables reales.
    MUTA CONTENEDOR["capacidades"] para que Engine reciba callables.
    """
    resueltas: Dict[str, Any] = {}
    for nombre, ref in cont["capacidades"].items():
        if callable(ref):
            resueltas[nombre] = ref
            continue
        if isinstance(ref, str):
            if ref not in _CAP_MAP:
                raise ContratoInvalido(
                    "{0}: capacidad '{1}' referencia inexistente: '{2}'".format(
                        NOMBRE_MODULO, nombre, ref
                    )
                )
            fn = _CAP_MAP[ref]
            if not callable(fn):
                raise ContratoInvalido(
                    "{0}: '{1}' no es callable".format(NOMBRE_MODULO, ref)
                )
            resueltas[nombre] = fn
            continue
        raise ContratoInvalido(
            "{0}: capacidad '{1}' tipo inválido: {2}".format(
                NOMBRE_MODULO, nombre, type(ref).__name__
            )
        )
    cont["capacidades"] = resueltas

# ===============================================================
# FIN 10.3
# ===============================================================


# ===============================================================
# 10.4 — VALIDAR Y RESOLVER AL IMPORTAR
# ===============================================================

_validar_contrato(CONTENEDOR)
_resolver_capacidades(CONTENEDOR)

# ===============================================================
# FIN 10.4
# ===============================================================


# ===============================================================
# 10.5 — EXPORTACIONES
# ===============================================================

__all__ = [
    "CONTENEDOR",
    "ID_MODULO",
    "NOMBRE_MODULO",
    "ROL_MODULO",
    "VERSION_MODULO",
    "VERSION_CONTRATO",
    "ESQUEMA_CONTRATO",
    "ESTABILIDAD",
    "listar",
    "listar_por_idioma",
    "meta",
    "cargar",
    "cargar_todos",
    "cargar_idioma",
    "definir",
    "significado",
    "palabras",
    "inyectar_en_peticion",
    "resolver",
    "verificar",
    "barrer",
    "verificar_salida",
    "inventario",
    "reporte",
    "diagnostico",
    "axiomas",
    "ejecutar_total",
    "inspeccionar",
    "registrar_inventario",
    "ContratoInvalido",
]

# ===============================================================
# FIN 10.5
# ===============================================================

# ===============================================================
# FIN 10 — VALIDACIÓN, RESOLUCIÓN Y EXPORTACIONES
# ===============================================================


# ===============================================================
# FIN DEL MÓDULO
# ===============================================================
