# ===============================================================
# VPSI-TRUTH — modules/axiomas/__init__.py
# ===============================================================
#
# MÓDULO:              axiomas
# ID:                  AX
# Rol:                 AX
# Versión módulo:      9.6
# Versión contrato:    1.0
# Esquema contrato:    VPSI-CONTRACT-1.0
# Estabilidad:         ESTABLE
# Compatible desde:    9.5
# API Engine:          >=1.0
#
# ENGINE EJECUTA CODAS LAS CAPACIDADES DE CADA MODULO 
# SIN EXCEPCION
# ===============================================================


# ===============================================================
# PARTE 1 — PRINCIPIOS, BANDERAS Y ESPECIFICACIONES PRECISAS
# ===============================================================

# ===============================================================
# 1.1 — IMPORTACIONES
# ===============================================================

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Set

try:
    from core.diagnostico import DiagnosticoGlobal  # type: ignore
except Exception:  # noqa: BLE001
    DiagnosticoGlobal = None  # type: ignore

# ===============================================================
# FIN 1.1
# ===============================================================


# ===============================================================
# 1.2 — BANDERAS DE ESTADO
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
# FIN 1.2
# ===============================================================


# ===============================================================
# 1.3 — TIPOS Y CLAVES OBLIGATORIAS
# ===============================================================

OBLIGATORIOS = ("id", "tipo", "sujeto", "relacion", "objeto", "polaridad")
TIPOS = ("axioma", "lema", "teorema", "corolario", "definicion")

AXIOMA = "axioma"
LEMA = "lema"
TEOREMA = "teorema"
COROLARIO = "corolario"
DEFINICION = "definicion"

# ===============================================================
# FIN 1.3
# ===============================================================


# ===============================================================
# 1.4 — TRADUCCIÓN DE CLAVES
# ===============================================================

TRADUCCION_CLAVES = {
    "type": "tipo",           # type = tipo
    "subject": "sujeto",      # subject = sujeto
    "relation": "relacion",   # relation = relación
    "object": "objeto",       # object = objeto
    "polarity": "polaridad",  # polarity = polaridad (verdadero o falso)
    "statement": "enunciado", # statement = el texto de la declaración
    "depends_on": "depende_de", # depends_on = de qué depende
    "governs": "gobierna",    # governs = qué dominios controla
    "cota": "cota",           # cota = límite o valor límite
}

# ===============================================================
# FIN 1.4
# ===============================================================


# ===============================================================
# 1.5 — DOMINIOS
# ===============================================================

DOMINIOS_K_O = frozenset({
    "contexto", "ontologia", "epistemologia", "verificacion",
    "dominio", "k", "o_context", "correlacion",
})

DOMINIO_CANONICO = {
    "ontologia": "ONT", "ont": "ONT",
    "informacion": "INF", "info": "INF",
    "logica": "LOG", "log": "LOG",
    "epistemologia": "EPI", "epi": "EPI",
    "semantica": "SEM", "sem": "SEM",
    "temporal": "TMP", "tmp": "TMP",
    "meta": "MET", "met": "MET",
    "constantes": "MET",
    "self": "EPI",
    "inferencia_causal": "INF",
    "verificacion": "EPI", "ver": "VER",
    "contexto": "SEM",
}

# ===============================================================
# FIN 1.5
# ===============================================================


# ===============================================================
# 1.6 — Θ CANÓNICO
# ===============================================================

THETA_24 = {
    "T1": frozenset({"ONT", "INF"}),
    "T2": frozenset({"INF", "LOG"}),
    "T3": frozenset({"INF", "TMP"}),
    "T4": frozenset({"EPI", "TMP"}),
    "T5": frozenset({"ONT", "EPI"}),
    "T6": frozenset({"LOG", "SEM"}),
    "T7": frozenset({"ONT", "MET"}),
    "T8": frozenset({"INF", "MET"}),
    "T9": frozenset({"EPI", "INF"}),
    "T10": frozenset({"ONT", "INF"}),
    "T11": frozenset({"ONT", "MET"}),
    "T12": frozenset({"EPI", "ONT"}),
    "T13": frozenset({"EPI", "SEM"}),
    "T14": frozenset({"EPI", "MET"}),
    "T15": frozenset({"ONT", "INF", "MET"}),
    "T16": frozenset({"EPI", "MET"}),
    "T17": frozenset({"ONT", "MET", "TMP"}),
    "U1": frozenset({"EPI", "TMP", "MET"}),
    "M1": frozenset({"MET", "LOG"}),
    "M.1": frozenset({"MET", "ONT"}),
    "B-Canonical": frozenset({"ONT", "LOG", "MET"}),
    "TT.6.1": frozenset({"LOG", "SEM", "EPI"}),
    "U0": frozenset({"ONT", "INF", "TMP"}),
    "TR1": frozenset({"MET", "INF", "LOG"}),
}

THETA_CANONICO = frozenset(THETA_24.keys())

# ===============================================================
# FIN 1.6
# ===============================================================


# ===============================================================
# 1.7 — INVARIANTES
# ===============================================================

INVARIANTES = (
    "el id del módulo nunca cambia",
    "el rol nunca cambia",
    "las capacidades declaradas son siempre callables tras la resolución",
    "este módulo no modifica el estado de otros módulos",
    "este módulo no inventa capacidades no declaradas en CONTENEDOR",
    "este módulo siempre puede reportar su propio estado",
    "una conclusión solo se reconoce como sustentada si sus premisas están en el cuerpo axiomático",
    "ausencia de premisa no se convierte en axioma",
    "contradicción y límite axiomático son estados distintos",
)

# ===============================================================
# FIN 1.7
# ===============================================================


# ===============================================================
# PARTE 2 — IDENTIDAD
# ===============================================================

# ===============================================================
# 2.1 — IDENTIFICADORES
# ===============================================================

ID_MODULO = "AX"
NOMBRE_MODULO = "axiomas"
ROL_MODULO = "AX"

# ===============================================================
# FIN 2.1
# ===============================================================


# ===============================================================
# 2.2 — VERSIONES Y ESTABILIDAD
# ===============================================================

VERSION_MODULO = "9.6"
VERSION_CONTRATO = "1.0"
ESQUEMA_CONTRATO = "VPSI-CONTRACT-1.0"
COMPATIBLE_DESDE = "9.5"
API_ENGINE = ">=1.0"
ESTABILIDAD = "ESTABLE"

# ===============================================================
# FIN 2.2
# ===============================================================


# ===============================================================
# PARTE 3 — CONFIGURACIÓN
# ===============================================================

_DIR = Path(__file__).parent


def _ruta_vpsi() -> Optional[Path]:
    candidatos = [
        _DIR.parent.parent / "VPSI.py",
        _DIR.parent / "VPSI.py",
        _DIR / "VPSI.py",
    ]
    for p in candidatos:
        if p.exists():
            return p
    return None


def _rutas_py() -> List[Path]:
    return sorted(
        p for p in _DIR.glob("**/*.py")
        if p.name != "__init__.py"
    )

# ===============================================================
# FIN PARTE 3
# ===============================================================


# ===============================================================
# PARTE 4 — EXCEPCIONES
# ===============================================================

