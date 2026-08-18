# ===============================================================
# VPSI-TRUTH — modules/citacion/__init__.py
# ===============================================================
#
# MÓDULO:              citacion
# ID:                  CIT
# Rol:                 CIT
# Versión módulo:      2.0
# Versión contrato:    1.0
# Esquema contrato:    VPSI-CONTRACT-1.0
# Estabilidad:         ESTABLE
# Compatible desde:    1.0
# API Engine:          >=1.0
#
# ---------------------------------------------------------------
# PRINCIPIO FUNDAMENTAL
# ---------------------------------------------------------------
#
# CIT no calcula.
# CIT no decide.
# CIT no interpreta.
# CIT no modifica.
# CIT no crea conocimiento.
#
# CIT conoce, resuelve, relaciona y cita.
#
# Toda declaración formal del VPSI debe poder ser resuelta por CIT.
#
# ---------------------------------------------------------------
# DEFINICIÓN
# ---------------------------------------------------------------
#
# CIT es la autoridad universal de fundamentación del VPSI.
#
# Conserva conocimiento resoluble de todas las declaraciones
# públicas existentes dentro del sistema.
#
# Puede resolver, relacionar y citar cualquier axioma, teorema,
# definición, corolario, fórmula, contexto, regla, correlación
# o declaración formal proveniente de cualquier módulo presente
# o futuro.
#
# Su autoridad es absoluta sobre la fundamentación.
# No posee autoridad para alterar el conocimiento.
#
# ---------------------------------------------------------------
# MODELO CONCEPTUAL
# ---------------------------------------------------------------
#
#   Declaración
#        ↓
#   Resolución
#        ↓
#   Relación
#        ↓
#   Cadena normativa
#        ↓
#   Citación
#        ↓
#   Explicación
#
# Internamente CIT administra declaraciones.
# Las citas son únicamente una representación de esas declaraciones.
#
# ---------------------------------------------------------------
# OFICIO ÚNICO
# ---------------------------------------------------------------
#
# Resolver, organizar, relacionar y citar cualquier declaración
# pública perteneciente al VPSI.
#
# ---------------------------------------------------------------
# RESTRICCIÓN ÚNICA
# ---------------------------------------------------------------
#
# Ninguna capacidad de CIT puede modificar el conocimiento declarado.
#
# ---------------------------------------------------------------
# DOS MODOS
# ---------------------------------------------------------------
#
# Modo Engine
#   Engine solicita fundamentación del ciclo.
#   CIT devuelve la cadena documental utilizada.
#
# Modo Consulta
#   Se solicita conocimiento ("Cítame TA-7", "¿Qué dice Def-5.3.1?").
#   El mismo motor responde.
#
# ---------------------------------------------------------------
# ESCALABILIDAD
# ---------------------------------------------------------------
#
# CIT nunca crece en lógica.
# Crece únicamente en conocimiento declarado.
# Todo módulo presente o futuro puede registrar declaraciones
# públicas; CIT las incorpora sin modificar este INIT.
#
# ===============================================================

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

# ===============================================================
# FIN PARTE 1
# ===============================================================


# ===============================================================
# PARTE 2 — IDENTIDAD
# ===============================================================

_ID = "CIT"
_NOMBRE = "citacion"
_ROL = "CIT"
_VERSION = "2.0"
_VERSION_CONTRATO = "1.0"
_ESQUEMA = "VPSI-CONTRACT-1.0"
_ESTABILIDAD = "ESTABLE"
_COMPATIBLE_DESDE = "1.0"
_API_ENGINE = ">=1.0"

ID_MODULO = _ID
NOMBRE_MODULO = _NOMBRE
ROL_MODULO = _ROL
VERSION_MODULO = _VERSION
VERSION_CONTRATO = _VERSION_CONTRATO
ESQUEMA_CONTRATO = _ESQUEMA
ESTABILIDAD = _ESTABILIDAD

ESTADO_OPERATIVO = "OPERATIVO"
ESTADO_DEGRADADO = "DEGRADADO"
ESTADOS_VALIDOS = (
    "NO_INICIADO",
    ESTADO_OPERATIVO,
    ESTADO_DEGRADADO,
    "RECHAZADO",
)

# ===============================================================
# FIN PARTE 2
# ===============================================================


# ===============================================================
# PARTE 3 — UNIVERSO DECLARATIVO
# ===============================================================

TIPOS_DECLARACION = (
    "axioma", "teorema", "definicion", "corolario", "lema",
    "regla", "principio", "formula", "correlacion", "contexto",
    "limite", "factor", "procedimiento", "contrato", "invariante",
    "capacidad", "evidencia", "citacion",
    "ax", "mc", "cx", "tx", "ca", "fo", "re", "ct", "ch", "sf",
)

RELACIONES = (
    "depende_de", "fundamenta", "contradice", "extiende",
    "deriva_de", "correlaciona_con", "limita", "activa",
    "desactiva", "requiere", "gobierna",
)

CAMPOS_OBLIGATORIOS = ("id", "tipo", "fuente", "enunciado")

