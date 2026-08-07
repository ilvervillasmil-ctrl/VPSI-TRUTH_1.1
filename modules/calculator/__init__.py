# ===============================================================
# VPSI-TRUTH — modules/calculator/__init__.py
# ===============================================================
#
# MÓDULO:              calculator
# ID:                  CA
# Rol:                 CA
# Versión módulo:      2.0
# Versión contrato:    1.0
# Esquema contrato:    VPSI-CONTRACT-1.0
# Estabilidad:         ESTABLE
# Compatible desde:    1.2
# API Engine:          >=1.0
#
# Función:
#   Única autoridad del dominio de cálculo estructural del sistema VPSI.
#   Calcula los factores C, L, K (y factores estructurales futuros).
#   No calcula Tru_Ri ni Tru_total (eso es FO).
#
# Qué hace:
#   - Calcula C, L, K
#   - Integra conocimiento autorizado del ecosistema vía capacidades
#   - Produce conteos operacionales si faltan
#   - Representa Fraction en decimal configurable (oficial = Fraction)
#   - Centinela interno de todo cálculo
#   - Inventario, reporte y diagnóstico propios
#
# Qué NO hace:
#   - No calcula Tru_Ri ni Tru_total
#   - No redefine constantes (CT), axiomas (AX) ni fórmulas (FO)
#   - No orquesta el sistema (Engine)
#   - No modifica otros módulos ni contratos ajenos
#
# Responsabilidad:
#   Ser la única autoridad del dominio de cálculo estructural.
#   Toda magnitud C/L/K debe estar sustentada por evidencia estructural
#   de módulos autorizados. Nunca estima por intuición.
#
# Autoridad:
#   - Calcular C, L, K y factores estructurales derivados
#   - Auditar integridad del dominio de cálculo
#   - Reportar inventario, estado y diagnóstico propios
#
# Conocimiento exportable:
#   C, L, K, factores, inventarios, reportes, diagnósticos, UNDEFINED
#
# Relación con Engine:
#   Engine descubre este CONTENEDOR y ejecuta capacidades declaradas.
#   CA integra conocimiento autorizado; no importa módulos ajenos a mano.
#
# Relación con Omega:
#   Omega no calcula nada de CA. Solo presenta lo que Engine entrega.
#
# Relación con FO:
#   CA entrega C, L, K. FO calcula Tru_Ri y Tru_total.
#
# Relación con CT:
#   CT entrega constantes oficiales. CA nunca crea constantes.
#
# ===============================================================


# ===============================================================
# IMPORTACIONES
# ===============================================================

from __future__ import annotations

import importlib
import importlib.util
import sys
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

# ===============================================================
# FIN IMPORTACIONES
# ===============================================================


# ===============================================================
# CONSTANTES
# ===============================================================

ID_MODULO = "CA"
NOMBRE_MODULO = "calculator"
ROL_MODULO = "CA"

VERSION_MODULO = "2.0"
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
    "CA calcula unicamente factores estructurales (C, L, K, derivados)",
    "FO es la unica autoridad sobre las formulas oficiales",
    "todo calculo interno utiliza Fraction",
    "float nunca representa el valor oficial",
    "el decimal es unicamente una representacion",
    "ningun calculo sale sin pasar por el centinela interno",
    "CA nunca modifica otros modulos ni redefine conocimiento ajeno",
    "CA solo integra conocimiento autorizado por contratos",
    "todo calculo es reproducible, auditable y trazable",
    "K ausente sin contexto/O es legitimo (Def-5.3.1)",
    "L = UNDEFINED cuando p=0 (AM-D6 / AM-A3)",
)

PRECISION_DECIMAL_DEFAULT = 3

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
    """El CONTENEDOR no cumple el esquema o la resolucion fallo."""
    pass


class DominioError(ValueError):
    """Entrada fuera de dominio."""


class MetodoError(ValueError):
    """Metodo de calculo no admitido."""


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
# FIN DEFINICIONES
# ===============================================================


# ===============================================================
# CONTRATO OFICIAL DEL MÓDULO
# ===============================================================

