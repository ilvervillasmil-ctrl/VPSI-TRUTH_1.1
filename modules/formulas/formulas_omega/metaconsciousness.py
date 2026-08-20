# ===============================================================
# formulas_omega/metaconsciousness.py — Metaconciencia (MC)
# ===============================================================
#
# Fórmula:
#
#   MC = R_fin · ∏_{i=3}^{6} [ L_i · (1 − φ_i) ]
#
# Variables:
#
#   L_i     — activación de la capa i ∈ [0, 1]
#   φ_i     — fricción de la capa i ∈ [0, 1]
#   R_fin   — 28/27  (excedente de emergencia)
#
# Dominio:
#   Solo L3…L6 (donde empieza el procesamiento).
#   Si alguna de L3…L6 es cero → MC = 0.
#
# Niveles:
#   0  None
#   1  Experiential   (MC < 0.3)
#   2  Sensitive      (MC < 0.7)
#   3  Structural     (MC ≥ 0.7)
#
# ===============================================================

from .constants import R_FIN

from .constants import R_FIN


class MetaconsciousnessCalculator:
    """
    MC = product(i=3 to 6) [Li * (1-phi_i)] * R_fin

    Only L3-L6: metaconsciousness begins where PROCESSING begins.
    If ANY of L3-L6 is zero, MC is zero.
    R_fin = 28/27 = the surplus of emergence.
    """

    @staticmethod
    def compute(activations, frictions):
        """MC = product(L3..L6) [Li * (1-phi_i)] * R_fin"""
        product = 1.0
        for i in range(3, 7):
            product *= activations[i] * (1.0 - frictions[i])
        return product * R_FIN

    @staticmethod
    def level(mc_value):
        """0=None, 1=Experiential, 2=Sensitive, 3=Structural"""
        if mc_value <= 0:
            return 0
        elif mc_value < 0.3:
            return 1
        elif mc_value < 0.7:
            return 2
        else:
            return 3

    @staticmethod
    def level_name(mc_value):
        """Return human-readable level name."""
        names = {0: "None", 1: "Experiential", 2: "Sensitive", 3: "Structural"}
        return names[MetaconsciousnessCalculator.level(mc_value)]
