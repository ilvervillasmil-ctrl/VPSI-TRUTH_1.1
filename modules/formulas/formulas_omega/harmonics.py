# ===============================================================
# formulas_omega/harmonics.py — Armónicos y decaimiento
# ===============================================================
#
# Fórmulas:
#
#   f_n = f₀ · PHI^n
#
#   A(t) = A₀ · e^(−λ · t)
#
# Variables:
#
#   f₀          — frecuencia base
#   n           — orden armónico (multiplier)
#   f_n         — frecuencia del armónico n
#   A₀          — amplitud inicial
#   λ           — tasa de decaimiento (decay_rate)
#   t           — tiempo
#   A(t)        — amplitud en el instante t
#   PHI         — razón áurea (escala de frecuencias)
#
# Qué hace:
#   Genera la serie armónica escalada por PHI y modela el
#   decaimiento de amplitud de la señal en el tiempo.
#   Acopla frecuencia áurea de capas con pérdida temporal.
#
# ===============================================================
import math
from formulas.constants import PHI

class Harmonics:
    @staticmethod
    def calculate_harmonic_ratio(base_frequency: float, multiplier: int) -> float:
        """
        Calculates the harmonic ratio relative to the golden ratio (PHI).

        base_frequency: The initial frequency to calculate harmonics for.
        multiplier: The harmonic level (e.g., 1st, 2nd, etc.).
        """
        return base_frequency * (PHI ** multiplier)

    @staticmethod
    def harmonic_decay(initial_amplitude: float, decay_rate: float, time: float) -> float:
        """
        Formula: A = A0 * e^(-lambda * t)
        Models the decay of a signal over time.
        """
        return initial_amplitude * math.exp(-decay_rate * time)
