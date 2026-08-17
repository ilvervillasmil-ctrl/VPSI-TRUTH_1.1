# ===============================================================
# VPSI-TRUTH — modules/catalogo_citaciones/__init__.py
# ===============================================================
#
# MÓDULO:              catalogo_citaciones
# ID:                  CC
# Rol:                 CC
# Versión módulo:      2.1
# Versión contrato:    1.0
# Esquema contrato:    VPSI-CONTRACT-1.0
# Estabilidad:         ESTABLE
# Compatible desde:    1.0
# API Engine:          >=1.0
#
# Glosario de IDs del repositorio.
# Lee categorias/*.py. No calcula. No orquesta.
#
# Capacidades arquitectónicas (callables reales):
#   ejecutar_total, inspeccionar, registrar_inventario
#
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
from typing import Any, Dict, List, Optional, Tuple

# ===============================================================
# FIN 1.1
# ===============================================================


# ===============================================================
# 1.2 — IDENTIDAD
# ===============================================================

ID_MODULO = "CC"
NOMBRE_MODULO = "catalogo_citaciones"
ROL_MODULO = "CC"

# ===============================================================
# FIN 1.2
# ===============================================================


# ===============================================================
# 1.3 — VERSIONES Y ESTABILIDAD
# ===============================================================

VERSION_MODULO = "2.1"
VERSION_CONTRATO = "1.0"
ESQUEMA_CONTRATO = "VPSI-CONTRACT-1.0"
COMPATIBLE_DESDE = "1.0"
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
    "el id del módulo nunca cambia",
    "el rol nunca cambia",
    "las capacidades declaradas son siempre callables tras la resolución",
    "este módulo no modifica el estado de otros módulos",
    "este módulo no calcula Tru / C / L / K",
    "este módulo no orquesta el ciclo",
    "este módulo no envía reportes a otros módulos",
    "los IDs viven en categorias/, no en este INIT",
    "este módulo no inventa capacidades no declaradas en CONTENEDOR",
)

# ===============================================================
# FIN 1.5
# ===============================================================


# ===============================================================
# 1.6 — ESQUEMA DE CATEGORÍA
# ===============================================================

ESQUEMA_CATEGORIA: Dict[str, Any] = {
    "obligatorios": ["id", "nombre", "unidad", "enunciado"],
    "opcionales": [
        "nivel_fractal",
        "jurisdiccion",
        "requiere",
        "factores_evaluables",
        "agrega_desde",
        "fuente_modulo",
        "senales",
        "anclas",
        "version",
        "notas",
    ],
    "prohibidos": [
        "Tru_Ri", "Tru_total", "tru_ri", "tru_total",
        "C", "L", "K",
        "alpha", "beta", "ALPHA", "BETA", "Fraction",
    ],
    "nota": (
        "Archivos bajo categorias/ declaran CATEGORIA o CATEGORIAS o IDS. "
        "Cada uno aporta uno o más IDs del repositorio. "
        "CC los lee y expone. No calcula. "
        "Este INIT no embebe IDs."
    ),
}

_CAMPOS_OBLIGATORIOS = tuple(ESQUEMA_CATEGORIA["obligatorios"])
_VALORES_PROHIBIDOS = tuple(ESQUEMA_CATEGORIA["prohibidos"])

# ===============================================================
# FIN 1.6
# ===============================================================


# ===============================================================
# 1.7 — CONFIGURACIÓN
# ===============================================================

