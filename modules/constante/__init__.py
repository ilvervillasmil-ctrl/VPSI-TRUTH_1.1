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
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List, Optional

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
    # 4.10 — AUTORIZACIÓN AL ENGINE
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
        # 4.10.1 — PERMISOS BASE
        # =======================================================

        "leer": True,
        "ejecutar": True,
        "consultar": True,
        "recombinar": True,
        "reportar": True,
        "auditar": True,
        "inventariar": True,


        # =======================================================
        # 4.10.2 — PERMISOS DE ESCRITURA
        # =======================================================

        "alterar": False,
        "crear": True,
        "actualizar": False,


        # =======================================================
        # 4.10.3 — PERMISOS DE PROCESAMIENTO
        # =======================================================

        "validar": True,
        "procesar": True,
        "analizar": True,
        "generar": True,


        # =======================================================
        # 4.10.4 — PERMISOS DE DATOS
        # =======================================================

        "exportar": True,
        "importar": True,
        "respaldar": True,
        "recuperar": True,
        "sincronizar": True,


        # =======================================================
        # 4.10.5 — PERMISOS DE MONITOREO
        # =======================================================

        "monitorear": True,
        "metricas": True,
        "diagnostico": True,


        # =======================================================
        # 4.10.6 — PERMISOS DE ESTADO
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
        # 4.10.7 — CAPACIDADES ARQUITECTÓNICAS AUTORIZADAS
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
        # 4.10.8 — PERMISOS OBLIGATORIOS DE ENGINE
        # =======================================================

        "validar_esquema": True,
        "acceso_archivos": True,
    },


    # ===========================================================
    # FIN SECCIÓN 4 — CONTINUACIÓN EN SIGUIENTES BLOQUES
    # ===========================================================

        # ============================================================
    # 1.15 — METADATOS DE CAPACIDADES (1:1 OBLIGATORIO)
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
        # 1.15.1 — ALPHA
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
        # 1.15.2 — BETA
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
        # 1.15.3 — DESCUBRIR CONSTANTES
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
        # 1.15.4 — LISTAR CONSTANTES
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
        # 1.15.5 — BUSCAR CONSTANTE
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
        # 1.15.6 — VERIFICAR CONSTANTES
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
        # 1.15.7 — INVENTARIO
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
        # 1.15.8 — REPORTE
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
        # 1.15.9 — DIAGNOSTICO
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
        # 1.15.10 — VERIFICAR
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
        # 1.15.11 — EJECUTAR TOTAL
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
        # 1.15.12 — INSPECCIONAR
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
        # 1.15.13 — REGISTRAR INVENTARIO
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
    # 1.16 — REPORTING (OBLIGATORIO EN EL ESQUEMA)
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
        # 1.16.1 — ESTADO Y SALUD
        # ========================================================

        "estado": True,
        "salud": True,


        # ========================================================
        # 1.16.2 — INVENTARIO Y CAPACIDADES
        # ========================================================

        "inventario": True,
        "capacidades": True,


        # ========================================================
        # 1.16.3 — ERRORES Y ADVERTENCIAS
        # ========================================================

        "errores": True,
        "advertencias": True,


        # ========================================================
        # 1.16.4 — DEPENDENCIAS Y VERSION
        # ========================================================

        "dependencias": True,
        "version": True,


        # ========================================================
        # 1.16.5 — CONTRATO Y CONOCIMIENTO
        # ========================================================

        "contrato": True,
        "conocimiento": True,


        # ========================================================
        # 1.16.6 — MÉTRICAS Y DIAGNÓSTICO
        # ========================================================

        "metricas": True,
        "diagnostico": True,


        # ========================================================
        # 1.16.7 — REPORTE
        # ========================================================

        "reporte": True,


        # ========================================================
        # 1.16.8 — ACCESO A ARCHIVOS
        # ========================================================

        "acceso_archivos": True,


        # ========================================================
        # 1.16.9 — VALIDACIÓN DE ESQUEMA
        # ========================================================

        "validar_esquema": True,


        # ========================================================
        # 1.16.10 — EJECUCIÓN TOTAL
        # ========================================================
        #
        # Declara que el módulo expone la superficie arquitectónica
        # de ejecución total para Engine.
        #

        "ejecutar_total": True,


        # ========================================================
        # 1.16.11 — INSPECCIÓN
        # ========================================================
        #
        # Declara que el módulo expone inspección estructural.
        #

        "inspeccionar": True,


        # ========================================================
        # 1.16.12 — REGISTRO DE INVENTARIO
        # ========================================================
        #
        # Declara que el módulo expone registro determinista de
        # inventario para Engine.
        #

        "registrar_inventario": True,
    },


    # ============================================================
    # 1.17 — CONSULTAS SOPORTADAS
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
    # 1.18 — CAPACIDADES
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
        # 1.18.1 — CAPACIDADES FUNDACIONALES
        # ========================================================

        "alpha": "get_alpha",
        "beta": "get_beta",


        # ========================================================
        # 1.18.2 — CAPACIDADES DE DESCUBRIMIENTO
        # ========================================================

        "descubrir_constantes": "descubrir_constantes",
        "listar_constantes": "listar_constantes",
        "buscar_constante": "buscar_constante",


        # ========================================================
        # 1.18.3 — CAPACIDADES DE VALIDACIÓN
        # ========================================================

        "verificar_constantes": "verificar_constantes",
        "verificar": "verificar",


        # ========================================================
        # 1.18.4 — CAPACIDADES DE ESTADO
        # ========================================================

        "inventario": "inventario",
        "reporte": "reporte",
        "diagnostico": "diagnostico",


        # ========================================================
        # 1.18.5 — CAPACIDADES ARQUITECTÓNICAS DE ENGINE
        # ========================================================

        "ejecutar_total": "ejecutar_total",
        "inspeccionar": "inspeccionar",
        "registrar_inventario": "registrar_inventario",
    },
    
    # ============================================================
    # ESTADOS VÁLIDOS
    # ============================================================
    "estados_validos": list(ESTADOS_VALIDOS),

    # ============================================================
    # INVARIANTES
    # ============================================================
    "invariantes": list(INVARIANTES),

}  # <--- CIERRE FINAL

