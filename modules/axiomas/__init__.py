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
# Función:
#   Responsable del conocimiento axiomático del sistema.
#   Mantiene, valida, organiza y expone todas las declaraciones
#   oficiales del repositorio para cualquier módulo autorizado.
#
# Qué hace:
#   - Carga, normaliza y recolecta declaraciones de todos los archivos
#   - Detecta contradicción directa y de cota
#   - Expone generatividad (TR1 / capa canónica)
#   - Responde consultas por id, dominio, sujeto, relación, objeto
#   - Cita cualquier declaración del grafo
#   - Genera inventario, reporte y diagnóstico propios
#   - Notifica a DiagnosticoGlobal cuando hay choques o errores
#   - Construye inventario estructural completo del módulo
#   - Expone ejecución total de unidades operativamente ejecutables
#
# Qué NO hace:
#   - No calcula Tru_total ni Tru_Ri
#   - No clasifica entrada de usuario (eso es CX)
#   - No orquesta el sistema (eso es Engine)
#   - No genera reportes de otros módulos
#   - No modifica declaraciones ajenas
#
# Responsabilidad:
#   Ser la fuente oficial y coherente del conocimiento axiomático.
#
# Autoridad:
#   - Exponer cualquier axioma, lema, teorema, corolario o definición
#   - Responder consultas y citar lo que el grafo contenga
#   - Verificar coherencia interna
#   - Reportar estado, salud, inventario y diagnóstico propios
#   - Declarar la política de inventario y ejecución del módulo
#   - Registrar todos los componentes descubiertos
#   - Determinar qué componentes son operacionalmente ejecutables
#   - Ejercer la ejecución total solicitada por Engine
#
# Conocimiento exportable:
#   declaraciones, referencias, dependencias, dominios,
#   generatividad, choques, inventario, estado, reporte, diagnóstico,
#   inventario_total, componentes, unidades_ejecutables, ejecucion
#
# Relación con Engine:
#   Engine descubre este CONTENEDOR, obtiene el inventario completo
#   del módulo, resuelve sus capacidades contractuales y puede
#   solicitar la ejecución total de las unidades operativamente
#   ejecutables del módulo conforme al contrato y sus leyes internas.
#
# Relación con Omega:
#   Omega no calcula nada de AX. Solo presenta lo que Engine entrega.
#
# ===============================================================


# ===============================================================
# PARTE 1 — PRINCIPIOS, BANDERAS Y ESPECIFICACIONES PRECISAS
# ===============================================================
#
# Responsabilidad: fijar todas las constantes, banderas, tipos,
# dominios y principios operativos antes de cualquier identidad
# o contrato.
# ===============================================================


# ===============================================================
# 1.1 — IMPORTACIONES
# ===============================================================

from __future__ import annotations

import importlib.util
import inspect
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    from core.diagnostico import DiagnosticoGlobal  # type: ignore
except Exception:  # noqa: BLE001
    DiagnosticoGlobal = None  # type: ignore

# ===============================================================
# FIN 1.1
# ===============================================================


# ===============================================================
# 1.2 — BANDERAS DE ESTADO DEL MÓDULO
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
# 1.3 — TIPOS DE DECLARACIÓN Y CLAVES OBLIGATORIAS
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
# 1.4 — TRADUCCIÓN DE CLAVES (NORMALIZACIÓN)
# ===============================================================

TRADUCCION_CLAVES = {
    "type": "tipo",
    "subject": "sujeto",
    "relation": "relacion",
    "object": "objeto",
    "polarity": "polaridad",
    "statement": "enunciado",
    "depends_on": "depende_de",
    "governs": "gobierna",
    "cota": "cota",
}

# ===============================================================
# FIN 1.4
# ===============================================================


# ===============================================================
# 1.5 — DOMINIOS K/O Y DOMINIOS CANÓNICOS
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
# 1.6 — Θ CANÓNICO (TR1 — ASIGNACIÓN FORMAL DEL PAPER)
# ===============================================================
#
# Asignación formal de dominios: Cuadro 4 del documento VPSI.
# NO se infiere de gobierna del repo. Es la definición de Θ.
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
# 1.7 — INVARIANTES DEL MÓDULO
# ===============================================================

