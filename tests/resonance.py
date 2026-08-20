# ===============================================================
# TEST — resonance.py (sin hardcode frágil)
# ===============================================================

from modules.formulas.formulas_omega.resonance import ResonanceLogic
from modules.formulas.formulas_omega.constants import PHI


def test_frecuencia_capa():
    assert ResonanceLogic.calculate_layer_frequency(0) == 1.0
    assert abs(ResonanceLogic.calculate_layer_frequency(2) - PHI) < 1e-12


def test_alineacion_fase():
    assert ResonanceLogic.calculate_phase_alignment(0, 5) == 0.0
    assert ResonanceLogic.calculate_phase_alignment(4, 4) == 1.0
    assert ResonanceLogic.calculate_phase_alignment(2, 8) == 0.25


def test_resonancia_par():
    r = ResonanceLogic.pair_resonance(5.0, 5.0, phase_diff=0.0)
    assert abs(r - 1.0) < 1e-12
    assert ResonanceLogic.pair_resonance(0.0, 3.0) == 0.0


def test_compute_rho():
    rho = ResonanceLogic.compute([1.0, 1.0, 1.0, 1.0])
    assert abs(rho - 1.0) < 1e-12
    assert ResonanceLogic.compute([0.0, 0.0, 0.0]) == 0.0


if __name__ == "__main__":
    test_frecuencia_capa()
    test_alineacion_fase()
    test_resonancia_par()
    test_compute_rho()
    print("OK  resonance.py")
