# ===============================================================
# VPSI-TRUTH — modules/spartaco_seguridad/__init__.py
# ===============================================================
#
# MÓDULO:              spartaco_seguridad
# ID:                  SC
# Rol:                 SC
# Versión módulo:      1.7
# Versión contrato:    1.0
# Esquema contrato:    VPSI-CONTRACT-1.0
# Estabilidad:         ESTABLE
# Compatible desde:    1.0
# API Engine:          >=1.0
#
# Función:
#   Mantener sincronizado el catálogo del módulo con el estado
#   real del árbol de directorios.
#
# Qué hace:
#   - Recorre recursivamente el árbol del módulo.
#   - Descubre y carga cada *.py válido con declaración SEGURIDAD.
#   - Registra recursos y conceptos declarados por esos archivos.
#   - Expone inventario, reporte, diagnóstico y catálogo.
#
# Responsabilidad:
#   Adaptador entre el árbol de archivos y el Engine.
#   No implementa la lógica de protección: la declaran los recursos.
#
# Autoridad:
#   - Sincronizar el catálogo con el árbol.
#   - Exponer recursos y conceptos descubiertos.
#   - Reportar el estado estructural del módulo.
#
# Conocimiento exportable:
#   - inventario
#   - reporte
#   - diagnostico
#   - catalogo
#   - conceptos
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
#   Todo archivo *.py del directorio (excepto __init__ y _*)
#   que declare SEGURIDAD forma parte del dominio y se incorpora
#   automáticamente. El adaptador no conoce de antemano los recursos.
#
# ===============================================================

# ===============================================================
# IMPORTACIONES
# ===============================================================

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ===============================================================
# FIN IMPORTACIONES
# ===============================================================

# ===============================================================
# CONSTANTES
# ===============================================================

ID_MODULO = "SC"
NOMBRE_MODULO = "spartaco_seguridad"
ROL_MODULO = "SC"

VERSION_MODULO = "1.7"
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
    "este módulo no inventa capacidades no declaradas en CONTENEDOR",
    "este archivo no ejecuta la lógica del árbol",
    "el catálogo refleja el árbol en tiempo de ejecución",
    "los conceptos de seguridad los declaran los recursos, no el adaptador",
)

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

# ===============================================================
# FIN DEFINICIONES
# ===============================================================

# ===============================================================
# FUNCIONES PRIVADAS — descubrimiento del árbol
# ===============================================================

def _sincronizar_arbol() -> Dict[str, Dict[str, Any]]:
    reg: Dict[str, Dict[str, Any]] = {}
    for path in sorted(_DIR.rglob("*.py")):
        if path.name.startswith("_") or path.name == "__init__.py":
            continue
        try:
            rel = str(path.relative_to(_DIR))
        except ValueError:
            rel = path.name
        clave = "sc_" + rel.replace("/", "_").replace("\\", "_").replace(".", "_")
        if clave.endswith("_py"):
            clave = clave[:-3]
        try:
            spec = importlib.util.spec_from_file_location(clave, str(path))
            if spec is None or spec.loader is None:
                continue
            mod = importlib.util.module_from_spec(spec)
            sys.modules[clave] = mod
            spec.loader.exec_module(mod)
        except Exception as e:
            reg[rel] = {"ruta": rel, "error": f"{type(e).__name__}: {e}"}
            continue

        meta = getattr(mod, "SEGURIDAD", None)
        if not isinstance(meta, dict):
            continue
        oid = meta.get("id")
        if not isinstance(oid, str) or not oid.strip():
            reg[rel] = {"ruta": rel, "error": "declaración sin id válido"}
            continue

        entrada: Dict[str, Any] = {"ruta": rel, "id": oid.strip()}
        for k, v in meta.items():
            if k != "id":
                entrada[k] = v
        reg[rel] = entrada
    return reg


def _particion(
    reg: Dict[str, Dict[str, Any]],
) -> Tuple[Dict[str, Dict[str, Any]], List[str], List[str]]:
    ok: Dict[str, Dict[str, Any]] = {}
    errores: List[str] = []
    por_id: Dict[str, List[str]] = {}
    for k, v in reg.items():
        if "error" in v:
            errores.append(f"{k}: {v['error']}")
            continue
        ok[k] = v
        por_id.setdefault(str(v["id"]), []).append(k)
    choques = [f"id '{i}' en {rs}" for i, rs in por_id.items() if len(rs) > 1]
    return ok, errores, choques


def _conceptos_descubiertos(ok: Dict[str, Dict[str, Any]]) -> List[str]:
    hallados = set()
    for meta in ok.values():
        raw = meta.get("conceptos")
        if isinstance(raw, (list, tuple, set)):
            for c in raw:
                if isinstance(c, str) and c.strip():
                    hallados.add(c.strip())
        elif isinstance(raw, str) and raw.strip():
            hallados.add(raw.strip())
    return sorted(hallados)