INVARIANTES = (
    "el id del módulo nunca cambia",
    "el rol nunca cambia",
    "las capacidades declaradas son siempre callables tras la resolución",
    "este módulo no modifica el estado de otros módulos",
    "este módulo no inventa capacidades no declaradas en CONTENEDOR",
    "este módulo siempre puede reportar su propio estado",
    "el inventario total no omite componentes descubiertos del módulo",
    "ejecutar no equivale a resolver",
    "ejecutar total ejerce todas las unidades operativamente ejecutables",
    "todo componente descubierto recibe clasificación estructural",
    "ningún componente descubierto se convierte en ejecutable arbitrariamente",
    "todo componente ejecutable posee una estrategia de ejecución válida",
)

# ===============================================================
# FIN 1.7
# ===============================================================


# ===============================================================
# PARTE 2 — IDENTIDAD DEL MÓDULO
# ===============================================================
#
# Responsabilidad: fijar la identidad contractual e inmutable.
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
# PARTE 3 — CONFIGURACIÓN DE DIRECTORIO
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
    """Retorna todos los archivos .py del módulo excepto __init__.py."""
    return sorted(
        p for p in _DIR.glob("**/*.py")
        if p.name != "__init__.py"
    )

# ===============================================================
# FIN PARTE 3
# ===============================================================


# ===============================================================
# PARTE 4 — DEFINICIONES DE EXCEPCIONES
# ===============================================================

class ContratoInvalido(Exception):
    """El CONTENEDOR no cumple el esquema o la resolución de capacidades falló."""

# ===============================================================
# FIN PARTE 4
# ===============================================================


# ===============================================================
# PARTE 5 — CONTRATO OFICIAL DEL MÓDULO (CONTENEDOR)
# ===============================================================
#
# Responsabilidad: declarar de forma completa e inmutable la identidad,
# autoridad, dominio, capacidades y reporting del módulo AX.
# Contrato: VPSI-CONTRACT-1.0.
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
        "citar declaraciones y exponer generatividad."
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
        "Declarar la política de inventario y ejecución del módulo",
        "Registrar todos los componentes descubiertos",
        "Determinar qué componentes son operacionalmente ejecutables conforme al contrato",
        "Ejercer la ejecución total solicitada por Engine",
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
        "inventario_total",
        "componentes",
        "unidades_ejecutables",
        "ejecucion",
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
        "CT", "AX", "FO", "MC", "SF", "CA", "CX", "CC",
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
        "ejecutar",
        "ejecutar_total",
        "inspeccionar",
        "registrar_inventario",
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
        "ejecutar": "ejecutar",
        "ejecutar_total": "ejecutar_total",
        "inspeccionar": "inspeccionar",
        "registrar_inventario": "registrar_inventario",
    },

    # ============================================================
    # 5.11 — METADATOS DE CAPACIDADES (1:1)
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
            "salida": "dict con estado, problemas, advertencias, recomendaciones",
            "acceso_archivos": ["acceso_archivos"],
        },
        "buscar_por_id": {
            "descripcion": "Busca y cita una declaración por su id.",
            "entrada": "id_decl: str",
            "validar_esquema": ["acceso_archivos"],
            "salida": "dict de la declaración o None",
            "acceso_archivos": ["acceso_archivos"],
        },
        "ejecutar": {
            "descripcion": (
                "Ejercer todas las unidades operativas ejecutables "
                "descubiertas dentro del módulo conforme al contrato "
                "y a sus leyes internas."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con inventario, ejecuciones, resultados, "
                "errores, advertencias y estado"
            ),
            "acceso_archivos": ["*"],
        },
        "ejecutar_total": {
            "descripcion": (
                "Operación arquitectónica genérica. "
                "Ejerce la totalidad de las unidades operativamente ejecutables "
                "pertenecientes al módulo, conforme a su contrato, inventario, "
                "clasificación, dependencias y leyes internas."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con inventario, ejecuciones, resultados, "
                "errores, advertencias y estado"
            ),
            "acceso_archivos": ["*"],
        },
        "registrar_inventario": {
            "descripcion": (
                "Construir el inventario estructural completo del módulo."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con archivos, componentes, funciones, clases, "
                "constantes, reglas, capacidades y unidades ejecutables"
            ),
            "acceso_archivos": ["*"],
        },
        "inspeccionar": {
            "descripcion": (
                "Inspeccionar el contenido estructural del módulo: "
                "archivos, componentes, funciones, clases, constantes, "
                "excepciones, reglas, clasificadores, validadores y "
                "unidades ejecutables descubiertas."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con inventario estructural completo, "
                "componentes clasificados y estado de descubrimiento"
            ),
            "acceso_archivos": ["*"],
        },
    },

    # ============================================================
    # 5.12 — INVENTARIO Y EJECUCIÓN TOTAL
    # ============================================================
    "inventario_total": {
        "modo": "completo",
        "incluye": [
            "archivos",
            "modulos",
            "funciones",
            "clases",
            "constantes",
            "excepciones",
            "reglas",
            "clasificadores",
            "validadores",
            "capacidades",
            "componentes",
        ],
        "descubrimiento": "dinamico",
        "incluye_no_declarados": True,
    },
    "ejecucion": {
        "modo": "total",
        "incluye_capacidades_declaradas": True,
        "incluye_componentes_ejecutables_descubiertos": True,
        "respeta_contrato": True,
        "respeta_leyes_internas": True,
        "ejecuta_constantes": False,
        "ejecuta_excepciones": False,
        "instancia_clases_automaticamente": False,
    },
    "capacidades_sistema": {
        "inventariar": "inventario",
        "registrar": "registrar_inventario",
        "resolver": "barrer",
        "ejecutar": "ejecutar",
    },

    # ============================================================
    # 5.13 — AUTORIZACIÓN AL ENGINE
    # ============================================================
    "autoriza_engine": {
        "leer": True,
        "ejecutar": True,
        "ejecutar_total": True,
        "inspeccionar": True,
        "registrar_inventario": True,
        "consultar": True,
        "recombinar": True,
        "reportar": True,
        "auditar": True,
        "inventariar": True,
        "alterar": False,
        "crear": True,
        "actualizar": False,
        "validar": True,
        "procesar": True,
        "analizar": True,
        "generar": True,
        "exportar": True,
        "importar": True,
        "respaldar": True,
        "recuperar": True,
        "sincronizar": True,
        "monitorear": True,
        "metricas": True,
        "diagnostico": True,
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
        "validar_esquema": True,
        "acceso_archivos": True,
    },

    # ============================================================
    # 5.14 — REPORTING
    # ============================================================
    "reporting": {
        "estado": True,
        "salud": True,
        "inventario": True,
        "capacidades": True,
        "errores": True,
        "advertencias": True,
        "dependencias": True,
        "version": True,
        "contrato": True,
        "conocimiento": True,
        "metricas": True,
        "diagnostico": True,
        "reporte": True,
        "acceso_archivos": True,
        "validar_esquema": True,
    },

    # ============================================================
    # 5.15 — ESTADOS VÁLIDOS E INVARIANTES
    # ============================================================
    "estados_validos": list(ESTADOS_VALIDOS),
    "invariantes": list(INVARIANTES),
}

