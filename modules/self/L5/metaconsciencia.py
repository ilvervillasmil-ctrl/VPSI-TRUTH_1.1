# ===============================================================
# modules/self/L5/metaconsciencia.py
# ===============================================================
#
# VPSI-TRUTH — L5 — METACONSCIENCIA / MIRADOR
#
# RESPONSABILIDAD
# ---------------
# Implementar exclusivamente la matemática del mirador L5:
#
#   receptor L1..L4 → ocupación h5 → visibilidad V5 → señal I5
#   → eje de observación N1|N2|N3 → configuración x.1..x.4
#   → retorno opcional L5 → L4 → L3 → L2 → L1
#
# L5 no es una octava capa física del carril.
# L5 es el mirador que observa el carril L0..L6.
# La casa del Yo permanece en L4 en todos los casos.
#
# ===============================================================
# SEPARACIÓN ESTRUCTURAL
# ===============================================================
#
# L0..L6
#   Capas funcionales del sistema (carril de siete posiciones).
#   L0 entrada/caos, L1 cuerpo, L2 ego, L3 mente,
#   L4 Yo (casa), L5 consciencia (mirador), L6 alma/propósito.
#
# L4
#   Casa del Yo. θ_Y vive en L4.
#   Este módulo NO mueve la casa del Yo a L5.
#
# L5
#   Mirador / campo de observación.
#   No se crea ni “crece” la consciencia: está presente;
#   lo que cambia es el nivel de observación N y el control.
#
# N1..N3
#   Eje de observación DENTRO de L5 (no son capas nuevas):
#     N1  consciencia descriptiva
#     N2  metaconsciencia (aparece el testigo)
#     N3  ultra-metaconsciencia (se observa nacer la estructura)
#
# Configuraciones de control (dentro de cada N):
#     x.1  sin agencia + sin autoreferencia
#     x.2  sin agencia + con autoreferencia
#     x.3  con agencia + sin autoreferencia
#     x.4  con agencia + con autoreferencia
#
# Condición funcional de consciencia (dentro del nivel):
#     agencia × autoreferencia
#
# ===============================================================
# SEMILLA Y DERIVADAS (no se redefinen aquí)
# ===============================================================
#
#   α, β     ← modules.constante
#   Φ, θ_cube, LAYER_FRICTION, NUM_LAYERS, …
#            ← modules.formulas.formulas_omega.constants
#   E_i, ν_i ← LayerEnergy (formulas_omega.energy)
#
#   α = 26/27
#   β =  1/27
#   α + β = 1
#
# Umbrales del eje N (derivados de β/α, propios de L5):
#
#   THRESHOLD_N2 = (β/α)^(1/2)
#   THRESHOLD_N3 = (β/α)^(1/3)
#
# Origen:
#   I5^(k) = α · (I5/α)^k  ≥ β
#   ⇒ (I5/α)^k ≥ β/α = 1/26
#
# ===============================================================
# CADENA CAUSAL DEL MIRADOR
# ===============================================================
#
#   activaciones L0..L6
#           │
#           ├→ E_i = L_i·(1−φ_i)·ν_i
#           ├→ w_i = E_i / Σ E_j
#           │
#           ├→ receptor L1..L4
#           │     coh4 = coherencia(L1..L4)
#           │     calibration = Π_{i=1..4} (1−φ_i)
#           │     q5 = coh4 · calibration
#           │     dist = 1 − q5
#           │
#           ├→ h5 = ocupación del mirador
#           │     h5 = exp( −(θ_Y − z5)² / (2·σ5²) )
#           │
#           ├→ V5 = visibilidad efectiva sobre L0..L4
#           │     v_i = 1 / (1 + |z5−z_i|/θ_cube)
#           │     V5  = Σ_{i=0..4} v_i·w_i / Σ_{i=0..4} w_i
#           │
#           ├→ I5 = α · q5 · h5 · V5
#           │     (techo estructural α; no se busca I5 = 1)
#           │
#           ├→ N = nivel de observación
#           │     AR < β            → N1
#           │     I5/α ≥ THR_N3     → N3
#           │     I5/α ≥ THR_N2     → N2
#           │     si no             → N1
#           │
#           ├→ configuración x.1..x.4  (agencia, autoreferencia)
#           │
#           └→ retorno opcional (solo si conscious)
#                 L5 → L4 → L3 → L2 → L1
#                 gain = β · min(1, agencia·autoreferencia)
#                 L1..L3 se atenúan; L4 se refuerza
#
# ===============================================================
# FÓRMULAS
# ===============================================================
#
# Energía (carril completo L0..L6):
#
#   ν_i = Φ^(i/2)
#   E_i = L_i · (1 − φ_i) · ν_i
#   w_i = E_i / Σ_j E_j          (si Σ=0 → 1/7)
#
# Receptor:
#
#   q5 = coh4 · Π_{i=1}^{4} (1 − φ_i)
#   dist = 1 − q5
#
# Ocupación del mirador:
#
#   h5 = exp( −(θ_Y − z5)² / (2·σ5²) )     σ5 > 0
#
# Visibilidad de capa i desde L5:
#
#   v_i = 1 / (1 + |z5 − z_i| / θ_cube)
#
# Señal recibida:
#
#   I5 = α · q5 · h5 · V5
#
# Intensidad de observación de orden k:
#
#   I5^(k) = α · (I5/α)^k
#
# ===============================================================
# VARIABLES
# ===============================================================
#
# Entrada
#   activations[0..6]   L0..L6 ∈ [0,1]
#   frictions[0..6]     φ_i ∈ [0,1]
#   theta_y             posición del carril del Yo (L4) [rad]
#   theta_eq            equilibrio de referencia del Yo [rad]
#   agency              agencia ∈ [0,1]
#   autoreference       autoreferencia ∈ [0,1]
#   novelty             novedad (reservada; no mueve N)
#   loop_detected       bandera de loop del carril (lectura)
#   sigma5              ancho del mirador (> 0)
#
# Derivadas
#   E_i, w_i            energía y pesos del carril
#   coh4, q5, dist      calidad del receptor L1..L4
#   h5                  ocupación de L5
#   V5                  visibilidad efectiva
#   I5                  señal del mirador
#   N                   nivel de observación ∈ {1,2,3}
#   control             configuración x.1..x.4
#   yo_state            etiqueta semántica (casa sigue en L4)
#   activations_after   carril tras retorno (si conscious)
#   movements           trazas del retorno hacia abajo
#
# ===============================================================
# MECANISMOS PARAMETRIZABLES (no axiomas del capítulo)
# ===============================================================
#
#   coherence_fn   → puede ser LayerCoherence del repo
#   frequency_fn   → puede ser LayerEnergy.frequency / resonance
#   h5, v_i        → formas operativas; σ5 y θ_cube explícitos
#
# No se presentan como definiciones canónicas del libro.
# Son el motor de cálculo sustituible por capacidades contractuales.
#
# ===============================================================
# LO QUE ESTE ARCHIVO NO HACE
# ===============================================================
#
#   - no declara CONTENEDOR
#   - no habla con Engine
#   - no redefine α, β, Φ, θ_cube
#   - no convierte L5 en capa física adicional del DE de L4
#   - no mueve la casa del Yo de L4 a L5
#   - no calcula el carril oscilatorio θ̈_Y (eso es L4 FO)
#   - no calcula L7 / emergencia
#   - no implementa casas discretas del mapa θ_Y → estación
#   - no usa emotion / desire / fear como variables
#
# ===============================================================
# RELACIÓN CON L4 (YO OSCILATORIO)
# ===============================================================
#
#   L4 produce / expone:  θ_Y, θ̇_Y, θ_eq, φ_Y, C_Ω, …
#   L5 consume:           θ_Y (ocupación h5), activaciones, fricciones
#   L5 no integra el DE del carril; solo observa y, si conscious,
#   devuelve un vector de activaciones modulado hacia abajo.
#
# ===============================================================
# RELACIÓN CON formulas_omega.metaconsciousness
# ===============================================================
#
#   FO MetaconsciousnessCalculator:
#       MC = R_FIN · Π_{i=3..6} [L_i·(1−φ_i)]
#
#   Este L5:
#       mirador I5, eje N, configuraciones de control, retorno
#
#   Son operadores distintos. Pueden coexistir.
#   No sustituirse el uno al otro.
#
# ===============================================================

