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
    "requiere": [
    "CE", "AX", "FO", "MC", "SF",
    "CA", "CX", "DI", "RE", "VX",
    "TX", "CH", "CIT", "DGCO", "UI",
    "CC", "TT", "SC",
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
        #  X4.1 Unidades privadas
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
        # X4.2 Unidades públicas
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
        "ejecutar_total": callable(ejecutar_total),
        "inspeccionar": True,
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

        "capacidades_declaradas": list(
            CONTENEDOR.get("capacidades", {}).keys()
        ),
        "capacidades_resueltas": list(CAPACIDADES_RESUELTAS.keys()),
        "capacidades_meta": list(
            CONTENEDOR.get("capacidades_meta", {}).keys()
        ),

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
            "conocimiento_exportable": CONTENEDOR.get(
                "conocimiento_exportable"
            ),
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
# ===============================================================# ===============================================================
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
# 7.1 — LÍMITE AXIOMÁTICO
# ===============================================================

def limite_axiomático(
    declaraciones_externas: Optional[Dict[str, List[Dict]]] = None,
    decls: Optional[List[Dict]] = None,
    errores: Optional[List[Dict]] = None,
) -> Dict[str, Any]:
    """
    Determina el límite axiomático de las declaraciones recolectadas.

    PRINCIPIO:
    Una declaración solo puede considerarse derivable hasta donde sus
    dependencias declaradas estén disponibles y no exista una dependencia
    circular.

    Esta función:
    - trabaja sobre la instantánea recibida o recolecta una nueva;
    - no inventa premisas;
    - no modifica declaraciones;
    - no interpreta el contenido matemático de las declaraciones;
    - resuelve dependencias de forma transitiva;
    - detecta ciclos de cualquier longitud;
    - distingue ausencia de premisa de circularidad;
    - conserva los errores de recolección;
    - informa exclusivamente el límite estructural de derivación.
    """

    # -----------------------------------------------------------
    # 1. Obtener la instantánea de declaraciones
    # -----------------------------------------------------------
    if decls is None or errores is None:
        decls, errores = recolectar(declaraciones_externas)

    decls = list(decls or [])
    errores = list(errores or [])

    # -----------------------------------------------------------
    # 2. Índice de declaraciones presentes
    # -----------------------------------------------------------
    por_id: Dict[str, Dict[str, Any]] = {
        d["id"]: d for d in decls if isinstance(d, dict) and "id" in d
    }

    ids_presentes: Set[str] = set(por_id)

    premisas_disponibles: List[str] = sorted(ids_presentes)

    # -----------------------------------------------------------
    # 3. Grafo axiomático
    #
    # Cada declaración D declara de qué otras declaraciones depende.
    # No se agregan dependencias implícitas.
    # -----------------------------------------------------------
    grafo: Dict[str, List[str]] = {}

    for declaracion_id, declaracion in por_id.items():
        dependencias = declaracion.get("depende_de") or []

        if isinstance(dependencias, str):
            dependencias = [dependencias]

        grafo[declaracion_id] = [
            dep for dep in dependencias
            if isinstance(dep, str) and dep
        ]

    # -----------------------------------------------------------
    # 4. Detección de ciclos
    #
    # El ciclo es una propiedad del grafo, no una premisa faltante.
    # Se registra cada componente circular una sola vez.
    # -----------------------------------------------------------
    ciclos_encontrados: List[List[str]] = []
    ciclos_normalizados: Set[tuple] = set()

    estado_dfs: Dict[str, int] = {}
    pila: List[str] = []
    posicion_pila: Dict[str, int] = {}

    def _dfs_ciclo(nodo: str) -> None:
        estado_dfs[nodo] = 1
        posicion_pila[nodo] = len(pila)
        pila.append(nodo)

        for dependencia in grafo.get(nodo, []):
            if dependencia not in grafo:
                continue

            estado = estado_dfs.get(dependencia, 0)

            if estado == 0:
                _dfs_ciclo(dependencia)

            elif estado == 1:
                inicio = posicion_pila[dependencia]
                ciclo = pila[inicio:] + [dependencia]

                miembros = tuple(sorted(set(ciclo[:-1])))

                if miembros and miembros not in ciclos_normalizados:
                    ciclos_normalizados.add(miembros)
                    ciclos_encontrados.append(ciclo)

        pila.pop()
        posicion_pila.pop(nodo, None)
        estado_dfs[nodo] = 2

    for declaracion_id in grafo:
        if estado_dfs.get(declaracion_id, 0) == 0:
            _dfs_ciclo(declaracion_id)

    # -----------------------------------------------------------
    # 5. Conjunto de declaraciones afectadas por circularidad
    # -----------------------------------------------------------
    ids_circulares: Set[str] = {
        nodo
        for ciclo in ciclos_encontrados
        for nodo in ciclo[:-1]
    }

    dependencias_circulares: List[Dict[str, Any]] = []

    for ciclo in ciclos_encontrados:
        dependencias_circulares.append({
            "ciclo": ciclo,
            "declaraciones": sorted(set(ciclo[:-1])),
            "mensaje": (
                "Dependencia circular: {0}".format(
                    " → ".join(ciclo)
                )
            ),
        })

    # -----------------------------------------------------------
    # 6. Resolución transitiva de dependencias faltantes
    #
    # IMPORTANTE:
    # El conjunto 'camino' representa solamente la rama actual.
    # No se utiliza un conjunto global de visitados que pueda ocultar
    # dependencias legítimas de otra rama.
    #
    # La circularidad ya fue determinada estructuralmente arriba.
    # -----------------------------------------------------------
    def _resolver_faltantes(
        inicio: str,
        camino: Optional[Set[str]] = None,
    ) -> Set[str]:

        camino_actual: Set[str] = set(camino or ())

        if inicio in camino_actual:
            return set()

        camino_actual.add(inicio)

        faltantes: Set[str] = set()

        for dependencia in grafo.get(inicio, []):
            if dependencia not in ids_presentes:
                faltantes.add(dependencia)
                continue

            if dependencia in ids_circulares:
                continue

            faltantes.update(
                _resolver_faltantes(
                    dependencia,
                    camino_actual,
                )
            )

        return faltantes

    # -----------------------------------------------------------
    # 7. Clasificación de cada declaración
    # -----------------------------------------------------------
    premisas_faltantes: List[Dict[str, Any]] = []
    dependencias_no_satisfechas: List[Dict[str, Any]] = []
    limites: List[Dict[str, Any]] = []

    ids_no_derivables: Set[str] = set()

    for declaracion_id in sorted(por_id):
        declaracion = por_id[declaracion_id]

        # -------------------------------------------------------
        # Circularidad: tiene prioridad estructural.
        # -------------------------------------------------------
        if declaracion_id in ids_circulares:
            limites.append({
                "tipo": "CIRCULAR",
                "declaracion": declaracion_id,
                "estado": "CIRCULAR",
                "ubicacion": ref(declaracion),
            })
            continue

        # -------------------------------------------------------
        # Dependencias ausentes, incluyendo las transitivas.
        # -------------------------------------------------------
        faltantes = sorted(
            _resolver_faltantes(declaracion_id)
        )

        if faltantes:
            ids_no_derivables.add(declaracion_id)

            premisas_faltantes.append({
                "declaracion": declaracion_id,
                "tipo": declaracion.get("tipo"),
                "premisas_faltantes": faltantes,
                "ubicacion": ref(declaracion),
            })

            dependencias_no_satisfechas.append({
                "declaracion": declaracion_id,
                "dependencias_faltantes": faltantes,
                "mensaje": (
                    "La declaración '{0}' depende de premisas no "
                    "presentes: {1}".format(
                        declaracion_id,
                        faltantes,
                    )
                ),
            })

            limites.append({
                "tipo": "PREMISA_FALTANTE",
                "declaracion": declaracion_id,
                "premisas_faltantes": faltantes,
                "estado": "NO_DERIVABLE",
                "ubicacion": ref(declaracion),
            })

    # -----------------------------------------------------------
    # 8. Estados estructurales por declaración
    #
    # Una declaración solo cuenta como satisfecha si:
    # - existe;
    # - no pertenece a un ciclo;
    # - no depende transitivamente de una premisa ausente.
    # -----------------------------------------------------------
    ids_satisfechos: Set[str] = (
        ids_presentes
        - ids_circulares
        - ids_no_derivables
    )

    # -----------------------------------------------------------
    # 9. Resumen de alcance
    # -----------------------------------------------------------
    alcance = {
        "total_declaraciones": len(ids_presentes),
        "con_dependencias_satisfechas": len(ids_satisfechos),
        "con_premisas_faltantes": len(premisas_faltantes),
        "con_dependencias_circulares": len(ids_circulares),
    }

    # -----------------------------------------------------------
    # 10. Resultado final
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
            "Una premisa ausente establece un límite de derivación; "
            "una dependencia circular establece circularidad. "
            "Las premisas no se inventan ni se sustituyen."
        ),
    }