# ===============================================================
# FIN PARTE 5
# ===============================================================


# ===============================================================
# PARTE 6 — FUNCIONES PRIVADAS
# ===============================================================
#
# Responsabilidad: carga, normalización, detección de choques,
# medición de generatividad e inventario estructural.
# ===============================================================


# ===============================================================
# 6.1 — CARGA DESDE ARCHIVO
# ===============================================================

def _cargar_declaraciones_desde_archivo(archivo: Path) -> List[Dict]:
    if archivo.name.startswith("_"):
        return []

    nombre_mod = "axiomas_{0}".format(archivo.stem)
    spec = importlib.util.spec_from_file_location(nombre_mod, archivo)
    if spec is None or spec.loader is None:
        return []

    mod = importlib.util.module_from_spec(spec)
    sys.modules[nombre_mod] = mod
    try:
        spec.loader.exec_module(mod)
    except Exception:
        if nombre_mod in sys.modules:
            del sys.modules[nombre_mod]
        return []

    declaraciones_raw = getattr(mod, "DECLARACIONES", None)
    if declaraciones_raw is None and callable(getattr(mod, "declaraciones", None)):
        try:
            declaraciones_raw = mod.declaraciones()
        except Exception:  # noqa: BLE001
            declaraciones_raw = []

    if declaraciones_raw is None:
        for attr in ("CUERPO", "declaraciones_lista"):
            val = getattr(mod, attr, None)
            if isinstance(val, list):
                declaraciones_raw = val
                break

    return declaraciones_raw if isinstance(declaraciones_raw, list) else []

# ===============================================================
# FIN 6.1
# ===============================================================


# ===============================================================
# 6.2 — NORMALIZACIÓN DE DECLARACIÓN
# ===============================================================

