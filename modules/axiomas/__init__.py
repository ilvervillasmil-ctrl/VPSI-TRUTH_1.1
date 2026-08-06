# ===============================================================
# VPSI-TRUTH — modules/axiomas/__init__.py
# ===============================================================
#
# MÓDULO:        axiomas
# Rol:           AX
# Versión:       9.5
#
# Función:
#   Vigilar declaraciones (axioma | lema | teorema | corolario | definicion)
#   y detectar contradicciones.
#
# Qué hace:
#   - Carga cuerpos de declaraciones
#   - Normaliza y recolecta
#   - Detecta contradicción directa y de cota
#   - Expone generatividad (TR1 / capa canónica)
#   - Reporta su propio estado
#
# Qué NO hace:
#   - No calcula Tru_total / Tru_Ri
#   - No clasifica entrada (eso es CX)
#   - No orquesta el sistema (eso es Engine)
#   - No genera reportes de otros módulos
#
# Responsabilidad:
#   Coherencia axiomática interna del repositorio.
#
# Conocimiento que aporta:
#   Declaraciones normalizadas, choques, generatividad, ids de dominio K/O.
#
# Relación con Engine:
#   Engine descubre este CONTENEDOR, ejecuta las capacidades declaradas
#   y consolida el reporte que este módulo produce.
#
# Relación con Omega:
#   Omega no calcula nada de AX. Solo presenta el reporte que Engine entrega.
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

VERSION_MODULO = "9.5"
NOMBRE_MODULO = "axiomas"
ROL_MODULO = "AX"

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

# ===============================================================
# FIN CONFIGURACIÓN
# ===============================================================


# ===============================================================
# DEFINICIONES
# ===============================================================
# (Estructuras conceptuales mínimas; la lógica vive en funciones)

# ===============================================================
# FIN DEFINICIONES
# ===============================================================


# ===============================================================
# CONTRATO OFICIAL DEL MÓDULO
# ===============================================================

CONTENEDOR = {
    # ----- IDENTIDAD -----
    "nombre": NOMBRE_MODULO,
    "rol": ROL_MODULO,
    "version": VERSION_MODULO,
    "descripcion": (
        "Contenedor de axiomas. Rol AX. "
        "Vigila declaraciones y contradicciones. "
        "El Engine ejecuta las capacidades declaradas aquí."
    ),

    # ----- PROPÓSITO -----
    "funcion": (
        "Vigilar coherencia axiomática: cargar declaraciones, "
        "detectar contradicción directa y de cota, exponer generatividad."
    ),
    "no_hace": [
        "No calcula Tru_total ni Tru_Ri",
        "No clasifica entrada de usuario (eso es CX)",
        "No orquesta el sistema (eso es Engine)",
        "No genera reportes de otros módulos",
    ],

    # ----- CONOCIMIENTO -----
    "conocimiento": (
        "Declaraciones normalizadas, choques, generatividad (TR1), "
        "ids de dominio K/O, inventario de cuerpos axiomáticos."
    ),

    # ----- DEPENDENCIAS -----
    "requiere": [],

    # ----- AUTORIZACIÓN AL ENGINE -----
    "autoriza_engine": {
        "leer_archivos_del_modulo": True,
        "ejecutar_capacidades": True,
        "combinar_con_otros_contratos": True,
        "persistir": False,
        "modificar_estado_externo": False,
    },

    # ----- CAPACIDADES -----
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
    },

    # ----- REPORTING -----
    "reporting": {
        "estado": True,
        "salud": True,
        "inventario": True,
        "estadisticas": True,
        "errores": True,
        "advertencias": True,
        "contrato": True,
        "capacidades": True,
        "dependencias": True,
    },
}

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

# ===============================================================
# FIN FUNCIONES PRIVADAS
# ===============================================================


# ===============================================================
# CAPACIDADES PÚBLICAS
# ===============================================================

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

    vpsi = _ruta_vpsi()
    if vpsi is not None:
        try:
            for d in _cargar_declaraciones_desde_archivo(vpsi):
                decls.append(normalizar(d, "VPSI"))
        except Exception as e:  # noqa: BLE001
            errores.append({
                "archivo": str(vpsi.name),
                "error": "{0}: {1}".format(type(e).__name__, e),
            })

    if declaraciones_externas:
        for nombre, lista in declaraciones_externas.items():
            if not isinstance(lista, list):
                errores.append({
                    "modulo": nombre,
                    "error": "declaraciones externas no es lista",
                })
                continue
            for d in lista:
                try:
                    decls.append(normalizar(d, nombre))
                except ValueError as e:
                    errores.append({"modulo": nombre, "error": str(e)})

    return decls, errores


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

# ===============================================================
# FIN CAPACIDADES PÚBLICAS
# ===============================================================


# ===============================================================
# REPORTING INTERNO
# ===============================================================

def reporte() -> Dict[str, Any]:
    """
    Reporte interno del módulo.
    Solo informa estado propio. No calcula Tru ni orquesta el sistema.
    """
    r = barrer()
    return {
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "estado": "OPERATIVO" if r.get("coherente") else "DEGRADADO",
        "coherente": r.get("coherente"),
        "declaraciones": r.get("declaraciones"),
        "choques": len(r.get("choques") or []),
        "errores": len(r.get("errores") or []),
        "cuerpos": r.get("cuerpos"),
        "por_tipo": r.get("por_tipo"),
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
    }

# ===============================================================
# FIN REPORTING
# ===============================================================


# ===============================================================
# VERIFICACIÓN
# ===============================================================

def verificar() -> Dict[str, Any]:
    """
    Verificación de coherencia interna del módulo.
    No verifica el sistema completo.
    """
    return barrer()

# ===============================================================
# FIN VERIFICACIÓN
# ===============================================================


# ===============================================================
# INVENTARIO
# ===============================================================

def inventario(peticion=None) -> Dict:
    decls, errores = recolectar()
    return {
        "nombre": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "tipos": list(TIPOS),
        "declaraciones": len(decls),
        "por_tipo": {
            t: sum(1 for d in decls if d["tipo"] == t) for t in TIPOS
        },
        "cuerpos": sorted({d["cuerpo"] for d in decls}),
        "errores": errores,
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
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
# EXPORTACIONES
# ===============================================================

# Resolver referencias de capacidades (str → callable)
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
}
CONTENEDOR["capacidades"] = {
    k: _CAP_MAP.get(v, v) if isinstance(v, str) else v
    for k, v in CONTENEDOR["capacidades"].items()
}

__all__ = [
    "CONTENEDOR",
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
]

# ===============================================================
# FIN EXPORTACIONES
# ===============================================================


# ===============================================================
# EXTENSIONES FUTURAS
# ===============================================================
#
# Nuevas capacidades deberán:
#   • mantener este contrato
#   • no romper compatibilidad hacia atrás
#   • añadirse únicamente en el bloque de capacidades
#   • actualizar inventario y reporting
#   • actualizar VERSION_MODULO
#
# Engine descubrirá automáticamente cualquier capacidad nueva
# declarada en CONTENEDOR["capacidades"].
# Omega la reportará sin modificar su código.
#
# ===============================================================
# FIN EXTENSIONES FUTURAS
# ===============================================================


# ===============================================================
# FIN DEL MÓDULO
# ===============================================================
