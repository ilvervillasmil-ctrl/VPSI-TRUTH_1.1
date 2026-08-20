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
from typing import Any, Dict, List, Optional, Sequence

# Autoridad de constantes (CT)
from modules.constante import ALPHA, BETA, C_MAX, R_FIN

# Constantes locales de omega
from .constants import (
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

# Hermanos dentro de formulas_omega
from .energy import LayerEnergy
from .negentropy import NegentropyCalculator
from .presence import PresenceLogic
from .wonder import WonderLogic
from .interaction import ExternalInteraction
from .resonance import ResonanceLogic
from .metaconsciousness import MetaconsciousnessCalculator

# ===============================================================
# NOTA TÉCNICA 1 — BACKEND NUMÉRICO
# ===============================================================
#
# Las operaciones de producto, normalización, clamp, √ y atan
# se solicitan al backend cuando el cálculo es local a este
# archivo.
#
# Las sub-fórmulas (energía, presencia, wonder, resonancia,
# negentropía, metaconciencia) viven en sus propios archivos.
# Cada una debe, con el tiempo, respetar el mismo protocolo de
# backend. Mientras tanto, este archivo documenta que el valor
# que recibe de ellas se incorpora tal cual a la cadena C_β.
#
# No se permite degradar silenciosamente Decimal → float → op.
#
# ===============================================================

# ===============================================================
# NOTA TÉCNICA 2 — QUÉ DETERMINA C_Ω
# ===============================================================
#
# C_Ω operativa = clamp(C_β, 0, C_MAX)
#
# C_α y C_total son métricas internas de balance angular.
# No entran en la fórmula maestra de C_Ω.
#
# La fórmula maestra es:
#
#   C_β = P_norm · (α/S) · R_fin · ρ · P_t · A · I_ext
#
# ===============================================================


# ---------------------------------------------------------------
# Constantes de normalización (derivadas, no libres)
# ---------------------------------------------------------------
# E_0_REF  = ν_0 = Φ^0 = 1  (con L=1 en definición de frequency(0))
# P_max    = Π_i [(1-φ_i)·ν_i] / E_0   con L_i = 1
# ---------------------------------------------------------------

_E0_REF = LayerEnergy.frequency(0)

_PRODUCTO_MAX = 1.0
for _i in range(NUM_LAYERS):
    _E_max_i = (1.0 - LAYER_FRICTION[_i]) * LayerEnergy.frequency(_i)
    _PRODUCTO_MAX *= _E_max_i

C_BETA_MAX = ALPHA_OVER_S * R_FIN


# ===============================================================
# C_β — FÓRMULA MAESTRA
# ===============================================================

def compute_c_beta(
    activations: Sequence[float],
    frictions: Optional[Sequence[float]] = None,
    rho: float = 1.0,
    delta_t: float = 0.0,
    tau: float = 1.0,
    novelty: float = 5.0,
    sensitivity: float = 5.0,
    external_coherences: Optional[Sequence[float]] = None,
    backend: str = "float",
    precision: int = 50,
) -> Dict[str, Any]:
    """
    C_β = P_norm · (α/S) · R_fin · ρ · P_t · A · I_ext

    P_norm = [Π (E_i/E_0)] / P_max
    """
    motor = obtener_backend(backend, precision)

    if frictions is None:
        frictions = LAYER_FRICTION

    energies = LayerEnergy.compute_all(list(activations), list(frictions))

    # Producto bruto Π (E_i / E_0)
    producto_raw = motor.convertir(1.0)
    e0 = motor.convertir(_E0_REF)

    for e in energies:
        e_m = motor.convertir(e)
        if e0 == motor.cero():
            factor = motor.cero()
        else:
            factor = motor.dividir(e_m, e0)
        producto_raw = motor.multiplicar(producto_raw, factor)

    p_max = motor.convertir(_PRODUCTO_MAX)
    if p_max == motor.cero():
        producto_norm = motor.cero()
    else:
        producto_norm = motor.dividir(producto_raw, p_max)

    p_t = PresenceLogic.compute(delta_t, tau)
    a = WonderLogic.compute(novelty, sensitivity)

    if external_coherences and len(external_coherences) > 0:
        i_ext = ExternalInteraction.compute_multi(list(external_coherences))
    else:
        i_ext = 1.0

    # C_β = P_norm · (α/S) · R_fin · ρ · P_t · A · I_ext
    c_beta = producto_norm
    for factor in (
        ALPHA_OVER_S,
        R_FIN,
        rho,
        p_t,
        a,
        i_ext,
    ):
        c_beta = motor.multiplicar(c_beta, motor.convertir(factor))

    return {
        "c_beta": c_beta,
        "energies": energies,
        "product": producto_norm,
        "producto_raw": producto_raw,
        "producto_norm": producto_norm,
        "producto_max": _PRODUCTO_MAX,
        "alpha_over_s": ALPHA_OVER_S,
        "r_fin": R_FIN,
        "rho": rho,
        "p_t": p_t,
        "wonder": a,
        "i_ext": i_ext,
        "backend": backend,
        "precision": precision if backend == "decimal" else None,
    }


# ===============================================================
# C_α
# ===============================================================

def compute_c_alpha(
    integration: float,
    quality: float,
    complexity: float,
    uncertainty: float,
    backend: str = "float",
    precision: int = 50,
) -> Dict[str, Any]:
    """
    C_α = (I · Q) / (Cpx + U + β)

    β actúa como u_min: piso que evita denominador nulo y
    expresa el residuo estructural.
    """
    motor = obtener_backend(backend, precision)

    u_min = motor.convertir(BETA)
    numerador = motor.multiplicar(
        motor.convertir(integration),
        motor.convertir(quality),
    )
    denominador = motor.sumar(
        motor.sumar(
            motor.convertir(complexity),
            motor.convertir(uncertainty),
        ),
        u_min,
    )

    if denominador == motor.cero():
        c_alpha = motor.cero()
    else:
        c_alpha = motor.dividir(numerador, denominador)

    return {
        "c_alpha": c_alpha,
        "integration": integration,
        "quality": quality,
        "complexity": complexity,
        "uncertainty": uncertainty,
        "u_min": BETA,
        "backend": backend,
        "precision": precision if backend == "decimal" else None,
    }


# ===============================================================
# C_total (métrica interna de balance; no define C_Ω)
# ===============================================================

def compute_c_total(
    c_beta: Any,
    c_alpha: Any,
    backend: str = "float",
    precision: int = 50,
) -> Dict[str, Any]:
    """
    C_total = √(C_β² + C_α²)
    θ_actual = atan(C_β / C_α)  si C_α > 0
    """
    motor = obtener_backend(backend, precision)

    cb = motor.convertir(c_beta)
    ca = motor.convertir(c_alpha)

    # √(cb² + ca²) — con float backend; Decimal exige sqrt en cadena
    if backend == "float":
        c_total = math.sqrt(float(cb) ** 2 + float(ca) ** 2)
        if float(ca) > 0.0:
            theta_actual = math.atan(float(cb) / float(ca))
        elif float(cb) > 0.0:
            theta_actual = math.pi / 2.0
        else:
            theta_actual = 0.0
    else:
        # Sin atan/sqrt de precisión arbitraria aún en el backend:
        # no se degrada a float en silencio.
        raise NotImplementedError(
            "compute_c_total en backend '{}' requiere sqrt y atan "
            "de precisión arbitraria en el backend numérico.".format(backend)
        )

    theta_deviation = theta_actual - THETA_CUBE

    if abs(theta_deviation) < 0.01:
        balance = "CENTERED"
    elif theta_deviation > 0:
        balance = "EXCESS_EXPERIENCE"
    else:
        balance = "EXCESS_MEASUREMENT"

    c_beta_ideal = c_total * math.sin(THETA_CUBE)
    c_alpha_ideal = c_total * math.cos(THETA_CUBE)

    return {
        "c_total": c_total,
        "c_beta": c_beta,
        "c_alpha": c_alpha,
        "theta_actual": theta_actual,
        "theta_actual_deg": math.degrees(theta_actual),
        "theta_cube": THETA_CUBE,
        "theta_cube_deg": math.degrees(THETA_CUBE),
        "theta_deviation": theta_deviation,
        "theta_deviation_deg": math.degrees(theta_deviation),
        "balance": balance,
        "c_beta_ideal": c_beta_ideal,
        "c_alpha_ideal": c_alpha_ideal,
        "backend": backend,
    }


# ===============================================================
# C_Ω BÁSICA
# ===============================================================

def compute_basic(
    energies: Sequence[float],
    i_ext: float = 1.0,
    backend: str = "float",
    precision: int = 50,
) -> Dict[str, Any]:
    """
    C_Ω_basic = α · H + β · I_ext
    H = negentropía (armonía) sobre la distribución de energías.
    """
    motor = obtener_backend(backend, precision)

    harmony = NegentropyCalculator.harmony(list(energies))
    c_omega = motor.sumar(
        motor.multiplicar(motor.convertir(ALPHA), motor.convertir(harmony)),
        motor.multiplicar(motor.convertir(BETA), motor.convertir(i_ext)),
    )

    return {
        "c_omega": c_omega,
        "harmony": harmony,
        "i_ext": i_ext,
        "backend": backend,
        "precision": precision if backend == "decimal" else None,
    }


# ===============================================================
# ANÁLISIS COMPLETO → C_Ω
# ===============================================================

def calcular(
    activations: Sequence[float],
    frictions: Optional[Sequence[float]] = None,
    rho: float = 1.0,
    delta_t: float = 0.0,
    tau: float = 1.0,
    novelty: float = 5.0,
    sensitivity: float = 5.0,
    external_coherences: Optional[Sequence[float]] = None,
    integration: float = 0.5,
    quality: float = 0.5,
    complexity: float = 1.0,
    uncertainty: float = 0.1,
    backend: str = "float",
    precision: int = 50,
) -> Dict[str, Any]:
    """
    Evaluación completa.

    C_Ω = clamp(C_β, 0, C_MAX)

    C_α y C_total se reportan como métricas internas.
    No determinan C_Ω.
    """
    if frictions is None:
        frictions = LAYER_FRICTION

    beta_r = compute_c_beta(
        activations,
        frictions,
        rho,
        delta_t,
        tau,
        novelty,
        sensitivity,
        external_coherences,
        backend=backend,
        precision=precision,
    )
    alpha_r = compute_c_alpha(
        integration,
        quality,
        complexity,
        uncertainty,
        backend=backend,
        precision=precision,
    )

    # C_total solo en float hasta tener atan/sqrt de alta precisión
    total_r = compute_c_total(
        float(beta_r["c_beta"]),
        float(alpha_r["c_alpha"]),
        backend="float",
        precision=precision,
    )

    energies = beta_r["energies"]
    mc = MetaconsciousnessCalculator.compute(
        list(activations),
        list(frictions),
    )

    # C_Ω = clamp(C_β, 0, C_MAX)
    c_beta_val = float(beta_r["c_beta"])
    c_omega = min(C_MAX, max(0.0, c_beta_val))

    if c_omega >= ALPHA:
        code, name = CODE_INTEGRATED, "Integrated Architect"
    elif c_omega >= 0.4:
        code, name = CODE_SATURATION, "Critical Saturation"
    else:
        code, name = CODE_ENTROPY, "Terminal Entropy"

    return {
        "ok": True,
        "valor": c_omega,
        "c_omega": c_omega,
        "c_beta": beta_r,
        "c_alpha": alpha_r,
        "c_total": total_r,
        "negentropy": NegentropyCalculator.compute(energies),
        "metaconsciousness": mc,
        "mc_level": MetaconsciousnessCalculator.level_name(mc),
        "resonance": ResonanceLogic.compute(energies),
        "diagnostic_code": code,
        "diagnostic_name": name,
        "four_pillars": {
            "beta": BETA,
            "kappa": KAPPA,
            "alpha": ALPHA,
            "emergence": sum(energies) * (1.0 - KAPPA) / 2.0,
        },
        "backend": backend,
        "precision": precision if backend == "decimal" else None,
        "nota": (
            "C_Ω = clamp(C_β, 0, C_MAX); "
            "C_β = P_norm·(α/S)·R_fin·ρ·P_t·A·I_ext. "
            "C_α y C_total no determinan C_Ω."
        ),
    }


# ===============================================================
# TRAYECTORIA TEMPORAL
# ===============================================================
#
# SessionStateOmega no altera la fórmula.
# Solo acumula evaluaciones sucesivas de calcular().
# CODE_LOOP: C_Ω alta sin variación → bucle, no máximo real.
# β > 0 garantiza que un sistema real no es estáticamente perfecto.
#
# ===============================================================

class SessionStateOmega:
    """
    Coherence as a trajectory, not a static number.
    """

    def __init__(self, tau: float = 60.0) -> None:
        self.tau = tau
        self.history: List[Dict[str, Any]] = []

    def update(
        self,
        activations: Sequence[float],
        frictions: Optional[Sequence[float]] = None,
        external_coherences: Optional[Sequence[float]] = None,
        integration: float = 0.5,
        quality: float = 0.5,
        complexity: float = 1.0,
        uncertainty: float = 0.1,
        backend: str = "float",
        precision: int = 50,
    ) -> float:
        result = calcular(
            activations=activations,
            frictions=frictions,
            integration=integration,
            quality=quality,
            complexity=complexity,
            uncertainty=uncertainty,
            external_coherences=external_coherences,
            backend=backend,
            precision=precision,
        )
        self.history.append(result)
        return float(result["c_omega"])

    def trajectory(self) -> List[float]:
        return [float(e["c_omega"]) for e in self.history]

    def detect_loop(
        self,
        window: int = LOOP_WINDOW,
        threshold: float = LOOP_THRESHOLD,
    ) -> bool:
        """
        CODE_LOOP (9999):
        C_Ω > threshold y (max-min) < LOOP_VARIANCE durante `window` ciclos.
        """
        if len(self.history) < window:
            return False
        recent = self.trajectory()[-window:]
        variance = max(recent) - min(recent)
        return all(c > threshold for c in recent) and variance < LOOP_VARIANCE

    def session_balance(self) -> str:
        if not self.history:
            return "NO_DATA"
        last = self.history[-1]
        return last.get("c_total", {}).get("balance", "NO_DATA")

    def c_omega_trajectory(self) -> List[float]:
        return self.trajectory()


# ===============================================================
# API DE COMPATIBILIDAD
# ===============================================================
# Una sola fuente matemática: las funciones de arriba.
# ===============================================================

class CoherenceEngine:
    PRODUCTO_MAX = _PRODUCTO_MAX
    C_BETA_MAX = C_BETA_MAX

    @staticmethod
    def compute_c_beta(*args, **kwargs):
        return compute_c_beta(*args, **kwargs)

    @staticmethod
    def compute_c_alpha(*args, **kwargs):
        return compute_c_alpha(*args, **kwargs)

    @staticmethod
    def compute_c_total(*args, **kwargs):
        return compute_c_total(*args, **kwargs)

    @staticmethod
    def compute_basic(*args, **kwargs):
        return compute_basic(*args, **kwargs)

    @staticmethod
    def full_analysis(*args, **kwargs):
        return calcular(*args, **kwargs)

    @staticmethod
    def metacube_level(c_total, level=0):
        return {
            "level": level,
            "c_total_here": c_total,
            "is_beta_of_level": level + 1,
            "ratio_alpha_beta": ALPHA / BETA,
        }


# ===============================================================
# NOTA DE IMPLEMENTACIÓN 1 — POR QUÉ C_Ω = C_β CLAMPED
# ===============================================================
#
# La fuente define la fórmula maestra como el producto de capas
# y factores (C_β). C_α mide otro eje (integración/calidad).
# C_total es la norma euclídea de ambos ejes para balance
# angular respecto de θ_cube. No sustituye a C_β.
#
# C_MAX = α = 26/27 es techo estructural (Ley de Manifestación
# Incompleta): β no se elimina.
#
# ===============================================================

# ===============================================================
# NOTA DE IMPLEMENTACIÓN 2 — PRECISIÓN Y SUB-FÓRMULAS
# ===============================================================
#
# Presence, Wonder, Energy, Negentropy, Resonance, Interaction
# y Metaconsciousness deben migrar al mismo protocolo de backend.
# Hasta entonces, sus salidas se incorporan a la cadena C_β
# sin conversión silenciosa adicional dentro de este archivo
# cuando backend="float".
#
# compute_c_total en backend distinto de float exige sqrt y atan
# de precisión arbitraria; no se degrada a math.* en silencio.
#
# ===============================================================

# ===============================================================
# NOTA METODOLÓGICA PERMANENTE
# ===============================================================
#
# La representación numérica nunca debe limitar
# anticipadamente la matemática del motor.
#
# Cada fórmula debe analizarse según su naturaleza matemática,
# científica y dimensional antes de seleccionar su backend.
#
# float es una opción de evaluación aproximada.
# Decimal es una opción de precisión decimal.
# Fraction permite exactitud racional cuando corresponde.
# Otros backends podrán proporcionar precisión arbitraria,
# cálculo simbólico, números complejos, unidades,
# incertidumbre u otras capacidades.
#
# La fórmula determina las capacidades necesarias del backend.
# El backend no determina ni modifica la fórmula.
#
# Ninguna operación intermedia debe degradar silenciosamente
# la precisión solicitada.
#
# ===============================================================

__all__ = [
    "compute_c_beta",
    "compute_c_alpha",
    "compute_c_total",
    "compute_basic",
    "calcular",
    "SessionStateOmega",
    "CoherenceEngine",
    "C_BETA_MAX",
]

# ===============================================================
# FIN
# ===============================================================