# Importante:
    # Las funciones de medición h5, v_i y coherencia son parametrizables.
    # No se presentan como axiomas del capítulo. Son mecanismos de cálculo
    # del modelo operativo y pueden sustituirse por las capacidades
    # contractuales del repositorio.

from __future__ import annotations

from dataclasses import dataclass
from math import exp, log, pi, sqrt
from typing import (
    Callable,
    Dict,
    List,
    Optional,
    Sequence,
    Tuple,
)

# ---------------------------------------------------------------
# ÚNICA FUENTE ESTRUCTURAL
# ---------------------------------------------------------------
from modules.constante import ALPHA, BETA

from modules.formulas.formulas_omega.constants import (
    PHI,
    THETA_CUBE,
    LAYER_FRICTION,
    NUM_LAYERS,
)
# ===========================================================
# 1. CONSTANTES ESTRUCTURALES
# ===========================================================

ALPHA: float = 26.0 / 27.0
BETA: float = 1.0 / 27.0
LAYER_COUNT: int = 7
N_MIN: int = 1
N_MAX: int = 3

L0, L1, L2, L3, L4, L5, L6 = range(7)

# El umbral se deriva de I5^(k) >= beta:
# (I5 / alpha)^k >= beta / alpha = 1/26.
THRESHOLD_N2: float = (BETA / ALPHA) ** (1.0 / 2.0)
THRESHOLD_N3: float = (BETA / ALPHA) ** (1.0 / 3.0)

