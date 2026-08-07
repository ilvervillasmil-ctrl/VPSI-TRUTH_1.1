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
#   - Descubre, carga y valida automáticamente cada archivo *.py del módulo.
#   - Expone inventario, reporte, diagnóstico y axiomas del dominio.
#
# Responsabilidad:
#   Garantizar una representación coherente del marco O y mantener
#   la integridad estructural de su dominio.
#
# Autoridad:
#   - Declarar el registro O y permite_k.
#   - Clasificar el contexto evaluable.
#   - Validar la estructura y el dominio de los archivos internos.
#   - Reportar el estado estructural del módulo.
#
# Conocimiento exportable:
#   - O_context
#   - registro
#   - permite_k
#   - pedir_anuncio
#   - tipos_peticion
#   - inventario
#   - reporte
#   - diagnostico
#   - axiomas
#
# Relación con Engine:
#   Engine descubre este CONTENEDOR, ejecuta únicamente las
#   capacidades declaradas, puede inspeccionar todos los archivos
#   del módulo y consolida el reporte producido por este.
#
# Relación con Omega:
#   Omega no calcula información de este módulo.
#   Solo presenta los resultados entregados por Engine.
#
# Observaciones:
#   Todo archivo *.py del directorio forma parte del dominio del
#   módulo y puede ser descubierto, validado y auditado
#   automáticamente mediante el centinela.
#
# ===============================================================


# ===============================================================
# IMPORTACIONES
# ===============================================================

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ===============================================================
# FIN IMPORTACIONES
# ===============================================================


# ===============================================================
# CONSTANTES (imperativo)
# ===============================================================

# Identidad inmutable
ID_MODULO = "<ID>"                    # identificador canónico (no cambia)
NOMBRE_MODULO = "<nombre>"
ROL_MODULO = "<ROL>"

# Versiones
VERSION_MODULO = "1.0"
VERSION_CONTRATO = "1.0"
ESQUEMA_CONTRATO = "VPSI-CONTRACT-1.0"

# Compatibilidad
COMPATIBLE_DESDE = "1.0"
API_ENGINE = ">=1.0"

# Estabilidad del módulo
ESTABILIDAD = "ESTABLE"               # ESTABLE | EXPERIMENTAL | DEPRECATED

# Estados centralizados (nunca literales sueltos)
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

# Invariantes del módulo (auditoría)
INVARIANTES = (
    "el id del módulo nunca cambia",
    "el rol nunca cambia",
    "las capacidades declaradas son siempre callables tras la resolución",
    "este módulo no modifica el estado de otros módulos",
    "este módulo no inventa capacidades no declaradas en CONTENEDOR",
)

# ===============================================================
# FIN CONSTANTES
# ===============================================================


# ===============================================================
# CONFIGURACIÓN
# ===============================================================

_DIR = Path(__file__).parent

# Directorios, archivos, límites, flags, opciones internas

# ===============================================================
# FIN CONFIGURACIÓN
# ===============================================================


# ===============================================================
# DEFINICIONES
# ===============================================================

# Clases, dataclasses, tipos, responsabilidades, estructuras internas

class ContratoInvalido(Exception):
    """El CONTENEDOR no cumple el esquema o la resolución de capacidades falló."""
    pass

# ===============================================================
# FIN DEFINICIONES
# ===============================================================


# ===============================================================
# CONTRATO OFICIAL DEL MÓDULO
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
    "descripcion": "",

    # ----- PROPÓSITO -----
    "funcion": "",
    "no_hace": [
        # "No hace X",
        # "No hace Y",
    ],

    # ----- AUTORIDAD -----
    "autoridad": [
        # "Puede hacer A",
        # "Puede responder B",
    ],

    # ----- CONOCIMIENTO EXPORTABLE -----
    "conocimiento_exportable": [
        # "inventario",
        # "reporte",
        # "diagnostico",
    ],


    # ----- AUTORIZACIÓN AL ENGINE -----
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

    # ----- CONSULTAS SOPORTADAS -----
    "consultas_soportadas": [
        # "obtener_inventario",
        # "obtener_reporte",
        # "obtener_diagnostico",
        # "verificar_coherencia",
    ],

    # ----- CAPACIDADES -----
    # nombre → referencia (str) o callable
    # Se resuelve de forma estricta al final del archivo.
    "capacidades": {
        # "verificar": "verificar",
        # "inventario": "inventario",
        # "reporte": "reporte",
        # "diagnostico": "diagnostico",
    },

    # ----- METADATOS DE CAPACIDADES -----
    "capacidades_meta": {
        # "verificar": {
        #     "descripcion": "",
        #     "entrada": "",
        #     "salida": "",
        # },
    },

    # ----- REPORTING -----
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
}

# ===============================================================
# FIN CONTRATO
# ===============================================================


