# ==============================================================
# INICIO: modules/correlacion_mecanica/__init__.py
# Núcleo mecánico del sistema VPSI-TRUTH
# ==============================================================

# -*- coding: utf-8 -*-
"""
VPSI-TRUTH --- modules/correlacion_mecanica

Rol MC: Núcleo de correlación mecánica del sistema completo.

Este módulo contiene y expone todos los órdenes causales / mecánicos
declarados en sus archivos internos (cualquier archivo .py que defina
la variable MECANICA).

El Engine y el resto del sistema entran aquí para conocer:
- Qué órdenes mecánicos existen
- Cuáles son sus secuencias nativas
- Si hay contradicciones o ciclos entre ellos

No envía reportes a Diagnóstico.
Solo expone su contrato y su contenido objetivo.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

# ===============================================================
# CONTENEDOR (Contrato del módulo)
# ===============================================================
CONTENEDOR = {
    "nombre": "correlacion_mecanica",
    "rol": "MC",
    "version": "1.2",
    "requiere": [],
    "descripcion": (
        "Núcleo de correlación mecánica del sistema completo. "
        "Contiene y expone todos los órdenes causales declarados "
        "en los archivos de esta carpeta mediante la variable MECANICA."
    ),
    "capacidades": {
        "verificar": "barrer",
        "axiomas": "axiomas",
        "evaluar": "barrer",
        "inventario": "inventario",
    },
}

# ===============================================================
# CONSTANTES
# ===============================================================
_DIR = Path(__file__).parent
APROBADO = "APROBADO"
RECHAZADO = "RECHAZADO"

# ===============================================================
# DECLARACIONES INTERNAS (opcionales, para trazabilidad)
# ===============================================================
DECLARACIONES = [
    {
        "id": "CORR_SEQ_01",
        "tipo": "axioma",
        "sujeto": "mecanica_declarada",
        "relacion": "se_lee_en",
        "objeto": "orden_nativo",
        "polaridad": True,
        "enunciado": (
            "Principio de Secuencia Transversal: Los objetos de la carpeta "
            "se leen en su orden nativo para verificar que la transición "
            "entre estados cumpla la continuidad causal."
        ),
    },
    {
        "id": "CORR_SEQ_02",
        "tipo": "axioma",
        "sujeto": "colision_sobre_un_nodo",
        "relacion": "permite_el_paso",
        "objeto": "mecanica",
        "polaridad": False,
        "enunciado": (
            "Criterio de No Contradicción Cruzada: Si dos declaraciones de "
            "archivos distintos colisionan sobre el mismo nodo, el paso se "
            "bloquea y se reportan los identificadores en desacuerdo."
        ),
    },
]

# ===============================================================
# LECTURA DE TODAS LAS MECÁNICAS DECLARADAS EN LA CARPETA
# ===============================================================
def _leer() -> Dict[str, Any]:
    """
    Recorre absolutamente todos los archivos .py de esta carpeta
    y recoge cualquier declaración MECANICA que encuentre.
    """
    hallado = {}
    for archivo in sorted(_DIR.glob("*.py")):
        if archivo.name.startswith("_") or archivo.name == "__init__.py":
            continue

        clave = f"mecanica_{archivo.stem}"
        spec = importlib.util.spec_from_file_location(clave, archivo)
        if spec is None or spec.loader is None:
            continue

        mod = importlib.util.module_from_spec(spec)
        sys.modules[clave] = mod
        try:
            spec.loader.exec_module(mod)
        except Exception:
            continue

        meta = getattr(mod, "MECANICA", None)
        if isinstance(meta, dict):
            hallado[archivo.name] = meta

    return hallado


def _nodos(meta: Dict[str, Any]) -> List[str]:
    orden = meta.get("orden", [])
    if isinstance(orden, (list, tuple)):
        return [str(x) for x in orden]
    return []


def _precedencias(nodos: List[str]) -> List[Tuple[str, str]]:
    return [(a, b) for i, a in enumerate(nodos) for b in nodos[i + 1:]]


# ===============================================================
# CAPACIDADES PÚBLICAS
# ===============================================================
def axiomas() -> List[Dict[str, Any]]:
    return DECLARACIONES


def barrer() -> Dict[str, Any]:
    """
    Lee todas las MECANICA declaradas en la carpeta,
    calcula el orden resultante y detecta contradicciones o ciclos.
    """
    hallado = _leer()
    choques: List[str] = []
    errores: List[str] = []

    if not hallado:
        errores.append("ninguna mecánica declarada en la carpeta")
        return _informe([], choques, errores, hallado)

    precede: Dict[Tuple[str, str], List[str]] = {}

    for archivo, meta in sorted(hallado.items()):
        nodos = _nodos(meta)
        if len(nodos) < 2:
            errores.append(f"{archivo}: sin orden nativo legible")
            continue
        for a, b in _precedencias(nodos):
            precede.setdefault((a, b), []).append(archivo)

    # Detectar colisiones de orden
    for (a, b), quienes in sorted(precede.items()):
        contrarios = precede.get((b, a))
        if contrarios and (a, b) < (b, a):
            choques.append(
                f"nodo '{a}'/'{b}': {quienes} lo ponen en un orden y "
                f"{contrarios} en el contrario"
            )

    # Detectar ciclos
    universo = {x for par in precede for x in par}
    pendientes = set(universo)
    mecanica: List[str] = []

    while pendientes:
        libres = sorted(
            n for n in pendientes
            if not any((o, n) in precede for o in pendientes if o != n)
        )
        if not libres:
            choques.append(
                f"nodos {sorted(pendientes)}: la secuencia se muerde la cola, "
                "no hay orden posible"
            )
            break
        mecanica.extend(libres)
        pendientes -= set(libres)

    return _informe(mecanica, choques, errores, hallado)


def inventario() -> Dict[str, Any]:
    """Muestra de forma objetiva qué mecánicas existen dentro de este núcleo."""
    hallado = _leer()
    return {
        "contenedor": CONTENEDOR["nombre"],
        "version": CONTENEDOR["version"],
        "total_mecanicas": len(hallado),
        "archivos": sorted(hallado.keys()),
        "declaran": {
            archivo: {
                "nombre": meta.get("nombre", "Sin nombre"),
                "longitud_orden": len(meta.get("orden", [])),
            }
            for archivo, meta in sorted(hallado.items())
        },
    }


def verificar_salida(salida: Dict[str, Any]) -> bool:
    return bool(salida.get("coherente", False))


def _informe(
    mecanica: List[str],
    choques: List[str],
    errores: List[str],
    hallado: Dict[str, Any],
) -> Dict[str, Any]:
    limpio = not (choques or errores)
    return {
        "contenedor": CONTENEDOR["nombre"],
        "estado": APROBADO if limpio else RECHAZADO,
        "coherente": limpio,
        "choques": choques,
        "errores": errores,
        "mecanica": mecanica if limpio else [],
        "archivos": sorted(hallado.keys()),
        "total_mecanicas": len(hallado),
    }


# ===============================================================
# EXPORTACIONES
# ===============================================================
__all__ = [
    "CONTENEDOR",
    "DECLARACIONES",
    "axiomas",
    "barrer",
    "inventario",
    "verificar_salida",
    "APROBADO",
    "RECHAZADO",
]

# ==============================================================
# FIN: modules/correlacion_mecanica/__init__.py
# ==============================================================