def normalizar(decl_original: Dict, cuerpo: str) -> Dict:
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
                cuerpo, decl["id"], tipo, TIPOS
            )
        )
    if not isinstance(decl["polaridad"], bool):
        raise ValueError(
            "{0}:{1} polaridad debe ser bool".format(cuerpo, decl["id"])
        )

    return {
        "id": str(decl["id"]),
        "cuerpo": cuerpo,
        "tipo": tipo,
        "sujeto": str(decl["sujeto"]),
        "relacion": str(decl["relacion"]),
        "objeto": str(decl["objeto"]),
        "polaridad": bool(decl["polaridad"]),
        "cota": None if decl.get("cota") is None else str(decl["cota"]),
        "depende_de": [str(x) for x in decl.get("depende_de", [])],
        "gobierna": [str(x) for x in decl.get("gobierna", [])],
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
            porcota.setdefault(d["cota"], []).append(ref(d))
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
    """
    TR1 / T15:
      compatible  ⇔ Di ∩ Dj ≠ ∅
      novedoso    ⇔ Di ∪ Dj ⊃ Di  ∧  Di ∪ Dj ⊃ Dj
      redundante  ⇔ compatible ∧ no novedoso
      incompatible⇔ Di ∩ Dj = ∅
    """
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
            f"{NOMBRE_MODULO}: version_contrato inválida: {cont.get('version_contrato')}"
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
# FIN 6.6
# ===============================================================


# ===============================================================
# 6.7 — DESCUBRIMIENTO DEL INVENTARIO TOTAL
# ===============================================================

def _descubrir_inventario_total() -> Dict[str, Any]:
    """
    Inspecciona el propio módulo y construye el inventario estructural completo.
    Clasifica cada componente descubierto.
    """
    componentes: List[Dict[str, Any]] = []
    archivos: List[Dict[str, Any]] = []
    funciones: List[Dict[str, Any]] = []
    clases: List[Dict[str, Any]] = []
    constantes: List[Dict[str, Any]] = []
    excepciones: List[Dict[str, Any]] = []
    unidades_ejecutables: List[Dict[str, Any]] = []
    errores_descubrimiento: List[str] = []

    for archivo in sorted(_DIR.glob("*.py")):
        archivos.append({
            "nombre": archivo.name,
            "ruta": str(archivo),
            "tipo": "archivo",
            "declarado": archivo.name == "__init__.py",
            "descubierto": True,
        })

    modulo_actual = sys.modules.get(__name__)
    if modulo_actual is None:
        errores_descubrimiento.append("módulo actual no disponible en sys.modules")
        return {
            "archivos": archivos,
            "componentes": componentes,
            "errores": errores_descubrimiento,
        }

    capacidades_declaradas = set(CONTENEDOR.get("capacidades", {}).keys())
    miembros = inspect.getmembers(modulo_actual)

    for nombre, obj in miembros:
        if nombre in ("__builtins__", "__cached__", "__file__", "__loader__",
                      "__name__", "__package__", "__spec__", "__doc__"):
            continue

        entry: Dict[str, Any] = {
            "nombre": nombre,
            "origen": __name__,
            "modulo": NOMBRE_MODULO,
            "archivo": "__init__.py",
            "declarado": nombre in capacidades_declaradas,
            "descubierto": True,
            "callable": callable(obj),
            "ejecutable": False,
            "requiere_entrada": False,
            "tipo": "desconocido",
            "estado": "descubierto",
            "errores": [],
        }

        if inspect.isfunction(obj) or inspect.ismethod(obj):
            entry["tipo"] = "funcion"
            entry["referencia"] = obj
            try:
                sig = inspect.signature(obj)
                params = [
                    p for p in sig.parameters.values()
                    if p.default is inspect.Parameter.empty
                    and p.kind in (
                        inspect.Parameter.POSITIONAL_ONLY,
                        inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    )
                ]
                params = [p for p in params if p.name not in ("self", "cls")]
                entry["requiere_entrada"] = len(params) > 0
                if nombre.startswith("_"):
                    entry["ejecutable"] = False
                    entry["ejecutable_directamente"] = False
                    entry["participa_en_ejecucion"] = True
                else:
                    entry["ejecutable"] = True
                    entry["ejecutable_directamente"] = not entry["requiere_entrada"]
            except (ValueError, TypeError):
                entry["requiere_entrada"] = True
                entry["ejecutable"] = False

            funciones.append(entry)
            componentes.append(entry)
            if entry["ejecutable"]:
                unidades_ejecutables.append(entry)

        elif inspect.isclass(obj):
            entry["tipo"] = "clase"
            entry["ejecutable"] = False
            if issubclass(obj, Exception):
                entry["tipo"] = "excepcion"
                excepciones.append(entry)
            else:
                clases.append(entry)
            componentes.append(entry)

        elif isinstance(obj, (str, int, float, bool, list, tuple, dict, set, frozenset, type(None))):
            if nombre.isupper() or nombre.startswith("_"):
                entry["tipo"] = "constante"
                entry["ejecutable"] = False
                try:
                    entry["representacion"] = repr(obj)[:200]
                except Exception:
                    entry["representacion"] = "<no representable>"
                constantes.append(entry)
                componentes.append(entry)

    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "archivos": archivos,
        "componentes": componentes,
        "funciones": funciones,
        "clases": clases,
        "constantes": constantes,
        "excepciones": excepciones,
        "capacidades_declaradas": list(capacidades_declaradas),
        "unidades_ejecutables": unidades_ejecutables,
        "total_componentes": len(componentes),
        "total_ejecutables": len(unidades_ejecutables),
        "errores_descubrimiento": errores_descubrimiento,
    }

