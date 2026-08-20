# ===============================================================
# VPSI-TRUTH — modules/calculator/__init__.py
# ===============================================================
#
# MÓDULO:              calculator
# ID:                  CA
# Rol:                 CA
# Versión módulo:      2.3
# Versión contrato:    1.0
# Esquema contrato:    VPSI-CONTRACT-1.0
# Estabilidad:         ESTABLE
# Compatible desde:    1.2
# API Engine:          >=1.0
#
# Regla de salida (determinista):
#   Todo factor se reporta SIEMPRE como un solo objeto:
#     {
#       valor, fraccion, numerador, denominador,
#       decimal, display, precision, undefined
#     }
#   Ejemplo display: "7/9 = 0.778"
#   No se duplican C_fraccion / C_decimal en la raíz de la respuesta.
#
# Pipeline oficial:
#   contexto → evidencia → C/L/K → centinela → ID → historial → salida
#
# ===============================================================

# ===============================================================
# PARTE 1 — PRINCIPIOS, BANDERAS Y ESPECIFICACIONES PRECISAS
# ===============================================================

# ===============================================================
# 1.1 — IMPORTACIONES
# ===============================================================

from __future__ import annotations

import hashlib
import importlib
from collections import deque
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any, Deque, Dict, List, Optional, Tuple
from .coherencia import coherencia, calcular_c, verificar_c, calcular_c as factor_c
from .logica import logica, calcular_l, verificar_l, calcular_l as factor_l
from .correlacion_k import correlacion, calcular_k, verificar_k, calcular_k as factor_k



getcontext().prec = 50

# ===============================================================
# FIN 1.1
# ===============================================================


# ===============================================================
# 1.2 — IDENTIDAD
# ===============================================================

ID_MODULO = "CA"
NOMBRE_MODULO = "calculator"
ROL_MODULO = "CA"

# ===============================================================
# FIN 1.2
# ===============================================================


# ===============================================================
# 1.3 — VERSIONES Y ESTABILIDAD
# ===============================================================

VERSION_MODULO = "2.3"
VERSION_CONTRATO = "1.0"
ESQUEMA_CONTRATO = "VPSI-CONTRACT-1.0"

COMPATIBLE_DESDE = "1.2"
API_ENGINE = ">=1.0"
ESTABILIDAD = "ESTABLE"

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
    "CA es la unica autoridad del dominio de calculo estructural",
    "todo calculo interno utiliza Fraction como valor oficial",
    "toda salida de factor es un solo objeto con fraccion+decimal (ej: 7/9 = 0.778)",
    "no se duplican campos de factor en la raiz de la respuesta",
    "float nunca es la fuente del decimal; se usa Decimal",
    "ningun calculo sale sin centinela ni ID unico compuesto",
    "toda magnitud registra evidencia trazable con id_evidencia",
    "K ausente sin contexto/O es legitimo (Def-5.3.1)",
    "L = UNDEFINED cuando p=0 (AM-D6 / AM-A3)",
)

# ===============================================================
# FIN 1.5
# ===============================================================


# ===============================================================
# 1.6 — CONSTANTES DE CÁLCULO
# ===============================================================

PRECISION_DECIMAL_DEFAULT = 3
HISTORIAL_MAX = 64

_FACTORES_CANONICOS = ("C", "L", "K")
_ARCHIVO_FACTOR = {
    "coherencia": "C",
    "logica": "L",
    "correlacion_k": "K",
}
_CLAVES_CONTEO = (
    "compromisos",
    "contradicciones",
    "posturas",
    "reversiones",
    "afirmaciones",
    "afirmaciones_falsas",
)

# ===============================================================
# FIN 1.6
# ===============================================================

# ===============================================================
# FIN PARTE 1
# ===============================================================
# ===============================================================
# 1.7 — CONFIGURACIÓN
# ===============================================================

_DIR = Path(__file__).parent

# ===============================================================
# FIN 1.7
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
    pass


class DominioError(ValueError):
    pass


class MetodoError(ValueError):
    pass

# ===============================================================
# FIN 4.1
# ===============================================================


# ===============================================================
# 4.2 — UNDEFINED
# ===============================================================

class _Undefined:
    __slots__ = ()

    def __repr__(self) -> str:
        return "UNDEFINED"

    def __bool__(self):
        raise TypeError("UNDEFINED no admite conversion a booleano")

    def __eq__(self, other):
        return isinstance(other, _Undefined)

    def __hash__(self):
        return hash("VPSI_CA_UNDEFINED")


UNDEFINED = _Undefined()


def es_undefined(v: Any) -> bool:
    return v is UNDEFINED or isinstance(v, _Undefined)

# ===============================================================
# FIN 4.2
# ===============================================================


# ===============================================================
# 4.3 — ESTADO INTERNO
# ===============================================================

_CALC_SEQ = 0
_EV_SEQ = 0
_HISTORIAL: Deque[Dict[str, Any]] = deque(maxlen=HISTORIAL_MAX)
_EVIDENCIA_POR_CALC: Dict[str, List[Dict[str, Any]]] = {}
_REG_EVIDENCIA: Dict[str, Dict[str, Any]] = {}

# ===============================================================
# FIN 4.3
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
        "Unica autoridad del dominio de calculo estructural. "
        "Calcula C, L, K. Cada factor se reporta como un solo objeto "
        "con fraccion y decimal (ej: 7/9 = 0.778). No calcula Tru (FO)."
    ),

    # ============================================================
    # 5.3 — PROPÓSITO
    # ============================================================
    "funcion": (
        "Pipeline: evidencia -> C/L/K -> centinela -> ID compuesto -> "
        "historial liviano. Valor oficial = Fraction. Decimal via Decimal."
    ),
    "no_hace": [
        "No calcula Tru_Ri ni Tru_total",
        "No redefine constantes, axiomas ni formulas",
        "No orquesta el sistema",
        "No estima por intuicion",
        "No duplica campos de factor en la raiz de la salida",
    ],

    # ============================================================
    # 5.4 — AUTORIDAD
    # ============================================================
    "autoridad": [
        "Unica autoridad para calcular C, L, K",
        "Reportar cada factor como fraccion = decimal en un solo objeto",
        "Validar evidencia y explicar calculos con trazabilidad real",
        "Auditar integridad del dominio",
    ],

    # ============================================================
    # 5.5 — CONOCIMIENTO EXPORTABLE
    # ============================================================
    "conocimiento_exportable": [
        "C", "L", "K", "factores", "UNDEFINED",
        "evidencia", "versiones_utilizadas", "contratos_utilizados",
        "historial", "explicaciones",
        "inventario", "estado", "reporte", "diagnostico",
        "ejecutar_total", "inspeccionar", "registrar_inventario",
    ],

    # ============================================================
    # 5.6 — ACCESO (obligatorio en el esquema)
    # ============================================================
    "acceso": {
    "nivel": "acceso_archivos",
    "descripcion": "Acceso total a recursos del módulo"
    },
    # ============================================================
    # 5.7 — DEPENDENCIAS
    # ============================================================
    "requiere": [
    "CT", "AX", "FO", "MC", "SF",
    "CA", "CX", "DI", "RE", "VX",
    "TX", "CH", "CIT", "DGCO", "UI",
    "CC", "TT", "SC",
    ],

    # ============================================================
    # 5.8 — ACCESO A ARCHIVOS (obligatorio en el esquema)
    # ============================================================
    "acceso_archivos": ["*"],

    # ============================================================
    # 5.9 — VALIDAR ESQUEMA A NIVEL MÓDULO (obligatorio)
    # ============================================================
    "validar_esquema": ["*"],

    # ============================================================
    # 5.10 — AUTORIZACIÓN AL ENGINE (SOLO PERMISOS)
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
        "evaluar_universal": True,
    },
    
    # ============================================================
    # 5.11 — CONSULTAS SOPORTADAS
    # ============================================================
    "consultas_soportadas": [
        "calcular", "calcular_C", "calcular_L", "calcular_K",
        "calcular_factor", "representar", "validar_evidencia",
        "explicar_calculo", "verificar_coherencia",
        "obtener_inventario", "obtener_reporte", "obtener_diagnostico",
        "leer_ids_escala", "historial", "verificar_calculo_de_C_L_K",
        "ejecutar_total", "inspeccionar", "registrar_inventario",
    ],

    # ============================================================
    # 5.12 — CAPACIDADES
    # ============================================================
    "capacidades": {
        "calcular": "calcular",
        "calcular_C": "calcular_C",
        "calcular_L": "calcular_L",
        "calcular_K": "calcular_K",
        "calcular_factor": "calcular_factor",
        "representar": "representar",
        "validar_evidencia": "validar_evidencia",
        "explicar_calculo": "explicar_calculo",
        "verificar": "barrer",
        "barrer": "barrer",
        "inventario": "inventario",
        "reporte": "reporte",
        "diagnostico": "diagnostico",
        "leer_ids_escala": "leer_ids_escala",
        "verificar_salida": "verificar_salida",
        "historial": "historial",
        "verificar_calculo_de_C_L_K": "verificar_calculo_de_C_L_K",
        "ejecutar_total": "ejecutar_total",
        "inspeccionar": "inspeccionar",
        "registrar_inventario": "registrar_inventario",
        "evaluar_universal": "evaluar_universal",
    },

    # ============================================================
    # 5.13 — METADATOS DE CAPACIDADES (1:1 OBLIGATORIO)
    # ============================================================
    "capacidades_meta": {
        "calcular": {
            "descripcion": (
                "Pipeline completo. C/L/K son objetos unicos con "
                "fraccion+decimal (ej display: 7/9 = 0.778)."
            ),
            "entrada": "peticion: dict",
            "validar_esquema": ["*"],
            "salida": (
                "dict con id_calculo, C, L, K, evidencia, "
                "versiones_utilizadas, centinela, errores"
            ),
            "acceso_archivos": ["*"],
        },
        "calcular_C": {
            "descripcion": "Factor C como objeto fraccion+decimal.",
            "entrada": "peticion: dict",
            "validar_esquema": ["*"],
            "salida": "dict con C, ruta, notas, evidencia",
            "acceso_archivos": ["*"],
        },
        "calcular_L": {
            "descripcion": "Factor L como objeto (o UNDEFINED).",
            "entrada": "peticion: dict",
            "validar_esquema": ["*"],
            "salida": "dict con L, p, r, ruta, notas, evidencia",
            "acceso_archivos": ["*"],
        },
        "calcular_K": {
            "descripcion": "Factor K como objeto (o None sin O).",
            "entrada": "peticion: dict",
            "validar_esquema": ["*"],
            "salida": "dict con K, ruta, notas, evidencia",
            "acceso_archivos": ["*"],
        },
        "calcular_factor": {
            "descripcion": "Factor por nombre C|L|K.",
            "entrada": "factor: str, peticion: dict",
            "validar_esquema": ["*"],
            "salida": "dict del factor",
            "acceso_archivos": ["*"],
        },
        "representar": {
            "descripcion": (
                "Fraction -> objeto con fraccion, numerador, denominador, "
                "decimal, display (7/9 = 0.778). Sin float."
            ),
            "entrada": "valor: Fraction|UNDEFINED|None, precision: int=3",
            "validar_esquema": ["*"],
            "salida": "dict valor completo",
            "acceso_archivos": ["*"],
        },
        "validar_evidencia": {
            "descripcion": (
                "Valida lista de evidencia sin calcular: estructura, "
                "rechazados, conflicto de versiones del mismo modulo."
            ),
            "entrada": "evidencia: list[dict]",
            "validar_esquema": ["*"],
            "salida": (
                "dict con ok, problemas, advertencias, "
                "evidencia_normalizada"
            ),
            "acceso_archivos": ["*"],
        },
        "explicar_calculo": {
            "descripcion": (
                "Explica un calculo por id usando evidencia real almacenada."
            ),
            "entrada": "id_calculo: str",
            "validar_esquema": ["*"],
            "salida": "dict explicativo dinamico o None",
            "acceso_archivos": ["*"],
        },
        "verificar": {
            "descripcion": "Centinela de integridad (APIs, hashes, choques).",
            "entrada": "ninguna",
            "validar_esquema": ["*"],
            "salida": "dict con coherente, errores, choques, hashes",
            "acceso_archivos": ["*"],
        },
        "barrer": {
            "descripcion": "Alias de verificar.",
            "entrada": "ninguna",
            "validar_esquema": ["*"],
            "salida": "dict con coherente, errores, choques, hashes",
            "acceso_archivos": ["*"],
        },
        "inventario": {
            "descripcion": "Inventario del dominio de calculo.",
            "entrada": "peticion opcional",
            "validar_esquema": ["*"],
            "salida": (
                "dict con capacidades, factores, archivos, hashes"
            ),
            "acceso_archivos": ["*"],
        },
        "reporte": {
            "descripcion": "Reporte de estado de CA.",
            "entrada": "ninguna",
            "validar_esquema": ["*"],
            "salida": "dict con estado, coherente, factores_api",
            "acceso_archivos": ["*"],
        },
        "diagnostico": {
            "descripcion": "Diagnostico de problemas y recomendaciones.",
            "entrada": "ninguna",
            "validar_esquema": ["*"],
            "salida": (
                "dict con estado, problemas, advertencias, "
                "recomendaciones"
            ),
            "acceso_archivos": ["*"],
        },
        "leer_ids_escala": {
            "descripcion": "Ids de escala reconocidos.",
            "entrada": "ninguna",
            "validar_esquema": ["*"],
            "salida": "dict con ids, n, origenes",
            "acceso_archivos": ["*"],
        },
        "verificar_salida": {
            "descripcion": (
                "Forma minima: C, L, K, id_calculo; "
                "cada factor con display."
            ),
            "entrada": "salida: dict",
            "validar_esquema": ["*"],
            "salida": "bool",
            "acceso_archivos": ["*"],
        },
        "historial": {
            "descripcion": "Buffer liviano de ultimos calculos.",
            "entrada": "limite opcional: int",
            "validar_esquema": ["*"],
            "salida": "list[dict]",
            "acceso_archivos": ["*"],
        },
        "verificar_calculo_de_C_L_K": {
            "descripcion": (
                "Verifica la integridad y coherencia del calculo "
                "de C, L y K."
            ),
            "entrada": "calculo: dict",
            "validar_esquema": ["*"],
            "salida": (
                "dict con valido, errores, advertencias, "
                "C, L, K y verificacion"
            ),
            "acceso_archivos": ["*"],
        },
        "ejecutar_total": {
            "descripcion": (
                "Autoridad total de ENGINE sobre CA. "
                "Ejerce TODAS las unidades operativamente ejecutables "
                "del modulo conforme a su contrato e inventario. "
                "Todo es callable real. No inventa capacidades."
            ),
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["*"],
            "salida": "dict con resultados de todas las unidades ejecutadas",
            "acceso_archivos": ["*"],
        },
        "inspeccionar": {
            "descripcion": (
                "Capacidad meta de inspeccion estructural de CA. "
                "Expone constantes, capacidades, APIs y estado "
                "sin alterar el contrato ni calcular factores."
            ),
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["acceso_archivos"],
            "salida": "dict con estructura, capacidades y estado del modulo",
            "acceso_archivos": ["acceso_archivos"],
        },
        "registrar_inventario": {
            "descripcion": (
                "Registra el inventario estructural de CA "
                "como instantanea determinista. No altera evidencia."
            ),
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["acceso_archivos"],
            "salida": "dict con inventario registrado",
            "acceso_archivos": ["acceso_archivos"],
        },
        "evaluar_universal": {
            "descripcion": (
                "Evalúa las capacidades reales de este módulo "
                "cuya firma se satisfaga con los hechos de entrada. "
                "Engine entrega la entrada; este callable solo aplica lo local."
           ),
          "entrada": "hechos: dict",
          "validar_esquema": ["*"],
          "salida": "dict con hechos, traza, ejecutadas",
          "acceso_archivos": ["*"],
         },
    },
    
    # ============================================================
    # 5.14 — REPORTING (OBLIGATORIO EN EL ESQUEMA)
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

        # --- BANDERAS OBLIGATORIAS  ENGINE ---
        "acceso_archivos": True,
        "validar_esquema": True,

        # --- BANDERAS NUEVAS (OBLIGATORIAS ENGINE) ---
        "ejecutar_total": True,
        "inspeccionar": True,
        "registrar_inventario": True,
        "evaluar_universal": True,
    },

    # ============================================================
    # 5.15 — ESTADOS VÁLIDOS
    # ============================================================
    "estados_validos": list(ESTADOS_VALIDOS),

    # ============================================================
    # 5.16 — INVARIANTES
    # ============================================================
    "invariantes": list(INVARIANTES),

}  # <--- CIERRE FINAL