class ContratoInvalido(Exception):
    """El CONTENEDOR no cumple el esquema o la resolución de capacidades falló."""

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
        "Responsable del conocimiento axiomático del sistema. "
        "Mantiene, valida, organiza y expone todas las declaraciones "
        "oficiales del repositorio a ENGINE."
    ),

    # ============================================================
    # 5.3 — PROPÓSITO
    # ============================================================
    "funcion": (
        "Ser la fuente oficial del conocimiento axiomático: "
        "cargar, normalizar, validar coherencia, responder consultas, "
        "citar declaraciones, exponer generatividad y determinar "
        "el límite axiomático."
    ),
    "no_hace": [
        "No calcula Tru_total ni Tru_Ri",
        "No orquesta el sistema (eso es Engine)",
        "No genera reportes de otros módulos",
    ],

    # ============================================================
    # 5.4 — AUTORIDAD
    # ============================================================
    "autoridad": [
        "Exponer cualquier axioma, lema, teorema, corolario o definición",
        "Responder consultas por id, dominio, sujeto, relación, objeto",
        "Citar y relacionar declaraciones del grafo",
        "Verificar coherencia interna",
        "Reportar estado, salud, inventario y diagnóstico propios",
        "Notificar a DiagnosticoGlobal cuando hay choques o errores",
        "Determinar el límite de derivación axiomática",
    ],

    # ============================================================
    # 5.5 — CONOCIMIENTO EXPORTABLE
    # ============================================================
    "conocimiento_exportable": [
        "declaraciones",
        "referencias",
        "dependencias",
        "dominios",
        "generatividad",
        "choques",
        "inventario",
        "estado",
        "reporte",
        "diagnostico",
        "limite_axiomático",
    ],

    # ============================================================
    # 5.6 — ACCESO
    # ============================================================
    "acceso": {
        "nivel": "acceso_archivos",
        "descripcion": "Acceso total a recursos del módulo"
    },

    # ============================================================
    # 5.7 — DEPENDENCIAS
    # ============================================================
    # CORRECCIÓN 1: eliminado "AX" de requiere (dependencia autorreferencial)
    "requiere": [
        "CT", "FO", "MC", "SF", "CA", "CX", "CC",
        "DI", "RE", "VX", "TX", "CH", "CIT", "TT", "CE",
    ],

    # ============================================================
    # 5.8 — ACCESO A ARCHIVOS / VALIDAR ESQUEMA
    # ============================================================
    "acceso_archivos": ["acceso_archivos"],
    "validar_esquema": ["*"],

    # ============================================================
    # 5.9 — CONSULTAS SOPORTADAS
    # ============================================================
    "consultas_soportadas": [
        "buscar_por_id",
        "buscar_por_dominio",
        "obtener_generatividad",
        "obtener_inventario",
        "obtener_reporte",
        "obtener_diagnostico",
        "verificar_coherencia",
        "ids_dominio_k_o",
        "recolectar",
        "limite_axiomático",
    ],

    # ============================================================
    # 5.10 — CAPACIDADES
    # ============================================================
    "capacidades": {
        "verificar": "barrer",
        "barrer": "barrer",
        "verificar_salida": "verificar_salida",
        "inventario": "inventario",
        "axiomas": "axiomas",
        "declaraciones": "declaraciones",
        "generatividad": "generatividad",
        "por_dominio": "por_dominio",
        "ids_dominio_k_o": "ids_dominio_k_o",
        "recolectar": "recolectar",
        "reporte": "reporte",
        "diagnostico": "diagnostico",
        "buscar_por_id": "buscar_por_id",
        "limite_axiomático": "limite_axiomático",
        "ejecutar_total": "ejecutar_total",
        "inspeccionar": "inspeccionar",
    },

    # ============================================================
    # 5.11 — METADATOS DE CAPACIDADES
    # ============================================================
    "capacidades_meta": {
        "verificar": {
            "descripcion": "Alias de barrer. Verifica coherencia interna del módulo.",
            "entrada": "declaraciones_externas opcional (dict)",
            "validar_esquema": ["acceso_archivos"],
            "salida": "dict con coherente, choques, errores, declaraciones, cuerpos, por_tipo",
            "acceso_archivos": ["acceso_archivos"],
        },
        "barrer": {
            "descripcion": "Analiza coherencia de todas las declaraciones (contradicción directa y de cota).",
            "entrada": "declaraciones_externas opcional (dict)",
            "validar_esquema": ["*"],
            "salida": "dict con coherente, choques, errores, declaraciones, cuerpos, por_tipo, ids_dominio_k_o",
            "acceso_archivos": ["*"],
        },
        "verificar_salida": {
            "descripcion": "Comprueba si una salida de barrer/verificar es coherente.",
            "entrada": "salida: dict",
            "validar_esquema": ["validar_esquema"],
            "salida": "bool",
            "acceso_archivos": ["acceso_archivos"],
        },
        "inventario": {
            "descripcion": "Inventario completo del módulo (declaraciones, cuerpos, capacidades).",
            "entrada": "peticion",
            "validar_esquema": ["acceso_archivos"],
            "salida": "dict con id, nombre, rol, version, declaraciones, cuerpos, capacidades",
            "acceso_archivos": ["acceso_archivos"],
        },
        "axiomas": {
            "descripcion": "Devuelve las declaraciones si el módulo es coherente; lista vacía si no.",
            "entrada": "declaraciones_externas opcional (dict)",
            "validar_esquema": ["*"],
            "salida": "list[dict] de declaraciones normalizadas",
            "acceso_archivos": ["*"],
        },
        "declaraciones": {
            "descripcion": "Igual que axiomas: declaraciones normalizadas si coherente.",
            "entrada": "declaraciones_externas opcional (dict)",
            "validar_esquema": ["*"],
            "salida": "list[dict] de declaraciones normalizadas",
            "acceso_archivos": ["*"],
        },
        "generatividad": {
            "descripcion": "Mide generatividad operativa y canónica (TR1).",
            "entrada": "acceso_archivos",
            "validar_esquema": ["acceso_archivos"],
            "salida": "dict con theta_n, pares, im_vs_theta, capa canonica, dominios, u1_proxy",
            "acceso_archivos": ["acceso_archivos"],
        },
        "por_dominio": {
            "descripcion": "Filtra declaraciones por dominio en gobierna.",
            "entrada": "dominio: str; declaraciones_externas opcional",
            "validar_esquema": ["acceso_archivos"],
            "salida": "list[dict] de declaraciones del dominio",
            "acceso_archivos": ["acceso_archivos"],
        },
        "ids_dominio_k_o": {
            "descripcion": "Ids de declaraciones ligadas a dominios K/O o Def-5.3.1.",
            "entrada": "declaraciones_externas (dict)",
            "validar_esquema": ["acceso_archivos"],
            "salida": "list[str] de ids ordenados",
            "acceso_archivos": ["acceso_archivos"],
        },
        "recolectar": {
            "descripcion": "Carga y normaliza todas las declaraciones de los cuerpos del módulo.",
            "entrada": "declaraciones_externas opcional (dict)",
            "validar_esquema": ["acceso_archivos"],
            "salida": "tuple[list[dict], list[dict]] → (declaraciones, errores)",
            "acceso_archivos": ["acceso_archivos"],
        },
        "reporte": {
            "descripcion": "Reporte interno de estado del módulo.",
            "entrada": "acceso_archivos",
            "validar_esquema": ["*"],
            "salida": "dict con estado, coherente, declaraciones, choques, errores, capacidades",
            "acceso_archivos": ["*"],
        },
        "diagnostico": {
            "descripcion": "Diagnóstico: qué me sucede, qué falta, qué está mal, qué necesito.",
            "entrada": "acceso_archivos",
            "validar_esquema": ["acceso_archivos"],
            "salida": "dict con estado, problemas, advertencias, recomendaciones, limites",
            "acceso_archivos": ["acceso_archivos"],
        },
        "buscar_por_id": {
            "descripcion": "Busca y cita una declaración por su id.",
            "entrada": "id_decl: str",
            "validar_esquema": ["acceso_archivos"],
            "salida": "dict de la declaración o None",
            "acceso_archivos": ["acceso_archivos"],
        },
        "limite_axiomático": {
                "descripcion": (
                "Determina el límite de derivación axiomática: "
                "premisas disponibles, premisas faltantes, dependencias "
                "no satisfechas, alcance y declaraciones no derivables."
            ),
            "entrada": "declaraciones_externas opcional (dict)",
            "validar_esquema": ["acceso_archivos"],
            "salida": (
                "dict con premisas_disponibles, premisas_faltantes, "
                "dependencias_no_satisfechas, limites, alcance"
            ),
            "acceso_archivos": ["acceso_archivos"],
        },
        "ejecutar_total": {
            "descripcion": (
                "Operación arquitectónica genérica. "
                "Ejerce la totalidad de las unidades operativamente "
                "ejecutables del módulo conforme a su contrato e inventario."
            ),
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["*"],
            "salida": "dict con resultados de las unidades ejecutadas",
            "acceso_archivos": ["*"],
        },
        "inspeccionar": {
            "descripcion": (
                "Capacidad meta de inspección estructural del módulo. "
                "Expone el estado interno, componentes y unidades "
                "ejecutables sin alterar el contrato."
            ),
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["acceso_archivos"],
            "salida": "dict con estructura, capacidades y estado del módulo",
            "acceso_archivos": ["acceso_archivos"],
        },
    },

    # ============================================================
    # 5.12 — AUTORIZACIÓN AL ENGINE
    # ============================================================
    "autoriza_engine": {
        # — LECTURA Y CONSULTA —
        "leer": True,
        "consultar": True,
        "estado": True,
        "version": True,
        "salud": True,
        "capacidades": True,
        "contrato": True,
        "conocimiento": True,
        "dependencias": True,

        # — EJECUCIÓN —
        "ejecutar": True,
        "ejecutar_total": True,
        "procesar": True,
        "analizar": True,
        "generar": True,
        "validar": True,
        "validar_esquema": True,

        # — INSPECCIÓN E INVENTARIO —
        "inspeccionar": True,
        "inventariar": True,
        "registrar_inventario": True,
        "inventario": True,
        "acceso_archivos": True,

        # — REPORTING Y DIAGNÓSTICO —
        "reportar": True,
        "reporte": True,
        "diagnostico": True,
        "metricas": True,
        "errores": True,
        "advertencias": True,
        "auditar": True,
        "monitorear": True,

        # — RECOMBINACIÓN Y SINCRONIZACIÓN —
        "recombinar": True,
        "sincronizar": True,
        "exportar": True,
        "importar": True,
        "respaldar": True,
        "recuperar": True,

        # — CREACIÓN Y MODIFICACIÓN —
        "crear": True,
        "actualizar": False,
        "alterar": False,
    },

    # ============================================================
    # 5.13 — REPORTING
    # ============================================================
    "reporting": {
        # — ESTADO Y SALUD —
        "estado": True,
        "salud": True,
        "version": True,

        # — INVENTARIO Y CAPACIDADES —
        "inventario": True,
        "capacidades": True,
        "acceso_archivos": True,
        "ejecutar_total": True,
        "inspeccionar": True,
        "registrar_inventario": True,

        # — ERRORES Y ADVERTENCIAS —
        "errores": True,
        "advertencias": True,

        # — DEPENDENCIAS Y CONTRATO —
        "dependencias": True,
        "contrato": True,
        "conocimiento": True,

        # — MÉTRICAS Y DIAGNÓSTICO —
        "metricas": True,
        "diagnostico": True,
        "reporte": True,
        "validar_esquema": True,
    },

    # ============================================================
    # 5.14 — ESTADOS VÁLIDOS E INVARIANTES
    # ============================================================
    "estados_validos": list(ESTADOS_VALIDOS),
    "invariantes": list(INVARIANTES),
}

