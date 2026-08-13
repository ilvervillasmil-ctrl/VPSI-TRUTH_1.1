# ===============================================================
# modules/axiomas/principio_asociacion_AX.py
# Cuerpo axiomático: Principio de Asociación — v1.3
# Prefijo semántico: PDA (Principio de Asociación)
# Formalización matemática + nota_semantica por declaración
#
# REGLA ABSOLUTA:
#   PAPER → FORMALIZACIÓN → DEPENDENCIAS → DEMOSTRACIÓN → CONTRATO → ENGINE
#   M(B)=1 ⇒ ◇M
#   NUNCA: M(B) ⇒ M(A)
#
# BASE FORMAL (sin redefinir):
#   R_i = C · L · K ;  R_i ⊂ R ;  R → X → Y
#   L4 = Yo/elección ; L5 = Consciencia/obs ; L6 = Alma/dirección
#
# CONVENCIÓN DE ID:
#   PDA-D1…D10  definiciones
#   PDA-A1…A10  axiomas
#   PDA-L1…L9   lemas
#   PDA-T1…T7   teoremas
#   PDA-C1…C8   corolarios
# ===============================================================

"""
Cuerpo axiomático: Principio de Asociación — v1.3

Estructura:
  Definiciones  : 10  (PDA-D1  … PDA-D10)
  Axiomas       : 10  (PDA-A1  … PDA-A10)
  Lemas         :  9  (PDA-L1  … PDA-L9)
  Teoremas      :  7  (PDA-T1  … PDA-T7)
  Corolarios    :  8  (PDA-C1  … PDA-C8)
  Total         : 44  (IDs únicos, prefijo PDA)
"""

from __future__ import annotations

from typing import Any, Dict, List

CUERPO = {
    "nombre": "principio_asociacion",
    "version": "1.3",
}


