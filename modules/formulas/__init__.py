# ===============================================================
# VPSI-TRUTH — modules/formulas/__init__.py
# ===============================================================
#
# MÓDULO:              formulas
# ID:                  FO
# Rol:                 FO
# Versión módulo:      2.0
# Versión contrato:    1.0
# Esquema contrato:    VPSI-CONTRACT-1.0
# Estabilidad:         ESTABLE
# Compatible desde:    1.0
# API Engine:          >=1.0
#
# Función:
#   Contenedor de fórmulas canónicas del sistema.
#   Expone y ejecuta tru_ri y tru_total, y cualquier fórmula
#   descubierta en los archivos del módulo.
#
# Qué hace:
#   - Descubre y carga todos los archivos .py del módulo
#   - Evalúa tru_ri(C, L, K) y tru_total(C, L, K) sin límites artificiales
#   - Valida coherencia de fórmulas (piso, canónicas)
#   - Expone declaraciones FO-1..FO-4
#   - Inventario, reporte y diagnóstico propios
#
# Qué NO hace:
#   - No calcula C, L, K (los recibe como entrada)
#   - No clasifica entrada de usuario (eso es CX)
#   - No orquesta el sistema (eso es Engine)
#   - No modifica otros módulos
#
# Responsabilidad:
#   Ser la fuente oficial de las fórmulas de verdad y su verificación.
#
# Autoridad:
#   - Ejecutar cualquier fórmula registrada o descubierta en el módulo
#   - Calcular tru_ri y tru_total para cualquier C, L, K válidos
#   - Reportar estado, inventario y diagnóstico propios
#
# Conocimiento exportable:
#   tru_ri, tru_total, fórmulas descubiertas, declaraciones,
#   inventario, estado, reporte, diagnóstico
#
# Relación con Engine:
#   Engine descubre este CONTENEDOR, ejecuta solo las capacidades
#   declaradas y consolida el reporte que este módulo produce.
#
# Relación con Omega:
#   Omega no calcula nada de FO. Solo presenta lo que Engine entrega.
#
# ===============================================================

# ===============================================================
# VPSI-TRUTH — modules/formulas/__init__.py
# ===============================================================
#
# MÓDULO:              formulas
# ID:                  FO
# Rol:                 FO
# Versión módulo:      2.0
# Versión contrato:    1.0
# Esquema contrato:    VPSI-CONTRACT-1.0
# Estabilidad:         ESTABLE
# Compatible desde:    1.0
# API Engine:          >=1.0
#
# ===============================================================

# ===============================================================
# 1. IMPORTACIONES
# ===============================================================

from __future__ import annotations

import sys
import math
import ast
import copy
import inspect
import threading
import importlib.util
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Set, Tuple
from modules.formulas.formulas_omega.coherence import CoherenceEngine
from collections import defaultdict
from decimal import Decimal, getcontext
from fractions import Fraction
from datetime import datetime, timezone

from modules.constante import ALPHA, BETA
import modules.formulas.formulas_omega  # fuerza la carga estricta del subpaquete
# ===============================================================
# 2. CONSTANTES DE IDENTIDAD
# ===============================================================

ID_MODULO = "FO"
NOMBRE_MODULO = "formulas"
ROL_MODULO = "FO"

VERSION_MODULO = "2.0"
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

INVARIANTES = (
    "el id del módulo nunca cambia",
    "el rol nunca cambia",
    "las capacidades declaradas son siempre callables tras la resolución",
    "este módulo no modifica el estado de otros módulos",
    "tru_ri y tru_total no imponen límites artificiales sobre C, L, K",
    "ALPHA y BETA provienen exclusivamente de modules.constante",
)

PISO_FORMULAS = 1

# ===============================================================
# 3. CONFIGURACIÓN
# ===============================================================

_DIR = Path(__file__).parent

# ===============================================================
# 4. DEFINICIONES
# ===============================================================

class ContratoInvalido(Exception):
    """El CONTENEDOR no cumple el esquema o la resolución falló."""
    pass

class FormulaError(Exception):
    pass

class FormulaNoEncontradaError(Exception):
    pass

_DECLARACIONES: List[Dict[str, Any]] = []
_REGLAS: List[Callable[[], List[str]]] = []
_FORMULAS: Dict[str, Dict[str, Any]] = {}