# ===============================================================
# PARTE 6 — FUNCIONES PRIVADAS
# ===============================================================
# ===============================================================
# PARTE X — EJECUTAR_TOTAL
# ===============================================================

def ejecutar_total(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Operación arquitectónica genérica.
    Ejerce la totalidad de las unidades operativamente ejecutables
    pertenecientes al módulo, conforme a su contrato, inventario,
    clasificación, dependencias y leyes internas.

    La totalidad se determina por inspección e inventario del módulo,
    no por una lista fija de funciones ni por nombres concretos.

    No enumera funciones concretas.
    No inventa capacidades ni unidades operativas.
    No altera los contratos internos del módulo.
    """

    # -----------------------------------------------------------
    # X1. Instantánea única
    # -----------------------------------------------------------
    externas = None
    if isinstance(peticion, dict):
        externas = peticion.get("declaraciones_externas")

    decls, errores = recolectar(externas)
    choques_directa = contradiccion_directa(decls)
    choques_cota = contradiccion_de_cota(decls)
    choques = choques_directa + choques_cota
    lim = limite_axiomático(decls=decls, errores=errores)

    # -----------------------------------------------------------
    # X2. Unidades privadas ejercidas
    # -----------------------------------------------------------
    rutas = _rutas_py()
    ruta_vpsi = _ruta_vpsi()

    # medir pares sobre capa canónica
    canonicos = [
        {"id": tid, "tipo": "teorema", "dominios": set(doms)}
        for tid, doms in THETA_24.items()
    ]
    medicion_canonica = _medir_pares(canonicos)

    # -----------------------------------------------------------
    # X3. Unidades públicas ejercidas
    # -----------------------------------------------------------
    resultado_barrer = {
        "coherente": not (choques or errores),
        "choques": choques,
        "choques_directa": len(choques_directa),
        "choques_cota": len(choques_cota),
        "errores": errores,
        "declaraciones": len(decls),
        "cuerpos": sorted({d["cuerpo"] for d in decls}),
        "por_tipo": {t: sum(1 for d in decls if d["tipo"] == t) for t in TIPOS},
        "ids_dominio_k_o": ids_dominio_k_o(externas) if not (choques or errores) else [],
    }

    resultado_verificar_salida = verificar_salida(resultado_barrer)
    resultado_declaraciones = decls if resultado_barrer["coherente"] else []
    resultado_axiomas = resultado_declaraciones
    resultado_generatividad = generatividad()
    resultado_inventario = inventario()
    resultado_reporte = reporte()
    resultado_diagnostico = diagnostico()
    resultado_ids_k_o = ids_dominio_k_o(externas)
    resultado_limite = lim

    # -----------------------------------------------------------
    # X4. Consolidación total
    # -----------------------------------------------------------
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "operacion": "ejecutar_total",
        "estado": (
            ESTADO_OPERATIVO
            if resultado_barrer["coherente"]
            else ESTADO_DEGRADADO
        ),
        "coherente": resultado_barrer["coherente"],

        # -------------------------------------------------------
        # Unidades privadas
        # -------------------------------------------------------
        "unidades_privadas": {
            "_ruta_vpsi": str(ruta_vpsi) if ruta_vpsi else None,
            "_rutas_py": [str(p) for p in rutas],
            "contradiccion_directa": {
                "total": len(choques_directa),
            },
            "contradiccion_de_cota": {
                "total": len(choques_cota),
            },
            "_medir_pares": {
                "theta_n": medicion_canonica.get("theta_n"),
                "pares_totales": medicion_canonica.get("pares_totales"),
                "pares_compatibles": medicion_canonica.get("pares_compatibles"),
                "pares_novedosos": medicion_canonica.get("pares_novedosos"),
                "pares_redundantes": medicion_canonica.get("pares_redundantes"),
                "pares_incompatibles": medicion_canonica.get("pares_incompatibles"),
                "im_vs_theta": medicion_canonica.get("im_vs_theta"),
            },
            "clave_ref": "disponible (helpers de tripleta y ubicación)",
            "normalizar": "disponible (normalización de declaraciones)",
            "_cargar_declaraciones_desde_archivo": "disponible (carga por archivo)",
            "_validar_contrato": "ejecutado al importar el módulo",
            "_resolver_capacidades": "ejecutado al importar el módulo",
        },

        # -------------------------------------------------------
        # Unidades públicas
        # -------------------------------------------------------
        "unidades_publicas": {
            "recolectar": {
                "declaraciones": len(decls),
                "errores": len(errores),
            },
            "barrer": resultado_barrer,
            "verificar": resultado_barrer,
            "verificar_salida": resultado_verificar_salida,
            "declaraciones": len(resultado_declaraciones),
            "axiomas": len(resultado_axiomas),
            "generatividad": {
                "theta_n": resultado_generatividad.get("theta_n"),
                "pares_totales": resultado_generatividad.get("pares_totales"),
                "pares_novedosos": resultado_generatividad.get("pares_novedosos"),
                "im_vs_theta": resultado_generatividad.get("im_vs_theta"),
                "u1_proxy": resultado_generatividad.get("u1_proxy"),
                "coincide_paper": (
                    resultado_generatividad.get("canonica", {}).get("coincide_paper")
                ),
            },
            "por_dominio": "disponible (requiere dominio)",
            "ids_dominio_k_o": resultado_ids_k_o,
            "limite_axiomático": {
                "premisas_disponibles": len(
                    resultado_limite.get("premisas_disponibles") or []
                ),
                "premisas_faltantes": len(
                    resultado_limite.get("premisas_faltantes") or []
                ),
                "dependencias_no_satisfechas": len(
                    resultado_limite.get("dependencias_no_satisfechas") or []
                ),
                "dependencias_circulares": len(
                    resultado_limite.get("dependencias_circulares") or []
                ),
                "alcance": resultado_limite.get("alcance"),
            },
            "inventario": {
                "declaraciones": resultado_inventario.get("declaraciones"),
                "cuerpos": resultado_inventario.get("cuerpos"),
                "capacidades": resultado_inventario.get("capacidades"),
            },
            "reporte": resultado_reporte,
            "diagnostico": {
                "estado": resultado_diagnostico.get("estado"),
                "problemas": len(resultado_diagnostico.get("problemas") or []),
                "advertencias": len(resultado_diagnostico.get("advertencias") or []),
                "limites": len(resultado_diagnostico.get("limites") or []),
            },
            "buscar_por_id": "disponible (requiere id_decl)",
        },

        "capacidades_declaradas": list(CONTENEDOR["capacidades"].keys()),
        "capacidades_resueltas": list(CAPACIDADES_RESUELTAS.keys()),

        "resumen": {
            "total_declaraciones": len(decls),
            "total_errores": len(errores),
            "total_choques": len(choques),
            "premisas_faltantes": len(
                resultado_limite.get("premisas_faltantes") or []
            ),
            "dependencias_circulares": len(
                resultado_limite.get("dependencias_circulares") or []
            ),
            "theta_n": resultado_generatividad.get("theta_n"),
            "im_vs_theta": resultado_generatividad.get("im_vs_theta"),
            "archivos_py": len(rutas),
            "vpsi_presente": ruta_vpsi is not None,
        },

        "nota": (
            "ejecutar_total ejerce la totalidad de las unidades "
            "públicas y privadas del módulo AX. "
            "No inventa capacidades. No altera el contrato."
        ),
    }

# ===============================================================
# FIN PARTE X
# ===============================================================

# ===============================================================
# PARTE Y — INSPECCIONAR
# ===============================================================

def inspeccionar(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Capacidad meta de inspección estructural del módulo.
    Expone el estado interno, componentes, unidades ejecutables,
    contrato y estructura sin alterar nada.

    No ejecuta capacidades de análisis profundo.
    No inventa componentes.
    No modifica el contrato.
    """

    # -----------------------------------------------------------
    # Y1. Instantánea estructural
    # -----------------------------------------------------------
    rutas = _rutas_py()
    ruta_vpsi = _ruta_vpsi()
    decls, errores = recolectar()

    # -----------------------------------------------------------
    # Y2. Componentes privados detectados
    # -----------------------------------------------------------
    privadas = {
        "_ruta_vpsi": callable(_ruta_vpsi),
        "_rutas_py": callable(_rutas_py),
        "_cargar_declaraciones_desde_archivo": callable(
            _cargar_declaraciones_desde_archivo
        ),
        "normalizar": callable(normalizar),
        "clave": callable(clave),
        "ref": callable(ref),
        "contradiccion_directa": callable(contradiccion_directa),
        "contradiccion_de_cota": callable(contradiccion_de_cota),
        "_medir_pares": callable(_medir_pares),
        "_validar_contrato": callable(_validar_contrato),
        "_resolver_capacidades": callable(_resolver_capacidades),
    }

    # -----------------------------------------------------------
    # Y3. Componentes públicos detectados
    # -----------------------------------------------------------
    publicas = {
        "recolectar": callable(recolectar),
        "barrer": callable(barrer),
        "verificar": callable(verificar),
        "verificar_salida": callable(verificar_salida),
        "declaraciones": callable(declaraciones),
        "axiomas": callable(axiomas),
        "generatividad": callable(generatividad),
        "por_dominio": callable(por_dominio),
        "ids_dominio_k_o": callable(ids_dominio_k_o),
        "limite_axiomático": callable(limite_axiomático),
        "inventario": callable(inventario),
        "reporte": callable(reporte),
        "diagnostico": callable(diagnostico),
        "buscar_por_id": callable(buscar_por_id),
        "ejecutar_total": callable(ejecutar_total) if "ejecutar_total" in dir() else False,
        "inspeccionar": True,
        "registrar_inventario": (
            callable(registrar_inventario)
            if "registrar_inventario" in dir()
            else False
        ),
    }

    # -----------------------------------------------------------
    # Y4. Contrato y constantes
    # -----------------------------------------------------------
    constantes = {
        "ID_MODULO": ID_MODULO,
        "NOMBRE_MODULO": NOMBRE_MODULO,
        "ROL_MODULO": ROL_MODULO,
        "VERSION_MODULO": VERSION_MODULO,
        "VERSION_CONTRATO": VERSION_CONTRATO,
        "ESQUEMA_CONTRATO": ESQUEMA_CONTRATO,
        "ESTABILIDAD": ESTABILIDAD,
        "COMPATIBLE_DESDE": COMPATIBLE_DESDE,
        "API_ENGINE": API_ENGINE,
        "TIPOS": list(TIPOS),
        "OBLIGATORIOS": list(OBLIGATORIOS),
        "ESTADOS_VALIDOS": list(ESTADOS_VALIDOS),
        "THETA_24_n": len(THETA_24),
        "DOMINIOS_K_O": sorted(DOMINIOS_K_O),
        "DOMINIO_CANONICO_n": len(DOMINIO_CANONICO),
    }

    # -----------------------------------------------------------
    # Y5. Resultado de inspección
    # -----------------------------------------------------------
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "operacion": "inspeccionar",

        "archivos": {
            "py_del_modulo": [str(p) for p in rutas],
            "total_py": len(rutas),
            "vpsi": str(ruta_vpsi) if ruta_vpsi else None,
        },

        "componentes_privados": privadas,
        "componentes_publicos": publicas,

        "capacidades_declaradas": list(CONTENEDOR.get("capacidades", {}).keys()),
        "capacidades_resueltas": list(CAPACIDADES_RESUELTAS.keys()),
        "capacidades_meta": list(CONTENEDOR.get("capacidades_meta", {}).keys()),

        "constantes": constantes,

        "cuerpo_axiomático": {
            "declaraciones_cargadas": len(decls),
            "errores_carga": len(errores),
            "cuerpos": sorted({d["cuerpo"] for d in decls}),
            "por_tipo": {
                t: sum(1 for d in decls if d["tipo"] == t) for t in TIPOS
            },
        },

        "contrato": {
            "esquema": CONTENEDOR.get("esquema"),
            "version_contrato": CONTENEDOR.get("version_contrato"),
            "version_modulo": CONTENEDOR.get("version_modulo"),
            "estabilidad": CONTENEDOR.get("estabilidad"),
            "requiere": CONTENEDOR.get("requiere"),
            "autoridad": CONTENEDOR.get("autoridad"),
            "conocimiento_exportable": CONTENEDOR.get("conocimiento_exportable"),
            "consultas_soportadas": CONTENEDOR.get("consultas_soportadas"),
            "invariantes": CONTENEDOR.get("invariantes"),
            "estados_validos": CONTENEDOR.get("estados_validos"),
        },

        "autoriza_engine": CONTENEDOR.get("autoriza_engine"),
        "reporting": CONTENEDOR.get("reporting"),

        "resumen": {
            "total_privadas": sum(1 for v in privadas.values() if v),
            "total_publicas": sum(1 for v in publicas.values() if v),
            "total_capacidades_declaradas": len(
                CONTENEDOR.get("capacidades", {})
            ),
            "total_capacidades_resueltas": len(CAPACIDADES_RESUELTAS),
            "total_archivos_py": len(rutas),
            "declaraciones": len(decls),
            "errores": len(errores),
        },

        "nota": (
            "inspeccionar expone la estructura completa del módulo "
            "sin ejecutar análisis profundo ni alterar el contrato."
        ),
    }

