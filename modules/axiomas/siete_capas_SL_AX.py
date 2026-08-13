# ===============================================================
# modules/axiomas/siete_capas_SL_AX.py
# Cuerpo axiomático: Seven-Layer Theorem (SLT)
#
# FUENTE NORMATIVA ÚNICA:
#   The Seven-Layer Theorem: Universal Structure, Bounded
#   Integration, and the Irreducibility of Potential in Complex
#   Systems — Ilver Villasmil
#
# REGLA ABSOLUTA:
#   Paper → representación contractual → Engine
#   El código no dice más, menos ni algo distinto de lo que dice
#   el Paper. No reinterpreta, no corrige, no suaviza, no amplía.
#
# Carga: modules/axiomas/__init__.py vía CUERPO + declaraciones()
# Esquema: id, tipo, sujeto, relacion, objeto, polaridad, cota,
#          depende_de, gobierna, enunciado
# Tipos: definicion | axioma | teorema | corolario
# ===============================================================

"""
Cuerpo axiomático: siete_capas_SL_AX

Transcripción contractual del Paper Seven-Layer Theorem.
Numeración, nombres, condiciones, cuantificadores, implicaciones,
equivalencias, cotas y alcance se conservan según el Paper.

Constantes del Paper (no redefinidas aquí como cuerpos ajenos):
  Cmax = 26/27
  β    = 1/27
  Cmax + β = 1
"""

from typing import List, Dict, Any

CUERPO = {
    "nombre": "siete_capas_SL_AX",
    "version": "1.0",
}


