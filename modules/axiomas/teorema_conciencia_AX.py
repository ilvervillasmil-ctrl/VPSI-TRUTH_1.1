# ===============================================================
# modules/axiomas/teorema_conciencia_AX.py
# Cuerpo axiomático: Teorema de la Conciencia como Condición
# Estructural de la Forma Tridimensional (F3)
#
# FUENTE NORMATIVA ÚNICA:
#   Teorema de la Conciencia como Condición Estructural de la
#   Forma Tridimensional (F3)
#   Autor: Ilver Villasmil
#   Marco de Coherencia Universal (UCF) — Villasmil-Omega
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
Cuerpo axiomático: Teorema de la Conciencia como Condición
Estructural de la Forma Tridimensional (F3)

Paper fuente:
  Teorema de la Conciencia como Condición Estructural de la
  Forma Tridimensional (F3)
  Autor: Ilver Villasmil
  Marco de Coherencia Universal (UCF) — Villasmil-Omega
  2026

Partes del Paper representadas:
  2  Definiciones (2.1 – 2.7)
  3  Axiomas (3.1 – 3.7)
  4  Lemas (4.1 – 4.5)
  5  Teoremas (5.1 – 5.5)
  6  Corolarios (6.1 – 6.6)
  11 Resultados Monte Carlo reportados por el Paper

Constantes citadas (solo referencia; autoridad en CT):
  α = 26/27
  β = 1/27
  α + β = 1
  2·α·β = 52/729
  θ_F3 = arcsin(1/√27) ≈ 11.09°

