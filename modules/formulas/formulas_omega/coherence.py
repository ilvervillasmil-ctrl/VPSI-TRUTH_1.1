# ===============================================================
# modules/formulas/formulas_omega/coherence.py
# ===============================================================
#
# VPSI-TRUTH — COHERENCE
#
# RESPONSABILIDAD:
#   Implementar exclusivamente la matemática de C_Ω, C_β, C_α,
#   C_total y la trayectoria temporal asociada.
#
# ESTE ARCHIVO:
#   - No declara CONTENEDOR.
#   - No habla con Engine.
#   - No interpreta contexto.
#   - No calcula Tru.
#   - No modifica la definición matemática.
#   - No decide el significado epistemológico del resultado.
#
# ===============================================================
# DEFINICIONES MATEMÁTICAS
# ===============================================================
#
# Energía de capa (delegada a energy.py):
#
#   E_i = L_i · (1 - φ_i) · ν_i
#   ν_i = Φ^(i/2)
#
# Producto normalizado de capas:
#
#   P_raw = Π_i (E_i / E_0)
#   P_max = Π_i (E_i^max / E_0)
#   P_norm = P_raw / P_max
#
#   con E_i^max = 1 · (1 - φ_i) · ν_i
#
# Fórmula maestra C_β (= C_Ω operativa):
#
#   C_β = P_norm · (α/S) · R_fin · ρ · P_t · A · I_ext
#
#   C_Ω = clamp(C_β, 0, C_MAX)
#   C_MAX = α = 26/27
#
# C_α:
#
#   C_α = (I · Q) / (Cpx + U + β)
#
#   I   = integration
#   Q   = quality
#   Cpx = complexity
#   U   = uncertainty
#   β   = 1/27  (piso estructural; u_min)
#
# C_total (métrica interna; no determina C_Ω):
#
#   C_total = √(C_β² + C_α²)
#   θ_actual = atan(C_β / C_α)   (si C_α > 0)
#   θ_dev    = θ_actual - θ_cube
#
# C_Ω básica (variante):
#
#   C_Ω_basic = α · H + β · I_ext
#   H = armonía = negentropía sobre energías
#
# Códigos de diagnóstico (por umbral sobre C_Ω):
#
#   C_Ω ≥ α     → CODE_INTEGRATED
#   C_Ω ≥ 0.4   → CODE_SATURATION
#   C_Ω < 0.4   → CODE_ENTROPY
#
# Bucle temporal (CODE_LOOP):
#
#   C_Ω > LOOP_THRESHOLD durante LOOP_WINDOW ciclos
#   y (max - min) < LOOP_VARIANCE
#   LOOP_VARIANCE = β
#
# ===============================================================
# VARIABLES
# ===============================================================
#
# L_i, φ_i     activación y fricción de la capa i          [0,1]
# E_i          energía de la capa i                        adimensional
# E_0          energía de referencia (capa 0 a L=1, φ=φ_0)
# P_raw        producto de E_i/E_0
# P_norm       producto normalizado por P_max
# ρ            resonancia inter-capas (resonance.py)
# P_t          presencia temporal (presence.py)
# A            wonder / asombro (wonder.py)
# I_ext        coherencia externa (interaction.py)
# α, β, S, R_fin, Φ, θ_cube, C_MAX, KAPPA
#              constantes estructurales (constants.py)
#
# ===============================================================
# DOMINIO Y RESTRICCIONES
# ===============================================================
#
#   L_i, φ_i ∈ [0, 1]
#   C_Ω ∈ [0, C_MAX]
#   β > 0  (ningún sistema real es estáticamente perfecto)
#   denominador de C_α > 0  (garantizado por + β)
#   E_0 > 0 para el cociente E_i/E_0
#
# ===============================================================
# CASOS LÍMITE
# ===============================================================
#
#   todas L_i = 0        → P_raw = 0 → C_β = 0 → C_Ω = 0
#   E_0 = 0              → cociente definido como 0 (no división)
#   C_α = 0, C_β > 0     → θ_actual = π/2
#   C_α = 0, C_β = 0     → θ_actual = 0
#   history < window     → detect_loop = False
#
# ===============================================================
from __future__ import annotations

import math

# ===============================================================
# SEMILLA (única autoridad)
# ===============================================================
from modules.constante import ALPHA, BETA

# ===============================================================
# DERIVADAS (formulas_omega.constants)
# ===============================================================
from modules.formulas.formulas_omega.constants import (
    C_MAX,
    R_FIN,
    S_REF,
    KAPPA,
    THETA_CUBE,
    ALPHA_OVER_S,
    NUM_LAYERS,
    LAYER_FRICTION,
    CODE_INTEGRATED,
    CODE_SATURATION,
    CODE_ENTROPY,
    PHI,
    CODE_LOOP,
    LOOP_THRESHOLD,
    LOOP_WINDOW,
    LOOP_VARIANCE,
    T_PERIOD,
)

