# ===============================================================
# VPSI-TRUTH — L4 — YO OSCILATORIO DINÁMICO
# CARRIL CONTINUO DEL YO
# ===============================================================
#
# SISTEMA:
#   L0 = entrada / caos / entorno       → NO es estado interno
#   L1..L6 = capas internas             → generan E_i y w_i
#   L7 = emergencia de integración      → NO es estado del carril
#
# El Yo NO salta entre L1...L6.
# El Yo es el grado de libertad continuo θ_Y(t).
#
# ECUACIÓN MAESTRA:
#
#   d²θ_Y/dt² + φ_Y(t)·dθ_Y/dt
#   + π²·[θ_Y(t) − θ_eq(t)] = F_Y(t)
#
# CIRCUITO:
#
#   L1..L6 → E_i → w_i → S → C_Ω
#                    ↓
#              φ_Y, θ_eq, F_Y
#                    ↓
#                 θ_Y(t)
#                    ↓
#             nuevo estado interno
#
# L0 entra únicamente como forzamiento.
# L7 se calcula posteriormente como emergencia de integración.
#
# EXTENSIONES ARQUITECTÓNICAS EXPLÍCITAS:
#   w_i = E_i / ΣE_j
#   φ_Y = Σw_iφ_i
#   θ_eq = θ_eq(t)
#   F_Y = F_L0 + F_L5 + F_L6 + F_β + F_COH
#
# ===============================================================

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import List, Optional, Sequence

try:
    from modules.constante import ALPHA, BETA
except Exception:
    from fractions import Fraction
    ALPHA = Fraction(26, 27)
    BETA = Fraction(1, 27)

try:
    from .constants import (
        PHI,
        THETA_CUBE,
        PHI_CRITICAL,
        LAYER_FRICTION,
        R_FIN,
        S_REF,
    )
    from .energy import LayerEnergy
except Exception:
    PHI = (1.0 + math.sqrt(5.0)) / 2.0
    THETA_CUBE = math.asin(1.0 / math.sqrt(27.0))
    PHI_CRITICAL = 2.0 * math.pi
    R_FIN = 28.0 / 27.0
    S_REF = math.e / math.pi
    LAYER_FRICTION = [0.10, 0.02, 0.05, 0.03, 0.01, 0.00]

    class LayerEnergy:
        @staticmethod
        def frequency(i: int) -> float:
            return PHI ** (i / 2.0)

        @staticmethod
        def compute(activation: float, friction: float, layer_index: int) -> float:
            return float(activation) * (1.0 - float(friction)) * LayerEnergy.frequency(layer_index)


# ===============================================================
# MARCO ESTRUCTURAL
# ===============================================================

ALPHA_F = float(ALPHA)
BETA_F = float(BETA)
PI2 = math.pi ** 2
INTERNAL_LAYERS = 6
LAYER_INDICES = tuple(range(1, 7))
ENTROPY_MAX = math.log(INTERNAL_LAYERS)


# ===============================================================
# VALIDACIÓN
# ===============================================================

def _validate_internal_inputs(
    activations: Sequence[float],
    frictions: Sequence[float],
) -> None:
    if len(activations) != INTERNAL_LAYERS:
        raise ValueError(
            "activations debe contener L1..L6: "
            f"se esperaban {INTERNAL_LAYERS}, recibido {len(activations)}"
        )
    if len(frictions) != INTERNAL_LAYERS:
        raise ValueError(
            "frictions debe contener L1..L6: "
            f"se esperaban {INTERNAL_LAYERS}, recibido {len(frictions)}"
        )
    for i, value in enumerate(activations, 1):
        if not 0.0 <= float(value) <= 1.0:
            raise ValueError(f"L{i} debe estar en [0,1], recibido {value}")


def _default_frictions() -> List[float]:
    # L1..L6; L6 conserva φ6 = 0.
    if len(LAYER_FRICTION) >= 7:
        return [float(x) for x in LAYER_FRICTION[1:7]]
    return [0.02, 0.05, 0.03, 0.01, 0.01, 0.00]


# ===============================================================
# 1. ENERGÍA OPERACIONAL
# ===============================================================

