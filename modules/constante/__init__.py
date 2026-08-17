# ===============================================================
# VPSI-TRUTH — modules/constante/__init__.py
# ===============================================================
#
# MÓDULO:              constante
# ID:                  CT
# Rol:                 CT
# Versión módulo:      2.1
# Versión contrato:    1.0
# Esquema contrato:    VPSI-CONTRACT-1.0
# Estabilidad:         ESTABLE
# Compatible desde:    1.0
# API Engine:          >=1.0
#
# Función:
#   Única autoridad del dominio de constantes del sistema VPSI.
#   Toda constante oficial utilizada por cualquier módulo debe ser
#   declarada, validada y exportada por CT. ALPHA y BETA son las
#   constantes fundacionales estructurales.
#
# Qué hace:
#   - Expone ALPHA = 26/27 y BETA = 1/27 (fundacionales)
#   - Descubre todas las constantes oficiales declaradas en el módulo
#   - Valida, lista y busca constantes
#   - Audita coherencia del dominio de constantes
#   - Inventario, reporte y diagnóstico del conjunto completo
#
# Qué NO hace:
#   - No calcula Tru_total ni Tru_Ri
#   - No clasifica entrada de usuario
#   - No orquesta el sistema (eso es Engine)
#   - No modifica otros módulos
#
# Responsabilidad:
#   Ser la única autoridad del dominio de constantes del sistema VPSI.
#   FO, AX, MC y el resto no definen constantes: todo pasa por CT.
#
# Autoridad:
#   - Exponer ALPHA y BETA
#   - Descubrir, validar y listar constantes oficiales
#   - Auditar coherencia del dominio de constantes
#   - Reportar inventario completo de constantes
#
# Conocimiento exportable:
#   ALPHA, BETA, constantes, inventario, estado, reporte, diagnostico
#
# Relación con Engine:
#   Engine descubre este CONTENEDOR y ejecuta las capacidades
#   declaradas. CT es la autoridad de dominio de constantes;
#   Engine ejerce la agencia autorizada por el contrato.
#
# Relación con Omega:
#   Omega no calcula nada de CT. Solo presenta lo que Engine entrega.
#
# ===============================================================

# ===============================================================
# IMPORTACIONES
# ===============================================================

from __future__ import annotations

import importlib.util
import math
import sys

from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List, Optional

# ===============================================================
# CONFIGURACIÓN NUMÉRICA
# ===============================================================

# Precisión decimal utilizada únicamente para representación y cálculo
# decimal de precisión controlada. No sustituye la representación exacta.
getcontext().prec = 50

# ===============================================================
# FIN IMPORTACIONES
# ===============================================================
# ===============================================================
# SECCIÓN 1 — CONSTANTES
# ===============================================================


# ===============================================================
# 1.1 — IDENTIDAD DEL MÓDULO
# ===============================================================

ID_MODULO = "CT"
NOMBRE_MODULO = "constante"
ROL_MODULO = "CT"

VERSION_MODULO = "2.1"
VERSION_CONTRATO = "1.0"
ESQUEMA_CONTRATO = "VPSI-CONTRACT-1.0"

COMPATIBLE_DESDE = "1.0"
API_ENGINE = ">=1.0"
ESTABILIDAD = "ESTABLE"


# ===============================================================
# 1.2 — ESTADOS CONTRACTUALES
# ===============================================================

ESTADO_NO_INICIADO = "NO_INICIADO"
ESTADO_OPERATIVO = "OPERATIVO"
ESTADO_DEGRADADO = "DEGRADADO"
ESTADO_RECHAZADO = "RECHAZADO"

ESTADOS_VALIDOS = (
    ESTADO_NO_INICIADO,
    ESTADO_OPERATIVO,
    ESTADO_DEGRADADO,
    ESTADO_RECHAZADO,
)


# ===============================================================
# 1.3 — INVARIANTES CONTRACTUALES
# ===============================================================

INVARIANTES = (
    "el id del módulo nunca cambia",
    "el rol nunca cambia",
    "ALPHA y BETA son invariantes del cubo 3x3x3 en R³",
    "ALPHA + BETA == 1",
    "CT es la única autoridad del dominio de constantes",
    "las capacidades declaradas son siempre callables tras la resolución",
    "este módulo no modifica el estado de otros módulos",
    "este módulo siempre puede reportar su propio estado",
)


# ===============================================================
# 1.4 — CONSTANTES FUNDACIONALES
# ===============================================================

ALPHA = Fraction(26, 27)
BETA = Fraction(1, 27)

CONSTANTES_FUNDACIONALES: Dict[str, Any] = {
    "ALPHA": ALPHA,
    "BETA": BETA,
}

FUNDACIONALES = frozenset(CONSTANTES_FUNDACIONALES.keys())


# ===============================================================
# 1.5 — ESPECIFICACIÓN DE CONSTANTES
# ===============================================================

CAMPOS_OBLIGATORIOS_CONSTANTE = (
    "nombre",
    "valor",
    "tipo",
    "origen",
    "descripcion",
)


# ===============================================================
# FIN SECCIÓN 1
# ===============================================================


# ===============================================================
# SECCIÓN 2 — CONFIGURACIÓN
# ===============================================================


# ===============================================================
# 2.1 — RUTA DEL MÓDULO
# ===============================================================

_DIR = Path(__file__).parent


# ===============================================================
# FIN SECCIÓN 2
# ===============================================================


# ===============================================================
# SECCIÓN 3 — DEFINICIONES
# ===============================================================


# ===============================================================
# 3.1 — EXCEPCIONES CONTRACTUALES
# ===============================================================

class ContratoInvalido(Exception):
    """El CONTENEDOR no cumple el esquema o la resolución falló."""
    pass


# ===============================================================
# FIN SECCIÓN 3
# ===============================================================

# ===============================================================
# SECCIÓN 4 — CONTRATO OFICIAL DEL MÓDULO
# ===============================================================