# ===============================================================
# FIN PARTE Y
# =============================================================== 
# ===============================================================
# 6.1 — CARGA DESDE ARCHIVO
# ===============================================================

def _cargar_declaraciones_desde_archivo(archivo: Path) -> Tuple[List[Dict], Optional[str]]:
    """
    CORRECCIÓN 21: Distingue archivo sin declaraciones vs error de ejecución.
    Retorna (lista, error_opcional).
    """
    if archivo.name.startswith("_"):
        return [], None

    # CORRECCIÓN 22: nombre de módulo inequívoco
    rel = archivo.relative_to(_DIR) if _DIR in archivo.parents or archivo.parent == _DIR else archivo.name
    nombre_mod = "axiomas_{0}".format(str(rel).replace("/", "_").replace("\\", "_").replace(".", "_"))
    spec = importlib.util.spec_from_file_location(nombre_mod, archivo)
    if spec is None or spec.loader is None:
        return [], "spec_invalido"

    mod = importlib.util.module_from_spec(spec)
    sys.modules[nombre_mod] = mod
    try:
        spec.loader.exec_module(mod)
    except Exception as e:
        if nombre_mod in sys.modules:
            del sys.modules[nombre_mod]
        return [], "{0}: {1}".format(type(e).__name__, e)

    declaraciones_raw = getattr(mod, "DECLARACIONES", None)
    if declaraciones_raw is None and callable(getattr(mod, "declaraciones", None)):
        try:
            declaraciones_raw = mod.declaraciones()
        except Exception as e:
            return [], "declaraciones(): {0}: {1}".format(type(e).__name__, e)

    if declaraciones_raw is None:
        for attr in ("CUERPO", "declaraciones_lista"):
            val = getattr(mod, attr, None)
            if isinstance(val, list):
                declaraciones_raw = val
                break

    if declaraciones_raw is None:
        return [], None  # archivo sin declaraciones

    if not isinstance(declaraciones_raw, list):
        return [], "DECLARACIONES no es list"

    return declaraciones_raw, None

# ===============================================================
# FIN 6.1
# ===============================================================


# ===============================================================
# 6.2 — NORMALIZACIÓN DE DECLARACIÓN
# ===============================================================

def normalizar(decl_original: Dict, cuerpo: str) -> Dict:
    """
    CORRECCIONES 6, 7, 8:
    - depende_de y gobierna deben ser iterables propios
    - id no vacío
    - sujeto/relacion/objeto no vacíos
    """
    if not isinstance(decl_original, dict):
        raise ValueError("{0}: declaración no es dict".format(cuerpo))

    decl: Dict[str, Any] = {}
    for clave_orig, valor in decl_original.items():
        decl[TRADUCCION_CLAVES.get(clave_orig, clave_orig)] = valor

    for k in OBLIGATORIOS:
        if k not in decl:
            raise ValueError(
                "{0}:{1} sin clave obligatoria '{2}'".format(
                    cuerpo, decl.get("id", "?"), k
                )
            )

    # CORRECCIÓN 7: id no vacío
    id_norm = str(decl["id"]).strip()
    if not id_norm:
        raise ValueError("{0}: id vacío o inválido".format(cuerpo))

    # CORRECCIÓN 8: sujeto/relacion/objeto no vacíos
    for campo in ("sujeto", "relacion", "objeto"):
        val = decl.get(campo)
        if val is None or str(val).strip() == "":
            raise ValueError("{0}:{1} '{2}' vacío o None".format(cuerpo, id_norm, campo))

    tipo = str(decl["tipo"]).lower()
    tipo = {
        "axiom": "axioma",
        "theorem": "teorema",
        "corollary": "corolario",
        "lemma": "lema",
        "definition": "definicion",
    }.get(tipo, tipo)

    if tipo not in TIPOS:
        raise ValueError(
            "{0}:{1} tipo '{2}' no válido. Admitidos: {3}".format(
                cuerpo, id_norm, tipo, TIPOS
            )
        )
    if not isinstance(decl["polaridad"], bool):
        raise ValueError(
            "{0}:{1} polaridad debe ser bool".format(cuerpo, id_norm)
        )

    # CORRECCIÓN 6: depende_de y gobierna deben ser list/tuple/set
    def _norm_lista(campo: str) -> List[str]:
        raw = decl.get(campo, [])
        if raw is None:
            return []
        if isinstance(raw, str):
            raise ValueError(
                "{0}:{1} '{2}' no puede ser str (sería convertido a caracteres)".format(
                    cuerpo, id_norm, campo
                )
            )
        if not isinstance(raw, (list, tuple, set)):
            raise ValueError(
                "{0}:{1} '{2}' debe ser list/tuple/set".format(cuerpo, id_norm, campo)
            )
        return [str(x).strip() for x in raw if str(x).strip()]

    return {
        "id": id_norm,
        "cuerpo": cuerpo,
        "tipo": tipo,
        "sujeto": str(decl["sujeto"]).strip(),
        "relacion": str(decl["relacion"]).strip(),
        "objeto": str(decl["objeto"]).strip(),
        "polaridad": bool(decl["polaridad"]),
        "cota": None if decl.get("cota") is None else str(decl["cota"]).strip(),
        "depende_de": _norm_lista("depende_de"),
        "gobierna": _norm_lista("gobierna"),
        "enunciado": str(decl.get("enunciado", "")),
    }

