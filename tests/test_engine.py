# -*- coding: utf-8 -*-
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.engine import Engine

def test_multiplicacion_simple():
    return (7 * 6) == 42

def test_engine_operativo():
    try:
        eng = Engine(Path("modules"), invocador_id="ci", strict=False)
        return eng.estado == "OPERATIVO" and eng.registro.total() > 0
    except Exception:
        return False
