# ===============================================================
# VPSI-TRUTH — modules/diccionario/__init__.py
# ===============================================================
#
# MÓDULO:              diccionario
# ID:                  DI
# Rol:                 DI
# Versión módulo:      1.0
# Versión contrato:    1.0
# Esquema contrato:    VPSI-CONTRACT-1.0
# Estabilidad:         ESTABLE
# Compatible desde:    1.0
# API Engine:          >=1.0
#
# Función:
#   Biblioteca de definiciones (materia prima léxica).
#   Herramienta para contrastar y correlacionar a nivel de significado.
#
# Qué hace:
#   - Auto-carga todos los archivos que declaren DICCIONARIO
#   - Expone definiciones y significados por palabra, idioma o fuente
#   - Entrega materia prima léxica a Engine y otros módulos
#   - Expone inventario, reporte, diagnóstico
#
# Responsabilidad:
#   Ser la fuente de definiciones del sistema.
#
# Autoridad:
#   - Exponer definiciones y significados
#   - Auto-cargar todos los archivos que declaren DICCIONARIO
#   - Entregar materia prima léxica a Engine y otros módulos
#   - Reportar el estado estructural del módulo.
#
# Conocimiento exportable:
#   - inventario
#   - reporte
#   - diagnostico
#   - listar, cargar, cargar_todos
#   - definir, significado, palabras
#   - inyectar_en_peticion
#   - verificar, barrer
#
# Relación con Engine:
#   Engine descubre este CONTENEDOR, ejecuta únicamente las
#   capacidades declaradas, puede inspeccionar todos los archivos
#   del módulo y consolida el reporte producido por este.
#
# Relación con Omega:
#   Omega no calcula información de este módulo.
#   Solo presenta los resultados entregados por Engine.
#
# Observaciones:
#   Todo archivo *.py del directorio o fuentes/ que declare DICCIONARIO
#   se carga automáticamente. No hace falta editar el init.
#
# NOTAS DE ARQUITECTURA (leer antes de editar):
#   1. El CONTENEDOR es la ÚNICA interfaz pública del módulo.
#   2. Engine solo lee CONTENEDOR; no lee constantes sueltas del código.
#   3. Toda capacidad en "capacidades" DEBE tener entrada 1:1 en
#      "capacidades_meta" con descripcion, entrada y salida (str).
#   4. "requiere" y "no_hace" son claves OBLIGATORIAS del esquema
#      (pueden ser listas vacías []).
#   5. El módulo no importa ni invoca otros módulos de dominio.
#      Si necesita algo, lo declara en "requiere"; Engine resuelve.
#   6. El contrato es positivo: describe qué ES y qué GARANTIZA.
#      "no_hace" existe por esquema; usar límites de oficio, no nombres
#      de otros módulos.
#   7. Al agregar capacidad nueva: capacidades + capacidades_meta +
#      _CAP_MAP + VERSION_MODULO.
#   8. Tras _resolver_capacidades, CONTENEDOR se considera inmutable.
#
# ===============================================================

# ===============================================================
# IMPORTACIONES
# ===============================================================

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

try:
    from core.diagnostico import DiagnosticoGlobal
except Exception:
    class DiagnosticoGlobal:
        @staticmethod
        def recibir_reporte(*args, **kwargs):
            pass

# ===============================================================
# FIN IMPORTACIONES
# ===============================================================

# ===============================================================
# CONSTANTES
# ===============================================================

ID_MODULO = "DI"
NOMBRE_MODULO = "diccionario"
ROL_MODULO = "DI"

VERSION_MODULO = "1.0"
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
    "DI es una herramienta de definiciones, no calcula Tru",
    "DI no clasifica O_context (eso es CX)",
    "DI auto-carga todo lo que está debajo del módulo",
    "las capacidades declaradas son siempre callables tras la resolución",
    "este módulo no modifica el estado de otros módulos",
    "este módulo no inventa capacidades no declaradas en CONTENEDOR",
    "este módulo siempre puede reportar su propio estado",
)

# ===============================================================
# FIN CONSTANTES
# ===============================================================

# ===============================================================
# CONFIGURACIÓN
# ===============================================================

_DIR = Path(__file__).parent
_FUENTES = _DIR / "fuentes"

# ===============================================================
# FIN CONFIGURACIÓN
# ===============================================================

# ===============================================================
# DEFINICIONES
# ===============================================================

class ContratoInvalido(Exception):
    """El CONTENEDOR no cumple el esquema o la resolución falló."""

