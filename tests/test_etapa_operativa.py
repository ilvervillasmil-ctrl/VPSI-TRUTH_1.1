# ===============================================================
# tests/test_etapa_operativa.py
# ===============================================================
#
# Etapa actual:
#   Engine 18.3 OPERATIVO
#   9 módulos · contratos válidos · 100% integridad de capacidades
#
# Qué cubre:
#   1. Arranque determinista
#   2. Esquema mínimo (no_hace / requiere son list)
#   3. capacidades ↔ capacidades_meta 1:1
#   4. TODAS las capacidades declaradas son resolubles con cont.fn()
#   5. Capacidades base, si existen, devuelven forma mínima correcta
#   6. Registro sin rechazados
#
# ===============================================================

from __future__ import annotations

from pathlib import Path

import pytest

from core.engine import Engine, ArranqueError

ROOT = Path(__file__).resolve().parents[1]
MODULES = ROOT / "modules"

# Forma mínima esperada si el módulo declara estas capacidades.
# No obliga a que existan; solo valida la forma cuando existen.
FORMA_MINIMA = {
    "verificar": ("coherente",),
    "barrer": ("coherente",),
    "inventario": ("id",),
    "reporte": ("estado",),
    "diagnostico": ("estado",),
}


@pytest.fixture(scope="module")
def engine():
    try:
        eng = Engine(MODULES, invocador_id="test_etapa", strict=True)
    except ArranqueError as e:
        pytest.fail("Engine no arrancó: {0}".format(e))
    assert eng.estado == "OPERATIVO"
    return eng


def _contenedor_raw(cont):
    """CONTENEDOR original del módulo, si está expuesto."""
    modulo = getattr(cont, "modulo", None)
    if modulo is None:
        return None
    raw = getattr(modulo, "CONTENEDOR", None)
    return raw if isinstance(raw, dict) else None


def _fn(cont, clave):
    """Resuelve capacidad por cont.fn o por dict de capacidades."""
    if hasattr(cont, "fn"):
        return cont.fn(clave)
    caps = dict(getattr(cont, "capacidades", {}) or {})
    obj = caps.get(clave)
    return obj if callable(obj) else None


# ---------------------------------------------------------------
# 1. Arranque determinista
# ---------------------------------------------------------------

def test_arranque_determinista():
    a = Engine(MODULES, invocador_id="det_a", strict=True)
    b = Engine(MODULES, invocador_id="det_b", strict=True)

    def resumen(eng):
        r = eng.censar()
        return {
            "estado": eng.estado,
            "total": r.get("total"),
            "roles": {
                k: sorted(v)
                for k, v in sorted((r.get("roles") or {}).items())
            },
            "cargados": sorted(
                c.get("nombre")
                for c in (r.get("cargados") or [])
                if isinstance(c, dict)
            ),
        }

    assert resumen(a) == resumen(b)


# ---------------------------------------------------------------
# 2. no_hace / requiere son list
# ---------------------------------------------------------------

def test_no_hace_y_requiere_son_listas(engine):
    roles = engine.censar().get("roles") or {}
    for rol in roles:
        cont = engine.registro.primero(rol)
        if cont is None:
            continue
        raw = _contenedor_raw(cont)
        if raw is None:
            continue
        assert isinstance(raw.get("no_hace"), list), (
            "{0}: no_hace debe ser list".format(rol)
        )
        assert isinstance(raw.get("requiere"), list), (
            "{0}: requiere debe ser list".format(rol)
        )


# ---------------------------------------------------------------
# 3. capacidades ↔ capacidades_meta 1:1
# ---------------------------------------------------------------

def test_capacidades_meta_uno_a_uno(engine):
    roles = engine.censar().get("roles") or {}
    for rol in sorted(roles):
        cont = engine.registro.primero(rol)
        if cont is None:
            continue
        raw = _contenedor_raw(cont)
        if raw is None:
            continue

        caps = raw.get("capacidades") or {}
        meta = raw.get("capacidades_meta") or {}
        assert isinstance(caps, dict)
        assert isinstance(meta, dict)

        for nombre_cap in caps:
            assert nombre_cap in meta, (
                "{0}: capacidad '{1}' sin capacidades_meta".format(
                    rol, nombre_cap
                )
            )
            entrada = meta[nombre_cap]
            assert isinstance(entrada, dict), (
                "{0}.{1}: meta debe ser dict".format(rol, nombre_cap)
            )
            for campo in ("descripcion", "entrada", "salida"):
                assert campo in entrada, (
                    "{0}.{1}: falta meta['{2}']".format(
                        rol, nombre_cap, campo
                    )
                )
                assert isinstance(entrada[campo], str), (
                    "{0}.{1}: meta['{2}'] debe ser str".format(
                        rol, nombre_cap, campo
                    )
                )


# ---------------------------------------------------------------
# 4. TODAS las capacidades declaradas son resolubles
# ---------------------------------------------------------------

def test_todas_las_capacidades_resolubles(engine):
    """
    Amplía la cobertura a las 100+ capacidades del sistema.
    Si el contrato declara X, cont.fn(X) debe ser callable.
    """
    roles = engine.censar().get("roles") or {}
    total = 0
    for rol in sorted(roles):
        cont = engine.registro.primero(rol)
        if cont is None:
            continue
        caps = dict(getattr(cont, "capacidades", {}) or {})
        for nombre in caps:
            fn = _fn(cont, nombre)
            assert callable(fn), (
                "{0}.{1}: capacidad no resoluble".format(rol, nombre)
            )
            total += 1
    assert total > 0, "ninguna capacidad fue resuelta"


# ---------------------------------------------------------------
# 5. Forma mínima de capacidades base (si existen)
# ---------------------------------------------------------------

def test_forma_minima_capacidades_base(engine):
    """
    No obliga a que existan verificar/inventario/reporte/diagnostico.
    Si el contrato las declara, valida la estructura de salida.
    """
    roles = engine.censar().get("roles") or {}
    for rol in sorted(roles):
        cont = engine.registro.primero(rol)
        if cont is None:
            continue
        caps = dict(getattr(cont, "capacidades", {}) or {})

        for clave, campos in FORMA_MINIMA.items():
            if clave not in caps:
                continue

            fn = _fn(cont, clave)
            assert callable(fn), (
                "{0}.{1}: no resoluble".format(rol, clave)
            )

            try:
                salida = fn()
            except TypeError:
                salida = fn(None)

            assert isinstance(salida, dict), (
                "{0}.{1}: debe devolver dict, obtuvo {2}".format(
                    rol, clave, type(salida).__name__
                )
            )
            assert salida, (
                "{0}.{1}: devolvió dict vacío".format(rol, clave)
            )
            for campo in campos:
                assert campo in salida, (
                    "{0}.{1}: falta clave '{2}' en salida".format(
                        rol, clave, campo
                    )
                )


# ---------------------------------------------------------------
# 6. Registro limpio
# ---------------------------------------------------------------

def test_sin_contenedores_rechazados(engine):
    rechazados = list((engine.censar().get("rechazados") or []))
    assert not rechazados, "hay rechazados: {0}".format(rechazados)


def test_roles_presentes(engine):
    roles = engine.censar().get("roles") or {}
    assert roles, "Engine no reportó roles"
    presentes = [r for r, mods in roles.items() if mods]
    assert presentes, "ningún rol tiene módulos cargados"
