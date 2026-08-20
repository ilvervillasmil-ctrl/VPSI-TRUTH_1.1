# ===============================================================
# formulas_omega/fractality.py — Fractalidad y distribución áurea
# ===============================================================
#
# Fórmulas:
#
#   D(level) = level · ln(base)     (base = PHI por defecto)
#
#   E_{n+1} = E_n / PHI
#   E_n restante se reparte en iteraciones fractales
#
# Variables:
#
#   level       — nivel de recursión fractal (≥ 1)
#   base        — factor de escala (PHI)
#   total_energy— energía total a repartir (> 0)
#   iterations  — número de niveles fractales (≥ 1)
#   E_i         — energía del nivel i
#
# Qué hace:
#   Dimensiona la recursión fractal con PHI y reparte energía
#   en cascada áurea: cada nivel toma 1/PHI de lo restante.
#   Estructura de escala autosimilar del motor.
#
# ===============================================================

import math
from .constants import PHI


class Fractality:
    @staticmethod
    def calculate_fractal_dimension(level: int, base: float = PHI) -> float:
        """
        Computes the fractal dimension based on the level and the base factor.

        level: Fractal recursion level.
        base: Scaling factor (default is PHI).
        """
        if level < 1:
            raise ValueError("Level must be at least 1.")
        return level * math.log(base)

    @staticmethod
    def fractal_energy_distribution(total_energy: float, iterations: int) -> list:
        """
        Distributes energy across fractal levels.

        total_energy: Total energy to distribute.
        iterations: Number of fractal levels.
        """
        if total_energy <= 0 or iterations < 1:
            raise ValueError("Invalid energy or iteration count.")

        energies = []
        remaining_energy = total_energy
        for _ in range(iterations):
            _energy = remaining_energy / PHI
            energies.append(_energy)
            remaining_energy -= _energy

        return energies