# ===============================================================
# FIN CONTRATO
# ===============================================================



# ===============================================================
# POLÍTICA ESTRICTA DE CONSTANTES
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
    "identidad_obligatoria": True,
    "nombre_no_vacio": True,
    "valor_obligatorio": True,
    "tipo_obligatorio": True,
    "origen_obligatorio": True,
    "descripcion_obligatoria": True,
    "tipo_declarado_debe_coincidir": True,
    "rechazar_float": True,
    "rechazar_nan": True,
    "rechazar_inf": True,
    "conversion_implicita": False,
    "conversion_float_a_fraction": False,
    "redondeo_automatico": False,
    "tolerancia_numerica": Fraction(0),
    "calculo_aproximado": False,
    "aritmetica_exacta": True,
    "fracciones_exactas": True,
    "formula_externa_obligatoria": False,
    "mutacion_despues_de_carga": False,
}


def _validar_especificacion_constante(item: Dict[str, Any]) -> None:
    """
    Valida estrictamente una declaracion CONSTANTE contra la politica
    oficial del modulo CT.

    Ninguna constante puede entrar al registro de CT si no cumple
    exactamente las especificaciones de identidad, tipo, valor,
    origen y descripcion.

    Reglas fundamentales:
    - CONSTANTE debe ser dict.
    - Todos los campos obligatorios deben existir.
    - nombre debe ser str no vacio.
    - valor debe existir y no puede ser None.
    - tipo debe ser uno de los tipos oficialmente autorizados.
    - origen debe ser str no vacio.
    - descripcion debe ser str no vacio.
    - el tipo declarado debe coincidir exactamente con el tipo real.
    - float queda prohibido.
    - no existen conversiones implicitas.
    - no existe conversion de float a Fraction.
    - no existe redondeo automatico.
    - no existe tolerancia numerica.
    - las constantes numericas utilizan representacion exacta.
    """

    if not isinstance(item, dict):
        raise ContratoInvalido(
            "CONSTANTE debe ser dict"
        )

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

    if POLITICA_CONSTANTES["nombre_no_vacio"]:
        if not isinstance(nombre, str) or not nombre.strip():
            raise ContratoInvalido(
                "CONSTANTE requiere 'nombre: str' no vacio"
            )

    nombre = nombre.strip()

    tipo = item.get("tipo")

    if POLITICA_CONSTANTES["tipo_obligatorio"]:
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

    if POLITICA_CONSTANTES["valor_obligatorio"]:
        if valor is None:
            raise ContratoInvalido(
                f"CONSTANTE '{nombre}': valor no puede ser None"
            )

    origen = item.get("origen")

    if POLITICA_CONSTANTES["origen_obligatorio"]:
        if not isinstance(origen, str) or not origen.strip():
            raise ContratoInvalido(
                f"CONSTANTE '{nombre}': 'origen' debe ser str no vacio"
            )

    descripcion = item.get("descripcion")

    if POLITICA_CONSTANTES["descripcion_obligatoria"]:
        if not isinstance(descripcion, str) or not descripcion.strip():
            raise ContratoInvalido(
                f"CONSTANTE '{nombre}': 'descripcion' debe ser str no vacio"
            )

    # -----------------------------------------------------------
    # RECHAZO ABSOLUTO DE FLOAT
    # -----------------------------------------------------------

    if POLITICA_CONSTANTES["rechazar_float"]:
        if isinstance(valor, float):
            raise ContratoInvalido(
                f"CONSTANTE '{nombre}': float no permitido. "
                "Las constantes numericas deben utilizar "
                "representacion exacta."
            )

    # -----------------------------------------------------------
    # VALIDACION EXACTA DEL TIPO REAL
    # -----------------------------------------------------------

    if POLITICA_CONSTANTES["tipo_declarado_debe_coincidir"]:
        tipo_esperado = TIPOS_CONSTANTE_EXACTOS[tipo]

        if type(valor) is not tipo_esperado:
            raise ContratoInvalido(
                f"CONSTANTE '{nombre}': incompatibilidad exacta. "
                f"Tipo declarado='{tipo}', "
                f"tipo real='{type(valor).__name__}'."
            )

    # -----------------------------------------------------------
    # PROHIBICION DE CONVERSIONES IMPLICITAS
    # -----------------------------------------------------------

    if not POLITICA_CONSTANTES["conversion_implicita"]:
        tipo_real = type(valor).__name__
        tipo_esperado = TIPOS_CONSTANTE_EXACTOS[tipo].__name__

        if tipo_real != tipo_esperado:
            raise ContratoInvalido(
                f"CONSTANTE '{nombre}': conversion implicita "
                f"no permitida. Esperado='{tipo_esperado}', "
                f"recibido='{tipo_real}'."
            )

    # -----------------------------------------------------------
    # PROHIBICION EXPLICITA DE FLOAT -> FRACTION
    # -----------------------------------------------------------

    if tipo == "Fraction" and isinstance(valor, float):
        if not POLITICA_CONSTANTES["conversion_float_a_fraction"]:
            raise ContratoInvalido(
                f"CONSTANTE '{nombre}': conversion float -> Fraction "
                "no permitida."
            )

    # -----------------------------------------------------------
    # VALIDACION DE FRACCIONES EXACTAS
    # -----------------------------------------------------------

    if tipo == "Fraction":
        if type(valor) is not Fraction:
            raise ContratoInvalido(
                f"CONSTANTE '{nombre}': Fraction invalido. "
                f"Tipo recibido='{type(valor).__name__}'."
            )

        if POLITICA_CONSTANTES["fracciones_exactas"] is not True:
            raise ContratoInvalido(
                f"CONSTANTE '{nombre}': las fracciones exactas "
                "son obligatorias."
            )

        if POLITICA_CONSTANTES["aritmetica_exacta"] is not True:
            raise ContratoInvalido(
                f"CONSTANTE '{nombre}': la aritmetica exacta "
                "es obligatoria."
            )

    # -----------------------------------------------------------
    # VALIDACION NUMERICA
    # -----------------------------------------------------------

    if tipo in {"Fraction", "int"}:

        if POLITICA_CONSTANTES["calculo_aproximado"]:
            raise ContratoInvalido(
                f"CONSTANTE '{nombre}': calculo aproximado "
                "no permitido."
            )

        if POLITICA_CONSTANTES["redondeo_automatico"]:
            raise ContratoInvalido(
                f"CONSTANTE '{nombre}': redondeo automatico "
                "no permitido."
            )

        if POLITICA_CONSTANTES["tolerancia_numerica"] != Fraction(0):
            raise ContratoInvalido(
                f"CONSTANTE '{nombre}': tolerancia numerica "
                "no permitida."
            )

    # -----------------------------------------------------------
    # RECHAZO EXPLICITO DE NaN E INFINITO
    # -----------------------------------------------------------
    # Esta comprobacion queda definida explicitamente aunque float
    # ya haya sido rechazado. Protege la politica si posteriormente
    # se amplia el dominio de tipos numericos.

    if POLITICA_CONSTANTES["rechazar_nan"]:
        if isinstance(valor, float):
            if valor != valor:
                raise ContratoInvalido(
                    f"CONSTANTE '{nombre}': NaN no permitido."
                )

    if POLITICA_CONSTANTES["rechazar_inf"]:
        if isinstance(valor, float):
            if valor in (float("inf"), float("-inf")):
                raise ContratoInvalido(
                    f"CONSTANTE '{nombre}': infinito no permitido."
                )


