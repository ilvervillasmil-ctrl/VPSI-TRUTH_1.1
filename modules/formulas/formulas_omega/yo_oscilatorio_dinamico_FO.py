# ===============================================================
# modules/formulas/formulas_omega/yo_oscilatorio_dinamico_FO.py
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
# ESTRUCTURA DE CAPAS
# ===============================================================
#
#   L0 — CAOS / ENTRADA EXTERNA
#        No pertenece al conjunto de capas internas de L4.
#        Puede actuar como entrada o forzamiento externo F_L0.
#
#   L1..L6 — SEIS CAPAS INTERNAS DEL SISTEMA
#        Son las únicas capas que participan en la distribución
#        energética interna del carril L4.
#
#        {L1, L2, L3, L4, L5, L6}
#
#        NUM_LAYERS = 6
#
#   L7 — EMERGENCIA
#        No es una octava capa interna utilizada por L4.
#        Representa la emergencia resultante de la integración del
#        sistema completo y constituye una salida/resultante posterior.
#        L7 NO entra en:
#          - E_i
#          - w_i
#          - S
#          - φ_Y
#          - Π f_i
#          - la distribución energética interna de L4.
#
#   Por tanto, para este módulo:
#
#        L0  → entrada / forzamiento externo
#        L1..L6 → dinámica interna
#        L7  → emergencia / resultado de integración
#
#   El carril de L4 no confunde las ocho posiciones conceptuales con
#   ocho capas internas. Su espacio energético interno está compuesto
#   exclusivamente por las seis capas L1..L6.
#
# ===============================================================
# DEFINICIONES MATEMÁTICAS
# ===============================================================
#
# Ecuación maestra de movimiento (Ecuación Diferencial Ordinaria):
#
#   d²θ_Y / dt² + φ_Y(t) · (dθ_Y / dt) + π² · (θ_Y(t) − θ_eq(t)) = F_Y(t)
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
# ===============================================================
# ENERGÍAS OPERACIONALES Y PESOS EMERGENTES
# ===============================================================
#
# Las energías y pesos internos se calculan exclusivamente sobre
# las seis capas internas L1..L6.
#
#   i ∈ {1,2,3,4,5,6}
#
#   E_i = L_i · (1 - φ_i) · ν_i
#
#   ν_i = Φ^(i/2)
#
#   w_i = E_i / Σ_j E_j
#
#   donde j ∈ {1,2,3,4,5,6}.
#
# Si:
#
#   Σ_j E_j = 0
#
# entonces:
#
#   w_i = 1/6
#
# para cada una de las seis capas internas.
#
# L0 no participa de esta normalización.
# L7 no participa de esta normalización.
#
# ===============================================================
# PROPIEDADES DERIVADAS EMERGENTES
# ===============================================================
#
# Entropía de pesos:
#
#   S = -Σ_i w_i · ln(w_i)
#
#   para w_i > 0
#
#   i ∈ {1,2,3,4,5,6}
#
# Entropía máxima del espacio interno:
#
#   S_MAX = ln(6)
#
# Amortiguamiento efectivo del Yo:
#
#   φ_Y = Σ_i w_i · φ_i
#
#   con:
#
#   φ_6 = 0
#
#   L6 no introduce fricción propia en el amortiguamiento efectivo.
#
# Amortiguamiento adimensional:
#
#   ζ_Y = φ_Y / (2π)
#
# Frecuencia amortiguada:
#
#   ω_Y = π · √(1 - ζ_Y²)
#
#   para ζ_Y < 1.
#
#   Si ζ_Y ≥ 1:
#
#   ω_Y = 0
#
# ===============================================================
# GEOMETRÍA DINÁMICA DEL ATRACTOR DE EQUILIBRIO
# ===============================================================
#
# El atractor geométrico θ_cube constituye la referencia base.
# El equilibrio del carril puede desplazarse dinámicamente según
# el estado instantáneo de la integración interna.
#
#   θ_eq(t) = θ_cube + Δθ_coh(t) + Δθ_w(t)
#
# Desplazamiento por coherencia:
#
#   Δθ_coh =
#       β · ((C_Ω / α) - 1) · (π / 27)
#
# Desplazamiento por distribución energética:
#
#   w_alto = (w_4 + w_5 + w_6) / 3
#
#   w_bajo = (w_1 + w_2) / 2
#
#   Δθ_w =
#       β · (w_alto - w_bajo) · (π / 54)
#
# Por tanto:
#
#   θ_eq =
#       θ_cube
#       + β · ((C_Ω / α) - 1) · (π / 27)
#       + β · (w_alto - w_bajo) · (π / 54)
#
# Las variables w_i utilizadas aquí corresponden exclusivamente
# a L1..L6.
#
# ===============================================================
# COMPONENTES DE LA FUERZA TOTAL F_Y(t)
# ===============================================================
#
#   F_Y = F_L0 + F_L5 + F_L6 + F_β + F_COH
#
# Entrada / forzamiento externo procedente de L0:
#
#   F_L0 = scale_L0 · L0
#
# L0 no forma parte de las seis capas internas y no recibe w_0.
#
# Retroalimentación metaestructural:
#
#   F_L5 =
#       ρ · P_t · C_Ω
#       + 0.5 · ΔC_Ω
#       - β · (S / ln(6))
#
# Dirección / propósito:
#
#   F_L6 = w_6 · P
#
# L6 sí pertenece a las seis capas internas y, por tanto, posee w_6,
# pero su fricción propia permanece fijada por el invariante:
#
#   φ_6 = 0
#
# Fuerza asociada al margen β / novedad:
#
#   F_β = β · (1 - exp(-N / k))
#
# Retroalimentación dinámica de coherencia:
#
#   F_COH = C_Ω · ΔC_Ω
#
# La suma de estos términos produce:
#
#   F_Y(t)
#
# ===============================================================
# RELACIÓN CON L7
# ===============================================================
#
# L7 NO es una variable de entrada de este módulo.
#
# L7 representa la emergencia producida por la integración del sistema:
#
#   L0
#    ↓
#   L1..L6
#    ↓
#   integración dinámica
#    ↓
#   L7 — EMERGENCIA
#
# Por tanto, L7 no debe introducirse artificialmente como:
#
#   E_7
#   w_7
#   φ_7
#   f_7
#
# dentro del carril L4.
#
# La emergencia L7 será tratada posteriormente como resultado de la
# integración correspondiente, no como una capa interna adicional
# del oscilador.
#
# ===============================================================
# VARIABLES
# ===============================================================
#
# θ_Y, θ̇_Y
#   posición y velocidad continua del carril
#   [rad], [rad/s]
#
# L_i
#   activación de cada capa interna
#   i ∈ {1,2,3,4,5,6}
#   [0,1]
#
# φ_i
#   fricción estructural de cada capa interna
#   i ∈ {1,2,3,4,5,6}
#   [0,1]
#
# φ_6
#   fricción propia de L6
#   fijada por invariante:
#   φ_6 = 0
#
# L0
#   entrada externa / caos / forzamiento
#   [0,1]
#
# P
#   magnitud computable de dirección / propósito de L6
#   [0,1]
#
# C_Ω
#   coherencia estructural global
#   [0, α]
#
# ΔC_Ω
#   variación temporal de C_Ω
#
# S
#   entropía de la distribución energética interna
#   [0, ln(6)]
#
# N
#   magnitud de novedad
#   adimensional
#
# k
#   escala de sensibilidad de la función de novedad
#   adimensional
#
# dt
#   paso temporal de integración
#   [s]
#
# α, β, Φ
#   constantes estructurales obtenidas de los módulos canónicos
#
# L7
#   resultado emergente posterior.
#   No constituye una variable interna del carril L4.
#
# ===============================================================
# DOMINIO Y RESTRICCIONES
# ===============================================================
#
#   L_i ∈ [0,1]
#   φ_i ∈ [0,1]
#
#   i ∈ {1,2,3,4,5,6}
#
#   φ_6 = 0
#
#   dt > 0
#
#   C_Ω ∈ [0, α]
#
#   Σ_i E_i ≥ 0
#
# Si:
#
#   Σ_i E_i == 0
#
# entonces:
#
#   w_i = 1/6
#
# para las seis capas internas.
#
# L0 queda fuera de la normalización energética.
# L7 queda fuera de la normalización energética.
#
# ===============================================================
# CASOS LÍMITE
# ===============================================================
#
# Todas las capas internas desactivadas:
#
#   L1 = L2 = L3 = L4 = L5 = L6 = 0
#
# entonces:
#
#   E_i = 0
#
#   w_i = 1/6
#
# y:
#
#   φ_Y = Σ_i (1/6 · φ_i)
#
# con:
#
#   φ_6 = 0.
#
# Si:
#
#   ζ_Y ≥ 1
#
# entonces:
#
#   régimen crítico o sobreamortiguado
#
#   ω_Y = 0
#
# Si:
#
#   ΔC_Ω = 0
#
# entonces:
#
#   F_COH = 0
#
# Si:
#
#   N = 0
#
# entonces:
#
#   F_β = 0
#
# ===============================================================
# CADENA CAUSAL DEL MÓDULO
# ===============================================================
#
#   L0
#    │
#    └──────────────→ F_L0
#                         │
#   L1..L6               │
#    │                   │
#    ├→ E_i              │
#    │    ↓              │
#    ├→ w_i              │
#    │    ↓              │
#    ├→ S                │
#    │    ↓              │
#    ├→ φ_Y → ζ_Y → ω_Y │
#    │                   │
#    └→ θ_eq ────────────┤
#                        ↓
#                  F_L5 + F_L6
#                  + F_β + F_COH
#                        ↓
#                       F_Y
#                        ↓
#              θ̈_Y = F_Y - φ_Yθ̇_Y
#                    - π²(θ_Y-θ_eq)
#                        ↓
#                 θ̇_Y(t + dt)
#                        ↓
#                  θ_Y(t + dt)
#                        ↓
#                nuevo estado
#                        ↓
#                 siguiente ciclo
#
# El resultado integrado puede posteriormente participar en la
# determinación de la emergencia L7, pero L7 no vuelve a entrar
# como capa interna de este cálculo salvo que una arquitectura
# posterior defina explícitamente dicho canal.
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
