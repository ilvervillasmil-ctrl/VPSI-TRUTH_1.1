# -*- coding: utf-8 -*-
from pathlib import Path
from core.engine import Engine

def test_multiplicacion_simple():
    """Test simple para validar que pytest encuentre al menos una prueba."""
    resultado = 7 * 6
    assert resultado == 42

def test_engine_operativo():
    """Verifica que el Engine arranca correctamente con los módulos."""
    eng = Engine(Path("modules"), invocador_id="ci", strict=False)
    assert eng.estado == "OPERATIVO"
    assert eng.registro.total() > 0