# ===============================================================
# FIN DEFINICIONES
# ===============================================================

# ===============================================================
# ESTADO INTERNO
# ===============================================================

_REGISTRO: Dict[str, Any] = {}
_META: Dict[str, Dict[str, Any]] = {}
_CARGADO = False

# ===============================================================
# FIN ESTADO INTERNO
# ===============================================================

# ===============================================================
# FUNCIONES PRIVADAS
# ===============================================================

def _norm_nombre(nombre: str) -> str:
    return (nombre or "").strip().lower().replace("-", "_").replace(" ", "_")


def _norm_palabra(p: str) -> str:
    return (p or "").strip().lower()


def _extraer_definicion(entrada: Any) -> Optional[str]:
    if entrada is None:
        return None
    if isinstance(entrada, str):
        return entrada.strip() or None
    if isinstance(entrada, dict):
        for k in ("definicion", "definición", "def", "meaning", "significado"):
            v = entrada.get(k)
            if v is not None and str(v).strip():
                return str(v).strip()
    return None


def _extraer_significado(entrada: Any) -> Optional[str]:
    if not isinstance(entrada, dict):
        return _extraer_definicion(entrada)
    for k in ("significado", "meaning", "interpretacion", "interpretación"):
        v = entrada.get(k)
        if v is not None and str(v).strip():
            return str(v).strip()
    return _extraer_definicion(entrada)


def _cargar_modulo(path: Path, clave: str) -> Optional[Any]:
    spec = importlib.util.spec_from_file_location(clave, path)
    if spec is None or spec.loader is None:
        return None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[clave] = mod
    try:
        spec.loader.exec_module(mod)
    except Exception:
        return None
    return mod


def _descubrir() -> None:
    global _CARGADO
    if _CARGADO:
        return

    candidatos: List[Path] = []
    if _FUENTES.is_dir():
        candidatos.extend(sorted(_FUENTES.glob("*.py")))
    candidatos.extend(sorted(_DIR.glob("*.py")))

    vistos: Set[Path] = set()
    for f in candidatos:
        if f.name == "__init__.py" or f.name.startswith("_"):
            continue
        resolved = f.resolve()
        if resolved in vistos:
            continue
        vistos.add(resolved)

        clave = "diccionario_{0}".format(f.stem)
        mod = _cargar_modulo(f, clave)
        if mod is None:
            _META[f.stem] = {"error": "carga fallida", "archivo": f.name}
            continue

        datos = getattr(mod, "DICCIONARIO", None)
        if datos is None:
            continue

        meta = getattr(mod, "META", None)
        nombre = None
        if isinstance(meta, dict):
            nombre = meta.get("nombre")
        if not nombre:
            nombre = f.stem
        key = _norm_nombre(str(nombre))

        _REGISTRO[key] = datos
        if isinstance(meta, dict):
            _META[key] = dict(meta)
            _META[key]["archivo"] = f.name
        else:
            _META[key] = {"nombre": key, "archivo": f.name}

    _CARGADO = True


def _asegurar() -> None:
    _descubrir()

# ===============================================================
# FIN FUNCIONES PRIVADAS
# ===============================================================

# ===============================================================
# CAPACIDADES PÚBLICAS
# ===============================================================

def listar() -> List[str]:
    _asegurar()
    return sorted(_REGISTRO.keys())


def listar_por_idioma(idioma: str) -> List[str]:
    _asegurar()
    idioma = (idioma or "").strip().lower()
    out = []
    for k, m in _META.items():
        if k in _REGISTRO and str(m.get("idioma", "")).lower() == idioma:
            out.append(k)
    return sorted(out)


def meta(nombre: str) -> Optional[Dict[str, Any]]:
    _asegurar()
    return _META.get(_norm_nombre(nombre))


def cargar(nombre: str) -> Any:
    _asegurar()
    key = _norm_nombre(nombre)
    if key not in _REGISTRO:
        raise KeyError(
            "diccionario no encontrado: {0!r}. Disponibles: {1}".format(
                nombre, listar()
            )
        )
    return _REGISTRO[key]


def cargar_todos() -> Dict[str, Any]:
    _asegurar()
    return {k: _REGISTRO[k] for k in sorted(_REGISTRO)}


def cargar_idioma(idioma: str) -> Dict[str, Any]:
    return {n: cargar(n) for n in listar_por_idioma(idioma)}


