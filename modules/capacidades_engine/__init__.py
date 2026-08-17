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
# Jerarquía:
#   Engine → Capacidad (CE) → Skills / Mandatos → Archivos
#
# CE descubre, valida y expone skills.
# Solo Engine ejecuta.
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
from typing import Any, Dict, List, Optional

# ===============================================================
# FIN 1.1
# ===============================================================


# ===============================================================
# 1.2 — IDENTIDAD
# ===============================================================

ID_MODULO = "CE"
NOMBRE_MODULO = "capacidades_engine"
ROL_MODULO = "CE"

# ===============================================================
# FIN 1.2
# ===============================================================


# ===============================================================
# 1.3 — VERSIONES Y ESTABILIDAD
# ===============================================================

VERSION_MODULO = "1.2"
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
)

# ===============================================================
# FIN 1.5
# ===============================================================


# ===============================================================
# 1.6 — CONFIGURACIÓN
# ===============================================================

_DIR = Path(__file__).resolve().parent
_CAP = _DIR

# ===============================================================
# FIN 1.6
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
    # 5.3 — PROPÓSITO
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
    # 5.4 — AUTORIDAD
    # ============================================================
    "autoridad": [
        "Mantener el inventario operativo de skills nativos del Engine",
        "Descubrir y validar forma mínima de cada skill",
        "Exponer ids y skills a Engine",
        "Reportar estado e inventario propios",
    ],

    # ============================================================
    # 5.5 — CONOCIMIENTO EXPORTABLE
    # ============================================================
    "conocimiento_exportable": [
        "skills",
        "ids",
        "por_id",
        "listar_archivos",
        "inventario",
        "barrer",
        "verificar",
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
        "CT", "AX", "FO", "MC", "SF", "CA", "CX",
        "DI", "RE", "VX", "TX", "CH", "CIT", "TT",
        "CE", "CC",
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
    },

    # ============================================================
    # 5.11 — CONSULTAS SOPORTADAS
    # ============================================================
    "consultas_soportadas": [
        "listar_skills",
        "listar_ids",
        "obtener_por_id",
        "listar_archivos",
        "obtener_inventario",
        "verificar_coherencia",
        "ejecutar_total",
        "inspeccionar",
        "registrar_inventario",
    ],

    # ============================================================
    # 5.12 — CAPACIDADES
    # ============================================================
    "capacidades": {
        "verificar": "verificar",
        "barrer": "barrer",
        "inventario": "inventario",
        "skills": "skills",
        "ids": "ids",
        "por_id": "por_id",
        "listar_archivos": "listar_archivos",
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
            "descripcion": (
                "Alias de barrer. ¿El inventario operativo de skills "
                "de CE es coherente?"
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con id, nombre, rol, version, coherente, ids, errores"
            ),
            "acceso_archivos": ["*"],
        },
        "barrer": {
            "descripcion": (
                "Centinela de CE: valida forma de skills nativos. "
                "No decide, no ejecuta, no restringe uso."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con id, nombre, rol, version, coherente, "
                "ids, n, archivos"
            ),
            "acceso_archivos": ["acceso_archivos"],
        },
        "inventario": {
            "descripcion": (
                "Inventario operativo de skills nativos del Engine "
                "expuestos por la capacidad CE."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con id, nombre, rol, version, version_contrato, "
                "esquema, estabilidad, ids, n, archivos, skills, coherente"
            ),
            "acceso_archivos": ["*"],
        },
        "skills": {
            "descripcion": (
                "Lista de skills válidos (nombre histórico de la API)."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "list[dict] con id, nombre, version, descripcion, archivo"
            ),
            "acceso_archivos": ["*"],
        },
        "ids": {
            "descripcion": "Ids de todos los skills válidos de CE.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "list[str]",
            "acceso_archivos": ["*"],
        },
        "por_id": {
            "descripcion": "Resuelve un skill por id.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict del skill o None",
            "acceso_archivos": ["*"],
        },
        "listar_archivos": {
            "descripcion": (
                "Nombres de *.py del directorio CE "
                "(implementación física de los skills)."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "list[str]",
            "acceso_archivos": ["*"],
        },
        "verificar_salida": {
            "descripcion": "Comprueba forma mínima de una salida de CE.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "bool",
            "acceso_archivos": ["*"],
        },
        "ejecutar_total": {
            "descripcion": (
                "Autoridad total de ENGINE sobre CE. "
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
                "Capacidad meta de inspeccion estructural de CE. "
                "Expone constantes, capacidades, skills y estado "
                "sin alterar el contrato ni ejecutar skills."
            ),
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["acceso_archivos"],
            "salida": "dict con estructura, capacidades y estado del modulo",
            "acceso_archivos": ["acceso_archivos"],
        },
        "registrar_inventario": {
            "descripcion": (
                "Registra el inventario estructural de CE "
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
        "acceso_archivos": True,
        "validar_esquema": True,
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
# 7.1 — EXTRACCIÓN DE META
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

# ===============================================================
# FIN 7.1
# ===============================================================


# ===============================================================
# 7.2 — CARGA DE SKILLS
# ===============================================================

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

# ===============================================================
# FIN 7.2
# ===============================================================


# ===============================================================
# 7.3 — VALIDACIÓN DE SKILLS
# ===============================================================

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
# FIN 7.3
# ===============================================================


# ===============================================================
# 7.4 — VALIDACIÓN DEL CONTRATO
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
# FIN 7.4
# ===============================================================

# ===============================================================
# FIN PARTE 7
# ===============================================================


# ===============================================================
# PARTE 8 — CAPACIDADES PÚBLICAS
# ===============================================================

# ===============================================================
# 8.1 — SKILLS
# ===============================================================

def skills() -> List[Dict[str, Any]]:
    """
    Todos los skills válidos de la capacidad CE — a disposición
    del Engine. Nombre histórico de la API.
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

# ===============================================================
# FIN 8.1
# ===============================================================


# ===============================================================
# 8.2 — IDS
# ===============================================================

def ids() -> List[str]:
    """Todos los ids de skills — Engine los usa cuando quiera."""
    return [s["id"] for s in skills() if s.get("id")]

# ===============================================================
# FIN 8.2
# ===============================================================


# ===============================================================
# 8.3 — POR ID
# ===============================================================

def por_id(skill_id: str) -> Optional[Dict[str, Any]]:
    if not skill_id:
        return None
    clave = str(skill_id).strip().lower()
    for s in skills():
        if s.get("id") == clave:
            return s
    return None

# ===============================================================
# FIN 8.3
# ===============================================================


# ===============================================================
# 8.4 — LISTAR ARCHIVOS
# ===============================================================

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
# FIN 8.4
# ===============================================================


# ===============================================================
# 8.5 — BARRER
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
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "contenedor": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
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

# ===============================================================
# FIN 8.5
# ===============================================================


# ===============================================================
# 8.6 — VERIFICAR
# ===============================================================

def verificar() -> Dict[str, Any]:
    """Alias contractual real de barrer."""
    return barrer()

# ===============================================================
# FIN 8.6
# ===============================================================


# ===============================================================
# 8.7 — INVENTARIO
# ===============================================================

def inventario(peticion: Any = None) -> Dict[str, Any]:
    """
    Inventario operativo de las capacidades nativas del Engine
    expuestas por CE.
    """
    b = barrer()
    return {
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "contenedor": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "compatible_desde": COMPATIBLE_DESDE,
        "api_engine": API_ENGINE,
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

# ===============================================================
# FIN 8.7
# ===============================================================


# ===============================================================
# 8.8 — VERIFICAR SALIDA
# ===============================================================

def verificar_salida(salida: Any) -> bool:
    if not isinstance(salida, dict):
        return False
    return "id" in salida or "coherente" in salida or "ids" in salida

# ===============================================================
# FIN 8.8
# ===============================================================


# ===============================================================
# 8.9 — EJECUTAR TOTAL
# ===============================================================

def ejecutar_total(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Autoridad total de ENGINE sobre CE.
    Ejerce TODAS las unidades operativamente ejecutables del módulo
    conforme a su contrato e inventario.
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
        resultados["skills"] = skills()
    except Exception as e:
        errores_ejecucion.append("skills: {0}".format(e))
        resultados["skills"] = None

    try:
        resultados["ids"] = ids()
    except Exception as e:
        errores_ejecucion.append("ids: {0}".format(e))
        resultados["ids"] = None

    try:
        resultados["listar_archivos"] = listar_archivos()
    except Exception as e:
        errores_ejecucion.append("listar_archivos: {0}".format(e))
        resultados["listar_archivos"] = None

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
            "ejecutar_total ejerce autoridad total de ENGINE sobre CE. "
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
    Inspección estructural de CE.
    Expone contrato, skills y estado sin ejecutar skills.
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
            "ids": res_barrer.get("ids"),
            "n": res_barrer.get("n"),
            "archivos": res_barrer.get("archivos"),
            "errores": res_barrer.get("errores"),
        },
        "autoriza_engine": CONTENEDOR.get("autoriza_engine"),
        "reporting": CONTENEDOR.get("reporting"),
        "invariantes": list(INVARIANTES),
        "nota": (
            "inspeccionar expone estructura de CE sin ejecutar "
            "skills ni alterar el contrato."
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
    Registra el inventario estructural de CE como instantánea determinista.
    No altera evidencia.
    """
    inv = inventario(peticion)
    return {
        "id": ID_MODULO,
        "operacion": "registrar_inventario",
        "registrado": True,
        "inventario": inv,
        "nota": (
            "Instantánea determinista del inventario de CE. "
            "No modifica estado de skills ni evidencia."
        ),
    }

# ===============================================================
# FIN 8.11
# ===============================================================

# ===============================================================
# FIN PARTE 8
# ===============================================================


# ===============================================================
# PARTE 10 — RESOLUCIÓN ESTRICTA Y EXPORTACIONES
# ===============================================================

# ===============================================================
# 10.1 — MAPA DE CAPACIDADES
# ===============================================================

_CAP_MAP = {
    "verificar": verificar,
    "barrer": barrer,
    "inventario": inventario,
    "skills": skills,
    "ids": ids,
    "por_id": por_id,
    "listar_archivos": listar_archivos,
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
    "skills",
    "ids",
    "por_id",
    "listar_archivos",
    "barrer",
    "verificar",
    "inventario",
    "verificar_salida",
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
