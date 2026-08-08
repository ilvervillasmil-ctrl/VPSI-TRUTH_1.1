# ===============================================================
# VPSI-TRUTH — modules/spartaco_seguridad/capacidades.py
# ===============================================================
#
# RECURSO:             CAPACIDADES
# Módulo contenedor:   spartaco_seguridad (SC)
# Versión recurso:     1.2
#
# Función:
#   Reportar, por cada recurso descubierto en el árbol del
#   módulo, las capacidades que ese recurso declara y el estado
#   estructural de cada una. Todo en números exactos.
#   No se elimina evidencia. No se filtra la declaración.
#
# Qué hace:
#   - Recorre el árbol con el mismo criterio que el adaptador.
#   - Por cada archivo descubierto produce una entrada.
#   - Si declara capacidades_recurso, evalúa cada elemento
#     tal como viene (válido o no).
#   - Cuenta existe / callable sin invocar.
#   - Los contadores reflejan el estado FINAL del diccionario.
#
# Qué NO hace:
#   - No infiere capacidades.
#   - No invoca ninguna capacidad.
#   - No modifica recursos, adaptador ni Engine.
#   - No descarta elementos inválidos de la declaración.
#   - No oculta archivos sin SEGURIDAD.
#
# ---------------------------------------------------------------
# CONTRATO DE DECLARACIÓN
# ---------------------------------------------------------------
#   "capacidades_recurso": ["nucleo", "canales", ...]
#
#   Clave distinta de CONTENEDOR["capacidades"].
#   Ausencia de la clave → SIN_DECLARAR (no es error).
#   Elemento no-str o no-identificador → se conserva y se marca.
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
        "Cuantifica exacto. No elimina evidencia. No ejecuta."
    ),
    "herramienta": (
        "Introspección hasattr + callable sobre los recursos descubiertos"
    ),
    "version": "1.2",
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
        "No descarta elementos inválidos de la declaración",
        "No oculta archivos sin SEGURIDAD",
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
PREFIJO_ADAPTADOR = "sc_"

# estado por capacidad
OK = "OK"
AUSENTE = "AUSENTE_EN_MODULO"
NO_CALLABLE = "NO_CALLABLE"
NOMBRE_INVALIDO = "NOMBRE_INVALIDO"

# estado por recurso
OPERATIVO = "OPERATIVO"
DEGRADADO = "DEGRADADO"
SIN_DECLARAR = "SIN_DECLARAR"
SIN_SEGURIDAD = "SIN_SEGURIDAD"
ID_AUSENTE = "ID_AUSENTE"
ID_DUPLICADO = "ID_DUPLICADO"
NO_CARGABLE = "NO_CARGABLE"

# procedencia
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

    Mismo criterio de exclusión que el adaptador.
    Se excluye a sí mismo.
    Reutiliza la instancia registrada por el adaptador;
    solo carga si no la encuentra.
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


def _elementos_declaracion(meta: Dict[str, Any]) -> Optional[List[Any]]:
    """
    Devuelve la lista cruda de la declaración, sin filtrar.
    None si la clave no existe o no es list/tuple/str.
    Cada elemento se conserva tal cual para no perder evidencia.
    """
    raw = meta.get(CLAVE_DECLARACION)

    if isinstance(raw, (list, tuple)):
        return list(raw)
    if isinstance(raw, str):
        return [raw]
    return None


def _estado_capacidad(mod: Any, elemento: Any) -> Dict[str, Any]:
    """
    Evalúa un elemento de la declaración tal como viene.
    No se descarta. Si no es str identificador válido → NOMBRE_INVALIDO.
    NUNCA invoca la capacidad.
    """
    base: Dict[str, Any] = {
        "nombre": None,
        "elemento_crudo": elemento,
        "declarado": True,
        "existe": False,
        "callable": False,
        "tipo": None,
        "ok": False,
        "estado": None,
        "motivo": None,
    }

    if not isinstance(elemento, str):
        base["nombre"] = repr(elemento)
        base["estado"] = NOMBRE_INVALIDO
        base["motivo"] = f"elemento no es str: {type(elemento).__name__}"
        return base

    nombre = elemento.strip()
    base["nombre"] = nombre if nombre else repr(elemento)

    if not nombre or not nombre.isidentifier():
        base["estado"] = NOMBRE_INVALIDO
        base["motivo"] = f"'{elemento!r}' no es identificador Python válido"
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


def _fraccion(num: int, den: int) -> str:
    """Representación textual n/m. No calcula cociente."""
    return f"{num}/{den}"

# ===============================================================
# FIN FUNCIONES PRIVADAS
# ===============================================================

