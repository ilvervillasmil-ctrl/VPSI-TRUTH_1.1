# ===============================================================
# VPSI-TRUTH — modules/axiomas/__init__.py
# ===============================================================
#
# MÓDULO:              axiomas
# ID:                  AX
# Rol:                 AX
# Versión módulo:      9.6
# Versión contrato:    1.0
# Esquema contrato:    VPSI-CONTRACT-1.0
# Estabilidad:         ESTABLE
# Compatible desde:    9.5
# API Engine:          >=1.0
#
# Función:
#   Responsable del conocimiento axiomático del sistema.
#   Mantiene, valida, organiza y expone todas las declaraciones
#   oficiales del repositorio para cualquier módulo autorizado.
#
# Qué hace:
#   - Carga, normaliza y recolecta declaraciones de todos los archivos
#   - Detecta contradicción directa y de cota
#   - Expone generatividad (TR1 / capa canónica)
#   - Responde consultas por id, dominio, sujeto, relación, objeto
#   - Cita cualquier declaración del grafo
#   - Genera inventario, reporte y diagnóstico propios
#   - Notifica a DiagnosticoGlobal cuando hay choques o errores
#
# Qué NO hace:
#   - No calcula Tru_total ni Tru_Ri
#   - No clasifica entrada de usuario (eso es CX)
#   - No orquesta el sistema (eso es Engine)
#   - No genera reportes de otros módulos
#   - No modifica declaraciones ajenas
#
# Responsabilidad:
#   Ser la fuente oficial y coherente del conocimiento axiomático.
#
# Autoridad:
#   - Exponer cualquier axioma, lema, teorema, corolario o definición
#   - Responder consultas y citar lo que el grafo contenga
#   - Verificar coherencia interna
#   - Reportar estado, salud, inventario y diagnóstico propios
#
# Conocimiento exportable:
#   declaraciones, referencias, dependencias, dominios,
#   generatividad, choques, inventario, estado, reporte, diagnóstico
#
# Relación con Engine:
#   Engine descubre este CONTENEDOR, ejecuta solo las capacidades
#   declaradas y consolida el reporte que este módulo produce.
#
# Relación con Omega:
#   Omega no calcula nada de AX. Solo presenta lo que Engine entrega.
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

try:
    from core.diagnostico import DiagnosticoGlobal  # type: ignore
except Exception:  # noqa: BLE001
    DiagnosticoGlobal = None  # type: ignore

# ===============================================================
# FIN IMPORTACIONES
# ===============================================================


# ===============================================================
# CONSTANTES
# ===============================================================

ID_MODULO = "AX"
NOMBRE_MODULO = "axiomas"
ROL_MODULO = "AX"

VERSION_MODULO = "9.6"
VERSION_CONTRATO = "1.0"
ESQUEMA_CONTRATO = "VPSI-CONTRACT-1.0"

COMPATIBLE_DESDE = "9.5"
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
    "este módulo siempre puede reportar su propio estado",
)

OBLIGATORIOS = ("id", "tipo", "sujeto", "relacion", "objeto", "polaridad")
TIPOS = ("axioma", "lema", "teorema", "corolario", "definicion")

AXIOMA = "axioma"
LEMA = "lema"
TEOREMA = "teorema"
COROLARIO = "corolario"
DEFINICION = "definicion"

TRADUCCION_CLAVES = {
    "type": "tipo",
    "subject": "sujeto",
    "relation": "relacion",
    "object": "objeto",
    "polarity": "polaridad",
    "statement": "enunciado",
    "depends_on": "depende_de",
    "governs": "gobierna",
    "cota": "cota",
}

DOMINIOS_K_O = frozenset({
    "contexto", "ontologia", "epistemologia", "verificacion",
    "dominio", "k", "o_context", "correlacion",
})

THETA_CANONICO = frozenset({
    "T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10",
    "T11", "T12", "T13", "T14", "T15", "T16", "T17",
    "U0", "U1", "M1", "M.1", "B-Canonical", "TT.6.1", "TR1",
})

DOMINIO_CANONICO = {
    "ontologia": "ONT", "ont": "ONT", "informacion": "INF", "info": "INF",
    "logica": "LOG", "log": "LOG", "epistemologia": "EPI", "epi": "EPI",
    "semantica": "SEM", "sem": "SEM", "temporal": "TMP", "tmp": "TMP",
    "meta": "MET", "met": "MET", "constantes": "MET", "self": "EPI",
    "inferencia_causal": "INF", "verificacion": "EPI", "ver": "VER",
    "contexto": "SEM",
}

# ===============================================================
# FIN CONSTANTES
# ===============================================================


# ===============================================================
# CONFIGURACIÓN
# ===============================================================

_DIR = Path(__file__).parent

def _ruta_vpsi() -> Optional[Path]:
    candidatos = [
        _DIR.parent.parent / "VPSI.py",
        _DIR.parent / "VPSI.py",
        _DIR / "VPSI.py",
    ]
    for p in candidatos:
        if p.exists():
            return p
    return None

def _rutas_py() -> List[Path]:
    """Retorna todos los archivos .py del módulo excepto __init__.py"""
    return sorted(
        p for p in _DIR.glob("**/*.py")
        if p.name != "__init__.py"
    )

# ===============================================================
# FIN CONFIGURACIÓN
# ===============================================================


# ===============================================================
# DEFINICIONES
# ===============================================================

class ContratoInvalido(Exception):
    """El CONTENEDOR no cumple el esquema o la resolución de capacidades falló."""
    pass

# ===============================================================
# FIN DEFINICIONES
# ===============================================================


