# ===============================================================
# modules/formulas/formulas_omega/yo_oscilatorio_dinamico_FO.py
# ===============================================================
#
# VPSI-TRUTH — L4 — YO OSCILATORIO DINÁMICO (carril)
#
# RESPONSABILIDAD
# ---------------
# Implementar exclusivamente la matemática continua del carril del
# Yo Oscilatorio Dinámico (L4):
#
#   θ̈_Y, θ̇_Y, θ_Y, F_Y, θ_eq, φ_Y
#
# Este módulo constituye el carril matemático continuo de L4.
#
# ===============================================================
# SEPARACIÓN ESTRUCTURAL DE CAPAS
# ===============================================================
#
# L0 — entrada / forzamiento externo.
#
#   L0 no pertenece al dominio energético interno de este carril.
#   L0 entra exclusivamente mediante:
#
#       F_L0 = scale_L0 · L0
#
#   Por tanto L0 NO participa en:
#
#       E_i
#       w_i
#       S
#       φ_Y
#       f_i
#
# L1..L6 — seis capas internas del carril.
#
#   Son las únicas capas que participan en:
#
#       E_i
#       w_i
#       S
#       φ_Y
#       f_i
#
#   El vector interno tiene exactamente seis posiciones:
#
#       [0] = L1
#       [1] = L2
#       [2] = L3
#       [3] = L4
#       [4] = L5
#       [5] = L6
#
# L7 — emergencia / resultado posterior de la integración.
#
#   L7 NO es una variable de este módulo.
#   L7 no participa en:
#
#       E_i
#       w_i
#       S
#       φ_Y
#       f_i
#       F_Y
#
#   La emergencia L7 corresponde a una fase posterior del sistema.
#
# ===============================================================
# REGLA DE BORDE
# ===============================================================
#
# Si otro componente del sistema trabaja conceptualmente con:
#
#       [L0,L1,L2,L3,L4,L5,L6]
#
# el corte debe realizarse ANTES de entrar a este módulo:
#
#       activations_L1_L6 = layers[1:7]
#       l0_input = layers[0]
#
# Este módulo NO acepta vectores de siete activaciones ni realiza
# internamente ese corte.
#
# Contrato de entrada:
#
#       activations = [L1,L2,L3,L4,L5,L6]
#       len(activations) == 6
#
#       frictions = [φ1,φ2,φ3,φ4,φ5,φ6]
#       len(frictions) == 6
#       φ6 = 0
#
# ===============================================================
# ECUACIÓN MAESTRA
# ===============================================================
#
#   d²θ_Y/dt² + φ_Y(t)·dθ_Y/dt
#       + π²·(θ_Y(t) − θ_eq(t)) = F_Y(t)
#
# Despejada:
#
#   θ̈_Y = F_Y − φ_Y·θ̇_Y
#          − π²·(θ_Y − θ_eq)
#
# ===============================================================
# INTEGRACIÓN TEMPORAL
# ===============================================================
#
# Euler semi-implícito:
#
#   θ̈ = F_Y − φ_Y·θ̇ − π²·(θ − θ_eq)
#
#   θ̇(t+dt) = θ̇(t) + θ̈·dt
#
#   θ(t+dt) = θ(t) + θ̇(t+dt)·dt
#
# Restricción:
#
#   dt > 0
#
# ===============================================================
# ENERGÍA OPERACIONAL
# ===============================================================
#
# Para i ∈ {1,2,3,4,5,6}:
#
#   ν_i = Φ^(i/2)
#
#   E_i = L_i·(1−φ_i)·ν_i
#
# En código:
#
#   idx = 0..5
#   layer_idx = idx + 1
#
# ===============================================================
# PESOS EMERGENTES
# ===============================================================
#
#   w_i = E_i / Σ_j E_j
#
# Si:
#
#   Σ_j E_j = 0
#
# entonces:
#
#   w_i = 1/6
#
# para todo i.
#
# Los pesos se calculan exclusivamente sobre L1..L6.
#
# ===============================================================
# CONTRIBUCIONES DOCUMENTALES
# ===============================================================
#
#   f_i = w_i·L_i·(1−φ_i)·E_i
#
# Estas contribuciones se exponen para trazabilidad y auditoría.
# No redefinen los pesos y no introducen una segunda normalización.
#
# ===============================================================
# ENTROPÍA
# ===============================================================
#
#   S = −Σ_i w_i·ln(w_i)
#
# únicamente para w_i > 0.
#
# Máximo:
#
#   S_MAX = ln(6)
#
# Entropía normalizada:
#
#   S_norm = S / ln(6)
#
# Negentropía:
#
#   1 − S_norm
#
# ===============================================================
# AMORTIGUAMIENTO DEL YO
# ===============================================================
#
#   φ_Y = Σ_i w_i·φ_i
#
# con:
#
#   φ_6 = 0
#
# Amortiguamiento adimensional:
#
#   ζ_Y = φ_Y / (2π)
#
# Frecuencia:
#
#   ω_Y = π·√(1−ζ_Y²)
#
# para:
#
#   ζ_Y < 1
#
# Si:
#
#   ζ_Y = 1
#
# régimen crítico:
#
#   ω_Y = 0
#
# Si:
#
#   ζ_Y > 1
#
# régimen sobreamortiguado:
#
#   ω_Y = 0
#
# ===============================================================
# EQUILIBRIO DINÁMICO
# ===============================================================
#
#   θ_eq(t) = θ_cube + Δθ_coh + Δθ_w
#
# donde:
#
#   Δθ_coh =
#       β·((C_Ω/α)−1)·(π/27)
#
#   w_alto = (w_4+w_5+w_6)/3
#
#   w_bajo = (w_1+w_2)/2
#
#   Δθ_w =
#       β·(w_alto−w_bajo)·(π/54)
#
# ===============================================================
# FUERZA TOTAL
# ===============================================================
#
#   F_Y = F_L0 + F_L5 + F_L6 + F_β + F_COH
#
#   F_L0 = scale_L0·L0
#
#   F_L5 =
#       ρ·P_t·C_Ω
#       + 0.5·ΔC_Ω
#       − β·(S/ln(6))
#
#   F_L6 = w_6·P
#
#   F_β =
#       β·(1−exp(−N/k))
#
#   F_COH = C_Ω·ΔC_Ω
#
# ===============================================================
# SEMILLA
# ===============================================================
#
# α y β son obtenidos exclusivamente desde modules.constante.
# No se redefinen en este módulo.
#
# PHI y THETA_CUBE son obtenidos desde formulas_omega.constants.
#
# ===============================================================
# RESTRICCIONES DE DOMINIO
# ===============================================================
#
#   activations → exactamente 6 valores
#   0 ≤ L_i ≤ 1
#
#   frictions → exactamente 6 valores
#   0 ≤ φ_i ≤ 1
#   φ_6 = 0
#
#   dt > 0
#
#   pesos → exactamente 6 valores
#
# El módulo falla explícitamente ante una violación de contrato.
#
# ===============================================================
# SIN RESPONSABILIDADES EXTERNAS
# ===============================================================
#
# Este archivo:
#
#   - no declara CONTENEDOR;
#   - no habla con Engine;
#   - no interpreta contexto;
#   - no asigna θ_Y a una casa;
#   - no calcula casas;
#   - no calcula L7;
#   - no ejecuta la emergencia;
#   - no decide significado psicológico;
#   - no convierte el oscilador continuo en autómata discreto.
#
# ===============================================================

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Sequence, Tuple

