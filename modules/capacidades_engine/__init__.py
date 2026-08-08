# ===============================================================
# VPSI-TRUTH — modules/capacidades_engine/__init__.py
# ===============================================================
#
# MÓDULO:              capacidades_engine
# ID:                  CE
# Rol:                 CE
# Versión módulo:      1.2
# Versión contrato:    1.0
# Esquema contrato:    VPSI-CONTRACT-1.0
# Estabilidad:         ESTABLE
# Compatible desde:    1.0
# API Engine:          >=1.0
#
# ---------------------------------------------------------------
# JERARQUÍA ESTRUCTURAL
# ---------------------------------------------------------------
#
#   Engine
#       ↓
#   Capacidad (CE)
#       ↓
#   Skills / Mandatos
#       ↓
#   Archivos que implementan esos skills
#
# CE representa una capacidad estructural del Engine.
# Cada archivo implementa uno o más skills pertenecientes
# a esa capacidad.
# Los archivos son implementación física;
# los skills son competencias operativas.
#
# Así como un brazo posee múltiples habilidades sin dejar
# de ser un único órgano, CE representa una única capacidad
# estructural del Engine que agrupa múltiples skills.
# El Engine no solicita permiso a CE para utilizarlos porque
# forman parte de su propia estructura.
#
# ---------------------------------------------------------------
# TERMINOLOGÍA FIJA
# ---------------------------------------------------------------
#
#   Capacidad  →  el módulo CE (órgano estructural)
#   Skill      →  competencia operacional individual
#   Mandato    →  forma en que el Engine invoca un skill
#   Archivo    →  implementación física del skill
#
# Compatibilidad interna (no romper mandatos existentes):
#   SKILL · SKILLS · CAPACIDAD · CAPACIDADES
#
# ---------------------------------------------------------------
# AUTORIDAD DE EJECUCIÓN
# ---------------------------------------------------------------
#
# El Engine es la única autoridad que ejecuta los skills
# expuestos por CE.
# CE únicamente los descubre, valida y expone.
#
# CE nunca toma decisiones.
# CE nunca selecciona un skill.
# CE nunca coordina un ciclo.
# CE nunca interpreta una petición.
#
# Secuencia:
#
#   L4
#    ↓
#   Engine decide
#    ↓
#   Engine consulta CE
#    ↓
#   CE expone skills
#    ↓
#   Engine ejecuta el skill elegido (mandato)
#
# ---------------------------------------------------------------
# MÓDULOS vs CAPACIDAD CE
# ---------------------------------------------------------------
#
# Los módulos representan autoridades funcionales de dominio:
#   AX → conocimiento
#   CA → cálculo
#   CH → registro
#   TT → verdad
#   SF → identidad de fase / elección
#
# CE representa otra categoría:
#   capacidad estructural interna del Engine.
#
# No compite con ningún módulo. Los utiliza cuando Engine
# ejecuta un skill que los invoca.
#
# ---------------------------------------------------------------
# INVENTARIO OPERATIVO
# ---------------------------------------------------------------
#
# Oficio de CE: mantener el inventario operativo de las
# capacidades nativas del Engine.
# El descubrimiento automático de *.py es el mecanismo
# para mantener dicho inventario actualizado.
#
# ---------------------------------------------------------------
# API — COMPATIBILIDAD Y FUTURO
# ---------------------------------------------------------------
#
# skills() es el nombre histórico de la API.
# En futuras versiones podrá coexistir con:
#   procedimientos()
#   competencias()
# manteniendo skills() como alias permanente por compatibilidad.
#
# Preparación documentada (no implementada aún):
#   resolver(id)  /  existe(id)
# para consultas futuras del Engine.
#
# ---------------------------------------------------------------
# REQUISITO
# ---------------------------------------------------------------
#
# "CE" debe figurar en ROLES de core/engine.py.
#
# ===============================================================

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# ===============================================================
# SECCIÓN 1 — RUTAS Y CONSTANTES DE CONTENEDOR
# ===============================================================

_DIR = Path(__file__).resolve().parent
_CAP = _DIR

