# ===============================================================
# VPSI-TRUTH — modules/tru_totales/__init__.py
# ===============================================================
#
# MÓDULO:              tru_totales
# ID:                  TT
# Rol:                 TT
# Versión módulo:      2.0
# Versión contrato:    1.0
# Esquema contrato:    VPSI-CONTRACT-1.0
# Estabilidad:         ESTABLE
# Compatible desde:    1.0
# API Engine:          >=1.0
#
# Función:
#   Catálogo pasivo de categorías de alcance de Tru_Ri / Tru_total.
#   Expone qué escalas existen, su unidad y qué material requieren.
#
# Qué hace:
#   - Descubre y normaliza categorias/*.py
#   - Expone el catálogo ordenado de escalas evaluables
#   - Resuelve un pedido de Omega/Engine a una categoría del catálogo
#   - Reporta coherencia, inventario y diagnóstico propios
#
# Qué NO hace:
#   - No calcula Tru_Ri ni Tru_total (eso es Calculator / FO)
#   - No calcula C, L, K
#   - No orquesta el ciclo (eso es Engine)
#   - No fija el contexto O (eso es CX)
#   - No cuenta material (eso es conteos)
#
# Responsabilidad:
#   Ser el catálogo pasivo de alcances. Cero voluntad. Cero aritmética.
#
# Autoridad:
#   - Declarar las categorías disponibles
#   - Resolver un pedido a una categoría del catálogo
#   - Reportar estado, inventario y diagnóstico propios
#
# Conocimiento exportable:
#   categorias, ids, resolver_pedido, inventario, reporte, diagnostico
#
# Relación con Engine:
#   Engine descubre este CONTENEDOR, consulta el catálogo,
#   resuelve el pedido y orquesta conteos + Calculator.
#   Este módulo no calcula ni orquesta.
#
# Relación con Omega:
#   Omega declara qué total quiere ver.
#   Engine le entrega el resultado. Omega solo presenta.
#   Este módulo no habla con Omega directamente.
#
# ===============================================================


# ===============================================================
# IMPORTACIONES
# ===============================================================

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ===============================================================
# FIN IMPORTACIONES
# ===============================================================


# ===============================================================
# CONSTANTES
# ===============================================================

ID_MODULO = "TT"
NOMBRE_MODULO = "tru_totales"
ROL_MODULO = "TT"

VERSION_MODULO = "2.0"
VERSION_CONTRATO = "1.0"
ESQUEMA_CONTRATO = "VPSI-CONTRACT-1.0"

COMPATIBLE_DESDE = "1.0"
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
    "el id del módulo nunca cambia",
    "el rol nunca cambia",
    "las capacidades declaradas son siempre callables tras la resolución",
    "este módulo no modifica el estado de otros módulos",
    "este módulo no calcula Tru_Ri ni Tru_total",
    "este módulo no orquesta el ciclo",
    "este módulo no inventa capacidades no declaradas en CONTENEDOR",
)

_CAMPOS_OBLIGATORIOS = (
    "id",
    "nombre",
    "unidad",
    "enunciado",
)

# ===============================================================
# FIN CONSTANTES
# ===============================================================


# ===============================================================
# CONFIGURACIÓN
# ===============================================================

_DIR = Path(__file__).parent
_CAT_DIR = _DIR / "categorias"

# ===============================================================
# FIN CONFIGURACIÓN
# ===============================================================


# ===============================================================
# DEFINICIONES
# ===============================================================

class ContratoInvalido(Exception):
    """El CONTENEDOR no cumple el esquema o la resolución falló."""
    pass


# ===============================================================
# FIN DEFINICIONES
# ===============================================================


# ===============================================================
# CONTRATO OFICIAL DEL MÓDULO
# ===============================================================

