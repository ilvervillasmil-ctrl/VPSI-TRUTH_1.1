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
    "requiere": [
    "CE", "AX", "FO", "MC", "SF",
    "CA", "CX", "DI", "RE", "VX",
    "TX", "CH", "CIT", "DGCO", "UI",
    "TT", "SC",
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
        "evaluar_universal": True,
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
        "evaluar_universal": "evaluar_universal",
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

    if not isinstance(cont, dict):
        raise ContratoInvalido(
            "{0}: CONTENEDOR debe ser dict".format(NOMBRE_MODULO)
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

    for campo in (
        "id", "nombre", "rol", "descripcion",
        "funcion", "estabilidad", "compatible_desde", "api_engine",
    ):
        valor = cont.get(campo)
        if not isinstance(valor, str) or not valor.strip():
            raise ContratoInvalido(
                "{0}: campo contractual '{1}' debe ser str no vacío".format(
                    NOMBRE_MODULO, campo
                )
            )

    capacidades = cont.get("capacidades")
    if not isinstance(capacidades, dict):
        raise ContratoInvalido(
            "{0}: 'capacidades' debe ser dict".format(NOMBRE_MODULO)
        )

    capacidades_meta = cont.get("capacidades_meta")
    if not isinstance(capacidades_meta, dict):
        raise ContratoInvalido(
            "{0}: 'capacidades_meta' debe ser dict".format(NOMBRE_MODULO)
        )

    nombres_capacidades = set(capacidades.keys())
    nombres_meta = set(capacidades_meta.keys())

    faltan_meta = sorted(nombres_capacidades - nombres_meta)
    if faltan_meta:
        raise ContratoInvalido(
            "{0}: capacidades sin capacidades_meta: {1}".format(
                NOMBRE_MODULO, faltan_meta
            )
        )

    meta_huerfanas = sorted(nombres_meta - nombres_capacidades)
    if meta_huerfanas:
        raise ContratoInvalido(
            "{0}: capacidades_meta sin capacidad declarada: {1}".format(
                NOMBRE_MODULO, meta_huerfanas
            )
        )

    for nombre_cap, ref in capacidades.items():
        if not isinstance(nombre_cap, str) or not nombre_cap.strip():
            raise ContratoInvalido(
                "{0}: nombre de capacidad inválido: {1!r}".format(
                    NOMBRE_MODULO, nombre_cap
                )
            )

        if callable(ref):
            pass
        elif isinstance(ref, str):
            if not ref.strip():
                raise ContratoInvalido(
                    "{0}: capacidad '{1}' tiene referencia vacía".format(
                        NOMBRE_MODULO, nombre_cap
                    )
                )
        else:
            raise ContratoInvalido(
                "{0}: capacidad '{1}' tiene referencia inválida: {2}".format(
                    NOMBRE_MODULO,
                    nombre_cap,
                    type(ref).__name__,
                )
            )

        entrada = capacidades_meta[nombre_cap]

        if not isinstance(entrada, dict):
            raise ContratoInvalido(
                "{0}: capacidades_meta['{1}'] debe ser dict".format(
                    NOMBRE_MODULO, nombre_cap
                )
            )

        for campo in ("descripcion", "entrada", "salida"):
            valor = entrada.get(campo)
            if not isinstance(valor, str) or not valor.strip():
                raise ContratoInvalido(
                    "{0}: capacidades_meta['{1}'] requiere "
                    "'{2}: str no vacío'".format(
                        NOMBRE_MODULO, nombre_cap, campo
                    )
                )

    estados = cont.get("estados_validos")
    if not isinstance(estados, (list, tuple)) or not estados:
        raise ContratoInvalido(
            "{0}: 'estados_validos' debe ser lista/tupla no vacía".format(
                NOMBRE_MODULO
            )
        )

    if len(set(estados)) != len(estados):
        raise ContratoInvalido(
            "{0}: 'estados_validos' contiene duplicados".format(
                NOMBRE_MODULO
            )
        )

    if ESTADO_NO_INICIADO not in estados:
        raise ContratoInvalido(
            "{0}: 'estados_validos' debe contener '{1}'".format(
                NOMBRE_MODULO, ESTADO_NO_INICIADO
            )
        )

    if ESTADO_OPERATIVO not in estados:
        raise ContratoInvalido(
            "{0}: 'estados_validos' debe contener '{1}'".format(
                NOMBRE_MODULO, ESTADO_OPERATIVO
            )
        )

    if ESTADO_DEGRADADO not in estados:
        raise ContratoInvalido(
            "{0}: 'estados_validos' debe contener '{1}'".format(
                NOMBRE_MODULO, ESTADO_DEGRADADO
            )
        )

    if ESTADO_RECHAZADO not in estados:
        raise ContratoInvalido(
            "{0}: 'estados_validos' debe contener '{1}'".format(
                NOMBRE_MODULO, ESTADO_RECHAZADO
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
    """
    Barrido determinista del catálogo de categorías de CC.
    Lee, valida, normaliza y verifica duplicidad de los IDs.
    No calcula, no interpreta, no modifica archivos ni altera estado externo.
    """
    cats, errores = recolectar()
    ids_catalogo = [c["id"] for c in cats]
    coherente = not bool(errores)
    notas: List[str] = []

    if not cats and not errores:
        notas.append(
            "glosario vacío (legítimo hasta montar archivos en categorias/)"
        )

    return {
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "contenedor": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "operacion": "barrer",
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "esquema_categoria": ESQUEMA_CATEGORIA,
        "coherente": coherente,
        "estado": (
            ESTADO_OPERATIVO
            if coherente and cats
            else ESTADO_NO_INICIADO
            if coherente and not cats
            else ESTADO_DEGRADADO
        ),
        "categorias": len(cats),
        "total": len(cats),
        "ids": ids_catalogo,
        "errores": errores,
        "errores_n": len(errores),
        "notas": notas,
    }

# ===============================================================
# FIN 8.1
# ===============================================================

# ===============================================================
# 8.2 — VERIFICAR
# ===============================================================

def verificar() -> Dict[str, Any]:
    """
    Verificación contractual determinista del catálogo de CC.
    Es un alias real de barrer y devuelve exactamente su misma salida.
    No ejecuta una segunda lógica de validación.
    """
    return barrer()

# ===============================================================
# FIN 8.2
# ===============================================================


# ===============================================================
# 8.3 — CATEGORIAS
# ===============================================================

def categorias() -> List[Dict[str, Any]]:
    """
    Devuelve las categorías normalizadas del catálogo si el barrido
    es coherente. Si existen errores, devuelve lista vacía.
    """
    cats, errores = recolectar()
    if errores:
        return []
    return [dict(c) for c in cats]

# ===============================================================
# FIN 8.3
# ===============================================================


# ===============================================================
# 8.4 — POR ID
# ===============================================================

def por_id(cat_id: str) -> Optional[Dict[str, Any]]:
    """
    Resuelve exactamente un ID del catálogo.
    La entrada se normaliza mediante strip/lower.
    Devuelve una copia de la categoría normalizada o None si no existe
    o si el catálogo contiene errores.
    """
    if not isinstance(cat_id, str):
        return None

    key = cat_id.strip().lower()
    if not key:
        return None

    cats, errores = recolectar()
    if errores:
        return None

    for categoria in cats:
        if categoria["id"] == key:
            return dict(categoria)

    return None

# ===============================================================
# FIN 8.4
# ===============================================================


# ===============================================================
# 8.5 — IDS
# ===============================================================

def ids() -> List[str]:
    """
    Devuelve los IDs del catálogo coherente en orden determinista.
    Si existen errores de catálogo, devuelve lista vacía.
    """
    cats, errores = recolectar()
    if errores:
        return []
    return [categoria["id"] for categoria in cats]

# ===============================================================
# FIN 8.5
# ===============================================================

# ===============================================================
# 8.6 — ESQUEMA
# ===============================================================

def esquema() -> Dict[str, Any]:
    """
    Devuelve una copia independiente del esquema de categorías.
    No expone referencias mutables al esquema interno de CC.
    """
    return {
        "obligatorios": list(ESQUEMA_CATEGORIA["obligatorios"]),
        "opcionales": list(ESQUEMA_CATEGORIA["opcionales"]),
        "prohibidos": list(ESQUEMA_CATEGORIA["prohibidos"]),
        "nota": ESQUEMA_CATEGORIA["nota"],
    }

# ===============================================================
# FIN 8.6
# ===============================================================


# ===============================================================
# 8.7 — INVENTARIO
# ===============================================================

def inventario(peticion: Any = None) -> Dict[str, Any]:
    """
    Produce una instantánea determinista del inventario de CC.
    La petición no modifica el comportamiento del inventario.
    Los errores de recolección invalidan la coherencia del inventario,
    pero se conservan como evidencia de la instantánea obtenida.
    """
    cats, errores = recolectar()
    coherente = not bool(errores)

    if coherente and cats:
        estado = ESTADO_OPERATIVO
    elif coherente and not cats:
        estado = ESTADO_NO_INICIADO
    else:
        estado = ESTADO_DEGRADADO

    ids_catalogo = [c["id"] for c in cats]

    return {
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "contenedor": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "estado": estado,
        "coherente": coherente,
        "funcion": (
            "Glosario de IDs del repositorio. "
            "Expone ids a Engine para citar/reportar. No calcula."
        ),
        "uso": [
            "consulta de IDs",
            "resolución por id",
            "esquema de categorías",
        ],
        "esquema_categoria": esquema(),
        "categorias": [dict(c) for c in cats],
        "ids": list(ids_catalogo),
        "total": len(cats),
        "errores": list(errores),
        "errores_n": len(errores),
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "invariantes": list(CONTENEDOR.get("invariantes") or []),
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

def verificar_salida(salida: Any) -> bool:
    """
    Valida estrictamente la salida contractual de barrer().
    No ejecuta capacidades. No modifica estado. No interpreta.
    Acepta únicamente un dict con la estructura y tipos exactos
    producidos por barrer().
    """
    if not isinstance(salida, dict):
        return False

    campos_obligatorios = {
        "contenedor",
        "rol",
        "coherente",
        "categorias",
        "ids",
        "errores",
        "notas",
        "version",
        "esquema",
    }

    if set(salida.keys()) != campos_obligatorios:
        return False

    if not isinstance(salida["contenedor"], str):
        return False

    if not isinstance(salida["rol"], str):
        return False

    if not isinstance(salida["coherente"], bool):
        return False

    if not isinstance(salida["categorias"], int):
        return False

    if isinstance(salida["categorias"], bool):
        return False

    if salida["categorias"] < 0:
        return False

    if not isinstance(salida["ids"], list):
        return False

    if any(
        not isinstance(cid, str) or not cid.strip()
        for cid in salida["ids"]
    ):
        return False

    if len(salida["ids"]) != salida["categorias"]:
        return False

    if len(set(salida["ids"])) != len(salida["ids"]):
        return False

    if any(cid != cid.strip().lower() for cid in salida["ids"]):
        return False

    if not isinstance(salida["errores"], list):
        return False

    for error in salida["errores"]:
        if not isinstance(error, dict):
            return False

        if set(error.keys()) != {"archivo", "error"}:
            return False

        if not isinstance(error["archivo"], str):
            return False

        if not isinstance(error["error"], str):
            return False

        if not error["archivo"].strip() or not error["error"].strip():
            return False

    if not isinstance(salida["notas"], list):
        return False

    if any(
        not isinstance(nota, str)
        for nota in salida["notas"]
    ):
        return False

    if not isinstance(salida["version"], str):
        return False

    if not isinstance(salida["esquema"], dict):
        return False

    if salida["coherente"] != (len(salida["errores"]) == 0):
        return False

    return True

# ===============================================================
# FIN 8.8
# ===============================================================

# ===============================================================
# 8.9 — EJECUTAR TOTAL
# ===============================================================

def ejecutar_total(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Autoridad total de ENGINE sobre CC.

    Ejecuta exactamente todas las capacidades declaradas en
    CONTENEDOR["capacidades"] después de su resolución contractual.

    No inventa capacidades.
    No omite capacidades declaradas.
    No ejecuta capacidades no declaradas.
    No modifica el contrato.
    No modifica el estado de otros módulos.

    Cada capacidad se ejecuta de forma independiente.
    Un fallo de una capacidad no impide ejecutar las restantes.
    La salida distingue ejecución realizada de resultado obtenido.
    """
    if peticion is not None and not isinstance(peticion, dict):
        raise TypeError(
            "{0}: peticion debe ser dict o None".format(NOMBRE_MODULO)
        )

    solicitud = dict(peticion) if isinstance(peticion, dict) else {}

    capacidades_declaradas = tuple(
        CONTENEDOR.get("capacidades", {}).keys()
    )

    resultados: Dict[str, Any] = {}
    errores_ejecucion: List[Dict[str, str]] = []
    capacidades_ejecutadas: List[str] = []

    for nombre in capacidades_declaradas:
        capacidad = CONTENEDOR["capacidades"].get(nombre)

        if not callable(capacidad):
            errores_ejecucion.append({
                "capacidad": nombre,
                "tipo": "capacidad_no_callable",
                "error": (
                    "La capacidad declarada no está resuelta como callable"
                ),
            })
            continue

        try:
            if nombre in (
                "inventario",
                "ejecutar_total",
                "inspeccionar",
                "registrar_inventario",
            ):
                resultado = capacidad(solicitud)
            elif nombre == "por_id":
                resultado = capacidad(
                    solicitud.get("id")
                    if "id" in solicitud
                    else ""
                )
            elif nombre == "verificar_salida":
                resultado = capacidad(
                    solicitud.get("salida")
                    if "salida" in solicitud
                    else {}
                )
            else:
                resultado = capacidad()

            resultados[nombre] = resultado
            capacidades_ejecutadas.append(nombre)

        except Exception as e:
            errores_ejecucion.append({
                "capacidad": nombre,
                "tipo": type(e).__name__,
                "error": str(e),
            })
            resultados[nombre] = None

    salida_barrer = resultados.get("barrer")
    salida_barrer_valida = verificar_salida(salida_barrer)

    if salida_barrer_valida:
        coherencia_base = bool(salida_barrer.get("coherente"))
    else:
        coherencia_base = False

    ejecucion_completa = (
        len(capacidades_ejecutadas) == len(capacidades_declaradas)
        and not errores_ejecucion
    )

    coherente = (
        coherencia_base
        and ejecucion_completa
    )

    estado = (
        ESTADO_OPERATIVO
        if coherente
        else ESTADO_DEGRADADO
    )

    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "operacion": "ejecutar_total",
        "estado": estado,
        "coherente": coherente,
        "ejecucion_completa": ejecucion_completa,
        "capacidades_declaradas": list(
            capacidades_declaradas
        ),
        "capacidades_ejecutadas": sorted(
            capacidades_ejecutadas
        ),
        "capacidades_no_ejecutadas": sorted(
            set(capacidades_declaradas)
            - set(capacidades_ejecutadas)
        ),
        "errores_ejecucion": errores_ejecucion,
        "salida_barrer_valida": salida_barrer_valida,
        "resultados": resultados,
        "nota": (
            "ejecutar_total ejerce autoridad total de ENGINE sobre CC. "
            "La ejecución se deriva exclusivamente de las capacidades "
            "declaradas y resueltas por el contrato. "
            "No inventa, omite ni altera capacidades."
        ),
    }

# ===============================================================
# FIN 8.9
# ===============================================================

# ===============================================================
# 8.10 — INSPECCIONAR
# ===============================================================

def inspeccionar(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Inspección estructural determinista de CC.

    Expone identidad, contrato, capacidades resueltas, esquema,
    integridad del catálogo y permisos arquitectónicos.

    No ejecuta skills de categorías.
    No modifica estado.
    No altera el contrato.
    La petición es opcional y no modifica el resultado.
    """
    if peticion is not None and not isinstance(peticion, dict):
        raise TypeError(
            "{0}: peticion debe ser dict o None".format(NOMBRE_MODULO)
        )

    res_barrer = barrer()
    salida_barrer_valida = verificar_salida(res_barrer)

    capacidades = CONTENEDOR.get("capacidades", {})
    capacidades_meta = CONTENEDOR.get("capacidades_meta", {})

    capacidades_nombres = tuple(capacidades.keys())
    capacidades_meta_nombres = tuple(capacidades_meta.keys())

    capacidades_resueltas = all(
        callable(capacidades.get(nombre))
        for nombre in capacidades_nombres
    )

    correspondencia_meta = (
        set(capacidades_nombres)
        == set(capacidades_meta_nombres)
    )

    contrato_integridad = (
        capacidades_resueltas
        and correspondencia_meta
    )

    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "operacion": "inspeccionar",

        "constantes": {
            "ID_MODULO": ID_MODULO,
            "NOMBRE_MODULO": NOMBRE_MODULO,
            "ROL_MODULO": ROL_MODULO,
            "VERSION_MODULO": VERSION_MODULO,
            "VERSION_CONTRATO": VERSION_CONTRATO,
            "ESQUEMA_CONTRATO": ESQUEMA_CONTRATO,
            "ESTABILIDAD": ESTABILIDAD,
            "COMPATIBLE_DESDE": COMPATIBLE_DESDE,
            "API_ENGINE": API_ENGINE,
        },

        "contrato": {
            "esquema": CONTENEDOR.get("esquema"),
            "version_contrato": CONTENEDOR.get(
                "version_contrato"
            ),
            "version_modulo": CONTENEDOR.get(
                "version_modulo"
            ),
            "estabilidad": CONTENEDOR.get(
                "estabilidad"
            ),
            "compatible_desde": CONTENEDOR.get(
                "compatible_desde"
            ),
            "api_engine": CONTENEDOR.get(
                "api_engine"
            ),
        },

        "capacidades": {
            "declaradas": list(capacidades_nombres),
            "meta": list(capacidades_meta_nombres),
            "resueltas": [
                nombre
                for nombre in capacidades_nombres
                if callable(capacidades.get(nombre))
            ],
            "no_resueltas": [
                nombre
                for nombre in capacidades_nombres
                if not callable(capacidades.get(nombre))
            ],
            "correspondencia_meta": correspondencia_meta,
            "todas_callable": capacidades_resueltas,
        },

        "integridad": {
            "contrato": contrato_integridad,
            "salida_barrer_valida": salida_barrer_valida,
            "catalogo": bool(
                res_barrer.get("coherente")
            ) if salida_barrer_valida else False,
            "coherente": (
                contrato_integridad
                and salida_barrer_valida
                and bool(res_barrer.get("coherente"))
            ),
            "categorias": (
                res_barrer.get("categorias")
                if salida_barrer_valida
                else 0
            ),
            "ids": (
                list(res_barrer.get("ids") or [])
                if salida_barrer_valida
                else []
            ),
            "errores": (
                list(res_barrer.get("errores") or [])
                if salida_barrer_valida
                else []
            ),
        },

        "esquema_categoria": dict(
            ESQUEMA_CATEGORIA
        ),

        "autoriza_engine": dict(
            CONTENEDOR.get("autoriza_engine") or {}
        ),

        "reporting": dict(
            CONTENEDOR.get("reporting") or {}
        ),

        "invariantes": list(INVARIANTES),

        "peticion_recibida": peticion is not None,

        "nota": (
            "inspeccionar expone una instantánea estructural "
            "determinista de CC. No calcula Tru / C / L / K, "
            "no ejecuta skills de categorías, no modifica "
            "el catálogo y no altera el contrato."
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
    Genera una instantánea determinista del inventario estructural de CC.

    No persiste datos.
    No modifica el glosario.
    No modifica evidencia.
    No altera el contrato.
    No modifica otros módulos.

    La operación se considera registrada únicamente cuando la
    instantánea de inventario ha sido generada y su estructura es válida.
    """
    if peticion is not None and not isinstance(peticion, dict):
        raise TypeError(
            "{0}: peticion debe ser dict o None".format(NOMBRE_MODULO)
        )

    solicitud = dict(peticion) if isinstance(peticion, dict) else {}

    inv = inventario(solicitud)

    if not isinstance(inv, dict):
        return {
            "id": ID_MODULO,
            "modulo": NOMBRE_MODULO,
            "rol": ROL_MODULO,
            "version": VERSION_MODULO,
            "version_contrato": VERSION_CONTRATO,
            "operacion": "registrar_inventario",
            "registrado": False,
            "coherente": False,
            "inventario": None,
            "error": (
                "inventario() no produjo una salida dict"
            ),
            "nota": (
                "No se generó una instantánea válida. "
                "No se modificó estado, glosario ni evidencia."
            ),
        }

    inventario_coherente = bool(inv.get("coherente")) and not bool(
        inv.get("errores")
    )

    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "operacion": "registrar_inventario",
        "registrado": True,
        "coherente": inventario_coherente,
        "inventario_valido": True,
        "inventario": inv,
        "peticion_recibida": peticion is not None,
        "nota": (
            "Instantánea determinista del inventario de CC. "
            "Registrar significa generar y exponer la instantánea "
            "en la salida de esta operación; no implica persistencia. "
            "No modifica el glosario, el contrato, la evidencia "
            "ni el estado de otros módulos."
        ),
    }

# ===============================================================
# FIN 8.11
# ===============================================================

# ===============================================================
# FIN PARTE 8
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
# PARTE 9 — REPORTING INTERNO
# ===============================================================

# ===============================================================
# 9.1 — REPORTE
# ===============================================================

def reporte() -> Dict[str, Any]:
    """
    Reporte estructural determinista de CC.
    Usa una única instantánea de barrer() para derivar todo el estado.
    No ejecuta capacidades ajenas, no modifica estado y no interpreta
    condiciones externas.
    """
    r = barrer()
    coherente = bool(r.get("coherente"))
    errores = list(r.get("errores") or [])
    categorias_n = int(r.get("categorias") or 0)
    estado = (
        ESTADO_OPERATIVO
        if coherente and categorias_n > 0
        else ESTADO_NO_INICIADO
        if coherente and categorias_n == 0
        else ESTADO_DEGRADADO
    )
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
        "categorias": categorias_n,
        "ids": list(r.get("ids") or []),
        "errores": errores,
        "errores_n": len(errores),
        "notas": list(r.get("notas") or []),
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "autoridad": list(CONTENEDOR.get("autoridad") or []),
        "conocimiento_exportable": list(
            CONTENEDOR.get("conocimiento_exportable") or []
        ),
        "consultas_soportadas": list(
            CONTENEDOR.get("consultas_soportadas") or []
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
    """
    Diagnóstico estructural determinista de CC.
    Usa una única instantánea de barrer() y clasifica exclusivamente
    los estados definidos por el contrato.
    """
    r = barrer()
    coherente = bool(r.get("coherente"))
    errores = list(r.get("errores") or [])
    categorias_n = int(r.get("categorias") or 0)

    problemas: List[Dict[str, Any]] = []
    advertencias: List[str] = []
    recomendaciones: List[str] = []

    if errores:
        problemas.append({
            "tipo": "errores_catalogo",
            "detalle": errores,
        })
        recomendaciones.append(
            "Corregir los archivos de categorias/ que presenten "
            "errores de carga, estructura o duplicidad."
        )

    if categorias_n == 0 and not errores:
        advertencias.append(
            "Glosario vacío: no existen categorías válidas cargadas."
        )

    if errores:
        estado = ESTADO_DEGRADADO
    elif categorias_n == 0:
        estado = ESTADO_NO_INICIADO
    else:
        estado = ESTADO_OPERATIVO

    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estado": estado,
        "coherente": coherente,
        "problemas": problemas,
        "advertencias": advertencias,
        "recomendaciones": recomendaciones,
        "errores_n": len(errores),
        "categorias_n": categorias_n,
        "ids_n": len(r.get("ids") or []),
        "ids": list(r.get("ids") or []),
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
    "evaluar_universal": evaluar_universal,
}

# ===============================================================
# FIN 10.1
# ===============================================================


# ===============================================================
# 10.2 — RESOLUCIÓN ESTRICTA DE CAPACIDADES
# ===============================================================

def _resolver_capacidades(cont: Dict[str, Any]) -> None:
    capacidades = cont.get("capacidades")

    if not isinstance(capacidades, dict):
        raise ContratoInvalido(
            "{0}: 'capacidades' debe ser dict".format(
                NOMBRE_MODULO
            )
        )

    capacidades_meta = cont.get("capacidades_meta")

    if not isinstance(capacidades_meta, dict):
        raise ContratoInvalido(
            "{0}: 'capacidades_meta' debe ser dict".format(
                NOMBRE_MODULO
            )
        )

    resueltas: Dict[str, Any] = {}

    for nombre, ref in capacidades.items():

        if not isinstance(nombre, str) or not nombre.strip():
            raise ContratoInvalido(
                "{0}: nombre de capacidad inválido: {1!r}".format(
                    NOMBRE_MODULO,
                    nombre,
                )
            )

        if not isinstance(ref, str) or not ref.strip():
            raise ContratoInvalido(
                "{0}: capacidad '{1}' debe declarar una "
                "referencia nominal no vacía".format(
                    NOMBRE_MODULO,
                    nombre,
                )
            )

        referencia = ref.strip()

        if referencia not in _CAP_MAP:
            raise ContratoInvalido(
                "{0}: capacidad '{1}' referencia inexistente: '{2}'".format(
                    NOMBRE_MODULO,
                    nombre,
                    referencia,
                )
            )

        fn = _CAP_MAP[referencia]

        if not callable(fn):
            raise ContratoInvalido(
                "{0}: referencia '{1}' no resuelve a callable".format(
                    NOMBRE_MODULO,
                    referencia,
                )
            )

        if nombre not in capacidades_meta:
            raise ContratoInvalido(
                "{0}: capacidad '{1}' no posee "
                "metadatos contractuales".format(
                    NOMBRE_MODULO,
                    nombre,
                )
            )

        meta = capacidades_meta[nombre]

        if not isinstance(meta, dict):
            raise ContratoInvalido(
                "{0}: capacidades_meta['{1}'] debe ser dict".format(
                    NOMBRE_MODULO,
                    nombre,
                )
            )

        for campo in ("descripcion", "entrada", "salida"):
            if campo not in meta:
                raise ContratoInvalido(
                    "{0}: capacidades_meta['{1}'] carece de '{2}'".format(
                        NOMBRE_MODULO,
                        nombre,
                        campo,
                    )
                )

            if not isinstance(meta[campo], str):
                raise ContratoInvalido(
                    "{0}: capacidades_meta['{1}']['{2}'] "
                    "debe ser str".format(
                        NOMBRE_MODULO,
                        nombre,
                        campo,
                    )
                )

        resueltas[nombre] = fn

    if not resueltas:
        raise ContratoInvalido(
            "{0}: no existen capacidades resolubles".format(
                NOMBRE_MODULO
            )
        )

    cont["capacidades"] = resueltas

# ===============================================================
# FIN 10.2
# ===============================================================


# ===============================================================
# 10.3 — EJECUCIÓN DE VALIDACIÓN, RESOLUCIÓN Y CIERRE
# ===============================================================

_validar_contrato(CONTENEDOR)
_resolver_capacidades(CONTENEDOR)

for _nombre_capacidad, _callable in CONTENEDOR["capacidades"].items():
    if not callable(_callable):
        raise ContratoInvalido(
            "{0}: capacidad '{1}' no quedó resuelta como callable".format(
                NOMBRE_MODULO,
                _nombre_capacidad,
            )
        )

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