CONTENEDOR: Dict[str, Any] = {
    # ============================================================
    # ESQUEMA CONTRATO ABIERTO
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
        "Responsable del conocimiento axiomático del sistema. "
        "Mantiene, valida, organiza y expone todas las declaraciones "
        "oficiales del repositorio."
    ),

    # ============================================================
    # PROPÓSITO
    # ============================================================
    "funcion": (
        "Ser la fuente oficial del conocimiento axiomático: "
        "cargar, normalizar, validar coherencia, responder consultas, "
        "citar declaraciones y exponer generatividad."
    ),
    "no_hace": [
        "No calcula Tru_total ni Tru_Ri",
        "No clasifica entrada de usuario (eso es CX)",
        "No orquesta el sistema (eso es Engine)",
        "No genera reportes de otros módulos",
        "No modifica declaraciones ajenas",
    ],

    # ============================================================
    # AUTORIDAD
    # ============================================================
    "autoridad": [
        "Exponer cualquier axioma, lema, teorema, corolario o definición",
        "Responder consultas por id, dominio, sujeto, relación, objeto",
        "Citar y relacionar declaraciones del grafo",
        "Verificar coherencia interna",
        "Reportar estado, salud, inventario y diagnóstico propios",
        "Notificar a DiagnosticoGlobal cuando hay choques o errores",
    ],

    # ============================================================
    # CONOCIMIENTO EXPORTABLE
    # ============================================================
    "conocimiento_exportable": [
        "declaraciones",
        "referencias",
        "dependencias",
        "dominios",
        "generatividad",
        "choques",
        "inventario",
        "estado",
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
    # CONSULTAS SOPORTADAS
    # ============================================================
    "consultas_soportadas": [
        "buscar_por_id",
        "buscar_por_dominio",
        "obtener_generatividad",
        "obtener_inventario",
        "obtener_reporte",
        "obtener_diagnostico",
        "verificar_coherencia",
        "ids_dominio_k_o",
        "recolectar",
    ],

    # ============================================================
    # CAPACIDADES
    # ============================================================
    "capacidades": {
        "verificar": "barrer",
        "barrer": "barrer",
        "verificar_salida": "verificar_salida",
        "inventario": "inventario",
        "axiomas": "axiomas",
        "declaraciones": "declaraciones",
        "generatividad": "generatividad",
        "por_dominio": "por_dominio",
        "ids_dominio_k_o": "ids_dominio_k_o",
        "recolectar": "recolectar",
        "reporte": "reporte",
        "diagnostico": "diagnostico",
        "buscar_por_id": "buscar_por_id",
    },

    # ============================================================
    # METADATOS DE CAPACIDADES (OBLIGATORIO EN EL ESQUEMA)
    # ============================================================
    "capacidades_meta": {
        "verificar": {
            "descripcion": "Alias de barrer. Verifica coherencia interna del módulo.",
            "entrada": "declaraciones_externas opcional (dict)",
            "validar_esquema": ["*"],                                     # ← AGREGADA
            "salida": "dict con coherente, choques, errores, declaraciones, cuerpos, por_tipo",
            "acceso_archivos": ["*"],                                    # ← AGREGADA
        },
        "barrer": {
            "descripcion": "Analiza coherencia de todas las declaraciones (contradicción directa y de cota).",
            "entrada": "declaraciones_externas opcional (dict)",
            "validar_esquema": ["*"],                                     # ← AGREGADA
            "salida": "dict con coherente, choques, errores, declaraciones, cuerpos, por_tipo, ids_dominio_k_o",
            "acceso_archivos": ["*"],                                    # ← AGREGADA
        },
        "verificar_salida": {
            "descripcion": "Comprueba si una salida de barrer/verificar es coherente.",
            "entrada": "salida: dict",
            "validar_esquema": ["*"],                                     # ← AGREGADA
            "salida": "bool",
            "acceso_archivos": ["*"],                                    # ← AGREGADA
        },
        "inventario": {
            "descripcion": "Inventario completo del módulo (declaraciones, cuerpos, capacidades).",
            "entrada": "peticion opcional",
            "validar_esquema": ["*"],                                     # ← AGREGADA
            "salida": "dict con id, nombre, rol, version, declaraciones, cuerpos, capacidades",
            "acceso_archivos": ["*"],                                    # ← AGREGADA
        },
        "axiomas": {
            "descripcion": "Devuelve las declaraciones si el módulo es coherente; lista vacía si no.",
            "entrada": "declaraciones_externas opcional (dict)",
            "validar_esquema": ["*"],                                     # ← AGREGADA
            "salida": "list[dict] de declaraciones normalizadas",
            "acceso_archivos": ["*"],                                    # ← AGREGADA
        },
        "declaraciones": {
            "descripcion": "Igual que axiomas: declaraciones normalizadas si coherente.",
            "entrada": "declaraciones_externas opcional (dict)",
            "validar_esquema": ["*"],                                     # ← AGREGADA
            "salida": "list[dict] de declaraciones normalizadas",
            "acceso_archivos": ["*"],                                    # ← AGREGADA
        },
        "generatividad": {
            "descripcion": "Mide generatividad operativa y canónica (TR1).",
            "entrada": "ninguna",
            "validar_esquema": ["*"],                                     # ← AGREGADA
            "salida": "dict con theta_n, pares, im_vs_theta, capa canonica, dominios, u1_proxy",
            "acceso_archivos": ["*"],                                    # ← AGREGADA
        },
        "por_dominio": {
            "descripcion": "Filtra declaraciones por dominio en gobierna.",
            "entrada": "dominio: str; declaraciones_externas opcional",
            "validar_esquema": ["*"],                                     # ← AGREGADA
            "salida": "list[dict] de declaraciones del dominio",
            "acceso_archivos": ["*"],                                    # ← AGREGADA
        },
        "ids_dominio_k_o": {
            "descripcion": "Ids de declaraciones ligadas a dominios K/O o Def-5.3.1.",
            "entrada": "declaraciones_externas opcional (dict)",
            "validar_esquema": ["*"],                                     # ← AGREGADA
            "salida": "list[str] de ids ordenados",
            "acceso_archivos": ["*"],                                    # ← AGREGADA
        },
        "recolectar": {
            "descripcion": "Carga y normaliza todas las declaraciones de los cuerpos del módulo.",
            "entrada": "declaraciones_externas opcional (dict)",
            "validar_esquema": ["*"],                                     # ← AGREGADA
            "salida": "tuple[list[dict], list[dict]] → (declaraciones, errores)",
            "acceso_archivos": ["*"],                                    # ← AGREGADA
        },
        "reporte": {
            "descripcion": "Reporte interno de estado del módulo.",
            "entrada": "ninguna",
            "validar_esquema": ["*"],                                     # ← AGREGADA
            "salida": "dict con estado, coherente, declaraciones, choques, errores, capacidades",
            "acceso_archivos": ["*"],                                    # ← AGREGADA
        },
        "diagnostico": {
            "descripcion": "Diagnóstico: qué me sucede, qué falta, qué está mal, qué necesito.",
            "entrada": "ninguna",
            "validar_esquema": ["*"],                                     # ← AGREGADA
            "salida": "dict con estado, problemas, advertencias, recomendaciones",
            "acceso_archivos": ["*"],                                    # ← AGREGADA
        },
        "buscar_por_id": {
            "descripcion": "Busca y cita una declaración por su id.",
            "entrada": "id_decl: str",
            "validar_esquema": ["*"],                                     # ← AGREGADA
            "salida": "dict de la declaración o None",
            "acceso_archivos": ["*"],                                    # ← AGREGADA
        },
    },
    

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
        "modificar": False,
        "alterar": False,
        "reescribir": False,
        "crear": True,
        "eliminar": False,
        "actualizar": False,

        # --- PERMISOS DE PROCESAMIENTO ---
        "validar": True,
        "procesar": True,
        "analizar": True,
        "generar": True,
        "transformar": False,

        # --- PERMISOS DE DATOS ---
        "exportar": True,
        "importar": True,
        "respaldar": True,
        "recuperar": True,
        "sincronizar": True,

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

def _cargar_declaraciones_desde_archivo(archivo: Path) -> List[Dict]:
    if archivo.name.startswith("_"):
        return []

    nombre_mod = "axiomas_{0}".format(archivo.stem)
    spec = importlib.util.spec_from_file_location(nombre_mod, archivo)
    if spec is None or spec.loader is None:
        return []

    mod = importlib.util.module_from_spec(spec)
    sys.modules[nombre_mod] = mod
    spec.loader.exec_module(mod)

    declaraciones_raw = getattr(mod, "DECLARACIONES", None)
    if declaraciones_raw is None and callable(getattr(mod, "declaraciones", None)):
        try:
            declaraciones_raw = mod.declaraciones()
        except Exception:  # noqa: BLE001
            declaraciones_raw = []

    if declaraciones_raw is None:
        for attr in ("CUERPO", "declaraciones_lista"):
            val = getattr(mod, attr, None)
            if isinstance(val, list):
                declaraciones_raw = val
                break

    return declaraciones_raw if isinstance(declaraciones_raw, list) else []


def normalizar(decl_original: Dict, cuerpo: str) -> Dict:
    if not isinstance(decl_original, dict):
        raise ValueError("{0}: declaración no es dict".format(cuerpo))

    decl: Dict[str, Any] = {}
    for clave_orig, valor in decl_original.items():
        decl[TRADUCCION_CLAVES.get(clave_orig, clave_orig)] = valor

    for k in OBLIGATORIOS:
        if k not in decl:
            raise ValueError(
                "{0}:{1} sin clave obligatoria '{2}'".format(
                    cuerpo, decl.get("id", "?"), k
                )
            )

    tipo = str(decl["tipo"]).lower()
    tipo = {
        "axiom": "axioma",
        "theorem": "teorema",
        "corollary": "corolario",
        "lemma": "lema",
        "definition": "definicion",
    }.get(tipo, tipo)

    if tipo not in TIPOS:
        raise ValueError(
            "{0}:{1} tipo '{2}' no válido. Admitidos: {3}".format(
                cuerpo, decl["id"], tipo, TIPOS
            )
        )
    if not isinstance(decl["polaridad"], bool):
        raise ValueError(
            "{0}:{1} polaridad debe ser bool".format(cuerpo, decl["id"])
        )

    return {
        "id": str(decl["id"]),
        "cuerpo": cuerpo,
        "tipo": tipo,
        "sujeto": str(decl["sujeto"]),
        "relacion": str(decl["relacion"]),
        "objeto": str(decl["objeto"]),
        "polaridad": bool(decl["polaridad"]),
        "cota": None if decl.get("cota") is None else str(decl["cota"]),
        "depende_de": [str(x) for x in decl.get("depende_de", [])],
        "gobierna": [str(x) for x in decl.get("gobierna", [])],
        "enunciado": str(decl.get("enunciado", "")),
    }


def clave(d: Dict) -> Tuple[str, str, str]:
    return (
        d["sujeto"].lower().strip(),
        d["relacion"].lower().strip(),
        d["objeto"].lower().strip(),
    )


def ref(d: Dict) -> str:
    return "{0}:{1}".format(d["cuerpo"], d["id"])


def contradiccion_directa(decls: List[Dict]) -> List[Dict]:
    grupos: Dict[Tuple[str, str, str], List[Dict]] = {}
    for d in decls:
        grupos.setdefault(clave(d), []).append(d)

    choques: List[Dict] = []
    for k, grupo in grupos.items():
        afirman = [d for d in grupo if d["polaridad"]]
        niegan = [d for d in grupo if not d["polaridad"]]
        for a in afirman:
            for n in niegan:
                choques.append({
                    "tipo": "contradiccion_directa",
                    "tripleta": " - ".join(k),
                    "declaracion_1": {
                        "id": a["id"],
                        "ubicacion": ref(a),
                        "enunciado": a["enunciado"],
                    },
                    "declaracion_2": {
                        "id": n["id"],
                        "ubicacion": ref(n),
                        "enunciado": n["enunciado"],
                    },
                    "mensaje": (
                        "Contradicción en '{0}': {1} AFIRMA vs {2} NIEGA".format(
                            " - ".join(k), ref(a), ref(n)
                        )
                    ),
                })
    return choques


def contradiccion_de_cota(decls: List[Dict]) -> List[Dict]:
    grupos: Dict[Tuple[str, str], List[Dict]] = {}
    for d in decls:
        if d["cota"] is None:
            continue
        grupos.setdefault(
            (d["sujeto"].lower().strip(), d["relacion"].lower().strip()),
            [],
        ).append(d)

    choques: List[Dict] = []
    for (suj, rel), grupo in grupos.items():
        porcota: Dict[str, List[str]] = {}
        for d in grupo:
            porcota.setdefault(d["cota"], []).append(ref(d))
        if len(porcota) > 1:
            choques.append({
                "tipo": "contradiccion_de_cota",
                "sujeto": suj,
                "relacion": rel,
                "cotas": porcota,
                "mensaje": (
                    "Contradicción de cota en '{0} {1}'. Cotas: {2}".format(
                        suj, rel, list(porcota.keys())
                    )
                ),
            })
    return choques


def _dominios_canonicos(gobierna) -> set:
    out = set()
    for g in gobierna or []:
        key = str(g).lower().strip()
        out.add(DOMINIO_CANONICO.get(key, key.upper()[:3]))
    return out


def _medir_pares(theta: list) -> dict:
    n = len(theta)
    pares_tot = n * (n - 1) // 2 if n >= 2 else 0
    compatibles = 0
    novedosos = 0
    for i in range(n):
        Di = theta[i]["dominios"]
        for j in range(i + 1, n):
            Dj = theta[j]["dominios"]
            if not (Di & Dj):
                continue
            compatibles += 1
            union = Di | Dj
            if union > Di and union > Dj:
                novedosos += 1
    return {
        "theta_n": n,
        "pares_totales": pares_tot,
        "pares_compatibles": compatibles,
        "pares_novedosos": novedosos,
        "im_vs_theta": (
            "GENERATIVO"
            if n > 0 and novedosos > n
            else ("ESTANCADO" if n > 0 else "SIN_DATOS")
        ),
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
            f"{NOMBRE_MODULO}: version_contrato inválida: {cont.get('version_contrato')}"
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
# ===============================================================
# Capacidades de contrato
# ===============================================================
def barrer(declaraciones_externas: Optional[Dict[str, List[Dict]]] = None) -> Dict:
    """Capacidad principal: coherencia axiomática del cuerpo."""
    decls, errores = recolectar(declaraciones_externas)
    choques = contradiccion_directa(decls) + contradiccion_de_cota(decls)

    if (choques or errores) and DiagnosticoGlobal is not None:
        try:
            DiagnosticoGlobal.recibir_reporte(
                modulo="axiomas",
                errores=(
                    [{"tipo": "choque", "detalle": c} for c in choques]
                    + [{"tipo": "error_carga", "detalle": e} for e in errores]
                ),
            )
        except Exception:  # noqa: BLE001
            pass

    cuerpos = sorted({d["cuerpo"] for d in decls})
    por_tipo = {t: sum(1 for d in decls if d["tipo"] == t) for t in TIPOS}

    return {
        "coherente": not (choques or errores),
        "choques": choques,
        "errores": errores,
        "declaraciones": len(decls),
        "cuerpos": cuerpos,
        "por_tipo": por_tipo,
        "ids_dominio_k_o": ids_dominio_k_o(declaraciones_externas)
        if not (choques or errores)
        else [],
    }


def verificar_salida(salida: Dict) -> bool:
    return bool(salida.get("coherente", False))


def declaraciones(
    declaraciones_externas: Optional[Dict[str, List[Dict]]] = None,
) -> List[Dict]:
    """Lista normalizada si el cuerpo es coherente; si no → []."""
    resultado = barrer(declaraciones_externas)
    if not resultado["coherente"]:
        return []
    decls, _ = recolectar(declaraciones_externas)
    return decls


def axiomas(
    declaraciones_externas: Optional[Dict[str, List[Dict]]] = None,
) -> List[Dict]:
    """Alias de contrato: misma semántica que declaraciones()."""
    return declaraciones(declaraciones_externas)


def inventario(peticion=None) -> Dict:
    decls, errores = recolectar()
    return {
        "contenedor": "axiomas",
        "version": "9.5",
        "tipos": list(TIPOS),
        "declaraciones": len(decls),
        "por_tipo": {t: sum(1 for d in decls if d["tipo"] == t) for t in TIPOS},
        "cuerpos": sorted({d["cuerpo"] for d in decls}),
        "errores": errores,
        "vigila": ["contradiccion_directa", "contradiccion_de_cota"],
        "ids_dominio_k_o": ids_dominio_k_o(),
        "nota": (
            "Def-5.3.1 y dominio O viven en los cuerpos cargados; "
            "este módulo los vigila y expone, no los clasifica en entrada."
        ),
    }


# --- ids canónicos del paper (TR1, |Θ|=24) ---
THETA_CANONICO = frozenset({
    "T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10",
    "T11", "T12", "T13", "T14", "T15", "T16", "T17",
    "U0", "U1", "M1", "M.1", "B-Canonical", "TT.6.1", "TR1",
})

DOMINIO_CANONICO = {
    "ontologia": "ONT",
    "ont": "ONT",
    "informacion": "INF",
    "info": "INF",
    "logica": "LOG",
    "log": "LOG",
    "epistemologia": "EPI",
    "epi": "EPI",
    "semantica": "SEM",
    "sem": "SEM",
    "temporal": "TMP",
    "tmp": "TMP",
    "meta": "MET",
    "met": "MET",
    "constantes": "MET",
    "self": "EPI",
    "inferencia_causal": "INF",
    "verificacion": "EPI",
    "ver": "VER",
    "contexto": "SEM",
}


def _dominios_canonicos(gobierna) -> set:
    out = set()
    for g in gobierna or []:
        key = str(g).lower().strip()
        out.add(DOMINIO_CANONICO.get(key, key.upper()[:3]))
    return out


def _medir_pares(theta: list) -> dict:
    n = len(theta)
    pares_tot = n * (n - 1) // 2 if n >= 2 else 0
    compatibles = 0
    novedosos = 0
    for i in range(n):
        Di = theta[i]["dominios"]
        for j in range(i + 1, n):
            Dj = theta[j]["dominios"]
            if not (Di & Dj):
                continue
            compatibles += 1
            union = Di | Dj
            if union > Di and union > Dj:
                novedosos += 1
    return {
        "theta_n": n,
        "pares_totales": pares_tot,
        "pares_compatibles": compatibles,
        "pares_novedosos": novedosos,
        "im_vs_theta": (
            "GENERATIVO" if n > 0 and novedosos > n
            else ("ESTANCADO" if n > 0 else "SIN_DATOS")
        ),
    }


def generatividad() -> dict:
    """
    TR1 en dos capas (saber, no creer):

    1) operativa  — todo axioma/teorema con gobierna (grafo del repo)
    2) canonica   — solo los 24 ids del paper + dominios normalizados

    No inventa candidatos. No calcula Tru. Una sola definición (sin duplicar).
    """
    decls, errores = recolectar()

    oper = []
    for d in decls:
        if d.get("tipo") not in ("teorema", "axioma"):
            continue
        gob = d.get("gobierna") or []
        if not gob:
            continue
        oper.append({
            "id": d["id"],
            "tipo": d["tipo"],
            "dominios": set(gob),
        })
    m_op = _medir_pares(oper)
    dominios_op = sorted({g for n in oper for g in n["dominios"]})

    por_id = {}
    for d in decls:
        i = str(d.get("id", ""))
        if i in THETA_CANONICO:
            cand = {
                "id": i,
                "tipo": d.get("tipo"),
                "dominios": _dominios_canonicos(d.get("gobierna")),
            }
            prev = por_id.get(i)
            if prev is None or len(cand["dominios"]) >= len(prev["dominios"]):
                por_id[i] = cand

    can = [por_id[i] for i in sorted(por_id.keys()) if por_id[i]["dominios"]]
    m_can = _medir_pares(can)
    dominios_can = sorted({g for n in can for g in n["dominios"]})
    faltan = sorted(THETA_CANONICO - set(por_id.keys()))
    sin_dominio = sorted(i for i, n in por_id.items() if not n["dominios"])

    u1_proxy = (
        "NO_STAGNANT"
        if m_can.get("pares_novedosos", 0) > 0 or m_op.get("pares_novedosos", 0) > 0
        else "REVISAR"
    )

    return {
        "contenedor": "axiomas",
        "theta_n": m_op["theta_n"],
        "pares_totales": m_op["pares_totales"],
        "pares_compatibles": m_op["pares_compatibles"],
        "pares_novedosos": m_op["pares_novedosos"],
        "im_vs_theta": m_op["im_vs_theta"],
        "dominios": dominios_op,
        "u1_proxy": u1_proxy,
        "errores_recoleccion": len(errores),
        "por_tipo_theta": {
            "axioma": sum(1 for n in oper if n["tipo"] == "axioma"),
            "teorema": sum(1 for n in oper if n["tipo"] == "teorema"),
        },
        "canonica": {
            **m_can,
            "ids_presentes": sorted(por_id.keys()),
            "ids_faltantes": faltan,
            "ids_sin_dominio": sin_dominio,
            "dominios": dominios_can,
            "objetivo_paper": {
                "theta_n": 24,
                "im_esperada": 153,
                "nota": "|Im(⊕)|=153 > 24=|Θ| en enumeración del texto",
            },
        },
        "ids_dominio_k_o": ids_dominio_k_o(),
        "nota": (
            "Capa operativa = grafo del repo. "
            "Capa canonica = solo ids TR1 del paper. "
            "Dominio O/K: ver ids_dominio_k_o y cuerpos (no se clasifica entrada aquí)."
        ),
    }
def recolectar(
    declaraciones_externas: Optional[Dict[str, List[Dict]]] = None,
) -> Tuple[List[Dict], List[Dict]]:
    decls: List[Dict] = []
    errores: List[Dict] = []

    for archivo in sorted(_DIR.glob("**/*.py")):
        if archivo.name == "__init__.py":
            continue
        try:
            for d in _cargar_declaraciones_desde_archivo(archivo):
                decls.append(normalizar(d, archivo.stem))
        except Exception as e:  # noqa: BLE001
            errores.append({
                "archivo": archivo.name,
                "error": "{0}: {1}".format(type(e).__name__, e),
            })

    for archivo in _rutas_py():
       try:
           for d in _cargar_declaraciones_desde_archivo(archivo):
               decls.append(normalizar(d, archivo.stem))
       except Exception as e:
           errores.append({
               "archivo": archivo.name,
               "error": f"{type(e).__name__}: {e}",
           })
# ===============================================================
# CAPACIDADES PÚBLICAS
# ===============================================================

def ids_dominio_k_o(
    declaraciones_externas: Optional[Dict[str, List[Dict]]] = None,
) -> List[str]:
    decls, _ = recolectar(declaraciones_externas)
    ids: List[str] = []
    for d in decls:
        gobs = {str(g).lower().strip() for g in (d.get("gobierna") or [])}
        if gobs & DOMINIOS_K_O:
            ids.append(d["id"])
        blob = (
            "{0} {1} {2}".format(
                d.get("sujeto", ""),
                d.get("objeto", ""),
                d.get("enunciado", ""),
            )
        ).lower()
        if any(
            x in blob
            for x in ("def-5.3.1", "o_context", "dominio o", "permite_k")
        ):
            if d["id"] not in ids:
                ids.append(d["id"])
    return sorted(set(ids))


def barrer(
    declaraciones_externas: Optional[Dict[str, List[Dict]]] = None,
) -> Dict:
    decls, errores = recolectar(declaraciones_externas)
    choques = contradiccion_directa(decls) + contradiccion_de_cota(decls)

    if (choques or errores) and DiagnosticoGlobal is not None:
        try:
            DiagnosticoGlobal.recibir_reporte(
                modulo="axiomas",
                errores=(
                    [{"tipo": "choque", "detalle": c} for c in choques]
                    + [{"tipo": "error_carga", "detalle": e} for e in errores]
                ),
            )
        except Exception:  # noqa: BLE001
            pass

    cuerpos = sorted({d["cuerpo"] for d in decls})
    por_tipo = {t: sum(1 for d in decls if d["tipo"] == t) for t in TIPOS}

    return {
        "coherente": not (choques or errores),
        "choques": choques,
        "errores": errores,
        "declaraciones": len(decls),
        "cuerpos": cuerpos,
        "por_tipo": por_tipo,
        "ids_dominio_k_o": (
            ids_dominio_k_o(declaraciones_externas)
            if not (choques or errores)
            else []
        ),
    }


def verificar_salida(salida: Dict) -> bool:
    return bool(salida.get("coherente", False))


def declaraciones(
    declaraciones_externas: Optional[Dict[str, List[Dict]]] = None,
) -> List[Dict]:
    resultado = barrer(declaraciones_externas)
    if not resultado["coherente"]:
        return []
    decls, _ = recolectar(declaraciones_externas)
    return decls


def por_dominio(
    dominio: str,
    declaraciones_externas: Optional[Dict[str, List[Dict]]] = None,
) -> List[Dict]:
    dom = str(dominio).lower().strip()
    decls, _ = recolectar(declaraciones_externas)
    out = []
    for d in decls:
        gobs = [str(g).lower().strip() for g in (d.get("gobierna") or [])]
        if dom in gobs or any(dom in g for g in gobs):
            out.append(d)
    return out


def recolectar(
    declaraciones_externas: Optional[Dict[str, List[Dict]]] = None,
) -> Tuple[List[Dict], List[Dict]]:
    decls: List[Dict] = []
    errores: List[Dict] = []

    # 1. Cargar declaraciones de la carpeta local del módulo
    for archivo in sorted(_DIR.glob("**/*.py")):
        if archivo.name == "__init__.py":
            continue
        try:
            for d in _cargar_declaraciones_desde_archivo(archivo):
                decls.append(normalizar(d, archivo.stem))
        except Exception as e:  # noqa: BLE001
            errores.append({
                "archivo": archivo.name,
                "error": f"{type(e).__name__}: {e}",
            })

    # 2. Cargar VPSI / Raíz si aplica
    vpsi = _ruta_vpsi()
    if vpsi is not None:
        try:
            for d in _cargar_declaraciones_desde_archivo(vpsi):
                decls.append(normalizar(d, "VPSI"))
        except Exception as e:  # noqa: BLE001
            errores.append({
                "archivo": str(vpsi.name),
                "error": f"{type(e).__name__}: {e}",
            })

        # 3. Manejo de declaraciones externas con recuperación y reporte de excepciones
    if declaraciones_externas:
        for nombre, lista in declaraciones_externas.items():
            elementos_a_procesar = []

            if isinstance(lista, list):
                elementos_a_procesar = lista
            else:
                # Si no es una lista, escaneamos las declaraciones reales de la carpeta
                for archivo in sorted(_DIR.glob("**/*.py")):
                    if archivo.name == "__init__.py":
                        continue
                    try:
                        for d in _cargar_declaraciones_desde_archivo(archivo):
                            tipo = str(d.get("tipo", "")).lower()
                            if tipo in ("axioma", "teorema", "axiom", "theorem"):
                                elementos_a_procesar.append(d)
                    except Exception as e:  # noqa: BLE001
                        errores.append({
                            "modulo": nombre,
                            "error": f"Error extrayendo axiomas de carpeta: {e}",
                        })
                
                # Si el valor no-lista es un diccionario individual, lo sumamos para evaluar
                if isinstance(lista, dict):
                    elementos_a_procesar.append(lista)

            # Evaluación de cada declaración / marca recibida
            for d in elementos_a_procesar:
                if not isinstance(d, dict):
                    errores.append({
                        "modulo": nombre,
                        "error": f"Declaración no válida (tipo incorrecto: {type(d).__name__})"
                    })
                    continue

                try:
                    # Intento de normalización/verificación de existencia
                    decl_norm = d if "cuerpo" in d else normalizar(d, nombre)
                    
                    # Verificamos si la declaración posee un cuerpo/ID válido dentro del dominio
                    if not decl_norm.get("id") or not decl_norm.get("cuerpo"):
                        # Captura de excepción: Axioma/Declaración no existe en el sistema
                        errores.append({
                            "modulo": nombre,
                            "tipo_excepcion": "axioma_no_existente",
                            "detalle": f"El axioma o marca '{decl_norm.get('id', 'desconocido')}' no existe en el registro.",
                            "declaracion_omitida": decl_norm
                        })
                        continue  # Salta y continúa con el siguiente sin tumbar el pipeline

                    # Si existe y es válida, la añade a la lista de declaraciones principales
                    decls.append(decl_norm)

                except ValueError as e:
                    # Manejo de la excepción cuando la normalización determina que no existe
                    errores.append({
                        "modulo": nombre,
                        "tipo_excepcion": "declaracion_invalida_omitida",
                        "error": str(e),
                    })
                    continue

    # ==========================================================
    # 2. CARGAR ARCHIVOS EN LA RAÍZ DEL PROYECTO
    # ==========================================================
    # Buscar en la raíz del proyecto (donde está VPSI.py)
    raiz_proyecto = _DIR.parent.parent
    for archivo in sorted(raiz_proyecto.glob("*.py")):
        if archivo.name in ("__init__.py", "setup.py", "conftest.py"):
            continue
        try:
            for d in _cargar_declaraciones_desde_archivo(archivo):
                decls.append(normalizar(d, archivo.stem))
        except Exception as e:
            errores.append({
                "archivo": archivo.name,
                "error": f"{type(e).__name__}: {e}",
            })

    # ==========================================================
    # 3. CARGAR ARCHIVOS EN EL DIRECTORIO PADRE
    # ==========================================================
    directorio_padre = _DIR.parent
    for archivo in sorted(directorio_padre.glob("*.py")):
        if archivo.name in ("__init__.py", "setup.py", "conftest.py"):
            continue
        try:
            for d in _cargar_declaraciones_desde_archivo(archivo):
                decls.append(normalizar(d, archivo.stem))
        except Exception as e:
            errores.append({
                "archivo": archivo.name,
                "error": f"{type(e).__name__}: {e}",
            })

    # ==========================================================
    # 4. SI SE PASARON EXTERNAS, LAS PROCESAMOS
    # ==========================================================
    if declaraciones_externas:
        for nombre, lista in declaraciones_externas.items():
            if not isinstance(lista, list):
                lista = []
            for d in lista:
                try:
                    decls.append(normalizar(d, nombre))
                except ValueError as e:
                    errores.append({"modulo": nombre, "error": str(e)})

    return decls, errores
# ===============================================================
# DECLARACIONES EXTERNAS AUTO-GENERADAS
# ===============================================================

def obtener_declaraciones_externas(
    incluir_cuerpos: Optional[List[str]] = None,
    excluir_cuerpos: Optional[List[str]] = None,
) -> Dict[str, List[Dict]]:
    """
    Genera declaraciones_externas a partir de las declaraciones internas.
    
    Args:
        incluir_cuerpos: Si se pasa, solo incluye estos cuerpos.
        excluir_cuerpos: Si se pasa, excluye estos cuerpos.
    
    Returns:
        Dict[str, List[Dict]]: Diccionario con declaraciones por cuerpo.
    
    Raises:
        ValueError: Si no se encuentran declaraciones.
    """
    decls, errores = recolectar()
    
    # Si hay errores de carga, los registramos pero no fallamos
    if errores:
        # Opcional: imprimir advertencia o registrar en diagnóstico
        print(f"[AXIOMAS] Advertencia: {len(errores)} errores al recolectar declaraciones internas")
    
    if not decls:
        raise ValueError(
            "No se encontraron declaraciones internas en el módulo axiomas. "
            "Verifica que los cuerpos tengan DECLARACIONES."
        )
    
    # Filtrar por cuerpos si se especifica
    cuerpos_permitidos = set(incluir_cuerpos) if incluir_cuerpos else None
    cuerpos_excluidos = set(excluir_cuerpos) if excluir_cuerpos else set()
    
    externas: Dict[str, List[Dict]] = {}
    for d in decls:
        cuerpo = d.get("cuerpo", "desconocido")
        
        # Aplicar filtros
        if cuerpos_permitidos and cuerpo not in cuerpos_permitidos:
            continue
        if cuerpo in cuerpos_excluidos:
            continue
            
        if cuerpo not in externas:
            externas[cuerpo] = []
        externas[cuerpo].append(d)
    
    if not externas:
        raise ValueError(
            f"No se encontraron declaraciones en los cuerpos especificados: {incluir_cuerpos}"
        )
    
    return externas

def axiomas(
    declaraciones_externas: Optional[Dict[str, List[Dict]]] = None,
) -> List[Dict]:
    return declaraciones(declaraciones_externas)


def generatividad() -> dict:
    decls, errores = recolectar()

    oper = []
    for d in decls:
        if d.get("tipo") not in ("teorema", "axioma"):
            continue
        gob = d.get("gobierna") or []
        if not gob:
            continue
        oper.append({
            "id": d["id"],
            "tipo": d["tipo"],
            "dominios": set(gob),
        })
    m_op = _medir_pares(oper)
    dominios_op = sorted({g for n in oper for g in n["dominios"]})

    por_id = {}
    for d in decls:
        i = str(d.get("id", ""))
        if i in THETA_CANONICO:
            cand = {
                "id": i,
                "tipo": d.get("tipo"),
                "dominios": _dominios_canonicos(d.get("gobierna")),
            }
            prev = por_id.get(i)
            if prev is None or len(cand["dominios"]) >= len(prev["dominios"]):
                por_id[i] = cand

    can = [por_id[i] for i in sorted(por_id.keys()) if por_id[i]["dominios"]]
    m_can = _medir_pares(can)
    dominios_can = sorted({g for n in can for g in n["dominios"]})
    faltan = sorted(THETA_CANONICO - set(por_id.keys()))
    sin_dominio = sorted(i for i, n in por_id.items() if not n["dominios"])

    u1_proxy = (
        "NO_STAGNANT"
        if m_can.get("pares_novedosos", 0) > 0
        or m_op.get("pares_novedosos", 0) > 0
        else "REVISAR"
    )

    return {
        "contenedor": "axiomas",
        "theta_n": m_op["theta_n"],
        "pares_totales": m_op["pares_totales"],
        "pares_compatibles": m_op["pares_compatibles"],
        "pares_novedosos": m_op["pares_novedosos"],
        "im_vs_theta": m_op["im_vs_theta"],
        "dominios": dominios_op,
        "u1_proxy": u1_proxy,
        "errores_recoleccion": len(errores),
        "por_tipo_theta": {
            "axioma": sum(1 for n in oper if n["tipo"] == "axioma"),
            "teorema": sum(1 for n in oper if n["tipo"] == "teorema"),
        },
        "canonica": {
            **m_can,
            "ids_presentes": sorted(por_id.keys()),
            "ids_faltantes": faltan,
            "ids_sin_dominio": sin_dominio,
            "dominios": dominios_can,
            "objetivo_paper": {
                "theta_n": 24,
                "im_esperada": 153,
                "nota": "|Im(⊕)|=153 > 24=|Θ| en enumeración del texto",
            },
        },
        "ids_dominio_k_o": ids_dominio_k_o(),
        "nota": (
            "Capa operativa = grafo del repo. "
            "Capa canonica = solo ids TR1 del paper. "
            "Dominio O/K: ver ids_dominio_k_o y cuerpos."
        ),
    }


def buscar_por_id(id_decl: str) -> Optional[Dict]:
    decls, _ = recolectar()
    for d in decls:
        if d.get("id") == id_decl:
            return d
    return None


def verificar(declaraciones_externas: Optional[Dict[str, List[Dict]]] = None) -> Dict[str, Any]:
    return barrer(declaraciones_externas)
# ===========================================================
# 4. RESOLUCIÓN POR REPERTORIO DECLARATIVO
# ===========================================================

def resolver_por_repertorio(
    consulta: Dict,
    declaraciones_externas: Optional[Dict[str, List[Dict]]] = None,
) -> Dict:
    decls, errores = recolectar(
        declaraciones_externas
    )

    if errores:
        return {
            "coherente": False,
            "estado": "ERROR_REPERTORIO",
            "errores": errores,
        }

    resultado = barrer(
        declaraciones_externas
    )

    if not resultado["coherente"]:
        return {
            "coherente": False,
            "estado": "INCONSISTENTE",
            "resultado": resultado,
        }

    # X representa cualquier objeto de la demanda.
    # No se codifica ningún X concreto.

    encontrada = correlacionar(
        consulta,
        decls,
    )

    if encontrada is not None:
        return {
            "coherente": True,
            "estado": "RESUELTA",
            "respuesta": encontrada,
        }

    # X no pertenece al repertorio.
    # No se inventa X.
    # La respuesta se deriva del propio repertorio AX.

    return {
        "coherente": True,
        "estado": "NO_SUSTENTADA",
        "respuesta": decls,
    }

def verificar(declaraciones_externas: Optional[Dict[str, List[Dict]]] = None) -> Dict[str, Any]:
    # ==========================================================
    # INTENTAR USAR BARRER
    # ==========================================================
    try:
        resultado = barrer(declaraciones_externas)
        if resultado.get("coherente"):
            # Si barrer funciona y es coherente, devolver su resultado
            return resultado
    except Exception:
        # Si barrer falla, no inventamos X
        pass

    # ==========================================================
    # SI BARRER NO EXISTE O FALLA: USAR LÓGICA DEL REPO
    # ==========================================================
    # Recolectar declaraciones directamente (sin barrer)
    decls, errores = recolectar(declaraciones_externas)

    # Verificar coherencia con lógica propia (no barrer)
    choques = contradiccion_directa(decls) + contradiccion_de_cota(decls)

    # Si hay errores o choques, reportarlos
    if errores or choques:
        return {
            "coherente": False,
            "choques": choques,
            "errores": errores,
            "declaraciones": len(decls),
            "cuerpos": sorted({d["cuerpo"] for d in decls}),
            "por_tipo": {t: sum(1 for d in decls if d["tipo"] == t) for t in TIPOS},
            "ids_dominio_k_o": [],
            "nota": "Barrer no disponible. Se usó lógica alternativa."
        }

    # Si no hay errores ni choques, es coherente
    return {
        "coherente": True,
        "choques": [],
        "errores": [],
        "declaraciones": len(decls),
        "cuerpos": sorted({d["cuerpo"] for d in decls}),
        "por_tipo": {t: sum(1 for d in decls if d["tipo"] == t) for t in TIPOS},
        "ids_dominio_k_o": ids_dominio_k_o(declaraciones_externas),
        "nota": "Barrer no disponible. Se usó lógica alternativa."
    }
# ===============================================================
# DECLARACIONES EXTERNAS - EXTRACCIÓN COMPLETA
# ===============================================================

def extraer_todas_declaraciones() -> Dict[str, List[Dict]]:
    """
    Extrae TODAS las declaraciones de TODOS los archivos del módulo.
    
    Returns:
        Dict[str, List[Dict]]: Diccionario con:
            - "declaraciones": Lista de todas las declaraciones válidas
            - "por_cuerpo": Diccionario con declaraciones agrupadas por cuerpo
            - "ids": Lista de todos los IDs
            - "totales": Conteo por tipo
    """
    declaraciones_validas: List[Dict] = []
    errores: List[Dict] = []
    ids_encontrados: List[str] = []
    
    # ==========================================================
    # RECORRER TODOS LOS ARCHIVOS
    # ==========================================================
    for archivo in sorted(_DIR.glob("**/*.py")):
        if archivo.name == "__init__.py":
            continue
        
        try:
            declaraciones_raw = _cargar_declaraciones_desde_archivo(archivo)
            if not declaraciones_raw:
                continue
                
            for d in declaraciones_raw:
                # ==============================================
                # VALIDAR CAMPOS OBLIGATORIOS
                # ==============================================
                id_decl = d.get("id")
                if not id_decl:
                    errores.append({
                        "archivo": archivo.name,
                        "error": f"Declaración sin ID: {d}"
                    })
                    continue
                
                                # Validar que el ID sea string
                if not isinstance(id_decl, str):
                    errores.append({
                        "archivo": archivo.name,
                        "error": f"ID no es string: {id_decl}"
                    })
                    continue
                
                # Validar campos obligatorios
                campos_obligatorios = ["sujeto", "relacion", "objeto", "polaridad", "tipo"]
                faltan = [c for c in campos_obligatorios if c not in d]
                if faltan:
                    errores.append({
                        "archivo": archivo.name,
                        "id": id_decl,
                        "error": f"Faltan campos: {faltan}"
                    })
                    continue

                
                # ==============================================
                # NORMALIZAR Y AGREGAR
                # ==============================================
                try:
                    decl_normalizada = normalizar(d, archivo.stem)
                    declaraciones_validas.append(decl_normalizada)
                    if id_decl not in ids_encontrados:
                        ids_encontrados.append(id_decl)
                except Exception as e:
                    errores.append({
                        "archivo": archivo.name,
                        "id": id_decl,
                        "error": f"Error al normalizar: {e}"
                    })
                    
        except Exception as e:
            errores.append({
                "archivo": archivo.name,
                "error": f"Error al cargar archivo: {e}"
            })
    
    # ==========================================================
    # AGRUPAR POR CUERPO
    # ==========================================================
    por_cuerpo: Dict[str, List[Dict]] = {}
    for d in declaraciones_validas:
        cuerpo = d.get("cuerpo", "desconocido")
        if cuerpo not in por_cuerpo:
            por_cuerpo[cuerpo] = []
        por_cuerpo[cuerpo].append(d)
    
    # ==========================================================
    # CONTAR POR TIPO
    # ==========================================================
    totales = {
        "axioma": sum(1 for d in declaraciones_validas if d.get("tipo") == "axioma"),
        "lema": sum(1 for d in declaraciones_validas if d.get("tipo") == "lema"),
        "teorema": sum(1 for d in declaraciones_validas if d.get("tipo") == "teorema"),
        "corolario": sum(1 for d in declaraciones_validas if d.get("tipo") == "corolario"),
        "definicion": sum(1 for d in declaraciones_validas if d.get("tipo") == "definicion"),
    }
    
    return {
        "declaraciones": declaraciones_validas,
        "por_cuerpo": por_cuerpo,
        "ids": sorted(ids_encontrados),
        "totales": totales,
        "total_general": len(declaraciones_validas),
        "errores": errores,
    }


# ===============================================================
# BUSCAR DECLARACIÓN POR ID
# ===============================================================

def buscar_por_id(id_buscado: str) -> Dict[str, Any]:
    """
    Busca una declaración por su ID.
    
    Args:
        id_buscado: ID de la declaración a buscar
    
    Returns:
        Dict con:
            - "encontrado": True/False
            - "declaracion": La declaración si existe, o None
            - "error": Mensaje de error si no existe
    """
    todas = extraer_todas_declaraciones()
    
    for d in todas["declaraciones"]:
        if d.get("id") == id_buscado:
            return {
                "encontrado": True,
                "declaracion": d,
                "error": None
            }
    
    return {
        "encontrado": False,
        "declaracion": None,
        "error": f"No se encontró declaración con ID '{id_buscado}'"
    }


# ===============================================================
# LISTAR TODOS LOS IDS
# ===============================================================

def listar_todos_ids() -> List[str]:
    """Retorna todos los IDs de declaraciones existentes."""
    todas = extraer_todas_declaraciones()
    return todas["ids"]


# ===============================================================
# VERIFICAR SI ID EXISTE
# ===============================================================

def id_existe(id_buscado: str) -> bool:
    """Verifica si un ID existe en las declaraciones."""
    todas = extraer_todas_declaraciones()
    return id_buscado in todas["ids"]

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
        "estado": ESTADO_OPERATIVO if r.get("coherente") else ESTADO_DEGRADADO,
        "coherente": r.get("coherente"),
        "declaraciones": r.get("declaraciones"),
        "choques": len(r.get("choques") or []),
        "errores": len(r.get("errores") or []),
        "cuerpos": r.get("cuerpos"),
        "por_tipo": r.get("por_tipo"),
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "autoridad": CONTENEDOR.get("autoridad"),
        "conocimiento_exportable": CONTENEDOR.get("conocimiento_exportable"),
        "consultas_soportadas": CONTENEDOR.get("consultas_soportadas"),
    }


def diagnostico() -> Dict[str, Any]:
    r = barrer()
    problemas = []
    advertencias = []
    recomendaciones = []

    if r.get("errores"):
        problemas.append({"tipo": "errores_carga", "detalle": r["errores"]})
        recomendaciones.append("Revisar archivos de cuerpos con error de carga")

    if r.get("choques"):
        problemas.append({
            "tipo": "contradicciones",
            "cantidad": len(r["choques"]),
            "detalle": r["choques"][:5],
        })
        recomendaciones.append("Resolver contradicciones directas o de cota")

    if not r.get("declaraciones"):
        advertencias.append("No hay declaraciones cargadas")
        recomendaciones.append("Verificar que existan cuerpos .py con DECLARACIONES")

    estado = ESTADO_OPERATIVO
    if problemas:
        estado = ESTADO_DEGRADADO
    if not r.get("declaraciones") and not problemas:
        estado = ESTADO_NO_INICIADO

    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "estado": estado,
        "problemas": problemas,
        "advertencias": advertencias,
        "recomendaciones": recomendaciones,
        "coherente": r.get("coherente"),
        "declaraciones": r.get("declaraciones"),
        "choques_n": len(r.get("choques") or []),
        "errores_n": len(r.get("errores") or []),
    }