# El ángulo no crea una capa nueva: solo pertenece a la geometría
# cuando el repositorio lo provea.
GOLDEN_ANGLE_DEG: float = 137.507764
GOLDEN_ANGLE_RAD: float = GOLDEN_ANGLE_DEG * pi / 180.0

# Valor de referencia del carril. Puede sustituirse por constants.py.
PHI: float = (1.0 + sqrt(5.0)) / 2.0
THETA_CUBE_DEFAULT: float = 0.19365830044432666

# Fricciones: por defecto no se inventan fricciones nuevas.
# El consumidor debe proporcionar las del carril real.
DEFAULT_FRICTIONS: Tuple[float, ...] = (0.0,) * LAYER_COUNT

# ===========================================================
# 2. VALIDACIÓN BÁSICA
# ===========================================================

def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))

def _validate_layers(values: Sequence[float]) -> Tuple[float, ...]:
    if len(values) != LAYER_COUNT:
        raise ValueError(f"Se requieren exactamente {LAYER_COUNT} capas: L0..L6.")
    result = tuple(float(v) for v in values)
    if any(v < 0.0 or v > 1.0 for v in result):
        raise ValueError("Cada activación L0..L6 debe pertenecer a [0,1].")
    return result

def _validate_friction(values: Sequence[float]) -> Tuple[float, ...]:
    if len(values) != LAYER_COUNT:
        raise ValueError(f"Se requieren exactamente {LAYER_COUNT} fricciones: L0..L6.")
    result = tuple(float(v) for v in values)
    if any(v < 0.0 or v > 1.0 for v in result):
        raise ValueError("Cada fricción debe pertenecer a [0,1].")
    return result

# ===========================================================
# 3. GEOMETRÍA DEL CARRIL
# ===========================================================

@dataclass(frozen=True)
class LayerGeometry:
    index: int
    radius: float
    phase: float
    z: float

def build_geometry(
    *,
    theta_cube: float = THETA_CUBE_DEFAULT,
    frequency_fn: Optional[Callable[[int], float]] = None,
) -> Tuple[LayerGeometry, ...]:
    """
    Construye la posición geométrica L0..L6.

    Si el repositorio dispone de resonance.calculate_layer_frequency,
    frequency_fn debe ser esa capacidad contractual. No se redefine
    aquí una segunda geometría cuando exista la capacidad real.
    """
    fn = frequency_fn or (lambda i: PHI ** (i / 2.0))
    geometry: List[LayerGeometry] = []

    for i in range(LAYER_COUNT):
        radius = float(fn(i))
        phase = i * GOLDEN_ANGLE_RAD
        z = theta_cube * (PHI ** ((i - L4) / 2.0))
        geometry.append(LayerGeometry(i, radius, phase, z))

    return tuple(geometry)

