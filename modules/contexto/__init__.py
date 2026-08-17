# ===============================================================
# VPSI-TRUTH — modules/contexto/__init__.py
# ===============================================================
#
# MÓDULO:              contexto
# ID:                  CX
# Rol:                 CX
# Versión módulo:      2.3
# Versión contrato:    1.0
# Esquema contrato:    VPSI-CONTRACT-1.0
# Estabilidad:         ESTABLE
# Compatible desde:    1.0
# API Engine:          >=1.0
#
# Función:
#   Representar operativamente el marco evaluable O_context.
#
# Qué hace:
#   - Genera el registro O a partir de la petición.
#   - Clasifica estado, evento, ligaduras y modo_entrada.
#   - Determina permite_k y pedir_anuncio.
#   - Garantiza la coherencia estructural del dominio.
#   - Descubre, registra, inspecciona y valida el contenido completo
#     del módulo, incluyendo archivos, funciones, clases, constantes,
#     excepciones, reglas, clasificadores, validadores, capacidades
#     y demás componentes detectables.
#   - Expone una operación de ejecución total que ejerce todas las
#     unidades operativamente ejecutables del módulo conforme al
#     contrato y a sus leyes internas.
#   - Expone inventario, reporte, diagnóstico y axiomas del dominio.
#
# Qué NO hace:
#   - No calcula valores de verdad
#   - No asigna magnitudes numéricas de correlación
#   - No importa código ajeno a su directorio
#   - No declara dependencias de dominio
#   - No orquesta ciclos
#   - No emite cadenas auditables
#
# Responsabilidad:
#   Garantizar una representación coherente del marco O y mantener
#   la integridad estructural de su dominio.
#
# Autoridad:
#   - Declarar el registro O y permite_k
#   - Clasificar el contexto evaluable
#   - Validar la estructura y el dominio de los archivos internos
#   - Reportar el estado estructural del módulo
#   - Declarar la política de inventario y ejecución del módulo
#   - Registrar todos los componentes descubiertos
#   - Determinar qué componentes son operacionalmente ejecutables
#   - Ejercer la ejecución total solicitada por Engine
#
# Conocimiento exportable:
#   O_context, registro, permite_k, pedir_anuncio, tipos_peticion,
#   inventario, inventario_total, componentes, unidades_ejecutables,
#   ejecucion, reporte, diagnostico, axiomas
#
# Relación con Engine:
#   Engine descubre este CONTENEDOR, obtiene el inventario completo
#   del módulo, resuelve sus capacidades contractuales y puede
#   solicitar la ejecución total de las unidades operativamente
#   ejecutables del módulo conforme al contrato y sus leyes internas.
#
# Relación con Omega:
#   Omega no calcula información de este módulo.
#   Solo presenta los resultados entregados por Engine.
#
# ===============================================================


# ===============================================================
# PARTE 1 — PRINCIPIOS, BANDERAS Y ESPECIFICACIONES PRECISAS
# ===============================================================
#
# Responsabilidad: fijar todas las constantes, banderas, tipos,
# dominios y principios operativos antes de cualquier identidad
# o contrato.
# ===============================================================


# ===============================================================
# 1.1 — IMPORTACIONES
# ===============================================================

from __future__ import annotations

import os
import sys
import json
import math
import copy
import time
import types
import logging
import hashlib
import inspect
import itertools
import functools
import traceback
import importlib
import importlib.util
from pathlib import Path

from dataclasses import dataclass, field
from collections import defaultdict, deque
from typing import Any, Dict, List, Tuple, Set, Optional, Iterable, Callable

# ===============================================================
# FIN 1.1
# ===============================================================


# ===============================================================
# 1.2 — BANDERAS DE ESTADO DEL MÓDULO
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
# FIN 1.2
# ===============================================================


# ===============================================================
# 1.3 — DOMINIO DEL REGISTRO O
# ===============================================================

ESTADOS_O = ["estable", "cambio", "indefinido"]
EVENTOS = ["mismo_O", "expansion", "cambio", "indefinido"]
MODOS_ENTRADA = [
    "conversacion",
    "afirmacion",
    "teorema",
    "auditoria",
    "texto_libre",
    "repositorio",
]
TIPOS_PETICION = [
    "por_que_valor",
    "dame_O",
    "dame_evidencia",
    "dame_normas",
    "dame_limites",
    "dame_cadena_completa",
]
CLAVES_PEDIR_ANUNCIO = [
    "pedir_anuncio",
    "pedir_cita",
    "anuncio",
    "citar",
    "cadena_auditable",
    "dame_por_que",
]
REGLA_CAMPOS_OBLIGATORIOS = ["id", "nombre", "version", "descripcion"]
CLAVES_FUERA_DE_DOMINIO = [
    "Tru_Ri", "Tru_total", "tru_ri", "tru_total",
    "C", "L", "K",
    "alpha", "beta", "ALPHA", "BETA",
]

# ===============================================================
# FIN 1.3
# ===============================================================


# ===============================================================
# 1.4 — INVARIANTES DEL MÓDULO
# ===============================================================

INVARIANTES = (
    "el id del módulo nunca cambia",
    "el rol nunca cambia",
    "las capacidades declaradas son siempre callables tras la resolución",
    "este módulo no modifica el estado de otros módulos",
    "este módulo no inventa capacidades no declaradas en CONTENEDOR",
    "todo *.py interno se valida por estructura y dominio",
    "permite_k exige registro con estado=estable, O_id y enunciado_O",
    "pedir_anuncio verdadero implica tipos_peticion no vacío",
    "el inventario total no omite componentes descubiertos del módulo",
    "ejecutar no equivale a resolver",
    "ejecutar total ejerce todas las unidades operativamente ejecutables",
    "todo componente descubierto recibe clasificación estructural",
    "ningún componente descubierto se convierte en ejecutable arbitrariamente",
    "todo componente ejecutable posee una estrategia de ejecución válida",
)

# ===============================================================
# FIN 1.4
# ===============================================================


# ===============================================================
# PARTE 2 — IDENTIDAD DEL MÓDULO
# ===============================================================
#
# Responsabilidad: fijar la identidad contractual e inmutable.
# ===============================================================


# ===============================================================
# 2.1 — IDENTIFICADORES
# ===============================================================

ID_MODULO = "CX"
NOMBRE_MODULO = "contexto"
ROL_MODULO = "CX"

# ===============================================================
# FIN 2.1
# ===============================================================


# ===============================================================
# 2.2 — VERSIONES Y ESTABILIDAD
# ===============================================================

VERSION_MODULO = "2.3"
VERSION_CONTRATO = "1.0"
ESQUEMA_CONTRATO = "VPSI-CONTRACT-1.0"

COMPATIBLE_DESDE = "1.0"
API_ENGINE = ">=1.0"
ESTABILIDAD = "ESTABLE"

# ===============================================================
# FIN 2.2
# ===============================================================


# ===============================================================
# PARTE 3 — CONFIGURACIÓN DE DIRECTORIO
# ===============================================================

_DIR = Path(__file__).parent

# ===============================================================
# FIN PARTE 3
# ===============================================================


# ===============================================================
# PARTE 4 — DEFINICIONES DE EXCEPCIONES Y UNDEFINED
# ===============================================================


# ===============================================================
# 4.1 — EXCEPCIONES
# ===============================================================

class ContratoInvalido(Exception):
    """El CONTENEDOR no cumple el esquema o la resolución de capacidades falló."""


class ContextoError(Exception):
    """Error de forma o de regla contextual."""

# ===============================================================
# FIN 4.1
# ===============================================================


# ===============================================================
# 4.2 — UNDEFINED
# ===============================================================

class _Undefined:
    __slots__ = ()

    def __repr__(self) -> str:
        return "UNDEFINED"

    def __bool__(self) -> bool:
        raise TypeError("UNDEFINED si admite conversión a booleano")

    def __eq__(self, other: object) -> bool:
        return isinstance(other, _Undefined)

    def __hash__(self) -> int:
        return hash("VPSI_UNDEFINED")


