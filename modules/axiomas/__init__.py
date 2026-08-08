# ===============================================================
# VPSI-TRUTH — modules/axiomas/__init__.py
# ===============================================================
#
# MÓDULO:              axiomas
# ID:                  AX
# Rol:                 AX
# Versión módulo:      2.3
# Versión contrato:    1.0
# Esquema contrato:    VPSI-CONTRACT-1.0
# Estabilidad:         ESTABLE
# Compatible desde:    1.0
# API Engine:          >=1.0
#
# Función:
#   Representar y validar formalmente los axiomas del sistema VPSI.
#
# ===============================================================

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

ID_MODULO = "AX"
NOMBRE_MODULO = "axiomas"
ROL_MODULO = "AX"

VERSION_MODULO = "2.3"
VERSION_CONTRATO = "1.0"
ESQUEMA_CONTRATO = "VPSI-CONTRACT-1.0"

COMPATIBLE_DESDE = "1.0"
API_ENGINE = ">=1.0"
ESTABILIDAD = "ESTABLE"

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
# CONTRATO OFICIAL DEL MÓDULO
# ===============================================================

CONTENEDOR: Dict[str, Any] = {
    "esquema": ESQUEMA_CONTRATO,
    "version_contrato": VERSION_CONTRATO,
    "version_modulo": VERSION_MODULO,
    "estabilidad": ESTABILIDAD,
    "compatible_desde": COMPATIBLE_DESDE,
    "api_engine": API_ENGINE,
    "id": ID_MODULO,
    "nombre": NOMBRE_MODULO,
    "rol": ROL_MODULO,
    "dominio": "AX",
    "descripcion": "Representación y validación de axiomas del sistema.",
    "funcion": "Emitir y verificar la consistencia de los axiomas base.",
    "no_hace": [
        "No calcula valores de verdad ajenos al dominio",
        "No modifica contratos de otros módulos",
    ],
    "autoridad": [
        "Declarar axiomas formales",
        "Validar la integridad de las reglas base",
    ],
    "conocimiento_exportable": [
        "axiomas",
        "inventario",
        "reporte",
        "diagnostico",
    ],
    # Axiomas es un cimiento base, por lo que requiere a DG para ser auditado por él si lo exige el flujo,
    # o limpio si opera de forma autónoma. Para que Diagnostics lo lea y reconozca sin fricción:
    "requiere": [],
    "autoriza_engine": {
        "leer": True,
        "ejecutar": True,
        "consultar": True,
        "recombinar": True,
        "reportar": True,
        "auditar": True,
        "inventariar": True,
        "modificar": False,
        "alterar": False,
        "reescribir": False,
    },
    "consultas_soportadas": [
        "axiomas",
        "inventario",
        "reporte",
        "diagnostico",
    ],
    "capacidades": {
        "axiomas": "axiomas",
        "inventario": "inventario",
        "reporte": "reporte",
        "diagnostico": "diagnostico",
    },
    "capacidades_meta": {
        "axiomas": {
            "descripcion": "Devuelve la lista oficial de axiomas.",
            "entrada": "ninguna",
            "salida": "list[dict]",
        },
        "inventario": {
            "descripcion": "Enumeración de componentes del módulo.",
            "entrada": "ninguna",
            "salida": "dict",
        },
        "reporte": {
            "descripcion": "Estado operativo del módulo.",
            "entrada": "ninguna",
            "salida": "dict",
        },
        "diagnostico": {
            "descripcion": "Evaluación diagnóstica del módulo.",
            "entrada": "ninguna",
            "salida": "dict",
        },
    },
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
    },
    "estados_validos": list(ESTADOS_VALIDOS),
    "invariantes": [
        "el id del módulo nunca cambia",
        "los axiomas exportados son inmutables en tiempo de ejecución",
    ],
}

# ===============================================================
# CAPACIDADES PÚBLICAS
# ===============================================================

def axiomas() -> List[Dict[str, Any]]:
    return [
        {
            "id": "AX-01",
            "tipo": "axioma",
            "sujeto": "sistema",
            "relacion": "opera_bajo",
            "objeto": "contratos_coherentes",
            "polaridad": True,
            enunciado := "Todo componente operativo responde a un contrato validado por el Engine.",
            "depende_de": [],
            "gobierna": ["core", "modules"],
        }
    ]

def inventario(peticion: Any = None) -> Dict[str, Any]:
    return {
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
    }

def reporte() -> Dict[str, Any]:
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "estado": ESTADO_OPERATIVO,
        "coherente": True,
    }

def diagnostico() -> Dict[str, Any]:
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "estado": ESTADO_OPERATIVO,
        "problemas": [],
        "advertencias": [],
        "recomendaciones": [],
        "coherente": True,
    }

__all__ = [
    "CONTENEDOR",
    "ID_MODULO",
    "NOMBRE_MODULO",
    "ROL_MODULO",
    "VERSION_MODULO",
    "axiomas",
    "inventario",
    "reporte",
    "diagnostico",
]