# ===============================================================
# FIN POLÍTICA ESTRICTA DE CONSTANTES
# ===============================================================

# ===============================================================
# FUNCIONES PRIVADAS
# ===============================================================

def _archivo_declara_constante(archivo: Path) -> bool:
    try:
        texto = archivo.read_text(encoding="utf-8")
    except Exception:  # noqa: BLE001
        return False
    return "CONSTANTE" in texto


def _descubrir_archivos() -> Dict[str, Any]:
    hallado: Dict[str, Any] = {}
    errores: List[Dict[str, str]] = []
    origen_por_nombre: Dict[str, List[str]] = {}

    for archivo in sorted(_DIR.glob("*.py")):
        if archivo.name.startswith("_") or archivo.name == "__init__.py":
            continue
        if not _archivo_declara_constante(archivo):
            continue

        clave = f"constante_{archivo.stem}"
        spec = importlib.util.spec_from_file_location(clave, archivo)
        if spec is None or spec.loader is None:
            errores.append({
                "archivo": archivo.name,
                "error": "no se pudo crear spec de importacion",
            })
            continue

        mod = importlib.util.module_from_spec(spec)
        sys.modules[clave] = mod
        try:
            spec.loader.exec_module(mod)
        except Exception as e:  # noqa: BLE001
            errores.append({
                "archivo": archivo.name,
                "error": f"archivo_corrupto: {type(e).__name__}: {e}",
            })
            continue

        meta = getattr(mod, "CONSTANTE", None)
        if meta is None:
            continue

        items = meta if isinstance(meta, list) else [meta]
        for item in items:
            if not isinstance(item, dict):
                errores.append({
                    "archivo": archivo.name,
                    "error": "CONSTANTE no es dict ni list[dict]",
                })
                continue

            try:
                _validar_especificacion_constante(item)
            except ContratoInvalido as e:
                errores.append({
                    "archivo": archivo.name,
                    "error": f"constante_rechazada: {e}",
                })
                continue

            nombre = str(item.get("nombre", "")).strip()
            if not nombre:
                errores.append({
                    "archivo": archivo.name,
                    "error": "CONSTANTE sin 'nombre'",
                })
                continue

            if nombre in FUNDACIONALES:
                errores.append({
                    "archivo": archivo.name,
                    "error": f"constante_fundacional_redefinida: {nombre}",
                })
                continue

            faltan = [
                c for c in CAMPOS_OBLIGATORIOS_CONSTANTE
                if c not in item or item.get(c) in (None, "")
            ]
            if faltan:
                errores.append({
                    "archivo": archivo.name,
                    "error": f"campos_faltantes en '{nombre}': {faltan}",
                })

            origen_por_nombre.setdefault(nombre, []).append(archivo.name)

            if nombre in hallado:
                errores.append({
                    "archivo": archivo.name,
                    "error": f"nombre_duplicado: {nombre}",
                })
                continue

            hallado[nombre] = {
                "nombre": nombre,
                "valor": item.get("valor"),
                "valor_str": str(item.get("valor")),
                "tipo": str(item.get("tipo", "")),
                "origen": str(item.get("origen", "")),
                "descripcion": str(item.get("descripcion", "")),
                "archivo": archivo.name,
                "fundacional": False,
            }

    for nombre, archivos in origen_por_nombre.items():
        if len(archivos) > 1:
            errores.append({
                "archivo": ",".join(archivos),
                "error": f"conflicto_entre_archivos: '{nombre}' en {archivos}",
            })

    return {"constantes": hallado, "errores": errores}


