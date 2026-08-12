# ===============================================================
# VPSI-TRUTH — modules/catalogo_citaciones/ids_sistema.py
# ===============================================================
#
# Catálogo de IDs del sistema.
# Vocabulario oficial del repositorio.
#
# Solo declara identificadores. No calcula. No orquesta.
#
# CC (catalogo_citaciones) lee automáticamente:
#   - IDS          → lista plana unificada
#   - CATEGORIAS   → entradas con clase semántica
#
# ===============================================================


# ===============================================================
# MÓDULOS (roles)
# ===============================================================

IDS_MODULOS = [
    "CA",                       # calculator
    "FO",                       # formulas
    "TT",                       # tru_totales
    "CC",                       # catalogo_citaciones
    "CT",                       # constante
    "AX",                       # axiomas
    "MC",                       # correlacion_mecanica
    "CX",                       # contexto
    "DG",                       # diagnostico
    "EN",                       # engine
]

# ===============================================================
# ARCHIVOS
# ===============================================================

IDS_ARCHIVOS = [
    # calculator
    "calculator",
    "coherencia",
    "logica",
    "correlacion_k",
    "conteos",
    "escalas_ids",
    # formulas
    "formulas",
    "truth",
    "escala",
    # catálogos
    "tru_totales",
    "catalogo_citaciones",
]

# ===============================================================
# FUNCIONES / CAPACIDADES
# ===============================================================

IDS_FUNCIONES = [
    # calculator — funciones puras
    "coherencia_fn",            # C(m, k, base_nula)
    "logica_fn",                # L(p, r, base_nula)
    "correlacion_fn",           # K(c, f, o_presente, base_nula)
    # calculator — adaptadores
    "calcular_c",
    "calcular_l",
    "calcular_k",
    "verificar_c",
    "verificar_l",
    "verificar_k",
    "extraer_conteos",
    "inyectar_en_peticion",
    "leer_ids_escala",
    "representar",
    # formulas
    "tru_ri",
    "tru_total",
    "aplicar_escala",
    "verificar_escala",
    # tru_totales
    "resolver_pedido",
    "categorias",
    "por_id",
    "ids",
    "es_valida",
    # catalogo_citaciones
    "esquema",
    # transversales
    "barrer",
    "verificar",
    "verificar_salida",
    "inventario",
    "reporte",
    "diagnostico",
    "recolectar",
    # engine
    "descubrir",
    "resolver_dependencias",
    "ejecutar_capacidad",
    "combinar_resultados",
]

# ===============================================================
# FACTORES Y MAGNITUDES
# ===============================================================

IDS_FACTORES = [
    "C",                        # coherencia
    "L",                        # logica / invariancia
    "K",                        # correlacion
    "Tru_Ri",
    "Tru_total",
    "ALPHA",                    # 26/27
    "BETA",                     # 1/27
]

# ===============================================================
# VARIABLES MATEMÁTICAS
# ===============================================================

IDS_VARIABLES = [
    "m",                        # tamaño base compromisos (C)
    "k",                        # peso contradicciones (C)
    "p",                        # tamaño base posturas (L)
    "r",                        # peso reversiones (L)
    "c",                        # tamaño base afirmaciones (K)
    "f",                        # peso divergencias (K)
]

# ===============================================================
# CLAVES DE CONTEO
# ===============================================================

IDS_CONTEO = [
    "compromisos",
    "contradicciones",
    "posturas",
    "reversiones",
    "afirmaciones",
    "afirmaciones_falsas",
]

# ===============================================================
# META / DOMINIO
# ===============================================================

IDS_META = [
    "base_nula",
    "base_nula_C",
    "base_nula_L",
    "base_nula_K",
    "o_presente",
    "O_context",
    "contexto",
    "UNDEFINED",
]

# ===============================================================
# ESCALAS DE ALCANCE (TT)
# ===============================================================

IDS_ESCALAS = [
    "tru_atomo",
    "tru_frase",
    "tru_sujeto",
    "tru_conversacion",
    "tru_repositorio",
]

