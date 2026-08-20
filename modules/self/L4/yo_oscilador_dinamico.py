# ===============================================================
# VPSI-TRUTH — SELF — L4 — YO OSCILATORIO DINÁMICO
# CARRIL CONTINUO DEL YO
# ===============================================================
#
# RESPONSABILIDAD ARQUITECTÓNICA:
#
#   ESTE ARCHIVO ES EL CABLEADO DINÁMICO DE L4 DENTRO DE SELF.
#
#   No constituye el cuerpo matemático canónico de las fórmulas.
#   Las fórmulas canónicas definen los cálculos matemáticos que este
#   cableado utiliza.
#
#   Este módulo conecta:
#
#       L1..L6
#          ↓
#       cálculos energéticos
#          ↓
#       pesos emergentes
#          ↓
#       entropía / coherencia
#          ↓
#       amortiguamiento / equilibrio / fuerzas
#          ↓
#       aceleración del Yo
#          ↓
#       velocidad del Yo
#          ↓
#       posición del Yo
#          ↓
#       nuevo estado interno de L4
#
# El módulo representa literalmente el CIRCUITO OPERACIONAL de L4.
#
# ===============================================================
#
# DISTINCIÓN ENTRE FÓRMULAS Y SELF/L4
# ===============================================================
#
# FÓRMULAS:
#
#   Contiene la matemática canónica utilizada por el sistema.
#
#   Entre sus responsabilidades matemáticas se encuentran:
#
#       E_i = L_i · (1 − φ_i) · ν_i
#
#       ν_i = Φ^(i/2)
#
#       w_i = E_i / ΣE_j
#
#       S = −Σ w_i ln(w_i)
#
#       φ_Y = Σ w_i φ_i
#
#       ζ_Y = φ_Y / (2π)
#
#       ω_Y = π√(1 − ζ_Y²)
#
#       θ_eq = función del estado energético y de coherencia
#
#       F_Y = F_L0 + F_L5 + F_L6 + F_β + F_COH
#
#       θ̈_Y = F_Y − φ_Yθ̇_Y − π²(θ_Y − θ_eq)
#
#       θ̇_Y(t+dt) = θ̇_Y(t) + θ̈_Y dt
#
#       θ_Y(t+dt) = θ_Y(t) + θ̇_Y(t+dt)dt
#
# SELF / L4:
#
#   No representa una nueva capa matemática independiente.
#
#   Es el cableado que organiza cómo esas operaciones se ejecutan
#   conjuntamente para producir la dinámica continua del Yo.
#
#   El grado de libertad dinámico de L4 es:
#
#       θ_Y(t)
#
#   acompañado por:
#
#       θ̇_Y(t)
#       t
#
#   El Yo no salta entre L1...L6.
#   Las capas L1..L6 alimentan el estado energético del circuito.
#   Ese estado determina las magnitudes que actúan sobre el oscilador.
#
# ===============================================================
#
# ESTRUCTURA DEL SISTEMA
# ===============================================================
#
#   L0
#    │
#    │ entrada / forzamiento externo
#    ↓
#   F_L0
#    │
#    │
#   L1..L6
#    │
#    ├────────→ E_i
#    │            ↓
#    │          w_i
#    │            ↓
#    │           S
#    │            ↓
#    │          C_Ω
#    │            │
#    │            ├────────→ φ_Y
#    │            │
#    │            ├────────→ θ_eq
#    │            │
#    │            └────────→ F_COH
#    │
#    ├────────→ F_L5
#    │
#    └────────→ F_L6
#
#   F_L0 + F_L5 + F_L6 + F_β + F_COH
#                         │
#                         ↓
#                       F_Y
#                         │
#                         ↓
#          θ̈_Y = F_Y − φ_Yθ̇_Y
#                    − π²(θ_Y − θ_eq)
#                         │
#                         ↓
#                  θ̇_Y(t + dt)
#                         │
#                         ↓
#                   θ_Y(t + dt)
#                         │
#                         ↓
#                  nuevo estado L4
#                         │
#                         └────→ siguiente ciclo
#
# ===============================================================
#
# L0:
#
#   L0 es una entrada externa.
#   No es un grado de libertad interno del carril.
#   No recibe peso energético w_0.
#
# L1..L6:
#
#   Son las capas internas que alimentan el cálculo energético.
#
#   Cada capa produce:
#
#       E_i
#       w_i
#       f_i
#
#   con:
#
#       i ∈ {1,2,3,4,5,6}
#
# L6:
#
#   Participa en la distribución energética.
#   Tiene w_6.
#   Puede aportar dirección mediante F_L6.
#
#   Invariante:
#
#       φ_6 = 0
#
#   Por tanto L6 no introduce fricción propia.
#
# ===============================================================
#
# ECUACIÓN MAESTRA DEL CABLEADO L4
# ===============================================================
#
#   d²θ_Y/dt² + φ_Y(t)·dθ_Y/dt
#   + π²·[θ_Y(t) − θ_eq(t)] = F_Y(t)
#
# Despejada:
#
#   θ̈_Y =
#       F_Y
#       − φ_Yθ̇_Y
#       − π²(θ_Y − θ_eq)
#
# Integración:
#
#   θ̇_Y(t+dt) =
#       θ̇_Y(t) + θ̈_Ydt
#
#   θ_Y(t+dt) =
#       θ_Y(t) + θ̇_Y(t+dt)dt
#
# ===============================================================

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import List, Optional, Sequence