def declaraciones() -> List[Dict[str, Any]]:
    return [

        # ==========================================================
        # DEFINITIONS (Paper §3, Definition 1–10)
        # ==========================================================

        # Paper Definition 1 (System)
        {
            "id": "SL-D1",
            "tipo": "definicion",
            "sujeto": "S",
            "relacion": "es_tupla_ordenada",
            "objeto": "(R, M, P, T, D, I, Q)",
            "polaridad": True,
            "cota": None,
            "depende_de": [],
            "gobierna": ["ontologia", "meta"],
            "enunciado": (
                "Definition 1 (System). A system S is an ordered tuple "
                "S = (R, M, P, T, D, I, Q) where R is the reality field, "
                "M is matter, P is programming, T is processing, D is "
                "direction, I is interference, and Q is purpose. Each "
                "component is non-empty and depends functionally on all "
                "preceding components."
            ),
        },

        # Paper Definition 2 (Reality)
        {
            "id": "SL-D2",
            "tipo": "definicion",
            "sujeto": "R",
            "relacion": "es_campo_absoluto_contenedor_de",
            "objeto": "todo_sistema_S",
            "polaridad": True,
            "cota": None,
            "depende_de": ["SL-D1"],
            "gobierna": ["realidad", "ontologia"],
            "enunciado": (
                "Definition 2 (Reality). R is the absolute field within which "
                "every system exists. R does not depend on S; rather, S depends "
                "on R. For every system S, we have S ⊂ R. Reality is a necessary "
                "precondition and is not a layer of the system but its container."
            ),
        },

        # Paper Definition 3 (Matter — Layer 1)
        {
            "id": "SL-D3",
            "tipo": "definicion",
            "sujeto": "M",
            "relacion": "da_forma_y_existencia_observable_a",
            "objeto": "S_dentro_de_R",
            "polaridad": True,
            "cota": None,
            "depende_de": ["SL-D1", "SL-D2"],
            "gobierna": ["ontologia"],
            "enunciado": (
                "Definition 3 (Matter — Layer 1). M is the structural composition "
                "that gives observable form and existence to S within R. M determines "
                "the boundaries, properties, and capacities of S. We write M : S → F, "
                "where F is the space of admissible forms within R. If M = ∅, then S = ∅."
            ),
        },

        # Paper Definition 4 (Programming — Layer 2)
        {
            "id": "SL-D4",
            "tipo": "definicion",
            "sujeto": "P",
            "relacion": "determina_correlacion_e_interdependencia_en",
            "objeto": "elementos_de_M",
            "polaridad": True,
            "cota": None,
            "depende_de": ["SL-D3"],
            "gobierna": ["ontologia", "informacion"],
            "enunciado": (
                "Definition 4 (Programming — Layer 2). P is the set of rules, laws, "
                "or patterns that determine correlation and interdependence among the "
                "elements of M. We write P : M × M → C, where C is the space of "
                "correlations. P requires no conscious author; it is inherent to the "
                "structure. If M ≠ ∅ and |M| ≥ 2 with relational elements, then P ≠ ∅."
            ),
        },

        # Paper Definition 5 (Processing — Layer 3)
        {
            "id": "SL-D5",
            "tipo": "definicion",
            "sujeto": "T",
            "relacion": "transforma_continuamente",
            "objeto": "entradas_en_salidas_para_mantener_estado_funcional_de_S",
            "polaridad": True,
            "cota": None,
            "depende_de": ["SL-D4"],
            "gobierna": ["ontologia", "informacion"],
            "enunciado": (
                "Definition 5 (Processing — Layer 3). T is the continuous transformation "
                "function that converts inputs into outputs to maintain the functional "
                "state of S. We write T : E × P → O, where E is the input space and O "
                "is the output space. T operates on the rules of P applied to the form M. "
                "If T = 0, then S disintegrates."
            ),
        },

        # Paper Definition 6 (Direction — Layer 4)
        {
            "id": "SL-D6",
            "tipo": "definicion",
            "sujeto": "D",
            "relacion": "es_trayectoria_resultante_de",
            "objeto": "P_ejecutado_a_traves_de_T_en_el_tiempo",
            "polaridad": True,
            "cota": None,
            "depende_de": ["SL-D4", "SL-D5"],
            "gobierna": ["ontologia", "temporal"],
            "enunciado": (
                "Definition 6 (Direction — Layer 4). D is the trajectory resulting from "
                "P executing through T over time: "
                "D = lim_{t→∞} ∫_0^t T(P(s)) ds. "
                "D is not intention; it is a structural consequence. D exists for every "
                "S with P ≠ ∅ and T ≠ 0."
            ),
        },

        # Paper Definition 7 (Interference — Layer 5)
        {
            "id": "SL-D7",
            "tipo": "definicion",
            "sujeto": "I",
            "relacion": "es_funcion_de_influencia_de",
            "objeto": "S_sobre_otros_sistemas_y_sobre_si_mismo",
            "polaridad": True,
            "cota": None,
            "depende_de": ["SL-D1", "SL-D2"],
            "gobierna": ["ontologia", "informacion"],
            "enunciado": (
                "Definition 7 (Interference — Layer 5). I is the influence function that "
                "S exerts on other systems Sj and on itself: "
                "I : S × {S1, S2, …, Sn} → Δ, "
                "where Δ is the space of alterations in the field R. No system operates "
                "in absolute isolation: for every S ∈ R, there exists Sj ∈ R such that "
                "I(S, Sj) ≠ 0."
            ),
        },

        # Paper Definition 8 (Purpose — Layer 6)
        {
            "id": "SL-D8",
            "tipo": "definicion",
            "sujeto": "Q",
            "relacion": "es_resultado_funcional_emergente_de",
            "objeto": "operacion_integrada_de_capas_1_a_5",
            "polaridad": True,
            "cota": None,
            "depende_de": ["SL-D3", "SL-D4", "SL-D5", "SL-D6", "SL-D7"],
            "gobierna": ["ontologia", "meta"],
            "enunciado": (
                "Definition 8 (Purpose — Layer 6). Q is the emergent functional result "
                "of the integrated operation of Layers 1–5: Q = f(M, P, T, D, I). "
                "Q requires no consciousness. Q is not assigned externally; it emerges "
                "from the structure. Even the apparent absence of purpose is itself a "
                "purpose: for every S, Q(S) ≠ ∅."
            ),
        },

        # Paper Definition 9 (Continuous Integration Measure)
        {
            "id": "SL-D9",
            "tipo": "definicion",
            "sujeto": "Omega_c",
            "relacion": "es_producto_de_salud_de_capas",
            "objeto": "s1*s2*s3*s4*s5*s6",
            "polaridad": True,
            "cota": "26/27",
            "depende_de": ["SL-D1"],
            "gobierna": ["constantes", "meta", "ontologia"],
            "enunciado": (
                "Definition 9 (Continuous Integration Measure). For a system S whose "
                "layers have health values si ∈ [0, 1] for i = 1, …, 6, the continuous "
                "integration measure is Ωc(S) = ∏_{i=1}^{6} si. "
                "The maximum attainable value of Ωc for a living system is "
                "Cmax = 26/27. A system with Ωc = 1 is closed and dead. "
                "The effective system state is "
                "Seff = β + Ωc · Cmax, "
                "where β = 1/27 is always present as irreducible potential regardless "
                "of layer health."
            ),
        },

        # Paper Definition 10 (Binary Integration Invariant)
        {
            "id": "SL-D10",
            "tipo": "definicion",
            "sujeto": "Omega",
            "relacion": "vale_1_si_y_solo_si",
            "objeto": "todas_las_capas_estan_activas",
            "polaridad": True,
            "cota": None,
            "depende_de": ["SL-D1", "SL-D9"],
            "gobierna": ["ontologia", "logica"],
            "enunciado": (
                "Definition 10 (Binary Integration Invariant). A system S is integrated "
                "if and only if all its layers are active. We define "
                "Ω(S) = ∏_{i=1}^{6} θ(Li), "
                "where θ(Li) = 1 if layer Li is active, and θ(Li) = 0 if layer Li fails. "
                "Ω(S) = 1 if and only if all layers are active. Ω(S) = 0 implies S ceases "
                "to be a system. Even when Ω(S) = 1, the system operates at most at "
                "Cmax = 26/27, never at 1."
            ),
        },

        # ==========================================================
        # AXIOMS (Paper §4, Axiom 1–7)
        # ==========================================================

        # Paper Axiom 1 (Containment)
        {
            "id": "SL-A1",
            "tipo": "axioma",
            "sujeto": "S",
            "relacion": "existe_dentro_de",
            "objeto": "R",
            "polaridad": True,
            "cota": None,
            "depende_de": ["SL-D1", "SL-D2"],
            "gobierna": ["realidad", "ontologia"],
            "enunciado": (
                "Axiom 1 (Containment). Every system S exists within reality R: "
                "∀S : S ⊂ R."
            ),
        },

        # Paper Axiom 2 (Materiality)
        {
            "id": "SL-A2",
            "tipo": "axioma",
            "sujeto": "S",
            "relacion": "no_vacio_implica",
            "objeto": "M(S) ≠ ∅",
            "polaridad": True,
            "cota": None,
            "depende_de": ["SL-D3"],
            "gobierna": ["ontologia"],
            "enunciado": (
                "Axiom 2 (Materiality). No system exists without form: "
                "S ≠ ∅ ⇒ M(S) ≠ ∅."
            ),
        },

        # Paper Axiom 3 (Inherent Encoding)
        {
            "id": "SL-A3",
            "tipo": "axioma",
            "sujeto": "M",
            "relacion": "con_elementos_interdependientes_implica",
            "objeto": "P ≠ ∅",
            "polaridad": True,
            "cota": None,
            "depende_de": ["SL-D4"],
            "gobierna": ["ontologia", "informacion"],
            "enunciado": (
                "Axiom 3 (Inherent Encoding). All matter with interdependent elements "
                "carries programming: |M| ≥ 2 with relational elements ⇒ P ≠ ∅."
            ),
        },

        # Paper Axiom 4 (Activity)
        {
            "id": "SL-A4",
            "tipo": "axioma",
            "sujeto": "Omega(S) = 1",
            "relacion": "implica",
            "objeto": "T(S) ≠ 0",
            "polaridad": True,
            "cota": None,
            "depende_de": ["SL-D5", "SL-D10"],
            "gobierna": ["ontologia"],
            "enunciado": (
                "Axiom 4 (Activity). Every system processes to persist: "
                "Ω(S) = 1 ⇒ T(S) ≠ 0."
            ),
        },

        # Paper Axiom 5 (Consequence)
        {
            "id": "SL-A5",
            "tipo": "axioma",
            "sujeto": "P ≠ ∅ ∧ T ≠ 0",
            "relacion": "implica",
            "objeto": "D_existe",
            "polaridad": True,
            "cota": None,
            "depende_de": ["SL-D6"],
            "gobierna": ["ontologia", "temporal"],
            "enunciado": (
                "Axiom 5 (Consequence). All programming executed over time produces "
                "direction: P ≠ ∅ ∧ T ≠ 0 ⇒ D exists."
            ),
        },

        # Paper Axiom 6 (Non-Isolation)
        {
            "id": "SL-A6",
            "tipo": "axioma",
            "sujeto": "S",
            "relacion": "tiene_interaccion_no_nula_con",
            "objeto": "algun_Sj_o_consigo_mismo",
            "polaridad": True,
            "cota": None,
            "depende_de": ["SL-D7"],
            "gobierna": ["ontologia", "informacion"],
            "enunciado": (
                "Axiom 6 (Non-Isolation). No system exists without interaction with at "
                "least one other system or with itself: "
                "∀S ∈ R, ∃Sj : I(S, Sj) ≠ 0."
            ),
        },

        # Paper Axiom 7 (Emergence)
        {
            "id": "SL-A7",
            "tipo": "axioma",
            "sujeto": "M≠∅ ∧ P≠∅ ∧ T≠0 ∧ D_existe ∧ I≠0",
            "relacion": "implica",
            "objeto": "Q ≠ ∅",
            "polaridad": True,
            "cota": None,
            "depende_de": ["SL-D8"],
            "gobierna": ["ontologia", "meta"],
            "enunciado": (
                "Axiom 7 (Emergence). The integrated operation of Layers 1–5 produces "
                "purpose: "
                "M ≠ ∅ ∧ P ≠ ∅ ∧ T ≠ 0 ∧ D exists ∧ I ≠ 0 ⇒ Q ≠ ∅."
            ),
        },

        # ==========================================================
        # MAIN THEOREM (Paper §5, Theorem 11)
        # ==========================================================

        # Paper Theorem 11 (Seven-Layer Theorem)
        {
            "id": "SL-T11",
            "tipo": "teorema",
            "sujeto": "S",
            "relacion": "es_sistema_si_y_solo_si",
            "objeto": "S_subset_R_y_Omega(S)=1_con_Omega_c_leq_Cmax",
            "polaridad": True,
            "cota": "26/27",
            "depende_de": [
                "SL-A1", "SL-A2", "SL-A3", "SL-A4", "SL-A5", "SL-A6", "SL-A7",
                "SL-D1", "SL-D9", "SL-D10",
            ],
            "gobierna": ["ontologia", "constantes", "meta", "logica"],
            "enunciado": (
                "Theorem 11 (Seven-Layer Theorem). Every system S that exists within "
                "reality R is composed of exactly six functional layers {M, P, T, D, I, Q} "
                "operating within a containing field R, and S is a system if and only if "
                "the integration of all its layers is maintained. Formally: "
                "S is a system ⇔ S ⊂ R ∧ Ω(S) = 1, "
                "where "
                "Ω(S) = 1 ⇔ M ≠ ∅ ∧ P ≠ ∅ ∧ T ≠ 0 ∧ D exists ∧ I ≠ 0 ∧ Q ≠ ∅. "
                "Moreover, even at maximum integration (Ω(S) = 1), the effective "
                "coherence of the system is bounded: "
                "Ωc(S) ≤ Cmax = 26/27 < 1."
            ),
        },

        # ==========================================================
        # COROLLARIES (Paper §6, Corollary 12–18)
        # ==========================================================

        # Paper Corollary 12 (Universality)
        {
            "id": "SL-C12",
            "tipo": "corolario",
            "sujeto": "Theorem_11",
            "relacion": "aplica_a_todo_sistema_sin_restriccion_de",
            "objeto": "escala_naturaleza_o_complejidad",
            "polaridad": True,
            "cota": None,
            "depende_de": ["SL-T11"],
            "gobierna": ["ontologia", "meta"],
            "enunciado": (
                "Corollary 12 (Universality). The theorem applies to every system "
                "without restriction of scale, nature, or complexity."
            ),
        },

        # Paper Corollary 13 (Sequential Dependence)
        {
            "id": "SL-C13",
            "tipo": "corolario",
            "sujeto": "capas",
            "relacion": "forman_cadena_de_dependencia",
            "objeto": "M→P→T→D→I→Q",
            "polaridad": True,
            "cota": None,
            "depende_de": ["SL-A2", "SL-A3", "SL-A4", "SL-A5", "SL-A6", "SL-A7", "SL-T11"],
            "gobierna": ["ontologia", "logica"],
            "enunciado": (
                "Corollary 13 (Sequential Dependence). The layers form a dependence "
                "chain: M → P → T → D → I → Q. Each layer requires the existence of "
                "all preceding layers."
            ),
        },

        # Paper Corollary 14 (Irreducibility)
        {
            "id": "SL-C14",
            "tipo": "corolario",
            "sujeto": "ninguna_capa",
            "relacion": "puede_eliminarse_sin",
            "objeto": "destruir_el_sistema",
            "polaridad": True,
            "cota": None,
            "depende_de": ["SL-T11"],
            "gobierna": ["ontologia"],
            "enunciado": (
                "Corollary 14 (Irreducibility). No layer can be eliminated without "
                "destroying the system."
            ),
        },

        # Paper Corollary 15 (Non-Fragmentation)
        {
            "id": "SL-C15",
            "tipo": "corolario",
            "sujeto": "S",
            "relacion": "es_sistema_si_y_solo_si",
            "objeto": "opera_como_unidad_integrada",
            "polaridad": True,
            "cota": None,
            "depende_de": ["SL-T11", "SL-D10"],
            "gobierna": ["ontologia", "logica"],
            "enunciado": (
                "Corollary 15 (Non-Fragmentation). A system is a system if and only if "
                "it operates as an integrated unit: Ω(S) = 0 ⇔ S is not a system."
            ),
        },

        # Paper Corollary 16 (Emergent Purpose)
        {
            "id": "SL-C16",
            "tipo": "corolario",
            "sujeto": "Q",
            "relacion": "emerge_de",
            "objeto": "integracion_de_capas_1_a_5",
            "polaridad": True,
            "cota": None,
            "depende_de": ["SL-A7", "SL-D8", "SL-T11"],
            "gobierna": ["ontologia", "meta"],
            "enunciado": (
                "Corollary 16 (Emergent Purpose). Purpose emerges from the integration "
                "of Layers 1–5. No system lacks functional purpose."
            ),
        },

        # Paper Corollary 17 (Mutual Containment)
        {
            "id": "SL-C17",
            "tipo": "corolario",
            "sujeto": "S",
            "relacion": "es_subsistema_y_contiene_subsistemas_dentro_de",
            "objeto": "R",
            "polaridad": True,
            "cota": None,
            "depende_de": ["SL-A6", "SL-A2", "SL-T11"],
            "gobierna": ["ontologia"],
            "enunciado": (
                "Corollary 17 (Mutual Containment). Within R, every system is a "
                "subsystem of at least one larger system, and contains at least one "
                "subsystem."
            ),
        },

        # Paper Corollary 18 (Bounded Integration Law)
        {
            "id": "SL-C18",
            "tipo": "corolario",
            "sujeto": "Omega_c",
            "relacion": "esta_estrictamente_acotado_por",
            "objeto": "Cmax = 26/27",
            "polaridad": True,
            "cota": "26/27",
            "depende_de": ["SL-T11", "SL-A6", "SL-D9"],
            "gobierna": ["constantes", "ontologia", "meta"],
            "enunciado": (
                "Corollary 18 (Bounded Integration Law). No system can achieve total "
                "integration. The maximum observable coherence is strictly bounded: "
                "Ωc(S) ≤ Cmax = 26/27 ≈ 0.963 "
                "with irreducible potential β = 1/27 ≈ 0.037 always present. "
                "The bound is tight: it is the condition that separates a living "
                "(open, adaptive, dynamic) system from a dead (closed, static, frozen) one."
            ),
        },
    ]


__all__ = ["CUERPO", "declaraciones"]
