# ===============================================================
# VPSI-TRUTH — modules/citacion/__init__.py
# ===============================================================
#
# MÓDULO:              citacion
# ID:                  CIT
# Rol:                 CIT
# Versión módulo:      2.0
# Versión contrato:    1.0
# Esquema contrato:    VPSI-CONTRACT-1.0
# Estabilidad:         ESTABLE
# Compatible desde:    1.0
# API Engine:          >=1.0
#
# ---------------------------------------------------------------
# PRINCIPIO FUNDAMENTAL
# ---------------------------------------------------------------
#
# CIT no calcula.
# CIT no decide.
# CIT no interpreta.
# CIT no modifica.
# CIT no crea conocimiento.
#
# CIT conoce, resuelve, relaciona y cita.
#
# Toda declaración formal del VPSI debe poder ser resuelta por CIT.
#
# ---------------------------------------------------------------
# DEFINICIÓN
# ---------------------------------------------------------------
#
# CIT es la autoridad universal de fundamentación del VPSI.
#
# Conserva conocimiento resoluble de todas las declaraciones
# públicas existentes dentro del sistema.
#
# Puede resolver, relacionar y citar cualquier axioma, teorema,
# definición, corolario, fórmula, contexto, regla, correlación
# o declaración formal proveniente de cualquier módulo presente
# o futuro.
#
# Su autoridad es absoluta sobre la fundamentación.
# No posee autoridad para alterar el conocimiento.
#
# ---------------------------------------------------------------
# MODELO CONCEPTUAL
# ---------------------------------------------------------------
#
#   Declaración
#        ↓
#   Resolución
#        ↓
#   Relación
#        ↓
#   Cadena normativa
#        ↓
#   Citación
#        ↓
#   Explicación
#
# Internamente CIT administra declaraciones.
# Las citas son únicamente una representación de esas declaraciones.
#
# ---------------------------------------------------------------
# OFICIO ÚNICO
# ---------------------------------------------------------------
#
# Resolver, organizar, relacionar y citar cualquier declaración
# pública perteneciente al VPSI.
#
# ---------------------------------------------------------------
# RESTRICCIÓN ÚNICA
# ---------------------------------------------------------------
#
# Ninguna capacidad de CIT puede modificar el conocimiento declarado.
#
# ---------------------------------------------------------------
# DOS MODOS
# ---------------------------------------------------------------
#
# Modo Engine
#   Engine solicita fundamentación del ciclo.
#   CIT devuelve la cadena documental utilizada.
#
# Modo Consulta
#   Se solicita conocimiento ("Cítame TA-7", "¿Qué dice Def-5.3.1?").
#   El mismo motor responde.
#
# ---------------------------------------------------------------
# ESCALABILIDAD
# ---------------------------------------------------------------
#
# CIT nunca crece en lógica.
# Crece únicamente en conocimiento declarado.
# Todo módulo presente o futuro puede registrar declaraciones
# públicas; CIT las incorpora sin modificar este INIT.
#
# ===============================================================

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

# ===============================================================
# VPSI-TRUTH — modules/citacion/__init__.py
# ===============================================================
#
# MÓDULO:              citacion
# ID:                  CIT
# Rol:                 CIT
# Versión módulo:      2.0
# Versión contrato:    1.0
# Esquema contrato:    VPSI-CONTRACT-1.0
# Estabilidad:         ESTABLE
# Compatible desde:   1.0
# API Engine:          >=1.0
#
# ===============================================================


# ===============================================================
# SECCIÓN 1 — IDENTIDAD
# ===============================================================

_ID = "CIT"
_NOMBRE = "citacion"
_ROL = "CIT"
_VERSION = "2.0"
_VERSION_CONTRATO = "1.0"
_ESQUEMA = "VPSI-CONTRACT-1.0"
_ESTABILIDAD = "ESTABLE"
_COMPATIBLE_DESDE = "1.0"
_API_ENGINE = ">=1.0"


# ===============================================================
# FIN SECCIÓN 1
# ===============================================================


# ===============================================================
# SECCIÓN 2 — UNIVERSO DECLARATIVO
# ===============================================================

# ===============================================================
# 2.1 — TIPOS DE DECLARACIÓN
# ===============================================================
#
# Tipos abiertos: no lista cerrada de módulos.
# Cualquier fuente presente o futura puede aportar declaraciones.
#

TIPOS_DECLARACION = (
    "axioma",
    "teorema",
    "definicion",
    "corolario",
    "lema",
    "regla",
    "principio",
    "formula",
    "correlacion",
    "contexto",
    "limite",
    "factor",
    "procedimiento",
    "contrato",
    "invariante",
    "capacidad",
    "evidencia",
    "citacion",

    # Compatibilidad con tipos legados de ciclo.
    "ax",
    "mc",
    "cx",
    "tx",
    "ca",
    "fo",
    "re",
    "ct",
    "ch",
    "sf",
)


# ===============================================================
# FIN 2.1
# ===============================================================


# ===============================================================
# 2.2 — RELACIONES DECLARATIVAS
# ===============================================================

RELACIONES = (
    "depende_de",
    "fundamenta",
    "contradice",
    "extiende",
    "deriva_de",
    "correlaciona_con",
    "limita",
    "activa",
    "desactiva",
    "requiere",
    "gobierna",
)


# ===============================================================
# FIN 2.2
# ===============================================================


# ===============================================================
# 2.3 — CAMPOS OBLIGATORIOS
# ===============================================================

CAMPOS_OBLIGATORIOS = (
    "id",
    "tipo",
    "fuente",
    "enunciado",
)


# ===============================================================
# FIN 2.3
# ===============================================================


# ===============================================================
# 2.4 — CAMPOS OPCIONALES
# ===============================================================

CAMPOS_OPCIONALES = (
    "descripcion",
    "evidencia_ref",
    "o_ref",
    "contexto_ciclo",
    "meta",
    "relaciones",
    "fuente_modulo",  # legado
)


# ===============================================================
# FIN 2.4
# ===============================================================


# ===============================================================
# FIN SECCIÓN 2
# ===============================================================

# ===============================================================
# SECCIÓN 3 — CONTENEDOR CONTRACTUAL
# VPSI-CONTRACT-1.0
# ===============================================================

CONTENEDOR: Dict[str, Any] = {

    # ===========================================================
    # 3.1 — IDENTIDAD CONTRACTUAL
    # ===========================================================

    "esquema": _ESQUEMA,
    "version_contrato": _VERSION_CONTRATO,
    "version_modulo": _VERSION,
    "id": _ID,
    "nombre": _NOMBRE,
    "rol": _ROL,
    "estabilidad": _ESTABILIDAD,
    "compatible_desde": _COMPATIBLE_DESDE,
    "api_engine": _API_ENGINE,


    # ===========================================================
    # 3.2 — DESCRIPCIÓN
    # ===========================================================

    "descripcion": (
        "Autoridad universal de fundamentación del VPSI. "
        "Conserva conocimiento resoluble de todas las declaraciones "
        "públicas del sistema. Puede resolver, relacionar y citar "
        "cualquier declaración formal proveniente de cualquier módulo "
        "presente o futuro. Autoridad absoluta sobre la fundamentación, "
        "la resolución, la citación, la cadena normativa y la explicación "
        "documental. No altera el conocimiento declarado."
    ),


    # ===========================================================
    # 3.3 — FUNCIÓN
    # ===========================================================

    "funcion": (
        "Resolver, organizar, relacionar y citar cualquier declaración "
        "pública perteneciente al VPSI. "
        "Modo Engine: cadena documental del ciclo. "
        "Modo Consulta: resolución y explicación bajo demanda."
    ),


    # ===========================================================
    # 3.4 — RESTRICCIONES / NO HACE
    # ===========================================================

    "no_hace": [
        "Ninguna capacidad de CIT puede modificar el conocimiento declarado",
    ],


    # ===========================================================
    # 3.5 — AUTORIDAD
    # ===========================================================

    "autoridad": [
        "Autoridad absoluta sobre la fundamentación",
        "Autoridad absoluta sobre la resolución de declaraciones",
        "Autoridad absoluta sobre la citación",
        "Autoridad absoluta sobre la cadena normativa",
        "Autoridad absoluta sobre la explicación documental de cualquier cálculo",
        "Autoridad absoluta sobre la relación entre declaraciones",
        "Autoridad absoluta para responder consultas sobre el conocimiento declarado",
    ],


    # ===========================================================
    # 3.6 — PODERES
    # ===========================================================

    "poderes": [
        "Puede resolver cualquier declaración registrada",
        "Puede localizar cualquier norma",
        "Puede construir cadenas normativas",
        "Puede relacionar declaraciones",
        "Puede explicar por qué un cálculo produjo determinado resultado (solo con declaraciones existentes)",
        "Puede responder consultas documentales",
        "Puede anunciar cualquier declaración existente",
        "Puede producir evidencia documental durante la ejecución del Engine",
        "Puede producir evidencia documental fuera del Engine",
        "Puede citar cualquier conocimiento declarado",
    ],


    # ===========================================================
    # 3.7 — CONOCIMIENTO EXPORTABLE
    # ===========================================================

    "conocimiento_exportable": [
        "declaraciones",
        "resolver",
        "buscar",
        "cadena",
        "explicar",
        "citar",
        "anunciar",
        "relacionar",
        "inventario",
        "reporte",
        "diagnostico",
    ],
}


