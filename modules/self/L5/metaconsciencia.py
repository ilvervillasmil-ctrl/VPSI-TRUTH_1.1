# ===============================================================
# modules/self/L5/metaconsciencia.py
# ===============================================================
#
# VPSI-TRUTH — L5 — METACONSCIENCIA / MIRADOR
#
# RESPONSABILIDAD
# ---------------
# Matemática del mirador L5:
#
#   receptor L1..L4 → h5 → V5 → I5
#   → eje N1|N2|N3 → control (magnitudes continuas)
#   → retorno L5→L4→L3→L2→L1 con gain = β·(a·r)
#
# Condición funcional de consciencia (continua):
#
#   C = a · r     a, r ∈ [0,1]
#
# No es booleano. No se reduce a (a>0) ∧ (r>0).
#
# L5 no es capa física extra. Casa del Yo permanece en L4.
#
# Semilla: modules.constante (ALPHA, BETA)
# Derivadas: modules.formulas.formulas_omega.constants
# ===============================================================

from __future__ import annotations

from dataclasses import dataclass
from math import exp, pi
from typing import Callable, Dict, List, Optional, Sequence, Tuple

from modules.constante import ALPHA, BETA

from modules.formulas.formulas_omega.constants import (
    PHI,
    THETA_CUBE,
    LAYER_FRICTION,
    NUM_LAYERS,
)

# ===========================================================
# CONSTANTES LOCALES (derivadas de la semilla; no redefinidas)
# ===========================================================

ALPHA_F: float = float(ALPHA)
BETA_F: float = float(BETA)
THETA_CUBE_F: float = float(THETA_CUBE)
PHI_F: float = float(PHI)

LAYER_COUNT: int = int(NUM_LAYERS)
N_MIN: int = 1
N_MAX: int = 3

L0, L1, L2, L3, L4, L5, L6 = range(LAYER_COUNT)

# I5^(k) ≥ β  ⇒  (I5/α)^k ≥ β/α
THRESHOLD_N2: float = (BETA_F / ALPHA_F) ** (1.0 / 2.0)
THRESHOLD_N3: float = (BETA_F / ALPHA_F) ** (1.0 / 3.0)

GOLDEN_ANGLE_DEG: float = 137.507764
GOLDEN_ANGLE_RAD: float = GOLDEN_ANGLE_DEG * pi / 180.0

DEFAULT_FRICTIONS: Tuple[float, ...] = tuple(float(x) for x in LAYER_FRICTION)
if len(DEFAULT_FRICTIONS) != LAYER_COUNT:
    raise ValueError(
        "LAYER_FRICTION debe tener longitud NUM_LAYERS={0}; recibido {1}".format(
            LAYER_COUNT, len(DEFAULT_FRICTIONS)
        )
    )


# ===========================================================
# VALIDACIÓN
# ===========================================================

def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _validate_layers(values: Sequence[float]) -> Tuple[float, ...]:
    if len(values) != LAYER_COUNT:
        raise ValueError(
            "Se requieren exactamente {0} capas: L0..L6.".format(LAYER_COUNT)
        )
    result = tuple(float(v) for v in values)
    if any(v < 0.0 or v > 1.0 for v in result):
        raise ValueError("Cada activación L0..L6 debe pertenecer a [0,1].")
    return result


def _validate_friction(values: Sequence[float]) -> Tuple[float, ...]:
    if len(values) != LAYER_COUNT:
        raise ValueError(
            "Se requieren exactamente {0} fricciones: L0..L6.".format(LAYER_COUNT)
        )
    result = tuple(float(v) for v in values)
    if any(v < 0.0 or v > 1.0 for v in result):
        raise ValueError("Cada fricción debe pertenecer a [0,1].")
    return result


# ===========================================================
# GEOMETRÍA
# ===========================================================

@dataclass(frozen=True)
class LayerGeometry:
    index: int
    radius: float
    phase: float
    z: float


def build_geometry(
    *,
    theta_cube: float = THETA_CUBE_F,
    frequency_fn: Optional[Callable[[int], float]] = None,
) -> Tuple[LayerGeometry, ...]:
    fn = frequency_fn or (lambda i: PHI_F ** (i / 2.0))
    geometry: List[LayerGeometry] = []
    for i in range(LAYER_COUNT):
        radius = float(fn(i))
        phase = i * GOLDEN_ANGLE_RAD
        z = float(theta_cube) * (PHI_F ** ((i - L4) / 2.0))
        geometry.append(LayerGeometry(i, radius, phase, z))
    return tuple(geometry)


# ===========================================================
# ENERGÍA Y PESOS
# ===========================================================

