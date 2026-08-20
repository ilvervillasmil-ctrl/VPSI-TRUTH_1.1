# ===============================================================
# modules/formulas/formulas_omega/yo_oscilatorio_FO.py
# ===============================================================
#
# VPSI-TRUTH — L4 — YO OSCILATORIO DINÁMICO
#
# RESPONSABILIDAD:
#   Implementar exclusivamente la matemática de la dinámica continua
#   del carril del Yo Oscilatorio (L4): aceleración θ̈_Y, velocidad θ̇_Y,
#   posición θ_Y, fuerzas F_Y, equilibrio θ_eq y amortiguamiento φ_Y.
#
# ESTE ARCHIVO:
#   - No declara CONTENEDOR.
#   - No habla con Engine.
#   - No interpreta contexto.
#   - No asigna θ_Y = L4, L5 o L6.
#   - No calcula el mapa posterior de casas (Fase 2).
#   - No decide el significado psicológico o epistemológico del resultado.
#
# ===============================================================
# DEFINICIONES MATEMÁTICAS
# ===============================================================
#
# Ecuación maestra de movimiento (Ecuación Diferencial Ordinaria):
#
#   d²θ_Y / dt² + φ_Y(t) · (dθ_Y / dt) + π² · (θ_Y(t) - θ_eq(t)) = F_Y(t)
#
# Despejada (Aceleración):
#
#   θ̈_Y = F_Y - φ_Y · θ̇_Y - π² · (θ_Y - θ_eq)
#
# Integración numérico-temporal (Euler Semi-Implícito):
#
#   θ̈ = F_Y - φ_Y · θ̇_Y - π² · (θ_Y - θ_eq)
#   θ̇(t + dt) = θ̇(t) + θ̈ · dt
#   θ(t + dt) = θ(t) + θ̇(t + dt) · dt
#
# Energías operacionales y pesos emergentes (6 capas internas L1..L6):
#
#   E_i = L_i · (1 - φ_i) · ν_i
#   ν_i = Φ^(i/2)
#   w_i = E_i / Σ_j E_j   (si Σ_j E_j = 0 → w_i = 1/6)
#
# Propiedades derivadas emergentes:
#
#   Entropía de pesos:
#     S = -Σ_i w_i · ln(w_i)   (para w_i > 0)
#
#   Amortiguamiento efectivo del Yo:
#     φ_Y = Σ_i w_i · φ_i      (con φ_6 = 0)
#     ζ_Y = φ_Y / (2π)         (amortiguamiento adimensional)
#     ω_Y = π · √(1 - ζ_Y²)    (para ζ_Y < 1; 0 si ζ_Y ≥ 1)
#
# Geometría dinámica del atractor de equilibrio:
#
#   θ_eq(t) = θ_cube + Δθ_coh(t) + Δθ_w(t)
#   Δθ_coh  = β · ((C_Ω / α) - 1) · (π / 27)
#   Δθ_w    = β · (w_alto - w_bajo) · (π / 54)
#   con w_alto = (w_4 + w_5 + w_6) / 3,  w_bajo = (w_1 + w_2) / 2
#
# Componentes de la fuerza total F_Y(t):
#
#   F_Y = F_L0 + F_L5 + F_L6 + F_β + F_COH
#
#   F_L0  = scale_L0 · L0
#   F_L5  = ρ · P_t · C_Ω + 0.5 · ΔC_Ω - β · (S / ln(6))
#   F_L6  = w_6 · P
#   F_β   = β · (1 - exp(-N / k))
#   F_COH = C_Ω · ΔC_Ω
#
# ===============================================================
# VARIABLES
# ===============================================================
#
# θ_Y, θ̇_Y      posición y velocidad continua del carril    [rad], [rad/s]
# L_i, φ_i     activaciones y fricción de las capas L1..L6 [0, 1]
# L0           entrada externa/forzamiento                 [0, 1]
# P            magnitud computable de dirección/propósito [0, 1]
# C_Ω, ΔC_Ω    coherencia global y su tasa de variación    [0, α]
# S            entropía de distribución energética        [0, ln(6)]
# N, k         novedad y escala de sensibilidad            adimensional
# dt           paso temporal de integración               [s]
# α, β, Φ      constantes estructurales (constants.py)
#
# ===============================================================
# DOMINIO Y RESTRICCIONES
# ===============================================================
#
#   L_i, φ_i ∈ [0, 1]
#   φ_6 = 0 (invariante: L6 no aporta fricción propia)
#   dt > 0
#   C_Ω ∈ [0, α]
#   Si Σ E_i == 0, w_i = 1/6 (evita división por cero)
#
# ===============================================================
# CASOS LÍMITE
# ===============================================================
#
#   todas L_i = 0        → E_i = 0 → w_i = 1/6 → φ_Y = Σ(1/6·φ_i)
#   ζ_Y ≥ 1              → régimen sobreamortiguado → ω_Y = 0
#   ΔC_Ω = 0             → F_COH = 0 (fuerza de coherencia estática es nula)
#   N = 0                → F_β = 0
#
# ===============================================================
from __future__ import annotations

