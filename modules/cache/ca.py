# ===============================================================
# VPSI-TRUTH — modules/cache/ca.py
# ===============================================================
#
# Diccionario oficial de eventos CA (calculator) para CACHE.
#
# No interpreta.
# No calcula.
# No deposita.
# Solo declara el vocabulario oficial de CA.
#
# Prefijo interno: CA_
# Valores registrados: ca.*  (autoidentificables)
#
# CACHE permanece neutro: recibe el evento tal cual.
# ===============================================================


# ===============================================================
# IDENTIDAD
# ===============================================================

MODULO = "CA"
NOMBRE = "calculator"
ROL = "CA"

# ===============================================================
# VERSIÓN DEL ESQUEMA DE EVENTOS CA
# ===============================================================

VERSION_EVENTOS = "1.0"

# ===============================================================
# TIPOS DE EVENTO (valores autoidentificables)
# ===============================================================

CA_TIPO_CALCULO = "ca.calculo"
CA_TIPO_COHERENCIA = "ca.coherencia"
CA_TIPO_LOGICA = "ca.logica"
CA_TIPO_CORRELACION = "ca.correlacion"
CA_TIPO_CONTEOS = "ca.conteos"
CA_TIPO_FACTORES = "ca.factores"
CA_TIPO_REPRESENTAR = "ca.representar"
CA_TIPO_RESULTADO = "ca.resultado"
CA_TIPO_ERROR = "ca.error"
CA_TIPO_RECHAZO = "ca.rechazo"
CA_TIPO_BASE_NULA = "ca.base_nula"

CA_TIPOS = (
    CA_TIPO_CALCULO,
    CA_TIPO_COHERENCIA,
    CA_TIPO_LOGICA,
    CA_TIPO_CORRELACION,
    CA_TIPO_CONTEOS,
    CA_TIPO_FACTORES,
    CA_TIPO_REPRESENTAR,
    CA_TIPO_RESULTADO,
    CA_TIPO_ERROR,
    CA_TIPO_RECHAZO,
    CA_TIPO_BASE_NULA,
)

# ===============================================================
# CATEGORÍAS (valores autoidentificables)
# ===============================================================

CA_CATEGORIA_CALCULO = "ca.calculo"
CA_CATEGORIA_FACTORES = "ca.factores"
CA_CATEGORIA_CONTEOS = "ca.conteos"
CA_CATEGORIA_REPRESENTACION = "ca.representacion"
CA_CATEGORIA_DOMINIO = "ca.dominio"

CA_CATEGORIAS = (
    CA_CATEGORIA_CALCULO,
    CA_CATEGORIA_FACTORES,
    CA_CATEGORIA_CONTEOS,
    CA_CATEGORIA_REPRESENTACION,
    CA_CATEGORIA_DOMINIO,
)

# ===============================================================
# CAPACIDADES CA EN EL REGISTRO
# ===============================================================

CA_CAP_CALCULAR = "ca.calcular"
CA_CAP_CALCULAR_C = "ca.calcular_c"
CA_CAP_CALCULAR_L = "ca.calcular_l"
CA_CAP_CALCULAR_K = "ca.calcular_k"
CA_CAP_COHERENCIA = "ca.coherencia"
CA_CAP_LOGICA = "ca.logica"
CA_CAP_CORRELACION = "ca.correlacion"
CA_CAP_EXTRAER_CONTEOS = "ca.extraer_conteos"
CA_CAP_INYECTAR = "ca.inyectar_en_peticion"
CA_CAP_REPRESENTAR = "ca.representar"
CA_CAP_VERIFICAR_C = "ca.verificar_c"
CA_CAP_VERIFICAR_L = "ca.verificar_l"
CA_CAP_VERIFICAR_K = "ca.verificar_k"
CA_CAP_BARRER = "ca.barrer"
CA_CAP_INVENTARIO = "ca.inventario"
CA_CAP_REPORTE = "ca.reporte"
CA_CAP_DIAGNOSTICO = "ca.diagnostico"

CA_CAPACIDADES = (
    CA_CAP_CALCULAR,
    CA_CAP_CALCULAR_C,
    CA_CAP_CALCULAR_L,
    CA_CAP_CALCULAR_K,
    CA_CAP_COHERENCIA,
    CA_CAP_LOGICA,
    CA_CAP_CORRELACION,
    CA_CAP_EXTRAER_CONTEOS,
    CA_CAP_INYECTAR,
    CA_CAP_REPRESENTAR,
    CA_CAP_VERIFICAR_C,
    CA_CAP_VERIFICAR_L,
    CA_CAP_VERIFICAR_K,
    CA_CAP_BARRER,
    CA_CAP_INVENTARIO,
    CA_CAP_REPORTE,
    CA_CAP_DIAGNOSTICO,
)

# ===============================================================
# ESTADOS ESPECÍFICOS CA
# (los globales viven en cache/common.py)
# ===============================================================

CA_ESTADO_OK = "ca.ok"
CA_ESTADO_ERROR = "ca.error"
CA_ESTADO_RECHAZADO = "ca.rechazado"
CA_ESTADO_DESCARTADO = "ca.descartado"
CA_ESTADO_UNDEFINED = "ca.undefined"