_ID = "CE"
_NOMBRE = "capacidades_engine"
_ROL = "CE"
_VERSION = "1.2"
_VERSION_CONTRATO = "1.0"
_ESQUEMA = "VPSI-CONTRACT-1.0"
_ESTABILIDAD = "ESTABLE"
_COMPATIBLE_DESDE = "1.0"
_API_ENGINE = ">=1.0"


# ===============================================================
# SECCIÓN 2 — CARGA Y META DE SKILLS
# ===============================================================

def _extraer_meta(mod: Any) -> Optional[Dict[str, Any]]:
    """
    Acepta SKILL / CAPACIDAD (dict) o SKILLS / CAPACIDADES (list).
    Compatibilidad con mandatos existentes.
    Normaliza descripcion <- enunciado si hace falta.
    """
    for attr in ("SKILL", "CAPACIDAD", "SKILLS", "CAPACIDADES"):
        raw = getattr(mod, attr, None)
        candidatos: List[Dict[str, Any]] = []
        if isinstance(raw, dict):
            candidatos = [raw]
        elif isinstance(raw, list):
            candidatos = [x for x in raw if isinstance(x, dict)]
        for meta in candidatos:
            sid = str(meta.get("id") or "").strip().lower()
            if not sid:
                continue
            meta = dict(meta)
            if not str(meta.get("descripcion") or "").strip():
                for alt in ("enunciado", "descripcion_larga", "nota"):
                    if str(meta.get(alt) or "").strip():
                        meta["descripcion"] = str(meta[alt]).strip()
                        break
            if not str(meta.get("nombre") or "").strip():
                meta["nombre"] = sid
            if not str(meta.get("version") or "").strip():
                meta["version"] = "1.0"
            if not str(meta.get("descripcion") or "").strip():
                meta["descripcion"] = (
                    "skill nativo del Engine: {0}".format(sid)
                )
            return meta
    return None


def _cargar_skills() -> Dict[str, Dict[str, Any]]:
    """
    Lee TODOS los *.py del directorio CE.
    Cada archivo válido implementa uno o más skills de la
    capacidad estructural CE. Engine tiene derecho a ver cada uno.
    """
    hallado: Dict[str, Dict[str, Any]] = {}
    if not _CAP.is_dir():
        return hallado

    for f in sorted(_CAP.glob("*.py")):
        if f.name.startswith("_"):
            continue
        clave = "ce_skill_{0}".format(f.stem)
        spec = importlib.util.spec_from_file_location(clave, str(f))
        if spec is None or spec.loader is None:
            hallado[f.stem] = {"archivo": f.name, "error": "spec_invalido"}
            continue
        mod = importlib.util.module_from_spec(spec)
        sys.modules[clave] = mod
        try:
            spec.loader.exec_module(mod)
        except Exception as e:
            hallado[f.stem] = {
                "archivo": f.name,
                "error": "{0}: {1}".format(type(e).__name__, e),
            }
            continue

        meta = _extraer_meta(mod)
        if meta is None:
            hallado[f.stem] = {
                "archivo": f.name,
                "error": "sin SKILL/CAPACIDAD con id",
            }
            continue

        sid = str(meta["id"]).strip().lower()
        hallado[sid] = {
            "archivo": f.name,
            "id": sid,
            "nombre": meta.get("nombre"),
            "version": str(meta.get("version") or "1.0"),
            "descripcion": str(meta.get("descripcion") or ""),
            "oficio": meta.get("oficio"),
            "material": meta.get("material"),
            "requiere_catalogo": meta.get("requiere_catalogo"),
            "raw": meta,
        }
    return hallado


