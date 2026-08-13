# ===============================================================
# tests/test_3oracle_semantico_tr1.py
# VPSI-TRUTH — TEST 3 — oracle semántico independiente TR1
#
# ---------------------------------------------------------------
# SEPARACIÓN
#   TEST 1  conteos / invariantes
#   TEST 2  observabilidad de traza individual
#   TEST 3  corrección semántica por vía independiente (este archivo)
#
# CADENA
#   especificación (Cuadro 4 del paper)
#        → D_A, D_B
#        → regla T15
#        → decisión_esperada
#        ↔ agregados canónicos publicados por generatividad()
#        ↔ (si existe) canonica["traza"] par a par
#
# LIMITACIÓN
#   Sin canonica["traza"] no hay comparación par-a-par pública.
#   Se certifica:
#     (a) oracle autoconsistente → 276/183/93/153/30
#     (b) esos agregados == generatividad()["canonica"]
#     (c) comparación individual solo contra capa CANÓNICA Θ24
#
# NO importa _medir_pares.
# NO usa gobierna como D_i.
# NO modifica producción.
# NO compara oracle Θ24 contra una traza operativa (otro universo).
# ===============================================================

from __future__ import annotations

from itertools import combinations
from typing import Dict, FrozenSet, List, Optional

from modules.axiomas import generatividad


# ---------------------------------------------------------------------------
# Oracle embebido — Cuadro 4 del paper (fuente independiente)
# ID alineado con producción: B-Canonical ≡ β-Canonical del texto
# ---------------------------------------------------------------------------
THETA_24_FORMAL: Dict[str, FrozenSet[str]] = {
    "T1": frozenset({"ONT", "INF"}),
    "T2": frozenset({"INF", "LOG"}),
    "T3": frozenset({"INF", "TMP"}),
    "T4": frozenset({"EPI", "TMP"}),
    "T5": frozenset({"ONT", "EPI"}),
    "T6": frozenset({"LOG", "SEM"}),
    "T7": frozenset({"ONT", "MET"}),
    "T8": frozenset({"INF", "MET"}),
    "T9": frozenset({"EPI", "INF"}),
    "T10": frozenset({"ONT", "INF"}),
    "T11": frozenset({"ONT", "MET"}),
    "T12": frozenset({"EPI", "ONT"}),
    "T13": frozenset({"EPI", "SEM"}),
    "T14": frozenset({"EPI", "MET"}),
    "T15": frozenset({"ONT", "INF", "MET"}),
    "T16": frozenset({"EPI", "MET"}),
    "T17": frozenset({"ONT", "MET", "TMP"}),
    "U1": frozenset({"EPI", "TMP", "MET"}),
    "M1": frozenset({"MET", "LOG"}),
    "M.1": frozenset({"MET", "ONT"}),
    "B-Canonical": frozenset({"ONT", "LOG", "MET"}),
    "TT.6.1": frozenset({"LOG", "SEM", "EPI"}),
    "U0": frozenset({"ONT", "INF", "TMP"}),
    "TR1": frozenset({"MET", "INF", "LOG"}),
}


def _dominio_formal(id_elem: str) -> FrozenSet[str]:
    if id_elem not in THETA_24_FORMAL:
        raise KeyError(f"id fuera de Θ formal: {id_elem!r}")
    return THETA_24_FORMAL[id_elem]


def _oracle_par(id_a: str, id_b: str) -> Dict[str, Optional[str]]:
    """Decisión esperada TR1/T15. Independiente de producción."""
    a, b = str(id_a).strip(), str(id_b).strip()
    if a == b:
        raise ValueError(f"par degenerado: ({a},{b})")
    Da, Db = _dominio_formal(a), _dominio_formal(b)
    if not (Da & Db):
        primaria, secundaria = "incompatible", None
    else:
        primaria = "compatible"
        union = Da | Db
        if union > Da and union > Db:
            secundaria = "novedoso"
        else:
            secundaria = "redundante"
    return {
        "id_a": a,
        "id_b": b,
        "D_a": sorted(Da),
        "D_b": sorted(Db),
        "esperada_primaria": primaria,
        "esperada_secundaria": secundaria,
    }


def _oracle_todos() -> List[Dict[str, Optional[str]]]:
    ids = sorted(THETA_24_FORMAL)
    return [_oracle_par(a, b) for a, b in combinations(ids, 2)]


