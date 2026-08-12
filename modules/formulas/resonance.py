# ===============================================================
# modules/formulas/resonance.py
# ===============================================================
#
# VPSI-TRUTH — RESONANCE
#
# RESPONSABILIDAD:
#   Implementar exclusivamente la matemática de la resonancia
#   inter-capas.
#
# ESTE ARCHIVO:
#   - No declara CONTENEDOR.
#   - No habla con Engine.
#   - No interpreta contexto.
#   - No calcula Tru.
#   - No modifica C, L o K.
#   - No decide el significado epistemológico del resultado.
#
# ===============================================================
# DEFINICIONES MATEMÁTICAS
# ===============================================================
#
# Frecuencia:
#
#   ν_i = Φ^(i/2)
#
# Alineación:
#
#   A_ij = min(E_i,E_j) / max(E_i,E_j)
#
# Factor de fase:
#
#   P_ij = (1 + cos(Δφ)) / 2
#
# Magnitud de resonancia:
#
#   M_ij = 2·√(E_i·E_j) / (E_i + E_j)
#
# Resonancia de par:
#
#   r_ij = M_ij · P_ij
#
# Resonancia global:
#
#   ρ = (1/N) · Σ r_ij
#
# ===============================================================


from __future__ import annotations

import math
from decimal import Decimal, getcontext
from fractions import Fraction
from typing import Any, Dict, List, Sequence

from .constants import PHI


# ===============================================================
# NOTA TÉCNICA 1 — BACKEND NUMÉRICO
# ===============================================================
#
# El tipo numérico NO determina por sí solo la precisión del
# cálculo.
#
# VPSI-TRUTH debe separar:
#
#   FÓRMULA
#       ↓
#   BACKEND NUMÉRICO
#       ↓
#   OPERACIONES MATEMÁTICAS
#
# Un backend debe proporcionar las operaciones necesarias para
# evaluar la fórmula completa:
#
#   +, -, ×, ÷
#   √
#   potencias
#   cos
#   sin
#   log
#   exp
#   y otras funciones cuando sean necesarias.
#
# No se permite degradar silenciosamente una operación de alta
# precisión a float.
#
# ===============================================================


# ===============================================================
# NOTA TÉCNICA 2 — FLOAT NO ES EL ESTÁNDAR
# ===============================================================
#
# float es solamente un backend posible.
#
# Puede utilizarse cuando:
#
#   - la aproximación sea suficiente;
#   - la velocidad sea prioritaria;
#   - el error sea aceptable.
#
# No debe utilizarse automáticamente para todas las fórmulas.
#
# Una fórmula científica puede requerir:
#
#   - precisión arbitraria;
#   - racionales;
#   - complejos;
#   - cálculo simbólico;
#   - notación científica;
#   - unidades;
#   - incertidumbre.
#
# El backend debe adaptarse a la fórmula.
#
# ===============================================================


# ===============================================================
# BACKEND
# ===============================================================

class NumericBackend:
    """
    Interfaz conceptual para el backend matemático.

    El objetivo es que las fórmulas no dependan directamente de
    math.sqrt(), math.cos(), etc.

    De esta manera puede conectarse posteriormente un backend de
    precisión arbitraria o simbólico sin modificar la fórmula.
    """

    nombre = "base"

    def convertir(self, valor):
        raise NotImplementedError

    def cero(self):
        raise NotImplementedError

    def dos(self):
        raise NotImplementedError

    def sumar(self, a, b):
        raise NotImplementedError

    def restar(self, a, b):
        raise NotImplementedError

    def multiplicar(self, a, b):
        raise NotImplementedError

    def dividir(self, a, b):
        raise NotImplementedError

    def raiz(self, valor):
        raise NotImplementedError

    def potencia(self, base, exponente):
        raise NotImplementedError

    def coseno(self, valor):
        raise NotImplementedError


# ===============================================================
# BACKEND FLOAT
# ===============================================================

class FloatBackend(NumericBackend):
    """
    Backend aproximado basado en float.
    """

    nombre = "float"

    def convertir(self, valor):
        return float(valor)

    def cero(self):
        return 0.0

    def dos(self):
        return 2.0

    def sumar(self, a, b):
        return a + b

    def restar(self, a, b):
        return a - b

    def multiplicar(self, a, b):
        return a * b

    def dividir(self, a, b):
        return a / b

    def raiz(self, valor):
        return math.sqrt(valor)

    def potencia(self, base, exponente):
        return base ** exponente

    def coseno(self, valor):
        return math.cos(valor)


# ===============================================================
# BACKEND DECIMAL
# ===============================================================

class DecimalBackend(NumericBackend):
    """
    Backend decimal de precisión configurable.

    Importante:
        Este backend NO convierte Decimal → float.

    Las operaciones que requieren funciones trascendentales deben
    ser proporcionadas por el backend matemático de precisión
    arbitraria que se conecte posteriormente.
    """

    nombre = "decimal"

    def convertir(self, valor):
        if isinstance(valor, Decimal):
            return valor

        return Decimal(str(valor))

    def cero(self):
        return Decimal(0)

    def dos(self):
        return Decimal(2)

    def sumar(self, a, b):
        return a + b

    def restar(self, a, b):
        return a - b

    def multiplicar(self, a, b):
        return a * b

    def dividir(self, a, b):
        return a / b

    def raiz(self, valor):
        return valor.sqrt()

    def potencia(self, base, exponente):
        return base ** exponente

    def coseno(self, valor):
        raise NotImplementedError(
            "El backend Decimal requiere una implementación "
            "trigonométrica de precisión arbitraria para cos()."
        )


