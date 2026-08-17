# ===============================================================
# VPSI-TRUTH — modules/capacidades_engine/__init__.py
# ===============================================================
#
# MÓDULO:              capacidades_engine
# ID:                  CE
# Rol:                 CE
# Versión módulo:      1.2
# Versión contrato:    1.0
# Esquema contrato:    VPSI-CONTRACT-1.0
# Estabilidad:         ESTABLE
# Compatible desde:    1.0
# API Engine:          >=1.0
#
# Jerarquía:
#   Engine → Capacidad (CE) → Skills / Mandatos → Archivos
#
# CE descubre, valida y expone skills.
# Solo Engine ejecuta.
#
# Capacidades arquitectónicas (callables reales):
#   ejecutar_total, inspeccionar, registrar_inventario
#
# ===============================================================


# ===============================================================
# PARTE 1 — PRINCIPIOS, BANDERAS Y ESPECIFICACIONES PRECISAS
# ===============================================================

# ===============================================================
# IMPORTACIONES
# ===============================================================

from __future__ import annotations

# --- Estándar del lenguaje ---
import sys
import math
import ast
import copy
import threading
import importlib.util

# --- Tipos y estructuras ---
from typing import Any, Dict, List, Optional, Set, Tuple
from collections import defaultdict

# --- Números y precisión ---
from decimal import Decimal, getcontext
from fractions import Fraction

# --- Sistema de archivos ---
from pathlib import Path


# ===============================================================
# FIN 1.1
# ===============================================================


# ===============================================================
# 1.2 — IDENTIDAD
# ===============================================================

ID_MODULO = "CE"
NOMBRE_MODULO = "capacidades_engine"
ROL_MODULO = "CE"

# ===============================================================
# FIN 1.2
# ===============================================================


# ===============================================================
# 1.3 — VERSIONES Y ESTABILIDAD
# ===============================================================

VERSION_MODULO = "1.2"
VERSION_CONTRATO = "1.0"
ESQUEMA_CONTRATO = "VPSI-CONTRACT-1.0"
COMPATIBLE_DESDE = "1.0"
API_ENGINE = ">=1.0"
ESTABILIDAD = "ESTABLE"

# ===============================================================
# FIN 1.3
# ===============================================================


# ===============================================================
# 1.4 — BANDERAS DE ESTADO
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
# FIN 1.4
# ===============================================================


# ===============================================================
# 1.5 — INVARIANTES
# ===============================================================

INVARIANTES = (
    "el id del módulo nunca cambia",
    "el rol nunca cambia",
    "CE es una capacidad estructural; los skills son competencias operativas",
    "Engine es la única autoridad que ejecuta los skills expuestos por CE",
    "CE únicamente descubre, valida y expone skills",
    "CE no toma decisiones ni selecciona skills",
    "CE no coordina ciclos ni interpreta peticiones",
    "las capacidades declaradas son callables tras la resolución",
    "este módulo no modifica el estado de otros módulos",
    "este módulo no inventa capacidades no declaradas en CONTENEDOR",
    "este módulo siempre puede reportar su propio estado",
    "CE debe figurar en ROLES de core/engine.py",
    "inventario() siempre incluye id, nombre, rol, version del CONTENEDOR",
)

# ===============================================================
# FIN 1.5
# ===============================================================


# ===============================================================
# 1.6 — CONFIGURACIÓN
# ===============================================================

_DIR = Path(__file__).resolve().parent
_CAP = _DIR

