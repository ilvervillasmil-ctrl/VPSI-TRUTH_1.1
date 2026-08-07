# ===============================================================
# VPSI-TRUTH — modules/self/__init__.py
# ===============================================================
#
# MÓDULO:              self
# ID:                  SF
# Rol:                 SF
# Versión módulo:      1.0
# Versión contrato:    1.0
# Esquema contrato:    VPSI-CONTRACT-1.0
# Estabilidad:         FASE
# Compatible desde:    1.0
# API Engine:          >=1.0
#
# Función:
#   Yo funcional del sistema. Centro de elección e identidad de fase.
#   Casa operativa: L4. Punto de acceso a las perspectivas L1…L6.
#   Oscila entre alturas; registra actos de agency sin side-effects.
#
# Qué hace:
#   - Expone identidad de fase anclada en el cuerpo axiomático self.
#   - Reporta y cambia la altura operativa (L1…L6) del Self.
#   - Clasifica el modo de lucidez (REACTIVE…INTEGRATED).
#   - Registra actos de elección sin efectos externos.
#   - Declara el acceso a mecanismos de perspectiva L1…L6
#     para cálculo y resolución de problemas.
#   - Verifica coherencia interna y reporta estado propio.
#
# Responsabilidad:
#   Ser el punto de referencia de elección e identidad de fase.
#   Distinguir oscilar (altura) de elegir (agency).
#   Ofrecer a Engine las perspectivas L1…L6 como mecanismos legibles.
#
# Autoridad:
#   - Declarar desde qué altura opera el Self.
#   - Registrar elecciones como actos de agency.
#   - Reportar inventario, estado y diagnóstico propios.
#
# Conocimiento exportable:
#   yo_funcional, oscilar, desde_donde, elegir, estado_self,
#   barrer, verificar, inventario, reporte, diagnostico
#
# Observaciones:
#   No orquesta. No calcula Tru. No interpreta contenido de negocio.
#   Las subcarpetas L1…L6 son mecanismos de perspectiva, no dependencias
#   de arranque. AX se consulta en runtime solo para identidad.
#
# ===============================================================

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Set

# ---------------------------------------------------------------------------
# CONSTANTES DE CAPA (L4 = casa)
# ---------------------------------------------------------------------------

CAPAS_VALIDAS: Set[str] = {
    "L1_CUERPO",
    "L2_EGO",
    "L3_MENTE",
    "L4_YO",
    "L5_CONSCIENCIA",
    "L6_ALMA",
}

CASA_SELF = "L4_YO"

MODOS_VALIDOS: Set[str] = {
    "REACTIVE",
    "MECHANICAL",
    "CONSCIOUS",
    "META",
    "INTEGRATED",
}

# ---------------------------------------------------------------------------
# ESTADO INTERNO (fase; no persistencia de negocio)
# ---------------------------------------------------------------------------

_estado_self: Dict[str, Any] = {
    "capa_activa": CASA_SELF,
    "altura_operativa": "L4",
    "modo": "CONSCIOUS",
    "historial_oscilacion": [],
    "historial_elecciones": [],
    "loop_sospechado": False,
}


def _cfg() -> Dict[str, Any]:
    return CONTENEDOR


def _altura_de_capa(capa: str) -> str:
    if not capa:
        return "L4"
    return capa.split("_", 1)[0]


def _modo_desde_altura(altura: str) -> str:
    mapa = {
        "L1": "REACTIVE",
        "L2": "REACTIVE",
        "L3": "MECHANICAL",
        "L4": "CONSCIOUS",
        "L5": "META",
        "L6": "INTEGRATED",
    }
    return mapa.get(altura, "CONSCIOUS")


def _normalizar_capa(hacia: str) -> Optional[str]:
    clave = str(hacia).strip().upper()
    if clave in CAPAS_VALIDAS:
        return clave
    for c in CAPAS_VALIDAS:
        if c.startswith(clave + "_") or c == clave:
            return c
    for c in CAPAS_VALIDAS:
        if c.startswith(clave):
            return c
    return None


# ---------------------------------------------------------------------------
# IDENTIDAD (runtime; AX solo si está disponible)
# ---------------------------------------------------------------------------