UNDEFINED = _Undefined()


def es_undefined(v: Any) -> bool:
    return v is UNDEFINED or isinstance(v, _Undefined)

# ===============================================================
# FIN 4.2
# ===============================================================


# ===============================================================
# PARTE 5 — CONTRATO OFICIAL DEL MÓDULO (CONTENEDOR)
# ===============================================================
#
# Responsabilidad: declarar de forma completa e inmutable la identidad,
# autoridad, dominio, capacidades y reporting del módulo CX.
# Contrato: VPSI-CONTRACT-1.0.
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
    "dominio": "CX",
    "prefijo_reglas": "CX",
    "descripcion": (
        "Representación operativa del marco evaluable O_context."
    ),

    # ============================================================
    # 5.3 — PROPÓSITO
    # ============================================================
    "funcion": (
        "Generar el marco O a partir de la petición y garantizar "
        "la coherencia estructural de su dominio."
    ),
    "no_hace": [
        "No calcula valores de verdad",
        "No asigna magnitudes numéricas de correlación",
        "No importa código ajeno a su directorio",
        "No declara dependencias de dominio",
        "No orquesta ciclos",
        "No emite cadenas auditables",
    ],

    # ============================================================
    # 5.4 — AUTORIDAD
    # ============================================================
    "autoridad": [
        "Declarar el registro O y permite_k",
        "Clasificar el contexto evaluable",
        "Validar la estructura y el dominio de los archivos internos",
        "Reportar el estado estructural del módulo",
        "Declarar la política de inventario y ejecución del módulo",
        "Registrar todos los componentes descubiertos",
        "Determinar qué componentes son operacionalmente ejecutables conforme al contrato",
        "Ejercer la ejecución total solicitada por Engine",
    ],

    # ============================================================
    # 5.5 — CONOCIMIENTO EXPORTABLE
    # ============================================================
    "conocimiento_exportable": [
        "O_context",
        "registro",
        "permite_k",
        "pedir_anuncio",
        "tipos_peticion",
        "inventario",
        "inventario_total",
        "componentes",
        "unidades_ejecutables",
        "ejecucion",
        "reporte",
        "diagnostico",
        "axiomas",
    ],

    # ============================================================
    # 5.6 — ACCESO
    # ============================================================
    "acceso": {
        "nivel": "completo",
        "descripcion": "Acceso total a recursos del módulo"
    },

    # ============================================================
    # 5.7 — DEPENDENCIAS
    # ============================================================
    "requiere": [
        "CT", "AX", "FO", "MC", "SF", "CA", "CX",
        "DI", "RE", "VX", "CH", "CIT", "TT",
        "CE", "CC",
    ],

    # ============================================================
    # 5.8 — ACCESO A ARCHIVOS / VALIDAR ESQUEMA
    # ============================================================
    "acceso_archivos": ["*"],
    "validar_esquema": ["*"],

    # ============================================================
    # 5.9 — DOMINIO
    # ============================================================
    "modos_entrada": list(MODOS_ENTRADA),
    "estados_O": list(ESTADOS_O),
    "eventos": list(EVENTOS),
    "tipos_peticion": list(TIPOS_PETICION),
    "claves_pedir_anuncio": list(CLAVES_PEDIR_ANUNCIO),
    "regla_campos_obligatorios": list(REGLA_CAMPOS_OBLIGATORIOS),
    "claves_fuera_de_dominio": list(CLAVES_FUERA_DE_DOMINIO),

    # ============================================================
    # 5.10 — AUTORIZACIÓN AL ENGINE
    # ============================================================
    "autoriza_engine": {
        "leer": True,
        "ejecutar": True,
        "ejecutar_total": True,
        "inspeccionar": True,
        "registrar_inventario": True,
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
    },

    # ============================================================
    # 5.11 — CONSULTAS SOPORTADAS
    # ============================================================
    "consultas_soportadas": [
        "resolver",
        "centinela",
        "inventario",
        "reporte",
        "diagnostico",
        "verificar",
        "axiomas",
        "ejecutar",
        "ejecutar_total",
        "registrar_inventario",
    ],

    # ============================================================
    # 5.12 — CAPACIDADES
    # ============================================================
    "capacidades": {
        "resolver": "resolver",
        "evaluar": "resolver",
        "centinela": "centinela",
        "verificar": "barrer",
        "barrer": "barrer",
        "inventario": "inventario",
        "reporte": "reporte",
        "diagnostico": "diagnostico",
        "axiomas": "axiomas",
        "verificar_salida": "verificar_salida",
        "ejecutar": "ejecutar",
        "ejecutar_total": "ejecutar",
        "registrar_inventario": "registrar_inventario",
    },

    # ============================================================
    # 5.13 — METADATOS DE CAPACIDADES (1:1)
    # ============================================================
    "capacidades_meta": {
        "resolver": {
            "descripcion": (
                "Garantiza el marco O clasificado a partir de la petición."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con O_context, registro, permite_k, "
                "coherente, errores"
            ),
            "acceso_archivos": ["*"],
        },
        "evaluar": {
            "descripcion": "Alias de resolver.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con O_context, registro, permite_k, coherente"
            ),
            "acceso_archivos": ["*"],
        },
        "centinela": {
            "descripcion": (
                "Garantiza la coherencia estructural del dominio."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con coherente, total, choques, detalle, errores"
            ),
            "acceso_archivos": ["*"],
        },
        "verificar": {
            "descripcion": "Alias de barrer.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con coherente, errores, reglas_internas"
            ),
            "acceso_archivos": ["*"],
        },
        "barrer": {
            "descripcion": (
                "Garantiza la coherencia de los clasificadores internos."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con coherente, errores, reglas_internas"
            ),
            "acceso_archivos": ["*"],
        },
        "inventario": {
            "descripcion": (
                "Garantiza la enumeración de lo que existe en el módulo."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con id, version, reglas_internas, modos, "
                "estados, capacidades, inventario_total"
            ),
            "acceso_archivos": ["*"],
        },
        "reporte": {
            "descripcion": (
                "Garantiza el estado actual del módulo."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con estado, coherente, version, reglas_n"
            ),
            "acceso_archivos": ["*"],
        },
        "diagnostico": {
            "descripcion": (
                "Garantiza problemas, advertencias y recomendaciones."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con estado, problemas, advertencias, "
                "recomendaciones"
            ),
            "acceso_archivos": ["*"],
        },
        "axiomas": {
            "descripcion": (
                "Garantiza las declaraciones operativas del dominio."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "list[dict]",
            "acceso_archivos": ["*"],
        },
        "verificar_salida": {
            "descripcion": (
                "Garantiza la validez estructural de una salida del módulo."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "bool",
            "acceso_archivos": ["*"],
        },
        "ejecutar": {
            "descripcion": (
                "Ejercer todas las unidades operativas ejecutables "
                "descubiertas dentro del módulo conforme al contrato "
                "y a sus leyes internas."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con inventario, ejecuciones, resultados, "
                "errores, advertencias y estado"
            ),
            "acceso_archivos": ["*"],
        },
        "ejecutar_total": {
            "descripcion": "Alias contractual de ejecutar.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con inventario, ejecuciones, resultados, "
                "errores, advertencias y estado"
            ),
            "acceso_archivos": ["*"],
        },
        "registrar_inventario": {
            "descripcion": (
                "Construir el inventario estructural completo del módulo."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con archivos, componentes, funciones, clases, "
                "constantes, reglas, capacidades y unidades ejecutables"
            ),
            "acceso_archivos": ["*"],
        },
    },

    # ============================================================
    # 5.14 — INVENTARIO Y EJECUCIÓN TOTAL
    # ============================================================
    "inventario_total": {
        "modo": "completo",
        "incluye": [
            "archivos",
            "modulos",
            "funciones",
            "clases",
            "constantes",
            "excepciones",
            "reglas",
            "clasificadores",
            "validadores",
            "capacidades",
            "componentes",
        ],
        "descubrimiento": "dinamico",
        "incluye_no_declarados": True,
    },
    "ejecucion": {
        "modo": "total",
        "incluye_capacidades_declaradas": True,
        "incluye_componentes_ejecutables_descubiertos": True,
        "respeta_contrato": True,
        "respeta_leyes_internas": True,
        "ejecuta_constantes": False,
        "ejecuta_excepciones": False,
        "instancia_clases_automaticamente": False,
    },
    "capacidades_sistema": {
        "inventariar": "inventario",
        "registrar": "registrar_inventario",
        "resolver": "resolver",
        "ejecutar": "ejecutar",
    },

    # ============================================================
    # 5.15 — REPORTING
    # ============================================================
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
    },

    # ============================================================
    # 5.16 — ESTADOS VÁLIDOS E INVARIANTES
    # ============================================================
    "estados_validos": list(ESTADOS_VALIDOS),
    "invariantes": list(INVARIANTES),
}