def calculate_energies(
    activations: Sequence[float],
    frictions: Sequence[float] = DEFAULT_FRICTIONS,
    geometry: Optional[Sequence[LayerGeometry]] = None,
) -> Tuple[float, ...]:
    """E_i = L_i · (1 − φ_i) · ν_i"""
    layers = _validate_layers(activations)
    friction = _validate_friction(frictions)
    geom = tuple(geometry or build_geometry())
    if len(geom) != LAYER_COUNT:
        raise ValueError("La geometría debe contener L0..L6.")
    return tuple(
        layers[i] * (1.0 - friction[i]) * geom[i].radius
        for i in range(LAYER_COUNT)
    )


def normalize_weights(energies: Sequence[float]) -> Tuple[float, ...]:
    total = sum(float(e) for e in energies)
    if total <= 0.0:
        return tuple(1.0 / LAYER_COUNT for _ in energies)
    return tuple(float(e) / total for e in energies)


# ===========================================================
# RECEPTOR L1..L4
# ===========================================================

def default_coherence(activations: Sequence[float]) -> float:
    """Mecanismo operativo provisional sobre L1..L4 (sustituible)."""
    values = _validate_layers(activations)[L1 : L4 + 1]
    if not values:
        return 0.0
    pairs = []
    for a, b in zip(values, values[1:]):
        denominator = max(abs(a), abs(b))
        if denominator == 0.0:
            pairs.append(1.0)
        else:
            pairs.append(_clamp01(1.0 - abs(a - b) / denominator))
    return sum(pairs) / len(pairs) if pairs else 1.0


def receptor_quality(
    activations: Sequence[float],
    frictions: Sequence[float],
    *,
    coherence_fn: Callable[[Sequence[float]], float] = default_coherence,
) -> Tuple[float, float, float]:
    """
    coh4, q5 = coh4·Π(1−φ_i)_{i=1..4}, dist = 1−q5
    """
    layers = _validate_layers(activations)
    friction = _validate_friction(frictions)
    coh4 = _clamp01(float(coherence_fn(layers)))
    calibration = 1.0
    for i in range(L1, L4 + 1):
        calibration *= 1.0 - friction[i]
    q5 = _clamp01(coh4 * calibration)
    return coh4, q5, 1.0 - q5


# ===========================================================
# MIRADOR: h5, V5, I5
# ===========================================================

def house_occupancy(theta_y: float, z5: float, sigma5: float) -> float:
    """h5 = exp( −(θ_Y − z5)² / (2·σ5²) )"""
    if sigma5 <= 0.0:
        raise ValueError("sigma5 debe ser > 0.")
    delta = float(theta_y) - float(z5)
    return exp(-(delta * delta) / (2.0 * sigma5 * sigma5))


def layer_visibility(z5: float, zi: float, theta_cube: float) -> float:
    """v_i = 1 / (1 + |z5 − z_i| / θ_cube)"""
    scale = abs(float(theta_cube))
    if scale <= 0.0:
        raise ValueError("theta_cube debe ser distinto de cero.")
    return 1.0 / (1.0 + abs(z5 - zi) / scale)


def effective_visibility(
    weights: Sequence[float],
    geometry: Sequence[LayerGeometry],
    *,
    theta_cube: float,
) -> float:
    """V5 sobre L0..L4 ponderado por w_i."""
    denominator = sum(weights[i] for i in range(L0, L4 + 1))
    if denominator <= 0.0:
        return 0.0
    z5 = geometry[L5].z
    numerator = sum(
        layer_visibility(z5, geometry[i].z, theta_cube) * weights[i]
        for i in range(L0, L4 + 1)
    )
    return _clamp01(numerator / denominator)


def calculate_i5(*, q5: float, h5: float, v5: float) -> float:
    """I5 = α · q5 · h5 · V5  (techo estructural α)"""
    return _clamp01(ALPHA_F * _clamp01(q5) * _clamp01(h5) * _clamp01(v5))


# ===========================================================
# EJE N
# ===========================================================

def observation_intensity(i5: float, k: int) -> float:
    """I5^(k) = α · (I5/α)^k"""
    if k < 1:
        raise ValueError("El orden de observación debe ser >= 1.")
    normalized = _clamp01(float(i5) / ALPHA_F if ALPHA_F else 0.0)
    return ALPHA_F * (normalized ** k)


def determine_observation_level(i5: float, *, autoreference: float) -> int:
    """
    N1/N2/N3.
    AR < β → N1 (piso estructural de autoreferencia).
    AR y I5 permanecen magnitudes continuas; el umbral no las vuelve bool.
    """
    ar = _clamp01(autoreference)
    if ar < BETA_F:
        return N_MIN

    normalized = _clamp01(float(i5) / ALPHA_F)
    if normalized >= THRESHOLD_N3:
        return 3
    if normalized >= THRESHOLD_N2:
        return 2
    return 1