# ===============================================================
# FIN 7.1
# ===============================================================
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
                errores.append({
                    "modulo": nombre,
                    "tipo": "error_entrada_externa",
                    "error": "declaraciones_externas['{0}'] debe ser list".format(nombre),
                })
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
# ===============================================================# ===============================================================
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
# ===============================================================# ===============================================================
# 8.3 — GENERATIVIDAD (TR1)
# ===============================================================

def generatividad() -> dict:
    """
    Capacidad pública callable. Calcula TR1 en dos capas independientes
    mediante la misma callable matemática _medir_pares.

    Capa operativa: nodos del repositorio (recolectar + DOMINIO_CANONICO).
    Capa canónica: nodos de THETA_24 en el orden de THETA_NAMES.

    Criterio TR1 (documento canónico):
      Di ∩ Dj = ∅              → incompatible
      Di ∩ Dj ≠ ∅              → compatible
      compatible ∧ (union ⊋ Di) ∧ (union ⊋ Dj) → novedoso
      compatible en otro caso  → redundante

    Identidades:
      compatibles + incompatibles == pares_totales
      novedosos + redundantes == compatibles
    Generatividad formal: novedosos > theta_n
    """

    # -----------------------------------------------------------
    # Orden canónico de Θ (fuente de n y del recorrido de pares)
    # -----------------------------------------------------------
    THETA_NAMES = (
        "T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8",
        "T9", "T10", "T11", "T12", "T13", "T14", "T15", "T16",
        "T17", "U1", "M1", "M.1", "B-Canonical", "TT.6.1",
        "U0", "TR1",
    )

    # -----------------------------------------------------------
    # 1. Capa operativa — grafo real del repositorio
    # -----------------------------------------------------------
    decls, errores = recolectar()

    oper: List[Dict] = []
    for d in decls:
        if d.get("tipo") not in ("teorema", "axioma"):
            continue
        gob = d.get("gobierna") or []
        if not gob:
            continue
        dominios_norm: Set[str] = set()
        for g in gob:
            key = str(g).lower().strip()
            dominios_norm.add(DOMINIO_CANONICO.get(key, key.upper()[:3]))
        oper.append({
            "id": d["id"],
            "tipo": d["tipo"],
            "dominios": dominios_norm,
        })

    # Misma callable matemática sobre el grafo operativo
    m_op = _medir_pares(oper)
    dominios_op = sorted({g for n in oper for g in n["dominios"]})

    # -----------------------------------------------------------
    # 2. Capa canónica — TR1 formal desde THETA_NAMES / THETA_24
    # -----------------------------------------------------------
    can: List[Dict] = [
        {
            "id": tid,
            "tipo": "teorema",
            "dominios": set(THETA_24[tid]),
        }
        for tid in THETA_NAMES
        if tid in THETA_24
    ]

    # Misma callable matemática sobre el grafo canónico
    m_can = _medir_pares(can)
    dominios_can = sorted({g for n in can for g in n["dominios"]})

    # Correspondencia repo ↔ canon (no altera el cálculo TR1)
    ids_en_repo = {str(d.get("id", "")) for d in decls}
    ids_presentes = sorted(i for i in THETA_NAMES if i in ids_en_repo)
    ids_faltantes = sorted(i for i in THETA_NAMES if i not in ids_en_repo)
    ids_sin_dominio = sorted(
        tid for tid in THETA_NAMES
        if tid in THETA_24 and not THETA_24[tid]
    )

    # -----------------------------------------------------------
    # 3. Indicadores derivados (no forman parte de la mecánica TR1)
    # -----------------------------------------------------------
    u1_proxy = (
        "NO_STAGNANT"
        if m_can.get("pares_novedosos", 0) > 0
        or m_op.get("pares_novedosos", 0) > 0
        else "REVISAR"
    )

    # Referencia documental (solo verificación; no es entrada de cálculo)
    ref_doc = {
        "theta_n": 24,
        "pares_totales": 276,
        "pares_compatibles": 183,
        "pares_novedosos": 153,
        "pares_redundantes": 30,
        "pares_incompatibles": 93,
        "condicion_central": "153 > 24",
    }

    coincide_paper = (
        m_can.get("pares_totales") == ref_doc["pares_totales"]
        and m_can.get("pares_compatibles") == ref_doc["pares_compatibles"]
        and m_can.get("pares_novedosos") == ref_doc["pares_novedosos"]
        and m_can.get("pares_redundantes") == ref_doc["pares_redundantes"]
        and m_can.get("pares_incompatibles") == ref_doc["pares_incompatibles"]
    )

    # -----------------------------------------------------------
    # 4. Salida contractual
    # -----------------------------------------------------------
    return {
        "contenedor": "axiomas",
        # capa operativa
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
        # capa canónica
        "canonica": {
            "theta_n": m_can["theta_n"],
            "pares_totales": m_can["pares_totales"],
            "pares_compatibles": m_can["pares_compatibles"],
            "pares_novedosos": m_can["pares_novedosos"],
            "pares_redundantes": m_can["pares_redundantes"],
            "pares_incompatibles": m_can["pares_incompatibles"],
            "im_vs_theta": m_can["im_vs_theta"],
            "identidad_pares": m_can["identidad_pares"],
            "identidad_compatibles": m_can["identidad_compatibles"],
            "ids_presentes": ids_presentes,
            "ids_faltantes": ids_faltantes,
            "ids_sin_dominio": ids_sin_dominio,
            "dominios": dominios_can,
            "dominios_formales": {
                k: sorted(v) for k, v in THETA_24.items()
            },
            "referencia_documental": ref_doc,
            "coincide_paper": coincide_paper,
        },
        "nota": (
            "Capa operativa = grafo del repo. "
            "Capa canónica = TR1 formal desde THETA_NAMES / THETA_24. "
            "Ambas capas usan la misma callable _medir_pares. "
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
    """
    Barrido de coherencia del cuerpo axiomático.

    Alcance exclusivo:
    - errores de recolección
    - contradiccion_directa
    - contradiccion_de_cota

    No invoca limite_axiomático.
    No fusiona coherencia con límite axiomático.
    Una sola recolección.
    """
    decls, errores = recolectar(declaraciones_externas)
    choques = contradiccion_directa(decls) + contradiccion_de_cota(decls)
    coherente = not (choques or errores)

    # Notificación a DiagnosticoGlobal (no altera el resultado de coherencia)
    if (choques or errores) and DiagnosticoGlobal is not None:
        try:
            DiagnosticoGlobal.recibir_reporte(
                modulo="axiomas",
                errores=(
                    [{"tipo": "choque", "detalle": c} for c in choques]
                    + list(errores)  # conserva tipo original (error_carga,
                                    # error_normalizacion, id_duplicado,
                                    # error_entrada_externa, etc.)
                ),
            )
        except Exception:
            pass

    cuerpos = sorted({d["cuerpo"] for d in decls})
    por_tipo = {t: sum(1 for d in decls if d["tipo"] == t) for t in TIPOS}

    return {
        "coherente": coherente,
        "choques": choques,
        "errores": errores,
        "declaraciones": len(decls),
        "cuerpos": cuerpos,
        "por_tipo": por_tipo,
        "ids_dominio_k_o": (
            ids_dominio_k_o(declaraciones_externas) if coherente else []
        ),
    }


def verificar_salida(salida: Dict) -> bool:
    """Interpreta la salida de barrer mediante su campo coherente."""
    return bool(salida.get("coherente", False))


def verificar(
    declaraciones_externas: Optional[Dict[str, List[Dict]]] = None,
) -> Dict[str, Any]:
    """Alias contractual de barrer. Sin segunda implementación."""
    return barrer(declaraciones_externas)

# ===============================================================
# FIN 8.4
# ===============================================================
# ===============================================================
# 8.5 — CONSULTAS Y APLICACIÓN DEL CUERPO AXIOMÁTICO
# ===============================================================

def declaraciones(
    declaraciones_externas: Optional[Dict[str, List[Dict]]] = None,
) -> List[Dict]:
    """
    Callable público.

    Obtiene las declaraciones normalizadas mediante la fuente única
    recolectar().

    La función permite consultar el conjunto de declaraciones disponible.
    No reconstruye, modifica ni inventa declaraciones.
    """
    decls, errores = recolectar(declaraciones_externas)
    choques = contradiccion_directa(decls) + contradiccion_de_cota(decls)
    if choques or errores:
        return []
    return decls


def axiomas(
    declaraciones_externas: Optional[Dict[str, List[Dict]]] = None,
) -> List[Dict]:
    """
    Callable universal del cuerpo axiomático de AX.

    Fuente única de verdad: recolectar(declaraciones_externas).

    Expone el cuerpo axiomático completo para su utilización por Engine
    y por cualquier módulo que requiera aplicar las reglas declaradas
    en dicho cuerpo.

    La capacidad pertenece a AX y no al módulo consumidor.

    El cuerpo contiene axiomas, lemas, teoremas, corolarios y definiciones.
    La aplicación de una declaración se realiza conforme a su estructura,
    contrato, dominio, premisas, dependencias y demás reglas declaradas
    en el cuerpo axiomático.

    No restringe el cuerpo a un dominio determinado.
    No selecciona arbitrariamente una declaración.
    No inventa premisas.
    No convierte una ausencia de premisa en axioma.
    No sustituye las reglas declaradas por heurística o búsqueda textual.

    La callable permanece abierta para cualquier dominio y cualquier
    módulo que Engine dirija hacia AX.

    Salida: cuerpo axiomático normalizado disponible para aplicación.
    """
    decls, _ = recolectar(declaraciones_externas)
    return decls


def por_dominio(
    dominio: str,
    declaraciones_externas: Optional[Dict[str, List[Dict]]] = None,
) -> List[Dict]:
    """
    Callable público.

    Selecciona declaraciones mediante la relación estructural
    "gobierna", normalizando el dominio con DOMINIO_CANONICO.

    No utiliza búsqueda textual ni heurística.
    """
    key = str(dominio).lower().strip()
    dom_can = DOMINIO_CANONICO.get(
        key,
        key.upper()[:3] if len(key) >= 3 else key.upper(),
    )

    decls, _ = recolectar(declaraciones_externas)

    out: List[Dict] = []

    for d in decls:
        gobs = {
            str(g).lower().strip()
            for g in (d.get("gobierna") or [])
        }

        gobs_can = {
            DOMINIO_CANONICO.get(
                g,
                g.upper()[:3] if len(g) >= 3 else g.upper(),
            )
            for g in gobs
        }

        if dom_can in gobs_can or key in gobs:
            out.append(d)

    return out


def buscar_por_id(id_decl: str) -> Optional[Dict]:
    """
    Callable público.

    Resuelve exactamente una declaración por su identificador.

    Si el identificador está afectado por un duplicado registrado por
    recolectar(), no selecciona ninguna declaración arbitrariamente.

    Si existe exactamente una declaración válida con ese ID, devuelve
    la declaración normalizada.

    En cualquier otro caso devuelve None.
    """
    decls, errores = recolectar()

    for error in errores:
        if (
            error.get("tipo") == "id_duplicado"
            and error.get("id") == id_decl
        ):
            return None

    matches = [
        d for d in decls
        if d.get("id") == id_decl
    ]

    if len(matches) != 1:
        return None

    return matches[0]

# ===============================================================
# FIN 8.5
# ===============================================================# 8.6 — # ===============================================================
# ===============================================================
# 8.6 — INVENTARIO
# ===============================================================

def inventario(peticion=None) -> Dict:
    """
    Inventario estructural del módulo.
    Callable público.

    peticion:
        Parámetro de compatibilidad contractual.
        Se conserva por contrato y no altera la construcción
        del inventario.

    Instantánea única:
        Una sola llamada a recolectar().
        limite_axiomático y el filtrado K/O operan sobre esa
        misma recolección.

    No invoca ids_dominio_k_o() porque esa callable realiza
    internamente una nueva recolección.

    La regla K/O utilizada aquí es exactamente la regla
    estructural definida en 8.2:
        gobierna ∩ DOMINIOS_K_O
    """
    decls, errores = recolectar()
    lim = limite_axiomático(decls=decls, errores=errores)

    # -----------------------------------------------------------
    # IDS DE DOMINIO K/O
    # -----------------------------------------------------------
    # Se aplica la misma regla de 8.2 sobre la instantánea ya
    # recolectada. No se crea una nueva función ni se realiza
    # una segunda recolección.
    ids_k_o: List[str] = []

    for d in decls:
        gobs = {
            str(g).lower().strip()
            for g in (d.get("gobierna") or [])
        }

        if gobs & DOMINIOS_K_O:
            ids_k_o.append(d["id"])

    ids_k_o = sorted(set(ids_k_o))

    # -----------------------------------------------------------
    # INVENTARIO
    # -----------------------------------------------------------
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
        "descripcion": CONTENEDOR.get("descripcion"),
        "funcion": CONTENEDOR.get("funcion"),
        "no_hace": CONTENEDOR.get("no_hace"),
        "tipos": list(TIPOS),
        "declaraciones": len(decls),
        "por_tipo": {
            t: sum(1 for d in decls if d["tipo"] == t)
            for t in TIPOS
        },
        "cuerpos": sorted({d["cuerpo"] for d in decls}),
        "errores": errores,
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "capacidades_resueltas": list(CAPACIDADES_RESUELTAS.keys()),
        "capacidades_meta": list(
            CONTENEDOR.get("capacidades_meta", {}).keys()
        ),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "autoridad": CONTENEDOR.get("autoridad"),
        "conocimiento_exportable": CONTENEDOR.get(
            "conocimiento_exportable"
        ),
        "consultas_soportadas": CONTENEDOR.get(
            "consultas_soportadas"
        ),
        "autoriza_engine": CONTENEDOR.get("autoriza_engine"),
        "reporting": CONTENEDOR.get("reporting"),
        "estados_validos": CONTENEDOR.get("estados_validos"),
        "invariantes": CONTENEDOR.get("invariantes"),
        "vigila": [
            "contradiccion_directa",
            "contradiccion_de_cota",
        ],
        "ids_dominio_k_o": ids_k_o,
        "limite_axiomático": {
            "premisas_faltantes": len(
                lim.get("premisas_faltantes") or []
            ),
            "dependencias_no_satisfechas": len(
                lim.get("dependencias_no_satisfechas") or []
            ),
            "dependencias_circulares": len(
                lim.get("dependencias_circulares") or []
            ),
            "alcance": lim.get("alcance"),
        },
        "operaciones_arquitectonicas": {
            "ejecutar_total": (
                "ejecutar_total"
                in CONTENEDOR.get("capacidades", {})
            ),
            "inspeccionar": (
                "inspeccionar"
                in CONTENEDOR.get("capacidades", {})
            ),
        },
        "nota": (
            "Inventario estructural. "
            "La información se construye sobre una única "
            "recolección. "
            "ids_dominio_k_o se determina mediante la misma "
            "regla estructural de 8.2 sobre esa instantánea, "
            "sin invocar nuevamente la callable. "
            "limite_axiomático se reporta como información "
            "estructural y no como criterio adicional de "
            "coherencia."
        ),
    }

# ===============================================================
# FIN 8.6
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
    caps = list(CONTENEDOR["capacidades"].keys())
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
        "por_tipo": {
            t: sum(1 for d in decls if d["tipo"] == t) for t in TIPOS
        },
        "capacidades": caps,
        "capacidades_resueltas": list(CAPACIDADES_RESUELTAS.keys()),
        "capacidades_meta": list(
            CONTENEDOR.get("capacidades_meta", {}).keys()
        ),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "autoridad": CONTENEDOR.get("autoridad"),
        "conocimiento_exportable": CONTENEDOR.get(
            "conocimiento_exportable"
        ),
        "consultas_soportadas": CONTENEDOR.get("consultas_soportadas"),
        "limite_axiomático": {
            "premisas_faltantes": len(
                lim.get("premisas_faltantes") or []
            ),
            "dependencias_no_satisfechas": len(
                lim.get("dependencias_no_satisfechas") or []
            ),
            "dependencias_circulares": len(
                lim.get("dependencias_circulares") or []
            ),
        },
        "operaciones_arquitectonicas": {
            nombre: True for nombre in caps
        },
    }

# ===============================================================
# FIN 9.1
# ===============================================================
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

# Estructura paralela de capacidades resueltas
CAPACIDADES_RESUELTAS: Dict[str, Any] = {}


def _resolver_capacidades() -> None:
    """
    Resuelve las referencias contractuales hacia callables reales.
    Materializa los callables en CONTENEDOR["capacidades"]
    porque Engine exige callables, no strings.
    """
    global CAPACIDADES_RESUELTAS
    resueltas: Dict[str, Any] = {}

    for nombre, ref in CONTENEDOR["capacidades"].items():
        # Ya es callable
        if callable(ref):
            resueltas[nombre] = ref
            continue

        # Es una referencia por nombre (str)
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

        # Tipo inválido
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: capacidad '{nombre}' "
            f"tiene tipo inválido: {type(ref).__name__}"
        )

    CAPACIDADES_RESUELTAS = resueltas
    # Engine exige callables en CONTENEDOR["capacidades"]
    CONTENEDOR["capacidades"] = resueltas

# ===============================================================
# FIN 10.2
# ===============================================================# ===============================================================
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