# ===============================================================
# FIN REPORTING
# ===============================================================


# ===============================================================
# INVENTARIO
# ===============================================================

def inventario(peticion=None) -> Dict:
    decls, errores = recolectar()
    return {
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "tipos": list(TIPOS),
        "declaraciones": len(decls),
        "por_tipo": {
            t: sum(1 for d in decls if d["tipo"] == t) for t in TIPOS
        },
        "cuerpos": sorted({d["cuerpo"] for d in decls}),
        "errores": errores,
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "autoridad": CONTENEDOR.get("autoridad"),
        "conocimiento_exportable": CONTENEDOR.get("conocimiento_exportable"),
        "consultas_soportadas": CONTENEDOR.get("consultas_soportadas"),
        "invariantes": CONTENEDOR.get("invariantes"),
        "vigila": ["contradiccion_directa", "contradiccion_de_cota"],
        "ids_dominio_k_o": ids_dominio_k_o(),
        "nota": (
            "Def-5.3.1 y dominio O viven en los cuerpos cargados; "
            "este módulo los vigila y expone, no los clasifica en entrada."
        ),
    }

# ===============================================================
# FIN INVENTARIO
# ===============================================================


# ===============================================================
# EXPORTACIONES + RESOLUCIÓN ESTRICTA
# ===============================================================

