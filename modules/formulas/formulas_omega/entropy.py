# ===============================================================
# formulas_omega/entropy.py — Entropía de Shannon
# ===============================================================
#
# Fórmulas:
#
#   H = − Σ_i p_i · log₂(p_i)     (p_i > 0)
#
#   p_i = E_i / Σ_j E_j           (desde distribución de energía)
#
# Variables:
#
#   p_i  — probabilidad del estado i  (Σ p_i = 1)
#   E_i  — energía de la capa / componente i
#   H    — entropía de Shannon (bits si log₂)
#
# Qué hace:
#   Mide incertidumbre / desorden de una distribución.
#   adjusted_entropy normaliza energías a probabilidades y
#   calcula H. Base para negentropía N = 1 − H/H_max.
#
# ===============================================================

import math
import math

class EntropyTool:
    @staticmethod
    def calculate_entropy(probabilities: list) -> float:
        """
        Calculates Shannon entropy of given probabilities.

        probabilities: List of probabilities (must sum up to 1).
        """
        if not probabilities or not math.isclose(sum(probabilities), 1.0):
            raise ValueError("Probabilities must sum to 1.")
        return -sum(p * math.log2(p) for p in probabilities if p > 0)

    @staticmethod
    def adjusted_entropy(energy_distribution: list) -> float:
        """
        Adjusted entropy calculation based on energy distribution.
        """
        total_energy = sum(energy_distribution)
        probabilities = [e / total_energy for e in energy_distribution]
        return EntropyTool.calculate_entropy(probabilities)
