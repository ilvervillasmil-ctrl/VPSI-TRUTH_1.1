# ===============================================================
# formulas_omega/exponential_decay.py — Decaimiento exponencial
# ===============================================================
#
# Fórmulas:
#
#   V(t) = V₀ · e^(−k · t)
#
#   T_½  = ln(2) / k
#
# Variables:
#
#   V₀  — valor inicial (V₀ > 0)
#   k   — tasa de decaimiento (k > 0)
#   t   — tiempo
#   V(t)— magnitud en el instante t
#   T_½ — tiempo de vida media (cuando V = V₀/2)
#
# Qué hace:
#   Modela la pérdida de amplitud / señal / activación en el
#   tiempo. Base de presencia temporal, fricción acumulada y
#   olvido estructural cuando el flujo no se renueva.
#
# ===============================================================

import math

class ExponentialDecay:
    @staticmethod
    def calculate_decay(initial_value: float, decay_rate: float, time: float) -> float:
        """
        Models exponential decay over time.
        Formula: V(t) = V0 * e^(-k * t)

        initial_value: Initial quantity.
        decay_rate: Rate of decay (k).
        time: Time (t).
        """
        if initial_value <= 0:
            raise ValueError("Initial value must be greater than zero.")
        return initial_value * math.exp(-decay_rate * time)

    @staticmethod
    def half_life(decay_rate: float) -> float:
        """
        Calculates the half-life based on the decay rate.
        Formula: T_half = ln(2) / decay_rate
        """
        if decay_rate <= 0:
            raise ValueError("Decay rate must be greater than zero.")
        return math.log(2) / decay_rate
