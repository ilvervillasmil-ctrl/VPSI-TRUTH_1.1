# ===============================================================
# VPSI-TRUTH — modules/verificacion/__init__.py
# ===============================================================
#
# MÓDULO:              verificacion
# ID:                  VX
# Rol:                 VX
# Versión módulo:      2.0
# Versión contrato:    1.0
# Esquema contrato:    VPSI-CONTRACT-1.0
# Estabilidad:         ESTABLE
# Compatible desde:    1.0
# API Engine:          >=1.0
#
# ---------------------------------------------------------------
# JURISDICCIÓN
# ---------------------------------------------------------------
#
# Autoridad exclusiva de verificación estructural.
#
# Jurisdicción: cualquier estructura susceptible de contrastarse
# contra reglas formales, por ejemplo:
#   - código
#   - contratos
#   - módulos
#   - configuraciones
#   - salidas
#   - estructuras
#   - grafos / árboles
#   - futuras representaciones
#
# Hoy el algoritmo operativo verifica código vía AuditorAxiomatico.
# Mañana podrá verificar más tipos de estructuras sin cambiar
# la responsabilidad del módulo ni su API pública.
#
# ---------------------------------------------------------------
# OFICIO ÚNICO
# ---------------------------------------------------------------
#
# Determinar si una estructura satisface o viola un conjunto
# de reglas formales.
#
# No interpreta intención.
# No calcula Tru.
# No toma decisiones.
# No corrige.
# No modifica.
# No ejecuta.
# Solo verifica. Solo produce evidencia.
#
# ---------------------------------------------------------------
# SEPARACIÓN DE AUTORIDADES
# ---------------------------------------------------------------
#
# VX produce evidencia de verificación.
# Diagnóstico decide qué hacer con ella (si Engine se la entrega).
# AX es la única autoridad del conocimiento axiomático.
#
# VX nunca conoce la implementación de Diagnóstico.
# VX nunca sustituye a AX.
# VX nunca sustituye a Diagnóstico.
#
# Secuencia correcta:
#
#   Engine decide verificar
#        ↓
#   Engine invoca VX.verificar / VX.barrer
#        ↓
#   VX produce evidencia estructurada
#        ↓
#   Engine decide si deposita / envía a Diagnóstico
#
# ---------------------------------------------------------------
# AX Y CONOCIMIENTO
# ---------------------------------------------------------------
#
# Las declaraciones oficiales viven únicamente en AX.
# VX puede consumir axiomas que Engine le entregue.
# axiomas() se mantiene solo como alias de compatibilidad
# temporal; no es un repositorio de conocimiento.
#
# ===============================================================

# ===============================================================
# PARTE 1 — PRINCIPIOS, BANDERAS Y ESPECIFICACIONES PRECISAS
# ===============================================================

# ===============================================================
# 1.1 — IMPORTACIONES
# ===============================================================

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .auditor import AuditorAxiomatico

# ===============================================================
# FIN 1.1
# ===============================================================


# ===============================================================
# 1.2 — IDENTIDAD
# ===============================================================

ID_MODULO = "VX"
NOMBRE_MODULO = "verificacion"
ROL_MODULO = "VX"

# Alias de compatibilidad con el init previo
_ID = ID_MODULO
_NOMBRE = NOMBRE_MODULO
_ROL = ROL_MODULO

# ===============================================================
# FIN 1.2
# ===============================================================


# ===============================================================
# 1.3 — VERSIONES Y ESTABILIDAD
# ===============================================================

VERSION_MODULO = "2.0"
VERSION_CONTRATO = "1.0"
ESQUEMA_CONTRATO = "VPSI-CONTRACT-1.0"
COMPATIBLE_DESDE = "1.0"
API_ENGINE = ">=1.0"
ESTABILIDAD = "ESTABLE"

# Alias de compatibilidad
_VERSION = VERSION_MODULO
_VERSION_CONTRATO = VERSION_CONTRATO
_ESQUEMA = ESQUEMA_CONTRATO
_ESTABILIDAD = ESTABILIDAD
_COMPATIBLE_DESDE = COMPATIBLE_DESDE
_API_ENGINE = API_ENGINE

