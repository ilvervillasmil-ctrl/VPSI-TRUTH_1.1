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
    "requiere": ["CT", "AX", "FO", "MC", "SF", "CA", "CX", "DI", "RE", "VX", "TX", "CH", "CIT", "TT", "CE",],

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
    Centinela de integridad estructural del dominio CA.

    Verifica, de forma determinista, la cadena contractual:
        factor/capacidad declarada
        → stem declarado
        → archivo físico
        → API cargada
        → callable

    También verifica:
        - APIs no declaradas.
        - Choques de stems por factor.
        - Hashes calculables.
        - APIs contractuales de conteos.
        - API contractual de escalas.
        - Ejecución segura de leer_ids_escala().
        - Estructura e integridad de los IDs de escala.

    No ejecuta ninguna fórmula.
    No calcula C, L, K ni ningún otro factor.
    No interpreta IDs.
    No determina variables de cálculo.
    No inventa capacidades.
    """

    errores: List[Dict[str, str]] = list(_ERRORES_CARGA)
    choques: List[str] = []

    # -----------------------------------------------------------
    # 8.4.1 — INVENTARIO FÍSICO Y HASHES
    # -----------------------------------------------------------
    archivos = [p.name for p in _listar_py()]
    hashes = _hashes_modulo()

    for nombre, meta in hashes.items():
        if meta.get("sha256") is None:
            errores.append({
                "archivo": nombre,
                "error": meta.get("error") or "hash no calculable",
            })

    # -----------------------------------------------------------
    # 8.4.2 — FACTORES:
    # factor → stem → archivo → API → callable
    # -----------------------------------------------------------
    #
    # _ARCHIVO_FACTOR constituye la relación declarada:
    #     stem → factor
    #
    # Se invierte exclusivamente para verificar:
    #     factor → stem
    #
    # No se crean factores nuevos.
    # No se agregan nombres manualmente.
    # -----------------------------------------------------------
    stem_por_factor: Dict[str, str] = {}

    for stem, factor in _ARCHIVO_FACTOR.items():
        if factor in stem_por_factor:
            choques.append(
                "factor '{0}' declarado por múltiples stems: "
                "'{1}' y '{2}'".format(
                    factor,
                    stem_por_factor[factor],
                    stem,
                )
            )
        else:
            stem_por_factor[factor] = stem

    factores_ok: List[str] = []
    apis_factor: Dict[str, bool] = {}

    for factor in _FACTORES_CANONICOS:
        stem = stem_por_factor.get(factor)

        # -------------------------------------------------------
        # Factor sin stem contractual
        # -------------------------------------------------------
        if stem is None:
            errores.append({
                "archivo": "?",
                "error": (
                    "factor '{0}' sin stem declarado en "
                    "_ARCHIVO_FACTOR".format(factor)
                ),
            })
            apis_factor[factor] = False
            continue

        # -------------------------------------------------------
        # Stem → archivo físico
        # -------------------------------------------------------
        path = _DIR / "{0}.py".format(stem)

        if not path.exists():
            errores.append({
                "archivo": "{0}.py".format(stem),
                "error": (
                    "factor '{0}' declara stem '{1}' pero el "
                    "archivo no existe fisicamente".format(
                        factor,
                        stem,
                    )
                ),
            })
            apis_factor[factor] = False
            continue

        # -------------------------------------------------------
        # Archivo → API
        # -------------------------------------------------------
        fn = _APIS.get(factor)
        es_callable = callable(fn)

        apis_factor[factor] = es_callable

        if not es_callable:
            errores.append({
                "archivo": "{0}.py".format(stem),
                "error": (
                    "factor '{0}' tiene archivo '{1}.py' pero "
                    "API no callable en _APIS".format(
                        factor,
                        stem,
                    )
                ),
            })
            continue

        factores_ok.append(factor)

    # -----------------------------------------------------------
    # 8.4.3 — APIs DE FACTORES NO DECLARADAS
    # -----------------------------------------------------------
    factores_no_declarados = sorted(
        set(_APIS.keys()) - set(_FACTORES_CANONICOS)
    )

    for factor_extra in factores_no_declarados:
        errores.append({
            "archivo": "?",
            "error": (
                "API de factor '{0}' cargada en _APIS pero no "
                "pertenece a _FACTORES_CANONICOS".format(
                    factor_extra
                )
            ),
        })

    # -----------------------------------------------------------
    # 8.4.4 — CHOQUES DE STEM → FACTOR
    # -----------------------------------------------------------
    #
    # Además de detectar duplicidad en la inversión anterior,
    # se verifica la relación física de los stems declarados.
    # -----------------------------------------------------------
    por_factor: Dict[str, List[str]] = {}

    for stem, factor in _ARCHIVO_FACTOR.items():
        if (_DIR / "{0}.py".format(stem)).exists():
            por_factor.setdefault(factor, []).append(stem)

    for factor, stems in por_factor.items():
        if len(stems) > 1:
            mensaje = "factor '{0}' reclamado por: {1}".format(
                factor,
                sorted(stems),
            )
            if mensaje not in choques:
                choques.append(mensaje)

    # -----------------------------------------------------------
    # 8.4.5 — ARCHIVOS EXTRA
    # -----------------------------------------------------------
    #
    # Un archivo adicional no constituye por sí mismo una
    # contradicción contractual.
    # -----------------------------------------------------------
    stems_conocidos = set(_ARCHIVO_FACTOR.keys()) | {
        "conteos",
        "escalas_ids",
    }

    extra = [
        p.stem
        for p in _listar_py()
        if p.stem not in stems_conocidos
    ]

    # -----------------------------------------------------------
    # 8.4.6 — CONTEOS
    # -----------------------------------------------------------
    #
    # Solo se validan las APIs contractuales existentes:
    #     extraer_conteos
    #     inyectar_en_peticion
    #
    # No se agrega ninguna API adicional.
    # -----------------------------------------------------------
    extraer_ok = (
        _CONTEOS is not None
        and callable(_CONTEOS.get("extraer_conteos"))
    )

    inyectar_ok = (
        _CONTEOS is not None
        and callable(_CONTEOS.get("inyectar_en_peticion"))
    )

    conteos_ok = extraer_ok and inyectar_ok

    if _CONTEOS is None:
        errores.append({
            "archivo": "conteos.py",
            "error": "API de conteos no cargada",
        })
    else:
        if not extraer_ok:
            errores.append({
                "archivo": "conteos.py",
                "error": "extraer_conteos no es callable",
            })

        if not inyectar_ok:
            errores.append({
                "archivo": "conteos.py",
                "error": "inyectar_en_peticion no es callable",
            })

    apis_conteos = {
        "extraer_conteos": extraer_ok,
        "inyectar_en_peticion": inyectar_ok,
    }

    # -----------------------------------------------------------
    # 8.4.7 — ESCALAS:
    # API → callable → ejecución → estructura → cardinalidad
    # -----------------------------------------------------------
    escalas_ok = (
        _ESCALAS is not None
        and callable(_ESCALAS.get("ids"))
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
            "error": "API de escalas_ids no cargada",
        })
        escalas_ok = False

    elif not callable(_ESCALAS.get("ids")):
        errores.append({
            "archivo": "escalas_ids.py",
            "error": "escalas_ids.ids no es callable",
        })
        escalas_ok = False

    else:
        try:
            resultado = leer_ids_escala()

            # ---------------------------------------------------
            # Retorno contractual mínimo
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
                        "leer_ids_escala retorno estructura invalida"
                    ),
                })
                escalas_ok = False

            else:
                ids_list = resultado.get("ids")
                n_val = resultado.get("n")

                # -----------------------------------------------
                # ids debe ser list
                # -----------------------------------------------
                if not isinstance(ids_list, list):
                    errores.append({
                        "archivo": "escalas_ids.py",
                        "error": (
                            "leer_ids_escala: 'ids' no es list"
                        ),
                    })
                    escalas_ok = False

                # -----------------------------------------------
                # n debe corresponder exactamente a ids
                # -----------------------------------------------
                elif n_val != len(ids_list):
                    errores.append({
                        "archivo": "escalas_ids.py",
                        "error": (
                            "leer_ids_escala: n={0} != "
                            "len(ids)={1}".format(
                                n_val,
                                len(ids_list),
                            )
                        ),
                    })
                    escalas_ok = False

                else:
                    ids_escala = resultado
                    escalas_ok = True

        except Exception as e:  # noqa: BLE001
            errores.append({
                "archivo": "escalas_ids.py",
                "error": (
                    "leer_ids_escala fallo: {0}: {1}".format(
                        type(e).__name__,
                        e,
                    )
                ),
            })
            escalas_ok = False

    # -----------------------------------------------------------
    # 8.4.8 — COHERENCIA FINAL
    # -----------------------------------------------------------
    #
    # No se ejecuta ninguna fórmula de cálculo.
    #
    # La coherencia depende exclusivamente de que no existan
    # errores estructurales ni choques contractuales.
    # -----------------------------------------------------------
    coherente = not errores and not choques

    # -----------------------------------------------------------
    # 8.4.9 — RETORNO CONTRACTUAL
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


def verificar() -> Dict[str, Any]:
    """
    Alias contractual real de barrer.

    Correspondencia:
        verificar → barrer

    Compatible con:
        CONTENEDOR['capacidades']['verificar']
        _CAP_MAP['verificar']
        __all__

    No reimplementa lógica.
    No ejecuta cálculos.
    No inventa comportamiento.
    """
    return barrer()


# ===============================================================
# FIN 8.4
# ===============================================================
# ===============================================================
# 8.5 — CALCULAR C
# ===============================================================

def calcular_C(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Ejecuta exclusivamente el cálculo contractual del factor C.

    Flujo determinista:
        petición
        → método
        → precisión
        → preparación de conteos cuando corresponde
        → normalización de evidencia
        → resolución de API C
        → ejecución única de API C
        → resolución del valor C
        → normalización a Fraction
        → representación contractual.

    No calcula L ni K.
    No inventa fórmulas.
    No sustituye una API C ausente.
    """

    if peticion is None:
        peticion = {}
    elif not isinstance(peticion, dict):
        return {
            "C": representar(None, PRECISION_DECIMAL_DEFAULT),
            "ruta": None,
            "notas": ["Peticion invalida: se esperaba dict"],
            "evidencia": [],
        }
    else:
        peticion = dict(peticion)

    metodo = str(peticion.get("metodo") or "operacional")

    try:
        prec = int(
            peticion.get("precision")
            or PRECISION_DECIMAL_DEFAULT
        )
    except (TypeError, ValueError):
        prec = PRECISION_DECIMAL_DEFAULT

    if prec < 0:
        prec = PRECISION_DECIMAL_DEFAULT

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
            for evidencia_item in evidencia:
                _REG_EVIDENCIA[
                    evidencia_item["id_evidencia"]
                ] = evidencia_item

            return {
                "C": representar(None, prec),
                "ruta": metodo,
                "notas": [
                    "Error preparando conteos para C: {0}".format(e)
                ],
                "evidencia": evidencia,
            }

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

    for evidencia_item in evidencia:
        _REG_EVIDENCIA[
            evidencia_item["id_evidencia"]
        ] = evidencia_item

    fn = _APIS.get("C")

    if not callable(fn):
        evidencia[-1]["rechazado"] = True
        return {
            "C": representar(None, prec),
            "ruta": None,
            "notas": ["API C no disponible"],
            "evidencia": evidencia,
        }

    try:
        if _acepta_dict(fn):
            raw = fn(peticion)
        else:
            raw = fn(
                compromisos=peticion.get("compromisos"),
                contradicciones=peticion.get("contradicciones"),
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

    if es_undefined(val):
        return {
            "C": representar(UNDEFINED, prec),
            "ruta": metodo,
            "notas": [],
            "evidencia": evidencia,
        }

    try:
        fraccion = (
            val
            if isinstance(val, Fraction)
            else _a_fraction(val)
        )
        obj = representar(fraccion, prec)
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

def calcular_L(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Ejecuta exclusivamente el cálculo contractual del factor L.

    Flujo determinista:
        petición
        → método
        → precisión
        → preparación de conteos cuando corresponde
        → normalización de evidencia
        → resolución de API L
        → ejecución única de API L
        → resolución del valor L
        → tratamiento de UNDEFINED
        → normalización a Fraction
        → representación contractual.

    No calcula C ni K.
    No inventa fórmulas.
    No sustituye una API L ausente.
    """

    if peticion is None:
        peticion = {}
    elif not isinstance(peticion, dict):
        return {
            "L": representar(None, PRECISION_DECIMAL_DEFAULT),
            "p": None,
            "r": None,
            "ruta": None,
            "notas": ["Peticion invalida: se esperaba dict"],
            "evidencia": [],
        }
    else:
        peticion = dict(peticion)

    metodo = str(peticion.get("metodo") or "operacional")

    try:
        prec = int(
            peticion.get("precision")
            or PRECISION_DECIMAL_DEFAULT
        )
    except (TypeError, ValueError):
        prec = PRECISION_DECIMAL_DEFAULT

    if prec < 0:
        prec = PRECISION_DECIMAL_DEFAULT

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
            for evidencia_item in evidencia:
                _REG_EVIDENCIA[
                    evidencia_item["id_evidencia"]
                ] = evidencia_item

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

    for evidencia_item in evidencia:
        _REG_EVIDENCIA[
            evidencia_item["id_evidencia"]
        ] = evidencia_item

    fn = _APIS.get("L")

    if not callable(fn):
        evidencia[-1]["rechazado"] = True
        return {
            "L": representar(None, prec),
            "p": None,
            "r": None,
            "ruta": None,
            "notas": ["API L no disponible"],
            "evidencia": evidencia,
        }

    try:
        if _acepta_dict(fn):
            raw = fn(peticion)
        else:
            raw = fn(
                posturas=peticion.get("posturas"),
                reversiones=peticion.get("reversiones"),
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

    if es_undefined(val):
        return {
            "L": representar(UNDEFINED, prec),
            "p": p,
            "r": str(r) if r is not None else None,
            "ruta": metodo,
            "notas": ["L=UNDEFINED (AM-D6)"],
            "evidencia": evidencia,
        }

    try:
        fraccion = (
            val
            if isinstance(val, Fraction)
            else _a_fraction(val)
        )
        obj = representar(fraccion, prec)
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

def calcular_K(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Ejecuta exclusivamente el cálculo contractual del factor K.

    Flujo determinista:
        petición
        → método
        → precisión
        → resolución explícita de O_context
        → normalización de evidencia
        → caso contractual K=None sin contexto/O
        → preparación de conteos cuando corresponde
        → resolución de API K
        → ejecución única de API K
        → resolución del valor K
        → tratamiento de UNDEFINED
        → normalización a Fraction
        → representación contractual.

    No calcula C ni L.
    No inventa fórmulas.
    No sustituye una API K ausente.
    No ejecuta la API K por una segunda firma ante TypeError.
    """

    # -----------------------------------------------------------
    # 8.7.1 — ENTRADA
    # -----------------------------------------------------------
    if peticion is None:
        peticion = {}
    elif not isinstance(peticion, dict):
        return {
            "K": representar(None, PRECISION_DECIMAL_DEFAULT),
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
    # 8.7.4 — O_context
    # -----------------------------------------------------------
    o_ctx = peticion.get("contexto")

    if o_ctx is None:
        o_ctx = peticion.get("O_context")

    if o_ctx is None:
        o_ctx = peticion.get("o_context")

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

    for evidencia_item in evidencia:
        _REG_EVIDENCIA[
            evidencia_item["id_evidencia"]
        ] = evidencia_item

    # -----------------------------------------------------------
    # 8.7.6 — CASO CONTRACTUAL K SIN CONTEXTO/O
    # -----------------------------------------------------------
    if o_ctx is None:
        return {
            "K": representar(None, prec),
            "ruta": metodo,
            "notas": [
                "K=None sin contexto/O (Def-5.3.1)"
            ],
            "evidencia": evidencia,
        }

    # -----------------------------------------------------------
    # 8.7.7 — CONTEOS PARA MÉTODO OPERACIONAL
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
    # 8.7.9 — EJECUCIÓN ÚNICA DE API K
    # -----------------------------------------------------------
    try:
        if _acepta_dict(fn):
            raw = fn(peticion)
        else:
            raw = fn(
                afirmaciones=peticion.get("afirmaciones"),
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
    # 8.7.10 — RESOLUCIÓN DEL RETORNO
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
        return {
            "K": representar(UNDEFINED, prec),
            "ruta": metodo,
            "notas": [],
            "evidencia": evidencia,
        }

    # -----------------------------------------------------------
    # 8.7.12 — NORMALIZACIÓN A FRACCIÓN
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
    # 8.7.13 — REPRESENTACIÓN CONTRACTUAL
    # -----------------------------------------------------------
    try:
        obj = representar(fraccion, prec)
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
    Salida sin duplicacion:
      C = {fraccion, numerador, denominador, decimal, display, ...}
      L = {...}
      K = {...}
    display ejemplo: "7/9 = 0.778"
    """
    t0 = datetime.now(timezone.utc)
    peticion = dict(peticion or {})
    metodo = str(peticion.get("metodo") or "operacional")
    prec = int(peticion.get("precision") or PRECISION_DECIMAL_DEFAULT)
    id_calculo = _nuevo_id_calculo()
    errores: List[str] = []

    # Validar evidencia entrante
    val_ev = validar_evidencia(peticion.get("evidencia"))
    evidencia = list(val_ev.get("evidencia_normalizada") or [])
    if not val_ev.get("ok"):
        errores.extend(val_ev.get("problemas") or [])

    escala_id = _id_escala_pedido(peticion)
    escala_meta = None
    if escala_id:
        inv = leer_ids_escala()
        conocido = escala_id in (inv.get("ids") or [])
        desc = None
        if _ESCALAS and callable(_ESCALAS.get("por_id")):
            try:
                desc = _ESCALAS["por_id"](escala_id)
            except Exception:  # noqa: BLE001
                desc = None
        escala_meta = {
            "escala_id": escala_id,
            "conocido": conocido,
            "ids_disponibles": list(inv.get("ids") or []),
        }
        if isinstance(desc, dict):
            escala_meta["material"] = desc.get("material")
            escala_meta["nombre"] = desc.get("nombre")

    if metodo == "operacional":
        peticion = _asegurar_conteos(peticion)
    meta_conteos = peticion.get("_conteos_meta")

    peticion_ev = dict(peticion)
    peticion_ev["evidencia"] = evidencia
    peticion_ev["precision"] = prec

    out_c = calcular_C(peticion_ev)
    out_l = calcular_L(peticion_ev)
    out_k = calcular_K(peticion_ev)

    C = out_c.get("C")
    L = out_l.get("L")
    K = out_k.get("K")

    ev_all: List[Dict[str, Any]] = []
    vistos_ev = set()
    for bloque in (out_c, out_l, out_k):
        for e in bloque.get("evidencia") or []:
            eid = e.get("id_evidencia")
            if eid and eid not in vistos_ev:
                vistos_ev.add(eid)
                ev_all.append(e)
        for n in bloque.get("notas") or []:
            if "Error" in str(n) or "no disponible" in str(n):
                errores.append(str(n))

    versiones_utilizadas: Dict[str, str] = {}
    contratos_utilizados: Dict[str, str] = {}
    for e in ev_all:
        mod = e.get("modulo")
        if mod and e.get("version_modulo"):
            versiones_utilizadas[str(mod)] = str(e["version_modulo"])
        if mod and e.get("version_contrato"):
            contratos_utilizados[str(mod)] = str(e["version_contrato"])

    salida: Dict[str, Any] = {
        "id_calculo": id_calculo,
        "C": C,
        "L": L,
        "K": K,
        "precision": prec,
        "errores": errores,
        "metodo": metodo,
        "evidencia": ev_all,
        "id_evidencias": [e.get("id_evidencia") for e in ev_all],
        "versiones_utilizadas": versiones_utilizadas,
        "contratos_utilizados": contratos_utilizados,
        "modulos_consultados": sorted({
            e.get("modulo") for e in ev_all if e.get("modulo")
        }),
        "capacidades_consultadas": sorted({
            e.get("capacidad") for e in ev_all if e.get("capacidad")
        }),
    }
    if meta_conteos is not None:
        salida["conteos"] = meta_conteos
    if escala_meta is not None:
        salida["escala"] = escala_meta

    cent = _centinela_resultado(salida, peticion, ev_all)
    salida["centinela"] = cent
    if not cent["ok"]:
        salida["errores"] = list(salida.get("errores") or []) + list(
            cent["problemas"]
        )

    t1 = datetime.now(timezone.utc)
    salida["inicio"] = t0.isoformat()
    salida["fin"] = t1.isoformat()
    salida["duracion_ms"] = int((t1 - t0).total_seconds() * 1000)
    salida["version_ca"] = VERSION_MODULO
    salida["esquema"] = ESQUEMA_CONTRATO

    # Historial liviano (sin evidencia completa)
    _EVIDENCIA_POR_CALC[id_calculo] = ev_all
    _HISTORIAL.append({
        "id_calculo": id_calculo,
        "timestamp": salida["fin"],
        "metodo": metodo,
        "resultado": {
            "C": {
                "fraccion": (C or {}).get("fraccion"),
                "decimal": (C or {}).get("decimal"),
                "display": (C or {}).get("display"),
            },
            "L": {
                "fraccion": (L or {}).get("fraccion"),
                "decimal": (L or {}).get("decimal"),
                "display": (L or {}).get("display"),
            },
            "K": {
                "fraccion": (K or {}).get("fraccion"),
                "decimal": (K or {}).get("decimal"),
                "display": (K or {}).get("display"),
            },
        },
        "id_evidencias": list(salida["id_evidencias"]),
        "modulos_consultados": salida["modulos_consultados"],
        "capacidades_consultadas": salida["capacidades_consultadas"],
        "versiones_utilizadas": versiones_utilizadas,
        "centinela_ok": cent["ok"],
        "errores": list(salida["errores"]),
        "duracion_ms": salida["duracion_ms"],
        "escala_id": escala_id,
        "precision": prec,
    })

    if salida["errores"]:
        try:
            from core.diagnostico import DiagnosticoGlobal  # type: ignore
            recibir = getattr(DiagnosticoGlobal, "recibir_reporte", None)
            if callable(recibir):
                recibir(
                    NOMBRE_MODULO,
                    [
                        {"tipo": "error_calculo", "detalle": e}
                        for e in salida["errores"]
                    ],
                )
        except Exception:  # noqa: BLE001
            pass

    return salida

# ===============================================================
# FIN 8.9
# ===============================================================


# ===============================================================
# 8.10 — EXPLICAR CÁLCULO
# ===============================================================

def explicar_calculo(id_calculo: str) -> Optional[Dict[str, Any]]:
    """Explicacion dinamica desde evidencia real del calculo."""
    key = str(id_calculo or "").strip()
    item = None
    for h in reversed(_HISTORIAL):
        if h.get("id_calculo") == key:
            item = h
            break
    if item is None:
        return None

    evidencia = list(_EVIDENCIA_POR_CALC.get(key) or [])
    # reconstruir desde ids si hace falta
    if not evidencia:
        for eid in item.get("id_evidencias") or []:
            if eid in _REG_EVIDENCIA:
                evidencia.append(_REG_EVIDENCIA[eid])

    por_factor: Dict[str, List[Dict[str, Any]]] = {"C": [], "L": [], "K": []}
    otros: List[Dict[str, Any]] = []
    for e in evidencia:
        cap = str(e.get("capacidad") or "")
        if "calcular_C" in cap or cap.endswith("_C") or "coherencia" in cap:
            por_factor["C"].append(e)
        elif "calcular_L" in cap or "logica" in cap:
            por_factor["L"].append(e)
        elif "calcular_K" in cap or "correlacion" in cap:
            por_factor["K"].append(e)
        else:
            otros.append(e)

    def _lineas(evs: List[Dict[str, Any]]) -> List[str]:
        lines = []
        for e in evs:
            lines.append(
                "{0}.{1} aporte={2} version={3}".format(
                    e.get("modulo"),
                    e.get("capacidad"),
                    e.get("aporte"),
                    e.get("version_modulo"),
                )
            )
        return lines

    res = item.get("resultado") or {}
    return {
        "id_calculo": key,
        "resultado": res,
        "C": {
            "display": (res.get("C") or {}).get("display"),
            "proviene_de": _lineas(por_factor["C"]) or [
                "API coherencia / conteos compromisos-contradicciones"
            ],
        },
        "L": {
            "display": (res.get("L") or {}).get("display"),
            "proviene_de": _lineas(por_factor["L"]) or [
                "API logica / 1 - r/p (UNDEFINED si p=0)"
            ],
        },
        "K": {
            "display": (res.get("K") or {}).get("display"),
            "proviene_de": _lineas(por_factor["K"]) or [
                "API correlacion_k / requiere O_context"
            ],
        },
        "evidencia_adicional": _lineas(otros),
        "modulos_consultados": item.get("modulos_consultados"),
        "capacidades_consultadas": item.get("capacidades_consultadas"),
        "versiones_utilizadas": item.get("versiones_utilizadas"),
        "evidencia": evidencia,
        "anclas": [
            "Def-5.3.1 (K sin O => None)",
            "AM-D6 / AM-A3 (L con p=0 => UNDEFINED)",
            "salida: un objeto por factor con fraccion = decimal",
        ],
        "centinela_ok": item.get("centinela_ok"),
        "errores": item.get("errores"),
        "timestamp": item.get("timestamp"),
        "duracion_ms": item.get("duracion_ms"),
        "precision": item.get("precision"),
    }

# ===============================================================
# FIN 8.10
# ===============================================================


# ===============================================================
# 8.11 — HISTORIAL
# ===============================================================

def historial(limite: Optional[int] = None) -> List[Dict[str, Any]]:
    items = list(_HISTORIAL)
    if limite is not None:
        try:
            items = items[-max(0, int(limite)):]
        except Exception:  # noqa: BLE001
            pass
    return items

# ===============================================================
# FIN 8.11
# ===============================================================


# ===============================================================
# 8.12 — VERIFICAR SALIDA
# ===============================================================

def verificar_salida(salida: Any) -> bool:
    if not isinstance(salida, dict):
        return False
    if not all(k in salida for k in ("C", "L", "K", "id_calculo")):
        return False
    for f in ("C", "L", "K"):
        bloque = salida.get(f)
        if bloque is None:
            continue
        if not isinstance(bloque, dict):
            return False
        if "display" not in bloque:
            return False
        # no debe haber C_fraccion en la raiz
    if any(k in salida for k in ("C_fraccion", "L_fraccion", "K_fraccion")):
        return False
    return True

# ===============================================================
# FIN 8.12
# ===============================================================
# ===============================================================
# 8.13 — VERIFICAR CÁLCULO DE C, L, K
# ===============================================================

def verificar_calculo_de_C_L_K(calculo: Dict[str, Any]) -> Dict[str, Any]:
    """
    Verifica la integridad y coherencia del cálculo de C, L y K.

    Args:
        calculo: Diccionario con los resultados de C, L, K (salida de calcular())

    Returns:
        Dict con:
            - valido: bool
            - errores: List[str]
            - advertencias: List[str]
            - C: dict o None
            - L: dict o None
            - K: dict o None
            - verificacion: dict con detalles por factor
    """
    if not isinstance(calculo, dict):
        return {
            "valido": False,
            "errores": ["El calculo debe ser un dict"],
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
    # 8.13.1 — VERIFICAR C
    # -----------------------------------------------------------
    C = calculo.get("C")
    if C is None:
        errores.append("C no está presente en el cálculo")
        verificacion["C"] = {"presente": False, "ok": False}
    elif not isinstance(C, dict):
        errores.append("C debe ser un dict")
        verificacion["C"] = {
            "presente": True,
            "ok": False,
            "tipo": type(C).__name__,
        }
    else:
        ok_c = True
        detalles = {}

        for campo in [
            "fraccion", "decimal", "display", "numerador", "denominador"
        ]:
            if campo not in C:
                errores.append(f"C falta campo '{campo}'")
                ok_c = False
                detalles[campo] = "FALTANTE"
            else:
                detalles[campo] = C.get(campo)

        if "fraccion" in C and "numerador" in C and "denominador" in C:
            fraccion = C.get("fraccion")
            num = C.get("numerador")
            den = C.get("denominador")
            if fraccion and num is not None and den is not None:
                esperado = f"{num}/{den}"
                if str(fraccion) != esperado:
                    advertencias.append(
                        f"C: fraccion '{fraccion}' no coincide con "
                        f"numerador/denominador '{esperado}'"
                    )

        verificacion["C"] = {
            "presente": True,
            "ok": ok_c,
            "detalles": detalles,
        }

    # -----------------------------------------------------------
    # 8.13.2 — VERIFICAR L
    # -----------------------------------------------------------
    L = calculo.get("L")
    if L is None:
        advertencias.append(
            "L no está presente en el cálculo (puede ser UNDEFINED)"
        )
        verificacion["L"] = {
            "presente": False,
            "ok": True,
            "nota": "L puede ser UNDEFINED si p=0",
        }
    elif not isinstance(L, dict):
        errores.append("L debe ser un dict")
        verificacion["L"] = {
            "presente": True,
            "ok": False,
            "tipo": type(L).__name__,
        }
    else:
        if L.get("undefined"):
            verificacion["L"] = {
                "presente": True,
                "ok": True,
                "undefined": True,
                "detalles": {"display": L.get("display")},
            }
        else:
            ok_l = True
            detalles = {}
            for campo in ["fraccion", "decimal", "display"]:
                if campo not in L:
                    errores.append(f"L falta campo '{campo}'")
                    ok_l = False
                    detalles[campo] = "FALTANTE"
                else:
                    detalles[campo] = L.get(campo)
            verificacion["L"] = {
                "presente": True,
                "ok": ok_l,
                "detalles": detalles,
            }

    # -----------------------------------------------------------
    # 8.13.3 — VERIFICAR K
    # -----------------------------------------------------------
    K = calculo.get("K")
    if K is None:
        advertencias.append(
            "K no está presente (puede ser None sin contexto/O)"
        )
        verificacion["K"] = {
            "presente": False,
            "ok": True,
            "nota": "K=None es legitimo sin contexto/O (Def-5.3.1)",
        }
    elif not isinstance(K, dict):
        errores.append("K debe ser un dict")
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
                "none": True,
                "detalles": {"display": K.get("display")},
            }
        else:
            ok_k = True
            detalles = {}
            for campo in ["fraccion", "decimal", "display"]:
                if campo not in K:
                    errores.append(f"K falta campo '{campo}'")
                    ok_k = False
                    detalles[campo] = "FALTANTE"
                else:
                    detalles[campo] = K.get(campo)
            verificacion["K"] = {
                "presente": True,
                "ok": ok_k,
                "detalles": detalles,
            }

    # -----------------------------------------------------------
    # 8.13.4 — VERIFICACIONES ADICIONALES
    # -----------------------------------------------------------
    if "id_calculo" not in calculo:
        advertencias.append("Falta 'id_calculo' en el resultado")

    centinela = calculo.get("centinela")
    if centinela is None:
        advertencias.append("Falta 'centinela' en el resultado")
    elif not centinela.get("ok"):
        errores.extend(centinela.get("problemas") or [])

    if calculo.get("errores"):
        errores.extend(calculo.get("errores") or [])

    # -----------------------------------------------------------
    # 8.13.5 — RESULTADO
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
            "C_ok": verificacion.get("C", {}).get("ok", False),
            "L_ok": verificacion.get("L", {}).get("ok", False),
            "K_ok": verificacion.get("K", {}).get("ok", False),
            "centinela_ok": centinela.get("ok") if centinela else False,
        },
    }

# ===============================================================
# FIN 8.13
# ===============================================================  
    # ===============================================================
# 8.14 — INVENTARIO
# ===============================================================

def inventario(peticion: Any = None) -> Dict[str, Any]:
    b = barrer()
    return {
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "archivos": b.get("archivos"),
        "hashes": b.get("hashes"),
        "factores_api": b.get("factores_api"),
        "conteos_disponible": b.get("conteos_disponible"),
        "escalas_ids_disponible": b.get("escalas_ids_disponible"),
        "ids_escala": b.get("ids_escala"),
        "coherente": b.get("coherente"),
        "historial_n": b.get("historial_n"),
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "invariantes": CONTENEDOR.get("invariantes"),
        "precision_decimal_default": PRECISION_DECIMAL_DEFAULT,
        "regla_salida": (
            "un objeto por factor: fraccion = decimal (7/9 = 0.778)"
        ),
    }

# ===============================================================
# FIN 8.14
# ===============================================================


# ===============================================================
# 8.15 — EJECUTAR TOTAL
# ===============================================================

def ejecutar_total(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Autoridad total de ENGINE sobre CA.
    Ejerce TODAS las unidades operativamente ejecutables del módulo
    conforme a su contrato e inventario.

    Todo es callable real. Nada es texto.
    No inventa capacidades. No altera el contrato.
    """
    peticion = dict(peticion or {}) if isinstance(peticion, dict) else {}
    resultados: Dict[str, Any] = {}
    errores_ejecucion: List[str] = []

    # 1. Centinela
    try:
        resultados["barrer"] = barrer()
        resultados["verificar"] = resultados["barrer"]
    except Exception as e:  # noqa: BLE001
        errores_ejecucion.append("barrer: {0}".format(e))
        resultados["barrer"] = None

    # 2. Inventario y diagnóstico
    try:
        resultados["inventario"] = inventario(peticion)
    except Exception as e:  # noqa: BLE001
        errores_ejecucion.append("inventario: {0}".format(e))
        resultados["inventario"] = None

    try:
        resultados["diagnostico"] = diagnostico()
    except Exception as e:  # noqa: BLE001
        errores_ejecucion.append("diagnostico: {0}".format(e))
        resultados["diagnostico"] = None

    try:
        resultados["reporte"] = reporte()
    except Exception as e:  # noqa: BLE001
        errores_ejecucion.append("reporte: {0}".format(e))
        resultados["reporte"] = None

    # 3. Escalas e historial
    try:
        resultados["leer_ids_escala"] = leer_ids_escala()
    except Exception as e:  # noqa: BLE001
        errores_ejecucion.append("leer_ids_escala: {0}".format(e))
        resultados["leer_ids_escala"] = None

    try:
        resultados["historial"] = historial()
    except Exception as e:  # noqa: BLE001
        errores_ejecucion.append("historial: {0}".format(e))
        resultados["historial"] = None

    # 4. Representación determinista
    try:
        resultados["representar"] = {
            "ejemplo_fraccion": representar(Fraction(7, 9)),
            "ejemplo_none": representar(None),
            "ejemplo_undefined": representar(UNDEFINED),
        }
    except Exception as e:  # noqa: BLE001
        errores_ejecucion.append("representar: {0}".format(e))
        resultados["representar"] = None

    # 5. Validación de evidencia
    try:
        resultados["validar_evidencia"] = validar_evidencia(
            peticion.get("evidencia")
        )
    except Exception as e:  # noqa: BLE001
        errores_ejecucion.append("validar_evidencia: {0}".format(e))
        resultados["validar_evidencia"] = None

    # 6. Factores C / L / K
    try:
        resultados["calcular_C"] = calcular_C(peticion)
    except Exception as e:  # noqa: BLE001
        errores_ejecucion.append("calcular_C: {0}".format(e))
        resultados["calcular_C"] = None

    try:
        resultados["calcular_L"] = calcular_L(peticion)
    except Exception as e:  # noqa: BLE001
        errores_ejecucion.append("calcular_L: {0}".format(e))
        resultados["calcular_L"] = None

    try:
        resultados["calcular_K"] = calcular_K(peticion)
    except Exception as e:  # noqa: BLE001
        errores_ejecucion.append("calcular_K: {0}".format(e))
        resultados["calcular_K"] = None

    # 7. Pipeline completo
    try:
        resultados["calcular"] = calcular(peticion)
    except Exception as e:  # noqa: BLE001
        errores_ejecucion.append("calcular: {0}".format(e))
        resultados["calcular"] = None

    # 8. Verificar salida del pipeline
    calc_out = resultados.get("calcular")
    if isinstance(calc_out, dict):
        try:
            resultados["verificar_salida"] = verificar_salida(calc_out)
            resultados["verificar_calculo_de_C_L_K"] = (
                verificar_calculo_de_C_L_K(calc_out)
            )
        except Exception as e:  # noqa: BLE001
            errores_ejecucion.append(
                "verificar_calculo: {0}".format(e)
            )
    else:
        resultados["verificar_salida"] = None
        resultados["verificar_calculo_de_C_L_K"] = None

    # 9. Inspección y registro
    try:
        resultados["inspeccionar"] = inspeccionar(peticion)
    except Exception as e:  # noqa: BLE001
        errores_ejecucion.append("inspeccionar: {0}".format(e))
        resultados["inspeccionar"] = None

    try:
        resultados["registrar_inventario"] = registrar_inventario(peticion)
    except Exception as e:  # noqa: BLE001
        errores_ejecucion.append("registrar_inventario: {0}".format(e))
        resultados["registrar_inventario"] = None

    coherente = False
    if isinstance(resultados.get("barrer"), dict):
        coherente = bool(resultados["barrer"].get("coherente"))

    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "operacion": "ejecutar_total",
        "estado": ESTADO_OPERATIVO if coherente else ESTADO_DEGRADADO,
        "coherente": coherente,
        "capacidades_ejecutadas": sorted([
            k for k, v in resultados.items() if v is not None
        ]),
        "errores_ejecucion": errores_ejecucion,
        "resultados": resultados,
        "capacidades_declaradas": list(
            CONTENEDOR.get("capacidades", {}).keys()
        ),
        "nota": (
            "ejecutar_total ejerce autoridad total de ENGINE sobre CA. "
            "Todas las unidades son callables reales. "
            "No inventa capacidades ni altera el contrato."
        ),
    }

# ===============================================================
# FIN 8.15
# ===============================================================


# ===============================================================
# 8.16 — INSPECCIONAR
# ===============================================================

def inspeccionar(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Inspección estructural de CA.
    Expone contrato, APIs y estado sin calcular factores.
    """
    res_barrer = barrer()
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
            "PRECISION_DECIMAL_DEFAULT": PRECISION_DECIMAL_DEFAULT,
            "FACTORES_CANONICOS": list(_FACTORES_CANONICOS),
        },
        "capacidades_contractuales": list(
            CONTENEDOR.get("capacidades", {}).keys()
        ),
        "capacidades_meta": list(
            CONTENEDOR.get("capacidades_meta", {}).keys()
        ),
        "apis": {
            "factores_cargados": sorted(_APIS.keys()),
            "errores_carga": list(_ERRORES_CARGA),
            "conteos_disponible": _CONTEOS is not None,
            "escalas_ids_disponible": _ESCALAS is not None,
        },
        "integridad": {
            "coherente": res_barrer.get("coherente"),
            "archivos": res_barrer.get("archivos"),
            "historial_n": res_barrer.get("historial_n"),
        },
        "autoriza_engine": CONTENEDOR.get("autoriza_engine"),
        "reporting": CONTENEDOR.get("reporting"),
        "invariantes": list(INVARIANTES),
        "nota": (
            "inspeccionar expone estructura de CA sin calcular "
            "ni alterar el contrato."
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
    Registra el inventario estructural de CA como instantánea determinista.
    No altera evidencia de cálculos previos.
    """
    inv = inventario(peticion)
    return {
        "id": ID_MODULO,
        "operacion": "registrar_inventario",
        "registrado": True,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "inventario": inv,
        "nota": (
            "Instantánea determinista del inventario de CA. "
            "No modifica historial ni evidencia de cálculos."
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
    b = barrer()
    estado = ESTADO_OPERATIVO if b.get("coherente") else ESTADO_DEGRADADO
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "estado": estado,
        "coherente": b.get("coherente"),
        "factores_api": b.get("factores_api"),
        "archivos": b.get("archivos"),
        "hashes": b.get("hashes"),
        "historial_n": b.get("historial_n"),
        "errores_n": len(b.get("errores") or []),
        "choques_n": len(b.get("choques") or []),
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "regla_salida": (
            "un objeto por factor: fraccion = decimal (7/9 = 0.778)"
        ),
        "autoridad": CONTENEDOR.get("autoridad"),
        "conocimiento_exportable": CONTENEDOR.get(
            "conocimiento_exportable"
        ),
        "operaciones_arquitectonicas": {
            "ejecutar_total": True,
            "inspeccionar": True,
            "registrar_inventario": True,
        },
    }

# ===============================================================
# FIN 9.1
# ===============================================================


# ===============================================================
# 9.2 — DIAGNÓSTICO
# ===============================================================

def diagnostico() -> Dict[str, Any]:
    b = barrer()
    problemas: List[Dict[str, Any]] = []
    advertencias: List[str] = []
    recomendaciones: List[str] = []

    if b.get("errores"):
        problemas.append({"tipo": "errores_carga", "detalle": b["errores"]})
        recomendaciones.append("Revisar APIs C/L/K y hashes")
    if b.get("choques"):
        problemas.append({"tipo": "choques_factor", "detalle": b["choques"]})
    if not b.get("conteos_disponible"):
        advertencias.append("conteos.py no disponible")
    if not b.get("factores_api"):
        problemas.append({"tipo": "sin_apis", "detalle": "sin C/L/K"})
        recomendaciones.append(
            "Verificar coherencia.py, logica.py, correlacion_k.py"
        )

    estado = ESTADO_OPERATIVO if b.get("coherente") else ESTADO_DEGRADADO
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "estado": estado,
        "problemas": problemas,
        "advertencias": advertencias,
        "recomendaciones": recomendaciones,
        "coherente": b.get("coherente"),
        "factores_api": b.get("factores_api"),
        "historial_n": b.get("historial_n"),
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
    "verificar": barrer,
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
}

# ===============================================================
# FIN 10.1
# ===============================================================


# ===============================================================
# 10.2 — RESOLUCIÓN DE CAPACIDADES
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
            f"{NOMBRE_MODULO}: capacidad '{nombre}' tipo invalido"
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