CONTENEDOR: Dict[str, Any] = {


    # ===========================================================
    # 4.1 — ESQUEMA CONTRACTUAL
    # ===========================================================

    "esquema": ESQUEMA_CONTRATO,
    "version_contrato": VERSION_CONTRATO,
    "version_modulo": VERSION_MODULO,
    "estabilidad": ESTABILIDAD,
    "compatible_desde": COMPATIBLE_DESDE,
    "api_engine": API_ENGINE,


    # ===========================================================
    # 4.2 — IDENTIDAD DEL MÓDULO
    # ===========================================================

    "id": ID_MODULO,
    "nombre": NOMBRE_MODULO,
    "rol": ROL_MODULO,

    "descripcion": (
        "Unica autoridad del dominio de constantes del sistema VPSI. "
        "Toda constante oficial utilizada por cualquier modulo debe ser "
        "declarada, validada y exportada por CT. ALPHA y BETA son las "
        "constantes fundacionales estructurales (cubo 3x3x3 en R3)."
    ),


    # ===========================================================
    # 4.3 — PROPÓSITO Y FUNCIÓN
    # ===========================================================

    "funcion": (
        "Ser la unica autoridad del dominio de constantes del sistema VPSI. "
        "Descubrir, validar, integrar, auditar y exportar todas las "
        "constantes oficiales. ALPHA y BETA constituyen las constantes "
        "fundacionales del sistema."
    ),

    "no_hace": [
        "No calcula Tru_total ni Tru_Ri",
        "No clasifica entrada de usuario",
        "No orquesta el sistema (eso es Engine)",
        "No modifica otros modulos",
        "No permite que FO, AX o MC definan constantes",
    ],


    # ===========================================================
    # 4.4 — AUTORIDAD
    # ===========================================================

    "autoridad": [
        "Unica autoridad del dominio de constantes",
        "Exponer ALPHA = 26/27 y BETA = 1/27",
        "Descubrir y validar constantes oficiales del modulo",
        "Listar y buscar constantes",
        "Auditar coherencia del dominio de constantes",
        "Reportar inventario completo de constantes",
        "Reportar estado y diagnostico propios",
    ],


    # ===========================================================
    # 4.5 — CONOCIMIENTO EXPORTABLE
    # ===========================================================

    "conocimiento_exportable": [
        "ALPHA",
        "BETA",
        "constantes",
        "inventario",
        "estado",
        "reporte",
        "diagnostico",
    ],


    # ===========================================================
    # 4.6 — ACCESO CONTRACTUAL
    # ===========================================================

    "acceso": {
        "nivel": "completo",
        "descripcion": "Acceso total a recursos del módulo",
    },


    # ===========================================================
    # 4.7 — DEPENDENCIAS
    # ===========================================================

    "requiere": [
        "CT",
        "AX",
        "FO",
        "MC",
        "SF",
        "CA",
        "CX",
        "DI",
        "RE",
        "VX",
        "TX",
        "CH",
        "CIT",
        "TT",
        "CE",
        "CC",
    ],


    # ===========================================================
    # 4.8 — ACCESO A ARCHIVOS
    # ===========================================================
    #
    # Acceso declarado por el contrato del módulo.
    #

    "acceso_archivos": ["*"],


    # ===========================================================
    # 4.9 — VALIDACIÓN DE ESQUEMA
    # ===========================================================
    #
    # Ámbito declarado para validación de esquema a nivel módulo.
    #

    "validar_esquema": ["*"],


    # ===========================================================
    # 5 — AUTORIZACIÓN AL ENGINE
    # ===========================================================
    #
    # Este bloque declara los permisos contractuales del Engine
    # sobre CT.
    #
    # La autorización no constituye por sí misma una implementación.
    # Las capacidades ejecutables serán declaradas y resueltas
    # posteriormente en la superficie "capacidades".
    #


    "autoriza_engine": {


        # =======================================================
        # 5.1 — PERMISOS BASE
        # =======================================================

        "leer": True,
        "ejecutar": True,
        "consultar": True,
        "recombinar": True,
        "reportar": True,
        "auditar": True,
        "inventariar": True,


        # =======================================================
        # 5.2 — PERMISOS DE ESCRITURA
        # =======================================================

        "alterar": False,
        "crear": True,
        "actualizar": False,


        # =======================================================
        # 5.3 — PERMISOS DE PROCESAMIENTO
        # =======================================================

        "validar": True,
        "procesar": True,
        "analizar": True,
        "generar": True,


        # =======================================================
        # 5.4 — PERMISOS DE DATOS
        # =======================================================

        "exportar": True,
        "importar": True,
        "respaldar": True,
        "recuperar": True,
        "sincronizar": True,


        # =======================================================
        # 5.5 — PERMISOS DE MONITOREO
        # =======================================================

        "monitorear": True,
        "metricas": True,
        "diagnostico": True,


        # =======================================================
        # 6 — PERMISOS DE ESTADO
        # =======================================================

        "estado": True,
        "version": True,
        "salud": True,
        "inventario": True,
        "capacidades": True,
        "errores": True,
        "advertencias": True,
        "dependencias": True,
        "contrato": True,
        "conocimiento": True,
        "reporte": True,


        # =======================================================
        # 6.1 — CAPACIDADES ARQUITECTÓNICAS AUTORIZADAS
        # =======================================================
        #
        # Estas banderas autorizan explícitamente al Engine a
        # ejercer las tres capacidades arquitectónicas incorporadas
        # a la superficie callable de CT.
        #
        # La implementación callable se declara posteriormente.
        #

        "ejecutar_total": True,
        "inspeccionar": True,
        "registrar_inventario": True,


        # =======================================================
        # 6.2 — PERMISOS OBLIGATORIOS DE ENGINE
        # =======================================================

        "validar_esquema": True,
        "acceso_archivos": True,
    },


    # ===========================================================
    # FIN SECCIÓN 4 — CONTINUACIÓN EN SIGUIENTES BLOQUES
    # ===========================================================

    # ============================================================
    # 7 — METADATOS DE CAPACIDADES (1:1 OBLIGATORIO)
    # ============================================================
    #
    # Cada entrada de CONTENEDOR["capacidades"] DEBE poseer una
    # entrada correspondiente en CONTENEDOR["capacidades_meta"].
    #
    # Las tres capacidades arquitectónicas de Engine forman parte
    # explícita del contrato de CT y deberán resolverse posteriormente
    # a callables reales:
    #
    #   ejecutar_total
    #   inspeccionar
    #   registrar_inventario
    #
    # Las metacapacidades describen el contrato de ejecución.
    # No ejecutan por sí mismas ninguna operación.
    # ============================================================

    "capacidades_meta": {

        # ========================================================
        # 7.1 — ALPHA
        # ========================================================

        "alpha": {
            "descripcion": (
                "Devuelve la constante fundacional ALPHA = 26/27."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "Fraction(26, 27)",
            "acceso_archivos": ["*"],
        },


        # ========================================================
        # 7.2 — BETA
        # ========================================================

        "beta": {
            "descripcion": (
                "Devuelve la constante fundacional BETA = 1/27."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "Fraction(1, 27)",
            "acceso_archivos": ["*"],
        },


        # ========================================================
        # 7.3 — DESCUBRIR CONSTANTES
        # ========================================================

        "descubrir_constantes": {
            "descripcion": (
                "Descubre todas las constantes oficiales declaradas "
                "dentro del modulo."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict nombre -> meta de constante + "
                "errores_carga + total"
            ),
            "acceso_archivos": ["*"],
        },


        # ========================================================
        # 7.4 — LISTAR CONSTANTES
        # ========================================================

        "listar_constantes": {
            "descripcion": (
                "Lista nombres de constantes fundacionales y auxiliares."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con fundacionales, auxiliares, total"
            ),
            "acceso_archivos": ["*"],
        },


        # ========================================================
        # 7.5 — BUSCAR CONSTANTE
        # ========================================================

        "buscar_constante": {
            "descripcion": (
                "Busca una constante oficial por nombre."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict de la constante o None",
            "acceso_archivos": ["*"],
        },


        # ========================================================
        # 7.6 — VERIFICAR CONSTANTES
        # ========================================================

        "verificar_constantes": {
            "descripcion": (
                "Audita el dominio de constantes: invariante fundacional, "
                "duplicados, tipos, campos obligatorios, conflictos y carga."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con coherente, problemas, advertencias, "
                "total_constantes"
            ),
            "acceso_archivos": ["*"],
        },


        # ========================================================
        # 7.7 — INVENTARIO
        # ========================================================

        "inventario": {
            "descripcion": (
                "Inventario completo de constantes del modulo."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con total, fundacionales, auxiliares, "
                "constantes descubiertas"
            ),
            "acceso_archivos": ["*"],
        },


        # ========================================================
        # 7.8 — REPORTE
        # ========================================================

        "reporte": {
            "descripcion": (
                "Reporte interno de estado del modulo CT."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con estado, ALPHA, BETA, "
                "total_constantes, capacidades"
            ),
            "acceso_archivos": ["*"],
        },


        # ========================================================
        # 7.9 — DIAGNOSTICO
        # ========================================================

        "diagnostico": {
            "descripcion": (
                "Diagnostico de coherencia del dominio de constantes."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con estado, problemas, advertencias, "
                "recomendaciones"
            ),
            "acceso_archivos": ["*"],
        },


        # ========================================================
        # 7.10 — VERIFICAR
        # ========================================================

        "verificar": {
            "descripcion": (
                "Verifica la invariante fundacional ALPHA + BETA == 1."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con coherente, ALPHA, BETA, suma"
            ),
            "acceso_archivos": ["*"],
        },


        # ========================================================
        # 7.11 — EJECUTAR TOTAL
        # ========================================================
        #
        # Capacidad arquitectónica de Engine.
        # Ejecuta el conjunto contractual de capacidades de CT
        # que hayan sido autorizadas y resueltas.
        #
        # No constituye autoridad para alterar el contrato.
        # La autoridad de dominio continúa perteneciendo a CT.
        #

        "ejecutar_total": {
            "descripcion": (
                "Ejecuta el conjunto completo de capacidades "
                "operativamente ejercibles por Engine sobre CT, "
                "respetando el contrato, las autorizaciones y las "
                "capacidades realmente declaradas."
            ),
            "entrada": "dict opcional de peticion",
            "validar_esquema": ["*"],
            "salida": (
                "dict con id, modulo, rol, version, operacion, estado, "
                "coherente, capacidades_ejecutadas, errores_ejecucion, "
                "resultados y capacidades_declaradas"
            ),
            "acceso_archivos": ["*"],
        },


        # ========================================================
        # 7.12 — INSPECCIONAR
        # ========================================================
        #
        # Capacidad arquitectónica de inspección contractual.
        # Expone estructura sin modificar el conocimiento declarado.
        #

        "inspeccionar": {
            "descripcion": (
                "Inspecciona estructuralmente CT y expone su contrato, "
                "capacidades, constantes, integridad, autorizaciones "
                "y estado sin modificar el conocimiento declarado."
            ),
            "entrada": "dict opcional de peticion",
            "validar_esquema": ["*"],
            "salida": (
                "dict con id, modulo, rol, version, operacion, "
                "constantes, capacidades_contractuales, "
                "capacidades_meta, integridad, esquema, "
                "autoriza_engine, reporting e invariantes"
            ),
            "acceso_archivos": ["*"],
        },


        # ========================================================
        # 7.13 — REGISTRAR INVENTARIO
        # ========================================================
        #
        # Capacidad arquitectónica de registro de inventario.
        # Produce una instantánea determinista del estado estructural.
        #

        "registrar_inventario": {
            "descripcion": (
                "Registra una instantánea determinista del inventario "
                "estructural y contractual de CT sin modificar las "
                "constantes declaradas ni el contrato del modulo."
            ),
            "entrada": "dict opcional de peticion",
            "validar_esquema": ["*"],
            "salida": (
                "dict con id, operacion, registrado, inventario y nota"
            ),
            "acceso_archivos": ["*"],
        },
    },


    # ============================================================
    # 8 — REPORTING (OBLIGATORIO EN EL ESQUEMA)
    # ============================================================
    #
    # Las banderas permiten a Engine determinar qué superficies
    # contractuales puede consultar, ejecutar o reportar.
    #
    # Las tres capacidades arquitectónicas se reflejan mediante
    # las banderas de capacidades, inventario, contrato, estado,
    # errores y diagnostico ya declaradas.
    #
    # Las banderas específicas de acceso a archivos y validación
    # de esquema son obligatorias para el acoplamiento Engine.
    # ============================================================

    "reporting": {

        # ========================================================
        # 8.1 — ESTADO Y SALUD
        # ========================================================

        "estado": True,
        "salud": True,


        # ========================================================
        # 2.2 — INVENTARIO Y CAPACIDADES
        # ========================================================

        "inventario": True,
        "capacidades": True,


        # ========================================================
        # 8.3 — ERRORES Y ADVERTENCIAS
        # ========================================================

        "errores": True,
        "advertencias": True,


        # ========================================================
        # 8.4 — DEPENDENCIAS Y VERSION
        # ========================================================

        "dependencias": True,
        "version": True,


        # ========================================================
        # 8.5 — CONTRATO Y CONOCIMIENTO
        # ========================================================

        "contrato": True,
        "conocimiento": True,


        # ========================================================
        # 8.6 — MÉTRICAS Y DIAGNÓSTICO
        # ========================================================

        "metricas": True,
        "diagnostico": True,


        # ========================================================
        # 8.7 — REPORTE
        # ========================================================

        "reporte": True,


        # ========================================================
        # 8.8 — ACCESO A ARCHIVOS
        # ========================================================

        "acceso_archivos": True,


        # ========================================================
        # 8.9 — VALIDACIÓN DE ESQUEMA
        # ========================================================

        "validar_esquema": True,


        # ========================================================
        # 8.10 — EJECUCIÓN TOTAL
        # ========================================================
        #
        # Declara que el módulo expone la superficie arquitectónica
        # de ejecución total para Engine.
        #

        "ejecutar_total": True,


        # ========================================================
        # 8.11 — INSPECCIÓN
        # ========================================================
        #
        # Declara que el módulo expone inspección estructural.
        #

        "inspeccionar": True,


        # ========================================================
        # 8.12 — REGISTRO DE INVENTARIO
        # ========================================================
        #
        # Declara que el módulo expone registro determinista de
        # inventario para Engine.
        #

        "registrar_inventario": True,
    },


    # ============================================================
    # 9 — CONSULTAS SOPORTADAS
    # ============================================================

    "consultas_soportadas": [
        "alpha",
        "beta",
        "descubrir_constantes",
        "listar_constantes",
        "buscar_constante",
        "verificar_constantes",
        "inventario",
        "reporte",
        "diagnostico",
        "verificar",

        # --------------------------------------------------------
        # Capacidades arquitectónicas de Engine
        # --------------------------------------------------------

        "ejecutar_total",
        "inspeccionar",
        "registrar_inventario",
    ],


    # ============================================================
    # 10 — CAPACIDADES
    # ============================================================
    #
    # Mapa contractual de nombre público -> callable o referencia
    # resoluble.
    #
    # Las tres capacidades arquitectónicas se declaran aquí para
    # que el resolvedor contractual pueda exigir posteriormente
    # sus callables reales.
    # ============================================================

    "capacidades": {

        # ========================================================
        # 10.1 — CAPACIDADES FUNDACIONALES
        # ========================================================

        "alpha": "get_alpha",
        "beta": "get_beta",


        # ========================================================
        # 10.2 — CAPACIDADES DE DESCUBRIMIENTO
        # ========================================================

        "descubrir_constantes": "descubrir_constantes",
        "listar_constantes": "listar_constantes",
        "buscar_constante": "buscar_constante",


        # ========================================================
        # 10.3 — CAPACIDADES DE VALIDACIÓN
        # ========================================================

        "verificar_constantes": "verificar_constantes",
        "verificar": "verificar",


        # ========================================================
        # 10.4 — CAPACIDADES DE ESTADO
        # ========================================================

        "inventario": "inventario",
        "reporte": "reporte",
        "diagnostico": "diagnostico",


        # ========================================================
        # 10.5 — CAPACIDADES ARQUITECTÓNICAS DE ENGINE
        # ========================================================

        "ejecutar_total": "ejecutar_total",
        "inspeccionar": "inspeccionar",
        "registrar_inventario": "registrar_inventario",
    },
    
    # ============================================================
    # 11 ESTADOS VÁLIDOS
    # ============================================================
    "estados_validos": list(ESTADOS_VALIDOS),

    # ============================================================
    # 12 INVARIANTES
    # ============================================================
    "invariantes": list(INVARIANTES),

}  # <--- CIERRE FINAL

# ===============================================================
# FIN CONTRATO
# ===============================================================

# ===============================================================
# VPSI-TRUTH — modules/constante/__init__.py
# SECCIÓN 5 — POLÍTICA ESTRICTA DE CONSTANTES
# ===============================================================


# ===============================================================
# 13 — ALCANCE CONTRACTUAL
# ===============================================================

TIPOS_CONSTANTE_VALIDOS = frozenset({
    "Fraction",
    "int",
    "str",
    "bool",
})

TIPOS_CONSTANTE_EXACTOS = {
    "Fraction": Fraction,
    "int": int,
    "str": str,
    "bool": bool,
}

POLITICA_CONSTANTES = {
    "aplica_a_todas_las_constantes_oficiales_del_modulo": True,
    "identidad_obligatoria": True,
    "nombre_no_vacio": True,
    "valor_obligatorio": True,
    "tipo_obligatorio": True,
    "origen_obligatorio": True,
    "descripcion_obligatoria": True,
    "tipo_declarado_debe_coincidir": True,
    "representacion_canonica_exacta": True,
    "float_como_representacion_canonica": False,
    "aritmetica_exacta": True,
    "fracciones_exactas": True,
    "representacion_float_operativa": True,
    "conversion_exacta_a_float_permitida": True,
    "float_como_constante_oficial": False,
    "conversion_implicita": False,
    "conversion_explicita_requerida": True,
    "conversion_float_a_fraction": False,
    "reconstruccion_desde_float": False,
    "calculo_aproximado_canonico": False,
    "representacion_aproximada_operativa": True,
    "redondeo_automatico": False,
    "tolerancia_numerica_canonica": Fraction(0),
    "rechazar_nan": True,
    "rechazar_inf": True,
    "formula_externa_obligatoria": False,
    "mutacion_despues_de_carga": False,
}


# ===============================================================
# 13.1 — REPRESENTACIÓN CANÓNICA
# ===============================================================

def _validar_especificacion_constante(item: Dict[str, Any]) -> None:
    if not isinstance(item, dict):
        raise ContratoInvalido("CONSTANTE debe ser dict")

    faltantes = [
        campo
        for campo in CAMPOS_OBLIGATORIOS_CONSTANTE
        if campo not in item
    ]

    if faltantes:
        raise ContratoInvalido(
            f"CONSTANTE incompleta. Faltan: {faltantes}"
        )

    nombre = item.get("nombre")
    if not isinstance(nombre, str) or not nombre.strip():
        raise ContratoInvalido(
            "CONSTANTE requiere 'nombre: str' no vacio"
        )

    nombre = nombre.strip()

    tipo = item.get("tipo")
    if not isinstance(tipo, str) or not tipo.strip():
        raise ContratoInvalido(
            f"CONSTANTE '{nombre}' requiere 'tipo: str'"
        )

    tipo = tipo.strip()

    if tipo not in TIPOS_CONSTANTE_VALIDOS:
        raise ContratoInvalido(
            f"CONSTANTE '{nombre}': tipo no autorizado: '{tipo}'. "
            f"Tipos validos: {sorted(TIPOS_CONSTANTE_VALIDOS)}"
        )

    valor = item.get("valor")

    if valor is None:
        raise ContratoInvalido(
            f"CONSTANTE '{nombre}': valor no puede ser None"
        )

    origen = item.get("origen")
    if not isinstance(origen, str) or not origen.strip():
        raise ContratoInvalido(
            f"CONSTANTE '{nombre}': origen debe ser str no vacio"
        )

    descripcion = item.get("descripcion")
    if not isinstance(descripcion, str) or not descripcion.strip():
        raise ContratoInvalido(
            f"CONSTANTE '{nombre}': descripcion debe ser str no vacio"
        )

    tipo_esperado = TIPOS_CONSTANTE_EXACTOS[tipo]

    if type(valor) is not tipo_esperado:
        raise ContratoInvalido(
            f"CONSTANTE '{nombre}': incompatibilidad exacta. "
            f"Tipo declarado='{tipo}', "
            f"tipo real='{type(valor).__name__}'."
        )

    if tipo == "Fraction":
        if type(valor) is not Fraction:
            raise ContratoInvalido(
                f"CONSTANTE '{nombre}': Fraction invalido."
            )

    if tipo in {"Fraction", "int"}:
        if POLITICA_CONSTANTES["calculo_aproximado_canonico"]:
            raise ContratoInvalido(
                f"CONSTANTE '{nombre}': "
                "calculo aproximado no permitido en canonico."
            )

        if POLITICA_CONSTANTES["redondeo_automatico"]:
            raise ContratoInvalido(
                f"CONSTANTE '{nombre}': "
                "redondeo automatico no permitido."
            )

        if POLITICA_CONSTANTES[
            "tolerancia_numerica_canonica"
        ] != Fraction(0):
            raise ContratoInvalido(
                f"CONSTANTE '{nombre}': "
                "tolerancia numerica canonica no permitida."
            )


# ===============================================================
# 13.2 — PROYECCIÓN OPERATIVA
# ===============================================================

def proyectar_float(valor: Any) -> float:
    if type(valor) is Fraction:
        return float(valor)

    if type(valor) is int:
        return float(valor)

    if type(valor) is float:
        raise ContratoInvalido(
            "Un float no puede utilizarse como fuente canonica."
        )

    raise ContratoInvalido(
        f"No existe proyeccion float contractual para "
        f"tipo '{type(valor).__name__}'."
    )


# ===============================================================
# 13.3 — PROHIBICIÓN DE RECONSTRUCCIÓN
# ===============================================================

def reconstruir_exactitud_desde_float(valor: float) -> Fraction:
    raise ContratoInvalido(
        "No se permite reconstruir una constante exacta desde float."
    )


# ===============================================================
# 13.4 — VALIDACIÓN DE REPRESENTACIÓN
# ===============================================================

def _validar_representacion_constante(
    nombre: str,
    valor: Any,
    tipo: str,
) -> None:
    if tipo not in TIPOS_CONSTANTE_VALIDOS:
        raise ContratoInvalido(
            f"Constante '{nombre}': tipo no autorizado: '{tipo}'."
        )

    esperado = TIPOS_CONSTANTE_EXACTOS[tipo]

    if type(valor) is not esperado:
        raise ContratoInvalido(
            f"Constante '{nombre}': "
            f"se esperaba '{tipo}' y se recibió "
            f"'{type(valor).__name__}'."
        )

    if type(valor) is float:
        raise ContratoInvalido(
            f"Constante '{nombre}': float prohibido como canonico."
        )


# ===============================================================
# SECCIÓN 14 — DESCUBRIMIENTO DETERMINISTA
# ===============================================================


# ===============================================================
# 14.1 — ARCHIVOS ELEGIBLES
# ===============================================================

def _archivos_constantes() -> List[Path]:
    archivos = []

    for archivo in sorted(_DIR.glob("*.py"), key=lambda p: p.name):
        if archivo.name == "__init__.py":
            continue

        if archivo.name.startswith("_"):
            continue

        archivos.append(archivo)

    return archivos


# ===============================================================
# 14.2 — INDICADOR DE DECLARACIÓN
# ===============================================================

def _archivo_declara_constante(archivo: Path) -> bool:
    try:
        texto = archivo.read_text(encoding="utf-8")
    except Exception:
        return False

    return "CONSTANTE" in texto


# ===============================================================
# 14.3 — CARGA AISLADA DE ARCHIVO
# ===============================================================

def _cargar_archivo_constante(
    archivo: Path,
) -> tuple[Optional[Any], Optional[Dict[str, str]]]:

    clave = f"_vpsi_ct_{archivo.stem}"

    spec = importlib.util.spec_from_file_location(
        clave,
        archivo,
    )

    if spec is None or spec.loader is None:
        return None, {
            "archivo": archivo.name,
            "error": "no se pudo crear spec de importacion",
        }

    mod = importlib.util.module_from_spec(spec)

    try:
        spec.loader.exec_module(mod)
    except Exception as exc:
        return None, {
            "archivo": archivo.name,
            "error": (
                f"archivo_corrupto: "
                f"{type(exc).__name__}: {exc}"
            ),
        }

    return getattr(mod, "CONSTANTE", None), None


# ===============================================================
# 14.4 — DESCUBRIMIENTO COMPLETO
# ===============================================================

def _descubrir_archivos() -> Dict[str, Any]:
    hallado: Dict[str, Any] = {}
    errores: List[Dict[str, str]] = []
    origen_por_nombre: Dict[str, List[str]] = {}

    for archivo in _archivos_constantes():

        if not _archivo_declara_constante(archivo):
            continue

        meta, error = _cargar_archivo_constante(archivo)

        if error is not None:
            errores.append(error)
            continue

        if meta is None:
            errores.append({
                "archivo": archivo.name,
                "error": "archivo marcado como CONSTANTE pero "
                         "no expone CONSTANTE",
            })
            continue

        items = meta if isinstance(meta, list) else [meta]

        if not items:
            errores.append({
                "archivo": archivo.name,
                "error": "CONSTANTE vacio",
            })
            continue

        for item in items:

            try:
                _validar_especificacion_constante(item)
            except ContratoInvalido as exc:
                errores.append({
                    "archivo": archivo.name,
                    "error": f"constante_rechazada: {exc}",
                })
                continue

            nombre = str(item["nombre"]).strip()

            if nombre in FUNDACIONALES:
                errores.append({
                    "archivo": archivo.name,
                    "error": (
                        f"constante_fundacional_redefinida: "
                        f"{nombre}"
                    ),
                })
                continue

            origen_por_nombre.setdefault(
                nombre,
                [],
            ).append(archivo.name)

            if nombre in hallado:
                errores.append({
                    "archivo": archivo.name,
                    "error": f"nombre_duplicado: {nombre}",
                })
                continue

            hallado[nombre] = {
                "nombre": nombre,
                "valor": item["valor"],
                "valor_str": str(item["valor"]),
                "tipo": item["tipo"],
                "origen": item["origen"].strip(),
                "descripcion": item["descripcion"].strip(),
                "archivo": archivo.name,
                "fundacional": False,
            }

    for nombre, archivos in sorted(
        origen_por_nombre.items(),
        key=lambda x: x[0],
    ):
        if len(archivos) > 1:
            errores.append({
                "archivo": ",".join(sorted(archivos)),
                "error": (
                    f"conflicto_entre_archivos: "
                    f"'{nombre}' en {sorted(archivos)}"
                ),
            })

    return {
        "constantes": dict(
            sorted(
                hallado.items(),
                key=lambda x: x[0],
            )
        ),
        "errores": sorted(
            errores,
            key=lambda x: (
                x.get("archivo", ""),
                x.get("error", ""),
            ),
        ),
    }


# ===============================================================
# SECCIÓN 15 — DOMINIO CANÓNICO
# ===============================================================


def _fundacionales() -> Dict[str, Any]:
    return {
        "ALPHA": {
            "nombre": "ALPHA",
            "valor": ALPHA,
            "valor_str": str(ALPHA),
            "tipo": "Fraction",
            "origen": "cubo 3x3x3 en R3",
            "descripcion": "Techo estructural",
            "archivo": "__init__.py",
            "fundacional": True,
        },
        "BETA": {
            "nombre": "BETA",
            "valor": BETA,
            "valor_str": str(BETA),
            "tipo": "Fraction",
            "origen": "cubo 3x3x3 en R3",
            "descripcion": "Piso estructural",
            "archivo": "__init__.py",
            "fundacional": True,
        },
    }


def _todas() -> Dict[str, Any]:
    base = _fundacionales()
    descubierto = _descubrir_archivos()

    base.update(descubierto["constantes"])

    return {
        "constantes": dict(
            sorted(
                base.items(),
                key=lambda x: x[0],
            )
        ),
        "errores_carga": descubierto["errores"],
        "archivos": sorted(
            {
                constante["archivo"]
                for constante in base.values()
            }
        ),
    }


# ===============================================================
# SECCIÓN 16 — VALIDACIÓN GLOBAL
# ===============================================================


def _validar_dominio_constantes(
    pack: Dict[str, Any],
) -> Dict[str, Any]:

    problemas: List[Dict[str, Any]] = []

    alpha = CONSTANTES_FUNDACIONALES["ALPHA"]
    beta = CONSTANTES_FUNDACIONALES["BETA"]

    if alpha + beta != Fraction(1):
        problemas.append({
            "tipo": "invariante_fundacional",
            "detalle": (
                f"ALPHA + BETA = {alpha + beta} != 1"
            ),
        })

    for error in pack["errores_carga"]:
        problemas.append({
            "tipo": "error_carga_o_conflicto",
            "detalle": error,
        })

    for nombre, meta in pack["constantes"].items():

        try:
            _validar_representacion_constante(
                nombre,
                meta["valor"],
                meta["tipo"],
            )
        except ContratoInvalido as exc:
            problemas.append({
                "tipo": "representacion_invalida",
                "detalle": str(exc),
            })

        if not meta.get("origen"):
            problemas.append({
                "tipo": "sin_origen",
                "detalle": nombre,
            })

        if not meta.get("descripcion"):
            problemas.append({
                "tipo": "sin_descripcion",
                "detalle": nombre,
            })

    return {
        "coherente": not problemas,
        "problemas": problemas,
    }


# ===============================================================
# SECCIÓN 17 — CAPACIDADES PÚBLICAS
# ===============================================================


def get_alpha(peticion=None) -> Fraction:
    return CONSTANTES_FUNDACIONALES["ALPHA"]


def get_beta(peticion=None) -> Fraction:
    return CONSTANTES_FUNDACIONALES["BETA"]


def descubrir_constantes(peticion=None) -> Dict[str, Any]:
    pack = _todas()

    return {
        "constantes": {
            nombre: {
                "nombre": meta["nombre"],
                "valor_str": meta["valor_str"],
                "tipo": meta["tipo"],
                "origen": meta["origen"],
                "descripcion": meta["descripcion"],
                "archivo": meta["archivo"],
                "fundacional": meta["fundacional"],
            }
            for nombre, meta in pack["constantes"].items()
        },
        "errores_carga": pack["errores_carga"],
        "archivos": pack["archivos"],
        "total": len(pack["constantes"]),
    }


def listar_constantes(peticion=None) -> Dict[str, Any]:
    pack = _todas()

    fundacionales = sorted(
        nombre
        for nombre, meta in pack["constantes"].items()
        if meta["fundacional"]
    )

    auxiliares = sorted(
        nombre
        for nombre, meta in pack["constantes"].items()
        if not meta["fundacional"]
    )

    return {
        "fundacionales": fundacionales,
        "auxiliares": auxiliares,
        "total": len(pack["constantes"]),
        "archivos": pack["archivos"],
    }


def buscar_constante(
    nombre: str,
    peticion=None,
) -> Optional[Dict[str, Any]]:

    if not isinstance(nombre, str):
        raise ContratoInvalido(
            "buscar_constante requiere nombre: str"
        )

    pack = _todas()

    meta = pack["constantes"].get(nombre.strip())

    if meta is None:
        return None

    return {
        "nombre": meta["nombre"],
        "valor_str": meta["valor_str"],
        "tipo": meta["tipo"],
        "origen": meta["origen"],
        "descripcion": meta["descripcion"],
        "archivo": meta["archivo"],
        "fundacional": meta["fundacional"],
    }


def verificar_constantes(peticion=None) -> Dict[str, Any]:
    pack = _todas()

    validacion = _validar_dominio_constantes(pack)

    alpha = CONSTANTES_FUNDACIONALES["ALPHA"]
    beta = CONSTANTES_FUNDACIONALES["BETA"]

    advertencias: List[str] = []

    if not pack["constantes"]:
        advertencias.append(
            "No hay constantes registradas"
        )

    return {
        "coherente": validacion["coherente"],
        "ALPHA": str(alpha),
        "BETA": str(beta),
        "suma": str(alpha + beta),
        "total_constantes": len(pack["constantes"]),
        "problemas": validacion["problemas"],
        "advertencias": advertencias,
    }


def verificar(peticion=None) -> Dict[str, Any]:
    alpha = CONSTANTES_FUNDACIONALES["ALPHA"]
    beta = CONSTANTES_FUNDACIONALES["BETA"]
    suma = alpha + beta

    return {
        "coherente": suma == Fraction(1),
        "ALPHA": str(alpha),
        "BETA": str(beta),
        "suma": str(suma),
        "invariante": "ALPHA + BETA == 1",
    }


# ===============================================================
# SECCIÓN 18 — INVENTARIO
# ===============================================================


def inventario(peticion=None) -> Dict[str, Any]:
    pack = _todas()

    fundacionales = {
        nombre: meta["valor_str"]
        for nombre, meta in pack["constantes"].items()
        if meta["fundacional"]
    }

    auxiliares = {
        nombre: {
            "valor_str": meta["valor_str"],
            "archivo": meta["archivo"],
            "tipo": meta["tipo"],
            "origen": meta["origen"],
        }
        for nombre, meta in pack["constantes"].items()
        if not meta["fundacional"]
    }

    return {
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "ALPHA": str(ALPHA),
        "BETA": str(BETA),
        "tipo_fundacionales": "Fraction",
        "origen_fundacionales": "cubo 3x3x3 en R3",
        "total_constantes": len(pack["constantes"]),
        "constantes_fundacionales": fundacionales,
        "constantes_auxiliares": auxiliares,
        "archivos": pack["archivos"],
        "errores_carga": pack["errores_carga"],
        "capacidades": sorted(
            CONTENEDOR["capacidades"].keys()
        ),
        "requiere": list(
            CONTENEDOR.get("requiere") or []
        ),
        "invariantes": list(
            CONTENEDOR.get("invariantes") or []
        ),
    }


# ===============================================================
# SECCIÓN 19 — REPORTING
# ===============================================================


def reporte(peticion=None) -> Dict[str, Any]:
    verificacion = verificar()
    constantes = verificar_constantes()
    pack = _todas()

    coherente = (
        verificacion["coherente"]
        and constantes["coherente"]
    )

    estado = (
        ESTADO_OPERATIVO
        if coherente
        else ESTADO_DEGRADADO
    )

    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "estado": estado,
        "coherente": coherente,
        "ALPHA": verificacion["ALPHA"],
        "BETA": verificacion["BETA"],
        "suma": verificacion["suma"],
        "total_constantes": len(pack["constantes"]),
        "archivos": pack["archivos"],
        "capacidades": sorted(
            CONTENEDOR["capacidades"].keys()
        ),
        "requiere": list(
            CONTENEDOR.get("requiere") or []
        ),
        "autoridad": list(
            CONTENEDOR.get("autoridad") or []
        ),
        "conocimiento_exportable": list(
            CONTENEDOR.get(
                "conocimiento_exportable"
            ) or []
        ),
        "consultas_soportadas": list(
            CONTENEDOR.get(
                "consultas_soportadas"
            ) or []
        ),
    }


def diagnostico(peticion=None) -> Dict[str, Any]:
    verificacion = verificar()
    constantes = verificar_constantes()

    problemas = list(
        constantes.get("problemas") or []
    )

    advertencias = list(
        constantes.get("advertencias") or []
    )

    recomendaciones: List[str] = []

    if not verificacion["coherente"]:
        recomendaciones.append(
            "Verificar ALPHA y BETA."
        )

    if problemas:
        recomendaciones.append(
            "Resolver los problemas del dominio de constantes."
        )

    if not problemas and not advertencias:
        recomendaciones.append(
            "Dominio de constantes coherente."
        )

    coherente = (
        verificacion["coherente"]
        and constantes["coherente"]
    )

    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "estado": (
            ESTADO_OPERATIVO
            if coherente
            else ESTADO_DEGRADADO
        ),
        "problemas": problemas,
        "advertencias": advertencias,
        "recomendaciones": recomendaciones,
        "coherente": coherente,
        "ALPHA": verificacion["ALPHA"],
        "BETA": verificacion["BETA"],
        "suma": verificacion["suma"],
        "total_constantes": constantes[
            "total_constantes"
        ],
    }


# ===============================================================
# SECCIÓN 20 — CAPACIDADES ARQUITECTÓNICAS DE ENGINE
# ===============================================================


def ejecutar_total(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Ejecuta todas las capacidades contractuales ordinarias de CT.

    Esta función NO ejecuta las capacidades arquitectónicas
    recursivamente. Las tres capacidades arquitectónicas de Engine
    quedan fuera del conjunto operativo para evitar recursión.
    """

    if peticion is None:
        peticion = {}

    if not isinstance(peticion, dict):
        raise ContratoInvalido(
            "ejecutar_total requiere peticion: dict o None"
        )

    capacidades_arquitectonicas = {
        "ejecutar_total",
        "inspeccionar",
        "registrar_inventario",
    }

    nombres = sorted(
        nombre
        for nombre in CONTENEDOR["capacidades"].keys()
        if nombre not in capacidades_arquitectonicas
    )

    resultados: Dict[str, Any] = {}
    errores: List[Dict[str, str]] = []
    ejecutadas: List[str] = []

    for nombre in nombres:
        fn = CONTENEDOR["capacidades"].get(nombre)

        if not callable(fn):
            errores.append({
                "capacidad": nombre,
                "error": "capacidad_no_callable",
            })
            continue

        try:
            resultados[nombre] = fn(peticion)
            ejecutadas.append(nombre)
        except TypeError:
            try:
                resultados[nombre] = fn()
                ejecutadas.append(nombre)
            except Exception as exc:
                errores.append({
                    "capacidad": nombre,
                    "error": (
                        f"{type(exc).__name__}: {exc}"
                    ),
                })
        except Exception as exc:
            errores.append({
                "capacidad": nombre,
                "error": (
                    f"{type(exc).__name__}: {exc}"
                ),
            })

    estado = (
        ESTADO_OPERATIVO
        if not errores
        else ESTADO_DEGRADADO
    )

    coherente = (
        verificar()["coherente"]
        and verificar_constantes()["coherente"]
        and not errores
    )

    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "operacion": "ejecutar_total",
        "estado": estado,
        "coherente": coherente,
        "capacidades_ejecutadas": ejecutadas,
        "errores_ejecucion": errores,
        "resultados": resultados,
        "capacidades_declaradas": sorted(
            CONTENEDOR["capacidades"].keys()
        ),
    }


def inspeccionar(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Expone la estructura contractual de CT sin modificarla.
    """

    if peticion is not None and not isinstance(
        peticion,
        dict,
    ):
        raise ContratoInvalido(
            "inspeccionar requiere peticion: dict o None"
        )

    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "operacion": "inspeccionar",
        "constantes": descubrir_constantes(),
        "capacidades_contractuales": sorted(
            CONTENEDOR["capacidades"].keys()
        ),
        "capacidades_meta": {
            nombre: dict(meta)
            for nombre, meta in sorted(
                CONTENEDOR[
                    "capacidades_meta"
                ].items()
            )
        },
        "integridad": verificar_constantes(),
        "esquema": ESQUEMA_CONTRATO,
        "autoriza_engine": dict(
            CONTENEDOR["autoriza_engine"]
        ),
        "reporting": dict(
            CONTENEDOR["reporting"]
        ),
        "invariantes": list(
            CONTENEDOR["invariantes"]
        ),
    }


def registrar_inventario(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Produce una instantánea determinista del inventario de CT.
    """

    if peticion is not None and not isinstance(
        peticion,
        dict,
    ):
        raise ContratoInvalido(
            "registrar_inventario requiere "
            "peticion: dict o None"
        )

    return {
        "id": ID_MODULO,
        "operacion": "registrar_inventario",
        "registrado": True,
        "inventario": inventario(peticion),
        "nota": (
            "Instantanea determinista del dominio "
            "de constantes de CT."
        ),
    }


# ===============================================================
# SECCIÓN 21 — MAPA CALLABLE
# ===============================================================


_CAP_MAP = {
    "get_alpha": get_alpha,
    "get_beta": get_beta,
    "descubrir_constantes": descubrir_constantes,
    "listar_constantes": listar_constantes,
    "buscar_constante": buscar_constante,
    "verificar_constantes": verificar_constantes,
    "inventario": inventario,
    "reporte": reporte,
    "diagnostico": diagnostico,
    "verificar": verificar,

    # -----------------------------------------------------------
    # Capacidades arquitectónicas de Engine
    # -----------------------------------------------------------

    "ejecutar_total": ejecutar_total,
    "inspeccionar": inspeccionar,
    "registrar_inventario": registrar_inventario,

    # -----------------------------------------------------------
    # Proyección operacional explícita
    # -----------------------------------------------------------

    "proyectar_float": proyectar_float,
}


# ===============================================================
# SECCIÓN 22 — RESOLUCIÓN ESTRICTA
# ===============================================================


def _resolver_capacidades(
    cont: Dict[str, Any],
) -> None:

    resueltas: Dict[str, Any] = {}

    for nombre in sorted(
        cont["capacidades"].keys()
    ):

        ref = cont["capacidades"][nombre]

        if callable(ref):
            resueltas[nombre] = ref
            continue

        if not isinstance(ref, str):
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: capacidad '{nombre}' "
                f"tiene tipo invalido: "
                f"{type(ref).__name__}"
            )

        if ref not in _CAP_MAP:
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: capacidad '{nombre}' "
                f"referencia inexistente: '{ref}'"
            )

        fn = _CAP_MAP[ref]

        if not callable(fn):
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: '{ref}' no es callable"
            )

        resueltas[nombre] = fn

    cont["capacidades"] = resueltas


# ===============================================================
# SECCIÓN 23 — VALIDACIÓN FINAL DEL CONTENEDOR
# ===============================================================


_validar_contrato(CONTENEDOR)
_resolver_capacidades(CONTENEDOR)


# ===============================================================
# SECCIÓN 24 — VALIDACIÓN DE SUPERFICIE CALLABLE
# ===============================================================


def _validar_superficie_callable(
    cont: Dict[str, Any],
) -> None:

    faltantes = []

    for nombre in sorted(
        cont["capacidades"].keys()
    ):
        if not callable(
            cont["capacidades"][nombre]
        ):
            faltantes.append(nombre)

    if faltantes:
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: capacidades no callables: "
            f"{faltantes}"
        )


_validar_superficie_callable(CONTENEDOR)


# ===============================================================
# SECCIÓN 25 — EXPORTACIONES
# ===============================================================


__all__ = [
    "CONTENEDOR",
    "ID_MODULO",
    "NOMBRE_MODULO",
    "ROL_MODULO",
    "VERSION_MODULO",
    "VERSION_CONTRATO",
    "ESQUEMA_CONTRATO",
    "ESTABILIDAD",
    "ALPHA",
    "BETA",
    "CONSTANTES_FUNDACIONALES",
    "TIPOS_CONSTANTE_VALIDOS",
    "TIPOS_CONSTANTE_EXACTOS",
    "POLITICA_CONSTANTES",
    "get_alpha",
    "get_beta",
    "descubrir_constantes",
    "listar_constantes",
    "buscar_constante",
    "verificar_constantes",
    "inventario",
    "verificar",
    "reporte",
    "diagnostico",
    "proyectar_float",
    "ejecutar_total",
    "inspeccionar",
    "registrar_inventario",
    "ContratoInvalido",
]


# ===============================================================
# FIN MÓDULO CT
# ===============================================================