# ===============================================================
# 5. CONTRATO OFICIAL DEL MÓDULO (CONTENEDOR)
# ===============================================================

CONTENEDOR: Dict[str, Any] = {

    # -----------------------------------------------------------
    # 5.1 ESQUEMA
    # -----------------------------------------------------------
    "esquema": ESQUEMA_CONTRATO,
    "version_contrato": VERSION_CONTRATO,
    "version_modulo": VERSION_MODULO,
    "estabilidad": ESTABILIDAD,
    "compatible_desde": COMPATIBLE_DESDE,
    "api_engine": API_ENGINE,

    # -----------------------------------------------------------
    # 5.2 IDENTIDAD
    # -----------------------------------------------------------
    "id": ID_MODULO,
    "nombre": NOMBRE_MODULO,
    "rol": ROL_MODULO,
    "descripcion": (
        "Contenedor de fórmulas. Expone y ejecuta tru_ri y tru_total "
        "y cualquier fórmula descubierta en los archivos del módulo. "
        "ALPHA y BETA se resuelven exclusivamente desde modules.constante."
    ),

    # -----------------------------------------------------------
    # 5.3 PROPÓSITO
    # -----------------------------------------------------------
    "funcion": (
        "Ser la fuente oficial de las fórmulas de verdad: descubrir archivos, "
        "registrar fórmulas, evaluar tru_ri(C,L,K) y tru_total(C,L,K), "
        "validar coherencia."
    ),
    "no_hace": [
        "No calcula C, L, K (los recibe como entrada)",
        "No clasifica entrada de usuario",
        "No orquesta el sistema (eso es Engine)",
        "No modifica otros módulos",
    ],

    # -----------------------------------------------------------
    # 5.4 AUTORIDAD
    # -----------------------------------------------------------
    "autoridad": [
        "Ejecutar cualquier fórmula registrada o descubierta",
        "Calcular tru_ri y tru_total para cualquier C, L, K válidos",
        "Leer y ejecutar todos los archivos .py del módulo",
        "Reportar estado, inventario y diagnóstico propios",
    ],

    # -----------------------------------------------------------
    # 5.5 CONOCIMIENTO EXPORTABLE
    # -----------------------------------------------------------
    "conocimiento_exportable": [
        "tru_ri",
        "tru_total",
        "formulas_descubiertas",
        "declaraciones",
        "inventario",
        "estado",
        "reporte",
        "diagnostico",
    ],

    # -----------------------------------------------------------
    # 5.6 ACCESO
    # -----------------------------------------------------------
    "acceso": {
        "nivel": "completo",
        "descripcion": "Acceso total a recursos del módulo",
    },

    # -----------------------------------------------------------
    # 5.7 DEPENDENCIAS
    # -----------------------------------------------------------
    "requiere": [
        "CE",
        "AX",
        "MC",
        "SF",
        "CA",
        "CX",
        "DI",
        "RE",
        "VX",
        "TX",
        "CH",
        "CIT",
        "DGCO",
        "UI",
        "CC",
        "TT",
        "SC",
        "CT",
    ],

    # -----------------------------------------------------------
    # 5.8 ACCESO A ARCHIVOS
    # -----------------------------------------------------------
    "acceso_archivos": [
        "*",
    ],

    # -----------------------------------------------------------
    # 5.9 VALIDAR ESQUEMA
    # -----------------------------------------------------------
    "validar_esquema": [
        "*",
    ],

    # -----------------------------------------------------------
    # 5.10 AUTORIZACIÓN AL ENGINE
    # -----------------------------------------------------------
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

        # --- PERMISOS OBLIGATORIOS DE ENGINE ---
        "validar_esquema": True,
        "acceso_archivos": True,

        # --- CAPACIDADES ARQUITECTÓNICAS ---
        "ejecutar_total": True,
        "inspeccionar": True,
        "registrar_inventario": True,
        "evaluar_universal": True,
    },

    # -----------------------------------------------------------
    # 5.11 CONSULTAS SOPORTADAS
    # -----------------------------------------------------------
    "consultas_soportadas": [
        "calcular_tru_ri",
        "calcular_tru_total",
        "obtener_inventario",
        "obtener_reporte",
        "obtener_diagnostico",
        "verificar_coherencia",
        "listar_formulas",
        "listar_declaraciones",
    ],

    # -----------------------------------------------------------
    # 5.12 CAPACIDADES (referencias a callables)
    # -----------------------------------------------------------
    "capacidades": {
        "verificar": "barrer",
        "barrer": "barrer",
        "evaluar": "barrer",
        "verificar_salida": "verificar_salida",
        "inventario": "inventario",
        "axiomas": "axiomas",
        "tru_ri": "tru_ri",
        "tru_total": "tru_total",
        "reporte": "reporte",
        "diagnostico": "diagnostico",
        "listar_formulas": "listar_formulas",
        "ejecutar_total": "ejecutar_total",
        "inspeccionar": "inspeccionar",
        "registrar_inventario": "registrar_inventario",
        "evaluar_universal": "evaluar_universal",
        "evaluar_coherencia": "evaluar_coherencia",
    },

    # -----------------------------------------------------------
    # 5.13 METADATOS DE CAPACIDADES (1:1)
    # -----------------------------------------------------------
    "capacidades_meta": {
        "verificar": {
            "descripcion": "Alias de barrer. Verifica coherencia de fórmulas.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con coherente, faltas, reglas, formulas",
            "acceso_archivos": ["*"],
        },
        "barrer": {
            "descripcion": "Barrido universal de todas las fórmulas del módulo.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con estado, coherente, faltas, formulas, verdad",
            "acceso_archivos": ["*"],
        },
        "evaluar": {
            "descripcion": "Alias de barrer.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con estado, coherente, faltas, formulas",
            "acceso_archivos": ["*"],
        },
        "verificar_salida": {
            "descripcion": "Comprueba forma mínima de una salida de barrer.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "bool",
            "acceso_archivos": ["*"],
        },
        "inventario": {
            "descripcion": "Inventario completo de fórmulas descubiertas y registradas.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con formulas, verdad, reglas, declaraciones",
            "acceso_archivos": ["*"],
        },
        "axiomas": {
            "descripcion": "Declaraciones FO-1 a FO-4.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "list[dict]",
            "acceso_archivos": ["*"],
        },
        "tru_ri": {
            "descripcion": "Calcula Tru_Ri = C * L * K sin límites artificiales.",
            "entrada": "C, L, K (Fraction)",
            "validar_esquema": ["*"],
            "salida": "Fraction",
            "acceso_archivos": ["*"],
        },
        "tru_total": {
            "descripcion": "Calcula Tru_total = (Tru_Ri * ALPHA) + BETA.",
            "entrada": "C, L, K (Fraction)",
            "validar_esquema": ["*"],
            "salida": "Fraction",
            "acceso_archivos": ["*"],
        },
        "reporte": {
            "descripcion": "Reporte de estado del módulo FO.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con estado, coherente, formulas, faltas",
            "acceso_archivos": ["*"],
        },
        "diagnostico": {
            "descripcion": "Diagnóstico de faltas y recomendaciones.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con problemas, advertencias, recomendaciones",
            "acceso_archivos": ["*"],
        },
        "listar_formulas": {
            "descripcion": "Lista todas las fórmulas existentes.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con descubiertas, registradas, todas, verdad",
            "acceso_archivos": ["*"],
        },
        "ejecutar_total": {
            "descripcion": "Autoridad total de Engine. Ejecuta todas las capacidades reales.",
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["*"],
            "salida": "dict con resultados de todas las unidades",
            "acceso_archivos": ["*"],
        },
        "inspeccionar": {
            "descripcion": "Inspección estructural sin calcular ni alterar.",
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["*"],
            "salida": "dict con estructura, capacidades y estado",
            "acceso_archivos": ["*"],
        },
        "registrar_inventario": {
            "descripcion": "Instantánea determinista del inventario.",
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["*"],
            "salida": "dict con inventario registrado",
            "acceso_archivos": ["*"],
        },
        "evaluar_universal": {
            "descripcion": "Evalúa capacidades reales cuya firma se satisfaga con los hechos.",
            "entrada": "hechos: dict",
            "validar_esquema": ["*"],
            "salida": "dict con hechos, traza, ejecutadas",
            "acceso_archivos": ["*"],
        },
        "evaluar_coherencia": {
            "descripcion": "Calcula C_Ω / C_β / C_α / C_total sobre el vector de capas (FO coherence).",
            "entrada": "capas: list[float], frictions: list[float] | None",
            "validar_esquema": ["*"],
            "salida": "dict con c_omega, c_beta, c_alpha, c_total, energies, diagnostico",
            "acceso_archivos": ["*"],
        },
    },

    # -----------------------------------------------------------
    # 5.14 REPORTING
    # -----------------------------------------------------------
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
        "evaluar_universal": True,
        "evaluar_coherencia": True,
    },

    # -----------------------------------------------------------
    # 5.15 ESTADOS E INVARIANTES
    # -----------------------------------------------------------
    "estados_validos": list(ESTADOS_VALIDOS),
    "invariantes": list(INVARIANTES),
}

