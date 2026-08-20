# ===============================================================
# formulas_omega/presence.py — Presencia temporal
# ===============================================================
#
# Fórmulas:
#
#   P_t = 1 / (1 + |Δt|)
#
#   P_t = e^(-|Δt| / τ)
#
# Donde:
#   Δt  = desplazamiento mental respecto al ahora
#         (ansiedad → futuro, depresión → pasado)
#   τ   = ancho de la ventana de atención
#
# ===============================================================

import math

import math


class PresenceLogic:
    """
    Temporal Presence

    compute_pt: P_t = 1 / (1 + |delta_t|)
    compute:    P_t = e^(-|delta_t|/tau)

    delta_t = mental displacement from now
    tau = attention window width
    """

    @staticmethod
    def compute_pt(delta_t):
        """P_t = 1 / (1 + |delta_t|)"""
        return 1.0 / (1.0 + abs(delta_t))

    @staticmethod
    def compute(delta_t, tau=1.0):
        """P_t = e^(-|delta_t|/tau)"""
        return math.exp(-abs(delta_t) / max(tau, 0.001))

    @staticmethod
    def from_state(anxiety=0, depression=0, mindfulness=1.0):
        """
        Compute from human-readable values (0-10 scales).

        anxiety: how much the mind is in the future
        depression: how much the mind is in the past
        mindfulness: width of attention (meditation expands)
        """
        delta_t = max(anxiety, depression)
        tau = max(0.1, mindfulness)
        return PresenceLogic.compute(delta_t, tau)


TemporalPresence = PresenceLogic