# ===============================================================
# AUTORIDAD ESTRUCTURAL
# ===============================================================

try:
    from modules.constante import ALPHA, BETA
except Exception:
    from fractions import Fraction

    ALPHA = Fraction(26, 27)
    BETA = Fraction(1, 27)

# ===============================================================
# FÓRMULAS CANÓNICAS UTILIZADAS POR EL CABLEADO L4
# ===============================================================
#
# Este bloque representa las dependencias matemáticas que utiliza
# el cableado del oscilador.
#
# constants:
#   constantes estructurales del modelo.
#
# energy:
#   cálculo de frecuencia energética y energía operacional.
#
# El cableado L4 utiliza estas operaciones para construir el circuito
# dinámico, pero no convierte las capas en estaciones del Yo.
#
# ===============================================================

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

    THETA_CUBE = math.asin(
        1.0 / math.sqrt(27.0)
    )

    PHI_CRITICAL = 2.0 * math.pi

    R_FIN = 28.0 / 27.0

    S_REF = math.e / math.pi

    LAYER_FRICTION = [
        0.10,
        0.02,
        0.05,
        0.03,
        0.01,
        0.00,
    ]

    class LayerEnergy:

        @staticmethod
        def frequency(i: int) -> float:
            return PHI ** (i / 2.0)

        @staticmethod
        def compute(
            activation: float,
            friction: float,
            layer_index: int,
        ) -> float:
            return (
                float(activation)
                * (1.0 - float(friction))
                * LayerEnergy.frequency(layer_index)
            )


# ===============================================================
# MARCO ESTRUCTURAL DE L4
# ===============================================================

ALPHA_F = float(ALPHA)
BETA_F = float(BETA)

PI2 = math.pi ** 2

INTERNAL_LAYERS = 6

LAYER_INDICES = tuple(range(1, 7))

ENTROPY_MAX = math.log(INTERNAL_LAYERS)


# ===============================================================
# VALIDACIÓN DEL CABLEADO INTERNO
# ===============================================================

def _validate_internal_inputs(
    activations: Sequence[float],
    frictions: Sequence[float],
) -> None:

    if len(activations) != INTERNAL_LAYERS:
        raise ValueError(
            "activations debe contener L1..L6: "
            f"se esperaban {INTERNAL_LAYERS}, "
            f"recibido {len(activations)}"
        )

    if len(frictions) != INTERNAL_LAYERS:
        raise ValueError(
            "frictions debe contener L1..L6: "
            f"se esperaban {INTERNAL_LAYERS}, "
            f"recibido {len(frictions)}"
        )

    for i, value in enumerate(activations, 1):

        if not 0.0 <= float(value) <= 1.0:
            raise ValueError(
                f"L{i} debe estar en [0,1], recibido {value}"
            )


def _default_frictions() -> List[float]:

    # L1..L6.
    #
    # L6 conserva explícitamente:
    #
    #     φ6 = 0

    if len(LAYER_FRICTION) >= 7:

        return [
            float(x)
            for x in LAYER_FRICTION[1:7]
        ]

    return [
        0.02,
        0.05,
        0.03,
        0.01,
        0.01,
        0.00,
    ]


