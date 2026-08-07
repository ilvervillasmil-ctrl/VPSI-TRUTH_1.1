# ===============================================================
# VPSI-TRUTH — modules/correlacion_mecanica/grafo_I_MC.py
# ===============================================================
#
# GRAFO MC — proyección del espacio de correlación mecánica.
# Instancia: GRAFO-MC-001 (una entre muchas posibles).
#
# ---------------------------------------------------------------
# CUATRO NIVELES (separados)
# ---------------------------------------------------------------
#
#   1. Catálogo de mecanismos     (conocimiento estructural)
#   2. Proceso de evaluación      (consulta → motor)
#   3. Resultado                  (conocimiento operativo, solo en consulta)
#   4. Principio de silencio      (epistemología del vacío)
#
#   Consulta
#      ↓
#   Mecanismo  (entidad del catálogo; no “produce” solo)
#      ↓
#   Evaluación
#      ↓
#   Resultado  (POSIBLE | IMPOSIBLE | INDEFINIDO | …)
#
# El resultado NO vive en el catálogo.
# Vive únicamente en la evaluación bajo una consulta concreta.
#
# ---------------------------------------------------------------
# MECANISMO ≠ REGLA
# ---------------------------------------------------------------
#
# Regla:        si ocurre A entonces ocurre B.
# Mecanismo:    si evalúo esta estructura, obtengo este resultado.
#
# Más general: el mismo mecanismo, con distinto contexto/O/evidencia,
# puede evaluarse de formas distintas por evaluadores distintos
# (Evaluador_MC, futuro Evaluador_CA, …) sin mover el catálogo.
#
# ---------------------------------------------------------------
# QUÉ ALMACENA UNA CORRELACIÓN (solo estructural)
# ---------------------------------------------------------------
#
#   id
#   antecedentes
#   mecanismo          (nombre del mecanismo-entidad)
#   consecuencia
#   efecto_estructural (admite | veda)
#   norma              (si veda; None si admite)
#   porque / fuente
#
# efecto_estructural es conocimiento permanente del mecanismo.
# resultado es conocimiento operativo de una evaluación.
#
# ---------------------------------------------------------------
# PRINCIPIO DE SILENCIO
# ---------------------------------------------------------------
#
# MC nunca infiere imposibilidad a partir del silencio.
# La imposibilidad requiere mecanismo con efecto_estructural=veda
# y norma declarada.
# El silencio produce únicamente INDEFINIDO.
#
# ---------------------------------------------------------------
# ESTRUCTURA
# ---------------------------------------------------------------
#
# No es un grafo de nodos con aristas pobres.
# Cada correlación es un objeto tipado (hiperarista semántica):
# antecedentes (conjunto) → mecanismo → consecuencia.
#
# Meta-correlación (mecanismos entre mecanismos): espacio abierto.
#
# ===============================================================

from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence

# ===============================================================
# SECCIÓN 1 — IDENTIDAD
# ===============================================================

GRAFO_ID = "GRAFO-MC-001"
VERSION = "1.3"

MECANICA = {
    "nombre": "grafo_mc",
    "version": VERSION,
    "grafo_id": GRAFO_ID,
    "orden": [
        "MMC_Barrido_Coherente",
        "Sistema",
        "Programacion",
        "Conocimiento",
        "CXF_Entrada_Natural",
        "CXF_Fijacion_O",
        "Declaracion_O",
        "Escala_O",
        "Regla_Significado",
        "Correlacion_K",
        "Modalidad",
        "O_context",
        "Canal_o_limite",
        "X_evidencia",
        "inclusion",
        "severidad",
        "C",
        "L",
        "K",
        "Tru_Ri",
        "Tru_total",
        "Cierre_Causal",
        "Empaquetado_Anuncio",
        "Cierre_Auditable",
    ],
    "descripcion": (
        "Catálogo de mecanismos de correlación (conocimiento estructural) "
        "y evaluador por defecto (conocimiento operativo). "
        "El resultado no está en el catálogo: aparece al evaluar una consulta."
    ),
    "notas": [
        "Cuatro niveles: catálogo, evaluación, resultado, principio de silencio.",
        "Mecanismo ≠ regla; evaluación ≠ estado permanente del grafo.",
        "efecto_estructural (admite|veda) es estructural; resultado es operativo.",
        "Silencio → INDEFINIDO; imposibilidad solo con veda + norma.",
        "API: correlacionar(antecedentes, consecuencia).",
        "Cobertura de antecedentes es pluggable (_cubre); puede evolucionar.",
        "Meta-correlación entre mecanismos: no implementada; espacio abierto.",
        "orden es vista lineal de esta proyección, no el objeto.",
    ],
    "principio_silencio": (
        "MC nunca infiere imposibilidad a partir del silencio. "
        "La imposibilidad requiere un mecanismo con efecto_estructural=veda "
        "y norma declarada. El silencio produce únicamente INDEFINIDO."
    ),
}


