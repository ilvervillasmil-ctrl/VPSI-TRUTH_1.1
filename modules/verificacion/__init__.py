# ===============================================================
# VPSI-TRUTH — modules/verificacion/__init__.py
# ===============================================================
#
# MÓDULO:              verificacion
# ID:                  VX
# Rol:                 VX
# Versión módulo:      2.0
# Versión contrato:    1.0
# Esquema contrato:    VPSI-CONTRACT-1.0
# Estabilidad:         ESTABLE
# Compatible desde:    1.0
# API Engine:          >=1.0
#
# ---------------------------------------------------------------
# JURISDICCIÓN
# ---------------------------------------------------------------
#
# Autoridad exclusiva de verificación estructural.
#
# Jurisdicción: cualquier estructura susceptible de contrastarse
# contra reglas formales, por ejemplo:
#   - código
#   - contratos
#   - módulos
#   - configuraciones
#   - salidas
#   - estructuras
#   - grafos / árboles
#   - futuras representaciones
#
# Hoy el algoritmo operativo verifica código vía AuditorAxiomatico.
# Mañana podrá verificar más tipos de estructuras sin cambiar
# la responsabilidad del módulo ni su API pública.
#
# ---------------------------------------------------------------
# OFICIO ÚNICO
# ---------------------------------------------------------------
#
# Determinar si una estructura satisface o viola un conjunto
# de reglas formales.
#
# No interpreta intención.
# No calcula Tru.
# No toma decisiones.
# No corrige.
# No modifica.
# No ejecuta.
# Solo verifica. Solo produce evidencia.
#
# ---------------------------------------------------------------
# SEPARACIÓN DE AUTORIDADES
# ---------------------------------------------------------------
#
# VX produce evidencia de verificación.
# Diagnóstico decide qué hacer con ella (si Engine se la entrega).
# AX es la única autoridad del conocimiento axiomático.
#
# VX nunca conoce la implementación de Diagnóstico.
# VX nunca sustituye a AX.
# VX nunca sustituye a Diagnóstico.
#
# Secuencia correcta:
#
#   Engine decide verificar
#        ↓
#   Engine invoca VX.verificar / VX.barrer
#        ↓
#   VX produce evidencia estructurada
#        ↓
#   Engine decide si deposita / envía a Diagnóstico
#
# ---------------------------------------------------------------
# AX Y CONOCIMIENTO
# ---------------------------------------------------------------
#
# Las declaraciones oficiales viven únicamente en AX.
# VX puede consumir axiomas que Engine le entregue.
# axiomas() se mantiene solo como alias de compatibilidad
# temporal; no es un repositorio de conocimiento.
#
# ===============================================================

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .auditor import AuditorAxiomatico

# ===============================================================
# SECCIÓN 1 — CONSTANTES DE IDENTIDAD
# ===============================================================

_ID = "VX"
_NOMBRE = "verificacion"
_ROL = "VX"
_VERSION = "2.0"
_VERSION_CONTRATO = "1.0"
_ESQUEMA = "VPSI-CONTRACT-1.0"
_ESTABILIDAD = "ESTABLE"
_COMPATIBLE_DESDE = "1.0"
_API_ENGINE = ">=1.0"


# ===============================================================
# SECCIÓN 2 — NÚCLEO DE VERIFICACIÓN (lógica de Auditor intacta)
# ===============================================================