def _validar_skills(hallado: Dict[str, Dict[str, Any]]) -> List[str]:
    errores: List[str] = []
    por_id: Dict[str, List[str]] = {}
    for sid, meta in sorted(hallado.items()):
        if meta.get("error"):
            if "sin SKILL" not in str(meta.get("error")):
                errores.append("{0}: {1}".format(sid, meta["error"]))
            continue
        for k in ("id", "nombre", "version", "descripcion"):
            if not str(meta.get(k) or "").strip():
                errores.append(
                    "skill '{0}': falta '{1}'".format(sid, k)
                )
        por_id.setdefault(sid, []).append(meta.get("archivo") or sid)
    for sid, archivos in por_id.items():
        if len(archivos) > 1:
            errores.append(
                "id '{0}' repetido en {1}".format(sid, archivos)
            )
    return errores


# ===============================================================
# SECCIÓN 3 — API PÚBLICA (skills / ids / por_id / archivos)
# ===============================================================

def skills() -> List[Dict[str, Any]]:
    """
    Todos los skills válidos de la capacidad CE — a disposición
    del Engine.

    Nombre histórico de la API.
    En futuras versiones podrá coexistir con:
      procedimientos()
      competencias()
    manteniendo skills() como alias permanente por compatibilidad.

    Preparación futura (no implementada): resolver(id) / existe(id).
    """
    hallado = _cargar_skills()
    out: List[Dict[str, Any]] = []
    for sid, meta in sorted(hallado.items()):
        if meta.get("error"):
            continue
        out.append({
            "id": meta.get("id"),
            "nombre": meta.get("nombre"),
            "version": meta.get("version"),
            "descripcion": meta.get("descripcion"),
            "archivo": meta.get("archivo"),
            "oficio": meta.get("oficio"),
            "material": meta.get("material"),
        })
    return out


def ids() -> List[str]:
    """Todos los ids de skills — Engine los usa cuando quiera."""
    return [s["id"] for s in skills() if s.get("id")]


def por_id(skill_id: str) -> Optional[Dict[str, Any]]:
    if not skill_id:
        return None
    clave = str(skill_id).strip().lower()
    for s in skills():
        if s.get("id") == clave:
            return s
    return None


def listar_archivos() -> List[str]:
    """
    Nombres de todo *.py del directorio CE.
    Archivo = implementación física del skill.
    """
    if not _CAP.is_dir():
        return []
    return [
        p.name for p in sorted(_CAP.glob("*.py"))
        if not p.name.startswith("_")
    ]


# ===============================================================
# SECCIÓN 4 — CENTINELA (barrer / verificar)
# ===============================================================

def barrer() -> Dict[str, Any]:
    """
    Centinela: ¿el inventario operativo de skills de CE es coherente?
    No calcula. No deposita. No restringe el uso.
    No decide. No selecciona. No coordina. No interpreta.
    No ejecuta skills (solo Engine ejecuta).
    """
    hallado = _cargar_skills()
    errores = _validar_skills(hallado)
    lista_ids = [
        sid for sid, m in sorted(hallado.items()) if not m.get("error")
    ]
    archivos = listar_archivos()
    notas: List[str] = []
    if not _CAP.is_dir():
        notas.append("directorio CE no existe")
    elif not lista_ids:
        notas.append(
            "ningún skill válido; archivos en CE: {0}".format(
                archivos or "(ninguno)"
            )
        )
        for sid, m in hallado.items():
            if m.get("error"):
                notas.append("  {0}: {1}".format(sid, m["error"]))

    return {
        "id": _ID,
        "nombre": _NOMBRE,
        "contenedor": _NOMBRE,
        "rol": _ROL,
        "version": _VERSION,
        "version_contrato": _VERSION_CONTRATO,
        "esquema": _ESQUEMA,
        "estabilidad": _ESTABILIDAD,
        "coherente": not errores,
        "errores": errores,
        "choques": [],
        "ids": lista_ids,
        "n": len(lista_ids),
        "archivos": archivos,
        "notas": notas,
        "ruta_capacidades": str(_CAP),
        "nota": (
            "CE es la capacidad estructural del Engine que agrupa "
            "skills nativos. Engine es la única autoridad de ejecución. "
            "CE solo descubre, valida y expone."
        ),
    }


def verificar() -> Dict[str, Any]:
    return barrer()


# ===============================================================
# SECCIÓN 5 — INVENTARIO (forma mínima contractual)
# ===============================================================