# ===============================================================
# FIN 1.6
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
        "Capacidad estructural del Engine: órgano único que agrupa "
        "múltiples skills nativos. Así como un brazo posee varias "
        "habilidades sin dejar de ser un solo órgano, CE agrupa skills "
        "sin ser un módulo de dominio. Los archivos son implementación "
        "física; los skills son competencias operativas; el mandato es "
        "la forma en que Engine los invoca. Engine no pide permiso a CE: "
        "los skills forman parte de su propia estructura. "
        "CE mantiene el inventario operativo de esas capacidades nativas."
    ),

    # ============================================================
    # 5.3 — PROPÓSITO
    # ============================================================
    "funcion": (
        "Mantener el inventario operativo de skills nativos del Engine. "
        "El descubrimiento automático de *.py actualiza ese inventario. "
        "Validar forma mínima y exponer ids/skills a Engine. "
        "No calcular. No depositar. No ejecutar. No decidir."
    ),
    "no_hace": [
        "No toma decisiones",
        "No selecciona skills",
        "No ejecuta skills (solo Engine ejecuta)",
        "No coordina ciclos",
        "No interpreta peticiones",
        "No calcula C / L / K / Tru",
        "No deposita evidencia",
        "No orquesta el sistema",
        "No compite con módulos de dominio (AX, CA, CH, TT, SF, …)",
    ],

    # ============================================================
    # 5.4 — AUTORIDAD
    # ============================================================
    "autoridad": [
        "Mantener el inventario operativo de skills nativos del Engine",
        "Descubrir y validar forma mínima de cada skill",
        "Exponer ids y skills a Engine",
        "Reportar estado e inventario propios",
    ],

    # ============================================================
    # 5.5 — CONOCIMIENTO EXPORTABLE
    # ============================================================
    "conocimiento_exportable": [
        "skills",
        "ids",
        "por_id",
        "listar_archivos",
        "inventario",
        "barrer",
        "verificar",
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
    "AX", "FO", "MC", "SF",
    "CA", "CX", "DI", "RE", "VX",
    "TX", "CH", "CIT", "DGCO", "UI",
    "CC", "TT", "SC",
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

        # --- PERMISOS OBLIGATORIOS ---
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
        "listar_skills",
        "listar_ids",
        "obtener_por_id",
        "listar_archivos",
        "obtener_inventario",
        "verificar_coherencia",
        "ejecutar_total",
        "inspeccionar",
        "registrar_inventario",
    ],

        # ============================================================
    # 5.12 — CAPACIDADES
    # ============================================================
    "capacidades": {
        "verificar": "verificar",
        "barrer": "barrer",
        "inventario": "inventario",
        "skills": "skills",
        "ids": "ids",
        "por_id": "por_id",
        "listar_archivos": "listar_archivos",
        "verificar_salida": "verificar_salida",
        "ejecutar_total": "ejecutar_total",
        "inspeccionar": "inspeccionar",
        "registrar_inventario": "registrar_inventario",
        "reporte": "reporte",
        "diagnostico": "diagnostico",
    },

    # ============================================================
    # 5.13 — METADATOS DE CAPACIDADES (1:1 OBLIGATORIO)
    # ============================================================
    "capacidades_meta": {
        "verificar": {
            "descripcion": (
                "Alias de barrer. ¿El inventario operativo de skills "
                "de CE es coherente?"
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con id, nombre, rol, version, coherente, ids, errores"
            ),
            "acceso_archivos": ["*"],
        },
        "barrer": {
            "descripcion": (
                "Centinela de CE: valida forma de skills nativos. "
                "No decide, no ejecuta, no restringe uso."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con id, nombre, rol, version, coherente, "
                "ids, n, archivos"
            ),
            "acceso_archivos": ["acceso_archivos"],
        },
        "inventario": {
            "descripcion": (
                "Inventario operativo de skills nativos del Engine "
                "expuestos por la capacidad CE."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con id, nombre, rol, version, version_contrato, "
                "esquema, estabilidad, ids, n, archivos, skills, coherente"
            ),
            "acceso_archivos": ["*"],
        },
        "skills": {
            "descripcion": (
                "Lista de skills válidos (nombre histórico de la API)."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "list[dict] con id, nombre, version, descripcion, archivo"
            ),
            "acceso_archivos": ["*"],
        },
        "ids": {
            "descripcion": "Ids de todos los skills válidos de CE.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "list[str]",
            "acceso_archivos": ["*"],
        },
        "por_id": {
            "descripcion": "Resuelve un skill por id.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict del skill o None",
            "acceso_archivos": ["*"],
        },
        "listar_archivos": {
            "descripcion": (
                "Nombres de *.py del directorio CE "
                "(implementación física de los skills)."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "list[str]",
            "acceso_archivos": ["*"],
        },
        "verificar_salida": {
            "descripcion": "Comprueba forma mínima de una salida de CE.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "bool",
            "acceso_archivos": ["*"],
        },
        "ejecutar_total": {
            "descripcion": (
                "Autoridad total de ENGINE sobre CE. "
                "Ejerce TODAS las unidades operativamente ejecutables "
                "del módulo conforme a su contrato e inventario. "
                "Todo es callable real. No inventa capacidades."
            ),
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["*"],
            "salida": "dict con resultados de todas las unidades ejecutadas",
            "acceso_archivos": ["*"],
        },
        "inspeccionar": {
            "descripcion": (
                "Capacidad meta de inspeccion estructural de CE. "
                "Expone constantes, capacidades, skills y estado "
                "sin alterar el contrato ni ejecutar skills."
            ),
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["acceso_archivos"],
            "salida": "dict con estructura, capacidades y estado del modulo",
            "acceso_archivos": ["acceso_archivos"],
        },
                "registrar_inventario": {
            "descripcion": (
                "Registra el inventario estructural de CE "
                "como instantanea determinista. No altera evidencia."
            ),
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["acceso_archivos"],
            "salida": "dict con inventario registrado",
            "acceso_archivos": ["acceso_archivos"],
        },
        "reporte": {
            "descripcion": (
                "Reporte de estado de CE: coherencia del inventario "
                "de skills, ids, archivos y capacidades declaradas."
            ),
            "entrada": "ninguna",
            "validar_esquema": ["*"],
            "salida": (
                "dict con estado, coherente, ids, n, archivos, "
                "capacidades, operaciones_arquitectonicas"
            ),
            "acceso_archivos": ["*"],
        },
        "diagnostico": {
            "descripcion": (
                "Diagnostico de problemas y recomendaciones "
                "sobre el inventario operativo de skills de CE."
            ),
            "entrada": "ninguna",
            "validar_esquema": ["*"],
            "salida": (
                "dict con estado, problemas, advertencias, "
                "recomendaciones, coherente, ids, archivos"
            ),
            "acceso_archivos": ["*"],
        },
    },

        # ============================================================
    # 5.14 — REPORTING
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
    # 5.15 — ESTADOS VÁLIDOS
    # ============================================================
    "estados_validos": list(ESTADOS_VALIDOS),

    # ============================================================
    # 5.16 — INVARIANTES
    # ============================================================
    "invariantes": list(INVARIANTES),
}

# ===============================================================
# FIN PARTE 5
# ===============================================================


# ===============================================================
# PARTE 7 — FUNCIONES PRIVADAS
# ===============================================================

# ===============================================================
# 7.1 — EXTRACCIÓN DE META
# ===============================================================

def _extraer_meta(mod: Any) -> Optional[Dict[str, Any]]:
    """
    Acepta SKILL / CAPACIDAD (dict) o SKILLS / CAPACIDADES (list).
    Compatibilidad con mandatos existentes.
    Normaliza descripcion <- enunciado si hace falta.
    """
    for attr in ("SKILL", "CAPACIDAD", "SKILLS", "CAPACIDADES"):
        raw = getattr(mod, attr, None)
        candidatos: List[Dict[str, Any]] = []
        if isinstance(raw, dict):
            candidatos = [raw]
        elif isinstance(raw, list):
            candidatos = [x for x in raw if isinstance(x, dict)]
        for meta in candidatos:
            sid = str(meta.get("id") or "").strip().lower()
            if not sid:
                continue
            meta = dict(meta)
            if not str(meta.get("descripcion") or "").strip():
                for alt in ("enunciado", "descripcion_larga", "nota"):
                    if str(meta.get(alt) or "").strip():
                        meta["descripcion"] = str(meta[alt]).strip()
                        break
            if not str(meta.get("nombre") or "").strip():
                meta["nombre"] = sid
            if not str(meta.get("version") or "").strip():
                meta["version"] = "1.0"
            if not str(meta.get("descripcion") or "").strip():
                meta["descripcion"] = (
                    "skill nativo del Engine: {0}".format(sid)
                )
            return meta
    return None

