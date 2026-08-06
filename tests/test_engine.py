# -*- coding: utf-8 -*-
import sys
from pathlib import Path

# Agrega la raíz del repositorio al sys.path para que encuentre "core"
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.engine import Engine

def test_multiplicacion_simple():
    resultado = 7 * 6
    assert resultado == 42

def test_engine_operativo():
    eng = Engine(Path("modules"), invocador_id="ci", strict=False)
    assert eng.estado == "OPERATIVO"
    assert eng.registro.total() > 0