# ===============================================================
# FIN PARTE 5
# ===============================================================


# ===============================================================
# PARTE 6 — FUNCIONES PRIVADAS
# ===============================================================
#
# Responsabilidad: normalización del registro O, validación de
# clasificadores, descubrimiento dinámico, inventario total y
# garantía de invariantes.
# ===============================================================


# ===============================================================
# 6.1 — ACCESO A CONFIGURACIÓN
# ===============================================================

def _cfg(clave: str, default: Any = None) -> Any:
    return CONTENEDOR.get(clave, default)

# ===============================================================
# FIN 6.1
# ===============================================================


# ===============================================================
# 6.2 — REGISTRO O CANÓNICO
# ===============================================================

def _registro_vacio() -> Dict[str, Any]:
    """Registro canónico vacío compatible con el dominio declarado."""
    return {
        "O_id": None,
        "escala": None,
        "enunciado_O": None,
        "ligaduras": {},
        "estado": "indefinido",
        "modo_entrada": None,
        "evento": "indefinido",
        "pedir_anuncio": False,
        "tipos_peticion": [],
    }

# ===============================================================
# FIN 6.2
# ===============================================================


# ===============================================================
# 6.3 — EVALUACIÓN DE pedir_anuncio
# ===============================================================

def _truthy_pedir(v: Any) -> bool:
    """Evalúa representaciones canónicas de petición de anuncio."""
    if v is True:
        return True
    if v is False or v is None:
        return False
    if isinstance(v, (int, float)):
        return v != 0
    s = str(v).strip().lower()
    return s in ("1", "true", "si", "sí", "yes", "on", "citar", "anuncio")

# ===============================================================
# FIN 6.3
# ===============================================================


# ===============================================================
# 6.4 — NORMALIZACIÓN DE TIPOS DE PETICIÓN
# ===============================================================

def _normalizar_tipos_peticion(raw: Any) -> List[str]:
    admitidos_cfg = _cfg("tipos_peticion")
    admitidos = set(admitidos_cfg) if isinstance(admitidos_cfg, (list, tuple, set)) else set()
    tipos: List[str] = []
    if isinstance(raw, str):
        for p in raw.replace(";", ",").split(","):
            p = p.strip()
            if p in admitidos and p not in tipos:
                tipos.append(p)
    elif isinstance(raw, (list, tuple, set)):
        for x in raw:
            s = str(x).strip()
            if s in admitidos and s not in tipos:
                tipos.append(s)
    return tipos

# ===============================================================
# FIN 6.4
# ===============================================================


# ===============================================================
# 6.5 — GARANTÍA ATÓMICA DE LA INVARIANTE pedir_anuncio
# ===============================================================

def _asegurar_invariante_pedir_anuncio(registro: Dict[str, Any]) -> None:
    """Garantiza: pedir_anuncio verdadero implica tipos_peticion no vacío."""
    if registro.get("pedir_anuncio") and not registro.get("tipos_peticion"):
        registro["tipos_peticion"] = ["dame_cadena_completa"]

# ===============================================================
# FIN 6.5
# ===============================================================


# ===============================================================
# 6.6 — NORMALIZACIÓN COMPLETA DEL REGISTRO
# ===============================================================

def _normalizar_registro(peticion: Dict[str, Any]) -> Dict[str, Any]:
    reg = _registro_vacio()
    estados_cfg = _cfg("estados_O")
    estados = set(estados_cfg) if isinstance(estados_cfg, (list, tuple, set)) else set()
    eventos_cfg = _cfg("eventos")
    eventos = set(eventos_cfg) if isinstance(eventos_cfg, (list, tuple, set)) else set()
    claves_pedir_cfg = _cfg("claves_pedir_anuncio")
    claves_pedir = tuple(claves_pedir_cfg) if isinstance(claves_pedir_cfg, (list, tuple)) else ()

    o_id = peticion.get("O_id")
    if o_id is None:
        o_id = peticion.get("o_id")
    enunciado = peticion.get("enunciado_O")
    if enunciado is None:
        enunciado = peticion.get("enunciado")
    if enunciado is None:
        enunciado = peticion.get("contexto")
    if enunciado is None:
        enunciado = peticion.get("O_context")
    escala = peticion.get("escala")
    modo = peticion.get("modo_entrada")
    if modo is None:
        modo = peticion.get("modo")
    ligaduras = peticion.get("ligaduras")
    if ligaduras is None:
        ligaduras = {}
    estado_decl = peticion.get("estado")

    if isinstance(ligaduras, dict):
        reg["ligaduras"] = {
            str(k).strip(): str(v).strip()
            for k, v in ligaduras.items()
            if str(k).strip() and str(v).strip()
        }
    else:
        reg["ligaduras"] = {}

    reg["O_id"] = str(o_id).strip() if o_id is not None else None
    reg["enunciado_O"] = str(enunciado).strip() if enunciado is not None else None
    reg["escala"] = str(escala).strip() if escala is not None else None
    reg["modo_entrada"] = str(modo).strip() if modo is not None else None

    if estado_decl in estados:
        reg["estado"] = estado_decl
    elif reg["O_id"] and reg["enunciado_O"]:
        reg["estado"] = "estable"
    else:
        reg["estado"] = "indefinido"

    evento = peticion.get("evento")
    if evento in eventos:
        reg["evento"] = evento
    elif reg["estado"] == "estable":
        reg["evento"] = "mismo_O"
    else:
        reg["evento"] = "indefinido"

    pedir = False
    for k in claves_pedir:
        if k in peticion and _truthy_pedir(peticion.get(k)):
            pedir = True
            break

    tipos = _normalizar_tipos_peticion(
        peticion.get("tipos_peticion") if "tipos_peticion" in peticion else peticion.get("tipo_peticion")
    )
    if tipos and not pedir:
        pedir = True
    if pedir and not tipos:
        tipos = ["dame_cadena_completa"]

    reg["pedir_anuncio"] = pedir
    reg["tipos_peticion"] = tipos
    return reg

# ===============================================================
# FIN 6.6
# ===============================================================


# ===============================================================
# 6.7 — CONFLICTOS DE LIGADURAS Y CÁLCULO DE permite_k
# ===============================================================

def _conflicto_ligaduras(ligaduras: Dict[str, str]) -> List[str]:
    errs: List[str] = []
    for forma, d in ligaduras.items():
        if not forma or not d:
            errs.append(
                "ligadura inválida: forma={0!r} D={1!r}".format(forma, d)
            )
    return errs


def _permite_k(registro: Dict[str, Any]) -> bool:
    if registro.get("estado") != "estable":
        return False
    if not registro.get("O_id") or not registro.get("enunciado_O"):
        return False
    return True

# ===============================================================
# FIN 6.7
# ===============================================================


# ===============================================================
# 6.8 — VALIDACIÓN DE CLASIFICADORES
# ===============================================================


# ===============================================================
# 6.8.1 — ANCLAJE DE ID
# ===============================================================