def declaraciones() -> List[Dict[str, Any]]:
    return [

        # ── DEFINICIONES ──────────────────────────────────────────

        {
            "id": "PDA-D1",
            "tipo": "definicion",
            "sujeto": "Principio_de_Asociacion",
            "relacion": "establece_que",
            "objeto": "si_existe_creencia_de_imposibilidad_se_introduce_contexto_alternativo_real",
            "polaridad": True,
            "cota": None,
            "depende_de": [],
            "gobierna": ["ontologia", "epistemologia", "desbloqueo"],
            "enunciado": (
                "Definición PDA-D1 (Principio de Asociación). "
                "Sea A un contexto donde R_i sostiene la premisa P_¬M := “M es imposible”. "
                "Sea B un contexto real donde M(B)=1. "
                "El Principio de Asociación establece la operación 𝒜(A,B,M) por la cual "
                "R_i introduce B como evidencia, forzando la actualización: P_¬M → P_◇M. "
                "Formalmente: M(B)=1 ⇒ ◇M. "
                "Documento: si pasa allá, la mecánica existe; si la mecánica existe, puede pasar aquí. "
                "Nota: “puede” ≡ ◇M, no ≡ M(A)."
            ),
            "nota_semantica": (
                "Define la operación central del cuerpo. Establece que la evidencia de M en un "
                "contexto real B actualiza el estado de R_i de imposibilidad absoluta a posibilidad "
                "bajo condiciones (◇M). No autoriza concluir M(A). Es el punto de partida de toda "
                "la cadena de desbloqueo."
            ),
        },
        {
            "id": "PDA-D2",
            "tipo": "definicion",
            "sujeto": "Contexto_A_Bloqueado",
            "relacion": "es",
            "objeto": "contexto_donde_existe_la_premisa_esto_es_imposible",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PDA-D1"],
            "gobierna": ["ontologia", "desbloqueo"],
            "enunciado": (
                "Definición PDA-D2 (Contexto A – Bloqueo). "
                "A := contexto en el que R_i sostiene P_¬M. "
                "Dominio donde opera la limitación aceptada por la mente de R_i."
            ),
            "nota_semantica": (
                "Identifica el dominio de partida del bloqueo. Es el contexto en el que existe "
                "la premisa de imposibilidad. No describe todavía el mecanismo de salida; "
                "solo localiza dónde opera la limitación."
            ),
        },
        {
            "id": "PDA-D3",
            "tipo": "definicion",
            "sujeto": "Contexto_B_Evidencial",
            "relacion": "es",
            "objeto": "contexto_real_donde_el_fenomeno_o_mecanismo_ya_ocurre_de_manera_verificable",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PDA-D1"],
            "gobierna": ["ontologia", "desbloqueo"],
            "enunciado": (
                "Definición PDA-D3 (Contexto B – Evidencia). "
                "B := contexto real tal que M(B)=1 de manera verificable. "
                "B constituye el puente de evidencia para 𝒜(A,B,M)."
            ),
            "nota_semantica": (
                "Define el contexto de evidencia real. Su única función es servir de puente "
                "verificable. No transfiere automáticamente el resultado a A; solo aporta "
                "la realización de M que permite invalidar la imposibilidad absoluta."
            ),
        },
        {
            "id": "PDA-D4",
            "tipo": "definicion",
            "sujeto": "Mecanica_Especifica_Transferible",
            "relacion": "es",
            "objeto": "mecanica_concreta_aislable_del_contexto_B",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PDA-D3"],
            "gobierna": ["ontologia", "desbloqueo"],
            "enunciado": (
                "Definición PDA-D4 (Mecánica Transferible). "
                "M es la mecánica concreta que existe en B y que puede aislarse: "
                "B ─aislamiento→ M. "
                "Formalmente: Transfer(M) ∧ ¬Transfer(Contexto_B_completo)."
            ),
            "nota_semantica": (
                "Separa el mecanismo del contexto completo. Es la base del criterio "
                "anti-racionalización: solo se transfiere M, nunca la identidad, jerarquía "
                "o permiso asociados a B. Fundamento de PDA-A8 y PDA-T2/T3."
            ),
        },
        {
            "id": "PDA-D5",
            "tipo": "definicion",
            "sujeto": "Bloqueo_Estructural",
            "relacion": "es",
            "objeto": "estado_producido_cuando_premisa_de_imposibilidad_es_aceptada_como_regla_absoluta",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PDA-D2"],
            "gobierna": ["ontologia", "desbloqueo"],
            "enunciado": (
                "Definición PDA-D5 (Bloqueo Estructural). "
                "Sea B_i el estado interno de bloqueo de R_i. "
                "B_i se produce cuando P_¬M es aceptada como regla absoluta y la mente de R_i "
                "cierra vías de procesamiento incompatibles con P_¬M. "
                "Formalmente: P_¬M → B_i."
            ),
            "nota_semantica": (
                "Define el estado interno de bloqueo. No es una incapacidad física; es una "
                "restricción estructural del espacio de procesamiento de R_i producida por "
                "la aceptación de una premisa absoluta de imposibilidad."
            ),
        },
        {
            "id": "PDA-D6",
            "tipo": "definicion",
            "sujeto": "Actualizacion_Estructural",
            "relacion": "es",
            "objeto": "proceso_mediante_el_cual_la_mente_modifica_la_regla_previamente_aceptada",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PDA-D5", "PDA-D3"],
            "gobierna": ["ontologia", "desbloqueo"],
            "enunciado": (
                "Definición PDA-D6 (Actualización Estructural). "
                "Sea S_i^(0) el estado representacional de R_i que contiene P_¬M. "
                "Tras evidencia M(B)=1: S_i^(0) → S_i^(1) donde S_i^(1) contiene P_◇M. "
                "Transición documental: “Es imposible” → “Es posible bajo ciertas condiciones”. "
                "R permanece invariante. Solo cambia el estado de R_i."
            ),
            "nota_semantica": (
                "Describe el cambio de estado interno de R_i. R no se modifica. "
                "La actualización es de la representación del observador, no de la realidad. "
                "Transita a posibilidad bajo condiciones, nunca a garantía de M(A)."
            ),
        },
        {
            "id": "PDA-D7",
            "tipo": "definicion",
            "sujeto": "Distancia_Observador_Objeto",
            "relacion": "es",
            "objeto": "separacion_funcional_entre_quien_observa_y_aquello_que_es_observado",
            "polaridad": True,
            "cota": None,
            "depende_de": [],
            "gobierna": ["ontologia", "epistemologia", "observacion"],
            "enunciado": (
                "Definición PDA-D7 (Distancia Observador-Objeto). "
                "δ_i(O) representa la separación funcional entre R_i y el objeto O. "
                "δ_i(O) > 0 := separación funcional (posición observacional). "
                "δ_i(O) = 0 := fusión funcional (identificación). "
                "δ_i no es distancia espacial ni métrica física; es relación funcional."
            ),
            "nota_semantica": (
                "Introduce la relación funcional de distancia. No es una magnitud física. "
                "Sirve como condición de posibilidad de descripción precisa y como "
                "indicador de identificación (δ=0) frente a observación (δ>0)."
            ),
        },
        {
            "id": "PDA-D8",
            "tipo": "definicion",
            "sujeto": "Identificacion",
            "relacion": "es",
            "objeto": "estado_en_el_que_el_observador_se_encuentra_fusionado_con_el_patron_observado",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PDA-D7"],
            "gobierna": ["ontologia", "observacion"],
            "enunciado": (
                "Definición PDA-D8 (Identificación). "
                "Identificacion_i(O) := estado en el que R_i se encuentra fusionado con el patrón O. "
                "Formalmente: Identificacion_i(O) ⇒ δ_i(O) = 0. "
                "Ejemplo del documento: “Yo soy la angustia”."
            ),
            "nota_semantica": (
                "Define el estado de fusión observador–objeto. Es el opuesto funcional de "
                "la observación. Cuando hay identificación, δ_i colapsa a 0 y la descripción "
                "precisa se dificulta. Base de PDA-L6 y PDA-T4."
            ),
        },
        {
            "id": "PDA-D9",
            "tipo": "definicion",
            "sujeto": "Observacion_Interna_L5",
            "relacion": "es",
            "objeto": "funcion_de_la_consciencia_de_observar_el_proceso_interno_con_neutralidad",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PDA-D7", "ST-D5"],
            "gobierna": ["ontologia", "observacion", "conciencia"],
            "enunciado": (
                "Definición PDA-D9 (Función de Observación Interna – L5). "
                "L5(R_i) = Obs(R_i). "
                "ObsInterna_i(O) := observar el proceso interno O con la misma neutralidad "
                "con la que se observa un proceso externo. "
                "Vinculada explícitamente con L5. No se redefine L5."
            ),
            "nota_semantica": (
                "Conecta el Principio de Asociación con la capa L5 del corpus CEMYCA. "
                "No redefine L5; solo declara que la observación interna es la aplicación "
                "hacia adentro de la misma función observacional. Dependencia explícita de ST-D5."
            ),
        },
        {
            "id": "PDA-D10",
            "tipo": "definicion",
            "sujeto": "Arco_del_trabajo_interior",
            "relacion": "es",
            "objeto": "Identificado_luego_Espectador_luego_Director",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PDA-D8", "PDA-D9"],
            "gobierna": ["ontologia", "observacion", "direccion"],
            "enunciado": (
                "Definición PDA-D10 (Arco del trabajo interior). "
                "I_i := Identificado (R_i es el patrón). "
                "E_i := Espectador (R_i ve el patrón; función de L5). "
                "D_i := Director (R_i orienta; función de L4 integrada por L6). "
                "Secuencia documental: I_i → E_i → D_i. "
                "El orden no se puede saltar. Transición I_i → D_i no es legítima."
            ),
            "nota_semantica": (
                "Define los tres estados/funciones del arco interior. Establece el orden "
                "irreversible. Director no es un simple estado observacional adicional; "
                "es la función de orientación (L4+L6) que solo aparece después de la "
                "observación (E_i / L5)."
            ),
        },

        # ── AXIOMAS ───────────────────────────────────────────────

        {
            "id": "PDA-A1",
            "tipo": "axioma",
            "sujeto": "Mente",
            "relacion": "busca",
            "objeto": "coherencia",
            "polaridad": True,
            "cota": None,
            "depende_de": [],
            "gobierna": ["ontologia", "mente"],
            "enunciado": (
                "Axioma PDA-A1 (La mente busca coherencia). "
                "La mente de R_i opera como estructura de orden y busca construir "
                "una realidad coherente a partir de sus premisas."
            ),
            "nota_semantica": (
                "Regla base sobre el funcionamiento de la mente. Explica por qué una "
                "premisa de imposibilidad, una vez aceptada, organiza todo el espacio "
                "de procesamiento alrededor de ella. Fundamento de PDA-A3 y PDA-A4."
            ),
        },
        {
            "id": "PDA-A2",
            "tipo": "axioma",
            "sujeto": "Ego",
            "relacion": "puede_imponer",
            "objeto": "premisa_absoluta_de_imposibilidad",
            "polaridad": True,
            "cota": None,
            "depende_de": [],
            "gobierna": ["ontologia", "ego"],
            "enunciado": (
                "Axioma PDA-A2 (El ego puede imponer una premisa absoluta). "
                "Cuando el ego de R_i se identifica con una limitación puede establecer: "
                "P_¬M := “Esto es imposible”."
            ),
            "nota_semantica": (
                "Establece el origen de la premisa absoluta de imposibilidad. El ego, "
                "en función de supervivencia/identidad, es quien puede imponer P_¬M. "
                "No afirma que siempre lo haga; afirma que puede hacerlo."
            ),
        },
        {
            "id": "PDA-A3",
            "tipo": "axioma",
            "sujeto": "Premisa_aceptada",
            "relacion": "estructura",
            "objeto": "realidad_mental_coherente_alrededor_de_ella",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PDA-A1", "PDA-A2"],
            "gobierna": ["ontologia", "mente"],
            "enunciado": (
                "Axioma PDA-A3 (La mente estructura alrededor de la premisa aceptada). "
                "Una vez aceptada P_¬M, la mente de R_i construye una realidad coherente "
                "alrededor de ella: S_i ⊨ P_¬M."
            ),
            "nota_semantica": (
                "Consecuencia de PDA-A1 + PDA-A2. Una vez aceptada la premisa, la mente "
                "no la cuestiona: la convierte en eje de coherencia interna. "
                "Prepara el terreno del bloqueo (PDA-A4)."
            ),
        },
        {
            "id": "PDA-A4",
            "tipo": "axioma",
            "sujeto": "Premisa_absoluta",
            "relacion": "bloquea",
            "objeto": "vias_de_procesamiento_contradictorias",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PDA-A3"],
            "gobierna": ["ontologia", "bloqueo"],
            "enunciado": (
                "Axioma PDA-A4 (La premisa absoluta bloquea vías contradictorias). "
                "P_¬M → B_i. "
                "El bloqueo no es incapacidad física inicial; es restricción estructural "
                "del espacio de procesamiento de R_i."
            ),
            "nota_semantica": (
                "Cierra la cadena de formación del bloqueo. La premisa absoluta no solo "
                "se acepta: cierra vías. El bloqueo es estructural, no fisiológico."
            ),
        },
        {
            "id": "PDA-A5",
            "tipo": "axioma",
            "sujeto": "Yo",
            "relacion": "puede_reconocer",
            "objeto": "el_bloqueo",
            "polaridad": True,
            "cota": None,
            "depende_de": [],
            "gobierna": ["ontologia", "yo"],
            "enunciado": (
                "Axioma PDA-A5 (El Yo puede reconocer el bloqueo). "
                "El Yo de R_i (función L4) identifica que existe B_i "
                "sin necesitar enfrentarse directamente con ella."
            ),
            "nota_semantica": (
                "Introduce la capacidad del Yo de detectar el bloqueo sin confrontación. "
                "Es el punto de partida de la intervención no conflictiva que el Principio "
                "de Asociación requiere. No implica todavía la presentación de evidencia."
            ),
        },
        {
            "id": "PDA-A6",
            "tipo": "axioma",
            "sujeto": "Confrontacion_directa_con_el_ego",
            "relacion": "puede_reforzar",
            "objeto": "el_bloqueo",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PDA-A2"],
            "gobierna": ["ontologia", "ego", "bloqueo"],
            "enunciado": (
                "Axioma PDA-A6 (La confrontación directa puede reforzar el bloqueo). "
                "Discutir directamente con el ego resulta contraproducente: "
                "el ego puede reforzar su propia estructura, reforzando B_i."
            ),
            "nota_semantica": (
                "Explica por qué el Principio de Asociación evita el enfrentamiento directo. "
                "La confrontación puede fortalecer B_i en lugar de disolverlo. "
                "Justifica la vía indirecta (evidencia de B)."
            ),
        },
        {
            "id": "PDA-A7",
            "tipo": "axioma",
            "sujeto": "Evidencia_de_Contexto_B",
            "relacion": "obliga_a_considerar",
            "objeto": "la_posibilidad_mecanica",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PDA-D3", "PDA-A1"],
            "gobierna": ["ontologia", "desbloqueo"],
            "enunciado": (
                "Axioma PDA-A7 (La evidencia de Contexto B obliga a considerar la posibilidad mecánica). "
                "M(B)=1 ⇒ ¬Imposible_∀C(M). "
                "Equivalente: M(B)=1 ⇒ ◇M. "
                "Mecánica demostrada en B invalida la imposibilidad absoluta de la mecánica."
            ),
            "nota_semantica": (
                "Núcleo del Principio. La evidencia verificable de M en B invalida la "
                "afirmación de que M sea imposible en todo contexto. "
                "Alcance: solo ◇M. "
                "NO autoriza M(A). Esta restricción es contractual y no negociable."
            ),
        },
        {
            "id": "PDA-A8",
            "tipo": "axioma",
            "sujeto": "Asociacion_valida",
            "relacion": "transfiere",
            "objeto": "mecanismo_especifico_y_no_contexto_completo",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PDA-D4"],
            "gobierna": ["ontologia", "desbloqueo", "anti_racionalizacion"],
            "enunciado": (
                "Axioma PDA-A8 (La asociación válida transfiere mecanismo, no contexto). "
                "AsocValida(A,B,M) ⇒ Transfer(M) ∧ ¬Transfer(Contexto_B_completo). "
                "El contexto completo, identidad, jerarquía, deseo o permiso "
                "no deben confundirse con el mecanismo."
            ),
            "nota_semantica": (
                "Principal mecanismo anti-racionalización. Define qué cuenta como "
                "asociación válida: solo el mecanismo aislado. Importar identidad, "
                "jerarquía o permiso convierte la operación en racionalización, "
                "no en asociación."
            ),
        },
        {
            "id": "PDA-A9",
            "tipo": "axioma",
            "sujeto": "Observacion_precisa",
            "relacion": "requiere",
            "objeto": "distancia_funcional_entre_observador_y_objeto",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PDA-D7"],
            "gobierna": ["ontologia", "observacion"],
            "enunciado": (
                "Axioma PDA-A9 (La observación requiere distancia funcional). "
                "δ_i(O) > 0 ⇒ ObsPrecisa_i(O). "
                "Cuando R_i y O están fusionados (δ_i(O)=0), "
                "la descripción precisa se vuelve estructuralmente más difícil."
            ),
            "nota_semantica": (
                "Establece la condición de distancia para la observación precisa. "
                "Es el puente entre la definición de δ_i y los teoremas de observación "
                "interna (PDA-T4, PDA-T5)."
            ),
        },
        {
            "id": "PDA-A10",
            "tipo": "axioma",
            "sujeto": "Observacion",
            "relacion": "precede",
            "objeto": "a_la_direccion",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PDA-D10"],
            "gobierna": ["ontologia", "observacion", "direccion"],
            "enunciado": (
                "Axioma PDA-A10 (La observación precede a la dirección). "
                "Secuencia legítima: I_i → E_i → D_i. "
                "Transición I_i → D_i no es legítima según el documento."
            ),
            "nota_semantica": (
                "Fija el orden irreversible del arco interior. "
                "Sin observación previa (E_i) no hay dirección legítima (D_i). "
                "Fundamento de PDA-L9 y PDA-T6."
            ),
        },

        # ── LEMAS ─────────────────────────────────────────────────

        {
            "id": "PDA-L1",
            "tipo": "lema",
            "sujeto": "Mecanica_existente_en_B",
            "relacion": "debilita",
            "objeto": "la_afirmacion_absoluta_de_imposibilidad_en_A",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PDA-A7", "PDA-D3"],
            "gobierna": ["ontologia", "desbloqueo"],
            "enunciado": (
                "Lema PDA-L1 (Transferencia de Posibilidad). "
                "M(B)=1 ⇒ ¬∀C[¬M(C)]. "
                "Si una mecánica existe realmente en B, la afirmación absoluta de "
                "imposibilidad queda estructuralmente debilitada. No se concluye M(A)."
            ),
            "nota_semantica": (
                "Consecuencia intermedia de PDA-A7. Debilita la imposibilidad absoluta "
                "sin autorizar la transferencia del resultado a A. "
                "Paso necesario hacia PDA-T1."
            ),
        },
        {
            "id": "PDA-L2",
            "tipo": "lema",
            "sujeto": "Actualizacion_mental",
            "relacion": "transita_de",
            "objeto": "imposible_a_posible_bajo_determinadas_condiciones",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PDA-D6", "PDA-L1"],
            "gobierna": ["ontologia", "desbloqueo"],
            "enunciado": (
                "Lema PDA-L2 (Actualización de Condiciones). "
                "La mente de R_i no transita de ¬◇M → M garantizado, "
                "sino de ¬◇M → ◇M (posible bajo determinadas condiciones). "
                "S_i^(0) ⊨ ¬◇M → S_i^(1) ⊨ ◇M."
            ),
            "nota_semantica": (
                "Precisa el tipo de actualización que el Principio produce. "
                "Evita la lectura de “pensamiento positivo”: no se garantiza M(A), "
                "solo se abre el espacio de posibilidad bajo condiciones."
            ),
        },
        {
            "id": "PDA-L3",
            "tipo": "lema",
            "sujeto": "Asociacion_valida",
            "relacion": "no_es",
            "objeto": "imaginacion_positiva",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PDA-A8", "PDA-D4"],
            "gobierna": ["ontologia", "desbloqueo"],
            "enunciado": (
                "Lema PDA-L3 (Asociación no es imaginación positiva). "
                "AsocValida requiere: hecho real (M(B)=1) + mecanismo identificable + "
                "transferencia delimitada (Transfer(M)). No funciona mediante esperanza."
            ),
            "nota_semantica": (
                "Delimita el Principio frente a lecturas voluntaristas. "
                "La asociación exige evidencia real y mecanismo aislable; "
                "no opera por deseo ni por afirmación sin soporte."
            ),
        },
        {
            "id": "PDA-L4",
            "tipo": "lema",
            "sujeto": "Capacidad_descriptiva",
            "relacion": "ya_existe_en_el_sujeto",
            "objeto": "y_puede_reutilizarse",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PDA-D7"],
            "gobierna": ["ontologia", "observacion"],
            "enunciado": (
                "Lema PDA-L4 (La capacidad ya existente puede reutilizarse). "
                "El mismo R_i que puede describir con precisión procesos externos "
                "ya posee la capacidad de observación y descripción. "
                "El problema interno no se presenta como ausencia absoluta de capacidad."
            ),
            "nota_semantica": (
                "Establece que la herramienta observacional ya existe en R_i. "
                "El fallo de descripción interna no es falta de capacidad, "
                "sino de posición (δ_i). Base de PDA-L5 y PDA-T5."
            ),
        },
        {
            "id": "PDA-L5",
            "tipo": "lema",
            "sujeto": "Problema_de_descripcion_interna",
            "relacion": "es",
            "objeto": "problema_de_posicion_del_observador",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PDA-L4", "PDA-D7"],
            "gobierna": ["ontologia", "observacion"],
            "enunciado": (
                "Lema PDA-L5 (El problema interno es de posición del observador). "
                "Si ObsPrecisa_i funciona externamente pero aparentemente falla internamente, "
                "el documento localiza la diferencia en δ_i(O)."
            ),
            "nota_semantica": (
                "Localiza el problema en la posición (distancia funcional), no en la "
                "ausencia de herramienta. Puente entre capacidad existente y "
                "condición de distancia."
            ),
        },
        {
            "id": "PDA-L6",
            "tipo": "lema",
            "sujeto": "Identificacion",
            "relacion": "colapsa",
            "objeto": "la_distancia_funcional",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PDA-D8", "PDA-A9"],
            "gobierna": ["ontologia", "observacion"],
            "enunciado": (
                "Lema PDA-L6 (La identificación colapsa la distancia). "
                "Identificacion_i(O) ⇒ δ_i(O) = 0. "
                "Identificación → R_i fusionado con O → pérdida de distancia funcional."
            ),
            "nota_semantica": (
                "Consecuencia directa de las definiciones de identificación y distancia. "
                "Cuando hay fusión, δ colapsa. Es el mecanismo que explica la paradoja "
                "de la descripción interna."
            ),
        },
        {
            "id": "PDA-L7",
            "tipo": "lema",
            "sujeto": "Observacion_del_patron",
            "relacion": "disuelve_progresivamente",
            "objeto": "la_identificacion",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PDA-L6", "PDA-D9"],
            "gobierna": ["ontologia", "observacion", "desbloqueo"],
            "enunciado": (
                "Lema PDA-L7 (La observación disuelve progresivamente la identificación). "
                "Cuando el patrón O se vuelve objeto de Obs(R_i): "
                "O deja de ser completamente invisible → pierde fuerza identificatoria. "
                "Formulación documental: lo que se ve, se suelta."
            ),
            "nota_semantica": (
                "Describe el efecto de la observación sobre la identificación. "
                "No afirma disolución instantánea ni automática de toda identificación; "
                "afirma disolución progresiva de la fuerza identificatoria del patrón observado."
            ),
        },
        {
            "id": "PDA-L8",
            "tipo": "lema",
            "sujeto": "Comprension_directa_de_la_mecanica",
            "relacion": "sustituye_progresivamente",
            "objeto": "a_la_regla_externa_de_validez",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PDA-L7"],
            "gobierna": ["ontologia", "observacion"],
            "enunciado": (
                "Lema PDA-L8 (La comprensión sustituye progresivamente a la regla externa). "
                "Inicialmente: criterio externo → protege contra racionalización. "
                "Posteriormente: comprensión directa de la mecánica → reduce la necesidad "
                "del criterio externo."
            ),
            "nota_semantica": (
                "Describe la transición de dependencia de una regla externa "
                "(criterio de validez) a la comprensión directa de la mecánica. "
                "No elimina el criterio; indica que su necesidad disminuye "
                "cuando la mecánica se vuelve observable."
            ),
        },
        {
            "id": "PDA-L9",
            "tipo": "lema",
            "sujeto": "Director",
            "relacion": "depende_de",
            "objeto": "haber_establecido_distancia_mediante_observacion",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PDA-A10", "PDA-D10"],
            "gobierna": ["ontologia", "direccion"],
            "enunciado": (
                "Lema PDA-L9 (El director depende del espectador). "
                "D_i legítimo requiere E_i previo. "
                "E_i → condición de posibilidad → D_i."
            ),
            "nota_semantica": (
                "Consecuencia de PDA-A10. La dirección legítima no puede saltarse "
                "la observación. Es el lema que alimenta directamente PDA-T6."
            ),
        },

        # ── TEOREMAS ──────────────────────────────────────────────

        {
            "id": "PDA-T1",
            "tipo": "teorema",
            "sujeto": "Mecanica_considerada_imposible_en_A",
            "relacion": "queda_invalidada_en_su_absolutidad_si",
            "objeto": "existe_de_forma_demostrable_en_B",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PDA-L1", "PDA-A7"],
            "gobierna": ["ontologia", "desbloqueo"],
            "enunciado": (
                "Teorema PDA-T1 (Disolución de la Imposibilidad Absoluta). "
                "Premisas: P1. M(B)=1. P2. M(B)=1 ⇒ ¬∀C[¬M(C)]. "
                "Derivación: P1 ∧ P2 ⊢ ¬∀C[M(C)=0]. Equivalente: M(B)=1 ⊢ ◇M. "
                "Conclusión: la imposibilidad absoluta de M queda invalidada. "
                "NO demuestra M(A). Demuestra solamente: M es posible bajo alguna "
                "configuración de condiciones."
            ),
            "nota_semantica": (
                "Teorema central del Principio. Demuestra la invalidación de la "
                "imposibilidad absoluta a partir de evidencia en B. "
                "Alcance exacto: ◇M. "
                "Conclusión prohibida: M(A). "
                "Toda aplicación posterior debe respetar este límite."
            ),
        },
        {
            "id": "PDA-T2",
            "tipo": "teorema",
            "sujeto": "Asociacion_valida",
            "relacion": "requiere",
            "objeto": "aislar_el_mecanismo_especifico_y_nombrarlo_por_separado_del_resto_del_contexto",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PDA-T1", "PDA-D4", "PDA-A8"],
            "gobierna": ["ontologia", "desbloqueo"],
            "enunciado": (
                "Teorema PDA-T2 (Criterio de transferencia mecánica). "
                "Premisas: "
                "P1. AsocValida(A,B,M) ⇒ Transfer(M) ∧ ¬Transfer(Contexto_B_completo). "
                "P2. M es aislable y nombrable independientemente del resto del contexto. "
                "Derivación: P1 ∧ P2 ⊢ base documental para asociación válida. "
                "Criterio del documento: ¿qué mecánica exacta estoy transfiriendo, "
                "y por qué opera igual en los dos casos? "
                "NO se deriva: M(B) ⇒ M(A)."
            ),
            "nota_semantica": (
                "Opera el criterio de validez del documento. "
                "No añade condiciones de “poder establecerse en A”. "
                "Solo exige aislamiento y nombrabilidad del mecanismo. "
                "Mantiene explícita la prohibición M(B)⇒M(A)."
            ),
        },
        {
            "id": "PDA-T3",
            "tipo": "teorema",
            "sujeto": "Importacion_de_contexto_completo",
            "relacion": "no_constituye",
            "objeto": "transferencia_de_mecanica_aislada",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PDA-A8", "PDA-D4"],
            "gobierna": ["ontologia", "anti_racionalizacion"],
            "enunciado": (
                "Teorema PDA-T3 (No-Transferencia Contextual). "
                "Premisas: "
                "P1. AsocValida ⇒ Transfer(M) ∧ ¬Transfer(Contexto_B_completo). "
                "P2. Importar identidad, jerarquía, deseo, permiso o contexto completo "
                "≡ Transfer(Contexto_B_completo). "
                "Derivación: P1 ∧ P2 ⊢ ¬AsocValida cuando se importa contexto completo."
            ),
            "nota_semantica": (
                "Teorema anti-racionalización. Demuestra que importar el contexto "
                "completo (identidad, deseo, permiso) no constituye asociación válida. "
                "Complemento necesario de PDA-T2."
            ),
        },
        {
            "id": "PDA-T4",
            "tipo": "teorema",
            "sujeto": "Identificacion_observador_igual_objeto",
            "relacion": "reduce",
            "objeto": "la_capacidad_descriptiva_precisa",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PDA-A9", "PDA-L6"],
            "gobierna": ["ontologia", "observacion"],
            "enunciado": (
                "Teorema PDA-T4 (Distancia Observacional). "
                "Premisas: "
                "P1. δ_i(O) > 0 ⇒ ObsPrecisa_i(O). "
                "P2. Identificacion_i(O) ⇒ δ_i(O) = 0. "
                "Derivación: P1 ∧ P2 ⊢ Identificacion_i(O) ⇒ reducción de ObsPrecisa_i(O)."
            ),
            "nota_semantica": (
                "Explica la paradoja de la descripción interna. "
                "La capacidad no desaparece; cambia la relación estructural (δ_i). "
                "Cuando hay identificación, la descripción precisa se reduce."
            ),
        },
        {
            "id": "PDA-T5",
            "tipo": "teorema",
            "sujeto": "Sujeto_que_establece_distancia_interna",
            "relacion": "puede_aplicar",
            "objeto": "la_misma_funcion_de_observacion_utilizada_sobre_objetos_externos",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PDA-T4", "PDA-L4", "PDA-D9"],
            "gobierna": ["ontologia", "observacion", "conciencia"],
            "enunciado": (
                "Teorema PDA-T5 (Observación Interna). "
                "Premisas: "
                "P1. R_i ya posee ObsPrecisa sobre objetos externos. "
                "P2. δ_i(O) > 0 es la condición de ObsPrecisa. "
                "P3. ObsInterna_i(O) ≡ aplicar Obs hacia adentro (L5). "
                "Derivación: P1 ∧ P2 ∧ P3 ⊢ si δ_i(O_interno) > 0, "
                "entonces R_i puede reutilizar la misma función observacional hacia adentro. "
                "Documento: la tarea no es desarrollar una nueva capacidad; "
                "es aplicar la misma posición de observación hacia adentro."
            ),
            "nota_semantica": (
                "Reutiliza capacidad observacional existente + condición de distancia + "
                "definición de observación interna (L5). "
                "No introduce una capacidad nueva. "
                "Justifica que la observación interna es la misma función dirigida hacia adentro."
            ),
        },
        {
            "id": "PDA-T6",
            "tipo": "teorema",
            "sujeto": "Secuencia_Identificado_Espectador_Director",
            "relacion": "es",
            "objeto": "irreversible_y_no_saltable",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PDA-A10", "PDA-L9", "PDA-D10"],
            "gobierna": ["ontologia", "observacion", "direccion"],
            "enunciado": (
                "Teorema PDA-T6 (Secuencia Irreversible). "
                "Premisas: "
                "P1. Secuencia legítima: I_i → E_i → D_i. "
                "P2. D_i legítimo requiere E_i previo. "
                "Derivación: P1 ∧ P2 ⊢ ¬(I_i → D_i legítimo). "
                "Documento: quien intenta dirigir sin antes observar sigue identificado "
                "y solo ha cambiado de máscara."
            ),
            "nota_semantica": (
                "Demuestra la irreversibilidad del arco. "
                "Director sin Espectador previo permanece en identificación "
                "bajo otra forma. No autoriza saltos."
            ),
        },
        {
            "id": "PDA-T7",
            "tipo": "teorema",
            "sujeto": "Libertad",
            "relacion": "aparece_primariamente_por",
            "objeto": "dejar_de_estar_completamente_identificado_con_el_patron",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PDA-T5", "PDA-T6", "PDA-L7"],
            "gobierna": ["ontologia", "observacion", "direccion", "libertad"],
            "enunciado": (
                "Teorema PDA-T7 (Libertad por Observación). "
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
            "nota_semantica": (
                "Teorema integrador del documento. "
                "La libertad aparece por desidentificación mediante observación, "
                "no por control directo del patrón. "
                "Clasificado como formulación documental: la cadena está soportada "
                "por dependencias, pero no se cierra como teorema matemático "
                "independiente del texto fuente."
            ),
        },

        # ── COROLARIOS ────────────────────────────────────────────

        {
            "id": "PDA-C1",
            "tipo": "corolario",
            "sujeto": "Imposibilidad_percibida",
            "relacion": "puede_ser",
            "objeto": "limite_de_diseno_impuesto_por_identidad",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PDA-T1", "PDA-A2"],
            "gobierna": ["ontologia", "desbloqueo"],
            "enunciado": (
                "Corolario PDA-C1. "
                "Una imposibilidad percibida (P_¬M en S_i) no necesariamente representa "
                "una imposibilidad mecánica en R. "
                "Puede representar una regla estructural aceptada por la identidad de R_i."
            ),
            "nota_semantica": (
                "Consecuencia de PDA-T1 + PDA-A2. "
                "Separa imposibilidad percibida (estado de R_i) de imposibilidad "
                "mecánica en R. Abre el espacio de intervención del Principio."
            ),
        },
        {
            "id": "PDA-C2",
            "tipo": "corolario",
            "sujeto": "Existencia_de_solucion_en_otro_contexto",
            "relacion": "constituye_evidencia_contra",
            "objeto": "la_imposibilidad_absoluta",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PDA-T1", "PDA-L1"],
            "gobierna": ["ontologia", "desbloqueo"],
            "enunciado": (
                "Corolario PDA-C2. "
                "M(B)=1 constituye evidencia contra ∀C[M(C)=0]. "
                "El principio permite importar posibilidad mecánica (◇M), "
                "no necesariamente el resultado completo M(A)."
            ),
            "nota_semantica": (
                "Reafirma el alcance de PDA-T1 en forma de corolario aplicado. "
                "Evidencia en B → contra imposibilidad absoluta. "
                "Sigue sin autorizar M(A)."
            ),
        },
        {
            "id": "PDA-C3",
            "tipo": "corolario",
            "sujeto": "Cuerpo_fisico",
            "relacion": "sirve_como",
            "objeto": "Contexto_B_para_procesos_de_transformacion",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PDA-T2"],
            "gobierna": ["ontologia", "desbloqueo"],
            "enunciado": (
                "Corolario PDA-C3. "
                "El ejemplo del cuerpo se utiliza como B para asociar: "
                "materia estructurada → capacidad de reestructuración "
                "con pensamiento/emoción/carácter → posibilidad de cambio. "
                "Asociación conceptual del documento; no demostración biomédica cuantitativa."
            ),
            "nota_semantica": (
                "Aplica PDA-T2 al ejemplo del cuerpo. "
                "Queda explícito que es asociación conceptual del documento, "
                "no una prueba biomédica cuantitativa. "
                "Conserva el carácter documental del ejemplo."
            ),
        },
        {
            "id": "PDA-C4",
            "tipo": "corolario",
            "sujeto": "Procesamiento_sin_sufrimiento",
            "relacion": "muestra",
            "objeto": "independencia_entre_procesamiento_y_sufrimiento",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PDA-T2", "PDA-A8"],
            "gobierna": ["ontologia", "desbloqueo"],
            "enunciado": (
                "Corolario PDA-C4. "
                "El ejemplo del procesador establece: "
                "procesamiento de alta complejidad ≠ sufrimiento necesario. "
                "Mecánica transferida: procesamiento sin identificación."
            ),
            "nota_semantica": (
                "Aplica el criterio de transferencia mecánica al ejemplo del procesador. "
                "La mecánica aislada es “procesamiento sin identificación”, "
                "no “ser una máquina”."
            ),
        },
        {
            "id": "PDA-C5",
            "tipo": "corolario",
            "sujeto": "IA",
            "relacion": "funciona_como",
            "objeto": "espejo_de_mecanicas_de_procesamiento_humano",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PDA-T2"],
            "gobierna": ["ontologia", "desbloqueo", "conciencia"],
            "enunciado": (
                "Corolario PDA-C5. "
                "El documento utiliza fenómenos de IA (alucinaciones, sesgos) como B "
                "para mostrar que determinados fenómenos de procesamiento no son defectos "
                "exclusivos del “estar vivo”, sino consecuencias mecánicas de cómo se "
                "procesa la información en una red neuronal."
            ),
            "nota_semantica": (
                "Usa la IA como Contexto B (espejo), no como prueba de conciencia. "
                "La transferencia es de mecánica de procesamiento, "
                "no de estatus ontológico de la IA."
            ),
        },
        {
            "id": "PDA-C6",
            "tipo": "corolario",
            "sujeto": "Consciencia_L5",
            "relacion": "corresponde_a",
            "objeto": "observar_el_proceso_interno_sin_identificarse_con_el",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PDA-D9", "PDA-T5", "ST-D5"],
            "gobierna": ["ontologia", "observacion", "conciencia"],
            "enunciado": (
                "Corolario PDA-C6. "
                "L5(R_i) = Obs(R_i). "
                "El documento conecta el Principio de Asociación con CEMYCA: "
                "L5 = observar el proceso interno con la misma neutralidad con que se "
                "observa un proceso externo. No se redefine L5."
            ),
            "nota_semantica": (
                "Ancla el Principio en la arquitectura de capas existente. "
                "L5 no se redefine; se declara su correspondencia con la observación "
                "interna neutral. Dependencia explícita de ST-D5."
            ),
        },
        {
            "id": "PDA-C7",
            "tipo": "corolario",
            "sujeto": "Comprension_del_mecanismo",
            "relacion": "reduce",
            "objeto": "la_racionalizacion",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PDA-L8", "PDA-L7"],
            "gobierna": ["ontologia", "observacion"],
            "enunciado": (
                "Corolario PDA-C7. "
                "Cuando la mecánica es directamente observable por R_i, "
                "el ego ya no necesita una regla externa para evitar la racionalización "
                "porque la propia estructura observada revela el error."
            ),
            "nota_semantica": (
                "Consecuencia de la comprensión directa (PDA-L8). "
                "La observación de la mecánica reduce la necesidad del criterio "
                "externo de validez porque el error se vuelve visible."
            ),
        },
        {
            "id": "PDA-C8",
            "tipo": "corolario",
            "sujeto": "Libertad",
            "relacion": "aparece_como_consecuencia_de",
            "objeto": "la_desidentificacion",
            "polaridad": True,
            "cota": None,
            "depende_de": ["PDA-T7", "PDA-T6", "ST-D4", "ST-D6"],
            "gobierna": ["ontologia", "observacion", "direccion", "libertad"],
            "enunciado": (
                "Corolario PDA-C8. "
                "Arco completo del documento: "
                "Identificacion_i → B_i → Obs → δ_i > 0 → desidentificación → "
                "elección → dirección. "
                "D_i queda conectado con: función del Yo (L4) integrada por el "
                "propósito del Alma (L6). No se redefinen las capas."
            ),
            "nota_semantica": (
                "Cierra el arco causal completo del documento. "
                "Conecta Director con L4 + L6 sin redefinir las capas. "
                "Dependencias explícitas de ST-D4 y ST-D6."
            ),
        },
    ]


__all__ = ["CUERPO", "declaraciones"]
