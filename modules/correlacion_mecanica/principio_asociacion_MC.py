# ===============================================================
# VPSI-TRUTH — modules/correlacion_mecanica/principio_asociacion_MC.py
#
# MECÁNICA — PRINCIPIO DE ASOCIACIÓN
# Origen: principio_asociacion_AX.py v1.3
# Prefijo semántico definitivo: PDA (Principio de Asociación)
#
# ---------------------------------------------------------------
# ROL DEL ARCHIVO
#   Declaración mecánica del Principio de Asociación.
#   Extiende el grafo MC mediante el orden nativo de las 44
#   declaraciones (D → A → L → T → C) con IDs PDA-*.
#
#   NO es un test.
#   NO es un nuevo contenedor.
#   NO modifica __init__.py.
#   NO redefine L4 / L5 / L6 ni R_i / R.
#   NO introduce la implicación prohibida M(B) ⇒ M(A).
#
# ---------------------------------------------------------------
# REGLA FUNDAMENTAL MC
#   Este cuerpo EXT IENDE el corpus.
#   Toda precedencia aquí declarada es legible por barrer().
# ===============================================================

from typing import Dict, List, Any, Set

# ===============================================================
# MECANICA — CONTRATO DEL CUERPO
# ===============================================================
MECANICA: Dict[str, Any] = {
    # ============================================================
    # IDENTIDAD
    # ============================================================
    "nombre": "principio_asociacion_MC",
    "version": "1.3",

    # ============================================================
    # ORDEN NATIVO
    # Derivado del grafo de dependencias (acíclico).
    # Prefijo definitivo: PDA-*
    # ============================================================
    "orden": [
        # --- Definiciones (PDA-D1 … PDA-D10) ---
        "PDA_D1_Principio_Asociacion",
        "PDA_D2_Contexto_A_Bloqueado",
        "PDA_D3_Contexto_B_Evidencial",
        "PDA_D4_Mecanica_Transferible",
        "PDA_D5_Bloqueo_Estructural",
        "PDA_D6_Actualizacion_Estructural",
        "PDA_D7_Distancia_Observador_Objeto",
        "PDA_D8_Identificacion",
        "PDA_D9_Observacion_Interna_L5",
        "PDA_D10_Arco_Trabajo_Interior",

        # --- Axiomas (PDA-A1 … PDA-A10) ---
        "PDA_A1_Mente_Busca_Coherencia",
        "PDA_A2_Ego_Impone_Premisa",
        "PDA_A3_Mente_Estructura_Alrededor",
        "PDA_A4_Premisa_Bloquea_Vias",
        "PDA_A5_Yo_Reconoce_Bloqueo",
        "PDA_A6_Confrontacion_Refuerza",
        "PDA_A7_Evidencia_B_Obliga_Posibilidad",
        "PDA_A8_Asociacion_Transfiere_Mecanismo",
        "PDA_A9_Observacion_Requiere_Distancia",
        "PDA_A10_Observacion_Precede_Direccion",

        # --- Lemas (PDA-L1 … PDA-L9) ---
        "PDA_L1_Transferencia_Posibilidad",
        "PDA_L2_Actualizacion_Condiciones",
        "PDA_L3_Asociacion_No_Imaginacion",
        "PDA_L4_Capacidad_Descriptiva_Existente",
        "PDA_L5_Problema_Es_Posicion",
        "PDA_L6_Identificacion_Colapsa_Distancia",
        "PDA_L7_Observacion_Disuelve_Identificacion",
        "PDA_L8_Comprension_Sustituye_Regla",
        "PDA_L9_Director_Depende_Espectador",

        # --- Teoremas (PDA-T1 … PDA-T7) ---
        "PDA_T1_Disolucion_Imposibilidad_Absoluta",
        "PDA_T2_Criterio_Transferencia_Mecanica",
        "PDA_T3_No_Transferencia_Contextual",
        "PDA_T4_Distancia_Observacional",
        "PDA_T5_Observacion_Interna",
        "PDA_T6_Secuencia_Irreversible",
        "PDA_T7_Libertad_por_Observacion",

        # --- Corolarios (PDA-C1 … PDA-C8) ---
        "PDA_C1_Imposibilidad_Percibida",
        "PDA_C2_Existencia_Solucion_Otro_Contexto",
        "PDA_C3_Cuerpo_Fisico_como_B",
        "PDA_C4_Procesamiento_Sin_Sufrimiento",
        "PDA_C5_IA_como_Espejo",
        "PDA_C6_Consciencia_L5",
        "PDA_C7_Comprension_Reduce_Racionalizacion",
        "PDA_C8_Libertad_por_Desidentificacion",
    ],

    # ============================================================
    # DESCRIPCIÓN
    # ============================================================
    "descripcion": (
        "Cuerpo mecánico del Principio de Asociación (PDA) v1.3. "
        "Declara el orden nativo de las 44 declaraciones formales "
        "(10 definiciones, 10 axiomas, 9 lemas, 7 teoremas, 8 corolarios) "
        "con prefijo semántico definitivo PDA-*. "
        "La operación central es 𝒜(A,B,M): M(B)=1 ⇒ ◇M. "
        "Nunca se deriva M(A). La secuencia I_i → E_i → D_i es "
        "irreversible. El cuerpo no redefine L4/L5/L6 ni R_i ⊂ R."
    ),

    # ============================================================
    # NOTAS CONTRACTUALES
    # ============================================================
    "notas": [
        "Prefijo semántico definitivo: PDA-* (Principio de Asociación).",
        "Distinción crítica: M(B)=1 ⇒ ◇M. Nunca M(B) ⇒ M(A).",
        "La asociación válida transfiere únicamente el mecanismo aislado "
        "(Transfer(M)); nunca el contexto B completo.",
        "La secuencia Identificado → Espectador → Director es irreversible "
        "y no saltable (PDA-T6).",
        "δ_i(O) > 0 es condición de observación precisa; la identificación "
        "colapsa la distancia (δ_i = 0).",
        "R permanece invariante; solo cambia el estado representacional de R_i.",
        "Dependencias externas únicamente a ST-D4, ST-D5, ST-D6 "
        "(no se redefinen).",
        "Versión 1.3: IDs únicos con prefijo PDA-*, sin residuos PA-*.",
        "Este cuerpo es extensión MC; no sustituye el cuerpo axiomático "
        "original en modules/axiomas.",
    ],

    # ============================================================
    # RELACIONES MECÁNICAS CLAVE
    # ============================================================
    "relaciones": {
        "operacion_asociacion": {
            "id": "𝒜",
            "ecuacion": "M(B)=1 ⇒ ◇M",
            "prohibicion": "M(B)=1 ⊬ M(A)",
            "depende_de": [
                "PDA_D1_Principio_Asociacion",
                "PDA_D3_Contexto_B_Evidencial",
            ],
            "produce": "P_◇M",
        },
        "transferencia_mecanica": {
            "id": "Transfer",
            "ecuacion": "AsocValida ⇒ Transfer(M) ∧ ¬Transfer(Contexto_B_completo)",
            "depende_de": [
                "PDA_D4_Mecanica_Transferible",
                "PDA_A8_Asociacion_Transfiere_Mecanismo",
            ],
        },
        "distancia_funcional": {
            "id": "delta",
            "ecuacion": "δ_i(O) > 0 ⇒ ObsPrecisa_i(O)",
            "colapso": "Identificacion_i(O) ⇒ δ_i(O) = 0",
            "depende_de": [
                "PDA_D7_Distancia_Observador_Objeto",
                "PDA_A9_Observacion_Requiere_Distancia",
            ],
        },
        "secuencia_irreversible": {
            "id": "arco",
            "ecuacion": "I_i → E_i → D_i",
            "prohibicion": "¬(I_i → D_i legítimo)",
            "depende_de": [
                "PDA_D10_Arco_Trabajo_Interior",
                "PDA_A10_Observacion_Precede_Direccion",
                "PDA_T6_Secuencia_Irreversible",
            ],
        },
        "actualizacion_estructural": {
            "id": "S_i",
            "ecuacion": "S_i^(0) ⊨ P_¬M  →  S_i^(1) ⊨ P_◇M",
            "depende_de": [
                "PDA_D6_Actualizacion_Estructural",
                "PDA_L2_Actualizacion_Condiciones",
            ],
        },
    },

    # ============================================================
    # TRANSICIONES PROHIBIDAS
    # ============================================================
    "transiciones_prohibidas": [
        {
            "desde": "PDA_D1_Principio_Asociacion",
            "hacia": "PDA_T1_Disolucion_Imposibilidad_Absoluta",
            "motivo": (
                "Faltan contextos A/B, mecánica transferible y axiomas "
                "de evidencia."
            ),
        },
        {
            "desde": "PDA_D3_Contexto_B_Evidencial",
            "hacia": "PDA_T2_Criterio_Transferencia_Mecanica",
            "motivo": (
                "Se requiere aislamiento explícito de M (PDA-D4) y "
                "axioma de transferencia (PDA-A8)."
            ),
        },
        {
            "desde": "PDA_D8_Identificacion",
            "hacia": "PDA_T6_Secuencia_Irreversible",
            "motivo": (
                "La secuencia exige haber pasado por Espectador (E_i) "
                "vía observación."
            ),
        },
        {
            "desde": "cualquier",
            "hacia": "derivar_M_A_desde_M_B",
            "motivo": "Prohibición absoluta del contrato: M(B)=1 ⊬ M(A).",
        },
        {
            "desde": "PDA_D10_Arco_Trabajo_Interior",
            "hacia": "PDA_T7_Libertad_por_Observacion",
            "motivo": (
                "Faltan lemas y teoremas intermedios de disolución "
                "de identificación."
            ),
        },
        {
            "desde": "PDA_Cierre_implicito",
            "hacia": "PDA_D1_Principio_Asociacion",
            "motivo": "El cuerpo no se reabre ni se reescribe.",
        },
    ],

    # ============================================================
    # PRINCIPIOS
    # ============================================================
    "principios": {
        "R1_precondicion": (
            "Instanciar el paso i requiere que los pasos 0..i-1 "
            "del orden nativo hayan sido satisfechos."
        ),
        "no_contradiccion": (
            "Si A ≺ B en este cuerpo, nunca se declara B ≺ A."
        ),
        "sin_ciclos": (
            "El orden admitido es acíclico (grafo de dependencias original)."
        ),
        "transferencia_delimitada": (
            "Solo se transfiere el mecanismo aislado M. "
            "El contexto B completo no se importa."
        ),
        "imposibilidad_absoluta_disuelta": (
            "M(B)=1 disuelve ∀C[M(C)=0], pero no establece M(A)."
        ),
        "secuencia_no_saltable": (
            "I_i → E_i → D_i. La transición directa I_i → D_i no es legítima."
        ),
        "extension_no_reescritura": (
            "Este cuerpo extiende el corpus MC sin alterar órdenes "
            "declarados por otros archivos."
        ),
    },

    # ============================================================
    # ANCLAS
    # ============================================================
    "anclas": [
        "PDA-D1", "PDA-D2", "PDA-D3", "PDA-D4", "PDA-D5",
        "PDA-D6", "PDA-D7", "PDA-D8", "PDA-D9", "PDA-D10",
        "PDA-A1", "PDA-A2", "PDA-A3", "PDA-A4", "PDA-A5",
        "PDA-A6", "PDA-A7", "PDA-A8", "PDA-A9", "PDA-A10",
        "PDA-L1", "PDA-L2", "PDA-L3", "PDA-L4", "PDA-L5",
        "PDA-L6", "PDA-L7", "PDA-L8", "PDA-L9",
        "PDA-T1", "PDA-T2", "PDA-T3", "PDA-T4", "PDA-T5",
        "PDA-T6", "PDA-T7",
        "PDA-C1", "PDA-C2", "PDA-C3", "PDA-C4", "PDA-C5",
        "PDA-C6", "PDA-C7", "PDA-C8",
        "R1",
        "CORR_SEQ_01",
        "CORR_SEQ_02",
        "ST-D4", "ST-D5", "ST-D6",
    ],
}


