# ===============================================================
# L4 — YO OSCILATORIO DINÁMICO  (carril)
# ===============================================================
#
# PROPÓSITO
# ---------
# Implementar el grado de libertad continuo del Yo:
#
#     d²θ_Y/dt²  +  φ_Y(t)·dθ_Y/dt  +  π²·(θ_Y(t) − θ_eq(t))  =  F_Y(t)
#
# No es una máquina de estados.
# No asigna θ_Y = L4 ni θ_Y = L5 ni θ_Y = L6.
# Las capas L1…L6 serán interpretaciones posteriores sobre este carril.
#
# CIRCUITO (única responsabilidad de este módulo)
# -----------------------------------------------
#   actividad → E_i → w_i → f_i → C_Ω
#                    ↘ φ_Y, F_Y, θ_eq → θ_Y → θ̇_Y → nuevo estado → E_i(t+dt)
#
# CORPUS vs EXTENSIÓN
# -------------------
#   Documentado / conservado:
#     • Ecuación de oscilador amortiguado con atractor geométrico
#     • f_i = w_i · L_i · (1 − φ_i) · E_i
#     • C_Ω = α · S_REF · Π f_i · R_FIN · Res_ζ · P_t · A · I_ext
#     • α = 26/27, β = 1/27, α+β = 1
#     • φ_6 = 0 (L6 no introduce fricción propia)
#     • L4 = Yo Oscilador; relaciones L6–L4, L5–L4, …, L4–L1
#
#   Extensión arquitectónica (explícita, no atribuida al libro):
#     • w_i(t) = E_i(t) / Σ_j E_j(t)   (pesos emergentes)
#     • φ_Y(t) = Σ_i w_i(t)·φ_i(t)     (con φ_6 = 0)
#     • F_Y = F_L0 + F_L5 + F_L6 + F_BETA + F_COH
#     • F_L6 = w_6 · P
#     • θ_eq = θ_eq(t)  (equilibrio instantáneo, no solo θ_cube fijo)
#
# Este archivo solo calcula. No orquesta. No declara contrato de Engine.
# ===============================================================

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import List, Optional, Sequence, Tuple

# ------------------------------------------------------------------
# IMPORTS ESTRUCTURALES
# En el repo real usar la ruta canónica del paquete.
# ------------------------------------------------------------------
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
        NUM_LAYERS,
        R_FIN,
        S_REF,
    )
    from .energy import LayerEnergy
except Exception:
    # Fallback mínimo de desarrollo (no usar en CI)
    PHI = (1.0 + math.sqrt(5.0)) / 2.0
    THETA_CUBE = math.asin(1.0 / math.sqrt(27.0))
    PHI_CRITICAL = 2.0 * math.pi
    NUM_LAYERS = 7
    LAYER_FRICTION = [0.10, 0.02, 0.05, 0.03, 0.01, 0.01, 0.00]
    R_FIN = 1.0 + float(BETA)
    S_REF = math.e / math.pi

    class LayerEnergy:
        @staticmethod
        def frequency(i: int) -> float:
            return PHI ** (i / 2.0)

        @staticmethod
        def compute(activation: float, friction: float, layer_index: int) -> float:
            return float(activation) * (1.0 - float(friction)) * LayerEnergy.frequency(layer_index)

        @staticmethod
        def compute_all(activations, frictions=None):
            if frictions is None:
                frictions = LAYER_FRICTION
            return [
                LayerEnergy.compute(activations[i], frictions[i], i)
                for i in range(NUM_LAYERS)
            ]


# ===============================================================
# CONSTANTES ESTRUCTURALES (marco — no dinámicas)
# ===============================================================
#
# ALPHA  = 26/27   techo observable (fracción exterior del cubo)
# BETA   =  1/27   residuo del observador (piso irreducible)
# ALPHA + BETA = 1
#
# No son pesos de capa. No se reasignan en runtime.

ALPHA_F: float = float(ALPHA)
BETA_F: float = float(BETA)
PI2: float = math.pi * math.pi


