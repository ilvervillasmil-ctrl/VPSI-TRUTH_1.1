# tests/test_resonance.py

from modules.formulas.formulas_omega.resonance import ResonanceLogic
from modules.formulas.formulas_omega.constants import PHI


def test_frecuencia_capa_cero():
    assert ResonanceLogic.calculate_layer_frequency(0) == 1.0


def test_frecuencia_capa_dos():
    assert abs(ResonanceLogic.calculate_layer_frequency(2) - PHI) < 1e-12


def test_alineacion_misma_energia():
    assert ResonanceLogic.calculate_phase_alignment(4.0, 4.0) == 1.0


def test_alineacion_cero():
    assert ResonanceLogic.calculate_phase_alignment(0.0, 5.0) == 0.0


def test_resonancia_par_perfecta():
    r = ResonanceLogic.pair_resonance(5.0, 5.0, phase_diff=0.0)
    assert abs(r - 1.0) < 1e-12


def test_resonancia_par_cero():
    assert ResonanceLogic.pair_resonance(0.0, 3.0) == 0.0


def test_compute_rho_perfecto():
    rho = ResonanceLogic.compute([1.0, 1.0, 1.0, 1.0])
    assert abs(rho - 1.0) < 1e-12


def test_compute_rho_cero():
    assert ResonanceLogic.compute([0.0, 0.0, 0.0]) == 0.0
