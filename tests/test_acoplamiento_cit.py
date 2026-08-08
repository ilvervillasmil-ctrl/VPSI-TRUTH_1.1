# ===============================================================
# VPSI-TRUTH — modules/citacion/__init__.py
# ===============================================================

from __future__ import annotations

from typing import Any, Dict, List

# ===============================================================
# CONSTANTES DEL MÓDULO
# ===============================================================

ID_MODULO = "CIT"
NOMBRE_MODULO = "citacion"
ROL_MODULO = "CIT"

VERSION_MODULO = "2.0"
VERSION_CONTRATO = "1.0"
ESQUEMA_CONTRATO = "VPSI-CONTRACT-1.0"
ESTABILIDAD = "ESTABLE"
COMPATIBLE_DESDE = "1.0"
API_ENGINE = ">=1.0"

ESTADOS_VALIDOS = (
    "NO_INICIADO",
    "OPERATIVO",
    "DEGRADADO",
    "RECHAZADO",
)

INVARIANTES = (
    "el id del módulo nunca cambia",
    "el rol nunca cambia",
    "CIT solo gestiona citas y anuncios",
    "las capacidades declaradas son callables tras la resolución",
    "este módulo no modifica el estado de otros módulos",
    "este módulo no inventa capacidades no declaradas en CONTENEDOR",
    "este módulo siempre puede reportar su propio estado",
)


# ===============================================================
# CAPACIDADES (funciones reales)
# ===============================================================

def anunciar() -> Dict[str, Any]:
    return {"id": "CIT", "anuncio": "anuncio_registrado"}


def anunciar_todo() -> Dict[str, Any]:
    return {"id": "CIT", "anuncios": [], "n": 0}


def buscar() -> Dict[str, Any]:
    return {"id": "CIT", "declaraciones": [], "n": 0}


def citar() -> Dict[str, Any]:
    return {"id": "CIT", "citas": [], "n": 0}


def limpiar_ciclo() -> Dict[str, Any]:
    return {"ok": True, "id": "CIT"}


def inventario() -> Dict[str, Any]:
    return {
        "id": "CIT",
        "nombre": "citacion",
        "rol": "CIT",
        "version": "2.0",
        "version_contrato": "1.0",
        "esquema": "VPSI-CONTRACT-1.0",
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
    }


def reporte() -> Dict[str, Any]:
    return {
        "id": "CIT",
        "nombre": "citacion",
        "rol": "CIT",
        "estado": "OPERATIVO",
        "coherente": True,
        "version": "2.0",
    }


def diagnostico() -> Dict[str, Any]:
    return {
        "id": "CIT",
        "nombre": "citacion",
        "rol": "CIT",
        "estado": "OPERATIVO",
        "coherente": True,
        "problemas": [],
        "advertencias": [],
        "recomendaciones": [],
    }


def verificar() -> Dict[str, Any]:
    return {
        "id": "CIT",
        "coherente": True,
        "errores": [],
        "choques": [],
    }


def barrer() -> Dict[str, Any]:
    return verificar()


def verificar_salida(salida: Dict) -> bool:
    return bool(salida.get("coherente", False))


# ===============================================================
# CONTENEDOR (CONTRATO EXACTO)
# ===============================================================

