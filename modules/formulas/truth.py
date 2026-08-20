# ======================================================================
#
# VPSI-TRUTH — modules/formulas/truth.py
#
# FÓRMULA DE LA VERDAD
#
# ======================================================================
#
# PROPÓSITO
#
# Este módulo define y expone las capacidades responsables de calcular
# la Fórmula de la Verdad conforme a las definiciones canónicas de
# VPSI-TRUTH.
#
#     tru_ri(C, L, K)
#         Calcula Tru_Ri.
#
#     tru_total(C, L, K)
#         Calcula Tru_total.
#
# Engine descubre y utiliza estas capacidades dentro de la evaluación
# universal. Este módulo no necesita conocer qué módulo produce C, L, K
# ni qué capacidad consumirá posteriormente sus resultados.
#
# ======================================================================
#
# DEFINICIONES CANÓNICAS — VPSI v9.4
#
#     Tru_Ri(D)    = C(D) × L(D) × K(D)
#
#     Tru_total(D) = (Tru_Ri(D) × ALPHA) + BETA
#
# ======================================================================
#
# FLUJO
#
#     C ─┐
#     L ─┼──► tru_ri ───► Tru_Ri
#     K ─┘                    │
#                             ▼
#                          × ALPHA
#                             │
#                             ▼
#                          + BETA
#                             │
#                             ▼
#                         Tru_total
#
# ======================================================================
#
# CONSTANTES — AUTORIDAD CT
#
#     ALPHA = 26/27
#     BETA  =  1/27
#
# ALPHA y BETA no se definen ni redefinen aquí.
# La única fuente autorizada es:
#
#     modules.constante
#
# Las fórmulas deben importar directamente dichas constantes y no
# contener valores locales, copias ni sustituciones equivalentes.
#
# ======================================================================
#
# EVALUACIÓN UNIVERSAL
#
# Este módulo participa en la evaluación universal mediante sus
# capacidades declaradas en el contrato.
#
# Engine entrega los hechos disponibles; las capacidades de este módulo
# reciben las entradas que correspondan y producen los resultados
# definidos por las fórmulas.
#
#     Engine
#       │
#       ▼
#     evaluar_universal
#       │
#       ▼
#     Calculator ──► C, L, K
#                       │
#                       ▼
#                    Formulas
#                       │
#                 tru_ri / tru_total
#                       │
#                       ▼
#                VERDAD CUANTIFICADA
#
# ======================================================================
#
# INTEGRIDAD MATEMÁTICA
#
# Las operaciones utilizan Fraction para conservar exactitud racional.
# No se introducen límites, normalizaciones ni transformaciones ajenas
# a las definiciones canónicas.
#
# ======================================================================
#
# FUENTE NORMATIVA
#
#     Teorema de la Verdad — VPSI v9.4
#     Sección 2.14 — Definición 2.14
#
# ======================================================================

from fractions import Fraction
from modules.constante import ALPHA, BETA

# Metadatos de la fórmula
FORMULA = {
    "nombre": "verdad",
    "expresion": "Tru_total(D) = (C(D) * L(D) * K(D) * ALPHA) + BETA",
    "fuente": "Teorema de la Verdad, VPSI v9.4",
    "nota": "Tru_Ri(D) = C(D) * L(D) * K(D) (sin límites artificiales).",
}


def _exigir_fraction(valor, nombre: str) -> Fraction:
    """Exige que el valor sea Fraction. Rechaza float y otros tipos."""
    if not isinstance(valor, Fraction):
        raise TypeError(
            f"{nombre} debe ser Fraction, se recibió {type(valor).__name__}"
        )
    return valor


def tru_ri(C: Fraction, L: Fraction, K: Fraction) -> Fraction:
    """
    Calcula la contribución del observador (Tru_Ri).

    Fórmula:
        Tru_Ri(D) = C(D) * L(D) * K(D)

    Parámetros:
        C (Fraction): Coherencia interna de la descripción D.
        L (Fraction): Lógica estructural de la descripción D.
        K (Fraction): Correlación con el dominio observado O.

    Retorna:
        Fraction: Valor de Tru_Ri(D) en el rango [0, 1].
    """
    C = _exigir_fraction(C, "C")
    L = _exigir_fraction(L, "L")
    K = _exigir_fraction(K, "K")
    return C * L * K


def tru_total(C: Fraction, L: Fraction, K: Fraction) -> Fraction:
    """
    Calcula la verdad total (Tru_total) según la fórmula canónica del framework VPSI.

    Fórmula:
        Tru_total(D) = (Tru_Ri(D) * ALPHA) + BETA
                     = (C(D) * L(D) * K(D) * ALPHA) + BETA

    Parámetros:
        C (Fraction): Coherencia interna de la descripción D.
        L (Fraction): Lógica estructural de la descripción D.
        K (Fraction): Correlación con el dominio observado O.

    Retorna:
        Fraction: Valor de Tru_total(D) en el rango [β, 1], donde β = 1/27.
    """
    C = _exigir_fraction(C, "C")
    L = _exigir_fraction(L, "L")
    K = _exigir_fraction(K, "K")
    return (C * L * K * ALPHA) + BETA
