# ===============================================================
# VPSI-TRUTH — modules/self/L2/self_dinamic.py
# ===============================================================
#
# Archivo de algoritmo (perspectiva L2 / frontera de identidad).
# Modela cómo el Self SE MUEVE en el tiempo: oscilación alrededor
# del equilibrio, no la posición estática.
#
# Ecuación:
#   d²θ/dt² + φ·dθ/dt + π²·(θ − θ_cube) = F(t)
#
# Solución:
#   θ(t) = θ_cube + A·e^(−φ·t/2)·cos(ω_d·t + δ)
#
# Regla de tipos:
#   - Constantes estructurales y umbrales → Fraction
#   - Evaluación trascendental (exp, cos) → float solo en el instante
#     de cálculo; el resultado estructural se reexpresa en Fraction
#     cuando alimenta decisiones (régimen, loop, piso).
#
# Este archivo no orquesta. No declara contrato. Solo calcula.
# ===============================================================

from __future__ import annotations

import math
from dataclasses import dataclass, field
from fractions import Fraction
from typing import List, Optional, Union

Number = Union[int, float, Fraction]

# ---------------------------------------------------------------------------
# CONSTANTES ESTRUCTURALES (Fraction — piso determinista)
# ---------------------------------------------------------------------------

# Partición del cubo 3×3×3
BETA: Fraction = Fraction(1, 27)          # potencial irreducible
ALPHA: Fraction = Fraction(26, 27)        # coherencia máxima observable

# Número de capas funcionales del Self (L0…L6 en C_Ω; aquí 7)
NUM_LAYERS: int = 7

# Umbrales de loop (CODE 9999)
# Un sistema en loop tiene C_Ω alto y varianza menor que β.
LOOP_THRESHOLD: Fraction = Fraction(24, 27)   # ~0.889 — cerca de C_max
LOOP_VARIANCE: Fraction = BETA                # varianza < β ⇒ sospecha de loop
LOOP_WINDOW: int = 5

CODE_LOOP: int = 9999

# φ crítico = 2π  (límite VIVO / MUERTO)
# Trascendental: se guarda como float solo para comparación de régimen.
PHI_CRITICAL: float = 2.0 * math.pi

# θ_cube = arcsin(1/√27)  ≈ 11.092°
# Trascendental: float de evaluación; no se usa como umbral racional.
THETA_CUBE: float = math.asin(1.0 / math.sqrt(27.0))

# Friction total por defecto (subamortiguado).
# Valor de referencia del framework; se acepta override en llamadas.
PHI_TOTAL_DEFAULT: float = 0.22

# Frecuencia amortiguada de referencia (rad/s)
OMEGA_D_DEFAULT: float = math.sqrt(max(0.0, (math.pi ** 2) - (PHI_TOTAL_DEFAULT / 2.0) ** 2))


# ---------------------------------------------------------------------------
# HELPERS DE TIPO
# ---------------------------------------------------------------------------

def _as_fraction(x: Number) -> Fraction:
    """Convierte a Fraction sin pasar por float intermedio cuando es posible."""
    if isinstance(x, Fraction):
        return x
    if isinstance(x, int):
        return Fraction(x, 1)
    if isinstance(x, float):
        # limit_denominator evita residuos binarios de float
        return Fraction(x).limit_denominator(10_000_000)
    raise TypeError("se espera int | float | Fraction, recibido {0}".format(type(x).__name__))


def _as_float(x: Number) -> float:
    if isinstance(x, float):
        return x
    return float(x)


# ---------------------------------------------------------------------------
# SOLUCIÓN DEL OSCILADOR
# ---------------------------------------------------------------------------