CAMPOS_OPCIONALES = (
    "descripcion", "evidencia_ref", "o_ref", "contexto_ciclo",
    "meta", "relaciones", "fuente_modulo",
)

INVARIANTES = (
    "el id del módulo nunca cambia",
    "el rol nunca cambia",
    "CIT no modifica el conocimiento declarado",
    "CIT no calcula",
    "CIT no interpreta",
    "las capacidades declaradas son callables tras la resolución",
    "este módulo no inventa capacidades no declaradas en CONTENEDOR",
)

# ===============================================================
# FIN PARTE 3
# ===============================================================


# ===============================================================
# PARTE 4 — ESTADO OPERATIVO (registro de ciclo)
# ===============================================================

_REGISTRO: Dict[str, Dict[str, Any]] = {}

# ===============================================================
# FIN PARTE 4
# ===============================================================


# ===============================================================
# PARTE 5 — CONTRATO (CONTENEDOR)
# ===============================================================

CONTENEDOR: Dict[str, Any] = {

    # ===========================================================
    # 5.1 — ESQUEMA E IDENTIDAD
    # ===========================================================
    "esquema": _ESQUEMA,
    "version_contrato": _VERSION_CONTRATO,
    "version_modulo": _VERSION,
    "id": _ID,
    "nombre": _NOMBRE,
    "rol": _ROL,
    "estabilidad": _ESTABILIDAD,
    "compatible_desde": _COMPATIBLE_DESDE,
    "api_engine": _API_ENGINE,

    # ===========================================================
    # 5.2 — DESCRIPCIÓN Y FUNCIÓN
    # ===========================================================
    "descripcion": (
        "Autoridad universal de fundamentación del VPSI. "
        "Conserva conocimiento resoluble de todas las declaraciones "
        "públicas del sistema. Resuelve, relaciona y cita. "
        "No altera el conocimiento declarado."
    ),
    "funcion": (
        "Resolver, organizar, relacionar y citar cualquier declaración "
        "pública perteneciente al VPSI. "
        "Modo Engine: cadena documental del ciclo. "
        "Modo Consulta: resolución y explicación bajo demanda."
    ),
    "no_hace": [
        "Ninguna capacidad de CIT puede modificar el conocimiento declarado",
        "No calcula",
        "No interpreta",
        "No decide",
    ],
    "autoridad": [
        "Fundamentación",
        "Resolución de declaraciones",
        "Citación",
        "Cadena normativa",
        "Explicación documental",
        "Relación entre declaraciones",
        "Consultas sobre conocimiento declarado",
    ],
    "conocimiento_exportable": [
        "declaraciones", "resolver", "buscar", "cadena", "explicar",
        "citar", "anunciar", "relacionar", "inventario", "reporte",
        "diagnostico", "ejecutar_total", "inspeccionar",
        "registrar_inventario",
    ],

    # ===========================================================
    # 5.3 — ACCESO Y DEPENDENCIAS
    # ===========================================================
    "acceso": {
        "nivel": "completo",
        "descripcion": "Acceso total a recursos del módulo",
    },
    "requiere": [
        "CE", "AX", "FO", "MC", "SF",
        "CA", "CX", "DI", "RE", "VX",
        "TX", "CH", "DGCO", "UI",
        "CC", "TT", "SC", "CT",
    ],
    "acceso_archivos": ["*"],
    "validar_esquema": ["*"],

    # ===========================================================
    # 5.4 — AUTORIZA ENGINE
    # ===========================================================
    "autoriza_engine": {
        "leer": True,
        "ejecutar": True,
        "consultar": True,
        "recombinar": True,
        "reportar": True,
        "auditar": True,
        "inventariar": True,
        "alterar": False,
        "crear": True,
        "actualizar": False,
        "validar": True,
        "procesar": True,
        "analizar": True,
        "generar": True,
        "exportar": True,
        "importar": True,
        "respaldar": True,
        "recuperar": True,
        "sincronizar": True,
        "monitorear": True,
        "metricas": True,
        "diagnostico": True,
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
        "validar_esquema": True,
        "acceso_archivos": True,
        "ejecutar_total": True,
        "inspeccionar": True,
        "registrar_inventario": True,
    },

    # ===========================================================
    # 5.5 — CONSULTAS SOPORTADAS
    # ===========================================================
    "consultas_soportadas": [
        "resolver", "buscar", "buscar_por_tipo", "buscar_por_fuente",
        "cadena", "explicar", "citar", "anunciar", "relacionar",
        "obtener_inventario", "obtener_reporte", "obtener_diagnostico",
        "ejecutar_total", "inspeccionar", "registrar_inventario",
    ],

    # ===========================================================
    # 5.6 — CAPACIDADES (solo strings; resolución al final)
    # ===========================================================
    "capacidades": {
        "verificar": "verificar",
        "barrer": "barrer",
        "verificar_salida": "verificar_salida",
        "inventario": "inventario",
        "reporte": "reporte",
        "diagnostico": "diagnostico",
        "anunciar": "anunciar",
        "anunciar_todo": "anunciar_todo",
        "citar": "citar",
        "registrar": "registrar",
        "resolver": "resolver",
        "resolver_enunciado": "resolver_enunciado",
        "buscar": "buscar",
        "cadena": "cadena",
        "explicar": "explicar",
        "relacionar": "relacionar",
        "limpiar_ciclo": "limpiar_ciclo",
        "evaluar": "anunciar",
        "ejecutar_total": "ejecutar_total",
        "inspeccionar": "inspeccionar",
        "registrar_inventario": "registrar_inventario",
    },

    # ===========================================================
    # 5.7 — CAPACIDADES META (1:1)
    # ===========================================================
    "capacidades_meta": {
        "verificar": {
            "descripcion": "Centinela del oficio de fundamentación.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con id, coherente, errores, choques",
            "acceso_archivos": ["*"],
        },
        "barrer": {
            "descripcion": "Alias de verificar.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con id, coherente, errores, choques",
            "acceso_archivos": ["*"],
        },
        "verificar_salida": {
            "descripcion": "Forma mínima de salida de CIT.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "bool",
            "acceso_archivos": ["*"],
        },
        "inventario": {
            "descripcion": "Inventario contractual de CIT.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con id, nombre, rol, version, capacidades",
            "acceso_archivos": ["*"],
        },
        "reporte": {
            "descripcion": "Reporte de estado de CIT.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con id, estado, coherente",
            "acceso_archivos": ["*"],
        },
        "diagnostico": {
            "descripcion": "Diagnóstico propio de CIT.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con id, estado, problemas, advertencias",
            "acceso_archivos": ["*"],
        },
        "anunciar": {
            "descripcion": "Fundamentación documental sin recálculo.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con anuncio o anuncios",
            "acceso_archivos": ["*"],
        },
        "anunciar_todo": {
            "descripcion": "Anuncia todas las declaraciones del registro.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con anuncios, n",
            "acceso_archivos": ["*"],
        },
        "citar": {
            "descripcion": "Representación citable de declaraciones.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con citas, n",
            "acceso_archivos": ["*"],
        },
        "registrar": {
            "descripcion": "Incorpora declaración al registro operativo.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con ok, declaracion",
            "acceso_archivos": ["*"],
        },
        "resolver": {
            "descripcion": "Resuelve una declaración por id.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con resuelto, declaracion",
            "acceso_archivos": ["*"],
        },
        "resolver_enunciado": {
            "descripcion": "Alias de resolución orientado a enunciado.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con resuelto, enunciado",
            "acceso_archivos": ["*"],
        },
        "buscar": {
            "descripcion": "Consulta declaraciones del registro operativo.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con declaraciones, n",
            "acceso_archivos": ["*"],
        },
        "cadena": {
            "descripcion": "Construye cadena normativa de ids resolubles.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con cadena, faltantes, completa",
            "acceso_archivos": ["*"],
        },
        "explicar": {
            "descripcion": "Explicación documental con declaraciones existentes.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con explicacion, n, completa",
            "acceso_archivos": ["*"],
        },
        "relacionar": {
            "descripcion": "Documenta relación entre dos declaraciones.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con ok, declaracion de enlace",
            "acceso_archivos": ["*"],
        },
        "limpiar_ciclo": {
            "descripcion": "Limpia registro operativo del ciclo.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con ok, limpiadas",
            "acceso_archivos": ["*"],
        },
        "evaluar": {
            "descripcion": "Alias de anunciar (compatibilidad Engine).",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict de anuncio / fundamentación",
            "acceso_archivos": ["*"],
        },
        "ejecutar_total": {
            "descripcion": (
                "Autoridad total de ENGINE sobre CIT. "
                "Ejerce todas las unidades ejecutables. No inventa."
            ),
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["*"],
            "salida": "dict con resultados de todas las unidades",
            "acceso_archivos": ["*"],
        },
        "inspeccionar": {
            "descripcion": (
                "Inspección estructural de CIT sin alterar contrato."
            ),
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["acceso_archivos"],
            "salida": "dict con estructura y estado",
            "acceso_archivos": ["acceso_archivos"],
        },
        "registrar_inventario": {
            "descripcion": (
                "Instantánea determinista del inventario de CIT."
            ),
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["acceso_archivos"],
            "salida": "dict con inventario registrado",
            "acceso_archivos": ["acceso_archivos"],
        },
    },

    # ===========================================================
    # 5.8 — REPORTING
    # ===========================================================
    "reporting": {
        "estado": True,
        "salud": True,
        "inventario": True,
        "capacidades": True,
        "errores": True,
        "advertencias": True,
        "dependencias": True,
        "version": True,
        "contrato": True,
        "conocimiento": True,
        "metricas": True,
        "diagnostico": True,
        "reporte": True,
        "acceso_archivos": True,
        "validar_esquema": True,
        "ejecutar_total": True,
        "inspeccionar": True,
        "registrar_inventario": True,
    },

    # ===========================================================
    # 5.9 — ESTADOS E INVARIANTES
    # ===========================================================
    "estados_validos": list(ESTADOS_VALIDOS),
    "invariantes": list(INVARIANTES),
}