# ===============================================================
# FIN 7.1
# ===============================================================

# ===============================================================
# 7.2 — CARGA DE SKILLS
# ===============================================================

def _cargar_skills() -> Dict[str, Dict[str, Any]]:
    """
    Lee los *.py del directorio CE y conserva toda la evidencia
    estructural encontrada.

    Cada archivo válido puede implementar uno o más skills de la
    capacidad estructural CE.

    Los IDs duplicados no se sobrescriben silenciosamente: se
    conservan como evidencia estructural para que el centinela
    pueda declarar el choque de forma determinista.
    """
    hallado: Dict[str, Dict[str, Any]] = {}
    if not _CAP.is_dir():
        return hallado

    for f in sorted(_CAP.glob("*.py")):
        if f.name.startswith("_"):
            continue

        clave = "ce_skill_{0}".format(f.stem)
        spec = importlib.util.spec_from_file_location(clave, str(f))

        if spec is None or spec.loader is None:
            hallado[f.stem] = {
                "archivo": f.name,
                "error": "spec_invalido",
            }
            continue

        mod = importlib.util.module_from_spec(spec)
        sys.modules[clave] = mod

        try:
            spec.loader.exec_module(mod)
        except Exception as e:
            hallado[f.stem] = {
                "archivo": f.name,
                "error": "{0}: {1}".format(type(e).__name__, e),
            }
            continue

        meta = _extraer_meta(mod)

        if meta is None:
            hallado[f.stem] = {
                "archivo": f.name,
                "error": "sin SKILL/CAPACIDAD con id",
            }
            continue

        sid = str(meta["id"]).strip().lower()

        registro = {
            "archivo": f.name,
            "id": sid,
            "nombre": meta.get("nombre"),
            "version": str(meta.get("version") or "1.0"),
            "descripcion": str(meta.get("descripcion") or ""),
            "oficio": meta.get("oficio"),
            "material": meta.get("material"),
            "requiere_catalogo": meta.get("requiere_catalogo"),
            "raw": meta,
        }

        existente = hallado.get(sid)

        if existente is None:
            hallado[sid] = registro
            continue

        if "_choques" not in hallado:
            hallado["_choques"] = []

        hallado["_choques"].append({
            "tipo": "id_duplicado",
            "id": sid,
            "archivos": [
                existente.get("archivo"),
                f.name,
            ],
        })

    return hallado

# ===============================================================
# FIN 7.2
# ===============================================================


# ===============================================================
# 7.3 — VALIDACIÓN DE SKILLS
# ===============================================================

def _validar_skills(hallado: Dict[str, Dict[str, Any]]) -> List[str]:
    errores: List[str] = []
    por_id: Dict[str, List[str]] = {}
    for sid, meta in sorted(hallado.items()):
        if meta.get("error"):
            if "sin SKILL" not in str(meta.get("error")):
                errores.append("{0}: {1}".format(sid, meta["error"]))
            continue
        for k in ("id", "nombre", "version", "descripcion"):
            if not str(meta.get(k) or "").strip():
                errores.append(
                    "skill '{0}': falta '{1}'".format(sid, k)
                )
        por_id.setdefault(sid, []).append(meta.get("archivo") or sid)
    for sid, archivos in por_id.items():
        if len(archivos) > 1:
            errores.append(
                "id '{0}' repetido en {1}".format(sid, archivos)
            )
    return errores

# ===============================================================
# FIN 7.3
# ===============================================================

# ===============================================================
# 7.4 — VALIDACIÓN DEL CONTRATO
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
            f"{NOMBRE_MODULO}: CONTENEDOR incompleto. Faltan: {faltantes}"
        )

    if cont.get("esquema") != ESQUEMA_CONTRATO:
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: esquema incompatible"
        )

    if str(cont.get("version_contrato")) != VERSION_CONTRATO:
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: version_contrato invalida"
        )

    capacidades = cont.get("capacidades")
    capacidades_meta = cont.get("capacidades_meta")

    if not isinstance(capacidades, dict):
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: 'capacidades' debe ser dict"
        )

    if not isinstance(capacidades_meta, dict):
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: 'capacidades_meta' debe ser dict"
        )

    nombres_capacidades = set(capacidades.keys())
    nombres_meta = set(capacidades_meta.keys())

    faltantes_meta = sorted(
        nombres_capacidades - nombres_meta
    )

    if faltantes_meta:
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: capacidades sin capacidades_meta: "
            f"{faltantes_meta}"
        )

    metas_sin_capacidad = sorted(
        nombres_meta - nombres_capacidades
    )

    if metas_sin_capacidad:
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: capacidades_meta sin capacidad declarada: "
            f"{metas_sin_capacidad}"
        )

    for nombre_cap in capacidades:
        entrada = capacidades_meta[nombre_cap]

        if not isinstance(entrada, dict):
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: capacidades_meta['{nombre_cap}'] "
                f"debe ser dict"
            )

        for campo in ("descripcion", "entrada", "salida"):
            if campo not in entrada or not isinstance(entrada[campo], str):
                raise ContratoInvalido(
                    f"{NOMBRE_MODULO}: capacidades_meta['{nombre_cap}'] "
                    f"requiere '{campo}: str'"
                )

# ===============================================================
# FIN 7.4
# ===============================================================

# ===============================================================
# FIN PARTE 7
# ===============================================================


# ===============================================================
# PARTE 8 — CAPACIDADES PÚBLICAS
# ===============================================================

# ===============================================================
# 8.1 — SKILLS
# ===============================================================

