# ===============================================================
# formulas_omega/metabolic_scaling.py — Escalado metabólico (Corolario 8)
# ===============================================================
#
# Fórmulas:
#
#   κ = Σᵢ (bᵢ_masa + bᵢ_tasa) · cᵢ  /  Σᵢ cᵢ     (solo L0–L5)
#
#   BMR(M) = B₀ · α · M^κ
#
# Variables:
#
#   M           — masa corporal (kg), M > 0
#   B₀          — constante de escala (default 4.6196 W·kg^−κ)
#   α           — ALPHA = 26/27 (L6 Propósito: no escala con M)
#   bᵢ_masa     — exponente de masa del órgano/capa i
#   bᵢ_tasa     — exponente de tasa específica del órgano/capa i
#   cᵢ          — fracción del BMR aportada por la capa i
#   κ           — exponente metabólico emergente (≈ 0.75 Kleiber)
#   BMR         — metabolismo basal predicho (Watts)
#
# Estructura:
#
#   L0–L5 escalan con la masa.
#   L6 (Propósito) es atractor estructural α: constante para
#   todo organismo vivo, independiente del tamaño.
#
# Fuentes:
#   Wang 2001, Gallagher 1998, Karbowski 2007, Lindstedt & Calder 1981
#   Kleiber 1932, McNab 2008
#
# ===============================================================

from modules.constante import ALPHA, BETA


# ── CAPAS L0-L5: datos reales de literatura ──────────────────
# Cada capa: (b_masa, b_tasa_especifica, ci_fraccion_BMR)
#   b_total = b_masa + b_tasa_especifica
#   ci      = fracción del BMR total aportada por ese órgano

LAYER_DATA = {
    "L0_caos_adiposo":   (1.000,  0.000, 0.100),  # Gallagher 1998
    "L1_cuerpo_musculo": (1.000, -0.170, 0.220),  # Wang 2001
    "L2_ego_higado":     (0.870, -0.270, 0.216),  # Wang 2001
    "L3_mente_cerebro":  (0.760, -0.140, 0.202),  # Karbowski 2007
    "L4_ser_cardio":     (0.917, -0.101, 0.169),  # Wang 2001
    "L5_meta_residual":  (1.000, -0.170, 0.093),  # Wang 2001
    # L6 Propósito: b=0, factor α constante — no entra en κ
}

# ── CONSTANTE DE L6 ───────────────────────────────────────────
L6_PURPOSE = ALPHA   # 26/27 — coherencia máxima, invariante


def kappa_bio() -> float:
    """
    Exponente metabólico de Kleiber derivado desde UCF.

    κ = Σᵢ (bᵢ_masa + bᵢ_tasa) · cᵢ / Σcᵢ

    Donde la suma corre sobre L0-L5 únicamente.
    L6 entra como factor multiplicativo constante α en B₀.

    Returns:
        κ ≈ 0.7526  (Kleiber empírico: 0.75, error < 0.3%)
    """
    weighted_sum = 0.0
    total_ci     = 0.0
    for b_masa, b_tasa, ci in LAYER_DATA.values():
        b_total       = b_masa + b_tasa
        weighted_sum += b_total * ci
        total_ci     += ci
    return weighted_sum / total_ci


def bmr(mass_kg: float, b0: float = 4.6196) -> float:
    """
    Metabolismo basal predicho por UCF.

    BMR(M) = B₀ · α · M^κ

    Args:
        mass_kg: masa corporal en kg
        b0:      constante de escala calibrada (W·kg^-κ)
                 default: 4.6196 calibrado sobre 9 mamíferos
                 (Kleiber 1932, McNab 2008)

    Returns:
        BMR en Watts
    """
    if mass_kg <= 0:
        raise ValueError("mass_kg debe ser positivo")
    return b0 * L6_PURPOSE * (mass_kg ** kappa_bio())


def layer_contribution(layer_name: str) -> float:
    """
    Contribución de una capa al exponente global κ.

    Returns:
        bᵢ_total · cᵢ  (contribución ponderada al exponente)
    """
    if layer_name not in LAYER_DATA:
        raise KeyError(f"Capa desconocida: {layer_name}")
    b_masa, b_tasa, ci = LAYER_DATA[layer_name]
    return (b_masa + b_tasa) * ci