# ===============================================================
# FIN PARTE 5
# ===============================================================


# ===============================================================
# PARTE 6 — HELPERS PRIVADOS
# ===============================================================

def _norm_id(valor: Any) -> str:
    return str(valor or "").strip()


def _es_declaracion(d: Any) -> bool:
    if not isinstance(d, dict):
        return False
    return all(k in d and str(d.get(k) or "").strip() for k in CAMPOS_OBLIGATORIOS)

# ===============================================================
# FIN PARTE 6
# ===============================================================


# ===============================================================
# PARTE 7 — CENTINELA
# ===============================================================

def verificar(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Centinela del oficio de fundamentación de CIT."""
    errores: List[str] = []
    choques: List[str] = []
    capacidades = CONTENEDOR.get("capacidades") or {}
    metas = CONTENEDOR.get("capacidades_meta") or {}

    if not isinstance(capacidades, dict):
        errores.append("CONTENEDOR['capacidades'] no es dict")
        capacidades = {}
    if not isinstance(metas, dict):
        errores.append("CONTENEDOR['capacidades_meta'] no es dict")
        metas = {}

    for nombre in capacidades:
        if nombre not in metas:
            errores.append("capacidad sin capacidades_meta: {0}".format(nombre))
    for nombre in metas:
        if nombre not in capacidades:
            errores.append("capacidades_meta sin capacidad: {0}".format(nombre))

    for nombre, ref in capacidades.items():
        if callable(ref):
            continue
        if isinstance(ref, str):
            if not callable(globals().get(ref)):
                errores.append(
                    "capacidad no resoluble a callable: {0}".format(nombre)
                )
            continue
        errores.append(
            "capacidad tipo inválido: {0} ({1})".format(
                nombre, type(ref).__name__
            )
        )

    coherente = not errores and not choques
    return {
        "id": _ID,
        "modulo": _NOMBRE,
        "rol": _ROL,
        "version": _VERSION,
        "coherente": coherente,
        "errores": errores,
        "choques": choques,
        "capacidades_n": len(capacidades),
        "capacidades_meta_n": len(metas),
        "registro_n": len(_REGISTRO),
        "nota": "Centinela CIT. No modifica conocimiento declarado.",
    }


def barrer(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Alias de verificar."""
    return verificar(peticion)


def verificar_salida(salida: Any) -> bool:
    """Forma mínima de una salida de CIT."""
    if not isinstance(salida, dict):
        return False
    return any(
        k in salida
        for k in (
            "id", "coherente", "ok", "resuelto", "declaraciones",
            "cadena", "citas", "anuncios", "explicacion",
            "registrado", "operacion",
        )
    )

# ===============================================================
# FIN PARTE 7
# ===============================================================


# ===============================================================
# PARTE 8 — REPORTING
# ===============================================================

def inventario(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Inventario contractual de CIT."""
    capacidades = CONTENEDOR.get("capacidades") or {}
    return {
        "id": _ID,
        "nombre": _NOMBRE,
        "rol": _ROL,
        "version": _VERSION,
        "version_contrato": _VERSION_CONTRATO,
        "esquema": _ESQUEMA,
        "estabilidad": _ESTABILIDAD,
        "compatible_desde": _COMPATIBLE_DESDE,
        "api_engine": _API_ENGINE,
        "capacidades": list(capacidades.keys()),
        "tipos_declaracion": list(TIPOS_DECLARACION),
        "relaciones": list(RELACIONES),
        "campos_obligatorios": list(CAMPOS_OBLIGATORIOS),
        "campos_opcionales": list(CAMPOS_OPCIONALES),
        "registro_n": len(_REGISTRO),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "conocimiento_exportable": list(
            CONTENEDOR.get("conocimiento_exportable") or []
        ),
        "autoridad": list(CONTENEDOR.get("autoridad") or []),
        "funcion": CONTENEDOR.get("funcion"),
        "nota": "Inventario estructural de CIT.",
    }


def reporte(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Reporte de estado de CIT."""
    b = verificar()
    capacidades = CONTENEDOR.get("capacidades") or {}
    return {
        "id": _ID,
        "modulo": _NOMBRE,
        "rol": _ROL,
        "version": _VERSION,
        "version_contrato": _VERSION_CONTRATO,
        "esquema": _ESQUEMA,
        "estabilidad": _ESTABILIDAD,
        "estado": ESTADO_OPERATIVO if b.get("coherente") else ESTADO_DEGRADADO,
        "coherente": b.get("coherente"),
        "errores": b.get("errores"),
        "choques": b.get("choques"),
        "capacidades_n": b.get("capacidades_n"),
        "registro_n": len(_REGISTRO),
        "capacidades": list(capacidades.keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "operaciones_arquitectonicas": {
            "ejecutar_total": True,
            "inspeccionar": True,
            "registrar_inventario": True,
        },
        "nota": "Reporte de estado de CIT.",
    }


def diagnostico(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Diagnóstico propio de CIT."""
    b = verificar()
    problemas = list(b.get("errores") or [])
    advertencias = list(b.get("choques") or [])
    recomendaciones: List[str] = []
    if not problemas and not advertencias:
        recomendaciones.append("CIT coherente")
    if len(_REGISTRO) == 0:
        advertencias.append("registro operativo vacío")
    return {
        "id": _ID,
        "modulo": _NOMBRE,
        "estado": ESTADO_OPERATIVO if b.get("coherente") else ESTADO_DEGRADADO,
        "problemas": problemas,
        "advertencias": advertencias,
        "recomendaciones": recomendaciones,
        "coherente": b.get("coherente"),
        "registro_n": len(_REGISTRO),
    }

# ===============================================================
# FIN PARTE 8
# ===============================================================


# ===============================================================
# CALLABLES — 1:1 CON CAPACIDADES META
# ===============================================================

# ---------------------------------------------------------------
# 1. verificar
# ---------------------------------------------------------------
def verificar(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    errores: List[str] = []
    choques: List[str] = []
    capacidades = CONTENEDOR.get("capacidades") or {}
    metas = CONTENEDOR.get("capacidades_meta") or {}
    if not isinstance(capacidades, dict):
        errores.append("CONTENEDOR['capacidades'] no es dict")
        capacidades = {}
    if not isinstance(metas, dict):
        errores.append("CONTENEDOR['capacidades_meta'] no es dict")
        metas = {}
    for nombre in capacidades:
        if nombre not in metas:
            errores.append("capacidad sin capacidades_meta: {0}".format(nombre))
    for nombre in metas:
        if nombre not in capacidades:
            errores.append("capacidades_meta sin capacidad: {0}".format(nombre))
    for nombre, ref in capacidades.items():
        if callable(ref):
            continue
        if isinstance(ref, str):
            if not callable(globals().get(ref)):
                errores.append("capacidad no resoluble a callable: {0}".format(nombre))
            continue
        errores.append("capacidad tipo inválido: {0}".format(nombre))
    coherente = not errores and not choques
    return {
        "id": _ID,
        "modulo": _NOMBRE,
        "rol": _ROL,
        "version": _VERSION,
        "coherente": coherente,
        "errores": errores,
        "choques": choques,
        "capacidades_n": len(capacidades),
        "capacidades_meta_n": len(metas),
        "registro_n": len(_REGISTRO),
    }


# ---------------------------------------------------------------
# 2. barrer
# ---------------------------------------------------------------
def barrer(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return verificar(peticion)


# ---------------------------------------------------------------
# 3. verificar_salida
# ---------------------------------------------------------------
def verificar_salida(salida: Any) -> bool:
    if not isinstance(salida, dict):
        return False
    return any(
        k in salida for k in (
            "id", "coherente", "ok", "resuelto", "declaraciones",
            "cadena", "citas", "anuncios", "explicacion",
            "registrado", "operacion",
        )
    )


# ---------------------------------------------------------------
# 4. inventario
# ---------------------------------------------------------------
def inventario(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    capacidades = CONTENEDOR.get("capacidades") or {}
    return {
        "id": _ID,
        "nombre": _NOMBRE,
        "rol": _ROL,
        "version": _VERSION,
        "version_contrato": _VERSION_CONTRATO,
        "esquema": _ESQUEMA,
        "estabilidad": _ESTABILIDAD,
        "capacidades": list(capacidades.keys()),
        "tipos_declaracion": list(TIPOS_DECLARACION),
        "relaciones": list(RELACIONES),
        "campos_obligatorios": list(CAMPOS_OBLIGATORIOS),
        "registro_n": len(_REGISTRO),
        "requiere": list(CONTENEDOR.get("requiere") or []),
    }


# ---------------------------------------------------------------
# 5. reporte
# ---------------------------------------------------------------
def reporte(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    b = verificar()
    return {
        "id": _ID,
        "modulo": _NOMBRE,
        "rol": _ROL,
        "version": _VERSION,
        "estado": "OPERATIVO" if b.get("coherente") else "DEGRADADO",
        "coherente": b.get("coherente"),
        "errores": b.get("errores"),
        "choques": b.get("choques"),
        "registro_n": len(_REGISTRO),
        "capacidades": list((CONTENEDOR.get("capacidades") or {}).keys()),
    }


# ---------------------------------------------------------------
# 6. diagnostico
# ---------------------------------------------------------------
def diagnostico(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    b = verificar()
    problemas = list(b.get("errores") or [])
    advertencias = list(b.get("choques") or [])
    if len(_REGISTRO) == 0:
        advertencias.append("registro operativo vacío")
    return {
        "id": _ID,
        "modulo": _NOMBRE,
        "estado": "OPERATIVO" if b.get("coherente") else "DEGRADADO",
        "problemas": problemas,
        "advertencias": advertencias,
        "recomendaciones": [] if problemas else ["CIT coherente"],
        "coherente": b.get("coherente"),
        "registro_n": len(_REGISTRO),
    }


# ---------------------------------------------------------------
# 7. registrar
# ---------------------------------------------------------------
def registrar(declaracion: Any = None) -> Dict[str, Any]:
    if not isinstance(declaracion, dict):
        return {"id": _ID, "ok": False, "errores": ["declaracion debe ser dict"], "declaracion": None}
    for k in CAMPOS_OBLIGATORIOS:
        if not str(declaracion.get(k) or "").strip():
            return {"id": _ID, "ok": False, "errores": ["falta campo: {0}".format(k)], "declaracion": None}
    d = dict(declaracion)
    clave = str(d.get("id") or "").strip()
    _REGISTRO[clave] = d
    return {"id": _ID, "ok": True, "declaracion": d, "registro_n": len(_REGISTRO)}


# ---------------------------------------------------------------
# 8. resolver
# ---------------------------------------------------------------
def resolver(id_decl: Any = None) -> Dict[str, Any]:
    clave = str(id_decl or "").strip()
    if not clave:
        return {"id": _ID, "resuelto": False, "declaracion": None, "errores": ["id vacío"]}
    d = _REGISTRO.get(clave)
    if d is None:
        return {"id": _ID, "resuelto": False, "declaracion": None, "errores": ["no encontrado: {0}".format(clave)]}
    return {"id": _ID, "resuelto": True, "declaracion": dict(d)}


# ---------------------------------------------------------------
# 9. resolver_enunciado
# ---------------------------------------------------------------
def resolver_enunciado(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    p = dict(peticion or {})
    r = resolver(p.get("id") or p.get("enunciado_id"))
    if not r.get("resuelto"):
        return {"id": _ID, "resuelto": False, "enunciado": None, "errores": r.get("errores")}
    d = r.get("declaracion") or {}
    return {"id": _ID, "resuelto": True, "enunciado": d.get("enunciado"), "declaracion": d}


# ---------------------------------------------------------------
# 10. buscar
# ---------------------------------------------------------------
def buscar(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    if peticion is not None and not isinstance(peticion, dict):
        return {"id": _ID, "ok": False, "declaraciones": [], "n": 0, "errores": ["peticion debe ser dict o None"]}
    filtro = dict(peticion or {})
    tipo = filtro.get("tipo")
    fuente = filtro.get("fuente") or filtro.get("modulo")
    texto = str(filtro.get("texto") or "").strip().lower()
    id_exacto = str(filtro.get("id") or "").strip()
    resultados: List[Dict[str, Any]] = []
    for clave, d in _REGISTRO.items():
        if id_exacto and clave != id_exacto:
            continue
        if tipo and str(d.get("tipo") or "") != str(tipo):
            continue
        if fuente and str(d.get("fuente") or "") != str(fuente):
            continue
        if texto:
            blob = " ".join(str(d.get(k) or "") for k in ("id", "tipo", "fuente", "enunciado", "descripcion")).lower()
            if texto not in blob:
                continue
        resultados.append(dict(d))
    return {"id": _ID, "ok": True, "declaraciones": resultados, "n": len(resultados)}


# ---------------------------------------------------------------
# 11. cadena
# ---------------------------------------------------------------
def cadena(ids: Optional[List[str]] = None) -> Dict[str, Any]:
    if ids is None:
        secuencia: List[Any] = []
    elif isinstance(ids, list):
        secuencia = list(ids)
    else:
        return {"id": _ID, "ok": False, "cadena": [], "n": 0, "faltantes": [], "completa": False, "errores": ["ids debe ser list o None"]}
    eslabones: List[Dict[str, Any]] = []
    faltantes: List[str] = []
    for elemento in secuencia:
        clave = str(elemento or "").strip()
        if not clave:
            faltantes.append(clave)
            continue
        r = resolver(clave)
        if r.get("resuelto") and isinstance(r.get("declaracion"), dict):
            eslabones.append(r["declaracion"])
        else:
            faltantes.append(clave)
    return {
        "id": _ID,
        "ok": True,
        "cadena": eslabones,
        "n": len(eslabones),
        "faltantes": faltantes,
        "completa": len(faltantes) == 0 and len(eslabones) > 0,
    }


# ---------------------------------------------------------------
# 12. explicar
# ---------------------------------------------------------------
def explicar(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    if peticion is not None and not isinstance(peticion, dict):
        return {"id": _ID, "ok": False, "explicacion": [], "n": 0, "faltantes": [], "completa": False, "errores": ["peticion debe ser dict o None"]}
    filtro = dict(peticion or {})
    ids = filtro.get("ids")
    if ids is None:
        ids = filtro.get("cadena")
    if ids is not None:
        if isinstance(ids, str):
            ids = [ids]
        if not isinstance(ids, list):
            return {"id": _ID, "ok": False, "explicacion": [], "n": 0, "faltantes": [], "completa": False, "errores": ["ids/cadena debe ser list o str"]}
        rc = cadena(list(ids))
        return {
            "id": _ID,
            "ok": True,
            "explicacion": rc.get("cadena") or [],
            "n": rc.get("n") or 0,
            "faltantes": rc.get("faltantes") or [],
            "completa": bool(rc.get("completa")),
        }
    rb = buscar(filtro)
    decls = rb.get("declaraciones") or []
    return {
        "id": _ID,
        "ok": bool(rb.get("ok")),
        "explicacion": decls,
        "n": len(decls),
        "faltantes": [],
        "completa": len(decls) > 0,
    }


# ---------------------------------------------------------------
# 13. citar
# ---------------------------------------------------------------
def citar(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    rb = buscar(peticion if isinstance(peticion, dict) else {})
    citas = [
        {"id": d.get("id"), "tipo": d.get("tipo"), "fuente": d.get("fuente"), "enunciado": d.get("enunciado")}
        for d in (rb.get("declaraciones") or [])
    ]
    return {"id": _ID, "ok": True, "citas": citas, "n": len(citas)}


# ---------------------------------------------------------------
# 14. anunciar
# ---------------------------------------------------------------
def anunciar(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    p = dict(peticion or {}) if isinstance(peticion, dict) else {}
    if "ids" in p or "cadena" in p:
        rc = cadena(p.get("ids") or p.get("cadena"))
        return {
            "id": _ID,
            "ok": True,
            "anuncio": rc.get("cadena") or [],
            "n": rc.get("n") or 0,
            "completa": bool(rc.get("completa")),
            "faltantes": rc.get("faltantes") or [],
        }
    if p.get("id"):
        r = resolver(p.get("id"))
        return {
            "id": _ID,
            "ok": bool(r.get("resuelto")),
            "anuncio": r.get("declaracion"),
            "resuelto": r.get("resuelto"),
            "errores": r.get("errores"),
        }
    rb = buscar(p)
    return {"id": _ID, "ok": True, "anuncios": rb.get("declaraciones") or [], "n": rb.get("n") or 0}


# ---------------------------------------------------------------
# 15. anunciar_todo
# ---------------------------------------------------------------
def anunciar_todo(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    anuncios = [dict(d) for d in _REGISTRO.values()]
    return {"id": _ID, "ok": True, "anuncios": anuncios, "n": len(anuncios)}


# ---------------------------------------------------------------
# 16. relacionar
# ---------------------------------------------------------------
def relacionar(id_a: Any = None, relacion: Any = None, id_b: Any = None) -> Dict[str, Any]:
    ra = resolver(id_a)
    rb = resolver(id_b)
    if not ra.get("resuelto") or not rb.get("resuelto"):
        return {"id": _ID, "ok": False, "errores": ["una o ambas declaraciones no resolubles"], "declaracion": None}
    rel = str(relacion or "").strip()
    if rel and rel not in RELACIONES:
        return {"id": _ID, "ok": False, "errores": ["relacion no admitida: {0}".format(rel)], "declaracion": None}
    a = str(id_a or "").strip()
    b = str(id_b or "").strip()
    enlace = {
        "id": "REL-{0}-{1}-{2}".format(a, rel or "relacion", b),
        "tipo": "citacion",
        "fuente": _NOMBRE,
        "enunciado": "{0} {1} {2}".format(a, rel or "relacion", b),
        "relaciones": {"desde": a, "relacion": rel, "hacia": b},
    }
    _REGISTRO[str(enlace["id"])] = enlace
    return {"id": _ID, "ok": True, "declaracion": enlace}


# ---------------------------------------------------------------
# 17. limpiar_ciclo
# ---------------------------------------------------------------
def limpiar_ciclo(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    n = len(_REGISTRO)
    _REGISTRO.clear()
    return {"id": _ID, "ok": True, "limpiadas": n, "registro_n": 0}


# ---------------------------------------------------------------
# 18. evaluar  (alias → anunciar)
# ---------------------------------------------------------------
def evaluar(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return anunciar(peticion)


# ---------------------------------------------------------------
# 19. ejecutar_total
# ---------------------------------------------------------------
def ejecutar_total(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    pet = dict(peticion) if isinstance(peticion, dict) else {}
    caps = list((CONTENEDOR.get("capacidades") or {}).keys())
    resultados: Dict[str, Any] = {}
    ejecutadas: List[str] = []
    errores_ejecucion: List[Dict[str, Any]] = []
    for nombre in caps:
        if nombre == "ejecutar_total":
            continue
        fn = CONTENEDOR["capacidades"].get(nombre)
        if not callable(fn):
            errores_ejecucion.append({"capacidad": nombre, "error": "no callable"})
            continue
        try:
            if nombre in (
                "verificar", "barrer", "inventario", "reporte", "diagnostico",
                "anunciar", "anunciar_todo", "buscar", "citar", "resolver_enunciado",
                "explicar", "limpiar_ciclo", "evaluar", "inspeccionar", "registrar_inventario",
            ):
                resultados[nombre] = fn(pet)
            elif nombre == "verificar_salida":
                resultados[nombre] = fn(pet.get("salida"))
            elif nombre == "registrar":
                resultados[nombre] = fn(pet.get("declaracion"))
            elif nombre == "resolver":
                resultados[nombre] = fn(pet.get("id"))
            elif nombre == "cadena":
                resultados[nombre] = fn(pet.get("ids"))
            elif nombre == "relacionar":
                resultados[nombre] = fn(pet.get("id_a"), pet.get("relacion"), pet.get("id_b"))
            else:
                resultados[nombre] = fn()
            ejecutadas.append(nombre)
        except Exception as exc:
            errores_ejecucion.append({"capacidad": nombre, "error": "{0}: {1}".format(type(exc).__name__, exc)})
    coherente = len(errores_ejecucion) == 0
    return {
        "id": _ID,
        "modulo": _NOMBRE,
        "operacion": "ejecutar_total",
        "estado": "OPERATIVO" if coherente else "DEGRADADO",
        "coherente": coherente,
        "capacidades_ejecutadas": ejecutadas,
        "errores_ejecucion": errores_ejecucion,
        "resultados": resultados,
        "capacidades_declaradas": caps,
    }


# ---------------------------------------------------------------
# 20. inspeccionar
# ---------------------------------------------------------------
def inspeccionar(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    capacidades = CONTENEDOR.get("capacidades") or {}
    metas = CONTENEDOR.get("capacidades_meta") or {}
    errores: List[str] = []
    resolubles = [n for n, r in capacidades.items() if callable(r)]
    no_resolubles = [n for n in capacidades if n not in resolubles]
    sin_meta = [n for n in capacidades if n not in metas]
    metas_sin = [n for n in metas if n not in capacidades]
    errores.extend("capacidad no resoluble: {0}".format(n) for n in no_resolubles)
    errores.extend("capacidad sin meta: {0}".format(n) for n in sin_meta)
    errores.extend("meta sin capacidad: {0}".format(n) for n in metas_sin)
    coherente = not errores
    return {
        "id": _ID,
        "modulo": _NOMBRE,
        "operacion": "inspeccionar",
        "estado": "OPERATIVO" if coherente else "DEGRADADO",
        "coherente": coherente,
        "capacidades_contractuales": list(capacidades.keys()),
        "capacidades_meta": list(metas.keys()),
        "capacidades_resolubles": resolubles,
        "capacidades_no_resolubles": no_resolubles,
        "registro_n": len(_REGISTRO),
        "errores": errores,
    }


# ---------------------------------------------------------------
# 21. registrar_inventario
# ---------------------------------------------------------------
def registrar_inventario(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    inv = inventario(peticion)
    return {
        "id": _ID,
        "operacion": "registrar_inventario",
        "registrado": True,
        "inventario": inv,
    }

# ===============================================================
# FIN CALLABLES
# ===============================================================

# ===============================================================
# FIN PARTE 10
# ===============================================================


# ===============================================================
# PARTE 11 — RESOLUCIÓN Y EXPORTACIONES
# ===============================================================

_CAP_MAP = {
    "verificar": verificar,
    "barrer": barrer,
    "verificar_salida": verificar_salida,
    "inventario": inventario,
    "reporte": reporte,
    "diagnostico": diagnostico,
    "anunciar": anunciar,
    "anunciar_todo": anunciar_todo,
    "citar": citar,
    "registrar": registrar,
    "resolver": resolver,
    "resolver_enunciado": resolver_enunciado,
    "buscar": buscar,
    "cadena": cadena,
    "explicar": explicar,
    "relacionar": relacionar,
    "limpiar_ciclo": limpiar_ciclo,
    "evaluar": anunciar,
    "ejecutar_total": ejecutar_total,
    "inspeccionar": inspeccionar,
    "registrar_inventario": registrar_inventario,
}


def _resolver_capacidades(cont: Dict[str, Any]) -> None:
    resueltas: Dict[str, Any] = {}
    for nombre, ref in cont["capacidades"].items():
        if callable(ref):
            resueltas[nombre] = ref
            continue
        if isinstance(ref, str):
            if ref not in _CAP_MAP:
                raise RuntimeError(
                    "{0}: capacidad '{1}' referencia inexistente: '{2}'".format(
                        _NOMBRE, nombre, ref
                    )
                )
            fn = _CAP_MAP[ref]
            if not callable(fn):
                raise RuntimeError(
                    "{0}: '{1}' no es callable".format(_NOMBRE, ref)
                )
            resueltas[nombre] = fn
            continue
        raise RuntimeError(
            "{0}: capacidad '{1}' tipo inválido: {2}".format(
                _NOMBRE, nombre, type(ref).__name__
            )
        )
    cont["capacidades"] = resueltas


_resolver_capacidades(CONTENEDOR)

__all__ = [
    "CONTENEDOR",
    "ID_MODULO",
    "NOMBRE_MODULO",
    "ROL_MODULO",
    "VERSION_MODULO",
    "VERSION_CONTRATO",
    "ESQUEMA_CONTRATO",
    "ESTABILIDAD",
    "TIPOS_DECLARACION",
    "RELACIONES",
    "CAMPOS_OBLIGATORIOS",
    "CAMPOS_OPCIONALES",
    "verificar",
    "barrer",
    "verificar_salida",
    "inventario",
    "reporte",
    "diagnostico",
    "registrar",
    "resolver",
    "resolver_enunciado",
    "buscar",
    "cadena",
    "explicar",
    "citar",
    "anunciar",
    "anunciar_todo",
    "relacionar",
    "limpiar_ciclo",
    "evaluar",
    "ejecutar_total",
    "inspeccionar",
    "registrar_inventario",
]

# ===============================================================
# FIN PARTE 11
# ===============================================================


# ===============================================================
# FIN DEL MÓDULO
# ===============================================================
