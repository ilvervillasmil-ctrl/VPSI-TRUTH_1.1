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
import inspect
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set

try:
    from core.diagnostico import DiagnosticoGlobal  # type: ignore
except Exception:  # noqa: BLE001
    DiagnosticoGlobal = None  # type: ignore


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
    "CE", "AX", "FO", "MC", "SF",
    "CA", "CX", "RE", "VX",
    "TX", "CH", "CIT", "DGCO", "UI",
    "CC", "TT", "SC", "CT"
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

## ===============================================================
# 8 — FUNCIONES PRIVADAS
# ===============================================================

# ===============================================================
# 8.1 — NORMALIZACIÓN
# ===============================================================

def _norm_nombre(nombre: str) -> str:
    """Normaliza un nombre de diccionario a clave determinista."""
    return (nombre or "").strip().lower().replace("-", "_").replace(" ", "_")


def _norm_palabra(p: str) -> str:
    """Normaliza una palabra a lema determinista."""
    return (p or "").strip().lower()

# ===============================================================
# FIN 8.1
# ===============================================================

# ===============================================================
# 8.1 — NORMALIZACIÓN
# ===============================================================

def _norm_nombre(nombre: str) -> str:
    if not isinstance(nombre, str):
        raise TypeError("nombre debe ser str")
    return nombre.strip().lower().replace("-", "_").replace(" ", "_")


def _norm_palabra(p: str) -> str:
    if not isinstance(p, str):
        raise TypeError("p debe ser str")
    return p.strip().lower()

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
        valor = entrada.strip()
        return valor or None
    if isinstance(entrada, dict):
        for clave in ("definicion", "definición", "def", "meaning", "significado"):
            valor = entrada.get(clave)
            if isinstance(valor, str):
                valor = valor.strip()
                if valor:
                    return valor
    return None


def _extraer_significado(entrada: Any) -> Optional[str]:
    if not isinstance(entrada, dict):
        return _extraer_definicion(entrada)
    for clave in ("significado", "meaning", "interpretacion", "interpretación"):
        valor = entrada.get(clave)
        if isinstance(valor, str):
            valor = valor.strip()
            if valor:
                return valor
    return _extraer_definicion(entrada)

# ===============================================================
# FIN 8.2
# ===============================================================
# ===============================================================
# 8.3 — CARGA DE MÓDULO
# ===============================================================

def _cargar_modulo(path: Path, clave: str) -> Optional[Any]:
    """
    Carga determinísticamente un archivo Python como módulo aislado.

    No ejecuta ninguna capacidad del módulo.
    Solo importa el archivo y devuelve su objeto módulo.
    Si la especificación, el loader o la ejecución fallan, devuelve None.
    """
    if not isinstance(path, Path):
        raise TypeError(
            f"{NOMBRE_MODULO}: path debe ser Path, recibido: {type(path).__name__}"
        )

    if not isinstance(clave, str) or not clave.strip():
        raise ValueError(
            f"{NOMBRE_MODULO}: clave de módulo inválida"
        )

    if not path.is_file():
        return None

    spec = importlib.util.spec_from_file_location(clave, path)

    if spec is None or spec.loader is None:
        return None

    mod = importlib.util.module_from_spec(spec)

    if mod is None:
        return None

    sys.modules[clave] = mod

    try:
        spec.loader.exec_module(mod)
    except Exception:
        sys.modules.pop(clave, None)
        return None

    return mod

# ===============================================================
# FIN 8.3
# ===============================================================


# ===============================================================
# 8.4 — DESCUBRIMIENTO
# ===============================================================

def _descubrir() -> None:
    """
    Descubre y registra determinísticamente todos los archivos Python
    que declaren DICCIONARIO dentro del módulo y de fuentes/.

    No modifica otros módulos.
    No inventa entradas.
    No ejecuta capacidades públicas del módulo descubierto.
    """
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

        mod = _cargar_modulo(resolved, clave)

        if mod is None:
            _META[f.stem] = {
                "error": "carga fallida",
                "archivo": f.name,
            }
            continue

        datos = getattr(mod, "DICCIONARIO", None)

        if datos is None:
            continue

        meta_modulo = getattr(mod, "META", None)

        nombre = None

        if isinstance(meta_modulo, dict):
            nombre = meta_modulo.get("nombre")

        if not nombre:
            nombre = f.stem

        key = _norm_nombre(str(nombre))

        if not key:
            _META[f.stem] = {
                "error": "nombre de diccionario inválido",
                "archivo": f.name,
            }
            continue

        _REGISTRO[key] = datos

        if isinstance(meta_modulo, dict):
            _META[key] = dict(meta_modulo)
            _META[key]["archivo"] = f.name
        else:
            _META[key] = {
                "nombre": key,
                "archivo": f.name,
            }

    _CARGADO = True


def _asegurar() -> None:
    """
    Garantiza que el descubrimiento haya ocurrido antes de acceder
    al registro léxico.
    """
    _descubrir()

# ===============================================================
# FIN 8.4
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

    if not isinstance(idioma, str):
        raise TypeError(
            f"{NOMBRE_MODULO}: idioma debe ser str, "
            f"recibido: {type(idioma).__name__}"
        )

    idioma_normalizado = idioma.strip().lower()

    if not idioma_normalizado:
        return []

    resultado: List[str] = []

    for nombre in sorted(_REGISTRO):
        meta_registro = _META.get(nombre)

        if not isinstance(meta_registro, dict):
            continue

        idioma_registro = meta_registro.get("idioma")

        if not isinstance(idioma_registro, str):
            continue

        if idioma_registro.strip().lower() == idioma_normalizado:
            resultado.append(nombre)

    return resultado