def _recolectar_self_ax() -> Dict[str, Any]:
    """
    Lee declaraciones del cuerpo self.
    Fail-closed: si no hay fuente, no inventa identidad.
    """
    try:
        from modules.axiomas import recolectar  # runtime only
    except Exception as e:
        return {
            "ok": False,
            "razon": "fuente axiomática no disponible: {0}: {1}".format(
                type(e).__name__, e
            ),
            "declaraciones": [],
            "n": 0,
            "errores_recoleccion": 1,
        }

    try:
        decls, errores = recolectar()
    except Exception as e:
        return {
            "ok": False,
            "razon": "recolección falló: {0}: {1}".format(type(e).__name__, e),
            "declaraciones": [],
            "n": 0,
            "errores_recoleccion": 1,
        }

    self_decls: List[Dict[str, Any]] = []
    for d in decls or []:
        cuerpo = str(d.get("cuerpo") or d.get("fuente") or "").lower()
        id_decl = str(d.get("id") or "")
        if cuerpo == "self" or id_decl.upper().startswith("SF"):
            self_decls.append(
                {
                    "id": d.get("id"),
                    "tipo": d.get("tipo"),
                    "gobierna": list(d.get("gobierna") or []),
                    "enunciado": d.get("enunciado") or d.get("sujeto"),
                }
            )

    return {
        "ok": True,
        "razon": None,
        "declaraciones": self_decls,
        "n": len(self_decls),
        "errores_recoleccion": len(errores or []),
    }


# ---------------------------------------------------------------------------
# CAPACIDADES
# ---------------------------------------------------------------------------