# ===============================================================
# SECCIÓN 2 — RESULTADOS DE EVALUACIÓN (solo operativos)
# ===============================================================

POSIBLE = "POSIBLE"
IMPOSIBLE = "IMPOSIBLE"
INDEFINIDO = "INDEFINIDO"

# Efecto estructural permanente del mecanismo (catálogo)
ADMITE = "admite"
VEDA = "veda"


# ===============================================================
# SECCIÓN 3 — CATÁLOGO (conocimiento estructural)
# ===============================================================
#
# Sin campo `resultado`.
# Cada entrada es una entidad-mecanismo (id estable).
#

CORRELACIONES: List[Dict[str, Any]] = [
    # ----- MMC -----
    {
        "id": "C-MMC-01",
        "antecedentes": ["MMC_Barrido_Coherente"],
        "mecanismo": "oficio_mc_habilita_permisos_dominio",
        "consecuencia": "permiso_uso_dominio",
        "efecto_estructural": ADMITE,
        "norma": None,
        "porque": (
            "Barrido coherente admite el uso legítimo de permite_* de dominio."
        ),
        "fuente": "mechanic_of_the_mechanics",
    },
    {
        "id": "C-MMC-02",
        "antecedentes": ["MMC_Barrido_Coherente=False"],
        "mecanismo": "oficio_mc_bloquea_permisos",
        "consecuencia": "MMC_Permisos_De_Dominio",
        "efecto_estructural": VEDA,
        "norma": "CORR_SEQ_02 / oficio MMC",
        "porque": "Barrido fallido veda permisos de dominio.",
        "fuente": "mechanic_of_the_mechanics",
    },
    {
        "id": "C-MMC-03",
        "antecedentes": ["sub_ruta_dominio_incompleta"],
        "mecanismo": "no_saltar_anclaje",
        "consecuencia": "K_numerico",
        "efecto_estructural": VEDA,
        "norma": "MMC_No_Saltar_Anclaje / CX-T16",
        "porque": "Anclaje incompleto veda K numérico a nivel de oficio.",
        "fuente": "mechanic_of_the_mechanics",
    },
    # ----- CXF / CX -----
    {
        "id": "C-CXF-01",
        "antecedentes": ["CXF_Fijacion_O"],
        "mecanismo": "fractal_alimenta_declaracion_o",
        "consecuencia": "Declaracion_O",
        "efecto_estructural": ADMITE,
        "norma": None,
        "porque": "Fijación fractal admite alimentar Declaracion_O (no K sola).",
        "fuente": "contexto_fractal_MC + contexto_MC",
    },
    {
        "id": "C-CXF-02",
        "antecedentes": ["CXF_Ciclo_Sesion"],
        "mecanismo": "permiso_k_local_sin_fijacion",
        "consecuencia": "CXF_Permiso_K_Local",
        "efecto_estructural": VEDA,
        "norma": "CX-T16 / Def-5.3.1",
        "porque": "Sesión sola sin fijación veda permiso K local.",
        "fuente": "contexto_fractal_MC",
    },
    {
        "id": "C-CX-01",
        "antecedentes": [
            "Ciclo_Id",
            "Declaracion_O",
            "Escala_O",
            "Regla_Significado",
        ],
        "mecanismo": "conjunto_minimo_contexto_para_k",
        "consecuencia": "Correlacion_K",
        "efecto_estructural": ADMITE,
        "norma": None,
        "porque": (
            "Conjunto mínimo de contexto admite K de ciclo "
            "(hiperarista; no arista O→K)."
        ),
        "fuente": "contexto_MC.permite_k",
    },
    {
        "id": "C-CX-02",
        "antecedentes": ["Ciclo_Id"],
        "mecanismo": "k_sin_o",
        "consecuencia": "Correlacion_K",
        "efecto_estructural": VEDA,
        "norma": "CX-A1 / Def-5.3.1",
        "porque": "Ciclo crudo sin O veda K numérico.",
        "fuente": "contexto_MC",
    },
    {
        "id": "C-CX-03",
        "antecedentes": ["Declaracion_O"],
        "mecanismo": "o_sin_escala_ni_regla",
        "consecuencia": "Correlacion_K",
        "efecto_estructural": VEDA,
        "norma": "CX-A11 / CX-A4",
        "porque": "O sin Escala_O ni Regla_Significado veda K.",
        "fuente": "contexto_MC",
    },
    # ----- RE -----
    {
        "id": "C-RE-01",
        "antecedentes": ["Modalidad", "O_context"],
        "mecanismo": "admisibilidad_k_de_hecho",
        "consecuencia": "K_de_hecho",
        "efecto_estructural": ADMITE,
        "norma": None,
        "porque": "Modalidad + O admiten reclamo de K de hecho.",
        "fuente": "realidad_MC",
    },
    {
        "id": "C-RE-02",
        "antecedentes": [
            "Modalidad",
            "O_context",
            "Canal_o_limite",
            "X_evidencia",
            "Instantanea",
        ],
        "mecanismo": "admisibilidad_k_sincronizacion_r",
        "consecuencia": "K_sincronizacion_con_R",
        "efecto_estructural": ADMITE,
        "norma": None,
        "porque": "Conjunto completo admite K de sincronización con R.",
        "fuente": "realidad_MC",
    },
    {
        "id": "C-RE-03",
        "antecedentes": ["cualquier"],
        "mecanismo": "k_realidad_sin_o",
        "consecuencia": "K_realidad_sin_O",
        "efecto_estructural": VEDA,
        "norma": "Def-5.3.1 / RE-A12",
        "porque": "K de realidad sin O queda vedado.",
        "fuente": "realidad_MC",
    },
    {
        "id": "C-RE-04",
        "antecedentes": ["cualquier"],
        "mecanismo": "puntuar_r_cero",
        "consecuencia": "asignar_R_igual_0",
        "efecto_estructural": VEDA,
        "norma": "TA4 / RE-A2 / RE-A11",
        "porque": "Puntuar R=0 queda vedado.",
        "fuente": "realidad_MC",
    },
    # ----- CALC -----
    {
        "id": "C-CALC-01",
        "antecedentes": ["O_context"],
        "mecanismo": "condicion_o_para_k",
        "consecuencia": "K",
        "efecto_estructural": ADMITE,
        "norma": None,
        "porque": "O_context admite que K pueda definirse.",
        "fuente": "ciclo_calculo_MC / Def-5.3.1",
    },
    {
        "id": "C-CALC-02",
        "antecedentes": ["inclusion", "severidad"],
        "mecanismo": "anclas_am_para_c",
        "consecuencia": "C",
        "efecto_estructural": ADMITE,
        "norma": None,
        "porque": "Anclas AM admiten C operacional.",
        "fuente": "ciclo_calculo_MC.DEF_C_OP",
    },
    {
        "id": "C-CALC-03",
        "antecedentes": ["inclusion", "severidad"],
        "mecanismo": "anclas_am_para_l",
        "consecuencia": "L",
        "efecto_estructural": ADMITE,
        "norma": None,
        "porque": "Anclas AM admiten L operacional.",
        "fuente": "ciclo_calculo_MC.DEF_L_OP",
    },
    {
        "id": "C-CALC-04",
        "antecedentes": ["O_context", "inclusion", "severidad"],
        "mecanismo": "anclas_am_para_k",
        "consecuencia": "K",
        "efecto_estructural": ADMITE,
        "norma": None,
        "porque": "Conjunto mínimo admite K operacional numérico.",
        "fuente": "ciclo_calculo_MC.DEF_K_OP",
    },
    {
        "id": "C-CALC-05",
        "antecedentes": ["C", "L", "K"],
        "mecanismo": "producto_tru_ri",
        "consecuencia": "Tru_Ri",
        "efecto_estructural": ADMITE,
        "norma": None,
        "porque": "C·L·K definidos admiten Tru_Ri.",
        "fuente": "ciclo_calculo_MC.DEF_TRU_RI",
    },
    {
        "id": "C-CALC-06",
        "antecedentes": ["Tru_Ri"],
        "mecanismo": "mapa_tru_total",
        "consecuencia": "Tru_total",
        "efecto_estructural": ADMITE,
        "norma": None,
        "porque": "Tru_Ri definido admite Tru_total (α, β).",
        "fuente": "ciclo_calculo_MC.DEF_TRU_TOTAL",
    },
    {
        "id": "C-CALC-07",
        "antecedentes": ["base_nula"],
        "mecanismo": "maquillaje_factor_1",
        "consecuencia": "asignar_factor_1",
        "efecto_estructural": VEDA,
        "norma": "AM-D6 / AM-A3",
        "porque": "Base nula veda asignar factor 1.",
        "fuente": "ciclo_calculo_MC",
    },
    # ----- CIT -----
    {
        "id": "C-CIT-01",
        "antecedentes": ["Cierre_Causal"],
        "mecanismo": "cierre_a_anuncio",
        "consecuencia": "Empaquetado_Anuncio",
        "efecto_estructural": ADMITE,
        "norma": None,
        "porque": "Cierre causal admite empaquetado de anuncio (CIT no calcula).",
        "fuente": "citacion_MC",
    },
    {
        "id": "C-CIT-02",
        "antecedentes": ["Ciclo_Id", "Precondicion_Entrada"],
        "mecanismo": "precondicion_emision_cadena",
        "consecuencia": "Respuesta_Peticion",
        "efecto_estructural": ADMITE,
        "norma": None,
        "porque": "Precondición de entrada admite emisión de cadena (PA-A1).",
        "fuente": "citacion_MC",
    },
    {
        "id": "C-CIT-03",
        "antecedentes": ["cualquier"],
        "mecanismo": "cit_no_calcula_tru",
        "consecuencia": "calcular_Tru",
        "efecto_estructural": VEDA,
        "norma": "PA-C2 / contrato CIT",
        "porque": "Oficio CIT veda calcular Tru.",
        "fuente": "citacion_MC",
    },
    {
        "id": "C-CIT-04",
        "antecedentes": ["cualquier"],
        "mecanismo": "no_inventar_clk",
        "consecuencia": "inventar_factores_CLK",
        "efecto_estructural": VEDA,
        "norma": "T9 / PA-A2",
        "porque": "Anuncio veda inventar factores no aportados por CA.",
        "fuente": "citacion_MC",
    },
    {
        "id": "C-CIT-05",
        "antecedentes": ["ausencia_de_cadena"],
        "mecanismo": "ausencia_no_eleva_tru",
        "consecuencia": "elevar_Tru",
        "efecto_estructural": VEDA,
        "norma": "PA-A3 / PA-C3",
        "porque": "Ausencia de cadena veda elevar Tru.",
        "fuente": "citacion_MC",
    },
    {
        "id": "C-CIT-06",
        "antecedentes": ["Resolucion_O_vacia"],
        "mecanismo": "k_sin_o_no_anunciable",
        "consecuencia": "anunciar_K_numerico",
        "efecto_estructural": VEDA,
        "norma": "Def-5.3.1 / PA-T3",
        "porque": "O vacío veda anunciar K numérico.",
        "fuente": "citacion_MC",
    },
]


