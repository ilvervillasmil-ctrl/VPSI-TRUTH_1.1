# ===============================================================
# VPSI-TRUTH — observador_estructural/__init__.py
# ===============================================================
#
# MÓDULO:              observador-estructural
# ID:                  OBS-ESTRUCTURAL
# Rol:                 observador
# Versión módulo:      1.0
# Versión contrato:    >=1.0
# Esquema contrato:    VPSI-CONTRACT-1.0
# Estabilidad:         ESTABLE
# Compatible desde:   19
# API Engine:          >=1.0
#
# Función:
#   observar la estructura real del módulo y su contrato.
#
# Qué hace:
#   inspecciona archivos descubiertos por Engine.
#   identifica la estructura física disponible.
#   verifica la estructura declarada por su propio contrato.
#
# Qué NO hace:
#   no modifica archivos.
#   no crea archivos.
#   no inventa capacidades.
#   no altera contratos externos.
#
# ===============================================================

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List


# ===============================================================
# IDENTIDAD
# ===============================================================

ID_MODULO = "OBS-ESTRUCTURAL"
NOMBRE_MODULO = "observador-estructural"
ROL_MODULO = "observador"

VERSION_MODULO = "1.0"
VERSION_CONTRATO = ">=1.0"

ESQUEMA_CONTRATO = "VPSI-CONTRACT-1.0"

ESTABILIDAD = "ESTABLE"
COMPATIBLE_DESDE = "19"
API_ENGINE = ">=1.0"


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
    "el id del módulo nunca cambia",
    "el nombre del módulo nunca cambia",
    "el rol del módulo nunca cambia",
)


# ===============================================================
# CONTEXTO INYECTADO POR ENGINE
# ===============================================================

ARCHIVOS_PY: List[Path] = []


# ===============================================================
# CAPACIDAD: INVENTARIO
# ===============================================================

def inventario() -> Dict[str, Any]:
    """
    Observa los archivos Python que Engine descubrió
    físicamente dentro de este módulo.

    La información procede del repositorio real.
    """

    archivos = []

    for ruta in ARCHIVOS_PY:

        path = Path(ruta)

        archivos.append({
            "nombre": path.name,
            "ruta": str(path),
            "existe": path.is_file(),
            "tipo": path.suffix,
        })

    return {
        "modulo": NOMBRE_MODULO,
        "id": ID_MODULO,
        "total_archivos": len(archivos),
        "archivos": archivos,
    }


# ===============================================================
# CAPACIDAD: DIAGNÓSTICO
# ===============================================================

def diagnostico() -> Dict[str, Any]:
    """
    Determina si la estructura física descubierta
    por Engine es consistente.
    """

    archivos = [
        Path(ruta)
        for ruta in ARCHIVOS_PY
    ]

    inexistentes = [
        str(ruta)
        for ruta in archivos
        if not ruta.is_file()
    ]

    tiene_init = any(
        ruta.name == "__init__.py"
        for ruta in archivos
    )

    if inexistentes:
        estado = "DEGRADADO"

    elif not tiene_init:
        estado = "DEGRADADO"

    else:
        estado = "OPERATIVO"

    return {
        "estado": estado,
        "modulo": NOMBRE_MODULO,
        "archivos_descubiertos": len(archivos),
        "archivos_inexistentes": inexistentes,
        "contiene_init": tiene_init,
    }


# ===============================================================
# CAPACIDAD META: VALIDAR ESQUEMA
# ===============================================================

def validar_esquema() -> Dict[str, Any]:
    """
    Verifica la estructura del contrato que este módulo
    realmente expone al Engine.

    No reemplaza la validación del Engine.
    Es una capacidad propia del módulo.
    """

    contrato = CONTENEDOR

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
        "acceso_archivos",
        "api_engine",
        "validar_esquema",
    )

    faltantes = [
        clave
        for clave in obligatorias
        if clave not in contrato
    ]

    capacidades = contrato.get("capacidades", {})
    capacidades_meta = contrato.get("capacidades_meta", {})

    capacidades_sin_meta = [
        clave
        for clave in capacidades
        if clave not in capacidades_meta
    ]

    no_callable = [
        clave
        for clave, funcion in capacidades.items()
        if not callable(funcion)
    ]

    coherente = (
        not faltantes
        and not capacidades_sin_meta
        and not no_callable
    )

    return {
        "coherente": coherente,
        "faltantes": faltantes,
        "capacidades_sin_meta": capacidades_sin_meta,
        "capacidades_no_callable": no_callable,
        "capacidades": list(capacidades.keys()),
    }