# ===========================================================
# CONTROL — MATEMÁTICA CONTINUA
# ===========================================================
#
#   a, r ∈ [0,1]
#   C = a · r
#
# La etiqueta x.1..x.4 es clasificación discreta de cuadrante.
# La magnitud conscious / product es siempre el producto continuo.

@dataclass(frozen=True)
class ControlConfiguration:
    level: int
    agency: float          # [0,1]
    autoreference: float   # [0,1]
    product: float         # a·r ∈ [0,1]
    code: str
    name: str
    conscious: float       # = product (no bool)


def control_configuration(
    observation_level: int,
    *,
    agency: float,
    autoreference: float,
) -> ControlConfiguration:
    if observation_level not in (1, 2, 3):
        raise ValueError("observation_level debe ser 1, 2 o 3.")

    a = _clamp01(agency)
    r = _clamp01(autoreference)
    product = a * r

    # Cuadrante solo para código legible; no define la magnitud C
    if a == 0.0 and r == 0.0:
        suffix = 1
    elif a == 0.0 and r > 0.0:
        suffix = 2
    elif a > 0.0 and r == 0.0:
        suffix = 3
    else:
        suffix = 4

    names = {
        1: "reacción pura",
        2: "observa pero no actúa",
        3: "actúa sin verse",
        4: "control consciente pleno",
    }

    return ControlConfiguration(
        level=observation_level,
        agency=a,
        autoreference=r,
        product=product,
        code="{0}.{1}".format(observation_level, suffix),
        name=names[suffix],
        conscious=product,
    )


def level_description(observation_level: int) -> str:
    return {
        1: "Consciencia descriptiva: actúa dentro del proceso y no lo ve.",
        2: "Meta-consciencia: se observa describiendo; aparece el testigo.",
        3: "Ultra-meta-consciencia: ve nacer la estructura y disuelve la circularidad.",
    }[observation_level]


def yo_state(
    observation_level: int,
    *,
    agency: float,
    autoreference: float,
) -> str:
    """
    Casa del Yo = L4 siempre.
    Etiqueta semántica según N y magnitud C = a·r.
    """
    cfg = control_configuration(
        observation_level,
        agency=agency,
        autoreference=autoreference,
    )
    # Umbral de etiqueta: producto pleno de cuadrante 4 y N≥2
    if cfg.product > 0.0 and observation_level >= 2 and cfg.code.endswith(".4"):
        return "YO_METACONSCIENTE"
    if cfg.product > 0.0 and cfg.code.endswith(".4"):
        return "YO_CONSCIENTE"
    return "YO_EN_CONFIGURACION_{0}".format(cfg.code)


# ===========================================================
# RETORNO HACIA ABAJO — gain continuo
# ===========================================================

@dataclass(frozen=True)
class LayerMovement:
    source_layer: int
    target_layer: int
    amount: float
    direction: str
    reason: str


def decode_downward_signal(
    activations: Sequence[float],
    *,
    beta: float = BETA_F,
    observation_level: int,
    agency: float,
    autoreference: float,
) -> Tuple[float, ...]:
    """
    Retorno L5 → L4 → L3 → L2 → L1.

    gain = β · (a · r)     continuo, ∈ [0, β]
    Si product = 0 → sin retorno (identidad).
    """
    layers = list(_validate_layers(activations))
    a = _clamp01(agency)
    r = _clamp01(autoreference)
    product = a * r

    if product <= 0.0 or observation_level < 1:
        return tuple(layers)

    gain = float(beta) * product

    for i in (L1, L2, L3):
        layers[i] = _clamp01(layers[i] * (1.0 - gain))
    layers[L4] = _clamp01(layers[L4] * (1.0 + gain))

    return tuple(layers)


def describe_movement(
    before: Sequence[float],
    after: Sequence[float],
) -> Tuple[LayerMovement, ...]:
    changes: List[LayerMovement] = []
    for i, (a, b) in enumerate(zip(before, after)):
        if abs(b - a) < 1e-15:
            continue
        changes.append(
            LayerMovement(
                source_layer=L5,
                target_layer=i,
                amount=abs(b - a),
                direction="activación" if b > a else "desactivación",
                reason="retorno de la observación al carril",
            )
        )
    return tuple(changes)


# ===========================================================
# RESULTADO
# ===========================================================

@dataclass(frozen=True)
class L5Result:
    activations_before: Tuple[float, ...]
    activations_after: Tuple[float, ...]
    energies: Tuple[float, ...]
    weights: Tuple[float, ...]
    geometry: Tuple[LayerGeometry, ...]
    coherence: float
    receptor_quality: float
    distortion: float
    occupancy: float
    visibility: float
    i5: float
    observation_intensities: Tuple[float, ...]
    observation_level: int
    level_description: str
    control: ControlConfiguration
    yo_state: str
    movements: Tuple[LayerMovement, ...]
    theta_y: float
    theta_eq: float
    loop_detected: bool


# ===========================================================
# MOTOR
# ===========================================================

