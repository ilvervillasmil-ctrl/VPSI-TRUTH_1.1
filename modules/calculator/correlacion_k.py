# ===============================================================
# VPSI-TRUTH — modules/calculator/correlacion_k.py
# ===============================================================
#
# CORRELACIÓN K
# -------------
# La correlación cuantifica la correspondencia de una base de
# afirmaciones verificables frente a sus divergencias, bajo un
# dominio O explícito.
#
#   K(c, f) =
#       UNDEFINED          si ¬o_presente ∨ base_nula ∨ c ≤ 0
#       1 − f/c ∈ [0, 1]   si o_presente ∧ c > 0
#
#   c           = tamaño de la base de afirmaciones verificables
#   f           = peso total de las divergencias sobre esa base
#   o_presente  = el dominio O está declarado
#
# Por qué UNDEFINED sin O:
#   Sin dominio declarado no hay correspondencia que medir.
#   K no se define; no se inventa un número.
#
# Por qué UNDEFINED cuando c ≤ 0:
#   Sin base de afirmaciones no hay correlación que medir.
#   Asignar K = 1 en ese caso inflaría artificialmente Tru_Ri.
#
# Por qué 1 − f/c:
#   Cada unidad de divergencia degrada la base de afirmaciones.
#   Si f = 0, K = 1 (correspondencia completa).
#   Si f = c, K = 0 (base anulada).
#
# Por qué f ∈ [0, c]:
#   El peso de divergencia no puede exceder la base que degrada.
#   Fuera de ese intervalo: violación de dominio → error.
#   Con el dominio respetado, 0 ≤ 1 − f/c ≤ 1 queda garantizado.
#
# Por qué Fraction:
#   K es un valor racional exacto.
#
# Este archivo implementa únicamente K(c, f) bajo o_presente.
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


def correlacion(
    c: int,
    f: Union[int, Fraction] = 0,
    o_presente: bool = False,
    base_nula: bool = False,
) -> Any:
    """
    K(c, f) =
        UNDEFINED          si ¬o_presente ∨ base_nula ∨ c ≤ 0
        1 − f/c ∈ [0, 1]   si o_presente ∧ c > 0
    """
    c = int(c)

    if c < 0:
        raise ValueError("c < 0 fuera de dominio")

    # Sin dominio O, o sin base, K no está definido.
    if not o_presente or base_nula or c <= 0:
        return UNDEFINED

    f_f = _a_fraction(f)

    if f_f < 0 or f_f > c:
        raise ValueError("f fuera de dominio [0, c]")

    # Dominio 0 ≤ f ≤ c ⇒ 0 ≤ 1 − f/c ≤ 1 (sin clamp adicional)
    return Fraction(1) - (f_f / Fraction(c))


def calcular_k(
    c: Optional[int] = None,
    f: Any = None,
    o_presente: bool = False,
    base_nula: bool = False,
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Interfaz mínima. Solo acepta c, f, o_presente, base_nula.
    """
    if peticion is not None:
        if not isinstance(peticion, dict):
            raise TypeError("peticion debe ser dict")
        if c is None:
            c = peticion.get("c")
        if f is None:
            f = peticion.get("f")
        if not o_presente:
            o_presente = bool(peticion.get("o_presente", False))
        if not base_nula:
            base_nula = bool(peticion.get("base_nula", False))

    if c is None:
        raise ValueError("falta c")
    if f is None:
        f = 0

    c = int(c)
    f_f = _a_fraction(f)
    valor = correlacion(
        c, f_f, o_presente=o_presente, base_nula=base_nula
    )

    return {
        "K": valor,
        "c": c,
        "f": f_f if not (not o_presente or base_nula or c <= 0) else Fraction(0),
        "o_presente": o_presente,
    }


def verificar_k(salida: Any) -> bool:
    """
    Propiedades matemáticas:
      K ∈ {UNDEFINED} ∪ [0, 1]
      c ≥ 0
      0 ≤ f ≤ c  (cuando c > 0 y K definido)
    """
    if not isinstance(salida, dict):
        return False
    if "K" not in salida:
        return False

    val = salida["K"]
    es_und = val is UNDEFINED or str(val).upper() == "UNDEFINED"

    if not es_und:
        if not isinstance(val, Fraction):
            return False
        if val < Fraction(0) or val > Fraction(1):
            return False

    if "c" in salida:
        try:
            c = int(salida["c"])
        except Exception:
            return False
        if c < 0:
            return False
    else:
        c = None

    if "f" in salida and salida["f"] is not None:
        try:
            f_f = _a_fraction(salida["f"])
        except Exception:
            return False
        if f_f < 0:
            return False
        if c is not None and c > 0 and f_f > c:
            return False

    return True


__all__ = [
    "correlacion",
    "calcular_k",
    "verificar_k",
    "UNDEFINED",
]
