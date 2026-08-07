# ===============================================================
# VPSI-TRUTH — modules/cache/fo.py
# ===============================================================
#
# Diccionario oficial de eventos FO (formulas) para CACHE.
#
# No interpreta.
# No calcula.
# No deposita.
# Solo declara el vocabulario oficial de FO.
#
# Prefijo interno: FO_
# Valores registrados: fo.*  (autoidentificables)
#
# CACHE permanece neutro: recibe el evento tal cual.
# ===============================================================


# ===============================================================
# IDENTIDAD
# ===============================================================

MODULO = "FO"
NOMBRE = "formulas"
ROL = "FO"

# ===============================================================
# VERSIÓN DEL ESQUEMA DE EVENTOS FO
# ===============================================================

VERSION_EVENTOS = "1.0"

# ===============================================================
# TIPOS DE EVENTO (valores autoidentificables)
# ===============================================================

FO_TIPO_FORMULA_EJECUTADA = "fo.formula_ejecutada"
FO_TIPO_TRU_RI = "fo.tru_ri"
FO_TIPO_TRU_TOTAL = "fo.tru_total"
FO_TIPO_ESCALA = "fo.escala"
FO_TIPO_CONSTANTE_USADA = "fo.constante_usada"
FO_TIPO_RESULTADO = "fo.resultado"
FO_TIPO_ERROR = "fo.error"
FO_TIPO_RECHAZO = "fo.rechazo"

FO_TIPOS = (
    FO_TIPO_FORMULA_EJECUTADA,
    FO_TIPO_TRU_RI,
    FO_TIPO_TRU_TOTAL,
    FO_TIPO_ESCALA,
    FO_TIPO_CONSTANTE_USADA,
    FO_TIPO_RESULTADO,
    FO_TIPO_ERROR,
    FO_TIPO_RECHAZO,
)

# ===============================================================
# CATEGORÍAS (valores autoidentificables)
# ===============================================================

FO_CATEGORIA_FORMULAS = "fo.formulas"
FO_CATEGORIA_VERDAD = "fo.verdad"
FO_CATEGORIA_ESCALA = "fo.escala"
FO_CATEGORIA_CONSTANTES = "fo.constantes"

FO_CATEGORIAS = (
    FO_CATEGORIA_FORMULAS,
    FO_CATEGORIA_VERDAD,
    FO_CATEGORIA_ESCALA,
    FO_CATEGORIA_CONSTANTES,
)

# ===============================================================
# CAPACIDADES FO EN EL REGISTRO
# ===============================================================

FO_CAP_TRU_RI = "fo.tru_ri"
FO_CAP_TRU_TOTAL = "fo.tru_total"
FO_CAP_ESCALA = "fo.escala"
FO_CAP_BARRER = "fo.barrer"
FO_CAP_INVENTARIO = "fo.inventario"
FO_CAP_REPORTE = "fo.reporte"
FO_CAP_DIAGNOSTICO = "fo.diagnostico"

FO_CAPACIDADES = (
    FO_CAP_TRU_RI,
    FO_CAP_TRU_TOTAL,
    FO_CAP_ESCALA,
    FO_CAP_BARRER,
    FO_CAP_INVENTARIO,
    FO_CAP_REPORTE,
    FO_CAP_DIAGNOSTICO,
)

# ===============================================================
# ESTADOS ESPECÍFICOS FO
# (los globales viven en cache/common.py)
# ===============================================================

FO_ESTADO_OK = "fo.ok"
FO_ESTADO_ERROR = "fo.error"
FO_ESTADO_RECHAZADO = "fo.rechazado"
FO_ESTADO_DESCARTADO = "fo.descartado"

FO_ESTADOS = (
    FO_ESTADO_OK,
    FO_ESTADO_ERROR,
    FO_ESTADO_RECHAZADO,
    FO_ESTADO_DESCARTADO,
)

# ===============================================================
# CAMPOS DE PAYLOAD FO
# ===============================================================

FO_CAMPO_FORMULA = "formula"
FO_CAMPO_VARIABLES = "variables"
FO_CAMPO_RESULTADO = "resultado"
FO_CAMPO_PRECISION = "precision"
FO_CAMPO_VERSION_FORMULA = "version_formula"
FO_CAMPO_CONSTANTES = "constantes"
FO_CAMPO_ENTRADA = "entrada"
FO_CAMPO_SALIDA = "salida"
FO_CAMPO_FRACCION = "fraccion"
FO_CAMPO_DECIMAL = "decimal"
FO_CAMPO_DISPLAY = "display"
FO_CAMPO_ALPHA = "alpha"
FO_CAMPO_BETA = "beta"
FO_CAMPO_C = "C"
FO_CAMPO_L = "L"
FO_CAMPO_K = "K"
FO_CAMPO_ERROR = "error"
FO_CAMPO_DETALLE = "detalle"

FO_CAMPOS_PAYLOAD = (
    FO_CAMPO_FORMULA,
    FO_CAMPO_VARIABLES,
    FO_CAMPO_RESULTADO,
    FO_CAMPO_PRECISION,
    FO_CAMPO_VERSION_FORMULA,
    FO_CAMPO_CONSTANTES,
    FO_CAMPO_ENTRADA,
    FO_CAMPO_SALIDA,
    FO_CAMPO_FRACCION,
    FO_CAMPO_DECIMAL,
    FO_CAMPO_DISPLAY,
    FO_CAMPO_ALPHA,
    FO_CAMPO_BETA,
    FO_CAMPO_C,
    FO_CAMPO_L,
    FO_CAMPO_K,
    FO_CAMPO_ERROR,
    FO_CAMPO_DETALLE,
)

