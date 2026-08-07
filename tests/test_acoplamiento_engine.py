# ===============================================================
# tests/test_acoplamiento_engine.py
# ===============================================================
#
# Objetivo:
#   Detectar qué contenedores existen en modules/ pero NO están
#   acoplados al Engine (no cargados, rechazados, sin rol, o
#   sin CONTENEDOR resoluble).
#
# Acoplado  = Engine lo descubre, valida contrato y lo deja
#             en registro (estado OPERATIVO del arranque).
# No acoplado = existe en disco y Engine no lo tiene operativo.
#
# ===============================================================

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any, Dict, List, Set

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULES = ROOT / "modules"
sys.path.insert(0, str(ROOT))


# ---------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------

def _modulos_en_disco() -> List[str]:
    """Nombres de carpetas bajo modules/ que tienen __init__.py."""
    if not MODULES.is_dir():
        return []
    out: List[str] = []
    for p in sorted(MODULES.iterdir()):
        if not p.is_dir():
            continue
        if p.name.startswith(("_", ".")):
            continue
        if (p / "__init__.py").is_file():
            out.append(p.name)
    return out


def _tiene_contenedor(nombre: str) -> bool:
    """¿El paquete expone CONTENEDOR al importarlo?"""
    init = MODULES / nombre / "__init__.py"
    if not init.is_file():
        return False
    clave = "probe_contenedor_{0}".format(nombre)
    spec = importlib.util.spec_from_file_location(clave, str(init))
    if spec is None or spec.loader is None:
        return False
    mod = importlib.util.module_from_spec(spec)
    try:
        sys.modules[clave] = mod
        spec.loader.exec_module(mod)
    except Exception:
        return False
    return isinstance(getattr(mod, "CONTENEDOR", None), dict)


def _engine():
    from core.engine import Engine, ArranqueError

    try:
        eng = Engine(MODULES, invocador_id="test_acoplamiento", strict=True)
        return eng, None
    except ArranqueError as e:
        return None, str(e)
    except Exception as e:
        return None, "{0}: {1}".format(type(e).__name__, e)


def _nombres_cargados(eng) -> Set[str]:
    resumen = eng.censar() if hasattr(eng, "censar") else {}
    cargados = resumen.get("cargados") or []
    nombres: Set[str] = set()
    for c in cargados:
        if isinstance(c, dict):
            n = c.get("nombre") or c.get("id")
            if n:
                nombres.add(str(n))
        else:
            n = getattr(c, "nombre", None) or getattr(c, "id", None)
            if n:
                nombres.add(str(n))
    # fallback registro
    reg = getattr(eng, "registro", None)
    if reg is not None:
        contenedores = getattr(reg, "contenedores", None) or {}
        if isinstance(contenedores, dict):
            for k, v in contenedores.items():
                nombres.add(str(k))
                if isinstance(v, dict) and v.get("nombre"):
                    nombres.add(str(v["nombre"]))
                elif hasattr(v, "nombre"):
                    nombres.add(str(v.nombre))
    return nombres


def _rechazados(eng) -> List[Any]:
    resumen = eng.censar() if hasattr(eng, "censar") else {}
    return list(resumen.get("rechazados") or [])


def _roles_engine(eng) -> Set[str]:
    resumen = eng.censar() if hasattr(eng, "censar") else {}
    roles = resumen.get("roles") or {}
    return set(roles.keys()) if isinstance(roles, dict) else set()


# ---------------------------------------------------------------
# Informe legible (también útil fuera de pytest)
# ---------------------------------------------------------------