def definir(palabra: str, *nombres: str) -> Optional[Dict[str, Any]]:
    _asegurar()
    p = _norm_palabra(palabra)
    if not p:
        return None

    fuentes = list(nombres) if nombres else listar()
    for nombre in fuentes:
        try:
            datos = cargar(nombre)
        except KeyError:
            continue

        if isinstance(datos, dict):
            for k, v in datos.items():
                if _norm_palabra(str(k)) == p:
                    return {
                        "palabra": p,
                        "definicion": _extraer_definicion(v),
                        "significado": _extraer_significado(v),
                        "fuente": _norm_nombre(nombre),
                        "entrada": v,
                    }
        elif isinstance(datos, (set, frozenset, list, tuple)):
            if p in {_norm_palabra(str(x)) for x in datos}:
                return {
                    "palabra": p,
                    "definicion": None,
                    "significado": None,
                    "fuente": _norm_nombre(nombre),
                    "entrada": p,
                    "nota": "término presente sin definición textual",
                }
    return None


def significado(palabra: str, *nombres: str) -> Optional[str]:
    r = definir(palabra, *nombres)
    if r is None:
        return None
    return r.get("significado") or r.get("definicion")


def palabras(*nombres: str) -> Set[str]:
    _asegurar()
    fuentes = list(nombres) if nombres else listar()
    out: Set[str] = set()
    for nombre in fuentes:
        try:
            datos = cargar(nombre)
        except KeyError:
            continue
        if isinstance(datos, dict):
            out |= {_norm_palabra(str(k)) for k in datos if k}
        elif isinstance(datos, (set, frozenset, list, tuple)):
            out |= {_norm_palabra(str(x)) for x in datos if x}
    return out


def inyectar_en_peticion(
    peticion: Optional[Dict[str, Any]] = None,
    *nombres: str,
    clave: str = "diccionario",
) -> Dict[str, Any]:
    base = dict(peticion or {})
    lemas = sorted(palabras(*nombres))
    base[clave] = lemas
    base["_diccionario_meta"] = {
        "nombres": list(nombres) if nombres else listar(),
        "size": len(lemas),
        "version": VERSION_MODULO,
        "modulo": "diccionario",
        "rol": "DI",
    }
    return base