def _fundacionales() -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for nombre, valor in CONSTANTES_FUNDACIONALES.items():
        out[nombre] = {
            "nombre": nombre,
            "valor": valor,
            "valor_str": str(valor),
            "tipo": type(valor).__name__,
            "origen": "cubo 3x3x3 en R3",
            "descripcion": (
                "Techo estructural" if nombre == "ALPHA" else "Piso estructural"
            ),
            "archivo": "__init__.py",
            "fundacional": True,
        }
    return out


def _todas() -> Dict[str, Any]:
    base = _fundacionales()
    desc = _descubrir_archivos()
    base.update(desc["constantes"])
    return {
        "constantes": base,
        "errores_carga": desc["errores"],
        "archivos": sorted({c["archivo"] for c in base.values()}),
    }


def _validar_contrato(cont: Dict[str, Any]) -> None:
    obligatorias = (
        "esquema", "version_contrato", "version_modulo",
        "id", "nombre", "rol", "descripcion",
        "funcion", "no_hace", "autoridad",
        "conocimiento_exportable", "requiere",
        "autoriza_engine", "consultas_soportadas",
        "capacidades", "capacidades_meta",
        "reporting", "estados_validos", "invariantes",
        "estabilidad", "compatible_desde", "api_engine",
    )
    faltantes = [k for k in obligatorias if k not in cont]
    if faltantes:
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: CONTENEDOR incompleto. Faltan: {faltantes}"
        )
    if cont.get("esquema") != ESQUEMA_CONTRATO:
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: esquema incompatible: {cont.get('esquema')}"
        )
    if str(cont.get("version_contrato")) != VERSION_CONTRATO:
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: version_contrato invalida: {cont.get('version_contrato')}"
        )
    meta_caps = cont.get("capacidades_meta") or {}
    for nombre_cap in cont.get("capacidades") or {}:
        if nombre_cap not in meta_caps:
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: capacidad '{nombre_cap}' sin capacidades_meta"
            )
        entrada = meta_caps[nombre_cap]
        if not isinstance(entrada, dict):
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: capacidades_meta['{nombre_cap}'] debe ser dict"
            )
        for campo in ("descripcion", "entrada", "salida"):
            if campo not in entrada or not isinstance(entrada[campo], str):
                raise ContratoInvalido(
                    f"{NOMBRE_MODULO}: capacidades_meta['{nombre_cap}'] "
                    f"requiere '{campo}: str'"
                )

