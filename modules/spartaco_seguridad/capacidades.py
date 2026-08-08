# ===============================================================
# VPSI-TRUTH — modules/spartaco_seguridad/capacidades.py
# ===============================================================
#
# RECURSO:             CAPACIDADES
# Módulo contenedor:   spartaco_seguridad (SC)
# Versión recurso:     1.0
#
# Función:
#   Reportar, por cada recurso descubierto en el árbol del
#   módulo, las capacidades que ese recurso declara y el estado
#   estructural de cada una.
#
# Qué hace:
#   - Recorre el árbol con el mismo criterio que el adaptador.
#   - Por cada recurso, lee su declaración de capacidades.
#   - Para cada capacidad declarada comprueba existencia y
#     callabilidad en el módulo real.
#   - Produce reporte por recurso, por capacidad y total.
#
# Qué NO hace:
#   - No infiere capacidades (ni de dir(), ni de __all__).
#   - No invoca ninguna capacidad auditada.
#   - No modifica ningún recurso ni el adaptador.
#   - No convierte ausencia de declaración en error.
#   - No obliga a ningún recurso a declarar.
#
# ---------------------------------------------------------------
# CONTRATO DE DECLARACIÓN
# ---------------------------------------------------------------
#   Un recurso que quiera ser auditado declara en su SEGURIDAD:
#
#       "capacidades_recurso": ["nucleo", "canales", "build", ...]
#
#   La clave es "capacidades_recurso" y NO "capacidades", para no
#   colisionar con CONTENEDOR["capacidades"] del adaptador, que
#   tiene significado propio y lo resuelve el Engine. Son capas
#   distintas y se auditan por separado.
#
#   Un recurso que no la declare produce SIN_DECLARAR. Eso NO es
#   error: es ausencia de declaración.
#
# ---------------------------------------------------------------
# QUÉ DEMUESTRA CADA COLUMNA
# ---------------------------------------------------------------
#       declarado  → el recurso lo dice en su SEGURIDAD
#       existe     → hasattr(modulo, nombre)
#       callable   → callable(getattr(modulo, nombre))
#       funciona   → NO SE DETERMINA AQUÍ
#
#   El campo "ok" de este recurso es ESTRUCTURAL, no funcional.
#   Significa: declarado, existe y es callable. No significa que
#   la capacidad funcione. Eso lo demuestra el pipeline de tests,
#   que sí ejecuta con argumentos válidos.
#
# ---------------------------------------------------------------
# CRECIMIENTO DEL ÁRBOL
# ---------------------------------------------------------------
#   Este archivo no conoce anticipadamente ningún recurso. Al
#   añadir un archivo nuevo con SEGURIDAD y su declaración de
#   capacidades, el adaptador lo descubre y este reporte lo
#   incorpora. No hay que modificar este archivo, ni el adaptador,
#   ni el Engine.
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
# DECLARACIÓN — la lee el adaptador SC
# ===============================================================

SEGURIDAD: Dict[str, Any] = {
    "id": "CAPACIDADES",
    "nombre": "capacidades",
    "hace": (
        "Reporta las capacidades declaradas por cada recurso del árbol "
        "y el estado estructural de cada una: existe y es callable. "
        "No las ejecuta."
    ),
    "herramienta": (
        "Introspección hasattr + callable sobre los recursos descubiertos"
    ),
    "version": "1.0",
    "clave_declaracion": "capacidades_recurso",
    "capacidades_recurso": [
        "auditar",
        "capacidades_de",
        "resumen",
        "tabla",
    ],
    "conceptos": [
        "CÓDIGO_INVÁLIDO",
    ],
    "no_hace": [
        "No ejecuta capacidades auditadas",
        "No infiere capacidades de dir() ni de __all__",
        "No modifica recursos, adaptador ni Engine",
        "No convierte ausencia de declaración en error",
    ],
}

# ===============================================================
# FIN DECLARACIÓN
# ===============================================================

# ===============================================================
# CONSTANTES
# ===============================================================

_DIR = Path(__file__).parent

CLAVE_DECLARACION = "capacidades_recurso"

# Prefijo con el que el adaptador registra los módulos del árbol.
PREFIJO_ADAPTADOR = "sc_"

# --- estado por capacidad ---
OK = "OK"
AUSENTE = "AUSENTE_EN_MODULO"
NO_CALLABLE = "NO_CALLABLE"
NOMBRE_INVALIDO = "NOMBRE_INVALIDO"

