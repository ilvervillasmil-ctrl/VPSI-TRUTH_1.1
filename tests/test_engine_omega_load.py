# tests/test_engine_omega_load.py
# T01–T02: carga estricta del Engine y cadena formulas_omega

from __future__ import annotations

import importlib
from pathlib import Path


def test_t01_engine_importa():
    """T01 — core.engine debe cargar y exponer la API estructural mínima."""
    mod = importlib.import_module("core.engine")
    assert hasattr(mod, "Engine")
    assert hasattr(mod, "ArranqueError")


def test_t01_engine_arranca():
    """T01 — Engine debe arrancar realmente en modo estricto."""
    from core.engine import Engine

    eng = Engine(Path("modules"), invocador_id="test_t01", strict=True)

    assert eng.estado == "OPERATIVO"
    assert eng.registro.total() >= 1


def test_t02_cadena_formulas_omega():
    """T02 — cada componente matemático de formulas_omega debe cargar."""
    piezas = [
        "modules.formulas.formulas_omega.constants",
        "modules.formulas.formulas_omega.energy",
        "modules.formulas.formulas_omega.negentropy",
        "modules.formulas.formulas_omega.presence",
        "modules.formulas.formulas_omega.wonder",
        "modules.formulas.formulas_omega.interaction",
        "modules.formulas.formulas_omega.resonance",
        "modules.formulas.formulas_omega.metaconsciousness",
        "modules.formulas.formulas_omega.coherence",
    ]

    for ruta in piezas:
        mod = importlib.import_module(ruta)
        assert mod is not None, f"falló import: {ruta}"
