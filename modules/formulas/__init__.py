# -*- coding: utf-8 -*-
"""
VPSI-TRUTH --- modules/formulas/__init__.py

Contenedor de fórmulas. Rol FO. v1.0

Expone tru_ri y tru_total.
El Engine lee CONTENEDOR.capacidades y ejecuta cada clave.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List

try:
    from core.diagnostico import DiagnosticoGlobal  # type: ignore
except Exception:  # noqa: BLE001
    DiagnosticoGlobal = None  # type: ignore

_DIR = Path(__file__).parent

# ===============================================================
# ERRORES
# ===============================================================
class FormulaError(Exception):
    pass


class FormulaNoEncontradaError(Exception):
    pass


# ===============================================================
# ESTADO
# ===============================================================
PISO_FORMULAS = 1
_DECLARACIONES: List[Dict[str, Any]] = []
_REGLAS: List[Callable[[], List[str]]] = []
_FORMULAS: Dict[str, Dict[str, Any]] = {}


# ===============================================================
# GANCHOS
# ===============================================================
def regla(fn: Callable[[], List[str]]) -> Callable[[], List[str]]:
    _REGLAS.append(fn)
    return fn


def declarar(d: Dict[str, Any]) -> Dict[str, Any]:
    _DECLARACIONES.append(d)
    return d


def registrar_formula(nombre: str, meta: Dict[str, Any]):
    def decorator(fn: Callable) -> Callable:
        _FORMULAS[nombre] = {**meta, "funcion": fn}
        return fn
    return decorator


# ===============================================================
# DESCUBRIMIENTO
# ===============================================================
def _descubrir_formulas() -> Dict[str, Dict[str, Any]]:
    registro: Dict[str, Dict[str, Any]] = {}
    for f in sorted(_DIR.glob("*.py")):
        if f.name.startswith("_"):
            continue
        clave = "formulas_{0}".format(f.stem)
        spec = importlib.util.spec_from_file_location(clave, f)
        if spec is None or spec.loader is None:
            continue
        mod = importlib.util.module_from_spec(spec)
        sys.modules[clave] = mod
        try:
            spec.loader.exec_module(mod)
        except Exception:  # noqa: BLE001
            continue
        meta = getattr(mod, "FORMULA", None)
        if isinstance(meta, dict) and "nombre" in meta:
            registro[meta["nombre"]] = {
                "archivo": f.name,
                "expresion": meta.get("expresion", "No definida"),
                "fuente": meta.get("fuente", "Desconocida"),
            }
    return registro


# ===============================================================
# CAPACIDADES
# ===============================================================
def barrer() -> Dict[str, Any]:
    faltas: List[str] = []
    for regla_fn in _REGLAS:
        try:
            faltas.extend(regla_fn() or [])
        except Exception as e:  # noqa: BLE001
            faltas.append(
                "{0}: {1}: {2}".format(
                    regla_fn.__name__, type(e).__name__, e
                )
            )

    if faltas and DiagnosticoGlobal is not None:
        try:
            DiagnosticoGlobal.recibir_reporte(
                modulo="formulas",
                errores=[
                    {"tipo": "falta", "detalle": falta}
                    for falta in faltas
                ],
            )
        except Exception:  # noqa: BLE001
            pass

    return {
        "contenedor": "formulas",
        "estado": "APROBADO" if not faltas else "RECHAZADO",
        "coherente": not faltas,
        "faltas": faltas,
        "reglas": [r.__name__ for r in _REGLAS],
        "formulas": list(_FORMULAS.keys()) or list(_descubrir_formulas().keys()),
    }


def verificar_salida(salida: Dict[str, Any]) -> bool:
    return bool(salida.get("coherente", False))


def inventario(peticion=None) -> Dict[str, Any]:
    return {
        "contenedor": "formulas",
        "version": "1.0",
        "formulas": _descubrir_formulas(),
        "formulas_registradas": list(_FORMULAS.keys()),
        "reglas": len(_REGLAS),
        "declaraciones": len(_DECLARACIONES),
    }


def axiomas() -> List[Dict[str, Any]]:
    return list(_DECLARACIONES)


# ===============================================================
# REGLAS
# ===============================================================
@regla
def _validar_piso_formulas() -> List[str]:
    if len(_descubrir_formulas()) < PISO_FORMULAS:
        return [
            "Menos de {0} fórmulas: coherencia por vacuidad".format(
                PISO_FORMULAS
            )
        ]
    return []


@regla
def _validar_formulas_canonicas() -> List[str]:
    faltas = []
    descubiertas = _descubrir_formulas()
    if "tru_ri" not in _FORMULAS and "tru_ri" not in descubiertas:
        faltas.append("Fórmula tru_ri no encontrada.")
    if "tru_total" not in _FORMULAS and "tru_total" not in descubiertas:
        faltas.append("Fórmula tru_total no encontrada.")
    return faltas


# ===============================================================
# DECLARACIONES
# ===============================================================
declarar({
    "id": "FO-1",
    "tipo": "axioma",
    "sujeto": "Tru_Ri",
    "relacion": "=",
    "objeto": "C * L * K",
    "polaridad": True,
    "enunciado": (
        "Tru_Ri(D) = C(D) * L(D) * K(D) (Axioma TA5: Multiplicatividad)."
    ),
    "cota": None,
    "depende_de": ["TA5"],
    "gobierna": ["tru_ri"],
})

declarar({
    "id": "FO-2",
    "tipo": "axioma",
    "sujeto": "Tru_total",
    "relacion": "=",
    "objeto": "(Tru_Ri * ALPHA) + BETA",
    "polaridad": True,
    "enunciado": (
        "Tru_total(D) = (Tru_Ri(D) * ALPHA) + BETA (Definición 2.14)."
    ),
    "cota": None,
    "depende_de": ["Def-2.14"],
    "gobierna": ["tru_total"],
})

declarar({
    "id": "FO-3",
    "tipo": "teorema",
    "sujeto": "Tru_Ri",
    "relacion": "≤",
    "objeto": "ALPHA",
    "polaridad": True,
    "enunciado": (
        "Tru_Ri(D) ≤ ALPHA = 26/27 (Teorema 16: Techo Estructural)."
    ),
    "cota": "26/27",
    "depende_de": ["T16"],
    "gobierna": ["tru_ri"],
})

declarar({
    "id": "FO-4",
    "tipo": "teorema",
    "sujeto": "Tru_total",
    "relacion": "≥",
    "objeto": "BETA",
    "polaridad": True,
    "enunciado": (
        "Tru_total(D) ≥ BETA = 1/27 (Teorema 17: Piso Estructural)."
    ),
    "cota": "1/27",
    "depende_de": ["T17"],
    "gobierna": ["tru_total"],
})


# ===============================================================
# FÓRMULAS CANÓNICAS
# ===============================================================
from .truth import tru_ri, tru_total, FORMULA as TRUTH_FORMULA  # noqa: E402


@registrar_formula("tru_ri", TRUTH_FORMULA)
def _tru_ri_wrapper(C, L, K):
    return tru_ri(C, L, K)


@registrar_formula("tru_total", TRUTH_FORMULA)
def _tru_total_wrapper(C, L, K):
    return tru_total(C, L, K)


# ===============================================================
# CONTENEDOR — contrato con el Engine
# ===============================================================
CONTENEDOR = {
    "nombre": "formulas",
    "rol": "FO",
    "version": "1.0",
    "requiere": ["CT"],
    "descripcion": (
        "Contenedor de fórmulas. Rol FO. "
        "Expone tru_ri y tru_total. "
        "El Engine ejecuta las capacidades declaradas aquí."
    ),
    "capacidades": {
        "verificar": barrer,
        "barrer": barrer,
        "evaluar": barrer,
        "verificar_salida": verificar_salida,
        "inventario": inventario,
        "axiomas": axiomas,
        "tru_ri": tru_ri,
        "tru_total": tru_total,
    },
}


__all__ = [
    "CONTENEDOR",
    "barrer",
    "verificar_salida",
    "inventario",
    "axiomas",
    "tru_ri",
    "tru_total",
    "FormulaError",
    "FormulaNoEncontradaError",
]
