# ===============================================================
# VPSI-TRUTH — modules/interfaz/__init__.py
# ===============================================================
#
# MÓDULO:              interfaz
# ID:                  UI
# Rol:                 UI
# Versión módulo:      1.0
# Versión contrato:    1.0
# Esquema contrato:    VPSI-CONTRACT-1.0
# Estabilidad:         ESTABLE
# Compatible desde:    1.0
# API Engine:          >=1.0
#
# Función:
#   Diseño de presentación del sistema.
#   Compone descripciones de interfaz bajo pedido explícito.
#   Inventaria paquetes de herramientas bajo paquetes/.
#   Vela la coherencia de sus propios archivos.
#
# Qué NO hace:
#   No calcula Tru. No escribe C/L/K. No orquesta el ciclo.
#   No aprueba su propia salida de diseño.
#
# ===============================================================


# ===============================================================
# Parte 1 — IMPORTACIONES
# ===============================================================

from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict, List, Optional


# ===============================================================
# Parte 2 — CONSTANTES DE IDENTIDAD
# ===============================================================

ID_MODULO = "UI"
NOMBRE_MODULO = "interfaz"
ROL_MODULO = "UI"

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
    "las capacidades declaradas son siempre callables tras la resolución",
    "este módulo no modifica el estado de otros módulos",
    "este módulo no inventa capacidades no declaradas en CONTENEDOR",
    "no calcula ni modifica C, L, K ni Tru",
    "no orquesta el ciclo Engine",
    "toda salida de componer es auditable por Centinela (declaración)",
    "presentar no forma parte de v1.0",
    "los estados de operación de componer (PROPUESTO|PARCIAL|RETENIDO) son distintos de los estados del módulo",
)

_DIR = Path(__file__).parent
_PAQUETES = _DIR / "paquetes"

SUPERFICIES_ADMITIDAS = ("web", "desktop", "mobile", "cli", "embebido")

_ZONAS_CANONICAS = (
    "contexto",
    "estado_marco",
    "reporte_simple",
    "reporte_detalle",
    "sistema",
    "centinela",
    "correlacion",
)

ESTADOS_OPERACION = ("PROPUESTO", "PARCIAL", "RETENIDO")


# ===============================================================
# Parte 3 — CONTRATO OFICIAL (CONTENEDOR)
# ===============================================================

