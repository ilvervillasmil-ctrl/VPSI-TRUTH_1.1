# ===============================================================
# formulas_omega/resonance_extended.py — Resonancia avanzada
# ===============================================================
#
# Fórmulas:
#
#   ρ_multi = (PHI/2) · mean( phase_alignment(e_i, e_{i+1}) )
#
#   align*(e_i, e_j) = min(1, boost · min(e_i,e_j)/max(e_i,e_j))
#
#   M_ij = pair_resonance(e_i, e_j) · PHI^(−|i−j|)   (i ≠ j)
#   M_ii = 1
#
#   E_transform = κ · Σ_i e_i
#
# Variables:
#
#   e_i     — energía de la capa i
#   PHI     — razón áurea (escala y decaimiento por distancia)
#   κ       — KAPPA, costo de integración (transformación, no pérdida)
#   boost   — factor de refuerzo de alineación
#   M       — matriz de resonancia completa (todos los pares)
#   ρ_multi — resonancia media adyacente escalada por PHI/2
#
# Qué hace:
#   Extiende ResonanceLogic: pares no adyacentes, decaimiento
#   fractal por distancia, alineación potenciada y costo de
#   integración κ·E_total.
#
# ===============================================================

import math

from .constants import PHI, KAPPA
from .resonance import ResonanceLogic


class AdvancedResonance:
    """
    Extended resonance: non-adjacent interactions, fractal patterns,
    and integration cost (kappa).
    """

    @staticmethod
    def multi_layer_resonance(energies):
        """
        Average phase alignment across all adjacent layer pairs,
        scaled by PHI/2.
        """
        if len(energies) <= 1:
            return 0.0
        total = 0.0
        pairs = 0
        for i in range(len(energies) - 1):
            alignment = ResonanceLogic.calculate_phase_alignment(energies[i], energies[i + 1])
            total += alignment
            pairs += 1
        average = total / pairs if pairs > 0 else 0.0
        return average * (PHI / 2)

    @staticmethod
    def enhanced_phase_alignment(e_i, e_j, boost=1.0):
        """
        Enhanced alignment with boost factor.
        Result capped at 1.0.
        """
        base = ResonanceLogic.calculate_phase_alignment(e_i, e_j)
        return min(1.0, base * boost)

    @staticmethod
    def full_resonance_matrix(energies):
        """Resonance between ALL pairs (not just adjacent)."""
        n = len(energies)
        matrix = [[0.0] * n for _ in range(n)]
        for i in range(n):
            matrix[i][i] = 1.0
            for j in range(i + 1, n):
                distance = j - i
                decay = PHI ** (-distance)
                r = ResonanceLogic.pair_resonance(energies[i], energies[j])
                matrix[i][j] = r * decay
                matrix[j][i] = r * decay
        return matrix

    @staticmethod
    def integration_cost(energies):
        """E_transform = kappa * E_total. NOT loss, transformation."""
        return KAPPA * sum(energies)