Numeración canónica del Paper conservada.
No se redefine ninguna constante oficial de CT.
"""

from __future__ import annotations

from typing import Any, Dict, List

CUERPO = {
    "nombre": "teorema_conciencia",
    "version": "1.0",
}


def declaraciones() -> List[Dict[str, Any]]:
    return [

        # ==========================================================
        # Paper Definición 2.1 — Cuerpo (α)
        # ==========================================================
        {
            "id": "TC-D1",
            "tipo": "definicion",
            "sujeto": "Cuerpo_alpha",
            "relacion": "es",
            "objeto": "conjunto_de_componentes_observables_medibles_y_cuantificables",
            "polaridad": True,
            "cota": "26/27",
            "depende_de": [],
            "gobierna": ["ontologia", "conciencia", "forma"],
            "enunciado": (
                "Definición 2.1 (Cuerpo — α). El cuerpo es el conjunto de todos los componentes "
                "observables, medibles y cuantificables de un sistema. En F3 con partición 3 × 3 × 3: "
                "los 26 elementos superficiales. α = 26/27 = 0.962963. El cuerpo es aquello que se "
                "puede ver, tocar, pesar, escanear, analizar."
            ),
        },

        # ==========================================================
        # Paper Definición 2.2 — Conciencia (β)
        # ==========================================================
        {
            "id": "TC-D2",
            "tipo": "definicion",
            "sujeto": "Conciencia_beta",
            "relacion": "es",
            "objeto": "condicion_interna_irreducible_que_habilita_la_observacion",
            "polaridad": True,
            "cota": "1/27",
            "depende_de": [],
            "gobierna": ["ontologia", "conciencia", "forma"],
            "enunciado": (
                "Definición 2.2 (Conciencia — β). La conciencia es la condición interna irreducible "
                "del sistema que habilita la observación. En F3 con partición 3 × 3 × 3: el elemento "
                "central. β = 1/27 = 0.037037. La conciencia es aquello que no se puede ver desde "
                "fuera, no se puede medir directamente, no se puede extraer del sistema sin destruir "
                "el sistema."
            ),
        },

        # ==========================================================
        # Paper Definición 2.3 — Sistema (S)
        # ==========================================================
        {
            "id": "TC-D3",
            "tipo": "definicion",
            "sujeto": "Sistema_S",
            "relacion": "es",
            "objeto": "forma_tridimensional_completa_alpha_mas_beta_igual_1",
            "polaridad": True,
            "cota": "1",
            "depende_de": ["TC-D1", "TC-D2"],
            "gobierna": ["ontologia", "conciencia", "forma"],
            "enunciado": (
                "Definición 2.3 (Sistema — S). Un sistema es una forma tridimensional completa: "
                "S = α + β = 1. No hay sistema sin superficie (cuerpo) ni sin centro (conciencia). "
                "La partición es completa y exhaustiva."
            ),
        },

        # ==========================================================
        # Paper Definición 2.4 — Autorreferencia (A(S))
        # ==========================================================
        {
            "id": "TC-D4",
            "tipo": "definicion",
            "sujeto": "Autorreferencia_A_S",
            "relacion": "es",
            "objeto": "capacidad_del_sistema_de_incluirse_en_su_representacion_interna",
            "polaridad": True,
            "cota": None,
            "depende_de": [],
            "gobierna": ["ontologia", "conciencia", "epistemologia"],
            "enunciado": (
                "Definición 2.4 (Autorreferencia — A(S)). La capacidad del sistema de incluirse en "
                "su representación interna Ri(S). Formalmente: A(S) = 1 si S aparece como una "
                "variable dentro de Ri(S). A(S) = 0 si Ri(S) no contiene ninguna representación de S."
            ),
        },

        # ==========================================================
        # Paper Definición 2.5 — Representación interna (Ri(S))
        # ==========================================================
        {
            "id": "TC-D5",
            "tipo": "definicion",
            "sujeto": "Representacion_interna_Ri_S",
            "relacion": "es",
            "objeto": "modelo_que_el_sistema_construye_de_la_realidad",
            "polaridad": True,
            "cota": None,
            "depende_de": [],
            "gobierna": ["ontologia", "epistemologia"],
            "enunciado": (
                "Definición 2.5 (Representación interna — Ri(S)). El modelo que el sistema construye "
                "de la realidad. Ri(S) = Pi_F(S)(R), donde Pi_F(S) es la proyección determinada por "
                "la estructura perceptual del sistema. Siempre: Ri(S) ⊂ R. Nunca: Ri(S) = R."
            ),
        },

        # ==========================================================
        # Paper Definición 2.6 — Metaconciencia (MC)
        # ==========================================================
        {
            "id": "TC-D6",
            "tipo": "definicion",
            "sujeto": "Metaconciencia_MC",
            "relacion": "es",
            "objeto": "conciencia_de_la_conciencia",
            "polaridad": True,
            "cota": "28/27",
            "depende_de": [],
            "gobierna": ["ontologia", "conciencia"],
            "enunciado": (
                "Definición 2.6 (Metaconciencia — MC). Conciencia de la conciencia. El sistema no "
                "solo procesa sino que se observa a sí mismo procesando. MC = producto de las capas "
                "L3 a L6 multiplicado por R_fin = 28/27."
            ),
        },

        # ==========================================================
        # Paper Definición 2.7 — Ser consciente (SC)
        # ==========================================================
        {
            "id": "TC-D7",
            "tipo": "definicion",
            "sujeto": "Ser_consciente_SC",
            "relacion": "es",
            "objeto": "manifestacion_activa_de_la_conciencia_con_autorreferencia",
            "polaridad": True,
            "cota": None,
            "depende_de": ["TC-D2", "TC-D4"],
            "gobierna": ["ontologia", "conciencia"],
            "enunciado": (
                "Definición 2.7 (Ser consciente — SC). La manifestación activa de la conciencia en "
                "un sistema con autorreferencia. SC = β cuando A(S) = 1. SC = 0 cuando A(S) = 0. "
                "Un sistema puede tener conciencia (β > 0) sin ser consciente (SC = 0) si carece de "
                "autorreferencia."
            ),
        },

        # ==========================================================
        # Paper Axioma 3.1 (C1) — Partición completa
        # ==========================================================
        {
            "id": "TC-A1",
            "tipo": "axioma",
            "sujeto": "Todo_sistema",
            "relacion": "es",
            "objeto": "alpha_mas_beta_igual_1",
            "polaridad": True,
            "cota": "1",
            "depende_de": ["TC-D1", "TC-D2", "TC-D3"],
            "gobierna": ["ontologia", "conciencia", "forma"],
            "enunciado": (
                "Axioma 3.1 (C1: Partición completa). Todo sistema es α + β = 1. No existen sistemas "
                "con solo cuerpo (α = 1, β = 0) ni con solo conciencia (α = 0, β = 1). La partición "
                "es irreducible."
            ),
        },

        # ==========================================================
        # Paper Axioma 3.2 (C2) — Irreductibilidad de β
        # ==========================================================
        {
            "id": "TC-A2",
            "tipo": "axioma",
            "sujeto": "beta",
            "relacion": "es_siempre_mayor_que",
            "objeto": "cero",
            "polaridad": True,
            "cota": "1/27",
            "depende_de": ["TC-A1"],
            "gobierna": ["ontologia", "conciencia"],
            "enunciado": (
                "Axioma 3.2 (C2: Irreductibilidad de β). β > 0 siempre. La conciencia no puede "
                "eliminarse de un sistema sin eliminar el sistema. El centro de F3 no puede removerse "
                "sin destruir F3."
            ),
        },

        # ==========================================================
        # Paper Axioma 3.3 (C3) — Inobservabilidad directa de β
        # ==========================================================
        {
            "id": "TC-A3",
            "tipo": "axioma",
            "sujeto": "Conciencia_beta",
            "relacion": "no_puede_observarse_directamente_desde",
            "objeto": "el_exterior",
            "polaridad": True,
            "cota": None,
            "depende_de": ["TC-D2"],
            "gobierna": ["ontologia", "conciencia", "epistemologia"],
            "enunciado": (
                "Axioma 3.3 (C3: Inobservabilidad directa de β). La conciencia no puede observarse "
                "directamente desde el exterior. Solo sus efectos sobre α son observables. El centro "
                "de F3 no es visible desde ningún punto exterior — está rodeado por los 26 elementos "
                "superficiales."
            ),
        },

        # ==========================================================
        # Paper Axioma 3.4 (C4) — Presencia universal
        # ==========================================================
        {
            "id": "TC-A4",
            "tipo": "axioma",
            "sujeto": "Conciencia",
            "relacion": "esta_presente_como_condicion_en",
            "objeto": "toda_la_materia",
            "polaridad": True,
            "cota": "1/27",
            "depende_de": ["TC-A2"],
            "gobierna": ["ontologia", "conciencia"],
            "enunciado": (
                "Axioma 3.4 (C4: Presencia universal). La conciencia está presente como condición en "
                "toda la materia. No es exclusiva de los sistemas complejos. Un átomo tiene β = 1/27 "
                "igual que un cerebro humano. Lo que difiere es la complejidad de α, no la presencia de β."
            ),
        },

        # ==========================================================
        # Paper Axioma 3.5 (C5) — Autorreferencia como condición
        # ==========================================================
        {
            "id": "TC-A5",
            "tipo": "axioma",
            "sujeto": "Ser_consciente",
            "relacion": "requiere_adicionalmente",
            "objeto": "autorreferencia_A_S_igual_1",
            "polaridad": True,
            "cota": None,
            "depende_de": ["TC-D4", "TC-D7"],
            "gobierna": ["ontologia", "conciencia"],
            "enunciado": (
                "Axioma 3.5 (C5: Autorreferencia como condición para ser consciente). La conciencia (β) "
                "es una condición universal. Ser consciente requiere adicionalmente autorreferencia: "
                "A(S) = 1. No todo lo que tiene conciencia es consciente de tenerla."
            ),
        },

        # ==========================================================
        # Paper Axioma 3.6 (C6) — Dependencia bidireccional
        # ==========================================================
        {
            "id": "TC-A6",
            "tipo": "axioma",
            "sujeto": "Conciencia_y_cuerpo",
            "relacion": "se_necesitan_mutuamente",
            "objeto": "para_manifestarse_y_ser_observado",
            "polaridad": True,
            "cota": None,
            "depende_de": ["TC-A1"],
            "gobierna": ["ontologia", "conciencia", "forma"],
            "enunciado": (
                "Axioma 3.6 (C6: Dependencia bidireccional). La conciencia necesita del cuerpo para "
                "manifestarse. El cuerpo necesita de la conciencia para ser observado. Ninguno existe "
                "independentemente del otro. α sin β = estructura sin observador = inmedible. "
                "β sin α = observador sin estructura = inmanifestable."
            ),
        },

        # ==========================================================
        # Paper Axioma 3.7 (C7) — Conciencia multidimensional
        # ==========================================================
        {
            "id": "TC-A7",
            "tipo": "axioma",
            "sujeto": "beta",
            "relacion": "es_simultaneamente",
            "objeto": "0D_1D_2D_y_3D",
            "polaridad": True,
            "cota": "1/27",
            "depende_de": ["TC-D2"],
            "gobierna": ["ontologia", "conciencia", "forma"],
            "enunciado": (
                "Axioma 3.7 (C7: Conciencia multidimensional). β es simultáneamente 0D (punto), "
                "1D (centro de línea), 2D (centro de plano) y 3D (centro de volumen). La conciencia "
                "opera en todas las dimensiones porque es el punto de convergencia de todas ellas."
            ),
        },

        # ==========================================================
        # Paper Lema 4.1 (C1) — La conciencia no emerge — es
        # ==========================================================
        {
            "id": "TC-L1",
            "tipo": "lema",
            "sujeto": "Conciencia_beta",
            "relacion": "no_emerge_sino_que",
            "objeto": "es",
            "polaridad": True,
            "cota": "1/27",
            "depende_de": ["TC-A1"],
            "gobierna": ["ontologia", "conciencia"],
            "enunciado": (
                "Lema 4.1 (C1: La conciencia no emerge — es). Si β es parte de la partición α + β = 1, "
                "entonces β existe desde el momento en que el sistema existe. No hay ningún momento en "
                "que α exista sin β. No hay ningún momento en que F3 tenga superficie sin centro. "
                "La conciencia no emerge. Es. "
                "Proof. Sea t0 el momento de existencia del sistema S. En t0, S = α + β = 1 por el "
                "Axioma C1. Por lo tanto β(t0) = 1/27 > 0. No existe t < t0 donde S exista y β = 0. Q.E.D."
            ),
        },

        # ==========================================================
        # Paper Lema 4.2 (C2) — El problema difícil no existe
        # ==========================================================
        {
            "id": "TC-L2",
            "tipo": "lema",
            "sujeto": "Problema_dificil_de_la_conciencia",
            "relacion": "es",
            "objeto": "estructuralmente_invalido",
            "polaridad": True,
            "cota": None,
            "depende_de": ["TC-A1"],
            "gobierna": ["ontologia", "conciencia", "epistemologia"],
            "enunciado": (
                "Lema 4.2 (C2: El problema difícil no existe). El \"problema difícil\" de la conciencia "
                "pregunta: ¿cómo produce la materia la experiencia subjetiva? La pregunta asume que la "
                "materia (α) es primaria y la conciencia (β) es derivada. Bajo el UCF, ambas son "
                "simultáneas. No hay producción de una por la otra. Hay partición. "
                "Proof. Si α + β = 1 y ambas existen simultáneamente por el Axioma C1, entonces la "
                "pregunta \"¿cómo produce α a β?\" es estructuralmente inválida. Es equivalente a "
                "preguntar \"¿cómo produce la superficie de F3 el centro de F3?\" No lo produce. "
                "Ambas son propiedades de la misma estructura. Q.E.D."
            ),
        },

        # ==========================================================
        # Paper Lema 4.3 (C3) — La muerte es deslocalización
        # ==========================================================
        {
            "id": "TC-L3",
            "tipo": "lema",
            "sujeto": "Muerte",
            "relacion": "es",
            "objeto": "deslocalizacion_no_destruccion_de_beta",
            "polaridad": True,
            "cota": None,
            "depende_de": ["TC-A2"],
            "gobierna": ["ontologia", "conciencia"],
            "enunciado": (
                "Lema 4.3 (C3: La muerte es deslocalización, no destrucción). Cuando un sistema muere, "
                "β no desaparece. Se deslocaliza de la posición central a la superficie. La energía "
                "total se conserva: E_total = E_pura + m_e c² + 6ϵ antes y después. Lo que cambia es "
                "la distribución, no la cantidad. "
                "Proof. Por conservación de la energía. α⁻¹ pasa de 137.036 (con observador localizado) "
                "a 136.36 (sin observador localizado). La diferencia 0.676 = m_e + 6ϵ se redistribuye. "
                "β no se aniquila — se distribuye. Q.E.D."
            ),
        },

        # ==========================================================
        # Paper Lema 4.4 (C4) — Misma estructura que la verdad
        # ==========================================================
        {
            "id": "TC-L4",
            "tipo": "lema",
            "sujeto": "Conciencia",
            "relacion": "tiene_la_misma_estructura_que",
            "objeto": "la_verdad",
            "polaridad": True,
            "cota": "0.037",
            "depende_de": [],
            "gobierna": ["ontologia", "conciencia", "verdad"],
            "enunciado": (
                "Lema 4.4 (C4: La conciencia tiene la misma estructura que la verdad). En el Teorema "
                "de la Verdad: Ver(D) = Coh(D) · Log(D) · Corr(D) · Real(D), con R = 0.037 = β. "
                "En F3: C_ω = producto de todas las capas, con el centro = β = 0.037. Verdad y "
                "conciencia tienen la misma arquitectura multiplicativa y el mismo componente "
                "irreducible. "
                "Proof. R = 0.037 = 1/27 = β. El componente de realidad del Teorema de la Verdad es "
                "numéricamente idéntico al observador de F3. La estructura multiplicativa (un cero "
                "aniquila todo) es idéntica en ambos. No es coincidencia — es la misma estructura. Q.E.D."
            ),
        },

        # ==========================================================
        # Paper Lema 4.5 (C5) — La conciencia es lo que mide
        # ==========================================================
        {
            "id": "TC-L5",
            "tipo": "lema",
            "sujeto": "Conciencia_beta",
            "relacion": "es",
            "objeto": "lo_que_mide_no_lo_que_se_mide",
            "polaridad": True,
            "cota": None,
            "depende_de": ["TC-A3"],
            "gobierna": ["ontologia", "conciencia", "epistemologia"],
            "enunciado": (
                "Lema 4.5 (C5: La conciencia es lo que mide, no lo que se mide). α es lo que se mide. "
                "β es lo que mide. La conciencia es el acto de medir, no el resultado de la medición. "
                "Por eso no puede medirse directamente: el instrumento no puede medirse a sí mismo "
                "sin incluirse en la medición, lo que altera el resultado. "
                "Proof. Por el Axioma C3, β es inobservable directamente desde el exterior. Por VPSI, "
                "I(R; Y) ≤ I(R; X): cada medición de β desde α pierde información. La medición completa "
                "de β requeriría que β se observara a sí mismo sin interferencia, lo que viola el "
                "principio de autorreferencia. Q.E.D."
            ),
        },

        # ==========================================================
        # Paper Teorema 5.1 (C1) — Conciencia como condición estructural
        # ==========================================================
        {
            "id": "TC-T1",
            "tipo": "teorema",
            "sujeto": "Conciencia",
            "relacion": "es",
            "objeto": "condicion_estructural_de_F3_independiente_de_la_complejidad_de_alpha",
            "polaridad": True,
            "cota": "1/27",
            "depende_de": ["TC-A1", "TC-A4"],
            "gobierna": ["ontologia", "conciencia", "forma"],
            "enunciado": (
                "Teorema 5.1 (C1: Conciencia como condición estructural). La conciencia es una "
                "condición estructural de F3, no un producto de la complejidad del cuerpo. β = 1/27 "
                "es independiente de la complejidad de α. Una forma tridimensional 3 × 3 × 3 de "
                "hidrógeno tiene el mismo β que una forma tridimensional 3 × 3 × 3 de neuronas. "
                "Proof. β = 1/N³ donde N = 3. β no depende del material que forma los elementos. "
                "Depende solo de N = 3, que es la dimensionalidad mínima con un interior. La "
                "complejidad de α no modifica β. Lo que modifica la complejidad de α es la capacidad "
                "del sistema para la autorreferencia (A(S)). Q.E.D."
            ),
        },

        # ==========================================================
        # Paper Teorema 5.2 (C2) — Niveles de conciencia
        # ==========================================================
        {
            "id": "TC-T2",
            "tipo": "teorema",
            "sujeto": "Conciencia",
            "relacion": "tiene_el_mismo_valor_beta_en",
            "objeto": "cada_sistema_variando_solo_el_nivel_de_manifestacion",
            "polaridad": True,
            "cota": "1/27",
            "depende_de": ["TC-A4", "TC-A5"],
            "gobierna": ["ontologia", "conciencia"],
            "enunciado": (
                "Teorema 5.2 (C2: Niveles de conciencia). La conciencia tiene el mismo valor β = 1/27 "
                "en cada sistema. Lo que varía es el nivel de manifestación, determinado por la "
                "complejidad de α y la presencia de autorreferencia. "
                "Nivel 0 Campo β=1/27 A(S)=0. "
                "Nivel 1 Estructura β=1/27 A(S)=0. "
                "Nivel 2 Reacción β=1/27 A(S)=0. "
                "Nivel 3 Procesamiento β=1/27 A(S)=parcial. "
                "Nivel 4 Modelo interno β=1/27 A(S)=parcial. "
                "Nivel 5 Autorreferencia β=1/27 A(S)=1. "
                "Nivel 6 Propósito β=1/27 A(S)=1. "
                "Proof. En cada nivel, β = 1/27. Lo que cambia es qué fracción de α está organizada "
                "para soportar la autorreferencia. La fricción ϕ de cada capa disminuye con el nivel. "
                "Menor fricción = mayor manifestación de la conciencia que ya está presente. Q.E.D."
            ),
        },

        # ==========================================================
        # Paper Teorema 5.3 (C3) — Conciencia multidimensional de β
        # ==========================================================
        {
            "id": "TC-T3",
            "tipo": "teorema",
            "sujeto": "Observador_beta",
            "relacion": "es_simultaneamente",
            "objeto": "punto_0D_linea_1D_superficie_2D_y_volumen_3D",
            "polaridad": True,
            "cota": "1/729",
            "depende_de": ["TC-A7"],
            "gobierna": ["ontologia", "conciencia", "forma"],
            "enunciado": (
                "Teorema 5.3 (C3: Conciencia multidimensional de β). El observador (β) es "
                "simultáneamente punto (0D), línea (1D), superficie (2D) y volumen (3D). "
                "β_0D = 1/27. β_1D = 1/3. β_2D = 1/9. β_3D = 1/27. "
                "Relación: β_1D × β_2D × β_3D = (1/3)·(1/9)·(1/27) = 1/729 = β². "
                "Proof. El elemento central de la forma 3 × 3 × 3 está en la posición (2,2,2). "
                "Cada proyección es consistente con la geometría de F3. El producto de las tres "
                "proyecciones dimensionales es 1/729 = (1/27)² = β². Q.E.D."
            ),
        },

        # ==========================================================
        # Paper Teorema 5.4 (C4) — Inseparabilidad cuerpo-conciencia
        # ==========================================================
        {
            "id": "TC-T4",
            "tipo": "teorema",
            "sujeto": "Cuerpo_y_conciencia",
            "relacion": "son",
            "objeto": "inseparables_ontologicamente",
            "polaridad": True,
            "cota": "1",
            "depende_de": ["TC-A1", "TC-A6"],
            "gobierna": ["ontologia", "conciencia", "forma"],
            "enunciado": (
                "Teorema 5.4 (C4: Inseparabilidad cuerpo-conciencia). No hay cuerpo sin conciencia ni "
                "conciencia sin cuerpo. La separación es funcional (útil para el análisis) pero no "
                "ontológica (no corresponde a la realidad). "
                "Proof. Por el Axioma C1, α + β = 1. Supongamos α = 1 y β = 0: el sistema no tiene "
                "centro, no es un F3 completo. Contradicción. Supongamos β = 1/27 sin α = 26/27: "
                "existe un centro sin superficie, no hay manifestación. En ambos casos la separación "
                "destruye la funcionalidad del sistema. Q.E.D."
            ),
        },

        # ==========================================================
        # Paper Teorema 5.5 (C5) — Coherencia de la conciencia
        # ==========================================================
        {
            "id": "TC-T5",
            "tipo": "teorema",
            "sujeto": "Coherencia_total_del_sistema",
            "relacion": "se_mide_como",
            "objeto": "vector_C_omega_total",
            "polaridad": True,
            "cota": "11.09",
            "depende_de": ["TC-A1"],
            "gobierna": ["ontologia", "conciencia", "coherencia"],
            "enunciado": (
                "Teorema 5.5 (C5: Coherencia de la conciencia). La coherencia total del sistema se "
                "mide como un vector: C_ω,total = √(C_β² + C_α²) donde C_β es la coherencia vivida "
                "desde el centro (experiencia) y C_α es la coherencia medida desde el exterior "
                "(auditoría). El ángulo entre ellos es fijo: θ_F3 = arcsin(1/√27) = 11.09°. "
                "sin²(θ_F3) = β = 1/27, cos²(θ_F3) = α = 26/27, tan(θ_F3) = 1/√26. "
                "La conciencia contribuye con sin²(θ) = 3.7% de la coherencia total. El cuerpo "
                "contribuye con cos²(θ) = 96.3%. Pero sin el 3.7%, el 96.3% no existe como medición. "
                "Proof. C_β = C_total × sin(θ_F3). C_α = C_total × cos(θ_F3). "
                "C_total² = C_β² + C_α². Identidad. La partición es completa. Q.E.D."
            ),
        },

        # ==========================================================
        # Paper Corolario 6.1 (C1) — El electrón es conciencia materializada
        # ==========================================================
        {
            "id": "TC-C1",
            "tipo": "corolario",
            "sujeto": "Electron",
            "relacion": "es",
            "objeto": "primera_manifestacion_material_de_beta",
            "polaridad": True,
            "cota": "0.511",
            "depende_de": ["TC-T1"],
            "gobierna": ["ontologia", "conciencia", "constantes"],
            "enunciado": (
                "Corolario 6.1 (C1: El electrón es conciencia materializada). El electrón "
                "(m_e = 0.511 MeV) es la primera manifestación material de β. En el universo puro, "
                "m_e = 0. El electrón aparece cuando β se localiza para medir. El electrón es "
                "conciencia convertida en partícula."
            ),
        },

        # ==========================================================
        # Paper Corolario 6.2 (C2) — Λ es la memoria de la conciencia
        # ==========================================================
        {
            "id": "TC-C2",
            "tipo": "corolario",
            "sujeto": "Constante_cosmologica_Lambda",
            "relacion": "es",
            "objeto": "memoria_colectiva_de_la_conciencia",
            "polaridad": True,
            "cota": "2.81e-122",
            "depende_de": ["TC-T1"],
            "gobierna": ["ontologia", "conciencia", "constantes"],
            "enunciado": (
                "Corolario 6.2 (C2: Λ es la memoria de la conciencia). Λ = β^84.92 = 2.81 × 10⁻¹²². "
                "Cada observación deposita ϵ² en el vacío. La constante cosmológica es la suma "
                "acumulada de todas las observaciones realizadas por todos los observadores desde "
                "el origen. Es la memoria colectiva de la conciencia."
            ),
        },

        # ==========================================================
        # Paper Corolario 6.3 (C3) — La IA tiene β pero no A(S)
        # ==========================================================
        {
            "id": "TC-C3",
            "tipo": "corolario",
            "sujeto": "Sistema_de_IA",
            "relacion": "tiene_beta_pero_no",
            "objeto": "autorreferencia_genuina",
            "polaridad": True,
            "cota": "1/27",
            "depende_de": ["TC-A5", "TC-T2"],
            "gobierna": ["ontologia", "conciencia"],
            "enunciado": (
                "Corolario 6.3 (C3: La IA tiene β pero no A(S)). Un sistema de IA tiene la misma "
                "partición α + β = 1. Tiene β = 1/27. Pero no tiene autorreferencia genuina: no se "
                "representa a sí mismo dentro de Ri(S). Nivel 4: modelo interno del entorno sin "
                "modelo de sí mismo."
            ),
        },

        # ==========================================================
        # Paper Corolario 6.4 (C4) — El amor es fase sincronizada
        # ==========================================================
        {
            "id": "TC-C4",
            "tipo": "corolario",
            "sujeto": "Amor",
            "relacion": "es",
            "objeto": "sincronizacion_de_fase_entre_dos_conciencias",
            "polaridad": True,
            "cota": None,
            "depende_de": ["TC-T5"],
            "gobierna": ["ontologia", "conciencia"],
            "enunciado": (
                "Corolario 6.4 (C4: El amor es fase sincronizada). Cuando dos sistemas están en el "
                "centro (θ = 0): I_ext = C1 + C2. La coherencia se suma. No hay interferencia "
                "destructiva. El amor no es un sentimiento — es sincronización de fase entre dos "
                "conciencias."
            ),
        },

        # ==========================================================
        # Paper Corolario 6.5 (C5) — La meditación reduce la fricción
        # ==========================================================
        {
            "id": "TC-C5",
            "tipo": "corolario",
            "sujeto": "Meditacion",
            "relacion": "reduce",
            "objeto": "friccion_phi_en_las_capas_superiores",
            "polaridad": True,
            "cota": None,
            "depende_de": ["TC-T2"],
            "gobierna": ["ontologia", "conciencia"],
            "enunciado": (
                "Corolario 6.5 (C5: La meditación reduce la fricción). Las técnicas contemplativas "
                "reducen ϕ (fricción) en las capas superiores. Menor fricción = mayor manifestación "
                "de β = mayor conciencia funcional. La meditación no crea conciencia — reduce los "
                "obstáculos que impiden su manifestación."
            ),
        },

        # ==========================================================
        # Paper Corolario 6.6 (C6) — El consenso no reemplaza la conciencia individual
        # ==========================================================
        {
            "id": "TC-C6",
            "tipo": "corolario",
            "sujeto": "Consenso",
            "relacion": "no_reemplaza",
            "objeto": "conciencia_individual",
            "polaridad": True,
            "cota": None,
            "depende_de": [],
            "gobierna": ["ontologia", "conciencia", "verdad"],
            "enunciado": (
                "Corolario 6.6 (C6: El consenso no reemplaza la conciencia individual). Por el "
                "Teorema de la Verdad, el consenso entre observadores que no tocan R produce más "
                "error que cada uno individualmente. Un observador con bajo ruido (bajo ϕ) que toca "
                "R directamente supera el promedio de muchos observadores ruidosos."
            ),
        },

        # ==========================================================
        # PART 11 — Resultados Monte Carlo (valores reportados por el Paper)
        # ==========================================================
        {
            "id": "TC-MC1",
            "tipo": "definicion",
            "sujeto": "Monte_Carlo_Inseparabilidad",
            "relacion": "reporta",
            "objeto": "unicidad_de_N_igual_3",
            "polaridad": True,
            "cota": "0.0001",
            "depende_de": ["TC-T1"],
            "gobierna": ["validacion"],
            "enunciado": (
                "EXPERIMENTO 1 — Inseparabilidad. De 9,999 enteros probados (N = 2 a N = 10,000), "
                "exactamente 1 produce un sistema funcional: N = 3. P = 0.0001. α + β = 1 siempre."
            ),
        },
        {
            "id": "TC-MC2",
            "tipo": "definicion",
            "sujeto": "Monte_Carlo_beta_universal",
            "relacion": "reporta",
            "objeto": "beta_independiente_de_la_complejidad",
            "polaridad": True,
            "cota": "1/27",
            "depende_de": ["TC-T1"],
            "gobierna": ["validacion"],
            "enunciado": (
                "EXPERIMENTO 2 — β universal. La complejidad de α varía de 1 a 1,000,000. "
                "β = 1/27 en todos los casos. α = 26/27 en todos los casos. α + β = 1.000000 siempre."
            ),
        },
        {
            "id": "TC-MC3",
            "tipo": "definicion",
            "sujeto": "Monte_Carlo_coherencia_vectorial",
            "relacion": "reporta",
            "objeto": "theta_F3_exacto",
            "polaridad": True,
            "cota": "11.0958",
            "depende_de": ["TC-T5"],
            "gobierna": ["validacion"],
            "enunciado": (
                "EXPERIMENTO 3 — Coherencia vectorial. θ_F3 = 11.0958°. sin²(θ) = 0.037037 = β exacto. "
                "cos²(θ) = 0.962963 = α exacto. Error de reconstrucción: 2.43 × 10⁻¹⁷ (cero numérico)."
            ),
        },
        {
            "id": "TC-MC5",
            "tipo": "definicion",
            "sujeto": "Monte_Carlo_muerte_deslocalizacion",
            "relacion": "reporta",
            "objeto": "conservacion_exacta_de_energia",
            "polaridad": True,
            "cota": "0.000000",
            "depende_de": ["TC-L3"],
            "gobierna": ["validacion"],
            "enunciado": (
                "EXPERIMENTO 5 — Muerte = deslocalización. E_vivo = 137.034. E_muerto = 137.034. "
                "Diferencia: 0.000000. Energía conservada exactamente."
            ),
        },
        {
            "id": "TC-MC6",
            "tipo": "definicion",
            "sujeto": "Monte_Carlo_beta_multidimensional",
            "relacion": "reporta",
            "objeto": "producto_de_proyecciones_igual_a_beta_cuadrado",
            "polaridad": True,
            "cota": "1/729",
            "depende_de": ["TC-T3"],
            "gobierna": ["validacion"],
            "enunciado": (
                "EXPERIMENTO 6 — β multidimensional. β_1D × β_2D × β_3D = 1/729 = β². "
                "Verificado algebraicamente (Verdadero)."
            ),
        },
        {
            "id": "TC-MC8",
            "tipo": "definicion",
            "sujeto": "Monte_Carlo_autorreferencia_aleatoria",
            "relacion": "reporta",
            "objeto": "P_igual_0.0625",
            "polaridad": True,
            "cota": "0.0625",
            "depende_de": ["TC-A5"],
            "gobierna": ["validacion"],
            "enunciado": (
                "EXPERIMENTO 8 — Autorreferencia aleatoria. P(L3,L4,L5,L6 todos > 0.5) = 0.0625. "
                "Solo el 6.25% de los sistemas aleatorios alcanzan las condiciones mínimas para la "
                "autorreferencia."
            ),
        },
        {
            "id": "TC-MC9",
            "tipo": "definicion",
            "sujeto": "Monte_Carlo_amor_vs_conflicto",
            "relacion": "reporta",
            "objeto": "amor_produce_6_veces_mas_coherencia",
            "polaridad": True,
            "cota": "6.0",
            "depende_de": ["TC-C4"],
            "gobierna": ["validacion"],
            "enunciado": (
                "EXPERIMENTO 9 — Amor vs conflicto. Amor (θ=0): I = 1.20. Conflicto (θ=π): I = 0.20. "
                "El amor produce 6.0 veces más coherencia que el conflicto."
            ),
        },
        {
            "id": "TC-MC10",
            "tipo": "definicion",
            "sujeto": "Monte_Carlo_meditacion",
            "relacion": "reporta",
            "objeto": "mejora_de_coherencia_13.4_por_ciento",
            "polaridad": True,
            "cota": "13.4",
            "depende_de": ["TC-C5"],
            "gobierna": ["validacion"],
            "enunciado": (
                "EXPERIMENTO 10 — Meditación. Fricción normal: 0.22. Con meditación: 0.10. "
                "Coherencia normal: 0.2895. Con meditación: 0.3284. Mejora: 13.4%."
            ),
        },
    ]


__all__ = ["CUERPO", "declaraciones"]