def skills() -> List[Dict[str, Any]]:
    """
    Todos los skills válidos de la capacidad CE — a disposición
    del Engine. Nombre histórico de la API.

    Los skills con errores estructurales no se convierten en
    capacidades válidas ni se descartan silenciosamente: su
    existencia y error quedan expuestos en la salida para mantener
    la trazabilidad contractual.
    """
    hallado = _cargar_skills()
    out: List[Dict[str, Any]] = []

    for sid, meta in sorted(hallado.items()):
        if meta.get("error"):
            out.append({
                "id": meta.get("id") or sid,
                "nombre": meta.get("nombre"),
                "version": meta.get("version"),
                "descripcion": meta.get("descripcion"),
                "archivo": meta.get("archivo"),
                "oficio": meta.get("oficio"),
                "material": meta.get("material"),
                "error": meta.get("error"),
                "valido": False,
            })
            continue

        out.append({
            "id": meta.get("id"),
            "nombre": meta.get("nombre"),
            "version": meta.get("version"),
            "descripcion": meta.get("descripcion"),
            "archivo": meta.get("archivo"),
            "oficio": meta.get("oficio"),
            "material": meta.get("material"),
            "valido": True,
        })

    return out

# ===============================================================
# FIN 8.1
# ===============================================================


# ===============================================================
# 8.2 — IDS
# ===============================================================

def ids() -> List[str]:
    """Todos los ids de skills válidos — Engine los usa cuando quiera."""
    return [s["id"] for s in skills() if s.get("id") and s.get("valido", True)]

# ===============================================================
# FIN 8.2
# ===============================================================


# ===============================================================
# 8.3 — POR ID
# ===============================================================

def por_id(skill_id: str) -> Optional[Dict[str, Any]]:
    if not skill_id:
        return None
    clave = str(skill_id).strip().lower()
    for s in skills():
        if s.get("id") == clave and s.get("valido", True):
            return s
    return None

# ===============================================================
# FIN 8.3
# ===============================================================


# ===============================================================
# 8.4 — LISTAR ARCHIVOS
# ===============================================================

def listar_archivos() -> List[str]:
    """
    Nombres de todo *.py del directorio CE.
    Archivo = implementación física del skill.
    """
    if not _CAP.is_dir():
        return []
    return [
        p.name for p in sorted(_CAP.glob("*.py"))
        if not p.name.startswith("_")
    ]

# ===============================================================
# 8.5 — BARRER
# ===============================================================

def barrer() -> Dict[str, Any]:
    """
    Centinela contractual determinista de CE.

    Verifica exclusivamente la estructura demostrable del módulo:
    contrato → capacidades declaradas → capacidades_meta → callable real,
    y archivo físico → módulo cargable → metadatos válidos → id canónico.

    No ejecuta skills.
    No selecciona skills.
    No interpreta peticiones.
    No calcula.
    No deposita evidencia.
    No modifica el contrato.
    No crea capacidades.
    No promueve archivos extra a capacidades.
    """
    errores: List[str] = []
    choques: List[str] = []

    # -----------------------------------------------------------
    # 8.5.1 — VALIDACIÓN DEL CONTRATO
    # -----------------------------------------------------------

    try:
        _validar_contrato(CONTENEDOR)
    except Exception as e:
        errores.append(
            "contrato: {0}: {1}".format(type(e).__name__, e)
        )

    # -----------------------------------------------------------
    # 8.5.2 — CARGA DETERMINISTA DEL INVENTARIO FÍSICO
    # -----------------------------------------------------------

    hallado = _cargar_skills()
    archivos = listar_archivos()

    # -----------------------------------------------------------
    # 8.5.3 — VALIDACIÓN DE SKILLS
    # -----------------------------------------------------------

    errores.extend(_validar_skills(hallado))

    # -----------------------------------------------------------
    # 8.5.4 — IDS CANÓNICOS
    # -----------------------------------------------------------

    lista_ids = sorted(
        sid
        for sid, meta in hallado.items()
        if not meta.get("error")
    )

    # -----------------------------------------------------------
    # 8.5.5 — CORRESPONDENCIA ARCHIVO ↔ SKILL
    # -----------------------------------------------------------

    archivos_validos = sorted(
        str(meta.get("archivo"))
        for meta in hallado.values()
        if not meta.get("error") and meta.get("archivo")
    )

    archivos_sin_skill = sorted(
        archivo
        for archivo in archivos
        if archivo not in archivos_validos
    )

    for archivo in archivos_sin_skill:
        errores.append(
            "archivo '{0}' no posee skill válido declarado".format(
                archivo
            )
        )

    # -----------------------------------------------------------
    # 8.5.6 — CORRESPONDENCIA CAPACIDADES ↔ META
    # -----------------------------------------------------------

    capacidades = CONTENEDOR.get("capacidades")

    if not isinstance(capacidades, dict):
        errores.append(
            "capacidades: debe ser dict"
        )
        capacidades = {}

    capacidades_meta = CONTENEDOR.get("capacidades_meta")

    if not isinstance(capacidades_meta, dict):
        errores.append(
            "capacidades_meta: debe ser dict"
        )
        capacidades_meta = {}

    nombres_capacidades = sorted(capacidades.keys())
    nombres_meta = sorted(capacidades_meta.keys())

    faltantes_meta = sorted(
        set(nombres_capacidades) - set(nombres_meta)
    )

    extras_meta = sorted(
        set(nombres_meta) - set(nombres_capacidades)
    )

    for nombre in faltantes_meta:
        errores.append(
            "capacidad '{0}' declarada sin capacidades_meta".format(
                nombre
            )
        )

    for nombre in extras_meta:
        errores.append(
            "capacidades_meta '{0}' no corresponde a capacidad declarada".format(
                nombre
            )
        )

    # -----------------------------------------------------------
    # 8.5.7 — RESOLUCIÓN REAL DE CAPACIDADES
    # -----------------------------------------------------------

    for nombre in nombres_capacidades:
        referencia = capacidades.get(nombre)

        if not callable(referencia):
            errores.append(
                "capacidad '{0}' no resuelve a callable real".format(
                    nombre
                )
            )

    # -----------------------------------------------------------
    # 8.5.8 — CORRESPONDENCIA 1:1 DECLARADA ↔ RESUELTA
    # -----------------------------------------------------------

    if nombres_capacidades != nombres_meta:
        choques.append(
            "capacidades y capacidades_meta no mantienen correspondencia 1:1"
        )

    # -----------------------------------------------------------
    # 8.5.9 — IDS DUPLICADOS
    # -----------------------------------------------------------

    ids_vistos: Dict[str, List[str]] = {}

    for sid, meta in sorted(hallado.items()):
        if meta.get("error"):
            continue

        archivo = str(meta.get("archivo") or sid)
        ids_vistos.setdefault(sid, []).append(archivo)

    for sid, fuentes in sorted(ids_vistos.items()):
        if len(fuentes) > 1:
            choques.append(
                "id '{0}' repetido en {1}".format(
                    sid,
                    sorted(fuentes),
                )
            )

    # -----------------------------------------------------------
    # 8.5.10 — ERRORES DE CARGA NO SILENCIADOS
    # -----------------------------------------------------------

    for sid, meta in sorted(hallado.items()):
        if not meta.get("error"):
            continue

        error = str(meta.get("error") or "").strip()

        if not error:
            errores.append(
                "skill '{0}' presenta error de carga no descrito".format(
                    sid
                )
            )
            continue

        errores.append(
            "skill '{0}': {1}".format(sid, error)
        )

    # -----------------------------------------------------------
    # 8.5.11 — DETERMINACIÓN DE COHERENCIA
    # -----------------------------------------------------------

    errores = sorted(set(errores))
    choques = sorted(set(choques))

    coherente = not errores and not choques

    # -----------------------------------------------------------
    # 8.5.12 — NOTAS ESTRUCTURALES
    # -----------------------------------------------------------

    notas: List[str] = []

    if not _CAP.is_dir():
        notas.append("directorio CE no existe")

    if not lista_ids:
        notas.append(
            "ningún skill válido encontrado en CE"
        )

    if archivos_sin_skill:
        notas.append(
            "existen archivos físicos sin skill contractual válido"
        )

    # -----------------------------------------------------------
    # 8.5.13 — SALIDA CONTRACTUAL DETERMINISTA
    # -----------------------------------------------------------

    return {
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "contenedor": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "coherente": coherente,
        "errores": errores,
        "choques": choques,
        "ids": lista_ids,
        "n": len(lista_ids),
        "archivos": archivos,
        "archivos_validos": archivos_validos,
        "archivos_sin_skill": archivos_sin_skill,
        "capacidades_declaradas": nombres_capacidades,
        "capacidades_meta": nombres_meta,
        "capacidades_callable": sorted(
            nombre
            for nombre in nombres_capacidades
            if callable(capacidades.get(nombre))
        ),
        "n_capacidades": len(nombres_capacidades),
        "n_capacidades_meta": len(nombres_meta),
        "n_capacidades_callable": len(
            [
                nombre
                for nombre in nombres_capacidades
                if callable(capacidades.get(nombre))
            ]
        ),
        "notas": sorted(set(notas)),
        "ruta_capacidades": str(_CAP),
        "nota": (
            "CE es la capacidad estructural del Engine que agrupa "
            "skills nativos. Engine es la única autoridad de ejecución. "
            "CE solo descubre, valida y expone. La coherencia contractual "
            "requiere correspondencia 1:1 entre capacidades declaradas, "
            "capacidades_meta y callables reales."
        ),
    }

