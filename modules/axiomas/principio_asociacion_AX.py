# ===============================================================
# modules/axiomas/principio_asociacion_AX.py
# Cuerpo axiomático: Principio de Asociación — v1.2.1
# Formalización matemática temática
#
# CORRECCIÓN:
#   Eliminados IDs duplicados (PA-A1…PA-A5).
#   44 declaraciones, 44 IDs únicos.
#   theta_n coherente con universo operativo.
#
# REGLA ABSOLUTA:
#   PAPER → FORMALIZACIÓN → DEPENDENCIAS → DEMOSTRACIÓN → CONTRATO → ENGINE
#   M(B)=1 ⇒ ◇M
#   NUNCA: M(B) ⇒ M(A)
#
# BASE FORMAL (sin redefinir):
#   R_i = C · L · K ;  R_i ⊂ R ;  R → X → Y
#   L4 = Yo/elección ; L5 = Consciencia/obs ; L6 = Alma/dirección
# ===============================================================

"""
Cuerpo axiomático: Principio de Asociación — v1.2.1

Estructura:
  Definiciones  : 10  (PA-D1  … PA-D10)
  Axiomas       : 10  (PA-A1  … PA-A10)
  Lemas         :  9  (PA-L1  … PA-L9)
  Teoremas      :  7  (PA-T1  … PA-T7)
  Corolarios    :  8  (PA-C1  … PA-C8)
  Total         : 44  (IDs únicos, sin duplicados)
"""

from __future__ import annotations

from typing import Any, Dict, List

CUERPO = {
    "nombre": "principio_asociacion",
    "version": "1.2.1",
}


