# ===============================================================
# VPSI-TRUTH — modules/spartaco_seguridad/__init__.py
# Adaptador: mantiene el catálogo sincronizado con el árbol.
# ===============================================================

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

ID_MODULO = "SC"
NOMBRE_MODULO = "spartaco"
ROL_MODULO = "SC"
VERSION_MODULO = "1.7"
VERSION_CONTRATO = "1.0"
ESQUEMA_CONTRATO = "VPSI-CONTRACT-1.0"
_DIR = Path(__file__).parent


def _sincronizar_arbol() -> Dict[str, Dict[str, Any]]:
    """Carga el árbol y registra recursos con declaración válida."""
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

        # Copia íntegra (incl. conceptos u otras claves del recurso).
        entrada: Dict[str, Any] = {"ruta": rel, "id": oid.strip()}
        for k, v in meta.items():
            if k != "id":
                entrada[k] = v
        reg[rel] = entrada
    return reg


def _particion(
    reg: Dict[str, Dict[str, Any]],
) -> Tuple[Dict[str, Dict[str, Any]], List[str], List[str]]:
    """Separa recursos válidos, errores y choques de id."""
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
    """
    Unión de conceptos declarados por los recursos del árbol.
    Sin vocabulario fijo en el adaptador.
    """
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


def barrer() -> Dict[str, Any]:
    ok, errores, choques = _particion(_sincronizar_arbol())
    return {
        "id": ID_MODULO,
        "coherente": not (errores or choques),
        "errores": errores,
        "choques": choques,
        "recursos": sorted(v["id"] for v in ok.values()),
        "conceptos": _conceptos_descubiertos(ok),
        "total_validos": len(ok),
    }


def verificar() -> Dict[str, Any]:
    return barrer()


def catalogo() -> Dict[str, Any]:
    ok, _, _ = _particion(_sincronizar_arbol())
    return {
        "id": ID_MODULO,
        "n": len(ok),
        "recursos": {
            v["id"]: {k: val for k, val in v.items() if k != "id"}
            for v in ok.values()
        },
        "conceptos": _conceptos_descubiertos(ok),
    }


def inventario(peticion: Any = None) -> Dict[str, Any]:
    ok, errores, choques = _particion(_sincronizar_arbol())
    return {
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "recursos": {
            v["id"]: {k: val for k, val in v.items() if k != "id"}
            for v in ok.values()
        },
        "conceptos": _conceptos_descubiertos(ok),
        "total_validos": len(ok),
        "coherente": not (errores or choques),
    }


def reporte() -> Dict[str, Any]:
    ok, errores, choques = _particion(_sincronizar_arbol())
    coherente = not (errores or choques)
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "version": VERSION_MODULO,
        "estado": "OPERATIVO" if coherente else "DEGRADADO",
        "recursos": sorted(v["id"] for v in ok.values()),
        "conceptos": _conceptos_descubiertos(ok),
        "total_validos": len(ok),
    }


def diagnostico() -> Dict[str, Any]:
    _, errores, choques = _particion(_sincronizar_arbol())
    return {
        "id": ID_MODULO,
        "estado": "OPERATIVO" if not (errores or choques) else "DEGRADADO",
        "problemas": errores + choques,
        "advertencias": [],
    }


def verificar_salida(salida: Any) -> bool:
    return isinstance(salida, dict) and (
        "coherente" in salida or "id" in salida or "recursos" in salida
    )


CONTENEDOR: Dict[str, Any] = {
    "esquema": ESQUEMA_CONTRATO,
    "version_contrato": VERSION_CONTRATO,
    "version_modulo": VERSION_MODULO,
    "estabilidad": "ESTABLE",
    "compatible_desde": "1.0",
    "api_engine": ">=1.0",
    "id": ID_MODULO,
    "nombre": NOMBRE_MODULO,
    "rol": ROL_MODULO,
    "descripcion": (
        "Adaptador del módulo seguridad. "
        "Mantiene sincronizado el catálogo con el estado real del árbol."
    ),
    "funcion": (
        "Mantener sincronizado el catálogo del módulo con el estado "
        "real del árbol de directorios."
    ),
    "no_hace": [
        "No implementa la lógica de los archivos del árbol",
        "No calcula C/L/K/Tru",
        "No orquesta Engine",
        "No define vocabulario fijo de conceptos de seguridad",
    ],
    "autoridad": [
        "Sincronizar el catálogo con el árbol",
        "Exponer recursos y conceptos descubiertos a Engine",
    ],
    "conocimiento_exportable": [
        "inventario", "reporte", "diagnostico", "catalogo", "conceptos",
    ],
    "requiere": [],
    "autoriza_engine": {
        "leer": True, "ejecutar": True, "consultar": True,
        "recombinar": True, "reportar": True, "auditar": True,
        "inventariar": True, "modificar": False,
        "alterar": False, "reescribir": False,
    },
    "consultas_soportadas": [
        "verificar", "barrer", "inventario", "reporte",
        "diagnostico", "catalogo", "verificar_salida",
    ],
    "capacidades": {
        "verificar": verificar,
        "barrer": barrer,
        "inventario": inventario,
        "reporte": reporte,
        "diagnostico": diagnostico,
        "catalogo": catalogo,
        "verificar_salida": verificar_salida,
    },
    "capacidades_meta": {
        "verificar": {
            "descripcion": "Coherencia del catálogo.",
            "entrada": "ninguna",
            "salida": "dict",
        },
        "barrer": {
            "descripcion": "Sincroniza el árbol y reporta coherencia.",
            "entrada": "ninguna",
            "salida": "dict",
        },
        "inventario": {
            "descripcion": "Catálogo sincronizado (recursos + conceptos).",
            "entrada": "opcional",
            "salida": "dict",
        },
        "reporte": {
            "descripcion": "Estado del módulo.",
            "entrada": "ninguna",
            "salida": "dict",
        },
        "diagnostico": {
            "descripcion": "Problemas del catálogo.",
            "entrada": "ninguna",
            "salida": "dict",
        },
        "catalogo": {
            "descripcion": "Recursos y conceptos descubiertos en el árbol.",
            "entrada": "ninguna",
            "salida": "dict",
        },
        "verificar_salida": {
            "descripcion": "Forma mínima.",
            "entrada": "dict",
            "salida": "bool",
        },
    },
    "reporting": {
        "estado": True, "salud": True, "inventario": True,
        "capacidades": True, "errores": True, "advertencias": True,
        "dependencias": True, "version": True, "contrato": True,
        "conocimiento": True, "metricas": True, "diagnostico": True,
    },
    "estados_validos": ["NO_INICIADO", "OPERATIVO", "DEGRADADO", "RECHAZADO"],
    "invariantes": [
        "el id no cambia",
        "este archivo no ejecuta la lógica del árbol",
        "el catálogo refleja el árbol en tiempo de ejecución",
        "los conceptos de seguridad los declaran los recursos, no el adaptador",
    ],
}

__all__ = [
    "CONTENEDOR", "ID_MODULO", "NOMBRE_MODULO", "ROL_MODULO",
    "verificar", "barrer", "inventario", "reporte", "diagnostico",
    "catalogo", "verificar_salida",
]