# ===============================================================
# FIN 8.5
# ===============================================================


# ===============================================================
# 8.6 — VERIFICAR
# ===============================================================

def verificar() -> Dict[str, Any]:
    """Alias contractual real de barrer."""
    return barrer()

# ===============================================================
# FIN 8.6
# ===============================================================


# ===============================================================
# 8.7 — INVENTARIO
# ===============================================================

def inventario(peticion: Any = None) -> Dict[str, Any]:
    """
    Inventario operativo y estructural de CE.

    Expone únicamente información demostrable del contrato,
    las capacidades resueltas, los skills descubiertos y el
    estado producido por el centinela.
    """
    b = barrer()

    capacidades_declaradas = sorted(
        CONTENEDOR.get("capacidades", {}).keys()
    )

    capacidades_meta = sorted(
        CONTENEDOR.get("capacidades_meta", {}).keys()
    )

    capacidades_callable = sorted(
        nombre
        for nombre in capacidades_declaradas
        if callable(CONTENEDOR["capacidades"].get(nombre))
    )

    return {
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "contenedor": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "compatible_desde": COMPATIBLE_DESDE,
        "api_engine": API_ENGINE,
        "ids": list(b.get("ids", [])),
        "n": int(b.get("n", 0)),
        "archivos": list(b.get("archivos", [])),
        "archivos_validos": list(b.get("archivos_validos", [])),
        "archivos_sin_skill": list(b.get("archivos_sin_skill", [])),
        "coherente": bool(b.get("coherente")),
        "errores": list(b.get("errores", [])),
        "choques": list(b.get("choques", [])),
        "notas": list(b.get("notas", [])),
        "skills": skills(),
        "capacidades": capacidades_declaradas,
        "capacidades_meta": capacidades_meta,
        "capacidades_callable": capacidades_callable,
        "n_capacidades": len(capacidades_declaradas),
        "n_capacidades_meta": len(capacidades_meta),
        "n_capacidades_callable": len(capacidades_callable),
        "funcion": (
            "Capacidad estructural del Engine. "
            "Mantiene el inventario operativo de skills nativos. "
            "Cada archivo implementa uno o más skills. "
            "Engine es la única autoridad que los ejecuta. "
            "CE no calcula, no deposita, no decide, no selecciona."
        ),
    }

# ===============================================================
# FIN 8.7
# ===============================================================


# ===============================================================
# 8.8 — VERIFICAR SALIDA
# ===============================================================