# ===============================================================
# 6. FUNCIONES PRIVADAS
# ===============================================================

def regla(fn: Callable[[], List[str]]) -> Callable[[], List[str]]:
    _REGLAS.append(fn)
    return fn

def declarar(d: Dict[str, Any]) -> Dict[str, Any]:
    _DECLARACIONES.append(d)
    return d

def registrar_formula(nombre: str, meta: Dict[str, Any]):
    def decorator(fn: Callable) -> Callable:
        _FORMULAS[nombre] = {**meta, "funcion": fn}
        return fn
    return decorator

def _descubrir_formulas() -> Dict[str, Dict[str, Any]]:
    registro: Dict[str, Dict[str, Any]] = {}
    prefijo = f"{__package__}."
    try:
        importlib.invalidate_caches()
    except Exception:
        pass
    modulos: Set[str] = set()
    for f in sorted(_DIR.glob("*.py")):
        if f.name.startswith("_") or f.name == "__init__.py":
            continue
        modulos.add(f"{__package__}.{f.stem}")
    try:
        for info in pkgutil.walk_packages([str(_DIR)], prefix=prefijo):
            if info.name.endswith(".__init__"):
                continue
            modulos.add(info.name)
    except Exception:
        pass
    for nombre_modulo in sorted(modulos):
        try:
            mod = importlib.import_module(nombre_modulo)
        except Exception:
            continue
        archivo = getattr(mod, "__file__", None)
        archivo_nombre = Path(archivo).name if archivo else nombre_modulo
        meta = getattr(mod, "FORMULA", None)
        if isinstance(meta, dict) and "nombre" in meta:
            nombre = str(meta["nombre"])
            funcion = getattr(mod, nombre, None)
            registro[nombre] = {
                "archivo": archivo_nombre,
                "modulo": nombre_modulo,
                "expresion": meta.get("expresion", "No definida"),
                "fuente": meta.get("fuente", "Desconocida"),
                "funcion": funcion,
            }
        for nombre, objeto in vars(mod).items():
            if nombre.startswith("_") or not callable(objeto):
                continue
            if getattr(objeto, "__module__", None) != nombre_modulo:
                continue
            meta_objeto = getattr(objeto, "FORMULA", None)
            if isinstance(meta_objeto, dict):
                nombre_formula = str(meta_objeto.get("nombre", nombre))
                registro[nombre_formula] = {
                    "archivo": archivo_nombre,
                    "modulo": nombre_modulo,
                    "expresion": meta_objeto.get("expresion", "No definida"),
                    "fuente": meta_objeto.get("fuente", "Desconocida"),
                    "funcion": objeto,
                }
    return registro

