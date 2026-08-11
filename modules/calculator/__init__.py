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
# IMPORTACIONES
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
# FIN IMPORTACIONES
# ===============================================================


# ===============================================================
# CONSTANTES
# ===============================================================

ID_MODULO = "CA"
NOMBRE_MODULO = "calculator"
ROL_MODULO = "CA"

VERSION_MODULO = "2.3"
VERSION_CONTRATO = "1.0"
ESQUEMA_CONTRATO = "VPSI-CONTRACT-1.0"

COMPATIBLE_DESDE = "1.2"
API_ENGINE = ">=1.0"
ESTABILIDAD = "ESTABLE"

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
# FIN CONSTANTES
# ===============================================================


# ===============================================================
# CONFIGURACIÓN
# ===============================================================

_DIR = Path(__file__).parent

# ===============================================================
# FIN CONFIGURACIÓN
# ===============================================================


# ===============================================================
# DEFINICIONES
# ===============================================================

class ContratoInvalido(Exception):
    pass


class DominioError(ValueError):
    pass


class MetodoError(ValueError):
    pass


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


_CALC_SEQ = 0
_EV_SEQ = 0
_HISTORIAL: Deque[Dict[str, Any]] = deque(maxlen=HISTORIAL_MAX)
_EVIDENCIA_POR_CALC: Dict[str, List[Dict[str, Any]]] = {}
_REG_EVIDENCIA: Dict[str, Dict[str, Any]] = {}

# ===============================================================
# FIN DEFINICIONES
# ===============================================================

# ===============================================================
# CONTRATO OFICIAL DEL MÓDULO
# ===============================================================

CONTENEDOR: Dict[str, Any] = {
    # ============================================================
    # ESQUEMA
    # ============================================================
    "esquema": ESQUEMA_CONTRATO,
    "version_contrato": VERSION_CONTRATO,
    "version_modulo": VERSION_MODULO,
    "estabilidad": ESTABILIDAD,
    "compatible_desde": COMPATIBLE_DESDE,
    "api_engine": API_ENGINE,

    # ============================================================
    # IDENTIDAD
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
    # PROPÓSITO
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
    # AUTORIDAD
    # ============================================================
    "autoridad": [
        "Unica autoridad para calcular C, L, K",
        "Reportar cada factor como fraccion = decimal en un solo objeto",
        "Validar evidencia y explicar calculos con trazabilidad real",
        "Auditar integridad del dominio",
    ],

    # ============================================================
    # CONOCIMIENTO EXPORTABLE
    # ============================================================
    "conocimiento_exportable": [
        "C", "L", "K", "factores", "UNDEFINED",
        "evidencia", "versiones_utilizadas", "contratos_utilizados",
        "historial", "explicaciones",
        "inventario", "estado", "reporte", "diagnostico",
    ],

    #============================================================
    # ACCESO (obligatorio en el esquema)
    # ============================================================
    "acceso": {
        "nivel": "completo",
        "descripcion": "Acceso total a recursos del módulo"
    },

    # ============================================================
    # DEPENDENCIAS
    # ============================================================
    "requiere": ["*"],

    # ============================================================
    # ACCESO A ARCHIVOS (AGREGADO — obligatorio en el esquema)
    # ============================================================
    "acceso_archivos": ["*"],

    # ============================================================
    # VALIDAR ESQUEMA A NIVEL MÓDULO (AGREGADO — obligatorio en el esquema)
    # ============================================================
    "validar_esquema": ["*"],


    # ============================================================
    # AUTORIZACIÓN AL ENGINE (SOLO PERMISOS)
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
        # "modificar": False,    # ← ELIMINADO (no permitido)
        "alterar": False,
        # "reescribir": False,   # ← ELIMINADO (no permitido)
        "crear": True,
        # "eliminar": False,     # ← ELIMINADO (no permitido)
        "actualizar": False,

        # --- PERMISOS DE PROCESAMIENTO ---
        "validar": True,
        "procesar": True,
        "analizar": True,
        "generar": True,
        # "transformar": False,  # ← ELIMINADO (no permitido)

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

        # --- PERMISOS AGREGADOS (OBLIGATORIOS) ---
        "validar_esquema": True,     # ← AGREGADO
        "acceso_archivos": True,     # ← AGREGADO
    },
    # ============================================================
    # CONSULTAS SOPORTADAS
    # ============================================================
    "consultas_soportadas": [
        "calcular", "calcular_C", "calcular_L", "calcular_K",
        "calcular_factor", "representar", "validar_evidencia",
        "explicar_calculo", "verificar_coherencia",
        "obtener_inventario", "obtener_reporte", "obtener_diagnostico",
        "leer_ids_escala", "historial", "verificar_calculo_de_C_L_K",
    ],

    # ============================================================
    # CAPACIDADES
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
        "verificar_calculo_de_C_L_K": "verificar_calculo_de_C_L_K"
    },

    # ============================================================
    # META CALCULOS DE CAPACIDADES (1:1 OBLIGATORIO)
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
    },
    
    # ============================================================
    # REPORTING (OBLIGATORIO EN EL ESQUEMA)
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
        "acceso_archivos": True,      # ← AGREGADA
        "validar_esquema": True,      # ← AGREGADA
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
# FUNCIONES PRIVADAS
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
# FIN FUNCIONES PRIVADAS
# ===============================================================