# ===============================================================
# FIN 6.2
# ===============================================================


# ===============================================================
# 6.3 — CLAVE Y REFERENCIA
# ===============================================================

def clave(d: Dict) -> Tuple[str, str, str]:
    return (
        d["sujeto"].lower().strip(),
        d["relacion"].lower().strip(),
        d["objeto"].lower().strip(),
    )


def ref(d: Dict) -> str:
    return "{0}:{1}".format(d["cuerpo"], d["id"])

# ===============================================================
# FIN 6.3
# ===============================================================


# ===============================================================
# 6.4 — DETECCIÓN DE CONTRADICCIONES
# ===============================================================

def contradiccion_directa(decls: List[Dict]) -> List[Dict]:
    grupos: Dict[Tuple[str, str, str], List[Dict]] = {}
    for d in decls:
        grupos.setdefault(clave(d), []).append(d)

    choques: List[Dict] = []
    for k, grupo in grupos.items():
        afirman = [d for d in grupo if d["polaridad"]]
        niegan = [d for d in grupo if not d["polaridad"]]
        for a in afirman:
            for n in niegan:
                choques.append({
                    "tipo": "contradiccion_directa",
                    "tripleta": " - ".join(k),
                    "declaracion_1": {
                        "id": a["id"],
                        "ubicacion": ref(a),
                        "enunciado": a["enunciado"],
                    },
                    "declaracion_2": {
                        "id": n["id"],
                        "ubicacion": ref(n),
                        "enunciado": n["enunciado"],
                    },
                    "mensaje": (
                        "Contradicción en '{0}': {1} AFIRMA vs {2} NIEGA".format(
                            " - ".join(k), ref(a), ref(n)
                        )
                    ),
                })
    return choques


def contradiccion_de_cota(decls: List[Dict]) -> List[Dict]:
    """CORRECCIÓN 12: normalización textual segura de cota (strip + espacios)."""
    grupos: Dict[Tuple[str, str], List[Dict]] = {}
    for d in decls:
        if d["cota"] is None:
            continue
        grupos.setdefault(
            (d["sujeto"].lower().strip(), d["relacion"].lower().strip()),
            [],
        ).append(d)

    choques: List[Dict] = []
    for (suj, rel), grupo in grupos.items():
        porcota: Dict[str, List[str]] = {}
        for d in grupo:
            # normalización textual segura
            cota_norm = " ".join(str(d["cota"]).split())
            porcota.setdefault(cota_norm, []).append(ref(d))
        if len(porcota) > 1:
            choques.append({
                "tipo": "contradiccion_de_cota",
                "sujeto": suj,
                "relacion": rel,
                "cotas": porcota,
                "mensaje": (
                    "Contradicción de cota en '{0} {1}'. Cotas: {2}".format(
                        suj, rel, list(porcota.keys())
                    )
                ),
            })
    return choques

# ===============================================================
# FIN 6.4
# ===============================================================


# ===============================================================
# 6.5 — MEDICIÓN DE PARES (TR1)
# ===============================================================

def _medir_pares(theta: list) -> dict:
    n = len(theta)
    pares_tot = n * (n - 1) // 2 if n >= 2 else 0
    compatibles = 0
    novedosos = 0
    redundantes = 0
    incompatibles = 0
    for i in range(n):
        Di = theta[i]["dominios"]
        for j in range(i + 1, n):
            Dj = theta[j]["dominios"]
            if not (Di & Dj):
                incompatibles += 1
                continue
            compatibles += 1
            union = Di | Dj
            if union != Di and union != Dj:
                novedosos += 1
            else:
                redundantes += 1
    return {
        "theta_n": n,
        "pares_totales": pares_tot,
        "pares_compatibles": compatibles,
        "pares_novedosos": novedosos,
        "pares_redundantes": redundantes,
        "pares_incompatibles": incompatibles,
        "im_vs_theta": (
            "GENERATIVO"
            if n > 0 and novedosos > n
            else ("ESTANCADO" if n > 0 else "SIN_DATOS")
        ),
        "identidad_pares": (compatibles + incompatibles == pares_tot),
        "identidad_compatibles": (novedosos + redundantes == compatibles),
    }

# ===============================================================
# FIN 6.5
# ===============================================================


# ===============================================================
# 6.6 — VALIDACIÓN DEL CONTRATO
# ===============================================================

def _validar_contrato(cont: Dict[str, Any]) -> None:
    """
    Valida que el CONTENEDOR cumpla el esquema contractual.
    CORRECCIONES 2 y 4:
    - validar acceso_archivos y validar_esquema como listas
    - validación completa de capacidades_meta (1:1, campos, sin huérfanas)
    """

    # -----------------------------------------------------------
    # Lista de claves que el contrato DEBE tener obligatoriamente
    # -----------------------------------------------------------
    obligatorias = (
        "esquema", "version_contrato", "version_modulo",
        "id", "nombre", "rol", "descripcion",
        "funcion", "no_hace", "autoridad",
        "conocimiento_exportable", "requiere",
        "autoriza_engine", "consultas_soportadas",
        "capacidades", "capacidades_meta",
        "reporting", "estados_validos", "invariantes",
        "estabilidad", "compatible_desde", "api_engine",
        "acceso_archivos", "validar_esquema",
    )

    # -----------------------------------------------------------
    # Comprueba si falta alguna clave obligatoria
    # -----------------------------------------------------------
    faltantes = [k for k in obligatorias if k not in cont]
    if faltantes:
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: CONTENEDOR incompleto. Faltan: {faltantes}"
        )

    # -----------------------------------------------------------
    # Verifica que el esquema sea exactamente el esperado
    # -----------------------------------------------------------
    if cont.get("esquema") != ESQUEMA_CONTRATO:
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: esquema incompatible: {cont.get('esquema')}"
        )

    # -----------------------------------------------------------
    # Verifica que la versión del contrato sea la correcta
    # -----------------------------------------------------------
    if str(cont.get("version_contrato")) != VERSION_CONTRATO:
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: version_contrato inválida: {cont.get('version_contrato')}"
        )

    # -----------------------------------------------------------
    # CORRECCIÓN 2:
    # acceso_archivos y validar_esquema deben ser listas
    # -----------------------------------------------------------
    for campo in ("acceso_archivos", "validar_esquema"):
        val = cont.get(campo)
        if not isinstance(val, list):
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: '{campo}' debe ser list"
            )

    # -----------------------------------------------------------
    # CORRECCIÓN 4:
    # capacidades y capacidades_meta deben coincidir 1:1
    # (ninguna capacidad sin meta, ninguna meta huérfana)
    # -----------------------------------------------------------
    caps = cont.get("capacidades") or {}
    meta_caps = cont.get("capacidades_meta") or {}
    if set(caps.keys()) != set(meta_caps.keys()):
        solo_caps = set(caps.keys()) - set(meta_caps.keys())
        solo_meta = set(meta_caps.keys()) - set(caps.keys())
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: desajuste capacidades/capacidades_meta. "
            f"solo_en_capacidades={solo_caps} solo_en_meta={solo_meta}"
        )

    # -----------------------------------------------------------
    # Cada entrada de capacidades_meta debe ser un diccionario
    # y debe contener los campos mínimos obligatorios
    # -----------------------------------------------------------
    for nombre_cap, entrada in meta_caps.items():
        if not isinstance(entrada, dict):
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: capacidades_meta['{nombre_cap}'] debe ser dict"
            )

        # Campos que siempre deben existir y ser texto
        for campo in ("descripcion", "entrada", "salida"):
            if campo not in entrada or not isinstance(entrada[campo], str):
                raise ContratoInvalido(
                    f"{NOMBRE_MODULO}: capacidades_meta['{nombre_cap}'] "
                    f"requiere '{campo}: str'"
                )

        # Campos opcionales que, si existen, deben ser listas
        for campo in ("validar_esquema", "acceso_archivos"):
            if campo in entrada and not isinstance(entrada[campo], list):
                raise ContratoInvalido(
                    f"{NOMBRE_MODULO}: capacidades_meta['{nombre_cap}']['{campo}'] "
                    f"debe ser list"
                )

# ===============================================================
# FIN 6.6
# ===============================================================

# ===============================================================
# PARTE 7 — LÍMITE AXIOMÁTICO
# ===============================================================

# ===============================================================
# 7.1 — LÍMITE AXIOMÁTICO
# ===============================================================