CONTENEDOR: Dict[str, Any] = {

    # -----------------------------------------------------------
    # Parte 3.1 — Esquema y versiones
    # -----------------------------------------------------------
    "esquema": ESQUEMA_CONTRATO,
    "version_contrato": VERSION_CONTRATO,
    "version_modulo": VERSION_MODULO,
    "estabilidad": ESTABILIDAD,
    "compatible_desde": COMPATIBLE_DESDE,
    "api_engine": API_ENGINE,

    # -----------------------------------------------------------
    # Parte 3.2 — Identidad
    # -----------------------------------------------------------
    "id": ID_MODULO,
    "nombre": NOMBRE_MODULO,
    "rol": ROL_MODULO,
    "descripcion": (
        "Diseño de presentación del sistema. Compone descripciones de "
        "interfaz bajo un pedido explícito y lo observable (CACHE). "
        "Cero actuación sobre evaluación."
    ),

    # -----------------------------------------------------------
    # Parte 3.3 — Propósito
    # -----------------------------------------------------------
    "funcion": (
        "Diseña descripciones de interfaz correlacionadas al mecanismo; "
        "vela sus paquetes; no calcula Tru."
    ),
    "no_hace": [
        "No calcula Tru_total ni Tru_Ri",
        "No escribe C/L/K",
        "No orquesta el ciclo Engine",
        "No aprueba su propia salida de diseño",
        "No inventa controles sin componente real",
    ],

    # -----------------------------------------------------------
    # Parte 3.4 — Autoridad
    # -----------------------------------------------------------
    "autoridad": [
        "Componer descripciones de interfaz",
        "Inventariar paquetes de diseño",
        "Observar pedido + evidencia CACHE",
        "Verificar coherencia interna de paquetes y contrato",
        "Reportar estado propio",
    ],

    # -----------------------------------------------------------
    # Parte 3.5 — Conocimiento exportable
    # -----------------------------------------------------------
    "conocimiento_exportable": [
        "componer", "observar", "inventario", "inventario_paquetes",
        "barrer", "verificar", "axiomas",
    ],

    # -----------------------------------------------------------
    # Parte 3.6 — Dependencias
    # -----------------------------------------------------------
    "requiere": [],

    # -----------------------------------------------------------
    # Parte 3.7 — Acceso y validación
    # -----------------------------------------------------------
    "acceso_archivos": ["paquetes/"],
    "validar_esquema": [],
    "acceso": {
        "nivel": "limitado",
        "descripcion": "Acceso de lectura a paquetes/ del módulo",
    },

    # -----------------------------------------------------------
    # Parte 3.8 — Consultas soportadas
    # -----------------------------------------------------------
    "consultas_soportadas": [
        "componer", "observar", "inventario", "inventario_paquetes",
        "barrer", "verificar",
    ],

    # -----------------------------------------------------------
    # Parte 3.9 — Capacidades
    # -----------------------------------------------------------
    "capacidades": {},

    # -----------------------------------------------------------
    # Parte 3.10 — Metadatos de capacidades
    # -----------------------------------------------------------
    "capacidades_meta": {
        "verificar": {
            "descripcion": "Alias de barrer. Verifica coherencia interna del módulo.",
            "entrada": "ninguna",
            "salida": "dict con id, nombre, rol, coherente, choques, errores, advertencias, paquetes",
            "validar_esquema": ["*"],
            "acceso_archivos": ["*"],
        },
        "barrer": {
            "descripcion": "Centinela de carpeta + verificación estructural del CONTENEDOR.",
            "entrada": "ninguna",
            "salida": "dict con id, nombre, rol, coherente, choques, errores, advertencias, paquetes_n",
            "validar_esquema": ["*"],
            "acceso_archivos": ["*"],
        },
        "componer": {
            "descripcion": "Genera descripción de interfaz (esquema). No inventa controles.",
            "entrada": "peticion: dict con O_uso, superficie, zonas, layout",
            "salida": "dict con id, nombre, rol, estado (PROPUESTO|PARCIAL|RETENIDO), esquema, observacion, auditable_por_centinela",
            "validar_esquema": ["*"],
            "acceso_archivos": ["*"],
        },
        "inventario": {
            "descripcion": "Inventario estructural del módulo UI.",
            "entrada": "peticion opcional",
            "salida": "dict con id, nombre, rol, version, superficies, zonas, paquetes, capacidades",
            "validar_esquema": ["*"],
            "acceso_archivos": ["*"],
        },
        "inventario_paquetes": {
            "descripcion": "Lista los paquetes descubiertos bajo paquetes/.",
            "entrada": "ninguna",
            "salida": "dict con id, nombre, rol, dir, n, paquetes",
            "validar_esquema": ["*"],
            "acceso_archivos": ["*"],
        },
        "observar": {
            "descripcion": "Reúne pedido + evidencia CACHE (solo lectura).",
            "entrada": "pedido y cache_snapshot opcionales",
            "salida": "dict con id, nombre, rol, pedido, evidencia_cache",
            "validar_esquema": ["*"],
            "acceso_archivos": ["*"],
        },
        "axiomas": {
            "descripcion": "Declaraciones operativas del módulo UI.",
            "entrada": "ninguna",
            "salida": "list[dict] de axiomas operativos",
            "validar_esquema": ["*"],
            "acceso_archivos": ["*"],
        },
    },

    # -----------------------------------------------------------
    # Parte 3.11 — Autorización al Engine
    # -----------------------------------------------------------
    "autoriza_engine": {
        "leer": True,
        "ejecutar": True,
        "consultar": True,
        "recombinar": False,
        "reportar": True,
        "auditar": True,
        "inventariar": True,
        "alterar": False,
        "metricas": True,
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
        "diagnostico": True,
        "reporte": True,
        "crear": False,
        "actualizar": False,
        "validar_esquema": True,
        "validar": True,
        "procesar": False,
        "analizar": False,
        "generar": True,
        "exportar": True,
        "importar": False,
        "respaldar": False,
        "recuperar": False,
        "sincronizar": False,
        "monitorear": True,
        "acceso_archivos": True,
    },

    # -----------------------------------------------------------
    # Parte 3.12 — Reporting
    # -----------------------------------------------------------
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
    },

    # -----------------------------------------------------------
    # Parte 3.13 — Estados válidos
    # -----------------------------------------------------------
    "estados_validos": list(ESTADOS_VALIDOS),

    # -----------------------------------------------------------
    # Parte 3.14 — Invariantes
    # -----------------------------------------------------------
    "invariantes": list(INVARIANTES),
}


# ===============================================================
# Parte 4 — CÓDIGO PRIVADO
# ===============================================================