CONTENEDOR: Dict[str, Any] = {
    # ----- ESQUEMA -----
    "esquema": ESQUEMA_CONTRATO,
    "version_contrato": VERSION_CONTRATO,
    "version_modulo": VERSION_MODULO,
    "estabilidad": ESTABILIDAD,
    "compatible_desde": COMPATIBLE_DESDE,
    "api_engine": API_ENGINE,

    # ----- IDENTIDAD -----
    "id": ID_MODULO,
    "nombre": NOMBRE_MODULO,
    "rol": ROL_MODULO,
    "descripcion": (
        "Catálogo pasivo de categorías de alcance de Tru_Ri / Tru_total. "
        "Declara qué escalas existen, su unidad y el material que requieren. "
        "No calcula. No orquesta."
    ),

    # ----- PROPÓSITO -----
    "funcion": (
        "Exponer el catálogo ordenado de categorías evaluables, "
        "resolver un pedido a una categoría y reportar coherencia propia."
    ),
    "no_hace": [
        "No calcula Tru_Ri ni Tru_total",
        "No calcula C, L, K",
        "No orquesta el ciclo (eso es Engine)",
        "No fija el contexto O (eso es CX)",
        "No cuenta material (eso es conteos)",
        "No modifica otros módulos",
    ],

    # ----- AUTORIDAD -----
    "autoridad": [
        "Declarar las categorías disponibles en el catálogo",
        "Resolver un pedido de Omega/Engine a una categoría",
        "Leer y normalizar todos los archivos de categorias/",
        "Reportar estado, inventario y diagnóstico propios",
    ],

    # ----- CONOCIMIENTO EXPORTABLE -----
    "conocimiento_exportable": [
        "categorias",
        "ids",
        "resolver_pedido",
        "inventario",
        "reporte",
        "diagnostico",
        "capacidades",
    ],

    # ============================================================
    # ACCESO (obligatorio en el esquema)
    # ============================================================
    "acceso": {
        "nivel": "completo",
        "descripcion": "Acceso total a recursos del módulo"
    },
    
    # ============================================================
    # DEPENDENCIAS
    # ============================================================
    "requiere": [
    "CE", "AX", "FO", "MC", "SF",
    "CA", "CX", "DI", "RE", "VX",
    "TX", "CH", "CIT", "DGCO", "UI",
    "CC", "SC", "CT",
    ],

    # ============================================================
    # ACCESO A ARCHIVOS (AGREGADO — obligatorio en el esquema)
    # ============================================================
    "acceso_archivos": ["*"],

    # ============================================================
    # VALIDAR ESQUEMA A NIVEL MÓDULO (AGREGADO — obligatorio en el esquema)
    # ============================================================
    "validar_esquema": ["*"],

    #============================================================
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
        "validar_esquema": True,          # ← AGREGADO
        "acceso_archivos": True,          # ← AGREGADO

        # --- BANDERAS NUEVAS (OBLIGATORIAS ENGINE) ---
        "ejecutar_total": True,           # ← AGREGADO
        "inspeccionar": True,             # ← AGREGADO
        "registrar_inventario": True,     # ← AGREGADO
        "evaluar_universal": True,
    },
    

    # ============================================================
    # CONSULTAS SOPORTADAS
    # ============================================================
    "consultas_soportadas": [
        # --- CENTINELA ---
        "verificar_coherencia",
        "listar_categorias",

        # --- CATÁLOGO ---
        "resolver_pedido",

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
    # CAPACIDADES
    # ============================================================
    "capacidades": {
        # --- CENTINELA ---
        "verificar": "barrer",
        "barrer": "barrer",
        "verificar_salida": "verificar_salida",

        # --- CATÁLOGO ---
        "categorias": "categorias",
        "capacidades": "capacidades",
        "resolver_pedido": "resolver_pedido",

        # --- INVENTARIO Y REPORTING ---
        "inventario": "inventario",
        "reporte": "reporte",
        "diagnostico": "diagnostico",

        # --- CAPACIDADES ARQUITECTÓNICAS (OBLIGATORIAS ENGINE) ---
        "ejecutar_total": "ejecutar_total",
        "inspeccionar": "inspeccionar",
        "registrar_inventario": "registrar_inventario",
        "evaluar_universal": "evaluar_universal",
    },

    # ============================================================
    # METADATOS DE CAPACIDADES (1:1 OBLIGATORIO)
    # ============================================================
    "capacidades_meta": {
        "verificar": {
            "descripcion": "Alias de barrer. Verifica coherencia del catálogo.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con coherente, categorias, ids, errores",
            "acceso_archivos": ["*"],
        },
        "barrer": {
            "descripcion": "Evalúa coherencia del catálogo. No calcula Tru.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con coherente, categorias, ids, errores, version",
            "acceso_archivos": ["*"],
        },
        "inventario": {
            "descripcion": "Inventario completo del módulo y del catálogo.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con id, version, capacidades, extension",
            "acceso_archivos": ["*"],
        },
        "capacidades": {
            "descripcion": "Vista explícita del catálogo para Engine/Omega.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con categorias resumidas, total, coherente",
            "acceso_archivos": ["*"],
        },
        "categorias": {
            "descripcion": "Lista del catálogo si coherente; si no, lista vacía.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "list[dict] de categorías normalizadas",
            "acceso_archivos": ["*"],
        },
        "resolver_pedido": {
            "descripcion": (
                "Normaliza un pedido de Omega/Engine a una categoría. "
                "No calcula. No orquesta."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con ok, categoria, unidad, factores_evaluables, ...",
            "acceso_archivos": ["*"],
        },
        "reporte": {
            "descripcion": "Reporte interno de estado del módulo TT.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con estado, coherente, categorias, errores",
            "acceso_archivos": ["*"],
        },
        "diagnostico": {
            "descripcion": "Diagnóstico: qué falta o está mal en el catálogo.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con estado, problemas, advertencias, recomendaciones",
            "acceso_archivos": ["*"],
        },
                "verificar_salida": {
            "descripcion": "Comprueba si una salida de barrer o resolver es válida.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "bool",
            "acceso_archivos": ["*"],
        },

        # --- CAPACIDADES ARQUITECTÓNICAS (OBLIGATORIAS ENGINE) ---
        "ejecutar_total": {
            "descripcion": (
                "Autoridad total de ENGINE sobre TT. "
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
                "Capacidad meta de inspeccion estructural de TT. "
                "Expone constantes, capacidades, catalogo y estado "
                "sin alterar el contrato ni calcular."
            ),
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["acceso_archivos"],
            "salida": "dict con estructura, capacidades y estado del modulo",
            "acceso_archivos": ["acceso_archivos"],
        },
        "registrar_inventario": {
            "descripcion": (
                "Registra el inventario estructural de TT "
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
        "acceso_archivos": True,          # ← AGREGADA
        "validar_esquema": True,          # ← AGREGADA

        # --- BANDERAS NUEVAS (OBLIGATORIAS ENGINE) ---
        "ejecutar_total": True,           # ← AGREGADA
        "inspeccionar": True,             # ← AGREGADA
        "registrar_inventario": True,     # ← AGREGADA
        "evaluar_universal": True,
    },


    # ----- ESTADOS VÁLIDOS -----
    "estados_validos": list(ESTADOS_VALIDOS),

    # ----- INVARIANTES -----
    "invariantes": list(INVARIANTES),
}

# ===============================================================
# FIN CONTRATO
# ===============================================================


# ===============================================================
# FUNCIONES PRIVADAS
# ===============================================================

def _cargar_desde_archivo(
    archivo: Path,
) -> Tuple[List[Dict[str, Any]], List[str]]:
    errores: List[str] = []
    if archivo.name.startswith("_") or archivo.name == "__init__.py":
        return [], errores

    nombre_mod = "tru_totales_cat_{0}".format(archivo.stem)
    spec = importlib.util.spec_from_file_location(nombre_mod, archivo)
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
    if not halladas:
        for attr in ("DECLARACION", "declaracion", "TOTAL"):
            val = getattr(mod, attr, None)
            if isinstance(val, dict):
                halladas.append(val)
                break
    if not halladas:
        errores.append(
            "{0}: sin CATEGORIA/CATEGORIAS exportada".format(archivo.name)
        )
    return halladas, errores


def _validar_categoria(cat: Dict[str, Any], origen: str) -> List[str]:
    errs: List[str] = []
    for k in _CAMPOS_OBLIGATORIOS:
        if k not in cat or not str(cat.get(k, "")).strip():
            errs.append(
                "{0}: falta campo obligatorio '{1}'".format(origen, k)
            )

    # Oficio prohibido: traer números de Tru / C / L / K
    for prohibido in (
        "Tru_Ri", "Tru_total", "tru_ri", "tru_total", "C", "L", "K",
    ):
        if prohibido in cat and cat[prohibido] is not None:
            if prohibido in ("C", "L", "K") and isinstance(
                cat.get(prohibido), bool
            ):
                continue
            errs.append(
                "{0}: no debe traer valor '{1}' "
                "(oficio Calculator; tru_totales solo cataloga)".format(
                    origen, prohibido
                )
            )
    return errs


def _normalizar(cat: Dict[str, Any], origen: str) -> Dict[str, Any]:
    factores = cat.get("factores_evaluables") or ["Tru_Ri", "Tru_total"]
    if not isinstance(factores, list):
        factores = ["Tru_Ri", "Tru_total"]

    nivel = cat.get("nivel_fractal")
    try:
        nivel_n = int(nivel) if nivel is not None else None
    except (TypeError, ValueError):
        nivel_n = None

    return {
        "id": str(cat["id"]).strip().lower(),
        "nombre": str(cat["nombre"]).strip(),
        "unidad": str(cat["unidad"]).strip(),
        "enunciado": str(cat["enunciado"]).strip(),
        "nivel_fractal": nivel_n,
        "requiere": [str(x) for x in (cat.get("requiere") or [])],
        "factores_evaluables": [str(x) for x in factores],
        "agrega_desde": [str(x) for x in (cat.get("agrega_desde") or [])],
        "senales": [str(x).lower() for x in (cat.get("senales") or [])],
        "anclas": [str(x) for x in (cat.get("anclas") or [])],
        "origen": origen,
        "version": str(cat.get("version") or "1.0"),
        "notas": str(cat.get("notas") or ""),
    }


def recolectar() -> Tuple[List[Dict[str, Any]], List[Dict[str, str]]]:
    """
    Lee categorias/*.py y *.py no privados en la raíz del módulo.
    Retorna (categorías normalizadas, errores de forma/carga).
    """
    cats: List[Dict[str, Any]] = []
    errores: List[Dict[str, str]] = []
    archivos: List[Path] = []

    if _CAT_DIR.is_dir():
        archivos.extend(sorted(_CAT_DIR.glob("*.py")))
    archivos.extend(sorted(_DIR.glob("*.py")))

    vistos: set = set()
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

    por_id: Dict[str, List[str]] = {}
    for c in cats:
        por_id.setdefault(c["id"], []).append(c["origen"])
    for cid, origenes in por_id.items():
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
# FIN FUNCIONES PRIVADAS
# ===============================================================


# ===============================================================
# CAPACIDADES PÚBLICAS
# ===============================================================

def barrer() -> Dict[str, Any]:
    """Coherencia del catálogo. No calcula Tru."""
    cats, errores = recolectar()
    return {
        "contenedor": NOMBRE_MODULO,
        "coherente": not errores,
        "categorias": len(cats),
        "ids": [c["id"] for c in cats],
        "errores": errores,
        "version": VERSION_MODULO,
        "contrato": (
            "Catálogo pasivo de alcances Tru_Ri/Tru_total. "
            "Engine usa; Calculator calcula; este módulo no calcula."
        ),
    }


def categorias() -> List[Dict[str, Any]]:
    """Lista del catálogo si coherente; si no → []."""
    r = barrer()
    if not r["coherente"]:
        return []
    cats, _ = recolectar()
    return cats


def por_id(cat_id: str) -> Optional[Dict[str, Any]]:
    key = str(cat_id or "").strip().lower()
    for c in categorias():
        if c["id"] == key:
            return dict(c)
    return None


def ids() -> List[str]:
    return [c["id"] for c in categorias()]


def es_valida(cat_id: str) -> bool:
    return str(cat_id or "").strip().lower() in set(ids())


def capacidades() -> Dict[str, Any]:
    """
    Vista explícita para Engine/Omega:
    «Aquí están las categorías; utilícenlas cuando quieran.»
    """
    cats, errores = recolectar()
    return {
        "modulo": NOMBRE_MODULO,
        "version": VERSION_MODULO,
        "mensaje": (
            "Capacidades de categorías de Tru_Ri y Tru_total. "
            "Úsenlas cuando quieran. Este módulo no calcula."
        ),
        "como_usar": (
            "Omega declara el total a mostrar; Engine resuelve la categoría "
            "con resolver_pedido / por_id; CX aporta O; conteos + Calculator "
            "aplican la fórmula sobre el segmento."
        ),
        "categorias": [
            {
                "id": c["id"],
                "nombre": c["nombre"],
                "unidad": c["unidad"],
                "nivel_fractal": c["nivel_fractal"],
                "factores_evaluables": c["factores_evaluables"],
                "requiere": c["requiere"],
            }
            for c in cats
        ],
        "total": len(cats),
        "coherente": not errores,
        "errores": errores,
    }


def inventario(peticion: Any = None) -> Dict[str, Any]:
    caps = capacidades()
    return {
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "funcion": (
            "Catálogo pasivo de categorías de alcance de Tru_Ri / Tru_total. "
            "Auto-carga categorias/*.py. No calcula. No orquesta."
        ),
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "catalogo": caps,
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "invariantes": CONTENEDOR.get("invariantes"),
        "extension": (
            "Editar o agregar un archivo en categorias/ sin tocar este INIT."
        ),
        "formula_referencia": (
            "Tru_Ri = C·L·K ; Tru_total = Tru_Ri·α + β — "
            "las aplica Calculator, no este módulo."
        ),
    }


def resolver_pedido(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Normaliza un pedido de Omega/Engine a una categoría del catálogo.
    No calcula. No orquesta.
    """
    peticion = dict(peticion or {})
    cats, errores = recolectar()
    if errores and not cats:
        return {
            "ok": False,
            "error": "modulo_incoherente",
            "errores": errores,
            "mensajes": [
                "Catálogo incoherente; no hay categorías cargadas."
            ],
        }

    raw_id = (
        peticion.get("escala_id")
        or peticion.get("categoria_tru")
        or peticion.get("categoria")
        or peticion.get("tipo_total")
        or peticion.get("id")
    )

    if raw_id and es_valida(str(raw_id)):
        meta = por_id(str(raw_id)) or {}
        return {
            "ok": True,
            "categoria": meta["id"],
            "nombre": meta.get("nombre"),
            "unidad": meta.get("unidad"),
            "nivel_fractal": meta.get("nivel_fractal"),
            "factores_evaluables": list(
                meta.get("factores_evaluables") or []
            ),
            "requiere": list(meta.get("requiere") or []),
            "agrega_desde": list(meta.get("agrega_desde") or []),
            "anclas": list(meta.get("anclas") or []),
            "sujeto_indice": peticion.get("sujeto_indice"),
            "mensajes": [
                "Categoría '{0}' disponible. "
                "Engine orquesta; Calculator calcula; "
                "tru_totales no calcula.".format(meta["id"])
            ],
        }

    tipos = peticion.get("tipos_total") or peticion.get("categorias")
    if isinstance(tipos, (list, tuple)):
        res = [
            str(t).strip().lower()
            for t in tipos
            if es_valida(str(t))
        ]
        if res:
            return {
                "ok": True,
                "categoria": res[0],
                "categorias": res,
                "multiple": True,
                "mensajes": [
                    "Varias categorías pedidas. Cada una se calcula "
                    "en su segmento/O; sin fusión silenciosa."
                ],
            }

    texto = " ".join(
        str(peticion.get(k) or "")
        for k in ("pedido", "texto", "objetivo", "tarea", "mensaje")
    ).lower()
    for c in cats:
        for s in c.get("senales") or []:
            if s and s in texto:
                return {
                    "ok": True,
                    "categoria": c["id"],
                    "nombre": c.get("nombre"),
                    "unidad": c.get("unidad"),
                    "nivel_fractal": c.get("nivel_fractal"),
                    "factores_evaluables": list(
                        c.get("factores_evaluables") or []
                    ),
                    "requiere": list(c.get("requiere") or []),
                    "agrega_desde": list(c.get("agrega_desde") or []),
                    "anclas": list(c.get("anclas") or []),
                    "mensajes": [
                        "Pedido en prosa → categoría '{0}'.".format(c["id"])
                    ],
                }

    return {
        "ok": False,
        "categoria": None,
        "error": "categoria_no_reconocida",
        "categorias_validas": [c["id"] for c in cats],
        "mensajes": [
            "Categoría no reconocida. Catálogo: {0}.".format(
                ", ".join(c["id"] for c in cats) or "(vacío)"
            )
        ],
    }


def verificar_salida(salida: Dict[str, Any]) -> bool:
    if not isinstance(salida, dict) or salida.get("error"):
        return False
    if "coherente" in salida:
        return bool(salida.get("coherente"))
    cat = salida.get("categoria")
    return bool(cat) and es_valida(str(cat))


def verificar() -> Dict[str, Any]:
    return barrer()

# ===============================================================
# CAPACIDADES ARQUITECTÓNICAS (OBLIGATORIAS ENGINE)
# ===============================================================

def ejecutar_total(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Autoridad total de ENGINE sobre TT.
    Fuente única: CONTENEDOR["capacidades"].
    No inventa. No autoinvoca. Todo callable real.
    """
    peticion_normalizada = (
        dict(peticion) if isinstance(peticion, dict) else {}
    )
    resultados: Dict[str, Any] = {}
    errores_ejecucion: List[str] = []

    capacidades_decl = CONTENEDOR.get("capacidades", {})
    if not isinstance(capacidades_decl, dict):
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

    for nombre in sorted(capacidades_decl):
        if nombre == "ejecutar_total":
            continue
        referencia = capacidades_decl[nombre]
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

            if nombre == "resolver_pedido":
                resultados[nombre] = fn(peticion_normalizada)
            elif nombre == "verificar_salida":
                resultados[nombre] = fn(
                    peticion_normalizada.get("salida")
                    if isinstance(
                        peticion_normalizada.get("salida"), dict
                    )
                    else {}
                )
            elif nombre in ("inventario",):
                resultados[nombre] = fn(peticion_normalizada)
            else:
                resultados[nombre] = fn()
        except Exception as exc:
            errores_ejecucion.append(f"{nombre}: {exc}")
            resultados[nombre] = None

    barrido = resultados.get("barrer")
    coherente = (
        isinstance(barrido, dict) and bool(barrido.get("coherente"))
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
        "capacidades_declaradas": sorted(capacidades_decl.keys()),
    }


def inspeccionar(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Inspección estructural de TT.
    Expone contrato y catálogo sin calcular ni alterar.
    """
    b = barrer()
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
            "CAMPOS_OBLIGATORIOS": list(_CAMPOS_OBLIGATORIOS),
        },
        "capacidades_contractuales": sorted(
            CONTENEDOR.get("capacidades", {}).keys()
        ),
        "capacidades_meta": sorted(
            CONTENEDOR.get("capacidades_meta", {}).keys()
        ),
        "integridad": {
            "coherente": b.get("coherente"),
            "categorias": b.get("categorias"),
            "ids": b.get("ids"),
            "errores": b.get("errores"),
        },
        "autoriza_engine": CONTENEDOR.get("autoriza_engine"),
        "reporting": CONTENEDOR.get("reporting"),
        "invariantes": list(INVARIANTES),
        "nota": (
            "inspeccionar expone estructura de TT sin calcular "
            "ni alterar el contrato ni el catálogo."
        ),
    }


def registrar_inventario(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Instantánea determinista del inventario de TT.
    No altera evidencia ni catálogo.
    """
    inv = inventario(peticion)
    return {
        "id": ID_MODULO,
        "operacion": "registrar_inventario",
        "registrado": True,
        "inventario": inv,
        "nota": (
            "Instantánea determinista del inventario de TT. "
            "No modifica categorías ni evidencia."
        ),
    }

# ===============================================================
# FIN CAPACIDADES ARQUITECTÓNICAS
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
# REPORTING INTERNO
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
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "autoridad": CONTENEDOR.get("autoridad"),
        "conocimiento_exportable": CONTENEDOR.get(
            "conocimiento_exportable"
        ),
        "consultas_soportadas": CONTENEDOR.get("consultas_soportadas"),
    }


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
        advertencias.append("No hay categorías cargadas")
        recomendaciones.append(
            "Agregar al menos un archivo válido en categorias/"
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
# FIN REPORTING
# ===============================================================


# ===============================================================
# PARTE 10 — VALIDACIÓN, RESOLUCIÓN Y EXPORTACIONES
# ===============================================================

# ===============================================================
# 10.1 — MAPA DE CAPACIDADES
# ===============================================================

_CAP_MAP = {
    # --- CENTINELA ---
    "barrer": barrer,
    "verificar": verificar,
    "verificar_salida": verificar_salida,

    # --- CATÁLOGO ---
    "categorias": categorias,
    "capacidades": capacidades,
    "resolver_pedido": resolver_pedido,

    # --- INVENTARIO Y REPORTING ---
    "inventario": inventario,
    "reporte": reporte,
    "diagnostico": diagnostico,

    # --- CAPACIDADES ARQUITECTÓNICAS (OBLIGATORIAS ENGINE) ---
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
            "{0}: capacidad '{1}' tiene tipo inválido: {2}".format(
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
    "recolectar",
    "barrer",
    "verificar",
    "categorias",
    "por_id",
    "ids",
    "es_valida",
    "capacidades",
    "inventario",
    "resolver_pedido",
    "verificar_salida",
    "reporte",
    "diagnostico",
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