# ===============================================================
# FIN SECCIÓN 3
# ===============================================================

    # ===========================================================
    # 3.8 — ACCESO
    # ===========================================================
    #
    # Acceso declarado por el contrato del módulo.
    #

    "acceso": {
        "nivel": "completo",
        "descripcion": "Acceso total a recursos del módulo",
    },


    # ===========================================================
    # 3.9 — DEPENDENCIAS
    # ===========================================================
    #
    # Módulos requeridos por CIT para su operación contractual.
    #

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
        "TT",
        "CE",
        "CC",
    ],


    # ===========================================================
    # 3.10 — ACCESO A ARCHIVOS
    # ===========================================================
    #
    # Acceso declarado a los recursos de archivos.
    #

    "acceso_archivos": ["*"],


    # ===========================================================
    # 3.11 — VALIDACIÓN DE ESQUEMA
    # ===========================================================
    #
    # Ámbito declarado para validación de esquema a nivel módulo.
    #

    "validar_esquema": ["*"],


    # ===========================================================
    # 3.12 — CONSULTAS SOPORTADAS
    # ===========================================================

    "consultas_soportadas": [
        "resolver",
        "buscar",
        "buscar_por_tipo",
        "buscar_por_fuente",
        "cadena",
        "explicar",
        "citar",
        "anunciar",
        "relacionar",
        "obtener_inventario",
        "obtener_reporte",
        "obtener_diagnostico",
    ],


    # ===========================================================
    # 3.13 — AUTORIZACIÓN AL ENGINE
    # ===========================================================
    #
    # Este bloque declara permisos del Engine sobre CIT.
    # No constituye por sí mismo una capacidad ejecutable.
    #

    "autoriza_engine": {

        # =======================================================
        # 3.13.1 — PERMISOS BASE
        # =======================================================

        "leer": True,
        "ejecutar": True,
        "consultar": True,
        "recombinar": True,
        "reportar": True,
        "auditar": True,
        "inventariar": True,


        # =======================================================
        # 3.13.2 — PERMISOS DE ESCRITURA
        # =======================================================

        "alterar": False,
        "crear": True,
        "actualizar": False,


        # =======================================================
        # 3.13.3 — PERMISOS DE PROCESAMIENTO
        # =======================================================

        "validar": True,
        "procesar": True,
        "analizar": True,
        "generar": True,


        # =======================================================
        # 3.13.4 — PERMISOS DE DATOS
        # =======================================================

        "exportar": True,
        "importar": True,
        "respaldar": True,
        "recuperar": True,
        "sincronizar": True,


        # =======================================================
        # 3.13.5 — PERMISOS DE MONITOREO
        # =======================================================

        "monitorear": True,
        "metricas": True,
        "diagnostico": True,


        # =======================================================
        # 3.13.6 — PERMISOS DE ESTADO
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
        # 3.13.7 — PERMISOS OBLIGATORIOS AGREGADOS
        # =======================================================

        "validar_esquema": True,
        "acceso_archivos": True,
    },


       # ===========================================================
    # 3.14 — CAPACIDADES
    # ===========================================================
    #
    # Mapa contractual completo de capacidades ejecutables de CIT.
    # No se elimina ninguna capacidad existente.
    # Las capacidades arquitectónicas de Engine forman parte
    # explícita de la superficie callable del módulo.
    #

    "capacidades": {
        "verificar": verificar,
        "barrer": barrer,
        "inventario": inventario,
        "reporte": reporte,
        "diagnostico": diagnostico,
        "verificar_salida": verificar_salida,

        "anunciar": anunciar,
        "anunciar_todo": anunciar_todo,
        "citar": citar,
        "registrar": registrar,
        "resolver": resolver,
        "resolver_enunciado": resolver_enunciado,
        "buscar": buscar,
        "cadena": cadena,
        "explicar": explicar,
        "relacionar": relacionar,
        "limpiar_ciclo": limpiar_ciclo,

        # Compatibilidad Engine.
        "evaluar": anunciar,

        # =======================================================
        # CAPACIDADES ARQUITECTÓNICAS DE ENGINE
        # =======================================================

        "ejecutar_total": ejecutar_total,
        "inspeccionar": inspeccionar,
        "registrar_inventario": registrar_inventario,
    },


        # ============================================================
    # 3.15 — CAPACIDADES META
    # ============================================================
    #
    # Describe formalmente cada capacidad callable declarada en
    # CONTENEDOR["capacidades"].
    #
    # Regla:
    #   cada capacidad declarada debe poseer una capacidades_meta
    #   correspondiente.
    #
    # Las metacapacidades no ejecutan la función.
    # Describen entrada, validación, salida y acceso contractual.
    #
    # Todas las capacidades deben ser resolubles a callables reales.
    # ============================================================

    "capacidades_meta": {

        # ========================================================
        # 3.15.1 — VERIFICAR
        # ========================================================

        "verificar": {
            "descripcion": "Centinela del oficio de fundamentación.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con id, coherente, errores, choques",
            "acceso_archivos": ["*"],
        },


        # ========================================================
        # 3.15.2 — BARRER
        # ========================================================

        "barrer": {
            "descripcion": "Alias de verificar.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con id, coherente, errores, choques",
            "acceso_archivos": ["*"],
        },


        # ========================================================
        # 3.15.3 — INVENTARIO
        # ========================================================

        "inventario": {
            "descripcion": "Inventario contractual de CIT.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con id, nombre, rol, version, capacidades, "
                "tipos_declaracion"
            ),
            "acceso_archivos": ["*"],
        },


        # ========================================================
        # 3.15.4 — REPORTE
        # ========================================================

        "reporte": {
            "descripcion": "Reporte de estado de CIT.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con id, estado, coherente, registro_n",
            "acceso_archivos": ["*"],
        },


        # ========================================================
        # 3.15.5 — DIAGNÓSTICO
        # ========================================================

        "diagnostico": {
            "descripcion": "Diagnóstico propio de CIT.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con id, estado, problemas, advertencias"
            ),
            "acceso_archivos": ["*"],
        },


        # ========================================================
        # 3.15.6 — VERIFICAR SALIDA
        # ========================================================

        "verificar_salida": {
            "descripcion": "Forma mínima de salida de CIT.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "bool",
            "acceso_archivos": ["*"],
        },


        # ========================================================
        # 3.15.7 — ANUNCIAR
        # ========================================================

        "anunciar": {
            "descripcion": (
                "Modo Engine (paquete) o Consulta (declaración). "
                "Fundamentación documental sin recálculo."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con anuncio, anuncios o cadena documental",
            "acceso_archivos": ["*"],
        },


        # ========================================================
        # 3.15.8 — ANUNCIAR TODO
        # ========================================================

        "anunciar_todo": {
            "descripcion": (
                "Anuncia todas las declaraciones del registro operativo."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con anuncios, n",
            "acceso_archivos": ["*"],
        },


        # ========================================================
        # 3.15.9 — CITAR
        # ========================================================

        "citar": {
            "descripcion": (
                "Representación citable de declaraciones."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con citas, n",
            "acceso_archivos": ["*"],
        },


        # ========================================================
        # 3.15.10 — REGISTRAR
        # ========================================================

        "registrar": {
            "descripcion": (
                "Incorpora declaración al registro operativo. "
                "No altera origen."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con ok, declaracion",
            "acceso_archivos": ["*"],
        },


        # ========================================================
        # 3.15.11 — RESOLVER
        # ========================================================

        "resolver": {
            "descripcion": "Resuelve una declaración por id.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con resuelto, declaracion",
            "acceso_archivos": ["*"],
        },


        # ========================================================
        # 3.15.12 — RESOLVER ENUNCIADO
        # ========================================================

        "resolver_enunciado": {
            "descripcion": (
                "Alias de resolución orientado a enunciado."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con resuelto, enunciado",
            "acceso_archivos": ["*"],
        },


        # ========================================================
        # 3.15.13 — BUSCAR
        # ========================================================

        "buscar": {
            "descripcion": (
                "Consulta declaraciones del registro operativo."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con declaraciones, n",
            "acceso_archivos": ["*"],
        },


        # ========================================================
        # 3.15.14 — CADENA
        # ========================================================

        "cadena": {
            "descripcion": (
                "Construye cadena normativa a partir de ids resolubles."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con cadena, faltantes, completa",
            "acceso_archivos": ["*"],
        },


        # ========================================================
        # 3.15.15 — EXPLICAR
        # ========================================================

        "explicar": {
            "descripcion": (
                "Explicación documental solo con declaraciones existentes."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con explicacion, n, completa",
            "acceso_archivos": ["*"],
        },


        # ========================================================
        # 3.15.16 — RELACIONAR
        # ========================================================

        "relacionar": {
            "descripcion": (
                "Documenta relación entre dos declaraciones resolubles."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con ok, declaracion de enlace",
            "acceso_archivos": ["*"],
        },


        # ========================================================
        # 3.15.17 — LIMPIAR CICLO
        # ========================================================

        "limpiar_ciclo": {
            "descripcion": (
                "Limpia registro operativo del ciclo."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con ok, limpiadas",
            "acceso_archivos": ["*"],
        },


        # ========================================================
        # 3.15.18 — EVALUAR
        # ========================================================

        "evaluar": {
            "descripcion": (
                "Alias de anunciar (compatibilidad Engine)."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict de anuncio / fundamentación",
            "acceso_archivos": ["*"],
        },


        # ========================================================
        # 3.15.19 — EJECUTAR TOTAL
        # ========================================================
        #
        # Autoridad operativa total del Engine sobre las unidades
        # ejecutables declaradas por CIT.
        #

        "ejecutar_total": {
            "descripcion": (
                "Ejecuta el conjunto completo de capacidades "
                "operativamente ejercibles por Engine sobre CIT, "
                "sin inventar capacidades ni alterar el contrato."
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
        # 3.15.20 — INSPECCIONAR
        # ========================================================
        #
        # Exposición estructural del módulo sin cálculo.
        #

        "inspeccionar": {
            "descripcion": (
                "Inspección estructural de CIT. Expone contrato, "
                "capacidades, constantes, integridad y estado "
                "sin modificar el conocimiento declarado."
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
        # 3.15.21 — REGISTRAR INVENTARIO
        # ========================================================
        #
        # Instantánea contractual del inventario.
        #

        "registrar_inventario": {
            "descripcion": (
                "Registra una instantánea determinista del inventario "
                "estructural de CIT sin modificar el conocimiento "
                "declarado ni el contrato."
            ),
            "entrada": "dict opcional de peticion",
            "validar_esquema": ["*"],
            "salida": (
                "dict con id, operacion, registrado, inventario y nota"
            ),
            "acceso_archivos": ["*"],
        },
    },


    # ===============================================================
# SECCIÓN 7 — REPORTING, ESTADOS E INVARIANTES CONTRACTUALES
# ===============================================================

    # ============================================================
    # 7.1 — REPORTING
    # ============================================================
    #
    # Reporting absoluto y obligatorio según VPSI-CONTRACT-1.0.
    # Todas las capacidades de estado, salud, inventario,
    # diagnóstico y operación declaradas por el contrato
    # permanecen disponibles para el Engine.
    #

    "reporting": {
        # --------------------------------------------------------
        # 7.1.1 — ESTADO Y SALUD
        # --------------------------------------------------------
        "estado": True,
        "salud": True,

        # --------------------------------------------------------
        # 7.1.2 — INVENTARIO Y CAPACIDADES
        # --------------------------------------------------------
        "inventario": True,
        "capacidades": True,

        # --------------------------------------------------------
        # 7.1.3 — ERRORES Y ADVERTENCIAS
        # --------------------------------------------------------
        "errores": True,
        "advertencias": True,

        # --------------------------------------------------------
        # 7.1.4 — DEPENDENCIAS Y VERSIÓN
        # --------------------------------------------------------
        "dependencias": True,
        "version": True,

        # --------------------------------------------------------
        # 7.1.5 — CONTRATO Y CONOCIMIENTO
        # --------------------------------------------------------
        "contrato": True,
        "conocimiento": True,

        # --------------------------------------------------------
        # 7.1.6 — MÉTRICAS Y DIAGNÓSTICO
        # --------------------------------------------------------
        "metricas": True,
        "diagnostico": True,

        # --------------------------------------------------------
        # 7.1.7 — REPORTE
        # --------------------------------------------------------
        "reporte": True,

        # --------------------------------------------------------
        # 7.1.8 — CAPACIDADES OBLIGATORIAS DEL ENGINE
        # --------------------------------------------------------
        "acceso_archivos": True,
        "validar_esquema": True,

        # --------------------------------------------------------
        # 7.1.9 — CAPACIDADES OPERATIVAS AGREGADAS
        # --------------------------------------------------------
        "ejecutar_total": True,
        "inspeccionar": True,
        "registrar_inventario": True,
    },

    # ============================================================
    # 7.2 — ESTADOS VÁLIDOS
    # ============================================================

    "estados_validos": [
        "NO_INICIADO",
        "OPERATIVO",
        "DEGRADADO",
        "RECHAZADO",
    ],

    # ============================================================
    # 7.3 — INVARIANTES CONTRACTUALES
    # ============================================================
    #
    # Las invariantes definen restricciones permanentes del
    # comportamiento de CIT. No constituyen capacidades nuevas.
    #

    "invariantes": [
        "CIT conserva conocimiento declarativo universal resoluble",
        "CIT puede resolver cualquier declaración registrada",
        "CIT puede citar cualquier declaración registrada",
        "CIT puede construir cadenas de fundamentación",
        "CIT puede responder consultas documentales",
        "CIT nunca altera el conocimiento declarado",
        "CIT nunca modifica resultados",
        "CIT nunca reemplaza la autoridad de otros módulos",
        "CIT únicamente documenta y fundamenta",
        "Toda explicación producida por CIT debe provenir de declaraciones existentes",
        "Toda cita debe ser resoluble",
        "Toda cadena normativa debe ser trazable",
        "el id del módulo nunca cambia",
        "el rol nunca cambia",
        "las capacidades declaradas son callables tras la resolución",
        "este módulo no inventa capacidades no declaradas en CONTENEDOR",
        "este módulo siempre puede reportar su propio estado",
        "inventario() siempre incluye id, nombre, rol, version",
    ],

}

# ===============================================================
# FIN SECCIÓN 3 — CONTENEDOR
# ===============================================================

# ===============================================================
# SECCIÓN 4 — REGISTRO DE DECLARACIONES
# ===============================================================
#
# Memoria operativa del ciclo / consulta.
#
# El registro:
#   - conserva declaraciones normalizadas;
#   - no constituye corpus persistente;
#   - no modifica conocimiento de origen;
#   - no calcula;
#   - no interpreta;
#   - no sustituye la autoridad del módulo fuente.
#
# Toda declaración incorporada al registro debe atravesar primero
# la validación determinista y posteriormente la normalización.
#
# ===============================================================


_REGISTRO: List[Dict[str, Any]] = []


# ===============================================================
# 4.1 — VALIDACIÓN DETERMINISTA DE DECLARACIÓN
# ===============================================================

def _validar_declaracion(decl: Dict[str, Any]) -> List[str]:
    errores: List[str] = []

    if not isinstance(decl, dict):
        return ["declaracion debe ser dict"]

    # -----------------------------------------------------------
    # 4.1.1 — VALIDACIÓN DEL TIPO
    # -----------------------------------------------------------

    tipo = decl.get("tipo")

    if tipo is None:
        errores.append("falta campo obligatorio: tipo")
    elif not isinstance(tipo, str):
        errores.append(
            "tipo de declaración inválido: {0}".format(
                type(tipo).__name__
            )
        )
    elif not tipo.strip():
        errores.append("tipo de declaración inválido: vacío")

    # -----------------------------------------------------------
    # 4.1.2 — VALIDACIÓN DEL ID
    # -----------------------------------------------------------
    #
    # Excepción contractual:
    # tipo == "limite" puede carecer de id.
    # -----------------------------------------------------------

    id_decl = decl.get("id")

    if tipo == "limite" and id_decl in (None, ""):
        pass
    elif id_decl is None:
        errores.append("falta campo obligatorio: id")
    elif not isinstance(id_decl, str):
        errores.append(
            "id de declaración inválido: {0}".format(
                type(id_decl).__name__
            )
        )
    elif not id_decl.strip():
        errores.append("id de declaración inválido: vacío")

    # -----------------------------------------------------------
    # 4.1.3 — VALIDACIÓN DE FUENTE
    # -----------------------------------------------------------

    fuente = decl.get("fuente")
    fuente_modulo = decl.get("fuente_modulo")

    if fuente in (None, ""):
        fuente = fuente_modulo

    if fuente is None:
        errores.append("falta campo obligatorio: fuente")
    elif not isinstance(fuente, str):
        errores.append(
            "fuente de declaración inválida: {0}".format(
                type(fuente).__name__
            )
        )
    elif not fuente.strip():
        errores.append("fuente de declaración inválida: vacío")

    # -----------------------------------------------------------
    # 4.1.4 — VALIDACIÓN DEL ENUNCIADO
    # -----------------------------------------------------------

    enunciado = decl.get("enunciado")

    if enunciado is None:
        errores.append("falta campo obligatorio: enunciado")
    elif not isinstance(enunciado, str):
        errores.append(
            "enunciado de declaración inválido: {0}".format(
                type(enunciado).__name__
            )
        )
    elif not enunciado.strip():
        errores.append("enunciado de declaración inválido: vacío")

    # -----------------------------------------------------------
    # 4.1.5 — VALIDACIÓN DE CAMPOS OPCIONALES
    # -----------------------------------------------------------

    if "descripcion" in decl and decl["descripcion"] is not None:
        if not isinstance(decl["descripcion"], str):
            errores.append(
                "descripcion debe ser str cuando está presente"
            )

    if "evidencia_ref" in decl and decl["evidencia_ref"] is not None:
        if not isinstance(decl["evidencia_ref"], str):
            errores.append(
                "evidencia_ref debe ser str cuando está presente"
            )

    if "o_ref" in decl and decl["o_ref"] is not None:
        if not isinstance(decl["o_ref"], str):
            errores.append(
                "o_ref debe ser str cuando está presente"
            )

    if "contexto_ciclo" in decl and decl["contexto_ciclo"] is not None:
        if not isinstance(decl["contexto_ciclo"], str):
            errores.append(
                "contexto_ciclo debe ser str cuando está presente"
            )

    if "meta" in decl and decl["meta"] is not None:
        if not isinstance(decl["meta"], dict):
            errores.append(
                "meta debe ser dict cuando está presente"
            )

    if "relaciones" in decl and decl["relaciones"] is not None:
        if not isinstance(decl["relaciones"], list):
            errores.append(
                "relaciones debe ser list cuando está presente"
            )

    return errores


# ===============================================================
# 4.2 — NORMALIZACIÓN DETERMINISTA DE DECLARACIÓN
# ===============================================================

def _normalizar_declaracion(
    decl: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Produce una representación canónica de una declaración.

    Esta función presupone que la declaración ya superó
    _validar_declaracion().
    """

    # -----------------------------------------------------------
    # 4.2.1 — RESOLUCIÓN CANÓNICA DE FUENTE
    # -----------------------------------------------------------

    fuente = decl.get("fuente")

    if fuente is None or (
        isinstance(fuente, str) and not fuente.strip()
    ):
        fuente = decl.get("fuente_modulo")

    if isinstance(fuente, str):
        fuente = fuente.strip()

    # -----------------------------------------------------------
    # 4.2.2 — RESOLUCIÓN CANÓNICA DE IDENTIFICADORES
    # -----------------------------------------------------------

    id_decl = decl.get("id")

    if isinstance(id_decl, str):
        id_decl = id_decl.strip()

    tipo = decl.get("tipo")

    if isinstance(tipo, str):
        tipo = tipo.strip()

    enunciado = decl.get("enunciado")

    if isinstance(enunciado, str):
        enunciado = enunciado.strip()

    # -----------------------------------------------------------
    # 4.2.3 — CONSTRUCCIÓN CANÓNICA
    # -----------------------------------------------------------

    out: Dict[str, Any] = {
        "id": id_decl,
        "tipo": tipo,
        "fuente": fuente,
        "fuente_modulo": fuente,
        "enunciado": enunciado,
        "descripcion": "",
        "evidencia_ref": "",
    }

    # -----------------------------------------------------------
    # 4.2.4 — CAMPOS OPCIONALES
    # -----------------------------------------------------------

    descripcion = decl.get("descripcion")

    if descripcion is not None:
        out["descripcion"] = (
            descripcion.strip()
            if isinstance(descripcion, str)
            else descripcion
        )

    evidencia_ref = decl.get("evidencia_ref")

    if evidencia_ref is not None:
        out["evidencia_ref"] = (
            evidencia_ref.strip()
            if isinstance(evidencia_ref, str)
            else evidencia_ref
        )

    # -----------------------------------------------------------
    # 4.2.5 — CAMPOS DECLARATIVOS OPCIONALES
    # -----------------------------------------------------------

    for campo in (
        "o_ref",
        "contexto_ciclo",
        "meta",
    ):
        if campo in decl and decl[campo] is not None:
            valor = decl[campo]

            if isinstance(valor, str):
                valor = valor.strip()

            out[campo] = valor

    # -----------------------------------------------------------
    # 4.2.6 — RELACIONES
    # -----------------------------------------------------------

    relaciones = decl.get("relaciones")

    if relaciones is None:
        relaciones = []

    out["relaciones"] = list(relaciones)

    # -----------------------------------------------------------
    # 4.2.7 — RESULTADO CANÓNICO
    # -----------------------------------------------------------

    return out


# ===============================================================
# 4.3 — INCORPORACIÓN DETERMINISTA AL REGISTRO
# ===============================================================

def registrar(
    declaracion: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Incorpora una declaración validada y normalizada al registro
    operativo del ciclo.

    No modifica conocimiento de origen.
    No sustituye declaraciones existentes.
    No calcula.
    No interpreta.
    """

    # -----------------------------------------------------------
    # 4.3.1 — VALIDACIÓN
    # -----------------------------------------------------------

    errores = _validar_declaracion(declaracion)

    if errores:
        return {
            "ok": False,
            "id": _ID,
            "errores": errores,
            "declaracion": None,
            "n": len(_REGISTRO),
        }

    # -----------------------------------------------------------
    # 4.3.2 — NORMALIZACIÓN
    # -----------------------------------------------------------

    normalizada = _normalizar_declaracion(declaracion)

    # -----------------------------------------------------------
    # 4.3.3 — INCORPORACIÓN
    # -----------------------------------------------------------

    _REGISTRO.append(normalizada)

    # -----------------------------------------------------------
    # 4.3.4 — SALIDA CANÓNICA
    # -----------------------------------------------------------

    return {
        "ok": True,
        "id": _ID,
        "n": len(_REGISTRO),
        "declaracion": normalizada,
    }


# ===============================================================
# 4.4 — LIMPIEZA DETERMINISTA DEL CICLO
# ===============================================================

def limpiar_ciclo() -> Dict[str, Any]:
    """
    Vacía exclusivamente la memoria operativa de CIT.

    No modifica ningún corpus externo ni conocimiento de origen.
    """

    n = len(_REGISTRO)

    _REGISTRO.clear()

    return {
        "ok": True,
        "id": _ID,
        "limpiadas": n,
        "n": len(_REGISTRO),
    }


# ===============================================================
# FIN SECCIÓN 4
# ===============================================================

# ===============================================================
# SECCIÓN 5 — RESOLUCIÓN DETERMINISTA DE DECLARACIONES
# ===============================================================
#
# Responsabilidad:
#   Resolver una declaración mediante su identificador.
#
# Orden de resolución:
#   5.1 Validación del identificador
#   5.2 Registro operativo
#   5.3 Fuente declarativa del sistema
#   5.4 Validación de respuesta de fuente
#   5.5 Normalización
#   5.6 Validación final
#   5.7 Salida canónica
#
# Principios:
#   - resolver() no crea declaraciones.
#   - resolver() no registra declaraciones.
#   - resolver() no modifica _REGISTRO.
#   - resolver() no modifica conocimiento de origen.
#   - el registro operativo tiene precedencia sobre la fuente.
#   - una fuente no resoluble no se convierte en declaración.
#   - toda salida tiene forma determinista.
#
# ===============================================================


def resolver(id_decl: str) -> Dict[str, Any]:

    # ===========================================================
    # 5.1 — VALIDACIÓN DEL IDENTIFICADOR
    # ===========================================================

    if id_decl is None:
        return {
            "id": None,
            "resuelto": False,
            "declaracion": None,
            "origen": None,
            "errores": ["id vacío"],
            "nota": "identificador no proporcionado",
        }

    if not isinstance(id_decl, str):
        return {
            "id": id_decl,
            "resuelto": False,
            "declaracion": None,
            "origen": None,
            "errores": [
                "id de declaración inválido: {0}".format(
                    type(id_decl).__name__
                )
            ],
            "nota": "el identificador debe ser str",
        }

    clave = id_decl.strip()

    if not clave:
        return {
            "id": id_decl,
            "resuelto": False,
            "declaracion": None,
            "origen": None,
            "errores": ["id vacío"],
            "nota": "identificador vacío después de normalización",
        }

    # ===========================================================
    # 5.2 — RESOLUCIÓN EN REGISTRO OPERATIVO
    # ===========================================================

    for declaracion in _REGISTRO:

        if declaracion.get("id") != clave:
            continue

        if not declaracion.get("enunciado"):
            return {
                "id": clave,
                "resuelto": False,
                "declaracion": None,
                "origen": "registro_ciclo",
                "errores": [
                    "declaración registrada sin enunciado resoluble"
                ],
                "nota": "el registro contiene el id pero la declaración no es resoluble",
            }

        return {
            "id": clave,
            "resuelto": True,
            "declaracion": declaracion,
            "origen": "registro_ciclo",
            "errores": [],
            "nota": "resuelto desde registro operativo de CIT",
        }

    # ===========================================================
    # 5.3 — RESOLUCIÓN DESDE FUENTE DECLARATIVA
    # ===========================================================

    try:
        from modules.citacion.fuentes import ax as fuente_ax
    except ImportError as exc:
        return {
            "id": clave,
            "resuelto": False,
            "declaracion": None,
            "origen": "fuente_sistema",
            "errores": [
                "fuente declarativa no disponible: {0}: {1}".format(
                    type(exc).__name__,
                    exc,
                )
            ],
            "nota": "no fue posible cargar la fuente declarativa",
        }

    try:
        resultado_fuente = fuente_ax.anunciar_id(
            clave,
            evidencia_ref="cit.resolver",
            registrar=False,
        )
    except Exception as exc:
        return {
            "id": clave,
            "resuelto": False,
            "declaracion": None,
            "origen": "fuente_sistema",
            "errores": [
                "error durante resolución de fuente: {0}: {1}".format(
                    type(exc).__name__,
                    exc,
                )
            ],
            "nota": "la fuente produjo una excepción durante la resolución",
        }

    # ===========================================================
    # 5.4 — VALIDACIÓN DE RESPUESTA DE FUENTE
    # ===========================================================

    if not isinstance(resultado_fuente, dict):
        return {
            "id": clave,
            "resuelto": False,
            "declaracion": None,
            "origen": "fuente_sistema",
            "errores": [
                "la fuente devolvió una salida no válida"
            ],
            "nota": "respuesta de fuente incompatible con contrato",
        }

    if not resultado_fuente.get("resuelto"):
        return {
            "id": clave,
            "resuelto": False,
            "declaracion": None,
            "origen": "fuente_sistema",
            "errores": [],
            "nota": "id no encontrado en la fuente declarativa",
        }

    cita = resultado_fuente.get("cita")

    if not isinstance(cita, dict):
        return {
            "id": clave,
            "resuelto": False,
            "declaracion": None,
            "origen": "fuente_sistema",
            "errores": [
                "la fuente indicó resolución sin proporcionar una cita dict"
            ],
            "nota": "respuesta de fuente incompleta",
        }

    # ===========================================================
    # 5.5 — NORMALIZACIÓN DE DECLARACIÓN DE FUENTE
    # ===========================================================

    declaracion = _normalizar_declaracion(
        {
            "id": clave,
            "tipo": cita.get("tipo") or "axioma",
            "fuente": (
                cita.get("fuente")
                or cita.get("fuente_modulo")
                or "ax"
            ),
            "enunciado": cita.get("enunciado"),
            "descripcion": cita.get("descripcion"),
            "evidencia_ref": cita.get("evidencia_ref"),
            "o_ref": cita.get("o_ref"),
            "contexto_ciclo": cita.get("contexto_ciclo"),
            "meta": cita.get("meta"),
            "relaciones": cita.get("relaciones"),
        }
    )

    # ===========================================================
    # 5.6 — VALIDACIÓN FINAL DE DECLARACIÓN
    # ===========================================================

    errores = _validar_declaracion(declaracion)

    if errores:
        return {
            "id": clave,
            "resuelto": False,
            "declaracion": None,
            "origen": "fuente_sistema",
            "errores": errores,
            "nota": (
                "la fuente proporcionó una declaración "
                "incompatible con el contrato de CIT"
            ),
        }

    # ===========================================================
    # 5.7 — SALIDA CANÓNICA
    # ===========================================================

    return {
        "id": clave,
        "resuelto": True,
        "declaracion": declaracion,
        "origen": "fuente_sistema",
        "errores": [],
        "nota": "resuelto desde fuente de declaraciones del sistema",
    }


# ===============================================================
# FIN SECCIÓN 5
# ===============================================================


# ===============================================================
# SECCIÓN 6 — ANUNCIO Y FUNDAMENTACIÓN DOCUMENTAL UNIVERSAL
# ===============================================================
#
# Responsabilidad:
#   - convertir declaraciones existentes en representaciones
#     documentales;
#   - anunciar el registro operativo;
#   - recibir paquetes de ciclo provenientes del Engine;
#   - descubrir fuentes declarativas mediante mecanismo genérico;
#   - consumir sus declaraciones mediante interfaz callable;
#   - registrar únicamente declaraciones que superen el contrato;
#   - producir la salida documental determinista.
#
# Restricciones:
#   - CIT no calcula;
#   - CIT no interpreta resultados;
#   - CIT no modifica conocimiento de origen;
#   - CIT no conoce módulos concretos;
#   - CIT no mantiene una lista cerrada de fuentes;
#   - CIT no inventa declaraciones;
#   - toda fuente debe entrar mediante el contrato genérico;
#   - toda capacidad declarada debe ser callable;
#   - toda salida debe ser verificable estructuralmente.
#
# ===============================================================


# ===============================================================
# 6.1 — REPRESENTACIÓN DOCUMENTAL DE UNA DECLARACIÓN
# ===============================================================

def _anuncio_de_declaracion(
    decl: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Convierte una declaración válida en su representación documental.

    No registra.
    No modifica.
    No calcula.
    """

    errores = _validar_declaracion(decl)

    if errores:
        return {
            "id": _ID,
            "ok": False,
            "errores": errores,
            "anuncio": None,
        }

    normalizada = _normalizar_declaracion(decl)

    anuncio = {
        "titulo": "[{0}] {1}".format(
            normalizada.get("fuente"),
            normalizada.get("id"),
        ),
        "tipo": normalizada.get("tipo"),
        "enunciado": normalizada.get("enunciado"),
        "descripcion": normalizada.get("descripcion"),
        "evidencia_ref": normalizada.get("evidencia_ref"),
        "o_ref": normalizada.get("o_ref"),
        "contexto_ciclo": normalizada.get("contexto_ciclo"),
        "relaciones": normalizada.get("relaciones") or [],
    }

    return {
        "id": _ID,
        "ok": True,
        "anuncio": anuncio,
    }


# ===============================================================
# 6.2 — ANUNCIO TOTAL DEL REGISTRO
# ===============================================================

def anunciar_todo(
    filtro: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Anuncia todas las declaraciones del registro que satisfacen
    el filtro recibido.

    El orden es exactamente el orden del registro.
    """

    paquete = buscar(filtro)

    anuncios: List[Dict[str, Any]] = []

    for declaracion in paquete.get("declaraciones") or []:
        resultado = _anuncio_de_declaracion(declaracion)

        if resultado.get("ok") is True:
            anuncio = resultado.get("anuncio")

            if anuncio is not None:
                anuncios.append(anuncio)

    return {
        "id": _ID,
        "anuncios": anuncios,
        "n": len(anuncios),
        "filtro": filtro or {},
        "nota": (
            "Anuncio documental de declaraciones existentes; "
            "sin recálculo y sin modificación."
        ),
    }


# ===============================================================
# 6.3 — IDENTIFICACIÓN DETERMINISTA DE ENTRADA
# ===============================================================

def _es_paquete_ciclo(
    obj: Any,
) -> bool:
    """
    Determina si una entrada posee forma contractual de paquete
    de ciclo.

    Tiene precedencia sobre declaración suelta.
    """

    if not isinstance(obj, dict):
        return False

    if (
        "resultado" in obj
        and isinstance(obj.get("resultado"), dict)
    ):
        return True

    if (
        "contexto_cx" in obj
        and "tipos_peticion" in obj
    ):
        return True

    if (
        obj.get("engine_version")
        and (
            "resultado" in obj
            or "peticion" in obj
        )
    ):
        return True

    return False


def _es_declaracion_suelta(
    obj: Any,
) -> bool:
    """
    Determina si una entrada posee forma de declaración individual.

    Un paquete de ciclo nunca se interpreta simultáneamente
    como declaración suelta.
    """

    if not isinstance(obj, dict):
        return False

    if _es_paquete_ciclo(obj):
        return False

    return (
        "tipo" in obj
        or "enunciado" in obj
        or "id" in obj
    )


# ===============================================================
# 6.4 — REFERENCIA DETERMINISTA DE EVIDENCIA
# ===============================================================

def _evidencia_ref(
    paquete: Dict[str, Any],
) -> str:
    """
    Construye la referencia documental del ciclo.

    La función únicamente representa información existente
    en el paquete.
    """

    invocador = paquete.get("invocador_id") or "ciclo"
    version = paquete.get("engine_version") or ""

    resultado = paquete.get("resultado")

    if not isinstance(resultado, dict):
        resultado = {}

    referencia = "ciclo:{0}:v{1}".format(
        invocador,
        version,
    )

    secuencia = resultado.get("secuencia")

    if secuencia is not None:
        referencia = "{0}:seq={1}".format(
            referencia,
            secuencia,
        )

    return referencia


# ===============================================================
# 6.5 — REFERENCIA DETERMINISTA DE O
# ===============================================================

def _o_ref(
    paquete: Dict[str, Any],
) -> Optional[str]:
    """
    Obtiene una referencia O ya existente.

    No crea contexto O.
    No interpreta contexto.
    """

    resultado = paquete.get("resultado")

    if not isinstance(resultado, dict):
        resultado = {}

    contexto = paquete.get("contexto_cx")

    if not isinstance(contexto, dict):
        contexto = {}

    registro = contexto.get("registro")

    if not isinstance(registro, dict):
        registro = {}

    peticion = paquete.get("peticion")

    if not isinstance(peticion, dict):
        peticion = {}

    fuentes = (
        resultado,
        contexto,
        registro,
        peticion,
    )

    claves = (
        "O_id",
        "o_id",
        "O_context",
        "contexto",
        "enunciado_O",
    )

    for fuente in fuentes:
        for clave in claves:
            valor = fuente.get(clave)

            if valor is None:
                continue

            texto = str(valor).strip()

            if not texto:
                continue

            if texto.lower() in (
                "undefined",
                "indefinido",
                "none",
                "null",
            ):
                continue

            return texto[:200]

    return None


# ===============================================================
# 6.6 — DESCUBRIMIENTO GENÉRICO DE FUENTES
# ===============================================================

def _obtener_fuentes_declarativas() -> List[Any]:
    """
    Obtiene las fuentes declarativas mediante el mecanismo
    genérico del paquete.

    CIT no enumera módulos.
    CIT no conoce fuentes concretas.
    """

    fuentes: List[Any] = []

    try:
        from modules.citacion import fuentes as registro_fuentes

        obtener = getattr(
            registro_fuentes,
            "obtener_fuentes",
            None,
        )

        if not callable(obtener):
            return fuentes

        resultado = obtener()

        if not isinstance(resultado, (list, tuple)):
            return fuentes

        for fuente in resultado:
            if fuente is not None:
                fuentes.append(fuente)

    except Exception:
        return []

    return fuentes


# ===============================================================
# 6.7 — VALIDACIÓN CONTRACTUAL DE FUENTE
# ===============================================================

def _validar_fuente_declarativa(
    fuente: Any,
) -> bool:
    """
    Determina si una fuente posee una interfaz callable válida.
    """

    if fuente is None:
        return False

    anunciar_fuente = getattr(
        fuente,
        "anunciar",
        None,
    )

    obtener_declaraciones = getattr(
        fuente,
        "obtener_declaraciones",
        None,
    )

    return (
        callable(anunciar_fuente)
        or callable(obtener_declaraciones)
    )


# ===============================================================
# 6.8 — EJECUCIÓN CONTRACTUAL DE UNA FUENTE
# ===============================================================

def _ejecutar_fuente_declarativa(
    fuente: Any,
    paquete: Dict[str, Any],
    evidencia_ref: str,
    o_ref: Optional[str],
    contexto_ciclo: str,
) -> Dict[str, Any]:
    """
    Ejecuta una fuente mediante su interfaz callable.

    CIT no conoce ni interpreta la implementación interna
    de la fuente.
    """

    if not _validar_fuente_declarativa(fuente):
        return {
            "id": _ID,
            "ok": False,
            "errores": [
                "fuente declarativa incompatible"
            ],
            "n": 0,
            "declaraciones": [],
        }

    anunciar_fuente = getattr(
        fuente,
        "anunciar",
        None,
    )

    obtener_declaraciones = getattr(
        fuente,
        "obtener_declaraciones",
        None,
    )

    try:
        if callable(anunciar_fuente):
            resultado = anunciar_fuente(
                paquete=paquete,
                evidencia_ref=evidencia_ref,
                o_ref=o_ref,
                contexto_ciclo=contexto_ciclo,
            )

        elif callable(obtener_declaraciones):
            resultado = obtener_declaraciones(
                paquete=paquete,
                evidencia_ref=evidencia_ref,
                o_ref=o_ref,
                contexto_ciclo=contexto_ciclo,
            )

        else:
            return {
                "id": _ID,
                "ok": False,
                "errores": [
                    "fuente sin interfaz callable"
                ],
                "n": 0,
                "declaraciones": [],
            }

    except Exception as error:
        return {
            "id": _ID,
            "ok": False,
            "errores": [
                "error en fuente declarativa: {0}: {1}".format(
                    type(error).__name__,
                    error,
                )
            ],
            "n": 0,
            "declaraciones": [],
        }

    if not isinstance(resultado, dict):
        return {
            "id": _ID,
            "ok": False,
            "errores": [
                "salida de fuente declarativa debe ser dict"
            ],
            "n": 0,
            "declaraciones": [],
        }

    declaraciones = resultado.get("declaraciones")

    if declaraciones is None:
        declaraciones = []

    if not isinstance(declaraciones, list):
        return {
            "id": _ID,
            "ok": False,
            "errores": [
                "declaraciones de fuente deben ser list"
            ],
            "n": 0,
            "declaraciones": [],
        }

    registradas: List[Dict[str, Any]] = []
    errores: List[str] = []

    for declaracion in declaraciones:
        resultado_registro = registrar(declaracion)

        if resultado_registro.get("ok") is True:
            registrada = (
                resultado_registro.get("declaracion")
                or declaracion
            )

            registradas.append(registrada)

        else:
            errores.extend(
                str(error)
                for error in (
                    resultado_registro.get("errores") or []
                )
            )

    return {
        "id": _ID,
        "ok": not errores,
        "errores": errores,
        "n": len(registradas),
        "declaraciones": registradas,
    }


# ===============================================================
# 6.9 — EJECUCIÓN UNIVERSAL DEL PAQUETE
# ===============================================================

def _anunciar_paquete(
    paquete: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Procesa un paquete de ciclo mediante fuentes declarativas
    descubiertas dinámicamente.

    No existe conocimiento específico de módulos dentro de esta
    función.
    """

    if not isinstance(paquete, dict):
        return {
            "id": _ID,
            "ok": False,
            "estado": "ERROR_FORMA",
            "errores": [
                "paquete debe ser dict"
            ],
            "n_declaraciones": 0,
            "n_citas": 0,
            "n_anuncios": 0,
            "anuncios": [],
        }

    limpiar_ciclo()

    resultado = paquete.get("resultado")

    if not isinstance(resultado, dict):
        resultado = {}

    contexto = paquete.get("contexto_cx")

    if not isinstance(contexto, dict):
        contexto = {}

    tipos = paquete.get("tipos_peticion")

    if not isinstance(tipos, list):
        tipos = contexto.get("tipos_peticion")

    if not isinstance(tipos, list):
        tipos = []

    tipos = list(tipos)

    if not tipos:
        tipos = ["dame_cadena_completa"]

    evidencia = _evidencia_ref(paquete)
    referencia_o = _o_ref(paquete)

    contexto_ciclo = str(
        resultado.get("estado")
        or contexto.get("modo_entrada")
        or "ciclo"
    )

    fuentes = _obtener_fuentes_declarativas()

    errores: List[str] = []
    fuentes_validas = 0
    declaraciones_fuentes = 0

    for fuente in fuentes:
        if not _validar_fuente_declarativa(fuente):
            errores.append(
                "fuente declarativa incompatible"
            )
            continue

        fuentes_validas += 1

        salida_fuente = _ejecutar_fuente_declarativa(
            fuente=fuente,
            paquete=paquete,
            evidencia_ref=evidencia,
            o_ref=referencia_o,
            contexto_ciclo=contexto_ciclo,
        )

        errores.extend(
            str(error)
            for error in (
                salida_fuente.get("errores") or []
            )
        )

        declaraciones_fuentes += int(
            salida_fuente.get("n") or 0
        )

    # -----------------------------------------------------------
    # AUTODECLARACIÓN CONTRACTUAL DE CIT
    # -----------------------------------------------------------

    declaracion_cit = {
        "id": "CIT-CICLO",
        "tipo": "citacion",
        "fuente": _NOMBRE,
        "enunciado": (
            "CIT fundamentó documentalmente el ciclo."
        ),
        "descripcion": (
            "Declaración del oficio de fundamentación de CIT."
        ),
        "evidencia_ref": evidencia,
        "o_ref": referencia_o,
        "contexto_ciclo": contexto_ciclo,
        "meta": {
            "tipos_peticion": tipos,
            "estado": resultado.get("estado"),
        },
    }

    registro_cit = registrar(declaracion_cit)

    if registro_cit.get("ok") is not True:
        errores.extend(
            str(error)
            for error in (
                registro_cit.get("errores") or []
            )
        )

    anuncios_pack = anunciar_todo()

    ok = (
        len(_REGISTRO) > 0
        and not (
            len(_REGISTRO) == 0
            and errores
        )
    )

    return {
        "id": _ID,
        "estado": "OK" if ok else "VACIO",
        "ok": ok,
        "n_fuentes": len(fuentes),
        "n_fuentes_validas": fuentes_validas,
        "n_declaraciones_fuentes": declaraciones_fuentes,
        "n_declaraciones": len(_REGISTRO),
        "n_citas": len(_REGISTRO),
        "n_anuncios": anuncios_pack.get("n", 0),
        "anuncios": anuncios_pack.get("anuncios") or [],
        "tipos_peticion": tipos,
        "evidencia_ref": evidencia,
        "o_ref": referencia_o,
        "errores": errores,
        "engine_version": paquete.get("engine_version"),
        "nota": (
            "CIT documenta y fundamenta mediante fuentes "
            "declarativas descubiertas contractualmente; "
            "sin cálculo, interpretación ni modificación "
            "del conocimiento de origen."
        ),
    }


# ===============================================================
# 6.10 — ENTRADA ÚNICA CALLABLE DE ANUNCIO
# ===============================================================

def anunciar(
    arg: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Entrada pública única de la capacidad anunciar.

    Rutas deterministas:

        None
            → anunciar_todo()

        paquete de ciclo
            → _anunciar_paquete()

        declaración suelta
            → registrar()
            → _anuncio_de_declaracion()

        cualquier otra forma
            → ERROR_FORMA
    """

    if arg is None:
        return anunciar_todo()

    if _es_paquete_ciclo(arg):
        return _anunciar_paquete(arg)

    if _es_declaracion_suelta(arg):
        resultado_registro = registrar(arg)

        if resultado_registro.get("ok") is not True:
            return {
                "id": _ID,
                "ok": False,
                "errores": (
                    resultado_registro.get("errores")
                    or ["declaración inválida"]
                ),
                "anuncio": None,
            }

        return _anuncio_de_declaracion(
            resultado_registro.get("declaracion")
            or arg
        )

    return {
        "id": _ID,
        "ok": False,
        "estado": "ERROR_FORMA",
        "errores": [
            "anunciar requiere None, paquete de ciclo "
            "o declaración individual"
        ],
        "anuncio": None,
    }


# ===============================================================
# FIN SECCIÓN 6
# ===============================================================

# ===============================================================
# SECCIÓN 7 — CAPACIDAD: CITAR
# ===============================================================
#
# Cita determinista de declaraciones.
#
# Esta capacidad:
#   - recibe una petición declarativa genérica;
#   - utiliza el registro operativo de CIT;
#   - no conoce módulos concretos;
#   - no contiene una lista cerrada de fuentes;
#   - no calcula;
#   - no interpreta;
#   - no modifica declaraciones;
#   - no modifica conocimiento de origen;
#   - conserva la representación declarativa existente.
#
# Toda declaración citable debe provenir del registro operativo
# y, por tanto, haber atravesado previamente la validación y
# normalización correspondientes.
#
# ===============================================================


def citar(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Produce una representación citable de las declaraciones
    resolubles mediante el registro operativo de CIT.

    La operación es puramente documental.

    Entrada:
        peticion:
            Diccionario opcional con los mismos filtros generales
            admitidos por buscar().

    Salida:
        {
            "id": _ID,
            "citas": [...],
            "n": int,
            "filtro": {...},
            "nota": str
        }

    Garantías:
        - no crea declaraciones;
        - no modifica declaraciones;
        - no modifica conocimiento externo;
        - no recalcula resultados;
        - no interpreta contenido;
        - no depende de módulos concretos;
        - la salida deriva determinísticamente de buscar().
    """

    # -----------------------------------------------------------
    # 7.1 — NORMALIZACIÓN DE PETICIÓN
    # -----------------------------------------------------------

    if peticion is None:
        filtro: Dict[str, Any] = {}

    elif isinstance(peticion, dict):
        filtro = dict(peticion)

    else:
        return {
            "id": _ID,
            "citas": [],
            "n": 0,
            "filtro": {},
            "ok": False,
            "errores": [
                "peticion debe ser dict o None"
            ],
            "nota": (
                "CIT no puede construir una cita desde una "
                "petición de forma inválida."
            ),
        }

    # -----------------------------------------------------------
    # 7.2 — RESOLUCIÓN DEL CONJUNTO DECLARATIVO
    # -----------------------------------------------------------
    #
    # citar no implementa filtros propios.
    # La selección pertenece a buscar().
    #

    resultado = buscar(filtro)

    declaraciones = resultado.get("declaraciones")

    if not isinstance(declaraciones, list):
        declaraciones = []

    # -----------------------------------------------------------
    # 7.3 — CONSTRUCCIÓN DETERMINISTA DE CITAS
    # -----------------------------------------------------------
    #
    # La cita conserva la declaración existente.
    # No se introduce información externa.
    #

    citas: List[Dict[str, Any]] = []

    for declaracion in declaraciones:
        if not isinstance(declaracion, dict):
            continue

        cita = dict(declaracion)

        # -------------------------------------------------------
        # 7.3.1 — IDENTIDAD DE LA CITA
        # -------------------------------------------------------

        cita["citable"] = True

        # -------------------------------------------------------
        # 7.3.2 — TRAZABILIDAD DE ORIGEN
        # -------------------------------------------------------

        if "fuente" not in cita:
            cita["fuente"] = ""

        if "fuente_modulo" not in cita:
            cita["fuente_modulo"] = cita.get("fuente")

        # -------------------------------------------------------
        # 7.3.3 — GARANTÍA DE REPRESENTACIÓN DECLARATIVA
        # -------------------------------------------------------

        if "id" not in cita:
            cita["id"] = None

        if "tipo" not in cita:
            cita["tipo"] = None

        if "enunciado" not in cita:
            cita["enunciado"] = ""

        citas.append(cita)

    # -----------------------------------------------------------
    # 7.4 — SALIDA DETERMINISTA
    # -----------------------------------------------------------

    return {
        "id": _ID,
        "ok": True,
        "citas": citas,
        "n": len(citas),
        "filtro": filtro,
        "nota": (
            "CIT: representación citable de declaraciones "
            "existentes. Sin recálculo, sin interpretación y "
            "sin modificación del conocimiento declarado."
        ),
    }


# ===============================================================
# FIN SECCIÓN 7
# ===============================================================

# ===============================================================
# SECCIÓN 8 — CAPACIDAD: REGISTRAR
# ===============================================================
#
# Incorpora una declaración al registro operativo de CIT.
#
# Esta capacidad:
#   - recibe cualquier declaración declarativa compatible;
#   - valida su estructura de forma determinista;
#   - normaliza su representación;
#   - incorpora únicamente declaraciones válidas;
#   - conserva la identidad y contenido declarado;
#   - no modifica el conocimiento de origen;
#   - no modifica otros módulos;
#   - no calcula;
#   - no interpreta;
#   - no requiere conocer qué módulo produjo la declaración.
#
# El registro es operativo y temporal.
# No constituye corpus persistente.
#
# ===============================================================


def registrar(
    declaracion: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Registra una declaración después de validarla y normalizarla.

    Entrada:
        declaracion:
            Declaración declarativa en forma dict.

    Salida válida:
        {
            "ok": True,
            "n": int,
            "declaracion": dict,
            "id": _ID
        }

    Salida inválida:
        {
            "ok": False,
            "errores": [...],
            "id": _ID
        }

    Garantías:
        - ninguna declaración inválida entra al registro;
        - toda declaración registrada está normalizada;
        - el origen no es modificado;
        - el registro no sustituye al módulo fuente;
        - no se introducen declaraciones no presentes en la entrada;
        - la operación es determinista respecto de la entrada y
          del estado previo de _REGISTRO.
    """

    # -----------------------------------------------------------
    # 8.1 — VALIDACIÓN
    # -----------------------------------------------------------

    errores = _validar_declaracion(declaracion)

    if errores:
        return {
            "ok": False,
            "errores": list(errores),
            "id": _ID,
        }

    # -----------------------------------------------------------
    # 8.2 — NORMALIZACIÓN
    # -----------------------------------------------------------

    normalizada = _normalizar_declaracion(declaracion)

    # -----------------------------------------------------------
    # 8.3 — INCORPORACIÓN AL REGISTRO OPERATIVO
    # -----------------------------------------------------------

    _REGISTRO.append(normalizada)

    # -----------------------------------------------------------
    # 8.4 — RESULTADO DETERMINISTA
    # -----------------------------------------------------------

    return {
        "ok": True,
        "n": len(_REGISTRO),
        "declaracion": normalizada,
        "id": _ID,
    }


# ===============================================================
# FIN SECCIÓN 8
# ===============================================================

# ===============================================================
# SECCIÓN 9 — CAPACIDAD: RESOLVER
# ===============================================================
#
# Resuelve una declaración por su identificador.
#
# Esta capacidad:
#   - acepta cualquier id declarativo;
#   - consulta primero el registro operativo;
#   - permite resolución desde fuentes declarativas disponibles;
#   - no mantiene una lista cerrada de módulos;
#   - no modifica declaraciones;
#   - no calcula;
#   - no interpreta;
#   - no inventa enunciados;
#   - devuelve explícitamente si la declaración fue resuelta.
#
# La resolución es una operación documental.
#
# ===============================================================


def resolver(id_decl: str) -> Dict[str, Any]:
    """
    Resuelve una declaración mediante su identificador.

    Orden determinista de resolución:

        1. Registro operativo de CIT.
        2. Fuentes declarativas disponibles en el sistema.
        3. Declaración no resoluble.

    Entrada:
        id_decl:
            Identificador de la declaración.

    Salida resuelta:
        {
            "id": str,
            "resuelto": True,
            "declaracion": dict,
            "origen": str,
            "nota": str
        }

    Salida no resuelta:
        {
            "id": str,
            "resuelto": False,
            "declaracion": None,
            "nota": str
        }

    Garantías:
        - un id vacío nunca se considera resoluble;
        - no se inventa una declaración;
        - una declaración debe contener enunciado para considerarse
          resuelta desde el registro;
        - la resolución no modifica el conocimiento de origen;
        - la resolución no calcula resultados;
        - la resolución no interpreta declaraciones.
    """

    # -----------------------------------------------------------
    # 9.1 — VALIDACIÓN DETERMINISTA DEL IDENTIFICADOR
    # -----------------------------------------------------------

    if not isinstance(id_decl, str):
        return {
            "id": id_decl,
            "resuelto": False,
            "declaracion": None,
            "nota": "id inválido: debe ser str",
        }

    clave = id_decl.strip()

    if not clave:
        return {
            "id": id_decl,
            "resuelto": False,
            "declaracion": None,
            "nota": "id vacío",
        }

    # -----------------------------------------------------------
    # 9.2 — RESOLUCIÓN EN REGISTRO OPERATIVO
    # -----------------------------------------------------------

    for declaracion in _REGISTRO:
        if not isinstance(declaracion, dict):
            continue

        if declaracion.get("id") != clave:
            continue

        if not declaracion.get("enunciado"):
            continue

        return {
            "id": clave,
            "resuelto": True,
            "declaracion": declaracion,
            "origen": "registro_ciclo",
            "nota": (
                "resuelto desde el registro operativo de CIT"
            ),
        }

    # -----------------------------------------------------------
    # 9.3 — RESOLUCIÓN DESDE FUENTES DECLARATIVAS DISPONIBLES
    # -----------------------------------------------------------
    #
    # No se declara aquí un universo cerrado de módulos.
    # La fuente declarativa disponible determina qué puede
    # resolverse externamente.
    #
    # La ausencia de una fuente no convierte el id en una
    # declaración inventada.
    #

    try:
        from modules.citacion.fuentes import ax as fuente

        resultado = fuente.anunciar_id(
            clave,
            evidencia_ref="cit.resolver",
            registrar=False,
        )

        if isinstance(resultado, dict):
            if resultado.get("resuelto") and resultado.get("cita"):
                cita = resultado.get("cita")

                if isinstance(cita, dict):
                    declaracion = _normalizar_declaracion({
                        "id": clave,
                        "tipo": cita.get("tipo"),
                        "fuente": (
                            cita.get("fuente")
                            or cita.get("fuente_modulo")
                            or ""
                        ),
                        "enunciado": cita.get("enunciado"),
                        "descripcion": cita.get("descripcion"),
                        "evidencia_ref": cita.get("evidencia_ref"),
                        "o_ref": cita.get("o_ref"),
                        "contexto_ciclo": cita.get("contexto_ciclo"),
                        "relaciones": cita.get("relaciones"),
                    })

                    errores = _validar_declaracion(declaracion)

                    if not errores:
                        return {
                            "id": clave,
                            "resuelto": True,
                            "declaracion": declaracion,
                            "origen": "fuente_sistema",
                            "nota": (
                                "resuelto desde una fuente "
                                "declarativa disponible"
                            ),
                        }

    except Exception:
        pass

    # -----------------------------------------------------------
    # 9.4 — DECLARACIÓN NO RESUELTA
    # -----------------------------------------------------------

    return {
        "id": clave,
        "resuelto": False,
        "declaracion": None,
        "nota": (
            "sin declaración resoluble en el registro "
            "ni en las fuentes declarativas disponibles"
        ),
    }


# ===============================================================
# FIN SECCIÓN 9
# ===============================================================

# ===============================================================
# SECCIÓN 10 — CAPACIDAD: RESOLVER_ENUNCIADO
# ===============================================================
#
# Resolución orientada al enunciado de una declaración.
#
# Esta capacidad:
#   - recibe un identificador declarativo;
#   - delega la resolución primaria en resolver();
#   - no implementa una segunda lógica de resolución;
#   - no depende de módulos concretos;
#   - no inventa enunciados;
#   - no calcula;
#   - no interpreta;
#   - no modifica el registro;
#   - no modifica conocimiento de origen.
#
# Es una proyección determinista de resolver().
#
# ===============================================================


def resolver_enunciado(id_norma: str) -> Dict[str, Any]:
    """
    Resuelve una declaración y expone específicamente su enunciado.

    Entrada:
        id_norma:
            Identificador de la declaración que se desea resolver.

    Salida:
        {
            "id": str,
            "enunciado": str | None,
            "descripcion": str | None,
            "fuente": str | None,
            "fuente_modulo": str | None,
            "resuelto": bool,
            "nota": str | None
        }

    Garantías:
        - utiliza exactamente la lógica de resolver();
        - no crea una resolución paralela;
        - si resolver() no resuelve, enunciado es None;
        - nunca fabrica un enunciado;
        - conserva la procedencia declarada;
        - no altera el registro;
        - no altera la declaración resuelta.
    """

    # -----------------------------------------------------------
    # 10.1 — RESOLUCIÓN PRIMARIA
    # -----------------------------------------------------------

    resultado = resolver(id_norma)

    resuelto = bool(resultado.get("resuelto"))

    declaracion = resultado.get("declaracion")

    if not isinstance(declaracion, dict):
        declaracion = {}

    # -----------------------------------------------------------
    # 10.2 — PROYECCIÓN DETERMINISTA
    # -----------------------------------------------------------

    if resuelto:
        enunciado = declaracion.get("enunciado")
        descripcion = declaracion.get("descripcion")
        fuente = declaracion.get("fuente")
    else:
        enunciado = None
        descripcion = None
        fuente = None

    # -----------------------------------------------------------
    # 10.3 — SALIDA CANÓNICA
    # -----------------------------------------------------------

    return {
        "id": id_norma,
        "enunciado": enunciado,
        "descripcion": descripcion,
        "fuente": fuente,
        "fuente_modulo": fuente,
        "resuelto": resuelto,
        "nota": resultado.get("nota"),
    }


# ===============================================================
# FIN SECCIÓN 10
# ===============================================================

# ===============================================================
# SECCIÓN 11 — CAPACIDAD: BUSCAR
# ===============================================================
#
# Consulta determinista del registro declarativo operativo.
#
# Esta capacidad:
#   - consulta declaraciones ya registradas;
#   - acepta filtros declarativos genéricos;
#   - no conoce módulos concretos;
#   - no contiene una lista cerrada de fuentes;
#   - no resuelve mediante fuentes externas;
#   - no crea declaraciones;
#   - no modifica declaraciones;
#   - no calcula;
#   - no interpreta;
#   - no sustituye la autoridad del módulo fuente.
#
# Filtros soportados:
#   - id
#   - tipo
#   - fuente
#   - modulo (alias de fuente)
#   - o_ref
#   - texto
#
# ===============================================================


def buscar(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Consulta declaraciones del registro operativo de CIT.

    La operación es exclusivamente de lectura.

    Entrada:
        peticion:
            dict opcional con filtros.

    Salida:
        {
            "id": _ID,
            "declaraciones": [...],
            "n": int,
            "filtro": {...},
            "nota": str
        }

    Garantías:
        - None equivale determinísticamente a {};
        - una petición dict se copia antes de utilizarse;
        - únicamente se consultan declaraciones del registro;
        - el orden del registro se conserva;
        - no se modifica _REGISTRO;
        - no se modifica ninguna declaración;
        - no se incorporan declaraciones externas;
        - el resultado depende exclusivamente del registro y del filtro.
    """

    # -----------------------------------------------------------
    # 11.1 — NORMALIZACIÓN DETERMINISTA DE PETICIÓN
    # -----------------------------------------------------------

    if peticion is None:
        filtro: Dict[str, Any] = {}

    elif isinstance(peticion, dict):
        filtro = dict(peticion)

    else:
        return {
            "id": _ID,
            "declaraciones": [],
            "n": 0,
            "filtro": {},
            "ok": False,
            "errores": [
                "peticion debe ser dict o None"
            ],
            "nota": (
                "La búsqueda requiere una petición dict "
                "o None."
            ),
        }

    # -----------------------------------------------------------
    # 11.2 — CONJUNTO INICIAL
    # -----------------------------------------------------------
    #
    # Se conserva exactamente el orden operativo del registro.
    #

    resultado: List[Dict[str, Any]] = list(_REGISTRO)

    # -----------------------------------------------------------
    # 11.3 — FILTRO POR ID
    # -----------------------------------------------------------

    id_filtro = filtro.get("id")

    if id_filtro not in (None, ""):
        resultado = [
            declaracion
            for declaracion in resultado
            if declaracion.get("id") == id_filtro
        ]

    # -----------------------------------------------------------
    # 11.4 — FILTRO POR TIPO
    # -----------------------------------------------------------

    tipo_filtro = filtro.get("tipo")

    if tipo_filtro not in (None, ""):
        resultado = [
            declaracion
            for declaracion in resultado
            if declaracion.get("tipo") == tipo_filtro
        ]

    # -----------------------------------------------------------
    # 11.5 — FILTRO POR FUENTE
    # -----------------------------------------------------------
    #
    # "modulo" permanece como alias compatible de "fuente".
    #

    fuente_filtro = (
        filtro.get("fuente")
        or filtro.get("modulo")
    )

    if fuente_filtro not in (None, ""):
        resultado = [
            declaracion
            for declaracion in resultado
            if (
                declaracion.get("fuente") == fuente_filtro
                or declaracion.get("fuente_modulo") == fuente_filtro
            )
        ]

    # -----------------------------------------------------------
    # 11.6 — FILTRO POR O_REF
    # -----------------------------------------------------------

    o_ref_filtro = filtro.get("o_ref")

    if o_ref_filtro not in (None, ""):
        resultado = [
            declaracion
            for declaracion in resultado
            if declaracion.get("o_ref") == o_ref_filtro
        ]

    # -----------------------------------------------------------
    # 11.7 — FILTRO POR TEXTO
    # -----------------------------------------------------------
    #
    # La búsqueda textual es una coincidencia de subcadena
    # sin distinción entre mayúsculas y minúsculas.
    #
    # Se consulta únicamente:
    #   - enunciado
    #   - descripcion
    #

    texto_filtro = filtro.get("texto")

    if texto_filtro not in (None, ""):
        texto = str(texto_filtro).lower()

        resultado = [
            declaracion
            for declaracion in resultado
            if (
                texto in str(
                    declaracion.get("enunciado") or ""
                ).lower()
                or
                texto in str(
                    declaracion.get("descripcion") or ""
                ).lower()
            )
        ]

    # -----------------------------------------------------------
    # 11.8 — SALIDA DETERMINISTA
    # -----------------------------------------------------------

    return {
        "id": _ID,
        "ok": True,
        "declaraciones": resultado,
        "n": len(resultado),
        "filtro": filtro,
        "nota": (
            "Consulta de lectura sobre el registro operativo "
            "de CIT. Sin recálculo y sin modificación."
        ),
    }


# ===============================================================
# FIN SECCIÓN 11
# ===============================================================
# ===============================================================
# SECCIÓN 12 — CAPACIDAD: CADENA
# ===============================================================
#
# Construcción determinista de una cadena de fundamentación.
#
# Esta capacidad:
#   - recibe una secuencia ordenada de ids;
#   - resuelve cada id mediante resolver();
#   - conserva el orden recibido;
#   - no inventa nodos;
#   - identifica explícitamente los faltantes;
#   - no calcula;
#   - no interpreta;
#   - no modifica el registro;
#   - no modifica conocimiento de origen;
#   - no conoce módulos concretos.
#
# ===============================================================


def cadena(
    ids: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Construye una cadena documental a partir de ids resolubles.

    Entrada:
        ids:
            Lista ordenada de identificadores declarativos.

    Salida:
        {
            "id": _ID,
            "cadena": [...],
            "n": int,
            "faltantes": [...],
            "completa": bool,
            "nota": str
        }

    Reglas deterministas:

        1. None equivale a una secuencia vacía.
        2. Una lista se procesa exactamente en su orden.
        3. Cada elemento se convierte a str antes de resolverlo.
        4. Un elemento resoluble entra en la cadena.
        5. Un elemento no resoluble entra en faltantes.
        6. No se generan nodos sustitutos.
        7. La cadena es completa únicamente cuando:
              - no existen faltantes;
              - existe al menos un eslabón.
        8. La operación no modifica el registro.
    """

    # -----------------------------------------------------------
    # 12.1 — NORMALIZACIÓN DE ENTRADA
    # -----------------------------------------------------------

    if ids is None:
        secuencia: List[Any] = []

    elif isinstance(ids, list):
        secuencia = list(ids)

    else:
        return {
            "id": _ID,
            "cadena": [],
            "n": 0,
            "faltantes": [],
            "completa": False,
            "ok": False,
            "errores": [
                "ids debe ser list o None"
            ],
            "nota": (
                "La cadena requiere una secuencia de "
                "identificadores."
            ),
        }

    # -----------------------------------------------------------
    # 12.2 — RESOLUCIÓN ORDENADA
    # -----------------------------------------------------------

    eslabones: List[Dict[str, Any]] = []
    faltantes: List[str] = []

    for elemento in secuencia:
        clave = str(elemento).strip()

        if not clave:
            faltantes.append(clave)
            continue

        resultado = resolver(clave)

        if resultado.get("resuelto") is True:
            declaracion = resultado.get("declaracion")

            if isinstance(declaracion, dict):
                eslabones.append(declaracion)
            else:
                faltantes.append(clave)
        else:
            faltantes.append(clave)

    # -----------------------------------------------------------
    # 12.3 — DETERMINACIÓN DE COMPLETITUD
    # -----------------------------------------------------------

    completa = (
        len(faltantes) == 0
        and len(eslabones) > 0
    )

    # -----------------------------------------------------------
    # 12.4 — SALIDA CANÓNICA
    # -----------------------------------------------------------

    return {
        "id": _ID,
        "ok": True,
        "cadena": eslabones,
        "n": len(eslabones),
        "faltantes": faltantes,
        "completa": completa,
        "nota": (
            "Cadena normativa documental. "
            "Solo contiene declaraciones resolubles; "
            "sin recálculo ni modificación."
        ),
    }


# ===============================================================
# FIN SECCIÓN 12
# ===============================================================
# ===============================================================
# SECCIÓN 13 — CAPACIDAD: EXPLICAR
# ===============================================================
#
# Explicación documental determinista de declaraciones existentes.
#
# Esta capacidad:
#   - recibe una petición declarativa genérica;
#   - puede utilizar filtros de buscar();
#   - puede construir una cadena mediante cadena();
#   - únicamente expone declaraciones existentes;
#   - no interpreta semánticamente el contenido;
#   - no calcula;
#   - no inventa premisas;
#   - no conoce módulos concretos;
#   - no modifica el registro;
#   - no modifica conocimiento de origen.
#
# ===============================================================


def explicar(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Construye una explicación documental a partir de declaraciones
    existentes.

    Entrada:
        peticion:
            dict opcional.

            Puede contener:
                - ids
                - cadena
                - id
                - tipo
                - fuente
                - modulo
                - o_ref
                - texto

    Reglas:

        1. None equivale determinísticamente a {}.
        2. Si existe "ids" o "cadena", se construye una cadena
           mediante cadena().
        3. Si no existe una secuencia explícita, se utiliza buscar().
        4. Toda declaración expuesta debe existir previamente o
           ser resoluble mediante la lógica declarativa de CIT.
        5. No se crean declaraciones.
        6. No se recalculan resultados.
        7. No se interpreta el contenido de las declaraciones.
        8. La explicación es completa únicamente cuando la fuente
           documental utilizada es completa.
    """

    # -----------------------------------------------------------
    # 13.1 — NORMALIZACIÓN DE PETICIÓN
    # -----------------------------------------------------------

    if peticion is None:
        filtro: Dict[str, Any] = {}

    elif isinstance(peticion, dict):
        filtro = dict(peticion)

    else:
        return {
            "id": _ID,
            "explicacion": [],
            "n": 0,
            "faltantes": [],
            "completa": False,
            "ok": False,
            "errores": [
                "peticion debe ser dict o None"
            ],
            "nota": (
                "La explicación requiere una petición "
                "dict o None."
            ),
        }

    # -----------------------------------------------------------
    # 13.2 — RESOLUCIÓN DE SECUENCIA EXPLÍCITA
    # -----------------------------------------------------------
    #
    # "ids" tiene prioridad sobre "cadena" cuando ambos existen.
    #

    ids = filtro.get("ids")

    if ids is None:
        ids = filtro.get("cadena")

    if ids is not None:

        if isinstance(ids, str):
            ids = [ids]

        elif not isinstance(ids, list):
            return {
                "id": _ID,
                "explicacion": [],
                "n": 0,
                "faltantes": [],
                "completa": False,
                "ok": False,
                "errores": [
                    "ids/cadena debe ser list o str"
                ],
                "nota": (
                    "La secuencia documental debe ser "
                    "una lista o un identificador."
                ),
            }

        # -------------------------------------------------------
        # 13.2.1 — CONSTRUCCIÓN DE CADENA
        # -------------------------------------------------------

        resultado_cadena = cadena(list(ids))

        explicacion = resultado_cadena.get("cadena") or []
        faltantes = resultado_cadena.get("faltantes") or []

        return {
            "id": _ID,
            "ok": True,
            "explicacion": explicacion,
            "n": len(explicacion),
            "faltantes": faltantes,
            "completa": bool(
                resultado_cadena.get("completa")
            ),
            "nota": (
                "Explicación documental construida a partir "
                "de declaraciones resolubles."
            ),
        }

    # -----------------------------------------------------------
    # 13.3 — EXPLICACIÓN MEDIANTE BÚSQUEDA
    # -----------------------------------------------------------

    resultado_busqueda = buscar(filtro)

    if resultado_busqueda.get("ok") is False:
        return {
            "id": _ID,
            "explicacion": [],
            "n": 0,
            "faltantes": [],
            "completa": False,
            "ok": False,
            "errores": (
                resultado_busqueda.get("errores") or []
            ),
            "nota": (
                "No fue posible obtener las declaraciones "
                "documentales solicitadas."
            ),
        }

    declaraciones = (
        resultado_busqueda.get("declaraciones") or []
    )

    # -----------------------------------------------------------
    # 13.4 — DETERMINACIÓN DE COMPLETITUD
    # -----------------------------------------------------------

    completa = len(declaraciones) > 0

    # -----------------------------------------------------------
    # 13.5 — SALIDA CANÓNICA
    # -----------------------------------------------------------

    return {
        "id": _ID,
        "ok": True,
        "explicacion": declaraciones,
        "n": len(declaraciones),
        "faltantes": [],
        "completa": completa,
        "nota": (
            "Explicación = declaraciones existentes. "
            "CIT documenta; no calcula ni interpreta."
        ),
    }


# ===============================================================
# FIN SECCIÓN 13
# ===============================================================

# ===============================================================
# SECCIÓN 8 — EJECUCIÓN TOTAL CALLABLE
# ===============================================================

def ejecutar_total(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Ejecuta determinísticamente todas las capacidades callable
    declaradas por CIT.

    Regla fundamental:
        CONTENEDOR["capacidades"] = autoridad declarativa.
        Cada nombre debe resolver a un callable real.

    ejecutar_total no se invoca a sí misma.
    No inventa capacidades.
    No elimina capacidades declaradas.
    No modifica CONTENEDOR.
    No modifica el contrato.
    """

    pet = peticion if isinstance(peticion, dict) else {}

    capacidades_declaradas = list(
        CONTENEDOR.get("capacidades", {}).keys()
    )

    resultados: Dict[str, Any] = {}
    capacidades_ejecutadas: List[str] = []
    errores_ejecucion: List[Dict[str, Any]] = []

    # -----------------------------------------------------------
    # 8.1 — RESOLUCIÓN CONTRACTUAL DE CALLABLES
    # -----------------------------------------------------------

    for nombre in capacidades_declaradas:

        # ejecutar_total no puede ejecutarse recursivamente.
        if nombre == "ejecutar_total":
            continue

        callable_obj = CONTENEDOR["capacidades"].get(nombre)

        if not callable(callable_obj):
            errores_ejecucion.append({
                "capacidad": nombre,
                "error": "capacidad declarada no resoluble a callable",
            })
            continue

        # -------------------------------------------------------
        # 8.1.1 — INVOCACIÓN DETERMINISTA
        # -------------------------------------------------------

        try:
            if nombre in (
                "verificar",
                "barrer",
                "inventario",
                "reporte",
                "diagnostico",
                "anunciar",
                "anunciar_todo",
                "buscar",
                "citar",
                "resolver_enunciado",
                "explicar",
                "cadena",
                "limpiar_ciclo",
                "evaluar",
                "inspeccionar",
                "registrar_inventario",
            ):
                resultado = callable_obj(pet)

            elif nombre == "verificar_salida":
                resultado = callable_obj(pet.get("salida"))

            elif nombre == "registrar":
                resultado = callable_obj(
                    pet.get("declaracion")
                )

            elif nombre == "resolver":
                resultado = callable_obj(
                    pet.get("id")
                )

            elif nombre == "relacionar":
                resultado = callable_obj(
                    pet.get("id_a"),
                    pet.get("relacion"),
                    pet.get("id_b"),
                )

            else:
                errores_ejecucion.append({
                    "capacidad": nombre,
                    "error": "firma callable no definida contractualmente",
                })
                continue

            resultados[nombre] = resultado
            capacidades_ejecutadas.append(nombre)

        except Exception as exc:
            errores_ejecucion.append({
                "capacidad": nombre,
                "error": "{0}: {1}".format(
                    type(exc).__name__,
                    exc,
                ),
            })

    # -----------------------------------------------------------
    # 8.2 — ESTADO DETERMINISTA
    # -----------------------------------------------------------

    coherente = (
        len(errores_ejecucion) == 0
        and all(
            nombre != "ejecutar_total"
            for nombre in capacidades_ejecutadas
        )
    )

    estado = "OK" if coherente else "DEGRADADO"

    # -----------------------------------------------------------
    # 8.3 — SALIDA CONTRACTUAL
    # -----------------------------------------------------------

    return {
        "id": _ID,
        "modulo": _NOMBRE,
        "rol": _ROL,
        "version": _VERSION,
        "operacion": "ejecutar_total",
        "estado": estado,
        "coherente": coherente,
        "capacidades_ejecutadas": capacidades_ejecutadas,
        "errores_ejecucion": errores_ejecucion,
        "resultados": resultados,
        "capacidades_declaradas": capacidades_declaradas,
    }

# ===============================================================
# 3.15.20 — INSPECCIONAR
# ===============================================================
#
# Inspección estructural determinista de CIT.
#
# No ejecuta capacidades.
# No modifica conocimiento.
# No modifica contrato.
# No depende de una lista cerrada de módulos.
#
# La fuente de verdad es CONTENEDOR.
#
# ===============================================================

def inspeccionar(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Expone el estado estructural y contractual de CIT.

    Verifica la correspondencia entre:
        capacidades declaradas
        capacidades_meta
        callables reales

    No ejecuta las capacidades inspeccionadas.
    """

    capacidades = CONTENEDOR.get("capacidades", {})
    capacidades_meta = CONTENEDOR.get("capacidades_meta", {})

    errores: List[str] = []
    advertencias: List[str] = []

    capacidades_contractuales = list(capacidades.keys())
    capacidades_meta_declaradas = list(capacidades_meta.keys())

    # -----------------------------------------------------------
    # 3.15.20.1 — RESOLUCIÓN DE CAPACIDADES
    # -----------------------------------------------------------

    resolubles: List[str] = []
    no_resolubles: List[str] = []

    for nombre in capacidades_contractuales:
        callable_obj = capacidades.get(nombre)

        if callable(callable_obj):
            resolubles.append(nombre)
        else:
            no_resolubles.append(nombre)
            errores.append(
                "capacidad no resoluble a callable: {0}".format(nombre)
            )

    # -----------------------------------------------------------
    # 3.15.20.2 — CORRESPONDENCIA CAPACIDAD / META
    # -----------------------------------------------------------

    sin_meta = [
        nombre
        for nombre in capacidades_contractuales
        if nombre not in capacidades_meta
    ]

    metas_sin_capacidad = [
        nombre
        for nombre in capacidades_meta_declaradas
        if nombre not in capacidades
    ]

    for nombre in sin_meta:
        errores.append(
            "capacidad sin capacidades_meta: {0}".format(nombre)
        )

    for nombre in metas_sin_capacidad:
        errores.append(
            "capacidades_meta sin capacidad declarada: {0}".format(nombre)
        )

    # -----------------------------------------------------------
    # 3.15.20.3 — INTEGRIDAD ESTRUCTURAL
    # -----------------------------------------------------------

    integridad = {
        "capacidades_declaradas": len(capacidades_contractuales),
        "capacidades_resolubles": len(resolubles),
        "capacidades_no_resolubles": len(no_resolubles),
        "capacidades_meta": len(capacidades_meta_declaradas),
        "sin_meta": sin_meta,
        "metas_sin_capacidad": metas_sin_capacidad,
        "orden_capacidades": capacidades_contractuales,
        "orden_capacidades_meta": capacidades_meta_declaradas,
        "completa": (
            not no_resolubles
            and not sin_meta
            and not metas_sin_capacidad
        ),
    }

    # -----------------------------------------------------------
    # 3.15.20.4 — ESTADO
    # -----------------------------------------------------------

    coherente = not errores

    estado = "OPERATIVO" if coherente else "DEGRADADO"

    # -----------------------------------------------------------
    # 3.15.20.5 — SALIDA CONTRACTUAL
    # -----------------------------------------------------------

    return {
        "id": _ID,
        "modulo": _NOMBRE,
        "rol": _ROL,
        "version": _VERSION,
        "operacion": "inspeccionar",
        "estado": estado,
        "coherente": coherente,
        "constantes": {
            "_ID": _ID,
            "_NOMBRE": _NOMBRE,
            "_ROL": _ROL,
            "_VERSION": _VERSION,
            "_VERSION_CONTRATO": _VERSION_CONTRATO,
            "_ESQUEMA": _ESQUEMA,
            "_ESTABILIDAD": _ESTABILIDAD,
            "_COMPATIBLE_DESDE": _COMPATIBLE_DESDE,
            "_API_ENGINE": _API_ENGINE,
        },
        "capacidades_contractuales": capacidades_contractuales,
        "capacidades_meta": capacidades_meta_declaradas,
        "capacidades_resolubles": resolubles,
        "capacidades_no_resolubles": no_resolubles,
        "integridad": integridad,
        "esquema": CONTENEDOR.get("esquema"),
        "autoriza_engine": CONTENEDOR.get("autoriza_engine"),
        "reporting": CONTENEDOR.get("reporting"),
        "invariantes": CONTENEDOR.get("invariantes"),
        "errores": errores,
        "advertencias": advertencias,
    }
# ===============================================================
# 3.15.21 — REGISTRAR INVENTARIO
# ===============================================================
#
# Registra una instantánea determinista del inventario estructural
# de CIT.
#
# REGLAS:
#
#   1. La fuente de verdad es CONTENEDOR.
#   2. No modifica el contrato.
#   3. No modifica el conocimiento declarado.
#   4. No ejecuta capacidades ajenas.
#   5. No depende de módulos concretos.
#   6. El inventario registrado corresponde exactamente al estado
#      contractual observado en el momento de la operación.
#
# ===============================================================

def registrar_inventario(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Registra una instantánea determinista del inventario contractual
    y estructural de CIT.

    La operación no altera CONTENEDOR ni el conocimiento declarado.
    """

    # -----------------------------------------------------------
    # 3.15.21.1 — CAPTURA DEL INVENTARIO
    # -----------------------------------------------------------

    capacidades = CONTENEDOR.get("capacidades", {})
    capacidades_meta = CONTENEDOR.get("capacidades_meta", {})

    capacidades_declaradas = list(capacidades.keys())

    capacidades_resolubles = [
        nombre
        for nombre, callable_obj in capacidades.items()
        if callable(callable_obj)
    ]

    capacidades_no_resolubles = [
        nombre
        for nombre in capacidades_declaradas
        if nombre not in capacidades_resolubles
    ]

    metas_sin_capacidad = [
        nombre
        for nombre in capacidades_meta.keys()
        if nombre not in capacidades
    ]

    capacidades_sin_meta = [
        nombre
        for nombre in capacidades_declaradas
        if nombre not in capacidades_meta
    ]

    # -----------------------------------------------------------
    # 3.15.21.2 — INTEGRIDAD DEL INVENTARIO
    # -----------------------------------------------------------

    integridad = (
        not capacidades_no_resolubles
        and not metas_sin_capacidad
        and not capacidades_sin_meta
    )

    inventario_registrado = {
        "id": _ID,
        "nombre": _NOMBRE,
        "rol": _ROL,
        "version": _VERSION,
        "version_contrato": _VERSION_CONTRATO,
        "esquema": _ESQUEMA,
        "estabilidad": _ESTABILIDAD,
        "compatible_desde": _COMPATIBLE_DESDE,
        "api_engine": _API_ENGINE,
        "tipos_declaracion": list(TIPOS_DECLARACION),
        "relaciones": list(RELACIONES),
        "campos_obligatorios": list(CAMPOS_OBLIGATORIOS),
        "campos_opcionales": list(CAMPOS_OPCIONALES),
        "capacidades_declaradas": capacidades_declaradas,
        "capacidades_resolubles": capacidades_resolubles,
        "capacidades_no_resolubles": capacidades_no_resolubles,
        "capacidades_meta": list(capacidades_meta.keys()),
        "capacidades_sin_meta": capacidades_sin_meta,
        "metas_sin_capacidad": metas_sin_capacidad,
        "integridad": integridad,
    }

    # -----------------------------------------------------------
    # 3.15.21.3 — RESULTADO CONTRACTUAL
    # -----------------------------------------------------------

    return {
        "id": _ID,
        "operacion": "registrar_inventario",
        "registrado": True,
        "inventario": inventario_registrado,
        "nota": (
            "Instantánea determinista del inventario estructural "
            "de CIT. No modifica contrato ni conocimiento declarado."
        ),
    }

# ===============================================================
# SECCIÓN 8 — INTEGRIDAD CONTRACTUAL DE CAPACIDADES
# ===============================================================

def _verificar_capacidades_contractuales() -> Dict[str, Any]:
    """
    Verifica la correspondencia exacta entre:

        CONTENEDOR["capacidades"]
        CONTENEDOR["capacidades_meta"]
        callable real

    No ejecuta capacidades.
    No modifica el contrato.
    """

    capacidades = CONTENEDOR.get("capacidades", {})
    metas = CONTENEDOR.get("capacidades_meta", {})

    declaradas = list(capacidades.keys())
    declaradas_meta = list(metas.keys())

    sin_meta = [
        nombre
        for nombre in declaradas
        if nombre not in metas
    ]

    meta_sin_capacidad = [
        nombre
        for nombre in declaradas_meta
        if nombre not in capacidades
    ]

    no_callable = [
        nombre
        for nombre, callable_obj in capacidades.items()
        if not callable(callable_obj)
    ]

    orden_meta_incorrecto = (
        declaradas != declaradas_meta
    )

    errores: List[str] = []

    if sin_meta:
        errores.append(
            "capacidades sin capacidades_meta: {0}".format(
                sin_meta
            )
        )

    if meta_sin_capacidad:
        errores.append(
            "capacidades_meta sin capacidad: {0}".format(
                meta_sin_capacidad
            )
        )

    if no_callable:
        errores.append(
            "capacidades no resolubles a callable: {0}".format(
                no_callable
            )
        )

    if orden_meta_incorrecto:
        errores.append(
            "el orden de capacidades y capacidades_meta no coincide"
        )

    return {
        "id": _ID,
        "coherente": not errores,
        "capacidades": declaradas,
        "capacidades_meta": declaradas_meta,
        "sin_meta": sin_meta,
        "meta_sin_capacidad": meta_sin_capacidad,
        "no_callable": no_callable,
        "orden_coherente": not orden_meta_incorrecto,
        "errores": errores,
    }

# ===============================================================
# SECCIÓN 9 — EXPORTS
# ===============================================================

__all__ = [
    "CONTENEDOR",
    "TIPOS_DECLARACION",
    "RELACIONES",
    "CAMPOS_OBLIGATORIOS",
    "CAMPOS_OPCIONALES",

    "registrar",
    "resolver",
    "resolver_enunciado",
    "buscar",
    "citar",

    "anunciar",
    "anunciar_todo",

    "cadena",
    "explicar",
    "relacionar",

    "limpiar_ciclo",

    "inventario",
    "reporte",
    "diagnostico",
    "barrer",
    "verificar",
    "verificar_salida",

    "evaluar",

    "ejecutar_total",
    "inspeccionar",
    "registrar_inventario",
]