import math
from typing import Dict, List, Optional, Tuple, Any

# ===============================================================
# SEMILLA (única autoridad)
# ===============================================================
from modules.constante import ALPHA, BETA

# ===============================================================
# DERIVADAS (formulas_omega.constants)
# ===============================================================
from modules.formulas.formulas_omega.constants import (
    C_MAX,
    PHI,
    THETA_CUBE,
    NUM_LAYERS,
    LAYER_FRICTION,
)

# Constante del umbral de amortiguamiento crítico (2π)
PHI_CRITICAL = 2.0 * math.pi
S_MAX = math.log(NUM_LAYERS)  # ln(6)


class YoOscilatorioEngine:
    """
    Calculador matemático estático para la dinámica instantánea del
    Yo Oscilatorio Dinámico (L4).
    """

    @staticmethod
    def compute_energies_and_weights(
        activations: List[float],
        frictions: Optional[List[float]] = None
    ) -> Tuple[List[float], List[float]]:
        """
        Calcula las energías operacionales E_i y los pesos emergentes w_i.
        """
        if frictions is None:
            frictions = LAYER_FRICTION

        energies = []
        for i in range(NUM_LAYERS):
            layer_idx = i + 1
            nu_i = PHI ** (layer_idx / 2.0)
            e_i = activations[i] * (1.0 - frictions[i]) * nu_i
            energies.append(e_i)

        total_energy = sum(energies)
        if total_energy > 0.0:
            weights = [e / total_energy for e in energies]
        else:
            weights = [1.0 / NUM_LAYERS] * NUM_LAYERS

        return energies, weights

    @staticmethod
    def compute_entropy(weights: List[float]) -> Dict[str, float]:
        """
        Calcula la entropía de Shannon S, entropía normalizada y negentropía.
        """
        s = 0.0
        for w in weights:
            if w > 0.0:
                s -= w * math.log(w)

        s_norm = s / S_MAX if S_MAX > 0 else 0.0
        n_neg = 1.0 - s_norm

        return {
            "s": s,
            "s_norm": s_norm,
            "negentropy": n_neg
        }

    @staticmethod
    def compute_damping_and_frequency(
        weights: List[float],
        frictions: Optional[List[float]] = None
    ) -> Dict[str, float]:
        """
        Calcula el amortiguamiento efectivo φ_Y, adimensional ζ_Y y frecuencia ω_Y.
        """
        if frictions is None:
            frictions = LAYER_FRICTION

        # Invariante: φ_6 = 0
        effective_frictions = list(frictions)
        if len(effective_frictions) >= 6:
            effective_frictions[5] = 0.0

        phi_Y = sum(w * f for w, f in zip(weights, effective_frictions))
        zeta_Y = phi_Y / PHI_CRITICAL

        if zeta_Y < 1.0:
            omega_Y = math.pi * math.sqrt(1.0 - (zeta_Y ** 2))
            regime = "SUBDAMPED"
        elif abs(zeta_Y - 1.0) < 1e-6:
            omega_Y = 0.0
            regime = "CRITICAL"
        else:
            omega_Y = 0.0
            regime = "OVERDAMPED"

        return {
            "phi_Y": phi_Y,
            "zeta_Y": zeta_Y,
            "omega_Y": omega_Y,
            "regime": regime
        }

    @staticmethod
    def compute_theta_eq(
        c_omega: float,
        weights: List[float]
    ) -> Dict[str, float]:
        """
        Calcula el punto de equilibrio geométrico instantáneo θ_eq(t).
        """
        delta_theta_coh = BETA * ((c_omega / ALPHA) - 1.0) * (math.pi / 27.0)

        # Desbalance energético entre capas altas (L4..L6) y bajas (L1..L2)
        w_alto = sum(weights[3:6]) / 3.0 if len(weights) >= 6 else 0.0
        w_bajo = sum(weights[0:2]) / 2.0 if len(weights) >= 2 else 0.0
        delta_theta_w = BETA * (w_alto - w_bajo) * (math.pi / 54.0)

        theta_eq = THETA_CUBE + delta_theta_coh + delta_theta_w

        return {
            "theta_eq": theta_eq,
            "delta_theta_coh": delta_theta_coh,
            "delta_theta_w": delta_theta_w,
            "theta_cube": THETA_CUBE
        }

    @staticmethod
    def compute_forces(
        l0_input: float,
        weights: List[float],
        c_omega: float,
        delta_c_omega: float,
        entropy: float,
        purpose_p: float = 0.0,
        rho: float = 1.0,
        p_t: float = 1.0,
        novelty: float = 0.0,
        sensitivity: float = 5.0,
        scale_l0: float = 1.0
    ) -> Dict[str, float]:
        """
        Calcula las fuerzas componentes y la fuerza total F_Y(t).
        """
        f_l0 = scale_l0 * l0_input

        # F_L5: retroalimentación metaestructural
        entropy_term = (entropy / S_MAX) if S_MAX > 0 else 0.0
        f_l5 = (rho * p_t * c_omega) + (0.5 * delta_c_omega) - (BETA * entropy_term)

        # F_L6: fuerza de dirección / propósito (w_6 * P)
        w6 = weights[5] if len(weights) >= 6 else 0.0
        f_l6 = w6 * purpose_p

        # F_β: fuerza de margen de novedad
        a_n = 1.0 - math.exp(-max(0.0, novelty) / max(1e-6, sensitivity))
        f_beta = BETA * a_n

        # F_COH: retroalimentación de coherencia dinámico-temporal
        f_coh = c_omega * delta_c_omega

        f_total = f_l0 + f_l5 + f_l6 + f_beta + f_coh

        return {
            "f_total": f_total,
            "f_l0": f_l0,
            "f_l5": f_l5,
            "f_l6": f_l6,
            "f_beta": f_beta,
            "f_coh": f_coh
        }

    @classmethod
    def step(
        cls,
        theta_Y: float,
        theta_dot_Y: float,
        activations: List[float],
        l0_input: float,
        c_omega: float,
        delta_c_omega: float,
        frictions: Optional[List[float]] = None,
        purpose_p: float = 0.0,
        rho: float = 1.0,
        p_t: float = 1.0,
        novelty: float = 0.0,
        sensitivity: float = 5.0,
        dt: float = 0.01,
        scale_l0: float = 1.0
    ) -> Dict[str, Any]:
        """
        Ejecuta un paso de integración numérico (Euler Semi-Implícito) para θ_Y.
        """
        energies, weights = cls.compute_energies_and_weights(activations, frictions)
        entropy_data = cls.compute_entropy(weights)
        damping_data = cls.compute_damping_and_frequency(weights, frictions)
        geom_data = cls.compute_theta_eq(c_omega, weights)
        forces_data = cls.compute_forces(
            l0_input=l0_input,
            weights=weights,
            c_omega=c_omega,
            delta_c_omega=delta_c_omega,
            entropy=entropy_data["s"],
            purpose_p=purpose_p,
            rho=rho,
            p_t=p_t,
            novelty=novelty,
            sensitivity=sensitivity,
            scale_l0=scale_l0
        )

        phi_Y = damping_data["phi_Y"]
        theta_eq = geom_data["theta_eq"]
        f_total = forces_data["f_total"]

        # Ecuación Maestra despejada para aceleración θ̈_Y
        restoration = (math.pi ** 2) * (theta_Y - theta_eq)
        theta_ddot = f_total - (phi_Y * theta_dot_Y) - restoration

        # Integración Euler Semi-Implícito
        new_theta_dot = theta_dot_Y + (theta_ddot * dt)
        new_theta = theta_Y + (new_theta_dot * dt)

        return {
            "theta_Y": new_theta,
            "theta_dot_Y": new_theta_dot,
            "theta_ddot_Y": theta_ddot,
            "energies": energies,
            "weights": weights,
            "entropy": entropy_data,
            "damping": damping_data,
            "geometry": geom_data,
            "forces": forces_data,
            "dt": dt
        }


