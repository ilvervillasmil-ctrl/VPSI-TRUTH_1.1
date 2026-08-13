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
# Función:
#   Glosario de IDs del repositorio.
#   Lee y organiza categorias/*.py y expone esos IDs a Engine.
#
# Qué hace:
#   - Descubre y normaliza categorias/*.py (CATEGORIA / CATEGORIAS / IDS)
#   - Expone el catálogo de IDs ordenado
#   - Responde por_id, ids, esquema
#   - Reporta coherencia, inventario y diagnóstico propios
#
# Qué NO hace:
#   - No calcula Tru_Ri / Tru_total / C / L / K
#   - No aplica α / β
#   - No hace conteos
#   - No clasifica O
#   - No orquesta el ciclo
#   - No envía reportes a otros módulos (Engine los recolecta)
#   - No sustituye CIT / CA / FO / AX / CX / MC / RE / TX / CH
#
# Responsabilidad:
#   Ser el glosario pasivo de IDs. Cero cálculo. Cero orquestación.
#
# Autoridad:
#   - Declarar los IDs disponibles
#   - Resolver consulta por_id / ids / esquema
#   - Reportar estado, inventario y diagnóstico propios
#
# Conocimiento exportable:
#   categorias, ids, por_id, esquema, inventario, reporte, diagnostico
#
# Relación con Engine:
#   Engine descubre este CONTENEDOR y consulta IDs cuando se
#   piden citar / reportar / referenciar.
#   Engine recolecta reporte() y diagnostico().
#   Este módulo solo informa.
#
# Relación con Omega:
#   Omega no calcula nada de CC. Solo presenta lo que Engine entrega.
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

ID_MODULO = "CC"
NOMBRE_MODULO = "catalogo_citaciones"
ROL_MODULO = "CC"

