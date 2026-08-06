# ===============================================================
# VPSI-TRUTH — modules/constante/__init__.py
# ===============================================================
#
# MÓDULO:              constante
# ID:                  CT
# Rol:                 CT
# Versión módulo:      1.1
# Versión contrato:    1.0
# Esquema contrato:    VPSI-CONTRACT-1.0
# Estabilidad:         ESTABLE
# Compatible desde:    1.0
# API Engine:          >=1.0
#
# Función:
#   Exponer las constantes geométricas fundamentales del marco VPSI
#   derivadas del cubo 3×3×3 en ℝ³.
#
# Qué hace:
#   - Expone ALPHA = 26/27 (techo estructural)
#   - Expone BETA  = 1/27  (piso estructural)
#   - Inventario, reporte y diagnóstico propios
#
# Qué NO hace:
#   - No calcula Tru_total ni Tru_Ri
#   - No clasifica entrada
#   - No orquesta el sistema
#   - No modifica otras constantes ni módulos
#
# Responsabilidad:
#   Ser la fuente oficial e invariante de ALPHA y BETA.
#
# Autoridad:
#   - Exponer ALPHA y BETA
#   - Reportar su propio estado e inventario
#
# Conocimiento exportable:
#   ALPHA, BETA, inventario, estado, reporte, diagnóstico
#
# Relación con Engine:
#   Engine descubre este CONTENEDOR, ejecuta solo las capacidades
#   declaradas y consolida el reporte que este módulo produce.
#
# Relación con Omega:
#   Omega no calcula nada de CT. Solo presenta lo que Engine entrega.
#
# ===============================================================


# ===============================================================
# IMPORTACIONES
# ===============================================================

from __future__ import annotations

from fractions import Fraction
from typing import Any, Dict, Optional

# ===============================================================
# FIN IMPORTACIONES
# ===============================================================


# ===============================================================
# CONSTANTES
# ===============================================================

ID_MODULO = "CT"
NOMBRE_MODULO = "constante"
ROL_MODULO = "CT"

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
    "ALPHA y BETA son invariantes del cubo 3x3x3 en R³",
    "las capacidades declaradas son siempre callables tras la resolución",
    "este módulo no modifica el estado de otros módulos",
)

# Constantes geométricas (derivadas del cubo 3×3×3 en ℝ³)
ALPHA = Fraction(26, 27)  # Techo estructural
BETA = Fraction(1, 27)    # Piso estructural

# ===============================================================
# FIN CONSTANTES
# ===============================================================


# ===============================================================
# CONFIGURACIÓN
# ===============================================================

# (Sin directorios ni archivos externos)

# ===============================================================
# FIN CONFIGURACIÓN
# ===============================================================