# ===============================================================
# FIN FUNCIONES PRIVADAS
# ===============================================================


# ===============================================================
# CAPACIDADES PÚBLICAS
# ===============================================================

def get_alpha(peticion=None) -> Fraction:
    return CONSTANTES_FUNDACIONALES["ALPHA"]


def get_beta(peticion=None) -> Fraction:
    return CONSTANTES_FUNDACIONALES["BETA"]


def descubrir_constantes() -> Dict[str, Any]:
    pack = _todas()
    return {
        "constantes": {
            k: {
                "nombre": v["nombre"],
                "valor_str": v["valor_str"],
                "tipo": v["tipo"],
                "origen": v["origen"],
                "descripcion": v["descripcion"],
                "archivo": v["archivo"],
                "fundacional": v["fundacional"],
            }
            for k, v in pack["constantes"].items()
        },
        "errores_carga": pack["errores_carga"],
        "archivos": pack["archivos"],
        "total": len(pack["constantes"]),
    }


def listar_constantes() -> Dict[str, Any]:
    pack = _todas()
    fund = sorted(k for k, v in pack["constantes"].items() if v["fundacional"])
    aux = sorted(k for k, v in pack["constantes"].items() if not v["fundacional"])
    return {
        "fundacionales": fund,
        "auxiliares": aux,
        "total": len(pack["constantes"]),
        "archivos": pack["archivos"],
    }


