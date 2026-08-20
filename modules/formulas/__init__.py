# ===============================================================
# VPSI-TRUTH — modules/formulas/__init__.py
# ===============================================================
#
# MÓDULO:              formulas
# ID:                  FO
# Rol:                 FO
# Versión módulo:      1.1
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

# --- Fechas y tiempo ---
from datetime import datetime, timezone

# --- Sistema de archivos ---
from pathlib import Path


# ===============================================================
# FIN IMPORTACIONES
# ===============================================================


# ===============================================================
# CONSTANTES
# ===============================================================

ID_MODULO = "FO"
NOMBRE_MODULO = "formulas"
ROL_MODULO = "FO"

VERSION_MODULO = "1.1"
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
)

PISO_FORMULAS = 1

# ===============================================================
# FIN CONSTANTES
# ===============================================================


# ===============================================================
# CONFIGURACIÓN
# ===============================================================

_DIR = Path(__file__).parent

# ===============================================================
# FIN CONFIGURACIÓN
# ===============================================================


# ===============================================================
# DEFINICIONES
# ===============================================================

class ContratoInvalido(Exception):
    """El CONTENEDOR no cumple el esquema o la resolución falló."""
    pass


class FormulaError(Exception):
    pass


class FormulaNoEncontradaError(Exception):
    pass


# Estado interno del módulo
_DECLARACIONES: List[Dict[str, Any]] = []
_REGLAS: List[Callable[[], List[str]]] = []
_FORMULAS: Dict[str, Dict[str, Any]] = {}

# ===============================================================
# FIN DEFINICIONES
# ===============================================================

# ===============================================================
# CONTRATO OFICIAL DEL MÓDULO
# ===============================================================