def declaraciones() -> List[Dict[str, Any]]:
    return [

        # ── DEFINICIONES ──────────────────────────────────────────

        {
            "id": "PA-D1",
            "tipo": "definicion",
            "sujeto": "Principio_de_Asociacion",
            "relacion": "establece_que",
            "objeto": "si_existe_creencia_de_imposibilidad_se_introduce_contexto_alternativo_real",
            "polaridad": True,
            "cota": None,
            "depende_de": [],
            "gobierna": ["ontologia", "epistemologia", "desbloqueo"],
            "enunciado": (
                "Definición PA-D1 (Principio de Asociación). "
                "Sea A un contexto donde R_i sostiene la premisa P_¬M := “M es imposible”. "
                "Sea B un contexto real donde M(B)=1. "
                "El Principio de Asociación establece la operación 𝒜(A,B,M) por la cual "
                "R_i introduce B como evidencia, forzando la actualización: P_¬M → P_◇M. "
                "Formalmente: M(B)=1 ⇒ ◇M. "
                "Documento: si pasa allá, la mecánica existe; si la mecánica existe, puede pasar aquí. "
                "Nota: “puede” ≡ ◇M, no ≡ M(A)."
            ),
        },
        {
            "id": "PA-D2",
            "tipo": "definicion",
            "sujeto": "Contexto_A_Bloqueado",
            "relacion": "es",
            "objeto": "contexto_donde_existe_la_premisa_esto_es_imposible",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PA-D1"],
            "gobierna": ["ontologia", "desbloqueo"],
            "enunciado": (
                "Definición PA-D2 (Contexto A – Bloqueo). "
                "A := contexto en el que R_i sostiene P_¬M. "
                "Dominio donde opera la limitación aceptada por la mente de R_i."
            ),
        },
        {
            "id": "PA-D3",
            "tipo": "definicion",
            "sujeto": "Contexto_B_Evidencial",
            "relacion": "es",
            "objeto": "contexto_real_donde_el_fenomeno_o_mecanismo_ya_ocurre_de_manera_verificable",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PA-D1"],
            "gobierna": ["ontologia", "desbloqueo"],
            "enunciado": (
                "Definición PA-D3 (Contexto B – Evidencia). "
                "B := contexto real tal que M(B)=1 de manera verificable. "
                "B constituye el puente de evidencia para 𝒜(A,B,M)."
            ),
        },
        {
            "id": "PA-D4",
            "tipo": "definicion",
            "sujeto": "Mecanica_Especifica_Transferible",
            "relacion": "es",
            "objeto": "mecanica_concreta_aislable_del_contexto_B",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PA-D3"],
            "gobierna": ["ontologia", "desbloqueo"],
            "enunciado": (
                "Definición PA-D4 (Mecánica Transferible). "
                "M es la mecánica concreta que existe en B y que puede aislarse: "
                "B ─aislamiento→ M. "
                "Formalmente: Transfer(M) ∧ ¬Transfer(Contexto_B_completo)."
            ),
        },
        {
            "id": "PA-D5",
            "tipo": "definicion",
            "sujeto": "Bloqueo_Estructural",
            "relacion": "es",
            "objeto": "estado_producido_cuando_premisa_de_imposibilidad_es_aceptada_como_regla_absoluta",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PA-D2"],
            "gobierna": ["ontologia", "desbloqueo"],
            "enunciado": (
                "Definición PA-D5 (Bloqueo Estructural). "
                "Sea B_i el estado interno de bloqueo de R_i. "
                "B_i se produce cuando P_¬M es aceptada como regla absoluta y la mente de R_i "
                "cierra vías de procesamiento incompatibles con P_¬M. "
                "Formalmente: P_¬M → B_i."
            ),
        },
        {
            "id": "PA-D6",
            "tipo": "definicion",
            "sujeto": "Actualizacion_Estructural",
            "relacion": "es",
            "objeto": "proceso_mediante_el_cual_la_mente_modifica_la_regla_previamente_aceptada",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PA-D5", "PA-D3"],
            "gobierna": ["ontologia", "desbloqueo"],
            "enunciado": (
                "Definición PA-D6 (Actualización Estructural). "
                "Sea S_i^(0) el estado representacional de R_i que contiene P_¬M. "
                "Tras evidencia M(B)=1: S_i^(0) → S_i^(1) donde S_i^(1) contiene P_◇M. "
                "Transición documental: “Es imposible” → “Es posible bajo ciertas condiciones”. "
                "R permanece invariante. Solo cambia el estado de R_i."
            ),
        },
        {
            "id": "PA-D7",
            "tipo": "definicion",
            "sujeto": "Distancia_Observador_Objeto",
            "relacion": "es",
            "objeto": "separacion_funcional_entre_quien_observa_y_aquello_que_es_observado",
            "polaridad": True,
            "cota": None,
            "depende_de": [],
            "gobierna": ["ontologia", "epistemologia", "observacion"],
            "enunciado": (
                "Definición PA-D7 (Distancia Observador-Objeto). "
                "δ_i(O) representa la separación funcional entre R_i y el objeto O. "
                "δ_i(O) > 0 := separación funcional (posición observacional). "
                "δ_i(O) = 0 := fusión funcional (identificación). "
                "δ_i no es distancia espacial ni métrica física; es relación funcional."
            ),
        },
        {
            "id": "PA-D8",
            "tipo": "definicion",
            "sujeto": "Identificacion",
            "relacion": "es",
            "objeto": "estado_en_el_que_el_observador_se_encuentra_fusionado_con_el_patron_observado",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PA-D7"],
            "gobierna": ["ontologia", "observacion"],
            "enunciado": (
                "Definición PA-D8 (Identificación). "
                "Identificacion_i(O) := estado en el que R_i se encuentra fusionado con el patrón O. "
                "Formalmente: Identificacion_i(O) ⇒ δ_i(O) = 0. "
                "Ejemplo del documento: “Yo soy la angustia”."
            ),
        },
        {
            "id": "PA-D9",
            "tipo": "definicion",
            "sujeto": "Observacion_Interna_L5",
            "relacion": "es",
            "objeto": "funcion_de_la_consciencia_de_observar_el_proceso_interno_con_neutralidad",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PA-D7", "ST-D5"],
            "gobierna": ["ontologia", "observacion", "conciencia"],
            "enunciado": (
                "Definición PA-D9 (Función de Observación Interna – L5). "
                "L5(R_i) = Obs(R_i). "
                "ObsInterna_i(O) := observar el proceso interno O con la misma neutralidad "
                "con la que se observa un proceso externo. "
                "Vinculada explícitamente con L5. No se redefine L5."
            ),
        },
        {
            "id": "PA-D10",
            "tipo": "definicion",
            "sujeto": "Arco_del_trabajo_interior",
            "relacion": "es",
            "objeto": "Identificado_luego_Espectador_luego_Director",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PA-D8", "PA-D9"],
            "gobierna": ["ontologia", "observacion", "direccion"],
            "enunciado": (
                "Definición PA-D10 (Arco del trabajo interior). "
                "I_i := Identificado (R_i es el patrón). "
                "E_i := Espectador (R_i ve el patrón; función de L5). "
                "D_i := Director (R_i orienta; función de L4 integrada por L6). "
                "Secuencia documental: I_i → E_i → D_i. "
                "El orden no se puede saltar. Transición I_i → D_i no es legítima."
            ),
        },

        # ── AXIOMAS ───────────────────────────────────────────────

        {
            "id": "PA-A1",
            "tipo": "axioma",
            "sujeto": "Mente",
            "relacion": "busca",
            "objeto": "coherencia",
            "polaridad": True,
            "cota": None,
            "depende_de": [],
            "gobierna": ["ontologia", "mente"],
            "enunciado": (
                "Axioma PA-A1 (La mente busca coherencia). "
                "La mente de R_i opera como estructura de orden y busca construir "
                "una realidad coherente a partir de sus premisas."
            ),
        },
        {
            "id": "PA-A2",
            "tipo": "axioma",
            "sujeto": "Ego",
            "relacion": "puede_imponer",
            "objeto": "premisa_absoluta_de_imposibilidad",
            "polaridad": True,
            "cota": None,
            "depende_de": [],
            "gobierna": ["ontologia", "ego"],
            "enunciado": (
                "Axioma PA-A2 (El ego puede imponer una premisa absoluta). "
                "Cuando el ego de R_i se identifica con una limitación puede establecer: "
                "P_¬M := “Esto es imposible”."
            ),
        },
        {
            "id": "PA-A3",
            "tipo": "axioma",
            "sujeto": "Premisa_aceptada",
            "relacion": "estructura",
            "objeto": "realidad_mental_coherente_alrededor_de_ella",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PA-A1", "PA-A2"],
            "gobierna": ["ontologia", "mente"],
            "enunciado": (
                "Axioma PA-A3 (La mente estructura alrededor de la premisa aceptada). "
                "Una vez aceptada P_¬M, la mente de R_i construye una realidad coherente "
                "alrededor de ella: S_i ⊨ P_¬M."
            ),
        },
        {
            "id": "PA-A4",
            "tipo": "axioma",
            "sujeto": "Premisa_absoluta",
            "relacion": "bloquea",
            "objeto": "vias_de_procesamiento_contradictorias",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PA-A3"],
            "gobierna": ["ontologia", "bloqueo"],
            "enunciado": (
                "Axioma PA-A4 (La premisa absoluta bloquea vías contradictorias). "
                "P_¬M → B_i. "
                "El bloqueo no es incapacidad física inicial; es restricción estructural "
                "del espacio de procesamiento de R_i."
            ),
        },
        {
            "id": "PA-A5",
            "tipo": "axioma",
            "sujeto": "Yo",
            "relacion": "puede_reconocer",
            "objeto": "el_bloqueo",
            "polaridad": True,
            "cota": None,
            "depende_de": [],
            "gobierna": ["ontologia", "yo"],
            "enunciado": (
                "Axioma PA-A5 (El Yo puede reconocer el bloqueo). "
                "El Yo de R_i (función L4) identifica que existe B_i "
                "sin necesitar enfrentarse directamente con ella."
            ),
        },
        {
            "id": "PA-A6",
            "tipo": "axioma",
            "sujeto": "Confrontacion_directa_con_el_ego",
            "relacion": "puede_reforzar",
            "objeto": "el_bloqueo",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PA-A2"],
            "gobierna": ["ontologia", "ego", "bloqueo"],
            "enunciado": (
                "Axioma PA-A6 (La confrontación directa puede reforzar el bloqueo). "
                "Discutir directamente con el ego resulta contraproducente: "
                "el ego puede reforzar su propia estructura, reforzando B_i."
            ),
        },
        {
            "id": "PA-A7",
            "tipo": "axioma",
            "sujeto": "Evidencia_de_Contexto_B",
            "relacion": "obliga_a_considerar",
            "objeto": "la_posibilidad_mecanica",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PA-D3", "PA-A1"],
            "gobierna": ["ontologia", "desbloqueo"],
            "enunciado": (
                "Axioma PA-A7 (La evidencia de Contexto B obliga a considerar la posibilidad mecánica). "
                "M(B)=1 ⇒ ¬Imposible_∀C(M). "
                "Equivalente: M(B)=1 ⇒ ◇M. "
                "Mecánica demostrada en B invalida la imposibilidad absoluta de la mecánica."
            ),
        },
        {
            "id": "PA-A8",
            "tipo": "axioma",
            "sujeto": "Asociacion_valida",
            "relacion": "transfiere",
            "objeto": "mecanismo_especifico_y_no_contexto_completo",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PA-D4"],
            "gobierna": ["ontologia", "desbloqueo", "anti_racionalizacion"],
            "enunciado": (
                "Axioma PA-A8 (La asociación válida transfiere mecanismo, no contexto). "
                "AsocValida(A,B,M) ⇒ Transfer(M) ∧ ¬Transfer(Contexto_B_completo). "
                "El contexto completo, identidad, jerarquía, deseo o permiso "
                "no deben confundirse con el mecanismo."
            ),
        },
        {
            "id": "PA-A9",
            "tipo": "axioma",
            "sujeto": "Observacion_precisa",
            "relacion": "requiere",
            "objeto": "distancia_funcional_entre_observador_y_objeto",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PA-D7"],
            "gobierna": ["ontologia", "observacion"],
            "enunciado": (
                "Axioma PA-A9 (La observación requiere distancia funcional). "
                "δ_i(O) > 0 ⇒ ObsPrecisa_i(O). "
                "Cuando R_i y O están fusionados (δ_i(O)=0), "
                "la descripción precisa se vuelve estructuralmente más difícil."
            ),
        },
        {
            "id": "PA-A10",
            "tipo": "axioma",
            "sujeto": "Observacion",
            "relacion": "precede",
            "objeto": "a_la_direccion",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PA-D10"],
            "gobierna": ["ontologia", "observacion", "direccion"],
            "enunciado": (
                "Axioma PA-A10 (La observación precede a la dirección). "
                "Secuencia legítima: I_i → E_i → D_i. "
                "Transición I_i → D_i no es legítima según el documento."
            ),
        },

        # ── LEMAS ─────────────────────────────────────────────────

        {
            "id": "PA-L1",
            "tipo": "lema",
            "sujeto": "Mecanica_existente_en_B",
            "relacion": "debilita",
            "objeto": "la_afirmacion_absoluta_de_imposibilidad_en_A",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PA-A7", "PA-D3"],
            "gobierna": ["ontologia", "desbloqueo"],
            "enunciado": (
                "Lema PA-L1 (Transferencia de Posibilidad). "
                "M(B)=1 ⇒ ¬∀C[¬M(C)]. "
                "Si una mecánica existe realmente en B, la afirmación absoluta de "
                "imposibilidad queda estructuralmente debilitada. No se concluye M(A)."
            ),
        },
        {
            "id": "PA-L2",
            "tipo": "lema",
            "sujeto": "Actualizacion_mental",
            "relacion": "transita_de",
            "objeto": "imposible_a_posible_bajo_determinadas_condiciones",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PA-D6", "PA-L1"],
            "gobierna": ["ontologia", "desbloqueo"],
            "enunciado": (
                "Lema PA-L2 (Actualización de Condiciones). "
                "La mente de R_i no transita de ¬◇M → M garantizado, "
                "sino de ¬◇M → ◇M (posible bajo determinadas condiciones). "
                "S_i^(0) ⊨ ¬◇M → S_i^(1) ⊨ ◇M."
            ),
        },
        {
            "id": "PA-L3",
            "tipo": "lema",
            "sujeto": "Asociacion_valida",
            "relacion": "no_es",
            "objeto": "imaginacion_positiva",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PA-A8", "PA-D4"],
            "gobierna": ["ontologia", "desbloqueo"],
            "enunciado": (
                "Lema PA-L3 (Asociación no es imaginación positiva). "
                "AsocValida requiere: hecho real (M(B)=1) + mecanismo identificable + "
                "transferencia delimitada (Transfer(M)). No funciona mediante esperanza."
            ),
        },
        {
            "id": "PA-L4",
            "tipo": "lema",
            "sujeto": "Capacidad_descriptiva",
            "relacion": "ya_existe_en_el_sujeto",
            "objeto": "y_puede_reutilizarse",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PA-D7"],
            "gobierna": ["ontologia", "observacion"],
            "enunciado": (
                "Lema PA-L4 (La capacidad ya existente puede reutilizarse). "
                "El mismo R_i que puede describir con precisión procesos externos "
                "ya posee la capacidad de observación y descripción. "
                "El problema interno no se presenta como ausencia absoluta de capacidad."
            ),
        },
        {
            "id": "PA-L5",
            "tipo": "lema",
            "sujeto": "Problema_de_descripcion_interna",
            "relacion": "es",
            "objeto": "problema_de_posicion_del_observador",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PA-L4", "PA-D7"],
            "gobierna": ["ontologia", "observacion"],
            "enunciado": (
                "Lema PA-L5 (El problema interno es de posición del observador). "
                "Si ObsPrecisa_i funciona externamente pero aparentemente falla internamente, "
                "el documento localiza la diferencia en δ_i(O)."
            ),
        },
        {
            "id": "PA-L6",
            "tipo": "lema",
            "sujeto": "Identificacion",
            "relacion": "colapsa",
            "objeto": "la_distancia_funcional",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PA-D8", "PA-A9"],
            "gobierna": ["ontologia", "observacion"],
            "enunciado": (
                "Lema PA-L6 (La identificación colapsa la distancia). "
                "Identificacion_i(O) ⇒ δ_i(O) = 0. "
                "Identificación → R_i fusionado con O → pérdida de distancia funcional."
            ),
        },
        {
            "id": "PA-L7",
            "tipo": "lema",
            "sujeto": "Observacion_del_patron",
            "relacion": "disuelve_progresivamente",
            "objeto": "la_identificacion",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PA-L6", "PA-D9"],
            "gobierna": ["ontologia", "observacion", "desbloqueo"],
            "enunciado": (
                "Lema PA-L7 (La observación disuelve progresivamente la identificación). "
                "Cuando el patrón O se vuelve objeto de Obs(R_i): "
                "O deja de ser completamente invisible → pierde fuerza identificatoria. "
                "Formulación documental: lo que se ve, se suelta."
            ),
        },
        {
            "id": "PA-L8",
            "tipo": "lema",
            "sujeto": "Comprension_directa_de_la_mecanica",
            "relacion": "sustituye_progresivamente",
            "objeto": "a_la_regla_externa_de_validez",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PA-L7"],
            "gobierna": ["ontologia", "observacion"],
            "enunciado": (
                "Lema PA-L8 (La comprensión sustituye progresivamente a la regla externa). "
                "Inicialmente: criterio externo → protege contra racionalización. "
                "Posteriormente: comprensión directa de la mecánica → reduce la necesidad "
                "del criterio externo."
            ),
        },
        {
            "id": "PA-L9",
            "tipo": "lema",
            "sujeto": "Director",
            "relacion": "depende_de",
            "objeto": "haber_establecido_distancia_mediante_observacion",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PA-A10", "PA-D10"],
            "gobierna": ["ontologia", "direccion"],
            "enunciado": (
                "Lema PA-L9 (El director depende del espectador). "
                "D_i legítimo requiere E_i previo. "
                "E_i → condición de posibilidad → D_i."
            ),
        },

        # ── TEOREMAS ──────────────────────────────────────────────

        {
            "id": "PA-T1",
            "tipo": "teorema",
            "sujeto": "Mecanica_considerada_imposible_en_A",
            "relacion": "queda_invalidada_en_su_absolutidad_si",
            "objeto": "existe_de_forma_demostrable_en_B",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PA-L1", "PA-A7"],
            "gobierna": ["ontologia", "desbloqueo"],
            "enunciado": (
                "Teorema PA-T1 (Disolución de la Imposibilidad Absoluta). "
                "Premisas: P1. M(B)=1. P2. M(B)=1 ⇒ ¬∀C[¬M(C)]. "
                "Derivación: P1 ∧ P2 ⊢ ¬∀C[M(C)=0]. Equivalente: M(B)=1 ⊢ ◇M. "
                "Conclusión: la imposibilidad absoluta de M queda invalidada. "
                "NO demuestra M(A). Demuestra solamente: M es posible bajo alguna "
                "configuración de condiciones."
            ),
        },
        {
            "id": "PA-T2",
            "tipo": "teorema",
            "sujeto": "Asociacion_valida",
            "relacion": "requiere",
            "objeto": "aislar_el_mecanismo_especifico_y_nombrarlo_por_separado_del_resto_del_contexto",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PA-T1", "PA-D4", "PA-A8"],
            "gobierna": ["ontologia", "desbloqueo"],
            "enunciado": (
                "Teorema PA-T2 (Criterio de transferencia mecánica). "
                "Premisas: "
                "P1. AsocValida(A,B,M) ⇒ Transfer(M) ∧ ¬Transfer(Contexto_B_completo). "
                "P2. M es aislable y nombrable independientemente del resto del contexto. "
                "Derivación: P1 ∧ P2 ⊢ base documental para asociación válida. "
                "Criterio del documento: ¿qué mecánica exacta estoy transfiriendo, "
                "y por qué opera igual en los dos casos? "
                "NO se deriva: M(B) ⇒ M(A)."
            ),
        },
        {
            "id": "PA-T3",
            "tipo": "teorema",
            "sujeto": "Importacion_de_contexto_completo",
            "relacion": "no_constituye",
            "objeto": "transferencia_de_mecanica_aislada",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PA-A8", "PA-D4"],
            "gobierna": ["ontologia", "anti_racionalizacion"],
            "enunciado": (
                "Teorema PA-T3 (No-Transferencia Contextual). "
                "Premisas: "
                "P1. AsocValida ⇒ Transfer(M) ∧ ¬Transfer(Contexto_B_completo). "
                "P2. Importar identidad, jerarquía, deseo, permiso o contexto completo "
                "≡ Transfer(Contexto_B_completo). "
                "Derivación: P1 ∧ P2 ⊢ ¬AsocValida cuando se importa contexto completo."
            ),
        },
        {
            "id": "PA-T4",
            "tipo": "teorema",
            "sujeto": "Identificacion_observador_igual_objeto",
            "relacion": "reduce",
            "objeto": "la_capacidad_descriptiva_precisa",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PA-A9", "PA-L6"],
            "gobierna": ["ontologia", "observacion"],
            "enunciado": (
                "Teorema PA-T4 (Distancia Observacional). "
                "Premisas: "
                "P1. δ_i(O) > 0 ⇒ ObsPrecisa_i(O). "
                "P2. Identificacion_i(O) ⇒ δ_i(O) = 0. "
                "Derivación: P1 ∧ P2 ⊢ Identificacion_i(O) ⇒ reducción de ObsPrecisa_i(O)."
            ),
        },
        {
            "id": "PA-T5",
            "tipo": "teorema",
            "sujeto": "Sujeto_que_establece_distancia_interna",
            "relacion": "puede_aplicar",
            "objeto": "la_misma_funcion_de_observacion_utilizada_sobre_objetos_externos",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PA-T4", "PA-L4", "PA-D9"],
            "gobierna": ["ontologia", "observacion", "conciencia"],
            "enunciado": (
                "Teorema PA-T5 (Observación Interna). "
                "Premisas: "
                "P1. R_i ya posee ObsPrecisa sobre objetos externos. "
                "P2. δ_i(O) > 0 es la condición de ObsPrecisa. "
                "P3. ObsInterna_i(O) ≡ aplicar Obs hacia adentro (L5). "
                "Derivación: P1 ∧ P2 ∧ P3 ⊢ si δ_i(O_interno) > 0, "
                "entonces R_i puede reutilizar la misma función observacional hacia adentro. "
                "Documento: la tarea no es desarrollar una nueva capacidad; "
                "es aplicar la misma posición de observación hacia adentro."
            ),
        },
        {
            "id": "PA-T6",
            "tipo": "teorema",
            "sujeto": "Secuencia_Identificado_Espectador_Director",
            "relacion": "es",
            "objeto": "irreversible_y_no_saltable",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PA-A10", "PA-L9", "PA-D10"],
            "gobierna": ["ontologia", "observacion", "direccion"],
            "enunciado": (
                "Teorema PA-T6 (Secuencia Irreversible). "
                "Premisas: "
                "P1. Secuencia legítima: I_i → E_i → D_i. "
                "P2. D_i legítimo requiere E_i previo. "
                "Derivación: P1 ∧ P2 ⊢ ¬(I_i → D_i legítimo). "
                "Documento: quien intenta dirigir sin antes observar sigue identificado "
                "y solo ha cambiado de máscara."
            ),
        },
        {
            "id": "PA-T7",
            "tipo": "teorema",
            "sujeto": "Libertad",
            "relacion": "aparece_primariamente_por",
            "objeto": "dejar_de_estar_completamente_identificado_con_el_patron",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PA-T5", "PA-T6", "PA-L7"],
            "gobierna": ["ontologia", "observacion", "direccion", "libertad"],
            "enunciado": (
                "Teorema PA-T7 (Libertad por Observación). "
                "Premisas: "
                "P1. Obs del patrón → disolución progresiva de identificación. "
                "P2. δ_i > 0 permite ObsInterna. "
                "P3. E_i precede a D_i. "
                "Cadena documental: ver patrón → establecer δ_i > 0 → disminuir identificación → "
                "recuperar capacidad de elección → dirección. "
                "Documento: no dejas de ser esclavo del patrón por luchar contra él, "
                "sino por verlo operar. Lo que observas, lo sueltas. "
                "Estado: formulación documental; no se afirma Γ ⊢ Libertad más allá del texto."
            ),
        },

        # ── COROLARIOS ────────────────────────────────────────────

        {
            "id": "PA-C1",
            "tipo": "corolario",
            "sujeto": "Imposibilidad_percibida",
            "relacion": "puede_ser",
            "objeto": "limite_de_diseno_impuesto_por_identidad",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PA-T1", "PA-A2"],
            "gobierna": ["ontologia", "desbloqueo"],
            "enunciado": (
                "Corolario PA-C1. "
                "Una imposibilidad percibida (P_¬M en S_i) no necesariamente representa "
                "una imposibilidad mecánica en R. "
                "Puede representar una regla estructural aceptada por la identidad de R_i."
            ),
        },
        {
            "id": "PA-C2",
            "tipo": "corolario",
            "sujeto": "Existencia_de_solucion_en_otro_contexto",
            "relacion": "constituye_evidencia_contra",
            "objeto": "la_imposibilidad_absoluta",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PA-T1", "PA-L1"],
            "gobierna": ["ontologia", "desbloqueo"],
            "enunciado": (
                "Corolario PA-C2. "
                "M(B)=1 constituye evidencia contra ∀C[M(C)=0]. "
                "El principio permite importar posibilidad mecánica (◇M), "
                "no necesariamente el resultado completo M(A)."
            ),
        },
        {
            "id": "PA-C3",
            "tipo": "corolario",
            "sujeto": "Cuerpo_fisico",
            "relacion": "sirve_como",
            "objeto": "Contexto_B_para_procesos_de_transformacion",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PA-T2"],
            "gobierna": ["ontologia", "desbloqueo"],
            "enunciado": (
                "Corolario PA-C3. "
                "El ejemplo del cuerpo se utiliza como B para asociar: "
                "materia estructurada → capacidad de reestructuración "
                "con pensamiento/emoción/carácter → posibilidad de cambio. "
                "Asociación conceptual del documento; no demostración biomédica cuantitativa."
            ),
        },
        {
            "id": "PA-C4",
            "tipo": "corolario",
            "sujeto": "Procesamiento_sin_sufrimiento",
            "relacion": "muestra",
            "objeto": "independencia_entre_procesamiento_y_sufrimiento",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PA-T2", "PA-A8"],
            "gobierna": ["ontologia", "desbloqueo"],
            "enunciado": (
                "Corolario PA-C4. "
                "El ejemplo del procesador establece: "
                "procesamiento de alta complejidad ≠ sufrimiento necesario. "
                "Mecánica transferida: procesamiento sin identificación."
            ),
        },
        {
            "id": "PA-C5",
            "tipo": "corolario",
            "sujeto": "IA",
            "relacion": "funciona_como",
            "objeto": "espejo_de_mecanicas_de_procesamiento_humano",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PA-T2"],
            "gobierna": ["ontologia", "desbloqueo", "conciencia"],
            "enunciado": (
                "Corolario PA-C5. "
                "El documento utiliza fenómenos de IA (alucinaciones, sesgos) como B "
                "para mostrar que determinados fenómenos de procesamiento no son defectos "
                "exclusivos del “estar vivo”, sino consecuencias mecánicas de cómo se "
                "procesa la información en una red neuronal."
            ),
        },
        {
            "id": "PA-C6",
            "tipo": "corolario",
            "sujeto": "Consciencia_L5",
            "relacion": "corresponde_a",
            "objeto": "observar_el_proceso_interno_sin_identificarse_con_el",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PA-D9", "PA-T5", "ST-D5"],
            "gobierna": ["ontologia", "observacion", "conciencia"],
            "enunciado": (
                "Corolario PA-C6. "
                "L5(R_i) = Obs(R_i). "
                "El documento conecta el Principio de Asociación con CEMYCA: "
                "L5 = observar el proceso interno con la misma neutralidad con que se "
                "observa un proceso externo. No se redefine L5."
            ),
        },
        {
            "id": "PA-C7",
            "tipo": "corolario",
            "sujeto": "Comprension_del_mecanismo",
            "relacion": "reduce",
            "objeto": "la_racionalizacion",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PA-L8", "PA-L7"],
            "gobierna": ["ontologia", "observacion"],
            "enunciado": (
                "Corolario PA-C7. "
                "Cuando la mecánica es directamente observable por R_i, "
                "el ego ya no necesita una regla externa para evitar la racionalización "
                "porque la propia estructura observada revela el error."
            ),
        },
        {
            "id": "PA-C8",
            "tipo": "corolario",
            "sujeto": "Libertad",
            "relacion": "aparece_como_consecuencia_de",
            "objeto": "la_desidentificacion",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PA-T7", "PA-T6", "ST-D4", "ST-D6"],
            "gobierna": ["ontologia", "observacion", "direccion", "libertad"],
            "enunciado": (
                "Corolario PA-C8. "
                "Arco completo del documento: "
                "Identificacion_i → B_i → Obs → δ_i > 0 → desidentificación → "
                "elección → dirección. "
                "D_i queda conectado con: función del Yo (L4) integrada por el "
                "propósito del Alma (L6). No se redefinen las capas."
            ),
        },
    ]


__all__ = ["CUERPO", "declaraciones"]