VERSION_MODULO = "2.1"
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
    "este módulo no calcula Tru / C / L / K",
    "este módulo no orquesta el ciclo",
    "este módulo no envía reportes a otros módulos",
    "los IDs viven en categorias/, no en este INIT",
    "este módulo no inventa capacidades no declaradas en CONTENEDOR",
)

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
        "Glosario de IDs del repositorio. Rol CC. "
        "Lee y organiza categorias/*.py. Los IDs viven ahí, no en el INIT. "
        "Engine consulta IDs para citar o reportar. "
        "No calcula. No interpreta pedidos. No envía reportes a terceros."
    ),

    # ============================================================
    # PROPÓSITO
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
    # AUTORIDAD
    # ============================================================
    "autoridad": [
        "Declarar los IDs disponibles en el catálogo",
        "Resolver consulta por_id / ids / esquema",
        "Leer y normalizar todos los archivos de categorias/",
        "Reportar estado, inventario y diagnóstico propios",
    ],

    # ============================================================
    # CONOCIMIENTO EXPORTABLE
    # ============================================================
    "conocimiento_exportable": [
        "categorias",
        "ids",
        "por_id",
        "esquema",
        "inventario",
        "reporte",
        "diagnostico",
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
    "requiere": ["CT", "AX", "FO", "MC", 
                 "SF", "CA", "CX", "DI",
                 "RE", "VX", "TX", "CH", 
                 "CIT", "TT", "CE",],

    # ============================================================
    # ACCESO A ARCHIVOS (AGREGADO — obligatorio en el esquema)
    # ============================================================
    "acceso_archivos": ["acceso_archivos"],

    # ============================================================
    # VALIDAR ESQUEMA A NIVEL MÓDULO (AGREGADO — obligatorio en el esquema)
    # ============================================================
    "validar_esquema": ["acceso_archivos"],
    
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
        "listar_ids",
        "consultar_por_id",
        "obtener_esquema",
        "obtener_inventario",
        "obtener_reporte",
        "obtener_diagnostico",
        "verificar_coherencia",
    ],

    # ============================================================
    # CAPACIDADES
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
    },

    # ============================================================
    # METADATOS DE CAPACIDADES (1:1 OBLIGATORIO)
    # ============================================================
    "capacidades_meta": {
        "verificar": {
            "descripcion": "Alias de barrer. Verifica coherencia del glosario.",
            "entrada": "acceso_archivos",
            "validar_esquema": ["acceso_archivos"],
            "salida": (
                "dict con coherente, categorias, ids, errores"
            ),
            "acceso_archivos": ["acceso_archivos"],
        },

        "barrer": {
            "descripcion": (
                "Evalúa coherencia del glosario de IDs. No calcula."
            ),
            "entrada": "accceso_archivos",
            "validar_esquema": ["*"],
            "salida": (
                "dict con coherente, categorias, ids, errores, esquema"
            ),
            "acceso_archivos": ["*"],
        },

        "inventario": {
            "descripcion": (
                "Inventario completo del módulo y de los IDs."
            ),
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
            "salida": (
                "list[dict] de categorías normalizadas"
            ),
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
            "descripcion": (
                "Lista de todos los ids del catálogo coherente."
            ),
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
            "descripcion": (
                "Reporte interno de estado del módulo CC."
            ),
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

def recolectar() -> Tuple[List[Dict[str, Any]], List[Dict[str, str]]]:
    cats: List[Dict[str, Any]] = []
    errores: List[Dict[str, str]] = []
    candidatos: List[Path] = []

    # 1. Descubrimiento de archivos de categorías (categorias/ + raíz)
    if _CAT_DIR.is_dir():
        candidatos.extend(sorted(_CAT_DIR.glob("*.py")))
    candidatos.extend(sorted(_DIR.glob("*.py")))

    # 2. Dedupe de ARCHIVOS: por ruta absoluta y por nombre de módulo
    archivos_unicos: List[Path] = []
    rutas_vistas = set()
    modulos_procesados = set()
    for p in candidatos:
        if p.name == "__init__.py" or p.name.startswith("_"):
            continue
        try:
            ruta_abs = str(p.resolve())
        except Exception:  # noqa: BLE001
            ruta_abs = str(p)
        if ruta_abs in rutas_vistas:
            continue
        if p.stem in modulos_procesados:
            continue
        rutas_vistas.add(ruta_abs)
        modulos_procesados.add(p.stem)
        archivos_unicos.append(p)

    # 3. Carga y normalización desde los archivos reales
    for archivo in archivos_unicos:
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

    # 4. Clasificación por espacio de nombres (MÓDULO + ID).
    #    Un mismo id en módulos distintos es legítimo: CX/carro y
    #    PG/carro conviven. No se elimina ninguno. No es error.
    for c in cats:
        c["modulo"] = str(c.get("fuente_modulo") or c["origen"]).upper()

    # 5. Orden por módulo, nivel_fractal e id
    cats.sort(
        key=lambda c: (
            c["modulo"],
            c["nivel_fractal"] is None,
            c["nivel_fractal"] or 0,
            c["id"],
        )
    )

    return cats, errores



def recolectar() -> dict:
    # Garantizar que no se procesen módulos duplicados
    modulos_procesados = set()
    todas_las_entradas = []

    # Supongamos que descubres los módulos en 'categorias/'
    modulos_descubiertos = _descubrir_modulos_categorias()

    for mod in modulos_descubiertos:
        nombre_mod = getattr(mod, "__name__", str(mod))
        if nombre_mod in modulos_procesados:
            continue
        modulos_procesados.add(nombre_mod)

        entradas = _cargar_desde_modulo(mod, mod.__file__.split("/")[-1].replace(".py", ""))
        todas_las_entradas.extend(entradas)

    # Desduplicación global defensiva por ID
    entradas_unicas = {}
    for entry in todas_las_entradas:
        key = entry["id"].lower()
        if key not in entradas_unicas:
            entradas_unicas[key] = entry

    return {
        "coherente": True,
        "total": len(entradas_unicas),
        "entradas": list(entradas_unicas.values()),
    }

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


def categorias() -> List[Dict[str, Any]]:
    r = barrer()
    if not r.get("coherente", False):
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


def esquema() -> Dict[str, Any]:
    return dict(ESQUEMA_CATEGORIA)


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


def verificar() -> Dict[str, Any]:
    return barrer()

# ===============================================================
# FIN CAPACIDADES PÚBLICAS
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
        "notas": r.get("notas"),
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
# FIN REPORTING
# ===============================================================


# ===============================================================
# EXPORTACIONES + RESOLUCIÓN ESTRICTA
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


_validar_contrato(CONTENEDOR)
_resolver_capacidades(CONTENEDOR)

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
    "ContratoInvalido",
]

# ===============================================================
# FIN EXPORTACIONES
# ===============================================================


# ===============================================================
# EXTENSIONES FUTURAS
# ===============================================================
#
# Toda capacidad nueva DEBE agregarse simultáneamente en:
#   1. capacidades
#   2. capacidades_meta  (descripcion, entrada, salida: str)
#   3. _CAP_MAP
#   4. VERSION_MODULO
#
# Todo ID nuevo: agregar archivo en categorias/*.py
# (CATEGORIA, CATEGORIAS o IDS). Este INIT los descubre solo.
#
# Si este módulo necesitara una capacidad de otro módulo,
# se declara en requiere[]. Engine la resuelve y la entrega.
#
# ===============================================================
# FIN EXTENSIONES FUTURAS
# ===============================================================


# ===============================================================
# FIN DEL MÓDULO
# ===============================================================
