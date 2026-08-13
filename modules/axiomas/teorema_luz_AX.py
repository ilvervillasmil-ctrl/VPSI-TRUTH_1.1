# ===============================================================
# modules/axiomas/teorema_luz_AX.py
# Cuerpo axiomático: Teorema de la Luz como Proyección
# Fundamental de Observabilidad
#
# FUENTE NORMATIVA ÚNICA:
#   Teorema de la Luz como Proyección Fundamental de Observabilidad
#   Formalización Completa — UCF v3.3
#   Autor: Ilver Villasmil
#   Marco: Unified Coherence Framework (UCF) — Villasmil-Omega
#   2026
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
Cuerpo axiomático: Teorema de la Luz como Proyección
Fundamental de Observabilidad

Paper fuente:
  Teorema de la Luz como Proyección Fundamental de Observabilidad
  Formalización Completa — UCF v3.3
  Autor: Ilver Villasmil
  Marco: Unified Coherence Framework (UCF) — Villasmil-Omega
  2026

Partes del Paper representadas:
  Parte I   — Definiciones Fundamentales (1–7)
  Parte II  — Axiomas de la Luz (L1–L8)
  Parte III — Lemas (L1–L8)
  Parte IV  — Teorema Principal
  Parte V   — Acoplamiento con F3
  Parte VI  — Percepción y Luz
  Parte VII — Corolarios (L1–L5)
  Parte VIII — Cierre Estructural
  Teorema Final

Constantes citadas (solo referencia; autoridad en CT):
  α = 26/27
  β = 1/27
  2·α·β = 52/729

