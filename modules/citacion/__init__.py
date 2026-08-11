# ===============================================================
# VPSI-TRUTH — modules/citacion/__init__.py
# ===============================================================
#
# MÓDULO:              citacion
# ID:                  CIT
# Rol:                 CIT
# Versión módulo:      2.0
# Versión contrato:    1.0
# Esquema contrato:    VPSI-CONTRACT-1.0
# Estabilidad:         ESTABLE
# Compatible desde:    1.0
# API Engine:          >=1.0
#
# ---------------------------------------------------------------
# PRINCIPIO FUNDAMENTAL
# ---------------------------------------------------------------
#
# CIT no calcula.
# CIT no decide.
# CIT no interpreta.
# CIT no modifica.
# CIT no crea conocimiento.
#
# CIT conoce, resuelve, relaciona y cita.
#
# Toda declaración formal del VPSI debe poder ser resuelta por CIT.
#
# ---------------------------------------------------------------
# DEFINICIÓN
# ---------------------------------------------------------------
#
# CIT es la autoridad universal de fundamentación del VPSI.
#
# Conserva conocimiento resoluble de todas las declaraciones
# públicas existentes dentro del sistema.
#
# Puede resolver, relacionar y citar cualquier axioma, teorema,
# definición, corolario, fórmula, contexto, regla, correlación
# o declaración formal proveniente de cualquier módulo presente
# o futuro.
#
# Su autoridad es absoluta sobre la fundamentación.
# No posee autoridad para alterar el conocimiento.
#
# ---------------------------------------------------------------
# MODELO CONCEPTUAL
# ---------------------------------------------------------------
#
#   Declaración
#        ↓
#   Resolución
#        ↓
#   Relación
#        ↓
#   Cadena normativa
#        ↓
#   Citación
#        ↓
#   Explicación
#
# Internamente CIT administra declaraciones.
# Las citas son únicamente una representación de esas declaraciones.
#
# ---------------------------------------------------------------
# OFICIO ÚNICO
# ---------------------------------------------------------------
#
# Resolver, organizar, relacionar y citar cualquier declaración
# pública perteneciente al VPSI.
#
# ---------------------------------------------------------------
# RESTRICCIÓN ÚNICA
# ---------------------------------------------------------------
#
# Ninguna capacidad de CIT puede modificar el conocimiento declarado.
#
# ---------------------------------------------------------------
# DOS MODOS
# ---------------------------------------------------------------
#
# Modo Engine
#   Engine solicita fundamentación del ciclo.
#   CIT devuelve la cadena documental utilizada.
#
# Modo Consulta
#   Se solicita conocimiento ("Cítame TA-7", "¿Qué dice Def-5.3.1?").
#   El mismo motor responde.
#
# ---------------------------------------------------------------
# ESCALABILIDAD
# ---------------------------------------------------------------
#
# CIT nunca crece en lógica.
# Crece únicamente en conocimiento declarado.
# Todo módulo presente o futuro puede registrar declaraciones
# públicas; CIT las incorpora sin modificar este INIT.
#
# ===============================================================

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

# ===============================================================
# SECCIÓN 1 — IDENTIDAD
# ===============================================================

_ID = "CIT"
_NOMBRE = "citacion"
_ROL = "CIT"
_VERSION = "2.0"
_VERSION_CONTRATO = "1.0"
_ESQUEMA = "VPSI-CONTRACT-1.0"
_ESTABILIDAD = "ESTABLE"
_COMPATIBLE_DESDE = "1.0"
_API_ENGINE = ">=1.0"


# ===============================================================
# SECCIÓN 2 — UNIVERSO DECLARATIVO (forma de declaración / cita)
# ===============================================================
#
# Tipos abiertos: no lista cerrada de módulos.
# Cualquier fuente presente o futura puede aportar declaraciones.
#

TIPOS_DECLARACION = (
    "axioma",
    "teorema",
    "definicion",
    "corolario",
    "lema",
    "regla",
    "principio",
    "formula",
    "correlacion",
    "contexto",
    "limite",
    "factor",
    "procedimiento",
    "contrato",
    "invariante",
    "capacidad",
    "evidencia",
    "citacion",
    # compatibilidad con tipos legados de ciclo
    "ax",
    "mc",
    "cx",
    "tx",
    "ca",
    "fo",
    "re",
    "ct",
    "ch",
    "sf",
)

RELACIONES = (
    "depende_de",
    "fundamenta",
    "contradice",
    "extiende",
    "deriva_de",
    "correlaciona_con",
    "limita",
    "activa",
    "desactiva",
    "requiere",
    "gobierna",
)

CAMPOS_OBLIGATORIOS = (
    "id",
    "tipo",
    "fuente",
    "enunciado",
)

CAMPOS_OPCIONALES = (
    "descripcion",
    "evidencia_ref",
    "o_ref",
    "contexto_ciclo",
    "meta",
    "relaciones",
    "fuente_modulo",  # legado
)


# ===============================================================
# SECCIÓN 3 — REGISTRO DE DECLARACIONES (proceso de ciclo)
# ===============================================================
#
# Memoria operativa del ciclo / consulta.
# No es verdad persistente del corpus AX.
# No modifica conocimiento de otros módulos.
#

