# -*- coding: utf-8 -*-
"""
modules/diccionario/__init__.py

Rol DI — Diccionario (biblioteca de definiciones / invariante de significado).
v1.0
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

try:
    from core.diagnostico import DiagnosticoGlobal
except Exception:  # pragma: no cover
    class DiagnosticoGlobal:
        @staticmethod
        def recibir_reporte(*args, **kwargs):
            pass

_DIR = Path(__file__).parent
_FUENTES = _DIR / "fuentes"

VERSION = "1.0"

# ===============================================================
# ESTADO (se llena solo por descubrimiento — nada arriba nombra abajo)
# ===============================================================
_REGISTRO: Dict[str, Any] = {}
_META: Dict[str, Dict[str, Any]] = {}
_CARGADO = False


# ===============================================================
# NORMALIZACIÓN
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


# ===============================================================
# DESCUBRIMIENTO FORENSE — lee todos los archivos y subcarpetas
# ===============================================================
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
    # Lee dinámicamente cualquier subcarpeta y archivo interno de fuentes y del módulo
    if _DIR.is_dir():
        candidatos.extend(sorted(_DIR.glob("**/*.py")))

    vistos: Set[Path] = set()
    for f in candidatos:
        if f.name == "__init__.py" or f.name.startswith("_"):
            continue
        resolved = f.resolve()
        if resolved in vistos:
            continue
        vistos.add(resolved)

        clave = "diccionario_{0}_{1}".format(f.parent.name, f.stem)
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
# API — materia prima de definiciones
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
        "version": VERSION,
        "modulo": "diccionario",
        "rol": "DI",
    }
    return base


# ===============================================================
# CENTINELA Y CAPACIDADES EXPUESTAS
# ===============================================================
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


def verificar_salida(salida: Dict[str, Any]) -> bool:
    return bool(salida.get("coherente", False))


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
        "contenedor": "diccionario",
        "version": VERSION,
        "rol": "DI",
        "total": b.get("total"),
        "diccionarios": detalle,
        "por_idioma": b.get("por_idioma"),
        "coherente": b.get("coherente"),
        "funcion": (
            "Biblioteca de definiciones (materia prima léxica). "
            "Engine puede solicitar y distribuir definiciones según contexto."
        ),
    }


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
    ]


def resolver(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
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
            "notas": ["Definición entregada."],
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
        "inventario": inventario(),
        "coherente": True,
        "notas": ["Materia prima entregada."],
    }


# ===============================================================
# CONTENEDOR (contrato estricto para Engine / Angie)
# ===============================================================
CONTENEDOR = {
    "nombre": "diccionario",
    "rol": "DI",
    "version": VERSION,
    "requiere": [],
    "descripcion": (
        "Biblioteca de definiciones. Rol DI. "
        "Materia prima léxica y descubrimiento dinámico total de fuentes y subcarpetas."
    ),
    "capacidades": {
        "verificar": barrer,
        "barrer": barrer,
        "inventario": inventario,
        "axiomas": axiomas,
        "resolver": resolver,
        "listar": listar,
        "cargar": cargar,
        "cargar_todos": cargar_todos,
        "definir": definir,
        "significado": significado,
        "inyectar_en_peticion": inyectar_en_peticion,
    },
}


__all__ = [
    "CONTENEDOR",
    "VERSION",
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
    "barrer",
    "verificar_salida",
    "inventario",
    "axiomas",
    "resolver",
]