def verificar_salida(salida: Any) -> bool:
    """
    Verifica la forma mínima demostrable de una salida estructural
    de CE.

    La salida debe ser un dict perteneciente inequívocamente a CE.
    Si contiene 'coherente', debe ser bool.
    Si contiene 'errores' o 'choques', deben ser listas.
    Debe contener al menos un campo estructural reconocido.
    """
    if not isinstance(salida, dict):
        return False

    if salida.get("id") != ID_MODULO:
        return False

    campos_estructurales = (
        "nombre",
        "modulo",
        "contenedor",
        "rol",
        "version",
        "operacion",
        "coherente",
        "ids",
        "capacidades",
        "capacidades_ejecutadas",
        "resultados",
        "inventario",
    )

    if not any(
        campo in salida
        for campo in campos_estructurales
    ):
        return False

    if "coherente" in salida and not isinstance(
        salida["coherente"],
        bool,
    ):
        return False

    if "errores" in salida and not isinstance(
        salida["errores"],
        list,
    ):
        return False

    if "choques" in salida and not isinstance(
        salida["choques"],
        list,
    ):
        return False

    if "ids" in salida and not isinstance(
        salida["ids"],
        list,
    ):
        return False

    if "capacidades" in salida and not isinstance(
        salida["capacidades"],
        list,
    ):
        return False

    if "capacidades_ejecutadas" in salida and not isinstance(
        salida["capacidades_ejecutadas"],
        list,
    ):
        return False

    return True

# ===============================================================
# FIN 8.8
# ===============================================================


# ===============================================================
# 8.9 — EJECUTAR TOTAL
# ===============================================================

def ejecutar_total(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Autoridad total de ENGINE sobre CE.

    Recorre las capacidades declaradas en CONTENEDOR después
    de su resolución contractual y ejerce únicamente los
    callables reales que pertenecen al contrato.

    No mantiene una lista paralela de capacidades.
    No inventa capacidades.
    No incorpora funciones externas.
    No ejecuta recursivamente ejecutar_total.
    """
    peticion = (
        dict(peticion)
        if isinstance(peticion, dict)
        else {}
    )

    capacidades = CONTENEDOR.get("capacidades", {})

    if not isinstance(capacidades, dict):
        return {
            "id": ID_MODULO,
            "modulo": NOMBRE_MODULO,
            "rol": ROL_MODULO,
            "version": VERSION_MODULO,
            "operacion": "ejecutar_total",
            "estado": ESTADO_RECHAZADO,
            "coherente": False,
            "capacidades_ejecutadas": [],
            "capacidades_declaradas": [],
            "errores_ejecucion": [
                "CONTENEDOR['capacidades'] no es dict"
            ],
            "resultados": {},
            "nota": (
                "ejecutar_total no puede ejercer el contrato porque "
                "las capacidades no tienen estructura contractual válida."
            ),
        }

    resultados: Dict[str, Any] = {}
    errores_ejecucion: List[str] = []
    capacidades_declaradas = sorted(capacidades.keys())

    # -----------------------------------------------------------
    # 8.9.1 — RECORRIDO CONTRACTUAL
    # -----------------------------------------------------------

    for nombre in capacidades_declaradas:
        # ejecutar_total es la autoridad que está ejecutándose;
        # invocarlo desde sí mismo produciría recursión contractual.
        if nombre == "ejecutar_total":
            continue

        callable_real = capacidades.get(nombre)

        # -------------------------------------------------------
        # 8.9.2 — COMPROBACIÓN DE CALLABLE
        # -------------------------------------------------------

        if not callable(callable_real):
            errores_ejecucion.append(
                "capacidad '{0}': referencia no callable".format(
                    nombre
                )
            )
            resultados[nombre] = None
            continue

        # -------------------------------------------------------
        # 8.9.3 — EJECUCIÓN REAL
        # -------------------------------------------------------

        try:
            if nombre in (
                "inventario",
                "inspeccionar",
                "registrar_inventario",
            ):
                resultado = callable_real(peticion)
            else:
                resultado = callable_real()

            resultados[nombre] = resultado

        except Exception as e:
            errores_ejecucion.append(
                "capacidad '{0}': {1}: {2}".format(
                    nombre,
                    type(e).__name__,
                    e,
                )
            )
            resultados[nombre] = None

    # -----------------------------------------------------------
    # 8.9.4 — CAPACIDADES EJECUTADAS
    # -----------------------------------------------------------

    capacidades_ejecutadas = sorted(
        nombre
        for nombre, resultado in resultados.items()
        if resultado is not None
    )

    # -----------------------------------------------------------
    # 8.9.5 — VALIDACIÓN DE SALIDAS
    # -----------------------------------------------------------

    for nombre in capacidades_ejecutadas:
        resultado = resultados.get(nombre)

        if isinstance(resultado, dict):
            if not verificar_salida(resultado):
                errores_ejecucion.append(
                    "capacidad '{0}': salida estructural inválida".format(
                        nombre
                    )
                )

    # -----------------------------------------------------------
    # 8.9.6 — COHERENCIA CONTRACTUAL FINAL
    # -----------------------------------------------------------

    coherente = not errores_ejecucion

    if not capacidades_declaradas:
        coherente = False
        errores_ejecucion.append(
            "el contrato no declara capacidades ejecutables"
        )

    # -----------------------------------------------------------
    # 8.9.7 — ESTADO OPERATIVO
    # -----------------------------------------------------------

    estado = (
        ESTADO_OPERATIVO
        if coherente
        else ESTADO_DEGRADADO
    )

    # -----------------------------------------------------------
    # 8.9.8 — SALIDA DETERMINISTA
    # -----------------------------------------------------------

    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "operacion": "ejecutar_total",
        "estado": estado,
        "coherente": coherente,
        "capacidades_declaradas": capacidades_declaradas,
        "capacidades_ejecutadas": capacidades_ejecutadas,
        "n_capacidades_declaradas": len(
            capacidades_declaradas
        ),
        "n_capacidades_ejecutadas": len(
            capacidades_ejecutadas
        ),
        "errores_ejecucion": sorted(
            set(errores_ejecucion)
        ),
        "resultados": resultados,
        "nota": (
            "ejecutar_total ejerce autoridad total de ENGINE sobre CE "
            "recorriendo exclusivamente las capacidades declaradas "
            "en el contrato y resueltas a callables reales. "
            "No utiliza listas manuales paralelas, no inventa "
            "capacidades y no ejecuta recursivamente ejecutar_total."
        ),
    }

# ===============================================================
# FIN 8.9
# ===============================================================
# ===============================================================
# 8.10 — INSPECCIONAR
# ===============================================================

def inspeccionar(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Inspección estructural de CE.

    Expone el contrato, las capacidades declaradas, sus metadatos,
    el mapa de resolución, el inventario de skills y el estado
    estructural del módulo.

    No ejecuta skills.
    No selecciona skills.
    No modifica CONTENEDOR.
    No modifica estado de otros módulos.
    """
    if peticion is not None and not isinstance(peticion, dict):
        raise TypeError(
            f"{NOMBRE_MODULO}: 'peticion' debe ser dict o None"
        )

    res_barrer = barrer()

    capacidades_declaradas = list(
        CONTENEDOR.get("capacidades", {}).keys()
    )

    capacidades_meta = list(
        CONTENEDOR.get("capacidades_meta", {}).keys()
    )

    capacidades_resueltas = {
        nombre: callable(ref)
        for nombre, ref in CONTENEDOR.get("capacidades", {}).items()
    }

    capacidades_no_resueltas = sorted(
        nombre
        for nombre, resoluble in capacidades_resueltas.items()
        if not resoluble
    )

    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "operacion": "inspeccionar",

        "constantes": {
            "ID_MODULO": ID_MODULO,
            "NOMBRE_MODULO": NOMBRE_MODULO,
            "ROL_MODULO": ROL_MODULO,
            "VERSION_MODULO": VERSION_MODULO,
            "VERSION_CONTRATO": VERSION_CONTRATO,
            "ESQUEMA_CONTRATO": ESQUEMA_CONTRATO,
            "COMPATIBLE_DESDE": COMPATIBLE_DESDE,
            "API_ENGINE": API_ENGINE,
            "ESTABILIDAD": ESTABILIDAD,
        },

        "contrato": {
            "esquema": CONTENEDOR.get("esquema"),
            "version_contrato": CONTENEDOR.get("version_contrato"),
            "version_modulo": CONTENEDOR.get("version_modulo"),
            "id": CONTENEDOR.get("id"),
            "nombre": CONTENEDOR.get("nombre"),
            "rol": CONTENEDOR.get("rol"),
            "estabilidad": CONTENEDOR.get("estabilidad"),
            "compatible_desde": CONTENEDOR.get("compatible_desde"),
            "api_engine": CONTENEDOR.get("api_engine"),
        },

        "capacidades": {
            "declaradas": capacidades_declaradas,
            "meta": capacidades_meta,
            "resueltas": sorted(
                nombre
                for nombre, resoluble in capacidades_resueltas.items()
                if resoluble
            ),
            "no_resueltas": capacidades_no_resueltas,
            "correspondencia_1_a_1": (
                capacidades_declaradas == capacidades_meta
                and not capacidades_no_resueltas
            ),
        },

        "inventario_skills": {
            "ids": list(res_barrer.get("ids") or []),
            "n": int(res_barrer.get("n") or 0),
            "archivos": list(res_barrer.get("archivos") or []),
        },

        "integridad": {
            "coherente": bool(res_barrer.get("coherente"))
            and not capacidades_no_resueltas,
            "ids": list(res_barrer.get("ids") or []),
            "n": int(res_barrer.get("n") or 0),
            "archivos": list(res_barrer.get("archivos") or []),
            "errores": list(res_barrer.get("errores") or []),
            "choques": list(res_barrer.get("choques") or []),
        },

        "autoriza_engine": dict(
            CONTENEDOR.get("autoriza_engine") or {}
        ),

        "reporting": dict(
            CONTENEDOR.get("reporting") or {}
        ),

        "invariantes": list(INVARIANTES),

        "nota": (
            "inspeccionar realiza únicamente inspección estructural. "
            "No ejecuta skills ni altera el contrato. "
            "La resolución de capacidades se considera válida únicamente "
            "cuando cada capacidad declarada apunta a un callable real."
        ),
    }