# --- estado por recurso ---
OPERATIVO = "OPERATIVO"
DEGRADADO = "DEGRADADO"
SIN_DECLARAR = "SIN_DECLARAR"
ID_AUSENTE = "ID_AUSENTE"
ID_DUPLICADO = "ID_DUPLICADO"
NO_CARGABLE = "NO_CARGABLE"

# --- procedencia de la instancia inspeccionada ---
YA_CARGADO = "YA_CARGADO"
CARGADO_AQUI = "CARGADO_AQUI"

# ===============================================================
# FIN CONSTANTES
# ===============================================================

# ===============================================================
# FUNCIONES PRIVADAS — descubrimiento del árbol
# ===============================================================

def _clave_modulo(rel: str) -> str:
    """Misma transformación de ruta a clave que aplica el adaptador."""
    clave = PREFIJO_ADAPTADOR + (
        rel.replace("/", "_").replace("\\", "_").replace(".", "_")
    )
    if clave.endswith("_py"):
        clave = clave[:-3]
    return clave


def _recursos_del_arbol() -> List[Tuple[str, Any, str, Optional[str]]]:
    """
    Devuelve [(ruta_rel, modulo|None, procedencia, error|None)].

    Mismo criterio de exclusión que el adaptador. Se excluye a sí mismo.
    Reutiliza la instancia que el adaptador dejó registrada; solo carga
    si no la encuentra, y lo marca en 'procedencia'.
    """
    yo = Path(__file__).resolve()
    salida: List[Tuple[str, Any, str, Optional[str]]] = []

    for path in sorted(_DIR.rglob("*.py")):
        if path.name.startswith("_") or path.name == "__init__.py":
            continue
        if path.resolve() == yo:
            continue

        try:
            rel = str(path.relative_to(_DIR))
        except ValueError:
            rel = path.name

        clave = _clave_modulo(rel)
        mod = sys.modules.get(clave)

        if mod is not None:
            salida.append((rel, mod, YA_CARGADO, None))
            continue

        try:
            spec = importlib.util.spec_from_file_location(clave, str(path))
            if spec is None or spec.loader is None:
                salida.append((rel, None, NO_CARGABLE, "spec no disponible"))
                continue
            mod = importlib.util.module_from_spec(spec)
            sys.modules[clave] = mod
            spec.loader.exec_module(mod)
            salida.append((rel, mod, CARGADO_AQUI, None))
        except Exception as e:
            salida.append((rel, None, NO_CARGABLE, f"{type(e).__name__}: {e}"))

    return salida


def _declaradas(meta: Dict[str, Any]) -> Optional[List[str]]:
    """
    Lee SOLO la clave contractual. None si el recurso no la declara.
    No busca claves alternativas. No infiere.
    """
    raw = meta.get(CLAVE_DECLARACION)

    if isinstance(raw, (list, tuple)):
        return [n for n in raw if isinstance(n, str) and n.strip()]
    if isinstance(raw, str) and raw.strip():
        return [raw.strip()]
    return None


def _estado_capacidad(mod: Any, nombre: str) -> Dict[str, Any]:
    """declarado / existe / callable. NUNCA invoca la capacidad."""
    base: Dict[str, Any] = {
        "nombre": nombre,
        "declarado": True,
        "existe": False,
        "callable": False,
        "tipo": None,
        "ok": False,
        "estado": None,
        "motivo": None,
    }

    if not nombre.isidentifier():
        base["estado"] = NOMBRE_INVALIDO
        base["motivo"] = f"'{nombre}' no es identificador Python válido"
        return base

    if not hasattr(mod, nombre):
        base["estado"] = AUSENTE
        base["motivo"] = f"declarado pero el módulo no expone '{nombre}'"
        return base

    obj = getattr(mod, nombre)
    base["existe"] = True
    base["tipo"] = type(obj).__name__

    if not callable(obj):
        base["estado"] = NO_CALLABLE
        base["motivo"] = f"existe como '{type(obj).__name__}', no invocable"
        return base

    base["callable"] = True
    base["ok"] = True
    base["estado"] = OK
    return base

# ===============================================================
# FIN FUNCIONES PRIVADAS
# ===============================================================

# ===============================================================
# CAPACIDADES PÚBLICAS
# ===============================================================