# ===============================================================
# FIN 1.3
# ===============================================================


# ===============================================================
# 1.4 — BANDERAS DE ESTADO
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
# FIN 1.4
# ===============================================================


# ===============================================================
# 1.5 — INVARIANTES
# ===============================================================

INVARIANTES = (
    "el id del módulo nunca cambia",
    "el rol nunca cambia",
    "VX nunca modifica la estructura auditada",
    "VX nunca corrige evidencia",
    "VX nunca interpreta intención",
    "VX nunca calcula métricas de verdad (C/L/K/Tru)",
    "VX solo produce evidencia verificable",
    "VX no deposita en Diagnóstico; Engine decide el destino de la evidencia",
    "VX no declara conocimiento axiomático oficial (AX es la autoridad)",
    "las capacidades declaradas son callables tras la resolución",
    "este módulo no modifica el estado de otros módulos",
    "este módulo no inventa capacidades no declaradas en CONTENEDOR",
    "este módulo siempre puede reportar su propio estado",
    "inventario() siempre incluye id, nombre, rol, version del CONTENEDOR",
)

# ===============================================================
# FIN 1.5
# ===============================================================

# ===============================================================
# FIN PARTE 1
# ===============================================================


# ===============================================================
# PARTE 4 — DEFINICIONES
# ===============================================================

# ===============================================================
# 4.1 — EXCEPCIONES
# ===============================================================

class ContratoInvalido(Exception):
    """El CONTENEDOR no cumple el esquema o la resolución falló."""
    pass

# ===============================================================
# FIN 4.1
# ===============================================================

# ===============================================================
# FIN PARTE 4
# ===============================================================


# ===============================================================
# PARTE 5 — CONTRATO OFICIAL (CONTENEDOR)
# ===============================================================