CONTENEDOR: Dict[str, Any] = {
    # ============================================================
    # ESQUEMA
    # ============================================================
    "esquema": ESQUEMA_CONTRATO,
    "version_contrato": VERSION_CONTRATO,
    "version_modulo": VERSION_MODULO,
    "estabilidad": ESTABILIDAD,
    "compatible_desde": COMPATIBLE_DESDE,
    "api_engine": API_ENGINE,

    # ============================================================
    # IDENTIDAD
    # ============================================================
    "id": ID_MODULO,
    "nombre": NOMBRE_MODULO,
    "rol": ROL_MODULO,
    "descripcion": (
        "Contenedor de fórmulas. Rol FO. "
        "Expone y ejecuta tru_ri y tru_total, y cualquier fórmula "
        "descubierta en los archivos del módulo. "
        "Sin límites artificiales sobre C, L, K."
    ),

    # ============================================================
    # PROPÓSITO
    # ============================================================
    "funcion": (
        "Ser la fuente oficial de las fórmulas de verdad: "
        "descubrir archivos del módulo, registrar fórmulas, "
        "evaluar tru_ri(C,L,K) y tru_total(C,L,K), validar coherencia."
    ),
    "no_hace": [
        "No calcula C, L, K (los recibe como entrada)",
        "No clasifica entrada de usuario (eso es CX)",
        "No orquesta el sistema (eso es Engine)",
        "No modifica otros módulos",
    ],

    # ============================================================
    # AUTORIDAD
    # ============================================================
    "autoridad": [
        "Ejecutar cualquier fórmula registrada o descubierta en el módulo",
        "Calcular tru_ri y tru_total para cualquier C, L, K válidos",
        "Leer y ejecutar todos los archivos .py del módulo",
        "Reportar estado, inventario y diagnóstico propios",
    ],

    # ============================================================
    # CONOCIMIENTO EXPORTABLE
    # ============================================================
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

     # ============================================================
    # ACCESO (obligatorio en el esquema)
    # ============================================================
    "acceso": {
        "nivel": "completo",
        "descripcion": "Acceso total a recursos del módulo"
    },
    
    # ============================================================
    # DEPENDENCIAS
    # ============================================================
    "requiere": ["*"],

    # ============================================================
    # ACCESO A ARCHIVOS (AGREGADO — obligatorio en el esquema)
    # ============================================================
    "acceso_archivos": [
    "CE", "AX", "MC", "SF",
    "CA", "CX", "DI", "RE", "VX",
    "TX", "CH", "CIT", "DGCO", "UI",
    "CC", "TT", "SC", "CT"
    ],
    # ============================================================
    # VALIDAR ESQUEMA A NIVEL MÓDULO (AGREGADO — obligatorio en el esquema)
    # ============================================================
    "validar_esquema": ["*"],
    
    # ============================================================
    # AUTORIZACIÓN AL ENGINE (SOLO PERMISOS)
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
        # "modificar": False,    # ← ELIMINADO (no permitido)
        "alterar": False,
        # "reescribir": False,   # ← ELIMINADO (no permitido)
        "crear": True,
        # "eliminar": False,     # ← ELIMINADO (no permitido)
        "actualizar": False,

        # --- PERMISOS DE PROCESAMIENTO ---
        "validar": True,
        "procesar": True,
        "analizar": True,
        "generar": True,
        # "transformar": False,  # ← ELIMINADO (no permitido)

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
        "evaluar_universal": True,

        # --- BANDERAS NUEVAS (OBLIGATORIAS ENGINE) ---
        "ejecutar_total": True,
        "inspeccionar": True,
        "registrar_inventario": True,
        "evaluar_universal": True,
    },


    # ============================================================
    # CONSULTAS SOPORTADAS
    # ============================================================
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

    # ============================================================
    # CAPACIDADES
    # ============================================================
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

        # --- CAPACIDADES ARQUITECTÓNICAS (OBLIGATORIAS ENGINE) ---
        "ejecutar_total": "ejecutar_total",
        "inspeccionar": "inspeccionar",
        "registrar_inventario": "registrar_inventario",
        "evaluar_universal": "evaluar_universal",

    },

    # ============================================================
    # METADATOS DE CAPACIDADES (1:1 OBLIGATORIO)
    # ============================================================

    "capacidades_meta": {
        "verificar": {
            "descripcion": (
                "Alias de barrer. Verifica coherencia de fórmulas."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con coherente, faltas, reglas, formulas"
            ),
            "acceso_archivos": ["*"],
        },

        "barrer": {
            "descripcion": (
                "Ejecuta todas las reglas y reporta faltas de coherencia."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con estado, coherente, faltas, reglas, formulas"
            ),
            "acceso_archivos": ["*"],
        },

        "evaluar": {
            "descripcion": (
                "Alias de barrer. Evalúa coherencia del módulo."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con estado, coherente, faltas, reglas, formulas"
            ),
            "acceso_archivos": ["*"],
        },

        "verificar_salida": {
            "descripcion": (
                "Comprueba si una salida de barrer es coherente."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "bool",
            "acceso_archivos": ["*"],
        },

        "inventario": {
            "descripcion": (
                "Inventario de fórmulas descubiertas y registradas."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con formulas, formulas_registradas, "
                "reglas, declaraciones"
            ),
            "acceso_archivos": ["*"],
        },

        "axiomas": {
            "descripcion": (
                "Declaraciones FO registradas (FO-1..FO-4)."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "list[dict] de declaraciones",
            "acceso_archivos": ["*"],
        },

        "tru_ri": {
            "descripcion": (
                "Calcula Tru_Ri = C * L * K. Sin límites artificiales "
                "sobre los valores de C, L, K."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "resultado de C * L * K",
            "acceso_archivos": ["*"],
        },

        "tru_total": {
            "descripcion": (
                "Calcula Tru_total = (Tru_Ri * ALPHA) + BETA. "
                "Sin límites artificiales sobre C, L, K."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "resultado de (C*L*K)*ALPHA + BETA"
            ),
            "acceso_archivos": ["*"],
        },

        "reporte": {
            "descripcion": (
                "Reporte interno de estado del módulo FO."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con estado, coherente, formulas, faltas, capacidades"
            ),
            "acceso_archivos": ["*"],
        },

        "diagnostico": {
            "descripcion": (
                "Diagnóstico: qué falta, qué está mal en FO."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con estado, problemas, advertencias, recomendaciones"
            ),
            "acceso_archivos": ["*"],
        },

                "listar_formulas": {
            "descripcion": (
                "Lista todas las fórmulas descubiertas y registradas."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con descubiertas y registradas"
            ),
            "acceso_archivos": ["*"],
        },

        # --- CAPACIDADES ARQUITECTÓNICAS (OBLIGATORIAS ENGINE) ---
        "ejecutar_total": {
            "descripcion": (
                "Autoridad total de ENGINE sobre FO. "
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
                "Capacidad meta de inspeccion estructural de FO. "
                "Expone constantes, capacidades, formulas y estado "
                "sin alterar el contrato ni calcular."
            ),
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["acceso_archivos"],
            "salida": "dict con estructura, capacidades y estado del modulo",
            "acceso_archivos": ["acceso_archivos"],
        },
        "registrar_inventario": {
            "descripcion": (
                "Registra el inventario estructural de FO "
                "como instantanea determinista. No altera evidencia."
            ),
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["acceso_archivos"],
            "salida": "dict con inventario registrado",
            "acceso_archivos": ["acceso_archivos"],
        },
        "evaluar_universal": {
            "descripcion": (
                "Evalúa las capacidades reales de este módulo "
                "cuya firma se satisfaga con los hechos de entrada. "
                "Engine entrega la entrada; este callable solo aplica lo local."
           ),
          "entrada": "hechos: dict",
          "validar_esquema": ["*"],
          "salida": "dict con hechos, traza, ejecutadas",
          "acceso_archivos": ["*"],
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
        "evaluar_universal": True,
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
# FUNCIONES PRIVADAS
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
    """Lee y ejecuta absolutamente todos los .py del módulo (excepto _*)."""
    registro: Dict[str, Dict[str, Any]] = {}
    for f in sorted(_DIR.glob("*.py")):
        if f.name.startswith("_") or f.name == "__init__.py":
            continue
        clave = "formulas_{0}".format(f.stem)
        spec = importlib.util.spec_from_file_location(clave, f)
        if spec is None or spec.loader is None:
            continue
        mod = importlib.util.module_from_spec(spec)
        sys.modules[clave] = mod
        try:
            spec.loader.exec_module(mod)
        except Exception:  # noqa: BLE001
            continue
        meta = getattr(mod, "FORMULA", None)
        if isinstance(meta, dict) and "nombre" in meta:
            registro[meta["nombre"]] = {
                "archivo": f.name,
                "expresion": meta.get("expresion", "No definida"),
                "fuente": meta.get("fuente", "Desconocida"),
            }
    return registro


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
            f"{NOMBRE_MODULO}: esquema incompatible: {cont.get('esquema')}"
        )
    if str(cont.get("version_contrato")) != VERSION_CONTRATO:
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: version_contrato inválida: {cont.get('version_contrato')}"
        )
    meta_caps = cont.get("capacidades_meta") or {}
    for nombre_cap in cont.get("capacidades") or {}:
        if nombre_cap not in meta_caps:
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: capacidad '{nombre_cap}' sin capacidades_meta"
            )
        entrada = meta_caps[nombre_cap]
        if not isinstance(entrada, dict):
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: capacidades_meta['{nombre_cap}'] debe ser dict"
            )
        for campo in ("descripcion", "entrada", "salida"):
            if campo not in entrada or not isinstance(entrada[campo], str):
                raise ContratoInvalido(
                    f"{NOMBRE_MODULO}: capacidades_meta['{nombre_cap}'] "
                    f"requiere '{campo}: str'"
                )

# ===============================================================
# FIN FUNCIONES PRIVADAS
# ===============================================================


# ===============================================================
# REGLAS
# ===============================================================

@regla
def _validar_piso_formulas() -> List[str]:
    if len(_descubrir_formulas()) < PISO_FORMULAS:
        return [
            "Menos de {0} fórmulas: coherencia por vacuidad".format(
                PISO_FORMULAS
            )
        ]
    return []


@regla
def _validar_formulas_canonicas() -> List[str]:
    faltas = []
    descubiertas = _descubrir_formulas()
    if "tru_ri" not in _FORMULAS and "tru_ri" not in descubiertas:
        faltas.append("Fórmula tru_ri no encontrada.")
    if "tru_total" not in _FORMULAS and "tru_total" not in descubiertas:
        faltas.append("Fórmula tru_total no encontrada.")
    return faltas

# ===============================================================
# FIN REGLAS
# ===============================================================


# ===============================================================
# DECLARACIONES
# ===============================================================

declarar({
    "id": "FO-1",
    "tipo": "axioma",
    "sujeto": "Tru_Ri",
    "relacion": "=",
    "objeto": "C * L * K",
    "polaridad": True,
    "enunciado": (
        "Tru_Ri(D) = C(D) * L(D) * K(D) (Axioma TA5: Multiplicatividad)."
    ),
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
    "enunciado": (
        "Tru_total(D) = (Tru_Ri(D) * ALPHA) + BETA (Definición 2.14)."
    ),
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
    "enunciado": (
        "Tru_Ri(D) ≤ ALPHA = 26/27 (Teorema 16: Techo Estructural)."
    ),
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
    "enunciado": (
        "Tru_total(D) ≥ BETA = 1/27 (Teorema 17: Piso Estructural)."
    ),
    "cota": "1/27",
    "depende_de": ["T17"],
    "gobierna": ["tru_total"],
})

# ===============================================================
# FIN DECLARACIONES
# ===============================================================


# ===============================================================
# FÓRMULAS CANÓNICAS
# ===============================================================

from .truth import tru_ri, tru_total, FORMULA as TRUTH_FORMULA  # noqa: E402


@registrar_formula("tru_ri", TRUTH_FORMULA)
def _tru_ri_wrapper(C, L, K):
    """Sin límites artificiales: acepta cualquier C, L, K válidos."""
    return tru_ri(C, L, K)


@registrar_formula("tru_total", TRUTH_FORMULA)
def _tru_total_wrapper(C, L, K):
    """Sin límites artificiales: acepta cualquier C, L, K válidos."""
    return tru_total(C, L, K)

# ===============================================================
# FIN FÓRMULAS CANÓNICAS
# ===============================================================


# ===============================================================
# CAPACIDADES PÚBLICAS
# ===============================================================

def barrer() -> Dict[str, Any]:
    faltas: List[str] = []
    for regla_fn in _REGLAS:
        try:
            faltas.extend(regla_fn() or [])
        except Exception as e:  # noqa: BLE001
            faltas.append(
                "{0}: {1}: {2}".format(
                    regla_fn.__name__, type(e).__name__, e
                )
            )

    if faltas and DiagnosticoGlobal is not None:
        try:
            DiagnosticoGlobal.recibir_reporte(
                modulo="formulas",
                errores=[
                    {"tipo": "falta", "detalle": falta}
                    for falta in faltas
                ],
            )
        except Exception:  # noqa: BLE001
            pass

    return {
        "contenedor": NOMBRE_MODULO,
        "estado": "APROBADO" if not faltas else "RECHAZADO",
        "coherente": not faltas,
        "faltas": faltas,
        "reglas": [r.__name__ for r in _REGLAS],
        "formulas": list(_FORMULAS.keys()) or list(_descubrir_formulas().keys()),
    }


def verificar_salida(salida: Dict[str, Any]) -> bool:
    return bool(salida.get("coherente", False))


def inventario(peticion=None) -> Dict[str, Any]:
    return {
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "formulas": _descubrir_formulas(),
        "formulas_registradas": list(_FORMULAS.keys()),
        "reglas": len(_REGLAS),
        "declaraciones": len(_DECLARACIONES),
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "invariantes": CONTENEDOR.get("invariantes"),
    }


def axiomas() -> List[Dict[str, Any]]:
    return list(_DECLARACIONES)


def listar_formulas() -> Dict[str, Any]:
    return {
        "descubiertas": _descubrir_formulas(),
        "registradas": list(_FORMULAS.keys()),
    }


def verificar() -> Dict[str, Any]:
    return barrer()

# ===============================================================
# CAPACIDADES ARQUITECTÓNICAS (OBLIGATORIAS ENGINE)
# ===============================================================

def ejecutar_total(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Autoridad total de ENGINE sobre FO.
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
                fn = referencia
            elif isinstance(referencia, str):
                fn = globals().get(referencia)
                if not callable(fn):
                    raise ContratoInvalido(
                        f"'{referencia}' no es callable"
                    )
            else:
                raise ContratoInvalido(
                    f"tipo inválido: {type(referencia).__name__}"
                )

            # tru_ri / tru_total requieren C, L, K — no se ejecutan a ciegas
            if nombre in ("tru_ri", "tru_total"):
                C = peticion_normalizada.get("C")
                L = peticion_normalizada.get("L")
                K = peticion_normalizada.get("K")
                if C is None or L is None or K is None:
                    resultados[nombre] = {
                        "omitido": True,
                        "motivo": "faltan C, L o K en peticion",
                    }
                    continue
                resultados[nombre] = fn(C, L, K)
                continue

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


def inspeccionar(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Inspección estructural de FO.
    Expone contrato y estado sin calcular ni alterar.
    """
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
        },
        "capacidades_contractuales": sorted(
            CONTENEDOR.get("capacidades", {}).keys()
        ),
        "capacidades_meta": sorted(
            CONTENEDOR.get("capacidades_meta", {}).keys()
        ),
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
        "nota": (
            "inspeccionar expone estructura de FO sin calcular "
            "ni alterar el contrato."
        ),
    }


def registrar_inventario(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Instantánea determinista del inventario de FO.
    No altera evidencia.
    """
    inv = inventario(peticion)
    return {
        "id": ID_MODULO,
        "operacion": "registrar_inventario",
        "registrado": True,
        "inventario": inv,
        "nota": (
            "Instantánea determinista del inventario de FO. "
            "No modifica fórmulas ni evidencia."
        ),
    }

# ===============================================================
# FIN CAPACIDADES ARQUITECTÓNICAS
# ===============================================================
# ===============================================================
# EVALUAR_UNIVERSAL
# ===============================================================

def evaluar_universal(
    hechos: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Engine entrega hechos.
    Este callable ejecuta las capacidades REALES de ESTE módulo
    (CONTENEDOR['capacidades'] ya resuelto a callables).
    Punto fijo local. No se llama a sí mismo. No toca otros módulos.
    """
    hechos_out: Dict[str, Any] = dict(hechos or {})
    traza: List[Dict[str, Any]] = []
    ejecutadas: set = set()

    capacidades = CONTENEDOR.get("capacidades") or {}

    while True:
        nuevos = 0

        for nombre, fn in capacidades.items():
            if nombre == "evaluar_universal":
                continue
            if not callable(fn):
                continue
            if nombre in ejecutadas:
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

            # --- resolución de argumentos (universal, sin nombres inventados) ---
            argumentos: Dict[str, Any] = {}

            if not requeridos:
                # firma vacía o solo opcionales: usar opcionales presentes en hechos
                for p in opcionales:
                    if p in hechos_out:
                        argumentos[p] = hechos_out[p]
                try:
                    salida = fn(**argumentos) if argumentos else fn()
                except Exception as ex:
                    ejecutadas.add(nombre)
                    traza.append({
                        "capacidad": nombre,
                        "estado": "ERROR",
                        "detalle": "{0}: {1}".format(type(ex).__name__, ex),
                    })
                    continue

            elif all(r in hechos_out for r in requeridos):
                # todos los requeridos existen como claves en hechos
                for p in requeridos + opcionales:
                    if p in hechos_out:
                        argumentos[p] = hechos_out[p]
                try:
                    salida = fn(**argumentos)
                except Exception as ex:
                    ejecutadas.add(nombre)
                    traza.append({
                        "capacidad": nombre,
                        "estado": "ERROR",
                        "detalle": "{0}: {1}".format(type(ex).__name__, ex),
                    })
                    continue

            elif len(requeridos) == 1:
                # patrón real del repo: calcular(peticion), verificar(datos), etc.
                # se entrega el dict de hechos completo en ese único parámetro
                argumentos[requeridos[0]] = hechos_out
                for p in opcionales:
                    if p in hechos_out:
                        argumentos[p] = hechos_out[p]
                try:
                    salida = fn(**argumentos)
                except Exception as ex:
                    ejecutadas.add(nombre)
                    traza.append({
                        "capacidad": nombre,
                        "estado": "ERROR",
                        "detalle": "{0}: {1}".format(type(ex).__name__, ex),
                    })
                    continue
            else:
                # varios requeridos ausentes: no aplicable aún
                continue

            ejecutadas.add(nombre)
            publicados: List[str] = []

            if isinstance(salida, dict):
                for clave, valor in salida.items():
                    if clave.startswith("_"):
                        continue
                    if clave not in hechos_out:
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
# FIN EVALUAR_UNIVERSAL
# ===============================================================

# ===============================================================
# FIN CAPACIDADES PÚBLICAS
# ===============================================================

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
        "estado": (
            ESTADO_OPERATIVO if r.get("coherente") else ESTADO_DEGRADADO
        ),
        "coherente": r.get("coherente"),
        "faltas": r.get("faltas"),
        "formulas": r.get("formulas"),
        "reglas": r.get("reglas"),
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "autoridad": CONTENEDOR.get("autoridad"),
        "conocimiento_exportable": CONTENEDOR.get("conocimiento_exportable"),
        "consultas_soportadas": CONTENEDOR.get("consultas_soportadas"),
        "operaciones_arquitectonicas": {
            "ejecutar_total": True,
            "inspeccionar": True,
            "registrar_inventario": True,
        },
    }


def diagnostico() -> Dict[str, Any]:
    r = barrer()
    problemas = []
    advertencias = []
    recomendaciones = []

    if r.get("faltas"):
        problemas.append({
            "tipo": "faltas_coherencia",
            "detalle": r["faltas"],
        })
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

# ===============================================================
# FIN REPORTING
# ===============================================================


# ===============================================================
# EXPORTACIONES + RESOLUCIÓN ESTRICTA
# ===============================================================

_CAP_MAP = {
    # --- CENTINELA ---
    "barrer": barrer,
    "verificar": verificar,
    "evaluar": barrer,
    "verificar_salida": verificar_salida,

    # --- INVENTARIO Y REPORTING ---
    "inventario": inventario,
    "reporte": reporte,
    "diagnostico": diagnostico,

    # --- CONOCIMIENTO ---
    "axiomas": axiomas,
    "listar_formulas": listar_formulas,

    # --- FÓRMULAS CANÓNICAS ---
    "tru_ri": tru_ri,
    "tru_total": tru_total,

    # --- CAPACIDADES ARQUITECTÓNICAS (OBLIGATORIAS ENGINE) ---
    "ejecutar_total": ejecutar_total,
    "inspeccionar": inspeccionar,
    "registrar_inventario": registrar_inventario,
    "evaluar_universal": evaluar_universal,
}


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
                    f"{NOMBRE_MODULO}: capacidad '{nombre}' "
                    f"referencia inexistente: '{ref}'"
                )
            fn = _CAP_MAP[ref]
            if not callable(fn):
                raise ContratoInvalido(
                    f"{NOMBRE_MODULO}: '{ref}' no es callable"
                )
            resueltas[nombre] = fn
            continue
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: capacidad '{nombre}' "
            f"tiene tipo inválido: {type(ref).__name__}"
        )
    cont["capacidades"] = resueltas


_validar_contrato(CONTENEDOR)
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
    "barrer",
    "verificar",
    "verificar_salida",
    "inventario",
    "axiomas",
    "tru_ri",
    "tru_total",
    "listar_formulas",
    "reporte",
    "diagnostico",
    "ejecutar_total",
    "inspeccionar",
    "registrar_inventario",
    "FormulaError",
    "FormulaNoEncontradaError",
    "ContratoInvalido",
    "evaluar_universal",
]

# ===============================================================
# FIN EXPORTACIONES
# ===============================================================
# ===============================================================
# FIN DEL MÓDULO
# ===============================================================