# ===============================================================
# FIN 9.2
# ===============================================================
# ===============================================================
# 9.3 — META
# ===============================================================

def meta(nombre: str) -> Optional[Dict[str, Any]]:
    _asegurar()

    if not isinstance(nombre, str):
        raise TypeError(
            "{0}: nombre debe ser str; recibido: {1}".format(
                NOMBRE_MODULO,
                type(nombre).__name__,
            )
        )

    key = _norm_nombre(nombre)
    if not key:
        return None

    registro = _META.get(key)
    if registro is None:
        return None

    return dict(registro)

# ===============================================================
# FIN 9.3
# ===============================================================


# ===============================================================
# 9.4 — CARGAR
# ===============================================================

def cargar(nombre: str) -> Any:
    _asegurar()

    if not isinstance(nombre, str):
        raise TypeError(
            "{0}: nombre debe ser str; recibido: {1}".format(
                NOMBRE_MODULO,
                type(nombre).__name__,
            )
        )

    key = _norm_nombre(nombre)

    if not key:
        raise KeyError(
            "{0}: nombre de diccionario vacío".format(
                NOMBRE_MODULO
            )
        )

    if key not in _REGISTRO:
        disponibles = sorted(_REGISTRO.keys())
        raise KeyError(
            "diccionario no encontrado: {0!r}. Disponibles: {1}".format(
                nombre,
                disponibles,
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

    return {
        nombre: _REGISTRO[nombre]
        for nombre in sorted(_REGISTRO.keys())
    }

# ===============================================================
# FIN 9.5
# ===============================================================


# ===============================================================
# 9.6 — CARGAR IDIOMA
# ===============================================================

def cargar_idioma(idioma: str) -> Dict[str, Any]:
    _asegurar()

    if not isinstance(idioma, str):
        raise TypeError(
            "{0}: idioma debe ser str; recibido: {1}".format(
                NOMBRE_MODULO,
                type(idioma).__name__,
            )
        )

    idioma_normalizado = idioma.strip().lower()

    if not idioma_normalizado:
        return {}

    nombres = listar_por_idioma(idioma_normalizado)

    return {
        nombre: _REGISTRO[nombre]
        for nombre in nombres
    }

# ===============================================================
# FIN 9.6
# ===============================================================


# ===============================================================
# 9.7 — DEFINIR
# ===============================================================

def definir(palabra: str, *nombres: str) -> Optional[Dict[str, Any]]:
    _asegurar()

    if not isinstance(palabra, str):
        raise TypeError(
            "{0}: palabra debe ser str; recibido: {1}".format(
                NOMBRE_MODULO,
                type(palabra).__name__,
            )
        )

    for nombre in nombres:
        if not isinstance(nombre, str):
            raise TypeError(
                "{0}: cada nombre de diccionario debe ser str; "
                "recibido: {1}".format(
                    NOMBRE_MODULO,
                    type(nombre).__name__,
                )
            )

    p = _norm_palabra(palabra)

    if not p:
        return None

    fuentes = list(nombres) if nombres else listar()

    for nombre in fuentes:
        key = _norm_nombre(nombre)

        if not key:
            raise KeyError(
                "{0}: nombre de diccionario vacío".format(
                    NOMBRE_MODULO
                )
            )

        if key not in _REGISTRO:
            raise KeyError(
                "diccionario no encontrado: {0!r}. Disponibles: {1}".format(
                    nombre,
                    sorted(_REGISTRO.keys()),
                )
            )

        datos = _REGISTRO[key]

        if isinstance(datos, dict):
            coincidencias = []

            for k, v in datos.items():
                termino = _norm_palabra(str(k))

                if termino and termino == p:
                    coincidencias.append((k, v))

            if len(coincidencias) > 1:
                raise ContratoInvalido(
                    "{0}: diccionario '{1}' contiene múltiples "
                    "entradas que normalizan a '{2}'".format(
                        NOMBRE_MODULO,
                        key,
                        p,
                    )
                )

            if coincidencias:
                _, entrada = coincidencias[0]

                return {
                    "palabra": p,
                    "definicion": _extraer_definicion(entrada),
                    "significado": _extraer_significado(entrada),
                    "fuente": key,
                    "entrada": entrada,
                }

        elif isinstance(datos, (set, frozenset, list, tuple)):
            for elemento in datos:
                termino = _norm_palabra(str(elemento))

                if termino and termino == p:
                    return {
                        "palabra": p,
                        "definicion": None,
                        "significado": None,
                        "fuente": key,
                        "entrada": elemento,
                        "nota": (
                            "término presente sin definición textual"
                        ),
                    }

    return None

# ===============================================================
# FIN 9.7
# ===============================================================


# ===============================================================
# 9.8 — SIGNIFICADO
# ===============================================================

def significado(palabra: str, *nombres: str) -> Optional[str]:
    resultado = definir(palabra, *nombres)

    if resultado is None:
        return None

    significado_resultado = resultado.get("significado")

    if isinstance(significado_resultado, str) and significado_resultado.strip():
        return significado_resultado

    definicion_resultado = resultado.get("definicion")

    if isinstance(definicion_resultado, str) and definicion_resultado.strip():
        return definicion_resultado

    return None

# ===============================================================
# FIN 9.8
# ===============================================================


# ===============================================================
# 9.9 — PALABRAS
# ===============================================================

def palabras(*nombres: str) -> Set[str]:
    _asegurar()

    for nombre in nombres:
        if not isinstance(nombre, str):
            raise TypeError(
                "{0}: cada nombre de diccionario debe ser str; "
                "recibido: {1}".format(
                    NOMBRE_MODULO,
                    type(nombre).__name__,
                )
            )

    fuentes = list(nombres) if nombres else listar()
    out: Set[str] = set()

    for nombre in fuentes:
        key = _norm_nombre(nombre)

        if not key:
            raise KeyError(
                "{0}: nombre de diccionario vacío".format(
                    NOMBRE_MODULO
                )
            )

        if key not in _REGISTRO:
            raise KeyError(
                "diccionario no encontrado: {0!r}. Disponibles: {1}".format(
                    nombre,
                    sorted(_REGISTRO.keys()),
                )
            )

        datos = _REGISTRO[key]

        if isinstance(datos, dict):
            elementos = datos.keys()
        elif isinstance(datos, (set, frozenset, list, tuple)):
            elementos = datos
        else:
            raise ContratoInvalido(
                "{0}: DICCIONARIO '{1}' tiene tipo inválido: {2}".format(
                    NOMBRE_MODULO,
                    key,
                    type(datos).__name__,
                )
            )

        for elemento in elementos:
            termino = _norm_palabra(str(elemento))

            if termino:
                out.add(termino)

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
    _asegurar()

    if peticion is not None and not isinstance(peticion, dict):
        raise TypeError(
            "{0}: peticion debe ser dict o None; recibido: {1}".format(
                NOMBRE_MODULO,
                type(peticion).__name__,
            )
        )

    if not isinstance(clave, str):
        raise TypeError(
            "{0}: clave debe ser str; recibido: {1}".format(
                NOMBRE_MODULO,
                type(clave).__name__,
            )
        )

    clave = clave.strip()

    if not clave:
        raise ValueError(
            "{0}: clave no puede estar vacía".format(
                NOMBRE_MODULO
            )
        )

    for nombre in nombres:
        if not isinstance(nombre, str):
            raise TypeError(
                "{0}: cada nombre de diccionario debe ser str; "
                "recibido: {1}".format(
                    NOMBRE_MODULO,
                    type(nombre).__name__,
                )
            )

    fuentes = list(nombres) if nombres else listar()
    lemas = sorted(palabras(*fuentes))

    base = dict(peticion) if peticion is not None else {}

    base[clave] = lemas
    base["_diccionario_meta"] = {
        "nombres": list(fuentes),
        "size": len(lemas),
        "version": VERSION_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
    }

    return base

# ===============================================================
# FIN 9.10
# ===============================================================


# ===============================================================
# 9.11 — RESOLVER
# ===============================================================

def resolver(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    _asegurar()

    if peticion is not None and not isinstance(peticion, dict):
        raise TypeError(
            "{0}: peticion debe ser dict o None; recibido: {1}".format(
                NOMBRE_MODULO,
                type(peticion).__name__,
            )
        )

    base = dict(peticion) if peticion is not None else {}

    tiene_palabra = "palabra" in base
    tiene_termino = "termino" in base

    if tiene_palabra and tiene_termino:
        raise ContratoInvalido(
            "{0}: petición ambigua; no puede contener simultáneamente "
            "'palabra' y 'termino'".format(
                NOMBRE_MODULO
            )
        )

    if tiene_palabra:
        palabra = base["palabra"]
    elif tiene_termino:
        palabra = base["termino"]
    else:
        palabra = None

    if palabra is not None:
        if not isinstance(palabra, str):
            raise TypeError(
                "{0}: 'palabra'/'termino' debe ser str; recibido: {1}".format(
                    NOMBRE_MODULO,
                    type(palabra).__name__,
                )
            )

        if not palabra.strip():
            return {
                "ok": False,
                "modulo": NOMBRE_MODULO,
                "rol": ROL_MODULO,
                "resultado": None,
                "coherente": True,
                "notas": [
                    "Palabra vacía; no se realizó resolución."
                ],
            }

    tiene_diccionarios = "diccionarios" in base
    tiene_nombres = "nombres" in base

    if tiene_diccionarios and tiene_nombres:
        raise ContratoInvalido(
            "{0}: petición ambigua; no puede contener simultáneamente "
            "'diccionarios' y 'nombres'".format(
                NOMBRE_MODULO
            )
        )

    if tiene_diccionarios:
        nombres = base["diccionarios"]
    elif tiene_nombres:
        nombres = base["nombres"]
    else:
        nombres = None

    if nombres is not None:
        if isinstance(nombres, str):
            nombres = [nombres]
        elif isinstance(nombres, (list, tuple)):
            nombres = list(nombres)
        else:
            raise TypeError(
                "{0}: 'diccionarios'/'nombres' debe ser str, "
                "list o tuple; recibido: {1}".format(
                    NOMBRE_MODULO,
                    type(nombres).__name__,
                )
            )

        for nombre in nombres:
            if not isinstance(nombre, str):
                raise TypeError(
                    "{0}: cada nombre de diccionario debe ser str; "
                    "recibido: {1}".format(
                        NOMBRE_MODULO,
                        type(nombre).__name__,
                    )
                )

    tiene_idioma = "idioma" in base
    idioma = base.get("idioma") if tiene_idioma else None

    if idioma is not None:
        if not isinstance(idioma, str):
            raise TypeError(
                "{0}: 'idioma' debe ser str; recibido: {1}".format(
                    NOMBRE_MODULO,
                    type(idioma).__name__,
                )
            )

        idioma = idioma.strip().lower()

        if not idioma:
            raise ValueError(
                "{0}: 'idioma' no puede estar vacío".format(
                    NOMBRE_MODULO
                )
            )

    # -----------------------------------------------------------
    # RESOLUCIÓN DE PALABRA
    # -----------------------------------------------------------

    if palabra is not None and palabra.strip():

        if nombres is not None:
            resultado = definir(
                palabra,
                *nombres,
            )

        elif idioma is not None:
            fuentes = listar_por_idioma(idioma)

            resultado = definir(
                palabra,
                *fuentes,
            ) if fuentes else None

        else:
            resultado = definir(palabra)

        return {
            "ok": resultado is not None,
            "modulo": NOMBRE_MODULO,
            "rol": ROL_MODULO,
            "resultado": resultado,
            "coherente": True,
            "notas": [
                "Definición entregada. No se calculó Tru ni se clasificó O."
            ],
        }

    # -----------------------------------------------------------
    # RESOLUCIÓN DE MATERIA PRIMA
    # -----------------------------------------------------------

    if nombres is not None:
        fuentes = list(nombres)

    elif idioma is not None:
        fuentes = listar_por_idioma(idioma)

    else:
        fuentes = listar()

    datos = {
        nombre: cargar(nombre)
        for nombre in fuentes
    }

    total_palabras = len(
        palabras(*fuentes)
    )

    return {
        "ok": True,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "diccionarios_usados": list(fuentes),
        "palabras_n": total_palabras,
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
    """
    Centinela estructural de DI.

    Garantiza una salida determinista basada exclusivamente en el
    contenido actualmente descubierto en _REGISTRO y _META.

    No calcula Tru.
    No clasifica O_context.
    No modifica otros módulos.
    """
    _asegurar()

    errores: List[str] = []
    notas: List[str] = []
    por_idioma: Dict[str, List[str]] = {}

    for nombre in sorted(_META):
        metadata = _META[nombre]

        if not isinstance(metadata, dict):
            errores.append(
                "{0}: metadatos inválidos: se esperaba dict".format(nombre)
            )
            continue

        if metadata.get("error"):
            errores.append(
                "{0}: {1}".format(nombre, str(metadata["error"]))
            )
            continue

        if nombre not in _REGISTRO:
            errores.append(
                "{0}: existe metadata sin DICCIONARIO registrado".format(
                    nombre
                )
            )
            continue

        idioma = str(metadata.get("idioma") or "?").strip().lower()
        por_idioma.setdefault(idioma, []).append(nombre)

        datos = _REGISTRO[nombre]

        if not isinstance(datos, (dict, set, frozenset, list, tuple)):
            errores.append(
                "{0}: DICCIONARIO debe ser dict, set, frozenset, "
                "list o tuple".format(nombre)
            )

    for nombre in sorted(_REGISTRO):
        if nombre not in _META:
            metadata = {}
            idioma = "?"
            por_idioma.setdefault(idioma, []).append(nombre)

            datos = _REGISTRO[nombre]

            if not isinstance(datos, (dict, set, frozenset, list, tuple)):
                errores.append(
                    "{0}: DICCIONARIO debe ser dict, set, frozenset, "
                    "list o tuple".format(nombre)
                )

    for idioma in por_idioma:
        por_idioma[idioma] = sorted(set(por_idioma[idioma]))

    if not _REGISTRO:
        notas.append(
            "ningún diccionario declarado todavía "
            "(vacío legítimo hasta montar fuentes)"
        )

    resultado: Dict[str, Any] = {
        "contenedor": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "coherente": not errores,
        "errores": list(errores),
        "diccionarios": sorted(_REGISTRO.keys()),
        "total": len(_REGISTRO),
        "por_idioma": por_idioma,
        "notas": list(notas),
    }

    if errores:
        try:
            DiagnosticoGlobal.recibir_reporte(
                modulo=NOMBRE_MODULO,
                errores=[
                    {
                        "tipo": "error",
                        "detalle": error,
                    }
                    for error in errores
                ],
            )
        except Exception:
            pass

    return resultado

# ===============================================================
# FIN 9.12
# ===============================================================


# ===============================================================
# 9.13 — VERIFICAR
# ===============================================================

def verificar() -> Dict[str, Any]:
    """
    Callable contractual de verificación de DI.

    Es un alias funcional de barrer(): no introduce una segunda
    implementación de la validación.
    """
    return barrer()

# ===============================================================
# FIN 9.13
# ===============================================================


# ===============================================================
# 9.14 — VERIFICAR SALIDA
# ===============================================================

def verificar_salida(salida: Dict[str, Any]) -> bool:
    """
    Valida la forma contractual mínima de una salida producida por DI.

    La función no evalúa si DI está coherente; únicamente determina
    si la salida tiene la estructura mínima exigida.
    """
    if not isinstance(salida, dict):
        return False

    campos_obligatorios = (
        "contenedor",
        "rol",
        "coherente",
        "errores",
        "diccionarios",
        "total",
        "por_idioma",
        "notas",
    )

    for campo in campos_obligatorios:
        if campo not in salida:
            return False

    if salida["contenedor"] != NOMBRE_MODULO:
        return False

    if salida["rol"] != ROL_MODULO:
        return False

    if not isinstance(salida["coherente"], bool):
        return False

    if not isinstance(salida["errores"], list):
        return False

    if not isinstance(salida["diccionarios"], list):
        return False

    if not isinstance(salida["total"], int):
        return False

    if isinstance(salida["total"], bool):
        return False

    if salida["total"] != len(salida["diccionarios"]):
        return False

    if not isinstance(salida["por_idioma"], dict):
        return False

    for idioma, nombres in salida["por_idioma"].items():
        if not isinstance(idioma, str):
            return False
        if not isinstance(nombres, list):
            return False
        if not all(isinstance(nombre, str) for nombre in nombres):
            return False

    if not isinstance(salida["notas"], list):
        return False

    return True

# ===============================================================
# FIN 9.14
# ===============================================================

# ===============================================================
# 9.15 — AXIOMAS
# ===============================================================

def axiomas() -> List[Dict[str, Any]]:
    """
    Devuelve las declaraciones axiomáticas operativas propias de DI.

    La función es determinista: no depende de estado externo,
    archivos, tiempo ni resultados de otras capacidades.
    Cada invocación construye una nueva colección de declaraciones.
    """
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
            "objeto": "Tru_Ri_Tru_total_C_L_K",
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
                "DI no clasifica O_context; la clasificación de O_context "
                "corresponde al oficio de CX."
            ),
            "depende_de": [],
            "gobierna": ["diccionario"],
        },
        {
            "id": "DI-OP-4",
            "tipo": "axioma",
            "sujeto": "fuentes_de_diccionario",
            "relacion": "se_descubren_y_cargan",
            "objeto": "automaticamente",
            "polaridad": True,
            "enunciado": (
                "Los archivos Python elegibles descubiertos directamente "
                "en las ubicaciones de fuentes del módulo que declaren "
                "DICCIONARIO son cargados automáticamente por DI."
            ),
            "depende_de": [],
            "gobierna": ["diccionario"],
        },
    ]

# ===============================================================
# FIN 9.15
# ===============================================================

# ===============================================================
# 10 — INVENTARIO
# ===============================================================

def inventario(peticion: Any = None) -> Dict[str, Any]:
    """
    Genera el inventario estructural determinista de DI.

    La petición se conserva por compatibilidad con la interfaz del Engine,
    pero no modifica el inventario: esta capacidad reporta exclusivamente
    el estado estructural actualmente descubierto por DI.
    """
    b = barrer()

    detalle: List[Dict[str, Any]] = []

    for nombre in sorted(_REGISTRO):
        metadata = _META.get(nombre)

        if not isinstance(metadata, dict):
            raise ContratoInvalido(
                "{0}: metadata ausente o inválida para '{1}'".format(
                    NOMBRE_MODULO,
                    nombre,
                )
            )

        datos = _REGISTRO[nombre]

        if isinstance(datos, dict):
            tipo_estructural = "definiciones"
            size = len(datos)
        elif isinstance(datos, (set, frozenset, list, tuple)):
            tipo_estructural = "terminos"
            size = len(datos)
        else:
            tipo_estructural = "invalido"
            size = None

        tipo = metadata.get("tipo") or tipo_estructural

        detalle.append(
            {
                "nombre": nombre,
                "idioma": metadata.get("idioma"),
                "tipo": tipo,
                "size": size,
                "version": metadata.get("version"),
                "archivo": metadata.get("archivo"),
            }
        )

    return {
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "total": b["total"],
        "diccionarios": detalle,
        "por_idioma": b["por_idioma"],
        "coherente": b["coherente"],
        "capacidades": sorted(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR["requiere"]),
        "autoridad": list(CONTENEDOR["autoridad"]),
        "conocimiento_exportable": list(
            CONTENEDOR["conocimiento_exportable"]
        ),
        "consultas_soportadas": list(
            CONTENEDOR["consultas_soportadas"]
        ),
        "invariantes": list(CONTENEDOR["invariantes"]),
    }

# ===============================================================
# FIN 10
# ===============================================================

# ===============================================================
# 11 — REPORTE
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
            ESTADO_OPERATIVO
            if b.get("coherente") is True
            else ESTADO_DEGRADADO
        ),
        "coherente": b.get("coherente") is True,
        "diccionarios": b.get("total", 0),
        "errores": len(b.get("errores") or []),
        "capacidades": sorted(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
    }