# ===============================================================
# FIN PARTE 5
# ===============================================================

# ===============================================================
# PARTE 7 — FUNCIONES PRIVADAS
# ===============================================================

# ===============================================================
# 7.1 — CARGA DE APIs C/L/K
# ===============================================================

def _importar_apis() -> Tuple[Dict[str, Any], List[Dict[str, str]]]:
    apis: Dict[str, Any] = {}
    errores: List[Dict[str, str]] = []
    pares = (
        ("coherencia", "calcular_c", "C"),
        ("logica", "calcular_l", "L"),
        ("correlacion_k", "calcular_k", "K"),
    )
    for mod_name, fn_name, factor in pares:
        try:
            mod = importlib.import_module(
                "modules.calculator.{0}".format(mod_name)
            )
            fn = getattr(mod, fn_name, None)
            if not callable(fn):
                errores.append({
                    "archivo": "{0}.py".format(mod_name),
                    "error": "falta API '{0}'".format(fn_name),
                })
                continue
            apis[factor] = fn
        except Exception as e:  # noqa: BLE001
            errores.append({
                "archivo": "{0}.py".format(mod_name),
                "error": "{0}: {1}".format(type(e).__name__, e),
            })
    return apis, errores


_APIS, _ERRORES_CARGA = _importar_apis()

# ===============================================================
# FIN 7.1
# ===============================================================


# ===============================================================
# 7.2 — CARGA DE CONTEOS
# ===============================================================

def _cargar_conteos():
    try:
        mod = importlib.import_module("modules.calculator.conteos")
        extraer = getattr(mod, "extraer_conteos", None)
        inyectar = getattr(mod, "inyectar_en_peticion", None)
        if callable(extraer) and callable(inyectar):
            return {
                "extraer_conteos": extraer,
                "inyectar_en_peticion": inyectar,
            }
    except Exception:  # noqa: BLE001
        pass
    return None


_CONTEOS = _cargar_conteos()

# ===============================================================
# FIN 7.2
# ===============================================================


# ===============================================================
# 7.3 — CARGA DE ESCALAS / IDS
# ===============================================================

def _cargar_escalas_ids():
    try:
        mod = importlib.import_module("modules.calculator.escalas_ids")
        ids_fn = getattr(mod, "ids", None)
        por_id = getattr(mod, "por_id", None)
        if callable(ids_fn):
            return {
                "ids": ids_fn,
                "por_id": por_id if callable(por_id) else None,
            }
    except Exception:  # noqa: BLE001
        pass
    return None


_ESCALAS = _cargar_escalas_ids()

# ===============================================================
# FIN 7.3
# ===============================================================


# ===============================================================
# 7.4 — ARCHIVOS Y HASHES
# ===============================================================

def _listar_py() -> List[Path]:
    return [
        f for f in sorted(_DIR.glob("*.py"))
        if f.name != "__init__.py" and not f.name.startswith("_")
    ]


def _meta_archivo(path: Path) -> Dict[str, Any]:
    try:
        st = path.stat()
        h = hashlib.sha256()
        with path.open("rb") as fh:
            for chunk in iter(lambda: fh.read(65536), b""):
                h.update(chunk)
        return {
            "archivo": path.name,
            "sha256": h.hexdigest(),
            "tamano": st.st_size,
            "timestamp_mtime": datetime.fromtimestamp(
                st.st_mtime, tz=timezone.utc
            ).isoformat(),
        }
    except Exception as e:  # noqa: BLE001
        return {
            "archivo": path.name,
            "sha256": None,
            "tamano": None,
            "timestamp_mtime": None,
            "error": "{0}: {1}".format(type(e).__name__, e),
        }


def _hashes_modulo() -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {
        "__init__.py": _meta_archivo(_DIR / "__init__.py")
    }
    for p in _listar_py():
        out[p.name] = _meta_archivo(p)
    return out

# ===============================================================
# FIN 7.4
# ===============================================================


# ===============================================================
# 7.5 — CONVERSIÓN Y CONTEOS OPERACIONALES
# ===============================================================

def _a_fraction(x: Any) -> Optional[Fraction]:
    if x is None or es_undefined(x):
        return None
    if isinstance(x, Fraction):
        return x
    if isinstance(x, Decimal):
        return Fraction(x)
    if isinstance(x, int):
        return Fraction(x)
    if isinstance(x, float):
        return Fraction(x).limit_denominator(10_000)
    if isinstance(x, str):
        try:
            return Fraction(x)
        except Exception:  # noqa: BLE001
            return None
    return None


def _faltan_conteos(peticion: Dict[str, Any]) -> bool:
    for k in _CLAVES_CONTEO:
        if k not in peticion or peticion[k] is None:
            return True
    return False


def _asegurar_conteos(peticion: Dict[str, Any]) -> Dict[str, Any]:
    if _CONTEOS is None:
        return peticion
    if not _faltan_conteos(peticion):
        return peticion
    return _CONTEOS["inyectar_en_peticion"](peticion)


def _id_escala_pedido(peticion: Dict[str, Any]) -> Optional[str]:
    for clave in ("escala_id", "categoria_tru", "id_escala", "escala"):
        v = peticion.get(clave)
        if v is not None and str(v).strip():
            return str(v).strip().lower()
    return None

# ===============================================================
# FIN 7.5
# ===============================================================


# ===============================================================
# 7.6 — IDS DE CÁLCULO Y EVIDENCIA
# ===============================================================

def _nuevo_id_calculo() -> str:
    global _CALC_SEQ
    _CALC_SEQ += 1
    dia = datetime.now(timezone.utc).strftime("%Y%m%d")
    return "CA-{0}-{1:06d}".format(dia, _CALC_SEQ)


def _nuevo_id_evidencia() -> str:
    global _EV_SEQ
    _EV_SEQ += 1
    return "EV-{0:09d}".format(_EV_SEQ)


def _normalizar_evidencia(raw: Any) -> List[Dict[str, Any]]:
    if not raw:
        return []
    if isinstance(raw, dict):
        raw = [raw]
    if not isinstance(raw, list):
        return []
    out: List[Dict[str, Any]] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        eid = item.get("id_evidencia") or _nuevo_id_evidencia()
        entry = {
            "id_evidencia": str(eid),
            "modulo": str(item.get("modulo") or item.get("nombre") or "?"),
            "capacidad": str(item.get("capacidad") or item.get("cap") or "?"),
            "aporte": item.get("aporte") or item.get("id") or item.get("valor"),
            "version_modulo": item.get("version_modulo") or item.get("version"),
            "version_contrato": item.get("version_contrato"),
            "rechazado": bool(item.get("rechazado", False)),
        }
        out.append(entry)
        _REG_EVIDENCIA[entry["id_evidencia"]] = entry
    return out


def _acepta_dict(fn: Any) -> bool:
    try:
        import inspect
        sig = inspect.signature(fn)
        params = list(sig.parameters.values())
        if not params:
            return False
        if len(params) == 1:
            return True
        if params[0].name in ("peticion", "request", "payload"):
            return True
    except Exception:  # noqa: BLE001
        pass
    return False

# ===============================================================
# FIN 7.6
# ===============================================================


# ===============================================================
# 7.7 — CENTINELA DE RESULTADO
# ===============================================================

