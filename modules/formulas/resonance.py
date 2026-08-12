# ===============================================================
# modules/formulas/resonance.py
# ===============================================================
#
# Archivo de cálculo. No es el adaptador del módulo.
# No declara CONTENEDOR. No habla con Engine.
# No interpreta sentido. Solo calcula.
#
# Responsabilidad:
#   Implementar el algoritmo exacto de ρ (resonancia entre capas).
#
# Definición:
#   ρ mide qué tan bien resuenan las capas adyacentes entre sí.
#   ρ = 1 → resonancia perfecta
#   ρ = 0 → capas desconectadas
#
#   Por par adyacente (i, i+1):
#     magnitude    = 2·√(E_i·E_j) / (E_i + E_j)
#     phase_factor = (1 + cos(Δφ)) / 2
#     r_ij         = magnitude · phase_factor
#
#   ρ = media de r_ij sobre todos los pares adyacentes.
#
#   ν_i = Φ^(i/2)  frecuencia de la capa i (capas altas vibran más rápido).
#   Alineación de fase entre dos energías: min(E_i, E_j) / max(E_i, E_j).
#
# Criterio por línea:
#   ¿Cambia el resultado matemático de ρ o de ν_i?
#   Sí → pertenece aquí. No → no pertenece aquí.
#
# ===============================================================

from __future__ import annotations

import math
from typing import Any, Dict, List, Sequence

from .constants import PHI, NUM_LAYERS, GOLDEN_ANG_RAD

# ---------------------------------------------------------------
# FRECUENCIA DE CAPA
# ---------------------------------------------------------------
# ν_i = Φ^(i/2)
# La capa 0 vibra más lento; la capa superior más rápido.
# ---------------------------------------------------------------


def frecuencia_capa(layer_index: int) -> float:
    """ν_i = PHI^(i/2)."""
    return PHI ** (layer_index / 2)


# ---------------------------------------------------------------
# ALINEACIÓN DE FASE
# ---------------------------------------------------------------
# Entre dos energías: razón min/max.
# Si alguna es 0 → no hay alineación (0).
# ---------------------------------------------------------------


def alineacion_fase(e_i: float, e_j: float) -> float:
    """Phase alignment: min(E_i, E_j) / max(E_i, E_j)."""
    if e_i == 0.0 or e_j == 0.0:
        return 0.0
    return min(e_i, e_j) / max(e_i, e_j)


# ---------------------------------------------------------------
# RESONANCIA DE UN PAR
# ---------------------------------------------------------------
# r_ij = [2·√(E_i·E_j)/(E_i+E_j)] · [(1+cos(Δφ))/2]
# Si E_i = 0 o E_j = 0 → r_ij = 0.
# ---------------------------------------------------------------


def resonancia_par(
    e_i: float,
    e_j: float,
    phase_diff: float = 0.0,
) -> float:
    """Resonancia entre dos capas adyacentes."""
    if e_i == 0.0 or e_j == 0.0:
        return 0.0
    magnitude = 2.0 * math.sqrt(e_i * e_j) / (e_i + e_j)
    phase_factor = (1.0 + math.cos(phase_diff)) / 2.0
    return magnitude * phase_factor


# ---------------------------------------------------------------
# ρ GLOBAL
# ---------------------------------------------------------------
# Media de resonancia sobre todos los pares adyacentes.
# Si la suma de energías es 0 → ρ = 0.
# ---------------------------------------------------------------


def calcular(energies: Sequence[float]) -> Dict[str, Any]:
    """
    ρ = media de resonancia entre pares adyacentes.

    Entrada:  secuencia de energías por capa (E_0 … E_n).
    Salida:   dict con valor ρ y factores del cálculo.
    """
    if not energies or sum(energies) == 0.0:
        return {
            "ok": True,
            "valor": 0.0,
            "factores": {
                "n_capas": len(energies) if energies else 0,
                "n_pares": 0,
                "energies": list(energies) if energies else [],
            },
            "nota": (
                "ρ = 0: sin energía en capas o lista vacía. "
                "Definición: media de r_ij en pares adyacentes."
            ),
        }

    total = 0.0
    pares = 0
    detalle_pares: List[float] = []

    for i in range(len(energies) - 1):
        r = resonancia_par(float(energies[i]), float(energies[i + 1]))
        detalle_pares.append(r)
        total += r
        pares += 1

    rho = total / pares if pares > 0 else 0.0

    return {
        "ok": True,
        "valor": float(rho),
        "factores": {
            "n_capas": len(energies),
            "n_pares": pares,
            "energies": [float(e) for e in energies],
            "r_pares": detalle_pares,
        },
        "nota": (
            "ρ = media de r_ij; "
            "r_ij = [2·√(E_i·E_j)/(E_i+E_j)] · [(1+cos(Δφ))/2]. "
            "ρ=1 resonancia perfecta; ρ=0 capas desconectadas."
        ),
    }


# ---------------------------------------------------------------
# API DE COMPATIBILIDAD (misma lógica, nombres previos)
# ---------------------------------------------------------------

class ResonanceLogic:
    """
    Inter-layer Resonance (rho).
    rho = 1: perfect resonance
    rho = 0: layers disconnected
    """

    @staticmethod
    def calculate_layer_frequency(layer_index: int) -> float:
        return frecuencia_capa(layer_index)

    @staticmethod
    def calculate_phase_alignment(e_i: float, e_j: float) -> float:
        return alineacion_fase(e_i, e_j)

    @staticmethod
    def pair_resonance(
        e_i: float,
        e_j: float,
        phase_diff: float = 0.0,
    ) -> float:
        return resonancia_par(e_i, e_j, phase_diff)

    @staticmethod
    def compute(energies: Sequence[float]) -> float:
        return float(calcular(energies)["valor"])


# ---------------------------------------------------------------
# EXPORTACIONES
# ---------------------------------------------------------------

__all__ = [
    "frecuencia_capa",
    "alineacion_fase",
    "resonancia_par",
    "calcular",
    "ResonanceLogic",
]

# ===============================================================
# FIN
# ===============================================================
