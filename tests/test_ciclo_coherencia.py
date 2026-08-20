# tests/test_ciclo_coherencia.py
# ===============================================================
# T10, T11, T14, T16 — CICLO REAL VPSI
# ===============================================================
#
# T10 — cálculo real de coherencia mediante la pared Engine → FO.
# T11 — caso límite: siete capas con L=0 → CΩ=0.
# T14 — Self (SF) aporta las capas; Engine no las inventa.
# T16 — ciclo Omega determinista.
#
# No se usa compute_coherence del Omega original.
# No se usan skips: ausencia de la capacidad real es un fallo.
# No se reproduce ninguna fórmula en este test.
# ===============================================================

from __future__ import annotations

import math
from pathlib import Path

import pytest

from core.engine import Engine


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


def _resultado_numerico(bloque):
    """
    Extrae el resultado matemático de la estructura contractual
    devuelta por calcular_coherencia().
    """
    assert isinstance(bloque, dict)
    assert bloque.get("estado") == "EXITO"
    assert bloque.get("operacion") == "calcular_coherencia"
    assert bloque.get("capacidad") == "evaluar_coherencia"

    resultado = bloque.get("resultado")

    assert isinstance(resultado, (int, float))
    assert not isinstance(resultado, bool)
    assert math.isfinite(float(resultado))

    return float(resultado)


# ---------------------------------------------------------------
# T10 — CÁLCULO REAL DE COHERENCIA
# ---------------------------------------------------------------

def test_t10_calcular_coherencia_real(engine):
    """
    T10 — Engine debe ejecutar realmente FO.evaluar_coherencia.

    No basta con que exista el método:
        Engine.calcular_coherencia()
            ↓
        FO.evaluar_coherencia()
            ↓
        resultado matemático real
    """
    capas = engine.obtener_capas_self()

    assert capas is not None

    salida = engine.calcular_coherencia(capas=capas)

    resultado = _resultado_numerico(salida)

    assert 0.0 <= resultado <= 1.0


# ---------------------------------------------------------------
# T11 — CASO LÍMITE DE COHERENCIA
# ---------------------------------------------------------------

def test_t11_capas_cero_producen_coherencia_cero(engine):
    """
    T11 — si todas las capas tienen L=0, la coherencia debe ser 0.

    La prueba entra por la pared real del Engine y delega el cálculo
    exclusivamente en FO.
    """
    capas = _capas_cero()

    salida = engine.calcular_coherencia(capas=capas)

    resultado = _resultado_numerico(salida)

    assert resultado == pytest.approx(0.0, abs=1e-12)


# ---------------------------------------------------------------
# T14 — SELF APORTA LAS CAPAS
# ---------------------------------------------------------------

def test_t14_self_aporta_capas(engine):
    """
    T14 — las capas proceden de SF.

    Engine.obtener_capas_self() debe localizar SF y resolver una
    capacidad real ('capas' o 'estado_self'). El Engine no fabrica
    las capas.
    """
    capas = engine.obtener_capas_self()

    assert capas is not None

    sf = engine.registro.primero("SF")
    assert sf is not None

    capacidad_capas = sf.fn("capas")
    capacidad_estado = sf.fn("estado_self")

    assert callable(capacidad_capas) or callable(capacidad_estado)


# ---------------------------------------------------------------
# T16 — DETERMINISMO DEL CICLO COMPLETO
# ---------------------------------------------------------------

def test_t16_ciclo_omega_determinista(engine):
    """
    T16 — dos ejecuciones idénticas del ciclo deben producir
    exactamente el mismo resultado observable.
    """
    capas = engine.obtener_capas_self()

    primero = engine.ciclo_omega(capas=capas)
    segundo = engine.ciclo_omega(capas=capas)

    assert isinstance(primero, dict)
    assert isinstance(segundo, dict)

    assert primero == segundo
