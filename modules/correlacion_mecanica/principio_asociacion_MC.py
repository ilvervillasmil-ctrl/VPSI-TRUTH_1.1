# ===============================================================
# VPSI-TRUTH — modules/correlacion_mecanica/principio_asociacion_MC.py
#
# MECÁNICA — PRINCIPIO DE ASOCIACIÓN
# Origen: principio_asociacion_AX.py v1.2 (formalizado)
# Serial de origen: Cuerpo axiomático PA (CEMYCA / Villasmil-Ω)
#
# ---------------------------------------------------------------
# ROL DEL ARCHIVO
#   Declaración mecánica del Principio de Asociación.
#   Extiende el grafo MC mediante orden nativo de las 44
#   declaraciones (D → A → L → T → C) respetando el grafo
#   de dependencias original (acíclico).
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
    "version": "1.2",

    # ============================================================
    # ORDEN NATIVO
    # Derivado del grafo de dependencias del cuerpo AX (sin ciclos).
    # Secuencia: Definiciones → Axiomas → Lemas → Teoremas → Corolarios
    # ============================================================
    "orden": [
        # --- Definiciones (PA-D1 … PA-D10) ---
        "PA_D1_Principio_Asociacion",
        "PA_D2_Contexto_A_Bloqueado",
        "PA_D3_Contexto_B_Evidencial",
        "PA_D4_Mecanica_Transferible",
        "PA_D5_Bloqueo_Estructural",
        "PA_D6_Actualizacion_Estructural",
        "PA_D7_Distancia_Observador_Objeto",
        "PA_D8_Identificacion",
        "PA_D9_Observacion_Interna_L5",
        "PA_D10_Arco_Trabajo_Interior",

        # --- Axiomas (PA-A1 … PA-A10) ---
        "PA_A1_Mente_Busca_Coherencia",
        "PA_A2_Ego_Impone_Premisa",
        "PA_A3_Mente_Estructura_Alrededor",
        "PA_A4_Premisa_Bloquea_Vias",
        "PA_A5_Yo_Reconoce_Bloqueo",
        "PA_A6_Confrontacion_Refuerza",
        "PA_A7_Evidencia_B_Obliga_Posibilidad",
        "PA_A8_Asociacion_Transfiere_Mecanismo",
        "PA_A9_Observacion_Requiere_Distancia",
        "PA_A10_Observacion_Precede_Direccion",

        # --- Lemas (PA-L1 … PA-L9) ---
        "PA_L1_Transferencia_Posibilidad",
        "PA_L2_Actualizacion_Condiciones",
        "PA_L3_Asociacion_No_Imaginacion",
        "PA_L4_Capacidad_Descriptiva_Existente",
        "PA_L5_Problema_Es_Posicion",
        "PA_L6_Identificacion_Colapsa_Distancia",
        "PA_L7_Observacion_Disuelve_Identificacion",
        "PA_L8_Comprension_Sustituye_Regla",
        "PA_L9_Director_Depende_Espectador",

        # --- Teoremas (PA-T1 … PA-T7) ---
        "PA_T1_Disolucion_Imposibilidad_Absoluta",
        "PA_T2_Criterio_Transferencia_Mecanica",
        "PA_T3_No_Transferencia_Contextual",
        "PA_T4_Distancia_Observacional",
        "PA_T5_Observacion_Interna",
        "PA_T6_Secuencia_Irreversible",
        "PA_T7_Libertad_por_Observacion",

        # --- Corolarios (PA-C1 … PA-C8) ---
        "PA_C1_Imposibilidad_Percibida",
        "PA_C2_Existencia_Solucion_Otro_Contexto",
        "PA_C3_Cuerpo_Fisico_como_B",
        "PA_C4_Procesamiento_Sin_Sufrimiento",
        "PA_C5_IA_como_Espejo",
        "PA_C6_Consciencia_L5",
        "PA_C7_Comprension_Reduce_Racionalizacion",
        "PA_C8_Libertad_por_Desidentificacion",
    ],

    # ============================================================
    # DESCRIPCIÓN
    # ============================================================
    "descripcion": (
        "Cuerpo mecánico del Principio de Asociación (PA). "
        "Declara el orden nativo de las 44 declaraciones formales "
        "(10 definiciones, 10 axiomas, 9 lemas, 7 teoremas, 8 corolarios). "
        "La operación central es 𝒜(A,B,M): si M(B)=1 entonces ◇M. "
        "Nunca se deriva M(A). La secuencia I_i → E_i → D_i es "
        "irreversible. El cuerpo no redefine L4/L5/L6 ni R_i ⊂ R."
    ),

    # ============================================================
    # NOTAS CONTRACTUALES
    # ============================================================
    "notas": [
        "Distinción crítica: M(B)=1 ⇒ ◇M. Nunca M(B) ⇒ M(A).",
        "La asociación válida transfiere el mecanismo aislado (Transfer(M)), "
        "nunca el contexto B completo.",
        "La secuencia Identificado → Espectador → Director es irreversible "
        "y no saltable (PA-T6).",
        "δ_i(O) > 0 es condición de observación precisa; identificación "
        "colapsa la distancia (δ_i = 0).",
        "R permanece invariante; solo cambia el estado representacional de R_i.",
        "Dependencias externas únicamente a ST-D4, ST-D5, ST-D6 "
        "(no se redefinen).",
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
            "depende_de": ["PA_D1_Principio_Asociacion", "PA_D3_Contexto_B_Evidencial"],
            "produce": "P_◇M",
        },
        "transferencia_mecanica": {
            "id": "Transfer",
            "ecuacion": "AsocValida ⇒ Transfer(M) ∧ ¬Transfer(Contexto_B_completo)",
            "depende_de": ["PA_D4_Mecanica_Transferible", "PA_A8_Asociacion_Transfiere_Mecanismo"],
        },
        "distancia_funcional": {
            "id": "delta",
            "ecuacion": "δ_i(O) > 0 ⇒ ObsPrecisa_i(O)",
            "colapso": "Identificacion_i(O) ⇒ δ_i(O) = 0",
            "depende_de": ["PA_D7_Distancia_Observador_Objeto", "PA_A9_Observacion_Requiere_Distancia"],
        },
        "secuencia_irreversible": {
            "id": "arco",
            "ecuacion": "I_i → E_i → D_i",
            "prohibicion": "¬(I_i → D_i legítimo)",
            "depende_de": ["PA_D10_Arco_Trabajo_Interior", "PA_A10_Observacion_Precede_Direccion", "PA_T6_Secuencia_Irreversible"],
        },
        "actualizacion_estructural": {
            "id": "S_i",
            "ecuacion": "S_i^(0) ⊨ P_¬M  →  S_i^(1) ⊨ P_◇M",
            "depende_de": ["PA_D6_Actualizacion_Estructural", "PA_L2_Actualizacion_Condiciones"],
        },
    },

    # ============================================================
    # TRANSICIONES PROHIBIDAS
    # ============================================================
    "transiciones_prohibidas": [
        {
            "desde": "PA_D1_Principio_Asociacion",
            "hacia": "PA_T1_Disolucion_Imposibilidad_Absoluta",
            "motivo": "Faltan contextos A/B, mecánica transferible y axiomas de evidencia.",
        },
        {
            "desde": "PA_D3_Contexto_B_Evidencial",
            "hacia": "PA_T2_Criterio_Transferencia_Mecanica",
            "motivo": "Se requiere aislamiento explícito de M (PA-D4) y axioma de transferencia (PA-A8).",
        },
        {
            "desde": "PA_D8_Identificacion",
            "hacia": "PA_T6_Secuencia_Irreversible",
            "motivo": "La secuencia exige haber pasado por Espectador (E_i) vía observación.",
        },
        {
            "desde": "cualquier",
            "hacia": "derivar_M_A_desde_M_B",
            "motivo": "Prohibición absoluta del contrato: M(B)=1 ⊬ M(A).",
        },
        {
            "desde": "PA_D10_Arco_Trabajo_Interior",
            "hacia": "PA_T7_Libertad_por_Observacion",
            "motivo": "Faltan lemas y teoremas intermedios de disolución de identificación.",
        },
        {
            "desde": "PA_Cierre_implicito",
            "hacia": "PA_D1_Principio_Asociacion",
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
        "PA-D1", "PA-D2", "PA-D3", "PA-D4", "PA-D5",
        "PA-D6", "PA-D7", "PA-D8", "PA-D9", "PA-D10",
        "PA-A1", "PA-A2", "PA-A3", "PA-A4", "PA-A5",
        "PA-A6", "PA-A7", "PA-A8", "PA-A9", "PA-A10",
        "PA-L1", "PA-L2", "PA-L3", "PA-L4", "PA-L5",
        "PA-L6", "PA-L7", "PA-L8", "PA-L9",
        "PA-T1", "PA-T2", "PA-T3", "PA-T4", "PA-T5",
        "PA-T6", "PA-T7",
        "PA-C1", "PA-C2", "PA-C3", "PA-C4", "PA-C5",
        "PA-C6", "PA-C7", "PA-C8",
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