# ===============================================================
# CAPACIDADES PÚBLICAS
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


def barrer() -> Dict[str, Any]:
    errores: List[Dict[str, str]] = list(_ERRORES_CARGA)
    choques: List[str] = []
    archivos = [p.name for p in _listar_py()]
    hashes = _hashes_modulo()

    factores_ok = sorted(_APIS.keys())
    for factor in _FACTORES_CANONICOS:
        if factor not in _APIS:
            errores.append({
                "archivo": "?",
                "error": "factor '{0}' sin API".format(factor),
            })

    por_factor: Dict[str, List[str]] = {}
    for stem, factor in _ARCHIVO_FACTOR.items():
        if (_DIR / "{0}.py".format(stem)).exists():
            por_factor.setdefault(factor, []).append(stem)
    for factor, stems in por_factor.items():
        if len(stems) > 1:
            choques.append(
                "factor '{0}' reclamado por: {1}".format(factor, stems)
            )

    stems_conocidos = set(_ARCHIVO_FACTOR.keys()) | {"conteos", "escalas_ids"}
    extra = [p.stem for p in _listar_py() if p.stem not in stems_conocidos]

    for nombre, meta in hashes.items():
        if meta.get("sha256") is None:
            errores.append({
                "archivo": nombre,
                "error": meta.get("error") or "hash no calculable",
            })

    return {
        "contenedor": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "coherente": not errores and not choques,
        "errores": errores,
        "choques": choques,
        "archivos": archivos,
        "hashes": hashes,
        "factores_api": factores_ok,
        "archivos_extra": extra,
        "conteos_disponible": _CONTEOS is not None,
        "escalas_ids_disponible": _ESCALAS is not None,
        "ids_escala": leer_ids_escala(),
        "historial_n": len(_HISTORIAL),
    }