_REGISTRO: List[Dict[str, Any]] = []


def _validar_declaracion(decl: Dict[str, Any]) -> List[str]:
    errores: List[str] = []
    if not isinstance(decl, dict):
        return ["declaracion debe ser dict"]
    tipo = decl.get("tipo")
    if tipo is not None and tipo not in TIPOS_DECLARACION:
        # tipos nuevos se admiten si son str no vacío (fractal)
        if not (isinstance(tipo, str) and tipo.strip()):
            errores.append("tipo de declaración inválido: {0}".format(tipo))
    for campo in CAMPOS_OBLIGATORIOS:
        if campo == "id" and decl.get("tipo") == "limite":
            continue
        # compat: fuente <- fuente_modulo
        if campo == "fuente":
            if not decl.get("fuente") and not decl.get("fuente_modulo"):
                errores.append("falta campo obligatorio: fuente")
            continue
        if decl.get(campo) in (None, ""):
            errores.append("falta campo obligatorio: {0}".format(campo))
    return errores


def _normalizar_declaracion(decl: Dict[str, Any]) -> Dict[str, Any]:
    fuente = decl.get("fuente") or decl.get("fuente_modulo") or ""
    out: Dict[str, Any] = {
        "id": decl.get("id"),
        "tipo": decl.get("tipo"),
        "fuente": fuente,
        "fuente_modulo": fuente,  # compat lectura legada
        "enunciado": decl.get("enunciado") or "",
        "descripcion": decl.get("descripcion") or "",
        "evidencia_ref": decl.get("evidencia_ref") or "",
    }
    for c in CAMPOS_OPCIONALES:
        if c in ("fuente_modulo",):
            continue
        if c in decl and decl[c] is not None:
            out[c] = decl[c]
    if "relaciones" not in out:
        out["relaciones"] = list(decl.get("relaciones") or [])
    return out


# ===============================================================
# SECCIÓN 4 — RESOLUCIÓN / REGISTRO / CONSULTA BASE
# ===============================================================

def limpiar_ciclo() -> Dict[str, Any]:
    """Limpia el registro operativo del ciclo. No toca corpus externo."""
    n = len(_REGISTRO)
    _REGISTRO.clear()
    return {"ok": True, "limpiadas": n, "id": _ID}


def registrar(declaracion: Dict[str, Any]) -> Dict[str, Any]:
    """
    Incorpora una declaración pública al registro operativo.
    No modifica el conocimiento de origen.
    """
    errores = _validar_declaracion(declaracion)
    if errores:
        return {"ok": False, "errores": errores, "id": _ID}
    normalizada = _normalizar_declaracion(declaracion)
    _REGISTRO.append(normalizada)
    return {
        "ok": True,
        "n": len(_REGISTRO),
        "declaracion": normalizada,
        "id": _ID,
    }


def resolver(id_decl: str) -> Dict[str, Any]:
    """
    Resuelve una declaración por id.
    1) registro operativo
    2) fuentes registradas del sistema (sin lista cerrada de módulos)
    No inventa enunciados.
    """
    if not id_decl or not str(id_decl).strip():
        return {
            "id": id_decl,
            "resuelto": False,
            "declaracion": None,
            "nota": "id vacío",
        }
    clave = str(id_decl).strip()

    for d in _REGISTRO:
        if d.get("id") == clave and d.get("enunciado"):
            return {
                "id": clave,
                "resuelto": True,
                "declaracion": d,
                "origen": "registro_ciclo",
                "nota": "resuelto desde registro operativo de CIT",
            }

    # Puente genérico a fuentes del paquete citacion (si existen)
    try:
        from modules.citacion.fuentes import ax as fuente_ax

        r = fuente_ax.anunciar_id(
            clave,
            evidencia_ref="cit.resolver",
            registrar=False,
        )
        if r.get("resuelto") and r.get("cita"):
            c = r["cita"]
            decl = _normalizar_declaracion({
                "id": clave,
                "tipo": c.get("tipo") or "axioma",
                "fuente": c.get("fuente_modulo") or "ax",
                "enunciado": c.get("enunciado"),
                "descripcion": c.get("descripcion"),
                "evidencia_ref": c.get("evidencia_ref"),
            })
            return {
                "id": clave,
                "resuelto": True,
                "declaracion": decl,
                "origen": "fuente_sistema",
                "nota": "resuelto desde fuente de declaraciones del sistema",
            }
    except Exception:
        pass

    return {
        "id": clave,
        "resuelto": False,
        "declaracion": None,
        "nota": "sin declaración resoluble en registro ni fuentes cargadas",
    }