from modules.constante import ALPHA, BETA

from modules.formulas.formulas_omega.constants import (
    PHI,
    THETA_CUBE,
)

# ===============================================================
# CONSTANTES LOCALES DEL CARRIL
# ===============================================================

NUM_LAYERS_YO: int = 6
S_MAX: float = math.log(NUM_LAYERS_YO)
PHI_CRITICAL: float = 2.0 * math.pi

ALPHA_F: float = float(ALPHA)
BETA_F: float = float(BETA)
THETA_CUBE_F: float = float(THETA_CUBE)
PI2: float = math.pi * math.pi

_DEFAULT_FRICTIONS_L1_L6: List[float] = [
    0.10,
    0.02,
    0.05,
    0.03,
    0.01,
    0.00,
]

# ===============================================================
# VALIDACIÓN DE ACTIVACIONES
# ===============================================================

def _validate_activations(activations: Sequence[float]) -> List[float]:
    act = [float(x) for x in activations]

    if len(act) != NUM_LAYERS_YO:
        raise ValueError(
            "activations debe tener exactamente 6 valores "
            "(L1..L6); recibido {0}".format(len(act))
        )

    for idx, value in enumerate(act):
        if not 0.0 <= value <= 1.0:
            raise ValueError(
                "activations[{0}] corresponde a L{1} y debe estar "
                "en [0,1]; recibido {2}".format(idx, idx + 1, value)
            )

    return act


# ===============================================================
# VALIDACIÓN Y RESOLUCIÓN DE FRICCIONES
# ===============================================================