def resolver(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    _asegurar()
    peticion = dict(peticion or {})
    palabra = peticion.get("palabra") or peticion.get("termino")
    idioma = peticion.get("idioma")
    nombres = peticion.get("diccionarios") or peticion.get("nombres")

    if palabra:
        if nombres:
            if isinstance(nombres, str):
                nombres = [nombres]
            r = definir(str(palabra), *nombres)
        elif idioma:
            r = definir(str(palabra), *listar_por_idioma(str(idioma)))
        else:
            r = definir(str(palabra))
        return {
            "ok": r is not None,
            "modulo": "diccionario",
            "rol": "DI",
            "resultado": r,
            "coherente": True,
            "notas": [
                "Definición entregada. No se calculó Tru ni se clasificó O."
            ],
        }

    if idioma and not nombres:
        datos = cargar_idioma(str(idioma))
        usados = list(datos.keys())
    elif nombres:
        if isinstance(nombres, str):
            nombres = [nombres]
        datos = {n: cargar(n) for n in nombres}
        usados = list(nombres)
    else:
        datos = cargar_todos()
        usados = list(datos.keys())

    return {
        "ok": True,
        "modulo": "diccionario",
        "rol": "DI",
        "diccionarios_usados": usados,
        "palabras_n": len(palabras(*usados)),
        "coherente": True,
        "notas": [
            "Materia prima entregada. No se calculó Tru ni se clasificó O."
        ],
    }


def barrer() -> Dict[str, Any]:
    _asegurar()
    errores: List[str] = []
    notas: List[str] = []
    por_idioma: Dict[str, List[str]] = {}

    for k, m in sorted(_META.items()):
        if m.get("error"):
            errores.append("{0}: {1}".format(k, m["error"]))
            continue
        if k not in _REGISTRO:
            continue
        idioma = str(m.get("idioma") or "?").lower()
        por_idioma.setdefault(idioma, []).append(k)
        datos = _REGISTRO[k]
        if not isinstance(datos, (dict, set, frozenset, list, tuple)):
            errores.append(
                "{0}: DICCIONARIO debe ser dict (definiciones) "
                "o set/list (términos)".format(k)
            )

    if not _REGISTRO:
        notas.append(
            "ningún diccionario declarado todavía "
            "(vacío legítimo hasta montar fuentes)"
        )

    if errores:
        try:
            DiagnosticoGlobal.recibir_reporte(
                modulo="diccionario",
                errores=[{"tipo": "error", "detalle": e} for e in errores],
            )
        except Exception:
            pass

    return {
        "contenedor": "diccionario",
        "rol": "DI",
        "coherente": not errores,
        "errores": errores,
        "diccionarios": listar(),
        "total": len(_REGISTRO),
        "por_idioma": por_idioma,
        "notas": notas,
    }


def verificar() -> Dict[str, Any]:
    return barrer()


def verificar_salida(salida: Dict[str, Any]) -> bool:
    return bool(salida.get("coherente", False))


def axiomas() -> List[Dict[str, Any]]:
    return [
        {
            "id": "DI-OP-1",
            "tipo": "axioma",
            "sujeto": "diccionario",
            "relacion": "es",
            "objeto": "herramienta_de_definiciones",
            "polaridad": True,
            "enunciado": (
                "DI es la herramienta de definiciones para contrastar y "
                "correlacionar a nivel léxico-significado."
            ),
            "depende_de": [],
            "gobierna": ["diccionario"],
        },
        {
            "id": "DI-OP-2",
            "tipo": "axioma",
            "sujeto": "diccionario",
            "relacion": "no_calcula",
            "objeto": "Tru_ni_C_L_K",
            "polaridad": True,
            "enunciado": (
                "DI no calcula Tru_Ri, Tru_total, C, L ni K."
            ),
            "depende_de": [],
            "gobierna": ["diccionario"],
        },
        {
            "id": "DI-OP-3",
            "tipo": "axioma",
            "sujeto": "diccionario",
            "relacion": "no_clasifica",
            "objeto": "O_context",
            "polaridad": True,
            "enunciado": (
                "DI no clasifica O_context (oficio CX)."
            ),
            "depende_de": [],
            "gobierna": ["diccionario", "contexto"],
        },
        {
            "id": "DI-OP-4",
            "tipo": "axioma",
            "sujeto": "fuentes_de_diccionario",
            "relacion": "se_leen",
            "objeto": "automaticamente",
            "polaridad": True,
            "enunciado": (
                "Todo archivo bajo el módulo que declare DICCIONARIO se carga solo."
            ),
            "depende_de": [],
            "gobierna": ["diccionario"],
        },
    ]

# ===============================================================
# FIN CAPACIDADES PÚBLICAS
# ===============================================================

# ===============================================================
# REPORTING INTERNO
# ===============================================================

def reporte() -> Dict[str, Any]:
    b = barrer()
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "estado": ESTADO_OPERATIVO if b.get("coherente") else ESTADO_DEGRADADO,
        "coherente": b.get("coherente"),
        "diccionarios": b.get("total"),
        "errores": len(b.get("errores") or []),
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
    }


def diagnostico() -> Dict[str, Any]:
    b = barrer()
    problemas = []
    advertencias = []
    recomendaciones = []

    if b.get("errores"):
        problemas.append({"tipo": "errores_carga", "detalle": b["errores"]})
        recomendaciones.append("Revisar archivos de fuentes con error de carga")

    if not b.get("diccionarios"):
        advertencias.append("No hay diccionarios cargados")
        recomendaciones.append("Agregar archivos con DICCIONARIO en fuentes/")

    estado = ESTADO_OPERATIVO
    if problemas:
        estado = ESTADO_DEGRADADO
    if not b.get("diccionarios") and not problemas:
        estado = ESTADO_NO_INICIADO

    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "estado": estado,
        "coherente": b.get("coherente"),
        "problemas": problemas,
        "advertencias": advertencias,
        "recomendaciones": recomendaciones,
        "diccionarios": b.get("total"),
        "errores_n": len(b.get("errores") or []),
    }


def inventario(peticion: Any = None) -> Dict[str, Any]:
    b = barrer()
    detalle = []
    for n in listar():
        m = meta(n) or {}
        datos = _REGISTRO.get(n)
        if isinstance(datos, dict):
            size = len(datos)
            tipo = m.get("tipo") or "definiciones"
        elif isinstance(datos, (set, frozenset, list, tuple)):
            size = len(datos)
            tipo = m.get("tipo") or "terminos"
        else:
            size = None
            tipo = m.get("tipo")
        detalle.append({
            "nombre": n,
            "idioma": m.get("idioma"),
            "tipo": tipo,
            "size": size,
            "version": m.get("version"),
            "archivo": m.get("archivo"),
        })
    return {
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "total": b.get("total"),
        "diccionarios": detalle,
        "por_idioma": b.get("por_idioma"),
        "coherente": b.get("coherente"),
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "autoridad": CONTENEDOR.get("autoridad"),
        "conocimiento_exportable": CONTENEDOR.get("conocimiento_exportable"),
        "consultas_soportadas": CONTENEDOR.get("consultas_soportadas"),
        "invariantes": CONTENEDOR.get("invariantes"),
    }