# ===============================================================
# VARIABLES — DEFINICIONES
# ===============================================================
#
# ESTADO DEL CARRIL (lo que integra el DE)
#   theta_Y      θ_Y(t)      posición continua del Yo en el carril [rad]
#   theta_dot_Y  θ̇_Y(t)     velocidad de desplazamiento [rad/s]
#   t            t          tiempo de integración [s]
#
# ENTRADAS DE CAPA (medidas)
#   L_i          activations[i]     activación de la capa i ∈ [0,1]
#   phi_i        frictions[i]       fricción estructural de la capa i
#   L0_input     L0_input           entrada / calle / caos (forzamiento)
#   P            purpose_magnitude  magnitud de dirección (L6)
#   Res_zeta     rho                resonancia inter-capa
#   P_t          P_t                presencia temporal
#   A            novelty_factor     factor de novedad A(N)=1−e^(−N/k)
#   I_ext        I_ext              interferencia / coherencia externa
#
# DERIVADAS OPERACIONALES
#   E_i          energies[i]   energía operacional de capa
#                              E_i = L_i · (1−φ_i) · ν_i
#                              ν_i = PHI^(i/2)
#   w_i          weights[i]    peso emergente
#                              w_i = E_i / Σ_j E_j   (extensión)
#   f_i          contrib[i]    contribución documental de capa
#                              f_i = w_i · L_i · (1−φ_i) · E_i
#   S            S             entropía de la distribución w
#                              S = −Σ w_i ln w_i
#   C_OMEGA      c_omega       coherencia estructural
#   phi_Y        phi_y         amortiguamiento efectivo del Yo
#                              φ_Y = Σ_i w_i·φ_i   (φ_6 = 0)
#   zeta_Y       zeta_y        ζ_Y = φ_Y / (2π)
#   omega_Y      omega_y       ω_Y = π·√(1−ζ_Y²) si ζ_Y < 1
#   theta_eq     theta_eq      equilibrio instantáneo θ_eq(t)
#   F_Y          force_y       forzamiento total del carril
#
# RÉGIMEN (matemático, no semántica humana obligatoria)
#   subamortiguado   ζ_Y < 1
#   crítico          ζ_Y = 1
#   sobreamortiguado ζ_Y > 1
# ===============================================================


# ===============================================================
# 1. ENERGÍA OPERACIONAL E_i
# ===============================================================

def compute_energies(
    activations: Sequence[float],
    frictions: Optional[Sequence[float]] = None,
) -> List[float]:
    """
    E_i(t) = L_i · (1 − φ_i) · ν_i
    ν_i = PHI^(i/2)

    Energía operacional de cada capa (magnitud abstracta del modelo).
    """
    if frictions is None:
        frictions = LAYER_FRICTION
    if len(activations) != NUM_LAYERS:
        raise ValueError(
            "activations debe tener longitud NUM_LAYERS={0}, recibido {1}".format(
                NUM_LAYERS, len(activations)
            )
        )
    return LayerEnergy.compute_all(list(activations), list(frictions))


# ===============================================================
# 2. PESOS EMERGENTES w_i  (extensión arquitectónica)
# ===============================================================

def compute_weights(energies: Sequence[float]) -> List[float]:
    """
    w_i(t) = E_i(t) / Σ_j E_j(t)

    Extensión: normalización por energía total.
    Si Σ E_j = 0 → distribución uniforme (evita singularidad).
    Los pesos NO se asignan manualmente.
    """
    total = sum(max(0.0, float(e)) for e in energies)
    n = len(energies)
    if total <= 0.0:
        return [1.0 / n] * n
    return [max(0.0, float(e)) / total for e in energies]


# ===============================================================
# 3. CONTRIBUCIÓN DOCUMENTAL f_i
# ===============================================================

def compute_contributions(
    weights: Sequence[float],
    activations: Sequence[float],
    energies: Sequence[float],
    frictions: Optional[Sequence[float]] = None,
) -> List[float]:
    """
    f_i(t) = w_i(t) · L_i(t) · (1 − φ_i(t)) · E_i(t)

    Pieza documental de la fórmula maestra de coherencia.
    No sustituir por otra definición.
    """
    if frictions is None:
        frictions = LAYER_FRICTION
    out: List[float] = []
    for i in range(NUM_LAYERS):
        w = float(weights[i])
        L = float(activations[i])
        phi = float(frictions[i])
        E = float(energies[i])
        out.append(w * L * (1.0 - phi) * E)
    return out


# ===============================================================
# 4. ENTROPÍA DE LA DISTRIBUCIÓN
# ===============================================================

def shannon_S(weights: Sequence[float]) -> float:
    """S(t) = −Σ_i w_i ln w_i  (solo w_i > 0)."""
    s = 0.0
    for w in weights:
        if w > 0.0:
            s -= w * math.log(w)
    return s


