# ===============================================================
# formulas_omega/layer_coherence.py — Coherencia entre capas
# ===============================================================
#
# Fórmulas:
#
#   c_i,i+1 = 1 − |A_i − A_{i+1}| / max(A_i, A_{i+1})
#
#   C_layers = (1 / (n−1)) · Σ_{i=0}^{n−2} c_i,i+1
#
# Variables:
#
#   A_i        — actividad (o energía) de la capa i
#   c_i,i+1    — alineación local entre capas adyacentes ∈ [0, 1]
#   C_layers   — coherencia media a lo largo de la cadena de capas
#   n          — número de capas (n ≥ 2)
#
# Calidad (umbrales de la semilla):
#
#   C_layers ≥ α      → High Coherence
#   β ≤ C_layers < α  → Moderate Coherence
#   C_layers < β      → Low Coherence
#
# Qué hace:
#   Mide qué tan alineada está la actividad entre capas vecinas.
#   No es C_Ω global: es coherencia de cadena local entre niveles.
#
# ===============================================================

import math

from modules.constante import ALPHA, BETA

class LayerCoherence:
    @staticmethod
    def calculate_layer_coherence(activity: list) -> float:
        """
        Calculates coherence across multiple layers.

        activity: List of layer activity levels [L1, L2, ..., Ln].
        """
        if not activity or len(activity) < 2:
            raise ValueError("At least two layers are required to calculate coherence.")

        total_coherence = 0
        for i in range(len(activity) - 1):
            total_coherence += 1 - (abs(activity[i] - activity[i + 1]) / max(activity[i], activity[i + 1]))

        return total_coherence / (len(activity) - 1)

    @staticmethod
    def layer_alignment_quality(energy_levels: list) -> str:
        """
        Provides a qualitative evaluation of layer alignment quality.
        """
        coherence = LayerCoherence.calculate_layer_coherence(energy_levels)
        if coherence >= ALPHA:
            return "High Coherence"
        elif coherence >= BETA:
            return "Moderate Coherence"
        else:
            return "Low Coherence"