# ===========================================================
# 4. ENERGÍA Y PESOS DEL CARRIL
# ===========================================================

def calculate_energies(
    activations: Sequence[float],
    frictions: Sequence[float] = DEFAULT_FRICTIONS,
    geometry: Optional[Sequence[LayerGeometry]] = None,
) -> Tuple[float, ...]:
    """
    E_i = L_i (1 - phi_i) nu_i.

    Esta forma conserva el carril de siete capas. La geometría se usa
    para obtener nu_i/radio; no se elimina L0.
    """
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
# 5. COHERENCIA DEL RECEPTOR
# ===========================================================

def default_coherence(
    activations: Sequence[float],
) -> float:
    """
    Mecanismo operativo provisional.

    No se declara como definición canónica del capítulo. La función
    puede ser sustituida por layer_coherence.calculate_layer_coherence
    mediante coherence_fn.
    """
    values = _validate_layers(activations)[L1:L4 + 1]
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
    Arquitectura del receptor L1..L4.

    coh4 = coherencia del receptor.
    calibration = producto de (1 - phi_i) para L1..L4.
    q5 = coh4 * calibration.
    dist = 1 - q5.
    """
    layers = _validate_layers(activations)
    friction = _validate_friction(frictions)

    coh4 = _clamp01(float(coherence_fn(layers)))
    calibration = 1.0
    for i in range(L1, L4 + 1):
        calibration *= 1.0 - friction[i]

    q5 = _clamp01(coh4 * calibration)
    distortion = 1.0 - q5
    return coh4, q5, distortion

# ===========================================================
# 6. MIRADOR L5: OCUPACIÓN Y VISIBILIDAD
# ===========================================================

def house_occupancy(
    theta_y: float,
    z5: float,
    sigma5: float,
) -> float:
    """
    h5 = exp(-(theta_y-z5)^2 / (2 sigma5^2)).

    Hipótesis operativa: el capítulo habla de casa/mirador, pero no
    fija una gaussiana. Por eso sigma5 permanece explícito.
    """
    if sigma5 <= 0.0:
        raise ValueError("sigma5 debe ser > 0.")
    delta = float(theta_y) - float(z5)
    return exp(-(delta * delta) / (2.0 * sigma5 * sigma5))

def layer_visibility(
    z5: float,
    zi: float,
    theta_cube: float,
) -> float:
    """
    v_i = 1 / (1 + |z5-z_i| / theta_cube).

    Hipótesis operativa parametrizable.
    """
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
    """
    Campo de visión efectivo de L5 sobre las capas inferiores L0..L4.
    """
    denominator = sum(weights[i] for i in range(L0, L4 + 1))
    if denominator <= 0.0:
        return 0.0

    z5 = geometry[L5].z
    numerator = sum(
        layer_visibility(z5, geometry[i].z, theta_cube) * weights[i]
        for i in range(L0, L4 + 1)
    )
    return _clamp01(numerator / denominator)

# ===========================================================
# 7. SEÑAL RECIBIDA POR L5
# ===========================================================

def calculate_i5(
    *,
    q5: float,
    h5: float,
    v5: float,
) -> float:
    """
    I5 = alpha * q5 * h5 * V5.

    El techo estructural es alpha; la señal nunca necesita llegar a 1.
    """
    return _clamp01(ALPHA * _clamp01(q5) * _clamp01(h5) * _clamp01(v5))

# ===========================================================
# 8. OBSERVACIÓN RECURSIVA: EJE N
# ===========================================================

def observation_intensity(i5: float, k: int) -> float:
    """
    I5^(k) = alpha * (I5/alpha)^k.
    """
    if k < 1:
        raise ValueError("El orden de observación debe ser >= 1.")
    normalized = _clamp01(i5 / ALPHA if ALPHA else 0.0)
    return ALPHA * (normalized ** k)

def determine_observation_level(
    i5: float,
    *,
    autoreference: float,
) -> int:
    """
    N1/N2/N3.

    N1 es el piso del eje de observación.
    AR < beta => N1: sin autoreferencia mínima no existe el estado meta.
    """
    ar = _clamp01(autoreference)

    if ar < BETA:
        return N_MIN

    normalized = _clamp01(i5 / ALPHA)

    if normalized >= THRESHOLD_N3:
        return 3
    if normalized >= THRESHOLD_N2:
        return 2
    return 1

# ===========================================================
# 9. CONFIGURACIONES DE CONTROL
# ===========================================================

@dataclass(frozen=True)
class ControlConfiguration:
    level: int
    agency: bool
    autoreference: bool
    code: str
    name: str
    conscious: bool

def control_configuration(
    observation_level: int,
    *,
    agency: float,
    autoreference: float,
) -> ControlConfiguration:
    """
    Las cuatro configuraciones se aplican DENTRO de cada N.

        x.1 = sin agencia + sin autoreferencia
        x.2 = sin agencia + con autoreferencia
        x.3 = con agencia + sin autoreferencia
        x.4 = con agencia + con autoreferencia

    La condición agency × autoreference identifica el estado consciente
    dentro del nivel. Esto no mueve el Yo entre capas.
    """
    if observation_level not in (1, 2, 3):
        raise ValueError("observation_level debe ser 1, 2 o 3.")

    a = _clamp01(agency) > 0.0
    ar = _clamp01(autoreference) > 0.0

    suffix = {(False, False): 1, (False, True): 2, (True, False): 3, (True, True): 4}[(a, ar)]
    names = {
        1: "reacción pura",
        2: "observa pero no actúa",
        3: "actúa sin verse",
        4: "control consciente pleno",
    }

    return ControlConfiguration(
        level=observation_level,
        agency=a,
        autoreference=ar,
        code=f"{observation_level}.{suffix}",
        name=names[suffix],
        conscious=(a and ar),
    )

# ===========================================================
# 10. ESTADO SEMÁNTICO DEL YO
# ===========================================================

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
    L4 sigue siendo la casa del Yo en todos los casos.

    El resultado semántico cambia por N y por la configuración de control,
    no por una transferencia L4 -> L5.
    """
    cfg = control_configuration(
        observation_level,
        agency=agency,
        autoreference=autoreference,
    )

    if cfg.conscious and observation_level >= 2:
        return "YO_METACONSCIENTE"

    if cfg.conscious:
        return "YO_CONSCIENTE"

    return f"YO_EN_CONFIGURACION_{cfg.code}"