# ===============================================================
# MÓDULOS HERMANOS (formulas_omega)
# ===============================================================
from .energy import LayerEnergy
from .negentropy import NegentropyCalculator
from .presence import PresenceLogic
from .wonder import WonderLogic
from .interaction import ExternalInteraction
from .resonance import ResonanceLogic
from .metaconsciousness import MetaconsciousnessCalculator


_E0_REF = LayerEnergy.frequency(0)

_PRODUCTO_MAX = 1.0
for _i in range(NUM_LAYERS):
    _E_max_i = 1.0 * (1.0 - LAYER_FRICTION[_i]) * LayerEnergy.frequency(_i)
    _PRODUCTO_MAX *= _E_max_i

C_BETA_MAX = ALPHA_OVER_S * R_FIN


class SessionStateOmega:
    """
    Coherence as a trajectory, not a static number.

    NEW v3.2:
      - Each interaction updates the state and stores it in history.
      - trajectory() returns the full C_Ω(t) series.
      - detect_loop() identifies CODE_LOOP (9999): C_Ω > threshold
        with no variation for LOOP_WINDOW consecutive cycles.
        β > 0 guarantees no real system is statically perfect.
        If C_Ω does not vary, the system is in a loop.
    """

    def __init__(self, tau=60.0):
        self.tau = tau
        self.history = []

    def update(self, activations, frictions=None, external_coherences=None,
               integration=0.5, quality=0.5, complexity=1.0, uncertainty=0.1):
        result = CoherenceEngine.full_analysis(
            activations=activations,
            frictions=frictions,
            integration=integration,
            quality=quality,
            complexity=complexity,
            uncertainty=uncertainty,
            external_coherences=external_coherences,
        )
        self.history.append(result)
        return result["c_omega"]

    def trajectory(self):
        """Returns the full C_Ω(t) series as a list of floats."""
        return [e["c_omega"] for e in self.history]

    def detect_loop(self, window=LOOP_WINDOW, threshold=LOOP_THRESHOLD):
        """
        Detects CODE_LOOP (9999): temporal loop.

        A system is in a loop when C_Ω > threshold with variance
        smaller than BETA for `window` consecutive cycles.

        Returns:
            bool: True if loop detected, False otherwise.
        """
        if len(self.history) < window:
            return False
        recent = self.trajectory()[-window:]
        variance = max(recent) - min(recent)
        return all(c > threshold for c in recent) and variance < LOOP_VARIANCE

    def session_balance(self):
        """
        Returns the balance state of the last recorded entry.

        NEW v3.2: exposes the theta balance from compute_c_total.
        Returns:
            str: 'CENTERED' | 'EXCESS_EXPERIENCE' | 'EXCESS_MEASUREMENT'
                 or 'NO_DATA' if history is empty.
        """
        if not self.history:
            return "NO_DATA"
        last = self.history[-1]
        return last.get("c_total", {}).get("balance", "NO_DATA")

    def c_omega_trajectory(self):
        """
        Alias for trajectory() with explicit name.
        Coherence is a trajectory, not a snapshot.
        """
        return self.trajectory()


