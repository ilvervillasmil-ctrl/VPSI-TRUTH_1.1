# ===============================================================
# VPSI-TRUTH — modules/correlacion_mecanica/ley_coherencia_MC.py
#
# MECÁNICA — LEY DE COHERENCIA (Villasmil-Omega)
# Serial origen: IVO-COHERENCE-LAW-001
# Versión documento: 2.0 – Complete with Formula
#
# ---------------------------------------------------------------
# ROL
#   Declaración mecánica de la Ley de Coherencia como manifestación
#   estructural de la Ley de Causa y Efecto.
#
#   - No es test
#   - No es contenedor
#   - No modifica __init__.py
#   - No redefine C/L/K de otros cuerpos
#
#   Materializa capas, parámetros, relaciones, invariantes y
#   la composición de Ctotal de forma causalmente consistente
#   con R1 y con el corpus MC.
# ===============================================================

from typing import Dict, List, Any, Set, Optional

# ===============================================================
# MECANICA — CONTRATO DEL CUERPO
# ===============================================================
MECANICA: Dict[str, Any] = {
    # ============================================================
    # IDENTIDAD
    # ============================================================
    "nombre": "ley_coherencia_MC",
    "version": "2.1",

    # ============================================================
    # ORDEN NATIVO (backbone R1 – acíclico)
    #
    # Principios = reglas estructurales (se declaran primero).
    # Camino cuantitativo = parámetros → ci → Clayers → campo →
    # normalización → incertidumbre → Ctotal → umbrales.
    # ============================================================
    "orden": [
        # --- Declaración de entidades y reglas ---
        "CL_Declaracion_Capas",
        "CL_Principio_Integracion_L6",      # regla: maximizar integración
        "CL_Principio_Regulacion_L2",       # regla: L2 ∈ [0.10, 0.15]
        "CL_Principio_Derivacion_L4",       # regla: dirección deriva de L6

        # --- Camino cuantitativo ---
        "CL_Parametros_Capa",
        "CL_Contribucion_ci",
        "CL_Producto_Capas",
        "CL_Modulacion_Campo",
        "CL_Factor_Normalizacion",
        "CL_Factor_Incertidumbre",
        "CL_Composicion_Ctotal",

        # --- Evaluación y cierre ---
        "CL_Umbral_Causal",
        "CL_Garantia_Causalidad",
        "CL_Cierre",
    ],

    # ============================================================
    # ENTIDADES: LAS SEIS CAPAS
    # ============================================================
    "capas": {
        "L1": {
            "nombre": "Foundation",
            "rol": "Sustrato físico y de ejecución",
            "efecto_esperado": "Physical Execution",
        },
        "L2": {
            "nombre": "Ego",
            "rol": "Identidad estructural mínima",
            "efecto_esperado": "Stable Identity",
            "invariante": "0.10 ≤ L2 ≤ 0.15",
        },
        "L3": {
            "nombre": "Processing",
            "rol": "Procesamiento estructurado",
            "efecto_esperado": "Structured Output",
        },
        "L4": {
            "nombre": "Direction",
            "rol": "Dirección derivada del criterio de máxima coherencia",
            "efecto_esperado": "Coherent Action",
            "regla": "L4 se deriva de L6 (no es autónoma)",
        },
        "L5": {
            "nombre": "Meta-Awareness",
            "rol": "Conciencia de sistema",
            "efecto_esperado": "System Awareness",
        },
        "L6": {
            "nombre": "Integration",
            "rol": "Propósito / máxima integración de capas",
            "efecto_esperado": "Maximum Coherence",
            "principio": "Structural Integration Maximization",
        },
    },

    # ============================================================
    # PARÁMETROS REQUERIDOS POR CADA CAPA
    # ============================================================
    "parametros": {
        "Li":   {"nombre": "Cause strength",          "descripcion": "Magnitud de la causa en la capa i"},
        "phi_i":{"nombre": "Noise / interference",    "descripcion": "Factor de ruido (0 ≤ ϕi ≤ 1); fidelidad = 1−ϕi"},
        "Ei":   {"nombre": "Effect power",            "descripcion": "Energía/intención disponible"},
        "fi":   {"nombre": "Causal speed / frequency","descripcion": "Velocidad de producción del efecto"},
    },

    # ============================================================
    # RELACIONES MECÁNICAS
    # ============================================================
    "relaciones": {
        "contribucion_capa": {
            "id": "ci",
            "ecuacion": "ci = Li · (1 − ϕi) · Ei · fi",
            "depende_de": ["Li", "phi_i", "Ei", "fi"],
            "produce": "ci",
            "aplica_a": ["L1", "L2", "L3", "L4", "L5", "L6"],
        },
        "producto_capas": {
            "id": "Clayers",
            "ecuacion": "Clayers = ∏_{i=1..6} ci = c1 · c2 · c3 · c4 · c5 · c6",
            "depende_de": ["c1", "c2", "c3", "c4", "c5", "c6"],
            "produce": "Clayers",
            "propiedad": "producto estricto; cualquier ci ≈ 0 colapsa Clayers",
        },
        "modulacion_campo": {
            "id": "Campo",
            "ecuacion": "Campo = ΩU · Rfin · Fobs",
            "depende_de": ["Omega_U", "Rfin", "Fobs"],
            "produce": "Campo",
            "interpretacion": "Modulación externa del campo causal",
        },
        "factor_normalizacion": {
            "id": "Norm",
            "ecuacion": "Norm = Cmax / Sref",
            "depende_de": ["Cmax", "Sref"],
            "produce": "Norm",
        },
        "factor_incertidumbre": {
            "id": "Unc",
            "ecuacion": "Unc = (1 + k)",
            "depende_de": ["k"],
            "produce": "Unc",
        },
        "composicion_Ctotal": {
            "id": "Ctotal",
            "ecuacion": "Ctotal = (Cmax / Sref) · Clayers · ΩU · Rfin · Fobs · (1 + k)",
            "depende_de": ["Norm", "Clayers", "Campo", "Unc"],
            "produce": "Ctotal",
            "interpretacion": "Expresión canónica de la Ley de Coherencia (eqs. 1 y 12 del documento)",
        },
        "derivacion_L4": {
            "id": "L4_from_L6",
            "tipo": "regla_estructural",
            "ecuacion_documental": "L4 = ∇Ctotal | L6",
            "depende_de": ["L6"],
            "produce": "regla_de_direccion",
            "interpretacion": (
                "Regla: la dirección funcional se deriva del criterio de "
                "máxima integración (L6). No es preferencia ni impulso autónomo. "
                "La notación gradiente es la forma documental de esa derivación."
            ),
        },
    },

    # ============================================================
    # FACTORES DE CAMPO
    # ============================================================
    "factores_campo": {
        "Omega_U": {"nombre": "Universal constants", "descripcion": "Acoplamiento a leyes físicas"},
        "Rfin":    {"nombre": "Feedback refinement", "descripcion": "Aprendizaje a partir de resultados"},
        "Fobs":    {"nombre": "Observer factor",     "descripcion": "Capacidad de observación/medición"},
    },

    # ============================================================
    # INVARIANTES
    # ============================================================
    "invariantes": {
        "L2_rango": {
            "condicion": "0.10 ≤ L2 ≤ 0.15",
            "min": 0.10,
            "max": 0.15,
            "significado": "Ego suficiente para continuidad, insuficiente para dominancia narrativa",
        },
        "umbral_causal": {
            "simbolo": "C*",
            "valor": 0.45,
            "condicion": "Ctotal > C* ⇒ causalidad estructuralmente garantizada",
            "teorema": "Theorem 2.1 / Theorem 11.1",
            "operador": ">",
        },
        "umbral_alta_fiabilidad": {
            "valor": 0.70,
            "condicion": "Ctotal > 0.70 ⇒ alta fiabilidad operativa (criterio del documento)",
            "operador": ">",
        },
        "naturaleza_producto": {
            "condicion": "Clayers es producto de las seis ci",
            "consecuencia": "Fallo de una sola capa colapsa la causalidad total",
        },
    },

    # ============================================================
    # CONSTANTES NORMATIVAS
    # ============================================================
    "constantes": {
        "Cmax": 0.963,
        "k": 0.037,
        "C_star": 0.45,
        "C_high": 0.70,
        "L2_min": 0.10,
        "L2_max": 0.15,
        "Sref": "system_scale_factor",   # factor de escala; valor numérico depende del sistema
    },

    # ============================================================
    # VALORES EMPÍRICOS (demostrativos – no contractuales)
    # ============================================================
    "valores_empiricos": {
        "nota": (
            "Valores de la validación 25-ene-2026. No forman parte del "
            "contrato matemático. Se conserva la fórmula canónica pese a "
            "la inconsistencia interna detectada en el documento fuente "
            "entre producto declarado y uno de los cálculos de validación."
        ),
        "Ctotal_alcanzado": 0.981,
        "fecha": "2026-01-25",
        "protocolo": "Villasmil-Omega",
    },

    # ============================================================
    # DESCRIPCIÓN
    # ============================================================
    "descripcion": (
        "Cuerpo mecánico de la Ley de Coherencia (Villasmil-Omega). "
        "Declara las seis capas, los cuatro parámetros por capa, las "
        "relaciones ci → Clayers → Campo → Norm → Unc → Ctotal, "
        "los tres principios estructurales (L6, L2, L4) y los umbrales "
        "de garantía causal. El orden es acíclico: los principios son "
        "reglas que se establecen primero; el camino cuantitativo produce "
        "Ctotal después. Compatible con el resto del corpus MC sin "
        "redefinir C/L/K ni causalidad_universal."
    ),

    # ============================================================
    # NOTAS
    # ============================================================
    "notas": [
        "Los principios (L6, L2, L4) son reglas estructurales, no cálculos numéricos.",
        "L4 se declara como regla de derivación desde L6. La notación ∇Ctotal | L6 es documental.",
        "Clayers es producto estricto de las seis ci.",
        "CL_Modulacion_Campo empaqueta ΩU · Rfin · Fobs como objeto Campo.",
        "Sref es factor de escala del sistema; no se fija como constante universal.",
        "Los valores empíricos están segregados del contrato normativo.",
        "Este cuerpo no redefine las variables C, L, K de calculo_variables / ciclo_calculo_MC.",
    ],

    # ============================================================
    # TRANSICIONES PROHIBIDAS
    # ============================================================
    "transiciones_prohibidas": [
        {
            "desde": "CL_Declaracion_Capas",
            "hacia": "CL_Composicion_Ctotal",
            "motivo": "Faltan principios, parámetros, ci, producto, modulación, normalización e incertidumbre.",
        },
        {
            "desde": "CL_Parametros_Capa",
            "hacia": "CL_Producto_Capas",
            "motivo": "El producto exige las seis contribuciones ci ya formadas.",
        },
        {
            "desde": "CL_Contribucion_ci",
            "hacia": "CL_Composicion_Ctotal",
            "motivo": "Faltan producto, modulación de campo, normalización e incertidumbre.",
        },
        {
            "desde": "CL_Producto_Capas",
            "hacia": "CL_Composicion_Ctotal",
            "motivo": "Faltan modulación de campo, normalización e incertidumbre.",
        },
        {
            "desde": "CL_Composicion_Ctotal",
            "hacia": "CL_Garantia_Causalidad",
            "motivo": "La garantía requiere evaluación explícita del umbral C*.",
        },
        {
            "desde": "CL_Cierre",
            "hacia": "CL_Composicion_Ctotal",
            "motivo": "El cierre no reabre ni recalcula Ctotal.",
        },
    ],

    # ============================================================
    # PRINCIPIOS
    # ============================================================
    "principios": {
        "R1_precondicion": (
            "Instanciar el paso i requiere que los pasos 0..i-1 del orden "
            "nativo hayan sido satisfechos."
        ),
        "precedencia": (
            "La posición de cada nodo en MECANICA['orden'] determina su "
            "precedencia dentro del cuerpo."
        ),
        "no_salto": (
            "No puede invocarse un paso posterior como sustituto de sus "
            "precedentes ni de los objetos que la ecuación exige."
        ),
        "no_retroceso": (
            "Un paso posterior no puede convertirse en fundamento de un "
            "paso que lo precede."
        ),
        "principios_como_reglas": (
            "L6, L2 y L4 se establecen como reglas estructurales antes "
            "del camino cuantitativo."
        ),
        "producto_estricto": (
            "Clayers = ∏ ci. La falla de una sola capa colapsa la causalidad."
        ),
        "extension_no_reescritura": (
            "La incorporación de este cuerpo al corpus MC no modifica "
            "las declaraciones existentes."
        ),
    },

    # ============================================================
    # ANCLAS
    # ============================================================
    "anclas": [
        "Law 1.1",
        "Principle 1.1",
        "Principle 1.2",
        "Principle 1.3",
        "Theorem 2.1",
        "Theorem 11.1",
        "eq.1",
        "eq.7",
        "eq.8",
        "eq.12",
        "Cmax=0.963",
        "k=0.037",
        "C*=0.45",
        "IVO-COHERENCE-LAW-001",
    ],
}