# ===============================================================
# DEFINICIONES
# ===============================================================

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
    "descripcion": (
        "Expone las constantes geométricas ALPHA y BETA, derivadas del "
        "cubo 3x3x3 en R³. Estas constantes son invariantes y se usan "
        "en todos los cálculos de verdad del sistema."
    ),

    # ----- PROPÓSITO -----
    "funcion": (
        "Ser la fuente oficial e invariante de ALPHA (26/27) y BETA (1/27)."
    ),
    "no_hace": [
        "No calcula Tru_total ni Tru_Ri",
        "No clasifica entrada de usuario",
        "No orquesta el sistema (eso es Engine)",
        "No modifica otras constantes ni módulos",
    ],

    # ----- AUTORIDAD -----
    "autoridad": [
        "Exponer ALPHA = 26/27",
        "Exponer BETA = 1/27",
        "Reportar inventario, estado y diagnóstico propios",
    ],

    # ----- CONOCIMIENTO EXPORTABLE -----
    "conocimiento_exportable": [
        "ALPHA",
        "BETA",
        "inventario",
        "estado",
        "reporte",
        "diagnostico",
    ],

    # ----- DEPENDENCIAS -----
    "requiere": [],

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
        "obtener_alpha",
        "obtener_beta",
        "obtener_inventario",
        "obtener_reporte",
        "obtener_diagnostico",
        "verificar_coherencia",
    ],

    # ----- CAPACIDADES -----
    "capacidades": {
        "alpha": "get_alpha",
        "beta": "get_beta",
        "inventario": "inventario",
        "reporte": "reporte",
        "diagnostico": "diagnostico",
        "verificar": "verificar",
    },

    # ----- METADATOS DE CAPACIDADES (1:1 obligatorio) -----
    "capacidades_meta": {
        "alpha": {
            "descripcion": "Devuelve la constante ALPHA = 26/27 (techo estructural).",
            "entrada": "peticion opcional (ignorada)",
            "salida": "Fraction(26, 27)",
        },
        "beta": {
            "descripcion": "Devuelve la constante BETA = 1/27 (piso estructural).",
            "entrada": "peticion opcional (ignorada)",
            "salida": "Fraction(1, 27)",
        },
        "inventario": {
            "descripcion": "Inventario de las constantes geométricas del módulo.",
            "entrada": "peticion opcional (ignorada)",
            "salida": "dict con ALPHA, BETA, tipo, origen, id, version",
        },
        "reporte": {
            "descripcion": "Reporte interno de estado del módulo CT.",
            "entrada": "ninguna",
            "salida": "dict con estado, ALPHA, BETA, capacidades",
        },
        "diagnostico": {
            "descripcion": "Diagnóstico: coherencia de ALPHA + BETA == 1.",
            "entrada": "ninguna",
            "salida": "dict con estado, problemas, advertencias, recomendaciones",
        },
        "verificar": {
            "descripcion": "Verifica la invariante ALPHA + BETA == 1.",
            "entrada": "ninguna",
            "salida": "dict con coherente, ALPHA, BETA, suma",
        },
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
# CAPACIDADES PÚBLICAS
# ===============================================================

def get_alpha(peticion=None) -> Fraction:
    """Capacidad alpha: devuelve ALPHA = 26/27."""
    return ALPHA


def get_beta(peticion=None) -> Fraction:
    """Capacidad beta: devuelve BETA = 1/27."""
    return BETA


def inventario(peticion=None) -> Dict[str, Any]:
    """Inventario de las constantes geométricas."""
    return {
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "ALPHA": str(ALPHA),
        "BETA": str(BETA),
        "tipo": "Fraction",
        "origen": "cubo 3x3x3 en R³",
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "invariantes": CONTENEDOR.get("invariantes"),
    }


def verificar() -> Dict[str, Any]:
    """Verifica la invariante ALPHA + BETA == 1."""
    suma = ALPHA + BETA
    coherente = suma == Fraction(1)
    return {
        "coherente": coherente,
        "ALPHA": str(ALPHA),
        "BETA": str(BETA),
        "suma": str(suma),
        "invariante": "ALPHA + BETA == 1",
    }

# ===============================================================
# FIN CAPACIDADES PÚBLICAS
# ===============================================================


# ===============================================================
# REPORTING INTERNO
# ===============================================================

def reporte() -> Dict[str, Any]:
    """Reporte interno del módulo. Solo informa estado propio."""
    v = verificar()
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "estado": ESTADO_OPERATIVO if v["coherente"] else ESTADO_DEGRADADO,
        "coherente": v["coherente"],
        "ALPHA": str(ALPHA),
        "BETA": str(BETA),
        "suma": v["suma"],
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "autoridad": CONTENEDOR.get("autoridad"),
        "conocimiento_exportable": CONTENEDOR.get("conocimiento_exportable"),
        "consultas_soportadas": CONTENEDOR.get("consultas_soportadas"),
    }


def diagnostico() -> Dict[str, Any]:
    """Diagnóstico: coherencia de ALPHA + BETA == 1."""
    v = verificar()
    problemas = []
    advertencias = []
    recomendaciones = []

    if not v["coherente"]:
        problemas.append({
            "tipo": "invariante_rota",
            "detalle": f"ALPHA + BETA = {v['suma']} != 1",
        })
        recomendaciones.append("Verificar definición de ALPHA y BETA")

    estado = ESTADO_OPERATIVO if v["coherente"] else ESTADO_DEGRADADO

    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "estado": estado,
        "problemas": problemas,
        "advertencias": advertencias,
        "recomendaciones": recomendaciones,
        "coherente": v["coherente"],
        "ALPHA": str(ALPHA),
        "BETA": str(BETA),
        "suma": v["suma"],
    }

# ===============================================================
# FIN REPORTING
# ===============================================================


# ===============================================================
# VERIFICACIÓN
# ===============================================================

# verificar() en CAPACIDADES PÚBLICAS

# ===============================================================
# FIN VERIFICACIÓN
# ===============================================================


# ===============================================================
# INVENTARIO
# ===============================================================

# inventario() en CAPACIDADES PÚBLICAS

# ===============================================================
# FIN INVENTARIO
# ===============================================================


# ===============================================================
# EXPORTACIONES + RESOLUCIÓN ESTRICTA
# ===============================================================

_CAP_MAP = {
    "get_alpha": get_alpha,
    "get_beta": get_beta,
    "inventario": inventario,
    "reporte": reporte,
    "diagnostico": diagnostico,
    "verificar": verificar,
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
    "ALPHA",
    "BETA",
    "get_alpha",
    "get_beta",
    "inventario",
    "verificar",
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
# Toda capacidad nueva DEBE agregarse simultáneamente en:
#   1. capacidades
#   2. capacidades_meta  (descripcion, entrada, salida: str)
#   3. _CAP_MAP
#   4. VERSION_MODULO
#
# ===============================================================
# FIN EXTENSIONES FUTURAS
# ===============================================================


# ===============================================================
# FIN DEL MÓDULO
# ===============================================================