def _resolve_frictions(
    frictions: Optional[Sequence[float]],
) -> List[float]:

    if frictions is None:
        out = list(_DEFAULT_FRICTIONS_L1_L6)
    else:
        out = [float(x) for x in frictions]

        if len(out) != NUM_LAYERS_YO:
            raise ValueError(
                "frictions debe tener exactamente 6 valores "
                "(φ1..φ6); recibido {0}. "
                "El corte de L0 debe realizarse antes de entrar "
                "al módulo L4.".format(len(out))
            )

    for idx, value in enumerate(out):
        if not 0.0 <= value <= 1.0:
            raise ValueError(
                "frictions[{0}] corresponde a φ{1} y debe estar "
                "en [0,1]; recibido {2}".format(idx, idx + 1, value)
            )

    out[5] = 0.0

    return out


# ===============================================================
# VALIDACIÓN DE PESOS
# ===============================================================

def _validate_weights(weights: Sequence[float]) -> List[float]:

    out = [float(x) for x in weights]

    if len(out) != NUM_LAYERS_YO:
        raise ValueError(
            "weights debe tener exactamente 6 valores "
            "(w1..w6); recibido {0}".format(len(out))
        )

    for idx, value in enumerate(out):
        if value < 0.0:
            raise ValueError(
                "weights[{0}] corresponde a w{1} y no puede ser "
                "negativo; recibido {2}".format(idx, idx + 1, value)
            )

    total = sum(out)

    if not math.isclose(total, 1.0, rel_tol=1e-9, abs_tol=1e-9):
        raise ValueError(
            "weights debe estar normalizado y sumar 1.0; suma={0}".format(
                total
            )
        )

    return out


# ===============================================================
# MOTOR MATEMÁTICO ESTÁTICO
# ===============================================================

