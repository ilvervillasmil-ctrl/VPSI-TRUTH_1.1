# ===============================================================
# formulas_omega/integration_laws.py — Ley de integración Ω
# ===============================================================
#
# Fórmulas:
#
#   Ω = (α / S_REF) · (1 + β)
#
#   colapso  ⇔  integración < umbral
#   umbral por defecto = α
#
# Variables:
#
#   α      — ALPHA (26/27)  fracción observable del cubo
#   β      — BETA  (1/27)   residuo interior irreducible
#   S_REF  — referencia de escala (e/π en el marco)
#   Ω      — ley de integración estructural
#   umbral — piso bajo el cual el sistema se considera en colapso
#
# Qué hace:
#   Cuantifica la integración global del sistema a partir de la
#   semilla (α, β) y la escala de referencia. Detecta colapso
#   cuando la integración cae por debajo de α.
#
# ===============================================================

from modules.constante import ALPHA, BETA
from .constants import S_REF

class IntegrationLaws:
    @staticmethod
    def calculate_omega_law(alpha: float, beta: float, s_ref: float) -> float:
        """
        Calculates the integration law (Law Ω) using the constants:
        Formula: Ω = (α / S_REF) * (1 + β)

        alpha: ALPHA constant.
        beta: BETA constant.
        s_ref: S_REF constant.
        """
        return (alpha / s_ref) * (1 + beta)

    @staticmethod
    def system_collapse_integration(integration: float, threshold: float = ALPHA) -> bool:
        """
        Checks if the system is collapsing based on its integration level.
        Collapse occurs when integration < threshold.
        """
        return integration < threshold
