# ===============================================================
# VPSI-TRUTH — modules/self/__init__.py
# ===============================================================
#
# MÓDULO:              self
# ID:                  SF
# Rol:                 SF
# Versión módulo:      1.0
# Versión contrato:    1.0
# Esquema contrato:    VPSI-CONTRACT-1.0
# Estabilidad:         FASE
# Compatible desde:    1.0
# API Engine:          >=1.0
#
# Función:
#   Yo funcional del sistema. Centro de elección e identidad de fase.
#   Casa operativa: L4. Punto de acceso a las perspectivas L1…L6.
#   Oscila entre alturas; registra actos de agency sin side-effects.
#
# Qué hace:
#   - Expone identidad de fase anclada en el cuerpo axiomático self.
#   - Reporta y cambia la altura operativa (L1…L6) del Self.
#   - Clasifica el modo de lucidez (REACTIVE…INTEGRATED).
#   - Registra actos de elección sin efectos externos.
#   - Declara el acceso a mecanismos de perspectiva L1…L6
#     para cálculo y resolución de problemas.
#   - Verifica coherencia interna y reporta estado propio.
#
# Responsabilidad:
#   Ser el punto de referencia de elección e identidad de fase.
#   Distinguir oscilar (altura) de elegir (agency).
#   Ofrecer a Engine las perspectivas L1…L6 como mecanismos legibles.
#
# Autoridad:
#   - Declarar desde qué altura opera el Self.
#   - Registrar elecciones como actos de agency.
#   - Reportar inventario, estado y diagnóstico propios.
#
# Conocimiento exportable:
#   yo_funcional, oscilar, desde_donde, elegir, estado_self,
#   barrer, verificar, inventario, reporte, diagnostico
#
# Observaciones:
#   No orquesta. No calcula Tru. No interpreta contenido de negocio.
#   Las subcarpetas L1…L6 son mecanismos de perspectiva, no dependencias
#   de arranque. AX se consulta en runtime solo para identidad.
#
# ===============================================================

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Set
# ===============================================================
# PARTE 1 — PRINCIPIOS, BANDERAS Y ESPECIFICACIONES PRECISAS
# ===============================================================

# ===============================================================
# 1.1 — IDENTIDAD
# ===============================================================

ID_MODULO = "SF"
NOMBRE_MODULO = "self"
ROL_MODULO = "SF"

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
ESTABILIDAD = "FASE"

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
# 1.4 — CAPAS Y MODOS (DOMINIO SF)
# ===============================================================

CAPAS_VALIDAS: Set[str] = {
    "L1_CUERPO",
    "L2_EGO",
    "L3_MENTE",
    "L4_YO",
    "L5_CONSCIENCIA",
    "L6_ALMA",
}

CASA_SELF = "L4_YO"

MODOS_VALIDOS: Set[str] = {
    "REACTIVE",
    "MECHANICAL",
    "CONSCIOUS",
    "META",
    "INTEGRATED",
}

# ===============================================================
# FIN 1.4
# ===============================================================


# ===============================================================
# 1.5 — INVARIANTES
# ===============================================================

INVARIANTES = (
    "el id del módulo nunca cambia",
    "el rol nunca cambia",
    "la casa operativa del Self es L4_YO",
    "oscilar no es elegir",
    "elegir no ejecuta efectos externos",
    "las perspectivas L1…L6 son mecanismos legibles, no dependencias de arranque",
    "las capacidades declaradas son callables tras la resolución",
    "este módulo no modifica el estado de otros módulos",
    "este módulo no inventa capacidades no declaradas en CONTENEDOR",
    "este módulo siempre puede reportar su propio estado",
)

# ===============================================================
# FIN 1.5
# ===============================================================


# ===============================================================
# 1.6 — CONFIGURACIÓN
# ===============================================================

_DIR = Path(__file__).parent

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
# 4.2 — ESTADO INTERNO (FASE; NO PERSISTENCIA DE NEGOCIO)
# ===============================================================

_estado_self: Dict[str, Any] = {
    "capa_activa": CASA_SELF,
    "altura_operativa": "L4",
    "modo": "CONSCIOUS",
    "historial_oscilacion": [],
    "historial_elecciones": [],
    "loop_sospechado": False,
}