CONTENEDOR: Dict[str, Any] = {
    "esquema": ESQUEMA_CONTRATO,
    "version_contrato": VERSION_CONTRATO,
    "version_modulo": VERSION_MODULO,
    "estabilidad": ESTABILIDAD,
    "compatible_desde": COMPATIBLE_DESDE,
    "api_engine": API_ENGINE,

    "id": ID_MODULO,
    "nombre": NOMBRE_MODULO,
    "rol": ROL_MODULO,
    "descripcion": (
        "Unica autoridad del dominio de calculo estructural del sistema VPSI. "
        "Calcula los factores C, L, K. No calcula Tru_Ri ni Tru_total (FO). "
        "Integra conocimiento autorizado del ecosistema. Todo valor oficial "
        "es Fraction; el decimal es solo representacion."
    ),

    "funcion": (
        "Calcular factores estructurales C, L, K (y derivados futuros) "
        "integrando conocimiento autorizado. Entregar resultados trazables "
        "a FO. Proteger la integridad del dominio de calculo."
    ),
    "no_hace": [
        "No calcula Tru_Ri ni Tru_total",
        "No redefine constantes (CT)",
        "No redefine axiomas (AX)",
        "No redefine formulas (FO)",
        "No orquesta el sistema (Engine)",
        "No modifica otros modulos ni contratos ajenos",
        "No estima por intuicion: toda magnitud requiere evidencia estructural",
    ],

    "autoridad": [
        "Unica autoridad para calcular C, L, K y factores estructurales",
        "Integrar conocimiento autorizado del ecosistema",
        "Auditar integridad del dominio de calculo (centinela)",
        "Representar Fraction en decimal configurable",
        "Reportar inventario, estado y diagnostico propios",
    ],

    "conocimiento_exportable": [
        "C",
        "L",
        "K",
        "factores",
        "UNDEFINED",
        "inventario",
        "estado",
        "reporte",
        "diagnostico",
    ],

    "requiere": [],

    "autoriza_engine": {
        "leer": True,
        "ejecutar": True,
        "consultar": True,
        "recombinar": True,
        "reportar": True,
        "auditar": True,
        "inventariar": True,
        "modificar": False,
        "alterar": False,
        "reescribir": False,
    },

    "consultas_soportadas": [
        "calcular_C",
        "calcular_L",
        "calcular_K",
        "calcular",
        "representar",
        "verificar_coherencia",
        "obtener_inventario",
        "obtener_reporte",
        "obtener_diagnostico",
        "leer_ids_escala",
    ],

    "capacidades": {
        "calcular": "calcular",
        "calcular_C": "calcular_C",
        "calcular_L": "calcular_L",
        "calcular_K": "calcular_K",
        "calcular_factor": "calcular_factor",
        "representar": "representar",
        "verificar": "barrer",
        "barrer": "barrer",
        "inventario": "inventario",
        "reporte": "reporte",
        "diagnostico": "diagnostico",
        "leer_ids_escala": "leer_ids_escala",
        "verificar_salida": "verificar_salida",
    },

    "capacidades_meta": {
        "calcular": {
            "descripcion": "Orquesta C, L, K sobre una peticion. Pasa por centinela.",
            "entrada": "peticion: dict (metodo, conteos, contexto/O, escala_id, ...)",
            "salida": "dict con C, L, K, errores, metodo, conteos?, escala?, centinela",
        },
        "calcular_C": {
            "descripcion": "Calcula el factor de coherencia C.",
            "entrada": "peticion: dict",
            "salida": "dict con C (Fraction|None), ruta, notas",
        },
        "calcular_L": {
            "descripcion": "Calcula el factor de logica L (UNDEFINED si p=0).",
            "entrada": "peticion: dict",
            "salida": "dict con L (Fraction|UNDEFINED), p, r, ruta, notas",
        },
        "calcular_K": {
            "descripcion": "Calcula el factor de correlacion K (None sin O/contexto).",
            "entrada": "peticion: dict con contexto/O_context",
            "salida": "dict con K (Fraction|None), ruta, notas",
        },
        "calcular_factor": {
            "descripcion": "Calcula un factor estructural por nombre (C|L|K).",
            "entrada": "factor: str, peticion: dict",
            "salida": "dict del factor solicitado",
        },
        "representar": {
            "descripcion": "Representa Fraction como decimal configurable. No altera el valor oficial.",
            "entrada": "valor: Fraction|UNDEFINED|None, precision: int=3",
            "salida": "dict con fraccion, decimal, precision, undefined",
        },
        "verificar": {
            "descripcion": "Centinela del modulo: archivos, APIs, choques, conteos.",
            "entrada": "ninguna",
            "salida": "dict con coherente, errores, choques, factores_api, archivos",
        },
        "barrer": {
            "descripcion": "Alias de verificar. Centinela de carpeta e integridad.",
            "entrada": "ninguna",
            "salida": "dict con coherente, errores, choques, factores_api",
        },
        "inventario": {
            "descripcion": "Inventario completo del dominio de calculo.",
            "entrada": "peticion opcional",
            "salida": "dict con capacidades, factores, archivos, estado, version",
        },
        "reporte": {
            "descripcion": "Reporte interno de estado del modulo CA.",
            "entrada": "ninguna",
            "salida": "dict con estado, coherente, factores_api, capacidades",
        },
        "diagnostico": {
            "descripcion": "Diagnostico: problemas, advertencias, recomendaciones.",
            "entrada": "ninguna",
            "salida": "dict con estado, problemas, advertencias, recomendaciones",
        },
        "leer_ids_escala": {
            "descripcion": "Ids de escala reconocidos (atomo, frase, sujeto, ...).",
            "entrada": "ninguna",
            "salida": "dict con ids, n, origenes, disponible",
        },
        "verificar_salida": {
            "descripcion": "Comprueba forma minima de salida de calcular (C, L, K).",
            "entrada": "salida: dict",
            "salida": "bool",
        },
    },

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
    },

    "estados_validos": list(ESTADOS_VALIDOS),
    "invariantes": list(INVARIANTES),
}