_CAP_MAP = {
    "barrer": barrer,
    "verificar_salida": verificar_salida,
    "inventario": inventario,
    "axiomas": axiomas,
    "declaraciones": declaraciones,
    "generatividad": generatividad,
    "por_dominio": por_dominio,
    "ids_dominio_k_o": ids_dominio_k_o,
    "recolectar": recolectar,
    "reporte": reporte,
    "diagnostico": diagnostico,
    "buscar_por_id": buscar_por_id,
    "verificar": verificar,
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
            f"tiene tipo inválido: {type(ref).__name__}"
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
    "AXIOMA",
    "LEMA",
    "TEOREMA",
    "COROLARIO",
    "DEFINICION",
    "TIPOS",
    "normalizar",
    "clave",
    "ref",
    "recolectar",
    "por_dominio",
    "ids_dominio_k_o",
    "declaraciones",
    "axiomas",
    "contradiccion_directa",
    "contradiccion_de_cota",
    "barrer",
    "verificar_salida",
    "inventario",
    "generatividad",
    "verificar",
    "reporte",
    "diagnostico",
    "buscar_por_id",
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
# ===============================================================
# FIN EXTENSIONES FUTURAS
# ===============================================================


# ===============================================================
# FIN DEL MÓDULO
# ===============================================================