def buscar(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Consulta sobre declaraciones del registro operativo.
    Filtros: id, tipo, fuente, o_ref, texto (subcadena en enunciado).
    """
    pet = peticion if isinstance(peticion, dict) else {}
    out = list(_REGISTRO)

    if pet.get("id"):
        out = [d for d in out if d.get("id") == pet["id"]]
    if pet.get("tipo"):
        out = [d for d in out if d.get("tipo") == pet["tipo"]]
    fuente = pet.get("fuente") or pet.get("modulo")
    if fuente:
        out = [
            d for d in out
            if d.get("fuente") == fuente or d.get("fuente_modulo") == fuente
        ]
    if pet.get("o_ref"):
        out = [d for d in out if d.get("o_ref") == pet["o_ref"]]
    if pet.get("texto"):
        t = str(pet["texto"]).lower()
        out = [
            d for d in out
            if t in str(d.get("enunciado") or "").lower()
            or t in str(d.get("descripcion") or "").lower()
        ]

    return {
        "id": _ID,
        "declaraciones": out,
        "n": len(out),
        "filtro": pet,
        "nota": "solo exposición; sin recálculo; sin modificación",
    }


def citar(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Representación citable de declaraciones (compatibilidad de API).
    Internamente = buscar + forma de cita.
    """
    pack = buscar(peticion)
    citas = pack.get("declaraciones") or []
    return {
        "id": _ID,
        "citas": citas,
        "n": len(citas),
        "nota": "citas = representación de declaraciones; sin recálculo",
    }


def resolver_enunciado(id_norma: str) -> Dict[str, Any]:
    """Alias de resolución orientado a enunciado (modo consulta)."""
    r = resolver(id_norma)
    d = r.get("declaracion") or {}
    return {
        "id": id_norma,
        "enunciado": d.get("enunciado") if r.get("resuelto") else None,
        "descripcion": d.get("descripcion") if r.get("resuelto") else None,
        "fuente": d.get("fuente") if r.get("resuelto") else None,
        "fuente_modulo": d.get("fuente") if r.get("resuelto") else None,
        "resuelto": bool(r.get("resuelto")),
        "nota": r.get("nota"),
    }


# ===============================================================
# SECCIÓN 5 — RELACIONES Y CADENA NORMATIVA
# ===============================================================

def relacionar(
    id_a: str,
    relacion: str,
    id_b: str,
) -> Dict[str, Any]:
    """
    Documenta una relación entre dos declaraciones ya resolubles.
    No altera el conocimiento de origen; solo el registro operativo.
    """
    if relacion not in RELACIONES:
        return {
            "ok": False,
            "errores": ["relacion no admitida: {0}".format(relacion)],
            "id": _ID,
        }
    ra = resolver(id_a)
    rb = resolver(id_b)
    if not ra.get("resuelto") or not rb.get("resuelto"):
        return {
            "ok": False,
            "errores": ["ambas declaraciones deben ser resolubles"],
            "a": ra,
            "b": rb,
            "id": _ID,
        }
    enlace = {
        "id": "REL-{0}-{1}-{2}".format(id_a, relacion, id_b),
        "tipo": "citacion",
        "fuente": _NOMBRE,
        "enunciado": "{0} {1} {2}".format(id_a, relacion, id_b),
        "descripcion": "Relación documental registrada por CIT.",
        "relaciones": [
            {"de": id_a, "relacion": relacion, "a": id_b},
        ],
        "meta": {"a": id_a, "b": id_b, "relacion": relacion},
    }
    return registrar(enlace)


def cadena(ids: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Construye una cadena de fundamentación a partir de ids ordenados.
    Cada eslabón debe ser resoluble. No inventa nodos.
    """
    secuencia = list(ids or [])
    eslabones: List[Dict[str, Any]] = []
    faltantes: List[str] = []
    for i in secuencia:
        r = resolver(str(i))
        if r.get("resuelto"):
            eslabones.append(r["declaracion"])
        else:
            faltantes.append(str(i))
    return {
        "id": _ID,
        "cadena": eslabones,
        "n": len(eslabones),
        "faltantes": faltantes,
        "completa": len(faltantes) == 0 and len(eslabones) > 0,
        "nota": (
            "Cadena normativa documental. "
            "Solo declaraciones resolubles; sin recálculo."
        ),
    }


def explicar(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Explicación documental: declaraciones del registro + cadena opcional.
    Toda explicación proviene de declaraciones existentes.
    """
    pet = peticion if isinstance(peticion, dict) else {}
    ids = pet.get("ids") or pet.get("cadena") or []
    if isinstance(ids, str):
        ids = [ids]
    pack_busca = buscar(pet)
    pack_cadena = cadena(list(ids)) if ids else {
        "cadena": pack_busca.get("declaraciones") or [],
        "n": pack_busca.get("n", 0),
        "faltantes": [],
        "completa": (pack_busca.get("n") or 0) > 0,
    }
    return {
        "id": _ID,
        "explicacion": pack_cadena.get("cadena") or [],
        "n": pack_cadena.get("n", 0),
        "faltantes": pack_cadena.get("faltantes") or [],
        "completa": bool(pack_cadena.get("completa")),
        "nota": (
            "Explicación = declaraciones existentes. "
            "CIT no interpreta ni calcula."
        ),
    }


# ===============================================================
# SECCIÓN 6 — ANUNCIO (forma + modo Engine)
# ===============================================================

def _anuncio_de_declaracion(decl: Dict[str, Any]) -> Dict[str, Any]:
    errores = _validar_declaracion(decl)
    if errores:
        return {"ok": False, "errores": errores, "anuncio": None}
    c = _normalizar_declaracion(decl)
    return {
        "ok": True,
        "anuncio": {
            "titulo": "[{0}] {1}".format(c.get("fuente"), c.get("id")),
            "tipo": c.get("tipo"),
            "enunciado": c.get("enunciado"),
            "descripcion": c.get("descripcion"),
            "evidencia_ref": c.get("evidencia_ref"),
            "o_ref": c.get("o_ref"),
            "contexto_ciclo": c.get("contexto_ciclo"),
            "relaciones": c.get("relaciones") or [],
        },
    }


def anunciar_todo(filtro: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    pack = buscar(filtro)
    anuncios: List[Dict[str, Any]] = []
    for d in pack.get("declaraciones") or []:
        r = _anuncio_de_declaracion(d)
        if r.get("ok") and r.get("anuncio"):
            anuncios.append(r["anuncio"])
    return {
        "id": _ID,
        "anuncios": anuncios,
        "n": len(anuncios),
        "filtro": filtro or {},
        "nota": "capacidad total de anuncio sobre declaraciones resolubles",
    }


def _es_paquete_ciclo(obj: Any) -> bool:
    if not isinstance(obj, dict):
        return False
    if "resultado" in obj and isinstance(obj.get("resultado"), dict):
        return True
    if "contexto_cx" in obj and "tipos_peticion" in obj:
        return True
    if obj.get("engine_version") and ("resultado" in obj or "peticion" in obj):
        return True
    return False


def _es_declaracion_suelta(obj: Any) -> bool:
    if not isinstance(obj, dict):
        return False
    if _es_paquete_ciclo(obj):
        return False
    return "tipo" in obj or "enunciado" in obj or "id" in obj


def _evidencia_ref(paquete: Dict[str, Any]) -> str:
    inv = paquete.get("invocador_id") or "ciclo"
    ver = paquete.get("engine_version") or ""
    res = paquete.get("resultado") or {}
    seq = res.get("secuencia")
    base = "ciclo:{0}:v{1}".format(inv, ver)
    if seq is not None:
        base = base + ":seq={0}".format(seq)
    return base


def _o_ref(paquete: Dict[str, Any]) -> Optional[str]:
    res = paquete.get("resultado") or {}
    cx = paquete.get("contexto_cx") or {}
    reg = cx.get("registro") if isinstance(cx.get("registro"), dict) else {}
    for src in (res, cx, reg, paquete.get("peticion") or {}):
        if not isinstance(src, dict):
            continue
        for k in ("O_id", "o_id", "O_context", "contexto", "enunciado_O"):
            v = src.get(k)
            if v is not None and str(v).strip() and str(v).strip().lower() not in (
                "undefined",
                "indefinido",
                "none",
                "null",
            ):
                return str(v).strip()[:200]
    return None


def _anunciar_paquete(paquete: Dict[str, Any]) -> Dict[str, Any]:
    """
    Modo Engine: fundamentación documental del ciclo.
    Lee solo el paquete. No calcula. No inventa factores.
    Incorpora declaraciones desde fuentes del sistema si están disponibles.
    Lista de fuentes: abierta (cualquier módulo presente o futuro vía fuentes/).
    """
    limpiar_ciclo()

    res = paquete.get("resultado") if isinstance(paquete.get("resultado"), dict) else {}
    cx = paquete.get("contexto_cx") if isinstance(paquete.get("contexto_cx"), dict) else {}
    tipos = list(paquete.get("tipos_peticion") or cx.get("tipos_peticion") or [])
    if not tipos:
        tipos = ["dame_cadena_completa"]

    evid = _evidencia_ref(paquete)
    o_ref = _o_ref(paquete)
    ctx_ciclo = str(res.get("estado") or cx.get("modo_entrada") or "ciclo")

    errores: List[str] = []
    n_fuentes = 0

    def _ok_fuente(r: Any) -> None:
        nonlocal n_fuentes
        if isinstance(r, dict) and r.get("ok") is False:
            errores.extend([str(e) for e in (r.get("errores") or [])])
        else:
            n_fuentes += 1

    # Fuentes opcionales bajo modules/citacion/fuentes/ (fractal: añadir archivo,
    # no modificar este INIT). Fallo de una fuente no detiene el resto.
    try:
        from modules.citacion.fuentes import cx as fuente_cx

        if cx:
            _ok_fuente(
                fuente_cx.desde_resolver(
                    cx,
                    evidencia_ref=evid,
                    contexto_ciclo=ctx_ciclo,
                    registrar=True,
                )
            )
        reg = cx.get("registro") if isinstance(cx.get("registro"), dict) else {}
        estado_cx = reg.get("estado") or cx.get("estado")
        if estado_cx in ("indefinido",) or res.get("estado") == "UNDEFINED":
            _ok_fuente(
                fuente_cx.anunciar_indefinido(
                    motivo=str(
                        res.get("razon")
                        or "O/contexto no usable en el ciclo"
                    ),
                    evidencia_ref=evid,
                    o_ref=o_ref,
                    contexto_ciclo=ctx_ciclo,
                    registrar=True,
                )
            )
    except Exception as e:
        errores.append("fuente cx: {0}: {1}".format(type(e).__name__, e))

    try:
        from modules.citacion.fuentes import ca as fuente_ca

        factores = res.get("factores") if isinstance(res.get("factores"), dict) else {}
        C, L, K = factores.get("C"), factores.get("L"), factores.get("K")
        if C is not None or L is not None or K is not None:
            _ok_fuente(
                fuente_ca.anunciar_factores(
                    C=C, L=L, K=K,
                    evidencia_ref=evid, o_ref=o_ref,
                    contexto_ciclo=ctx_ciclo, registrar=True,
                )
            )
        elif res.get("estado") in ("PARCIAL", "UNDEFINED"):
            _ok_fuente(
                fuente_ca.anunciar_sin_factores(
                    motivo=str(res.get("razon") or "factores incompletos"),
                    evidencia_ref=evid, o_ref=o_ref,
                    contexto_ciclo=ctx_ciclo, registrar=True,
                )
            )
    except Exception as e:
        errores.append("fuente ca: {0}: {1}".format(type(e).__name__, e))

    try:
        from modules.citacion.fuentes import fo as fuente_fo

        tru_ri = res.get("tru_ri") or res.get("Tru_Ri")
        tru_total = res.get("tru_total") or res.get("Tru_total")
        if (
            tru_ri is not None
            and tru_total is not None
            and str(tru_ri) not in ("UNDEFINED", "None")
            and str(tru_total) not in ("UNDEFINED", "None")
        ):
            factores = res.get("factores") if isinstance(res.get("factores"), dict) else {}
            _ok_fuente(
                fuente_fo.anunciar_formula_aplicada(
                    tru_ri=tru_ri, tru_total=tru_total,
                    evidencia_ref=evid, o_ref=o_ref,
                    contexto_ciclo=ctx_ciclo,
                    C=factores.get("C"), L=factores.get("L"), K=factores.get("K"),
                    registrar=True,
                )
            )
        elif "dame_normas" in tipos or "dame_cadena_completa" in tipos:
            _ok_fuente(
                fuente_fo.anunciar_expresion(
                    evidencia_ref=evid, o_ref=o_ref,
                    contexto_ciclo=ctx_ciclo, registrar=True,
                )
            )
    except Exception as e:
        errores.append("fuente fo: {0}: {1}".format(type(e).__name__, e))

    try:
        from modules.citacion.fuentes import ct as fuente_ct

        if res.get("alpha") is not None or res.get("beta") is not None:
            _ok_fuente(
                fuente_ct.anunciar_valores(
                    alpha=res.get("alpha"), beta=res.get("beta"),
                    evidencia_ref=evid, o_ref=o_ref,
                    contexto_ciclo=ctx_ciclo, registrar=True,
                )
            )
        elif "dame_normas" in tipos or "dame_cadena_completa" in tipos:
            _ok_fuente(
                fuente_ct.anunciar_ancla(
                    evidencia_ref=evid, o_ref=o_ref,
                    contexto_ciclo=ctx_ciclo, registrar=True,
                )
            )
    except Exception as e:
        errores.append("fuente ct: {0}: {1}".format(type(e).__name__, e))

    try:
        from modules.citacion.fuentes import ax as fuente_ax

        ids: List[str] = []
        val = res.get("valuacion") if isinstance(res.get("valuacion"), dict) else {}
        for src in (val.get("ids"), cx.get("ids_cx_relevantes"), res.get("ids")):
            if isinstance(src, list):
                for i in src:
                    s = str(i).strip()
                    if s and s not in ids:
                        ids.append(s)
        if ids:
            pack_ax = fuente_ax.anunciar_lista(
                ids,
                evidencia_ref=evid, o_ref=o_ref,
                contexto_ciclo=ctx_ciclo, registrar=True,
            )
            n_fuentes += int(pack_ax.get("n") or 0)
    except Exception as e:
        errores.append("fuente ax: {0}: {1}".format(type(e).__name__, e))

    try:
        from modules.citacion.fuentes import mc as fuente_mc

        if "permite_k" in cx:
            _ok_fuente(
                fuente_mc.anunciar_permite_k(
                    permite_k=bool(cx.get("permite_k")),
                    enunciado="permite_k={0} según contexto del ciclo.".format(
                        cx.get("permite_k")
                    ),
                    evidencia_ref=evid, o_ref=o_ref,
                    contexto_ciclo=ctx_ciclo, registrar=True,
                )
            )
        informe_mc = paquete.get("informe_mecanica") or res.get("informe_mecanica")
        if isinstance(informe_mc, dict):
            _ok_fuente(
                fuente_mc.desde_informe_barrer(
                    informe_mc,
                    evidencia_ref=evid, o_ref=o_ref,
                    contexto_ciclo=ctx_ciclo, registrar=True,
                )
            )
    except Exception as e:
        errores.append("fuente mc: {0}: {1}".format(type(e).__name__, e))

    try:
        from modules.citacion.fuentes import limite as fuente_lim

        factores = res.get("factores") if isinstance(res.get("factores"), dict) else {}
        tiene_factores = all(
            factores.get(k) is not None
            and str(factores.get(k)) not in ("UNDEFINED", "None", "")
            for k in ("C", "L", "K")
        )
        permite_k = cx.get("permite_k")
        reg = cx.get("registro") if isinstance(cx.get("registro"), dict) else {}
        o_estado = reg.get("estado")
        if res.get("estado") == "UNDEFINED":
            o_estado = o_estado or "indefinido"

        pack_lim = fuente_lim.anunciar_desde_ciclo(
            evidencia_ref=evid, o_ref=o_ref, contexto_ciclo=ctx_ciclo,
            permite_k=permite_k if isinstance(permite_k, bool) else None,
            tiene_factores=tiene_factores, o_estado=o_estado, registrar=True,
        )
        if pack_lim.get("citas"):
            n_fuentes += len(pack_lim.get("citas") or [])
    except Exception as e:
        errores.append("fuente limite: {0}: {1}".format(type(e).__name__, e))

    # Auto-declaración del oficio CIT (fractal, no cálculo)
    try:
        from modules.citacion.esquema import plantilla

        cita_self = plantilla(
            id="CIT-CICLO",
            tipo="citacion",
            fuente_modulo=_NOMBRE,
            enunciado=(
                "CIT fundamentó el ciclo; estado_resultado={0}; "
                "tipos_peticion={1}.".format(res.get("estado"), tipos)
            ),
            descripcion=(
                "Declaración del oficio de fundamentación; "
                "no calcula; documenta el cierre de anuncio."
            ),
            evidencia_ref=evid,
            o_ref=o_ref,
            contexto_ciclo=ctx_ciclo,
            meta={"tipos_peticion": tipos, "estado": res.get("estado")},
        )
        registrar(cita_self)
        n_fuentes += 1
    except Exception as e:
        errores.append("declaracion fractal: {0}: {1}".format(type(e).__name__, e))

    anuncios_pack = anunciar_todo()
    return {
        "id": _ID,
        "estado": "OK" if n_fuentes > 0 else "VACIO",
        "ok": n_fuentes > 0,
        "n_declaraciones": len(_REGISTRO),
        "n_citas": len(_REGISTRO),
        "n_anuncios": anuncios_pack.get("n", 0),
        "anuncios": anuncios_pack.get("anuncios") or [],
        "tipos_peticion": tipos,
        "evidencia_ref": evid,
        "o_ref": o_ref,
        "errores": errores,
        "engine_version": paquete.get("engine_version"),
        "nota": (
            "CIT: autoridad universal de fundamentación sobre el paquete; "
            "cero agencia sobre valores numéricos; sin recálculo; "
            "sin modificación del conocimiento declarado."
        ),
    }


def anunciar(arg: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Entrada única — modo Engine y modo Consulta.

    - paquete de ciclo → cadena documental completa
    - declaración suelta → registro + anuncio de forma
    - None → anunciar_todo() del registro actual
    """
    if arg is None:
        return anunciar_todo()

    if _es_paquete_ciclo(arg):
        return _anunciar_paquete(arg)

    if _es_declaracion_suelta(arg):
        reg = registrar(arg)
        if not reg.get("ok"):
            return {
                "ok": False,
                "errores": reg.get("errores") or ["declaracion inválida"],
                "anuncio": None,
                "id": _ID,
            }
        return _anuncio_de_declaracion(reg.get("declaracion") or arg)

    return {
        "ok": False,
        "estado": "ERROR_FORMA",
        "errores": [
            "anunciar: se esperaba paquete de ciclo o una declaración "
            "con tipo/enunciado/id"
        ],
        "anuncio": None,
        "id": _ID,
    }


# ===============================================================
# SECCIÓN 7 — REPORTING ESTÁNDAR
# ===============================================================

def inventario(peticion: Any = None) -> Dict[str, Any]:
    return {
        "id": _ID,
        "nombre": _NOMBRE,
        "rol": _ROL,
        "version": _VERSION,
        "version_contrato": _VERSION_CONTRATO,
        "esquema": _ESQUEMA,
        "estabilidad": _ESTABILIDAD,
        "compatible_desde": _COMPATIBLE_DESDE,
        "api_engine": _API_ENGINE,
        "tipos_declaracion": list(TIPOS_DECLARACION),
        "relaciones": list(RELACIONES),
        "campos_obligatorios": list(CAMPOS_OBLIGATORIOS),
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "registro_n": len(_REGISTRO),
        "funcion": (
            "Autoridad universal de fundamentación. "
            "Resuelve, organiza, relaciona y cita cualquier declaración "
            "pública del VPSI. No modifica conocimiento."
        ),
        "modos": ["engine", "consulta"],
        "requiere": [],
    }


def reporte(peticion: Any = None) -> Dict[str, Any]:
    return {
        "id": _ID,
        "nombre": _NOMBRE,
        "rol": _ROL,
        "version": _VERSION,
        "estado": "OPERATIVO",
        "coherente": True,
        "registro_n": len(_REGISTRO),
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "nota": (
            "CIT documenta y fundamenta. "
            "No calcula. No altera declaraciones de origen."
        ),
    }


def diagnostico(peticion: Any = None) -> Dict[str, Any]:
    return {
        "id": _ID,
        "nombre": _NOMBRE,
        "rol": _ROL,
        "estado": "OPERATIVO",
        "problemas": [],
        "advertencias": [],
        "recomendaciones": [],
        "coherente": True,
        "registro_n": len(_REGISTRO),
        "nota": "Diagnóstico propio de CIT. No consulta autoridades ajenas.",
    }


def barrer(peticion: Any = None) -> Dict[str, Any]:
    errores: List[str] = []
    choques: List[str] = []

    for t in TIPOS_DECLARACION:
        if not isinstance(t, str) or not t:
            errores.append("tipo inválido en TIPOS_DECLARACION")

    # Restricción única: ninguna capacidad puede modificar conocimiento
    for cap in CONTENEDOR["capacidades"]:
        nombre = str(cap).lower()
        if any(x in nombre for x in ("modificar", "alterar", "reescribir", "borrar_corpus")):
            choques.append(
                "capacidad incompatible con restricción única de CIT: {0}".format(cap)
            )

    coherente = not errores and not choques
    return {
        "id": _ID,
        "nombre": _NOMBRE,
        "rol": _ROL,
        "version": _VERSION,
        "coherente": coherente,
        "choques": choques,
        "errores": errores,
        "registro_n": len(_REGISTRO),
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "nota": (
            "Centinela CIT: integridad del oficio de fundamentación. "
            "Sin juicio de verdad numérica."
        ),
    }


def verificar(peticion: Any = None) -> Dict[str, Any]:
    return barrer(peticion)


def verificar_salida(salida: Any) -> bool:
    if not isinstance(salida, dict):
        return False
    return (
        "id" in salida
        or "coherente" in salida
        or "anuncios" in salida
        or "declaraciones" in salida
        or "citas" in salida
        or "resuelto" in salida
    )


# ===============================================================
# SECCIÓN 8 — CONTENEDOR (VPSI-CONTRACT-1.0)
# ===============================================================

CONTENEDOR: Dict[str, Any] = {
    "esquema": _ESQUEMA,
    "version_contrato": _VERSION_CONTRATO,
    "version_modulo": _VERSION,
    "id": _ID,
    "nombre": _NOMBRE,
    "rol": _ROL,
    "estabilidad": _ESTABILIDAD,
    "compatible_desde": _COMPATIBLE_DESDE,
    "api_engine": _API_ENGINE,
    "descripcion": (
        "Autoridad universal de fundamentación del VPSI. "
        "Conserva conocimiento resoluble de todas las declaraciones "
        "públicas del sistema. Puede resolver, relacionar y citar "
        "cualquier declaración formal proveniente de cualquier módulo "
        "presente o futuro. Autoridad absoluta sobre la fundamentación, "
        "la resolución, la citación, la cadena normativa y la explicación "
        "documental. No altera el conocimiento declarado."
    ),
    "funcion": (
        "Resolver, organizar, relacionar y citar cualquier declaración "
        "pública perteneciente al VPSI. "
        "Modo Engine: cadena documental del ciclo. "
        "Modo Consulta: resolución y explicación bajo demanda."
    ),
    "no_hace": [
        "Ninguna capacidad de CIT puede modificar el conocimiento declarado",
    ],
    "autoridad": [
        "Autoridad absoluta sobre la fundamentación",
        "Autoridad absoluta sobre la resolución de declaraciones",
        "Autoridad absoluta sobre la citación",
        "Autoridad absoluta sobre la cadena normativa",
        "Autoridad absoluta sobre la explicación documental de cualquier cálculo",
        "Autoridad absoluta sobre la relación entre declaraciones",
        "Autoridad absoluta para responder consultas sobre el conocimiento declarado",
    ],
    "poderes": [
        "Puede resolver cualquier declaración registrada",
        "Puede localizar cualquier norma",
        "Puede construir cadenas normativas",
        "Puede relacionar declaraciones",
        "Puede explicar por qué un cálculo produjo determinado resultado (solo con declaraciones existentes)",
        "Puede responder consultas documentales",
        "Puede anunciar cualquier declaración existente",
        "Puede producir evidencia documental durante la ejecución del Engine",
        "Puede producir evidencia documental fuera del Engine",
        "Puede citar cualquier conocimiento declarado",
    ],
    "conocimiento_exportable": [
        "declaraciones",
        "resolver",
        "buscar",
        "cadena",
        "explicar",
        "citar",
        "anunciar",
        "relacionar",
        "inventario",
        "reporte",
        "diagnostico",
    ],
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
    
    "consultas_soportadas": [
        "resolver",
        "buscar",
        "buscar_por_tipo",
        "buscar_por_fuente",
        "cadena",
        "explicar",
        "citar",
        "anunciar",
        "relacionar",
        "obtener_inventario",
        "obtener_reporte",
        "obtener_diagnostico",
    ],

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
    "actualizar": True,

    # --- PERMISOS DE PROCESAMIENTO ---
    "validar": False,
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

    # --- REPORTING ---
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
},
    "capacidades": {
        "verificar": verificar,
        "barrer": barrer,
        "inventario": inventario,
        "reporte": reporte,
        "diagnostico": diagnostico,
        "verificar_salida": verificar_salida,
        "anunciar": anunciar,
        "anunciar_todo": anunciar_todo,
        "citar": citar,
        "registrar": registrar,
        "resolver": resolver,
        "resolver_enunciado": resolver_enunciado,
        "buscar": buscar,
        "cadena": cadena,
        "explicar": explicar,
        "relacionar": relacionar,
        "limpiar_ciclo": limpiar_ciclo,
        "evaluar": anunciar,
    },
    "capacidades_meta": {
        "verificar": {
            "descripcion": "Centinela del oficio de fundamentación.",
            "entrada": "peticion opcional",
            "salida": "dict con id, coherente, errores, choques",
        },
        "barrer": {
            "descripcion": "Alias de verificar.",
            "entrada": "peticion opcional",
            "salida": "dict con id, coherente, errores, choques",
        },
        "inventario": {
            "descripcion": "Inventario contractual de CIT.",
            "entrada": "peticion opcional",
            "salida": "dict con id, nombre, rol, version, capacidades, tipos_declaracion",
        },
        "reporte": {
            "descripcion": "Reporte de estado de CIT.",
            "entrada": "peticion opcional",
            "salida": "dict con id, estado, coherente, registro_n",
        },
        "diagnostico": {
            "descripcion": "Diagnóstico propio de CIT.",
            "entrada": "peticion opcional",
            "salida": "dict con id, estado, problemas, advertencias",
        },
        "verificar_salida": {
            "descripcion": "Forma mínima de salida de CIT.",
            "entrada": "salida: dict",
            "salida": "bool",
        },
        "anunciar": {
            "descripcion": (
                "Modo Engine (paquete) o Consulta (declaración). "
                "Fundamentación documental sin recálculo."
            ),
            "entrada": "paquete de ciclo | declaración | None",
            "salida": "dict con anuncios / cadena documental",
        },
        "anunciar_todo": {
            "descripcion": "Anuncia todas las declaraciones del registro operativo.",
            "entrada": "filtro opcional",
            "salida": "dict con anuncios, n",
        },
        "citar": {
            "descripcion": "Representación citable de declaraciones.",
            "entrada": "peticion opcional (filtros)",
            "salida": "dict con citas, n",
        },
        "registrar": {
            "descripcion": "Incorpora declaración al registro operativo. No altera origen.",
            "entrada": "declaracion: dict",
            "salida": "dict con ok, declaracion",
        },
        "resolver": {
            "descripcion": "Resuelve una declaración por id.",
            "entrada": "id_decl: str",
            "salida": "dict con resuelto, declaracion",
        },
        "resolver_enunciado": {
            "descripcion": "Alias de resolución orientado a enunciado.",
            "entrada": "id_norma: str",
            "salida": "dict con resuelto, enunciado",
        },
        "buscar": {
            "descripcion": "Consulta declaraciones del registro operativo.",
            "entrada": "peticion con filtros opcionales",
            "salida": "dict con declaraciones, n",
        },
        "cadena": {
            "descripcion": "Construye cadena normativa a partir de ids resolubles.",
            "entrada": "ids: list[str]",
            "salida": "dict con cadena, faltantes, completa",
        },
        "explicar": {
            "descripcion": "Explicación documental solo con declaraciones existentes.",
            "entrada": "peticion opcional (ids/filtros)",
            "salida": "dict con explicacion, n, completa",
        },
        "relacionar": {
            "descripcion": "Documenta relación entre dos declaraciones resolubles.",
            "entrada": "id_a, relacion, id_b",
            "salida": "dict con ok, declaracion de enlace",
        },
        "limpiar_ciclo": {
            "descripcion": "Limpia registro operativo del ciclo.",
            "entrada": "ninguna",
            "salida": "dict con ok, limpiadas",
        },
        "evaluar": {
            "descripcion": "Alias de anunciar (compatibilidad Engine).",
            "entrada": "paquete | declaración | None",
            "salida": "dict de anuncio / fundamentación",
        },
    },
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
    "estados_validos": [
        "NO_INICIADO",
        "OPERATIVO",
        "DEGRADADO",
        "RECHAZADO",
    ],
    "invariantes": [
        "CIT conserva conocimiento declarativo universal resoluble",
        "CIT puede resolver cualquier declaración registrada",
        "CIT puede citar cualquier declaración registrada",
        "CIT puede construir cadenas de fundamentación",
        "CIT puede responder consultas documentales",
        "CIT nunca altera el conocimiento declarado",
        "CIT nunca modifica resultados",
        "CIT nunca reemplaza la autoridad de otros módulos",
        "CIT únicamente documenta y fundamenta",
        "Toda explicación producida por CIT debe provenir de declaraciones existentes",
        "Toda cita debe ser resoluble",
        "Toda cadena normativa debe ser trazable",
        "el id del módulo nunca cambia",
        "el rol nunca cambia",
        "las capacidades declaradas son callables tras la resolución",
        "este módulo no inventa capacidades no declaradas en CONTENEDOR",
        "este módulo siempre puede reportar su propio estado",
        "inventario() siempre incluye id, nombre, rol, version",
    ],
}


# ===============================================================
# SECCIÓN 9 — EXPORTS
# ===============================================================

__all__ = [
    "CONTENEDOR",
    "TIPOS_DECLARACION",
    "RELACIONES",
    "CAMPOS_OBLIGATORIOS",
    "CAMPOS_OPCIONALES",
    "registrar",
    "resolver",
    "resolver_enunciado",
    "buscar",
    "citar",
    "anunciar",
    "anunciar_todo",
    "cadena",
    "explicar",
    "relacionar",
    "limpiar_ciclo",
    "inventario",
    "reporte",
    "diagnostico",
    "barrer",
    "verificar",
    "verificar_salida",
]