def compute_energies(
    activations: Sequence[float],
    frictions: Optional[Sequence[float]] = None,
) -> List[float]:
    """
    E_i = L_i · (1 − φ_i) · ν_i
    ν_i = PHI^(i/2), i = 1..6.

    La energía es una magnitud operacional abstracta del modelo.
    L0 y L7 no participan aquí.
    """
    if frictions is None:
        frictions = _default_frictions()
    _validate_internal_inputs(activations, frictions)

    return [
        float(activations[k - 1])
        * (1.0 - float(frictions[k - 1]))
        * float(LayerEnergy.frequency(k))
        for k in LAYER_INDICES
    ]


# ===============================================================
# 2. PESOS EMERGENTES
# ===============================================================

def compute_weights(energies: Sequence[float]) -> List[float]:
    """
    w_i = E_i / ΣE_j.

    Los pesos no son asignados manualmente.
    Emergen de la distribución energética instantánea.
    """
    if len(energies) != INTERNAL_LAYERS:
        raise ValueError("energies debe contener E1..E6")

    positive = [max(0.0, float(e)) for e in energies]
    total = sum(positive)

    if total <= 0.0:
        return [1.0 / INTERNAL_LAYERS] * INTERNAL_LAYERS

    return [e / total for e in positive]


# ===============================================================
# 3. CONTRIBUCIÓN f_i
# ===============================================================

def compute_contributions(
    weights: Sequence[float],
    activations: Sequence[float],
    energies: Sequence[float],
    frictions: Optional[Sequence[float]] = None,
) -> List[float]:
    """
    f_i = w_i · L_i · (1 − φ_i) · E_i
    """
    if frictions is None:
        frictions = _default_frictions()

    _validate_internal_inputs(activations, frictions)

    return [
        float(weights[i])
        * float(activations[i])
        * (1.0 - float(frictions[i]))
        * float(energies[i])
        for i in range(INTERNAL_LAYERS)
    ]


# ===============================================================
# 4. ENTROPÍA
# ===============================================================

def shannon_S(weights: Sequence[float]) -> float:
    """S = −Σ w_i ln(w_i)."""
    return -sum(
        float(w) * math.log(float(w))
        for w in weights
        if float(w) > 0.0
    )


def normalized_entropy(S: float) -> float:
    """S/S_max ∈ [0,1]."""
    return min(1.0, max(0.0, float(S) / ENTROPY_MAX))


def negentropy(weights: Sequence[float]) -> float:
    """N_neg = 1 − S/ln(6)."""
    return 1.0 - normalized_entropy(shannon_S(weights))


# ===============================================================
# 5. COHERENCIA C_Ω
# ===============================================================

def compute_c_omega(
    contributions: Sequence[float],
    rho: float = 1.0,
    P_t: float = 1.0,
    A: float = 1.0,
    I_ext: float = 1.0,
    s_ref: Optional[float] = None,
    r_fin: Optional[float] = None,
) -> float:
    """
    C_Ω = α · S_REF · Πf_i · R_FIN · Res_ζ · P_t · A · I_ext.

    C_Ω queda acotada por α como techo observable.
    """
    if len(contributions) != INTERNAL_LAYERS:
        raise ValueError("contributions debe contener f1..f6")

    s_ref = float(S_REF if s_ref is None else s_ref)
    r_fin = float(R_FIN if r_fin is None else r_fin)

    product = math.prod(max(0.0, float(f)) for f in contributions)

    raw = (
        ALPHA_F
        * s_ref
        * product
        * float(r_fin)
        * max(0.0, float(rho))
        * max(0.0, float(P_t))
        * max(0.0, float(A))
        * max(0.0, float(I_ext))
    )

    return min(ALPHA_F, max(0.0, raw))


# ===============================================================
# 6. AMORTIGUAMIENTO DEL YO
# ===============================================================

def phi_Y(
    weights: Sequence[float],
    frictions: Optional[Sequence[float]] = None,
) -> float:
    """
    φ_Y = Σ(w_i φ_i), i=1..6.

    Invariante:
        φ_6 = 0

    L6 aporta dirección, no fricción propia.
    """
    if frictions is None:
        frictions = _default_frictions()

    if len(weights) != INTERNAL_LAYERS:
        raise ValueError("weights debe contener w1..w6")

    return sum(
        float(weights[i]) *
        (0.0 if i == 5 else float(frictions[i]))
        for i in range(INTERNAL_LAYERS)
    )