def inventario(peticion: Any = None) -> Dict[str, Any]:
    """
    Inventario operativo de las capacidades nativas del Engine
    expuestas por CE. El descubrimiento automático mantiene
    este inventario actualizado.

    Forma mínima alineada a VPSI-CONTRACT-1.0:
      id, nombre, rol, version, version_contrato, esquema,
      estabilidad, + campos propios de CE.
    """
    b = barrer()
    return {
        "id": _ID,
        "nombre": _NOMBRE,
        "contenedor": _NOMBRE,
        "rol": _ROL,
        "version": _VERSION,
        "version_contrato": _VERSION_CONTRATO,
        "esquema": _ESQUEMA,
        "estabilidad": _ESTABILIDAD,
        "compatible_desde": _COMPATIBLE_DESDE,
        "api_engine": _API_ENGINE,
        "ids": b.get("ids"),
        "n": b.get("n"),
        "archivos": b.get("archivos"),
        "coherente": b.get("coherente"),
        "skills": skills(),
        "notas": b.get("notas"),
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "funcion": (
            "Capacidad estructural del Engine. "
            "Mantiene el inventario operativo de skills nativos. "
            "Cada archivo implementa uno o más skills. "
            "Engine es la única autoridad que los ejecuta. "
            "CE no calcula, no deposita, no decide, no selecciona."
        ),
    }


def verificar_salida(salida: Any) -> bool:
    if not isinstance(salida, dict):
        return False
    return "id" in salida or "coherente" in salida or "ids" in salida

# ===============================================================
# SECCIÓN 6 — CONTENEDOR (contrato exclusivo de Engine)
# ===============================================================

