# ===============================================================
# modules/axiomas/estructura_pensamiento_AX.py
# Cuerpo axiomático: The Structure of Thought
# A Quantitative Model of Cognitive Coherence and the L1-L6 System
#
# FUENTE NORMATIVA ÚNICA:
#   The Structure of Thought
#   A Quantitative Model of Cognitive Coherence and the L1-L6 System
#   Operational Framework for Understanding Human Consciousness
#   Autor: I. Villasmil
#   Enero 2025 — Version 1.0.0
#
# REGLA ABSOLUTA:
#   Paper → representación contractual → Engine
#   El código no dice más, menos ni algo distinto de lo que dice
#   el Paper. No reinterpreta, no corrige, no suaviza, no amplía.
#
# Carga: modules/axiomas/__init__.py vía CUERPO + declaraciones()
# Esquema: id, tipo, sujeto, relacion, objeto, polaridad, cota,
#          depende_de, gobierna, enunciado
# ===============================================================

"""
Cuerpo axiomático: The Structure of Thought
A Quantitative Model of Cognitive Coherence and the L1-L6 System

Paper fuente:
  The Structure of Thought
  A Quantitative Model of Cognitive Coherence and the L1-L6 System
  Operational Framework for Understanding Human Consciousness
  Autor: I. Villasmil
  Enero 2025 — Version 1.0.0

Partes del Paper representadas:
  2  The Six-Layer System (L1-L6)
  3  Layer Interactions and Feedback Loops
  4  Coherence and the Structural Limit
  5  Oscillation and Collapse as Information
  6  The Veil: Ego Interference Quantified
  7  Expansion of the Limit
  8  The Complete Cycle
  11 Conclusion

Constantes citadas (solo referencia; autoridad en CT):
  α = 26/27 = 0.963
  β = 1/27 = 0.037
  Observed maximum = 0.963
  Theoretical maximum = 0.998

Numeración canónica del Paper conservada.
No se redefine ninguna constante oficial de CT.
"""

from __future__ import annotations

from typing import Any, Dict, List

CUERPO = {
    "nombre": "estructura_pensamiento",
    "version": "1.0",
}