def _id_anclado(rid: str, regla: Dict[str, Any]) -> bool:
    prefijo_cfg = _cfg("prefijo_reglas")
    if prefijo_cfg is None:
        prefijo_cfg = _cfg("dominio")
    prefijo = str(prefijo_cfg) if prefijo_cfg is not None else ""
    if not rid:
        return False
    if prefijo and (
        rid.startswith(prefijo + "-")
        or rid.startswith(prefijo + "_")
        or prefijo.upper() in rid.upper()
    ):
        return True
    if regla.get("anclas_cx") or regla.get("anclas"):
        return True
    return False

# ===============================================================
# FIN 6.8.1
# ===============================================================


# ===============================================================
# 6.8.2 — VALIDACIÓN DE META DE REGLA
# ===============================================================

def _validar_regla_meta(stem: str, regla: Any) -> List[str]:
    errs: List[str] = []
    if not isinstance(regla, dict):
        return ["{0}: REGLA debe ser dict".format(stem)]

    campos_cfg = _cfg("regla_campos_obligatorios")
    campos = campos_cfg if isinstance(campos_cfg, list) else []
    for k in campos:
        if k not in regla or not str(regla.get(k, "")).strip():
            errs.append(
                "{0}: REGLA sin campo obligatorio '{1}'".format(stem, k)
            )

    rid = str(regla.get("id", "")).strip()
    if rid and not _id_anclado(rid, regla):
        errs.append(
            "{0}: id '{1}' sin anclaje al dominio {2}".format(
                stem, rid, _cfg("dominio")
            )
        )

    fuera_cfg = _cfg("claves_fuera_de_dominio")
    fuera = set(fuera_cfg) if isinstance(fuera_cfg, (list, tuple, set)) else set()
    for clave in fuera:
        if clave in regla and regla[clave] is not None:
            errs.append(
                "{0}: REGLA contiene clave fuera de dominio: '{1}'".format(
                    stem, clave
                )
            )
    return errs

# ===============================================================
# FIN 6.8.2
# ===============================================================


# ===============================================================
# 6.8.3 — VALIDACIÓN DE CLASIFICACIÓN
# ===============================================================

def _validar_clasificacion(stem: str, cls: Any) -> List[str]:
    errs: List[str] = []
    if not isinstance(cls, dict):
        return ["{0}: clasificar() debe devolver dict".format(stem)]

    fuera_cfg = _cfg("claves_fuera_de_dominio")
    fuera = set(fuera_cfg) if isinstance(fuera_cfg, (list, tuple, set)) else set()
    for clave in fuera:
        if clave in cls and cls[clave] is not None:
            if clave == "K" and isinstance(cls.get("K"), bool):
                continue
            errs.append(
                "{0}: clasificar() emite clave fuera de dominio: '{1}'".format(
                    stem, clave
                )
            )

    estados_cfg = _cfg("estados_O")
    estados = set(estados_cfg) if isinstance(estados_cfg, (list, tuple, set)) else set()
    eventos_cfg = _cfg("eventos")
    eventos = set(eventos_cfg) if isinstance(eventos_cfg, (list, tuple, set)) else set()
    tipos_cfg = _cfg("tipos_peticion")
    tipos_ok = set(tipos_cfg) if isinstance(tipos_cfg, (list, tuple, set)) else set()

    if "estado" in cls and cls["estado"] is not None:
        if cls["estado"] not in estados:
            errs.append(
                "{0}: estado {1!r} no admitido".format(stem, cls["estado"])
            )
    if "evento" in cls and cls["evento"] is not None:
        if cls["evento"] not in eventos:
            errs.append(
                "{0}: evento {1!r} no admitido".format(stem, cls["evento"])
            )

    tps = cls.get("tipos_peticion")
    if tps is not None:
        if not isinstance(tps, list):
            errs.append("{0}: tipos_peticion debe ser list".format(stem))
        else:
            for t in tps:
                if t not in tipos_ok:
                    errs.append(
                        "{0}: tipo_peticion no admitido: {1!r}".format(stem, t)
                    )
    return errs

# ===============================================================
# FIN 6.8.3
# ===============================================================


# ===============================================================
# 6.8.4 — CENTINELA DE ARCHIVO INDIVIDUAL
# ===============================================================