def buscar_constante(nombre: str) -> Optional[Dict[str, Any]]:
    pack = _todas()
    c = pack["constantes"].get(str(nombre).strip())
    if c is None:
        return None
    return {
        "nombre": c["nombre"],
        "valor_str": c["valor_str"],
        "tipo": c["tipo"],
        "origen": c["origen"],
        "descripcion": c["descripcion"],
        "archivo": c["archivo"],
        "fundacional": c["fundacional"],
    }


def verificar_constantes() -> Dict[str, Any]:
    problemas: List[Dict[str, Any]] = []
    advertencias: List[str] = []

    alpha = CONSTANTES_FUNDACIONALES["ALPHA"]
    beta = CONSTANTES_FUNDACIONALES["BETA"]
    suma = alpha + beta
    if suma != Fraction(1):
        problemas.append({
            "tipo": "invariante_fundacional",
            "detalle": f"ALPHA + BETA = {suma} != 1",
        })

    pack = _todas()
    for err in pack["errores_carga"]:
        problemas.append({
            "tipo": "error_carga_o_conflicto",
            "detalle": err,
        })

    for nombre, meta in pack["constantes"].items():
        if meta["fundacional"]:
            continue
        if not meta.get("tipo"):
            problemas.append({"tipo": "tipo_invalido_o_vacio", "detalle": nombre})
        if not meta.get("origen"):
            problemas.append({"tipo": "sin_origen", "detalle": nombre})
        if not meta.get("descripcion"):
            problemas.append({"tipo": "sin_descripcion", "detalle": nombre})
        if meta.get("valor") is None and meta.get("valor_str") in ("None", ""):
            problemas.append({"tipo": "constante_sin_valor", "detalle": nombre})

    if not pack["constantes"]:
        advertencias.append("No hay constantes registradas")

    return {
        "coherente": not problemas,
        "ALPHA": str(alpha),
        "BETA": str(beta),
        "suma": str(suma),
        "total_constantes": len(pack["constantes"]),
        "problemas": problemas,
        "advertencias": advertencias,
    }


def verificar() -> Dict[str, Any]:
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