# ===============================================================
# FIN 6.7
# ===============================================================


# ===============================================================
# PARTE 7 — CAPACIDADES PÚBLICAS
# ===============================================================
#
# Responsabilidad: implementar las capacidades declaradas en CONTENEDOR.
# ===============================================================


# ===============================================================
# 7.1 — RECOLECCIÓN (FUENTE ÚNICA DE VERDAD)
# ===============================================================

def recolectar(
    declaraciones_externas: Optional[Dict[str, List[Dict]]] = None,
) -> Tuple[List[Dict], List[Dict]]:
    """
    Carga y normaliza todas las declaraciones de los cuerpos del módulo.
    Fuente única de verdad para el resto de capacidades.
    """
    decls: List[Dict] = []
    errores: List[Dict] = []

    for archivo in sorted(_DIR.glob("**/*.py")):
        if archivo.name == "__init__.py":
            continue
        try:
            for d in _cargar_declaraciones_desde_archivo(archivo):
                decls.append(normalizar(d, archivo.stem))
        except Exception as e:  # noqa: BLE001
            errores.append({
                "archivo": archivo.name,
                "error": "{0}: {1}".format(type(e).__name__, e),
            })

    vpsi = _ruta_vpsi()
    if vpsi is not None:
        try:
            for d in _cargar_declaraciones_desde_archivo(vpsi):
                decls.append(normalizar(d, "VPSI"))
        except Exception as e:  # noqa: BLE001
            errores.append({
                "archivo": str(vpsi.name),
                "error": "{0}: {1}".format(type(e).__name__, e),
            })

    if declaraciones_externas:
        for nombre, lista in declaraciones_externas.items():
            if not isinstance(lista, list):
                continue
            for d in lista:
                try:
                    decls.append(normalizar(d, nombre))
                except ValueError as e:
                    errores.append({"modulo": nombre, "error": str(e)})

    return decls, errores

# ===============================================================
# FIN 7.1
# ===============================================================


# ===============================================================
# 7.2 — IDS DE DOMINIO K/O
# ===============================================================

def ids_dominio_k_o(
    declaraciones_externas: Optional[Dict[str, List[Dict]]] = None,
) -> List[str]:
    """Ids de declaraciones ligadas a dominios K/O o Def-5.3.1."""
    decls, _ = recolectar(declaraciones_externas)
    ids: List[str] = []
    for d in decls:
        gobs = {str(g).lower().strip() for g in (d.get("gobierna") or [])}
        if gobs & DOMINIOS_K_O:
            ids.append(d["id"])
        blob = (
            "{0} {1} {2}".format(
                d.get("sujeto", ""),
                d.get("objeto", ""),
                d.get("enunciado", ""),
            )
        ).lower()
        if any(
            x in blob
            for x in ("def-5.3.1", "o_context", "dominio o", "permite_k")
        ):
            if d["id"] not in ids:
                ids.append(d["id"])
    return sorted(set(ids))

# ===============================================================
# FIN 7.2
# ===============================================================


# ===============================================================
# 7.3 — GENERATIVIDAD (TR1)
# ===============================================================