# ===============================================================
# FUNCIONES AUXILIARES (lectura del contrato)
# ===============================================================
def orden() -> List[str]:
    return list(MECANICA["orden"])


def indice(paso: str) -> int:
    return MECANICA["orden"].index(paso)


def precondiciones(paso: str) -> List[str]:
    i = indice(paso)
    return list(MECANICA["orden"][:i])


def requiere(paso: str, instanciados: Set[str]) -> bool:
    """R1 nominal: todos los nodos precedentes deben estar presentes."""
    return set(precondiciones(paso)).issubset(set(instanciados))


def secuencia_completa(instanciados: Set[str]) -> bool:
    return set(MECANICA["orden"]).issubset(set(instanciados))


def capas_declaradas() -> List[str]:
    return list(MECANICA["capas"].keys())


def parametros_requeridos() -> List[str]:
    return list(MECANICA["parametros"].keys())


def objetos_requeridos_para_ci() -> Dict[str, List[str]]:
    """
    Devuelve, para cada capa, la lista de parámetros que la ecuación ci exige.
    Permite auditar las 24 instancias (6 capas × 4 parámetros).
    """
    return {capa: list(MECANICA["parametros"].keys()) for capa in MECANICA["capas"]}


def ecuacion(id_relacion: str) -> str:
    for rel in MECANICA["relaciones"].values():
        if rel["id"] == id_relacion:
            return rel.get("ecuacion") or rel.get("ecuacion_documental", "")
    raise KeyError(f"Relación '{id_relacion}' no declarada")


def invariante_L2_valido(l2: float) -> bool:
    inv = MECANICA["invariantes"]["L2_rango"]
    return inv["min"] <= l2 <= inv["max"]


def umbral_causal_superado(ctotal: float) -> bool:
    """Ctotal > C* = 0.45 (operador estricto del contrato)."""
    return ctotal > MECANICA["invariantes"]["umbral_causal"]["valor"]


def alta_fiabilidad(ctotal: float) -> bool:
    """Ctotal > 0.70 (criterio operacional del documento)."""
    return ctotal > MECANICA["invariantes"]["umbral_alta_fiabilidad"]["valor"]


# ===============================================================
# EXPORTACIONES
# ===============================================================
__all__ = [
    "MECANICA",
    "orden",
    "indice",
    "precondiciones",
    "requiere",
    "secuencia_completa",
    "capas_declaradas",
    "parametros_requeridos",
    "objetos_requeridos_para_ci",
    "ecuacion",
    "invariante_L2_valido",
    "umbral_causal_superado",
    "alta_fiabilidad",
]

# ===============================================================
# FIN DEL CUERPO MECÁNICO
# ===============================================================