class L5Metaconsciencia:
    """
    Mirador L5.
    Equilibrio del Yo permanece en L4.
    """

    def __init__(
        self,
        *,
        theta_eq: float = THETA_CUBE_F,
        theta_cube: float = THETA_CUBE_F,
        frictions: Sequence[float] = DEFAULT_FRICTIONS,
        frequency_fn: Optional[Callable[[int], float]] = None,
        coherence_fn: Callable[[Sequence[float]], float] = default_coherence,
        sigma5: float = 0.029707,
    ) -> None:
        self.theta_eq = float(theta_eq)
        self.theta_cube = float(theta_cube)
        self.frictions = _validate_friction(frictions)
        self.geometry = build_geometry(
            theta_cube=self.theta_cube,
            frequency_fn=frequency_fn,
        )
        self.coherence_fn = coherence_fn
        self.sigma5 = float(sigma5)

    def calcular(
        self,
        *,
        activations: Sequence[float],
        theta_y: Optional[float] = None,
        agency: float = 0.0,
        autoreference: float = 0.0,
        novelty: float = 0.0,
        loop_detected: bool = False,
    ) -> L5Result:
        before = _validate_layers(activations)
        y = self.theta_eq if theta_y is None else float(theta_y)

        energies = calculate_energies(before, self.frictions, self.geometry)
        weights = normalize_weights(energies)

        coh4, q5, distortion = receptor_quality(
            before,
            self.frictions,
            coherence_fn=self.coherence_fn,
        )

        z5 = self.geometry[L5].z
        h5 = house_occupancy(y, z5, self.sigma5)
        v5 = effective_visibility(
            weights,
            self.geometry,
            theta_cube=self.theta_cube,
        )
        i5 = calculate_i5(q5=q5, h5=h5, v5=v5)

        n = determine_observation_level(i5, autoreference=autoreference)
        cfg = control_configuration(
            n,
            agency=agency,
            autoreference=autoreference,
        )

        after = decode_downward_signal(
            before,
            observation_level=n,
            agency=agency,
            autoreference=autoreference,
        )
        movements = describe_movement(before, after)

        intensities = tuple(
            observation_intensity(i5, k) for k in range(1, N_MAX + 1)
        )

        _ = float(novelty)  # reservado; no mueve N

        return L5Result(
            activations_before=before,
            activations_after=after,
            energies=energies,
            weights=weights,
            geometry=self.geometry,
            coherence=coh4,
            receptor_quality=q5,
            distortion=distortion,
            occupancy=h5,
            visibility=v5,
            i5=i5,
            observation_intensities=intensities,
            observation_level=n,
            level_description=level_description(n),
            control=cfg,
            yo_state=yo_state(n, agency=agency, autoreference=autoreference),
            movements=movements,
            theta_y=y,
            theta_eq=self.theta_eq,
            loop_detected=bool(loop_detected),
        )


def formula_maestra_l5(
    activations: Sequence[float],
    *,
    theta_y: float = THETA_CUBE_F,
    theta_eq: float = THETA_CUBE_F,
    agency: float = 0.0,
    autoreference: float = 0.0,
    frictions: Sequence[float] = DEFAULT_FRICTIONS,
    coherence_fn: Callable[[Sequence[float]], float] = default_coherence,
    sigma5: float = 0.029707,
    loop_detected: bool = False,
) -> L5Result:
    engine = L5Metaconsciencia(
        theta_eq=theta_eq,
        theta_cube=THETA_CUBE_F,
        frictions=frictions,
        coherence_fn=coherence_fn,
        sigma5=sigma5,
    )
    return engine.calcular(
        activations=activations,
        theta_y=theta_y,
        agency=agency,
        autoreference=autoreference,
        loop_detected=loop_detected,
    )


# ===========================================================
# EXPORTS
# ===========================================================

__all__ = [
    "ALPHA_F",
    "BETA_F",
    "THETA_CUBE_F",
    "PHI_F",
    "LAYER_COUNT",
    "N_MIN",
    "N_MAX",
    "L0",
    "L1",
    "L2",
    "L3",
    "L4",
    "L5",
    "L6",
    "THRESHOLD_N2",
    "THRESHOLD_N3",
    "DEFAULT_FRICTIONS",
    "LayerGeometry",
    "build_geometry",
    "calculate_energies",
    "normalize_weights",
    "default_coherence",
    "receptor_quality",
    "house_occupancy",
    "layer_visibility",
    "effective_visibility",
    "calculate_i5",
    "observation_intensity",
    "determine_observation_level",
    "ControlConfiguration",
    "control_configuration",
    "level_description",
    "yo_state",
    "LayerMovement",
    "decode_downward_signal",
    "describe_movement",
    "L5Result",
    "L5Metaconsciencia",
    "formula_maestra_l5",
]