CONTENEDOR: Dict[str, Any] = {
    # ============================================================
    # ESQUEMA
    # ============================================================
    "esquema": _ESQUEMA,
    "version_contrato": _VERSION_CONTRATO,
    "version_modulo": _VERSION,
    "estabilidad": _ESTABILIDAD,
    "compatible_desde": _COMPATIBLE_DESDE,
    "api_engine": _API_ENGINE,

    # ============================================================
    # IDENTIDAD
    # ============================================================
    "id": _ID,
    "nombre": _NOMBRE,
    "rol": _ROL,
    "descripcion": (
        "Capacidad estructural del Engine: órgano único que agrupa "
        "múltiples skills nativos. Así como un brazo posee varias "
        "habilidades sin dejar de ser un solo órgano, CE agrupa skills "
        "sin ser un módulo de dominio. Los archivos son implementación "
        "física; los skills son competencias operativas; el mandato es "
        "la forma en que Engine los invoca. Engine no pide permiso a CE: "
        "los skills forman parte de su propia estructura. "
        "CE mantiene el inventario operativo de esas capacidades nativas."
    ),

    # ============================================================
    # PROPÓSITO
    # ============================================================
    "funcion": (
        "Mantener el inventario operativo de skills nativos del Engine. "
        "El descubrimiento automático de *.py actualiza ese inventario. "
        "Validar forma mínima y exponer ids/skills a Engine. "
        "No calcular. No depositar. No ejecutar. No decidir."
    ),
    "no_hace": [
        "No toma decisiones",
        "No selecciona skills",
        "No ejecuta skills (solo Engine ejecuta)",
        "No coordina ciclos",
        "No interpreta peticiones",
        "No calcula C / L / K / Tru",
        "No deposita evidencia",
        "No orquesta el sistema",
        "No compite con módulos de dominio (AX, CA, CH, TT, SF, …)",
    ],

    # ============================================================
    # AUTORIDAD
    # ============================================================
    "autoridad": [
        "Mantener el inventario operativo de skills nativos del Engine",
        "Descubrir y validar forma mínima de cada skill",
        "Exponer ids y skills a Engine",
        "Reportar estado e inventario propios",
    ],

    # ============================================================
    # CONOCIMIENTO EXPORTABLE
    # ============================================================
    "conocimiento_exportable": [
        "skills",
        "ids",
        "por_id",
        "listar_archivos",
        "inventario",
        "barrer",
        "verificar",
    ],

    # ============================================================
    # DEPENDENCIAS
    # ============================================================
    "requiere": [],

    # ============================================================
    # AUTORIZACIÓN AL ENGINE (TODOS LOS PERMISOS)
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
        "listar_skills",
        "listar_ids",
        "obtener_por_id",
        "listar_archivos",
        "obtener_inventario",
        "verificar_coherencia",
    ],

    # ============================================================
    # CAPACIDADES
    # ============================================================
    "capacidades": {
        "verificar": verificar,
        "barrer": barrer,
        "inventario": inventario,
        "skills": skills,
        "ids": ids,
        "por_id": por_id,
        "listar_archivos": listar_archivos,
        "verificar_salida": verificar_salida,
    },

    # ============================================================
    # METADATOS DE CAPACIDADES (1:1 OBLIGATORIO)
    # ============================================================
    "capacidades_meta": {
        "verificar": {
            "descripcion": (
                "Alias de barrer. ¿El inventario operativo de skills "
                "de CE es coherente?"
            ),
            "entrada": "ninguna",
            "salida": "dict con id, nombre, rol, version, coherente, ids, errores",
        },
        "barrer": {
            "descripcion": (
                "Centinela de CE: valida forma de skills nativos. "
                "No decide, no ejecuta, no restringe uso."
            ),
            "entrada": "ninguna",
            "salida": "dict con id, nombre, rol, version, coherente, ids, n, archivos",
        },
        "inventario": {
            "descripcion": (
                "Inventario operativo de skills nativos del Engine "
                "expuestos por la capacidad CE. Incluye encabezado "
                "contractual completo (id, nombre, rol, version, …)."
            ),
            "entrada": "peticion opcional",
            "salida": (
                "dict con id, nombre, rol, version, version_contrato, "
                "esquema, estabilidad, ids, n, archivos, skills, coherente"
            ),
        },
        "skills": {
            "descripcion": (
                "Lista de skills válidos (nombre histórico de la API). "
                "Futuro: podrá coexistir con procedimientos()/competencias() "
                "como alias. Preparación: resolver(id)/existe(id)."
            ),
            "entrada": "ninguna",
            "salida": "list[dict] con id, nombre, version, descripcion, archivo",
        },
        "ids": {
            "descripcion": "Ids de todos los skills válidos de CE.",
            "entrada": "ninguna",
            "salida": "list[str]",
        },
        "por_id": {
            "descripcion": "Resuelve un skill por id.",
            "entrada": "skill_id: str",
            "salida": "dict del skill o None",
        },
        "listar_archivos": {
            "descripcion": (
                "Nombres de *.py del directorio CE "
                "(implementación física de los skills)."
            ),
            "entrada": "ninguna",
            "salida": "list[str]",
        },
        "verificar_salida": {
            "descripcion": "Comprueba forma mínima de una salida de CE.",
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
    "estados_validos": [
        "NO_INICIADO",
        "OPERATIVO",
        "DEGRADADO",
        "RECHAZADO",
    ],

    # ============================================================
    # INVARIANTES
    # ============================================================
    "invariantes": [
        "el id del módulo nunca cambia",
        "el rol nunca cambia",
        "CE es una capacidad estructural; los skills son competencias operativas",
        "Engine es la única autoridad que ejecuta los skills expuestos por CE",
        "CE únicamente descubre, valida y expone skills",
        "CE no toma decisiones ni selecciona skills",
        "CE no coordina ciclos ni interpreta peticiones",
        "las capacidades declaradas son callables tras la resolución",
        "este módulo no modifica el estado de otros módulos",
        "este módulo no inventa capacidades no declaradas en CONTENEDOR",
        "este módulo siempre puede reportar su propio estado",
        "CE debe figurar en ROLES de core/engine.py",
        "inventario() siempre incluye id, nombre, rol, version del CONTENEDOR",
    ],

}  # <--- CIERRE FINAL

# ===============================================================
# FIN CONTENEDOR
# ===============================================================