@regla
def _validar_piso_formulas() -> List[str]:
    if len(_descubrir_formulas()) < PISO_FORMULAS and not _FORMULAS:
        return [f"Menos de {PISO_FORMULAS} fórmulas: coherencia por vacuidad"]
    return []

@regla
def _validar_formulas_canonicas() -> List[str]:
    faltas = []
    descubiertas = _descubrir_formulas()
    if "tru_ri" not in _FORMULAS and "tru_ri" not in descubiertas:
        faltas.append("Fórmula canónica 'tru_ri' no encontrada.")
    if "tru_total" not in _FORMULAS and "tru_total" not in descubiertas:
        faltas.append("Fórmula canónica 'tru_total' no encontrada.")
    return faltas

declarar({
    "id": "FO-1",
    "tipo": "axioma",
    "sujeto": "Tru_Ri",
    "relacion": "=",
    "objeto": "C * L * K",
    "polaridad": True,
    "enunciado": "Tru_Ri(D) = C(D) * L(D) * K(D) (Axioma TA5).",
    "cota": None,
    "depende_de": ["TA5"],
    "gobierna": ["tru_ri"],
})

declarar({
    "id": "FO-2",
    "tipo": "axioma",
    "sujeto": "Tru_total",
    "relacion": "=",
    "objeto": "(Tru_Ri * ALPHA) + BETA",
    "polaridad": True,
    "enunciado": "Tru_total(D) = (Tru_Ri(D) * ALPHA) + BETA (Definición 2.14).",
    "cota": None,
    "depende_de": ["Def-2.14"],
    "gobierna": ["tru_total"],
})

