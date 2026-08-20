# ===============================================================
# formulas_omega/neuroscience_logic.py — Resonancia neural
# ===============================================================
#
# Fórmulas:
#
#   R(a, b) = α − β · |a − b| / max(a, b)
#             (si max(a, b) = 0 → R = 0)
#
#   f(t) = f₀ · e^(−λ · t)
#
# Variables:
#
#   a, b     — actividad de dos capas neurales
#   α        — ALPHA (26/27) techo estructural de resonancia
#   β        — BETA  (1/27)  penalización por desalineación
#   R(a, b)  — resonancia neural entre capas ∈ [β-ish, α]
#   f₀       — frecuencia inicial de resonancia
#   λ        — factor de decaimiento
#   t        — tiempo
#   f(t)     — frecuencia residual tras el decaimiento
#
# Qué hace:
#   Cuantifica el acoplamiento entre dos capas neurales con la
#   semilla del cubo (α techo, β costo de diferencia) y modela
#   el decaimiento temporal de esa resonancia.
#
# ===============================================================

import math

from modules.constante import ALPHA, BETA

class NeuroscienceLogic:
    @staticmethod
    def compute_neural_resonance(layer_a: float, layer_b: float) -> float:
        """
        Calculates resonance between two neural layers based on ALPHA and BETA.

        layer_a: Activity in layer A.
        layer_b: Activity in layer B.
        """
        max_energy = max(layer_a, layer_b)
        if max_energy == 0:
            return 0.0
        return ALPHA - (BETA * abs(layer_a - layer_b) / max_energy)

    @staticmethod
    def simulate_neural_decay(frequency: float, decay_factor: float, time: float) -> float:
        """
        Simulates the decay of neural resonance frequency over time.

        frequency: Initial frequency.
        decay_factor: Decay constant.
        time: Time elapsed.
        """
        return frequency * math.exp(-decay_factor * time)
