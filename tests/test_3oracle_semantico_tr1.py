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
# CADENA DEMOSTRADA
#   especificación (Cuadro 4 del paper)
#        → D_A, D_B
#        → regla T15
#        → decisión_esperada
#        ↔ agregados canónicos publicados por generatividad()
#
# LIMITACIÓN ACTUAL
#   Sin g["traza"] no hay comparación par-a-par pública.
#   El test certifica:
#     (a) el oracle es autoconsistente y reproduce 276/183/93/153/30
#     (b) esos agregados coinciden con generatividad()["canonica"]
#     (c) comparación individual queda NO OBSERVABLE hasta que
#         exista superficie contractual de traza
#
# NO importa _medir_pares.
# NO usa gobierna como D_i.
# NO modifica producción.
# ===============================================================

from __future__ import annotations

from itertools import combinations

from modules.axiomas import generatividad

from tests.oracle_tr1 import (
    THETA_24_FORMAL,
    oracle_agregados,
    oracle_par,
    oracle_todos,
)


def test_3_oracle_semantico_tr1():
    """
    TEST 3 — oracle semántico independiente.

    Afirmación fuerte posible hoy:
      La especificación formal (Cuadro 4 + T15) produce, por sí sola,
      exactamente 276/183/93/153/30, y esos agregados coinciden con
      la capa canónica publicada por generatividad().

    Afirmación todavía no posible sin traza pública:
      Cada decisión individual publicada == decisión del oracle.
    """

    # ---------------------------------------------------------------
    # 1. Universo formal
    # ---------------------------------------------------------------
    ids = sorted(THETA_24_FORMAL)
    assert len(ids) == 24
    assert len(set(ids)) == 24

    # ---------------------------------------------------------------
    # 2. Oracle exhaustivo — 276 decisiones independientes
    # ---------------------------------------------------------------
    decisiones = oracle_todos()
    assert len(decisiones) == 276

    claves = [
        tuple(sorted((d["id_a"], d["id_b"])))
        for d in decisiones
    ]
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
    # 3. Agregados del oracle (consecuencia de las 276 decisiones)
    # ---------------------------------------------------------------
    agg = oracle_agregados()
    assert agg["pares_totales"] == 276
    assert agg["pares_compatibles"] == 183
    assert agg["pares_incompatibles"] == 93
    assert agg["pares_novedosos"] == 153
    assert agg["pares_redundantes"] == 30
    assert agg["pares_compatibles"] + agg["pares_incompatibles"] == 276
    assert agg["pares_novedosos"] + agg["pares_redundantes"] == 183

    # ---------------------------------------------------------------
    # 4. Comparación contra capa canónica publicada (agregados)
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
    # 5. Comparación individual — solo si existe traza contractual
    # ---------------------------------------------------------------
    traza = None
    if isinstance(g.get("traza"), list) and g["traza"]:
        traza = g["traza"]
    elif isinstance(c.get("traza"), list) and c["traza"]:
        traza = c["traza"]

    if traza is None:
        # Hallazgo arquitectónico (no fallo semántico):
        # oracle construido y agregados coinciden;
        # decisión par-a-par aún no observable públicamente.
        return

    # Rama defensiva: si aparece traza pública, comparar par a par
    def _clave(item):
        return tuple(sorted((str(item["id_a"]), str(item["id_b"]))))

    mapa_prod = {}
    for item in traza:
        k = _clave(item)
        assert k not in mapa_prod, f"traza con par duplicado: {k}"
        sec = item.get("secundaria")
        if sec == "":
            sec = None
        mapa_prod[k] = (item["primaria"], sec)

    mapa_oracle = {
        tuple(sorted((d["id_a"], d["id_b"]))): (
            d["esperada_primaria"],
            d["esperada_secundaria"],
        )
        for d in decisiones
    }

    assert set(mapa_prod) == set(mapa_oracle), (
        "traza vs oracle: conjuntos de pares difieren — "
        f"solo_prod={sorted(set(mapa_prod) - set(mapa_oracle))[:5]} "
        f"solo_oracle={sorted(set(mapa_oracle) - set(mapa_prod))[:5]}"
    )

    for par in mapa_oracle:
        esp = mapa_oracle[par]
        pub = mapa_prod[par]
        assert esp == pub, (
            f"discrepancia semántica par={par} "
            f"D_a={sorted(THETA_24_FORMAL[par[0]])} "
            f"D_b={sorted(THETA_24_FORMAL[par[1]])} "
            f"esperada={esp} publicada={pub}"
        )


def test_3_oracle_no_importa_clasificador_de_produccion():
    """
    Guardia estructural: el módulo oracle no debe depender del
    clasificador de producción.
    """
    import tests.oracle_tr1 as oracle_mod
    import inspect

    src = inspect.getsource(oracle_mod)
    prohibidos = (
        "generatividad",
        "_medir_pares",
        "pares_compatibles",
        "pares_novedosos",
        "from modules.axiomas",
        "import modules.axiomas",
    )
    for p in prohibidos:
        assert p not in src, (
            f"oracle_tr1.py contiene dependencia circular prohibida: {p!r}"
        )


def test_3_oracle_caso_puntual_conocido():
    """
    Casos puntuales del paper / T15 para anclar el oracle.
    """
    # Par con intersección vacía → incompatible
    # T2={INF,LOG} vs T5={ONT,EPI} → ∅
    d = oracle_par("T2", "T5")
    assert d["esperada_primaria"] == "incompatible"
    assert d["esperada_secundaria"] is None

    # Par compatible novedoso: T1={ONT,INF} vs T15={ONT,INF,MET}
    # intersección {ONT,INF} ≠ ∅; unión {ONT,INF,MET} ⊃ T1 y ⊃? T15
    # unión == T15, no strict ⊃ T15 → redundante (T15 ya cubre T1)
    d = oracle_par("T1", "T15")
    assert d["esperada_primaria"] == "compatible"
    assert d["esperada_secundaria"] == "redundante"

    # Par compatible novedoso: T1={ONT,INF} vs T16={EPI,MET}
    # intersección ∅ → incompatible
    d = oracle_par("T1", "T16")
    assert d["esperada_primaria"] == "incompatible"

    # Par novedoso clásico: T1={ONT,INF} vs M1={MET,LOG}
    # intersección ∅ → incompatible
    d = oracle_par("T1", "M1")
    assert d["esperada_primaria"] == "incompatible"

    # T1={ONT,INF} vs TR1={MET,INF,LOG}: intersección {INF}
    # unión {ONT,INF,MET,LOG} ⊃ ambos → novedoso
    d = oracle_par("T1", "TR1")
    assert d["esperada_primaria"] == "compatible"
    assert d["esperada_secundaria"] == "novedoso"