class SessionStateYoOscilatorio:
    """
    Gestiona la trayectoria temporal del carril continuo del Yo Oscilatorio (L4).
    """

    def __init__(self, initial_theta: float = THETA_CUBE, initial_theta_dot: float = 0.0):
        self.theta_Y = initial_theta
        self.theta_dot_Y = initial_theta_dot
        self.prev_c_omega: Optional[float] = None
        self.history: List[Dict[str, Any]] = []

    def update(
        self,
        activations: List[float],
        l0_input: float,
        c_omega: float,
        frictions: Optional[List[float]] = None,
        purpose_p: float = 0.0,
        rho: float = 1.0,
        p_t: float = 1.0,
        novelty: float = 0.0,
        sensitivity: float = 5.0,
        dt: float = 0.01,
        scale_l0: float = 1.0
    ) -> Dict[str, Any]:
        """
        Actualiza el estado continuo del carril dado el nuevo paso temporal.
        """
        if self.prev_c_omega is None:
            delta_c_omega = 0.0
        else:
            delta_c_omega = c_omega - self.prev_c_omega

        result = YoOscilatorioEngine.step(
            theta_Y=self.theta_Y,
            theta_dot_Y=self.theta_dot_Y,
            activations=activations,
            l0_input=l0_input,
            c_omega=c_omega,
            delta_c_omega=delta_c_omega,
            frictions=frictions,
            purpose_p=purpose_p,
            rho=rho,
            p_t=p_t,
            novelty=novelty,
            sensitivity=sensitivity,
            dt=dt,
            scale_l0=scale_l0
        )

        self.theta_Y = result["theta_Y"]
        self.theta_dot_Y = result["theta_dot_Y"]
        self.prev_c_omega = c_omega

        self.history.append(result)
        return result

    def trajectory(self) -> List[float]:
        """Retorna la serie temporal completa de posiciones θ_Y(t)."""
        return [e["theta_Y"] for e in self.history]

    def velocity_trajectory(self) -> List[float]:
        """Retorna la serie temporal completa de velocidades θ̇_Y(t)."""
        return [e["theta_dot_Y"] for e in self.history]