# ===============================================================
# FIN REPORTING
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
        "Biblioteca de definiciones. Rol DI. "
        "Materia prima léxica: palabra → definición → significado. "
        "Herramienta para contrastar y correlacionar a nivel de significado. "
        "Auto-carga todos los archivos debajo del módulo. "
        "Engine puede solicitar y distribuir definiciones según contexto. "
        "No calcula Tru. No clasifica O. No trae dominios externos."
    ),

    # ============================================================
    # PROPÓSITO
    # ============================================================
    "funcion": (
        "Biblioteca de definiciones para contrastar y correlacionar a nivel "
        "léxico-significado. Materia prima: palabra → definición → significado. "
        "Auto-carga todo lo que está debajo del módulo."
    ),
    "no_hace": [
        "No calcula C, L, K, Tru_Ri ni Tru_total",
        "No clasifica O_context (eso es CX)",
        "No trae material externo de dominios (eso es RE)",
        "No orquesta el ciclo (eso es Engine)",
        "No sustituye AX, MC, CA, FO, CIT",
    ],

    # ============================================================
    # AUTORIDAD
    # ============================================================
    "autoridad": [
        "Exponer definiciones y significados",
        "Auto-cargar todos los archivos que declaren DICCIONARIO",
        "Entregar materia prima léxica a Engine y otros módulos",
        "Reportar estado, inventario y diagnóstico propios",
    ],

    # ============================================================
    # CONOCIMIENTO EXPORTABLE
    # ============================================================
    "conocimiento_exportable": [
        "inventario",
        "reporte",
        "diagnostico",
        "listar",
        "cargar",
        "cargar_todos",
        "definir",
        "significado",
        "palabras",
        "inyectar_en_peticion",
        "verificar",
        "barrer",
        "resolver",
        "axiomas",
    ],

    # ============================================================
    # DEPENDENCIAS
    # ============================================================
    "requiere": ["CT", "FO", "MC", "SF", "CA", "CX", "RE", "VX", "TX", "CH", "CIT", "CT",],

    # ============================================================
    # AUTORIZACIÓN AL ENGINE
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
        "modificar": False,
        "alterar": False,
        "reescribir": False,
        "crear": False,
        "eliminar": False,
        "actualizar": False,

        # --- PERMISOS DE PROCESAMIENTO ---
        "validar": True,
        "procesar": True,
        "analizar": True,
        "generar": False,
        "transformar": False,

        # --- PERMISOS DE DATOS ---
        "exportar": True,
        "importar": False,
        "respaldar": False,
        "recuperar": True,
        "sincronizar": False,

        # --- PERMISOS DE MONITOREO ---
        "monitorear": True,
        "alertar": True,
        "metricas": True,
        "diagnostico": True,

        # --- PERMISOS DE ESTADO (OBLIGATORIOS) ---
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
    },

    # ============================================================
    # CONSULTAS SOPORTADAS
    # ============================================================
    "consultas_soportadas": [
        "listar",
        "cargar",
        "cargar_todos",
        "definir",
        "significado",
        "palabras",
        "inyectar_en_peticion",
        "inventario",
        "reporte",
        "diagnostico",
        "verificar",
        "barrer",
        "resolver",
        "axiomas",
    ],

    # ============================================================
    # CAPACIDADES
    # ============================================================
    "capacidades": {
        "verificar": "verificar",
        "barrer": "barrer",
        "inventario": "inventario",
        "reporte": "reporte",
        "diagnostico": "diagnostico",
        "axiomas": "axiomas",
        "resolver": "resolver",
        "listar": "listar",
        "cargar": "cargar",
        "cargar_todos": "cargar_todos",
        "definir": "definir",
        "significado": "significado",
        "palabras": "palabras",
        "inyectar_en_peticion": "inyectar_en_peticion",
        "verificar_salida": "verificar_salida",
    },

    # ============================================================
    # METADATOS DE CAPACIDADES (1:1 OBLIGATORIO)
    # ============================================================
    "capacidades_meta": {
        "verificar": {
            "descripcion": "Alias de barrer. Verifica coherencia del diccionario.",
            "entrada": "ninguna",
            "salida": "dict con coherente, errores, diccionarios, total",
        },
        "barrer": {
            "descripcion": (
                "Centinela de DI: valida forma de las fuentes, "
                "reporta errores de carga. No calcula Tru."
            ),
            "entrada": "ninguna",
            "salida": "dict con coherente, errores, diccionarios, total, por_idioma",
        },
        "inventario": {
            "descripcion": "Inventario de diccionarios descubiertos.",
            "entrada": "ninguna",
            "salida": "dict con id, version, total, diccionarios, por_idioma",
        },
        "reporte": {
            "descripcion": "Reporte interno de estado del módulo DI.",
            "entrada": "ninguna",
            "salida": "dict con id, estado, coherente, diccionarios, capacidades",
        },
        "diagnostico": {
            "descripcion": "Diagnóstico del módulo DI.",
            "entrada": "ninguna",
            "salida": "dict con id, estado, problemas, advertencias, recomendaciones",
        },
        "axiomas": {
            "descripcion": "Declaraciones axiomáticas del módulo DI.",
            "entrada": "ninguna",
            "salida": "list[dict] de declaraciones",
        },
        "resolver": {
            "descripcion": "Entrega definiciones según palabra, idioma o fuente.",
            "entrada": "dict con palabra, idioma, diccionarios opcionales",
            "salida": "dict con definiciones o materia prima",
        },
        "listar": {
            "descripcion": "Nombres de todos los diccionarios descubiertos.",
            "entrada": "ninguna",
            "salida": "list[str]",
        },
        "cargar": {
            "descripcion": "Carga un diccionario por nombre.",
            "entrada": "nombre: str",
            "salida": "dict con el DICCIONARIO",
        },
        "cargar_todos": {
            "descripcion": "Carga todos los diccionarios descubiertos.",
            "entrada": "ninguna",
            "salida": "dict nombre → datos",
        },
        "definir": {
            "descripcion": "Busca definición de una palabra en fuentes.",
            "entrada": "palabra: str, *nombres",
            "salida": "dict con definicion, significado, fuente o None",
        },
        "significado": {
            "descripcion": "Atajo para obtener significado/definición de una palabra.",
            "entrada": "palabra: str, *nombres",
            "salida": "str o None",
        },
        "palabras": {
            "descripcion": "Conjunto de lemas de las fuentes indicadas.",
            "entrada": "*nombres",
            "salida": "set[str]",
        },
        "inyectar_en_peticion": {
            "descripcion": "Entrega lemas a una petición para el ciclo.",
            "entrada": "peticion opcional, *nombres, clave='diccionario'",
            "salida": "peticion con lemas inyectados",
        },
        "verificar_salida": {
            "descripcion": "Comprueba forma mínima de una salida de DI.",
            "entrada": "salida: dict",
            "salida": "bool",
        },
    },

    # ============================================================
    # REPORTING
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
# VALIDACIÓN Y RESOLUCIÓN (después de definir todo)
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


