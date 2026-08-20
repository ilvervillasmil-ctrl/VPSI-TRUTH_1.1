# ===============================================================
# VPSI-TRUTH — TEST INTEGRAL — SELF/L4 — CABLEADO DINÁMICO
# ===============================================================

import math

from modules.self import (
    YoOscillator,
    YoState,
    compute_energies,
    compute_weights,
    compute_contributions,
    shannon_S,
    compute_c_omega,
    phi_Y,
    zeta_Y,
    omega_Y,
    dynamic_equilibrium,
    force_Y,
)

# ===============================================================
# 1. ENTRADAS CANÓNICAS
# ===============================================================

ACT = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60]
FRICTION = [0.02, 0.05, 0.03, 0.01, 0.01, 0.00]

assert len(ACT) == 6
assert len(FRICTION) == 6
assert FRICTION[5] == 0.0

# ===============================================================
# 2. ENERGÍAS — L1..L6
# ===============================================================

energies = compute_energies(ACT, FRICTION)

assert len(energies) == 6
assert all(math.isfinite(x) for x in energies)
assert all(x >= 0.0 for x in energies)

for i in range(1, 7):
    expected = ACT[i - 1] * (1.0 - FRICTION[i - 1]) * (
        (1.0 + math.sqrt(5.0)) / 2.0
    ) ** (i / 2.0)
    assert math.isclose(
        energies[i - 1],
        expected,
        rel_tol=1e-12,
        abs_tol=1e-15,
    ), f"E{i} no coincide con la fórmula canónica"

# ===============================================================
# 3. PESOS — E_i → w_i
# ===============================================================

weights = compute_weights(energies)

assert len(weights) == 6
assert all(math.isfinite(x) for x in weights)
assert all(x >= 0.0 for x in weights)
assert math.isclose(sum(weights), 1.0, rel_tol=1e-12)

for i in range(6):
    assert math.isclose(
        weights[i],
        energies[i] / sum(energies),
        rel_tol=1e-12,
        abs_tol=1e-15,
    ), f"w{i + 1} no deriva correctamente de E{i + 1}"

# ===============================================================
# 4. CONTRIBUCIONES — w_i → f_i
# ===============================================================

contributions = compute_contributions(
    weights,
    ACT,
    energies,
    FRICTION,
)

assert len(contributions) == 6
assert all(math.isfinite(x) for x in contributions)
assert all(x >= 0.0 for x in contributions)

for i in range(6):
    expected = (
        weights[i]
        * ACT[i]
        * (1.0 - FRICTION[i])
        * energies[i]
    )
    assert math.isclose(
        contributions[i],
        expected,
        rel_tol=1e-12,
        abs_tol=1e-15,
    ), f"f{i + 1} incorrecta"

# ===============================================================
# 5. ENTROPÍA
# ===============================================================

S = shannon_S(weights)

assert math.isfinite(S)
assert S >= 0.0
assert S <= math.log(6.0) + 1e-12

# ===============================================================
# 6. COHERENCIA
# ===============================================================

C = compute_c_omega(
    contributions,
    rho=1.0,
    P_t=1.0,
    A=1.0,
    I_ext=1.0,
)

assert math.isfinite(C)
assert 0.0 <= C <= 26.0 / 27.0

# ===============================================================
# 7. AMORTIGUAMIENTO
# ===============================================================

phi = phi_Y(
    weights,
    FRICTION,
)

expected_phi = sum(
    weights[i] * FRICTION[i]
    for i in range(6)
)

assert math.isclose(
    phi,
    expected_phi,
    rel_tol=1e-12,
    abs_tol=1e-15,
)

# L6 NO debe aportar fricción.
phi_without_l6 = sum(
    weights[i] * FRICTION[i]
    for i in range(5)
)

assert math.isclose(
    phi,
    phi_without_l6,
    rel_tol=1e-12,
    abs_tol=1e-15,
)

zeta = zeta_Y(phi)
omega = omega_Y(phi)

assert math.isfinite(zeta)
assert math.isfinite(omega)
assert zeta >= 0.0
assert omega >= 0.0

# ===============================================================
# 8. EQUILIBRIO DINÁMICO
# ===============================================================

theta_eq = dynamic_equilibrium(
    C,
    weights,
)

assert math.isfinite(theta_eq)

# ===============================================================
# 9. FUERZA TOTAL
# ===============================================================

force = force_Y(
    L0_input=0.25,
    weights=weights,
    purpose_magnitude=0.50,
    c_omega=C,
    rho=1.0,
    P_t=1.0,
    S=S,
    delta_c=C,
    novelty=0.20,
)

assert math.isfinite(force)

# ===============================================================
# 10. EJECUCIÓN REAL DEL CABLE
# ===============================================================