# ===============================================================
# PAYLOAD OBLIGATORIO / OPCIONAL (por tipo de evento)
# CACHE no valida estos esquemas.
# Son contrato oficial para desarrolladores y analizadores futuros.
# ===============================================================

FO_PAYLOAD_OBLIGATORIO_TRU_RI = (
    FO_CAMPO_C,
    FO_CAMPO_L,
    FO_CAMPO_K,
    FO_CAMPO_RESULTADO,
)

FO_PAYLOAD_OPCIONAL_TRU_RI = (
    FO_CAMPO_FORMULA,
    FO_CAMPO_VERSION_FORMULA,
    FO_CAMPO_DETALLE,
)

FO_PAYLOAD_OBLIGATORIO_TRU_TOTAL = (
    FO_CAMPO_C,
    FO_CAMPO_L,
    FO_CAMPO_K,
    FO_CAMPO_ALPHA,
    FO_CAMPO_BETA,
    FO_CAMPO_RESULTADO,
)

FO_PAYLOAD_OPCIONAL_TRU_TOTAL = (
    FO_CAMPO_FORMULA,
    FO_CAMPO_VERSION_FORMULA,
    FO_CAMPO_FRACCION,
    FO_CAMPO_DECIMAL,
    FO_CAMPO_DISPLAY,
    FO_CAMPO_DETALLE,
)

FO_PAYLOAD_OBLIGATORIO_ESCALA = (
    FO_CAMPO_ENTRADA,
    FO_CAMPO_SALIDA,
)

FO_PAYLOAD_OPCIONAL_ESCALA = (
    FO_CAMPO_PRECISION,
    FO_CAMPO_FRACCION,
    FO_CAMPO_DECIMAL,
    FO_CAMPO_DISPLAY,
    FO_CAMPO_DETALLE,
)

FO_PAYLOAD_OBLIGATORIO_ERROR = (
    FO_CAMPO_ERROR,
)

FO_PAYLOAD_OPCIONAL_ERROR = (
    FO_CAMPO_DETALLE,
    FO_CAMPO_FORMULA,
    FO_CAMPO_ENTRADA,
)

# ===============================================================
# ESQUEMA DE EVENTOS FO
# ===============================================================

FO_ESQUEMA_EVENTOS = {
    FO_TIPO_TRU_RI: {
        "obligatorios": FO_PAYLOAD_OBLIGATORIO_TRU_RI,
        "opcionales": FO_PAYLOAD_OPCIONAL_TRU_RI,
    },
    FO_TIPO_TRU_TOTAL: {
        "obligatorios": FO_PAYLOAD_OBLIGATORIO_TRU_TOTAL,
        "opcionales": FO_PAYLOAD_OPCIONAL_TRU_TOTAL,
    },
    FO_TIPO_ESCALA: {
        "obligatorios": FO_PAYLOAD_OBLIGATORIO_ESCALA,
        "opcionales": FO_PAYLOAD_OPCIONAL_ESCALA,
    },
    FO_TIPO_ERROR: {
        "obligatorios": FO_PAYLOAD_OBLIGATORIO_ERROR,
        "opcionales": FO_PAYLOAD_OPCIONAL_ERROR,
    },
    FO_TIPO_FORMULA_EJECUTADA: {
        "obligatorios": (FO_CAMPO_FORMULA, FO_CAMPO_RESULTADO),
        "opcionales": (
            FO_CAMPO_VARIABLES,
            FO_CAMPO_CONSTANTES,
            FO_CAMPO_ENTRADA,
            FO_CAMPO_SALIDA,
            FO_CAMPO_VERSION_FORMULA,
            FO_CAMPO_DETALLE,
        ),
    },
    FO_TIPO_CONSTANTE_USADA: {
        "obligatorios": (FO_CAMPO_CONSTANTES,),
        "opcionales": (FO_CAMPO_DETALLE, FO_CAMPO_FORMULA),
    },
    FO_TIPO_RESULTADO: {
        "obligatorios": (FO_CAMPO_RESULTADO,),
        "opcionales": (
            FO_CAMPO_FRACCION,
            FO_CAMPO_DECIMAL,
            FO_CAMPO_DISPLAY,
            FO_CAMPO_DETALLE,
        ),
    },
    FO_TIPO_RECHAZO: {
        "obligatorios": (FO_CAMPO_ERROR,),
        "opcionales": (FO_CAMPO_DETALLE, FO_CAMPO_ENTRADA),
    },
}

# ===============================================================
# CAMPOS DE METADATA ESPECÍFICOS FO
# (además de los universales en cache/common.py)
# ===============================================================

FO_META_VERSION_EVENTOS = "version_eventos"
FO_META_MODULO = "modulo"
FO_META_ROL = "rol"

FO_CAMPOS_METADATA = (
    FO_META_VERSION_EVENTOS,
    FO_META_MODULO,
    FO_META_ROL,
)

# ===============================================================
# FIN DEL ARCHIVO
# ===============================================================