def _oracle_agregados() -> Dict[str, int]:
    C = I = N = R = 0
    for d in _oracle_todos():
        if d["esperada_primaria"] == "compatible":
            C += 1
            if d["esperada_secundaria"] == "novedoso":
                N += 1
            else:
                R += 1
        else:
            I += 1
    return {
        "theta_n": 24,
        "pares_totales": C + I,
        "pares_compatibles": C,
        "pares_incompatibles": I,
        "pares_novedosos": N,
        "pares_redundantes": R,
    }


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_3_oracle_semantico_tr1():
    """
    TEST 3 — oracle semántico independiente.

    Hoy:
      Cuadro 4 + T15 → 276/183/93/153/30
      y coincide con generatividad()["canonica"].

    Comparación individual:
      SOLO contra canonica["traza"] (universo Θ24).
      Nunca contra g["traza"] operativa (otro universo).
      Si no existe traza canónica → NO OBSERVABLE (no es fallo).
    """
    assert len(THETA_24_FORMAL) == 24
    ids = sorted(THETA_24_FORMAL)
    assert len(set(ids)) == 24

    # ---------------------------------------------------------------
    # Oracle exhaustivo
    # ---------------------------------------------------------------
    decisiones = _oracle_todos()
    assert len(decisiones) == 276

    claves = [tuple(sorted((d["id_a"], d["id_b"]))) for d in decisiones]
    assert len(claves) == len(set(claves)), "oracle: pares duplicados"
    expected_pairs = {
        tuple(sorted((a, b))) for a, b in combinations(ids, 2)
    }
    assert set(claves) == expected_pairs, "oracle: cobertura incompleta"

    for d in decisiones:
        prim = d["esperada_primaria"]
        sec = d["esperada_secundaria"]
        assert prim in ("compatible", "incompatible"), (
            f"oracle primaria inválida par=({d['id_a']},{d['id_b']}): {prim!r}"
        )
        if prim == "compatible":
            assert sec in ("novedoso", "redundante"), (
                f"oracle secundaria inválida par=({d['id_a']},{d['id_b']}): {sec!r}"
            )
        else:
            assert sec is None, (
                f"oracle incompatible con secundaria "
                f"par=({d['id_a']},{d['id_b']}): {sec!r}"
            )

    # ---------------------------------------------------------------
    # Agregados del oracle (consecuencia de las 276 decisiones)
    # ---------------------------------------------------------------
    agg = _oracle_agregados()
    assert agg["pares_totales"] == 276
    assert agg["pares_compatibles"] == 183
    assert agg["pares_incompatibles"] == 93
    assert agg["pares_novedosos"] == 153
    assert agg["pares_redundantes"] == 30
    assert agg["pares_compatibles"] + agg["pares_incompatibles"] == 276
    assert agg["pares_novedosos"] + agg["pares_redundantes"] == 183

    # ---------------------------------------------------------------
    # Comparación contra capa canónica publicada (agregados)
    # ---------------------------------------------------------------
    g = generatividad()
    c = g.get("canonica")
    assert isinstance(c, dict), "canonica debe ser dict"
    assert c.get("theta_n") == 24
    assert c.get("pares_totales") == agg["pares_totales"]
    assert c.get("pares_compatibles") == agg["pares_compatibles"]
    assert c.get("pares_incompatibles") == agg["pares_incompatibles"]
    assert c.get("pares_novedosos") == agg["pares_novedosos"]
    assert c.get("pares_redundantes") == agg["pares_redundantes"]

    # ---------------------------------------------------------------
    # Comparación semántica individual:
    # SOLO contra la traza de la capa CANÓNICA Θ24.
    #
    # La traza operativa (g["traza"]), si algún día existe, pertenece
    # a otro universo y requiere otro oracle. No se mezcla aquí.
    # ---------------------------------------------------------------
    traza = c.get("traza")
    if not isinstance(traza, list) or not traza:
        # Hallazgo arquitectónico: oracle y agregados OK;
        # decisión par-a-par canónica aún no observable.
        return

    assert len(traza) == 276, (
        f"canonica['traza']: len={len(traza)} != 276"
    )

    def _clave(item):
        return tuple(sorted((str(item["id_a"]), str(item["id_b"]))))

    mapa_prod = {}
    for item in traza:
        assert isinstance(item, dict), (
            f"entrada de traza canónica no es dict: {item!r}"
        )
        assert "id_a" in item and "id_b" in item and "primaria" in item, (
            f"entrada de traza canónica incompleta: {item!r}"
        )
        k = _clave(item)
        assert k[0] != k[1], f"par degenerado en traza canónica: {k}"
        assert k not in mapa_prod, f"par duplicado en traza canónica: {k}"

        prim = item["primaria"]
        assert prim in ("compatible", "incompatible"), (
            f"primaria inválida en traza canónica par={k}: {prim!r}"
        )
        sec = item.get("secundaria")
        if sec == "":
            sec = None
        if prim == "compatible":
            assert sec in ("novedoso", "redundante"), (
                f"secundaria inválida en traza canónica par={k}: {sec!r}"
            )
        else:
            assert sec is None, (
                f"incompatible con secundaria en traza canónica par={k}: {sec!r}"
            )
        mapa_prod[k] = (prim, sec)

    assert set(mapa_prod) == expected_pairs, (
        "canonica['traza']: cobertura de Θ24 incompleta — "
        f"faltan={sorted(expected_pairs - set(mapa_prod))[:5]} "
        f"extra={sorted(set(mapa_prod) - expected_pairs)[:5]}"
    )

    mapa_oracle = {
        tuple(sorted((d["id_a"], d["id_b"]))): (
            d["esperada_primaria"],
            d["esperada_secundaria"],
        )
        for d in decisiones
    }

    for par in mapa_oracle:
        esp = mapa_oracle[par]
        pub = mapa_prod[par]
        assert esp == pub, (
            f"discrepancia semántica canónica par={par} "
            f"D_a={sorted(THETA_24_FORMAL[par[0]])} "
            f"D_b={sorted(THETA_24_FORMAL[par[1]])} "
            f"esperada={esp} publicada={pub}"
        )


def test_3_oracle_caso_puntual_conocido():
    """Casos ancla T15 / Cuadro 4."""
    d = _oracle_par("T2", "T5")
    assert d["esperada_primaria"] == "incompatible"
    assert d["esperada_secundaria"] is None

    d = _oracle_par("T1", "T15")
    assert d["esperada_primaria"] == "compatible"
    assert d["esperada_secundaria"] == "redundante"

    d = _oracle_par("T1", "T16")
    assert d["esperada_primaria"] == "incompatible"

    d = _oracle_par("T1", "M1")
    assert d["esperada_primaria"] == "incompatible"

    d = _oracle_par("T1", "TR1")
    assert d["esperada_primaria"] == "compatible"
    assert d["esperada_secundaria"] == "novedoso"