def generatividad() -> dict:
    """
    TR1 en dos capas (saber, no creer):

    1) operativa  — todo axioma/teorema con gobierna (grafo real del repo)
    2) canónica   — solo los 24 ids del paper con dominios formales (Cuadro 4)

    No inventa candidatos. No calcula Tru.
    La capa canónica NO infiere dominios desde gobierna: usa THETA_24.
    """
    decls, errores = recolectar()

    oper = []
    for d in decls:
        if d.get("tipo") not in ("teorema", "axioma"):
            continue
        gob = d.get("gobierna") or []
        if not gob:
            continue
        oper.append({
            "id": d["id"],
            "tipo": d["tipo"],
            "dominios": set(str(x) for x in gob),
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
    ids_sin_dominio = sorted(
        tid for tid, doms in THETA_24.items() if not doms
    )

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
            "dominios_formales": {
                k: sorted(v) for k, v in THETA_24.items()
            },
            "referencia_formal": {
                "theta_n": 24,
                "pares_totales": 276,
                "pares_compatibles": 183,
                "pares_novedosos": 153,
                "pares_redundantes": 30,
                "pares_incompatibles": 93,
                "nota": (
                    "|Im(⊕)|=153 > 24=|Θ| — enumeración exacta Cuadro 3/4 "
                    "del documento VPSI. El CI recalcula; no hardcodea."
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
            "Capa operativa = grafo del repo (gobierna real). "
            "Capa canónica = THETA_24 formal del paper (Cuadro 4). "
            "Identidades: C+I=T y N+R=C deben cumplirse o se reporta fallo."
        ),
    }

# ===============================================================
# FIN 7.3
# ===============================================================


# ===============================================================
# 7.4 — COHERENCIA (barrer / verificar)
# ===============================================================

def barrer(
    declaraciones_externas: Optional[Dict[str, List[Dict]]] = None,
) -> Dict:
    """Capacidad principal: coherencia axiomática del cuerpo."""
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
        except Exception:  # noqa: BLE001
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
    """Alias de contrato de barrer."""
    return barrer(declaraciones_externas)

# ===============================================================
# FIN 7.4
# ===============================================================


# ===============================================================
# 7.5 — CONSULTAS DE DECLARACIONES
# ===============================================================

def declaraciones(
    declaraciones_externas: Optional[Dict[str, List[Dict]]] = None,
) -> List[Dict]:
    """Lista normalizada si el cuerpo es coherente; si no → []."""
    resultado = barrer(declaraciones_externas)
    if not resultado["coherente"]:
        return []
    decls, _ = recolectar(declaraciones_externas)
    return decls


def axiomas(
    declaraciones_externas: Optional[Dict[str, List[Dict]]] = None,
) -> List[Dict]:
    """Alias de contrato: misma semántica que declaraciones()."""
    return declaraciones(declaraciones_externas)


def por_dominio(
    dominio: str,
    declaraciones_externas: Optional[Dict[str, List[Dict]]] = None,
) -> List[Dict]:
    """Filtra declaraciones por dominio en gobierna."""
    dom = str(dominio).lower().strip()
    decls, _ = recolectar(declaraciones_externas)
    out = []
    for d in decls:
        gobs = [str(g).lower().strip() for g in (d.get("gobierna") or [])]
        if dom in gobs or any(dom in g for g in gobs):
            out.append(d)
    return out


def buscar_por_id(id_decl: str) -> Optional[Dict]:
    """Busca y cita una declaración por su id."""
    decls, _ = recolectar()
    for d in decls:
        if d.get("id") == id_decl:
            return d
    return None

# ===============================================================
# FIN 7.5
# ===============================================================


# ===============================================================
# 7.6 — REGISTRAR_INVENTARIO
# ===============================================================

def registrar_inventario() -> Dict[str, Any]:
    """Construye el inventario estructural completo del módulo."""
    inv = _descubrir_inventario_total()
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "operacion": "registrar_inventario",
        "archivos": inv.get("archivos", []),
        "componentes": inv.get("componentes", []),
        "funciones": inv.get("funciones", []),
        "clases": inv.get("clases", []),
        "constantes": inv.get("constantes", []),
        "excepciones": inv.get("excepciones", []),
        "capacidades_declaradas": inv.get("capacidades_declaradas", []),
        "unidades_ejecutables": inv.get("unidades_ejecutables", []),
        "total_componentes": inv.get("total_componentes", 0),
        "total_ejecutables": inv.get("total_ejecutables", 0),
        "errores_descubrimiento": inv.get("errores_descubrimiento", []),
    }

# ===============================================================
# FIN 7.6
# ===============================================================


# ===============================================================
# 7.7 — INSPECCIONAR
# ===============================================================

def inspeccionar(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Inspeccionar el contenido estructural del módulo.
    """
    return registrar_inventario()

# ===============================================================
# FIN 7.7
# ===============================================================


# ===============================================================
# 7.8 — INVENTARIO (AMPLIADO)
# ===============================================================

def inventario(peticion=None) -> Dict:
    decls, errores = recolectar()
    inv_total = _descubrir_inventario_total()
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
        "por_tipo": {
            t: sum(1 for d in decls if d["tipo"] == t) for t in TIPOS
        },
        "cuerpos": sorted({d["cuerpo"] for d in decls}),
        "errores": errores,
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "autoridad": CONTENEDOR.get("autoridad"),
        "conocimiento_exportable": CONTENEDOR.get("conocimiento_exportable"),
        "consultas_soportadas": CONTENEDOR.get("consultas_soportadas"),
        "invariantes": CONTENEDOR.get("invariantes"),
        "vigila": ["contradiccion_directa", "contradiccion_de_cota"],
        "ids_dominio_k_o": ids_dominio_k_o(),
        "archivos": inv_total.get("archivos", []),
        "componentes": inv_total.get("componentes", []),
        "funciones": inv_total.get("funciones", []),
        "clases": inv_total.get("clases", []),
        "constantes": inv_total.get("constantes", []),
        "excepciones": inv_total.get("excepciones", []),
        "unidades_ejecutables": inv_total.get("unidades_ejecutables", []),
        "total_componentes": inv_total.get("total_componentes", 0),
        "total_ejecutables": inv_total.get("total_ejecutables", 0),
        "nota": (
            "Def-5.3.1 y dominio O viven en los cuerpos cargados; "
            "este módulo los vigila y expone, no los clasifica en entrada."
        ),
    }

# ===============================================================
# FIN 7.8
# ===============================================================


# ===============================================================
# 7.9 — EJECUCIÓN TOTAL DEL MÓDULO
# ===============================================================

def ejecutar(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Ejercer todas las unidades operativas ejecutables descubiertas
    dentro del módulo conforme al contrato y a sus leyes internas.
    """
    inv = _descubrir_inventario_total()
    unidades = inv.get("unidades_ejecutables", [])
    resultados: List[Dict[str, Any]] = []
    errores: List[Dict[str, Any]] = []
    advertencias: List[str] = []
    ejecutados = 0

    for unidad in unidades:
        nombre = unidad.get("nombre")
        ref = unidad.get("referencia")
        if not callable(ref):
            advertencias.append(
                "unidad '{0}' marcada ejecutable pero no es callable".format(nombre)
            )
            continue

        if unidad.get("requiere_entrada") and not (peticion and isinstance(peticion, dict)):
            advertencias.append(
                "unidad '{0}' requiere entrada; no se inventa argumento".format(nombre)
            )
            resultados.append({
                "nombre": nombre,
                "estado": "OMITIDA",
                "razon": "requiere_entrada",
            })
            continue

        try:
            if unidad.get("requiere_entrada"):
                out = ref(peticion)
            else:
                out = ref()
            ejecutados += 1
            resultados.append({
                "nombre": nombre,
                "estado": "EXITO",
                "resultado": out if not isinstance(out, (dict, list)) else "<objeto>",
            })
        except Exception as e:
            errores.append({
                "nombre": nombre,
                "error": "{0}: {1}".format(type(e).__name__, e),
            })
            resultados.append({
                "nombre": nombre,
                "estado": "ERROR",
                "error": "{0}: {1}".format(type(e).__name__, e),
            })

    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "operacion": "ejecutar",
        "modo": "total",
        "inventario": {
            "total_componentes": inv.get("total_componentes", 0),
            "total_ejecutables": inv.get("total_ejecutables", 0),
        },
        "total_componentes": inv.get("total_componentes", 0),
        "total_ejecutables": inv.get("total_ejecutables", 0),
        "ejecutados": ejecutados,
        "resultados": resultados,
        "errores": errores,
        "advertencias": advertencias,
        "coherente": len(errores) == 0,
        "estado": ESTADO_OPERATIVO if len(errores) == 0 else ESTADO_DEGRADADO,
    }


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
    return ejecutar(peticion)

# ===============================================================
# FIN 7.9
# ===============================================================


# ===============================================================
# PARTE 8 — REPORTING INTERNO
# ===============================================================


# ===============================================================
# 8.1 — REPORTE
# ===============================================================

def reporte() -> Dict[str, Any]:
    r = barrer()
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "estado": ESTADO_OPERATIVO if r.get("coherente") else ESTADO_DEGRADADO,
        "coherente": r.get("coherente"),
        "declaraciones": r.get("declaraciones"),
        "choques": len(r.get("choques") or []),
        "errores": len(r.get("errores") or []),
        "cuerpos": r.get("cuerpos"),
        "por_tipo": r.get("por_tipo"),
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "autoridad": CONTENEDOR.get("autoridad"),
        "conocimiento_exportable": CONTENEDOR.get("conocimiento_exportable"),
        "consultas_soportadas": CONTENEDOR.get("consultas_soportadas"),
    }