def _centinela_archivo(
    stem: str,
    mod: Any,
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    entrada: Dict[str, Any] = {"archivo": "{0}.py".format(stem)}
    errores_c: List[str] = []

    meta = getattr(mod, "REGLA", None)
    validador = getattr(mod, "validar", None)
    clasificador = getattr(mod, "clasificar", None)

    if meta is None and not callable(validador) and not callable(clasificador):
        errores_c.append(
            "{0}: sin REGLA ni validar()/clasificar()".format(stem)
        )
        entrada["error"] = errores_c[-1]
        entrada["errores_centinela"] = errores_c
        return entrada

    if meta is not None:
        entrada["regla"] = meta if isinstance(meta, dict) else {"raw": str(meta)}
        errores_c.extend(_validar_regla_meta(stem, meta))

    if callable(clasificador) and peticion is not None:
        try:
            cls = clasificador(peticion)
            entrada["clasificacion"] = cls
            errores_c.extend(_validar_clasificacion(stem, cls))
        except Exception as e:
            errores_c.append(
                "{0}: clasificar: {1}: {2}".format(
                    stem, type(e).__name__, e
                )
            )
            entrada["error"] = errores_c[-1]
    elif callable(validador):
        try:
            entrada["resultado"] = validador()
        except Exception as e:
            errores_c.append(
                "{0}: validar: {1}: {2}".format(
                    stem, type(e).__name__, e
                )
            )
            entrada["error"] = errores_c[-1]

    if errores_c:
        entrada["errores_centinela"] = errores_c
        if "error" not in entrada:
            entrada["error"] = errores_c[0]
    return entrada

# ===============================================================
# FIN 6.8.4
# ===============================================================


# ===============================================================
# 6.9 — DESCUBRIMIENTO Y CARGA DINÁMICA DE REGLAS
# ===============================================================


# ===============================================================
# 6.9.1 — CARGA DE REGLAS
# ===============================================================

def _cargar_reglas(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    registro: Dict[str, Any] = {}
    for archivo in sorted(_DIR.glob("*.py")):
        if archivo.name == "__init__.py" or archivo.name.startswith("_"):
            continue
        nombre_mod = "{0}_regla_{1}".format(NOMBRE_MODULO, archivo.stem)
        spec = importlib.util.spec_from_file_location(nombre_mod, archivo)
        if spec is None or spec.loader is None:
            registro[archivo.stem] = {
                "error": "spec_from_file_location falló",
                "errores_centinela": ["carga imposible"],
            }
            continue
        mod = importlib.util.module_from_spec(spec)
        sys.modules[nombre_mod] = mod
        try:
            spec.loader.exec_module(mod)
        except Exception as e:
            if nombre_mod in sys.modules:
                del sys.modules[nombre_mod]
            registro[archivo.stem] = {
                "error": "{0}: {1}".format(type(e).__name__, e),
                "errores_centinela": ["import: {0}".format(e)],
                "traceback": traceback.format_exc(),
            }
            continue
        registro[archivo.stem] = _centinela_archivo(
            archivo.stem, mod, peticion
        )
    return registro

# ===============================================================
# FIN 6.9.1
# ===============================================================


# ===============================================================
# 6.9.2 — DETECCIÓN DE CHOQUES
# ===============================================================

def _detectar_choques_reglas(reglas: Dict[str, Any]) -> List[str]:
    choques: List[str] = []
    por_id: Dict[str, List[str]] = {}
    por_nombre: Dict[str, List[str]] = {}

    for clave, datos in reglas.items():
        if datos.get("errores_centinela") and "regla" not in datos:
            continue
        regla = datos.get("regla") or {}
        if not isinstance(regla, dict):
            continue
        rid = str(regla.get("id", "")).strip()
        nom = str(regla.get("nombre", "")).strip()
        if rid:
            por_id.setdefault(rid, []).append(clave)
        if nom:
            por_nombre.setdefault(nom, []).append(clave)

    for rid, archivos in por_id.items():
        if len(archivos) > 1:
            choques.append(
                "id de regla '{0}' repetido en {1}".format(rid, archivos)
            )
    for nom, archivos in por_nombre.items():
        if len(archivos) > 1:
            choques.append(
                "nombre de regla '{0}' repetido en {1}".format(nom, archivos)
            )
    return choques

# ===============================================================
# FIN 6.9.2
# ===============================================================


# ===============================================================
# 6.10 — VALIDACIÓN DEL CONTRATO
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

    if not isinstance(cont.get("capacidades"), dict):
        raise ContratoInvalido(
            "{0}: 'capacidades' debe ser dict".format(NOMBRE_MODULO)
        )

    if not isinstance(cont.get("requiere"), list):
        raise ContratoInvalido(
            "{0}: 'requiere' debe ser list".format(NOMBRE_MODULO)
        )

    if not isinstance(cont.get("no_hace"), list):
        raise ContratoInvalido(
            "{0}: 'no_hace' debe ser list".format(NOMBRE_MODULO)
        )

    estructuras_lista = (
        "modos_entrada",
        "estados_O",
        "eventos",
        "tipos_peticion",
        "claves_pedir_anuncio",
        "regla_campos_obligatorios",
        "claves_fuera_de_dominio",
        "estados_validos",
    )
    for clave in estructuras_lista:
        valor = cont.get(clave)
        if valor is not None and not isinstance(valor, list):
            raise ContratoInvalido(
                "{0}: '{1}' debe ser list, recibido {2}".format(
                    NOMBRE_MODULO, clave, type(valor).__name__
                )
            )

    meta_caps = cont.get("capacidades_meta")
    if meta_caps is None:
        raise ContratoInvalido(
            "{0}: 'capacidades_meta' ausente".format(NOMBRE_MODULO)
        )
    if not isinstance(meta_caps, dict):
        raise ContratoInvalido(
            "{0}: 'capacidades_meta' debe ser dict".format(NOMBRE_MODULO)
        )

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
# FIN 6.10
# ===============================================================


# ===============================================================
# 6.11 — DESCUBRIMIENTO DEL INVENTARIO TOTAL
# ===============================================================
#
# Descubre la realidad existente en el módulo.
# No depende exclusivamente de CONTENEDOR["capacidades"].
# ===============================================================

def _descubrir_inventario_total() -> Dict[str, Any]:
    """
    Inspecciona el propio módulo y construye el inventario estructural completo.
    Clasifica cada componente descubierto.
    """
    componentes: List[Dict[str, Any]] = []
    archivos: List[Dict[str, Any]] = []
    funciones: List[Dict[str, Any]] = []
    clases: List[Dict[str, Any]] = []
    constantes: List[Dict[str, Any]] = []
    excepciones: List[Dict[str, Any]] = []
    reglas: List[Dict[str, Any]] = []
    clasificadores: List[Dict[str, Any]] = []
    validadores: List[Dict[str, Any]] = []
    unidades_ejecutables: List[Dict[str, Any]] = []
    errores_descubrimiento: List[str] = []

    # -----------------------------------------------------------
    # 6.11.1 — ARCHIVOS INTERNOS
    # -----------------------------------------------------------
    for archivo in sorted(_DIR.glob("*.py")):
        if archivo.name.startswith("_") and archivo.name != "__init__.py":
            continue
        archivos.append({
            "nombre": archivo.name,
            "ruta": str(archivo),
            "tipo": "archivo",
            "declarado": archivo.name == "__init__.py",
            "descubierto": True,
        })

    # -----------------------------------------------------------
    # 6.11.2 — INSPECCIÓN DEL MÓDULO ACTUAL
    # -----------------------------------------------------------
    modulo_actual = sys.modules.get(__name__)
    if modulo_actual is None:
        errores_descubrimiento.append("módulo actual no disponible en sys.modules")
        return {
            "archivos": archivos,
            "componentes": componentes,
            "errores": errores_descubrimiento,
        }

    miembros = inspect.getmembers(modulo_actual)
    capacidades_declaradas = set(CONTENEDOR.get("capacidades", {}).keys())

    for nombre, obj in miembros:
        # omitir builtins y imports
        if nombre in ("__builtins__", "__cached__", "__file__", "__loader__",
                      "__name__", "__package__", "__spec__", "__doc__"):
            continue

        entry: Dict[str, Any] = {
            "nombre": nombre,
            "origen": __name__,
            "modulo": NOMBRE_MODULO,
            "archivo": "__init__.py",
            "declarado": nombre in capacidades_declaradas,
            "descubierto": True,
            "callable": callable(obj),
            "ejecutable": False,
            "requiere_entrada": False,
            "tipo": "desconocido",
            "estado": "descubierto",
            "errores": [],
        }

        if inspect.isfunction(obj) or inspect.ismethod(obj):
            entry["tipo"] = "funcion"
            entry["referencia"] = obj
            # Firmar
            try:
                sig = inspect.signature(obj)
                params = [
                    p for p in sig.parameters.values()
                    if p.default is inspect.Parameter.empty
                    and p.kind in (
                        inspect.Parameter.POSITIONAL_ONLY,
                        inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    )
                ]
                # self / cls no cuentan como requeridos para funciones de módulo
                params = [p for p in params if p.name not in ("self", "cls")]
                entry["requiere_entrada"] = len(params) > 0
                # Ejecutable si no requiere argumentos obligatorios o si es capacidad declarada
                if nombre.startswith("_"):
                    entry["ejecutable"] = False
                    entry["ejecutable_directamente"] = False
                    entry["participa_en_ejecucion"] = True
                else:
                    entry["ejecutable"] = True
                    entry["ejecutable_directamente"] = not entry["requiere_entrada"]
            except (ValueError, TypeError):
                entry["requiere_entrada"] = True
                entry["ejecutable"] = False

            funciones.append(entry)
            componentes.append(entry)
            if entry["ejecutable"]:
                unidades_ejecutables.append(entry)

        elif inspect.isclass(obj):
            entry["tipo"] = "clase"
            entry["ejecutable"] = False  # no instanciar automáticamente
            if issubclass(obj, Exception):
                entry["tipo"] = "excepcion"
                excepciones.append(entry)
            else:
                clases.append(entry)
            componentes.append(entry)

        elif isinstance(obj, (str, int, float, bool, list, tuple, dict, set, frozenset, type(None))):
            if nombre.isupper() or nombre.startswith("_"):
                entry["tipo"] = "constante"
                entry["ejecutable"] = False
                try:
                    entry["representacion"] = repr(obj)[:200]
                except Exception:
                    entry["representacion"] = "<no representable>"
                constantes.append(entry)
                componentes.append(entry)

    # -----------------------------------------------------------
    # 6.11.3 — REGLAS INTERNAS (reutiliza mecanismo existente)
    # -----------------------------------------------------------
    try:
        reglas_raw = _cargar_reglas(None)
        for stem, datos in reglas_raw.items():
            entry_r = {
                "nombre": stem,
                "tipo": "regla",
                "origen": stem + ".py",
                "modulo": NOMBRE_MODULO,
                "archivo": stem + ".py",
                "declarado": False,
                "descubierto": True,
                "callable": False,
                "ejecutable": False,
                "estado": "descubierto" if "error" not in datos else "error",
                "errores": datos.get("errores_centinela") or [],
            }
            if "clasificacion" in datos:
                entry_r["tipo"] = "clasificador"
                clasificadores.append(entry_r)
            elif "resultado" in datos:
                entry_r["tipo"] = "validador"
                validadores.append(entry_r)
            else:
                reglas.append(entry_r)
            componentes.append(entry_r)
    except Exception as e:
        errores_descubrimiento.append(
            "error al cargar reglas: {0}: {1}".format(type(e).__name__, e)
        )

    # -----------------------------------------------------------
    # 6.11.4 — CONSOLIDACIÓN
    # -----------------------------------------------------------
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "archivos": archivos,
        "componentes": componentes,
        "funciones": funciones,
        "clases": clases,
        "constantes": constantes,
        "excepciones": excepciones,
        "reglas": reglas,
        "clasificadores": clasificadores,
        "validadores": validadores,
        "capacidades_declaradas": list(capacidades_declaradas),
        "unidades_ejecutables": unidades_ejecutables,
        "total_componentes": len(componentes),
        "total_ejecutables": len(unidades_ejecutables),
        "errores_descubrimiento": errores_descubrimiento,
    }

# ===============================================================
# FIN 6.11
# ===============================================================


# ===============================================================
# PARTE 7 — CAPACIDADES PÚBLICAS
# ===============================================================
#
# Responsabilidad: implementar las capacidades declaradas en CONTENEDOR.
# ===============================================================


# ===============================================================
# 7.1 — CENTINELA ESTRUCTURAL
# ===============================================================

def centinela() -> Dict[str, Any]:
    reglas = _cargar_reglas(None)
    choques = _detectar_choques_reglas(reglas)
    errores: List[str] = list(choques)

    for nombre, datos in reglas.items():
        if "error" in datos:
            errores.append("regla '{0}': {1}".format(nombre, datos["error"]))
        for ec in datos.get("errores_centinela") or []:
            if ec not in errores:
                errores.append("centinela '{0}': {1}".format(nombre, ec))

    return {
        "contenedor": NOMBRE_MODULO,
        "dominio": _cfg("dominio"),
        "coherente": not errores,
        "total": len(reglas),
        "choques": choques,
        "detalle": reglas,
        "errores": errores,
        "version": VERSION_MODULO,
    }

# ===============================================================
# FIN 7.1
# ===============================================================


# ===============================================================
# 7.2 — RESOLVER (CAPACIDAD PRINCIPAL)
# ===============================================================

def resolver(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    if peticion is not None and not isinstance(peticion, dict):
        return {
            "O_context": None,
            "registro": None,
            "permite_k": False,
            "pedir_anuncio": False,
            "tipos_peticion": [],
            "coherente": False,
            "escala": "macro",
            "modo_entrada": None,
            "reglas_internas": {
                "total": 0,
                "choques": [],
            },
            "errores": [
                "peticion debe ser dict o None; recibido {0}".format(
                    type(peticion).__name__
                )
            ],
            "notas": ["tipo de petición inválido"],
        }

    # Semántica contractual vigente: tanto None como {} producen auditoría pura.
    es_auditoria_pura = peticion is None
    peticion_datos = dict(peticion) if peticion is not None else {}

    modos_cfg = _cfg("modos_entrada")
    modos = set(modos_cfg) if isinstance(modos_cfg, (list, tuple, set)) else set()
    estados_cfg = _cfg("estados_O")
    estados = set(estados_cfg) if isinstance(estados_cfg, (list, tuple, set)) else set()
    eventos_cfg = _cfg("eventos")
    eventos = set(eventos_cfg) if isinstance(eventos_cfg, (list, tuple, set)) else set()
    tipos_cfg = _cfg("tipos_peticion")
    tipos_ok = set(tipos_cfg) if isinstance(tipos_cfg, (list, tuple, set)) else set()

    if es_auditoria_pura or not peticion_datos:
        audit = centinela()
        return {
            "O_context": None,
            "registro": None,
            "permite_k": False,
            "pedir_anuncio": False,
            "tipos_peticion": [],
            "coherente": audit.get("coherente", False),
            "escala": "macro",
            "modo_entrada": "repositorio",
            "reglas_internas": {
                "total": audit.get("total", 0),
                "choques": audit.get("choques") if audit.get("choques") is not None else [],
            },
            "errores": list(audit.get("errores") if audit.get("errores") is not None else []),
            "notas": ["sin petición: solo auditoría de clasificadores"],
        }

    reglas = _cargar_reglas(peticion_datos)
    choques = _detectar_choques_reglas(reglas)
    errores: List[str] = list(choques)

    for nombre, datos in reglas.items():
        if "error" in datos:
            errores.append("regla '{0}': {1}".format(nombre, datos["error"]))
        for ec in datos.get("errores_centinela") or []:
            if ec not in errores:
                errores.append("centinela '{0}': {1}".format(nombre, ec))

    registro = _normalizar_registro(peticion_datos)
    errores.extend(_conflicto_ligaduras(registro.get("ligaduras") or {}))

    if registro.get("modo_entrada") and registro["modo_entrada"] not in modos:
        errores.append(
            "modo_entrada no reconocido: {0!r}".format(
                registro["modo_entrada"]
            )
        )

    for nombre, datos in reglas.items():
        cls = datos.get("clasificacion")
        if not isinstance(cls, dict):
            continue
        if cls.get("estado") in estados:
            registro["estado"] = cls["estado"]
        if cls.get("evento") in eventos:
            registro["evento"] = cls["evento"]
        if cls.get("pedir_anuncio") is True:
            registro["pedir_anuncio"] = True
        tps = cls.get("tipos_peticion")
        if isinstance(tps, list) and tps:
            seen = set(registro.get("tipos_peticion") or [])
            for t in tps:
                if t in tipos_ok and t not in seen:
                    registro.setdefault("tipos_peticion", []).append(t)
                    seen.add(t)
            if registro.get("tipos_peticion") and not registro.get("pedir_anuncio"):
                registro["pedir_anuncio"] = True
        if cls.get("error"):
            errores.append(
                "clasificacion '{0}': {1}".format(nombre, cls["error"])
            )

    _asegurar_invariante_pedir_anuncio(registro)

    permite = _permite_k(registro)
    o_ctx = registro.get("enunciado_O") or registro.get("O_id") or UNDEFINED

    notas: List[str] = []
    if not registro.get("O_id") or not registro.get("enunciado_O"):
        notas.append("registro incompleto: sin O_id o enunciado_O")
    if not permite:
        notas.append("permite_k=False")
    if registro.get("pedir_anuncio"):
        notas.append("pedir_anuncio=True")
    if not reglas:
        notas.append("sin clasificadores internos")

    return {
        "O_context": o_ctx if not es_undefined(o_ctx) else UNDEFINED,
        "registro": registro,
        "permite_k": permite,
        "pedir_anuncio": bool(registro.get("pedir_anuncio")),
        "tipos_peticion": list(registro.get("tipos_peticion") or []),
        "coherente": not errores,
        "escala": "micro",
        "modo_entrada": registro.get("modo_entrada"),
        "reglas_internas": {
            "total": len(reglas),
            "choques": choques,
        },
        "errores": errores,
        "notas": notas,
    }

# ===============================================================
# FIN 7.2
# ===============================================================


# ===============================================================
# 7.3 — BARRER / VERIFICAR
# ===============================================================

def barrer() -> Dict[str, Any]:
    audit = centinela()
    return {
        "contenedor": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "dominio": _cfg("dominio"),
        "coherente": audit.get("coherente", False),
        "errores": audit.get("errores") if audit.get("errores") is not None else [],
        "reglas_internas": {
            "total": audit.get("total", 0),
            "choques": audit.get("choques") if audit.get("choques") is not None else [],
        },
        "version": VERSION_MODULO,
    }


def verificar() -> Dict[str, Any]:
    return barrer()

# ===============================================================
# FIN 7.3
# ===============================================================


# ===============================================================
# 7.4 — VERIFICAR_SALIDA
# ===============================================================

def verificar_salida(salida: Dict[str, Any]) -> bool:
    if not isinstance(salida, dict):
        return False
    if "coherente" not in salida or not isinstance(salida["coherente"], bool):
        return False
    if "errores" in salida and not isinstance(salida["errores"], list):
        return False
    if "notas" in salida and not isinstance(salida["notas"], list):
        return False

    estados_cfg = _cfg("estados_O")
    estados = set(estados_cfg) if isinstance(estados_cfg, (list, tuple, set)) else set()
    eventos_cfg = _cfg("eventos")
    eventos = set(eventos_cfg) if isinstance(eventos_cfg, (list, tuple, set)) else set()
    tipos_cfg = _cfg("tipos_peticion")
    tipos_ok = set(tipos_cfg) if isinstance(tipos_cfg, (list, tuple, set)) else set()

    if "permite_k" in salida:
        if not isinstance(salida["permite_k"], bool):
            return False
        if salida["permite_k"] is True:
            reg = salida.get("registro")
            if not isinstance(reg, dict):
                return False
            if reg.get("estado") != "estable":
                return False
            if not reg.get("O_id") or not reg.get("enunciado_O"):
                return False
    else:
        if "registro" in salida and salida["registro"] is not None:
            return False

    if "registro" in salida:
        reg = salida["registro"]
        if reg is not None:
            if not isinstance(reg, dict):
                return False
            if "estado" in reg and reg["estado"] not in estados:
                return False
            if "evento" in reg and reg["evento"] not in eventos:
                return False
            if "tipos_peticion" in reg:
                if not isinstance(reg["tipos_peticion"], list):
                    return False
                for t in reg["tipos_peticion"]:
                    if t not in tipos_ok:
                        return False
            if "pedir_anuncio" in reg and not isinstance(reg["pedir_anuncio"], bool):
                return False
            if isinstance(reg, dict) and reg.get("pedir_anuncio") is True:
                if not (reg.get("tipos_peticion") or []):
                    return False

    if "pedir_anuncio" in salida and not isinstance(salida["pedir_anuncio"], bool):
        return False

    if "tipos_peticion" in salida:
        if not isinstance(salida["tipos_peticion"], list):
            return False
        for t in salida["tipos_peticion"]:
            if t not in tipos_ok:
                return False
    return True

# ===============================================================
# FIN 7.4
# ===============================================================


# ===============================================================
# 7.5 — REGISTRAR_INVENTARIO
# ===============================================================

def registrar_inventario() -> Dict[str, Any]:
    """Construye el inventario estructural completo del módulo."""
    inv = _descubrir_inventario_total()
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "operacion": "registrar_inventario",
        "archivos": inv.get("archivos", []),
        "componentes": inv.get("componentes", []),
        "funciones": inv.get("funciones", []),
        "clases": inv.get("clases", []),
        "constantes": inv.get("constantes", []),
        "excepciones": inv.get("excepciones", []),
        "reglas": inv.get("reglas", []),
        "clasificadores": inv.get("clasificadores", []),
        "validadores": inv.get("validadores", []),
        "capacidades_declaradas": inv.get("capacidades_declaradas", []),
        "unidades_ejecutables": inv.get("unidades_ejecutables", []),
        "total_componentes": inv.get("total_componentes", 0),
        "total_ejecutables": inv.get("total_ejecutables", 0),
        "errores_descubrimiento": inv.get("errores_descubrimiento", []),
    }

# ===============================================================
# FIN 7.5
# ===============================================================


# ===============================================================
# 7.6 — INVENTARIO (AMPLIADO)
# ===============================================================

def inventario(peticion: Any = None) -> Dict[str, Any]:
    reglas = _cargar_reglas()
    inv_total = _descubrir_inventario_total()
    return {
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "dominio": CONTENEDOR.get("dominio"),
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "capacidades_declaradas": list(CONTENEDOR["capacidades"].keys()),
        "capacidades_resueltas": list(CONTENEDOR["capacidades"].keys()),
        "reglas_internas": sorted(reglas.keys()),
        "total_reglas": len(reglas),
        "modos_entrada": list(_cfg("modos_entrada") if isinstance(_cfg("modos_entrada"), list) else []),
        "estados_O": list(_cfg("estados_O") if isinstance(_cfg("estados_O"), list) else []),
        "eventos": list(_cfg("eventos") if isinstance(_cfg("eventos"), list) else []),
        "tipos_peticion": list(_cfg("tipos_peticion") if isinstance(_cfg("tipos_peticion"), list) else []),
        "requiere": list(CONTENEDOR.get("requiere") if isinstance(CONTENEDOR.get("requiere"), list) else []),
        "autoridad": CONTENEDOR.get("autoridad"),
        "conocimiento_exportable": CONTENEDOR.get("conocimiento_exportable"),
        "consultas_soportadas": CONTENEDOR.get("consultas_soportadas"),
        "invariantes": CONTENEDOR.get("invariantes"),
        # inventario total
        "archivos": inv_total.get("archivos", []),
        "componentes": inv_total.get("componentes", []),
        "funciones": inv_total.get("funciones", []),
        "clases": inv_total.get("clases", []),
        "constantes": inv_total.get("constantes", []),
        "excepciones": inv_total.get("excepciones", []),
        "clasificadores": inv_total.get("clasificadores", []),
        "validadores": inv_total.get("validadores", []),
        "unidades_ejecutables": inv_total.get("unidades_ejecutables", []),
        "total_componentes": inv_total.get("total_componentes", 0),
        "total_ejecutables": inv_total.get("total_ejecutables", 0),
    }

# ===============================================================
# FIN 7.6
# ===============================================================


# ===============================================================
# 7.7 — EJECUCIÓN TOTAL DEL MÓDULO
# ===============================================================

def ejecutar(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Ejercer todas las unidades operativas ejecutables descubiertas
    dentro del módulo conforme al contrato y a sus leyes internas.

    NO es un alias de resolver().
    NO se limita a CONTENEDOR["capacidades"].
    """
    inv = _descubrir_inventario_total()
    unidades = inv.get("unidades_ejecutables", [])
    resultados: List[Dict[str, Any]] = []
    errores: List[Dict[str, Any]] = []
    advertencias: List[str] = []
    ejecutados = 0

    for unidad in unidades:
        nombre = unidad.get("nombre")
        ref = unidad.get("referencia")
        if not callable(ref):
            advertencias.append(
                "unidad '{0}' marcada ejecutable pero no es callable".format(nombre)
            )
            continue

        if unidad.get("requiere_entrada") and not (peticion and isinstance(peticion, dict)):
            advertencias.append(
                "unidad '{0}' requiere entrada; no se inventa argumento".format(nombre)
            )
            resultados.append({
                "nombre": nombre,
                "estado": "OMITIDA",
                "razon": "requiere_entrada",
            })
            continue

        try:
            if unidad.get("requiere_entrada"):
                # Solo pasar peticion si la firma lo admite de forma legítima
                out = ref(peticion)
            else:
                out = ref()
            ejecutados += 1
            resultados.append({
                "nombre": nombre,
                "estado": "EXITO",
                "resultado": out if not isinstance(out, (dict, list)) else "<objeto>",
            })
        except Exception as e:
            errores.append({
                "nombre": nombre,
                "error": "{0}: {1}".format(type(e).__name__, e),
            })
            resultados.append({
                "nombre": nombre,
                "estado": "ERROR",
                "error": "{0}: {1}".format(type(e).__name__, e),
            })

    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "operacion": "ejecutar",
        "modo": "total",
        "inventario": {
            "total_componentes": inv.get("total_componentes", 0),
            "total_ejecutables": inv.get("total_ejecutables", 0),
        },
        "total_componentes": inv.get("total_componentes", 0),
        "total_ejecutables": inv.get("total_ejecutables", 0),
        "ejecutados": ejecutados,
        "resultados": resultados,
        "errores": errores,
        "advertencias": advertencias,
        "coherente": len(errores) == 0,
        "estado": ESTADO_OPERATIVO if len(errores) == 0 else ESTADO_DEGRADADO,
    }

# ===============================================================
# FIN 7.7
# ===============================================================


# ===============================================================
# 7.8 — AXIOMAS
# ===============================================================

def axiomas() -> List[Dict[str, Any]]:
    return [
        {
            "id": "CX-OP-1",
            "tipo": "axioma",
            "sujeto": "contexto",
            "relacion": "genera",
            "objeto": "marco_O",
            "polaridad": True,
            "enunciado": (
                "Este módulo genera el marco evaluable O a partir "
                "de la petición."
            ),
            "depende_de": [],
            "gobierna": ["contexto"],
        },
        {
            "id": "CX-OP-2",
            "tipo": "axioma",
            "sujeto": "permite_k",
            "relacion": "exige",
            "objeto": "registro_O_estable",
            "polaridad": True,
            "enunciado": (
                "permite_k es verdadero solo con registro estable "
                "que tenga O_id y enunciado_O."
            ),
            "depende_de": [],
            "gobierna": ["contexto"],
        },
        {
            "id": "CX-OP-3",
            "tipo": "axioma",
            "sujeto": "reglas_internas",
            "relacion": "unicidad",
            "objeto": "id_y_nombre",
            "polaridad": True,
            "enunciado": (
                "Los clasificadores internos no comparten id ni nombre."
            ),
            "depende_de": [],
            "gobierna": ["contexto"],
        },
        {
            "id": "CX-OP-4",
            "tipo": "axioma",
            "sujeto": "pedir_anuncio",
            "relacion": "implica",
            "objeto": "tipos_peticion_no_vacio",
            "polaridad": True,
            "enunciado": (
                "pedir_anuncio verdadero implica tipos_peticion no vacío."
            ),
            "depende_de": [],
            "gobierna": ["contexto"],
        },
        {
            "id": "CX-OP-5",
            "tipo": "axioma",
            "sujeto": "centinela",
            "relacion": "garantiza",
            "objeto": "coherencia_estructural_del_dominio",
            "polaridad": True,
            "enunciado": (
                "Todo *.py interno se valida por estructura, dominio "
                "y unicidad según el CONTENEDOR."
            ),
            "depende_de": ["CX-OP-3"],
            "gobierna": ["contexto"],
        },
        {
            "id": "CX-OP-6",
            "tipo": "axioma",
            "sujeto": "ejecucion_total",
            "relacion": "ejerce",
            "objeto": "todas_las_unidades_operativamente_ejecutables",
            "polaridad": True,
            "enunciado": (
                "La ejecución total ejerce todas las unidades operativamente "
                "ejecutables descubiertas dentro del módulo conforme al contrato "
                "y a sus leyes internas."
            ),
            "depende_de": ["CX-OP-5"],
            "gobierna": ["contexto"],
        },
        {
            "id": "CX-OP-7",
            "tipo": "axioma",
            "sujeto": "inventario_total",
            "relacion": "incluye",
            "objeto": "componentes_descubiertos",
            "polaridad": True,
            "enunciado": (
                "El inventario total registra los componentes existentes del módulo "
                "aunque no estén declarados como capacidades nominales."
            ),
            "depende_de": [],
            "gobierna": ["contexto"],
        },
    ]

# ===============================================================
# FIN 7.8
# ===============================================================


# ===============================================================
# 7.9 — FUNCIÓN AUXILIAR recibir_comentarios
# ===============================================================
#
# Función auxiliar; no forma parte de las capacidades contractuales
# declaradas en CONTENEDOR (decisión Option B).
# Debe ser descubierta por el inventario total.
# ===============================================================

def recibir_comentarios(paquetes: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recibe el paquete de comentarios entregado por el Engine.
    Función auxiliar; no forma parte de las capacidades contractuales
    declaradas en CONTENEDOR.
    """
    if not isinstance(paquetes, dict):
        return {
            "estado": "ERROR",
            "error": "paquetes debe ser dict"
        }

    return {
        "estado": "RECIBIDO",
        "total_modulos": len(paquetes),
        "modulos": list(paquetes.keys()),
        "paquetes": paquetes
    }

# ===============================================================
# FIN 7.9
# ===============================================================


# ===============================================================
# PARTE 8 — REPORTING INTERNO
# ===============================================================


# ===============================================================
# 8.1 — REPORTE
# ===============================================================

def reporte() -> Dict[str, Any]:
    audit = centinela()
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "dominio": CONTENEDOR.get("dominio"),
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "estado": (
            ESTADO_OPERATIVO if audit.get("coherente") else ESTADO_DEGRADADO
        ),
        "coherente": audit.get("coherente"),
        "reglas_n": audit.get("total", 0),
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") if isinstance(CONTENEDOR.get("requiere"), list) else []),
        "autoridad": CONTENEDOR.get("autoridad"),
        "conocimiento_exportable": CONTENEDOR.get("conocimiento_exportable"),
        "consultas_soportadas": CONTENEDOR.get("consultas_soportadas"),
    }

# ===============================================================
# FIN 8.1
# ===============================================================


# ===============================================================
# 8.2 — DIAGNÓSTICO
# ===============================================================

def diagnostico() -> Dict[str, Any]:
    audit = centinela()
    problemas: List[Dict[str, Any]] = []
    advertencias: List[str] = []
    recomendaciones: List[str] = []

    if audit.get("errores"):
        problemas.append({
            "tipo": "errores_clasificadores",
            "detalle": audit["errores"],
        })
        recomendaciones.append(
            "Corregir archivos internos con errores de forma o carga"
        )

    total = audit.get("total", 0)
    if not total:
        advertencias.append("Sin clasificadores internos")

    if audit.get("choques"):
        problemas.append({
            "tipo": "choques_id_nombre",
            "detalle": audit["choques"],
        })
        recomendaciones.append(
            "Unificar o renombrar reglas con id/nombre duplicado"
        )

    estado = ESTADO_OPERATIVO if audit.get("coherente") else ESTADO_DEGRADADO
    if not total and not problemas:
        estado = ESTADO_NO_INICIADO

    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "estado": estado,
        "problemas": problemas,
        "advertencias": advertencias,
        "recomendaciones": recomendaciones,
        "coherente": audit.get("coherente"),
        "errores_n": len(audit.get("errores") or []),
        "reglas_n": total,
    }