declarar({
    "id": "FO-3",
    "tipo": "teorema",
    "sujeto": "Tru_Ri",
    "relacion": "≤",
    "objeto": "ALPHA",
    "polaridad": True,
    "enunciado": "Tru_Ri(D) ≤ ALPHA = 26/27 (Teorema 16).",
    "cota": "26/27",
    "depende_de": ["T16"],
    "gobierna": ["tru_ri"],
})

declarar({
    "id": "FO-4",
    "tipo": "teorema",
    "sujeto": "Tru_total",
    "relacion": "≥",
    "objeto": "BETA",
    "polaridad": True,
    "enunciado": "Tru_total(D) ≥ BETA = 1/27 (Teorema 17).",
    "cota": "1/27",
    "depende_de": ["T17"],
    "gobierna": ["tru_total"],
})

from .truth import tru_ri, tru_total, FORMULA as TRUTH_FORMULA  # noqa: E402

@registrar_formula("tru_ri", TRUTH_FORMULA)
def _tru_ri_wrapper(C, L, K):
    return tru_ri(C, L, K)

@registrar_formula("tru_total", TRUTH_FORMULA)
def _tru_total_wrapper(C, L, K):
    return tru_total(C, L, K)

# ===============================================================
# 7. CAPACIDADES PÚBLICAS — CALLABLES REALES
# ===============================================================

# ---------------------------------------------------------------
# 7.1 barrer
# ---------------------------------------------------------------
def barrer() -> Dict[str, Any]:
    faltas: List[str] = []
    descubiertas = _descubrir_formulas()
    registradas = dict(_FORMULAS)
    todas: Dict[str, Any] = {}
    for nombre, meta in sorted(descubiertas.items()):
        todas[nombre] = {"origen": "descubierta", **meta}
    for nombre, meta in sorted(registradas.items()):
        todas[nombre] = {"origen": "registrada", **{k: v for k, v in meta.items() if k != "funcion"}}
    if "tru_ri" not in todas:
        faltas.append("Fórmula canónica de verdad 'tru_ri' ausente.")
    if "tru_total" not in todas:
        faltas.append("Fórmula canónica de verdad 'tru_total' ausente.")
    for regla_fn in _REGLAS:
        try:
            resultado = regla_fn()
            if resultado:
                faltas.extend(resultado)
        except Exception as e:
            faltas.append(f"{getattr(regla_fn, '__name__', 'regla')}: {type(e).__name__}: {e}")
    limpio = not faltas
    return {
        "contenedor": NOMBRE_MODULO,
        "id": ID_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "estado": "APROBADO" if limpio else "RECHAZADO",
        "coherente": limpio,
        "faltas": list(faltas),
        "formulas": sorted(todas.keys()),
        "formulas_registradas": sorted(registradas.keys()),
        "formulas_descubiertas": sorted(descubiertas.keys()),
        "total_formulas": len(todas),
        "verdad": {
            "tru_ri": "tru_ri" in todas,
            "tru_total": "tru_total" in todas,
        },
        "reglas": [r.__name__ for r in _REGLAS],
    }

# ---------------------------------------------------------------
# 7.2 verificar_salida
# ---------------------------------------------------------------
def verificar_salida(salida: Dict[str, Any]) -> bool:
    if not isinstance(salida, dict):
        return False
    if "coherente" not in salida or not isinstance(salida["coherente"], bool):
        return False
    if "estado" not in salida or not isinstance(salida["estado"], str):
        return False
    if "faltas" in salida and not isinstance(salida["faltas"], list):
        return False
    return True