# ===========================================================
# 11. MOVIMIENTO DEL YO: DINÁMICA ENTRE CAPAS
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
    beta: float = BETA,
    observation_level: int,
    agency: float,
    autoreference: float,
) -> Tuple[float, ...]:
    """
    Decodificación L5 -> L4 -> L3 -> L2 -> L1.

    El movimiento no convierte L5 en una capa física adicional.
    L5 modula/observa; el retorno se expresa sobre el carril.

    La ganancia g = beta * D se usa únicamente cuando existe
    autoreferencia y agencia. El mecanismo de D puede reemplazarse por
    el detector contractual del repositorio.
    """
    layers = list(_validate_layers(activations))

    # En el modelo base, la consciencia por sí sola no altera el carril.
    # Solo un estado con agencia + autoreferencia produce retorno activo.
    conscious = (
        observation_level >= 1
        and _clamp01(agency) > 0.0
        and _clamp01(autoreference) > 0.0
    )

    if not conscious:
        return tuple(layers)

    # D_real completo requiere una medición temporal de identificación.
    # Aquí se utiliza beta como ganancia máxima estructural del retorno.
    gain = beta * min(1.0, _clamp01(agency) * _clamp01(autoreference))

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

        if b > a:
            direction = "activación"
        else:
            direction = "desactivación"

        changes.append(
            LayerMovement(
                source_layer=L5,
                target_layer=i,
                amount=abs(b - a),
                direction=direction,
                reason="retorno de la observación al carril",
            )
        )

    return tuple(changes)