def limite_axiomático(
    declaraciones_externas: Optional[Dict[str, List[Dict]]] = None,
    decls: Optional[List[Dict]] = None,
    errores: Optional[List[Dict]] = None,
) -> Dict[str, Any]:
    """
    Determina el límite de derivación axiomática.
    CORRECCIONES 9, 10, 27:
    - resolución transitiva de dependencias
    - detección de ciclos de cualquier longitud
    - estados: NO_DERIVABLE, PREMISA_FALTANTE, CIRCULAR
    """

    # -----------------------------------------------------------
    # Si no se recibe una instantánea, se recolecta una nueva
    # -----------------------------------------------------------
    if decls is None or errores is None:
        decls, errores = recolectar(declaraciones_externas)

    # -----------------------------------------------------------
    # Conjuntos de trabajo
    # -----------------------------------------------------------
    ids_presentes: Set[str] = {d["id"] for d in decls}
    premisas_disponibles: List[str] = sorted(ids_presentes)
    premisas_faltantes: List[Dict[str, Any]] = []
    dependencias_no_satisfechas: List[Dict[str, Any]] = []
    dependencias_circulares: List[Dict[str, Any]] = []
    limites: List[Dict[str, Any]] = []

    # -----------------------------------------------------------
    # Grafo de dependencias:
    # cada declaración apunta a las que necesita (depende_de)
    # -----------------------------------------------------------
    grafo: Dict[str, List[str]] = {
        d["id"]: list(d.get("depende_de") or []) for d in decls
    }

    # -----------------------------------------------------------
    # Detección de ciclos de cualquier longitud (CORRECCIÓN 10)
    # Usa DFS para encontrar ciclos en el grafo
    # -----------------------------------------------------------
    def _detectar_ciclos() -> List[List[str]]:
        ciclos: List[List[str]] = []
        visitado: Set[str] = set()
        stack: List[str] = []
        en_stack: Set[str] = set()

        def dfs(nodo: str) -> None:
            visitado.add(nodo)
            stack.append(nodo)
            en_stack.add(nodo)
            for vecino in grafo.get(nodo, []):
                if vecino not in grafo:
                    continue
                if vecino not in visitado:
                    dfs(vecino)
                elif vecino in en_stack:
                    # Se encontró un ciclo
                    idx = stack.index(vecino)
                    ciclo = stack[idx:] + [vecino]
                    # Evitar registrar el mismo ciclo varias veces
                    ciclo_norm = tuple(sorted(set(ciclo[:-1])))
                    if ciclo_norm and ciclo_norm not in {
                        tuple(sorted(set(c[:-1]))) for c in ciclos
                    }:
                        ciclos.append(ciclo)
            stack.pop()
            en_stack.discard(nodo)

        for n in list(grafo.keys()):
            if n not in visitado:
                dfs(n)
        return ciclos

    # -----------------------------------------------------------
    # Registrar cada ciclo encontrado
    # -----------------------------------------------------------
    for ciclo in _detectar_ciclos():
        dependencias_circulares.append({
            "ciclo": ciclo,
            "mensaje": "Dependencia circular: {0}".format(" → ".join(ciclo)),
        })
        limites.append({
            "tipo": "CIRCULAR",
            "ciclo": ciclo,
            "estado": "CIRCULAR",
        })

    # -----------------------------------------------------------
    # Resolución transitiva de premisas faltantes (CORRECCIÓN 9)
    # Si A depende de B y B depende de C, y C no existe,
    # entonces A también tiene premisa faltante
    # -----------------------------------------------------------
    def _premisas_transitivas(
        start: str, vistos: Optional[Set[str]] = None
    ) -> Set[str]:
        if vistos is None:
            vistos = set()
        if start in vistos:
            return set()
        vistos.add(start)
        faltantes: Set[str] = set()
        for dep in grafo.get(start, []):
            if dep not in ids_presentes:
                faltantes.add(dep)
            else:
                faltantes |= _premisas_transitivas(dep, vistos)
        return faltantes

    # -----------------------------------------------------------
    # Revisar cada declaración y registrar premisas faltantes
    # -----------------------------------------------------------
    for d in decls:
        faltantes = sorted(_premisas_transitivas(d["id"]))
        if faltantes:
            premisas_faltantes.append({
                "declaracion": d["id"],
                "tipo": d["tipo"],
                "premisas_faltantes": faltantes,
                "ubicacion": ref(d),
            })
            dependencias_no_satisfechas.append({
                "declaracion": d["id"],
                "dependencias_faltantes": faltantes,
                "mensaje": (
                    "La declaración '{0}' depende transitivamente de premisas "
                    "no presentes: {1}".format(d["id"], faltantes)
                ),
            })
            limites.append({
                "tipo": "PREMISA_FALTANTE",
                "declaracion": d["id"],
                "premisas_faltantes": faltantes,
                "estado": "NO_DERIVABLE",
            })

    # -----------------------------------------------------------
    # Resumen de alcance
    # -----------------------------------------------------------
    alcance = {
        "total_declaraciones": len(decls),
        "con_dependencias_satisfechas": (
            len(decls)
            - len(dependencias_no_satisfechas)
            - len(dependencias_circulares)
        ),
        "con_premisas_faltantes": len(premisas_faltantes),
        "con_dependencias_circulares": len(dependencias_circulares),
    }

    # -----------------------------------------------------------
    # Resultado final
    # -----------------------------------------------------------
    return {
        "contenedor": NOMBRE_MODULO,
        "premisas_disponibles": premisas_disponibles,
        "premisas_faltantes": premisas_faltantes,
        "dependencias_no_satisfechas": dependencias_no_satisfechas,
        "dependencias_circulares": dependencias_circulares,
        "limites": limites,
        "alcance": alcance,
        "errores_recoleccion": errores,
        "nota": (
            "Límite axiomático ≠ contradicción. "
            "Si falta una premisa requerida (incluso transitiva), se declara el límite. "
            "No se inventan premisas."
        ),
    }

# ===============================================================
# FIN 7.1
# ===============================================================

# ===============================================================
# PARTE 8 — CAPACIDADES PÚBLICAS
# ===============================================================

# ===============================================================
# 8.1 — RECOLECCIÓN (FUENTE ÚNICA DE VERDAD)
# ===============================================================

def recolectar(
    declaraciones_externas: Optional[Dict[str, List[Dict]]] = None,
) -> Tuple[List[Dict], List[Dict]]:
    """
    Carga y normaliza todas las declaraciones del módulo.
    CORRECCIONES 5 y 21:
    - detección de IDs duplicados
    - trazabilidad de errores de carga
    """

    # -----------------------------------------------------------
    # Listas de resultado
    # -----------------------------------------------------------
    decls: List[Dict] = []
    errores: List[Dict] = []
    ids_vistos: Dict[str, str] = {}  # id → primera ubicación

    # -----------------------------------------------------------
    # 1. Recorrer todos los archivos .py del módulo
    # -----------------------------------------------------------
    for archivo in sorted(_DIR.glob("**/*.py")):
        if archivo.name == "__init__.py":
            continue

        # Cargar declaraciones del archivo
        raw, err = _cargar_declaraciones_desde_archivo(archivo)

        # Si hubo error de carga, registrarlo y pasar al siguiente
        if err:
            errores.append({
                "archivo": archivo.name,
                "error": err,
                "tipo": "error_carga",
            })
            continue

        # Normalizar cada declaración encontrada
        for d in raw:
            try:
                norm = normalizar(d, archivo.stem)

                # CORRECCIÓN 5: detectar ID duplicado
                if norm["id"] in ids_vistos:
                    errores.append({
                        "tipo": "id_duplicado",
                        "id": norm["id"],
                        "primera_ubicacion": ids_vistos[norm["id"]],
                        "segunda_ubicacion": ref(norm),
                    })
                    continue  # no se agrega el duplicado

                # Registrar el ID y agregar la declaración
                ids_vistos[norm["id"]] = ref(norm)
                decls.append(norm)

            except ValueError as e:
                # Error de normalización (id vacío, polaridad inválida, etc.)
                errores.append({
                    "archivo": archivo.name,
                    "error": str(e),
                    "tipo": "error_normalizacion",
                })

    # -----------------------------------------------------------
    # 2. Cargar declaraciones desde VPSI.py (si existe)
    # -----------------------------------------------------------
    vpsi = _ruta_vpsi()
    if vpsi is not None:
        raw, err = _cargar_declaraciones_desde_archivo(vpsi)
        if err:
            errores.append({
                "archivo": str(vpsi.name),
                "error": err,
                "tipo": "error_carga",
            })
        else:
            for d in raw:
                try:
                    norm = normalizar(d, "VPSI")
                    if norm["id"] in ids_vistos:
                        errores.append({
                            "tipo": "id_duplicado",
                            "id": norm["id"],
                            "primera_ubicacion": ids_vistos[norm["id"]],
                            "segunda_ubicacion": ref(norm),
                        })
                        continue
                    ids_vistos[norm["id"]] = ref(norm)
                    decls.append(norm)
                except ValueError as e:
                    errores.append({
                        "archivo": "VPSI",
                        "error": str(e),
                        "tipo": "error_normalizacion",
                    })

    # -----------------------------------------------------------
    # 3. Incorporar declaraciones externas (si se reciben)
    # -----------------------------------------------------------
    if declaraciones_externas:
        for nombre, lista in declaraciones_externas.items():
            if not isinstance(lista, list):
                continue
            for d in lista:
                try:
                    norm = normalizar(d, nombre)
                    if norm["id"] in ids_vistos:
                        errores.append({
                            "tipo": "id_duplicado",
                            "id": norm["id"],
                            "primera_ubicacion": ids_vistos[norm["id"]],
                            "segunda_ubicacion": ref(norm),
                        })
                        continue
                    ids_vistos[norm["id"]] = ref(norm)
                    decls.append(norm)
                except ValueError as e:
                    errores.append({
                        "modulo": nombre,
                        "error": str(e),
                        "tipo": "error_normalizacion",
                    })

    # -----------------------------------------------------------
    # Resultado: (declaraciones normalizadas, errores encontrados)
    # -----------------------------------------------------------
    return decls, errores