def yo_funcional(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Identidad de fase del sistema.
    Ancla: cuerpo axiomático self. No modifica estado externo.
    """
    ax = _recolectar_self_ax()
    return {
        "contenedor": "self",
        "id": "SF",
        "rol": "SF",
        "tipo": "yo_funcional",
        "capa_activa": _estado_self.get("capa_activa"),
        "altura_operativa": _estado_self.get("altura_operativa"),
        "modo": _estado_self.get("modo"),
        "casa": CASA_SELF,
        "ax_self": ax,
        "identidad_disponible": bool(ax.get("ok") and ax.get("n", 0) > 0),
        "perspectivas": sorted(CAPAS_VALIDAS),
        "nota": (
            "Yo funcional de fase. Casa L4. "
            "Acceso a perspectivas L1…L6 para cálculo y resolución. "
            "Identidad anclada en cuerpo self."
        ),
    }


def oscilar(
    hacia: Optional[str] = None,
    contexto: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Cambia o reporta la altura operativa del Self.
    Oscilar ≠ elegir. Solo mueve perspectiva.
    """
    actual = _estado_self.get("capa_activa")
    if hacia is None:
        return {
            "ok": True,
            "capa_activa": actual,
            "altura_operativa": _estado_self.get("altura_operativa"),
            "modo": _estado_self.get("modo"),
            "cambio": False,
            "capas_validas": sorted(CAPAS_VALIDAS),
            "contexto": contexto or {},
        }

    destino = _normalizar_capa(hacia)
    if destino is None:
        return {
            "ok": False,
            "capa_activa": actual,
            "cambio": False,
            "error": "capa no válida: {0}".format(hacia),
            "capas_validas": sorted(CAPAS_VALIDAS),
        }

    cambio = destino != actual
    if cambio:
        hist = list(_estado_self.get("historial_oscilacion") or [])
        hist.append({"desde": actual, "hacia": destino})
        _estado_self["historial_oscilacion"] = hist[-20:]
        _estado_self["capa_activa"] = destino
        altura = _altura_de_capa(destino)
        _estado_self["altura_operativa"] = altura
        _estado_self["modo"] = _modo_desde_altura(altura)

    return {
        "ok": True,
        "capa_activa": _estado_self["capa_activa"],
        "altura_operativa": _estado_self["altura_operativa"],
        "modo": _estado_self["modo"],
        "cambio": cambio,
        "desde": actual,
        "hacia": destino,
        "contexto": contexto or {},
        "nota": "oscilación de altura; no es acto de elección",
    }


def desde_donde(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Reporta desde qué altura y en qué modo opera el Self ahora."""
    return {
        "contenedor": "self",
        "capa_activa": _estado_self.get("capa_activa"),
        "altura_operativa": _estado_self.get("altura_operativa"),
        "modo": _estado_self.get("modo"),
        "casa": CASA_SELF,
        "en_casa": _estado_self.get("capa_activa") == CASA_SELF,
        "loop_sospechado": bool(_estado_self.get("loop_sospechado")),
        "n_oscilaciones": len(_estado_self.get("historial_oscilacion") or []),
        "n_elecciones": len(_estado_self.get("historial_elecciones") or []),
        "perspectivas": sorted(CAPAS_VALIDAS),
    }


def estado_self(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Clasificación de lucidez del Self.
    REACTIVE | MECHANICAL | CONSCIOUS | META | INTEGRATED
    """
    modo = _estado_self.get("modo") or "CONSCIOUS"
    return {
        "contenedor": "self",
        "modo": modo,
        "modos_validos": sorted(MODOS_VALIDOS),
        "capa_activa": _estado_self.get("capa_activa"),
        "altura_operativa": _estado_self.get("altura_operativa"),
        "casa": CASA_SELF,
        "en_casa": _estado_self.get("capa_activa") == CASA_SELF,
        "coherente": modo in MODOS_VALIDOS,
        "nota": (
            "CONSCIOUS = casa L4 (elige). "
            "REACTIVE = arrastrado. MECHANICAL = patrón. "
            "META = observa procesos. INTEGRATED = dirige."
        ),
    }


def elegir(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Registra un acto de agency.
    No ejecuta efectos externos. No orquesta. Solo deja constancia.
    """
    p = dict(peticion or {})
    opciones = p.get("opciones")
    criterio = p.get("criterio")
    eleccion = p.get("eleccion")
    desde = p.get("desde") or _estado_self.get("capa_activa") or CASA_SELF

    if opciones is not None and not isinstance(opciones, (list, tuple)):
        return {
            "ok": False,
            "error": "opciones debe ser lista o None",
            "capa_activa": _estado_self.get("capa_activa"),
        }

    if eleccion is None and opciones:
        return {
            "ok": False,
            "error": "eleccion requerida cuando hay opciones",
            "opciones": list(opciones),
            "capa_activa": _estado_self.get("capa_activa"),
        }

    registro = {
        "eleccion": eleccion,
        "criterio": criterio,
        "desde": desde,
        "modo": _estado_self.get("modo"),
        "altura_operativa": _estado_self.get("altura_operativa"),
    }
    hist = list(_estado_self.get("historial_elecciones") or [])
    hist.append(registro)
    _estado_self["historial_elecciones"] = hist[-50:]

    return {
        "ok": True,
        "eleccion": eleccion,
        "criterio": criterio,
        "desde": desde,
        "modo": _estado_self.get("modo"),
        "altura_operativa": _estado_self.get("altura_operativa"),
        "casa": CASA_SELF,
        "n_elecciones": len(_estado_self["historial_elecciones"]),
        "nota": "acto de agency registrado; sin ejecución externa",
    }


def barrer(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Centinela de SF: identidad legible y estado interno coherente."""
    yo = yo_funcional()
    ax = yo.get("ax_self") or {}
    modo = _estado_self.get("modo")
    capa = _estado_self.get("capa_activa")

    errores: List[str] = []
    if not ax.get("ok"):
        errores.append(str(ax.get("razon") or "identidad axiomática no legible"))
    if modo not in MODOS_VALIDOS:
        errores.append("modo inválido: {0}".format(modo))
    if capa not in CAPAS_VALIDAS:
        errores.append("capa_activa inválida: {0}".format(capa))

    coherente = len(errores) == 0
    return {
        "contenedor": "self",
        "id": "SF",
        "rol": "SF",
        "coherente": coherente,
        "identidad_disponible": yo.get("identidad_disponible"),
        "capa_activa": capa,
        "altura_operativa": _estado_self.get("altura_operativa"),
        "modo": modo,
        "casa": CASA_SELF,
        "n_declaraciones_self": ax.get("n", 0),
        "n_oscilaciones": len(_estado_self.get("historial_oscilacion") or []),
        "n_elecciones": len(_estado_self.get("historial_elecciones") or []),
        "capas_validas": sorted(CAPAS_VALIDAS),
        "perspectivas": sorted(CAPAS_VALIDAS),
        "errores": errores,
    }


def verificar(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return barrer(peticion)


def verificar_salida(salida: Any) -> bool:
    if not isinstance(salida, dict):
        return False
    return (
        "coherente" in salida
        or "capa_activa" in salida
        or "modo" in salida
        or "eleccion" in salida
        or "ax_self" in salida
    )


def inventario(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    cfg = _cfg()
    return {
        "id": cfg.get("id"),
        "nombre": cfg.get("nombre"),
        "rol": cfg.get("rol"),
        "version": cfg.get("version_modulo"),
        "version_contrato": cfg.get("version_contrato"),
        "esquema": cfg.get("esquema"),
        "estabilidad": cfg.get("estabilidad"),
        "compatible_desde": cfg.get("compatible_desde"),
        "api_engine": cfg.get("api_engine"),
        "casa": CASA_SELF,
        "capa_activa": _estado_self.get("capa_activa"),
        "modo": _estado_self.get("modo"),
        "capacidades": sorted((cfg.get("capacidades") or {}).keys()),
        "capas_validas": sorted(CAPAS_VALIDAS),
        "modos_validos": sorted(MODOS_VALIDOS),
        "perspectivas": sorted(CAPAS_VALIDAS),
        "n_oscilaciones": len(_estado_self.get("historial_oscilacion") or []),
        "n_elecciones": len(_estado_self.get("historial_elecciones") or []),
        "invariantes": list(cfg.get("invariantes") or []),
    }


def reporte(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    b = barrer()
    cfg = _cfg()
    return {
        "id": cfg.get("id"),
        "modulo": cfg.get("nombre"),
        "rol": cfg.get("rol"),
        "version": cfg.get("version_modulo"),
        "estado": "OPERATIVO" if b.get("coherente") else "DEGRADADO",
        "coherente": b.get("coherente"),
        "capa_activa": b.get("capa_activa"),
        "altura_operativa": b.get("altura_operativa"),
        "modo": b.get("modo"),
        "casa": CASA_SELF,
        "identidad_disponible": b.get("identidad_disponible"),
        "n_declaraciones_self": b.get("n_declaraciones_self"),
        "n_oscilaciones": b.get("n_oscilaciones"),
        "n_elecciones": b.get("n_elecciones"),
        "capacidades": sorted((cfg.get("capacidades") or {}).keys()),
        "errores": list(b.get("errores") or []),
    }


def diagnostico(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    b = barrer()
    problemas: List[Dict[str, Any]] = []
    advertencias: List[str] = []
    recomendaciones: List[str] = []

    for e in b.get("errores") or []:
        problemas.append({"tipo": "coherencia", "detalle": e})

    if not b.get("identidad_disponible"):
        advertencias.append("identidad axiomática self aún no disponible")
        recomendaciones.append(
            "cargar cuerpo axiomático self en AX para anclar yo_funcional"
        )

    if b.get("capa_activa") != CASA_SELF:
        advertencias.append(
            "Self fuera de casa ({0}); casa operativa es {1}".format(
                b.get("capa_activa"), CASA_SELF
            )
        )

    estado = "OPERATIVO"
    if problemas:
        estado = "DEGRADADO"
    elif not b.get("identidad_disponible"):
        estado = "DEGRADADO"

    return {
        "id": "SF",
        "modulo": "self",
        "estado": estado,
        "problemas": problemas,
        "advertencias": advertencias,
        "recomendaciones": recomendaciones,
        "coherente": b.get("coherente"),
        "capa_activa": b.get("capa_activa"),
        "modo": b.get("modo"),
        "casa": CASA_SELF,
    }


# ---------------------------------------------------------------------------
# CONTRATO
# ---------------------------------------------------------------------------

CONTENEDOR: Dict[str, Any] = {
    "esquema": "VPSI-CONTRACT-1.0",
    "version_contrato": "1.0",
    "version_modulo": "1.0",
    "id": "SF",
    "nombre": "self",
    "rol": "SF",
    "estabilidad": "FASE",
    "compatible_desde": "1.0",
    "api_engine": ">=1.0",
    "descripcion": (
        "Yo funcional del sistema. Centro de elección e identidad de fase. "
        "Casa operativa L4. Punto de acceso a perspectivas L1…L6. "
        "Oscila entre alturas; registra actos de agency sin side-effects. "
        "No orquesta. No calcula Tru."
    ),
    "funcion": (
        "Ser el punto de referencia de elección e identidad de fase: "
        "exponer quién es el sistema en fase, desde qué altura opera, "
        "en qué modo de lucidez está, registrar actos de elección, "
        "y ofrecer a Engine las perspectivas L1…L6 como mecanismos "
        "legibles para cálculo y resolución de problemas."
    ),
    "no_hace": [],
    "autoridad": [
        "Exponer identidad de fase (yo_funcional)",
        "Reportar y cambiar altura operativa del Self (oscilar)",
        "Declarar desde qué altura opera (desde_donde)",
        "Clasificar modo de lucidez (estado_self)",
        "Registrar actos de agency sin side-effects (elegir)",
        "Declarar acceso a perspectivas L1…L6",
        "Verificar coherencia interna y reportar estado propio",
    ],
    "conocimiento_exportable": [
        "yo_funcional",
        "oscilar",
        "desde_donde",
        "elegir",
        "estado_self",
        "barrer",
        "verificar",
        "inventario",
        "reporte",
        "diagnostico",
    ],
    "requiere": [],
    "autoriza_engine": {
        "leer": True,
        "ejecutar": True,
        "consultar": True,
        "recombinar": True,
        "reportar": True,
        "auditar": True,
        "inventariar": True,
        "modificar": False,
        "alterar": False,
        "reescribir": False,
    },
    "consultas_soportadas": [
        "yo_funcional",
        "desde_donde",
        "estado_self",
        "oscilar",
        "elegir",
        "obtener_inventario",
        "obtener_reporte",
        "obtener_diagnostico",
        "verificar_coherencia",
    ],
    "capacidades": {
        "verificar": verificar,
        "barrer": barrer,
        "verificar_salida": verificar_salida,
        "yo_funcional": yo_funcional,
        "oscilar": oscilar,
        "desde_donde": desde_donde,
        "estado_self": estado_self,
        "elegir": elegir,
        "inventario": inventario,
        "reporte": reporte,
        "diagnostico": diagnostico,
    },
    "capacidades_meta": {
        "verificar": {
            "descripcion": "Alias de barrer. Verifica coherencia interna de SF.",
            "entrada": "peticion opcional (dict)",
            "salida": "dict con coherente, capa_activa, modo, errores",
        },
        "barrer": {
            "descripcion": "Centinela de SF: identidad y estado interno.",
            "entrada": "peticion opcional (dict)",
            "salida": "dict con coherente, identidad_disponible, capa_activa, modo, errores",
        },
        "verificar_salida": {
            "descripcion": "Comprueba forma mínima de una salida de SF.",
            "entrada": "salida: dict",
            "salida": "bool",
        },
        "yo_funcional": {
            "descripcion": "Identidad de fase anclada en cuerpo axiomático self.",
            "entrada": "peticion opcional (dict)",
            "salida": "dict con capa_activa, modo, ax_self, identidad_disponible, perspectivas",
        },
        "oscilar": {
            "descripcion": "Cambia o reporta la altura operativa del Self (L1…L6).",
            "entrada": "hacia opcional (str); contexto opcional (dict)",
            "salida": "dict con ok, capa_activa, altura_operativa, modo, cambio",
        },
        "desde_donde": {
            "descripcion": "Reporta altura y modo actuales del Self.",
            "entrada": "peticion opcional (dict)",
            "salida": "dict con capa_activa, altura_operativa, modo, en_casa, perspectivas",
        },
        "estado_self": {
            "descripcion": "Clasifica lucidez: REACTIVE|MECHANICAL|CONSCIOUS|META|INTEGRATED.",
            "entrada": "peticion opcional (dict)",
            "salida": "dict con modo, capa_activa, en_casa, coherente",
        },
        "elegir": {
            "descripcion": "Registra un acto de agency sin ejecutar efectos externos.",
            "entrada": "dict con opciones, eleccion, criterio, desde (opcionales)",
            "salida": "dict con ok, eleccion, desde, modo, n_elecciones",
        },
        "inventario": {
            "descripcion": "Inventario estructural del módulo SF.",
            "entrada": "peticion opcional (dict)",
            "salida": "dict con id, capacidades, capas_validas, modos_validos, perspectivas",
        },
        "reporte": {
            "descripcion": "Reporte de estado del módulo SF.",
            "entrada": "peticion opcional (dict)",
            "salida": "dict con estado, coherente, capa_activa, modo, errores",
        },
        "diagnostico": {
            "descripcion": "Diagnóstico: problemas, advertencias, recomendaciones.",
            "entrada": "peticion opcional (dict)",
            "salida": "dict con estado, problemas, advertencias, recomendaciones",
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
        "el id del módulo nunca cambia",
        "el rol nunca cambia",
        "la casa operativa del Self es L4_YO",
        "oscilar no es elegir",
        "elegir no ejecuta efectos externos",
        "las perspectivas L1…L6 son mecanismos legibles, no dependencias de arranque",
        "las capacidades declaradas son callables tras la resolución",
        "este módulo no modifica el estado de otros módulos",
        "este módulo no inventa capacidades no declaradas en CONTENEDOR",
        "este módulo siempre puede reportar su propio estado",
    ],
}

__all__ = [
    "CONTENEDOR",
    "CAPAS_VALIDAS",
    "CASA_SELF",
    "MODOS_VALIDOS",
    "yo_funcional",
    "oscilar",
    "desde_donde",
    "estado_self",
    "elegir",
    "barrer",
    "verificar",
    "verificar_salida",
    "inventario",
    "reporte",
    "diagnostico",
]