# ===============================================================
# FIN 8.10
# ===============================================================


# ===============================================================
# 8.11 — REGISTRAR INVENTARIO
# ===============================================================

def registrar_inventario(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Produce una instantánea determinista del inventario estructural de CE.

    No persiste.
    No modifica CONTENEDOR.
    No modifica skills.
    No deposita evidencia.
    No ejecuta skills.
    """
    if peticion is not None and not isinstance(peticion, dict):
        raise TypeError(
            f"{NOMBRE_MODULO}: 'peticion' debe ser dict o None"
        )

    inv = inventario(peticion)

    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "operacion": "registrar_inventario",
        "registrado": True,
        "persistido": False,
        "inventario": inv,
        "nota": (
            "Instantánea estructural determinista del inventario de CE. "
            "Registrar significa producir y devolver la instantánea; "
            "no implica persistencia ni modificación de evidencia."
        ),
    }

# ===============================================================
# FIN 8.11
# ===============================================================

# ===============================================================
# FIN PARTE 8
# ===============================================================
# ===============================================================
# PARTE 9 — REPORTES Y DIAGNÓSTICO
# ===============================================================

# ===============================================================
# 9.1 — REPORTE
# ===============================================================

def reporte() -> Dict[str, Any]:
    """
    Genera un reporte estructural determinista del módulo CE.

    No ejecuta skills.
    No modifica el contrato.
    No altera estado externo.
    Utiliza la evidencia estructural producida por barrer().
    """
    b = barrer()
    coherente = bool(b.get("coherente"))
    estado = ESTADO_OPERATIVO if coherente else ESTADO_DEGRADADO

    capacidades = CONTENEDOR.get("capacidades") or {}
    capacidades_meta = CONTENEDOR.get("capacidades_meta") or {}

    operaciones_arquitectonicas = {
        "ejecutar_total": callable(ejecutar_total),
        "inspeccionar": callable(inspeccionar),
        "registrar_inventario": callable(registrar_inventario),
    }

    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "estado": estado,
        "coherente": coherente,
        "ids": list(b.get("ids") or []),
        "n": int(b.get("n") or 0),
        "archivos": list(b.get("archivos") or []),
        "errores": list(b.get("errores") or []),
        "errores_n": len(b.get("errores") or []),
        "choques": list(b.get("choques") or []),
        "notas": list(b.get("notas") or []),
        "capacidades": list(capacidades.keys()),
        "capacidades_meta": list(capacidades_meta.keys()),
        "autoridad": list(CONTENEDOR.get("autoridad") or []),
        "conocimiento_exportable": list(
            CONTENEDOR.get("conocimiento_exportable") or []
        ),
        "operaciones_arquitectonicas": operaciones_arquitectonicas,
    }

# ===============================================================
# FIN 9.1
# ===============================================================


# ===============================================================
# 9.2 — DIAGNÓSTICO
# ===============================================================

def diagnostico() -> Dict[str, Any]:
    """
    Produce diagnóstico estructural determinista a partir de barrer().

    No ejecuta skills.
    No selecciona skills.
    No modifica el contrato.
    No convierte advertencias en coherencia.
    """
    b = barrer()

    problemas: List[Dict[str, Any]] = []
    advertencias: List[str] = []
    recomendaciones: List[str] = []

    errores = list(b.get("errores") or [])
    notas = list(b.get("notas") or [])
    ids_validos = list(b.get("ids") or [])
    archivos = list(b.get("archivos") or [])

    if errores:
        problemas.append({
            "tipo": "errores_skills",
            "detalle": errores,
        })
        recomendaciones.append(
            "Revisar los archivos *.py de CE y corregir toda "
            "inconsistencia estructural de los skills descubiertos."
        )

    if not ids_validos:
        problemas.append({
            "tipo": "sin_skills",
            "detalle": "ningún skill válido descubierto",
        })
        recomendaciones.append(
            "Verificar que existan archivos *.py válidos con "
            "SKILL/CAPACIDAD y un id."
        )

    if notas:
        advertencias.extend(notas)

    coherente = bool(b.get("coherente"))
    estado = ESTADO_OPERATIVO if coherente else ESTADO_DEGRADADO

    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "estado": estado,
        "coherente": coherente,
        "problemas": problemas,
        "advertencias": advertencias,
        "recomendaciones": recomendaciones,
        "ids": ids_validos,
        "n": int(b.get("n") or 0),
        "archivos": archivos,
        "errores": errores,
    }

# ===============================================================
# FIN 9.2
# ===============================================================


# ===============================================================
# FIN PARTE 9
# ===============================================================

# ===============================================================
# PARTE 10 — RESOLUCIÓN ESTRICTA Y EXPORTACIONES
# ===============================================================

# ===============================================================
# 10.1 — MAPA DE CAPACIDADES
# ===============================================================

_CAP_MAP = {
    "verificar": verificar,
    "barrer": barrer,
    "inventario": inventario,
    "skills": skills,
    "ids": ids,
    "por_id": por_id,
    "listar_archivos": listar_archivos,
    "verificar_salida": verificar_salida,
    "ejecutar_total": ejecutar_total,
    "inspeccionar": inspeccionar,
    "registrar_inventario": registrar_inventario,
    "reporte": reporte,
    "diagnostico": diagnostico,
}

# ===============================================================
# FIN 10.1
# ===============================================================


# ===============================================================
# 10.2 — RESOLUCIÓN DE CAPACIDADES
# ===============================================================

def _resolver_capacidades(cont: Dict[str, Any]) -> None:
    capacidades = cont.get("capacidades")

    if not isinstance(capacidades, dict):
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: 'capacidades' debe ser dict"
        )

    declaradas = set(capacidades.keys())
    disponibles = set(_CAP_MAP.keys())

    faltantes = sorted(declaradas - disponibles)
    extras = sorted(disponibles - declaradas)

    if faltantes:
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: capacidades declaradas sin entrada "
            f"en _CAP_MAP: {faltantes}"
        )

    if extras:
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: _CAP_MAP contiene capacidades no "
            f"declaradas en CONTENEDOR: {extras}"
        )

    resueltas: Dict[str, Any] = {}

    for nombre, ref in capacidades.items():
        if callable(ref):
            fn = ref
        elif isinstance(ref, str):
            if ref not in _CAP_MAP:
                raise ContratoInvalido(
                    f"{NOMBRE_MODULO}: capacidad '{nombre}' "
                    f"referencia inexistente: '{ref}'"
                )
            fn = _CAP_MAP[ref]
        else:
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: capacidad '{nombre}' "
                f"tipo invalido: {type(ref).__name__}"
            )

        if not callable(fn):
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: capacidad '{nombre}' "
                f"no resuelve a callable real"
            )

        resueltas[nombre] = fn

    if set(resueltas.keys()) != declaradas:
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: resolución de capacidades no coincide "
            f"1:1 con CONTENEDOR"
        )

    cont["capacidades"] = resueltas

# ===============================================================
# FIN 10.2
# ===============================================================


# ===============================================================
# 10.3 — EJECUCIÓN DE VALIDACIÓN Y RESOLUCIÓN
# ===============================================================

_validar_contrato(CONTENEDOR)
_resolver_capacidades(CONTENEDOR)

# ===============================================================
# FIN 10.3
# ===============================================================


# ===============================================================
# 10.4 — EXPORTACIONES
# ===============================================================

__all__ = [
    "CONTENEDOR",
    "ID_MODULO",
    "NOMBRE_MODULO",
    "ROL_MODULO",
    "VERSION_MODULO",
    "skills",
    "ids",
    "por_id",
    "listar_archivos",
    "barrer",
    "verificar",
    "inventario",
    "verificar_salida",
    "ejecutar_total",
    "inspeccionar",
    "registrar_inventario",
    "reporte",
    "diagnostico",
    "ContratoInvalido",
]

# ===============================================================
# FIN 10.4
# ===============================================================

# ===============================================================
# FIN PARTE 10
# ===============================================================


# ===============================================================
# FIN DEL MÓDULO
# ===============================================================