# ===============================================================
# FIN 8.2
# ===============================================================


# ===============================================================
# PARTE 9 — RESOLUCIÓN ESTRICTA DEL CONTRATO
# ===============================================================


# ===============================================================
# 9.1 — MAPA DE CAPACIDADES
# ===============================================================

_CAP_MAP = {
    "resolver": resolver,
    "evaluar": resolver,
    "centinela": centinela,
    "barrer": barrer,
    "verificar": verificar,
    "inventario": inventario,
    "reporte": reporte,
    "diagnostico": diagnostico,
    "axiomas": axiomas,
    "verificar_salida": verificar_salida,
    "ejecutar": ejecutar,
    "ejecutar_total": ejecutar,
    "registrar_inventario": registrar_inventario,
}

# ===============================================================
# FIN 9.1
# ===============================================================


# ===============================================================
# 9.2 — RESOLUCIÓN DE CAPACIDADES
# ===============================================================

def _resolver_capacidades(cont: Dict[str, Any]) -> None:
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
            "{0}: capacidad '{1}' tiene tipo inválido: {2}".format(
                NOMBRE_MODULO, nombre, type(ref).__name__
            )
        )
    cont["capacidades"] = resueltas

# ===============================================================
# FIN 9.2
# ===============================================================


# ===============================================================
# 9.3 — EJECUCIÓN DE VALIDACIÓN Y RESOLUCIÓN
# ===============================================================

_validar_contrato(CONTENEDOR)
_resolver_capacidades(CONTENEDOR)

# ===============================================================
# FIN 9.3
# ===============================================================


# ===============================================================
# PARTE 10 — EXPORTACIONES
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
    "UNDEFINED",
    "es_undefined",
    "ContextoError",
    "ContratoInvalido",
    "resolver",
    "centinela",
    "barrer",
    "verificar",
    "verificar_salida",
    "inventario",
    "axiomas",
    "reporte",
    "diagnostico",
    "ejecutar",
    "registrar_inventario",
]

# ===============================================================
# FIN PARTE 10
# ===============================================================


# ===============================================================
# PARTE 11 — EXTENSIONES FUTURAS
# ===============================================================
#
# Capacidad nueva → capacidades + capacidades_meta + _CAP_MAP
# + VERSION_MODULO (solo si el contrato lo exige)
#
# Clasificador nuevo → *.py en este directorio con REGLA
# y/o clasificar()/validar(). Descubrimiento automático.
#
# ===============================================================
# FIN PARTE 11
# ===============================================================


# ===============================================================
# FIN DEL MÓDULO
# ===============================================================