# ---------------------------------------------------------------
# 7.3 verificar
# ---------------------------------------------------------------
def verificar() -> Dict[str, Any]:
    return barrer()

def evaluar_coherencia(capas, frictions=None, **kwargs):
    """
    Capacidad contractual del módulo formulas.
    Delega en formulas_omega.coherence.CoherenceEngine.
    """
    result = CoherenceEngine.full_analysis(
        activations=capas,
        frictions=frictions,
        **kwargs
    )
    return result  # o el bloque que Engine espera (c_omega + detalle)
# ---------------------------------------------------------------
# 7.4 inventario
# ---------------------------------------------------------------
def inventario(peticion: Any = None) -> Dict[str, Any]:
    descubiertas = _descubrir_formulas()
    registradas = list(_FORMULAS.keys())
    todas = sorted(set(descubiertas.keys()) | set(registradas))
    return {
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "formulas": todas,
        "formulas_descubiertas": descubiertas,
        "formulas_registradas": registradas,
        "total_formulas": len(todas),
        "verdad": {
            "tru_ri": "tru_ri" in todas,
            "tru_total": "tru_total" in todas,
        },
        "reglas": len(_REGLAS),
        "declaraciones": len(_DECLARACIONES),
        "capacidades": list(CONTENEDOR.get("capacidades", {}).keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "invariantes": CONTENEDOR.get("invariantes"),
    }

# ---------------------------------------------------------------
# 7.5 axiomas
# ---------------------------------------------------------------
def axiomas() -> List[Dict[str, Any]]:
    return list(_DECLARACIONES)

# ---------------------------------------------------------------
# 7.6 listar_formulas
# ---------------------------------------------------------------
def listar_formulas() -> Dict[str, Any]:
    descubiertas = _descubrir_formulas()
    registradas = list(_FORMULAS.keys())
    return {
        "descubiertas": descubiertas,
        "registradas": registradas,
        "todas": sorted(set(descubiertas.keys()) | set(registradas)),
        "total": len(set(descubiertas.keys()) | set(registradas)),
        "verdad": {
            "tru_ri": "tru_ri" in descubiertas or "tru_ri" in registradas,
            "tru_total": "tru_total" in descubiertas or "tru_total" in registradas,
        },
    }

# ---------------------------------------------------------------
# 7.7 reporte
# ---------------------------------------------------------------
def reporte() -> Dict[str, Any]:
    r = barrer()
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "estado": ESTADO_OPERATIVO if r.get("coherente") else ESTADO_DEGRADADO,
        "coherente": r.get("coherente"),
        "faltas": r.get("faltas"),
        "formulas": r.get("formulas"),
        "reglas": r.get("reglas"),
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "autoridad": CONTENEDOR.get("autoridad"),
        "conocimiento_exportable": CONTENEDOR.get("conocimiento_exportable"),
        "consultas_soportadas": CONTENEDOR.get("consultas_soportadas"),
    }

# ---------------------------------------------------------------
# 7.8 diagnostico
# ---------------------------------------------------------------
def diagnostico() -> Dict[str, Any]:
    r = barrer()
    problemas = []
    advertencias = []
    recomendaciones = []
    if r.get("faltas"):
        problemas.append({"tipo": "faltas_coherencia", "detalle": r["faltas"]})
        recomendaciones.append("Resolver faltas de fórmulas o reglas")
    if not r.get("formulas"):
        advertencias.append("No hay fórmulas descubiertas ni registradas")
        recomendaciones.append("Verificar archivos .py del módulo formulas")
    estado = ESTADO_OPERATIVO if r.get("coherente") else ESTADO_DEGRADADO
    if not r.get("formulas") and not problemas:
        estado = ESTADO_NO_INICIADO
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "estado": estado,
        "problemas": problemas,
        "advertencias": advertencias,
        "recomendaciones": recomendaciones,
        "coherente": r.get("coherente"),
        "faltas_n": len(r.get("faltas") or []),
        "formulas_n": len(r.get("formulas") or []),
    }