CONTENEDOR: Dict[str, Any] = {

    # ============================================================
    # 5.1 — ESQUEMA
    # ============================================================
    "esquema": ESQUEMA_CONTRATO,
    "version_contrato": VERSION_CONTRATO,
    "version_modulo": VERSION_MODULO,
    "estabilidad": ESTABILIDAD,
    "compatible_desde": COMPATIBLE_DESDE,
    "api_engine": API_ENGINE,

    # ============================================================
    # 5.2 — IDENTIDAD
    # ============================================================
    "id": ID_MODULO,
    "nombre": NOMBRE_MODULO,
    "rol": ROL_MODULO,
    "descripcion": (
        "Autoridad exclusiva de verificación estructural. "
        "Determina si una estructura satisface o viola un conjunto "
        "de reglas formales. Jurisdicción: código, contratos, módulos, "
        "configuraciones, salidas, estructuras, grafos y futuras "
        "representaciones. Solo produce evidencia verificable. "
        "No interpreta, no calcula Tru, no decide, no corrige, "
        "no modifica, no ejecuta. No sustituye a AX ni a Diagnóstico."
    ),

    # ============================================================
    # 5.3 — PROPÓSITO
    # ============================================================
    "funcion": (
        "Contrastar estructuras contra reglas formales y generar "
        "evidencia de verificación. El algoritmo operativo actual "
        "usa AuditorAxiomatico sobre código; la responsabilidad del "
        "módulo admite cualquier estructura formal sin cambiar la API."
    ),
    "no_hace": [
        "No interpreta intención",
        "No calcula C",
        "No calcula L",
        "No calcula K",
        "No calcula Tru",
        "No modifica estructuras auditadas",
        "No corrige implementaciones",
        "No toma decisiones",
        "No ejecuta acciones",
        "No deposita en Diagnóstico",
        "No sustituye a AX",
        "No sustituye a Diagnóstico",
        "No declara conocimiento axiomático oficial",
    ],

    # ============================================================
    # 5.4 — AUTORIDAD
    # ============================================================
    "autoridad": [
        "Verificar estructuras",
        "Contrastar estructuras contra reglas formales",
        "Reportar inconsistencias estructurales",
        "Generar evidencia de verificación",
        "Reportar su estado",
        "Reportar inventario",
        "Reportar diagnóstico propio",
    ],

    # ============================================================
    # 5.5 — CONOCIMIENTO EXPORTABLE
    # ============================================================
    "conocimiento_exportable": [
        "verificar",
        "barrer",
        "inventario",
        "reporte",
        "diagnostico",
        "verificar_salida",
        "axiomas",
        "evidencia",
        "ejecutar_total",
        "inspeccionar",
        "registrar_inventario",
    ],

    # ============================================================
    # 5.6 — ACCESO
    # ============================================================
    "acceso": {
        "nivel": "completo",
        "descripcion": "Acceso total a recursos del módulo",
    },

    # ============================================================
    # 5.7 — DEPENDENCIAS
    # ============================================================
    "requiere": [
        "CE", "AX", "FO", "MC", "SF",
        "CA", "CX", "DI", "RE",
        "TX", "CH", "CIT", "DGCO", "UI",
        "CC", "TT", "SC", "CT",
    ],

    # ============================================================
    # 5.8 — ACCESO A ARCHIVOS
    # ============================================================
    "acceso_archivos": ["*"],

    # ============================================================
    # 5.9 — VALIDAR ESQUEMA
    # ============================================================
    "validar_esquema": ["*"],

    # ============================================================
    # 5.10 — AUTORIZACIÓN AL ENGINE
    # ============================================================
    "autoriza_engine": {
        # --- PERMISOS BASE ---
        "leer": True,
        "ejecutar": True,
        "consultar": True,
        "recombinar": True,
        "reportar": True,
        "auditar": True,
        "inventariar": True,

        # --- PERMISOS DE ESCRITURA ---
        "alterar": False,
        "crear": True,
        "actualizar": False,

        # --- PERMISOS DE PROCESAMIENTO ---
        "validar": True,
        "procesar": True,
        "analizar": True,
        "generar": True,

        # --- PERMISOS DE DATOS ---
        "exportar": True,
        "importar": True,
        "respaldar": True,
        "recuperar": True,
        "sincronizar": True,

        # --- PERMISOS DE MONITOREO ---
        "monitorear": True,
        "metricas": True,
        "diagnostico": True,

        # --- PERMISOS DE ESTADO ---
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

        # --- PERMISOS OBLIGATORIOS ---
        "validar_esquema": True,
        "acceso_archivos": True,

        # --- BANDERAS NUEVAS (OBLIGATORIAS ENGINE) ---
        "ejecutar_total": True,
        "inspeccionar": True,
        "registrar_inventario": True,
    },

    # ============================================================
    # 5.11 — CONSULTAS SOPORTADAS
    # ============================================================
    "consultas_soportadas": [
        # --- CENTINELA ---
        "verificar_estructura",
        "barrer",
        "verificar_salida",

        # --- INVENTARIO Y REPORTING ---
        "obtener_inventario",
        "obtener_reporte",
        "obtener_diagnostico",

        # --- CAPACIDADES ARQUITECTÓNICAS ---
        "ejecutar_total",
        "inspeccionar",
        "registrar_inventario",
    ],

    # ============================================================
    # 5.12 — CAPACIDADES
    # ============================================================
    "capacidades": {
        # --- CENTINELA ---
        "verificar": "verificar",
        "barrer": "barrer",
        "verificar_salida": "verificar_salida",

        # --- COMPATIBILIDAD ---
        "axiomas": "axiomas",

        # --- INVENTARIO Y REPORTING ---
        "inventario": "inventario",
        "reporte": "reporte",
        "diagnostico": "diagnostico",

        # --- CAPACIDADES ARQUITECTÓNICAS (OBLIGATORIAS ENGINE) ---
        "ejecutar_total": "ejecutar_total",
        "inspeccionar": "inspeccionar",
        "registrar_inventario": "registrar_inventario",
    },

    # ============================================================
    # 5.13 — METADATOS DE CAPACIDADES (1:1 OBLIGATORIO)
    # ============================================================
    "capacidades_meta": {
        "verificar": {
            "descripcion": (
                "Verifica una estructura contra reglas formales. "
                "Produce evidencia. No interpreta ni corrige."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con id, coherente, errores, evidencia, detalle"
            ),
            "acceso_archivos": ["*"],
        },
        "barrer": {
            "descripcion": (
                "Alias de verificar. Centinela de coherencia estructural."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con id, coherente, errores, evidencia, detalle"
            ),
            "acceso_archivos": ["*"],
        },
        "inventario": {
            "descripcion": (
                "Inventario contractual del módulo VX."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con id, nombre, rol, version, version_contrato, "
                "esquema, estabilidad, capacidades, jurisdiccion"
            ),
            "acceso_archivos": ["*"],
        },
        "reporte": {
            "descripcion": (
                "Reporte interno de estado de VX."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con id, estado, coherente, capacidades, jurisdiccion"
            ),
            "acceso_archivos": ["*"],
        },
        "diagnostico": {
            "descripcion": (
                "Diagnóstico propio de VX. No consulta DiagnosticoGlobal."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con id, estado, problemas, advertencias, "
                "recomendaciones"
            ),
            "acceso_archivos": ["*"],
        },
        "verificar_salida": {
            "descripcion": (
                "Comprueba forma mínima de una salida de VX."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "bool",
            "acceso_archivos": ["*"],
        },
        "axiomas": {
            "descripcion": (
                "Alias temporal de compatibilidad. "
                "AX es la única autoridad del conocimiento. "
                "No declara corpus oficial."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "list vacía (conocimiento oficial en AX)"
            ),
            "acceso_archivos": ["*"],
        },
        "ejecutar_total": {
            "descripcion": (
                "Autoridad total de ENGINE sobre VX. "
                "Ejerce TODAS las unidades operativamente ejecutables "
                "del módulo conforme a su contrato e inventario. "
                "Todo es callable real. No inventa capacidades."
            ),
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["*"],
            "salida": "dict con resultados de todas las unidades ejecutadas",
            "acceso_archivos": ["*"],
        },
        "inspeccionar": {
            "descripcion": (
                "Capacidad meta de inspeccion estructural de VX. "
                "Expone constantes, capacidades y estado "
                "sin alterar el contrato ni calcular."
            ),
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["acceso_archivos"],
            "salida": "dict con estructura, capacidades y estado del modulo",
            "acceso_archivos": ["acceso_archivos"],
        },
        "registrar_inventario": {
            "descripcion": (
                "Registra el inventario estructural de VX "
                "como instantanea determinista. No altera evidencia."
            ),
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["acceso_archivos"],
            "salida": "dict con inventario registrado",
            "acceso_archivos": ["acceso_archivos"],
        },
    },

    # ============================================================
    # 5.14 — REPORTING
    # ============================================================
    "reporting": {
        # --- BANDERAS DE ESTADO Y SALUD ---
        "estado": True,
        "salud": True,

        # --- BANDERAS DE INVENTARIO Y CAPACIDADES ---
        "inventario": True,
        "capacidades": True,

        # --- BANDERAS DE ERRORES Y ADVERTENCIAS ---
        "errores": True,
        "advertencias": True,

        # --- BANDERAS DE DEPENDENCIAS Y VERSION ---
        "dependencias": True,
        "version": True,

        # --- BANDERAS DE CONTRATO Y CONOCIMIENTO ---
        "contrato": True,
        "conocimiento": True,

        # --- BANDERAS DE METRICAS Y DIAGNOSTICO ---
        "metricas": True,
        "diagnostico": True,

        # --- BANDERA DE REPORTE ---
        "reporte": True,

        # --- BANDERAS OBLIGATORIAS SEGÚN ENGINE ---
        "acceso_archivos": True,
        "validar_esquema": True,

        # --- BANDERAS NUEVAS (OBLIGATORIAS ENGINE) ---
        "ejecutar_total": True,
        "inspeccionar": True,
        "registrar_inventario": True,
    },

    # ============================================================
    # 5.15 — ESTADOS VÁLIDOS
    # ============================================================
    "estados_validos": list(ESTADOS_VALIDOS),

    # ============================================================
    # 5.16 — INVARIANTES
    # ============================================================
    "invariantes": list(INVARIANTES),
}

# ===============================================================
# FIN PARTE 5
# ===============================================================


# ===============================================================
# PARTE 7 — FUNCIONES PRIVADAS
# ===============================================================

# ===============================================================
# 7.1 — EJECUTAR BARRIDO
# ===============================================================

def _ejecutar_barrido(
    codigo_fuente: Optional[Dict[str, Any]] = None,
    declaraciones_axiomaticas: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Orquesta el barrido transversal mediante AuditorAxiomatico.
    No modifica la lógica del auditor.
    No llama a Diagnóstico.
    Solo produce evidencia.
    """
    auditor = AuditorAxiomatico()
    resultado = auditor.ejecutar_barrido_transversal(
        codigo_fuente or {},
        declaraciones_axiomaticas or {},
    )
    if not isinstance(resultado, dict):
        return {
            "coherente": False,
            "errores": [
                {
                    "tipo": "salida_invalida",
                    "detalle": "AuditorAxiomatico no devolvió dict",
                }
            ],
            "evidencia": [],
        }
    return resultado

# ===============================================================
# FIN 7.1
# ===============================================================


# ===============================================================
# 7.2 — VALIDAR CONTRATO
# ===============================================================

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
            "{0}: CONTENEDOR incompleto. Faltan: {1}".format(
                NOMBRE_MODULO, faltantes
            )
        )
    if cont.get("esquema") != ESQUEMA_CONTRATO:
        raise ContratoInvalido(
            "{0}: esquema incompatible: {1}".format(
                NOMBRE_MODULO, cont.get("esquema")
            )
        )
    meta_caps = cont.get("capacidades_meta") or {}
    for nombre_cap in cont.get("capacidades") or {}:
        if nombre_cap not in meta_caps:
            raise ContratoInvalido(
                "{0}: capacidad '{1}' sin capacidades_meta".format(
                    NOMBRE_MODULO, nombre_cap
                )
            )
        entrada = meta_caps[nombre_cap]
        if not isinstance(entrada, dict):
            raise ContratoInvalido(
                "{0}: capacidades_meta['{1}'] debe ser dict".format(
                    NOMBRE_MODULO, nombre_cap
                )
            )
        for campo in ("descripcion", "entrada", "salida"):
            if campo not in entrada or not isinstance(entrada[campo], str):
                raise ContratoInvalido(
                    "{0}: capacidades_meta['{1}'] requiere '{2}: str'".format(
                        NOMBRE_MODULO, nombre_cap, campo
                    )
                )

# ===============================================================
# FIN 7.2
# ===============================================================

# ===============================================================
# FIN PARTE 7
# ===============================================================


# ===============================================================
# PARTE 8 — CAPACIDADES PÚBLICAS
# ===============================================================

# ===============================================================
# 8.1 — VERIFICAR
# ===============================================================

def verificar(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Capacidad principal: verificar una estructura contra reglas formales.

    peticion (opcional) puede incluir:
      - codigo_fuente
      - declaraciones_axiomaticas
      - estructura (futuro: contratos, módulos, grafos, …)

    Hoy el camino operativo usa codigo_fuente + declaraciones.
    La forma de la API admite crecimiento sin romper firmas.
    """
    base = peticion if isinstance(peticion, dict) else {}
    resultado = _ejecutar_barrido(
        base.get("codigo_fuente"),
        base.get("declaraciones_axiomaticas"),
    )
    return {
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "coherente": bool(resultado.get("coherente", False)),
        "errores": list(resultado.get("errores") or []),
        "evidencia": resultado.get("evidencia", resultado),
        "detalle": resultado,
        "nota": (
            "VX solo produce evidencia de verificación estructural. "
            "No interpreta, no corrige, no deposita en Diagnóstico."
        ),
    }

# ===============================================================
# FIN 8.1
# ===============================================================


# ===============================================================
# 8.2 — BARRER
# ===============================================================

def barrer(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Alias operativo de verificar.
    Centinela de coherencia estructural del barrido.
    """
    return verificar(peticion)

# ===============================================================
# FIN 8.2
# ===============================================================


# ===============================================================
# 8.3 — AXIOMAS (compatibilidad temporal)
# ===============================================================

def axiomas() -> List[Dict[str, Any]]:
    """
    Alias temporal de compatibilidad.

    AX es la única autoridad del conocimiento axiomático.
    Esta función NO declara conocimiento oficial.
    No duplica el corpus de AX.
    Devuelve lista vacía: las declaraciones se consumen vía Engine → AX.
    """
    return []

# ===============================================================
# FIN 8.3
# ===============================================================


# ===============================================================
# 8.4 — INVENTARIO
# ===============================================================

def inventario(peticion: Any = None) -> Dict[str, Any]:
    """
    Inventario del módulo VX.
    Forma mínima contractual alineada a VPSI-CONTRACT-1.0.
    """
    return {
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "compatible_desde": COMPATIBLE_DESDE,
        "api_engine": API_ENGINE,
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "funcion": (
            "Autoridad de verificación estructural. "
            "Determina si una estructura satisface o viola reglas formales. "
            "Solo produce evidencia. No interpreta, no corrige, no ejecuta."
        ),
        "jurisdiccion": [
            "codigo",
            "contratos",
            "modulos",
            "configuraciones",
            "salidas",
            "estructuras",
            "grafos",
            "arboles",
            "futuras_representaciones",
        ],
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "invariantes": list(INVARIANTES),
    }

# ===============================================================
# FIN 8.4
# ===============================================================


# ===============================================================
# 8.5 — REPORTE
# ===============================================================

def reporte(peticion: Any = None) -> Dict[str, Any]:
    """Reporte interno de estado del módulo VX."""
    inv = inventario()
    return {
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "estado": ESTADO_OPERATIVO,
        "coherente": True,
        "capacidades": inv.get("capacidades"),
        "jurisdiccion": inv.get("jurisdiccion"),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "operaciones_arquitectonicas": {
            "ejecutar_total": True,
            "inspeccionar": True,
            "registrar_inventario": True,
        },
        "nota": (
            "VX no mantiene sesión de auditoría persistente. "
            "Cada verificar()/barrer() produce evidencia puntual."
        ),
    }

# ===============================================================
# FIN 8.5
# ===============================================================


# ===============================================================
# 8.6 — DIAGNÓSTICO
# ===============================================================

def diagnostico(peticion: Any = None) -> Dict[str, Any]:
    """
    Diagnóstico propio del módulo VX.
    No consulta DiagnosticoGlobal.
    Solo reporta el estado interno de esta autoridad.
    """
    return {
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "estado": ESTADO_OPERATIVO,
        "problemas": [],
        "advertencias": [],
        "recomendaciones": [],
        "coherente": True,
        "nota": (
            "Diagnóstico propio de VX. "
            "La evidencia de verificaciones concretas se obtiene "
            "invocando verificar()/barrer(); Engine decide su destino."
        ),
    }

# ===============================================================
# FIN 8.6
# ===============================================================


# ===============================================================
# 8.7 — VERIFICAR SALIDA
# ===============================================================

def verificar_salida(salida: Any) -> bool:
    """
    Valida forma mínima de una salida de VX.
    No interpreta contenido semántico.
    """
    if not isinstance(salida, dict):
        return False
    return "coherente" in salida or "id" in salida

# ===============================================================
# FIN 8.7
# ===============================================================


# ===============================================================
# 8.8 — EJECUTAR TOTAL
# ===============================================================

def ejecutar_total(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Autoridad total de ENGINE sobre VX.
    Fuente única: CONTENEDOR["capacidades"].
    No inventa. No autoinvoca. Todo callable real.
    """
    peticion_normalizada = (
        dict(peticion) if isinstance(peticion, dict) else {}
    )
    resultados: Dict[str, Any] = {}
    errores_ejecucion: List[str] = []

    capacidades = CONTENEDOR.get("capacidades", {})
    if not isinstance(capacidades, dict):
        return {
            "id": ID_MODULO,
            "modulo": NOMBRE_MODULO,
            "rol": ROL_MODULO,
            "version": VERSION_MODULO,
            "operacion": "ejecutar_total",
            "estado": ESTADO_DEGRADADO,
            "coherente": False,
            "capacidades_ejecutadas": [],
            "errores_ejecucion": [
                f"{NOMBRE_MODULO}: CONTENEDOR['capacidades'] no es dict"
            ],
            "resultados": {},
            "capacidades_declaradas": [],
        }

    for nombre in sorted(capacidades):
        if nombre == "ejecutar_total":
            continue
        referencia = capacidades[nombre]
        try:
            if callable(referencia):
                fn = referencia
            elif isinstance(referencia, str):
                fn = globals().get(referencia)
                if not callable(fn):
                    raise ContratoInvalido(
                        f"'{referencia}' no es callable"
                    )
            else:
                raise ContratoInvalido(
                    f"tipo inválido: {type(referencia).__name__}"
                )

            if nombre in ("verificar", "barrer"):
                resultados[nombre] = fn(peticion_normalizada)
            elif nombre == "verificar_salida":
                resultados[nombre] = fn(
                    peticion_normalizada.get("salida")
                    if "salida" in peticion_normalizada
                    else {}
                )
            elif nombre in ("inventario", "reporte", "diagnostico"):
                resultados[nombre] = fn(peticion_normalizada)
            else:
                resultados[nombre] = fn()
        except Exception as exc:
            errores_ejecucion.append(f"{nombre}: {exc}")
            resultados[nombre] = None

    verificacion = resultados.get("verificar") or resultados.get("barrer")
    coherente = (
        isinstance(verificacion, dict)
        and bool(verificacion.get("coherente"))
    )
    ejecutadas = sorted(
        n for n, r in resultados.items() if r is not None
    )

    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "operacion": "ejecutar_total",
        "estado": (
            ESTADO_OPERATIVO
            if coherente and not errores_ejecucion
            else ESTADO_DEGRADADO
        ),
        "coherente": coherente and not errores_ejecucion,
        "capacidades_ejecutadas": ejecutadas,
        "errores_ejecucion": errores_ejecucion,
        "resultados": resultados,
        "capacidades_declaradas": sorted(capacidades.keys()),
    }

# ===============================================================
# FIN 8.8
# ===============================================================


# ===============================================================
# 8.9 — INSPECCIONAR
# ===============================================================

def inspeccionar(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Inspección estructural de VX.
    Expone contrato y estado sin calcular ni alterar.
    """
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "operacion": "inspeccionar",
        "constantes": {
            "ID_MODULO": ID_MODULO,
            "NOMBRE_MODULO": NOMBRE_MODULO,
            "ROL_MODULO": ROL_MODULO,
            "VERSION_MODULO": VERSION_MODULO,
            "VERSION_CONTRATO": VERSION_CONTRATO,
            "ESQUEMA_CONTRATO": ESQUEMA_CONTRATO,
            "ESTABILIDAD": ESTABILIDAD,
        },
        "capacidades_contractuales": sorted(
            CONTENEDOR.get("capacidades", {}).keys()
        ),
        "capacidades_meta": sorted(
            CONTENEDOR.get("capacidades_meta", {}).keys()
        ),
        "jurisdiccion": [
            "codigo",
            "contratos",
            "modulos",
            "configuraciones",
            "salidas",
            "estructuras",
            "grafos",
            "arboles",
            "futuras_representaciones",
        ],
        "autoriza_engine": CONTENEDOR.get("autoriza_engine"),
        "reporting": CONTENEDOR.get("reporting"),
        "invariantes": list(INVARIANTES),
        "nota": (
            "inspeccionar expone estructura de VX sin calcular "
            "ni alterar el contrato ni la evidencia."
        ),
    }

# ===============================================================
# FIN 8.9
# ===============================================================


# ===============================================================
# 8.10 — REGISTRAR INVENTARIO
# ===============================================================

def registrar_inventario(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Instantánea determinista del inventario de VX.
    No altera evidencia.
    """
    inv = inventario(peticion)
    return {
        "id": ID_MODULO,
        "operacion": "registrar_inventario",
        "registrado": True,
        "inventario": inv,
        "nota": (
            "Instantánea determinista del inventario de VX. "
            "No modifica evidencia ni estructuras auditadas."
        ),
    }

# ===============================================================
# FIN 8.10
# ===============================================================

# ===============================================================
# FIN PARTE 8
# ===============================================================


# ===============================================================
# PARTE 10 — VALIDACIÓN, RESOLUCIÓN Y EXPORTACIONES
# ===============================================================

# ===============================================================
# 10.1 — MAPA DE CAPACIDADES
# ===============================================================

_CAP_MAP = {
    # --- CENTINELA ---
    "verificar": verificar,
    "barrer": barrer,
    "verificar_salida": verificar_salida,

    # --- COMPATIBILIDAD ---
    "axiomas": axiomas,

    # --- INVENTARIO Y REPORTING ---
    "inventario": inventario,
    "reporte": reporte,
    "diagnostico": diagnostico,

    # --- CAPACIDADES ARQUITECTÓNICAS (OBLIGATORIAS ENGINE) ---
    "ejecutar_total": ejecutar_total,
    "inspeccionar": inspeccionar,
    "registrar_inventario": registrar_inventario,
}

# ===============================================================
# FIN 10.1
# ===============================================================


# ===============================================================
# 10.2 — RESOLUCIÓN DE CAPACIDADES
# ===============================================================

def _resolver_capacidades(cont: Dict[str, Any]) -> None:
    """
    Resuelve referencias str → callables reales.
    MUTA CONTENEDOR["capacidades"] para que Engine reciba callables.
    """
    resueltas: Dict[str, Any] = {}
    for nombre, ref in cont["capacidades"].items():
        if callable(ref):
            resueltas[nombre] = ref
            continue
        if isinstance(ref, str):
            if ref not in _CAP_MAP:
                raise ContratoInvalido(
                    "{0}: capacidad '{1}' referencia inexistente: '{2}'".format(
                        NOMBRE_MODULO, nombre, ref
                    )
                )
            fn = _CAP_MAP[ref]
            if not callable(fn):
                raise ContratoInvalido(
                    "{0}: '{1}' no es callable".format(
                        NOMBRE_MODULO, ref
                    )
                )
            resueltas[nombre] = fn
            continue
        raise ContratoInvalido(
            "{0}: capacidad '{1}' tipo inválido: {2}".format(
                NOMBRE_MODULO, nombre, type(ref).__name__
            )
        )
    cont["capacidades"] = resueltas

# ===============================================================
# FIN 10.2
# ===============================================================


# ===============================================================
# 10.3 — VALIDAR Y RESOLVER AL IMPORTAR
# ===============================================================

_validar_contrato(CONTENEDOR)
_resolver_capacidades(CONTENEDOR)

# ===============================================================
# FIN 10.3
# ===============================================================


# ===============================================================
# 10.4 — EXPORTACIONES
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
    "verificar",
    "barrer",
    "inventario",
    "reporte",
    "diagnostico",
    "verificar_salida",
    "axiomas",
    "ejecutar_total",
    "inspeccionar",
    "registrar_inventario",
    "ContratoInvalido",
]

# ===============================================================
# FIN 10.4
# ===============================================================

# ===============================================================
# FIN PARTE 10
# ===============================================================


# ===============================================================
# FIN DEL MÓDULO
# ===============================================================