Numeración canónica del Paper conservada.
No se redefine ninguna constante oficial de CT.
"""

from __future__ import annotations

from typing import Any, Dict, List

CUERPO = {
    "nombre": "teorema_luz",
    "version": "1.0",
}


def declaraciones() -> List[Dict[str, Any]]:
    return [

        # ==========================================================
        # Parte I — Definición 1 (R)
        # ==========================================================
        {
            "id": "TL-D1",
            "tipo": "definicion",
            "sujeto": "R",
            "relacion": "denota",
            "objeto": "realidad_total",
            "polaridad": True,
            "cota": None,
            "depende_de": [],
            "gobierna": ["ontologia", "luz"],
            "enunciado": (
                "Definición 1. R denota la realidad total, es decir, el conjunto de todas las "
                "situaciones, estados y objetos que existen fuera de la interpretación de cualquier "
                "sistema observador."
            ),
        },

        # ==========================================================
        # Parte I — Definición 2 (F3)
        # ==========================================================
        {
            "id": "TL-D2",
            "tipo": "definicion",
            "sujeto": "F3",
            "relacion": "denota",
            "objeto": "forma_tridimensional",
            "polaridad": True,
            "cota": None,
            "depende_de": [],
            "gobierna": ["ontologia", "luz", "forma"],
            "enunciado": (
                "Definición 2. F3 denota una forma tridimensional, entendida como una entidad con "
                "volumen, extensión en el espacio y capacidad de ser manipulada o medible como objeto "
                "material. Toda materia, toda superficie, todo cuerpo físico observable se describe como F3."
            ),
        },

        # ==========================================================
        # Parte I — Definición 3 (P2)
        # ==========================================================
        {
            "id": "TL-D3",
            "tipo": "definicion",
            "sujeto": "P2",
            "relacion": "denota",
            "objeto": "proyeccion_sin_volumen_dependiente_de_F3",
            "polaridad": True,
            "cota": None,
            "depende_de": ["TL-D2"],
            "gobierna": ["ontologia", "luz", "forma"],
            "enunciado": (
                "Definición 3. P2 denota una proyección sin volumen, dependiente de F3. Es una "
                "restricción geométrica que se genera al imponer condiciones sobre una forma "
                "tridimensional: rendijas, aberturas, planos, pantallas, lentes, o cualquier "
                "configuración que filtre o redirija la acción de un objeto 3D. No tiene espesor "
                "ni masa; solo estructura y posición."
            ),
        },

        # ==========================================================
        # Parte I — Definición 4 (C1)
        # ==========================================================
        {
            "id": "TL-D4",
            "tipo": "definicion",
            "sujeto": "C1",
            "relacion": "denota",
            "objeto": "contorno_derivado_de_P2",
            "polaridad": True,
            "cota": None,
            "depende_de": ["TL-D3"],
            "gobierna": ["ontologia", "luz", "forma"],
            "enunciado": (
                "Definición 4. C1 denota el contorno derivado de P2, entendido como la frontera "
                "unidimensional que separa la proyección de su entorno. Es el borde perceptible o "
                "medible de una proyección, no una entidad independiente, sino una consecuencia "
                "geométrica de la restricción P2."
            ),
        },

        # ==========================================================
        # Parte I — Definición 5 (S)
        # ==========================================================
        {
            "id": "TL-D5",
            "tipo": "definicion",
            "sujeto": "S",
            "relacion": "denota",
            "objeto": "sistema_observador",
            "polaridad": True,
            "cota": None,
            "depende_de": [],
            "gobierna": ["ontologia", "luz", "epistemologia"],
            "enunciado": (
                "Definición 5. S denota el sistema observador, cualquier dispositivo, organismo o "
                "sistema de detección capaz de registrar señales de R. No presupone conciencia en "
                "sentido clásico, solo capacidad de medir o registrar interacciones con el entorno."
            ),
        },

        # ==========================================================
        # Parte I — Definición 6 (Ri(S))
        # ==========================================================
        {
            "id": "TL-D6",
            "tipo": "definicion",
            "sujeto": "Ri_S",
            "relacion": "denota",
            "objeto": "realidad_interpretada_por_S",
            "polaridad": True,
            "cota": None,
            "depende_de": ["TL-D5"],
            "gobierna": ["ontologia", "luz", "epistemologia"],
            "enunciado": (
                "Definición 6. Ri(S) denota la realidad interpretada por S, es decir, la "
                "representación interna que S construye a partir de sus mediciones sobre R. No es "
                "la realidad misma, sino el modelo que el sistema observador infiere."
            ),
        },

        # ==========================================================
        # Parte I — Definición 7 (L)
        # ==========================================================
        {
            "id": "TL-D7",
            "tipo": "definicion",
            "sujeto": "L",
            "relacion": "denota",
            "objeto": "luz_como_proyeccion_estructural",
            "polaridad": True,
            "cota": None,
            "depende_de": ["TL-D2", "TL-D3"],
            "gobierna": ["ontologia", "luz"],
            "enunciado": (
                "Definición 7. L denota la luz, entendida aquí no como una forma tridimensional, "
                "sino como una proyección estructural generada por una fuente tridimensional, "
                "cuya función es habilitar la observabilidad de R para S."
            ),
        },

        # ==========================================================
        # Parte II — Axioma 1 (L1: Origen tridimensional)
        # ==========================================================
        {
            "id": "TL-A1",
            "tipo": "axioma",
            "sujeto": "Toda_luz_L",
            "relacion": "es_generada_por",
            "objeto": "fuente_tridimensional_F3",
            "polaridad": True,
            "cota": None,
            "depende_de": ["TL-D7", "TL-D2"],
            "gobierna": ["ontologia", "luz"],
            "enunciado": (
                "Axioma 1 (L1: Origen tridimensional). Toda luz L es generada por una fuente "
                "tridimensional F3. Formalmente, L = P2(F3,fuente), donde F3,fuente es un objeto "
                "material que emite radiación, y P2(F3,fuente) denota la proyección estructural de "
                "esa fuente. La luz, por tanto, no surge de la nada, sino como consecuencia de la "
                "acción de un objeto 3D."
            ),
        },

        # ==========================================================
        # Parte II — Axioma 2 (L2: No tridimensionalidad)
        # ==========================================================
        {
            "id": "TL-A2",
            "tipo": "axioma",
            "sujeto": "Luz_L",
            "relacion": "no_pertenece_a",
            "objeto": "F3",
            "polaridad": True,
            "cota": None,
            "depende_de": ["TL-D7", "TL-D2"],
            "gobierna": ["ontologia", "luz"],
            "enunciado": (
                "Axioma 2 (L2: No tridimensionalidad). La luz no posee volumen ni extensión sólida. "
                "Formalmente, L ∉ F3. No hay en L una forma rígida, discreta o independiente; su "
                "naturaleza es esencialmente proyectiva. Todo lo que se atribuye a la luz como "
                "“forma” proviene de la geometría de la fuente y de la restricción sobre la que se "
                "proyecta."
            ),
        },

        # ==========================================================
        # Parte II — Axioma 3 (L3: Dependencia ontológica)
        # ==========================================================
        {
            "id": "TL-A3",
            "tipo": "axioma",
            "sujeto": "Luz_L",
            "relacion": "depende_de",
            "objeto": "F3_y_P2",
            "polaridad": True,
            "cota": None,
            "depende_de": ["TL-A1", "TL-A2"],
            "gobierna": ["ontologia", "luz"],
            "enunciado": (
                "Axioma 3 (L3: Dependencia ontológica). La luz no existe independientemente de una "
                "fuente tridimensional ni de una proyección. Formalmente, L ⊂ P2 ⇒ depende de F3. "
                "Esto significa que la luz es una consecuencia funcional de la existencia de F3 y "
                "de la geometría de P2. Sin un objeto emisor ni una restricción que lo filtre, no "
                "hay luz en el sentido que aquí se define."
            ),
        },

        # ==========================================================
        # Parte II — Axioma 4 (L4: Condición de observabilidad)
        # ==========================================================
        {
            "id": "TL-A4",
            "tipo": "axioma",
            "sujeto": "Percepcion_visual_Ri_S",
            "relacion": "presupone",
            "objeto": "presencia_de_luz_L",
            "polaridad": True,
            "cota": None,
            "depende_de": ["TL-D6", "TL-D7"],
            "gobierna": ["ontologia", "luz", "epistemologia"],
            "enunciado": (
                "Axioma 4 (L4: Condición de observabilidad). La percepción visual Ri(S)visual "
                "presupone la presencia de luz L: Ri(S)visual ⇒ L. Sin luz, no hay señal para el "
                "sistema observador; sin señal, no hay contenido visual en Ri(S). La luz actúa "
                "como condición necesaria, no como una propiedad adicional, de la observabilidad "
                "visual."
            ),
        },

        # ==========================================================
        # Parte II — Axioma 5 (L5: Dependencia de interacción)
        # ==========================================================
        {
            "id": "TL-A5",
            "tipo": "axioma",
            "sujeto": "Luz_L",
            "relacion": "solo_es_observable_si_interactua_con",
            "objeto": "F3_o_S",
            "polaridad": True,
            "cota": None,
            "depende_de": ["TL-A2"],
            "gobierna": ["ontologia", "luz"],
            "enunciado": (
                "Axioma 5 (L5: Dependencia de interacción). La luz solo es observable si interactúa "
                "con un objeto tridimensional o con un sistema de detección. Formalmente, "
                "L → (F3 ∪ S), donde la flecha indica que toda observación de L requiere su "
                "interacción con F3 o con S. No es posible “ver la luz en sí misma” sin que medie "
                "un objeto 3D o un sistema de medición sensible."
            ),
        },

        # ==========================================================
        # Parte II — Axioma 6 (L6: Detectabilidad para el sistema)
        # ==========================================================
        {
            "id": "TL-A6",
            "tipo": "axioma",
            "sujeto": "Luz_L",
            "relacion": "solo_existe_para_S_si",
            "objeto": "es_detectable_por_S",
            "polaridad": True,
            "cota": None,
            "depende_de": ["TL-A5", "TL-D5"],
            "gobierna": ["ontologia", "luz", "epistemologia"],
            "enunciado": (
                "Axioma 6 (L6: Detectabilidad para el sistema). La luz solo existe para el sistema "
                "observador S si es detectable por él. Formalmente, I(R; L) > 0 ⇒ L ∈ Ri(S), "
                "donde I(R; L) denota la información mutua entre la realidad R y la luz L. Si no "
                "hay transferencia de información relevante, no hay luz en Ri(S), aunque L exista "
                "en R."
            ),
        },

        # ==========================================================
        # Parte II — Axioma 7 (L7: Acoplamiento bidireccional)
        # ==========================================================
        {
            "id": "TL-A7",
            "tipo": "axioma",
            "sujeto": "Proyeccion_P2_y_forma_F3",
            "relacion": "se_acoplan_de_forma",
            "objeto": "reciproca",
            "polaridad": True,
            "cota": "52/729",
            "depende_de": ["TL-D3", "TL-D2"],
            "gobierna": ["ontologia", "luz", "forma", "constantes"],
            "enunciado": (
                "Axioma 7 (L7: Acoplamiento bidireccional). La proyección P2 y la forma "
                "tridimensional F3 se acoplan de forma recíproca: P2 ↔ F3. La luz, como "
                "proyección, modifica la distribución de energía en F3, y F3 influye a su vez "
                "en la geometría y la intensidad de la luz. "
                "Formalización energética: E² = α² p² c² + 2 α β p m c³ + β² m² c⁴. "
                "El término cruzado 2 α β p m c³ representa la contribución del acoplamiento. "
                "En el caso de α = 26/27 y β = 1/27 se obtiene 2 α β = 52/729."
            ),
        },

        # ==========================================================
        # Parte II — Axioma 8 (L8: Percepción como proyección)
        # ==========================================================
        {
            "id": "TL-A8",
            "tipo": "axioma",
            "sujeto": "Realidad_interpretada_Ri_S",
            "relacion": "es",
            "objeto": "proyeccion_de_la_realidad_total",
            "polaridad": True,
            "cota": None,
            "depende_de": ["TL-D6"],
            "gobierna": ["ontologia", "luz", "epistemologia"],
            "enunciado": (
                "Axioma 8 (L8: Percepción como proyección). La realidad interpretada por el sistema "
                "S es una proyección de la realidad total: Ri(S) = Pi(S)(R), donde Pi(S) denota la "
                "función de interpretación que convierte los datos de R en una representación "
                "interna para S."
            ),
        },

        # ==========================================================
        # Parte III — Lema 1 (L1: Invisibilidad en vacío)
        # ==========================================================
        {
            "id": "TL-L1",
            "tipo": "lema",
            "sujeto": "Luz_L_sin_interaccion",
            "relacion": "no_forma_parte_de",
            "objeto": "Ri_S",
            "polaridad": True,
            "cota": None,
            "depende_de": ["TL-A5", "TL-A6"],
            "gobierna": ["ontologia", "luz"],
            "enunciado": (
                "Lema 1 (L1: Invisibilidad en vacío). Si la luz L no interactúa con ningún objeto "
                "tridimensional F3 ni con el sistema observador S, entonces no forma parte de la "
                "realidad interpretada por S: L ∉ Ri(S). Esto significa que, en un vacío absoluto "
                "sin medios ni detectores, la luz no es observable ni significativa para el sistema, "
                "aunque pueda existir en la realidad R."
            ),
        },

        # ==========================================================
        # Parte III — Lema 2 (L2: Forma inducida)
        # ==========================================================
        {
            "id": "TL-L2",
            "tipo": "lema",
            "sujeto": "Forma_percibida_de_la_luz",
            "relacion": "no_es_propiedad_intrinseca_sino",
            "objeto": "funcion_de_fuente_medio_y_sistema",
            "polaridad": True,
            "cota": None,
            "depende_de": ["TL-A2"],
            "gobierna": ["ontologia", "luz"],
            "enunciado": (
                "Lema 2 (L2: Forma inducida). La forma percibida de la luz no es una propiedad "
                "intrínseca de L, sino función de la fuente, del medio y del sistema: "
                "Forma(L) = f(F3,fuente, F3,medio, S). La luz no tiene forma propia; la apariencia "
                "geométrica que se le atribuye es el resultado de cómo la fuente emite, cómo el "
                "medio filtra y cómo S interpreta la señal recibida."
            ),
        },

        # ==========================================================
        # Parte III — Lema 3 (L3: Equivalencia estructural con P2)
        # ==========================================================
        {
            "id": "TL-L3",
            "tipo": "lema",
            "sujeto": "Luz_L",
            "relacion": "es_equivalente_a",
            "objeto": "P2",
            "polaridad": True,
            "cota": None,
            "depende_de": ["TL-A2", "TL-A3", "TL-D3"],
            "gobierna": ["ontologia", "luz", "forma"],
            "enunciado": (
                "Lema 3 (L3: Equivalencia estructural con P2). La luz cumple todas las propiedades "
                "que definen una proyección P2: no volumen, dependencia de un objeto tridimensional, "
                "naturaleza de proyección. Por tanto, se puede escribir: L ≡ P2. Esta equivalencia "
                "formaliza la idea de que la luz es, en el marco UCF, indistinguible de una "
                "proyección estructural derivada de F3."
            ),
        },

        # ==========================================================
        # Parte III — Lema 4 (L4: Observación indirecta)
        # ==========================================================
        {
            "id": "TL-L4",
            "tipo": "lema",
            "sujeto": "Toda_observacion_de_la_luz",
            "relacion": "es",
            "objeto": "observacion_de_interaccion_P2_con_F3",
            "polaridad": True,
            "cota": None,
            "depende_de": ["TL-A5", "TL-L3"],
            "gobierna": ["ontologia", "luz"],
            "enunciado": (
                "Lema 4 (L4: Observación indirecta). Toda observación de la luz es, en realidad, "
                "observación de una interacción entre la proyección P2 y un objeto tridimensional: "
                "Ver(L) = Ver(P2 ∩ F3). No hay “ver la luz en sí”; solo se ve la luz que se ha "
                "reflejado, dispersado o absorbido por un objeto 3D, o que ha interactuado con el "
                "sistema de detección."
            ),
        },

        # ==========================================================
        # Parte III — Lema 5 (L5: Dependencia del sistema)
        # ==========================================================
        {
            "id": "TL-L5",
            "tipo": "lema",
            "sujeto": "Ri_S",
            "relacion": "es",
            "objeto": "proyeccion_interpretativa_de_R",
            "polaridad": True,
            "cota": None,
            "depende_de": ["TL-A8"],
            "gobierna": ["ontologia", "luz", "epistemologia"],
            "enunciado": (
                "Lema 5 (L5: Dependencia del sistema). La realidad interpretada Ri(S) es una "
                "proyección de la realidad total R construida por el sistema S: Ri(S) = Pi(S)(R), "
                "donde Pi(S) es la proyección interpretativa de S. En consecuencia, la percepción "
                "de la luz L depende de las capacidades y de la sensibilidad de S."
            ),
        },

        # ==========================================================
        # Parte III — Lema 6 (L6: Capacidad de influencia)
        # ==========================================================
        {
            "id": "TL-L6",
            "tipo": "lema",
            "sujeto": "Luz",
            "relacion": "puede_modificar",
            "objeto": "F3_sin_ser_F3",
            "polaridad": True,
            "cota": None,
            "depende_de": ["TL-A7"],
            "gobierna": ["ontologia", "luz", "forma"],
            "enunciado": (
                "Lema 6 (L6: Capacidad de influencia). La luz puede modificar la distribución "
                "espacial y energética de F3 sin que la luz misma sea una parte constitutiva de "
                "la materia: La luz puede modificar F3 sin ser F3. Este lema refuerza la idea de "
                "que la luz actúa como canal de información y energía entre diferentes "
                "configuraciones de F3."
            ),
        },

        # ==========================================================
        # Parte III — Lema 7 (L7: Dependencia visual)
        # ==========================================================
        {
            "id": "TL-L7",
            "tipo": "lema",
            "sujeto": "Percepcion_visual_de_S",
            "relacion": "es_subconjunto_de",
            "objeto": "luz_disponible_en_el_entorno",
            "polaridad": True,
            "cota": None,
            "depende_de": ["TL-A4"],
            "gobierna": ["ontologia", "luz", "epistemologia"],
            "enunciado": (
                "Lema 7 (L7: Dependencia visual). La percepción visual de S es subconjunto de la "
                "luz disponible en el entorno: Ri(S)visual ⊆ L. Todo lo que se ve está mediado por "
                "la luz; sin ella, ningún contenido visual existe en Ri(S)."
            ),
        },

        # ==========================================================
        # Parte III — Lema 8 (L8: Relatividad perceptual)
        # ==========================================================
        {
            "id": "TL-L8",
            "tipo": "lema",
            "sujeto": "Distintos_sistemas",
            "relacion": "pueden_percibir",
            "objeto": "rangos_diferentes_de_luz",
            "polaridad": True,
            "cota": None,
            "depende_de": ["TL-L5"],
            "gobierna": ["ontologia", "luz", "epistemologia"],
            "enunciado": (
                "Lema 8 (L8: Relatividad perceptual). Distintos sistemas pueden percibir rangos "
                "diferentes de luz. Ri(S1) ≠ Ri(S2). La sensibilidad espectral, la resolución y la "
                "arquitectura del sistema determinan qué partes de la luz son realmente "
                "traducibles a experiencia visual."
            ),
        },

        # ==========================================================
        # Parte IV — Teorema 1 (Teorema de la Luz)
        # ==========================================================
        {
            "id": "TL-T1",
            "tipo": "teorema",
            "sujeto": "Luz_L",
            "relacion": "es",
            "objeto": "proyeccion_P2_funcional_no_material",
            "polaridad": True,
            "cota": None,
            "depende_de": ["TL-A1", "TL-A2", "TL-A3", "TL-A4", "TL-A5", "TL-L3"],
            "gobierna": ["ontologia", "luz"],
            "enunciado": (
                "Teorema 1 (Teorema de la Luz). Sea L la luz generada por una fuente tridimensional "
                "F3. Entonces se cumplen las siguientes propiedades: "
                "1. L no pertenece a F3. "
                "2. L es una proyección P2. "
                "3. L no es observable sin interacción con F3 o con S. "
                "4. L no posee forma intrínseca. "
                "5. L es condición necesaria de observabilidad visual. "
                "Por lo tanto, en el marco UCF, L ≡ P2(F3,fuente), y la existencia de la luz es "
                "funcional, no material: actúa como proyección de la fuente, no como objeto "
                "tridimensional independiente."
            ),
        },

        # ==========================================================
        # Parte V — Teorema 2 (Acoplamiento de la luz)
        # ==========================================================
        {
            "id": "TL-T2",
            "tipo": "teorema",
            "sujeto": "Luz",
            "relacion": "participa_en_la_dinamica_material_mediante",
            "objeto": "termino_cruzado_2_alpha_beta",
            "polaridad": True,
            "cota": "52/729",
            "depende_de": ["TL-A7", "TL-L6"],
            "gobierna": ["ontologia", "luz", "forma", "constantes"],
            "enunciado": (
                "Teorema 2 (L2: Acoplamiento de la luz). La luz participa en la dinámica material "
                "mediante el término cruzado 2αβ, que cuantifica su capacidad de redistribuir la "
                "energía y la información sin constituir una forma tridimensional en sí. "
                "2αβ = 52/729."
            ),
        },

        # ==========================================================
        # Parte VI — Teorema 3 (Luz como interfaz)
        # ==========================================================
        {
            "id": "TL-T3",
            "tipo": "teorema",
            "sujeto": "Luz",
            "relacion": "es_el_canal_que_conecta",
            "objeto": "F3_con_Ri_S",
            "polaridad": True,
            "cota": None,
            "depende_de": ["TL-T1", "TL-A8", "TL-L7"],
            "gobierna": ["ontologia", "luz", "epistemologia"],
            "enunciado": (
                "Teorema 3 (L3: Luz como interfaz). La luz es el canal que conecta F3 con Ri(S). "
                "F3 → L → Ri(S). Entre la realidad material y la realidad interpretada, la luz "
                "actúa como interfaz estructural, sin contribuir con una forma propia, sino con "
                "una proyección dependiente de la fuente y del medio."
            ),
        },

        # ==========================================================
        # Parte VII — Corolario 1 (Paradoja resuelta)
        # ==========================================================
        {
            "id": "TL-C1",
            "tipo": "corolario",
            "sujeto": "Luz",
            "relacion": "es",
            "objeto": "condicion_de_vision",
            "polaridad": True,
            "cota": None,
            "depende_de": ["TL-T1", "TL-L4"],
            "gobierna": ["ontologia", "luz"],
            "enunciado": (
                "Corolario 1 (L1: Paradoja resuelta). No es posible ver la luz en sí misma, porque "
                "la luz no es un objeto de la realidad que se distinga de la condición de la visión. "
                "Formalmente: L = condición de visión. Ver la luz implica ver la interacción de la "
                "luz con un objeto 3D."
            ),
        },

        # ==========================================================
        # Parte VII — Corolario 2 (Oscuridad)
        # ==========================================================
        {
            "id": "TL-C2",
            "tipo": "corolario",
            "sujeto": "Ausencia_de_luz",
            "relacion": "implica",
            "objeto": "ausencia_de_percepcion_visual",
            "polaridad": True,
            "cota": None,
            "depende_de": ["TL-A4", "TL-L7"],
            "gobierna": ["ontologia", "luz"],
            "enunciado": (
                "Corolario 2 (L2: Oscuridad). La ausencia de luz implica la ausencia de percepción "
                "visual. Formalmente: L = 0 ⇒ Ri(S)visual = 0. Cuando no hay luz medible o "
                "detectable por el sistema S, no hay contenido visual en la realidad interpretada."
            ),
        },

        # ==========================================================
        # Parte VII — Corolario 3 (Haz visible)
        # ==========================================================
        {
            "id": "TL-C3",
            "tipo": "corolario",
            "sujeto": "Haz_de_luz_visible",
            "relacion": "requiere",
            "objeto": "interaccion_con_F3",
            "polaridad": True,
            "cota": None,
            "depende_de": ["TL-A5", "TL-L4"],
            "gobierna": ["ontologia", "luz"],
            "enunciado": (
                "Corolario 3 (L3: Haz visible). Un haz de luz visible solo es observable si interviene "
                "al menos un objeto tridimensional que dispersa, refleja o absorbe la luz en la "
                "dirección del sistema observador: Un haz visible ⇒ Interacción con F3. Un rayo de "
                "láser en el vacío puro no se ve."
            ),
        },

        # ==========================================================
        # Parte VII — Corolario 4 (Fuente determina luz)
        # ==========================================================
        {
            "id": "TL-C4",
            "tipo": "corolario",
            "sujeto": "Luz",
            "relacion": "esta_completamente_determinada_por",
            "objeto": "la_fuente_tridimensional",
            "polaridad": True,
            "cota": None,
            "depende_de": ["TL-A1", "TL-T1"],
            "gobierna": ["ontologia", "luz"],
            "enunciado": (
                "Corolario 4 (L4: Fuente determina luz). La luz está completamente determinada por "
                "la fuente tridimensional que la genera: L = P2(F3,fuente). Ni el medio ni el "
                "sistema pueden crear luz; solo pueden modificar, filtrar o medir la proyección de "
                "la fuente hacia Ri(S)."
            ),
        },

        # ==========================================================
        # Parte VII — Corolario 5 (No independencia)
        # ==========================================================
        {
            "id": "TL-C5",
            "tipo": "corolario",
            "sujeto": "Luz",
            "relacion": "no_existe_sin",
            "objeto": "fuente_o_medio_o_sistema",
            "polaridad": True,
            "cota": None,
            "depende_de": ["TL-A3", "TL-A5", "TL-A6"],
            "gobierna": ["ontologia", "luz"],
            "enunciado": (
                "Corolario 5 (L5: No independencia). No existe luz sin al menos una de las tres "
                "condiciones siguientes: una fuente F3, un medio o interacción con F3, o un sistema "
                "observador S. La ausencia de cualquiera de ellas hace que la luz no sea detectable "
                "ni significativa para el sistema."
            ),
        },

        # ==========================================================
        # Teorema Final (Teorema 4)
        # ==========================================================
        {
            "id": "TL-T4",
            "tipo": "teorema",
            "sujeto": "Luz",
            "relacion": "es",
            "objeto": "condicion_estructural_de_observabilidad",
            "polaridad": True,
            "cota": None,
            "depende_de": ["TL-T1", "TL-T2", "TL-T3", "TL-C1", "TL-C2", "TL-C3", "TL-C4", "TL-C5"],
            "gobierna": ["ontologia", "luz"],
            "enunciado": (
                "Teorema 4 (Teorema de la luz como condición estructural de observabilidad). "
                "Sea L la luz generada por una fuente tridimensional F3 en el marco UCF. Se deduce que: "
                "1. La luz no es una forma en sí dentro de la realidad R, sino una condición estructural "
                "que permite que las formas F3 sean observables. "
                "2. La luz no posee volumen, no existe independientemente de una fuente tridimensional "
                "y no tiene forma intrínseca. "
                "3. La existencia de la luz es relacional (se define entre F3 y S), su manifestación es "
                "proyectiva (L ≡ P2(F3)), y su función es mediar entre la realidad tridimensional F3 "
                "y la realidad interpretada Ri(S). "
                "Por tanto: L ∉ F3, L ≡ P2(F3,fuente), L → (Ri(S)visual). "
                "La luz no es una forma dentro de la realidad, sino la condición estructural que permite "
                "que las formas sean observables. No posee volumen, no es independiente y no tiene forma "
                "intrínseca. Su existencia es relacional, su manifestación es proyectiva y su función es "
                "mediar entre la realidad tridimensional y la percepción del sistema."
            ),
        },
    ]


__all__ = ["CUERPO", "declaraciones"]