def _centinela_resultado(
    salida: Dict[str, Any],
    peticion: Dict[str, Any],
    evidencia: List[Dict[str, Any]],
) -> Dict[str, Any]:
    problemas: List[str] = []
    advertencias: List[str] = []

    if CONTENEDOR.get("esquema") != ESQUEMA_CONTRATO:
        problemas.append("esquema del contrato CA incompatible")

    for factor in _FACTORES_CANONICOS:
        bloque = salida.get(factor)
        if bloque is None:
            continue
        if not isinstance(bloque, dict):
            problemas.append("factor '{0}' debe ser dict valor".format(factor))
            continue
        if bloque.get("undefined"):
            continue
        if bloque.get("fraccion") and not bloque.get("decimal"):
            problemas.append(
                "factor '{0}' tiene fraccion sin decimal".format(factor)
            )
        if bloque.get("fraccion") and (
            bloque.get("numerador") is None or bloque.get("denominador") is None
        ):
            problemas.append(
                "factor '{0}' sin numerador/denominador".format(factor)
            )

    for ev in evidencia:
        if ev.get("rechazado"):
            problemas.append(
                "evidencia de modulo rechazado: {0}".format(ev.get("modulo"))
            )

    # Mismo modulo con versiones distintas
    por_mod: Dict[str, set] = {}
    for ev in evidencia:
        mod = ev.get("modulo")
        ver = ev.get("version_modulo")
        if mod and ver:
            por_mod.setdefault(str(mod), set()).add(str(ver))
    for mod, vers in por_mod.items():
        if len(vers) > 1:
            problemas.append(
                "modulo '{0}' aparece con versiones distintas: {1}".format(
                    mod, sorted(vers)
                )
            )

    esperadas = peticion.get("versiones_esperadas") or {}
    if isinstance(esperadas, dict):
        for ev in evidencia:
            mod = ev.get("modulo")
            ver = ev.get("version_modulo")
            exp = esperadas.get(mod)
            if exp and ver and str(ver) != str(exp):
                advertencias.append(
                    "version de {0}: evidencia={1}, esperada={2}".format(
                        mod, ver, exp
                    )
                )

    if salida.get("K") is None and not (
        peticion.get("contexto")
        or peticion.get("O_context")
        or peticion.get("o_context")
    ):
        advertencias.append("K=None legitimo: sin contexto/O (Def-5.3.1)")

    if isinstance(salida.get("L"), dict) and salida["L"].get("undefined"):
        advertencias.append("L=UNDEFINED: p=0 (AM-D6/AM-A3)")

    if not evidencia:
        advertencias.append(
            "sin evidencia externa; calculo solo con datos de peticion/CA"
        )

    return {
        "ok": not problemas,
        "problemas": problemas,
        "advertencias": advertencias,
        "evidencia_n": len(evidencia),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

# ===============================================================
# FIN 7.7
# ===============================================================


# ===============================================================
# 7.8 — VALIDACIÓN DEL CONTRATO
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
        raise ContratoInvalido(f"{NOMBRE_MODULO}: esquema incompatible")
    if str(cont.get("version_contrato")) != VERSION_CONTRATO:
        raise ContratoInvalido(f"{NOMBRE_MODULO}: version_contrato invalida")
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
# FIN 7.8
# ===============================================================

# ===============================================================
# FIN PARTE 7
# ===============================================================

# ===============================================================
# PARTE 8 — CAPACIDADES PÚBLICAS
# ===============================================================

# ===============================================================
# 8.1 — REPRESENTAR
# ===============================================================

def representar(
    valor: Any,
    precision: int = PRECISION_DECIMAL_DEFAULT,
) -> Dict[str, Any]:
    """
    Un solo objeto determinista:
      7/9 = 0.778
    con numerador/denominador explicitos.
    """
    prec = max(0, int(precision))

    if es_undefined(valor):
        return {
            "valor": UNDEFINED,
            "fraccion": None,
            "numerador": None,
            "denominador": None,
            "decimal": None,
            "display": "UNDEFINED",
            "precision": prec,
            "undefined": True,
        }
    if valor is None:
        return {
            "valor": None,
            "fraccion": None,
            "numerador": None,
            "denominador": None,
            "decimal": None,
            "display": "None",
            "precision": prec,
            "undefined": False,
        }

    fr = _a_fraction(valor)
    if fr is None:
        return {
            "valor": None,
            "fraccion": None,
            "numerador": None,
            "denominador": None,
            "decimal": None,
            "display": "?",
            "precision": prec,
            "undefined": False,
            "error": "no convertible a Fraction",
        }

    dec_val = Decimal(fr.numerator) / Decimal(fr.denominator)
    quant = Decimal("1").scaleb(-prec)
    dec_str = str(dec_val.quantize(quant, rounding=ROUND_HALF_UP))
    frac_str = str(fr)
    return {
        "valor": fr,
        "fraccion": frac_str,
        "numerador": fr.numerator,
        "denominador": fr.denominator,
        "decimal": dec_str,
        "display": "{0} = {1}".format(frac_str, dec_str),
        "precision": prec,
        "undefined": False,
    }

# ===============================================================
# FIN 8.1
# ===============================================================


# ===============================================================
# 8.2 — VALIDAR EVIDENCIA
# ===============================================================

def validar_evidencia(evidencia: Any = None) -> Dict[str, Any]:
    """Valida evidencia sin calcular."""
    normalizada = _normalizar_evidencia(evidencia)
    problemas: List[str] = []
    advertencias: List[str] = []

    for ev in normalizada:
        if not ev.get("modulo") or ev["modulo"] == "?":
            problemas.append(
                "evidencia {0} sin modulo".format(ev.get("id_evidencia"))
            )
        if not ev.get("capacidad") or ev["capacidad"] == "?":
            advertencias.append(
                "evidencia {0} sin capacidad".format(ev.get("id_evidencia"))
            )
        if ev.get("rechazado"):
            problemas.append(
                "modulo rechazado: {0}".format(ev.get("modulo"))
            )

    por_mod: Dict[str, set] = {}
    for ev in normalizada:
        mod = ev.get("modulo")
        ver = ev.get("version_modulo")
        if mod and ver:
            por_mod.setdefault(str(mod), set()).add(str(ver))
    for mod, vers in por_mod.items():
        if len(vers) > 1:
            problemas.append(
                "modulo '{0}' con versiones distintas: {1}".format(
                    mod, sorted(vers)
                )
            )

    return {
        "ok": not problemas,
        "problemas": problemas,
        "advertencias": advertencias,
        "evidencia_normalizada": normalizada,
        "n": len(normalizada),
    }

# ===============================================================
# FIN 8.2
# ===============================================================


# ===============================================================
# 8.3 — LEER IDS ESCALA
# ===============================================================

def leer_ids_escala() -> Dict[str, Any]:
    ids_local: List[str] = []
    origenes: List[str] = []
    if _ESCALAS is not None:
        try:
            ids_local = list(_ESCALAS["ids"]())
            origenes.append("escalas_ids")
        except Exception:  # noqa: BLE001
            pass
    unidos: List[str] = []
    vistos = set()
    for i in ids_local:
        k = str(i).strip().lower()
        if k and k not in vistos:
            vistos.add(k)
            unidos.append(k)
    return {
        "ids": unidos,
        "n": len(unidos),
        "origenes": origenes,
        "disponible": bool(unidos),
    }

# ===============================================================
# FIN 8.3
# ===============================================================
# ===============================================================
# 8.4 — BARRER / VERIFICAR
# ===============================================================

def barrer() -> Dict[str, Any]:
    """
    Centinela determinista de integridad del dominio CA.

    Responsabilidad exclusiva:
        verificar estructura, presencia, correspondencia y callability.

    No calcula C.
    No calcula L.
    No calcula K.
    No ejecuta calcular().
    No interpreta fórmulas.
    No crea capacidades.
    No modifica el contrato.
    No resuelve capacidades contractuales.
    No depende de _CAP_MAP.

    La coherencia solo puede ser True cuando todas las condiciones
    estructurales declaradas por este contenedor son satisfechas.
    """

    # -----------------------------------------------------------
    # 8.4.1 — ESTADO INICIAL DEL CENTINELA
    # -----------------------------------------------------------

    errores: List[Dict[str, str]] = list(_ERRORES_CARGA)
    choques: List[str] = []

    archivos = [p.name for p in _listar_py()]
    hashes = _hashes_modulo()

    # -----------------------------------------------------------
    # 8.4.2 — FACTORES CANÓNICOS
    #
    # Contrato:
    #     factor
    #       → stem declarado
    #       → archivo físico existente
    #       → API cargada
    #       → API callable
    #
    # No se calcula ningún factor.
    # -----------------------------------------------------------

    factores_ok: List[str] = []
    apis_factor: Dict[str, bool] = {}

    # Detectar todos los stems declarados por factor.
    factores_declarados: Dict[str, List[str]] = {}

    for stem, factor in _ARCHIVO_FACTOR.items():
        factores_declarados.setdefault(
            factor,
            [],
        ).append(stem)

    # -----------------------------------------------------------
    # 8.4.3 — DETECCIÓN DE COLISIÓN FACTOR → STEM
    #
    # Un factor canónico no puede tener múltiples stems físicos
    # reclamándolo.
    # -----------------------------------------------------------

    for factor, stems in sorted(factores_declarados.items()):
        if len(stems) > 1:
            choques.append(
                "factor '{0}' reclamado por múltiples stems: {1}".format(
                    factor,
                    sorted(stems),
                )
            )

    # -----------------------------------------------------------
    # 8.4.4 — FACTOR → STEM → ARCHIVO → API
    # -----------------------------------------------------------

    for factor in _FACTORES_CANONICOS:

        stems = factores_declarados.get(factor) or []

        # -------------------------------------------------------
        # 8.4.4.1 — STEM DECLARADO
        # -------------------------------------------------------

        if len(stems) == 0:
            errores.append({
                "archivo": "?",
                "error": (
                    "factor '{0}' sin stem declarado en "
                    "_ARCHIVO_FACTOR"
                ).format(factor),
            })

            apis_factor[factor] = False
            continue

        # -------------------------------------------------------
        # 8.4.4.2 — STEM ÚNICO
        # -------------------------------------------------------

        if len(stems) != 1:
            errores.append({
                "archivo": "?",
                "error": (
                    "factor '{0}' tiene {1} stems declarados: {2}"
                ).format(
                    factor,
                    len(stems),
                    sorted(stems),
                ),
            })

            apis_factor[factor] = False
            continue

        stem = stems[0]

        # -------------------------------------------------------
        # 8.4.4.3 — ARCHIVO FÍSICO
        # -------------------------------------------------------

        path = _DIR / "{0}.py".format(stem)

        if not path.exists():
            errores.append({
                "archivo": "{0}.py".format(stem),
                "error": (
                    "factor '{0}' declara stem '{1}' pero "
                    "el archivo no existe fisicamente"
                ).format(
                    factor,
                    stem,
                ),
            })

            apis_factor[factor] = False
            continue

        # -------------------------------------------------------
        # 8.4.4.4 — API CARGADA
        # -------------------------------------------------------

        fn = _APIS.get(factor)

        if fn is None:
            errores.append({
                "archivo": "{0}.py".format(stem),
                "error": (
                    "factor '{0}' tiene archivo '{1}.py' pero "
                    "no existe API cargada en _APIS"
                ).format(
                    factor,
                    stem,
                ),
            })

            apis_factor[factor] = False
            continue

        # -------------------------------------------------------
        # 8.4.4.5 — API CALLABLE
        # -------------------------------------------------------

        es_callable = callable(fn)
        apis_factor[factor] = es_callable

        if not es_callable:
            errores.append({
                "archivo": "{0}.py".format(stem),
                "error": (
                    "factor '{0}' tiene API cargada pero "
                    "no es callable"
                ).format(factor),
            })
            continue

        factores_ok.append(factor)

    # -----------------------------------------------------------
    # 8.4.5 — APIs DE FACTORES NO DECLARADAS
    #
    # Toda API factor cargada en _APIS debe pertenecer al contrato
    # canónico.
    # -----------------------------------------------------------

    factores_no_declarados = sorted(
        set(_APIS.keys()) -
        set(_FACTORES_CANONICOS)
    )

    for factor_extra in factores_no_declarados:
        errores.append({
            "archivo": "?",
            "error": (
                "API de factor '{0}' cargada en _APIS pero "
                "no pertenece a _FACTORES_CANONICOS"
            ).format(factor_extra),
        })

    # -----------------------------------------------------------
    # 8.4.6 — ARCHIVOS EXTRA
    #
    # La existencia de un archivo adicional no es contradicción
    # por sí misma.
    # -----------------------------------------------------------

    stems_conocidos = (
        set(_ARCHIVO_FACTOR.keys())
        | {
            "conteos",
            "escalas_ids",
        }
    )

    extra = sorted(
        p.stem
        for p in _listar_py()
        if p.stem not in stems_conocidos
    )

    # -----------------------------------------------------------
    # 8.4.7 — HASHES
    #
    # Todo archivo incluido en el inventario debe poder ser
    # identificado mediante SHA-256.
    # -----------------------------------------------------------

    for nombre, meta in hashes.items():
        if meta.get("sha256") is None:
            errores.append({
                "archivo": nombre,
                "error": (
                    meta.get("error")
                    or
                    "hash no calculable"
                ),
            })

    # -----------------------------------------------------------
    # 8.4.8 — CONTEOS
    #
    # Contrato vigente:
    #     extraer_conteos
    #     inyectar_en_peticion
    #
    # No se agrega verificar_conteos porque no pertenece al
    # contrato declarado.
    # -----------------------------------------------------------

    extraer_ok = (
        _CONTEOS is not None
        and callable(
            _CONTEOS.get("extraer_conteos")
        )
    )

    inyectar_ok = (
        _CONTEOS is not None
        and callable(
            _CONTEOS.get("inyectar_en_peticion")
        )
    )

    conteos_ok = (
        extraer_ok
        and inyectar_ok
    )

    if _CONTEOS is None:

        errores.append({
            "archivo": "conteos.py",
            "error": "API de conteos no cargada",
        })

    else:

        if not extraer_ok:
            errores.append({
                "archivo": "conteos.py",
                "error": (
                    "extraer_conteos no es callable"
                ),
            })

        if not inyectar_ok:
            errores.append({
                "archivo": "conteos.py",
                "error": (
                    "inyectar_en_peticion no es callable"
                ),
            })

    apis_conteos = {
        "extraer_conteos": extraer_ok,
        "inyectar_en_peticion": inyectar_ok,
    }

    # -----------------------------------------------------------
    # 8.4.9 — ESCALAS
    #
    # Se valida:
    #     API ids callable
    #     ejecución de lectura
    #     estructura de retorno
    #     ids como list
    #     n == len(ids)
    #
    # No se modifica el inventario.
    # -----------------------------------------------------------

    escalas_ok = (
        _ESCALAS is not None
        and callable(
            _ESCALAS.get("ids")
        )
    )

    ids_escala: Dict[str, Any] = {
        "ids": [],
        "n": 0,
        "origenes": [],
        "disponible": False,
    }

    if _ESCALAS is None:

        errores.append({
            "archivo": "escalas_ids.py",
            "error": (
                "API de escalas_ids no cargada"
            ),
        })

        escalas_ok = False

    elif not callable(
        _ESCALAS.get("ids")
    ):

        errores.append({
            "archivo": "escalas_ids.py",
            "error": (
                "escalas_ids.ids no es callable"
            ),
        })

        escalas_ok = False

    else:

        try:

            resultado = leer_ids_escala()

            # ---------------------------------------------------
            # 8.4.9.1 — ESTRUCTURA
            # ---------------------------------------------------

            if not (
                isinstance(resultado, dict)
                and "ids" in resultado
                and "n" in resultado
                and "disponible" in resultado
            ):

                errores.append({
                    "archivo": "escalas_ids.py",
                    "error": (
                        "leer_ids_escala retorno "
                        "estructura invalida"
                    ),
                })

                escalas_ok = False

            else:

                ids_list = resultado.get("ids")
                n_val = resultado.get("n")

                # -----------------------------------------------
                # 8.4.9.2 — TIPO DE IDS
                # -----------------------------------------------

                if not isinstance(
                    ids_list,
                    list,
                ):

                    errores.append({
                        "archivo": "escalas_ids.py",
                        "error": (
                            "leer_ids_escala: "
                            "'ids' no es list"
                        ),
                    })

                    escalas_ok = False

                # -----------------------------------------------
                # 8.4.9.3 — CONSISTENCIA N
                # -----------------------------------------------

                elif n_val != len(ids_list):

                    errores.append({
                        "archivo": "escalas_ids.py",
                        "error": (
                            "leer_ids_escala: n={0} "
                            "!= len(ids)={1}"
                        ).format(
                            n_val,
                            len(ids_list),
                        ),
                    })

                    escalas_ok = False

                # -----------------------------------------------
                # 8.4.9.4 — RESULTADO VÁLIDO
                # -----------------------------------------------

                else:

                    ids_escala = resultado
                    escalas_ok = True

        except Exception as e:  # noqa: BLE001

            errores.append({
                "archivo": "escalas_ids.py",
                "error": (
                    "leer_ids_escala fallo: {0}: {1}"
                ).format(
                    type(e).__name__,
                    e,
                ),
            })

            escalas_ok = False

    # -----------------------------------------------------------
    # 8.4.10 — COHERENCIA FINAL
    #
    # barrer NO ejecuta calcular_C/L/K.
    #
    # La coherencia depende exclusivamente de la integridad
    # estructural validada por esta función.
    # -----------------------------------------------------------

    coherente = (
        not errores
        and not choques
    )

    # -----------------------------------------------------------
    # 8.4.11 — RETORNO CONTRACTUAL
    # -----------------------------------------------------------

    return {
        "contenedor": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "coherente": coherente,
        "errores": errores,
        "choques": choques,
        "archivos": archivos,
        "hashes": hashes,
        "factores_api": sorted(factores_ok),
        "factores_no_declarados": factores_no_declarados,
        "archivos_extra": extra,
        "conteos_disponible": conteos_ok,
        "escalas_ids_disponible": escalas_ok,
        "ids_escala": ids_escala,
        "historial_n": len(_HISTORIAL),
        "apis_factor": apis_factor,
        "apis_conteos": apis_conteos,
    }


# ===============================================================
# 8.4.12 — VERIFICAR
# ===============================================================

def verificar() -> Dict[str, Any]:
    """
    Alias contractual 1:1 de barrer.

    No contiene lógica independiente.
    No duplica la verificación.
    No modifica el resultado.

        verificar()
            ↓
        barrer()
    """
    return barrer()


# ===============================================================
# FIN 8.4
# ===============================================================
# ===============================================================
# 8.5 — CALCULAR C
# ===============================================================

def calcular_C(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Ejecuta exclusivamente el cálculo contractual del factor C.

    Fórmula contractual ejecutada por la API C:
        C = 1 - k/m

    Correspondencia de variables:
        m = compromisos
        k = contradicciones

    Flujo determinista:
        entrada
        → método
        → precisión
        → conteos cuando corresponde
        → evidencia
        → API C
        → resultado C
        → normalización
        → representación
        → salida.

    No calcula L ni K.
    No implementa una fórmula paralela.
    No sustituye una API C ausente.
    """

    # -----------------------------------------------------------
    # 8.5.1 — ENTRADA
    # -----------------------------------------------------------
    if peticion is None:
        peticion = {}
    elif not isinstance(peticion, dict):
        return {
            "C": representar(
                None,
                PRECISION_DECIMAL_DEFAULT,
            ),
            "ruta": None,
            "notas": [
                "Peticion invalida: se esperaba dict"
            ],
            "evidencia": [],
        }
    else:
        peticion = dict(peticion)

    # -----------------------------------------------------------
    # 8.5.2 — MÉTODO
    # -----------------------------------------------------------
    metodo = str(
        peticion.get("metodo") or "operacional"
    )

    # -----------------------------------------------------------
    # 8.5.3 — PRECISIÓN
    # -----------------------------------------------------------
    try:
        prec = int(
            peticion.get("precision")
            or PRECISION_DECIMAL_DEFAULT
        )
    except (TypeError, ValueError):
        prec = PRECISION_DECIMAL_DEFAULT

    if prec < 0:
        prec = PRECISION_DECIMAL_DEFAULT

    # -----------------------------------------------------------
    # 8.5.4 — CONTEOS
    # -----------------------------------------------------------
    if metodo == "operacional":
        try:
            peticion = _asegurar_conteos(peticion)
        except Exception as e:  # noqa: BLE001
            evidencia = _normalizar_evidencia(
                peticion.get("evidencia")
            )

            evidencia.append({
                "id_evidencia": _nuevo_id_evidencia(),
                "modulo": NOMBRE_MODULO,
                "capacidad": "calcular_C",
                "aporte": "factor_C",
                "version_modulo": VERSION_MODULO,
                "version_contrato": VERSION_CONTRATO,
                "rechazado": True,
            })

            for e in evidencia:
                _REG_EVIDENCIA[e["id_evidencia"]] = e

            return {
                "C": representar(None, prec),
                "ruta": metodo,
                "notas": [
                    "Error preparando conteos para C: {0}".format(e)
                ],
                "evidencia": evidencia,
            }

    # -----------------------------------------------------------
    # 8.5.5 — EVIDENCIA
    # -----------------------------------------------------------
    evidencia = _normalizar_evidencia(
        peticion.get("evidencia")
    )

    evidencia.append({
        "id_evidencia": _nuevo_id_evidencia(),
        "modulo": NOMBRE_MODULO,
        "capacidad": "calcular_C",
        "aporte": "factor_C",
        "version_modulo": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "rechazado": False,
    })

    for e in evidencia:
        _REG_EVIDENCIA[e["id_evidencia"]] = e

    # -----------------------------------------------------------
    # 8.5.6 — RESOLUCIÓN DE API C
    # -----------------------------------------------------------
    fn = _APIS.get("C")

    if not callable(fn):
        evidencia[-1]["rechazado"] = True

        return {
            "C": representar(None, prec),
            "ruta": None,
            "notas": [
                "API C no disponible"
            ],
            "evidencia": evidencia,
        }

    # -----------------------------------------------------------
    # 8.5.7 — EJECUCIÓN DE API C
    # -----------------------------------------------------------
    try:
        if _acepta_dict(fn):
            raw = fn(peticion)
        else:
            raw = fn(
                compromisos=peticion.get("compromisos"),
                contradicciones=peticion.get(
                    "contradicciones"
                ),
                metodo=metodo,
            )
    except Exception as e:  # noqa: BLE001
        evidencia[-1]["rechazado"] = True

        return {
            "C": representar(None, prec),
            "ruta": metodo,
            "notas": [
                "Error en API C: {0}: {1}".format(
                    type(e).__name__,
                    e,
                )
            ],
            "evidencia": evidencia,
        }

    # -----------------------------------------------------------
    # 8.5.8 — RESULTADO C
    # -----------------------------------------------------------
    if isinstance(raw, dict):
        if "C" not in raw:
            evidencia[-1]["rechazado"] = True

            return {
                "C": representar(None, prec),
                "ruta": metodo,
                "notas": [
                    "API C retorno dict sin campo 'C'"
                ],
                "evidencia": evidencia,
            }

        val = raw["C"]
    else:
        val = raw

    # -----------------------------------------------------------
    # 8.5.9 — UNDEFINED
    # -----------------------------------------------------------
    if es_undefined(val):
        obj = representar(
            UNDEFINED,
            prec,
        )

        return {
            "C": obj,
            "ruta": metodo,
            "notas": [],
            "evidencia": evidencia,
        }

    # -----------------------------------------------------------
    # 8.5.10 — NORMALIZACIÓN
    # -----------------------------------------------------------
    try:
        fraccion = (
            val
            if isinstance(val, Fraction)
            else _a_fraction(val)
        )
    except Exception as e:  # noqa: BLE001
        evidencia[-1]["rechazado"] = True

        return {
            "C": representar(None, prec),
            "ruta": metodo,
            "notas": [
                "Valor C no normalizable: {0}: {1}".format(
                    type(e).__name__,
                    e,
                )
            ],
            "evidencia": evidencia,
        }

    # -----------------------------------------------------------
    # 8.5.11 — REPRESENTACIÓN
    # -----------------------------------------------------------
    try:
        obj = representar(
            fraccion,
            prec,
        )
    except Exception as e:  # noqa: BLE001
        evidencia[-1]["rechazado"] = True

        return {
            "C": representar(None, prec),
            "ruta": metodo,
            "notas": [
                "Error representando C: {0}: {1}".format(
                    type(e).__name__,
                    e,
                )
            ],
            "evidencia": evidencia,
        }

    # -----------------------------------------------------------
    # 8.5.12 — SALIDA
    # -----------------------------------------------------------
    return {
        "C": obj,
        "ruta": metodo,
        "notas": [],
        "evidencia": evidencia,
    }


# ===============================================================
# FIN 8.5
# ===============================================================


# ===============================================================
# 8.6 — CALCULAR L
# ===============================================================

def calcular_L(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Ejecuta exclusivamente el cálculo contractual del factor L.

    Fórmula contractual ejecutada por la API L:
        L = 1 - r/p

    Correspondencia de variables:
        p = posturas
        r = reversiones

    Flujo determinista:
        entrada
        → método
        → precisión
        → conteos cuando corresponde
        → evidencia
        → API L
        → resultado L
        → normalización
        → representación
        → salida.

    No calcula C ni K.
    No implementa una fórmula paralela.
    No sustituye una API L ausente.
    """

    # -----------------------------------------------------------
    # 8.6.1 — ENTRADA
    # -----------------------------------------------------------
    if peticion is None:
        peticion = {}
    elif not isinstance(peticion, dict):
        return {
            "L": representar(
                None,
                PRECISION_DECIMAL_DEFAULT,
            ),
            "p": None,
            "r": None,
            "ruta": None,
            "notas": [
                "Peticion invalida: se esperaba dict"
            ],
            "evidencia": [],
        }
    else:
        peticion = dict(peticion)

    # -----------------------------------------------------------
    # 8.6.2 — MÉTODO
    # -----------------------------------------------------------
    metodo = str(
        peticion.get("metodo") or "operacional"
    )

    # -----------------------------------------------------------
    # 8.6.3 — PRECISIÓN
    # -----------------------------------------------------------
    try:
        prec = int(
            peticion.get("precision")
            or PRECISION_DECIMAL_DEFAULT
        )
    except (TypeError, ValueError):
        prec = PRECISION_DECIMAL_DEFAULT

    if prec < 0:
        prec = PRECISION_DECIMAL_DEFAULT

    # -----------------------------------------------------------
    # 8.6.4 — CONTEOS
    # -----------------------------------------------------------
    if metodo == "operacional":
        try:
            peticion = _asegurar_conteos(peticion)
        except Exception as e:  # noqa: BLE001
            evidencia = _normalizar_evidencia(
                peticion.get("evidencia")
            )

            evidencia.append({
                "id_evidencia": _nuevo_id_evidencia(),
                "modulo": NOMBRE_MODULO,
                "capacidad": "calcular_L",
                "aporte": "factor_L",
                "version_modulo": VERSION_MODULO,
                "version_contrato": VERSION_CONTRATO,
                "rechazado": True,
            })

            for e in evidencia:
                _REG_EVIDENCIA[e["id_evidencia"]] = e

            return {
                "L": representar(None, prec),
                "p": None,
                "r": None,
                "ruta": metodo,
                "notas": [
                    "Error preparando conteos para L: {0}".format(e)
                ],
                "evidencia": evidencia,
            }

    # -----------------------------------------------------------
    # 8.6.5 — EVIDENCIA
    # -----------------------------------------------------------
    evidencia = _normalizar_evidencia(
        peticion.get("evidencia")
    )

    evidencia.append({
        "id_evidencia": _nuevo_id_evidencia(),
        "modulo": NOMBRE_MODULO,
        "capacidad": "calcular_L",
        "aporte": "factor_L",
        "version_modulo": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "rechazado": False,
    })

    for e in evidencia:
        _REG_EVIDENCIA[e["id_evidencia"]] = e

    # -----------------------------------------------------------
    # 8.6.6 — RESOLUCIÓN DE API L
    # -----------------------------------------------------------
    fn = _APIS.get("L")

    if not callable(fn):
        evidencia[-1]["rechazado"] = True

        return {
            "L": representar(None, prec),
            "p": None,
            "r": None,
            "ruta": None,
            "notas": [
                "API L no disponible"
            ],
            "evidencia": evidencia,
        }

    # -----------------------------------------------------------
    # 8.6.7 — EJECUCIÓN DE API L
    # -----------------------------------------------------------
    try:
        if _acepta_dict(fn):
            raw = fn(peticion)
        else:
            raw = fn(
                posturas=peticion.get("posturas"),
                reversiones=peticion.get(
                    "reversiones"
                ),
                metodo=metodo,
            )
    except Exception as e:  # noqa: BLE001
        evidencia[-1]["rechazado"] = True

        return {
            "L": representar(None, prec),
            "p": None,
            "r": None,
            "ruta": metodo,
            "notas": [
                "Error en API L: {0}: {1}".format(
                    type(e).__name__,
                    e,
                )
            ],
            "evidencia": evidencia,
        }

    # -----------------------------------------------------------
    # 8.6.8 — RESULTADO L
    # -----------------------------------------------------------
    p = None
    r = None

    if isinstance(raw, dict):
        if "L" not in raw:
            evidencia[-1]["rechazado"] = True

            return {
                "L": representar(None, prec),
                "p": None,
                "r": None,
                "ruta": metodo,
                "notas": [
                    "API L retorno dict sin campo 'L'"
                ],
                "evidencia": evidencia,
            }

        val = raw["L"]
        p = raw.get("p")
        r = raw.get("r")
    else:
        val = raw

    # -----------------------------------------------------------
    # 8.6.9 — UNDEFINED
    # -----------------------------------------------------------
    if es_undefined(val):
        obj = representar(
            UNDEFINED,
            prec,
        )

        return {
            "L": obj,
            "p": p,
            "r": str(r) if r is not None else None,
            "ruta": metodo,
            "notas": [
                "L=UNDEFINED (AM-D6)"
            ],
            "evidencia": evidencia,
        }

    # -----------------------------------------------------------
    # 8.6.10 — NORMALIZACIÓN
    # -----------------------------------------------------------
    try:
        fraccion = (
            val
            if isinstance(val, Fraction)
            else _a_fraction(val)
        )
    except Exception as e:  # noqa: BLE001
        evidencia[-1]["rechazado"] = True

        return {
            "L": representar(None, prec),
            "p": p,
            "r": str(r) if r is not None else None,
            "ruta": metodo,
            "notas": [
                "Valor L no normalizable: {0}: {1}".format(
                    type(e).__name__,
                    e,
                )
            ],
            "evidencia": evidencia,
        }

    # -----------------------------------------------------------
    # 8.6.11 — REPRESENTACIÓN
    # -----------------------------------------------------------
    try:
        obj = representar(
            fraccion,
            prec,
        )
    except Exception as e:  # noqa: BLE001
        evidencia[-1]["rechazado"] = True

        return {
            "L": representar(None, prec),
            "p": p,
            "r": str(r) if r is not None else None,
            "ruta": metodo,
            "notas": [
                "Error representando L: {0}: {1}".format(
                    type(e).__name__,
                    e,
                )
            ],
            "evidencia": evidencia,
        }

    # -----------------------------------------------------------
    # 8.6.12 — SALIDA
    # -----------------------------------------------------------
    return {
        "L": obj,
        "p": p,
        "r": str(r) if r is not None else None,
        "ruta": metodo,
        "notas": [],
        "evidencia": evidencia,
    }


# ===============================================================
# FIN 8.6
# ===============================================================


# ===============================================================
# 8.7 — CALCULAR K
# ===============================================================

def calcular_K(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Ejecuta exclusivamente el cálculo contractual del factor K.

    Fórmula contractual ejecutada por la API K:
        K = 1 - f/c

    Correspondencia de variables:
        c = afirmaciones
        f = afirmaciones_falsas

    Contexto contractual:
        O_context = contexto / O_context / o_context

    Flujo determinista:
        entrada
        → método
        → precisión
        → O_context
        → conteos cuando corresponde
        → evidencia
        → API K
        → resultado K
        → normalización
        → representación
        → salida.

    No calcula C ni L.
    No implementa una fórmula paralela.
    No inventa un O_context.
    No sustituye una API K ausente.
    """

    # -----------------------------------------------------------
    # 8.7.1 — ENTRADA
    # -----------------------------------------------------------
    if peticion is None:
        peticion = {}
    elif not isinstance(peticion, dict):
        return {
            "K": representar(
                None,
                PRECISION_DECIMAL_DEFAULT,
            ),
            "ruta": None,
            "notas": [
                "Peticion invalida: se esperaba dict"
            ],
            "evidencia": [],
        }
    else:
        peticion = dict(peticion)

    # -----------------------------------------------------------
    # 8.7.2 — MÉTODO
    # -----------------------------------------------------------
    metodo = str(
        peticion.get("metodo") or "operacional"
    )

    # -----------------------------------------------------------
    # 8.7.3 — PRECISIÓN
    # -----------------------------------------------------------
    try:
        prec = int(
            peticion.get("precision")
            or PRECISION_DECIMAL_DEFAULT
        )
    except (TypeError, ValueError):
        prec = PRECISION_DECIMAL_DEFAULT

    if prec < 0:
        prec = PRECISION_DECIMAL_DEFAULT

    # -----------------------------------------------------------
    # 8.7.4 — O_CONTEXT
    # -----------------------------------------------------------
    o_ctx = (
        peticion.get("contexto")
        or peticion.get("O_context")
        or peticion.get("o_context")
    )

    # -----------------------------------------------------------
    # 8.7.5 — EVIDENCIA
    # -----------------------------------------------------------
    evidencia = _normalizar_evidencia(
        peticion.get("evidencia")
    )

    evidencia.append({
        "id_evidencia": _nuevo_id_evidencia(),
        "modulo": NOMBRE_MODULO,
        "capacidad": "calcular_K",
        "aporte": "factor_K",
        "version_modulo": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "rechazado": False,
    })

    for e in evidencia:
        _REG_EVIDENCIA[e["id_evidencia"]] = e

    # -----------------------------------------------------------
    # 8.7.6 — AUSENCIA DE O_CONTEXT
    # -----------------------------------------------------------
    if o_ctx is None:
        return {
            "K": representar(
                None,
                prec,
            ),
            "ruta": metodo,
            "notas": [
                "K=None sin contexto/O (Def-5.3.1)"
            ],
            "evidencia": evidencia,
        }

    # -----------------------------------------------------------
    # 8.7.7 — CONTEOS
    # -----------------------------------------------------------
    if metodo == "operacional":
        try:
            peticion = _asegurar_conteos(peticion)
        except Exception as e:  # noqa: BLE001
            evidencia[-1]["rechazado"] = True

            return {
                "K": representar(None, prec),
                "ruta": metodo,
                "notas": [
                    "Error preparando conteos para K: {0}".format(e)
                ],
                "evidencia": evidencia,
            }

    # -----------------------------------------------------------
    # 8.7.8 — RESOLUCIÓN DE API K
    # -----------------------------------------------------------
    fn = _APIS.get("K")

    if not callable(fn):
        evidencia[-1]["rechazado"] = True

        return {
            "K": representar(None, prec),
            "ruta": None,
            "notas": [
                "API K no disponible"
            ],
            "evidencia": evidencia,
        }

    # -----------------------------------------------------------
    # 8.7.9 — EJECUCIÓN DE API K
    # -----------------------------------------------------------
    try:
        if _acepta_dict(fn):
            raw = fn(peticion)
        else:
            raw = fn(
                afirmaciones=peticion.get(
                    "afirmaciones"
                ),
                afirmaciones_falsas=peticion.get(
                    "afirmaciones_falsas"
                ),
                o_context=o_ctx,
                metodo=metodo,
            )
    except Exception as e:  # noqa: BLE001
        evidencia[-1]["rechazado"] = True

        return {
            "K": representar(None, prec),
            "ruta": metodo,
            "notas": [
                "Error en API K: {0}: {1}".format(
                    type(e).__name__,
                    e,
                )
            ],
            "evidencia": evidencia,
        }

    # -----------------------------------------------------------
    # 8.7.10 — RESULTADO K
    # -----------------------------------------------------------
    if isinstance(raw, dict):
        if "K" not in raw:
            evidencia[-1]["rechazado"] = True

            return {
                "K": representar(None, prec),
                "ruta": metodo,
                "notas": [
                    "API K retorno dict sin campo 'K'"
                ],
                "evidencia": evidencia,
            }

        val = raw["K"]
    else:
        val = raw

    # -----------------------------------------------------------
    # 8.7.11 — UNDEFINED
    # -----------------------------------------------------------
    if es_undefined(val):
        obj = representar(
            UNDEFINED,
            prec,
        )

        return {
            "K": obj,
            "ruta": metodo,
            "notas": [],
            "evidencia": evidencia,
        }

    # -----------------------------------------------------------
    # 8.7.12 — NORMALIZACIÓN
    # -----------------------------------------------------------
    try:
        fraccion = (
            val
            if isinstance(val, Fraction)
            else _a_fraction(val)
        )
    except Exception as e:  # noqa: BLE001
        evidencia[-1]["rechazado"] = True

        return {
            "K": representar(None, prec),
            "ruta": metodo,
            "notas": [
                "Valor K no normalizable: {0}: {1}".format(
                    type(e).__name__,
                    e,
                )
            ],
            "evidencia": evidencia,
        }

    # -----------------------------------------------------------
    # 8.7.13 — REPRESENTACIÓN
    # -----------------------------------------------------------
    try:
        obj = representar(
            fraccion,
            prec,
        )
    except Exception as e:  # noqa: BLE001
        evidencia[-1]["rechazado"] = True

        return {
            "K": representar(None, prec),
            "ruta": metodo,
            "notas": [
                "Error representando K: {0}: {1}".format(
                    type(e).__name__,
                    e,
                )
            ],
            "evidencia": evidencia,
        }

    # -----------------------------------------------------------
    # 8.7.14 — SALIDA
    # -----------------------------------------------------------
    return {
        "K": obj,
        "ruta": metodo,
        "notas": [],
        "evidencia": evidencia,
    }


# ===============================================================
# FIN 8.7
# ===============================================================
# ===============================================================
# 8.8 — CALCULAR FACTOR
# ===============================================================

def calcular_factor(
    factor: str,
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    f = str(factor or "").strip().upper()
    if f == "C":
        return calcular_C(peticion)
    if f == "L":
        return calcular_L(peticion)
    if f == "K":
        return calcular_K(peticion)
    return {
        "error": "factor no soportado: {0}".format(factor),
        "soportados": list(_FACTORES_CANONICOS),
    }

# ===============================================================
# FIN 8.8
# ===============================================================

# ===============================================================
# 8.9 — CALCULAR (PIPELINE COMPLETO)
# ===============================================================

def calcular(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Pipeline completo y determinista de cálculo de CA.

    8.9 no implementa fórmulas propias.
    Las fórmulas pertenecen exclusivamente a sus capacidades:

        C = 1 - k/m
        L = 1 - r/p
        K = 1 - f/c

    8.9 únicamente:
        1. valida la entrada;
        2. determina método y precisión;
        3. prepara los datos operacionales una sola vez;
        4. conserva la evidencia recibida;
        5. ejecuta calcular_C, calcular_L y calcular_K;
        6. consolida sus resultados;
        7. conserva trazabilidad de módulos, capacidades y versiones;
        8. valida la salida consolidada;
        9. registra el cálculo en historial;
        10. devuelve el resultado completo.

    No inventa fórmulas.
    No modifica C, L ni K.
    No sustituye una capacidad ausente.
    No interpreta IDs de forma implícita.
    No elimina resultados parciales.
    """

    # -----------------------------------------------------------
    # 8.9.1 — ENTRADA
    # -----------------------------------------------------------
    t0 = datetime.now(timezone.utc)

    if peticion is None:
        peticion = {}
    elif not isinstance(peticion, dict):
        return {
            "id_calculo": None,
            "C": representar(None, PRECISION_DECIMAL_DEFAULT),
            "L": representar(None, PRECISION_DECIMAL_DEFAULT),
            "K": representar(None, PRECISION_DECIMAL_DEFAULT),
            "precision": PRECISION_DECIMAL_DEFAULT,
            "errores": [
                "Peticion invalida: se esperaba dict"
            ],
            "advertencias": [],
            "metodo": None,
            "evidencia": [],
            "id_evidencias": [],
            "versiones_utilizadas": {},
            "contratos_utilizados": {},
            "modulos_consultados": [],
            "capacidades_consultadas": [],
            "centinela": {
                "ok": False,
                "problemas": [
                    "Peticion invalida: se esperaba dict"
                ],
            },
            "inicio": t0.isoformat(),
            "fin": datetime.now(timezone.utc).isoformat(),
            "duracion_ms": 0,
            "version_ca": VERSION_MODULO,
            "esquema": ESQUEMA_CONTRATO,
        }

    peticion = dict(peticion)

    # -----------------------------------------------------------
    # 8.9.2 — MÉTODO
    # -----------------------------------------------------------
    metodo = str(
        peticion.get("metodo") or "operacional"
    )

    # -----------------------------------------------------------
    # 8.9.3 — PRECISIÓN
    # -----------------------------------------------------------
    try:
        prec = int(
            peticion.get("precision")
            or PRECISION_DECIMAL_DEFAULT
        )
    except (TypeError, ValueError):
        prec = PRECISION_DECIMAL_DEFAULT

    if prec < 0:
        prec = PRECISION_DECIMAL_DEFAULT

    # -----------------------------------------------------------
    # 8.9.4 — IDENTIDAD DEL CÁLCULO
    # -----------------------------------------------------------
    id_calculo = _nuevo_id_calculo()

    errores: List[str] = []
    advertencias: List[str] = []

    # -----------------------------------------------------------
    # 8.9.5 — VALIDACIÓN DE EVIDENCIA ENTRANTE
    # -----------------------------------------------------------
    val_ev = validar_evidencia(
        peticion.get("evidencia")
    )

    evidencia = list(
        val_ev.get("evidencia_normalizada") or []
    )

    if not val_ev.get("ok"):
        errores.extend(
            val_ev.get("problemas") or []
        )

    # -----------------------------------------------------------
    # 8.9.6 — PREPARACIÓN ÚNICA DE CONTEOS
    # -----------------------------------------------------------
    if metodo == "operacional":
        try:
            peticion = _asegurar_conteos(peticion)
        except Exception as e:  # noqa: BLE001
            errores.append(
                "Error preparando conteos: {0}: {1}".format(
                    type(e).__name__,
                    e,
                )
            )

    meta_conteos = peticion.get(
        "_conteos_meta"
    )

    # -----------------------------------------------------------
    # 8.9.7 — PETICIÓN NORMALIZADA PARA LAS CAPACIDADES
    # -----------------------------------------------------------
    peticion_ev = dict(peticion)
    peticion_ev["evidencia"] = evidencia
    peticion_ev["precision"] = prec
    peticion_ev["metodo"] = metodo

    # -----------------------------------------------------------
    # 8.9.8 — EJECUCIÓN DE C
    # -----------------------------------------------------------
    try:
        out_c = calcular_C(peticion_ev)
    except Exception as e:  # noqa: BLE001
        out_c = {
            "C": representar(None, prec),
            "ruta": metodo,
            "notas": [
                "Excepcion en calcular_C: {0}: {1}".format(
                    type(e).__name__,
                    e,
                )
            ],
            "evidencia": [],
        }

    # -----------------------------------------------------------
    # 8.9.9 — EJECUCIÓN DE L
    # -----------------------------------------------------------
    try:
        out_l = calcular_L(peticion_ev)
    except Exception as e:  # noqa: BLE001
        out_l = {
            "L": representar(None, prec),
            "ruta": metodo,
            "notas": [
                "Excepcion en calcular_L: {0}: {1}".format(
                    type(e).__name__,
                    e,
                )
            ],
            "evidencia": [],
        }

    # -----------------------------------------------------------
    # 8.9.10 — EJECUCIÓN DE K
    # -----------------------------------------------------------
    try:
        out_k = calcular_K(peticion_ev)
    except Exception as e:  # noqa: BLE001
        out_k = {
            "K": representar(None, prec),
            "ruta": metodo,
            "notas": [
                "Excepcion en calcular_K: {0}: {1}".format(
                    type(e).__name__,
                    e,
                )
            ],
            "evidencia": [],
        }

    # -----------------------------------------------------------
    # 8.9.11 — RESULTADOS DE LOS FACTORES
    # -----------------------------------------------------------
    C = out_c.get("C")
    L = out_l.get("L")
    K = out_k.get("K")

    # -----------------------------------------------------------
    # 8.9.12 — CONSOLIDACIÓN DE EVIDENCIA
    # -----------------------------------------------------------
    ev_all: List[Dict[str, Any]] = []
    vistos_ev = set()

    for bloque in (
        out_c,
        out_l,
        out_k,
    ):
        for e in bloque.get("evidencia") or []:
            eid = e.get("id_evidencia")

            if eid is None:
                continue

            if eid not in vistos_ev:
                vistos_ev.add(eid)
                ev_all.append(e)

    # -----------------------------------------------------------
    # 8.9.13 — CONSOLIDACIÓN DE NOTAS Y ERRORES
    # -----------------------------------------------------------
    for nombre_factor, bloque in (
        ("C", out_c),
        ("L", out_l),
        ("K", out_k),
    ):
        notas = bloque.get("notas") or []

        for nota in notas:
            texto = str(nota)

            if (
                "Error" in texto
                or "Excepcion" in texto
                or "no disponible" in texto
                or "invalida" in texto
            ):
                errores.append(
                    "{0}: {1}".format(
                        nombre_factor,
                        texto,
                    )
                )
            else:
                advertencias.append(
                    "{0}: {1}".format(
                        nombre_factor,
                        texto,
                    )
                )

    # -----------------------------------------------------------
    # 8.9.14 — VERSIONES Y CONTRATOS UTILIZADOS
    # -----------------------------------------------------------
    versiones_utilizadas: Dict[str, str] = {}
    contratos_utilizados: Dict[str, str] = {}

    for e in ev_all:
        mod = e.get("modulo")

        if mod and e.get("version_modulo"):
            versiones_utilizadas[
                str(mod)
            ] = str(e["version_modulo"])

        if mod and e.get("version_contrato"):
            contratos_utilizados[
                str(mod)
            ] = str(e["version_contrato"])

    # -----------------------------------------------------------
    # 8.9.15 — TRAZABILIDAD DE CAPACIDADES
    # -----------------------------------------------------------
    modulos_consultados = sorted({
        str(e.get("modulo"))
        for e in ev_all
        if e.get("modulo")
    })

    capacidades_consultadas = sorted({
        str(e.get("capacidad"))
        for e in ev_all
        if e.get("capacidad")
    })

    # -----------------------------------------------------------
    # 8.9.16 — SALIDA BASE
    # -----------------------------------------------------------
    salida: Dict[str, Any] = {
        "id_calculo": id_calculo,
        "C": C,
        "L": L,
        "K": K,
        "precision": prec,
        "errores": errores,
        "advertencias": advertencias,
        "metodo": metodo,
        "evidencia": ev_all,
        "id_evidencias": [
            e.get("id_evidencia")
            for e in ev_all
            if e.get("id_evidencia") is not None
        ],
        "versiones_utilizadas": versiones_utilizadas,
        "contratos_utilizados": contratos_utilizados,
        "modulos_consultados": modulos_consultados,
        "capacidades_consultadas": capacidades_consultadas,
    }

    # -----------------------------------------------------------
    # 8.9.17 — METADATOS DE CONTEOS
    # -----------------------------------------------------------
    if meta_conteos is not None:
        salida["conteos"] = meta_conteos

    # -----------------------------------------------------------
    # 8.9.18 — ESCALA SOLICITADA
    # -----------------------------------------------------------
    escala_id = _id_escala_pedido(peticion)

    if escala_id:
        try:
            inv = leer_ids_escala()
        except Exception:
            inv = {
                "ids": [],
                "n": 0,
                "origenes": [],
                "disponible": False,
            }

        conocidos = inv.get("ids") or []
        conocido = escala_id in conocidos

        desc = None

        if (
            _ESCALAS
            and callable(_ESCALAS.get("por_id"))
        ):
            try:
                desc = _ESCALAS["por_id"](
                    escala_id
                )
            except Exception:
                desc = None

        escala_meta = {
            "escala_id": escala_id,
            "conocido": conocido,
            "ids_disponibles": list(conocidos),
        }

        if isinstance(desc, dict):
            escala_meta["material"] = desc.get(
                "material"
            )
            escala_meta["nombre"] = desc.get(
                "nombre"
            )

        salida["escala"] = escala_meta

    # -----------------------------------------------------------
    # 8.9.19 — CENTINELA DE RESULTADO
    # -----------------------------------------------------------
    cent = _centinela_resultado(
        salida,
        peticion,
        ev_all,
    )

    salida["centinela"] = cent

    if not cent.get("ok"):
        salida["errores"] = list(
            salida.get("errores") or []
        ) + list(
            cent.get("problemas") or []
        )

    # -----------------------------------------------------------
    # 8.9.20 — METADATOS DE EJECUCIÓN
    # -----------------------------------------------------------
    t1 = datetime.now(timezone.utc)

    salida["inicio"] = t0.isoformat()
    salida["fin"] = t1.isoformat()
    salida["duracion_ms"] = int(
        (t1 - t0).total_seconds() * 1000
    )
    salida["version_ca"] = VERSION_MODULO
    salida["esquema"] = ESQUEMA_CONTRATO

    # -----------------------------------------------------------
    # 8.9.21 — REGISTRO DE EVIDENCIA
    # -----------------------------------------------------------
    _EVIDENCIA_POR_CALC[
        id_calculo
    ] = ev_all

    # -----------------------------------------------------------
    # 8.9.22 — HISTORIAL
    # -----------------------------------------------------------
    def _resumen_factor(
        factor: Any,
    ) -> Dict[str, Any]:
        if not isinstance(factor, dict):
            return {
                "fraccion": None,
                "numerador": None,
                "denominador": None,
                "decimal": None,
                "display": None,
            }

        return {
            "fraccion": factor.get(
                "fraccion"
            ),
            "numerador": factor.get(
                "numerador"
            ),
            "denominador": factor.get(
                "denominador"
            ),
            "decimal": factor.get(
                "decimal"
            ),
            "display": factor.get(
                "display"
            ),
        }

    _HISTORIAL.append({
        "id_calculo": id_calculo,
        "timestamp": salida["fin"],
        "metodo": metodo,
        "resultado": {
            "C": _resumen_factor(C),
            "L": _resumen_factor(L),
            "K": _resumen_factor(K),
        },
        "id_evidencias": list(
            salida["id_evidencias"]
        ),
        "modulos_consultados": list(
            modulos_consultados
        ),
        "capacidades_consultadas": list(
            capacidades_consultadas
        ),
        "versiones_utilizadas": dict(
            versiones_utilizadas
        ),
        "contratos_utilizados": dict(
            contratos_utilizados
        ),
        "centinela_ok": bool(
            cent.get("ok")
        ),
        "errores": list(
            salida.get("errores") or []
        ),
        "duracion_ms": salida[
            "duracion_ms"
        ],
        "escala_id": escala_id,
        "precision": prec,
    })

    # -----------------------------------------------------------
    # 8.9.23 — DIAGNÓSTICO GLOBAL
    # -----------------------------------------------------------
    if salida["errores"]:
        try:
            from core.diagnostico import (
                DiagnosticoGlobal
            )  # type: ignore

            recibir = getattr(
                DiagnosticoGlobal,
                "recibir_reporte",
                None,
            )

            if callable(recibir):
                recibir(
                    NOMBRE_MODULO,
                    [
                        {
                            "tipo": "error_calculo",
                            "detalle": error,
                        }
                        for error in salida[
                            "errores"
                        ]
                    ],
                )
            else:
                advertencias.append(
                    "DiagnosticoGlobal.reci" 
                    "bir_reporte no es callable"
                )

        except Exception as e:  # noqa: BLE001
            advertencias.append(
                "DiagnosticoGlobal no disponible: "
                "{0}: {1}".format(
                    type(e).__name__,
                    e,
                )
            )

    # -----------------------------------------------------------
    # 8.9.24 — SALIDA FINAL
    # -----------------------------------------------------------
    return salida


# ===============================================================
# FIN 8.9
# ===============================================================
# ===============================================================
# 8.10 — EXPLICAR CÁLCULO
# ===============================================================

def explicar_calculo(
    id_calculo: str,
) -> Optional[Dict[str, Any]]:
    """
    Explicación determinista de un cálculo previamente registrado.

    La explicación se reconstruye exclusivamente desde:
        1. id_calculo;
        2. _HISTORIAL;
        3. _EVIDENCIA_POR_CALC;
        4. _REG_EVIDENCIA.

    No ejecuta nuevamente C, L ni K.
    No modifica el cálculo.
    No inventa evidencia.
    No inventa módulos.
    No inventa capacidades.
    No sustituye evidencia faltante por texto descriptivo.

    Las fórmulas explicativas corresponden al contrato matemático
    existente:

        C = 1 - k/m
        L = 1 - r/p
        K = 1 - f/c

    La función explica el cálculo registrado; no vuelve a calcularlo.
    """

    # -----------------------------------------------------------
    # 8.10.1 — IDENTIFICACIÓN DEL CÁLCULO
    # -----------------------------------------------------------
    key = str(id_calculo or "").strip()

    if not key:
        return None

    # -----------------------------------------------------------
    # 8.10.2 — LOCALIZACIÓN EN HISTORIAL
    # -----------------------------------------------------------
    item = None

    for h in reversed(_HISTORIAL):
        if h.get("id_calculo") == key:
            item = h
            break

    if item is None:
        return None

    # -----------------------------------------------------------
    # 8.10.3 — RECUPERACIÓN DE EVIDENCIA
    # -----------------------------------------------------------
    evidencia = list(
        _EVIDENCIA_POR_CALC.get(key) or []
    )

    # Si no existe evidencia directa asociada al cálculo,
    # reconstruirla exclusivamente mediante los IDs registrados
    # en el historial.
    if not evidencia:
        for eid in item.get("id_evidencias") or []:
            if eid in _REG_EVIDENCIA:
                evidencia.append(
                    _REG_EVIDENCIA[eid]
                )

    # -----------------------------------------------------------
    # 8.10.4 — CLASIFICACIÓN CONTRACTUAL POR CAPACIDAD EXACTA
    # -----------------------------------------------------------
    por_factor: Dict[
        str,
        List[Dict[str, Any]]
    ] = {
        "C": [],
        "L": [],
        "K": [],
    }

    otros: List[Dict[str, Any]] = []

    for e in evidencia:
        capacidad = e.get("capacidad")

        if capacidad == "calcular_C":
            por_factor["C"].append(e)

        elif capacidad == "calcular_L":
            por_factor["L"].append(e)

        elif capacidad == "calcular_K":
            por_factor["K"].append(e)

        else:
            otros.append(e)

    # -----------------------------------------------------------
    # 8.10.5 — REPRESENTACIÓN DETERMINISTA DE EVIDENCIA
    # -----------------------------------------------------------
    def _lineas(
        evs: List[Dict[str, Any]]
    ) -> List[str]:
        lineas: List[str] = []

        for e in evs:
            lineas.append(
                "{0}.{1} aporte={2} version={3}".format(
                    e.get("modulo"),
                    e.get("capacidad"),
                    e.get("aporte"),
                    e.get("version_modulo"),
                )
            )

        return lineas

    # -----------------------------------------------------------
    # 8.10.6 — RESULTADO REGISTRADO
    # -----------------------------------------------------------
    resultado = item.get("resultado") or {}

    C = resultado.get("C")
    L = resultado.get("L")
    K = resultado.get("K")

    # -----------------------------------------------------------
    # 8.10.7 — EXTRACCIÓN SEGURA DEL DISPLAY
    # -----------------------------------------------------------
    def _display(
        factor: Any
    ) -> Optional[Any]:
        if not isinstance(factor, dict):
            return None

        return factor.get("display")

    # -----------------------------------------------------------
    # 8.10.8 — EXTRACCIÓN DE VARIABLES REGISTRADAS
    # -----------------------------------------------------------
    def _variables_factor(
        evs: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        variables: Dict[str, Any] = {}

        for e in evs:
            datos = e.get("variables")

            if isinstance(datos, dict):
                for nombre, valor in datos.items():
                    if nombre not in variables:
                        variables[nombre] = valor

        return variables

    variables_C = _variables_factor(
        por_factor["C"]
    )

    variables_L = _variables_factor(
        por_factor["L"]
    )

    variables_K = _variables_factor(
        por_factor["K"]
    )

    # -----------------------------------------------------------
    # 8.10.9 — EXPLICACIÓN CONTRACTUAL DE C
    # -----------------------------------------------------------
    explicacion_C = {
        "formula": "C = 1 - k/m",
        "display": _display(C),
        "variables": variables_C,
        "evidencia": _lineas(
            por_factor["C"]
        ),
    }

    # -----------------------------------------------------------
    # 8.10.10 — EXPLICACIÓN CONTRACTUAL DE L
    # -----------------------------------------------------------
    explicacion_L = {
        "formula": "L = 1 - r/p",
        "display": _display(L),
        "variables": variables_L,
        "evidencia": _lineas(
            por_factor["L"]
        ),
    }

    # -----------------------------------------------------------
    # 8.10.11 — EXPLICACIÓN CONTRACTUAL DE K
    # -----------------------------------------------------------
    explicacion_K = {
        "formula": "K = 1 - f/c",
        "display": _display(K),
        "variables": variables_K,
        "evidencia": _lineas(
            por_factor["K"]
        ),
    }

    # -----------------------------------------------------------
    # 8.10.12 — ANCLAS CONTRACTUALES
    # -----------------------------------------------------------
    anclas: List[str] = [
        "C = 1 - k/m",
        "L = 1 - r/p",
        "K = 1 - f/c",
    ]

    # -----------------------------------------------------------
    # 8.10.13 — ESTADO DE INFORMACIÓN DISPONIBLE
    # -----------------------------------------------------------
    faltantes: List[str] = []

    if not por_factor["C"]:
        faltantes.append(
            "evidencia de calcular_C"
        )

    if not por_factor["L"]:
        faltantes.append(
            "evidencia de calcular_L"
        )

    if not por_factor["K"]:
        faltantes.append(
            "evidencia de calcular_K"
        )

    # -----------------------------------------------------------
    # 8.10.14 — SALIDA
    # -----------------------------------------------------------
    return {
        "id_calculo": key,
        "resultado": resultado,

        "C": explicacion_C,
        "L": explicacion_L,
        "K": explicacion_K,

        "evidencia_adicional": _lineas(
            otros
        ),

        "modulos_consultados": item.get(
            "modulos_consultados"
        ),

        "capacidades_consultadas": item.get(
            "capacidades_consultadas"
        ),

        "versiones_utilizadas": item.get(
            "versiones_utilizadas"
        ),

        "contratos_utilizados": item.get(
            "contratos_utilizados"
        ),

        "evidencia": evidencia,

        "anclas": anclas,

        "centinela_ok": item.get(
            "centinela_ok"
        ),

        "errores": item.get(
            "errores"
        ),

        "timestamp": item.get(
            "timestamp"
        ),

        "duracion_ms": item.get(
            "duracion_ms"
        ),

        "precision": item.get(
            "precision"
        ),

        "evidencia_completa": not bool(
            faltantes
        ),

        "evidencia_faltante": faltantes,
    }


# ===============================================================
# FIN 8.10
# ===============================================================
# ===============================================================
# EVALUAR_UNIVERSAL
# ===============================================================

def evaluar_universal(
    hechos: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Engine entrega hechos.
    Este callable ejecuta las capacidades REALES de ESTE módulo
    (CONTENEDOR['capacidades'] ya resuelto a callables).
    Punto fijo local. No se llama a sí mismo. No toca otros módulos.
    """
    hechos_out: Dict[str, Any] = dict(hechos or {})
    traza: List[Dict[str, Any]] = []
    ejecutadas: set = set()

    capacidades = CONTENEDOR.get("capacidades") or {}

    while True:
        nuevos = 0

        for nombre, fn in capacidades.items():
            if nombre == "evaluar_universal":
                continue
            if not callable(fn):
                continue
            if nombre in ejecutadas:
                continue

            try:
                sig = inspect.signature(fn)
            except (TypeError, ValueError):
                continue

            requeridos = []
            opcionales = []
            for pname, p in sig.parameters.items():
                if p.kind not in (
                    inspect.Parameter.POSITIONAL_ONLY,
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    inspect.Parameter.KEYWORD_ONLY,
                ):
                    continue
                if p.default is inspect.Parameter.empty:
                    requeridos.append(pname)
                else:
                    opcionales.append(pname)

            # --- resolución de argumentos (universal, sin nombres inventados) ---
            argumentos: Dict[str, Any] = {}

            if not requeridos:
                # firma vacía o solo opcionales: usar opcionales presentes en hechos
                for p in opcionales:
                    if p in hechos_out:
                        argumentos[p] = hechos_out[p]
                try:
                    salida = fn(**argumentos) if argumentos else fn()
                except Exception as ex:
                    ejecutadas.add(nombre)
                    traza.append({
                        "capacidad": nombre,
                        "estado": "ERROR",
                        "detalle": "{0}: {1}".format(type(ex).__name__, ex),
                    })
                    continue

            elif all(r in hechos_out for r in requeridos):
                # todos los requeridos existen como claves en hechos
                for p in requeridos + opcionales:
                    if p in hechos_out:
                        argumentos[p] = hechos_out[p]
                try:
                    salida = fn(**argumentos)
                except Exception as ex:
                    ejecutadas.add(nombre)
                    traza.append({
                        "capacidad": nombre,
                        "estado": "ERROR",
                        "detalle": "{0}: {1}".format(type(ex).__name__, ex),
                    })
                    continue

            elif len(requeridos) == 1:
                # patrón real del repo: calcular(peticion), verificar(datos), etc.
                # se entrega el dict de hechos completo en ese único parámetro
                argumentos[requeridos[0]] = hechos_out
                for p in opcionales:
                    if p in hechos_out:
                        argumentos[p] = hechos_out[p]
                try:
                    salida = fn(**argumentos)
                except Exception as ex:
                    ejecutadas.add(nombre)
                    traza.append({
                        "capacidad": nombre,
                        "estado": "ERROR",
                        "detalle": "{0}: {1}".format(type(ex).__name__, ex),
                    })
                    continue
            else:
                # varios requeridos ausentes: no aplicable aún
                continue

            ejecutadas.add(nombre)
            publicados: List[str] = []

            if isinstance(salida, dict):
                for clave, valor in salida.items():
                    if clave.startswith("_"):
                        continue
                    if clave not in hechos_out:
                        hechos_out[clave] = valor
                        publicados.append(clave)
                        nuevos += 1

            traza.append({
                "capacidad": nombre,
                "estado": "EXITO",
                "argumentos": sorted(argumentos.keys()),
                "publica": publicados,
            })

        if nuevos == 0:
            break

    return {
        "hechos": hechos_out,
        "traza": traza,
        "ejecutadas": sorted(ejecutadas),
    }

# ===============================================================
# FIN EVALUAR_UNIVERSAL
# ===============================================================

# ===============================================================
# 8.11 — HISTORIAL
# ===============================================================

def historial(limite: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Consulta determinista del historial de cálculos.

    Contrato:
      limite is None -> devuelve todo el historial.
      limite == 0    -> devuelve lista vacía.
      limite > 0     -> devuelve los últimos N registros.
      limite < 0     -> devuelve lista vacía.
      limite inválido -> devuelve lista vacía.

    No calcula C, L ni K.
    No modifica _HISTORIAL.
    No crea registros.
    """

    items = list(_HISTORIAL)

    # -----------------------------------------------------------
    # 8.11.1 — SIN LÍMITE
    # -----------------------------------------------------------
    if limite is None:
        return items

    # -----------------------------------------------------------
    # 8.11.2 — NORMALIZACIÓN DETERMINISTA DEL LÍMITE
    # -----------------------------------------------------------
    try:
        n = int(limite)
    except (TypeError, ValueError):
        return []

    # -----------------------------------------------------------
    # 8.11.3 — LÍMITE CERO
    # -----------------------------------------------------------
    if n == 0:
        return []

    # -----------------------------------------------------------
    # 8.11.4 — LÍMITE NEGATIVO
    # -----------------------------------------------------------
    if n < 0:
        return []

    # -----------------------------------------------------------
    # 8.11.5 — ÚLTIMOS N REGISTROS
    # -----------------------------------------------------------
    return items[-n:]


# ===============================================================
# FIN 8.11
# ===============================================================


# ===============================================================
# 8.12 — VERIFICAR SALIDA
# ===============================================================

def verificar_salida(salida: Any) -> bool:
    """
    Verificador estructural de la salida contractual de calcular().

    No calcula C, L ni K.
    No modifica la salida.
    No sustituye valores.
    No interpreta fórmulas.

    Comprueba únicamente que la estructura entregada sea compatible
    con la representación contractual producida por calcular().
    """

    # -----------------------------------------------------------
    # 8.12.1 — TIPO RAÍZ
    # -----------------------------------------------------------
    if not isinstance(salida, dict):
        return False

    # -----------------------------------------------------------
    # 8.12.2 — CAMPOS RAÍZ OBLIGATORIOS
    # -----------------------------------------------------------
    campos_obligatorios = (
        "id_calculo",
        "C",
        "L",
        "K",
    )

    if not all(
        campo in salida
        for campo in campos_obligatorios
    ):
        return False

    # -----------------------------------------------------------
    # 8.12.3 — ID DE CÁLCULO
    # -----------------------------------------------------------
    id_calculo = salida.get("id_calculo")

    if not isinstance(id_calculo, str):
        return False

    if not id_calculo.strip():
        return False

    # -----------------------------------------------------------
    # 8.12.4 — VERIFICACIÓN DE BLOQUES C/L/K
    # -----------------------------------------------------------
    for factor in ("C", "L", "K"):
        bloque = salida.get(factor)

        # None representa dato no disponible.
        if bloque is None:
            continue

        if not isinstance(bloque, dict):
            return False

        # -------------------------------------------------------
        # 8.12.4.1 — REPRESENTACIÓN MÍNIMA
        # -------------------------------------------------------
        if "display" not in bloque:
            return False

        if not isinstance(bloque.get("display"), str):
            return False

        # -------------------------------------------------------
        # 8.12.4.2 — FRACCIÓN
        # -------------------------------------------------------
        if "fraccion" in bloque:
            fraccion = bloque.get("fraccion")

            if fraccion is not None and not isinstance(
                fraccion,
                str,
            ):
                return False

        # -------------------------------------------------------
        # 8.12.4.3 — NUMERADOR
        # -------------------------------------------------------
        if "numerador" in bloque:
            numerador = bloque.get("numerador")

            if numerador is not None and not isinstance(
                numerador,
                int,
            ):
                return False

        # -------------------------------------------------------
        # 8.12.4.4 — DENOMINADOR
        # -------------------------------------------------------
        if "denominador" in bloque:
            denominador = bloque.get("denominador")

            if denominador is not None and not isinstance(
                denominador,
                int,
            ):
                return False

        # -------------------------------------------------------
        # 8.12.4.5 — DECIMAL
        # -------------------------------------------------------
        if "decimal" in bloque:
            decimal = bloque.get("decimal")

            if decimal is not None and not isinstance(
                decimal,
                (int, float, str),
            ):
                return False

    # -----------------------------------------------------------
    # 8.12.5 — PROHIBICIÓN DE CAMPOS DE FRACCIÓN EN RAÍZ
    # -----------------------------------------------------------
    campos_raiz_prohibidos = (
        "C_fraccion",
        "L_fraccion",
        "K_fraccion",
        "C_numerador",
        "C_denominador",
        "L_numerador",
        "L_denominador",
        "K_numerador",
        "K_denominador",
    )

    if any(
        campo in salida
        for campo in campos_raiz_prohibidos
    ):
        return False

    # -----------------------------------------------------------
    # 8.12.6 — RESULTADO ESTRUCTURALMENTE VÁLIDO
    # -----------------------------------------------------------
    return True


# ===============================================================
# FIN 8.12
# ===============================================================


# ===============================================================
# 8.13 — VERIFICAR CÁLCULO DE C, L, K
# ===============================================================

def verificar_calculo_de_C_L_K(
    calculo: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Verifica estructura y coherencia matemática de C, L y K.

    Fórmulas contractuales:

        C = 1 - k/m

        L = 1 - r/p

        K = 1 - f/c

    Donde:

        C:
          m = compromisos
          k = contradicciones

        L:
          p = posturas
          r = reversiones

        K:
          c = afirmaciones
          f = afirmaciones_falsas

    Esta función NO sustituye los cálculos realizados por las APIs
    C, L y K.

    Si los operandos necesarios están disponibles en el resultado,
    verifica el valor producido contra la fórmula correspondiente.

    Si los operandos no están disponibles, no inventa valores:
    informa que la verificación matemática no puede ejecutarse.

    No modifica el cálculo recibido.
    """

    # -----------------------------------------------------------
    # 8.13.1 — VALIDACIÓN DE ENTRADA
    # -----------------------------------------------------------
    if not isinstance(calculo, dict):
        return {
            "valido": False,
            "errores": [
                "El calculo debe ser un dict"
            ],
            "advertencias": [],
            "C": None,
            "L": None,
            "K": None,
            "verificacion": {},
        }

    errores: List[str] = []
    advertencias: List[str] = []
    verificacion: Dict[str, Any] = {}

    # -----------------------------------------------------------
    # 8.13.2 — VALIDACIÓN ESTRUCTURAL DE LA SALIDA
    # -----------------------------------------------------------
    if not verificar_salida(calculo):
        errores.append(
            "La estructura del calculo no cumple el contrato de salida"
        )

    # -----------------------------------------------------------
    # 8.13.3 — EXTRACCIÓN DE C/L/K
    # -----------------------------------------------------------
    C = calculo.get("C")
    L = calculo.get("L")
    K = calculo.get("K")

    # -----------------------------------------------------------
    # 8.13.4 — VALIDACIÓN ESTRUCTURAL DE C
    # -----------------------------------------------------------
    if C is None:
        errores.append(
            "C no está disponible en el cálculo"
        )
        verificacion["C"] = {
            "presente": False,
            "ok": False,
        }

    elif not isinstance(C, dict):
        errores.append(
            "C debe ser un dict o None"
        )
        verificacion["C"] = {
            "presente": True,
            "ok": False,
            "tipo": type(C).__name__,
        }

    else:
        ok_c = True
        detalles_c: Dict[str, Any] = {}

        for campo in (
            "fraccion",
            "decimal",
            "display",
        ):
            presente = campo in C
            detalles_c[campo] = (
                C.get(campo)
                if presente
                else None
            )

            if not presente:
                errores.append(
                    "C falta campo '{0}'".format(campo)
                )
                ok_c = False

        if (
            "numerador" in C
            and "denominador" in C
            and "fraccion" in C
        ):
            num = C.get("numerador")
            den = C.get("denominador")
            frac = C.get("fraccion")

            if (
                isinstance(num, int)
                and isinstance(den, int)
                and den != 0
                and frac is not None
            ):
                esperado = "{0}/{1}".format(
                    num,
                    den,
                )

                if str(frac) != esperado:
                    errores.append(
                        "C: fraccion no coincide con "
                        "numerador/denominador"
                    )
                    ok_c = False

        verificacion["C"] = {
            "presente": True,
            "ok": ok_c,
            "detalles": detalles_c,
        }

    # -----------------------------------------------------------
    # 8.13.5 — VALIDACIÓN ESTRUCTURAL DE L
    # -----------------------------------------------------------
    if L is None:
        verificacion["L"] = {
            "presente": False,
            "ok": True,
            "estado": "None",
        }

    elif not isinstance(L, dict):
        errores.append(
            "L debe ser un dict o None"
        )
        verificacion["L"] = {
            "presente": True,
            "ok": False,
            "tipo": type(L).__name__,
        }

    else:
        if L.get("undefined") is True:
            verificacion["L"] = {
                "presente": True,
                "ok": True,
                "estado": "UNDEFINED",
                "detalles": {
                    "display": L.get("display"),
                },
            }
        else:
            ok_l = True
            detalles_l: Dict[str, Any] = {}

            for campo in (
                "fraccion",
                "decimal",
                "display",
            ):
                presente = campo in L
                detalles_l[campo] = (
                    L.get(campo)
                    if presente
                    else None
                )

                if not presente:
                    errores.append(
                        "L falta campo '{0}'".format(campo)
                    )
                    ok_l = False

            if (
                "numerador" in L
                and "denominador" in L
                and "fraccion" in L
            ):
                num = L.get("numerador")
                den = L.get("denominador")
                frac = L.get("fraccion")

                if (
                    isinstance(num, int)
                    and isinstance(den, int)
                    and den != 0
                    and frac is not None
                ):
                    esperado = "{0}/{1}".format(
                        num,
                        den,
                    )

                    if str(frac) != esperado:
                        errores.append(
                            "L: fraccion no coincide con "
                            "numerador/denominador"
                        )
                        ok_l = False

            verificacion["L"] = {
                "presente": True,
                "ok": ok_l,
                "detalles": detalles_l,
            }

    # -----------------------------------------------------------
    # 8.13.6 — VALIDACIÓN ESTRUCTURAL DE K
    # -----------------------------------------------------------
    if K is None:
        verificacion["K"] = {
            "presente": False,
            "ok": True,
            "estado": "None",
        }

    elif not isinstance(K, dict):
        errores.append(
            "K debe ser un dict o None"
        )
        verificacion["K"] = {
            "presente": True,
            "ok": False,
            "tipo": type(K).__name__,
        }

    else:
        if K.get("valor") is None and K.get("fraccion") is None:
            verificacion["K"] = {
                "presente": True,
                "ok": True,
                "estado": "None",
                "detalles": {
                    "display": K.get("display"),
                },
            }
        else:
            ok_k = True
            detalles_k: Dict[str, Any] = {}

            for campo in (
                "fraccion",
                "decimal",
                "display",
            ):
                presente = campo in K
                detalles_k[campo] = (
                    K.get(campo)
                    if presente
                    else None
                )

                if not presente:
                    errores.append(
                        "K falta campo '{0}'".format(campo)
                    )
                    ok_k = False

            if (
                "numerador" in K
                and "denominador" in K
                and "fraccion" in K
            ):
                num = K.get("numerador")
                den = K.get("denominador")
                frac = K.get("fraccion")

                if (
                    isinstance(num, int)
                    and isinstance(den, int)
                    and den != 0
                    and frac is not None
                ):
                    esperado = "{0}/{1}".format(
                        num,
                        den,
                    )

                    if str(frac) != esperado:
                        errores.append(
                            "K: fraccion no coincide con "
                            "numerador/denominador"
                        )
                        ok_k = False

            verificacion["K"] = {
                "presente": True,
                "ok": ok_k,
                "detalles": detalles_k,
            }

    # -----------------------------------------------------------
    # 8.13.7 — EXTRACCIÓN DE CONTEOS
    # -----------------------------------------------------------
    conteos = calculo.get("conteos")

    if not isinstance(conteos, dict):
        advertencias.append(
            "No hay conteos en la salida; "
            "verificacion matematica de C/L/K no ejecutable"
        )

        verificacion["formulas"] = {
            "ejecutable": False,
            "motivo": "conteos no disponibles",
        }

    else:
        # -------------------------------------------------------
        # 8.13.7.1 — OPERANDOS DE C
        # -------------------------------------------------------
        m = conteos.get("compromisos")
        k = conteos.get("contradicciones")

        # -------------------------------------------------------
        # 8.13.7.2 — OPERANDOS DE L
        # -------------------------------------------------------
        p = conteos.get("posturas")
        r = conteos.get("reversiones")

        # -------------------------------------------------------
        # 8.13.7.3 — OPERANDOS DE K
        # -------------------------------------------------------
        c = conteos.get("afirmaciones")
        f = conteos.get("afirmaciones_falsas")

        formulas: Dict[str, Any] = {
            "ejecutable": True,
            "C": {
                "formula": "1 - k/m",
                "m": m,
                "k": k,
            },
            "L": {
                "formula": "1 - r/p",
                "p": p,
                "r": r,
            },
            "K": {
                "formula": "1 - f/c",
                "c": c,
                "f": f,
            },
        }

        # -------------------------------------------------------
        # 8.13.7.4 — VALIDACIÓN DE OPERANDOS
        # -------------------------------------------------------
        operandos = {
            "m": m,
            "k": k,
            "p": p,
            "r": r,
            "c": c,
            "f": f,
        }

        operandos_validos = all(
            isinstance(valor, int)
            and valor >= 0
            for valor in operandos.values()
        )

        if not operandos_validos:
            formulas["ejecutable"] = False
            formulas["motivo"] = (
                "uno o más operandos no son enteros "
                "no negativos"
            )

        # -------------------------------------------------------
        # 8.13.7.5 — DIVISIÓN VÁLIDA
        # -------------------------------------------------------
        if formulas["ejecutable"]:
            if m == 0:
                formulas["C"]["ejecutable"] = False
                formulas["C"]["motivo"] = "m=0"

            if p == 0:
                formulas["L"]["ejecutable"] = False
                formulas["L"]["motivo"] = "p=0"

            if c == 0:
                formulas["K"]["ejecutable"] = False
                formulas["K"]["motivo"] = "c=0"

        # -------------------------------------------------------
        # 8.13.7.6 — CÁLCULO DE REFERENCIA
        # -------------------------------------------------------
        if formulas["ejecutable"] and m != 0:
            esperado_c = Fraction(m - k, m)
            formulas["C"]["esperado"] = str(esperado_c)

        # -------------------------------------------------------
        # 8.13.7.7 — CÁLCULO DE REFERENCIA L
        # -------------------------------------------------------
        if formulas["ejecutable"] and p != 0:
            esperado_l = Fraction(p - r, p)
            formulas["L"]["esperado"] = str(esperado_l)

        # -------------------------------------------------------
        # 8.13.7.8 — CÁLCULO DE REFERENCIA K
        # -------------------------------------------------------
        if formulas["ejecutable"] and c != 0:
            esperado_k = Fraction(c - f, c)
            formulas["K"]["esperado"] = str(esperado_k)

        # -------------------------------------------------------
        # 8.13.7.9 — COMPARACIÓN CON C
        # -------------------------------------------------------
        if (
            formulas.get("C", {}).get("ejecutable", False)
            and isinstance(C, dict)
            and "fraccion" in C
        ):
            esperado = formulas["C"]["esperado"]

            if str(C.get("fraccion")) != esperado:
                errores.append(
                    "C no coincide con la formula C = 1 - k/m"
                )

        # -------------------------------------------------------
        # 8.13.7.10 — COMPARACIÓN CON L
        # -------------------------------------------------------
        if (
            formulas.get("L", {}).get("ejecutable", False)
            and isinstance(L, dict)
            and L.get("undefined") is not True
            and "fraccion" in L
        ):
            esperado = formulas["L"]["esperado"]

            if str(L.get("fraccion")) != esperado:
                errores.append(
                    "L no coincide con la formula L = 1 - r/p"
                )

        # -------------------------------------------------------
        # 8.13.7.11 — COMPARACIÓN CON K
        # -------------------------------------------------------
        if (
            formulas.get("K", {}).get("ejecutable", False)
            and isinstance(K, dict)
            and "fraccion" in K
        ):
            esperado = formulas["K"]["esperado"]

            if str(K.get("fraccion")) != esperado:
                errores.append(
                    "K no coincide con la formula K = 1 - f/c"
                )

        verificacion["formulas"] = formulas

    # -----------------------------------------------------------
    # 8.13.8 — CENTINELA
    # -----------------------------------------------------------
    centinela = calculo.get("centinela")

    if centinela is None:
        advertencias.append(
            "Falta 'centinela' en el resultado"
        )
        centinela_ok = False
    elif not isinstance(centinela, dict):
        errores.append(
            "'centinela' debe ser un dict"
        )
        centinela_ok = False
    else:
        centinela_ok = centinela.get("ok") is True

        if not centinela_ok:
            problemas = centinela.get("problemas") or []

            for problema in problemas:
                errores.append(str(problema))

    # -----------------------------------------------------------
    # 8.13.9 — ERRORES PRODUCIDOS POR calcular()
    # -----------------------------------------------------------
    errores_calculo = calculo.get("errores")

    if errores_calculo:
        if isinstance(errores_calculo, list):
            errores.extend(
                str(error)
                for error in errores_calculo
            )
        else:
            errores.append(
                "El campo 'errores' no es una lista"
            )

    # -----------------------------------------------------------
    # 8.13.10 — RESULTADO FINAL
    # -----------------------------------------------------------
    valido = len(errores) == 0

    return {
        "valido": valido,
        "errores": errores,
        "advertencias": advertencias,
        "C": C,
        "L": L,
        "K": K,
        "verificacion": verificacion,
        "resumen": {
            "C_ok": verificacion.get(
                "C",
                {},
            ).get("ok", False),
            "L_ok": verificacion.get(
                "L",
                {},
            ).get("ok", False),
            "K_ok": verificacion.get(
                "K",
                {},
            ).get("ok", False),
            "formulas_ejecutadas": verificacion.get(
                "formulas",
                {},
            ).get("ejecutable", False),
            "centinela_ok": centinela_ok,
        },
    }


# ===============================================================
# FIN 8.13
# ===============================================================
# ===============================================================
# 8.14 — INVENTARIO
# ===============================================================

def inventario(peticion: Any = None) -> Dict[str, Any]:
    """
    Inventario contractual del módulo CA.

    8.14.1 — BARRER / FUENTE DE VERDAD
    Utiliza barrer() como fuente única para el estado técnico
    verificable del módulo.

    8.14.2 — IDENTIDAD DEL MÓDULO
    Expone únicamente la identidad contractual ya declarada:
    ID, nombre, rol, versión, contrato, esquema y estabilidad.

    8.14.3 — ESTADO ESTRUCTURAL
    Expone archivos, hashes, factores, APIs y disponibilidad
    exactamente según el resultado producido por barrer().

    8.14.4 — DEPENDENCIAS Y CONTRATO
    Expone las capacidades y dependencias declaradas por
    CONTENEDOR sin modificarlas ni inferir otras.

    8.14.5 — INVARIANTES
    Expone los invariantes declarados por CONTENEDOR.

    8.14.6 — HISTORIAL
    Expone únicamente el número de cálculos registrados.

    8.14.7 — PRECISIÓN Y SALIDA
    Expone la precisión decimal predeterminada y la regla real
    de representación contractual.

    No calcula C, L ni K.
    No ejecuta fórmulas.
    No crea IDs.
    No modifica la petición.
    No agrega capacidades.
    No interpreta capacidades que no estén declaradas.
    """

    # -----------------------------------------------------------
    # 8.14.1 — FUENTE DE ESTADO VERIFICABLE
    # -----------------------------------------------------------
    b = barrer()

    # -----------------------------------------------------------
    # 8.14.2 — IDENTIDAD DEL MÓDULO
    # -----------------------------------------------------------
    resultado: Dict[str, Any] = {
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,

        # -------------------------------------------------------
        # 8.14.3 — ESTADO ESTRUCTURAL
        # -------------------------------------------------------
        "archivos": b.get("archivos"),
        "hashes": b.get("hashes"),
        "factores_api": b.get("factores_api"),
        "factores_no_declarados": b.get(
            "factores_no_declarados"
        ),
        "archivos_extra": b.get("archivos_extra"),
        "apis_factor": b.get("apis_factor"),

        # -------------------------------------------------------
        # 8.14.4 — CONTEOS
        # -------------------------------------------------------
        "conteos_disponible": b.get(
            "conteos_disponible"
        ),
        "apis_conteos": b.get(
            "apis_conteos"
        ),

        # -------------------------------------------------------
        # 8.14.5 — ESCALAS
        # -------------------------------------------------------
        "escalas_ids_disponible": b.get(
            "escalas_ids_disponible"
        ),
        "ids_escala": b.get(
            "ids_escala"
        ),

        # -------------------------------------------------------
        # 8.14.6 — ESTADO DE COHERENCIA
        # -------------------------------------------------------
        "coherente": b.get("coherente"),
        "errores": b.get("errores"),
        "choques": b.get("choques"),

        # -------------------------------------------------------
        # 8.14.7 — HISTORIAL
        # -------------------------------------------------------
        "historial_n": b.get("historial_n"),

        # -------------------------------------------------------
        # 8.14.8 — CAPACIDADES CONTRACTUALES
        # -------------------------------------------------------
        "capacidades": sorted(
            CONTENEDOR["capacidades"].keys()
        ),

        # -------------------------------------------------------
        # 8.14.9 — DEPENDENCIAS CONTRACTUALES
        # -------------------------------------------------------
        "requiere": sorted(
            CONTENEDOR.get("requiere") or []
        ),

        # -------------------------------------------------------
        # 8.14.10 — INVARIANTES CONTRACTUALES
        # -------------------------------------------------------
        "invariantes": CONTENEDOR.get("invariantes"),

        # -------------------------------------------------------
        # 8.14.11 — PRECISIÓN
        # -------------------------------------------------------
        "precision_decimal_default": (
            PRECISION_DECIMAL_DEFAULT
        ),

        # -------------------------------------------------------
        # 8.14.12 — REGLA DE REPRESENTACIÓN
        # -------------------------------------------------------
        "regla_salida": (
            "cada factor se representa mediante su objeto "
            "contractual; cuando existe un valor definido, "
            "el objeto contiene fraccion, numerador, "
            "denominador, decimal y display"
        ),
    }

    return resultado


# ===============================================================
# FIN 8.14
# ===============================================================

# ===============================================================
# 8.15 — EJECUTAR TOTAL
# ===============================================================

def ejecutar_total(
    peticion: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Autoridad total de ENGINE sobre CA.

    Ejecuta las capacidades declaradas por el contrato de CA
    mediante sus callables reales.

    Principios deterministas:

        CONTENEDOR["capacidades"]
            ↓
        resolución en _CAP_MAP
            ↓
        callable real
            ↓
        ejecución
            ↓
        resultado
            ↓
        registro de estado

    No ejecuta capacidades no declaradas.
    No inventa capacidades.
    No sustituye callables ausentes.
    No ejecuta dos veces una misma capacidad.
    No reimplementa la lógica de las capacidades.
    No calcula fórmulas directamente.
    No modifica el contrato.
    """

    # -----------------------------------------------------------
    # 8.15.1 — NORMALIZACIÓN DE PETICIÓN
    # -----------------------------------------------------------
    if peticion is None:
        peticion_base: Dict[str, Any] = {}
    elif isinstance(peticion, dict):
        peticion_base = dict(peticion)
    else:
        peticion_base = {}

    resultados: Dict[str, Any] = {}
    errores_ejecucion: List[str] = []
    capacidades_declaradas = sorted(
        CONTENEDOR.get("capacidades", {}).keys()
    )

    capacidades_ejecutadas: List[str] = []
    capacidades_fallidas: List[str] = []
    capacidades_no_resueltas: List[str] = []

    # -----------------------------------------------------------
    # 8.15.2 — RESOLUCIÓN CONTRACTUAL
    # -----------------------------------------------------------
    #
    # _CAP_MAP es la tabla de resolución contractual.
    # Solamente se ejecutan capacidades que aparecen en
    # CONTENEDOR["capacidades"].
    #
    # No se utiliza globals(), getattr() arbitrario ni una lista
    # paralela de funciones.
    # -----------------------------------------------------------
    for capacidad in capacidades_declaradas:

        fn = _CAP_MAP.get(capacidad)

        if not callable(fn):
            capacidades_no_resueltas.append(capacidad)
            errores_ejecucion.append(
                "capacidad '{0}' declarada pero sin callable "
                "resoluble en _CAP_MAP".format(capacidad)
            )
            resultados[capacidad] = None
            continue

        # -------------------------------------------------------
        # 8.15.3 — PROTECCIÓN CONTRA RECURSIÓN
        # -------------------------------------------------------
        if capacidad == "ejecutar_total":
            resultados[capacidad] = None
            capacidades_fallidas.append(capacidad)
            errores_ejecucion.append(
                "capacidad 'ejecutar_total' no puede invocarse "
                "recursivamente desde ejecutar_total"
            )
            continue

        # -------------------------------------------------------
        # 8.15.4 — EJECUCIÓN ÚNICA
        # -------------------------------------------------------
        #
        # Cada callable contractual recibe la misma petición base.
        # No se ejecuta nuevamente una capacidad para comprobarla.
        # La verificación se realiza sobre el resultado obtenido.
        # -------------------------------------------------------
        try:
            resultado = fn(peticion_base)
            resultados[capacidad] = resultado
            capacidades_ejecutadas.append(capacidad)

        except Exception as e:  # noqa: BLE001
            resultados[capacidad] = None
            capacidades_fallidas.append(capacidad)
            errores_ejecucion.append(
                "{0}: {1}: {2}".format(
                    capacidad,
                    type(e).__name__,
                    e,
                )
            )

    # -----------------------------------------------------------
    # 8.15.5 — COBERTURA CONTRACTUAL
    # -----------------------------------------------------------
    #
    # Toda capacidad declarada debe terminar en uno de estos
    # estados:
    #
    #   ejecutada
    #   fallida
    #   no_resuelta
    #
    # Nunca se considera ejecutada una capacidad omitida.
    # -----------------------------------------------------------
    estados_capacidades: Dict[str, str] = {}

    for capacidad in capacidades_declaradas:
        if capacidad in capacidades_ejecutadas:
            estados_capacidades[capacidad] = "ejecutada"
        elif capacidad in capacidades_fallidas:
            estados_capacidades[capacidad] = "fallida"
        elif capacidad in capacidades_no_resueltas:
            estados_capacidades[capacidad] = "no_resuelta"
        else:
            estados_capacidades[capacidad] = "no_ejecutada"

    cobertura_completa = all(
        estados_capacidades.get(capacidad) == "ejecutada"
        for capacidad in capacidades_declaradas
    )

    # -----------------------------------------------------------
    # 8.15.6 — ESTADO ESTRUCTURAL DEL MÓDULO
    # -----------------------------------------------------------
    #
    # barrer() continúa siendo la fuente contractual de coherencia
    # estructural. No se sustituye por la ejecución.
    # -----------------------------------------------------------
    try:
        resultado_barrer = barrer()
    except Exception as e:  # noqa: BLE001
        resultado_barrer = None
        errores_ejecucion.append(
            "barrer: {0}: {1}".format(
                type(e).__name__,
                e,
            )
        )

    resultados["barrer"] = resultado_barrer

    coherente = (
        isinstance(resultado_barrer, dict)
        and resultado_barrer.get("coherente") is True
    )

    # -----------------------------------------------------------
    # 8.15.7 — ESTADO FINAL DE EJECUCIÓN
    # -----------------------------------------------------------
    ejecucion_completa = (
        cobertura_completa
        and not capacidades_fallidas
        and not capacidades_no_resueltas
        and not errores_ejecucion
    )

    operativo = (
        coherente
        and ejecucion_completa
    )

    # -----------------------------------------------------------
    # 8.15.8 — RESULTADO CONTRACTUAL
    # -----------------------------------------------------------
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "operacion": "ejecutar_total",

        "estado": (
            ESTADO_OPERATIVO
            if operativo
            else ESTADO_DEGRADADO
        ),

        "coherente": coherente,
        "ejecucion_completa": ejecucion_completa,
        "cobertura_completa": cobertura_completa,

        "capacidades_declaradas": capacidades_declaradas,
        "capacidades_ejecutadas": sorted(
            capacidades_ejecutadas
        ),
        "capacidades_fallidas": sorted(
            capacidades_fallidas
        ),
        "capacidades_no_resueltas": sorted(
            capacidades_no_resueltas
        ),
        "estados_capacidades": estados_capacidades,

        "errores_ejecucion": errores_ejecucion,

        "resultados": resultados,
    }


# ===============================================================
# FIN 8.15
# ===============================================================

# ===============================================================
# 8.16 — INSPECCIONAR
# ===============================================================

def inspeccionar(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Inspección estructural de CA.

    Expone exclusivamente el contrato, las capacidades declaradas,
    las APIs cargadas y el estado de integridad.

    No ejecuta calcular_C, calcular_L, calcular_K ni calcular.
    No altera historial, evidencia ni inventario.
    No inventa capacidades.
    """

    # -----------------------------------------------------------
    # 8.16.1 — INTEGRIDAD ESTRUCTURAL
    # -----------------------------------------------------------
    res_barrer = barrer()

    # -----------------------------------------------------------
    # 8.16.2 — CALLABILITY DE APIs DE FACTORES
    # -----------------------------------------------------------
    apis_factor: Dict[str, bool] = {}
    for factor in _FACTORES_CANONICOS:
        apis_factor[factor] = callable(_APIS.get(factor))

    # -----------------------------------------------------------
    # 8.16.3 — CALLABILITY DE CONTEOS
    # -----------------------------------------------------------
    apis_conteos = {
        "extraer_conteos": (
            _CONTEOS is not None
            and callable(_CONTEOS.get("extraer_conteos"))
        ),
        "inyectar_en_peticion": (
            _CONTEOS is not None
            and callable(_CONTEOS.get("inyectar_en_peticion"))
        ),
    }

    # -----------------------------------------------------------
    # 8.16.4 — CALLABILITY DE ESCALAS
    # -----------------------------------------------------------
    apis_escalas = {
        "ids": (
            _ESCALAS is not None
            and callable(_ESCALAS.get("ids"))
        ),
        "por_id": (
            _ESCALAS is not None
            and callable(_ESCALAS.get("por_id"))
        ),
    }

    # -----------------------------------------------------------
    # 8.16.5 — ESTRUCTURA CONTRACTUAL
    # -----------------------------------------------------------
    capacidades_contractuales = list(
        CONTENEDOR.get("capacidades", {}).keys()
    )
    capacidades_meta = list(
        CONTENEDOR.get("capacidades_meta", {}).keys()
    )

    # -----------------------------------------------------------
    # 8.16.6 — RESULTADO
    # -----------------------------------------------------------
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
            "PRECISION_DECIMAL_DEFAULT": (
                PRECISION_DECIMAL_DEFAULT
            ),
            "FACTORES_CANONICOS": list(_FACTORES_CANONICOS),
        },

        "capacidades_contractuales": capacidades_contractuales,
        "capacidades_meta": capacidades_meta,

        "apis": {
            "factores_cargados": sorted(_APIS.keys()),
            "factores_callable": apis_factor,
            "errores_carga": list(_ERRORES_CARGA),
            "conteos_disponible": _CONTEOS is not None,
            "conteos_callable": apis_conteos,
            "escalas_ids_disponible": _ESCALAS is not None,
            "escalas_callable": apis_escalas,
        },

        "integridad": {
            "coherente": res_barrer.get("coherente"),
            "errores": list(res_barrer.get("errores") or []),
            "choques": list(res_barrer.get("choques") or []),
            "archivos": res_barrer.get("archivos"),
            "archivos_extra": res_barrer.get("archivos_extra"),
            "hashes": res_barrer.get("hashes"),
            "historial_n": res_barrer.get("historial_n"),
        },

        "autoriza_engine": CONTENEDOR.get("autoriza_engine"),
        "reporting": CONTENEDOR.get("reporting"),
        "invariantes": list(INVARIANTES),

        "nota": (
            "inspeccionar expone estructura, contrato, APIs y "
            "estado de integridad de CA sin ejecutar factores "
            "ni alterar el estado de calculos previos."
        ),
    }


# ===============================================================
# FIN 8.16
# ===============================================================


# ===============================================================
# 8.17 — REGISTRAR INVENTARIO
# ===============================================================

def registrar_inventario(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Genera una instantánea estructural del inventario de CA.

    No modifica historial.
    No modifica evidencia.
    No ejecuta factores.
    No crea capacidades.
    No afirma persistencia que no exista.
    """

    # -----------------------------------------------------------
    # 8.17.1 — INVENTARIO ACTUAL
    # -----------------------------------------------------------
    inv = inventario(peticion)

    # -----------------------------------------------------------
    # 8.17.2 — RESULTADO
    # -----------------------------------------------------------
    return {
        "id": ID_MODULO,
        "operacion": "registrar_inventario",
        "registrado": True,
        "inventario": inv,
        "nota": (
            "Instantanea del inventario estructural actual de CA. "
            "La funcion no modifica historial ni evidencia y no "
            "realiza persistencia externa."
        ),
    }


# ===============================================================
# FIN 8.17
# ===============================================================


# ===============================================================
# FIN PARTE 8
# ===============================================================

# ===============================================================
# PARTE 9 — REPORTING INTERNO
# ===============================================================

# ===============================================================
# 9.1 — REPORTE
# ===============================================================

def reporte() -> Dict[str, Any]:
    """
    Reporte estructural y operativo de CA.

    El reporte utiliza exclusivamente el estado real obtenido
    mediante barrer() y el contrato vigente de CONTENEDOR.

    No ejecuta factores C/L/K.
    No modifica historial.
    No inventa capacidades.
    """

    # -----------------------------------------------------------
    # 9.1.1 — ESTADO REAL DEL MÓDULO
    # -----------------------------------------------------------
    b = barrer()

    coherente = bool(b.get("coherente"))
    estado = (
        ESTADO_OPERATIVO
        if coherente
        else ESTADO_DEGRADADO
    )

    # -----------------------------------------------------------
    # 9.1.2 — CAPACIDADES CONTRACTUALES
    # -----------------------------------------------------------
    capacidades = list(
        CONTENEDOR.get("capacidades", {}).keys()
    )

    capacidades_callable = sorted(
        nombre
        for nombre, ref in CONTENEDOR.get(
            "capacidades", {}
        ).items()
        if callable(ref)
    )

    # -----------------------------------------------------------
    # 9.1.3 — OPERACIONES ARQUITECTÓNICAS REALES
    # -----------------------------------------------------------
    operaciones_arquitectonicas = {
        nombre: callable(
            CONTENEDOR.get("capacidades", {}).get(nombre)
        )
        for nombre in (
            "ejecutar_total",
            "inspeccionar",
            "registrar_inventario",
        )
    }

    # -----------------------------------------------------------
    # 9.1.4 — RESULTADO
    # -----------------------------------------------------------
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

        "factores_api": b.get("factores_api"),
        "apis_factor": b.get("apis_factor"),

        "archivos": b.get("archivos"),
        "archivos_extra": b.get("archivos_extra"),
        "hashes": b.get("hashes"),

        "conteos_disponible": b.get(
            "conteos_disponible"
        ),
        "escalas_ids_disponible": b.get(
            "escalas_ids_disponible"
        ),

        "historial_n": b.get("historial_n"),

        "errores_n": len(
            b.get("errores") or []
        ),
        "choques_n": len(
            b.get("choques") or []
        ),

        "capacidades": capacidades,
        "capacidades_callable": capacidades_callable,

        "operaciones_arquitectonicas": (
            operaciones_arquitectonicas
        ),

        "autoridad": CONTENEDOR.get(
            "autoridad"
        ),
        "autoriza_engine": CONTENEDOR.get(
            "autoriza_engine"
        ),
        "conocimiento_exportable": CONTENEDOR.get(
            "conocimiento_exportable"
        ),

        "regla_salida": (
            "un objeto por factor: "
            "fraccion = decimal"
        ),
    }


# ===============================================================
# FIN 9.1
# ===============================================================


# ===============================================================
# 9.2 — DIAGNÓSTICO
# ===============================================================

def diagnostico() -> Dict[str, Any]:
    """
    Diagnóstico determinista del estado de CA.

    Clasifica únicamente condiciones observables del módulo.
    No ejecuta cálculos.
    No modifica el estado.
    """

    # -----------------------------------------------------------
    # 9.2.1 — ESTADO BASE
    # -----------------------------------------------------------
    b = barrer()

    problemas: List[Dict[str, Any]] = []
    advertencias: List[str] = []
    recomendaciones: List[str] = []

    # -----------------------------------------------------------
    # 9.2.2 — ERRORES ESTRUCTURALES
    # -----------------------------------------------------------
    errores = list(
        b.get("errores") or []
    )

    if errores:
        problemas.append({
            "tipo": "errores_integridad",
            "detalle": errores,
        })

        recomendaciones.append(
            "Resolver los errores reportados por barrer() "
            "antes de considerar CA coherente."
        )

    # -----------------------------------------------------------
    # 9.2.3 — CHOQUES CONTRACTUALES
    # -----------------------------------------------------------
    choques = list(
        b.get("choques") or []
    )

    if choques:
        problemas.append({
            "tipo": "choques_factor",
            "detalle": choques,
        })

        recomendaciones.append(
            "Resolver los choques de asignacion "
            "factor -> stem."
        )

    # -----------------------------------------------------------
    # 9.2.4 — FACTORES CANÓNICOS
    # -----------------------------------------------------------
    apis_factor = dict(
        b.get("apis_factor") or {}
    )

    factores_faltantes = sorted(
        factor
        for factor in _FACTORES_CANONICOS
        if not apis_factor.get(factor, False)
    )

    if factores_faltantes:
        problemas.append({
            "tipo": "factores_no_callable",
            "detalle": factores_faltantes,
        })

        recomendaciones.append(
            "Resolver las APIs no callables de los "
            "factores canonicos."
        )

    # -----------------------------------------------------------
    # 9.2.5 — CONTEOS
    # -----------------------------------------------------------
    if not b.get("conteos_disponible"):
        problemas.append({
            "tipo": "conteos_no_disponible",
            "detalle": (
                "Las APIs contractuales de conteos "
                "no estan completamente disponibles."
            ),
        })

        recomendaciones.append(
            "Resolver la disponibilidad callable de "
            "extraer_conteos e inyectar_en_peticion."
        )

    # -----------------------------------------------------------
    # 9.2.6 — ESCALAS
    # -----------------------------------------------------------
    if not b.get("escalas_ids_disponible"):
        advertencias.append(
            "La API de escalas_ids no esta disponible "
            "o no supera su verificacion."
        )

    # -----------------------------------------------------------
    # 9.2.7 — ARCHIVOS EXTRA
    # -----------------------------------------------------------
    archivos_extra = list(
        b.get("archivos_extra") or []
    )

    if archivos_extra:
        advertencias.append(
            "Existen archivos no incluidos en el "
            "mapa estructural conocido: {0}".format(
                archivos_extra
            )
        )

    # -----------------------------------------------------------
    # 9.2.8 — ESTADO FINAL
    # -----------------------------------------------------------
    coherente = bool(
        b.get("coherente")
    )

    estado = (
        ESTADO_OPERATIVO
        if coherente
        else ESTADO_DEGRADADO
    )

    # -----------------------------------------------------------
    # 9.2.9 — RESULTADO
    # -----------------------------------------------------------
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "estado": estado,
        "coherente": coherente,

        "problemas": problemas,
        "advertencias": advertencias,
        "recomendaciones": recomendaciones,

        "factores_api": b.get(
            "factores_api"
        ),
        "apis_factor": apis_factor,

        "conteos_disponible": b.get(
            "conteos_disponible"
        ),
        "escalas_ids_disponible": b.get(
            "escalas_ids_disponible"
        ),

        "historial_n": b.get(
            "historial_n"
        ),
    }


# ===============================================================
# FIN 9.2
# ===============================================================


# ===============================================================
# FIN PARTE 9
# ===============================================================

# ===============================================================
# PARTE 10 — RESOLUCIÓN ESTRICTA Y EXPORTACIONES
# ===============================================================

# ===============================================================
# 10.1 — MAPA DE CAPACIDADES
# ===============================================================

_CAP_MAP = {
    "calcular": calcular,
    "calcular_C": calcular_C,
    "calcular_L": calcular_L,
    "calcular_K": calcular_K,
    "calcular_factor": calcular_factor,
    "representar": representar,
    "validar_evidencia": validar_evidencia,
    "explicar_calculo": explicar_calculo,
    "barrer": barrer,
    "verificar": verificar,
    "inventario": inventario,
    "reporte": reporte,
    "diagnostico": diagnostico,
    "leer_ids_escala": leer_ids_escala,
    "verificar_salida": verificar_salida,
    "historial": historial,
    "verificar_calculo_de_C_L_K": verificar_calculo_de_C_L_K,
    "ejecutar_total": ejecutar_total,
    "inspeccionar": inspeccionar,
    "registrar_inventario": registrar_inventario,
    "evaluar_universal": evaluar_universal,
}

# ===============================================================
# FIN 10.1
# ===============================================================


# ===============================================================
# 10.2 — RESOLUCIÓN DE CAPACIDADES
# ===============================================================

def _resolver_capacidades(cont: Dict[str, Any]) -> None:
    """
    Resuelve exclusivamente las capacidades declaradas
    por el contrato.

    Reglas deterministas:
      1. Cada capacidad debe existir en CONTENEDOR["capacidades"].
      2. Una referencia callable se acepta directamente.
      3. Una referencia str debe existir exactamente en _CAP_MAP.
      4. La referencia resuelta debe ser callable.
      5. Una referencia de otro tipo invalida el contrato.
      6. No se crean capacidades.
      7. No se sustituyen capacidades.
      8. No se infieren nombres.
      9. No se modifican contratos externos.
    """

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
            f"tipo invalido: {type(ref).__name__}"
        )

    cont["capacidades"] = resueltas


# ===============================================================
# FIN 10.2
# ===============================================================


# ===============================================================
# 10.3 — EJECUCIÓN DE VALIDACIÓN Y RESOLUCIÓN
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
    "UNDEFINED",
    "es_undefined",
    "calcular",
    "calcular_C",
    "calcular_L",
    "calcular_K",
    "calcular_factor",
    "representar",
    "validar_evidencia",
    "explicar_calculo",
    "barrer",
    "verificar",
    "inventario",
    "reporte",
    "diagnostico",
    "leer_ids_escala",
    "verificar_salida",
    "historial",
    "verificar_calculo_de_C_L_K",
    "ejecutar_total",
    "inspeccionar",
    "registrar_inventario",
    "ContratoInvalido",
    "evaluar_universal",
    
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