# ---------------------------------------------------------------
# 7.9 ejecutar_total
# ---------------------------------------------------------------
def ejecutar_total(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    peticion_normalizada = dict(peticion) if isinstance(peticion, dict) else {}
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
            "errores_ejecucion": ["capacidades no es dict"],
            "resultados": {},
            "capacidades_declaradas": [],
        }
    for nombre in sorted(capacidades):
        if nombre == "ejecutar_total":
            continue
        referencia = capacidades[nombre]
        try:
            fn = referencia if callable(referencia) else globals().get(str(referencia))
            if not callable(fn):
                raise ContratoInvalido(f"'{referencia}' no es callable")
            if nombre in ("tru_ri", "tru_total"):
                C = peticion_normalizada.get("C")
                L = peticion_normalizada.get("L")
                K = peticion_normalizada.get("K")
                if C is None or L is None or K is None:
                    resultados[nombre] = {"omitido": True, "motivo": "faltan C, L o K"}
                    continue
                resultados[nombre] = fn(C, L, K)
                continue
            firma = inspect.signature(fn)
            params = list(firma.parameters.values())
            obligatorios = [
                p for p in params
                if p.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
                and p.default is inspect.Parameter.empty
            ]
            if not obligatorios:
                resultados[nombre] = fn()
            elif len(obligatorios) == 1:
                resultados[nombre] = fn(peticion_normalizada)
            else:
                resultados[nombre] = fn()
        except Exception as exc:
            errores_ejecucion.append(f"{nombre}: {exc}")
            resultados[nombre] = None
    barrido = resultados.get("barrer")
    coherente = isinstance(barrido, dict) and bool(barrido.get("coherente"))
    ejecutadas = sorted(n for n, r in resultados.items() if r is not None)
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "operacion": "ejecutar_total",
        "estado": ESTADO_OPERATIVO if coherente and not errores_ejecucion else ESTADO_DEGRADADO,
        "coherente": coherente and not errores_ejecucion,
        "capacidades_ejecutadas": ejecutadas,
        "errores_ejecucion": errores_ejecucion,
        "resultados": resultados,
        "capacidades_declaradas": sorted(capacidades.keys()),
    }

# ---------------------------------------------------------------
# 7.10 inspeccionar
# ---------------------------------------------------------------
def inspeccionar(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    r = barrer()
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
            "PISO_FORMULAS": PISO_FORMULAS,
            "ALPHA": str(ALPHA),
            "BETA": str(BETA),
        },
        "capacidades_contractuales": sorted(CONTENEDOR.get("capacidades", {}).keys()),
        "capacidades_meta": sorted(CONTENEDOR.get("capacidades_meta", {}).keys()),
        "integridad": {
            "coherente": r.get("coherente"),
            "faltas": r.get("faltas"),
            "reglas": r.get("reglas"),
            "formulas": r.get("formulas"),
        },
        "formulas_registradas": list(_FORMULAS.keys()),
        "formulas_descubiertas": _descubrir_formulas(),
        "declaraciones_n": len(_DECLARACIONES),
        "reglas_n": len(_REGLAS),
        "autoriza_engine": CONTENEDOR.get("autoriza_engine"),
        "reporting": CONTENEDOR.get("reporting"),
        "invariantes": list(INVARIANTES),
    }