def _leer_manifiesto(ruta: Path) -> Optional[Dict[str, Any]]:
    for nombre in ("manifiesto.json", "manifest.json", "paquete.json"):
        f = ruta / nombre
        if f.is_file():
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                return data if isinstance(data, dict) else None
            except Exception:
                return {"_error": f"manifiesto ilegible: {f.name}"}
    if (ruta / "__init__.py").is_file() or any(ruta.glob("*.py")):
        return {
            "id": ruta.name,
            "nombre": ruta.name,
            "version": "0.0",
            "superficie": ["web"],
            "implicit": True,
        }
    return None

def _descubrir_paquetes() -> Dict[str, Dict[str, Any]]:
    hallado: Dict[str, Dict[str, Any]] = {}
    if not _PAQUETES.is_dir():
        return hallado
    for child in sorted(_PAQUETES.iterdir()):
        if not child.is_dir() or child.name.startswith(("_", ".")):
            continue
        meta = _leer_manifiesto(child)
        if meta is None:
            hallado[child.name] = {
                "id": child.name,
                "error": "sin manifiesto ni código",
                "ruta": str(child),
            }
            continue
        if meta.get("_error"):
            hallado[child.name] = {
                "id": child.name,
                "error": meta["_error"],
                "ruta": str(child),
            }
            continue
        pid = str(meta.get("id") or child.name)
        hallado[pid] = {
            "id": pid,
            "nombre": meta.get("nombre") or child.name,
            "version": str(meta.get("version") or "0.0"),
            "superficies": list(meta.get("superficies") or meta.get("superficie") or ["web"]),
            "componentes": list(meta.get("componentes") or []),
            "ruta": str(child),
            "implicit": bool(meta.get("implicit")),
        }
    return hallado

def _detectar_choques_paquetes(paquetes: Dict[str, Dict[str, Any]]) -> List[str]:
    """Validación declarativa del manifiesto. No analiza código ejecutable."""
    choques: List[str] = []
    for pid, meta in paquetes.items():
        if meta.get("error"):
            choques.append(f"paquete '{pid}': {meta['error']}")
            continue
        for s in meta.get("superficies") or []:
            if s not in SUPERFICIES_ADMITIDAS:
                choques.append(f"paquete '{pid}': superficie no admitida {s!r}")
        for c in meta.get("componentes") or []:
            cl = str(c).lower()
            if any(x in cl for x in ("tru_total", "tru_ri", "escribir_k", "set_c", "set_l", "forzar_ok")):
                choques.append(f"paquete '{pid}': componente sospechoso (declarativo): {c!r}")
    return choques


# ===============================================================
# Parte 5 — CAPACIDADES PÚBLICAS
# ===============================================================

def barrer() -> Dict[str, Any]:
    """Centinela de carpeta + verificación estructural del CONTENEDOR."""
    errores: List[str] = []
    advertencias: List[str] = []

    if not isinstance(CONTENEDOR, dict):
        errores.append("CONTENEDOR ausente o no es dict")
    else:
        if CONTENEDOR.get("id") != ID_MODULO:
            errores.append(f"id inválido: {CONTENEDOR.get('id')}")
        if CONTENEDOR.get("nombre") != NOMBRE_MODULO:
            errores.append(f"nombre inválido: {CONTENEDOR.get('nombre')}")
        if CONTENEDOR.get("rol") != ROL_MODULO:
            errores.append(f"rol inválido: {CONTENEDOR.get('rol')}")
        if CONTENEDOR.get("esquema") != ESQUEMA_CONTRATO:
            errores.append(f"esquema inválido: {CONTENEDOR.get('esquema')}")
        if str(CONTENEDOR.get("version_contrato")) != VERSION_CONTRATO:
            errores.append(f"version_contrato inválida: {CONTENEDOR.get('version_contrato')}")
        if not CONTENEDOR.get("version_modulo"):
            errores.append("version_modulo vacía")

        caps = CONTENEDOR.get("capacidades") or {}
        meta_caps = CONTENEDOR.get("capacidades_meta") or {}
        if not isinstance(caps, dict):
            errores.append("capacidades debe ser dict")
        if not isinstance(meta_caps, dict):
            errores.append("capacidades_meta debe ser dict")
        else:
            for k in caps:
                if k not in meta_caps:
                    errores.append(f"capacidad '{k}' sin capacidades_meta")
                else:
                    entrada = meta_caps[k]
                    for campo in ("descripcion", "entrada", "salida", "validar_esquema", "acceso_archivos"):
                        if campo not in entrada:
                            errores.append(f"capacidades_meta['{k}'] falta '{campo}'")

        if not CONTENEDOR.get("invariantes"):
            errores.append("invariantes ausentes o vacíos")

    paquetes = _descubrir_paquetes()
    choques = _detectar_choques_paquetes(paquetes)

    if not _PAQUETES.exists():
        advertencias.append("paquetes/ aún no existe (vacío legítimo hasta montar herramientas)")

    coherente = len(errores) == 0 and len(choques) == 0

    return {
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "coherente": coherente,
        "choques": choques,
        "errores": errores,
        "advertencias": advertencias,
        "paquetes_n": len(paquetes),
        "paquetes": sorted(paquetes.keys()),
        "superficies_admitidas": list(SUPERFICIES_ADMITIDAS),
    }