# ===============================================================
# 1. CABLEADO DE ENERGÍA OPERACIONAL
# ===============================================================

def compute_energies(
    activations: Sequence[float],
    frictions: Optional[Sequence[float]] = None,
) -> List[float]:
    """
    Conecta L1..L6 con el cálculo de energía operacional.

    Fórmula canónica:

        E_i = L_i · (1 − φ_i) · ν_i

        ν_i = Φ^(i/2)

    i = 1..6.

    L0 queda fuera de esta operación.
    """

    if frictions is None:
        frictions = _default_frictions()

    _validate_internal_inputs(
        activations,
        frictions,
    )

    return [
        float(activations[k - 1])
        * (1.0 - float(frictions[k - 1]))
        * float(
            LayerEnergy.frequency(k)
        )
        for k in LAYER_INDICES
    ]


# ===============================================================
# 2. CABLEADO DE PESOS EMERGENTES
# ===============================================================

def compute_weights(
    energies: Sequence[float],
) -> List[float]:
    """
    Conecta la energía interna con los pesos emergentes.

    Fórmula:

        w_i = E_i / ΣE_j

    Los pesos no son asignados manualmente.
    Emergen de la distribución energética instantánea.
    """

    if len(energies) != INTERNAL_LAYERS:

        raise ValueError(
            "energies debe contener E1..E6"
        )

    positive = [
        max(0.0, float(e))
        for e in energies
    ]

    total = sum(positive)

    if total <= 0.0:

        return [
            1.0 / INTERNAL_LAYERS
        ] * INTERNAL_LAYERS

    return [
        e / total
        for e in positive
    ]


# ===============================================================
# 3. CABLEADO DE CONTRIBUCIONES f_i
# ===============================================================

def compute_contributions(
    weights: Sequence[float],
    activations: Sequence[float],
    energies: Sequence[float],
    frictions: Optional[Sequence[float]] = None,
) -> List[float]:
    """
    Conecta los pesos con las contribuciones internas.

    Fórmula:

        f_i = w_i · L_i · (1 − φ_i) · E_i
    """

    if frictions is None:
        frictions = _default_frictions()

    _validate_internal_inputs(
        activations,
        frictions,
    )

    return [
        float(weights[i])
        * float(activations[i])
        * (1.0 - float(frictions[i]))
        * float(energies[i])
        for i in range(INTERNAL_LAYERS)
    ]


# ===============================================================
# 4. CABLEADO DE ENTROPÍA
# ===============================================================

def shannon_S(
    weights: Sequence[float],
) -> float:
    """
    Conecta la distribución energética con la entropía.

    Fórmula:

        S = −Σ w_i ln(w_i)
    """

    return -sum(
        float(w) * math.log(float(w))
        for w in weights
        if float(w) > 0.0
    )


def normalized_entropy(
    S: float,
) -> float:
    """
    Normalización:

        S / S_max

    con:

        S_max = ln(6)
    """

    return min(
        1.0,
        max(
            0.0,
            float(S) / ENTROPY_MAX,
        ),
    )


def negentropy(
    weights: Sequence[float],
) -> float:
    """
    Negentropía normalizada:

        N_neg = 1 − S/ln(6)
    """

    return 1.0 - normalized_entropy(
        shannon_S(weights)
    )