# ===============================================================
# SECCIÓN 4 — COBERTURA (pluggable; no es el catálogo)
# ===============================================================
#
# Hoy: inclusión de conjuntos / comodín "cualquier".
# Mañana: expresiones (A∧B)∨(C∧D), excepciones, etc.
# Cambiar _cubre no exige reescribir CORRELACIONES.
#

def _cubre(corr: Dict[str, Any], antecedentes: List[str]) -> bool:
    ant = list(corr.get("antecedentes") or [])
    if ant == ["cualquier"]:
        return True
    if not antecedentes:
        return False
    if len(ant) == 1:
        return ant[0] in antecedentes or ant[0] == antecedentes[0]
    return set(ant).issubset(set(antecedentes))


def _norm_antecedentes(
    antecedentes: Optional[Sequence[str]] = None,
    desde: Optional[str] = None,
) -> List[str]:
    if antecedentes is not None:
        return [str(a) for a in antecedentes]
    if desde is not None:
        return [str(desde)]
    return []


# ===============================================================
# SECCIÓN 5 — EVALUADOR (motor; conocimiento operativo)
# ===============================================================
#
# Evaluador por defecto de este módulo.
# Otros evaluadores podrían consultar el mismo CORRELACIONES.
#

def evaluar(
    consecuencia: str,
    antecedentes: Optional[Sequence[str]] = None,
    desde: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Consulta → mecanismos aplicables → resultado operativo.

    Prioridad de evaluación:
      1) mecanismo VEDA aplicable  → IMPOSIBLE (norma)
      2) mecanismo ADMITE aplicable → POSIBLE
      3) ninguno                    → INDEFINIDO (silencio)
    """
    ants = _norm_antecedentes(antecedentes, desde)
    aplicables = [
        c for c in CORRELACIONES
        if c.get("consecuencia") == consecuencia and _cubre(c, ants)
    ]

    vedas = [c for c in aplicables if c.get("efecto_estructural") == VEDA]
    if vedas:
        c = vedas[0]
        return {
            "consulta": {
                "antecedentes": ants,
                "consecuencia": consecuencia,
            },
            "mecanismo_id": c.get("id"),
            "mecanismo": c.get("mecanismo"),
            "efecto_estructural": VEDA,
            "resultado": IMPOSIBLE,
            "norma": c.get("norma"),
            "porque": c.get("porque"),
            "fuente": c.get("fuente"),
            "nota": (
                "Evaluación: el mecanismo veda la consecuencia. "
                "Resultado operativo IMPOSIBLE (no ausente de correlación)."
            ),
        }

    admisiones = [c for c in aplicables if c.get("efecto_estructural") == ADMITE]
    if admisiones:
        c = max(admisiones, key=lambda x: len(x.get("antecedentes") or []))
        return {
            "consulta": {
                "antecedentes": ants,
                "consecuencia": consecuencia,
            },
            "mecanismo_id": c.get("id"),
            "mecanismo": c.get("mecanismo"),
            "efecto_estructural": ADMITE,
            "resultado": POSIBLE,
            "norma": None,
            "porque": c.get("porque"),
            "fuente": c.get("fuente"),
            "nota": "Evaluación: el mecanismo admite la consecuencia. Resultado POSIBLE.",
        }

    return {
        "consulta": {
            "antecedentes": ants,
            "consecuencia": consecuencia,
        },
        "mecanismo_id": None,
        "mecanismo": None,
        "efecto_estructural": None,
        "resultado": INDEFINIDO,
        "norma": None,
        "porque": (
            "Ningún mecanismo del catálogo declara admisión ni veda "
            "para esta consulta."
        ),
        "fuente": None,
        "nota": MECANICA["principio_silencio"],
    }


def correlacionar(
    antecedentes: Optional[Sequence[str]] = None,
    consecuencia: Optional[str] = None,
    *,
    desde: Optional[str] = None,
    hacia: Optional[str] = None,
) -> Dict[str, Any]:
    """
    API natural:

      correlacionar(antecedentes=[...], consecuencia="...")

    Compatibilidad par:

      correlacionar(desde=A, hacia=B)
    """
    cons = consecuencia if consecuencia is not None else hacia
    if not cons:
        return {
            "consulta": None,
            "resultado": INDEFINIDO,
            "errores": ["falta consecuencia (o hacia)"],
            "nota": "Sin consecuencia no hay evaluación.",
        }
    return evaluar(cons, antecedentes=antecedentes, desde=desde)


def resolver(desde: str, hacia: str) -> Dict[str, Any]:
    return correlacionar(desde=desde, hacia=hacia)


def mecanismo_por_id(mid: str) -> Optional[Dict[str, Any]]:
    """Los ids (C-CX-01, …) son entidades-mecanismo consultables."""
    for c in CORRELACIONES:
        if c.get("id") == mid:
            return dict(c)
    return None


def catalogo() -> Dict[str, Any]:
    """Solo conocimiento estructural (sin resultados de evaluación)."""
    return {
        "grafo_id": GRAFO_ID,
        "version": VERSION,
        "n": len(CORRELACIONES),
        "mecanismos": [
            {
                "id": c.get("id"),
                "mecanismo": c.get("mecanismo"),
                "consecuencia": c.get("consecuencia"),
                "efecto_estructural": c.get("efecto_estructural"),
                "norma": c.get("norma"),
                "n_antecedentes": len(c.get("antecedentes") or []),
            }
            for c in CORRELACIONES
        ],
        "principio_silencio": MECANICA["principio_silencio"],
        "nota": (
            "Catálogo = base de conocimiento estructural. "
            "Resultados solo existen tras evaluar(...)."
        ),
    }


def orden() -> List[str]:
    return list(MECANICA["orden"])


def indice(paso: str) -> int:
    return MECANICA["orden"].index(paso)


def precondiciones(paso: str) -> List[str]:
    i = indice(paso)
    return list(MECANICA["orden"][:i])


# ===============================================================
# SECCIÓN 6 — EXPORTS
# ===============================================================

__all__ = [
    "MECANICA",
    "GRAFO_ID",
    "VERSION",
    "POSIBLE",
    "IMPOSIBLE",
    "INDEFINIDO",
    "ADMITE",
    "VEDA",
    "CORRELACIONES",
    "evaluar",
    "correlacionar",
    "resolver",
    "mecanismo_por_id",
    "catalogo",
    "orden",
    "indice",
    "precondiciones",
]
