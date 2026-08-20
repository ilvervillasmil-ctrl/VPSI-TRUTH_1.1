# ===============================================================
# VPSI-TRUTH — modules/formulas/f_escala.py
# ===============================================================
#
# ESCALA
# ------
# Representación determinista de un valor racional.
#
#   escala(v) =
#       {
#         valor:       Fraction(v),
#         fraccion:    "n/d",
#         numerador:   n,
#         denominador: d,
#         decimal:     representación Decimal de v,
#         display:     "n/d = decimal",
#         precision:   p
#       }
#
#   Ejemplo:  escala(7/9) →  "7/9 = 0.778"
#
# Dominio:
#   v ∈ ℚ
#   p ∈ ℕ₀   (cifras decimales; por defecto 3)
#
# Codominio:
#   dict con valor ∈ ℚ, fraccion ∈ str, decimal ∈ str,
#   display ∈ str, numerador ∈ ℤ, denominador ∈ ℤ>0
#
# Propiedades:
#   display contiene fraccion y decimal
#   valor = numerador / denominador
#   float no es autoridad matemática
#
# ===============================================================

from __future__ import annotations

from fractions import Fraction
from typing import Any, Dict, List, Optional
from decimal import Decimal, ROUND_HALF_UP, getcontext

# ===============================================================
# AUTORIDAD DE CONSTANTES (CT) — OBLIGATORIO
# ===============================================================
from modules.constante import ALPHA, BETA
# ===============================================================


getcontext().prec = 50

PRECISION_DEFAULT = 3

FORMULA = {
    "nombre": "escala",
    "expresion": "display(v) = fraccion(v) = decimal(v)",
    "fuente": "Representación determinista Fraction → Decimal",
    "nota": "7/9 = 0.778",
}


def _a_fraction(x: Any) -> Fraction:
    if isinstance(x, Fraction):
        return x
    if isinstance(x, bool):
        return Fraction(int(x))
    if isinstance(x, int):
        return Fraction(x)
    if isinstance(x, float):
        return Fraction(x).limit_denominator(10_000)
    if isinstance(x, str):
        return Fraction(x)
    if isinstance(x, Decimal):
        return Fraction(x)
    raise TypeError(
        "se esperaba int|float|str|Fraction|Decimal, recibido {0}".format(
            type(x).__name__
        )
    )


def escala(v: Any, p: int = PRECISION_DEFAULT) -> Dict[str, Any]:
    """
    escala(v, p) =
        representación determinista de v ∈ ℚ
        con p cifras decimales.
    """
    p = int(p)
    if p < 0:
        raise ValueError("p < 0 fuera de dominio")

    fr = _a_fraction(v)

    if fr.denominator == 0:
        raise ValueError("denominador = 0 fuera de dominio")

    dec_val = Decimal(fr.numerator) / Decimal(fr.denominator)
    quant = Decimal("1").scaleb(-p)
    dec_str = str(dec_val.quantize(quant, rounding=ROUND_HALF_UP))
    frac_str = str(fr)

    return {
        "valor": fr,
        "fraccion": frac_str,
        "numerador": fr.numerator,
        "denominador": fr.denominator,
        "decimal": dec_str,
        "display": "{0} = {1}".format(frac_str, dec_str),
        "precision": p,
    }


def verificar_escala(salida: Any) -> bool:
    """
    Propiedades matemáticas del resultado:
      valor ∈ Fraction
      denominador > 0
      fraccion, decimal, display ∈ str
      display contiene fraccion y decimal
    """
    if not isinstance(salida, dict):
        return False
    for clave in (
        "valor",
        "fraccion",
        "numerador",
        "denominador",
        "decimal",
        "display",
        "precision",
    ):
        if clave not in salida:
            return False
    if not isinstance(salida["valor"], Fraction):
        return False
    if salida["denominador"] <= 0:
        return False
    if not isinstance(salida["fraccion"], str):
        return False
    if not isinstance(salida["decimal"], str):
        return False
    if salida["fraccion"] not in str(salida["display"]):
        return False
    if salida["decimal"] not in str(salida["display"]):
        return False
    return True


__all__ = [
    "FORMULA",
    "escala",
    "verificar_escala",
    "PRECISION_DEFAULT",
]