# ===============================================================
# 5. COHERENCIA C_Ω  (forma documental)
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
    C_Ω(t) =
        α · S_REF · (Π_i f_i) · R_FIN · Res_ζ · P_t · A · I_ext

    Magnitud de coherencia estructural.
    No es “conciencia”. Puede retroalimentar F_Y si se define F_COH.
    """
    if s_ref is None:
        s_ref = float(S_REF)
    if r_fin is None:
        r_fin = float(R_FIN)

    product = 1.0
    for f in contributions:
        product *= max(0.0, float(f))

    return (
        ALPHA_F
        * float(s_ref)
        * product
        * float(r_fin)
        * float(rho)
        * float(P_t)
        * float(A)
        * float(I_ext)
    )


# ===============================================================
# 6. AMORTIGUAMIENTO DEL YO φ_Y
# ===============================================================

def phi_Y(
    weights: Sequence[float],
    frictions: Optional[Sequence[float]] = None,
) -> float:
    """
    φ_Y(t) = Σ_i w_i(t) · φ_i(t)

    Con invariante φ_6 = 0: L6 no aporta fricción; solo dirección.
    """
    if frictions is None:
        frictions = LAYER_FRICTION
    acc = 0.0
    for i in range(NUM_LAYERS):
        phi_i = float(frictions[i])
        if i == 6:
            phi_i = 0.0  # invariante estructural
        acc += float(weights[i]) * phi_i
    return acc


def zeta_Y(phi_y: float) -> float:
    """ζ_Y(t) = φ_Y(t) / (2π)."""
    return float(phi_y) / (2.0 * math.pi)


def omega_Y(phi_y: float) -> float:
    """
    ω_Y(t) = π · √(1 − ζ_Y²)   si ζ_Y < 1
           = 0                 si ζ_Y ≥ 1
    """
    z = zeta_Y(phi_y)
    if z >= 1.0:
        return 0.0
    return math.pi * math.sqrt(max(0.0, 1.0 - z * z))


def regime_Y(phi_y: float) -> str:
    """
    Régimen dinámico matemático:
      ζ < 1 → SUBAMORTIGUADO
      ζ = 1 → CRITICO
      ζ > 1 → SOBREAMORTIGUADO
    """
    z = zeta_Y(phi_y)
    if abs(z - 1.0) < 1e-12:
        return "CRITICO"
    if z < 1.0:
        return "SUBAMORTIGUADO"
    return "SOBREAMORTIGUADO"


# ===============================================================
# 7. EQUILIBRIO DINÁMICO θ_eq(t)
# ===============================================================

def dynamic_equilibrium(
    c_omega: float,
    weights: Sequence[float],
    activations: Sequence[float],
    base: Optional[float] = None,
) -> float:
    """
    θ_eq(t) = dynamic_equilibrium(C_Ω, w_i, L_i, …)

    Extensión: el atractor deja de ser un punto inmóvil.
    θ_cube permanece como referencia geométrica base.
    El desplazamiento instantáneo es función acotada del estado.

    Forma mínima auditable (no antropomórfica):
      θ_eq = θ_cube + β · (C_Ω/α − 1) · π/27
             + desplazamiento leve por desbalance de pesos altos

    No introduce emociones ni etiquetas de capa.
    """
    if base is None:
        base = float(THETA_CUBE)

    # tracción por coherencia relativa al techo α
    c_ratio = float(c_omega) / max(ALPHA_F, 1e-15)
    shift_coh = BETA_F * (c_ratio - 1.0) * (math.pi / 27.0)

    # desbalance hacia capas altas (L4–L6) vs bajas (L0–L2)
    w = [float(x) for x in weights]
    high = sum(w[4:7]) if len(w) >= 7 else 0.0
    low = sum(w[0:3]) if len(w) >= 3 else 0.0
    shift_w = BETA_F * (high - low) * (math.pi / 54.0)

    return float(base) + shift_coh + shift_w


# ===============================================================
# 8. FUERZAS  F_Y = F_L0 + F_L5 + F_L6 + F_BETA + F_COH
# ===============================================================
#
# Cada término sale de magnitudes computables.
# Prohibido: emotion, desire, fear, self_awareness como variables.

def force_L0(L0_input: float, scale: float = 1.0) -> float:
    """
    F_L0(t) — entrada / calle / caos.
    L0 no es estado libre del oscilador: es forzamiento externo.
    """
    return float(scale) * float(L0_input)


def force_L5(
    c_omega: float,
    rho: float,
    P_t: float,
    S: float,
    delta_c: float = 0.0,
) -> float:
    """
    F_L5(t) — meta-retroalimentación (canal L5 → proceso).

    No es “if reflection: go_to_L5”.
    L5 modifica la dinámica por magnitudes: E5 → w5 → C_Ω → F_L5.
    """
    s_norm = float(S) / max(math.log(max(NUM_LAYERS, 2)), 1e-12)
    drive = float(rho) * float(P_t) * float(c_omega)
    return drive + 0.5 * float(delta_c) - BETA_F * s_norm


def force_L6(w6: float, purpose_magnitude: float) -> float:
    """
    F_L6(t) = w_6(t) · P(t)

    Extensión de implementación.
    Principio respaldado: L6 = dirección / propósito (no fricción).
    """
    return float(w6) * float(purpose_magnitude)


def force_BETA(novelty: float = 0.0, k: Optional[float] = None) -> float:
    """
    F_BETA(t) = β · A(N)
    A(N) = 1 − e^(−N/k)

    Margen irreducible: β ≠ 0 impide cierre absoluto del estado.
    """
    if k is None or k <= 0.0:
        k = float(S_REF) if float(S_REF) > 0.0 else 1.0
    A = 1.0 - math.exp(-max(0.0, float(novelty)) / k)
    return BETA_F * A


def force_COH(c_omega: float, delta_c: float = 0.0) -> float:
    """
    F_COH(t) — retroalimentación directa de coherencia al carril.

    Penaliza pretender C_Ω > α (techo estructural).
    Premia variación (anti-loop): si ΔC ≈ 0 y C alto, el empuje baja.
    """
    excess = max(0.0, float(c_omega) - ALPHA_F)
    return float(c_omega) * float(delta_c) - excess


def force_Y(
    L0_input: float,
    weights: Sequence[float],
    purpose_magnitude: float,
    c_omega: float,
    rho: float = 1.0,
    P_t: float = 1.0,
    S: float = 1.0,
    delta_c: float = 0.0,
    novelty: float = 0.0,
    I_ext: float = 1.0,
    scale_L0: float = 1.0,
) -> float:
    """
    F_Y(t) = F_L0 + F_L5 + F_L6 + F_BETA + F_COH

    Forzamiento total del carril.
    """
    w6 = float(weights[6]) if len(weights) > 6 else 0.0
    return (
        force_L0(L0_input, scale=scale_L0)
        + force_L5(c_omega, rho=rho, P_t=P_t, S=S, delta_c=delta_c)
        + force_L6(w6, purpose_magnitude)
        + force_BETA(novelty)
        + force_COH(c_omega, delta_c=delta_c)
    )


# ===============================================================
# 9. ESTADO DEL CARRIL
# ===============================================================

@dataclass
class YoState:
    """
    Estado fundamental que integra el DE.

    Solo:
      theta_Y, theta_dot_Y, t

    Más lectura operacional del último paso (no grados de libertad extra).
    """
    theta: float = THETA_CUBE
    theta_dot: float = 0.0
    t: float = 0.0
    # lectura del último paso
    phi_y: float = 0.0
    zeta_y: float = 0.0
    omega_y: float = 0.0
    theta_eq: float = THETA_CUBE
    force_y: float = 0.0
    c_omega: float = 0.0
    S: float = 0.0
    weights: List[float] = field(default_factory=lambda: [1.0 / NUM_LAYERS] * NUM_LAYERS)
    energies: List[float] = field(default_factory=lambda: [0.0] * NUM_LAYERS)
    contributions: List[float] = field(default_factory=lambda: [0.0] * NUM_LAYERS)
    regime: str = "SUBAMORTIGUADO"


# ===============================================================
# 10. PASO DE INTEGRACIÓN
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
    delta_c: float = 0.0,
    frictions: Optional[Sequence[float]] = None,
    scale_L0: float = 1.0,
    theta_eq_override: Optional[float] = None,
) -> YoState:
    """
    Un paso del DE:

        θ̈_Y = F_Y − φ_Y · θ̇_Y − π² · (θ_Y − θ_eq)

    Integración semi-implícita de Euler (estable a dt pequeños).

    No muta `state`. Devuelve un YoState nuevo.
    """
    if frictions is None:
        frictions = LAYER_FRICTION

    # --- cadena causal ---
    energies = compute_energies(activations, frictions)
    weights = compute_weights(energies)
    contribs = compute_contributions(weights, activations, energies, frictions)
    S = shannon_S(weights)
    c_omega = compute_c_omega(
        contribs, rho=rho, P_t=P_t, A=A, I_ext=I_ext
    )

    phi = phi_Y(weights, frictions)
    z = zeta_Y(phi)
    om = omega_Y(phi)
    reg = regime_Y(phi)

    if theta_eq_override is not None:
        theta_eq = float(theta_eq_override)
    else:
        theta_eq = dynamic_equilibrium(c_omega, weights, activations)

    F = force_Y(
        L0_input=L0_input,
        weights=weights,
        purpose_magnitude=purpose_magnitude,
        c_omega=c_omega,
        rho=rho,
        P_t=P_t,
        S=S,
        delta_c=delta_c,
        novelty=novelty,
        I_ext=I_ext,
        scale_L0=scale_L0,
    )

    theta = float(state.theta)
    theta_dot = float(state.theta_dot)

    # aceleración
    acc = F - phi * theta_dot - PI2 * (theta - theta_eq)

    # semi-implícito
    theta_dot_new = theta_dot + acc * float(dt)
    theta_new = theta + theta_dot_new * float(dt)

    return YoState(
        theta=theta_new,
        theta_dot=theta_dot_new,
        t=float(state.t) + float(dt),
        phi_y=phi,
        zeta_y=z,
        omega_y=om,
        theta_eq=theta_eq,
        force_y=F,
        c_omega=c_omega,
        S=S,
        weights=weights,
        energies=energies,
        contributions=contribs,
        regime=reg,
    )


def oscillator_solution_Y(
    t: float,
    A: float,
    delta: float,
    phi_y: float,
    theta_eq: Optional[float] = None,
) -> float:
    """
    Solución analítica cuando F_Y ≈ 0 y φ_Y, θ_eq constantes:

        θ_Y(t) = θ_eq + A · e^(−φ_Y·t/2) · cos(ω_Y·t + δ)
    """
    if theta_eq is None:
        theta_eq = float(THETA_CUBE)
    om = omega_Y(phi_y)
    decay = math.exp(-float(phi_y) * float(t) / 2.0)
    return float(theta_eq) + float(A) * decay * math.cos(om * float(t) + float(delta))


# ===============================================================
# 11. LECTURA DEL CARRIL (sin casas)
# ===============================================================

def read_rail(state: YoState) -> dict:
    """
    Snapshot estructural del carril.
    No mapea a estaciones L1…L6 (fase posterior).
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
        "S": state.S,
        "weights": list(state.weights),
        "energies": list(state.energies),
        "contributions_f_i": list(state.contributions),
        "ALPHA": ALPHA_F,
        "BETA": BETA_F,
        "THETA_CUBE": float(THETA_CUBE),
    }