def zeta_Y(phi_y: float) -> float:
    return float(phi_y) / PHI_CRITICAL


def omega_Y(phi_y: float) -> float:
    zeta = zeta_Y(phi_y)
    if zeta >= 1.0:
        return 0.0
    return math.pi * math.sqrt(max(0.0, 1.0 - zeta ** 2))


def regime_Y(phi_y: float) -> str:
    zeta = zeta_Y(phi_y)

    if abs(zeta - 1.0) < 1e-12:
        return "CRITICO"
    if zeta < 1.0:
        return "SUBAMORTIGUADO"
    return "SOBREAMORTIGUADO"


# ===============================================================
# 7. GEOMETRÍA DINÁMICA DEL CARRIL
# ===============================================================

def dynamic_equilibrium(
    c_omega: float,
    weights: Sequence[float],
    base: Optional[float] = None,
) -> float:
    """
    θ_eq(t) = atractor geométrico dinámico.

    THETA_CUBE sigue siendo la referencia.
    La posición del atractor puede desplazarse según el
    estado energético/coherente del sistema.

    El desplazamiento queda acotado por β.
    No representa una estación L1...L6.
    """
    base = float(THETA_CUBE if base is None else base)

    coherence_term = (
        BETA_F
        * ((float(c_omega) / ALPHA_F) - 1.0)
        * (math.pi / 27.0)
    )

    high = sum(float(w) for w in weights[3:6])   # L4-L6
    low = sum(float(w) for w in weights[0:2])    # L1-L2

    weight_term = BETA_F * (high - low) * (math.pi / 54.0)

    return base + coherence_term + weight_term


# ===============================================================
# 8. FUERZAS DEL CARRIL
# ===============================================================

def force_L0(L0_input: float, scale: float = 1.0) -> float:
    """L0 = entrada externa; no es grado de libertad interno."""
    return float(L0_input) * float(scale)


def force_L5(
    c_omega: float,
    rho: float,
    P_t: float,
    S: float,
    delta_c: float,
) -> float:
    """
    Retroalimentación cuantificable asociada al canal L5.
    No se interpreta como psicología humana.
    """
    s_norm = normalized_entropy(S)

    return (
        float(rho) * float(P_t) * float(c_omega)
        + 0.5 * float(delta_c)
        - BETA_F * s_norm
    )


def force_L6(w6: float, purpose_magnitude: float) -> float:
    """
    L6 = dirección/propósito.
    No introduce fricción propia.
    """
    return float(w6) * float(purpose_magnitude)


def force_BETA(novelty: float = 0.0, k: Optional[float] = None) -> float:
    """
    F_β = β · A(N)
    A(N) = 1 − exp(−N/k)
    """
    if k is None or k <= 0.0:
        k = float(S_REF) if float(S_REF) > 0.0 else 1.0

    novelty = max(0.0, float(novelty))
    A = 1.0 - math.exp(-novelty / k)

    return BETA_F * A


def force_COH(c_omega: float, delta_c: float = 0.0) -> float:
    """
    Retroalimentación de coherencia.
    C_Ω ya está acotada a α, por lo que no existe exceso
    positivo cuando el clamp está activo.
    """
    return float(c_omega) * float(delta_c)


def force_Y(
    L0_input: float,
    weights: Sequence[float],
    purpose_magnitude: float,
    c_omega: float,
    rho: float = 1.0,
    P_t: float = 1.0,
    S: float = 0.0,
    delta_c: float = 0.0,
    novelty: float = 0.0,
    scale_L0: float = 1.0,
) -> float:
    """
    F_Y = F_L0 + F_L5 + F_L6 + F_β + F_COH.
    """
    return (
        force_L0(L0_input, scale_L0)
        + force_L5(c_omega, rho, P_t, S, delta_c)
        + force_L6(weights[5], purpose_magnitude)
        + force_BETA(novelty)
        + force_COH(c_omega, delta_c)
    )