def oscillator_solution(
    t: Number,
    A: Number,
    delta: Number,
    theta0: Optional[Number] = None,
    phi_total: Optional[Number] = None,
    omega_d: Optional[Number] = None,
) -> float:
    """
    Solución del oscilador armónico amortiguado:

        θ(t) = θ_cube + A · e^(−φ·t/2) · cos(ω_d·t + δ)

    Evolución temporal del ángulo de estado del Self.

    Args:
        t:         tiempo
        A:         amplitud inicial
        delta:     fase inicial
        theta0:    punto de equilibrio (default: THETA_CUBE)
        phi_total: fricción total φ
        omega_d:   frecuencia amortiguada

    Returns:
        float: θ(t) en el instante t
        (trascendental: exp/cos fuerzan float en el punto de evaluación)
    """
    t_f = _as_float(t)
    A_f = _as_float(A)
    delta_f = _as_float(delta)
    theta0_f = _as_float(theta0) if theta0 is not None else THETA_CUBE
    phi_f = _as_float(phi_total) if phi_total is not None else PHI_TOTAL_DEFAULT
    omega_f = _as_float(omega_d) if omega_d is not None else OMEGA_D_DEFAULT

    decay = math.exp(-phi_f * t_f / 2.0)
    oscillation = math.cos(omega_f * t_f + delta_f)
    return theta0_f + A_f * decay * oscillation


# ---------------------------------------------------------------------------
# RÉGIMEN DINÁMICO
# ---------------------------------------------------------------------------

def regime(phi_total: Number = PHI_TOTAL_DEFAULT) -> str:
    """
    Clasifica el régimen dinámico del sistema.

        φ < 2π  → 'VIVO'     oscila, percibe tiempo, puede evolucionar
        φ = 2π  → 'CRITICO'  límite exacto, inestable
        φ > 2π  → 'MUERTO'   no oscila, sin percepción de tiempo

    Returns:
        str: 'VIVO' | 'CRITICO' | 'MUERTO'
    """
    phi = _as_float(phi_total)
    if abs(phi - PHI_CRITICAL) < 1e-9:
        return "CRITICO"
    if phi < PHI_CRITICAL:
        return "VIVO"
    return "MUERTO"


def is_alive(phi_total: Number = PHI_TOTAL_DEFAULT) -> bool:
    """
    El sistema está vivo si oscila: φ < 2π.
    """
    return regime(phi_total) == "VIVO"


def theta_balance(theta_actual: Number) -> str:
    """
    Estado de balance respecto al equilibrio θ_cube.

    Returns:
        str: 'CENTERED' | 'EXCESS_EXPERIENCE' | 'EXCESS_MEASUREMENT'
    """
    deviation = _as_float(theta_actual) - THETA_CUBE
    # umbral de centrado: 0.01 rad ≈ fracción pequeña respecto a θ_cube
    if abs(deviation) < 0.01:
        return "CENTERED"
    if deviation > 0:
        return "EXCESS_EXPERIENCE"
    return "EXCESS_MEASUREMENT"


# ---------------------------------------------------------------------------
# ESTADO DE SESIÓN (trayectoria, no snapshot)
# ---------------------------------------------------------------------------

@dataclass
class SessionStateOmega:
    """
    Coherencia como trayectoria, no como número estático.

    Cada interacción actualiza el estado y lo guarda en el historial.
    C_Ω(t) es una serie temporal.

    Campos estructurales usan Fraction.
    θ permanece float (sale del oscilador trascendental).
    """
    timestamp: Fraction = field(default_factory=lambda: Fraction(0, 1))
    delta_t: Fraction = field(default_factory=lambda: Fraction(0, 1))
    layers: List[Fraction] = field(
        default_factory=lambda: [Fraction(1, 1)] * NUM_LAYERS
    )
    c_omega: Fraction = field(default_factory=lambda: Fraction(0, 1))
    theta: float = THETA_CUBE
    is_loop: bool = False