def auditar() -> Dict[str, Any]:
    """Estado estructural de cada capacidad declarada, por recurso."""
    recursos: Dict[str, Any] = {}
    problemas: List[str] = []
    duplicados: Dict[str, List[str]] = {}
    cargados_aqui: List[str] = []

    n_declaradas = 0
    n_ok = 0
    n_fallidas = 0
    n_auditados = 0
    n_sin_declarar = 0

    for rel, mod, procedencia, error in _recursos_del_arbol():

        if procedencia == CARGADO_AQUI:
            cargados_aqui.append(rel)

        if mod is None:
            recursos[f"<{rel}>"] = {
                "ruta": rel,
                "estado": NO_CARGABLE,
                "procedencia": procedencia,
                "ok": False,
                "auditado": False,
                "error": error,
                "n_capacidades": 0,
                "capacidades": [],
            }
            problemas.append(f"{rel}: {NO_CARGABLE} — {error}")
            continue

        meta = getattr(mod, "SEGURIDAD", None)
        if not isinstance(meta, dict):
            continue

        rid_raw = meta.get("id")
        if not (isinstance(rid_raw, str) and rid_raw.strip()):
            recursos[f"<{rel}>"] = {
                "ruta": rel,
                "id": None,
                "estado": ID_AUSENTE,
                "procedencia": procedencia,
                "ok": False,
                "auditado": False,
                "motivo": "SEGURIDAD sin id válido",
                "n_capacidades": 0,
                "capacidades": [],
            }
            problemas.append(f"{rel}: SEGURIDAD sin id válido")
            continue

        rid = rid_raw.strip()
        declaradas = _declaradas(meta)

        entrada: Dict[str, Any] = {
            "ruta": rel,
            "id": rid,
            "modulo": getattr(mod, "__name__", None),
            "procedencia": procedencia,
        }

        if declaradas is None:
            n_sin_declarar += 1
            entrada.update({
                "estado": SIN_DECLARAR,
                "ok": True,
                "auditado": False,
                "n_capacidades": 0,
                "n_ok": 0,
                "n_fallidas": 0,
                "capacidades": [],
                "motivo": (
                    f"no declara '{CLAVE_DECLARACION}'; "
                    "ausencia de declaración, no contradicción"
                ),
            })
        else:
            detalle = [_estado_capacidad(mod, n) for n in declaradas]
            fallidas = [d for d in detalle if not d["ok"]]

            n_auditados += 1
            n_declaradas += len(detalle)
            n_ok += len(detalle) - len(fallidas)
            n_fallidas += len(fallidas)

            for d in fallidas:
                problemas.append(
                    f"{rid} ({rel}) :: {d['nombre']} → {d['estado']} — {d['motivo']}"
                )

            entrada.update({
                "estado": OPERATIVO if not fallidas else DEGRADADO,
                "ok": not fallidas,
                "auditado": True,
                "n_capacidades": len(detalle),
                "n_ok": len(detalle) - len(fallidas),
                "n_fallidas": len(fallidas),
                "capacidades": detalle,
            })

        if rid in recursos:
            duplicados.setdefault(rid, [recursos[rid].get("ruta")]).append(rel)
            problemas.append(
                f"id '{rid}' declarado por más de un archivo: "
                f"{sorted(duplicados[rid])}"
            )
            recursos[rid]["estado"] = ID_DUPLICADO
            recursos[rid]["ok"] = False
            recursos[rid].setdefault("colisiones", []).append(entrada)
        else:
            recursos[rid] = entrada

    return {
        "recurso": "CAPACIDADES",
        "version": SEGURIDAD["version"],
        "clave_declaracion": CLAVE_DECLARACION,
        "ok": not problemas,
        "coherente": not problemas,
        "n_recursos": len(recursos),
        "n_auditados": n_auditados,
        "n_sin_declarar": n_sin_declarar,
        "capacidades_declaradas": n_declaradas,
        "capacidades_ok": n_ok,
        "capacidades_fallidas": n_fallidas,
        "ids_duplicados": {k: sorted(v) for k, v in sorted(duplicados.items())},
        "cargados_por_auditor": cargados_aqui,
        "recursos": recursos,
        "problemas": problemas,
        "conceptos": [] if not problemas else ["CÓDIGO_INVÁLIDO"],
        "nota": (
            "'ok' es ESTRUCTURAL: declarado, existe y callable. "
            "No significa que la capacidad funcione: eso lo demuestra "
            "el pipeline de tests."
        ),
    }