# ===============================================================
# CAPACIDADES PÚBLICAS
# ===============================================================

def auditar() -> Dict[str, Any]:
    """
    Estado estructural de cada capacidad declarada, por recurso.
    Contadores = estado FINAL del diccionario de recursos.
    No se elimina evidencia.
    """
    # Fase 1: recolectar entradas sin consolidar contadores finales
    entradas: List[Dict[str, Any]] = []
    problemas: List[str] = []
    cargados_aqui: List[str] = []
    n_ya_cargado = 0
    n_cargado_aqui = 0

    dist_cap: Dict[str, int] = {
        OK: 0,
        AUSENTE: 0,
        NO_CALLABLE: 0,
        NOMBRE_INVALIDO: 0,
    }

    for rel, mod, procedencia, error in _recursos_del_arbol():

        if procedencia == CARGADO_AQUI:
            cargados_aqui.append(rel)
            n_cargado_aqui += 1
        elif procedencia == YA_CARGADO:
            n_ya_cargado += 1

        # --- no cargable ---
        if mod is None:
            entradas.append({
                "clave": f"<{rel}>",
                "ruta": rel,
                "id": None,
                "estado": NO_CARGABLE,
                "procedencia": procedencia,
                "ok": False,
                "auditado": False,
                "error": error,
                "n_capacidades": 0,
                "n_ok": 0,
                "n_fallidas": 0,
                "capacidades": [],
            })
            problemas.append(f"{rel}: {NO_CARGABLE} — {error}")
            continue

        meta = getattr(mod, "SEGURIDAD", None)

        # --- sin SEGURIDAD: se reporta, no se oculta ---
        if not isinstance(meta, dict):
            entradas.append({
                "clave": f"<{rel}>",
                "ruta": rel,
                "id": None,
                "estado": SIN_SEGURIDAD,
                "procedencia": procedencia,
                "ok": True,
                "auditado": False,
                "motivo": "archivo sin SEGURIDAD dict",
                "n_capacidades": 0,
                "n_ok": 0,
                "n_fallidas": 0,
                "capacidades": [],
            })
            continue

        rid_raw = meta.get("id")

        # --- id ausente ---
        if not (isinstance(rid_raw, str) and rid_raw.strip()):
            entradas.append({
                "clave": f"<{rel}>",
                "ruta": rel,
                "id": None,
                "estado": ID_AUSENTE,
                "procedencia": procedencia,
                "ok": False,
                "auditado": False,
                "motivo": "SEGURIDAD sin id válido",
                "n_capacidades": 0,
                "n_ok": 0,
                "n_fallidas": 0,
                "capacidades": [],
            })
            problemas.append(f"{rel}: SEGURIDAD sin id válido")
            continue

        rid = rid_raw.strip()
        elementos = _elementos_declaracion(meta)

        entrada: Dict[str, Any] = {
            "clave": rid,
            "ruta": rel,
            "id": rid,
            "modulo": getattr(mod, "__name__", None),
            "procedencia": procedencia,
        }

        # --- sin declaración de capacidades ---
        if elementos is None:
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
            # cada elemento se evalúa; ninguno se descarta
            detalle = [_estado_capacidad(mod, el) for el in elementos]
            fallidas = [d for d in detalle if not d["ok"]]
            ok_count = len(detalle) - len(fallidas)

            for d in detalle:
                est = d["estado"]
                if est in dist_cap:
                    dist_cap[est] += 1

            for d in fallidas:
                problemas.append(
                    f"{rid} ({rel}) :: {d['nombre']} → {d['estado']} — {d['motivo']}"
                )

            entrada.update({
                "estado": OPERATIVO if not fallidas else DEGRADADO,
                "ok": not fallidas,
                "auditado": True,
                "n_capacidades": len(detalle),
                "n_ok": ok_count,
                "n_fallidas": len(fallidas),
                "fraccion_ok": _fraccion(ok_count, len(detalle)),
                "capacidades": detalle,
            })

        entradas.append(entrada)

    # Fase 2: consolidar por id (detectar duplicados)
    recursos: Dict[str, Any] = {}
    duplicados: Dict[str, List[str]] = {}

    for entrada in entradas:
        clave = entrada["clave"]
        ruta = entrada.get("ruta")

        if clave in recursos:
            # colisión de id
            prev = recursos[clave]
            duplicados.setdefault(clave, [prev.get("ruta")]).append(ruta)
            problemas.append(
                f"id '{clave}' declarado por más de un archivo: "
                f"{sorted(duplicados[clave])}"
            )
            prev["estado"] = ID_DUPLICADO
            prev["ok"] = False
            prev.setdefault("colisiones", []).append(entrada)
        else:
            recursos[clave] = entrada

    # Fase 3: contadores desde el estado FINAL
    n_recursos = len(recursos)
    n_auditados = 0
    n_sin_declarar = 0
    n_sin_seguridad = 0
    n_operativo = 0
    n_degradado = 0
    n_no_cargable = 0
    n_id_ausente = 0
    n_id_duplicado = 0
    n_declaradas = 0
    n_ok = 0
    n_fallidas = 0

    for e in recursos.values():
        estado = e.get("estado")

        if estado == OPERATIVO:
            n_operativo += 1
            n_auditados += 1
        elif estado == DEGRADADO:
            n_degradado += 1
            n_auditados += 1
        elif estado == SIN_DECLARAR:
            n_sin_declarar += 1
        elif estado == SIN_SEGURIDAD:
            n_sin_seguridad += 1
        elif estado == NO_CARGABLE:
            n_no_cargable += 1
        elif estado == ID_AUSENTE:
            n_id_ausente += 1
        elif estado == ID_DUPLICADO:
            n_id_duplicado += 1
            # un duplicado puede haber sido auditado antes de la colisión
            if e.get("auditado"):
                n_auditados += 1

        if e.get("auditado"):
            n_declaradas += e.get("n_capacidades", 0)
            n_ok += e.get("n_ok", 0)
            n_fallidas += e.get("n_fallidas", 0)

    return {
        "recurso": "CAPACIDADES",
        "version": SEGURIDAD["version"],
        "clave_declaracion": CLAVE_DECLARACION,

        "ok": not problemas,
        "coherente": not problemas,

        # recursos (estado final)
        "n_recursos": n_recursos,
        "n_auditados": n_auditados,
        "n_sin_declarar": n_sin_declarar,
        "n_sin_seguridad": n_sin_seguridad,
        "n_operativo": n_operativo,
        "n_degradado": n_degradado,
        "n_no_cargable": n_no_cargable,
        "n_id_ausente": n_id_ausente,
        "n_id_duplicado": n_id_duplicado,

        # capacidades
        "capacidades_declaradas": n_declaradas,
        "capacidades_ok": n_ok,
        "capacidades_fallidas": n_fallidas,
        "fraccion_capacidades": _fraccion(n_ok, n_declaradas),
        "distribucion_estados": dict(dist_cap),

        # procedencia
        "n_ya_cargado": n_ya_cargado,
        "n_cargado_aqui": n_cargado_aqui,
        "cargados_por_auditor": list(cargados_aqui),

        # colisiones
        "n_ids_duplicados": len(duplicados),
        "ids_duplicados": {k: sorted(v) for k, v in sorted(duplicados.items())},

        "recursos": recursos,
        "problemas": problemas,
        "n_problemas": len(problemas),
        "conceptos": [] if not problemas else ["CÓDIGO_INVÁLIDO"],

        "nota": (
            "'ok' es ESTRUCTURAL: declarado + existe + callable. "
            "No significa que la capacidad funcione. "
            "Contadores = estado final. No se elimina evidencia."
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
            "n_disponibles": len(r["recursos"]),
            "conceptos": [],
        }

    return {
        "recurso": "CAPACIDADES",
        "id": clave,
        "ok": bool(entrada.get("ok")),
        "auditado": bool(entrada.get("auditado")),
        "estado": entrada.get("estado"),
        "n_capacidades": entrada.get("n_capacidades", 0),
        "n_ok": entrada.get("n_ok", 0),
        "n_fallidas": entrada.get("n_fallidas", 0),
        "fraccion_ok": entrada.get("fraccion_ok", _fraccion(0, 0)),
        "detalle": entrada,
        "conceptos": [] if entrada.get("ok") else ["CÓDIGO_INVÁLIDO"],
    }


def resumen() -> Dict[str, Any]:
    """Totales numéricos y una línea por recurso. Estado final."""
    r = auditar()
    return {
        "recurso": "CAPACIDADES",
        "version": SEGURIDAD["version"],
        "ok": r["ok"],
        "coherente": r["coherente"],

        "n_recursos": r["n_recursos"],
        "n_auditados": r["n_auditados"],
        "n_sin_declarar": r["n_sin_declarar"],
        "n_sin_seguridad": r["n_sin_seguridad"],
        "n_operativo": r["n_operativo"],
        "n_degradado": r["n_degradado"],
        "n_no_cargable": r["n_no_cargable"],
        "n_id_ausente": r["n_id_ausente"],
        "n_id_duplicado": r["n_id_duplicado"],

        "capacidades_declaradas": r["capacidades_declaradas"],
        "capacidades_ok": r["capacidades_ok"],
        "capacidades_fallidas": r["capacidades_fallidas"],
        "fraccion_capacidades": r["fraccion_capacidades"],
        "distribucion_estados": r["distribucion_estados"],

        "n_ya_cargado": r["n_ya_cargado"],
        "n_cargado_aqui": r["n_cargado_aqui"],
        "cargados_por_auditor": r["cargados_por_auditor"],

        "n_ids_duplicados": r["n_ids_duplicados"],
        "ids_duplicados": r["ids_duplicados"],
        "n_problemas": r["n_problemas"],
        "problemas": r["problemas"],

        "por_recurso": {
            rid: {
                "ruta": e.get("ruta"),
                "estado": e.get("estado"),
                "procedencia": e.get("procedencia"),
                "n_capacidades": e.get("n_capacidades", 0),
                "n_ok": e.get("n_ok", 0),
                "n_fallidas": e.get("n_fallidas", 0),
                "fraccion_ok": e.get("fraccion_ok", _fraccion(0, 0)),
            }
            for rid, e in sorted(r["recursos"].items())
        },
    }


def tabla() -> str:
    """Reporte en texto plano con conteos exactos del estado final."""
    r = auditar()
    lineas: List[str] = []

    for rid, e in sorted(r["recursos"].items()):
        estado = e.get("estado")

        if estado == SIN_DECLARAR:
            lineas.append(f"{rid} — sin declaración de capacidades")
            lineas.append("")
            continue

        if estado == SIN_SEGURIDAD:
            lineas.append(f"{rid} — sin SEGURIDAD")
            lineas.append(f"  ruta: {e.get('ruta')}")
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
        n_ok = e.get("n_ok", 0)
        n_f = e.get("n_fallidas", 0)
        lineas.append(f"{rid} — {n} capacidades  ({_fraccion(n_ok, n)} OK)")
        lineas.append("-" * 44)

        for c in e.get("capacidades", []):
            if c["ok"]:
                lineas.append(f"  OK     {c['nombre']}")
            else:
                lineas.append(f"  FALLA  {c['nombre']}  -> {c['estado']}")

        lineas.append(f"  {n_ok}/{n} OK")
        if n_f:
            nombres = [c["nombre"] for c in e["capacidades"] if not c["ok"]]
            lineas.append(f"  {n_f} FALLA -> {', '.join(nombres)}")
        lineas.append("")

    lineas.append("=" * 44)
    lineas.append(
        f"TOTAL CAPACIDADES: {r['capacidades_ok']}/{r['capacidades_declaradas']} OK "
        f"({r['fraccion_capacidades']})"
    )
    lineas.append(
        f"RECURSOS: {r['n_operativo']} operativo | "
        f"{r['n_degradado']} degradado | "
        f"{r['n_sin_declarar']} sin declarar | "
        f"{r['n_sin_seguridad']} sin SEGURIDAD | "
        f"{r['n_no_cargable']} no cargable | "
        f"{r['n_id_ausente']} id ausente | "
        f"{r['n_id_duplicado']} id duplicado"
    )
    lineas.append(
        f"AUDITADOS: {r['n_auditados']}  |  "
        f"PROCEDENCIA: {r['n_ya_cargado']} ya_cargado + "
        f"{r['n_cargado_aqui']} cargado_aqui"
    )
    lineas.append("ok estructural: declarado + existe + callable")

    dist = r["distribucion_estados"]
    lineas.append(
        f"DISTRIBUCIÓN CAPACIDADES: "
        f"OK={dist.get(OK, 0)}  "
        f"AUSENTE={dist.get(AUSENTE, 0)}  "
        f"NO_CALLABLE={dist.get(NO_CALLABLE, 0)}  "
        f"NOMBRE_INVALIDO={dist.get(NOMBRE_INVALIDO, 0)}"
    )

    if r["cargados_por_auditor"]:
        lineas.append("")
        lineas.append(
            f"AVISO: cargados por el auditor (no por el adaptador): "
            f"{r['cargados_por_auditor']}"
        )

    if r["problemas"]:
        lineas.append("")
        lineas.append(f"PROBLEMAS ({r['n_problemas']}):")
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
    "SIN_SEGURIDAD",
    "ID_AUSENTE",
    "ID_DUPLICADO",
    "NO_CARGABLE",
    "YA_CARGADO",
    "CARGADO_AQUI",
]

# ===============================================================
# FIN DEL ARCHIVO
# ===============================================================