# ===============================================================
# FIN 8.1
# ===============================================================


# ===============================================================
# 8.2 — DIAGNÓSTICO
# ===============================================================

def diagnostico() -> Dict[str, Any]:
    r = barrer()
    problemas = []
    advertencias = []
    recomendaciones = []

    if r.get("errores"):
        problemas.append({"tipo": "errores_carga", "detalle": r["errores"]})
        recomendaciones.append("Revisar archivos de cuerpos con error de carga")

    if r.get("choques"):
        problemas.append({
            "tipo": "contradicciones",
            "cantidad": len(r["choques"]),
            "detalle": r["choques"][:5],
        })
        recomendaciones.append("Resolver contradicciones directas o de cota")

    if not r.get("declaraciones"):
        advertencias.append("No hay declaraciones cargadas")
        recomendaciones.append("Verificar que existan cuerpos .py con DECLARACIONES")

    estado = ESTADO_OPERATIVO
    if problemas:
        estado = ESTADO_DEGRADADO
    if not r.get("declaraciones") and not problemas:
        estado = ESTADO_NO_INICIADO

    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "estado": estado,
        "problemas": problemas,
        "advertencias": advertencias,
        "recomendaciones": recomendaciones,
        "coherente": r.get("coherente"),
        "declaraciones": r.get("declaraciones"),
        "choques_n": len(r.get("choques") or []),
        "errores_n": len(r.get("errores") or []),
    }