# ===============================================================
# FIN CONTRATO
# ===============================================================


# ===============================================================
# FUNCIONES PRIVADAS — carga de submódulos
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
                    "error": "falta API publica callable '{0}'".format(fn_name),
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
        verificar = getattr(mod, "verificar_conteos", None)
        if callable(extraer) and callable(inyectar):
            return {
                "extraer_conteos": extraer,
                "inyectar_en_peticion": inyectar,
                "verificar_conteos": verificar if callable(verificar) else None,
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
        version = getattr(mod, "VERSION", None)
        if callable(ids_fn):
            return {
                "ids": ids_fn,
                "por_id": por_id if callable(por_id) else None,
                "version": version,
            }
    except Exception:  # noqa: BLE001
        pass
    return None


_ESCALAS = _cargar_escalas_ids()


def _listar_py() -> List[Path]:
    out = []
    for f in sorted(_DIR.glob("*.py")):
        if f.name == "__init__.py" or f.name.startswith("_"):
            continue
        out.append(f)
    return out


def _a_fraction(x: Any) -> Optional[Fraction]:
    if x is None or es_undefined(x):
        return None
    if isinstance(x, Fraction):
        return x
    if isinstance(x, (int, float)):
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


def _centinela_resultado(
    salida: Dict[str, Any],
    peticion: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Centinela interno: ningun calculo sale sin validacion.
    Verifica tipos, rango, presencia de claves y trazabilidad minima.
    """
    problemas: List[str] = []
    advertencias: List[str] = []

    for factor in _FACTORES_CANONICOS:
        if factor not in salida:
            problemas.append("falta clave de factor '{0}'".format(factor))
            continue
        val = salida[factor]
        if val is None or es_undefined(val):
            continue
        if not isinstance(val, Fraction):
            problemas.append(
                "factor '{0}' no es Fraction (tipo={1})".format(
                    factor, type(val).__name__
                )
            )
            continue
        if val < Fraction(0) or val > Fraction(1):
            problemas.append(
                "factor '{0}' fuera de [0,1]: {1}".format(factor, val)
            )

    if salida.get("K") is None and not (
        peticion.get("contexto")
        or peticion.get("O_context")
        or peticion.get("o_context")
    ):
        advertencias.append("K=None legítimo: sin contexto/O (Def-5.3.1)")

    if es_undefined(salida.get("L")):
        advertencias.append("L=UNDEFINED: p=0 o base_nula (AM-D6/AM-A3)")

    return {
        "ok": not problemas,
        "problemas": problemas,
        "advertencias": advertencias,
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
    """Centinela de carpeta e integridad del dominio CA."""
    errores: List[Dict[str, str]] = list(_ERRORES_CARGA)
    choques: List[str] = []
    archivos = [p.name for p in _listar_py()]

    factores_ok = sorted(_APIS.keys())
    for factor in _FACTORES_CANONICOS:
        if factor not in _APIS:
            errores.append({
                "archivo": "?",
                "error": "factor canonico '{0}' sin API publica cargada".format(
                    factor
                ),
            })

    por_factor: Dict[str, List[str]] = {}
    for stem, factor in _ARCHIVO_FACTOR.items():
        path = _DIR / "{0}.py".format(stem)
        if path.exists():
            por_factor.setdefault(factor, []).append(stem)
    for factor, stems in por_factor.items():
        if len(stems) > 1:
            choques.append(
                "factor '{0}' reclamado por varios archivos: {1}".format(
                    factor, stems
                )
            )

    stems_conocidos = set(_ARCHIVO_FACTOR.keys()) | {"conteos", "escalas_ids"}
    extra = [p.stem for p in _listar_py() if p.stem not in stems_conocidos]

    limpio = not errores and not choques
    return {
        "contenedor": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "coherente": limpio,
        "errores": errores,
        "choques": choques,
        "archivos": archivos,
        "factores_api": factores_ok,
        "archivos_extra": extra,
        "conteos_disponible": _CONTEOS is not None,
        "escalas_ids_disponible": _ESCALAS is not None,
        "ids_escala": leer_ids_escala(),
    }


def representar(
    valor: Any,
    precision: int = PRECISION_DECIMAL_DEFAULT,
) -> Dict[str, Any]:
    """
    Representacion decimal de un Fraction.
    Nunca modifica el valor oficial (Fraction).
    """
    if es_undefined(valor):
        return {
            "fraccion": None,
            "decimal": None,
            "precision": precision,
            "undefined": True,
        }
    if valor is None:
        return {
            "fraccion": None,
            "decimal": None,
            "precision": precision,
            "undefined": False,
        }
    fr = _a_fraction(valor)
    if fr is None:
        return {
            "fraccion": None,
            "decimal": None,
            "precision": precision,
            "undefined": False,
            "error": "no convertible a Fraction",
        }
    prec = max(0, int(precision))
    dec = format(float(fr), ".{0}f".format(prec))
    return {
        "fraccion": str(fr),
        "decimal": dec,
        "precision": prec,
        "undefined": False,
    }


def calcular_C(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    peticion = dict(peticion or {})
    metodo = str(peticion.get("metodo") or "operacional")
    if metodo == "operacional":
        peticion = _asegurar_conteos(peticion)

    fn = _APIS.get("C")
    if not callable(fn):
        return {"C": None, "ruta": None, "notas": ["API C no disponible"]}

    try:
        # Compatibilidad: algunas APIs aceptan kwargs, otras dict
        try:
            raw = fn(peticion) if _acepta_dict(fn) else fn(
                compromisos=peticion.get("compromisos"),
                contradicciones=peticion.get("contradicciones"),
                metodo=metodo,
            )
        except TypeError:
            raw = fn(peticion)

        if isinstance(raw, dict) and "C" in raw:
            return raw
        if es_undefined(raw):
            return {"C": UNDEFINED, "ruta": metodo, "notas": ["C UNDEFINED"]}
        C = raw if isinstance(raw, Fraction) else _a_fraction(raw)
        return {"C": C, "ruta": metodo, "notas": []}
    except Exception as e:  # noqa: BLE001
        return {"C": None, "ruta": metodo, "notas": ["Error en C: {0}".format(e)]}


def calcular_L(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    peticion = dict(peticion or {})
    metodo = str(peticion.get("metodo") or "operacional")
    if metodo == "operacional":
        peticion = _asegurar_conteos(peticion)

    fn = _APIS.get("L")
    if not callable(fn):
        return {
            "L": None,
            "p": None,
            "r": None,
            "ruta": None,
            "notas": ["API L no disponible"],
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

        if isinstance(raw, dict) and "L" in raw:
            return raw
        if es_undefined(raw):
            return {
                "L": UNDEFINED,
                "p": peticion.get("p"),
                "r": peticion.get("reversiones"),
                "ruta": metodo,
                "notas": ["L=UNDEFINED (AM-D6)"],
            }
        L = raw if isinstance(raw, Fraction) else _a_fraction(raw)
        return {"L": L, "ruta": metodo, "notas": []}
    except Exception as e:  # noqa: BLE001
        return {
            "L": None,
            "ruta": metodo,
            "notas": ["Error en L: {0}".format(e)],
        }


def calcular_K(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    peticion = dict(peticion or {})
    metodo = str(peticion.get("metodo") or "operacional")
    o_ctx = (
        peticion.get("contexto")
        or peticion.get("O_context")
        or peticion.get("o_context")
    )
    if o_ctx is None:
        return {
            "K": None,
            "ruta": metodo,
            "notas": ["K=None sin contexto/O (Def-5.3.1)"],
        }

    if metodo == "operacional":
        peticion = _asegurar_conteos(peticion)

    fn = _APIS.get("K")
    if not callable(fn):
        return {"K": None, "ruta": None, "notas": ["API K no disponible"]}

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

        if isinstance(raw, dict) and "K" in raw:
            return raw
        if es_undefined(raw):
            return {"K": UNDEFINED, "ruta": metodo, "notas": ["K UNDEFINED"]}
        K = raw if isinstance(raw, Fraction) else _a_fraction(raw)
        return {"K": K, "ruta": metodo, "notas": []}
    except Exception as e:  # noqa: BLE001
        return {"K": None, "ruta": metodo, "notas": ["Error en K: {0}".format(e)]}


def _acepta_dict(fn: Any) -> bool:
    """Heuristica: logica.py usa calcular_l(peticion: dict)."""
    try:
        import inspect
        sig = inspect.signature(fn)
        params = list(sig.parameters.values())
        if len(params) == 1:
            return True
        if params and params[0].name in ("peticion", "request", "payload"):
            return True
    except Exception:  # noqa: BLE001
        pass
    return False


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
    Oficio principal: orquesta C, L, K y pasa por centinela interno.
    Flujo: peticion -> conteos si faltan -> C/L/K -> centinela -> salida.
    """
    peticion = dict(peticion or {})
    metodo = str(peticion.get("metodo") or "operacional")
    errores: List[str] = []
    meta_conteos = None

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

    out_c = calcular_C(peticion)
    out_l = calcular_L(peticion)
    out_k = calcular_K(peticion)

    C = out_c.get("C")
    L = out_l.get("L")
    K = out_k.get("K")

    for bloque in (out_c, out_l, out_k):
        for n in bloque.get("notas") or []:
            if "Error" in str(n) or "no disponible" in str(n):
                errores.append(str(n))

    salida: Dict[str, Any] = {
        "C": C,
        "L": L,
        "K": K,
        "errores": errores,
        "metodo": metodo,
        "C_repr": representar(C),
        "L_repr": representar(L),
        "K_repr": representar(K),
    }
    if meta_conteos is not None:
        salida["conteos"] = meta_conteos
    if escala_meta is not None:
        salida["escala"] = escala_meta

    cent = _centinela_resultado(salida, peticion)
    salida["centinela"] = cent
    if not cent["ok"]:
        salida["errores"] = list(salida.get("errores") or []) + list(
            cent["problemas"]
        )

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


def verificar_salida(salida: Any) -> bool:
    if not isinstance(salida, dict):
        return False
    return all(k in salida for k in ("C", "L", "K"))


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
        "factores_api": b.get("factores_api"),
        "conteos_disponible": b.get("conteos_disponible"),
        "escalas_ids_disponible": b.get("escalas_ids_disponible"),
        "ids_escala": b.get("ids_escala"),
        "coherente": b.get("coherente"),
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "invariantes": CONTENEDOR.get("invariantes"),
        "precision_decimal_default": PRECISION_DECIMAL_DEFAULT,
        "funcion": (
            "Calcula C, L, K. No calcula Tru (FO). "
            "K ausente sin contexto/O (Def-5.3.1). "
            "L=UNDEFINED si p=0 (AM-D6). "
            "Valor oficial = Fraction; decimal solo representacion."
        ),
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
        "conteos_disponible": b.get("conteos_disponible"),
        "errores_n": len(b.get("errores") or []),
        "choques_n": len(b.get("choques") or []),
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "autoridad": CONTENEDOR.get("autoridad"),
        "conocimiento_exportable": CONTENEDOR.get("conocimiento_exportable"),
        "consultas_soportadas": CONTENEDOR.get("consultas_soportadas"),
    }


def diagnostico() -> Dict[str, Any]:
    b = barrer()
    problemas: List[Dict[str, Any]] = []
    advertencias: List[str] = []
    recomendaciones: List[str] = []

    if b.get("errores"):
        problemas.append({"tipo": "errores_carga", "detalle": b["errores"]})
        recomendaciones.append("Revisar APIs C/L/K y archivos del modulo")
    if b.get("choques"):
        problemas.append({"tipo": "choques_factor", "detalle": b["choques"]})
        recomendaciones.append("Resolver stems que reclaman el mismo factor")
    if not b.get("conteos_disponible"):
        advertencias.append("conteos.py no disponible: ruta operacional limitada")
    if not b.get("factores_api"):
        problemas.append({
            "tipo": "sin_apis",
            "detalle": "ningun factor C/L/K cargado",
        })
        recomendaciones.append("Verificar coherencia.py, logica.py, correlacion_k.py")

    estado = ESTADO_OPERATIVO if b.get("coherente") else ESTADO_DEGRADADO
    if not b.get("factores_api") and not problemas:
        estado = ESTADO_NO_INICIADO

    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "estado": estado,
        "problemas": problemas,
        "advertencias": advertencias,
        "recomendaciones": recomendaciones,
        "coherente": b.get("coherente"),
        "factores_api": b.get("factores_api"),
        "errores_n": len(b.get("errores") or []),
        "choques_n": len(b.get("choques") or []),
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
    "barrer": barrer,
    "inventario": inventario,
    "reporte": reporte,
    "diagnostico": diagnostico,
    "leer_ids_escala": leer_ids_escala,
    "verificar_salida": verificar_salida,
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

# Exponer oficio de conteos si existe
if _CONTEOS is not None:
    CONTENEDOR["capacidades"]["extraer_conteos"] = _CONTEOS["extraer_conteos"]
    CONTENEDOR["capacidades"]["inyectar_conteos"] = _CONTEOS["inyectar_en_peticion"]
    # Nota: capacidades dinamicas post-resolucion solo si Engine tolera;
    # si strict exige meta 1:1 al arranque, estas deben declararse en contrato.
    # Por ahora se anexan solo si conteos cargo, sin romper meta de las fijas.

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
    "DominioError",
    "MetodoError",
    "ContratoInvalido",
    "calcular",
    "calcular_C",
    "calcular_L",
    "calcular_K",
    "calcular_factor",
    "representar",
    "barrer",
    "inventario",
    "reporte",
    "diagnostico",
    "leer_ids_escala",
    "verificar_salida",
]

# ===============================================================
# FIN EXPORTACIONES
# ===============================================================


# ===============================================================
# EXTENSIONES FUTURAS
# ===============================================================
#
# Factores nuevos: archivo + API + capacidades + capacidades_meta + _CAP_MAP.
# Valor oficial siempre Fraction. Decimal solo via representar().
#
# ===============================================================
# FIN EXTENSIONES FUTURAS
# ===============================================================


# ===============================================================
# FIN DEL MÓDULO
# ===============================================================