# ===============================================================
# SELECCIÓN DEL BACKEND
# ===============================================================

def obtener_backend(
    backend: str = "float",
    precision: int = 50,
) -> NumericBackend:

    if backend == "float":
        return FloatBackend()

    if backend == "decimal":
        getcontext().prec = precision
        return DecimalBackend()

    raise ValueError(
        "backend debe ser 'float' o 'decimal'. "
        "Los backends adicionales podrán incorporarse "
        "sin modificar las fórmulas."
    )


# ===============================================================
# FRECUENCIA DE CAPA
# ===============================================================

def frecuencia_capa(
    layer_index: int,
    backend: str = "float",
    precision: int = 50,
):
    """
    ν_i = Φ^(i/2)
    """

    motor = obtener_backend(
        backend,
        precision,
    )

    phi = motor.convertir(PHI)

    exponente = motor.dividir(
        motor.convertir(layer_index),
        motor.dos(),
    )

    return motor.potencia(
        phi,
        exponente,
    )


# ===============================================================
# ALINEACIÓN DE FASE / MAGNITUD
# ===============================================================

def alineacion_fase(
    e_i,
    e_j,
    backend: str = "float",
    precision: int = 50,
):
    """
    A_ij = min(E_i,E_j) / max(E_i,E_j)
    """

    motor = obtener_backend(
        backend,
        precision,
    )

    e_i = motor.convertir(e_i)
    e_j = motor.convertir(e_j)

    if e_i == motor.cero() or e_j == motor.cero():
        return motor.cero()

    menor = min(e_i, e_j)
    mayor = max(e_i, e_j)

    return motor.dividir(
        menor,
        mayor,
    )


# ===============================================================
# FACTOR DE FASE
# ===============================================================

def factor_fase(
    phase_diff,
    backend: str = "float",
    precision: int = 50,
):
    """
    P_ij = (1 + cos(Δφ)) / 2
    """

    motor = obtener_backend(
        backend,
        precision,
    )

    phase_diff = motor.convertir(
        phase_diff
    )

    coseno = motor.coseno(
        phase_diff
    )

    numerador = motor.sumar(
        motor.dos(),
        coseno,
    )

    return motor.dividir(
        numerador,
        motor.dos(),
    )


# ===============================================================
# RESONANCIA DE UN PAR
# ===============================================================

def resonancia_par(
    e_i,
    e_j,
    phase_diff=0,
    backend: str = "float",
    precision: int = 50,
):
    """
    r_ij =
        [2·√(E_i·E_j)/(E_i+E_j)]
        ·
        [(1+cos(Δφ))/2]
    """

    motor = obtener_backend(
        backend,
        precision,
    )

    e_i = motor.convertir(e_i)
    e_j = motor.convertir(e_j)

    if (
        e_i == motor.cero()
        or e_j == motor.cero()
    ):
        return motor.cero()

    producto = motor.multiplicar(
        e_i,
        e_j,
    )

    raiz = motor.raiz(
        producto
    )

    numerador = motor.multiplicar(
        motor.dos(),
        raiz,
    )

    denominador = motor.sumar(
        e_i,
        e_j,
    )

    magnitud = motor.dividir(
        numerador,
        denominador,
    )

    fase = factor_fase(
        phase_diff,
        backend=backend,
        precision=precision,
    )

    return motor.multiplicar(
        magnitud,
        fase,
    )


# ===============================================================
# ρ GLOBAL
# ===============================================================