# ===============================================================
# FIN 8.1
# ===============================================================
# ===============================================================
# 8.2 — IDS DE DOMINIO K/O
# ===============================================================

def ids_dominio_k_o(
    declaraciones_externas: Optional[Dict[str, List[Dict]]] = None,
) -> List[str]:
    """
    Determinismo estructural absoluto.
    Una declaración pertenece al dominio K/O únicamente si su
    propiedad "gobierna" declara explícitamente una relación
    perteneciente a DOMINIOS_K_O.

    Cero búsqueda de texto libre.
    Cero heurística.
    Cero adivinación por palabras clave en sujeto, objeto o enunciado.

    Si la estructura no lo declara, el sistema no lo asume.
    """

    # -----------------------------------------------------------
    # Cargar declaraciones normalizadas
    # -----------------------------------------------------------
    decls, _ = recolectar(declaraciones_externas)

    # -----------------------------------------------------------
    # Recorrer cada declaración y filtrar solo por gobierna
    # -----------------------------------------------------------
    ids: List[str] = []
    for d in decls:
        gobs = {
            str(g).lower().strip()
            for g in (d.get("gobierna") or [])
        }
        # Pertenencia estructural estricta
        if gobs & DOMINIOS_K_O:
            ids.append(d["id"])

    # -----------------------------------------------------------
    # Resultado determinista, ordenado y sin duplicados
    # -----------------------------------------------------------
    return sorted(set(ids))

# ===============================================================
# FIN 8.2
# ===============================================================

# ===============================================================
# 8.3 — GENERATIVIDAD (TR1)
# ===============================================================

def generatividad() -> dict:
    """
    CORRECCIÓN 14: normalizar dominios de la capa operativa con DOMINIO_CANONICO.
    """
    decls, errores = recolectar()

    oper = []
    for d in decls:
        if d.get("tipo") not in ("teorema", "axioma"):
            continue
        gob = d.get("gobierna") or []
        if not gob:
            continue
        dominios_norm = set()
        for g in gob:
            key = str(g).lower().strip()
            dominios_norm.add(DOMINIO_CANONICO.get(key, key.upper()[:3]))
        oper.append({
            "id": d["id"],
            "tipo": d["tipo"],
            "dominios": dominios_norm,
        })
    m_op = _medir_pares(oper)
    dominios_op = sorted({g for n in oper for g in n["dominios"]})

    can = [
        {"id": tid, "tipo": "teorema", "dominios": set(doms)}
        for tid, doms in THETA_24.items()
    ]
    m_can = _medir_pares(can)
    dominios_can = sorted({g for n in can for g in n["dominios"]})

    ids_en_repo = {str(d.get("id", "")) for d in decls}
    ids_presentes = sorted(i for i in THETA_CANONICO if i in ids_en_repo)
    ids_faltantes = sorted(THETA_CANONICO - set(ids_presentes))
    ids_sin_dominio = sorted(tid for tid, doms in THETA_24.items() if not doms)

    u1_proxy = (
        "NO_STAGNANT"
        if m_can.get("pares_novedosos", 0) > 0 or m_op.get("pares_novedosos", 0) > 0
        else "REVISAR"
    )

    return {
        "contenedor": "axiomas",
        "theta_n": m_op["theta_n"],
        "pares_totales": m_op["pares_totales"],
        "pares_compatibles": m_op["pares_compatibles"],
        "pares_novedosos": m_op["pares_novedosos"],
        "pares_redundantes": m_op["pares_redundantes"],
        "pares_incompatibles": m_op["pares_incompatibles"],
        "im_vs_theta": m_op["im_vs_theta"],
        "identidad_pares": m_op["identidad_pares"],
        "identidad_compatibles": m_op["identidad_compatibles"],
        "dominios": dominios_op,
        "u1_proxy": u1_proxy,
        "errores_recoleccion": len(errores),
        "por_tipo_theta": {
            "axioma": sum(1 for n in oper if n["tipo"] == "axioma"),
            "teorema": sum(1 for n in oper if n["tipo"] == "teorema"),
        },
        "canonica": {
            **m_can,
            "ids_presentes": ids_presentes,
            "ids_faltantes": ids_faltantes,
            "ids_sin_dominio": ids_sin_dominio,
            "dominios": dominios_can,
            "dominios_formales": {k: sorted(v) for k, v in THETA_24.items()},
            "referencia_formal": {
                "theta_n": 24,
                "pares_totales": 276,
                "pares_compatibles": 183,
                "pares_novedosos": 153,
                "pares_redundantes": 30,
                "pares_incompatibles": 93,
                "nota": (
                    "|Im(⊕)|=153 > 24=|Θ| — enumeración exacta. "
                    "El CI recalcula; no hardcodea."
                ),
            },
            "coincide_paper": (
                m_can.get("pares_totales") == 276
                and m_can.get("pares_compatibles") == 183
                and m_can.get("pares_novedosos") == 153
                and m_can.get("pares_redundantes") == 30
                and m_can.get("pares_incompatibles") == 93
            ),
        },
        "ids_dominio_k_o": ids_dominio_k_o(),
        "nota": (
            "Capa operativa = grafo del repo normalizado. "
            "Capa canónica = THETA_24 formal. "
            "Identidades C+I=T y N+R=C deben cumplirse."
        ),
    }

# ===============================================================
# FIN 8.3
# ===============================================================


# ===============================================================
# 8.4 — COHERENCIA (barrer / verificar)
# ===============================================================

def barrer(
    declaraciones_externas: Optional[Dict[str, List[Dict]]] = None,
) -> Dict:
    decls, errores = recolectar(declaraciones_externas)
    choques = contradiccion_directa(decls) + contradiccion_de_cota(decls)

    if (choques or errores) and DiagnosticoGlobal is not None:
        try:
            DiagnosticoGlobal.recibir_reporte(
                modulo="axiomas",
                errores=(
                    [{"tipo": "choque", "detalle": c} for c in choques]
                    + [{"tipo": "error_carga", "detalle": e} for e in errores]
                ),
            )
        except Exception:
            pass

    cuerpos = sorted({d["cuerpo"] for d in decls})
    por_tipo = {t: sum(1 for d in decls if d["tipo"] == t) for t in TIPOS}

    return {
        "coherente": not (choques or errores),
        "choques": choques,
        "errores": errores,
        "declaraciones": len(decls),
        "cuerpos": cuerpos,
        "por_tipo": por_tipo,
        "ids_dominio_k_o": (
            ids_dominio_k_o(declaraciones_externas)
            if not (choques or errores)
            else []
        ),
    }


def verificar_salida(salida: Dict) -> bool:
    return bool(salida.get("coherente", False))


def verificar(
    declaraciones_externas: Optional[Dict[str, List[Dict]]] = None,
) -> Dict[str, Any]:
    """API compatible. El alias contractual 'verificar' resuelve a barrer."""
    return barrer(declaraciones_externas)

# ===============================================================
# FIN 8.4
# ===============================================================


# ===============================================================
# 8.5 — CONSULTAS DE DECLARACIONES
# ===============================================================

def declaraciones(
    declaraciones_externas: Optional[Dict[str, List[Dict]]] = None,
) -> List[Dict]:
    """CORRECCIÓN 17: evita doble recolección innecesaria cuando es posible."""
    decls, errores = recolectar(declaraciones_externas)
    choques = contradiccion_directa(decls) + contradiccion_de_cota(decls)
    if choques or errores:
        return []
    return decls


def axiomas(
    declaraciones_externas: Optional[Dict[str, List[Dict]]] = None,
) -> List[Dict]:
    return declaraciones(declaraciones_externas)


def por_dominio(
    dominio: str,
    declaraciones_externas: Optional[Dict[str, List[Dict]]] = None,
) -> List[Dict]:
    """CORRECCIÓN 13: normalizar dominio con DOMINIO_CANONICO."""
    key = str(dominio).lower().strip()
    dom_can = DOMINIO_CANONICO.get(key, key.upper()[:3] if len(key) >= 3 else key.upper())
    decls, _ = recolectar(declaraciones_externas)
    out = []
    for d in decls:
        gobs_raw = [str(g).lower().strip() for g in (d.get("gobierna") or [])]
        gobs_can = {DOMINIO_CANONICO.get(g, g.upper()[:3]) for g in gobs_raw}
        if dom_can in gobs_can or key in gobs_raw:
            out.append(d)
    return out


def buscar_por_id(id_decl: str) -> Optional[Dict]:
    """CORRECCIÓN 18: no seleccionar arbitrariamente si hay duplicados."""
    decls, errores = recolectar()
    matches = [d for d in decls if d.get("id") == id_decl]
    if len(matches) == 0:
        return None
    if len(matches) > 1:
        # conflicto de ID duplicado — no escoger
        return None
    return matches[0]