# ===============================================================
# 9. ESTADO FUNDAMENTAL
# ===============================================================

@dataclass
class YoState:
    # ÚNICOS GRADOS DE LIBERTAD INTEGRADOS:
    theta: float = THETA_CUBE
    theta_dot: float = 0.0
    t: float = 0.0

    # Lecturas derivadas:
    phi_y: float = 0.0
    zeta_y: float = 0.0
    omega_y: float = 0.0
    theta_eq: float = THETA_CUBE
    force_y: float = 0.0
    c_omega: float = 0.0
    c_omega_raw: float = 0.0
    delta_c: float = 0.0
    S: float = 0.0
    weights: List[float] = field(
        default_factory=lambda: [1.0 / INTERNAL_LAYERS] * INTERNAL_LAYERS
    )
    energies: List[float] = field(
        default_factory=lambda: [0.0] * INTERNAL_LAYERS
    )
    contributions: List[float] = field(
        default_factory=lambda: [0.0] * INTERNAL_LAYERS
    )
    regime: str = "SUBAMORTIGUADO"


# ===============================================================
# 10. INTEGRACIÓN DEL CARRIL
# ===============================================================

def step_yo(
    state: YoState,
    activations: Sequence[float],
    dt: float,
    L0_input: float = 0.0,
    purpose_magnitude: float = 0.0,
    rho: float = 1.0,
    P_t: float = 1.0,
    A: float = 1.0,
    I_ext: float = 1.0,
    novelty: float = 0.0,
    frictions: Optional[Sequence[float]] = None,
    scale_L0: float = 1.0,
    theta_eq_override: Optional[float] = None,
) -> YoState:
    """
    Un paso de integración semi-implícita:

        θ̈ = F_Y − φ_Y θ̇ − π²(θ_Y − θ_eq)

        θ̇(t+dt) = θ̇(t) + θ̈dt
        θ(t+dt)  = θ(t) + θ̇(t+dt)dt
    """
    if dt <= 0.0:
        raise ValueError("dt debe ser > 0")

    if frictions is None:
        frictions = _default_frictions()

    energies = compute_energies(activations, frictions)
    weights = compute_weights(energies)
    contributions = compute_contributions(
        weights, activations, energies, frictions
    )
    S = shannon_S(weights)

    c_omega = compute_c_omega(
        contributions,
        rho=rho,
        P_t=P_t,
        A=A,
        I_ext=I_ext,
    )

    delta_c = c_omega - float(state.c_omega)

    phi = phi_Y(weights, frictions)
    zeta = zeta_Y(phi)
    omega = omega_Y(phi)
    regime = regime_Y(phi)

    theta_eq = (
        float(theta_eq_override)
        if theta_eq_override is not None
        else dynamic_equilibrium(c_omega, weights)
    )

    force = force_Y(
        L0_input=L0_input,
        weights=weights,
        purpose_magnitude=purpose_magnitude,
        c_omega=c_omega,
        rho=rho,
        P_t=P_t,
        S=S,
        delta_c=delta_c,
        novelty=novelty,
        scale_L0=scale_L0,
    )

    theta = float(state.theta)
    theta_dot = float(state.theta_dot)

    acceleration = (
        force
        - phi * theta_dot
        - PI2 * (theta - theta_eq)
    )

    theta_dot_new = theta_dot + acceleration * float(dt)
    theta_new = theta + theta_dot_new * float(dt)

    return YoState(
        theta=theta_new,
        theta_dot=theta_dot_new,
        t=float(state.t) + float(dt),
        phi_y=phi,
        zeta_y=zeta,
        omega_y=omega,
        theta_eq=theta_eq,
        force_y=force,
        c_omega=c_omega,
        c_omega_raw=c_omega,
        delta_c=delta_c,
        S=S,
        weights=weights,
        energies=energies,
        contributions=contributions,
        regime=regime,
    )


# ===============================================================
# 11. SOLUCIÓN ANALÍTICA — RÉGIMEN CONSTANTE
# ===============================================================