# ===============================================================
# 12. API L4 — YoOscillator
# ===============================================================

class YoOscillator:
    """
    L4 — carril del Yo Oscilatorio Dinámico.

    Integra únicamente (θ_Y, θ̇_Y, t).
    Pesos emergentes desde energía.
    φ_6 = 0.
    θ_eq dinámico.
    Retroalimentación por magnitudes computables (no etiquetas).
    """

    def __init__(
        self,
        theta0: Optional[float] = None,
        theta_dot0: float = 0.0,
    ):
        self.state = YoState(
            theta=float(theta0) if theta0 is not None else float(THETA_CUBE),
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
        delta_c: float = 0.0,
        frictions: Optional[Sequence[float]] = None,
        scale_L0: float = 1.0,
        theta_eq_override: Optional[float] = None,
    ) -> dict:
        """
        Avanza el carril un paso dt y devuelve read_rail().
        """
        # delta_c por defecto: cambio respecto al C_Ω anterior
        if delta_c == 0.0 and self.state.c_omega != 0.0:
            # el caller puede pasar delta_c explícito; si no, 0
            pass

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
            delta_c=delta_c,
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
    # energía / pesos / contribución
    "compute_energies",
    "compute_weights",
    "compute_contributions",
    "shannon_S",
    # coherencia
    "compute_c_omega",
    # amortiguamiento y régimen
    "phi_Y",
    "zeta_Y",
    "omega_Y",
    "regime_Y",
    # equilibrio y fuerzas
    "dynamic_equilibrium",
    "force_L0",
    "force_L5",
    "force_L6",
    "force_BETA",
    "force_COH",
    "force_Y",
    # integración
    "YoState",
    "step_yo",
    "oscillator_solution_Y",
    "read_rail",
    "YoOscillator",
]