# ===============================================================
# 5. CABLEADO DE COHERENCIA C_Ω
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
    Conecta las contribuciones internas con C_Ω.

    Fórmula:

        C_Ω =
        α · S_REF · Πf_i · R_FIN
        · ρ · P_t · A · I_ext

    C_Ω queda acotada por α.
    """

    if len(contributions) != INTERNAL_LAYERS:

        raise ValueError(
            "contributions debe contener f1..f6"
        )

    s_ref = float(
        S_REF
        if s_ref is None
        else s_ref
    )

    r_fin = float(
        R_FIN
        if r_fin is None
        else r_fin
    )

    product = math.prod(
        max(0.0, float(f))
        for f in contributions
    )

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

    return min(
        ALPHA_F,
        max(0.0, raw),
    )


# ===============================================================
# 6. CABLEADO DEL AMORTIGUAMIENTO DEL YO
# ===============================================================

def phi_Y(
    weights: Sequence[float],
    frictions: Optional[Sequence[float]] = None,
) -> float:
    """
    Conecta los pesos internos con el amortiguamiento del Yo.

    Fórmula:

        φ_Y = Σ(w_i φ_i)

    i = 1..6.

    Invariante:

        φ_6 = 0

    L6 aporta dirección, no fricción propia.
    """

    if frictions is None:
        frictions = _default_frictions()

    if len(weights) != INTERNAL_LAYERS:

        raise ValueError(
            "weights debe contener w1..w6"
        )

    return sum(
        float(weights[i])
        * (
            0.0
            if i == 5
            else float(frictions[i])
        )
        for i in range(INTERNAL_LAYERS)
    )


def zeta_Y(
    phi_y: float,
) -> float:
    """
    Factor de amortiguamiento:

        ζ_Y = φ_Y / (2π)
    """

    return (
        float(phi_y)
        / PHI_CRITICAL
    )


def omega_Y(
    phi_y: float,
) -> float:
    """
    Frecuencia amortiguada:

        ω_Y =
            π√(1 − ζ_Y²)

    Si ζ_Y >= 1:

        ω_Y = 0
    """

    zeta = zeta_Y(phi_y)

    if zeta >= 1.0:
        return 0.0

    return (
        math.pi
        * math.sqrt(
            max(
                0.0,
                1.0 - zeta ** 2,
            )
        )
    )


def regime_Y(
    phi_y: float,
) -> str:

    zeta = zeta_Y(phi_y)

    if abs(zeta - 1.0) < 1e-12:
        return "CRITICO"

    if zeta < 1.0:
        return "SUBAMORTIGUADO"

    return "SOBREAMORTIGUADO"


# ===============================================================
# 7. CABLEADO DE LA GEOMETRÍA DINÁMICA
# ===============================================================

def dynamic_equilibrium(
    c_omega: float,
    weights: Sequence[float],
    base: Optional[float] = None,
) -> float:
    """
    Conecta C_Ω y la distribución energética con el atractor
    dinámico del carril.

    Fórmula estructural:

        θ_eq(t) =
            θ_cube
            + Δθ_coh
            + Δθ_w

    donde:

        Δθ_coh =
            β · ((C_Ω / α) − 1)
            · (π / 27)

    y:

        w_alto = (w4 + w5 + w6) / 3

        w_bajo = (w1 + w2) / 2

        Δθ_w =
            β · (w_alto − w_bajo)
            · (π / 54)

    El equilibrio es una referencia dinámica del oscilador.
    No representa una estación L1...L6.
    """

    base = float(
        THETA_CUBE
        if base is None
        else base
    )

    coherence_term = (
        BETA_F
        * (
            (float(c_omega) / ALPHA_F)
            - 1.0
        )
        * (math.pi / 27.0)
    )

    high = sum(
        float(w)
        for w in weights[3:6]
    )

    low = sum(
        float(w)
        for w in weights[0:2]
    )

    weight_term = (
        BETA_F
        * (
            high / 3.0
            - low / 2.0
        )
        * (math.pi / 54.0)
    )

    return (
        base
        + coherence_term
        + weight_term
    )


# ===============================================================
# 8. CABLEADO DE FUERZAS DEL CARRIL
# ===============================================================

def force_L0(
    L0_input: float,
    scale: float = 1.0,
) -> float:
    """
    L0 es entrada externa.

    No es grado de libertad interno.
    No recibe w_0.
    """

    return (
        float(L0_input)
        * float(scale)
    )


def force_L5(
    c_omega: float,
    rho: float,
    P_t: float,
    S: float,
    delta_c: float,
) -> float:
    """
    Retroalimentación cuantificable asociada al canal L5.

        F_L5 =
            ρP_tC_Ω
            + 0.5ΔC_Ω
            − β(S/ln(6))
    """

    s_norm = normalized_entropy(S)

    return (
        float(rho)
        * float(P_t)
        * float(c_omega)
        + 0.5
        * float(delta_c)
        - BETA_F
        * s_norm
    )


def force_L6(
    w6: float,
    purpose_magnitude: float,
) -> float:
    """
    L6 aporta dirección mediante:

        F_L6 = w_6 · P

    L6 no introduce fricción propia.
    """

    return (
        float(w6)
        * float(purpose_magnitude)
    )


def force_BETA(
    novelty: float = 0.0,
    k: Optional[float] = None,
) -> float:
    """
    Fuerza asociada al margen β.

        F_β = β · A(N)

    con:

        A(N) = 1 − exp(−N/k)
    """

    if k is None or k <= 0.0:

        k = (
            float(S_REF)
            if float(S_REF) > 0.0
            else 1.0
        )

    novelty = max(
        0.0,
        float(novelty),
    )

    A = (
        1.0
        - math.exp(
            -novelty / k
        )
    )

    return BETA_F * A


def force_COH(
    c_omega: float,
    delta_c: float = 0.0,
) -> float:
    """
    Retroalimentación dinámica de coherencia.

        F_COH = C_Ω · ΔC_Ω
    """

    return (
        float(c_omega)
        * float(delta_c)
    )


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
    Cableado de la fuerza total del carril.

        F_Y =
            F_L0
            + F_L5
            + F_L6
            + F_β
            + F_COH
    """

    return (
        force_L0(
            L0_input,
            scale_L0,
        )
        + force_L5(
            c_omega,
            rho,
            P_t,
            S,
            delta_c,
        )
        + force_L6(
            weights[5],
            purpose_magnitude,
        )
        + force_BETA(
            novelty
        )
        + force_COH(
            c_omega,
            delta_c,
        )
    )