def inventario(peticion=None) -> Dict[str, Any]:
    pack = _todas()
    fund = {
        k: v["valor_str"]
        for k, v in pack["constantes"].items()
        if v["fundacional"]
    }
    aux = {
        k: {
            "valor_str": v["valor_str"],
            "archivo": v["archivo"],
            "tipo": v["tipo"],
            "origen": v["origen"],
        }
        for k, v in pack["constantes"].items()
        if not v["fundacional"]
    }
    return {
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "ALPHA": str(CONSTANTES_FUNDACIONALES["ALPHA"]),
        "BETA": str(CONSTANTES_FUNDACIONALES["BETA"]),
        "tipo_fundacionales": "Fraction",
        "origen_fundacionales": "cubo 3x3x3 en R3",
        "total_constantes": len(pack["constantes"]),
        "constantes_fundacionales": fund,
        "constantes_auxiliares": aux,
        "archivos": pack["archivos"],
        "errores_carga": pack["errores_carga"],
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "invariantes": CONTENEDOR.get("invariantes"),
    }

# ===============================================================
# FIN CAPACIDADES PÚBLICAS
# ===============================================================


# ===============================================================
# REPORTING INTERNO
# ===============================================================

def reporte() -> Dict[str, Any]:
    v = verificar()
    vc = verificar_constantes()
    pack = _todas()
    estado = ESTADO_OPERATIVO if (v["coherente"] and vc["coherente"]) else ESTADO_DEGRADADO
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "estado": estado,
        "coherente": v["coherente"] and vc["coherente"],
        "ALPHA": v["ALPHA"],
        "BETA": v["BETA"],
        "suma": v["suma"],
        "total_constantes": len(pack["constantes"]),
        "archivos": pack["archivos"],
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "autoridad": CONTENEDOR.get("autoridad"),
        "conocimiento_exportable": CONTENEDOR.get("conocimiento_exportable"),
        "consultas_soportadas": CONTENEDOR.get("consultas_soportadas"),
    }


def diagnostico() -> Dict[str, Any]:
    v = verificar()
    vc = verificar_constantes()
    problemas = list(vc.get("problemas") or [])
    advertencias = list(vc.get("advertencias") or [])
    recomendaciones: List[str] = []

    if not v["coherente"]:
        recomendaciones.append(
            "Verificar definicion de ALPHA y BETA en CONSTANTES_FUNDACIONALES"
        )
    if vc.get("problemas"):
        recomendaciones.append("Resolver problemas del dominio de constantes")
    if not _descubrir_archivos()["constantes"] and not problemas:
        advertencias.append(
            "Solo hay constantes fundacionales; no hay auxiliares declaradas"
        )

    estado = ESTADO_OPERATIVO if (v["coherente"] and vc["coherente"]) else ESTADO_DEGRADADO
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "estado": estado,
        "problemas": problemas,
        "advertencias": advertencias,
        "recomendaciones": recomendaciones,
        "coherente": v["coherente"] and vc["coherente"],
        "ALPHA": v["ALPHA"],
        "BETA": v["BETA"],
        "suma": v["suma"],
        "total_constantes": vc.get("total_constantes"),
    }

# ===============================================================
# FIN REPORTING
# ===============================================================


# ===============================================================
# EXPORTACIONES + RESOLUCIÓN ESTRICTA
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
}


def _resolver_capacidades(cont: Dict[str, Any]) -> None:
    resueltas: Dict[str, Any] = {}
    for nombre, ref in cont["capacidades"].items():
        if callable(ref):
            resueltas[nombre] = ref
            continue
        if isinstance(ref, str):
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
            continue
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: capacidad '{nombre}' "
            f"tiene tipo invalido: {type(ref).__name__}"
        )
    cont["capacidades"] = resueltas


_validar_contrato(CONTENEDOR)
_resolver_capacidades(CONTENEDOR)

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
    "ContratoInvalido",
]

# ===============================================================
# FIN EXPORTACIONES
# ===============================================================


# ===============================================================
# FIN DEL MÓDULO
# ===============================================================