class YoOscilatorioEngine:
    """
    Calculador matemático del carril L4 Yo Oscilatorio Dinámico.

    Opera exclusivamente sobre el dominio interno L1..L6.
    """

    # ===========================================================
    # ENERGÍAS Y PESOS
    # ===========================================================

    @staticmethod
    def compute_energies_and_weights(
        activations: Sequence[float],
        frictions: Optional[Sequence[float]] = None,
    ) -> Tuple[List[float], List[float]]:

        act = _validate_activations(activations)
        fr = _resolve_frictions(frictions)

        energies: List[float] = []

        for idx in range(NUM_LAYERS_YO):
            layer_idx = idx + 1
            nu_i = PHI ** (layer_idx / 2.0)
            e_i = act[idx] * (1.0 - fr[idx]) * nu_i
            energies.append(e_i)

        total_energy = sum(energies)

        if total_energy > 0.0:
            weights = [
                energy / total_energy
                for energy in energies
            ]
        else:
            weights = [
                1.0 / NUM_LAYERS_YO
            ] * NUM_LAYERS_YO

        return energies, weights

    # ===========================================================
    # CONTRIBUCIONES f_i
    # ===========================================================

    @staticmethod
    def compute_contributions(
        weights: Sequence[float],
        activations: Sequence[float],
        energies: Sequence[float],
        frictions: Optional[Sequence[float]] = None,
    ) -> List[float]:

        act = _validate_activations(activations)
        fr = _resolve_frictions(frictions)
        w = _validate_weights(weights)

        if len(energies) != NUM_LAYERS_YO:
            raise ValueError(
                "energies debe tener exactamente 6 valores; "
                "recibido {0}".format(len(energies))
            )

        return [
            w[idx]
            * act[idx]
            * (1.0 - fr[idx])
            * float(energies[idx])
            for idx in range(NUM_LAYERS_YO)
        ]

    # ===========================================================
    # ENTROPÍA
    # ===========================================================

    @staticmethod
    def compute_entropy(
        weights: Sequence[float],
    ) -> Dict[str, float]:

        w = _validate_weights(weights)

        s = 0.0

        for value in w:
            if value > 0.0:
                s -= value * math.log(value)

        s_norm = s / S_MAX if S_MAX > 0.0 else 0.0
        negentropy = 1.0 - s_norm

        return {
            "s": s,
            "s_norm": s_norm,
            "negentropy": negentropy,
        }

    # ===========================================================
    # AMORTIGUAMIENTO Y FRECUENCIA
    # ===========================================================

    @staticmethod
    def compute_damping_and_frequency(
        weights: Sequence[float],
        frictions: Optional[Sequence[float]] = None,
    ) -> Dict[str, float]:

        w = _validate_weights(weights)
        fr = _resolve_frictions(frictions)

        phi_y = sum(
            w[idx] * fr[idx]
            for idx in range(NUM_LAYERS_YO)
        )

        zeta_y = phi_y / PHI_CRITICAL

        if zeta_y < 1.0:
            omega_y = math.pi * math.sqrt(
                max(
                    0.0,
                    1.0 - (zeta_y ** 2),
                )
            )
            regime = "SUBDAMPED"
        elif math.isclose(
            zeta_y,
            1.0,
            rel_tol=1e-9,
            abs_tol=1e-9,
        ):
            omega_y = 0.0
            regime = "CRITICAL"
        else:
            omega_y = 0.0
            regime = "OVERDAMPED"

        return {
            "phi_Y": phi_y,
            "zeta_Y": zeta_y,
            "omega_Y": omega_y,
            "regime": regime,
        }

    # ===========================================================
    # EQUILIBRIO DINÁMICO
    # ===========================================================

    @staticmethod
    def compute_theta_eq(
        c_omega: float,
        weights: Sequence[float],
    ) -> Dict[str, float]:

        w = _validate_weights(weights)

        if ALPHA_F <= 0.0:
            raise ValueError(
                "ALPHA debe ser estrictamente positiva para calcular "
                "C_Ω / α."
            )

        delta_theta_coh = (
            BETA_F
            * ((float(c_omega) / ALPHA_F) - 1.0)
            * (math.pi / 27.0)
        )

        w_alto = (
            w[3]
            + w[4]
            + w[5]
        ) / 3.0

        w_bajo = (
            w[0]
            + w[1]
        ) / 2.0

        delta_theta_w = (
            BETA_F
            * (w_alto - w_bajo)
            * (math.pi / 54.0)
        )

        theta_eq = (
            THETA_CUBE_F
            + delta_theta_coh
            + delta_theta_w
        )

        return {
            "theta_eq": theta_eq,
            "delta_theta_coh": delta_theta_coh,
            "delta_theta_w": delta_theta_w,
            "theta_cube": THETA_CUBE_F,
        }

    # ===========================================================
    # FUERZAS
    # ===========================================================

    @staticmethod
    def compute_forces(
        l0_input: float,
        weights: Sequence[float],
        c_omega: float,
        delta_c_omega: float,
        entropy_s: float,
        purpose_p: float = 0.0,
        rho: float = 1.0,
        p_t: float = 1.0,
        novelty: float = 0.0,
        sensitivity: float = 5.0,
        scale_l0: float = 1.0,
    ) -> Dict[str, float]:

        w = _validate_weights(weights)

        if float(sensitivity) <= 0.0:
            raise ValueError(
                "sensitivity debe ser > 0."
            )

        f_l0 = (
            float(scale_l0)
            * float(l0_input)
        )

        entropy_term = (
            float(entropy_s) / S_MAX
            if S_MAX > 0.0
            else 0.0
        )

        f_l5 = (
            float(rho)
            * float(p_t)
            * float(c_omega)
            + 0.5 * float(delta_c_omega)
            - BETA_F * entropy_term
        )

        w6 = w[5]

        f_l6 = (
            w6
            * float(purpose_p)
        )

        a_n = (
            1.0
            - math.exp(
                -max(0.0, float(novelty))
                / float(sensitivity)
            )
        )

        f_beta = BETA_F * a_n

        f_coh = (
            float(c_omega)
            * float(delta_c_omega)
        )

        f_total = (
            f_l0
            + f_l5
            + f_l6
            + f_beta
            + f_coh
        )

        return {
            "f_total": f_total,
            "f_l0": f_l0,
            "f_l5": f_l5,
            "f_l6": f_l6,
            "f_beta": f_beta,
            "f_coh": f_coh,
        }

    # ===========================================================
    # PASO DE INTEGRACIÓN
    # ===========================================================

    @classmethod
    def step(
        cls,
        theta_Y: float,
        theta_dot_Y: float,
        activations: Sequence[float],
        l0_input: float,
        c_omega: float,
        delta_c_omega: float,
        frictions: Optional[Sequence[float]] = None,
        purpose_p: float = 0.0,
        rho: float = 1.0,
        p_t: float = 1.0,
        novelty: float = 0.0,
        sensitivity: float = 5.0,
        dt: float = 0.01,
        scale_l0: float = 1.0,
    ) -> Dict[str, Any]:

        dt_f = float(dt)

        if dt_f <= 0.0:
            raise ValueError("dt debe ser > 0.")

        act = _validate_activations(activations)
        fr = _resolve_frictions(frictions)

        energies, weights = (
            cls.compute_energies_and_weights(
                act,
                fr,
            )
        )

        contributions = cls.compute_contributions(
            weights=weights,
            activations=act,
            energies=energies,
            frictions=fr,
        )

        entropy_data = cls.compute_entropy(
            weights
        )

        damping_data = (
            cls.compute_damping_and_frequency(
                weights,
                fr,
            )
        )

        geometry_data = cls.compute_theta_eq(
            c_omega=float(c_omega),
            weights=weights,
        )

        forces_data = cls.compute_forces(
            l0_input=float(l0_input),
            weights=weights,
            c_omega=float(c_omega),
            delta_c_omega=float(delta_c_omega),
            entropy_s=entropy_data["s"],
            purpose_p=float(purpose_p),
            rho=float(rho),
            p_t=float(p_t),
            novelty=float(novelty),
            sensitivity=float(sensitivity),
            scale_l0=float(scale_l0),
        )

        phi_y = damping_data["phi_Y"]
        theta_eq = geometry_data["theta_eq"]
        f_total = forces_data["f_total"]

        restoration = (
            PI2
            * (
                float(theta_Y)
                - theta_eq
            )
        )

        theta_ddot = (
            f_total
            - (
                phi_y
                * float(theta_dot_Y)
            )
            - restoration
        )

        new_theta_dot = (
            float(theta_dot_Y)
            + theta_ddot * dt_f
        )

        new_theta = (
            float(theta_Y)
            + new_theta_dot * dt_f
        )

        return {
            "theta_Y": new_theta,
            "theta_dot_Y": new_theta_dot,
            "theta_ddot_Y": theta_ddot,
            "energies": energies,
            "weights": weights,
            "contributions_f_i": contributions,
            "entropy": entropy_data,
            "damping": damping_data,
            "geometry": geometry_data,
            "forces": forces_data,
            "dt": dt_f,
            "ALPHA": ALPHA_F,
            "BETA": BETA_F,
            "NUM_LAYERS_YO": NUM_LAYERS_YO,
        }