# ===========================================================
# 12. RESULTADO COMPLETO
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
# 13. FÓRMULA MAESTRA
# ===========================================================

class L5Metaconsciencia:
    """
    Motor operativo del mirador L5.

    La posición del equilibrio del Yo permanece en L4.
    theta_eq no se utiliza para mover la geometría del edificio.
    """

    def __init__(
        self,
        *,
        theta_eq: float = THETA_CUBE_DEFAULT,
        theta_cube: float = THETA_CUBE_DEFAULT,
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
        """
        Cadena completa:

        1. estado L0..L6
        2. energía
        3. pesos
        4. receptor L1..L4
        5. ocupación de L5
        6. visibilidad desde L5
        7. señal I5
        8. observación N
        9. configuración x.1..x.4
        10. retorno L5 -> L4 -> L3 -> L2 -> L1
        11. salida completa
        """
        before = _validate_layers(activations)
        y = self.theta_eq if theta_y is None else float(theta_y)

        energies = calculate_energies(
            before,
            self.frictions,
            self.geometry,
        )
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

        i5 = calculate_i5(
            q5=q5,
            h5=h5,
            v5=v5,
        )

        n = determine_observation_level(
            i5,
            autoreference=autoreference,
        )

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
            observation_intensity(i5, k)
            for k in range(1, N_MAX + 1)
        )

        # novelty se conserva como entrada del modelo para la futura
        # función de paso beta. No se usa para alterar N: N es observación.
        _ = float(novelty)

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
            yo_state=yo_state(
                n,
                agency=agency,
                autoreference=autoreference,
            ),
            movements=movements,
            theta_y=y,
            theta_eq=self.theta_eq,
            loop_detected=bool(loop_detected),
        )

# ===========================================================
# 14. API DE COMPATIBILIDAD SIMPLE
# ===========================================================

def formula_maestra_l5(
    activations: Sequence[float],
    *,
    theta_y: float = THETA_CUBE_DEFAULT,
    theta_eq: float = THETA_CUBE_DEFAULT,
    agency: float = 0.0,
    autoreference: float = 0.0,
    frictions: Sequence[float] = DEFAULT_FRICTIONS,
    coherence_fn: Callable[[Sequence[float]], float] = default_coherence,
    sigma5: float = 0.029707,
    loop_detected: bool = False,
) -> L5Result:
    engine = L5Metaconsciencia(
        theta_eq=theta_eq,
        theta_cube=THETA_CUBE_DEFAULT,
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
# 15. PRUEBA DIRECTA DEL CARRIL COMPLETO
# ===========================================================

if __name__ == "__main__":
    estado = (1.0, 0.8, 0.7, 0.8, 0.9, 0.7, 0.8)

    resultado = formula_maestra_l5(
        estado,
        theta_y=THETA_CUBE_DEFAULT,
        agency=1.0,
        autoreference=1.0,
    )

    print("=" * 64)
    print("VPSI-TRUTH — FÓRMULA MAESTRA L5")
    print("=" * 64)
    print(f"Casa del Yo              : L4")
    print(f"Mirador                  : L5")
    print(f"Nivel de observación N   : {resultado.observation_level}")
    print(f"Configuración            : {resultado.control.code}")
    print(f"Estado del Yo            : {resultado.yo_state}")
    print(f"Coherencia receptor      : {resultado.coherence:.12f}")
    print(f"Calidad receptor q5      : {resultado.receptor_quality:.12f}")
    print(f"Distorsión               : {resultado.distortion:.12f}")
    print(f"Ocupación h5             : {resultado.occupancy:.12f}")
    print(f"Visibilidad V5           : {resultado.visibility:.12f}")
    print(f"Señal I5                 : {resultado.i5:.12f}")
    print(f"Umbral N2                : {THRESHOLD_N2:.12f}")
    print(f"Umbral N3                : {THRESHOLD_N3:.12f}")
    print(f"Descripción              : {resultado.level_description}")
    print("Activaciones antes      :", resultado.activations_before)
    print("Activaciones después    :", resultado.activations_after)
    print("Movimientos             :", len(resultado.movements))
    print("=" * 64)
