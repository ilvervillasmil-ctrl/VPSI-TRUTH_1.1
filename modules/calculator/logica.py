# ===============================================================
# VPSI-TRUTH — modules/calculator/logica.py
# ===============================================================
#
# LÓGICA L
# --------
# La lógica cuantifica la invariancia de una base de posturas
# frente a sus reversiones.
#
#   L(p, r) =
#       UNDEFINED          si base_nula ∨ p ≤ 0
#       1 − r/p ∈ [0, 1]   si p > 0
#
#   p  = tamaño de la base de posturas
#   r  = peso total de las reversiones sobre esa base
#
# Por qué UNDEFINED cuando p ≤ 0:
#   Sin base de posturas no hay invariancia que medir.
#   Asignar L = 1 en ese caso inflaría artificialmente Tru_Ri.
#
# Por qué 1 − r/p:
#   Cada unidad de reversión degrada la base de posturas.
#   Si r = 0, L = 1 (invariancia completa).
#   Si r = p, L = 0 (base anulada).
#
# Por qué r ∈ [0, p]:
#   El peso de reversión no puede exceder la base que degrada.
#   Fuera de ese intervalo: violación de dominio → error.
#   Con el dominio respetado, 0 ≤ 1 − r/p ≤ 1 queda garantizado.
#
# Por qué Fraction:
#   L es un valor racional exacto.
#
# Este archivo implementa únicamente L(p, r).
# ===============================================================

from __future__ import annotations

from fractions import Fraction
from typing import Any, Dict, Optional, Union


try:
    from modules.calculator import UNDEFINED
except Exception:
    class _Undefined:
        __slots__ = ()

        def __repr__(self) -> str:
            return "UNDEFINED"

        def __bool__(self):
            raise TypeError("UNDEFINED no admite conversion a booleano")

        def __eq__(self, other):
            return isinstance(other, _Undefined)

        def __hash__(self):
            return hash("VPSI_CA_UNDEFINED")

    UNDEFINED = _Undefined()


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
    raise TypeError(
        "se esperaba int|float|str|Fraction, recibido {0}".format(
            type(x).__name__
        )
    )


def logica(
    p: int,
    r: Union[int, Fraction] = 0,
    base_nula: bool = False,
) -> Any:
    """
    L(p, r) =
        UNDEFINED          si base_nula ∨ p ≤ 0
        1 − r/p ∈ [0, 1]   si p > 0
    """
    p = int(p)

    if p < 0:
        raise ValueError("p < 0 fuera de dominio")

    if base_nula or p <= 0:
        return UNDEFINED

    r_f = _a_fraction(r)

    if r_f < 0 or r_f > p:
        raise ValueError("r fuera de dominio [0, p]")

    # Dominio 0 ≤ r ≤ p ⇒ 0 ≤ 1 − r/p ≤ 1 (sin clamp adicional)
    return Fraction(1) - (r_f / Fraction(p))


def calcular_l(
    p: Optional[int] = None,
    r: Any = None,
    base_nula: bool = False,
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Interfaz mínima. Solo acepta p, r, base_nula.
    """
    if peticion is not None:
        if not isinstance(peticion, dict):
            raise TypeError("peticion debe ser dict")
        if p is None:
            p = peticion.get("p")
        if r is None:
            r = peticion.get("r")
        if not base_nula:
            base_nula = bool(peticion.get("base_nula", False))

    if p is None:
        raise ValueError("falta p")
    if r is None:
        r = 0

    p = int(p)
    r_f = _a_fraction(r)
    valor = logica(p, r_f, base_nula=base_nula)

    return {
        "L": valor,
        "p": p,
        "r": r_f if not (base_nula or p <= 0) else Fraction(0),
    }


def verificar_l(salida: Any) -> bool:
    """
    Propiedades matemáticas:
      L ∈ {UNDEFINED} ∪ [0, 1]
      p ≥ 0
      0 ≤ r ≤ p  (cuando p > 0)
    """
    if not isinstance(salida, dict):
        return False
    if "L" not in salida:
        return False

    val = salida["L"]
    es_und = val is UNDEFINED or str(val).upper() == "UNDEFINED"

    if not es_und:
        if not isinstance(val, Fraction):
            return False
        if val < Fraction(0) or val > Fraction(1):
            return False

    if "p" in salida:
        try:
            p = int(salida["p"])
        except Exception:
            return False
        if p < 0:
            return False
    else:
        p = None

    if "r" in salida and salida["r"] is not None:
        try:
            r_f = _a_fraction(salida["r"])
        except Exception:
            return False
        if r_f < 0:
            return False
        if p is not None and p > 0 and r_f > p:
            return False

    return True


__all__ = [
    "logica",
    "calcular_l",
    "verificar_l",
    "UNDEFINED",
]
