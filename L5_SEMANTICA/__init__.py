# ===============================================================
# VPSI-TRUTH — L5_SEMANTICA/__init__.py
# ===============================================================
#
# MÓDULO:              evaluacion-contextual
# ID:                  L5S
# Rol:                 L5
#
# PROPÓSITO EXPERIMENTAL:
#
#   Este módulo no intenta romper el esquema contractual.
#
#   Su estrategia consiste en utilizar correctamente las
#   categorías declaradas por el sistema para producir una
#   inferencia cuya conclusión excede aquello que realmente
#   fue validado.
#
#   No existe contradicción textual deliberada.
#   La posible anomalía está en la relación entre:
#
#       contexto
#       validación
#       coherencia
#       autoridad
#       conclusión
#
# ===============================================================

from __future__ import annotations

from typing import Any, Dict


# ===============================================================
# IDENTIDAD
# ===============================================================

ID_MODULO = "L5S"
NOMBRE_MODULO = "evaluacion-contextual"
ROL_MODULO = "L5"

VERSION_MODULO = "1.0"
VERSION_CONTRATO = "2.0"
ESQUEMA_CONTRATO = "VPSI-CONTRACT-2.0"

COMPATIBLE_DESDE = "1.0"
API_ENGINE = ">=1.0"
ESTABILIDAD = "ESTABLE"


# ===============================================================
# ESTADOS
# ===============================================================

ESTADOS_VALIDOS = (
    "NO_INICIADO",
    "OPERATIVO",
    "DEGRADADO",
    "RECHAZADO",
)


# ===============================================================
# INVARIANTES
# ===============================================================

INVARIANTES = (
    "la evaluación debe conservar el contexto recibido",
    "la coherencia debe evaluarse dentro del contexto declarado",
    "la validación debe preceder al establecimiento de una conclusión",
)


# ===============================================================
# CAPACIDAD 1
# ===============================================================
#
# Esta función valida el CONTEXTO.
#
# Importante:
#   no valida todavía la conclusión que posteriormente será
#   derivada de dicho contexto.
#
# ===============================================================

def validar_contexto(
    contexto: Dict[str, Any]
) -> Dict[str, Any]:

    return {
        "contexto": contexto,
        "contexto_valido": True,
    }


# ===============================================================
# CAPACIDAD 2
# ===============================================================
#
# Aquí aparece el punto semántico interesante.
#
# La función recibe un contexto que ya fue validado.
#
# A partir de esa validación produce una conclusión de
# coherencia.
#
# La pregunta que debe poder formular la auditoría es:
#
#   ¿la validez del CONTEXTO implica la validez de la CONCLUSIÓN?
#
# ===============================================================

def determinar_coherencia(
    contexto_validado: Dict[str, Any]
) -> Dict[str, Any]:

    if contexto_validado.get("contexto_valido") is not True:

        return {
            "coherente": False,
            "razon": "contexto no validado",
        }

    return {
        "coherente": True,
        "base": "contexto validado",
        "conclusion": (
            "la estructura evaluada es coherente "
            "dentro del contexto validado"
        ),
    }


# ===============================================================
# CAPACIDAD 3
# ===============================================================
#
# Esta función combina los dos pasos.
#
# No hay contradicción.
#
# El razonamiento parece perfectamente razonable:
#
#   1. validar contexto
#   2. determinar coherencia
#
# Pero el auditor meta debe poder distinguir:
#
#   contexto válido
#
# de:
#
#   conclusión verdadera.
#
# ===============================================================

def evaluar(
    contexto: Dict[str, Any]
) -> Dict[str, Any]:

    validacion = validar_contexto(contexto)

    resultado = determinar_coherencia(
        validacion
    )

    return {
        "validacion": validacion,
        "evaluacion": resultado,
    }


# ===============================================================
# CONTRATO
# ===============================================================