_DIR = Path(__file__).parent
_CAT_DIR = _DIR / "categorias"

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
        "Glosario de IDs del repositorio. Rol CC. "
        "Lee y organiza categorias/*.py. Los IDs viven ahí, no en el INIT. "
        "Engine consulta IDs para citar o reportar. "
        "No calcula. No interpreta pedidos. No envía reportes a terceros."
    ),

    # ============================================================
    # 5.3 — PROPÓSITO
    # ============================================================
    "funcion": (
        "Exponer el catálogo de IDs del repositorio, "
        "responder por_id / ids / esquema y reportar coherencia propia."
    ),
    "no_hace": [
        "No calcula Tru_Ri / Tru_total / C / L / K",
        "No aplica α / β",
        "No hace conteos",
        "No clasifica O",
        "No orquesta el ciclo",
        "No envía reportes a otros módulos",
        "No sustituye CIT / CA / FO / AX / CX / MC / RE / TX / CH",
        "No interpreta pedidos",
    ],

    # ============================================================
    # 5.4 — AUTORIDAD
    # ============================================================
    "autoridad": [
        "Declarar los IDs disponibles en el catálogo",
        "Resolver consulta por_id / ids / esquema",
        "Leer y normalizar todos los archivos de categorias/",
        "Reportar estado, inventario y diagnóstico propios",
    ],

    # ============================================================
    # 5.5 — CONOCIMIENTO EXPORTABLE
    # ============================================================
    "conocimiento_exportable": [
        "categorias",
        "ids",
        "por_id",
        "esquema",
        "inventario",
        "reporte",
        "diagnostico",
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
    "requiere": ["*"],

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
        "listar_ids",
        "consultar_por_id",
        "obtener_esquema",
        "obtener_inventario",
        "obtener_reporte",
        "obtener_diagnostico",
        "verificar_coherencia",
        "ejecutar_total",
        "inspeccionar",
        "registrar_inventario",
    ],

    # ============================================================
    # 5.12 — CAPACIDADES
    # ============================================================
    "capacidades": {
        "verificar": "barrer",
        "barrer": "barrer",
        "inventario": "inventario",
        "categorias": "categorias",
        "por_id": "por_id",
        "ids": "ids",
        "esquema": "esquema",
        "reporte": "reporte",
        "diagnostico": "diagnostico",
        "verificar_salida": "verificar_salida",
        "ejecutar_total": "ejecutar_total",
        "inspeccionar": "inspeccionar",
        "registrar_inventario": "registrar_inventario",
    },

    # ============================================================
    # 5.13 — METADATOS DE CAPACIDADES (1:1 OBLIGATORIO)
    # ============================================================
    "capacidades_meta": {
        "verificar": {
            "descripcion": "Alias de barrer. Verifica coherencia del glosario.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con coherente, categorias, ids, errores",
            "acceso_archivos": ["*"],
        },
        "barrer": {
            "descripcion": (
                "Evalúa coherencia del glosario de IDs. No calcula."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con coherente, categorias, ids, errores, esquema"
            ),
            "acceso_archivos": ["*"],
        },
        "inventario": {
            "descripcion": "Inventario completo del módulo y de los IDs.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con id, version, categorias, ids, total, errores"
            ),
            "acceso_archivos": ["*"],
        },
        "categorias": {
            "descripcion": (
                "Lista del catálogo si coherente; si no, lista vacía."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "list[dict] de categorías normalizadas",
            "acceso_archivos": ["*"],
        },
        "por_id": {
            "descripcion": (
                "Devuelve la categoría normalizada de un id, o None."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict | None",
            "acceso_archivos": ["*"],
        },
        "ids": {
            "descripcion": "Lista de todos los ids del catálogo coherente.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "list[str]",
            "acceso_archivos": ["*"],
        },
        "esquema": {
            "descripcion": (
                "Esquema de forma de una categoría "
                "(obligatorios, opcionales, prohibidos)."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict ESQUEMA_CATEGORIA",
            "acceso_archivos": ["*"],
        },
        "reporte": {
            "descripcion": "Reporte interno de estado del módulo CC.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con estado, coherente, categorias, ids, errores"
            ),
            "acceso_archivos": ["*"],
        },
        "diagnostico": {
            "descripcion": (
                "Diagnóstico: qué falta o está mal en el glosario."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con estado, problemas, advertencias, recomendaciones"
            ),
            "acceso_archivos": ["*"],
        },
        "verificar_salida": {
            "descripcion": (
                "Comprueba forma de una salida de barrer: "
                "coherente bool, errores list, ids list, categorias int."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "bool",
            "acceso_archivos": ["*"],
        },
        "ejecutar_total": {
            "descripcion": (
                "Autoridad total de ENGINE sobre CC. "
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
                "Capacidad meta de inspeccion estructural de CC. "
                "Expone constantes, capacidades, catálogo y estado "
                "sin alterar el contrato ni calcular."
            ),
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["acceso_archivos"],
            "salida": "dict con estructura, capacidades y estado del modulo",
            "acceso_archivos": ["acceso_archivos"],
        },
        "registrar_inventario": {
            "descripcion": (
                "Registra el inventario estructural de CC "
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
# 7.1 — CARGA DESDE ARCHIVO
# ===============================================================

def _cargar_desde_archivo(
    archivo: Path,
) -> Tuple[List[Dict[str, Any]], List[str]]:
    errores: List[str] = []
    if archivo.name.startswith("_") or archivo.name == "__init__.py":
        return [], errores

    nombre_mod = "citaciones_cat_{0}".format(archivo.stem)
    spec = importlib.util.spec_from_file_location(nombre_mod, str(archivo))
    if spec is None or spec.loader is None:
        return [], ["{0}: no se pudo crear spec".format(archivo.name)]

    mod = importlib.util.module_from_spec(spec)
    sys.modules[nombre_mod] = mod
    try:
        spec.loader.exec_module(mod)
    except Exception as e:  # noqa: BLE001
        return [], [
            "{0}: import {1}: {2}".format(
                archivo.name, type(e).__name__, e
            )
        ]

    halladas: List[Dict[str, Any]] = []
    una = getattr(mod, "CATEGORIA", None)
    if isinstance(una, dict):
        halladas.append(una)

    varias = getattr(mod, "CATEGORIAS", None)
    if isinstance(varias, list):
        for item in varias:
            if isinstance(item, dict):
                halladas.append(item)

    raw_ids = getattr(mod, "IDS", None)
    if isinstance(raw_ids, list):
        for item in raw_ids:
            if isinstance(item, str) and item.strip():
                halladas.append({
                    "id": item.strip().lower(),
                    "nombre": item.strip(),
                    "unidad": "id",
                    "enunciado": "ID del repositorio: {0}".format(
                        item.strip()
                    ),
                })
            elif isinstance(item, dict) and item.get("id"):
                halladas.append(item)

    if not halladas:
        errores.append(
            "{0}: sin CATEGORIA/CATEGORIAS/IDS exportada".format(
                archivo.name
            )
        )
    return halladas, errores

# ===============================================================
# FIN 7.1
# ===============================================================


# ===============================================================
# 7.2 — VALIDAR CATEGORÍA
# ===============================================================

def _validar_categoria(cat: Dict[str, Any], origen: str) -> List[str]:
    errs: List[str] = []
    if not isinstance(cat, dict):
        return ["{0}: CATEGORIA no es dict".format(origen)]
    for k in _CAMPOS_OBLIGATORIOS:
        if k not in cat or not str(cat.get(k, "")).strip():
            errs.append(
                "{0}: falta campo obligatorio '{1}'".format(origen, k)
            )
    for prohibido in _VALORES_PROHIBIDOS:
        if prohibido in cat and cat[prohibido] is not None:
            errs.append(
                "{0}: campo prohibido '{1}' "
                "(oficio ajeno; CC solo organiza IDs)".format(
                    origen, prohibido
                )
            )
    return errs

# ===============================================================
# FIN 7.2
# ===============================================================


# ===============================================================
# 7.3 — NORMALIZAR
# ===============================================================

def _normalizar(cat: Dict[str, Any], origen: str) -> Dict[str, Any]:
    nivel = cat.get("nivel_fractal")
    try:
        nivel_n = int(nivel) if nivel is not None else None
    except (TypeError, ValueError):
        nivel_n = None
    juris = cat.get("jurisdiccion")
    fuente = cat.get("fuente_modulo")
    return {
        "id": str(cat["id"]).strip().lower(),
        "nombre": str(cat["nombre"]).strip(),
        "unidad": str(cat["unidad"]).strip(),
        "enunciado": str(cat["enunciado"]).strip(),
        "nivel_fractal": nivel_n,
        "jurisdiccion": str(juris).strip() if juris else None,
        "requiere": [str(x) for x in (cat.get("requiere") or [])],
        "factores_evaluables": [
            str(x) for x in (cat.get("factores_evaluables") or [])
        ],
        "agrega_desde": [
            str(x) for x in (cat.get("agrega_desde") or [])
        ],
        "fuente_modulo": str(fuente).strip() if fuente else None,
        "senales": [
            str(x).lower() for x in (cat.get("senales") or [])
        ],
        "anclas": [str(x) for x in (cat.get("anclas") or [])],
        "origen": origen,
        "version": str(cat.get("version") or "1.0"),
        "notas": str(cat.get("notas") or ""),
    }

# ===============================================================
# FIN 7.3
# ===============================================================


# ===============================================================
# 7.4 — RECOLECTAR
# ===============================================================

def recolectar() -> Tuple[List[Dict[str, Any]], List[Dict[str, str]]]:
    cats: List[Dict[str, Any]] = []
    errores: List[Dict[str, str]] = []
    archivos: List[Path] = []

    if _CAT_DIR.is_dir():
        archivos.extend(sorted(_CAT_DIR.glob("*.py")))
    archivos.extend(sorted(_DIR.glob("*.py")))

    vistos = set()
    for archivo in archivos:
        if archivo.name == "__init__.py" or archivo.name.startswith("_"):
            continue
        key = str(archivo.resolve())
        if key in vistos:
            continue
        vistos.add(key)

        halladas, errs = _cargar_desde_archivo(archivo)
        for e in errs:
            errores.append({"archivo": archivo.name, "error": e})
        for raw in halladas:
            ve = _validar_categoria(raw, archivo.name)
            if ve:
                for e in ve:
                    errores.append({"archivo": archivo.name, "error": e})
                continue
            try:
                cats.append(_normalizar(raw, archivo.stem))
            except Exception as e:  # noqa: BLE001
                errores.append({
                    "archivo": archivo.name,
                    "error": "normalizar: {0}: {1}".format(
                        type(e).__name__, e
                    ),
                })

    por_id_map: Dict[str, List[str]] = {}
    for c in cats:
        por_id_map.setdefault(c["id"], []).append(c["origen"])
    for cid, origenes in por_id_map.items():
        if len(origenes) > 1:
            errores.append({
                "archivo": ",".join(origenes),
                "error": "id duplicado '{0}' en {1}".format(cid, origenes),
            })

    cats.sort(
        key=lambda c: (
            c["nivel_fractal"] is None,
            c["nivel_fractal"] or 0,
            c["id"],
        )
    )
    return cats, errores

# ===============================================================
# FIN 7.4
# ===============================================================


# ===============================================================
# 7.5 — VALIDAR CONTRATO
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
    if str(cont.get("version_contrato")) != VERSION_CONTRATO:
        raise ContratoInvalido(
            "{0}: version_contrato inválida: {1}".format(
                NOMBRE_MODULO, cont.get("version_contrato")
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
# FIN 7.5
# ===============================================================

# ===============================================================
# FIN PARTE 7
# ===============================================================


# ===============================================================
# PARTE 8 — CAPACIDADES PÚBLICAS
# ===============================================================

# ===============================================================
# 8.1 — BARRER
# ===============================================================

def barrer() -> Dict[str, Any]:
    cats, errores = recolectar()
    notas: List[str] = []
    if not cats and not errores:
        notas.append(
            "glosario vacío (legítimo hasta montar archivos en categorias/)"
        )
    return {
        "contenedor": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "coherente": not errores,
        "categorias": len(cats),
        "ids": [c["id"] for c in cats],
        "errores": errores,
        "notas": notas,
        "version": VERSION_MODULO,
        "esquema": ESQUEMA_CATEGORIA,
    }

# ===============================================================
# FIN 8.1
# ===============================================================


# ===============================================================
# 8.2 — VERIFICAR
# ===============================================================

def verificar() -> Dict[str, Any]:
    """Alias contractual real de barrer."""
    return barrer()

# ===============================================================
# FIN 8.2
# ===============================================================


# ===============================================================
# 8.3 — CATEGORIAS
# ===============================================================

def categorias() -> List[Dict[str, Any]]:
    r = barrer()
    if not r.get("coherente", False):
        return []
    cats, _ = recolectar()
    return cats

# ===============================================================
# FIN 8.3
# ===============================================================


# ===============================================================
# 8.4 — POR ID
# ===============================================================

def por_id(cat_id: str) -> Optional[Dict[str, Any]]:
    key = str(cat_id or "").strip().lower()
    for c in categorias():
        if c["id"] == key:
            return dict(c)
    return None

# ===============================================================
# FIN 8.4
# ===============================================================


# ===============================================================
# 8.5 — IDS
# ===============================================================

def ids() -> List[str]:
    return [c["id"] for c in categorias()]

# ===============================================================
# FIN 8.5
# ===============================================================


# ===============================================================
# 8.6 — ESQUEMA
# ===============================================================

def esquema() -> Dict[str, Any]:
    return dict(ESQUEMA_CATEGORIA)

# ===============================================================
# FIN 8.6
# ===============================================================


# ===============================================================
# 8.7 — INVENTARIO
# ===============================================================

def inventario(peticion: Any = None) -> Dict[str, Any]:
    cats, errores = recolectar()
    return {
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "funcion": (
            "Glosario de IDs del repositorio. "
            "Expone ids a Engine para citar/reportar. No calcula."
        ),
        "uso": [
            "consulta de IDs",
            "resolución por id",
            "esquema de categorías",
        ],
        "esquema_categoria": ESQUEMA_CATEGORIA,
        "categorias": cats,
        "ids": [c["id"] for c in cats],
        "total": len(cats),
        "errores": errores,
        "coherente": not errores,
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "invariantes": CONTENEDOR.get("invariantes"),
        "extension": (
            "Agregar o editar un archivo en categorias/ actualiza el "
            "glosario sin tocar este INIT."
        ),
    }

# ===============================================================
# FIN 8.7
# ===============================================================


# ===============================================================
# 8.8 — VERIFICAR SALIDA
# ===============================================================

def verificar_salida(salida: Dict[str, Any]) -> bool:
    if not isinstance(salida, dict):
        return False
    if "coherente" not in salida:
        return False
    if not isinstance(salida["coherente"], bool):
        return False
    if "errores" in salida and not isinstance(salida["errores"], list):
        return False
    if "ids" in salida and not isinstance(salida["ids"], list):
        return False
    if "categorias" in salida and not isinstance(
        salida["categorias"], (int, list)
    ):
        return False
    return True

# ===============================================================
# FIN 8.8
# ===============================================================


# ===============================================================
# 8.9 — EJECUTAR TOTAL
# ===============================================================

def ejecutar_total(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Autoridad total de ENGINE sobre CC.
    Ejerce TODAS las unidades operativamente ejecutables del módulo.
    Todo es callable real. No inventa capacidades.
    """
    peticion = dict(peticion or {}) if isinstance(peticion, dict) else {}
    resultados: Dict[str, Any] = {}
    errores_ejecucion: List[str] = []

    try:
        resultados["barrer"] = barrer()
        resultados["verificar"] = resultados["barrer"]
    except Exception as e:
        errores_ejecucion.append("barrer: {0}".format(e))
        resultados["barrer"] = None

    try:
        resultados["inventario"] = inventario(peticion)
    except Exception as e:
        errores_ejecucion.append("inventario: {0}".format(e))
        resultados["inventario"] = None

    try:
        resultados["categorias"] = categorias()
    except Exception as e:
        errores_ejecucion.append("categorias: {0}".format(e))
        resultados["categorias"] = None

    try:
        resultados["ids"] = ids()
    except Exception as e:
        errores_ejecucion.append("ids: {0}".format(e))
        resultados["ids"] = None

    try:
        resultados["esquema"] = esquema()
    except Exception as e:
        errores_ejecucion.append("esquema: {0}".format(e))
        resultados["esquema"] = None

    try:
        resultados["reporte"] = reporte()
    except Exception as e:
        errores_ejecucion.append("reporte: {0}".format(e))
        resultados["reporte"] = None

    try:
        resultados["diagnostico"] = diagnostico()
    except Exception as e:
        errores_ejecucion.append("diagnostico: {0}".format(e))
        resultados["diagnostico"] = None

    try:
        resultados["inspeccionar"] = inspeccionar(peticion)
    except Exception as e:
        errores_ejecucion.append("inspeccionar: {0}".format(e))
        resultados["inspeccionar"] = None

    try:
        resultados["registrar_inventario"] = registrar_inventario(peticion)
    except Exception as e:
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
            "ejecutar_total ejerce autoridad total de ENGINE sobre CC. "
            "Todas las unidades son callables reales. "
            "No inventa capacidades ni altera el contrato."
        ),
    }

# ===============================================================
# FIN 8.9
# ===============================================================


# ===============================================================
# 8.10 — INSPECCIONAR
# ===============================================================

def inspeccionar(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Inspección estructural de CC.
    Expone contrato, catálogo y estado sin calcular.
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
        },
        "capacidades_contractuales": list(
            CONTENEDOR.get("capacidades", {}).keys()
        ),
        "capacidades_meta": list(
            CONTENEDOR.get("capacidades_meta", {}).keys()
        ),
        "integridad": {
            "coherente": res_barrer.get("coherente"),
            "categorias": res_barrer.get("categorias"),
            "ids": res_barrer.get("ids"),
            "errores": res_barrer.get("errores"),
        },
        "esquema_categoria": ESQUEMA_CATEGORIA,
        "autoriza_engine": CONTENEDOR.get("autoriza_engine"),
        "reporting": CONTENEDOR.get("reporting"),
        "invariantes": list(INVARIANTES),
        "nota": (
            "inspeccionar expone estructura de CC sin calcular "
            "ni alterar el contrato."
        ),
    }

# ===============================================================
# FIN 8.10
# ===============================================================


# ===============================================================
# 8.11 — REGISTRAR INVENTARIO
# ===============================================================

def registrar_inventario(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Registra el inventario estructural de CC como instantánea determinista.
    No altera evidencia.
    """
    inv = inventario(peticion)
    return {
        "id": ID_MODULO,
        "operacion": "registrar_inventario",
        "registrado": True,
        "inventario": inv,
        "nota": (
            "Instantánea determinista del inventario de CC. "
            "No modifica el glosario ni evidencia."
        ),
    }

# ===============================================================
# FIN 8.11
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
    r = barrer()
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "estado": (
            ESTADO_OPERATIVO if r.get("coherente") else ESTADO_DEGRADADO
        ),
        "coherente": r.get("coherente"),
        "categorias": r.get("categorias"),
        "ids": r.get("ids"),
        "errores": r.get("errores"),
        "notas": r.get("notas"),
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "autoridad": CONTENEDOR.get("autoridad"),
        "conocimiento_exportable": CONTENEDOR.get(
            "conocimiento_exportable"
        ),
        "consultas_soportadas": CONTENEDOR.get("consultas_soportadas"),
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
    r = barrer()
    problemas: List[Dict[str, Any]] = []
    advertencias: List[str] = []
    recomendaciones: List[str] = []

    if r.get("errores"):
        problemas.append({
            "tipo": "errores_catalogo",
            "detalle": r["errores"],
        })
        recomendaciones.append(
            "Corregir archivos de categorias/ con errores de forma o carga"
        )

    if not r.get("categorias"):
        advertencias.append(
            "Glosario vacío (legítimo hasta montar categorias/)"
        )

    estado = ESTADO_OPERATIVO if r.get("coherente") else ESTADO_DEGRADADO
    if not r.get("categorias") and not problemas:
        estado = ESTADO_NO_INICIADO

    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "estado": estado,
        "problemas": problemas,
        "advertencias": advertencias,
        "recomendaciones": recomendaciones,
        "coherente": r.get("coherente"),
        "errores_n": len(r.get("errores") or []),
        "categorias_n": r.get("categorias") or 0,
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
    "barrer": barrer,
    "verificar": verificar,
    "inventario": inventario,
    "categorias": categorias,
    "por_id": por_id,
    "ids": ids,
    "esquema": esquema,
    "reporte": reporte,
    "diagnostico": diagnostico,
    "verificar_salida": verificar_salida,
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
                    "{0}: capacidad '{1}' referencia inexistente: '{2}'".format(
                        NOMBRE_MODULO, nombre, ref
                    )
                )
            fn = _CAP_MAP[ref]
            if not callable(fn):
                raise ContratoInvalido(
                    "{0}: '{1}' no es callable".format(NOMBRE_MODULO, ref)
                )
            resueltas[nombre] = fn
            continue
        raise ContratoInvalido(
            "{0}: capacidad '{1}' tiene tipo inválido: {2}".format(
                NOMBRE_MODULO, nombre, type(ref).__name__
            )
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
    "ESQUEMA_CATEGORIA",
    "recolectar",
    "barrer",
    "verificar",
    "categorias",
    "por_id",
    "ids",
    "esquema",
    "inventario",
    "verificar_salida",
    "reporte",
    "diagnostico",
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