# ===============================================================
# FIN 8.5
# ===============================================================
# ===============================================================
# 8.6 — INVENTARIO
# ===============================================================

def inventario(peticion=None) -> Dict:
    decls, errores = recolectar()
    lim = limite_axiomático(decls=decls, errores=errores)
    return {
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "tipos": list(TIPOS),
        "declaraciones": len(decls),
        "por_tipo": {t: sum(1 for d in decls if d["tipo"] == t) for t in TIPOS},
        "cuerpos": sorted({d["cuerpo"] for d in decls}),
        "errores": errores,
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "capacidades_resueltas": list(CAPACIDADES_RESUELTAS.keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "autoridad": CONTENEDOR.get("autoridad"),
        "conocimiento_exportable": CONTENEDOR.get("conocimiento_exportable"),
        "consultas_soportadas": CONTENEDOR.get("consultas_soportadas"),
        "invariantes": CONTENEDOR.get("invariantes"),
        "vigila": [
            "contradiccion_directa",
            "contradiccion_de_cota",
            "limite_axiomático",
        ],
        "ids_dominio_k_o": ids_dominio_k_o(),
        "limite_axiomático": {
            "premisas_faltantes": len(lim.get("premisas_faltantes") or []),
            "dependencias_no_satisfechas": len(
                lim.get("dependencias_no_satisfechas") or []
            ),
            "dependencias_circulares": len(
                lim.get("dependencias_circulares") or []
            ),
            "alcance": lim.get("alcance"),
        },
        "operaciones_arquitectonicas": {
            "ejecutar_total": "ejecutar_total" in CONTENEDOR.get("capacidades", {}),
            "inspeccionar": "inspeccionar" in CONTENEDOR.get("capacidades", {}),
            "registrar_inventario": (
                "registrar_inventario" in CONTENEDOR.get("capacidades", {})
            ),
        },
        "nota": (
            "Def-5.3.1 y dominio O viven en los cuerpos cargados; "
            "este módulo los vigila y expone, no los clasifica en entrada."
        ),
    }

# ===============================================================
# FIN 8.6
# ===============================================================

# ===============================================================
# PARTE 9 — REPORTING
# ===============================================================

# ===============================================================
# 9.1 — REPORTE
# ===============================================================

def reporte() -> Dict[str, Any]:
    """CORRECCIÓN 29: una sola instantánea."""
    decls, errores = recolectar()
    choques = contradiccion_directa(decls) + contradiccion_de_cota(decls)
    lim = limite_axiomático(decls=decls, errores=errores)
    coherente = not (choques or errores)
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "estado": ESTADO_OPERATIVO if coherente else ESTADO_DEGRADADO,
        "coherente": coherente,
        "declaraciones": len(decls),
        "choques": len(choques),
        "errores": len(errores),
        "cuerpos": sorted({d["cuerpo"] for d in decls}),
        "por_tipo": {t: sum(1 for d in decls if d["tipo"] == t) for t in TIPOS},
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "capacidades_resueltas": list(CAPACIDADES_RESUELTAS.keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "autoridad": CONTENEDOR.get("autoridad"),
        "conocimiento_exportable": CONTENEDOR.get("conocimiento_exportable"),
        "consultas_soportadas": CONTENEDOR.get("consultas_soportadas"),
        "limite_axiomático": {
            "premisas_faltantes": len(lim.get("premisas_faltantes") or []),
            "dependencias_no_satisfechas": len(
                lim.get("dependencias_no_satisfechas") or []
            ),
            "dependencias_circulares": len(
                lim.get("dependencias_circulares") or []
            ),
        },
        "operaciones_arquitectonicas": {
            "ejecutar_total": "ejecutar_total" in CONTENEDOR.get("capacidades", {}),
            "inspeccionar": "inspeccionar" in CONTENEDOR.get("capacidades", {}),
        },
    }

# ===============================================================
# FIN 9.1
# ===============================================================
# ===============================================================
# 9.2 — DIAGNÓSTICO
# ===============================================================

def diagnostico() -> Dict[str, Any]:
    """CORRECCIÓN 30: distinguir problemas / advertencias / limites."""
    decls, errores = recolectar()
    choques = contradiccion_directa(decls) + contradiccion_de_cota(decls)
    lim = limite_axiomático(decls=decls, errores=errores)

    problemas = []
    advertencias = []
    recomendaciones = []
    limites_reportados = []

    if errores:
        problemas.append({"tipo": "errores_carga", "detalle": errores})
        recomendaciones.append("Revisar archivos de cuerpos con error de carga")

    if choques:
        problemas.append({
            "tipo": "contradicciones",
            "cantidad": len(choques),
            "detalle": choques[:5],
        })
        recomendaciones.append("Resolver contradicciones directas o de cota")

    if lim.get("premisas_faltantes"):
        limites_reportados.append({
            "tipo": "PREMISA_FALTANTE",
            "cantidad": len(lim["premisas_faltantes"]),
            "detalle": lim["premisas_faltantes"][:5],
        })
        recomendaciones.append(
            "Existen declaraciones cuyas premisas no están en el cuerpo axiomático"
        )

    if lim.get("dependencias_circulares"):
        limites_reportados.append({
            "tipo": "CIRCULAR",
            "cantidad": len(lim["dependencias_circulares"]),
        })

    if not decls:
        advertencias.append("No hay declaraciones cargadas")
        recomendaciones.append("Verificar que existan cuerpos .py con DECLARACIONES")

    estado = ESTADO_OPERATIVO
    if problemas:
        estado = ESTADO_DEGRADADO
    if not decls and not problemas:
        estado = ESTADO_NO_INICIADO

    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "estado": estado,
        "problemas": problemas,
        "advertencias": advertencias,
        "recomendaciones": recomendaciones,
        "limites": limites_reportados,
        "coherente": not (choques or errores),
        "declaraciones": len(decls),
        "choques_n": len(choques),
        "errores_n": len(errores),
        "premisas_faltantes_n": len(lim.get("premisas_faltantes") or []),
    }

# ===============================================================
# FIN 9.2
# ===============================================================


# ===============================================================
# PARTE 10 — RESOLUCIÓN ESTRICTA (sin mutar CONTENEDOR)
# ===============================================================
# ===============================================================
# 10.1 — MAPA DE CAPACIDADES
# ===============================================================

# CORRECCIÓN 3 y 24/25: mapa de resolución separado; no mutar CONTENEDOR
_CAP_MAP = {
    "barrer": barrer,
    "verificar_salida": verificar_salida,
    "inventario": inventario,
    "axiomas": axiomas,
    "declaraciones": declaraciones,
    "generatividad": generatividad,
    "por_dominio": por_dominio,
    "ids_dominio_k_o": ids_dominio_k_o,
    "recolectar": recolectar,
    "reporte": reporte,
    "diagnostico": diagnostico,
    "buscar_por_id": buscar_por_id,
    "verificar": barrer,          # alias contractual → barrer
    "limite_axiomático": limite_axiomático,
    "ejecutar_total": ejecutar_total,
    "inspeccionar": inspeccionar,
}

# ===============================================================
# FIN 10.1
# ===============================================================


# ===============================================================
# 10.2 — RESOLUCIÓN DE CAPACIDADES
# ===============================================================

# Estructura paralela de capacidades resueltas (no muta el contrato)
CAPACIDADES_RESUELTAS: Dict[str, Any] = {}


def _resolver_capacidades() -> None:
    """CORRECCIÓN 24/25: no mutar CONTENEDOR['capacidades']."""
    global CAPACIDADES_RESUELTAS
    resueltas: Dict[str, Any] = {}
    for nombre, ref in CONTENEDOR["capacidades"].items():
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
            f"tiene tipo inválido: {type(ref).__name__}"
        )
    CAPACIDADES_RESUELTAS = resueltas
    # CONTENEDOR["capacidades"] permanece como declaración contractual.
    # No se muta.

# ===============================================================
# FIN 10.2
# ===============================================================


# ===============================================================
# 10.3 — EJECUCIÓN DE VALIDACIÓN Y RESOLUCIÓN
# ===============================================================

_validar_contrato(CONTENEDOR)
_resolver_capacidades()

# ===============================================================
# FIN 10.3
# ===============================================================
# ===============================================================
# PARTE 11 — EXPORTACIONES
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
    "AXIOMA",
    "LEMA",
    "TEOREMA",
    "COROLARIO",
    "DEFINICION",
    "TIPOS",
    "normalizar",
    "clave",
    "ref",
    "recolectar",
    "por_dominio",
    "ids_dominio_k_o",
    "declaraciones",
    "axiomas",
    "contradiccion_directa",
    "contradiccion_de_cota",
    "barrer",
    "verificar_salida",
    "inventario",
    "generatividad",
    "verificar",
    "reporte",
    "diagnostico",
    "buscar_por_id",
    "limite_axiomático",
    "ejecutar_total",
    "inspeccionar",
    "ContratoInvalido",
    "CAPACIDADES_RESUELTAS",
]

# ===============================================================
# FIN PARTE 11
# ===============================================================


# ===============================================================
# FIN DEL MÓDULO
# ===============================================================