_CAP_MAP = {
    "verificar": verificar,
    "barrer": barrer,
    "inventario": inventario,
    "reporte": reporte,
    "diagnostico": diagnostico,
    "axiomas": axiomas,
    "resolver": resolver,
    "listar": listar,
    "cargar": cargar,
    "cargar_todos": cargar_todos,
    "definir": definir,
    "significado": significado,
    "palabras": palabras,
    "inyectar_en_peticion": inyectar_en_peticion,
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
            "{0}: capacidad '{1}' tipo inválido: {2}".format(
                NOMBRE_MODULO, nombre, type(ref).__name__
            )
        )
    cont["capacidades"] = resueltas


# ===============================================================
# VALIDAR Y RESOLVER AL IMPORTAR
# ===============================================================

_validar_contrato(CONTENEDOR)
_resolver_capacidades(CONTENEDOR)

# ===============================================================
# EXPORTACIONES PÚBLICAS
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
    "listar",
    "listar_por_idioma",
    "meta",
    "cargar",
    "cargar_todos",
    "cargar_idioma",
    "definir",
    "significado",
    "palabras",
    "inyectar_en_peticion",
    "resolver",
    "verificar",
    "barrer",
    "verificar_salida",
    "inventario",
    "reporte",
    "diagnostico",
    "axiomas",
    "ContratoInvalido",
]