# ===============================================================
# FIN 11
# ===============================================================
# ===============================================================
# 12 — DIAGNÓSTICO
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
# FIN 
# ===============================================================


# ===============================================================
# 13 — EJECUTAR TOTAL
# ===============================================================

# ===============================================================
# 13.1 — PREPARACIÓN DETERMINISTA DE ARGUMENTOS
# ===============================================================

def _preparar_argumentos_capacidad(
    nombre: str,
    funcion: Callable[..., Any],
    peticion: Dict[str, Any],
) -> Tuple[Tuple[Any, ...], Dict[str, Any]]:
    """
    Determina de forma estricta los argumentos que recibirá una capacidad.

    Reglas contractuales:

    1. La capacidad debe ser callable real.
    2. Un parámetro llamado 'peticion' recibe la petición completa.
    3. Un parámetro obligatorio recibe exclusivamente el valor de una
       clave con el mismo nombre presente en la petición.
    4. 'nombres' puede resolverse desde 'nombres' o 'diccionarios'.
    5. Los parámetros con valor por defecto no requieren resolución.
    6. Los parámetros *args y **kwargs no se inventan.
    7. Si falta un argumento obligatorio, la capacidad no se ejecuta.
    8. No se utiliza globals() para resolver referencias.
    9. No se transforma silenciosamente una referencia inválida.
    """
    if not callable(funcion):
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: capacidad '{nombre}' no es callable"
        )

    try:
        firma = inspect.signature(funcion)
    except (TypeError, ValueError) as exc:
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: no se puede inspeccionar la firma "
            f"de la capacidad '{nombre}': {exc}"
        ) from exc

    args: List[Any] = []
    kwargs: Dict[str, Any] = {}

    for parametro in firma.parameters.values():

        if parametro.kind is inspect.Parameter.VAR_POSITIONAL:
            continue

        if parametro.kind is inspect.Parameter.VAR_KEYWORD:
            continue

        if parametro.name == "peticion":
            valor = peticion

        elif parametro.name == "nombres":
            if "nombres" in peticion:
                valor = peticion["nombres"]
            elif "diccionarios" in peticion:
                valor = peticion["diccionarios"]
            elif parametro.default is not inspect.Parameter.empty:
                continue
            else:
                raise ContratoInvalido(
                    f"{NOMBRE_MODULO}: capacidad '{nombre}' requiere "
                    "el parámetro 'nombres' y la petición no lo proporciona"
                )

        elif parametro.name in peticion:
            valor = peticion[parametro.name]

        elif parametro.default is not inspect.Parameter.empty:
            continue

        else:
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: capacidad '{nombre}' requiere "
                f"el parámetro '{parametro.name}' y no existe en la petición"
            )

        if parametro.kind is inspect.Parameter.POSITIONAL_ONLY:
            args.append(valor)
        else:
            kwargs[parametro.name] = valor

    return tuple(args), kwargs