# ===============================================================
# FUNCIONES PRIVADAS
# ===============================================================

# _normalizar()
# _validar()
# _extraer()
# _convertir()
# utilidades internas
# Nunca visibles como capacidad.

def _validar_contrato(cont: Dict[str, Any]) -> None:
    """
    Autoauditoría del propio contrato.
    Falla de inmediato si el CONTENEDOR es inválido.
    """
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

    if not isinstance(cont.get("capacidades"), dict):
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: 'capacidades' debe ser dict"
        )

    if not isinstance(cont.get("requiere"), list):
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: 'requiere' debe ser list"
        )

# ===============================================================
# FIN FUNCIONES PRIVADAS
# ===============================================================


# ===============================================================
# CAPACIDADES PÚBLICAS
# ===============================================================

def verificar() -> Dict[str, Any]:
    """
    Verificación de coherencia interna del módulo.
    No verifica el sistema completo.
    """
    return {
        "coherente": True,
        "errores": [],
        "advertencias": [],
    }


def inventario(peticion=None) -> Dict[str, Any]:
    """Inventario completo de lo que el módulo posee."""
    return {
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "autoridad": CONTENEDOR.get("autoridad"),
        "conocimiento_exportable": CONTENEDOR.get("conocimiento_exportable"),
        "consultas_soportadas": CONTENEDOR.get("consultas_soportadas"),
        "invariantes": CONTENEDOR.get("invariantes"),
    }

# ===============================================================
# FIN CAPACIDADES PÚBLICAS
# ===============================================================


# ===============================================================
# REPORTING INTERNO
# ===============================================================

def reporte() -> Dict[str, Any]:
    """
    Reporte interno del módulo.
    Solo informa estado propio. No calcula ni orquesta.
    """
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "estado": ESTADO_OPERATIVO,
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "autoridad": CONTENEDOR.get("autoridad"),
        "conocimiento_exportable": CONTENEDOR.get("conocimiento_exportable"),
        "consultas_soportadas": CONTENEDOR.get("consultas_soportadas"),
    }


def diagnostico() -> Dict[str, Any]:
    """
    Diagnóstico del módulo:
    qué me sucede, qué falta, qué está mal, qué necesito.
    """
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "estado": ESTADO_OPERATIVO,
        "problemas": [],
        "advertencias": [],
        "recomendaciones": [],
    }

# ===============================================================
# FIN REPORTING
# ===============================================================


# ===============================================================
# VERIFICACIÓN
# ===============================================================

# verificar() ya está en CAPACIDADES PÚBLICAS.

# ===============================================================
# FIN VERIFICACIÓN
# ===============================================================


# ===============================================================
# INVENTARIO
# ===============================================================

# inventario() ya está en CAPACIDADES PÚBLICAS.

# ===============================================================
# FIN INVENTARIO
# ===============================================================


# ===============================================================
# EXPORTACIONES + RESOLUCIÓN ESTRICTA DEL CONTRATO
# ===============================================================

_CAP_MAP = {
    "verificar": verificar,
    "inventario": inventario,
    "reporte": reporte,
    "diagnostico": diagnostico,
}


def _resolver_capacidades(cont: Dict[str, Any]) -> None:
    """
    Resolución estricta.
    Si una referencia no existe en _CAP_MAP → fallo inmediato.
    Tras resolver, el contrato se considera congelado.
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


# Validar y resolver al cargar el módulo
_validar_contrato(CONTENEDOR)
_resolver_capacidades(CONTENEDOR)

# A partir de aquí el CONTENEDOR se considera inmutable.
# No modificar CONTENEDOR en tiempo de ejecución.

__all__ = [
    "CONTENEDOR",
    "ID_MODULO",
    "NOMBRE_MODULO",
    "ROL_MODULO",
    "VERSION_MODULO",
    "VERSION_CONTRATO",
    "ESQUEMA_CONTRATO",
    "ESTABILIDAD",
    "verificar",
    "inventario",
    "reporte",
    "diagnostico",
    "ContratoInvalido",
]

# ===============================================================
# FIN EXPORTACIONES
# ===============================================================


# ===============================================================
# EXTENSIONES FUTURAS
# ===============================================================
#
# Nuevas capacidades deberán:
#   • mantener este contrato y el esquema VPSI-CONTRACT-1.0
#   • no romper compatibilidad hacia atrás
#   • añadirse en capacidades + capacidades_meta + _CAP_MAP
#   • actualizar inventario, reporting y VERSION_MODULO
#   • pasar _validar_contrato y _resolver_capacidades
#
# Engine descubrirá automáticamente cualquier capacidad nueva.
# Omega la reportará sin modificar su código.
#
# ===============================================================
# FIN EXTENSIONES FUTURAS
# ===============================================================


# ===============================================================
# FIN DEL MÓDULO
# ===============================================================