# ===============================================================
# ESTADO TEMPORAL DEL CARRIL
# ===============================================================

class SessionStateYoOscilatorio:
    """
    Gestiona exclusivamente la trayectoria temporal del carril
    continuo del Yo Oscilatorio Dinámico (L4).
    """

    def __init__(
        self,
        initial_theta: Optional[float] = None,
        initial_theta_dot: float = 0.0,
    ):

        self.theta_Y = (
            float(initial_theta)
            if initial_theta is not None
            else THETA_CUBE_F
        )

        self.theta_dot_Y = float(
            initial_theta_dot
        )

        self.prev_c_omega: Optional[float] = None

        self.history: List[
            Dict[str, Any]
        ] = []

    def update(
        self,
        activations: Sequence[float],
        l0_input: float,
        c_omega: float,
        frictions: Optional[Sequence[float]] = None,
        purpose_p: float = 0.0,
        rho: float = 1.0,
        p_t: float = 1.0,
        novelty: float = 0.0,
        sensitivity: float = 5.0,
        dt: float = 0.01,
        scale_l0: float = 1.0,
    ) -> Dict[str, Any]:

        c_omega_f = float(c_omega)

        if self.prev_c_omega is None:
            delta_c_omega = 0.0
        else:
            delta_c_omega = (
                c_omega_f
                - self.prev_c_omega
            )

        result = YoOscilatorioEngine.step(
            theta_Y=self.theta_Y,
            theta_dot_Y=self.theta_dot_Y,
            activations=activations,
            l0_input=l0_input,
            c_omega=c_omega_f,
            delta_c_omega=delta_c_omega,
            frictions=frictions,
            purpose_p=purpose_p,
            rho=rho,
            p_t=p_t,
            novelty=novelty,
            sensitivity=sensitivity,
            dt=dt,
            scale_l0=scale_l0,
        )

        self.theta_Y = result["theta_Y"]
        self.theta_dot_Y = result["theta_dot_Y"]
        self.prev_c_omega = c_omega_f

        self.history.append(result)

        return result

    def trajectory(self) -> List[float]:
        return [
            entry["theta_Y"]
            for entry in self.history
        ]

    def velocity_trajectory(self) -> List[float]:
        return [
            entry["theta_dot_Y"]
            for entry in self.history
        ]


# ===============================================================
# EXPORTS
# ===============================================================

__all__ = [
    "NUM_LAYERS_YO",
    "S_MAX",
    "PHI_CRITICAL",
    "YoOscilatorioEngine",
    "SessionStateYoOscilatorio",
]