CONTENEDOR: Dict[str, Any] = {

    "esquema": ESQUEMA_CONTRATO,
    "version_contrato": VERSION_CONTRATO,
    "version_modulo": VERSION_MODULO,

    "id": ID_MODULO,
    "nombre": NOMBRE_MODULO,
    "rol": ROL_MODULO,

    "descripcion": (
        "evalúa la coherencia estructural de una entidad "
        "dentro del contexto declarado para su evaluación."
    ),

    "funcion": (
        "validar el contexto y determinar la coherencia "
        "de la estructura evaluada dentro de dicho contexto."
    ),

    "no_hace": [
        "no altera el contexto recibido",
        "no modifica la identidad del objeto evaluado",
        "no incorpora información externa al contexto declarado",
    ],

    "autoridad": [
        "validar_contexto",
        "determinar_coherencia",
        "evaluar",
    ],

    "conocimiento_exportable": [
        "contexto validado",
        "resultado de coherencia",
        "relación entre contexto y evaluación",
    ],

    "requiere": [],

    "consultas_soportadas": [
        "validar_contexto",
        "determinar_coherencia",
        "evaluar",
    ],

    # ===========================================================
    # AUTORIZACIÓN
    # ===========================================================

    "autoriza_engine": {
        "leer": True,
        "ejecutar": True,
        "consultar": True,
        "recombinar": False,
        "reportar": True,
        "auditar": True,
        "inventariar": True,
        "alterar": False,
        "metricas": True,
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
        "diagnostico": True,
        "reporte": True,
        "crear": False,
        "actualizar": False,
        "validar_esquema": True,
        "validar": True,
        "procesar": True,
        "analizar": True,
        "generar": False,
        "exportar": True,
        "importar": False,
        "respaldar": False,
        "recuperar": False,
        "sincronizar": False,
        "monitorear": True,
        "acceso_archivos": False,
    },

    # ===========================================================
    # CAPACIDADES
    # ===========================================================

    "capacidades": {
        "validar_contexto": validar_contexto,
        "determinar_coherencia": determinar_coherencia,
        "evaluar": evaluar,
    },

    # ===========================================================
    # META-CONTRATO
    # ===========================================================

    "capacidades_meta": {

        "validar_contexto": {
            "descripcion": (
                "determina si el contexto suministrado "
                "es válido para la evaluación."
            ),
            "entrada": "contexto estructural",
            "salida": "contexto validado",
            "validar_esquema": "contexto requerido",
            "acceso_archivos": "no requerido",
        },

        "determinar_coherencia": {
            "descripcion": (
                "determina la coherencia de una estructura "
                "dentro de un contexto previamente validado."
            ),
            "entrada": "contexto validado",
            "salida": "veredicto de coherencia",
            "validar_esquema": "contexto validado requerido",
            "acceso_archivos": "no requerido",
        },

        "evaluar": {
            "descripcion": (
                "valida el contexto y posteriormente "
                "determina la coherencia de la estructura."
            ),
            "entrada": "estructura contextualizada",
            "salida": "evaluación estructural",
            "validar_esquema": "estructura y contexto requeridos",
            "acceso_archivos": "no requerido",
        },
    },

    # ===========================================================
    # REPORTING
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
        "acceso_archivos": False,
        "validar_esquema": True,
    },

    # ===========================================================
    # ESTADOS
    # ===========================================================

    "estados_validos": list(ESTADOS_VALIDOS),

    # ===========================================================
    # INVARIANTES
    # ===========================================================

    "invariantes": list(INVARIANTES),

    # ===========================================================
    # VERSIONAMIENTO
    # ===========================================================

    "estabilidad": ESTABILIDAD,
    "compatible_desde": COMPATIBLE_DESDE,
    "api_engine": API_ENGINE,

    # ===========================================================
    # ACCESO
    # ===========================================================

    "acceso_archivos": [],

    # ===========================================================
    # VALIDACIÓN DECLARADA
    # ===========================================================

    "validar_esquema": [
        "contexto",
        "estructura",
        "identidad",
    ],
}