def verificar() -> Dict[str, Any]:
    """Alias contractual de barrer."""
    return barrer()

def observar(
    pedido: Optional[Dict[str, Any]] = None,
    cache_snapshot: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Reúne pedido + evidencia CACHE (solo lectura)."""
    pedido = dict(pedido or {})
    snap = dict(cache_snapshot or {})
    return {
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "pedido": {
            "O_uso": pedido.get("O_uso") or pedido.get("contexto") or pedido.get("enunciado") or pedido.get("descripcion"),
            "superficie": pedido.get("superficie") or "web",
            "zonas_solicitadas": list(pedido.get("zonas") or pedido.get("paneles") or []),
            "restricciones": list(pedido.get("restricciones") or []),
        },
        "evidencia_cache": {
            "disponible": bool(snap),
            "claves": sorted(snap.keys()) if snap else [],
            "ciclo_id": snap.get("ciclo_id"),
            "estado_sistema": snap.get("estado") or snap.get("estado_engine"),
            "contenido": snap,
        },
        "nota": "Observación de solo lectura. Sin O_uso claro la composición queda PARCIAL.",
    }

def componer(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Genera descripción de interfaz (esquema). No inventa controles."""
    peticion = dict(peticion or {})
    obs = observar(peticion, peticion.get("cache_snapshot"))
    o_uso = obs["pedido"]["O_uso"]
    superficie = obs["pedido"]["superficie"]

    if superficie not in SUPERFICIES_ADMITIDAS:
        return {
            "id": ID_MODULO,
            "nombre": NOMBRE_MODULO,
            "rol": ROL_MODULO,
            "estado": "RETENIDO",
            "razon": f"superficie no admitida: {superficie!r}",
            "esquema": None,
            "auditable_por_centinela": True,
            "nota": "Estado de operación RETENIDO (no es estado del módulo)",
        }

    if not o_uso or not str(o_uso).strip():
        return {
            "id": ID_MODULO,
            "nombre": NOMBRE_MODULO,
            "rol": ROL_MODULO,
            "estado": "PARCIAL",
            "razon": "sin O_uso / pedido de diseño",
            "observacion": obs,
            "esquema": None,
            "auditable_por_centinela": True,
            "nota": "Estado de operación PARCIAL (no es estado del módulo)",
        }

    zonas_req = obs["pedido"]["zonas_solicitadas"]
    zonas: List[Dict[str, Any]] = []
    for z in zonas_req:
        zid = str(z)
        if zid not in _ZONAS_CANONICAS:
            zonas.append({
                "id": zid,
                "canonica": False,
                "aviso": "zona no canónica — requiere validación de Centinela",
            })
        else:
            zonas.append({
                "id": zid,
                "canonica": True,
                "actuacion_evaluacion": False,
            })

    paquetes = _descubrir_paquetes()
    paquetes_ok = {k: v for k, v in paquetes.items() if not v.get("error")}

    esquema = {
        "tipo": "descripcion_interfaz",
        "version": "1.0",
        "O_uso": str(o_uso).strip(),
        "superficie": superficie,
        "layout": peticion.get("layout") or "libre",
        "zonas": zonas,
        "paquetes_aplicables": [
            pid for pid, meta in paquetes_ok.items()
            if superficie in (meta.get("superficies") or [])
        ],
        "prohibido_en_ui": list(CONTENEDOR.get("no_hace") or []),
        "mapeo_mecanismo_declarativo": {
            "nota": "Referencias declarativas. No verificadas en runtime por este módulo.",
            "contexto": "modules.contexto",
            "centinela": "core.centinela",
        },
    }
    return {
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "estado": "PROPUESTO",
        "observacion": obs,
        "esquema": esquema,
        "barrido_local": barrer(),
        "auditable_por_centinela": True,
        "nota": (
            "Estado de operación PROPUESTO (no es estado del módulo). "
            "Descripción de diseño únicamente. Centinela debe verificar antes de adoptar."
        ),
    }

def inventario_paquetes() -> Dict[str, Any]:
    paquetes = _descubrir_paquetes()
    return {
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "dir": str(_PAQUETES),
        "n": len(paquetes),
        "paquetes": paquetes,
    }

def inventario(peticion: Any = None) -> Dict[str, Any]:
    return {
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "superficies": list(SUPERFICIES_ADMITIDAS),
        "zonas_canonicas": list(_ZONAS_CANONICAS),
        "paquetes": inventario_paquetes(),
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "estados_operacion": list(ESTADOS_OPERACION),
        "nota": "presentar no forma parte de v1.0",
    }

def axiomas() -> List[Dict[str, Any]]:
    return [
        {
            "id": "UI-OP-1",
            "tipo": "axioma",
            "sujeto": "modulo_interfaz",
            "relacion": "compone_descripcion_y_no_calcula",
            "objeto": "Tru_ni_factores",
            "polaridad": True,
            "enunciado": "El módulo interfaz compone descripciones de presentación; no calcula ni modifica C, L, K ni Tru.",
            "depende_de": [],
            "gobierna": ["interfaz"],
        },
        {
            "id": "UI-OP-2",
            "tipo": "axioma",
            "sujeto": "composicion_de_interfaz",
            "relacion": "exige",
            "objeto": "pedido_O_uso_explicito",
            "polaridad": True,
            "enunciado": "Sin pedido de diseño (O_uso) no se inventa la interfaz completa; estado de operación PARCIAL.",
            "depende_de": [],
            "gobierna": ["interfaz"],
        },
        {
            "id": "UI-OP-3",
            "tipo": "axioma",
            "sujeto": "paquetes_de_diseno",
            "relacion": "deben",
            "objeto": "pasar_barrido_local_sin_actuacion_evaluacion",
            "polaridad": True,
            "enunciado": "Los paquetes bajo interfaz/paquetes/ no pueden declarar componentes de actuación sobre evaluación (validación declarativa del manifiesto).",
            "depende_de": [],
            "gobierna": ["interfaz"],
        },
        {
            "id": "UI-OP-4",
            "tipo": "axioma",
            "sujeto": "salida_de_componer",
            "relacion": "es",
            "objeto": "auditable_por_Centinela",
            "polaridad": True,
            "enunciado": "Toda descripción de interfaz es paquete verificable por Centinela antes de adoptarse. auditable_por_centinela es una declaración, no una garantía automática.",
            "depende_de": [],
            "gobierna": ["interfaz"],
        },
    ]


# ===============================================================
# Parte 6 — RESOLUCIÓN DE CAPACIDADES + EXPORTACIONES
# ===============================================================

_CAP_MAP = {
    "verificar": verificar,
    "barrer": barrer,
    "componer": componer,
    "inventario": inventario,
    "inventario_paquetes": inventario_paquetes,
    "observar": observar,
    "axiomas": axiomas,
}

def _resolver_capacidades(cont: Dict[str, Any]) -> None:
    resueltas: Dict[str, Any] = {}
    for nombre, ref in cont["capacidades"].items():
        if callable(ref):
            resueltas[nombre] = ref
            continue
        if isinstance(ref, str):
            if ref not in _CAP_MAP:
                raise Exception(f"{NOMBRE_MODULO}: capacidad '{nombre}' referencia inexistente: '{ref}'")
            fn = _CAP_MAP[ref]
            if not callable(fn):
                raise Exception(f"{NOMBRE_MODULO}: '{ref}' no es callable")
            resueltas[nombre] = fn
            continue
        raise Exception(f"{NOMBRE_MODULO}: capacidad '{nombre}' tiene tipo inválido")
    cont["capacidades"] = resueltas

# Materialización directa (compatible con Engine)
CONTENEDOR["capacidades"] = {
    "verificar": verificar,
    "barrer": barrer,
    "componer": componer,
    "inventario": inventario,
    "inventario_paquetes": inventario_paquetes,
    "observar": observar,
    "axiomas": axiomas,
}

__all__ = [
    "CONTENEDOR",
    "ID_MODULO",
    "NOMBRE_MODULO",
    "ROL_MODULO",
    "VERSION_MODULO",
    "SUPERFICIES_ADMITIDAS",
    "ESTADOS_OPERACION",
    "barrer",
    "verificar",
    "observar",
    "componer",
    "inventario",
    "inventario_paquetes",
    "axiomas",
]
