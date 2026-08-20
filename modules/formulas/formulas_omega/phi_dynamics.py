# ===============================================================
# formulas_omega/phi_dynamics.py — Dinámica áurea (PHI)
# ===============================================================
#
# Fórmulas:
#
#   r_{n+1} = r_n · PHI
#   θ_{n+1} = θ_n + ψ
#
#   x_n = r_n · cos(θ_n)
#   y_n = r_n · sin(θ_n)
#
#   s'_i = s_i · PHI
#
# Variables:
#
#   r_n     — radio en el paso n
#   θ_n     — ángulo en el paso n
#   ψ       — ángulo dorado (default ≈ 137.507764°)
#   PHI     — razón áurea (1 + √5)/2
#   (x_n,y_n)— punto de la espiral áurea
#   s_i     — valor de una serie a escalar
#
# Qué hace:
#   Construye la espiral áurea discreta (radio × PHI, giro ψ)
#   y escala series por PHI. Geometría de crecimiento autosimilar
#   del marco.
#
# ===============================================================

import math

from .constants import PHI

class PhiDynamics:
    @staticmethod
    def golden_spiral(radius: float, angle_step: float = 137.507764) -> list:
        """
        Computes the golden spiral points.
        
        radius: The initial radius.
        angle_step: Golden angle in degrees (default ≈ 137.5°).
        """
        points = []
        angle = 0
        for _ in range(100):  # Limit to 100 points for now
            x = radius * math.cos(math.radians(angle))
            y = radius * math.sin(math.radians(angle))
            points.append((x, y))
            angle += angle_step
            radius *= PHI  # Expand the radius using the golden ratio
        return points

    @staticmethod
    def phi_scaling(series: list) -> list:
        """
        Scales a given series based on the golden ratio.
        """
        return [value * PHI for value in series]