def informe_acoplamiento() -> Dict[str, Any]:
    en_disco = _modulos_en_disco()
    con_contrato = [m for m in en_disco if _tiene_contenedor(m)]
    sin_contrato = [m for m in en_disco if m not in con_contrato]

    eng, error_arranque = _engine()

    if eng is None:
        return {
            "engine_operativo": False,
            "error_arranque": error_arranque,
            "en_disco": en_disco,
            "con_contrato": con_contrato,
            "sin_contrato": sin_contrato,
            "acoplados": [],
            "no_acoplados": con_contrato[:],  # ninguno pudo acoplarse
            "rechazados": [],
            "roles": [],
        }

    cargados = _nombres_cargados(eng)
    rechazados = _rechazados(eng)
    roles = sorted(_roles_engine(eng))

    # Acoplado = aparece en cargados (por nombre de carpeta o nombre de CONTENEDOR)
    acoplados: List[str] = []
    no_acoplados: List[str] = []
    for m in con_contrato:
        if m in cargados or any(m in str(x) for x in cargados):
            acoplados.append(m)
        else:
            # también aceptar si el CONTENEDOR.nombre coincide
            try:
                init = MODULES / m / "__init__.py"
                clave = "probe2_{0}".format(m)
                spec = importlib.util.spec_from_file_location(clave, str(init))
                mod = importlib.util.module_from_spec(spec)
                sys.modules[clave] = mod
                spec.loader.exec_module(mod)  # type: ignore[union-attr]
                cont = getattr(mod, "CONTENEDOR", {}) or {}
                nombre = str(cont.get("nombre") or "")
                rol = str(cont.get("rol") or cont.get("id") or "")
                if nombre in cargados or rol in cargados or rol in roles:
                    acoplados.append(m)
                else:
                    no_acoplados.append(m)
            except Exception:
                no_acoplados.append(m)

    return {
        "engine_operativo": getattr(eng, "estado", None) == "OPERATIVO",
        "estado_engine": getattr(eng, "estado", None),
        "error_arranque": None,
        "en_disco": en_disco,
        "con_contrato": con_contrato,
        "sin_contrato": sin_contrato,
        "acoplados": sorted(set(acoplados)),
        "no_acoplados": sorted(set(no_acoplados)),
        "rechazados": rechazados,
        "roles": roles,
        "cargados": sorted(cargados),
        "total_disco": len(en_disco),
        "total_acoplados": len(set(acoplados)),
        "total_no_acoplados": len(set(no_acoplados)),
    }


# ---------------------------------------------------------------
# Tests
# ---------------------------------------------------------------

def test_engine_arranca_para_medir_acoplamiento():
    eng, err = _engine()
    assert eng is not None, "Engine no arrancó: {0}".format(err)
    assert eng.estado == "OPERATIVO"


def test_listar_no_acoplados():
    """
    Reporta contenedores en disco con CONTENEDOR que Engine no tiene operativos.
    Si la lista no está vacía, el assert falla e imprime el informe.
    """
    info = informe_acoplamiento()

    print("\n" + "=" * 60)
    print("ACOPLAMIENTO ENGINE ↔ CONTENEDORES")
    print("=" * 60)
    print("estado_engine     :", info.get("estado_engine"))
    print("en_disco          :", info.get("en_disco"))
    print("con_contrato      :", info.get("con_contrato"))
    print("sin_contrato      :", info.get("sin_contrato"))
    print("roles             :", info.get("roles"))
    print("cargados          :", info.get("cargados"))
    print("acoplados         :", info.get("acoplados"))
    print("no_acoplados      :", info.get("no_acoplados"))
    print("rechazados        :", info.get("rechazados"))
    print("total_no_acoplados:", info.get("total_no_acoplados"))
    print("=" * 60)

    # Carpeta sin CONTENEDOR no es "contenedor" acoplable; solo se informa.
    assert info.get("engine_operativo") is True
    assert info.get("no_acoplados") == [], (
        "Contenedores NO acoplados al Engine: {0}".format(info.get("no_acoplados"))
    )


def test_sin_contrato_solo_informativo():
    """Módulos en disco sin CONTENEDOR (no son contenedores del contrato)."""
    info = informe_acoplamiento()
    # No falla el CI: solo deja constancia.
    print("\nMódulos en disco SIN CONTENEDOR:", info.get("sin_contrato"))


if __name__ == "__main__":
    import json

    info = informe_acoplamiento()
    print(json.dumps(info, indent=2, ensure_ascii=False, default=str))