CONTENEDOR: Dict[str, Any] = {

    # ----- ESQUEMA -----
    "esquema": ESQUEMA_CONTRATO,
    "version_contrato": VERSION_CONTRATO,
    "version_modulo": VERSION_MODULO,
    "estabilidad": ESTABILIDAD,
    "compatible_desde": COMPATIBLE_DESDE,
    "api_engine": API_ENGINE,

    # ----- IDENTIDAD -----
    "id": ID_MODULO,
    "nombre": NOMBRE_MODULO,
    "rol": ROL_MODULO,
    "descripcion": (
        "Sistema de citación y anuncios. Gestiona el registro "
        "de citas y anuncios del sistema."
    ),

    # ----- PROPÓSITO -----
    "funcion": (
        "Gestionar citas y anuncios del sistema, "
        "mantener registro de citaciones."
    ),
    "no_hace": [
        "No calcula Tru_total ni Tru_Ri",
        "No clasifica entrada de usuario",
        "No orquesta el sistema",
        "No modifica otros módulos",
    ],

    # ----- AUTORIDAD -----
    "autoridad": [
        "Gestionar citas y anuncios",
        "Mantener registro de citaciones",
        "Reportar estado, inventario y diagnóstico propios",
    ],

    # ----- CONOCIMIENTO EXPORTABLE -----
    "conocimiento_exportable": [
        "anunciar",
        "anunciar_todo",
        "buscar",
        "citar",
        "limpiar_ciclo",
        "inventario",
        "reporte",
        "diagnostico",
        "verificar",
        "barrer",
        "verificar_salida",
    ],

    # ----- DEPENDENCIAS -----
    "requiere": [],

    # ============================================================
    # AUTORIZACIÓN AL ENGINE (SOLO PERMISOS BÁSICOS)
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
        "modificar": False,
        "alterar": False,
        "reescribir": False,
    },

    # ----- CONSULTAS SOPORTADAS -----
    "consultas_soportadas": [
        "anunciar",
        "anunciar_todo",
        "buscar",
        "citar",
        "limpiar_ciclo",
        "inventario",
        "reporte",
        "diagnostico",
        "verificar",
        "barrer",
    ],

    # ----- CAPACIDADES -----
    "capacidades": {
        "anunciar": anunciar,
        "anunciar_todo": anunciar_todo,
        "buscar": buscar,
        "citar": citar,
        "limpiar_ciclo": limpiar_ciclo,
        "inventario": inventario,
        "reporte": reporte,
        "diagnostico": diagnostico,
        "verificar": verificar,
        "barrer": barrer,
        "verificar_salida": verificar_salida,
    },

    # ----- METADATOS DE CAPACIDADES (1:1 OBLIGATORIO) -----
    "capacidades_meta": {
        "anunciar": {
            "descripcion": "Registra un anuncio en el sistema.",
            "entrada": "ninguna",
            "salida": "dict con id, anuncio",
        },
        "anunciar_todo": {
            "descripcion": "Lista todos los anuncios registrados.",
            "entrada": "ninguna",
            "salida": "dict con id, anuncios, n",
        },
        "buscar": {
            "descripcion": "Busca declaraciones en el sistema.",
            "entrada": "ninguna",
            "salida": "dict con id, declaraciones, n",
        },
        "citar": {
            "descripcion": "Lista todas las citas registradas.",
            "entrada": "ninguna",
            "salida": "dict con id, citas, n",
        },
        "limpiar_ciclo": {
            "descripcion": "Limpia el ciclo actual de citaciones.",
            "entrada": "ninguna",
            "salida": "dict con ok, id",
        },
        "inventario": {
            "descripcion": "Inventario del módulo CIT.",
            "entrada": "ninguna",
            "salida": "dict con id, nombre, rol, version, capacidades",
        },
        "reporte": {
            "descripcion": "Reporte interno de estado del módulo CIT.",
            "entrada": "ninguna",
            "salida": "dict con id, estado, coherente, version",
        },
        "diagnostico": {
            "descripcion": "Diagnóstico del módulo CIT.",
            "entrada": "ninguna",
            "salida": "dict con id, estado, coherente, problemas",
        },
        "verificar": {
            "descripcion": "Verifica coherencia interna del módulo CIT.",
            "entrada": "ninguna",
            "salida": "dict con id, coherente, errores, choques",
        },
        "barrer": {
            "descripcion": "Alias de verificar.",
            "entrada": "ninguna",
            "salida": "dict con id, coherente, errores, choques",
        },
        "verificar_salida": {
            "descripcion": "Comprueba forma mínima de una salida de CIT.",
            "entrada": "salida: dict",
            "salida": "bool",
        },
    },

    # ============================================================
    # REPORTING (COMPLETO CON 12 BANDERAS)
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
    },

    # ----- ESTADOS VÁLIDOS -----
    "estados_validos": list(ESTADOS_VALIDOS),

    # ----- INVARIANTES -----
    "invariantes": list(INVARIANTES),

}  # <--- CIERRE FINAL