# ===============================================================
# FIN 4.2
# ===============================================================

# ===============================================================
# FIN PARTE 4
# ===============================================================

CONTENEDOR: Dict[str, Any] = {
    # ============================================================
    # ESQUEMA
    # ============================================================
    "esquema": "VPSI-CONTRACT-1.0",
    "version_contrato": "1.0",
    "version_modulo": "1.0",
    "estabilidad": "FASE",
    "compatible_desde": "1.0",
    "api_engine": ">=1.0",

    # ============================================================
    # IDENTIDAD
    # ============================================================
    "id": "SF",
    "nombre": "self",
    "rol": "SF",
    "descripcion": (
        "Yo funcional del sistema. Centro de elección e identidad de fase. "
        "Casa operativa L4. Punto de acceso a perspectivas L1…L6. "
        "Oscila entre alturas; registra actos de agency sin side-effects. "
        "No orquesta. No calcula Tru."
    ),

    # ============================================================
    # PROPÓSITO
    # ============================================================
    "funcion": (
        "Ser el punto de referencia de elección e identidad de fase: "
        "exponer quién es el sistema en fase, desde qué altura opera, "
        "en qué modo de lucidez está, registrar actos de elección, "
        "y ofrecer a Engine las perspectivas L1…L6 como mecanismos "
        "legibles para cálculo y resolución de problemas."
    ),
    "no_hace": [],

    # ============================================================
    # AUTORIDAD
    # ============================================================
    "autoridad": [
        "Exponer identidad de fase (yo_funcional)",
        "Reportar y cambiar altura operativa del Self (oscilar)",
        "Declarar desde qué altura opera (desde_donde)",
        "Clasificar modo de lucidez (estado_self)",
        "Registrar actos de agency sin side-effects (elegir)",
        "Declarar acceso a perspectivas L1…L6",
        "Verificar coherencia interna y reportar estado propio",
    ],

    # ============================================================
    # CONOCIMIENTO EXPORTABLE
    # ============================================================
    "conocimiento_exportable": [
        "yo_funcional",
        "oscilar",
        "desde_donde",
        "elegir",
        "estado_self",
        "barrer",
        "verificar",
        "inventario",
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
    "requiere": [
    "CE", "AX", "FO", "MC",
    "CA", "CX", "DI", "RE", "VX",
    "TX", "CH", "CIT", "DGCO", "UI",
    "CC", "TT", "SC", "CT"
    ],
    # ============================================================
    # ACCESO A ARCHIVOS (AGREGADO — obligatorio en el esquema)
    # ============================================================
    "acceso_archivos": ["*"],

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
        "yo_funcional",
        "desde_donde",
        "estado_self",
        "oscilar",
        "elegir",
        "obtener_inventario",
        "obtener_reporte",
        "obtener_diagnostico",
        "verificar_coherencia",
    ],

    # ============================================================
    # CAPACIDADES
    # ============================================================
        "capacidades": {
        # --- CENTINELA ---
        "verificar": "verificar",
        "barrer": "barrer",
        "verificar_salida": "verificar_salida",

        # --- IDENTIDAD Y FASE ---
        "yo_funcional": "yo_funcional",
        "oscilar": "oscilar",
        "desde_donde": "desde_donde",
        "estado_self": "estado_self",
        "elegir": "elegir",

        # --- INVENTARIO Y REPORTING ---
        "inventario": "inventario",
        "reporte": "reporte",
        "diagnostico": "diagnostico",

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
                "Alias de barrer. Verifica coherencia interna de SF."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con coherente, capa_activa, modo, errores"
            ),
            "acceso_archivos": ["*"],
        },

        "barrer": {
            "descripcion": (
                "Centinela de SF: identidad y estado interno."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con coherente, identidad_disponible, "
                "capa_activa, modo, errores"
            ),
            "acceso_archivos": ["*"],
        },

        "verificar_salida": {
            "descripcion": (
                "Comprueba forma mínima de una salida de SF."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "bool",
            "acceso_archivos": ["*"],
        },

        "yo_funcional": {
            "descripcion": (
                "Identidad de fase anclada en cuerpo axiomático self."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con capa_activa, modo, ax_self, "
                "identidad_disponible, perspectivas"
            ),
            "acceso_archivos": ["*"],
        },

        "oscilar": {
            "descripcion": (
                "Cambia o reporta la altura operativa del Self (L1…L6)."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con ok, capa_activa, altura_operativa, "
                "modo, cambio"
            ),
            "acceso_archivos": ["*"],
        },

        "desde_donde": {
            "descripcion": (
                "Reporta altura y modo actuales del Self."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con capa_activa, altura_operativa, modo, "
                "en_casa, perspectivas"
            ),
            "acceso_archivos": ["*"],
        },

        "estado_self": {
            "descripcion": (
                "Clasifica lucidez: "
                "REACTIVE|MECHANICAL|CONSCIOUS|META|INTEGRATED."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con modo, capa_activa, en_casa, coherente"
            ),
            "acceso_archivos": ["*"],
        },

        "elegir": {
            "descripcion": (
                "Registra un acto de agency sin ejecutar efectos externos."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con ok, eleccion, desde, modo, n_elecciones"
            ),
            "acceso_archivos": ["*"],
        },

        "inventario": {
            "descripcion": (
                "Inventario estructural del módulo SF."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con id, capacidades, capas_validas, "
                "modos_validos, perspectivas"
            ),
            "acceso_archivos": ["*"],
        },

        "reporte": {
            "descripcion": (
                "Reporte de estado del módulo SF."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con estado, coherente, capa_activa, "
                "modo, errores"
            ),
            "acceso_archivos": ["*"],
        },

                "diagnostico": {
            "descripcion": (
                "Diagnóstico: problemas, advertencias, recomendaciones."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con estado, problemas, advertencias, "
                "recomendaciones"
            ),
            "acceso_archivos": ["*"],
        },

        # --- CAPACIDADES ARQUITECTÓNICAS (OBLIGATORIAS ENGINE) ---
        "ejecutar_total": {
            "descripcion": (
                "Autoridad total de ENGINE sobre SF. "
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
                "Capacidad meta de inspeccion estructural de SF. "
                "Expone constantes, capacidades, capas, modos y estado "
                "sin alterar el contrato ni calcular."
            ),
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["acceso_archivos"],
            "salida": "dict con estructura, capacidades y estado del modulo",
            "acceso_archivos": ["acceso_archivos"],
        },
        "registrar_inventario": {
            "descripcion": (
                "Registra el inventario estructural de SF "
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
        "evaluar_universal": True,

        # --- BANDERAS NUEVAS (OBLIGATORIAS ENGINE) ---
        "ejecutar_total": True,
        "inspeccionar": True,
        "registrar_inventario": True,
    },
    # ============================================================
    # ESTADOS VÁLIDOS
    # ============================================================
    "estados_validos": [
        "NO_INICIADO",
        "OPERATIVO",
        "DEGRADADO",
        "RECHAZADO",
    ],

    # ============================================================
    # INVARIANTES
    # ============================================================
    "invariantes": [
        "el id del módulo nunca cambia",
        "el rol nunca cambia",
        "la casa operativa del Self es L4_YO",
        "oscilar no es elegir",
        "elegir no ejecuta efectos externos",
        "las perspectivas L1…L6 son mecanismos legibles, no dependencias de arranque",
        "las capacidades declaradas son callables tras la resolución",
        "este módulo no modifica el estado de otros módulos",
        "este módulo no inventa capacidades no declaradas en CONTENEDOR",
        "este módulo siempre puede reportar su propio estado",
    ],

}  # <--- CIERRE FINAL

# ---------------------------------------------------------------------------
# CONSTANTES DE CAPA (L4 = casa)
# ---------------------------------------------------------------------------

CAPAS_VALIDAS: Set[str] = {
    "L1_CUERPO",
    "L2_EGO",
    "L3_MENTE",
    "L4_YO",
    "L5_CONSCIENCIA",
    "L6_ALMA",
}

CASA_SELF = "L4_YO"

MODOS_VALIDOS: Set[str] = {
    "REACTIVE",
    "MECHANICAL",
    "CONSCIOUS",
    "META",
    "INTEGRATED",
}

# ---------------------------------------------------------------------------
# ESTADO INTERNO (fase; no persistencia de negocio)
# ---------------------------------------------------------------------------

_estado_self: Dict[str, Any] = {
    "capa_activa": CASA_SELF,
    "altura_operativa": "L4",
    "modo": "CONSCIOUS",
    "historial_oscilacion": [],
    "historial_elecciones": [],
    "loop_sospechado": False,
}


def _cfg() -> Dict[str, Any]:
    return CONTENEDOR


def _altura_de_capa(capa: str) -> str:
    if not capa:
        return "L4"
    return capa.split("_", 1)[0]


def _modo_desde_altura(altura: str) -> str:
    mapa = {
        "L1": "REACTIVE",
        "L2": "REACTIVE",
        "L3": "MECHANICAL",
        "L4": "CONSCIOUS",
        "L5": "META",
        "L6": "INTEGRATED",
    }
    return mapa.get(altura, "CONSCIOUS")


def _normalizar_capa(hacia: str) -> Optional[str]:
    clave = str(hacia).strip().upper()
    if clave in CAPAS_VALIDAS:
        return clave
    for c in CAPAS_VALIDAS:
        if c.startswith(clave + "_") or c == clave:
            return c
    for c in CAPAS_VALIDAS:
        if c.startswith(clave):
            return c
    return None


# ---------------------------------------------------------------------------
# IDENTIDAD (runtime; AX solo si está disponible)
# ---------------------------------------------------------------------------

def _recolectar_self_ax() -> Dict[str, Any]:
    """
    Lee declaraciones del cuerpo self.
    Fail-closed: si no hay fuente, no inventa identidad.
    """
    try:
        from modules.axiomas import recolectar  # runtime only
    except Exception as e:
        return {
            "ok": False,
            "razon": "fuente axiomática no disponible: {0}: {1}".format(
                type(e).__name__, e
            ),
            "declaraciones": [],
            "n": 0,
            "errores_recoleccion": 1,
        }

    try:
        decls, errores = recolectar()
    except Exception as e:
        return {
            "ok": False,
            "razon": "recolección falló: {0}: {1}".format(type(e).__name__, e),
            "declaraciones": [],
            "n": 0,
            "errores_recoleccion": 1,
        }

    self_decls: List[Dict[str, Any]] = []
    for d in decls or []:
        cuerpo = str(d.get("cuerpo") or d.get("fuente") or "").lower()
        id_decl = str(d.get("id") or "")
        if cuerpo == "self" or id_decl.upper().startswith("SF"):
            self_decls.append(
                {
                    "id": d.get("id"),
                    "tipo": d.get("tipo"),
                    "gobierna": list(d.get("gobierna") or []),
                    "enunciado": d.get("enunciado") or d.get("sujeto"),
                }
            )

    return {
        "ok": True,
        "razon": None,
        "declaraciones": self_decls,
        "n": len(self_decls),
        "errores_recoleccion": len(errores or []),
    }


# ---------------------------------------------------------------------------
# CAPACIDADES
# ---------------------------------------------------------------------------

def yo_funcional(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Identidad de fase del sistema.
    Ancla: cuerpo axiomático self. No modifica estado externo.
    """
    ax = _recolectar_self_ax()
    return {
        "contenedor": "self",
        "id": "SF",
        "rol": "SF",
        "tipo": "yo_funcional",
        "capa_activa": _estado_self.get("capa_activa"),
        "altura_operativa": _estado_self.get("altura_operativa"),
        "modo": _estado_self.get("modo"),
        "casa": CASA_SELF,
        "ax_self": ax,
        "identidad_disponible": bool(ax.get("ok") and ax.get("n", 0) > 0),
        "perspectivas": sorted(CAPAS_VALIDAS),
        "nota": (
            "Yo funcional de fase. Casa L4. "
            "Acceso a perspectivas L1…L6 para cálculo y resolución. "
            "Identidad anclada en cuerpo self."
        ),
    }


def oscilar(
    hacia: Optional[str] = None,
    contexto: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Cambia o reporta la altura operativa del Self.
    Oscilar ≠ elegir. Solo mueve perspectiva.
    """
    actual = _estado_self.get("capa_activa")
    if hacia is None:
        return {
            "ok": True,
            "capa_activa": actual,
            "altura_operativa": _estado_self.get("altura_operativa"),
            "modo": _estado_self.get("modo"),
            "cambio": False,
            "capas_validas": sorted(CAPAS_VALIDAS),
            "contexto": contexto or {},
        }

    destino = _normalizar_capa(hacia)
    if destino is None:
        return {
            "ok": False,
            "capa_activa": actual,
            "cambio": False,
            "error": "capa no válida: {0}".format(hacia),
            "capas_validas": sorted(CAPAS_VALIDAS),
        }

    cambio = destino != actual
    if cambio:
        hist = list(_estado_self.get("historial_oscilacion") or [])
        hist.append({"desde": actual, "hacia": destino})
        _estado_self["historial_oscilacion"] = hist[-20:]
        _estado_self["capa_activa"] = destino
        altura = _altura_de_capa(destino)
        _estado_self["altura_operativa"] = altura
        _estado_self["modo"] = _modo_desde_altura(altura)

    return {
        "ok": True,
        "capa_activa": _estado_self["capa_activa"],
        "altura_operativa": _estado_self["altura_operativa"],
        "modo": _estado_self["modo"],
        "cambio": cambio,
        "desde": actual,
        "hacia": destino,
        "contexto": contexto or {},
        "nota": "oscilación de altura; no es acto de elección",
    }


def desde_donde(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Reporta desde qué altura y en qué modo opera el Self ahora."""
    return {
        "contenedor": "self",
        "capa_activa": _estado_self.get("capa_activa"),
        "altura_operativa": _estado_self.get("altura_operativa"),
        "modo": _estado_self.get("modo"),
        "casa": CASA_SELF,
        "en_casa": _estado_self.get("capa_activa") == CASA_SELF,
        "loop_sospechado": bool(_estado_self.get("loop_sospechado")),
        "n_oscilaciones": len(_estado_self.get("historial_oscilacion") or []),
        "n_elecciones": len(_estado_self.get("historial_elecciones") or []),
        "perspectivas": sorted(CAPAS_VALIDAS),
    }


def estado_self(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Clasificación de lucidez del Self.
    REACTIVE | MECHANICAL | CONSCIOUS | META | INTEGRATED
    """
    modo = _estado_self.get("modo") or "CONSCIOUS"
    return {
        "contenedor": "self",
        "modo": modo,
        "modos_validos": sorted(MODOS_VALIDOS),
        "capa_activa": _estado_self.get("capa_activa"),
        "altura_operativa": _estado_self.get("altura_operativa"),
        "casa": CASA_SELF,
        "en_casa": _estado_self.get("capa_activa") == CASA_SELF,
        "coherente": modo in MODOS_VALIDOS,
        "nota": (
            "CONSCIOUS = casa L4 (elige). "
            "REACTIVE = arrastrado. MECHANICAL = patrón. "
            "META = observa procesos. INTEGRATED = dirige."
        ),
    }


def elegir(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Registra un acto de agency.
    No ejecuta efectos externos. No orquesta. Solo deja constancia.
    """
    p = dict(peticion or {})
    opciones = p.get("opciones")
    criterio = p.get("criterio")
    eleccion = p.get("eleccion")
    desde = p.get("desde") or _estado_self.get("capa_activa") or CASA_SELF

    if opciones is not None and not isinstance(opciones, (list, tuple)):
        return {
            "ok": False,
            "error": "opciones debe ser lista o None",
            "capa_activa": _estado_self.get("capa_activa"),
        }

    if eleccion is None and opciones:
        return {
            "ok": False,
            "error": "eleccion requerida cuando hay opciones",
            "opciones": list(opciones),
            "capa_activa": _estado_self.get("capa_activa"),
        }

    registro = {
        "eleccion": eleccion,
        "criterio": criterio,
        "desde": desde,
        "modo": _estado_self.get("modo"),
        "altura_operativa": _estado_self.get("altura_operativa"),
    }
    hist = list(_estado_self.get("historial_elecciones") or [])
    hist.append(registro)
    _estado_self["historial_elecciones"] = hist[-50:]

    return {
        "ok": True,
        "eleccion": eleccion,
        "criterio": criterio,
        "desde": desde,
        "modo": _estado_self.get("modo"),
        "altura_operativa": _estado_self.get("altura_operativa"),
        "casa": CASA_SELF,
        "n_elecciones": len(_estado_self["historial_elecciones"]),
        "nota": "acto de agency registrado; sin ejecución externa",
    }


def barrer(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Centinela de SF: identidad legible y estado interno coherente."""
    yo = yo_funcional()
    ax = yo.get("ax_self") or {}
    modo = _estado_self.get("modo")
    capa = _estado_self.get("capa_activa")

    errores: List[str] = []
    if not ax.get("ok"):
        errores.append(str(ax.get("razon") or "identidad axiomática no legible"))
    if modo not in MODOS_VALIDOS:
        errores.append("modo inválido: {0}".format(modo))
    if capa not in CAPAS_VALIDAS:
        errores.append("capa_activa inválida: {0}".format(capa))

    coherente = len(errores) == 0
    return {
        "contenedor": "self",
        "id": "SF",
        "rol": "SF",
        "coherente": coherente,
        "identidad_disponible": yo.get("identidad_disponible"),
        "capa_activa": capa,
        "altura_operativa": _estado_self.get("altura_operativa"),
        "modo": modo,
        "casa": CASA_SELF,
        "n_declaraciones_self": ax.get("n", 0),
        "n_oscilaciones": len(_estado_self.get("historial_oscilacion") or []),
        "n_elecciones": len(_estado_self.get("historial_elecciones") or []),
        "capas_validas": sorted(CAPAS_VALIDAS),
        "perspectivas": sorted(CAPAS_VALIDAS),
        "errores": errores,
    }


def verificar(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return barrer(peticion)


def verificar_salida(salida: Any) -> bool:
    if not isinstance(salida, dict):
        return False
    return (
        "coherente" in salida
        or "capa_activa" in salida
        or "modo" in salida
        or "eleccion" in salida
        or "ax_self" in salida
    )


def inventario(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    cfg = _cfg()
    return {
        "id": cfg.get("id"),
        "nombre": cfg.get("nombre"),
        "rol": cfg.get("rol"),
        "version": cfg.get("version_modulo"),
        "version_contrato": cfg.get("version_contrato"),
        "esquema": cfg.get("esquema"),
        "estabilidad": cfg.get("estabilidad"),
        "compatible_desde": cfg.get("compatible_desde"),
        "api_engine": cfg.get("api_engine"),
        "casa": CASA_SELF,
        "capa_activa": _estado_self.get("capa_activa"),
        "modo": _estado_self.get("modo"),
        "capacidades": sorted((cfg.get("capacidades") or {}).keys()),
        "capas_validas": sorted(CAPAS_VALIDAS),
        "modos_validos": sorted(MODOS_VALIDOS),
        "perspectivas": sorted(CAPAS_VALIDAS),
        "n_oscilaciones": len(_estado_self.get("historial_oscilacion") or []),
        "n_elecciones": len(_estado_self.get("historial_elecciones") or []),
        "invariantes": list(cfg.get("invariantes") or []),
    }

# ===============================================================
# 8.x — DIAGNÓSTICO
# ===============================================================

def diagnostico(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Problemas y advertencias propios de SF. No diagnostica el sistema."""
    b = barrer()
    problemas = list(b.get("errores") or [])
    advertencias: List[str] = []
    recomendaciones: List[str] = []

    if not b.get("identidad_disponible"):
        advertencias.append("identidad axiomática self no disponible")
        recomendaciones.append(
            "Verificar cuerpo axiomático self en AX"
        )

    if b.get("capa_activa") != CASA_SELF:
        advertencias.append(
            "Self fuera de casa operativa ({0})".format(
                b.get("capa_activa")
            )
        )

    if not problemas and not advertencias:
        recomendaciones.append("SF coherente")

    coherente = bool(b.get("coherente"))
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "estado": (
            ESTADO_OPERATIVO if coherente else ESTADO_DEGRADADO
        ),
        "problemas": problemas,
        "advertencias": advertencias,
        "recomendaciones": recomendaciones,
        "coherente": coherente,
        "capa_activa": b.get("capa_activa"),
        "modo": b.get("modo"),
        "identidad_disponible": b.get("identidad_disponible"),
    }

# ===============================================================
# FIN 8.x
# ===============================================================


# ===============================================================
# CAPACIDADES ARQUITECTÓNICAS (OBLIGATORIAS ENGINE)
# ===============================================================

def ejecutar_total(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Autoridad total de ENGINE sobre SF.
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

            # Capacidades de SF con firma específica
            if nombre == "oscilar":
                hacia = peticion_normalizada.get("hacia")
                contexto = peticion_normalizada.get("contexto")
                resultados[nombre] = fn(hacia=hacia, contexto=contexto)
                continue

            if nombre == "elegir":
                resultados[nombre] = fn(peticion_normalizada)
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
    Inspección estructural de SF.
    Expone contrato y estado de fase sin calcular ni alterar.
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
            "CASA_SELF": CASA_SELF,
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
            "identidad_disponible": b.get("identidad_disponible"),
            "capa_activa": b.get("capa_activa"),
            "altura_operativa": b.get("altura_operativa"),
            "modo": b.get("modo"),
            "n_declaraciones_self": b.get("n_declaraciones_self"),
            "n_oscilaciones": b.get("n_oscilaciones"),
            "n_elecciones": b.get("n_elecciones"),
        },
        "capas_validas": sorted(CAPAS_VALIDAS),
        "modos_validos": sorted(MODOS_VALIDOS),
        "autoriza_engine": CONTENEDOR.get("autoriza_engine"),
        "reporting": CONTENEDOR.get("reporting"),
        "invariantes": list(INVARIANTES),
        "nota": (
            "inspeccionar expone estructura de SF sin calcular "
            "ni alterar el contrato ni el estado de fase."
        ),
    }


def registrar_inventario(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Instantánea determinista del inventario de SF.
    No altera evidencia ni estado de fase.
    """
    inv = inventario(peticion)
    return {
        "id": ID_MODULO,
        "operacion": "registrar_inventario",
        "registrado": True,
        "inventario": inv,
        "nota": (
            "Instantánea determinista del inventario de SF. "
            "No modifica fase ni evidencia."
        ),
    }

# ===============================================================
# 10 — VALIDACIÓN, RESOLUCIÓN Y EXPORTACIONES
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
# 8.x — REPORTE
# ===============================================================

def reporte(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Reporte de estado del módulo SF. No diagnostica el sistema."""
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
        "capa_activa": b.get("capa_activa"),
        "altura_operativa": b.get("altura_operativa"),
        "modo": b.get("modo"),
        "casa": CASA_SELF,
        "identidad_disponible": b.get("identidad_disponible"),
        "n_declaraciones_self": b.get("n_declaraciones_self"),
        "n_oscilaciones": b.get("n_oscilaciones"),
        "n_elecciones": b.get("n_elecciones"),
        "errores": b.get("errores"),
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "operaciones_arquitectonicas": {
            "ejecutar_total": True,
            "inspeccionar": True,
            "registrar_inventario": True,
        },
    }

# ===============================================================
# FIN 8.x
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

    # --- IDENTIDAD Y FASE ---
    "yo_funcional": yo_funcional,
    "oscilar": oscilar,
    "desde_donde": desde_donde,
    "estado_self": estado_self,
    "elegir": elegir,

    # --- INVENTARIO Y REPORTING ---
    "inventario": inventario,
    "reporte": reporte,
    "diagnostico": diagnostico,

    # --- CAPACIDADES ARQUITECTÓNICAS (OBLIGATORIAS ENGINE) ---
    "ejecutar_total": ejecutar_total,
    "inspeccionar": inspeccionar,
    "registrar_inventario": registrar_inventario,
    "evaluar_universal": evaluar_universal,
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
    "CAPAS_VALIDAS",
    "CASA_SELF",
    "MODOS_VALIDOS",
    "yo_funcional",
    "oscilar",
    "desde_donde",
    "estado_self",
    "elegir",
    "barrer",
    "verificar",
    "verificar_salida",
    "inventario",
    "reporte",
    "diagnostico",
    "ejecutar_total",
    "inspeccionar",
    "registrar_inventario",
    "ContratoInvalido",
    "evaluar_universal",
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