# ===============================================================
# REPRESENTACIÓN EN ESCALA
# ===============================================================

IDS_REPRESENTACION = [
    "fraccion",
    "decimal",
    "display",
    "numerador",
    "denominador",
    "precision",
    "valor",
]

# ===============================================================
# CONTRATO — campos estructurales
# ===============================================================

IDS_CONTRATO = [
    "CONTENEDOR",
    "capacidades",
    "capacidades_meta",
    "autoriza_engine",
    "conocimiento_exportable",
    "requiere",
    "reporting",
    "invariantes",
    "estados_validos",
    "ESQUEMA_CATEGORIA",
]

# ===============================================================
# ESTADOS
# ===============================================================

IDS_ESTADOS = [
    "NO_INICIADO",
    "OPERATIVO",
    "DEGRADADO",
    "RECHAZADO",
]

# ===============================================================
# AGENTES
# ===============================================================

IDS_AGENTES = [
    "Engine",
    "Omega",
    "OmegaReport",
]

# ===============================================================
# CATEGORIAS CON CLASE SEMÁNTICA Y METADATOS ENGINE
# ===============================================================

def _cat(id_: str, clase: str, unidad: str, enunciado: str) -> dict:
    # Normalización consistente en minúsculas para evitar choques en el map por_id
    normalized_id = id_.lower()
    return {
        "id": normalized_id,
        "nombre": id_,
        "unidad": unidad,
        "enunciado": enunciado,
        "nivel_fractal": 1,
        "jurisdiccion": "SISTEMA",
        "fuente_modulo": "CC",
        "origen": "ids_sistema",
        "version": "1.0",
        "notas": "clase={0}".format(clase),
    }


# Construcción estructurada desduplicada por ID
_BRUTAS = (
    [
        _cat(x, "modulo", "rol", "Módulo / rol del sistema: {0}".format(x))
        for x in IDS_MODULOS
    ]
    + [
        _cat(x, "archivo", "archivo", "Archivo del repositorio: {0}".format(x))
        for x in IDS_ARCHIVOS
    ]
    + [
        _cat(x, "funcion", "funcion", "Función o capacidad: {0}".format(x))
        for x in IDS_FUNCIONES
    ]
    + [
        _cat(x, "factor", "factor", "Factor o magnitud: {0}".format(x))
        for x in IDS_FACTORES
    ]
    + [
        _cat(x, "variable", "variable", "Variable matemática: {0}".format(x))
        for x in IDS_VARIABLES
    ]
    + [
        _cat(x, "conteo", "clave", "Clave de conteo: {0}".format(x))
        for x in IDS_CONTEO
    ]
    + [
        _cat(x, "meta", "meta", "Metadato de dominio: {0}".format(x))
        for x in IDS_META
    ]
    + [
        _cat(x, "escala", "escala", "Escala de alcance Tru: {0}".format(x))
        for x in IDS_ESCALAS
    ]
    + [
        _cat(x, "representacion", "campo", "Campo de representación: {0}".format(x))
        for x in IDS_REPRESENTACION
    ]
    + [
        _cat(x, "contrato", "campo", "Campo estructural de contrato: {0}".format(x))
        for x in IDS_CONTRATO
    ]
    + [
        _cat(x, "estado", "estado", "Estado de módulo: {0}".format(x))
        for x in IDS_ESTADOS
    ]
    + [
        _cat(x, "agente", "agente", "Agente del sistema: {0}".format(x))
        for x in IDS_AGENTES
    ]
)

# Desduplicación garantizada respetando el primer tipo asignado
_CATEGORIAS_MAP = {}
for entry in _BRUTAS:
    key = entry["id"]
    if key not in _CATEGORIAS_MAP:
        _CATEGORIAS_MAP[key] = entry

CATEGORIAS = list(_CATEGORIAS_MAP.values())

# ===============================================================
# IDS PLANO (Derivado de CATEGORIAS para garantizar sincronía 1:1)
# ===============================================================

IDS = [item["id"] for item in CATEGORIAS]

# ===============================================================
# FIN DEL ARCHIVO
# ===============================================================