def _ejecutar_barrido(
    codigo_fuente: Optional[Dict[str, Any]] = None,
    declaraciones_axiomaticas: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Orquesta el barrido transversal mediante AuditorAxiomatico.
    No modifica la lógica del auditor.
    No llama a Diagnóstico.
    Solo produce evidencia.
    """
    auditor = AuditorAxiomatico()
    resultado = auditor.ejecutar_barrido_transversal(
        codigo_fuente or {},
        declaraciones_axiomaticas or {},
    )
    if not isinstance(resultado, dict):
        return {
            "coherente": False,
            "errores": [
                {
                    "tipo": "salida_invalida",
                    "detalle": "AuditorAxiomatico no devolvió dict",
                }
            ],
            "evidencia": [],
        }
    return resultado


def verificar(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Capacidad principal: verificar una estructura contra reglas formales.

    peticion (opcional) puede incluir:
      - codigo_fuente
      - declaraciones_axiomaticas
      - estructura (futuro: contratos, módulos, grafos, …)

    Hoy el camino operativo usa codigo_fuente + declaraciones.
    La forma de la API admite crecimiento sin romper firmas.
    """
    base = peticion if isinstance(peticion, dict) else {}
    resultado = _ejecutar_barrido(
        base.get("codigo_fuente"),
        base.get("declaraciones_axiomaticas"),
    )
    return {
        "id": _ID,
        "nombre": _NOMBRE,
        "rol": _ROL,
        "version": _VERSION,
        "coherente": bool(resultado.get("coherente", False)),
        "errores": list(resultado.get("errores") or []),
        "evidencia": resultado.get("evidencia", resultado),
        "detalle": resultado,
        "nota": (
            "VX solo produce evidencia de verificación estructural. "
            "No interpreta, no corrige, no deposita en Diagnóstico."
        ),
    }


def barrer(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Alias operativo de verificar.
    Centinela de coherencia estructural del barrido.
    """
    return verificar(peticion)


# ===============================================================
# SECCIÓN 3 — COMPATIBILIDAD axiomas() (no es repositorio)
# ===============================================================

def axiomas() -> List[Dict[str, Any]]:
    """
    Alias temporal de compatibilidad.

    AX es la única autoridad del conocimiento axiomático.
    Esta función NO declara conocimiento oficial.
    No duplica el corpus de AX.
    Devuelve lista vacía: las declaraciones se consumen vía Engine → AX.
    """
    return []


# ===============================================================
# SECCIÓN 4 — REPORTING ESTÁNDAR (sin dependencias externas)
# ===============================================================

def inventario(peticion: Any = None) -> Dict[str, Any]:
    """
    Inventario del módulo VX.
    Forma mínima contractual alineada a VPSI-CONTRACT-1.0.
    """
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
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "funcion": (
            "Autoridad de verificación estructural. "
            "Determina si una estructura satisface o viola reglas formales. "
            "Solo produce evidencia. No interpreta, no corrige, no ejecuta."
        ),
        "jurisdiccion": [
            "codigo",
            "contratos",
            "modulos",
            "configuraciones",
            "salidas",
            "estructuras",
            "grafos",
            "arboles",
            "futuras_representaciones",
        ],
        "requiere": [],
    }


def reporte(peticion: Any = None) -> Dict[str, Any]:
    """Reporte interno de estado del módulo VX."""
    inv = inventario()
    return {
        "id": _ID,
        "nombre": _NOMBRE,
        "rol": _ROL,
        "version": _VERSION,
        "version_contrato": _VERSION_CONTRATO,
        "esquema": _ESQUEMA,
        "estabilidad": _ESTABILIDAD,
        "estado": "OPERATIVO",
        "coherente": True,
        "capacidades": inv.get("capacidades"),
        "jurisdiccion": inv.get("jurisdiccion"),
        "requiere": [],
        "nota": (
            "VX no mantiene sesión de auditoría persistente. "
            "Cada verificar()/barrer() produce evidencia puntual."
        ),
    }


def diagnostico(peticion: Any = None) -> Dict[str, Any]:
    """
    Diagnóstico propio del módulo VX.
    No consulta DiagnosticoGlobal.
    Solo reporta el estado interno de esta autoridad.
    """
    return {
        "id": _ID,
        "nombre": _NOMBRE,
        "rol": _ROL,
        "estado": "OPERATIVO",
        "problemas": [],
        "advertencias": [],
        "recomendaciones": [],
        "coherente": True,
        "nota": (
            "Diagnóstico propio de VX. "
            "La evidencia de verificaciones concretas se obtiene "
            "invocando verificar()/barrer(); Engine decide su destino."
        ),
    }


def verificar_salida(salida: Any) -> bool:
    """
    Valida forma mínima de una salida de VX.
    No interpreta contenido semántico.
    """
    if not isinstance(salida, dict):
        return False
    return "coherente" in salida or "id" in salida


# ===============================================================
# SECCIÓN 5 VPSI-CONTRACTo
# ===============================================================

CONTENEDOR: Dict[str, Any] = {
    # ============================================================
    # ESQUEMA
    # ============================================================
    "esquema": _ESQUEMA,
    "version_contrato": _VERSION_CONTRATO,
    "version_modulo": _VERSION,
    "estabilidad": _ESTABILIDAD,
    "compatible_desde": _COMPATIBLE_DESDE,
    "api_engine": _API_ENGINE,

    # ============================================================
    # IDENTIDAD
    # ============================================================
    "id": _ID,
    "nombre": _NOMBRE,
    "rol": _ROL,
    "descripcion": (
        "Autoridad exclusiva de verificación estructural. "
        "Determina si una estructura satisface o viola un conjunto "
        "de reglas formales. Jurisdicción: código, contratos, módulos, "
        "configuraciones, salidas, estructuras, grafos y futuras "
        "representaciones. Solo produce evidencia verificable. "
        "No interpreta, no calcula Tru, no decide, no corrige, "
        "no modifica, no ejecuta. No sustituye a AX ni a Diagnóstico."
    ),

    # ============================================================
    # PROPÓSITO
    # ============================================================
    "funcion": (
        "Contrastar estructuras contra reglas formales y generar "
        "evidencia de verificación. El algoritmo operativo actual "
        "usa AuditorAxiomatico sobre código; la responsabilidad del "
        "módulo admite cualquier estructura formal sin cambiar la API."
    ),
    "no_hace": [
        "No interpreta intención",
        "No calcula C",
        "No calcula L",
        "No calcula K",
        "No calcula Tru",
        "No modifica estructuras auditadas",
        "No corrige implementaciones",
        "No toma decisiones",
        "No ejecuta acciones",
        "No deposita en Diagnóstico",
        "No sustituye a AX",
        "No sustituye a Diagnóstico",
        "No declara conocimiento axiomático oficial",
    ],

    # ============================================================
    # AUTORIDAD
    # ============================================================
    "autoridad": [
        "Verificar estructuras",
        "Contrastar estructuras contra reglas formales",
        "Reportar inconsistencias estructurales",
        "Generar evidencia de verificación",
        "Reportar su estado",
        "Reportar inventario",
        "Reportar diagnóstico propio",
    ],

    # ============================================================
    # CONOCIMIENTO EXPORTABLE
    # ============================================================
    "conocimiento_exportable": [
        "verificar",
        "barrer",
        "inventario",
        "reporte",
        "diagnostico",
        "verificar_salida",
        "evidencia",
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
    "acceso_archivos": ["*"],

    # ============================================================
    # VALIDAR ESQUEMA A NIVEL MÓDULO (AGREGADO — obligatorio en el esquema)
    # ============================================================
    "validar_esquema": ["*"],

    #============================================================
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
        "validar_esquema": True,     # ← AGREGADO
        "acceso_archivos": True,     # ← AGREGADO
    },

    # ============================================================
    # CONSULTAS SOPORTADAS
    # ============================================================
    "consultas_soportadas": [
        "verificar_estructura",
        "barrer",
        "obtener_inventario",
        "obtener_reporte",
        "obtener_diagnostico",
        "verificar_salida",
    ],

    # ============================================================
    # CAPACIDADES
    # ============================================================
    "capacidades": {
        "verificar": verificar,
        "barrer": barrer,
        "inventario": inventario,
        "reporte": reporte,
        "diagnostico": diagnostico,
        "verificar_salida": verificar_salida,
        "axiomas": axiomas,
    },

    # ============================================================
    # METADATOS DE CAPACIDADES (1:1 OBLIGATORIO)
    # ============================================================
    "capacidades_meta": {
        "verificar": {
            "descripcion": (
                "Verifica una estructura contra reglas formales. "
                "Produce evidencia. No interpreta ni corrige."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con id, coherente, errores, evidencia, detalle"
            ),
            "acceso_archivos": ["*"],
        },
        "barrer": {
            "descripcion": (
                "Alias de verificar. Centinela de coherencia estructural."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con id, coherente, errores, evidencia, detalle"
            ),
            "acceso_archivos": ["*"],
        },
        "inventario": {
            "descripcion": (
                "Inventario contractual del módulo VX."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con id, nombre, rol, version, version_contrato, "
                "esquema, estabilidad, capacidades, jurisdiccion"
            ),
            "acceso_archivos": ["*"],
        },
        "reporte": {
            "descripcion": (
                "Reporte interno de estado de VX."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con id, estado, coherente, capacidades, jurisdiccion"
            ),
            "acceso_archivos": ["*"],
        },
        "diagnostico": {
            "descripcion": (
                "Diagnóstico propio de VX. No consulta DiagnosticoGlobal."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con id, estado, problemas, advertencias, "
                "recomendaciones"
            ),
            "acceso_archivos": ["*"],
        },
        "verificar_salida": {
            "descripcion": (
                "Comprueba forma mínima de una salida de VX."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "bool",
            "acceso_archivos": ["*"],
        },
        "axiomas": {
            "descripcion": (
                "Alias temporal de compatibilidad. "
                "AX es la única autoridad del conocimiento. "
                "No declara corpus oficial."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "list vacía (conocimiento oficial en AX)"
            ),
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
        "acceso_archivos": True,      # ← AGREGADA
        "validar_esquema": True,      # ← AGREGADA
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
        "VX nunca modifica la estructura auditada",
        "VX nunca corrige evidencia",
        "VX nunca interpreta intención",
        "VX nunca calcula métricas de verdad (C/L/K/Tru)",
        "VX solo produce evidencia verificable",
        "VX no deposita en Diagnóstico; Engine decide el destino de la evidencia",
        "VX no declara conocimiento axiomático oficial (AX es la autoridad)",
        "las capacidades declaradas son callables tras la resolución",
        "este módulo no modifica el estado de otros módulos",
        "este módulo no inventa capacidades no declaradas en CONTENEDOR",
        "este módulo siempre puede reportar su propio estado",
        "inventario() siempre incluye id, nombre, rol, version del CONTENEDOR",
    ],

}  # <--- CIERRE FINAL
# ===============================================================
# SECCIÓN 6 — EXPORTS
# ===============================================================

__all__ = [
    "CONTENEDOR",
    "verificar",
    "barrer",
    "inventario",
    "reporte",
    "diagnostico",
    "verificar_salida",
    "axiomas",
]