yo = YoOscillator()

before = yo.snapshot()

assert math.isclose(
    before["t"],
    0.0,
    abs_tol=1e-15,
)

after = yo.step(
    ACT,
    dt=0.001,
    L0_input=0.25,
    purpose_magnitude=0.50,
    rho=1.0,
    P_t=1.0,
    A=1.0,
    I_ext=1.0,
    novelty=0.20,
    frictions=FRICTION,
)

# ===============================================================
# 11. ESTADO TEMPORAL
# ===============================================================

assert math.isclose(
    after["t"],
    0.001,
    rel_tol=1e-12,
    abs_tol=1e-15,
)

assert math.isfinite(after["theta_Y"])
assert math.isfinite(after["theta_dot_Y"])

# ===============================================================
# 12. VERIFICAR QUE EL STEP USÓ LAS MISMAS ENERGÍAS
# ===============================================================

for i in range(6):
    assert math.isclose(
        after["energies_L1_L6"][i],
        energies[i],
        rel_tol=1e-12,
        abs_tol=1e-15,
    ), f"STEP no utilizó E{i + 1} calculada por el cable"

# ===============================================================
# 13. VERIFICAR PESOS
# ===============================================================

for i in range(6):
    assert math.isclose(
        after["weights_L1_L6"][i],
        weights[i],
        rel_tol=1e-12,
        abs_tol=1e-15,
    ), f"STEP no utilizó w{i + 1} derivado de E{i + 1}"

# ===============================================================
# 14. VERIFICAR CADENA COMPLETA
# ===============================================================

assert math.isclose(
    after["S"],
    S,
    rel_tol=1e-12,
    abs_tol=1e-15,
)

assert math.isclose(
    after["C_OMEGA"],
    C,
    rel_tol=1e-12,
    abs_tol=1e-15,
)

assert math.isclose(
    after["phi_Y"],
    phi,
    rel_tol=1e-12,
    abs_tol=1e-15,
)

assert math.isclose(
    after["omega_Y"],
    omega,
    rel_tol=1e-12,
    abs_tol=1e-15,
)

assert math.isclose(
    after["theta_eq"],
    theta_eq,
    rel_tol=1e-12,
    abs_tol=1e-15,
)

# ===============================================================
# 15. L6 — INVARIANTE φ6 = 0
# ===============================================================

ACT_L6_ONLY = [0.0, 0.0, 0.0, 0.0, 0.0, 1.0]

E_L6 = compute_energies(
    ACT_L6_ONLY,
    FRICTION,
)

W_L6 = compute_weights(E_L6)

PHI_L6 = phi_Y(
    W_L6,
    FRICTION,
)

assert math.isclose(
    PHI_L6,
    0.0,
    abs_tol=1e-15,
), "L6 está introduciendo fricción"

assert math.isclose(
    W_L6[5],
    1.0,
    rel_tol=1e-12,
)

# ===============================================================
# 16. DINÁMICA — CAMBIO REAL DE ESTADO
# ===============================================================

yo2 = YoOscillator()

s0 = yo2.snapshot()

s1 = yo2.step(
    [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    dt=0.001,
)

assert s1["t"] > s0["t"]
assert math.isfinite(s1["theta_Y"])
assert math.isfinite(s1["theta_dot_Y"])

# ===============================================================
# 17. RETROALIMENTACIÓN TEMPORAL ΔCΩ
# ===============================================================

s2 = yo2.step(
    [0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
    dt=0.001,
)

assert math.isclose(
    s2["delta_C_OMEGA"],
    s2["C_OMEGA"] - s1["C_OMEGA"],
    rel_tol=1e-12,
    abs_tol=1e-15,
)

# ===============================================================
# 18. TEST DE CERO
# ===============================================================

zero = YoOscillator()

z = zero.step(
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    dt=0.001,
)

assert all(
    math.isclose(w, 1.0 / 6.0, rel_tol=1e-12)
    for w in z["weights_L1_L6"]
)

assert math.isclose(
    z["S"],
    math.log(6.0),
    rel_tol=1e-12,
    abs_tol=1e-15,
)

assert math.isclose(
    z["C_OMEGA"],
    0.0,
    abs_tol=1e-15,
)

# ===============================================================
# RESULTADO
# ===============================================================

print("PASS — CABLEADO SELF/L4 VERIFICADO")
print("PASS — L1..L6 → E → w → f")
print("PASS — E → S / CΩ / φY")
print("PASS — CΩ / φY → θeq / FY")
print("PASS — θ̈ → θ̇ → θ")
print("PASS — ΔCΩ temporal")
print("PASS — φ6 = 0")
print("PASS — caso ΣE = 0")