def capacidades_de(recurso_id: str) -> Dict[str, Any]:
    """Detalle de un solo recurso, por su id declarado."""
    if not isinstance(recurso_id, str) or not recurso_id.strip():
        return {
            "recurso": "CAPACIDADES",
            "ok": False,
            "error": "recurso_id inválido",
            "conceptos": ["CÓDIGO_INVÁLIDO"],
        }

    r = auditar()
    clave = recurso_id.strip()
    entrada = r["recursos"].get(clave)

    if entrada is None:
        return {
            "recurso": "CAPACIDADES",
            "ok": False,
            "error": f"recurso '{clave}' no encontrado",
            "disponibles": sorted(r["recursos"].keys()),
            "conceptos": [],
        }

    return {
        "recurso": "CAPACIDADES",
        "id": clave,
        "ok": bool(entrada.get("ok")),
        "auditado": bool(entrada.get("auditado")),
        "estado": entrada.get("estado"),
        "detalle": entrada,
        "conceptos": [] if entrada.get("ok") else ["CÓDIGO_INVÁLIDO"],
    }


def resumen() -> Dict[str, Any]:
    """Totales y una línea por recurso."""
    r = auditar()
    return {
        "recurso": "CAPACIDADES",
        "version": SEGURIDAD["version"],
        "ok": r["ok"],
        "n_recursos": r["n_recursos"],
        "n_auditados": r["n_auditados"],
        "n_sin_declarar": r["n_sin_declarar"],
        "capacidades_declaradas": r["capacidades_declaradas"],
        "capacidades_ok": r["capacidades_ok"],
        "capacidades_fallidas": r["capacidades_fallidas"],
        "por_recurso": {
            rid: {
                "ruta": e.get("ruta"),
                "estado": e.get("estado"),
                "procedencia": e.get("procedencia"),
                "n_capacidades": e.get("n_capacidades", 0),
                "n_ok": e.get("n_ok", 0),
                "n_fallidas": e.get("n_fallidas", 0),
            }
            for rid, e in sorted(r["recursos"].items())
        },
        "ids_duplicados": r["ids_duplicados"],
        "cargados_por_auditor": r["cargados_por_auditor"],
        "problemas": r["problemas"],
    }


def tabla() -> str:
    """Reporte en texto plano, para el log del pipeline."""
    r = auditar()
    lineas: List[str] = []

    for rid, e in sorted(r["recursos"].items()):
        estado = e.get("estado")

        if estado == SIN_DECLARAR:
            lineas.append(f"{rid} — sin declaración de capacidades")
            lineas.append("")
            continue

        if not e.get("auditado"):
            lineas.append(f"{rid} — {estado}")
            if e.get("error"):
                lineas.append(f"  {e['error']}")
            if e.get("motivo"):
                lineas.append(f"  {e['motivo']}")
            lineas.append("")
            continue

        n = e.get("n_capacidades", 0)
        lineas.append(f"{rid} — {n} capacidades")
        lineas.append("-" * 44)

        for c in e.get("capacidades", []):
            if c["ok"]:
                lineas.append(f"  OK     {c['nombre']}")
            else:
                lineas.append(f"  FALLA  {c['nombre']}  -> {c['estado']}")

        n_ok = e.get("n_ok", 0)
        n_f = e.get("n_fallidas", 0)
        lineas.append(f"  {n_ok}/{n} OK")
        if n_f:
            nombres = [c["nombre"] for c in e["capacidades"] if not c["ok"]]
            lineas.append(f"  {n_f} FALLA -> {', '.join(nombres)}")
        lineas.append("")

    lineas.append("=" * 44)
    lineas.append(
        f"TOTAL: {r['capacidades_ok']}/{r['capacidades_declaradas']} OK "
        f"en {r['n_auditados']} recursos auditados "
        f"({r['n_sin_declarar']} sin declarar)"
    )
    lineas.append("ok estructural: declarado + existe + callable")

    if r["cargados_por_auditor"]:
        lineas.append("")
        lineas.append(
            f"AVISO: cargados por el auditor (no por el adaptador): "
            f"{r['cargados_por_auditor']}"
        )

    if r["problemas"]:
        lineas.append("")
        for p in r["problemas"]:
            lineas.append(f"  ! {p}")

    return "\n".join(lineas)

# ===============================================================
# FIN CAPACIDADES PÚBLICAS
# ===============================================================

# ===============================================================
# EXPORTACIONES
# ===============================================================

__all__ = [
    "SEGURIDAD",
    "auditar",
    "capacidades_de",
    "resumen",
    "tabla",
    "CLAVE_DECLARACION",
    "OK",
    "AUSENTE",
    "NO_CALLABLE",
    "NOMBRE_INVALIDO",
    "OPERATIVO",
    "DEGRADADO",
    "SIN_DECLARAR",
    "ID_AUSENTE",
    "ID_DUPLICADO",
    "NO_CARGABLE",
    "YA_CARGADO",
    "CARGADO_AQUI",
]

# ===============================================================
# FIN DEL ARCHIVO
# ===============================================================