# ---------------------------------------------------------------
# 7.11 registrar_inventario
# ---------------------------------------------------------------
def registrar_inventario(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return {
        "id": ID_MODULO,
        "operacion": "registrar_inventario",
        "registrado": True,
        "inventario": inventario(peticion),
        "nota": "Instantánea determinista del inventario de FO.",
    }

# ---------------------------------------------------------------
# 7.12 evaluar_universal
# ---------------------------------------------------------------
def evaluar_universal(hechos: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    hechos_out: Dict[str, Any] = dict(hechos or {})
    traza: List[Dict[str, Any]] = []
    ejecutadas: set = set()
    capacidades = CONTENEDOR.get("capacidades") or {}
    while True:
        nuevos = 0
        for nombre, fn in list(capacidades.items()):
            if nombre == "evaluar_universal" or not callable(fn) or nombre in ejecutadas:
                continue
            try:
                sig = inspect.signature(fn)
            except (TypeError, ValueError):
                continue
            requeridos = []
            opcionales = []
            for pname, p in sig.parameters.items():
                if p.kind not in (
                    inspect.Parameter.POSITIONAL_ONLY,
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    inspect.Parameter.KEYWORD_ONLY,
                ):
                    continue
                if p.default is inspect.Parameter.empty:
                    requeridos.append(pname)
                else:
                    opcionales.append(pname)
            argumentos: Dict[str, Any] = {}
            try:
                if not requeridos:
                    for p in opcionales:
                        if p in hechos_out:
                            argumentos[p] = hechos_out[p]
                    salida = fn(**argumentos) if argumentos else fn()
                elif all(r in hechos_out for r in requeridos):
                    for p in requeridos + opcionales:
                        if p in hechos_out:
                            argumentos[p] = hechos_out[p]
                    salida = fn(**argumentos)
                elif len(requeridos) == 1:
                    argumentos[requeridos[0]] = hechos_out
                    for p in opcionales:
                        if p in hechos_out:
                            argumentos[p] = hechos_out[p]
                    salida = fn(**argumentos)
                else:
                    continue
            except Exception as ex:
                ejecutadas.add(nombre)
                traza.append({
                    "capacidad": nombre,
                    "estado": "ERROR",
                    "detalle": f"{type(ex).__name__}: {ex}",
                })
                continue
            ejecutadas.add(nombre)
            publicados = []
            if isinstance(salida, dict):
                for clave, valor in salida.items():
                    if not clave.startswith("_") and clave not in hechos_out:
                        hechos_out[clave] = valor
                        publicados.append(clave)
                        nuevos += 1
            traza.append({
                "capacidad": nombre,
                "estado": "EXITO",
                "argumentos": sorted(argumentos.keys()),
                "publica": publicados,
            })
        if nuevos == 0:
            break
    return {
        "hechos": hechos_out,
        "traza": traza,
        "ejecutadas": sorted(ejecutadas),
    }

# ===============================================================
# 8. RESOLUCIÓN ESTRICTA DE CAPACIDADES
# ===============================================================

_CAP_MAP = {
    "barrer": barrer,
    "verificar": verificar,
    "evaluar": barrer,
    "verificar_salida": verificar_salida,
    "inventario": inventario,
    "axiomas": axiomas,
    "tru_ri": tru_ri,
    "tru_total": tru_total,
    "reporte": reporte,
    "diagnostico": diagnostico,
    "listar_formulas": listar_formulas,
    "ejecutar_total": ejecutar_total,
    "inspeccionar": inspeccionar,
    "registrar_inventario": registrar_inventario,
    "evaluar_universal": evaluar_universal,
    "evaluar_coherencia": evaluar_coherencia,
}

def _resolver_capacidades(cont: Dict[str, Any]) -> None:
    resueltas: Dict[str, Any] = {}
    for nombre, ref in cont["capacidades"].items():
        if callable(ref):
            resueltas[nombre] = ref
            continue
        if isinstance(ref, str):
            if ref not in _CAP_MAP:
                raise ContratoInvalido(
                    f"{NOMBRE_MODULO}: capacidad '{nombre}' referencia inexistente: '{ref}'"
                )
            fn = _CAP_MAP[ref]
            if not callable(fn):
                raise ContratoInvalido(f"{NOMBRE_MODULO}: '{ref}' no es callable")
            resueltas[nombre] = fn
            continue
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: capacidad '{nombre}' tiene tipo inválido: {type(ref).__name__}"
        )
    cont["capacidades"] = resueltas

def _validar_contrato(cont: Dict[str, Any]) -> None:
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
        raise ContratoInvalido(f"{NOMBRE_MODULO}: CONTENEDOR incompleto. Faltan: {faltantes}")
    meta = cont.get("capacidades_meta") or {}
    for nombre in cont.get("capacidades") or {}:
        if nombre not in meta:
            raise ContratoInvalido(f"{NOMBRE_MODULO}: capacidad '{nombre}' sin capacidades_meta")

_validar_contrato(CONTENEDOR)
_resolver_capacidades(CONTENEDOR)

# ===============================================================
# 9. EXPORTACIONES
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
    "barrer",
    "verificar",
    "verificar_salida",
    "inventario",
    "axiomas",
    "listar_formulas",
    "tru_ri",
    "tru_total",
    "reporte",
    "diagnostico",
    "ejecutar_total",
    "inspeccionar",
    "registrar_inventario",
    "evaluar_universal",
    "FormulaError",
    "FormulaNoEncontradaError",
    "ContratoInvalido",
    "evaluar_coherencia",
]