CA_ESTADOS = (
    CA_ESTADO_OK,
    CA_ESTADO_ERROR,
    CA_ESTADO_RECHAZADO,
    CA_ESTADO_DESCARTADO,
    CA_ESTADO_UNDEFINED,
)

# ===============================================================
# CAMPOS DE PAYLOAD CA
# ===============================================================

CA_CAMPO_C = "C"
CA_CAMPO_L = "L"
CA_CAMPO_K = "K"
CA_CAMPO_M = "m"
CA_CAMPO_K_PESO = "k"
CA_CAMPO_P = "p"
CA_CAMPO_R = "r"
CA_CAMPO_C_BASE = "c"
CA_CAMPO_F = "f"
CA_CAMPO_BASE_NULA = "base_nula"
CA_CAMPO_O_PRESENTE = "o_presente"
CA_CAMPO_O_CONTEXT = "O_context"
CA_CAMPO_RESULTADO = "resultado"
CA_CAMPO_FRACCION = "fraccion"
CA_CAMPO_DECIMAL = "decimal"
CA_CAMPO_DISPLAY = "display"
CA_CAMPO_NUMERADOR = "numerador"
CA_CAMPO_DENOMINADOR = "denominador"
CA_CAMPO_PRECISION = "precision"
CA_CAMPO_COMPROMISOS = "compromisos"
CA_CAMPO_CONTRADICCIONES = "contradicciones"
CA_CAMPO_POSTURAS = "posturas"
CA_CAMPO_REVERSIONES = "reversiones"
CA_CAMPO_AFIRMACIONES = "afirmaciones"
CA_CAMPO_AFIRMACIONES_FALSAS = "afirmaciones_falsas"
CA_CAMPO_ENTRADA = "entrada"
CA_CAMPO_SALIDA = "salida"
CA_CAMPO_ERROR = "error"
CA_CAMPO_DETALLE = "detalle"
CA_CAMPO_ID_CALCULO = "id_calculo"

CA_CAMPOS_PAYLOAD = (
    CA_CAMPO_C,
    CA_CAMPO_L,
    CA_CAMPO_K,
    CA_CAMPO_M,
    CA_CAMPO_K_PESO,
    CA_CAMPO_P,
    CA_CAMPO_R,
    CA_CAMPO_C_BASE,
    CA_CAMPO_F,
    CA_CAMPO_BASE_NULA,
    CA_CAMPO_O_PRESENTE,
    CA_CAMPO_O_CONTEXT,
    CA_CAMPO_RESULTADO,
    CA_CAMPO_FRACCION,
    CA_CAMPO_DECIMAL,
    CA_CAMPO_DISPLAY,
    CA_CAMPO_NUMERADOR,
    CA_CAMPO_DENOMINADOR,
    CA_CAMPO_PRECISION,
    CA_CAMPO_COMPROMISOS,
    CA_CAMPO_CONTRADICCIONES,
    CA_CAMPO_POSTURAS,
    CA_CAMPO_REVERSIONES,
    CA_CAMPO_AFIRMACIONES,
    CA_CAMPO_AFIRMACIONES_FALSAS,
    CA_CAMPO_ENTRADA,
    CA_CAMPO_SALIDA,
    CA_CAMPO_ERROR,
    CA_CAMPO_DETALLE,
    CA_CAMPO_ID_CALCULO,
)

# ===============================================================
# PAYLOAD OBLIGATORIO / OPCIONAL (por tipo de evento)
# CACHE no valida estos esquemas.
# ===============================================================

CA_PAYLOAD_OBLIGATORIO_COHERENCIA = (
    CA_CAMPO_M,
    CA_CAMPO_K_PESO,
    CA_CAMPO_RESULTADO,
)

CA_PAYLOAD_OPCIONAL_COHERENCIA = (
    CA_CAMPO_BASE_NULA,
    CA_CAMPO_C,
    CA_CAMPO_DETALLE,
)

CA_PAYLOAD_OBLIGATORIO_LOGICA = (
    CA_CAMPO_P,
    CA_CAMPO_R,
    CA_CAMPO_RESULTADO,
)

CA_PAYLOAD_OPCIONAL_LOGICA = (
    CA_CAMPO_BASE_NULA,
    CA_CAMPO_L,
    CA_CAMPO_DETALLE,
)

CA_PAYLOAD_OBLIGATORIO_CORRELACION = (
    CA_CAMPO_C_BASE,
    CA_CAMPO_F,
    CA_CAMPO_O_PRESENTE,
    CA_CAMPO_RESULTADO,
)

CA_PAYLOAD_OPCIONAL_CORRELACION = (
    CA_CAMPO_BASE_NULA,
    CA_CAMPO_O_CONTEXT,
    CA_CAMPO_K,
    CA_CAMPO_DETALLE,
)

CA_PAYLOAD_OBLIGATORIO_FACTORES = (
    CA_CAMPO_C,
    CA_CAMPO_L,
    CA_CAMPO_K,
)