# ===============================================================
# 9. ESTADO FUNDAMENTAL DEL CABLEADO L4
# ===============================================================

@dataclass
class YoState:

    # ===========================================================
    # ÚNICOS GRADOS DE LIBERTAD INTEGRADOS POR EL CARRIL
    # ===========================================================

    theta: float = THETA_CUBE

    theta_dot: float = 0.0

    t: float = 0.0

    # ===========================================================
    # LECTURAS DERIVADAS DEL CIRCUITO
    # ===========================================================

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
        default_factory=lambda: [
            1.0 / INTERNAL_LAYERS
        ] * INTERNAL_LAYERS
    )

    energies: List[float] = field(
        default_factory=lambda: [
            0.0
        ] * INTERNAL_LAYERS
    )

    contributions: List[float] = field(
        default_factory=lambda: [
            0.0
        ] * INTERNAL_LAYERS
    )

    regime: str = "SUBAMORTIGUADO"


# ===============================================================
# 10. CABLEADO DE INTEGRACIÓN DEL CARRIL
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
    Ejecuta un ciclo completo del cableado dinámico de L4.

    Secuencia:

        L1..L6
          ↓
        E_i
          ↓
        w_i
          ↓
        f_i
          ↓
        S
          ↓
        C_Ω
          ↓
        φ_Y
        θ_eq
        F_Y
          ↓
        θ̈_Y
          ↓
        θ̇_Y
          ↓
        θ_Y
          ↓
        nuevo estado
    """

    if dt <= 0.0:

        raise ValueError(
            "dt debe ser > 0"
        )

    if frictions is None:
        frictions = _default_frictions()

    # ===========================================================
    # ETAPA 1 — ENERGÍAS
    # ===========================================================

    energies = compute_energies(
        activations,
        frictions,
    )

    # ===========================================================
    # ETAPA 2 — PESOS
    # ===========================================================

    weights = compute_weights(
        energies
    )

    # ===========================================================
    # ETAPA 3 — CONTRIBUCIONES
    # ===========================================================

    contributions = compute_contributions(
        weights,
        activations,
        energies,
        frictions,
    )

    # ===========================================================
    # ETAPA 4 — ENTROPÍA
    # ===========================================================

    S = shannon_S(
        weights
    )

    # ===========================================================
    # ETAPA 5 — COHERENCIA
    # ===========================================================

    c_omega = compute_c_omega(
        contributions,
        rho=rho,
        P_t=P_t,
        A=A,
        I_ext=I_ext,
    )

    delta_c = (
        c_omega
        - float(state.c_omega)
    )

    # ===========================================================
    # ETAPA 6 — AMORTIGUAMIENTO
    # ===========================================================

    phi = phi_Y(
        weights,
        frictions,
    )

    zeta = zeta_Y(
        phi
    )

    omega = omega_Y(
        phi
    )

    regime = regime_Y(
        phi
    )

    # ===========================================================
    # ETAPA 7 — EQUILIBRIO DINÁMICO
    # ===========================================================

    theta_eq = (
        float(theta_eq_override)
        if theta_eq_override is not None
        else dynamic_equilibrium(
            c_omega,
            weights,
        )
    )

    # ===========================================================
    # ETAPA 8 — FUERZA TOTAL
    # ===========================================================

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

    # ===========================================================
    # ETAPA 9 — ESTADO ACTUAL
    # ===========================================================

    theta = float(
        state.theta
    )

    theta_dot = float(
        state.theta_dot
    )

    # ===========================================================
    # ETAPA 10 — ECUACIÓN DINÁMICA
    # ===========================================================

    acceleration = (
        force
        - phi * theta_dot
        - PI2 * (
            theta
            - theta_eq
        )
    )

    # ===========================================================
    # ETAPA 11 — EULER SEMI-IMPLÍCITO
    # ===========================================================

    theta_dot_new = (
        theta_dot
        + acceleration
        * float(dt)
    )

    theta_new = (
        theta
        + theta_dot_new
        * float(dt)
    )

    # ===========================================================
    # ETAPA 12 — NUEVO ESTADO DEL CABLEADO L4
    # ===========================================================

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
# 11. SOLUCIÓN ANALÍTICA DEL OSCILADOR
# ===============================================================

def oscillator_solution_Y(
    t: float,
    amplitude: float,
    delta: float,
    phi_y: float,
    theta_eq: Optional[float] = None,
) -> float:
    """
    Solución del oscilador para régimen constante.

    Condición:

        F_Y ≈ 0

    con:

        φ_Y = constante
        θ_eq = constante

    Entonces:

        θ_Y(t) =
            θ_eq
            + A exp(−φ_Y t/2)
            · cos(ω_Y t + δ)
    """

    theta_eq = (
        float(THETA_CUBE)
        if theta_eq is None
        else float(theta_eq)
    )

    omega = omega_Y(
        phi_y
    )

    decay = math.exp(
        -float(phi_y)
        * float(t)
        / 2.0
    )

    return (
        theta_eq
        + float(amplitude)
        * decay
        * math.cos(
            omega * float(t)
            + float(delta)
        )
    )


# ===============================================================
# 12. LECTURA DEL CARRIL L4
# ===============================================================

def read_rail(
    state: YoState,
) -> dict:
    """
    Devuelve la lectura actual del cableado L4.

    La lectura representa el estado dinámico del carril:
        θ_Y
        θ̇_Y
        t
        θ_eq
        φ_Y
        ζ_Y
        ω_Y
        F_Y
        C_Ω
        S
        w_i
        E_i
        f_i

    No existe aquí un mapeo del Yo a estaciones L1...L6.
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
        "contributions_f1_f6": list(
            state.contributions
        ),
        "ALPHA": ALPHA_F,
        "BETA": BETA_F,
        "THETA_CUBE": float(
            THETA_CUBE
        ),
        "L0_ROLE": "INPUT_EXTERNAL",
    }


# ===============================================================
# 13. API DEL CABLEADO L4 — YoOscillator
# ===============================================================

class YoOscillator:
    """
    L4 — Yo Oscilatorio Dinámico.

    Esta clase constituye la interfaz del cableado dinámico.

    Integra únicamente:

        θ_Y
        θ̇_Y
        t

    Las magnitudes restantes son lecturas derivadas del circuito.

    L1..L6 alimentan el cálculo energético.

    L0 actúa como forzamiento externo.

    L6 puede aportar dirección.

    El Yo permanece como un grado de libertad continuo.
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
            theta_dot=float(
                theta_dot0
            ),
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
        """
        Ejecuta un ciclo del cableado dinámico de L4.
        """

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

        return read_rail(
            self.state
        )

    def snapshot(self) -> dict:
        """
        Devuelve el estado actual del cableado L4.
        """

        return read_rail(
            self.state
        )


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