class CoherenceEngine:
    PRODUCTO_MAX = _PRODUCTO_MAX
    C_BETA_MAX   = C_BETA_MAX

    @staticmethod
    def compute_c_beta(
        activations,
        frictions=None,
        rho=1.0,
        delta_t=0.0,
        tau=1.0,
        novelty=5.0,
        sensitivity=5.0,
        external_coherences=None,
    ):
        if frictions is None:
            frictions = LAYER_FRICTION

        energies = LayerEnergy.compute_all(activations, frictions)

        producto_raw = 1.0
        for e in energies:
            producto_raw *= (e / _E0_REF) if _E0_REF > 0 else 0.0

        producto_norm = producto_raw / _PRODUCTO_MAX

        p_t   = PresenceLogic.compute(delta_t, tau)
        a     = WonderLogic.compute(novelty, sensitivity)

        if external_coherences and len(external_coherences) > 0:
            i_ext = ExternalInteraction.compute_multi(external_coherences)
        else:
            i_ext = 1.0

        c_beta = producto_norm * ALPHA_OVER_S * R_FIN * rho * p_t * a * i_ext

        return {
            "c_beta":        c_beta,
            "energies":      energies,
            "product":       producto_norm,
            "producto_raw":  producto_raw,
            "producto_norm": producto_norm,
            "producto_max":  _PRODUCTO_MAX,
            "alpha_over_s":  ALPHA_OVER_S,
            "r_fin":         R_FIN,
            "rho":           rho,
            "p_t":           p_t,
            "wonder":        a,
            "i_ext":         i_ext,
        }

    @staticmethod
    def compute_c_alpha(integration, quality, complexity, uncertainty):
        u_min       = BETA
        denominator = complexity + uncertainty + u_min
        c_alpha     = (integration * quality) / denominator if denominator > 0 else 0.0

        return {
            "c_alpha":     c_alpha,
            "integration": integration,
            "quality":     quality,
            "complexity":  complexity,
            "uncertainty": uncertainty,
            "u_min":       u_min,
        }

    @staticmethod
    def compute_c_total(c_beta, c_alpha):
        c_total = math.sqrt(c_beta ** 2 + c_alpha ** 2)

        if c_alpha > 0:
            theta_actual = math.atan(c_beta / c_alpha)
        elif c_beta > 0:
            theta_actual = math.pi / 2
        else:
            theta_actual = 0.0

        theta_deviation = theta_actual - THETA_CUBE

        if abs(theta_deviation) < 0.01:
            balance = "CENTERED"
        elif theta_deviation > 0:
            balance = "EXCESS_EXPERIENCE"
        else:
            balance = "EXCESS_MEASUREMENT"

        c_beta_ideal  = c_total * math.sin(THETA_CUBE)
        c_alpha_ideal = c_total * math.cos(THETA_CUBE)

        return {
            "c_total":              c_total,
            "c_beta":               c_beta,
            "c_alpha":              c_alpha,
            "theta_actual":         theta_actual,
            "theta_actual_deg":     math.degrees(theta_actual),
            "theta_cube":           THETA_CUBE,
            "theta_cube_deg":       math.degrees(THETA_CUBE),
            "theta_deviation":      theta_deviation,
            "theta_deviation_deg":  math.degrees(theta_deviation),
            "balance":              balance,
            "c_beta_ideal":         c_beta_ideal,
            "c_alpha_ideal":        c_alpha_ideal,
        }

    @staticmethod
    def compute_basic(energies, i_ext=1.0):
        harmony = NegentropyCalculator.harmony(energies)
        c_omega = ALPHA * harmony + BETA * i_ext
        return {"c_omega": c_omega, "harmony": harmony, "i_ext": i_ext}

    @staticmethod
    def full_analysis(
        activations,
        frictions=None,
        rho=1.0,
        delta_t=0.0,
        tau=1.0,
        novelty=5.0,
        sensitivity=5.0,
        external_coherences=None,
        integration=0.5,
        quality=0.5,
        complexity=1.0,
        uncertainty=0.1,
    ):
        if frictions is None:
            frictions = LAYER_FRICTION

        beta_r  = CoherenceEngine.compute_c_beta(
            activations, frictions, rho, delta_t, tau,
            novelty, sensitivity, external_coherences
        )
        alpha_r = CoherenceEngine.compute_c_alpha(
            integration, quality, complexity, uncertainty
        )
        total_r = CoherenceEngine.compute_c_total(
            beta_r["c_beta"], alpha_r["c_alpha"]
        )

        energies = beta_r["energies"]
        mc       = MetaconsciousnessCalculator.compute(activations, frictions)

        # MASTER FORMULA: C_Ω = [∏(Eᵢ/E₀)] * (α/S) * R * ρ * P_t * A * I_ext
        # c_beta ya es la Master Formula completa.
        # c_total y c_alpha son métricas internas — no determinan c_omega.
        c_omega = min(C_MAX, max(0.0, beta_r["c_beta"]))

        if c_omega >= ALPHA:
            code, name = CODE_INTEGRATED, "Integrated Architect"
        elif c_omega >= 0.4:
            code, name = CODE_SATURATION, "Critical Saturation"
        else:
            code, name = CODE_ENTROPY, "Terminal Entropy"

        return {
            "c_beta":            beta_r,
            "c_alpha":           alpha_r,
            "c_total":           total_r,
            "c_omega":           c_omega,
            "negentropy":        NegentropyCalculator.compute(energies),
            "metaconsciousness": mc,
            "mc_level":          MetaconsciousnessCalculator.level_name(mc),
            "resonance":         ResonanceLogic.compute(energies),
            "diagnostic_code":   code,
            "diagnostic_name":   name,
            "four_pillars": {
                "beta":       BETA,
                "kappa":      KAPPA,
                "alpha":      ALPHA,
                "emergence":  sum(energies) * (1 - KAPPA) / 2,
            },
        }

    @staticmethod
    def metacube_level(c_total, level=0):
        return {
            "level":             level,
            "c_total_here":      c_total,
            "is_beta_of_level":  level + 1,
            "ratio_alpha_beta":  ALPHA / BETA,
        }