# ===============================================================
# FIN FUNCIONES PRIVADAS — descubrimiento
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
        "Adaptador Spartaco (SC). Mantiene sincronizado el catálogo "
        "con el estado real del árbol de directorios."
    ),

    # ============================================================
    # PROPÓSITO
    # ============================================================
    "funcion": (
        "Mantener sincronizado el catálogo del módulo con el estado "
        "real del árbol de directorios."
    ),
    "no_hace": [
        "No implementa la lógica de los archivos del árbol",
        "No calcula C/L/K/Tru",
        "No orquesta ciclos",
        "No define vocabulario fijo de conceptos de seguridad",
    ],

    # ============================================================
    # AUTORIDAD
    # ============================================================
    "autoridad": [
        "Sincronizar el catálogo con el árbol",
        "Exponer recursos y conceptos descubiertos",
        "Reportar el estado estructural del módulo",
    ],

    # ============================================================
    # CONOCIMIENTO EXPORTABLE
    # ============================================================
    "conocimiento_exportable": [
        "inventario",
        "reporte",
        "diagnostico",
        "catalogo",
        "conceptos",
    ],

    # ============================================================
    # ACCESO (obligatorio en el esquema)
    # ============================================================
    "acceso": {
        "nivel": "completo",
        "descripcion": "Acceso total a recursos del módulo"
    
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
        "validar_esquema": True,     # ← AGREGADO
        "acceso_archivos": True,     # ← AGREGADO
    },

    # ============================================================
    # CAPACIDADES
    # ============================================================
    "capacidades": {
        "verificar": "verificar",
        "barrer": "barrer",
        "inventario": "inventario",
        "reporte": "reporte",
        "diagnostico": "diagnostico",
        "catalogo": "catalogo",
        "verificar_salida": "verificar_salida",
    },

    # ============================================================
    # METADATOS DE CAPACIDADES (1:1 OBLIGATORIO)
    # ============================================================
    "capacidades_meta": {
        "verificar": {
            "descripcion": "Garantiza la coherencia del catálogo sincronizado.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con coherente, errores, choques, recursos",
            "acceso_archivos": ["*"],
        },

        "barrer": {
            "descripcion": "Sincroniza el árbol y reporta coherencia.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con coherente, recursos, conceptos",
            "acceso_archivos": ["*"],
        },

        "inventario": {
            "descripcion": "Garantiza la enumeración de recursos y conceptos.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con id, version, recursos, conceptos",
            "acceso_archivos": ["*"],
        },

        "reporte": {
            "descripcion": "Garantiza el estado actual del módulo.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con estado, version, recursos",
            "acceso_archivos": ["*"],
        },

        "diagnostico": {
            "descripcion": "Garantiza problemas y advertencias del catálogo.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con estado, problemas, advertencias",
            "acceso_archivos": ["*"],
        },

        "catalogo": {
            "descripcion": "Recursos y conceptos descubiertos en el árbol.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con n, recursos, conceptos",
            "acceso_archivos": ["*"],
        },

        "verificar_salida": {
            "descripcion": "Forma mínima de una salida del módulo.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "bool",
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
# FUNCIONES PRIVADAS — validación de contrato
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
    meta_caps = cont.get("capacidades_meta") or {}
    if not isinstance(meta_caps, dict):
        raise ContratoInvalido(
            "{0}: 'capacidades_meta' debe ser dict".format(NOMBRE_MODULO)
        )
    for nombre_cap in cont["capacidades"]:
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
# FIN FUNCIONES PRIVADAS — validación
# ===============================================================

# ===============================================================
# CAPACIDADES PÚBLICAS
# ===============================================================

def barrer() -> Dict[str, Any]:
    ok, errores, choques = _particion(_sincronizar_arbol())
    return {
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "coherente": not (errores or choques),
        "errores": errores,
        "choques": choques,
        "recursos": sorted(v["id"] for v in ok.values()),
        "conceptos": _conceptos_descubiertos(ok),
        "total_validos": len(ok),
        "archivos": sorted(ok.keys()),
    }


def verificar(peticion: Any = None) -> Dict[str, Any]:
    return barrer()


def inventario(peticion: Any = None) -> Dict[str, Any]:
    ok, errores, choques = _particion(_sincronizar_arbol())
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
        "recursos": {
            v["id"]: {k: val for k, val in v.items() if k != "id"}
            for v in ok.values()
        },
        "conceptos": _conceptos_descubiertos(ok),
        "total_validos": len(ok),
        "archivos": sorted(ok.keys()),
        "coherente": not (errores or choques),
    }


def catalogo() -> Dict[str, Any]:
    ok, _, _ = _particion(_sincronizar_arbol())
    return {
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "n": len(ok),
        "recursos": {
            v["id"]: {k: val for k, val in v.items() if k != "id"}
            for v in ok.values()
        },
        "conceptos": _conceptos_descubiertos(ok),
    }


def reporte() -> Dict[str, Any]:
    ok, errores, choques = _particion(_sincronizar_arbol())
    coherente = not (errores or choques)
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "nombre": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "estado": ESTADO_OPERATIVO if coherente else ESTADO_DEGRADADO,
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "recursos": sorted(v["id"] for v in ok.values()),
        "conceptos": _conceptos_descubiertos(ok),
        "total_validos": len(ok),
        "errores": errores,
        "choques": choques,
    }


def diagnostico() -> Dict[str, Any]:
    _, errores, choques = _particion(_sincronizar_arbol())
    limpio = not (errores or choques)
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "estado": ESTADO_OPERATIVO if limpio else ESTADO_DEGRADADO,
        "problemas": errores + choques,
        "advertencias": [],
        "recomendaciones": [],
        "salud": limpio,
    }


def verificar_salida(salida: Any) -> bool:
    return isinstance(salida, dict) and (
        "coherente" in salida or "id" in salida or "recursos" in salida
    )

# ===============================================================
# FIN CAPACIDADES PÚBLICAS
# ===============================================================

# ===============================================================
# EXPORTACIONES + RESOLUCIÓN ESTRICTA DEL CONTRATO
# ===============================================================

_CAP_MAP = {
    "verificar": verificar,
    "barrer": barrer,
    "inventario": inventario,
    "reporte": reporte,
    "diagnostico": diagnostico,
    "catalogo": catalogo,
    "verificar_salida": verificar_salida,
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
    "verificar",
    "barrer",
    "inventario",
    "reporte",
    "diagnostico",
    "catalogo",
    "verificar_salida",
    "ContratoInvalido",
]

# ===============================================================
# FIN DEL MÓDULO
# ===============================================================