CA_PAYLOAD_OPCIONAL_FACTORES = (
    CA_CAMPO_ID_CALCULO,
    CA_CAMPO_FRACCION,
    CA_CAMPO_DECIMAL,
    CA_CAMPO_DISPLAY,
    CA_CAMPO_DETALLE,
)

CA_PAYLOAD_OBLIGATORIO_CONTEOS = (
    CA_CAMPO_M,
    CA_CAMPO_P,
    CA_CAMPO_C_BASE,
)

CA_PAYLOAD_OPCIONAL_CONTEOS = (
    CA_CAMPO_K_PESO,
    CA_CAMPO_R,
    CA_CAMPO_F,
    CA_CAMPO_COMPROMISOS,
    CA_CAMPO_CONTRADICCIONES,
    CA_CAMPO_POSTURAS,
    CA_CAMPO_REVERSIONES,
    CA_CAMPO_AFIRMACIONES,
    CA_CAMPO_AFIRMACIONES_FALSAS,
    CA_CAMPO_DETALLE,
)

CA_PAYLOAD_OBLIGATORIO_REPRESENTAR = (
    CA_CAMPO_ENTRADA,
    CA_CAMPO_SALIDA,
)

CA_PAYLOAD_OPCIONAL_REPRESENTAR = (
    CA_CAMPO_FRACCION,
    CA_CAMPO_DECIMAL,
    CA_CAMPO_DISPLAY,
    CA_CAMPO_NUMERADOR,
    CA_CAMPO_DENOMINADOR,
    CA_CAMPO_PRECISION,
    CA_CAMPO_DETALLE,
)

CA_PAYLOAD_OBLIGATORIO_ERROR = (
    CA_CAMPO_ERROR,
)

CA_PAYLOAD_OPCIONAL_ERROR = (
    CA_CAMPO_DETALLE,
    CA_CAMPO_ENTRADA,
)

# ===============================================================
# ESQUEMA DE EVENTOS CA
# ===============================================================

CA_ESQUEMA_EVENTOS = {
    CA_TIPO_COHERENCIA: {
        "obligatorios": CA_PAYLOAD_OBLIGATORIO_COHERENCIA,
        "opcionales": CA_PAYLOAD_OPCIONAL_COHERENCIA,
    },
    CA_TIPO_LOGICA: {
        "obligatorios": CA_PAYLOAD_OBLIGATORIO_LOGICA,
        "opcionales": CA_PAYLOAD_OPCIONAL_LOGICA,
    },
    CA_TIPO_CORRELACION: {
        "obligatorios": CA_PAYLOAD_OBLIGATORIO_CORRELACION,
        "opcionales": CA_PAYLOAD_OPCIONAL_CORRELACION,
    },
    CA_TIPO_FACTORES: {
        "obligatorios": CA_PAYLOAD_OBLIGATORIO_FACTORES,
        "opcionales": CA_PAYLOAD_OPCIONAL_FACTORES,
    },
    CA_TIPO_CONTEOS: {
        "obligatorios": CA_PAYLOAD_OBLIGATORIO_CONTEOS,
        "opcionales": CA_PAYLOAD_OPCIONAL_CONTEOS,
    },
    CA_TIPO_REPRESENTAR: {
        "obligatorios": CA_PAYLOAD_OBLIGATORIO_REPRESENTAR,
        "opcionales": CA_PAYLOAD_OPCIONAL_REPRESENTAR,
    },
    CA_TIPO_CALCULO: {
        "obligatorios": (CA_CAMPO_RESULTADO,),
        "opcionales": (
            CA_CAMPO_C,
            CA_CAMPO_L,
            CA_CAMPO_K,
            CA_CAMPO_ID_CALCULO,
            CA_CAMPO_DETALLE,
        ),
    },
    CA_TIPO_RESULTADO: {
        "obligatorios": (CA_CAMPO_RESULTADO,),
        "opcionales": (
            CA_CAMPO_FRACCION,
            CA_CAMPO_DECIMAL,
            CA_CAMPO_DISPLAY,
            CA_CAMPO_DETALLE,
        ),
    },
    CA_TIPO_ERROR: {
        "obligatorios": CA_PAYLOAD_OBLIGATORIO_ERROR,
        "opcionales": CA_PAYLOAD_OPCIONAL_ERROR,
    },
    CA_TIPO_RECHAZO: {
        "obligatorios": (CA_CAMPO_ERROR,),
        "opcionales": (CA_CAMPO_DETALLE, CA_CAMPO_ENTRADA),
    },
    CA_TIPO_BASE_NULA: {
        "obligatorios": (CA_CAMPO_BASE_NULA, CA_CAMPO_RESULTADO),
        "opcionales": (CA_CAMPO_DETALLE,),
    },
}

# ===============================================================
# CAMPOS DE METADATA ESPECÍFICOS CA
# ===============================================================

CA_META_VERSION_EVENTOS = "version_eventos"
CA_META_MODULO = "modulo"
CA_META_ROL = "rol"

CA_CAMPOS_METADATA = (
    CA_META_VERSION_EVENTOS,
    CA_META_MODULO,
    CA_META_ROL,
)

# ===============================================================
# FIN DEL ARCHIVO
# ===============================================================