def calcular(
    energies: Sequence,
    backend: str = "float",
    precision: int = 50,
    phase_diffs: Sequence | None = None,
) -> Dict[str, Any]:
    """
    ρ = media de resonancia entre pares adyacentes.

    Si phase_diffs no se proporciona:

        Δφ = 0

    para todos los pares.

    Entonces:

        P_ij = 1
    """

    motor = obtener_backend(
        backend,
        precision,
    )

    if not energies:

        return {
            "ok": True,
            "valor": motor.cero(),
            "backend": backend,
            "precision": (
                precision
                if backend == "decimal"
                else None
            ),
            "factores": {
                "n_capas": 0,
                "n_pares": 0,
                "energies": [],
                "r_pares": [],
            },
        }

    valores = [
        motor.convertir(e)
        for e in energies
    ]

    if all(
        e == motor.cero()
        for e in valores
    ):

        return {
            "ok": True,
            "valor": motor.cero(),
            "backend": backend,
            "precision": (
                precision
                if backend == "decimal"
                else None
            ),
            "factores": {
                "n_capas": len(valores),
                "n_pares": 0,
                "energies": valores,
                "r_pares": [],
            },
        }

    n_pares = len(valores) - 1

    if phase_diffs is None:

        fases = [
            motor.cero()
            for _ in range(n_pares)
        ]

    else:

        if len(phase_diffs) != n_pares:
            raise ValueError(
                "phase_diffs debe contener "
                "exactamente un valor por cada "
                "par adyacente."
            )

        fases = [
            motor.convertir(f)
            for f in phase_diffs
        ]

    total = motor.cero()
    detalle_pares: List[Any] = []

    for i in range(n_pares):

        r = resonancia_par(
            valores[i],
            valores[i + 1],
            phase_diff=fases[i],
            backend=backend,
            precision=precision,
        )

        detalle_pares.append(r)
        total = motor.sumar(
            total,
            r,
        )

    rho = motor.dividir(
        total,
        motor.convertir(n_pares),
    )

    return {
        "ok": True,
        "valor": rho,
        "backend": backend,
        "precision": (
            precision
            if backend == "decimal"
            else None
        ),
        "factores": {
            "n_capas": len(valores),
            "n_pares": n_pares,
            "energies": valores,
            "phase_diffs": fases,
            "r_pares": detalle_pares,
        },
        "nota": (
            "ρ = media de r_ij; "
            "r_ij = [2·√(E_i·E_j)/(E_i+E_j)] "
            "· [(1+cos(Δφ))/2]."
        ),
    }


# ===============================================================
# API DE COMPATIBILIDAD
# ===============================================================

class ResonanceLogic:

    @staticmethod
    def calculate_layer_frequency(
        layer_index: int,
        backend: str = "float",
        precision: int = 50,
    ):
        return frecuencia_capa(
            layer_index,
            backend,
            precision,
        )

    @staticmethod
    def calculate_phase_alignment(
        e_i,
        e_j,
        backend: str = "float",
        precision: int = 50,
    ):
        return alineacion_fase(
            e_i,
            e_j,
            backend,
            precision,
        )

    @staticmethod
    def pair_resonance(
        e_i,
        e_j,
        phase_diff=0,
        backend: str = "float",
        precision: int = 50,
    ):
        return resonancia_par(
            e_i,
            e_j,
            phase_diff,
            backend,
            precision,
        )

    @staticmethod
    def compute(
        energies: Sequence,
        backend: str = "float",
        precision: int = 50,
        phase_diffs: Sequence | None = None,
    ):
        return calcular(
            energies,
            backend=backend,
            precision=precision,
            phase_diffs=phase_diffs,
        )["valor"]


# ===============================================================
# NOTA DE IMPLEMENTACIÓN 1 — POR QUÉ EXISTE EL BACKEND
# ===============================================================
#
# La fórmula no debe conocer la implementación concreta del
# cálculo numérico.
#
# Resonance solicita:
#
#   raíz
#   coseno
#   multiplicación
#   división
#
# al backend.
#
# Esto permite incorporar posteriormente un backend de:
#
#   - precisión arbitraria;
#   - cálculo simbólico;
#   - números complejos;
#   - unidades físicas;
#   - intervalos/incertidumbre;
#   - otras representaciones especializadas.
#
# sin modificar las ecuaciones de Resonance.
#
# ===============================================================


# ===============================================================
# NOTA DE IMPLEMENTACIÓN 2 — PRECISIÓN END-TO-END
# ===============================================================
#
# La precisión debe mantenerse durante TODA la cadena de cálculo.
#
# No es suficiente almacenar:
#
#   E_i → Decimal
#
# para posteriormente hacer:
#
#   Decimal → float → cos() → Decimal
#
# porque la operación intermedia ya degradó la representación.
#
# El backend seleccionado debe ejecutar todas las operaciones
# compatibles con la precisión solicitada.
#
# Si una operación no está disponible, debe incorporarse al
# backend o seleccionarse otro backend apropiado.
#
# La fórmula nunca debe degradarse para adaptarse a una
# limitación accidental de implementación.
#
# ===============================================================


# ===============================================================
# NOTA METODOLÓGICA PERMANENTE
# ===============================================================
#
# La representación numérica nunca debe limitar anticipadamente
# la matemática del motor.
#
# Cada fórmula debe analizarse según su naturaleza matemática,
# científica y dimensional antes de seleccionar su backend.
#
# float es una opción de evaluación aproximada.
# Decimal es una opción de precisión decimal.
# Fraction permite exactitud racional cuando corresponde.
# Otros backends podrán proporcionar precisión arbitraria,
# cálculo simbólico, complejos, unidades, incertidumbre u otras
# capacidades requeridas por futuras fórmulas.
#
# La fórmula determina las capacidades necesarias del backend.
# El backend no determina ni modifica la fórmula.
#
# ===============================================================


# ---------------------------------------------------------------
# EXPORTACIONES
# ---------------------------------------------------------------

__all__ = [
    "NumericBackend",
    "FloatBackend",
    "DecimalBackend",
    "obtener_backend",
    "frecuencia_capa",
    "alineacion_fase",
    "factor_fase",
    "resonancia_par",
    "calcular",
    "ResonanceLogic",
]

# ===============================================================
# FIN
# ===============================================================
