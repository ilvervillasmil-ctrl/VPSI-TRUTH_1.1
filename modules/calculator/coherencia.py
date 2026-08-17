# ===============================================================
# VPSI-TRUTH — modules/calculator/coherencia.py
# ===============================================================
#
# COHERENCIA C
# -------------
# La coherencia mide la ausencia de contradicción interna en D.
# C = 1  si y solo si no existe una proposición P tal que
#        D afirma P y D afirma ¬P a la vez.
#
# Fórmula operacional:
#
#   C(m, k) =
#       UNDEFINED          si base_nula ∨ m ≤ 0
#       1 − k/m ∈ [0, 1]   si m > 0
#
#   m  = tamaño de la base (cuántos compromisos se adoptan)
#   k  = peso total de las contradicciones sobre esa base
#
# Por qué UNDEFINED cuando m ≤ 0:
#   Sin base no hay nada que contradecir ni que sostener.
#   Asignar C = 1 en ese caso inflaría artificialmente Tru_Ri.
#   Por eso la base vacía no produce un número: produce UNDEFINED.
#
# Por qué 1 − k/m:
#   Cada unidad de contradicción (k) degrada la base (m).
#   Si no hay contradicción (k = 0), C = 1.
#   Si la base queda anulada (k = m), C = 0.
#
# Por qué k debe estar en [0, m]:
#   Un peso de contradicción mayor que la base no tiene sentido
#   en la definición: no se puede romper más de lo que existe.
#   Si llega k fuera de [0, m], es violación de dominio → error.
#
# Por qué Fraction y no float:
#   C es un valor racional exacto. float introduciría error binario.
#
# Este archivo solo implementa esa función. No interpreta texto,
# no cuenta compromisos, no orquesta. Recibe m, k, base_nula
# ya resueltos y devuelve C.
# ===============================================================

# ===============================================================
# IMPORTACIONES
# ===============================================================

from __future__ import annotations

# --- Tipos y estructuras ---
from typing import Any, Dict, Optional, Union

# --- Números y precisión ---
from fractions import Fraction


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
    # Conversión estricta al dominio racional.
    # No inventa ceros: una entrada inválida debe fallar a la vista.
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


def coherencia(
    m: int,
    k: Union[int, Fraction] = 0,
    base_nula: bool = False,
) -> Any:
    """
    C(m, k) =
        UNDEFINED          si base_nula ∨ m ≤ 0
        1 − k/m ∈ [0, 1]   si m > 0

    m : tamaño de la base de compromisos (entero ≥ 0)
    k : peso de contradicción sobre esa base (racional en [0, m])
    """
    m = int(m)

    # m negativo no pertenece al dominio de la definición.
    if m < 0:
        raise ValueError("m < 0 fuera de dominio")

    # Base vacía o marcada nula → no hay C numérico.
    # UNDEFINED evita inflar Tru_Ri con un 1 artificial.
    if base_nula or m <= 0:
        return UNDEFINED

    k_f = _a_fraction(k)

    # Dominio de k: 0 ≤ k ≤ m.
    # k > m rompería más de lo que la base contiene.
    # k < 0 no es un peso de contradicción válido.
    if k_f < 0 or k_f > m:
        raise ValueError("k fuera de dominio [0, m]")

    # Núcleo de la definición: C = 1 − k/m
    resultado = Fraction(1) - (k_f / Fraction(m))

    # Cierre del intervalo [0, 1] (propiedad del dominio de C).
    if resultado < 0:
        resultado = Fraction(0)
    if resultado > 1:
        resultado = Fraction(1)
    return resultado


def calcular_c(
    m: Optional[int] = None,
    k: Any = None,
    base_nula: bool = False,
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Interfaz mínima hacia Calculator.

    Solo acepta m, k, base_nula.
    Calculator es quien normaliza nombres operacionales
    y entrega estos tres datos ya resueltos.
    """
    if peticion is not None:
        if not isinstance(peticion, dict):
            raise TypeError("peticion debe ser dict")
        if m is None:
            m = peticion.get("m")
        if k is None:
            k = peticion.get("k")
        if not base_nula:
            base_nula = bool(peticion.get("base_nula", False))

    if m is None:
        raise ValueError("falta m")
    if k is None:
        k = 0

    m = int(m)
    k_f = _a_fraction(k)
    valor = coherencia(m, k_f, base_nula=base_nula)

    return {
        "C": valor,
        "m": m,
        # Si la base es nula, k efectivo para el registro es 0.
        "k": k_f if not (base_nula or m <= 0) else Fraction(0),
    }


def verificar_c(salida: Any) -> bool:
    """
    Comprueba solo propiedades matemáticas del resultado:
      C ∈ {UNDEFINED} ∪ [0, 1]
      m ≥ 0
      0 ≤ k ≤ m   (cuando m > 0)
    """
    if not isinstance(salida, dict):
        return False
    if "C" not in salida:
        return False

    val = salida["C"]
    es_und = val is UNDEFINED or str(val).upper() == "UNDEFINED"

    if not es_und:
        if not isinstance(val, Fraction):
            return False
        if val < Fraction(0) or val > Fraction(1):
            return False

    if "m" in salida:
        try:
            m = int(salida["m"])
        except Exception:
            return False
        if m < 0:
            return False
    else:
        m = None

    if "k" in salida and salida["k"] is not None:
        try:
            k_f = _a_fraction(salida["k"])
        except Exception:
            return False
        if k_f < 0:
            return False
        if m is not None and m > 0 and k_f > m:
            return False

    return True


__all__ = [
    "coherencia",
    "calcular_c",
    "verificar_c",
    "UNDEFINED",
]