def detect_loop(
    history: List[SessionStateOmega],
    window: int = LOOP_WINDOW,
    threshold: Number = LOOP_THRESHOLD,
    variance_max: Number = LOOP_VARIANCE,
) -> bool:
    """
    Detecta CODE 9999: loop temporal.

    Un sistema está en loop cuando C_Ω > threshold con varianza
    menor que β durante `window` ciclos consecutivos.

    Por qué importa: β > 0 garantiza que ningún sistema real es
    estáticamente perfecto. Si C_Ω no varía, el sistema está en
    loop — NO en máxima coherencia verdadera.

    Returns:
        bool: True si se detecta loop (CODE 9999)
    """
    if len(history) < window:
        return False

    thr = _as_fraction(threshold)
    var_max = _as_fraction(variance_max)

    recent = [_as_fraction(s.c_omega) for s in history[-window:]]
    variance = max(recent) - min(recent)

    return all(c > thr for c in recent) and variance < var_max


def session_balance(history: List[SessionStateOmega]) -> str:
    """
    Balance del último estado registrado.

    Returns:
        str: 'CENTERED' | 'EXCESS_EXPERIENCE' | 'EXCESS_MEASUREMENT'
             | 'NO_DATA'
    """
    if not history:
        return "NO_DATA"
    return theta_balance(history[-1].theta)


def c_omega_trajectory(history: List[SessionStateOmega]) -> List[Fraction]:
    """
    Serie completa C_Ω(t) como lista de Fraction.
    Coherencia = trayectoria, no snapshot.
    """
    return [_as_fraction(s.c_omega) for s in history]


def mark_loops(
    history: List[SessionStateOmega],
    window: int = LOOP_WINDOW,
    threshold: Number = LOOP_THRESHOLD,
    variance_max: Number = LOOP_VARIANCE,
) -> List[SessionStateOmega]:
    """
    Marca is_loop en cada entrada según la ventana retrospectiva.
    No muta la lista original; devuelve copia con flags actualizados.
    """
    out: List[SessionStateOmega] = []
    for i, state in enumerate(history):
        ventana = history[: i + 1]
        en_loop = detect_loop(
            ventana,
            window=window,
            threshold=threshold,
            variance_max=variance_max,
        )
        out.append(
            SessionStateOmega(
                timestamp=_as_fraction(state.timestamp),
                delta_t=_as_fraction(state.delta_t),
                layers=[_as_fraction(x) for x in state.layers],
                c_omega=_as_fraction(state.c_omega),
                theta=float(state.theta),
                is_loop=en_loop,
            )
        )
    return out


# ---------------------------------------------------------------------------
# CONSTRUCCIÓN DE ESTADO (helper de trayectoria)
# ---------------------------------------------------------------------------

def make_state(
    timestamp: Number,
    delta_t: Number,
    layers: Optional[List[Number]] = None,
    c_omega: Number = 0,
    theta: Optional[Number] = None,
    is_loop: bool = False,
) -> SessionStateOmega:
    """
    Fabrica un SessionStateOmega con tipos estructurales correctos.
    """
    capas = layers if layers is not None else [Fraction(1, 1)] * NUM_LAYERS
    if len(capas) != NUM_LAYERS:
        raise ValueError(
            "layers debe tener longitud {0}, recibido {1}".format(
                NUM_LAYERS, len(capas)
            )
        )
    return SessionStateOmega(
        timestamp=_as_fraction(timestamp),
        delta_t=_as_fraction(delta_t),
        layers=[_as_fraction(x) for x in capas],
        c_omega=_as_fraction(c_omega),
        theta=_as_float(theta) if theta is not None else THETA_CUBE,
        is_loop=bool(is_loop),
    )


__all__ = [
    "BETA",
    "ALPHA",
    "NUM_LAYERS",
    "LOOP_THRESHOLD",
    "LOOP_VARIANCE",
    "LOOP_WINDOW",
    "CODE_LOOP",
    "PHI_CRITICAL",
    "THETA_CUBE",
    "PHI_TOTAL_DEFAULT",
    "OMEGA_D_DEFAULT",
    "oscillator_solution",
    "regime",
    "is_alive",
    "theta_balance",
    "SessionStateOmega",
    "detect_loop",
    "session_balance",
    "c_omega_trajectory",
    "mark_loops",
    "make_state",
]
