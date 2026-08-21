# tests/test_ciclo_coherencia.py
# ===============================================================
# T10, T11, T14 — CICLO REAL VPSI
# ===============================================================
#
# T10 — cálculo real de coherencia mediante la pared Engine → FO.
# T11 — caso límite: siete capas con L=0 → CΩ=0.
# T14 — Self (SF) aporta las capas; Engine no las inventa.
#
# Este test verifica únicamente el contrato de coherencia.
#
# No se usa compute_coherence del Omega original.
# No se usan skips.
# No se reproduce ninguna fórmula de FO en el test.
# No se inyectan implementaciones alternativas.
# No se hardcodea el resultado de la fórmula real.
# ===============================================================

from __future__ import annotations

import math
from pathlib import Path

import pytest

from core.engine import Engine


# ===============================================================
# FIXTURE — ENGINE REAL
# ===============================================================

@pytest.fixture(scope="module")
def engine():
    """Engine real del repositorio, en modo estricto."""
    eng = Engine(
        Path("modules"),
        invocador_id="test_ciclo_coherencia",
        strict=True,
    )
    assert eng.estado == "OPERATIVO"
    return eng


# ===============================================================
# CASO LÍMITE
# ===============================================================

def _capas_cero():
    """Caso límite válido: siete capas con L=0 y φ=0."""
    return [
        {"L": 0.0, "phi": 0.0},
        {"L": 0.0, "phi": 0.0},
        {"L": 0.0, "phi": 0.0},
        {"L": 0.0, "phi": 0.0},
        {"L": 0.0, "phi": 0.0},
        {"L": 0.0, "phi": 0.0},
        {"L": 0.0, "phi": 0.0},
    ]


# ===============================================================
# EXTRACCIÓN CONTRACTUAL DEL RESULTADO
# ===============================================================

def _resultado_numerico(bloque):
    """
    Extrae el resultado matemático de la estructura contractual
    devuelta por Engine.calcular_coherencia().

    El test no calcula CΩ.
    Únicamente valida y extrae la salida producida por FO.
    """
    assert isinstance(bloque, dict)
    assert bloque.get("estado") == "EXITO"
    assert bloque.get("operacion") == "calcular_coherencia"
    assert bloque.get("capacidad") == "evaluar_coherencia"

    resultado = bloque.get("c_omega")

    if resultado is None:
        resultado = bloque.get("resultado")

    if isinstance(resultado, dict):
        resultado = resultado.get("c_omega")

    assert isinstance(resultado, (int, float))
    assert not isinstance(resultado, bool)
    assert math.isfinite(float(resultado))

    return float(resultado)


# ===============================================================
# T10 — CÁLCULO REAL DE COHERENCIA
# ===============================================================

def test_t10_calcular_coherencia_real(engine):
    """
    T10 — Engine debe atravesar la pared contractual real:

        Engine.calcular_coherencia()
                    ↓
        FO.evaluar_coherencia()
                    ↓
        resultado matemático real

    El test no implementa ni reproduce la fórmula de coherencia.
    """
    capas = engine.obtener_capas_self()

    assert capas is not None

    salida = engine.calcular_coherencia(capas=capas)

    resultado = _resultado_numerico(salida)

    assert 0.0 <= resultado <= 1.0


# ===============================================================
# T11 — CASO LÍMITE DE COHERENCIA
# ===============================================================

def test_t11_capas_cero_producen_coherencia_cero(engine):
    """
    T11 — con las siete capas en L=0, la capacidad real de FO debe
    producir CΩ=0.

    La entrada atraviesa Engine y el cálculo continúa siendo
    responsabilidad exclusiva de FO.evaluar_coherencia().
    """
    capas = _capas_cero()

    salida = engine.calcular_coherencia(capas=capas)

    resultado = _resultado_numerico(salida)

    assert resultado == pytest.approx(0.0, abs=1e-12)


# ===============================================================
# T14 — SELF APORTA LAS CAPAS
# ===============================================================

def test_t14_self_aporta_capas(engine):
    """
    T14 — las capas utilizadas por el ciclo proceden de SF.

    Engine.obtener_capas_self() debe resolver una capacidad real
    del contenedor SF.

    El Engine no debe fabricar las capas.
    """
    capas = engine.obtener_capas_self()

    assert capas is not None

    sf = engine.registro.primero("SF")

    assert sf is not None

    capacidad_capas = sf.fn("capas")
    capacidad_estado = sf.fn("estado_self")

    assert callable(capacidad_capas) or callable(capacidad_estado)