# ===============================================================
# FIN 13.1
# ===============================================================


# ===============================================================
# 13.2 — EJECUCIÓN DE UNA CAPACIDAD
# ===============================================================

def _ejecutar_capacidad(
    nombre: str,
    funcion: Callable[..., Any],
    peticion: Dict[str, Any],
) -> Any:
    """
    Ejecuta una única capacidad ya resuelta.

    No acepta referencias string.
    No busca funciones en globals().
    No modifica la capacidad.
    No convierte errores en resultados válidos.
    """
    if not callable(funcion):
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: capacidad '{nombre}' "
            "no está resuelta a callable"
        )

    args, kwargs = _preparar_argumentos_capacidad(
        nombre,
        funcion,
        peticion,
    )

    return funcion(*args, **kwargs)

# ===============================================================
# FIN 13.2
# ===============================================================


# ===============================================================
# 13.3 — EJECUTAR TOTAL
# ===============================================================

def ejecutar_total(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Autoridad total de ENGINE sobre DI.

    Fuente única:
        CONTENEDOR["capacidades"]

    Reglas:

    - Solo ejecuta capacidades declaradas.
    - Solo ejecuta callables ya resueltos.
    - No resuelve strings.
    - No utiliza globals() como mecanismo de resolución.
    - No autoinvoca ejecutar_total.
    - Ejecuta en orden determinista.
    - No confunde resultado None con fallo.
    - Registra separadamente capacidades ejecutadas y errores.
    - No inventa argumentos.
    """

    # ============================================================
    # 13.3.1 — NORMALIZACIÓN ESTRICTA DE PETICIÓN
    # ============================================================

    if peticion is None:
        peticion_normalizada: Dict[str, Any] = {}
    elif isinstance(peticion, dict):
        peticion_normalizada = dict(peticion)
    else:
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
                (
                    f"{NOMBRE_MODULO}: petición inválida; "
                    f"se esperaba dict y se recibió "
                    f"{type(peticion).__name__}"
                )
            ],
            "resultados": {},
            "capacidades_declaradas": [],
        }

    # ============================================================
    # 13.3.2 — OBTENCIÓN CONTRACTUAL DE CAPACIDADES
    # ============================================================

    capacidades = CONTENEDOR.get("capacidades")

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
                (
                    f"{NOMBRE_MODULO}: "
                    "CONTENEDOR['capacidades'] no es dict"
                )
            ],
            "resultados": {},
            "capacidades_declaradas": [],
        }

    # ============================================================
    # 13.3.3 — VERIFICACIÓN PREVIA DE CALLABLES
    # ============================================================

    capacidades_declaradas = sorted(capacidades.keys())
    errores_contractuales: List[str] = []

    for nombre in capacidades_declaradas:
        referencia = capacidades[nombre]

        if not isinstance(nombre, str) or not nombre.strip():
            errores_contractuales.append(
                f"{NOMBRE_MODULO}: identificador de capacidad inválido"
            )
            continue

        if not callable(referencia):
            errores_contractuales.append(
                f"{NOMBRE_MODULO}: capacidad '{nombre}' "
                "no está resuelta a callable"
            )

    if errores_contractuales:
        return {
            "id": ID_MODULO,
            "modulo": NOMBRE_MODULO,
            "rol": ROL_MODULO,
            "version": VERSION_MODULO,
            "operacion": "ejecutar_total",
            "estado": ESTADO_RECHAZADO,
            "coherente": False,
            "capacidades_ejecutadas": [],
            "errores_ejecucion": errores_contractuales,
            "resultados": {},
            "capacidades_declaradas": capacidades_declaradas,
        }

    # ============================================================
    # 13.3.4 — EJECUCIÓN DETERMINISTA
    # ============================================================

    resultados: Dict[str, Any] = {}
    capacidades_ejecutadas: List[str] = []
    errores_ejecucion: List[str] = []

    for nombre in capacidades_declaradas:

        # --------------------------------------------------------
        # ejecutar_total NO SE AUTOINVOCA
        # --------------------------------------------------------

        if nombre == "ejecutar_total":
            continue

        funcion = capacidades[nombre]

        try:
            resultado = _ejecutar_capacidad(
                nombre,
                funcion,
                peticion_normalizada,
            )

            # None puede ser una salida legítima.
            resultados[nombre] = resultado
            capacidades_ejecutadas.append(nombre)

        except Exception as exc:
            errores_ejecucion.append(
                f"{nombre}: {type(exc).__name__}: {exc}"
            )

            # Se conserva explícitamente la existencia del intento.
            resultados[nombre] = None

    # ============================================================
    # 13.3.5 — DETERMINACIÓN DE COHERENCIA
    # ============================================================

    barrido = resultados.get("barrer")

    barrer_ejecutado = "barrer" in capacidades_ejecutadas

    coherencia_datos = (
        isinstance(barrido, dict)
        and isinstance(barrido.get("coherente"), bool)
        and bool(barrido.get("coherente"))
    )

    if not barrer_ejecutado:
        coherente = False
    else:
        coherente = coherencia_datos and not errores_ejecucion

    # ============================================================
    # 13.3.6 — ESTADO FINAL
    # ============================================================

    if coherente:
        estado = ESTADO_OPERATIVO
    elif errores_ejecucion or not barrer_ejecutado:
        estado = ESTADO_DEGRADADO
    else:
        estado = ESTADO_DEGRADADO

    # ============================================================
    # 13.3.7 — SALIDA CONTRACTUAL
    # ============================================================

    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "operacion": "ejecutar_total",
        "estado": estado,
        "coherente": coherente,
        "capacidades_ejecutadas": sorted(capacidades_ejecutadas),
        "errores_ejecucion": errores_ejecucion,
        "resultados": resultados,
        "capacidades_declaradas": capacidades_declaradas,
    }

# ===============================================================
# FIN 13.3
# ===============================================================


# ===============================================================
# FIN 13 — EJECUTAR TOTAL
# ===============================================================

# ===============================================================
# 14 — INSPECCIONAR
# ===============================================================

def inspeccionar(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Inspección estructural de DI.
    Expone contrato, capacidades y estado estructural.
    Obtiene la evidencia de estado mediante barrer().
    No modifica el contrato ni las fuentes del módulo.
    """
    b = barrer()

    capacidades = CONTENEDOR.get("capacidades", {})
    capacidades_meta = CONTENEDOR.get("capacidades_meta", {})

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
        "capacidades_contractuales": (
            sorted(capacidades.keys())
            if isinstance(capacidades, dict)
            else []
        ),
        "capacidades_meta": (
            sorted(capacidades_meta.keys())
            if isinstance(capacidades_meta, dict)
            else []
        ),
        "integridad": {
            "coherente": b.get("coherente"),
            "errores": list(b.get("errores") or []),
            "diccionarios": list(b.get("diccionarios") or []),
            "total": b.get("total"),
            "por_idioma": dict(b.get("por_idioma") or {}),
        },
        "autoriza_engine": dict(
            CONTENEDOR.get("autoriza_engine") or {}
        ),
        "reporting": dict(
            CONTENEDOR.get("reporting") or {}
        ),
        "invariantes": list(INVARIANTES),
        "nota": (
            "Inspección estructural de DI. "
            "La evidencia de estado procede de barrer(). "
            "No modifica el contrato ni las fuentes."
        ),
    }