# ===============================================================
# CONTRATO OFICIAL
# ===============================================================

CONTENEDOR: Dict[str, Any] = {

    # -----------------------------------------------------------
    # IDENTIDAD CONTRACTUAL
    # -----------------------------------------------------------

    "esquema": ESQUEMA_CONTRATO,

    "version_contrato": VERSION_CONTRATO,

    "version_modulo": VERSION_MODULO,

    "id": ID_MODULO,

    "nombre": NOMBRE_MODULO,

    "rol": ROL_MODULO,

    "descripcion":
        "Observa la estructura física y contractual "
        "del módulo dentro del repositorio.",

    "funcion":
        "observar estructura real y coherencia contractual.",


    # -----------------------------------------------------------
    # LÍMITES
    # -----------------------------------------------------------

    "no_hace": [
        "no modifica archivos",
        "no crea archivos",
        "no modifica contratos",
        "no inventa capacidades",
        "no altera módulos externos",
    ],


    # -----------------------------------------------------------
    # AUTORIDAD
    # -----------------------------------------------------------

    "autoridad": [
        "observar archivos descubiertos",
        "diagnosticar estructura física",
        "validar su propia estructura contractual",
    ],


    # -----------------------------------------------------------
    # CONOCIMIENTO EXPORTABLE
    # -----------------------------------------------------------

    "conocimiento_exportable": [
        "inventario estructural",
        "diagnóstico estructural",
        "coherencia contractual",
    ],


    # -----------------------------------------------------------
    # DEPENDENCIAS
    # -----------------------------------------------------------

    "requiere": [],


    # -----------------------------------------------------------
    # AUTORIZACIÓN DEL ENGINE
    # -----------------------------------------------------------

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
        "acceso_archivos": True,
    },


    # -----------------------------------------------------------
    # CONSULTAS
    # -----------------------------------------------------------

    "consultas_soportadas": [
        "inventario",
        "diagnostico",
        "validar_esquema",
    ],


    # -----------------------------------------------------------
    # CAPACIDADES REALES
    # -----------------------------------------------------------

    "capacidades": {
        "inventario": inventario,
        "diagnostico": diagnostico,
        "validar_esquema": validar_esquema,
    },


    # -----------------------------------------------------------
    # META-CONTRATO DE LAS CAPACIDADES
    # -----------------------------------------------------------

    "capacidades_meta": {

        "inventario": {
            "descripcion":
                "Inspecciona los archivos Python descubiertos.",
            "entrada":
                "contexto ARCHIVOS_PY proporcionado por Engine",
            "validar_esquema":
                "requiere contexto estructural disponible",
            "salida":
                "inventario estructural",
            "acceso_archivos":
                "lectura",
        },

        "diagnostico": {
            "descripcion":
                "Determina el estado de la estructura física.",
            "entrada":
                "contexto ARCHIVOS_PY proporcionado por Engine",
            "validar_esquema":
                "requiere contexto estructural disponible",
            "salida":
                "diagnóstico estructural",
            "acceso_archivos":
                "lectura",
        },

        "validar_esquema": {
            "descripcion":
                "Valida la coherencia estructural del contrato.",
            "entrada":
                "contrato CONTENEDOR del módulo",
            "validar_esquema":
                "requiere contrato dict",
            "salida":
                "resultado de coherencia contractual",
            "acceso_archivos":
                "no requiere acceso",
        },
    },


    # -----------------------------------------------------------
    # REPORTING
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
    },


    # -----------------------------------------------------------
    # ESTADOS
    # -----------------------------------------------------------

    "estados_validos": list(ESTADOS_VALIDOS),


    # -----------------------------------------------------------
    # INVARIANTES
    # -----------------------------------------------------------

    "invariantes": list(INVARIANTES),


    # -----------------------------------------------------------
    # COMPATIBILIDAD
    # -----------------------------------------------------------

    "estabilidad": ESTABILIDAD,

    "compatible_desde": COMPATIBLE_DESDE,

    "api_engine": API_ENGINE,


    # -----------------------------------------------------------
    # ACCESO A ARCHIVOS
    # -----------------------------------------------------------

    "acceso_archivos": [
        "lectura",
        "inspeccion",
        "sin modificación",
    ],


    # -----------------------------------------------------------
    # VALIDACIÓN CONTRACTUAL DECLARADA
    # -----------------------------------------------------------

    "validar_esquema": [
        "validar claves obligatorias",
        "validar capacidades",
        "validar capacidades_meta",
        "validar coherencia estructural",
    ],
}


# ===============================================================
# FIN DEL MÓDULO
# ===============================================================