def oscillator_solution_Y(
    t: float,
    amplitude: float,
    delta: float,
    phi_y: float,
    theta_eq: Optional[float] = None,
) -> float:
    """
    Para F_Y ≈ 0 y φ_Y, θ_eq constantes:

        θ_Y(t) =
        θ_eq + A exp(−φ_Y t/2) cos(ω_Y t + δ)
    """
    theta_eq = (
        float(THETA_CUBE)
        if theta_eq is None
        else float(theta_eq)
    )

    omega = omega_Y(phi_y)
    decay = math.exp(-float(phi_y) * float(t) / 2.0)

    return (
        theta_eq
        + float(amplitude)
        * decay
        * math.cos(omega * float(t) + float(delta))
    )


# ===============================================================
# 12. LECTURA DEL CARRIL
# ===============================================================

def read_rail(state: YoState) -> dict:
    """
    Lectura del carril.

    L0 y L7 se exponen únicamente como notas estructurales:
      L0 → entrada externa.
      L7 → emergencia posterior.

    No se mapean estaciones L1...L6 todavía.
    """
    return {
        "theta_Y": state.theta,
        "theta_dot_Y": state.theta_dot,
        "t": state.t,
        "theta_eq": state.theta_eq,
        "phi_Y": state.phi_y,
        "zeta_Y": state.zeta_y,
        "omega_Y": state.omega_y,
        "regime": state.regime,
        "force_Y": state.force_y,
        "C_OMEGA": state.c_omega,
        "C_OMEGA_RAW": state.c_omega_raw,
        "delta_C_OMEGA": state.delta_c,
        "S": state.S,
        "weights_L1_L6": list(state.weights),
        "energies_L1_L6": list(state.energies),
        "contributions_f1_f6": list(state.contributions),
        "ALPHA": ALPHA_F,
        "BETA": BETA_F,
        "THETA_CUBE": float(THETA_CUBE),
        "L0_ROLE": "INPUT_EXTERNAL",
        "L7_ROLE": "EMERGENT_INTEGRATION_OUTPUT",
    }


# ===============================================================
# 13. API L4 — YoOscillator
# ===============================================================

class YoOscillator:
    """
    L4 — Yo Oscilatorio Dinámico.

    Integra únicamente:
        θ_Y, θ̇_Y, t

    Los pesos emergen de E1...E6.
    L0 fuerza el sistema.
    L6 aporta dirección.
    L7 queda fuera del carril como emergencia.
    """

    def __init__(
        self,
        theta0: Optional[float] = None,
        theta_dot0: float = 0.0,
    ):
        self.state = YoState(
            theta=(
                float(THETA_CUBE)
                if theta0 is None
                else float(theta0)
            ),
            theta_dot=float(theta_dot0),
        )

    def step(
        self,
        activations: Sequence[float],
        dt: float,
        L0_input: float = 0.0,
        purpose_magnitude: float = 0.0,
        rho: float = 1.0,
        P_t: float = 1.0,
        A: float = 1.0,
        I_ext: float = 1.0,
        novelty: float = 0.0,
        frictions: Optional[Sequence[float]] = None,
        scale_L0: float = 1.0,
        theta_eq_override: Optional[float] = None,
    ) -> dict:
        self.state = step_yo(
            self.state,
            activations=activations,
            dt=dt,
            L0_input=L0_input,
            purpose_magnitude=purpose_magnitude,
            rho=rho,
            P_t=P_t,
            A=A,
            I_ext=I_ext,
            novelty=novelty,
            frictions=frictions,
            scale_L0=scale_L0,
            theta_eq_override=theta_eq_override,
        )
        return read_rail(self.state)

    def snapshot(self) -> dict:
        return read_rail(self.state)


# ===============================================================
# EXPORTS
# ===============================================================

__all__ = [
    "compute_energies",
    "compute_weights",
    "compute_contributions",
    "shannon_S",
    "normalized_entropy",
    "negentropy",
    "compute_c_omega",
    "phi_Y",
    "zeta_Y",
    "omega_Y",
    "regime_Y",
    "dynamic_equilibrium",
    "force_L0",
    "force_L5",
    "force_L6",
    "force_BETA",
    "force_COH",
    "force_Y",
    "YoState",
    "step_yo",
    "oscillator_solution_Y",
    "read_rail",
    "YoOscillator",
]