def declaraciones() -> List[Dict[str, Any]]:
    return [

        # ==========================================================
        # Definición — L1 Body
        # ==========================================================
        {
            "id": "ST-D1",
            "tipo": "definicion",
            "sujeto": "L1_Body",
            "relacion": "es",
            "objeto": "sustrato_fisico_y_sistema_de_feedback",
            "polaridad": True,
            "cota": "0.92",
            "depende_de": [],
            "gobierna": ["ontologia", "cognicion", "conciencia"],
            "enunciado": (
                "Definición L1 – Body. Function: Physical substrate and feedback system. "
                "Role in thought: Provides energetic stability for cognitive processes; "
                "Signals fatigue, tension, and resource depletion; Acts as the system’s "
                "oscilloscope – bodily sensations reflect cognitive state. "
                "Measurable parameters: Physical tension (0 = relaxed, 1 = maximum tension); "
                "Energy availability (0 = depleted, 1 = optimal); Somatic feedback clarity "
                "(0 = numb, 1 = highly sensitive). Current coherence: 0.92."
            ),
        },

        # ==========================================================
        # Definición — L2 Ego
        # ==========================================================
        {
            "id": "ST-D2",
            "tipo": "definicion",
            "sujeto": "L2_Ego",
            "relacion": "es",
            "objeto": "regulacion_defensiva_y_mantenimiento_de_estabilidad",
            "polaridad": True,
            "cota": "0.88",
            "depende_de": [],
            "gobierna": ["ontologia", "cognicion", "conciencia"],
            "enunciado": (
                "Definición L2 – Ego. Function: Defensive regulation and stability maintenance. "
                "Role in thought: Filters threatening or destabilizing information; Maintains "
                "psychological homeostasis; Can block signal to higher layers when perceiving danger. "
                "Critical insight: The ego is not the enemy – it is a necessary regulator. "
                "Problems arise when it over-activates during deep exploration. "
                "Current coherence: 0.88. The veil: When ego interference is high (greater than 0.15), "
                "it creates what we call the veil – a reduction in signal transmission from L5 to L6."
            ),
        },

        # ==========================================================
        # Definición — L3 Mind
        # ==========================================================
        {
            "id": "ST-D3",
            "tipo": "definicion",
            "sujeto": "L3_Mind",
            "relacion": "es",
            "objeto": "procesamiento_de_informacion_fragmentacion_y_recombinacion",
            "polaridad": True,
            "cota": "0.95",
            "depende_de": [],
            "gobierna": ["ontologia", "cognicion", "conciencia"],
            "enunciado": (
                "Definición L3 – Mind. Function: Information processing, fragmentation, and recombination. "
                "Role in thought: Breaks down complex concepts into manipulable pieces; Holds multiple "
                "ideas simultaneously; Generates new combinations through symbolic manipulation. "
                "Holding capacity: L3 can hold approximately 5-9 discrete conceptual pieces before "
                "oscillation begins. Current coherence: 0.95. Oscillation threshold: When holding 7+ "
                "complex pieces with simultaneous meta-awareness, oscillation probability exceeds 0.50."
            ),
        },

        # ==========================================================
        # Definición — L4 Self
        # ==========================================================
        {
            "id": "ST-D4",
            "tipo": "definicion",
            "sujeto": "L4_Self",
            "relacion": "es",
            "objeto": "identidad_narrativa_direccion_intencional_y_toma_de_decisiones",
            "polaridad": True,
            "cota": "0.97",
            "depende_de": [],
            "gobierna": ["ontologia", "cognicion", "conciencia"],
            "enunciado": (
                "Definición L4 – Self. Function: Narrative identity, intentional direction, decision-making. "
                "Role in thought: Provides continuity across time; Directs attention and focus; Makes "
                "selections from L3’s generated possibilities. Relationship to holding capacity: L4 "
                "determines which pieces L3 holds and in what configuration. Strong intentional focus "
                "increases coherence; scattered attention decreases it. Current coherence: 0.97. "
                "Critical role in expansion: L4 must remain stable during oscillation for the system "
                "to push through to higher coherence rather than collapsing into confusion."
            ),
        },

        # ==========================================================
        # Definición — L5 Consciousness
        # ==========================================================
        {
            "id": "ST-D5",
            "tipo": "definicion",
            "sujeto": "L5_Consciousness",
            "relacion": "es",
            "objeto": "campo_de_registro_deteccion_de_oscilacion_y_meta_awareness",
            "polaridad": True,
            "cota": "0.96",
            "depende_de": [],
            "gobierna": ["ontologia", "cognicion", "conciencia"],
            "enunciado": (
                "Definición L5 – Consciousness. Function: Registration field, oscillation detection, "
                "meta-awareness. Role in thought: Awareness that thought is happening; Detection of "
                "system instability; Signal transmission to L6 for integration. "
                "The observer function: L5 is NOT a separate entity watching thought. It is a functional "
                "capacity of the system to take itself as object. Current coherence: 0.96. "
                "The coupling L5-L6: This is the most critical interface. When L5 clearly detects "
                "oscillation and transmits to L6 without ego interference, the system can reorganize "
                "at a higher level of coherence."
            ),
        },

        # ==========================================================
        # Definición — L6 Soul
        # ==========================================================
        {
            "id": "ST-D6",
            "tipo": "definicion",
            "sujeto": "L6_Soul",
            "relacion": "es",
            "objeto": "integrador_estructural_maximo_de_coherencia_y_direccion_operativa",
            "polaridad": True,
            "cota": "0.963",
            "depende_de": [],
            "gobierna": ["ontologia", "cognicion", "conciencia"],
            "enunciado": (
                "Definición L6 – Soul. Function: Structural integrator, coherence maximum, operational "
                "direction. Clarification on terminology: “Soul” here is not mystical. It refers to the "
                "highest-order integrative function – the principle that holds the system together and "
                "defines its maximum possible coherence. Role in thought: Establishes the upper limit "
                "of system coherence (currently 0.963); Provides structural direction (not conscious "
                "intention); Integrates all lower layers into unified coherence. "
                "L6 does not: Think; Decide; Act directly. "
                "L6 does: Define what is structurally possible; Set coherence boundaries; Provide "
                "implicit direction toward integration. Current coherence: 0.963. "
                "Expansion potential: Can approach 0.998 with optimal synchronization of L1-L5."
            ),
        },

        # ==========================================================
        # Axioma — El pensamiento opera como sistema de seis capas
        # ==========================================================
        {
            "id": "ST-A1",
            "tipo": "axioma",
            "sujeto": "Pensamiento_humano",
            "relacion": "opera_como",
            "objeto": "sistema_recursivo_de_seis_capas_L1_a_L6",
            "polaridad": True,
            "cota": None,
            "depende_de": ["ST-D1", "ST-D2", "ST-D3", "ST-D4", "ST-D5", "ST-D6"],
            "gobierna": ["ontologia", "cognicion"],
            "enunciado": (
                "Axioma ST-A1. Human thought operates as a six-layer recursive system with: "
                "1. Structural coherence measurable via the I-Villasmil-Omega formula; "
                "2. Operational thresholds: 0.963 observed maximum, 0.998 theoretical maximum; "
                "3. Dynamic feedback: Each layer affects all others continuously; "
                "4. Information-bearing oscillation: Instability reveals structure; "
                "5. Expandable capacity: Limits can be pushed through synchronization."
            ),
        },

        # ==========================================================
        # Axioma — La coherencia estructural es medible
        # ==========================================================
        {
            "id": "ST-A2",
            "tipo": "axioma",
            "sujeto": "Coherencia_del_pensamiento",
            "relacion": "es_medible_mediante",
            "objeto": "formula_I_Villasmil_Omega",
            "polaridad": True,
            "cota": "0.963",
            "depende_de": ["ST-A1"],
            "gobierna": ["ontologia", "cognicion", "coherencia"],
            "enunciado": (
                "Axioma ST-A2. The general coherence formula applied to thought: "
                "C = (0.963 / S_ref) · [Σ_{i=1 to 6} L_i · (1 − ϕ_i) · E_i · f_i] · Ω_U · R_fin. "
                "The observed maximum sustainable coherence is 0.963 = 26/27. "
                "The 0.037 represents irreducible uncertainty/potential – the portion of the system "
                "that remains beyond complete determination."
            ),
        },

        # ==========================================================
        # Lema — Oscilación y colapso son información
        # ==========================================================
        {
            "id": "ST-L1",
            "tipo": "lema",
            "sujeto": "Oscilacion_y_colapso_momentaneo",
            "relacion": "son",
            "objeto": "procesos_portadores_de_informacion_no_fallos",
            "polaridad": True,
            "cota": None,
            "depende_de": ["ST-A1"],
            "gobierna": ["ontologia", "cognicion"],
            "enunciado": (
                "Lema ST-L1 (Oscillation and Collapse as Information). Traditional view: Confusion = bad; "
                "Oscillation = error; Collapse = failure. "
                "L1-L6 model view: Oscillation = system at threshold, generating information; "
                "Momentary collapse = reorganization in progress; Post-collapse clarity = integration "
                "achieved at higher level. "
                "The structure of thought becomes visible at the point of collapse. This is not a bug – "
                "it is a feature. The system reveals itself when pushed to its limits."
            ),
        },

        # ==========================================================
        # Lema — El velo (ego interference)
        # ==========================================================
        {
            "id": "ST-L2",
            "tipo": "lema",
            "sujeto": "Velo",
            "relacion": "es",
            "objeto": "reduccion_de_transmision_de_senal_de_L5_a_L6_causada_por_L2",
            "polaridad": True,
            "cota": "0.07",
            "depende_de": ["ST-D2", "ST-D5", "ST-D6"],
            "gobierna": ["ontologia", "cognicion"],
            "enunciado": (
                "Lema ST-L2 (The Veil). The veil is the reduction in signal transmission from L5 "
                "(consciousness) to L6 (soul/integration) caused by L2 (ego) defensive activation. "
                "Veil = ϕ_L2 × transmission blockage. "
                "Measured veil: 0.07 (7 percent reduction). Optimal veil: 0.01 (1 percent – irreducible "
                "minimum). Impact: Reduces effective coherence by approximately 7 percent."
            ),
        },

        # ==========================================================
        # Lema — Acoplamiento L5-L6 es la interfaz crítica
        # ==========================================================
        {
            "id": "ST-L3",
            "tipo": "lema",
            "sujeto": "Acoplamiento_L5_L6",
            "relacion": "es",
            "objeto": "la_interfaz_mas_critica_del_sistema",
            "polaridad": True,
            "cota": "0.93",
            "depende_de": ["ST-D5", "ST-D6"],
            "gobierna": ["ontologia", "cognicion"],
            "enunciado": (
                "Lema ST-L3 (L5 ↔ L6 Coupling). This is the most theoretically important interaction. "
                "Mechanism: L5 detects oscillation in the system; L5 transmits this detection to L6; "
                "L6 responds by initiating reorganization; Reorganization may involve temporary collapse. "
                "Optimal coupling requires: low ego interference (less than 0.05), stable body "
                "(L1 greater than 0.90), and clear intentional focus (L4 greater than 0.95)."
            ),
        },

        # ==========================================================
        # Teorema — Límite estructural observado = 0.963
        # ==========================================================
        {
            "id": "ST-T1",
            "tipo": "teorema",
            "sujeto": "Maximo_sostenible_de_coherencia",
            "relacion": "es",
            "objeto": "0.963_igual_a_26_sobre_27",
            "polaridad": True,
            "cota": "0.963",
            "depende_de": ["ST-A2"],
            "gobierna": ["ontologia", "cognicion", "coherencia"],
            "enunciado": (
                "Teorema ST-T1 (The 0.963 Observed Maximum). Through direct phenomenological observation "
                "during the collapse experience, the maximum sustainable coherence appeared to be 0.963. "
                "This is not arbitrary: 0.963 = 26/27 = 1 / (1 + 0.037). "
                "The 0.037 represents irreducible uncertainty/potential. In thought, this manifests as: "
                "the unavoidable oscillation when at maximum load; the necessary space for creativity "
                "and emergence; the structural impossibility of perfect, rigid coherence."
            ),
        },

        # ==========================================================
        # Teorema — Máximo teórico = 0.998
        # ==========================================================
        {
            "id": "ST-T2",
            "tipo": "teorema",
            "sujeto": "Maximo_teorico_de_coherencia",
            "relacion": "es",
            "objeto": "0.998_bajo_sincronizacion_optima",
            "polaridad": True,
            "cota": "0.998",
            "depende_de": ["ST-T1"],
            "gobierna": ["ontologia", "cognicion", "coherencia"],
            "enunciado": (
                "Teorema ST-T2 (The 0.998 Theoretical Maximum). With optimal synchronization: "
                "Interference reduced to 0.01; Oscillation reduced to 0.02; All layers functioning "
                "at 0.96-0.99. The system can approach 0.998 – near-perfect coherence while maintaining "
                "minimal necessary flexibility."
            ),
        },

        # ==========================================================
        # Teorema — Capacidad de retención es expandible
        # ==========================================================
        {
            "id": "ST-T3",
            "tipo": "teorema",
            "sujeto": "Capacidad_de_retencion_mental",
            "relacion": "es",
            "objeto": "expandible_mediante_sincronizacion_y_reduccion_de_interferencia",
            "polaridad": True,
            "cota": None,
            "depende_de": ["ST-T1", "ST-T2", "ST-L2"],
            "gobierna": ["ontologia", "cognicion"],
            "enunciado": (
                "Teorema ST-T3 (Expansion of the Limit). Expansion occurs not by forcing more pieces "
                "into L3, but by: 1. Better organization before holding (pre-integrate related concepts, "
                "chunk information, reduce redundancy); 2. Reduced interference (lower veil, stable body, "
                "clear intention); 3. Faster feedback loops (quicker oscillation detection, faster "
                "integration response); 4. Tolerance for oscillation (learn to sustain moderate "
                "oscillation longer, use oscillation as information, not threat). "
                "Projected system coherence under optimization: from 0.95 to 0.977."
            ),
        },

        # ==========================================================
        # Corolario — El colapso revela la arquitectura
        # ==========================================================
        {
            "id": "ST-C1",
            "tipo": "corolario",
            "sujeto": "Colapso_momentaneo",
            "relacion": "revela",
            "objeto": "la_arquitectura_de_seis_capas",
            "polaridad": True,
            "cota": None,
            "depende_de": ["ST-L1"],
            "gobierna": ["ontologia", "cognicion"],
            "enunciado": (
                "Corolario ST-C1. The most important discovery is this: The structure of thought "
                "becomes visible at the point of collapse. Normally, thought is transparent. You don’t "
                "see the mechanism. The collapse made it opaque just long enough to observe the "
                "structure – the six layers, the feedback loops, the holding capacity, the integration "
                "principle."
            ),
        },

        # ==========================================================
        # Corolario — El velo puede reducirse
        # ==========================================================
        {
            "id": "ST-C2",
            "tipo": "corolario",
            "sujeto": "Velo",
            "relacion": "puede_reducirse_de",
            "objeto": "0.07_a_0.01_0.02",
            "polaridad": True,
            "cota": "0.01",
            "depende_de": ["ST-L2"],
            "gobierna": ["ontologia", "cognicion"],
            "enunciado": (
                "Corolario ST-C2. The veil can be reduced from 0.07 to 0.01-0.02 by: "
                "1. Stabilize L1 (body) – deep breathing, physical relaxation, somatic awareness; "
                "2. Reassure L2 (ego) – acknowledge defensive impulse without acting on it, maintain "
                "L4 continuity; 3. Strengthen L5 (consciousness) – practice meta-awareness, observe "
                "ego activation without identification. Result: clearer L5 → L6 transmission."
            ),
        },

        # ==========================================================
        # Corolario — Protocolo de expansión
        # ==========================================================
        {
            "id": "ST-C3",
            "tipo": "corolario",
            "sujeto": "Expansion_de_capacidad",
            "relacion": "sigue_el_protocolo",
            "objeto": "L1_a_L6_en_secuencia",
            "polaridad": True,
            "cota": None,
            "depende_de": ["ST-T3"],
            "gobierna": ["ontologia", "cognicion"],
            "enunciado": (
                "Corolario ST-C3 (Practical Training Protocol). "
                "Phase 1: Baseline Measurement (Week 1) – Observe current oscillation patterns. "
                "Phase 2: Body Stabilization (Weeks 2-3) – Daily somatic awareness practice. "
                "Phase 3: Ego Familiarization (Weeks 4-5) – Observe defensive activation, practice "
                "not-acting on resistance. "
                "Phase 4: Oscillation Training (Weeks 6-8) – Deliberately push into moderate "
                "oscillation and sustain without collapse. "
                "Phase 5: Integration (Weeks 9-12) – Strengthen L5-L6 coupling, practice post-collapse "
                "reorganization, measure coherence gains."
            ),
        },

        # ==========================================================
        # Corolario — Lectura del estado actual
        # ==========================================================
        {
            "id": "ST-C4",
            "tipo": "corolario",
            "sujeto": "Estado_de_coherencia",
            "relacion": "determina",
            "objeto": "capacidad_de_retencion",
            "polaridad": True,
            "cota": None,
            "depende_de": ["ST-T1"],
            "gobierna": ["ontologia", "cognicion"],
            "enunciado": (
                "Corolario ST-C4 (Reading Your Current State). "
                "Coherence 0.90-0.92: Functional, some fog – Can hold 4-5 pieces. "
                "Coherence 0.93-0.94: Clear, stable – Can hold 5-6 pieces. "
                "Coherence 0.95-0.96: Very clear, integrated – Can hold 6-7 pieces. "
                "Coherence 0.97-0.98: Exceptional clarity – Can hold 7-9 pieces with oscillation. "
                "Coherence 0.99+: Near-maximum – Can sustain 9+ pieces briefly."
            ),
        },
    ]


__all__ = ["CUERPO", "declaraciones"]