def calcular_C(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    peticion = dict(peticion or {})
    metodo = str(peticion.get("metodo") or "operacional")
    prec = int(peticion.get("precision") or PRECISION_DECIMAL_DEFAULT)
    if metodo == "operacional":
        peticion = _asegurar_conteos(peticion)

    evidencia = _normalizar_evidencia(peticion.get("evidencia"))
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

    fn = _APIS.get("C")
    if not callable(fn):
        return {
            "C": representar(None, prec),
            "ruta": None,
            "notas": ["API C no disponible"],
            "evidencia": evidencia,
        }

    try:
        try:
            raw = fn(peticion) if _acepta_dict(fn) else fn(
                compromisos=peticion.get("compromisos"),
                contradicciones=peticion.get("contradicciones"),
                metodo=metodo,
            )
        except TypeError:
            raw = fn(peticion)

        val = raw["C"] if isinstance(raw, dict) and "C" in raw else raw
        if es_undefined(val):
            obj = representar(UNDEFINED, prec)
        else:
            obj = representar(
                val if isinstance(val, Fraction) else _a_fraction(val),
                prec,
            )
        return {"C": obj, "ruta": metodo, "notas": [], "evidencia": evidencia}
    except Exception as e:  # noqa: BLE001
        return {
            "C": representar(None, prec),
            "ruta": metodo,
            "notas": ["Error en C: {0}".format(e)],
            "evidencia": evidencia,
        }


def calcular_L(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    peticion = dict(peticion or {})
    metodo = str(peticion.get("metodo") or "operacional")
    prec = int(peticion.get("precision") or PRECISION_DECIMAL_DEFAULT)
    if metodo == "operacional":
        peticion = _asegurar_conteos(peticion)

    evidencia = _normalizar_evidencia(peticion.get("evidencia"))
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

    fn = _APIS.get("L")
    if not callable(fn):
        return {
            "L": representar(None, prec),
            "p": None,
            "r": None,
            "ruta": None,
            "notas": ["API L no disponible"],
            "evidencia": evidencia,
        }

    try:
        try:
            raw = fn(peticion) if _acepta_dict(fn) else fn(
                posturas=peticion.get("posturas"),
                reversiones=peticion.get("reversiones"),
                metodo=metodo,
            )
        except TypeError:
            raw = fn(peticion)

        p = r = None
        if isinstance(raw, dict) and "L" in raw:
            val = raw["L"]
            p = raw.get("p")
            r = raw.get("r")
        else:
            val = raw

        if es_undefined(val):
            obj = representar(UNDEFINED, prec)
            notas = ["L=UNDEFINED (AM-D6)"]
        else:
            obj = representar(
                val if isinstance(val, Fraction) else _a_fraction(val),
                prec,
            )
            notas = []

        return {
            "L": obj,
            "p": p,
            "r": str(r) if r is not None else None,
            "ruta": metodo,
            "notas": notas,
            "evidencia": evidencia,
        }
    except Exception as e:  # noqa: BLE001
        return {
            "L": representar(None, prec),
            "ruta": metodo,
            "notas": ["Error en L: {0}".format(e)],
            "evidencia": evidencia,
        }


def calcular_K(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    peticion = dict(peticion or {})
    metodo = str(peticion.get("metodo") or "operacional")
    prec = int(peticion.get("precision") or PRECISION_DECIMAL_DEFAULT)
    o_ctx = (
        peticion.get("contexto")
        or peticion.get("O_context")
        or peticion.get("o_context")
    )

    evidencia = _normalizar_evidencia(peticion.get("evidencia"))
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

    if o_ctx is None:
        return {
            "K": representar(None, prec),
            "ruta": metodo,
            "notas": ["K=None sin contexto/O (Def-5.3.1)"],
            "evidencia": evidencia,
        }

    if metodo == "operacional":
        peticion = _asegurar_conteos(peticion)

    fn = _APIS.get("K")
    if not callable(fn):
        return {
            "K": representar(None, prec),
            "ruta": None,
            "notas": ["API K no disponible"],
            "evidencia": evidencia,
        }

    try:
        try:
            raw = fn(peticion) if _acepta_dict(fn) else fn(
                afirmaciones=peticion.get("afirmaciones"),
                afirmaciones_falsas=peticion.get("afirmaciones_falsas"),
                o_context=o_ctx,
                metodo=metodo,
            )
        except TypeError:
            raw = fn(peticion)

        val = raw["K"] if isinstance(raw, dict) and "K" in raw else raw
        if es_undefined(val):
            obj = representar(UNDEFINED, prec)
        else:
            obj = representar(
                val if isinstance(val, Fraction) else _a_fraction(val),
                prec,
            )
        return {"K": obj, "ruta": metodo, "notas": [], "evidencia": evidencia}
    except Exception as e:  # noqa: BLE001
        return {
            "K": representar(None, prec),
            "ruta": metodo,
            "notas": ["Error en K: {0}".format(e)],
            "evidencia": evidencia,
        }


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


def historial(limite: Optional[int] = None) -> List[Dict[str, Any]]:
    items = list(_HISTORIAL)
    if limite is not None:
        try:
            items = items[-max(0, int(limite)):]
        except Exception:  # noqa: BLE001
            pass
    return items


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
        "regla_salida": "un objeto por factor: fraccion = decimal (7/9 = 0.778)",
    }

# ===============================================================
# FIN CAPACIDADES PÚBLICAS
# ===============================================================


# ===============================================================
# REPORTING INTERNO
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
        "regla_salida": "un objeto por factor: fraccion = decimal (7/9 = 0.778)",
        "autoridad": CONTENEDOR.get("autoridad"),
        "conocimiento_exportable": CONTENEDOR.get("conocimiento_exportable"),
    }


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
        recomendaciones.append("Verificar coherencia.py, logica.py, correlacion_k.py")

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
# FIN REPORTING
# ===============================================================


# ===============================================================
# EXPORTACIONES + RESOLUCIÓN ESTRICTA
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
    "inventario": inventario,
    "reporte": reporte,
    "diagnostico": diagnostico,
    "leer_ids_escala": leer_ids_escala,
    "verificar_salida": verificar_salida,
    "historial": historial,
    "verificar_calculo_de_C_L_K": verificar_calculo_de_C_L_K
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
            f"{NOMBRE_MODULO}: capacidad '{nombre}' tipo invalido"
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
    "ContratoInvalido",
]

# ===============================================================
# FIN DEL MÓDULO
# ===============================================================