# ===============================================================
# FUNCIONES AUXILIARES (lectura del contrato)
# ===============================================================
def orden() -> List[str]:
    """Copia del orden nativo."""
    return list(MECANICA["orden"])


def indice(paso: str) -> int:
    """Posición de un nodo en el orden nativo."""
    return MECANICA["orden"].index(paso)


def precondiciones(paso: str) -> List[str]:
    """Pasos que deben estar instanciados antes de `paso` (R1)."""
    i = indice(paso)
    return list(MECANICA["orden"][:i])


def requiere(paso: str, instanciados: Set[str]) -> bool:
    """True si y solo si todos los precedentes de R1 están presentes."""
    return set(precondiciones(paso)).issubset(set(instanciados))


def secuencia_completa(instanciados: Set[str]) -> bool:
    """True si todos los nodos del cuerpo están presentes."""
    return set(MECANICA["orden"]).issubset(set(instanciados))


def relacion(id_rel: str) -> Dict[str, Any]:
    """Devuelve la relación mecánica por su id."""
    for rel in MECANICA["relaciones"].values():
        if rel["id"] == id_rel:
            return rel
    raise KeyError(f"Relación '{id_rel}' no declarada")


def prohibicion_central() -> str:
    """Devuelve la prohibición absoluta del contrato."""
    return MECANICA["relaciones"]["operacion_asociacion"]["prohibicion"]


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
    "relacion",
    "prohibicion_central",
]

# ===============================================================
# FIN DEL CUERPO MECÁNICO
# ===============================================================