# ===============================================================
# FIN 8.2
# ===============================================================


# ===============================================================
# PARTE 9 — RESOLUCIÓN ESTRICTA DEL CONTRATO
# ===============================================================


# ===============================================================
# 9.1 — MAPA DE CAPACIDADES
# ===============================================================

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
    "verificar": verificar,
    "ejecutar": ejecutar,
    "ejecutar_total": ejecutar_total,
    "inspeccionar": inspeccionar,
    "registrar_inventario": registrar_inventario,
}

# ===============================================================
# FIN 9.1
# ===============================================================


# ===============================================================
# 9.2 — RESOLUCIÓN DE CAPACIDADES
# ===============================================================

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
            f"tiene tipo inválido: {type(ref).__name__}"
        )
    cont["capacidades"] = resueltas

# ===============================================================
# FIN 9.2
# ===============================================================


# ===============================================================
# 9.3 — EJECUCIÓN DE VALIDACIÓN Y RESOLUCIÓN
# ===============================================================

_validar_contrato(CONTENEDOR)
_resolver_capacidades(CONTENEDOR)

# ===============================================================
# FIN 9.3
# ===============================================================


# ===============================================================
# PARTE 10 — EXPORTACIONES
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
    "ejecutar",
    "ejecutar_total",
    "inspeccionar",
    "registrar_inventario",
    "ContratoInvalido",
]

# ===============================================================
# FIN PARTE 10
# ===============================================================


# ===============================================================
# PARTE 11 — EXTENSIONES FUTURAS
# ===============================================================
#
# Toda capacidad nueva DEBE agregarse simultáneamente en:
#   1. capacidades
#   2. capacidades_meta  (descripcion, entrada, salida: str)
#   3. _CAP_MAP
#   4. VERSION_MODULO
#
# ===============================================================
# FIN PARTE 11
# ===============================================================


# ===============================================================
# FIN DEL MÓDULO
# ===============================================================