# ===============================================================
# FIN 14
# ===============================================================


# ===============================================================
# 15 — REGISTRAR INVENTARIO
# ===============================================================

def registrar_inventario(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Genera una instantánea determinista del inventario actual de DI.
    No persiste ni registra externamente la instantánea.
    No modifica fuentes, contrato ni evidencia.
    """
    inv = inventario(peticion)

    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "operacion": "registrar_inventario",
        "registrado": False,
        "inventario": inv,
        "nota": (
            "Instantánea determinista del inventario actual de DI. "
            "La capacidad no persiste la instantánea ni modifica "
            "fuentes, contrato o evidencia."
        ),
    }

# ===============================================================
# FIN 15
# ===============================================================


# ===============================================================
# FIN — CAPACIDADES PÚBLICAS
# ===============================================================
# ===============================================================
# 16 — VALIDACIÓN, RESOLUCIÓN Y EXPORTACIONES
# ===============================================================
# ===============================================================
# 16.1 — VALIDACIÓN DE CONTRATO
# ===============================================================

def _validar_contrato(cont: Dict[str, Any]) -> None:
    if not isinstance(cont, dict):
        raise ContratoInvalido(
            "{0}: CONTENEDOR debe ser dict".format(NOMBRE_MODULO)
        )

    obligatorias = (
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

    faltantes = [k for k in obligatorias if k not in cont]

    if faltantes:
        raise ContratoInvalido(
            "{0}: CONTENEDOR incompleto. Faltan: {1}".format(
                NOMBRE_MODULO,
                faltantes,
            )
        )

    if cont.get("esquema") != ESQUEMA_CONTRATO:
        raise ContratoInvalido(
            "{0}: esquema incompatible: {1}".format(
                NOMBRE_MODULO,
                cont.get("esquema"),
            )
        )

    if str(cont.get("version_contrato")) != VERSION_CONTRATO:
        raise ContratoInvalido(
            "{0}: version_contrato inválida: {1}".format(
                NOMBRE_MODULO,
                cont.get("version_contrato"),
            )
        )

    capacidades = cont.get("capacidades")
    capacidades_meta = cont.get("capacidades_meta")

    if not isinstance(capacidades, dict):
        raise ContratoInvalido(
            "{0}: CONTENEDOR['capacidades'] debe ser dict".format(
                NOMBRE_MODULO
            )
        )

    if not isinstance(capacidades_meta, dict):
        raise ContratoInvalido(
            "{0}: CONTENEDOR['capacidades_meta'] debe ser dict".format(
                NOMBRE_MODULO
            )
        )

    nombres_capacidades = set(capacidades.keys())
    nombres_meta = set(capacidades_meta.keys())

    sin_meta = sorted(nombres_capacidades - nombres_meta)
    meta_sin_capacidad = sorted(nombres_meta - nombres_capacidades)

    if sin_meta:
        raise ContratoInvalido(
            "{0}: capacidades sin capacidades_meta: {1}".format(
                NOMBRE_MODULO,
                sin_meta,
            )
        )

    if meta_sin_capacidad:
        raise ContratoInvalido(
            "{0}: capacidades_meta sin capacidad declarada: {1}".format(
                NOMBRE_MODULO,
                meta_sin_capacidad,
            )
        )

    capacidades_arquitectonicas = (
        "ejecutar_total",
        "inspeccionar",
        "registrar_inventario",
    )

    for nombre_cap in capacidades_arquitectonicas:
        if nombre_cap not in capacidades:
            raise ContratoInvalido(
                "{0}: capacidad arquitectónica obligatoria ausente: '{1}'".format(
                    NOMBRE_MODULO,
                    nombre_cap,
                )
            )

        if nombre_cap not in capacidades_meta:
            raise ContratoInvalido(
                "{0}: capacidad arquitectónica '{1}' sin capacidades_meta".format(
                    NOMBRE_MODULO,
                    nombre_cap,
                )
            )

    for nombre_cap in sorted(nombres_capacidades):
        ref = capacidades[nombre_cap]

        if not isinstance(ref, (str, type(lambda: None))):
            if not callable(ref):
                raise ContratoInvalido(
                    "{0}: capacidad '{1}' tiene referencia inválida: {2}".format(
                        NOMBRE_MODULO,
                        nombre_cap,
                        type(ref).__name__,
                    )
                )

        entrada = capacidades_meta[nombre_cap]

        if not isinstance(entrada, dict):
            raise ContratoInvalido(
                "{0}: capacidades_meta['{1}'] debe ser dict".format(
                    NOMBRE_MODULO,
                    nombre_cap,
                )
            )

        for campo in ("descripcion", "entrada", "salida"):
            if campo not in entrada:
                raise ContratoInvalido(
                    "{0}: capacidades_meta['{1}'] requiere '{2}'".format(
                        NOMBRE_MODULO,
                        nombre_cap,
                        campo,
                    )
                )

            if not isinstance(entrada[campo], str):
                raise ContratoInvalido(
                    "{0}: capacidades_meta['{1}']['{2}'] debe ser str".format(
                        NOMBRE_MODULO,
                        nombre_cap,
                        campo,
                    )
                )

            if not entrada[campo].strip():
                raise ContratoInvalido(
                    "{0}: capacidades_meta['{1}']['{2}'] no puede estar vacío".format(
                        NOMBRE_MODULO,
                        nombre_cap,
                        campo,
                    )
                )


# ===============================================================
# FIN 16.1
# ===============================================================


# ===============================================================
# 17 — MAPA DE CAPACIDADES
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

    # --- CAPACIDADES ARQUITECTÓNICAS ---
    "ejecutar_total": ejecutar_total,
    "inspeccionar": inspeccionar,
    "registrar_inventario": registrar_inventario,
}

# ===============================================================
# FIN 17
# ===============================================================


# ===============================================================
# 18 — RESOLUCIÓN DE CAPACIDADES
# ===============================================================

def _resolver_capacidades(cont: Dict[str, Any]) -> None:
    """
    Resuelve las referencias declaradas en CONTENEDOR["capacidades"]
    y garantiza que todas terminen como callables reales.

    Fuente de resolución:
        CONTENEDOR["capacidades"] → _CAP_MAP → callable

    No inventa capacidades.
    No agrega capacidades.
    No elimina capacidades.
    """

    capacidades = cont.get("capacidades")

    if not isinstance(capacidades, dict):
        raise ContratoInvalido(
            "{0}: CONTENEDOR['capacidades'] debe ser dict".format(
                NOMBRE_MODULO
            )
        )

    resueltas: Dict[str, Any] = {}

    for nombre, ref in capacidades.items():

        if callable(ref):
            resueltas[nombre] = ref
            continue

        if isinstance(ref, str):
            if ref not in _CAP_MAP:
                raise ContratoInvalido(
                    "{0}: capacidad '{1}' referencia inexistente: '{2}'".format(
                        NOMBRE_MODULO,
                        nombre,
                        ref,
                    )
                )

            fn = _CAP_MAP[ref]

            if not callable(fn):
                raise ContratoInvalido(
                    "{0}: referencia '{1}' de capacidad '{2}' no es callable".format(
                        NOMBRE_MODULO,
                        ref,
                        nombre,
                    )
                )

            resueltas[nombre] = fn
            continue

        raise ContratoInvalido(
            "{0}: capacidad '{1}' tipo inválido: {2}".format(
                NOMBRE_MODULO,
                nombre,
                type(ref).__name__,
            )
        )

    esperadas = set(capacidades.keys())
    obtenidas = set(resueltas.keys())

    faltantes = sorted(esperadas - obtenidas)
    inesperadas = sorted(obtenidas - esperadas)

    if faltantes:
        raise ContratoInvalido(
            "{0}: capacidades no resueltas: {1}".format(
                NOMBRE_MODULO,
                faltantes,
            )
        )

    if inesperadas:
        raise ContratoInvalido(
            "{0}: capacidades no declaradas resueltas: {1}".format(
                NOMBRE_MODULO,
                inesperadas,
            )
        )

    no_callable = sorted(
        nombre
        for nombre, fn in resueltas.items()
        if not callable(fn)
    )

    if no_callable:
        raise ContratoInvalido(
            "{0}: capacidades finales no callables: {1}".format(
                NOMBRE_MODULO,
                no_callable,
            )
        )

    cont["capacidades"] = resueltas


# ===============================================================
# FIN 18
# ===============================================================


# ===============================================================
# 19 — VALIDAR Y RESOLVER AL IMPORTAR
# ===============================================================

_validar_contrato(CONTENEDOR)
_resolver_capacidades(CONTENEDOR)

# ===============================================================
# FIN 19
# ===============================================================


# ===============================================================
# 20 — EXPORTACIONES
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
# FIN 20
# ===============================================================


# ===============================================================
# FIN 20 — VALIDACIÓN, RESOLUCIÓN Y EXPORTACIONES
# ===============================================================


# ===============================================================
# FIN DEL MÓDULO
# ===============================================================
