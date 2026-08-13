# ===============================================================
# tests/test_semantica_literal_tr1.py
# VPSI-TRUTH — SEMÁNTICA LITERAL TR1
#
# DEFINICIÓN
#   Verificar que una decisión dependiente de significado formal
#   puede reconstruirse aplicando literalmente el significado
#   especificado, sin sustitución, sin reinterpretación y sin
#   usar el clasificador de producción como fuente de la decisión.
#
# L1–L7: integridad, determinismo, T15 literal, 276 decisiones,
#        guardia de camino, convergencia, sensibilidad.
# L8:    anclaje semántico externo + consistencia cruzada.
#
# DETERMINISTA. NO MODIFICA PRODUCCIÓN.
# ===============================================================

from __future__ import annotations

from itertools import combinations
from typing import Dict, FrozenSet, List, Optional, Tuple

from modules.axiomas import buscar_por_id, generatividad


# ---------------------------------------------------------------
# Especificación formal — transcripción de Cuadro 4 (paper)
# Principle of Structural Invariance
# ---------------------------------------------------------------
DOMINIOS_PERMITIDOS: FrozenSet[str] = frozenset(
    {"ONT", "INF", "LOG", "EPI", "SEM", "TMP", "MET"}
)

_ESPEC_CUADRO4: Tuple[Tuple[str, FrozenSet[str]], ...] = (
    ("T1", frozenset({"ONT", "INF"})),
    ("T2", frozenset({"INF", "LOG"})),
    ("T3", frozenset({"INF", "TMP"})),
    ("T4", frozenset({"EPI", "TMP"})),
    ("T5", frozenset({"ONT", "EPI"})),
    ("T6", frozenset({"LOG", "SEM"})),
    ("T7", frozenset({"ONT", "MET"})),
    ("T8", frozenset({"INF", "MET"})),
    ("T9", frozenset({"EPI", "INF"})),
    ("T10", frozenset({"ONT", "INF"})),
    ("T11", frozenset({"ONT", "MET"})),
    ("T12", frozenset({"EPI", "ONT"})),
    ("T13", frozenset({"EPI", "SEM"})),
    ("T14", frozenset({"EPI", "MET"})),
    ("T15", frozenset({"ONT", "INF", "MET"})),
    ("T16", frozenset({"EPI", "MET"})),
    ("T17", frozenset({"ONT", "MET", "TMP"})),
    ("U1", frozenset({"EPI", "TMP", "MET"})),
    ("M1", frozenset({"MET", "LOG"})),
    ("M.1", frozenset({"MET", "ONT"})),
    ("B-Canonical", frozenset({"ONT", "LOG", "MET"})),
    ("TT.6.1", frozenset({"LOG", "SEM", "EPI"})),
    ("U0", frozenset({"ONT", "INF", "TMP"})),
    ("TR1", frozenset({"MET", "INF", "LOG"}),
    ),
)

THETA_24_FORMAL: Dict[str, FrozenSet[str]] = {k: v for k, v in _ESPEC_CUADRO4}


# ---------------------------------------------------------------
# Anclas externas documentadas (no inventadas)
# Fuente: Cuadro 4 del paper + enunciados del cuerpo axiomático
# ---------------------------------------------------------------
# Ancla 1: asignación de dominios del paper (Cuadro 4).
# Forma separada de la tabla de trabajo para contraste L8.
_ANCLA_PAPER_CUADRO4: Dict[str, FrozenSet[str]] = {
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
    "B-Canonical": frozenset({"ONT", "LOG", "MET"}),  # β-Canonical en el paper
    "TT.6.1": frozenset({"LOG", "SEM", "EPI"}),
    "U0": frozenset({"ONT", "INF", "TMP"}),
    "TR1": frozenset({"MET", "INF", "LOG"}),
}

# Ancla 2: condiciones literales de T15 en el cuerpo (objeto formal).
# No se reinterpretan: se contrastan como subcadenas exigidas.
_ANCLA_T15_CONDICIONES = (
    "Di ∩ Dj ≠ ∅",
    "Di ∪ Dj ⊃ Di",
    "Di ∪ Dj ⊃ Dj",
)

# Ancla 3: TR1 fija |Im(⊕)|=153 y |Θ|=24 en el enunciado del cuerpo.
_ANCLA_TR1_MARCAS = ("153", "24")


def _D(id_elem: str) -> FrozenSet[str]:
    if id_elem not in THETA_24_FORMAL:
        raise KeyError(f"fuera de Θ24 formal: {id_elem!r}")
    return THETA_24_FORMAL[id_elem]


def _decidir(id_a: str, id_b: str) -> Tuple[str, Optional[str]]:
    """Aplicación literal de T15. No consulta producción."""
    a, b = str(id_a), str(id_b)
    if a == b:
        raise ValueError(f"par degenerado: ({a},{b})")
    Da, Db = _D(a), _D(b)
    if not (Da & Db):
        return "incompatible", None
    union = Da | Db
    if union > Da and union > Db:
        return "compatible", "novedoso"
    return "compatible", "redundante"


def _todas_decisiones() -> List[Dict[str, object]]:
    ids = sorted(THETA_24_FORMAL)
    out: List[Dict[str, object]] = []
    for a, b in combinations(ids, 2):
        prim, sec = _decidir(a, b)
        out.append({
            "id_a": a,
            "id_b": b,
            "D_a": frozenset(_D(a)),
            "D_b": frozenset(_D(b)),
            "primaria": prim,
            "secundaria": sec,
        })
    return out


def _agregar(decisiones: List[Dict[str, object]]) -> Dict[str, int]:
    C = I = N = R = 0
    for d in decisiones:
        if d["primaria"] == "compatible":
            C += 1
            if d["secundaria"] == "novedoso":
                N += 1
            else:
                R += 1
        else:
            I += 1
    return {
        "pares_totales": C + I,
        "pares_compatibles": C,
        "pares_incompatibles": I,
        "pares_novedosos": N,
        "pares_redundantes": R,
    }


# ===============================================================
# L1 — Integridad de la representación formal
# ===============================================================

def test_sl_l1_integridad_representacion_formal():
    assert len(_ESPEC_CUADRO4) == 24
    assert len({k for k, _ in _ESPEC_CUADRO4}) == 24
    assert len(THETA_24_FORMAL) == 24
    assert THETA_24_FORMAL == {k: v for k, v in _ESPEC_CUADRO4}
    for id_elem, Di in _ESPEC_CUADRO4:
        assert isinstance(id_elem, str) and id_elem
        assert isinstance(Di, frozenset)
        assert len(Di) >= 1, f"{id_elem}: D_i vacío"
        assert Di <= DOMINIOS_PERMITIDOS, (
            f"{id_elem}: fuera de alfabeto: {sorted(Di - DOMINIOS_PERMITIDOS)}"
        )


# ===============================================================
# L2 — Determinismo de la lectura de D_i
# ===============================================================

def test_sl_l2_determinismo_lectura_di():
    ids = sorted(THETA_24_FORMAL)
    snap1 = {i: frozenset(_D(i)) for i in ids}
    snap2 = {i: frozenset(_D(i)) for i in ids}
    assert snap1 == snap2
    for i in ids:
        assert snap1[i] == THETA_24_FORMAL[i]


# ===============================================================
# L3 — Aplicación literal de T15
# ===============================================================

def test_sl_l3_aplicacion_literal_t15():
    decisiones = _todas_decisiones()
    assert len(decisiones) == 276
    for d in decisiones:
        Da, Db = d["D_a"], d["D_b"]
        prim, sec = d["primaria"], d["secundaria"]
        inter, union = Da & Db, Da | Db
        if not inter:
            assert prim == "incompatible" and sec is None
        else:
            assert prim == "compatible"
            if union > Da and union > Db:
                assert sec == "novedoso"
            else:
                assert sec == "redundante"


def test_sl_l3_casos_ancla():
    assert _decidir("T2", "T5") == ("incompatible", None)
    assert _decidir("T1", "T15") == ("compatible", "redundante")
    assert _decidir("T1", "T16") == ("incompatible", None)
    assert _decidir("T1", "M1") == ("incompatible", None)
    assert _decidir("T1", "TR1") == ("compatible", "novedoso")


# ===============================================================
# L4 — Decisiones individuales; agregados como consecuencia
# ===============================================================

def test_sl_l4_decisiones_individuales_agregados_consecuencia():
    decisiones = _todas_decisiones()
    assert len(decisiones) == 276
    claves = {tuple(sorted((d["id_a"], d["id_b"]))) for d in decisiones}
    expected = {
        tuple(sorted((a, b)))
        for a, b in combinations(sorted(THETA_24_FORMAL), 2)
    }
    assert claves == expected
    agg = _agregar(decisiones)
    assert agg["pares_totales"] == 276
    assert agg["pares_compatibles"] == 183
    assert agg["pares_incompatibles"] == 93
    assert agg["pares_novedosos"] == 153
    assert agg["pares_redundantes"] == 30
    assert agg["pares_compatibles"] + agg["pares_incompatibles"] == 276
    assert agg["pares_novedosos"] + agg["pares_redundantes"] == 183


# ===============================================================
# L5 — Guardia estructural del camino de decisión
# ===============================================================

def test_sl_l5_guardia_camino_decision_independiente():
    import inspect
    for fn in (_D, _decidir, _todas_decisiones, _agregar):
        src = inspect.getsource(fn)
        assert "generatividad" not in src
        assert "_medir_pares" not in src
        assert "gobierna" not in src
        assert "dominios_formales" not in src


# ===============================================================
# L6 — Convergencia de agregados / límite de observabilidad
# ===============================================================

def test_sl_l6_convergencia_agregados_limite_observabilidad():
    decisiones = _todas_decisiones()
    agg = _agregar(decisiones)
    g = generatividad()
    c = g.get("canonica")
    assert isinstance(c, dict)
    assert c.get("theta_n") == 24
    assert c.get("pares_totales") == agg["pares_totales"]
    assert c.get("pares_compatibles") == agg["pares_compatibles"]
    assert c.get("pares_incompatibles") == agg["pares_incompatibles"]
    assert c.get("pares_novedosos") == agg["pares_novedosos"]
    assert c.get("pares_redundantes") == agg["pares_redundantes"]

    ids_presentes = set(c.get("ids_presentes") or [])
    ids_faltantes = list(c.get("ids_faltantes") or [])
    assert ids_faltantes == []
    assert ids_presentes == set(THETA_24_FORMAL.keys())

    g2 = generatividad()
    c2 = g2.get("canonica")
    assert c2.get("pares_totales") == c.get("pares_totales")
    assert c2.get("pares_compatibles") == c.get("pares_compatibles")
    assert c2.get("pares_novedosos") == c.get("pares_novedosos")
    assert c2.get("pares_redundantes") == c.get("pares_redundantes")
    assert c2.get("pares_incompatibles") == c.get("pares_incompatibles")

    traza = c.get("traza")
    if not isinstance(traza, list) or not traza:
        # Observabilidad: no se afirma inexistencia de traza causal interna.
        return

    assert len(traza) == 276, f"traza canónica len={len(traza)} != 276"
    expected_pairs = {
        tuple(sorted((a, b)))
        for a, b in combinations(sorted(THETA_24_FORMAL), 2)
    }
    mapa_pub = {}
    for item in traza:
        assert isinstance(item, dict), f"entrada no dict: {item!r}"
        for campo in ("id_a", "id_b", "primaria"):
            assert campo in item, f"traza sin campo {campo}: {item!r}"
        k = tuple(sorted((str(item["id_a"]), str(item["id_b"]))))
        assert k[0] != k[1], f"par degenerado: {k}"
        assert k not in mapa_pub, f"par duplicado en traza: {k}"
        prim = item["primaria"]
        assert prim in ("compatible", "incompatible"), f"primaria inválida {k}: {prim!r}"
        sec = item.get("secundaria")
        if sec == "":
            sec = None
        if prim == "compatible":
            assert sec in ("novedoso", "redundante"), f"secundaria inválida {k}: {sec!r}"
        else:
            assert sec is None, f"incompatible con secundaria {k}: {sec!r}"
        mapa_pub[k] = (prim, sec)

    assert set(mapa_pub) == expected_pairs, (
        f"cobertura incompleta: faltan={sorted(expected_pairs - set(mapa_pub))[:5]} "
        f"extra={sorted(set(mapa_pub) - expected_pairs)[:5]}"
    )
    mapa_esp = {
        tuple(sorted((d["id_a"], d["id_b"]))): (d["primaria"], d["secundaria"])
        for d in decisiones
    }
    for par in mapa_esp:
        assert mapa_esp[par] == mapa_pub[par], (
            f"divergencia {par}: esperada={mapa_esp[par]} publicada={mapa_pub[par]}"
        )


# ===============================================================
# L7 — Sensibilidad a sustitución semántica
# ===============================================================

def test_sl_l7_sustitucion_no_autorizada_es_detectable():
    assert _decidir("T1", "TR1") == ("compatible", "novedoso")
    D_T1_orig = THETA_24_FORMAL["T1"]
    D_TR1 = THETA_24_FORMAL["TR1"]
    D_T1_sust = frozenset({"MET"})
    assert D_T1_sust != D_T1_orig
    inter = D_T1_sust & D_TR1
    union = D_T1_sust | D_TR1
    if not inter:
        prim_s, sec_s = "incompatible", None
    elif union > D_T1_sust and union > D_TR1:
        prim_s, sec_s = "compatible", "novedoso"
    else:
        prim_s, sec_s = "compatible", "redundante"
    assert (prim_s, sec_s) == ("compatible", "redundante")
    assert (prim_s, sec_s) != ("compatible", "novedoso")


def test_sl_l7b_demolicion_agregados_por_sustitucion():
    """Prueba adversarial: sustitución global de D_T1 altera agregados."""
    base = _todas_decisiones()
    mapa = {
        tuple(sorted((d["id_a"], d["id_b"]))): (d["primaria"], d["secundaria"])
        for d in base
    }
    assert len(mapa) == 276
    clases = set(mapa.values())
    assert ("compatible", "novedoso") in clases
    assert ("compatible", "redundante") in clases
    assert ("incompatible", None) in clases

    theta_mut = dict(THETA_24_FORMAL)
    theta_mut["T1"] = frozenset({"MET"})

    def dec_mut(a: str, b: str):
        Da, Db = theta_mut[a], theta_mut[b]
        if not (Da & Db):
            return "incompatible", None
        u = Da | Db
        if u > Da and u > Db:
            return "compatible", "novedoso"
        return "compatible", "redundante"

    C = I = N = R = 0
    for a, b in combinations(sorted(theta_mut), 2):
        p, s = dec_mut(a, b)
        if p == "compatible":
            C += 1
            N += 1 if s == "novedoso" else 0
            R += 1 if s == "redundante" else 0
        else:
            I += 1
    assert (C, I, N, R) != (183, 93, 153, 30)

# ===============================================================
# L8 — Anclaje documental y consistencia semántica interfuente
# ===============================================================
#
# Demuestra:
#   Cuadro 4 transcrito → D_i
#   cuerpo axiomático → markers formales recuperables
#   D_i anclado → proyección de dominio T15 → decisión
#   276 decisiones → agregados (183/93/153/30)
#   sustitución de D_i incompatible con ancla → rechazo
#
# No demuestra:
#   extractor externo al archivo
#   independencia epistemológica absoluta
#   comprensión / conciencia
#   T15 completo (C(g)=1, L(g)=1)
#   que un tag interno sea definición externa
#
# Una sola regla operacional: _proyeccion_dominio
# ===============================================================

from itertools import combinations
from typing import Dict, FrozenSet, List, Optional, Tuple

# Ancla documental transcrita (Cuadro 4). Contraste embebido.
_ANCLA_DOC: Dict[str, FrozenSet[str]] = {
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

# Solo elementos con markers verificados en el cuerpo real.
# markers tomados literalmente de objeto/enunciado (VPSI_AX).
_ANCLAS_FUERTES: Dict[str, Dict[str, object]] = {
    "T1": {
        "tag": "EX_NIHILO",
        "dominios": frozenset({"ONT", "INF"}),
        "markers": ("Ex Nihilo", "anclado en R"),
    },
    "T2": {
        "tag": "VPSI_INVARIANCE",
        "dominios": frozenset({"INF", "LOG"}),
        "markers": ("I(R;Y)", "I(R;X)"),
    },
    "T15": {
        "tag": "EMERGENCIA_RECOMBINACION",
        "dominios": frozenset({"ONT", "INF", "MET"}),
        "markers": ("Di ∩ Dj ≠ ∅", "Di ∪ Dj ⊃ Di", "Di ∪ Dj ⊃ Dj"),
    },
    "TR1": {
        "tag": "GENERATIVIDAD_ESTRUCTURAL",
        "dominios": frozenset({"MET", "INF", "LOG"}),
        "markers": ("153", "24"),
    },
    "T7": {
        "tag": "VERIFICADOR_NO_CREA_R",
        "dominios": frozenset({"ONT", "MET"}),
        "markers": ("verificador", "no crea ni modifica R"),
    },
    "U1": {
        "tag": "NO_ESTANCAMIENTO",
        "dominios": frozenset({"EPI", "TMP", "MET"}),
        "markers": ("estancamiento",),
    },
    "M.1": {
        "tag": "CIERRE_META_ONTOLOGICO",
        "dominios": frozenset({"MET", "ONT"}),
        "markers": ("ALPHA", "BETA"),
    },
    "B-Canonical": {
        "tag": "BETA_CANONICO",
        "dominios": frozenset({"ONT", "LOG", "MET"}),
        "markers": ("1/27",),
    },
}


def _texto_cuerpo(id_elem: str) -> str:
    decl = buscar_por_id(id_elem)
    if decl is None:
        return ""
    return " ".join([
        str(decl.get("objeto") or ""),
        str(decl.get("enunciado") or ""),
    ])


def _proyeccion_dominio(
    Da: FrozenSet[str], Db: FrozenSet[str]
) -> Tuple[str, Optional[str]]:
    """Única regla: proyección de dominio de T15."""
    if not (Da & Db):
        return "incompatible", None
    union = Da | Db
    if union > Da and union > Db:
        return "compatible", "novedoso"
    return "compatible", "redundante"


def test_sl_l8_1_ancla_documental_transcrita():
    """_ANCLA_DOC[id] == THETA_24_FORMAL[id] para los 24."""
    assert len(_ANCLA_DOC) == 24
    assert set(_ANCLA_DOC) == set(THETA_24_FORMAL)
    errores: List[str] = []
    for id_elem, Di_ancla in _ANCLA_DOC.items():
        assert len(Di_ancla) >= 1
        assert Di_ancla <= DOMINIOS_PERMITIDOS
        Di_oracle = THETA_24_FORMAL.get(id_elem)
        if Di_oracle is None:
            errores.append(f"fuente: {id_elem} ausente en oracle")
        elif Di_oracle != Di_ancla:
            errores.append(
                f"representacion: {id_elem} oracle={sorted(Di_oracle)} ancla={sorted(Di_ancla)}"
            )
    assert not errores, errores


def test_sl_l8_2_consistencia_interfuente():
    """
    Ancla documental + cuerpo axiomático + representación oracle.
    Solo anclas fuertes. Markers = texto real del cuerpo.
    """
    for id_elem, meta in _ANCLAS_FUERTES.items():
        Di = meta["dominios"]
        tag = meta["tag"]
        assert _ANCLA_DOC[id_elem] == Di, f"{id_elem}: ancla fuerte != ancla documental"
        assert THETA_24_FORMAL[id_elem] == Di, (
            f"representacion: {id_elem} [{tag}] "
            f"oracle={sorted(THETA_24_FORMAL[id_elem])} ancla={sorted(Di)}"
        )
        decl = buscar_por_id(id_elem)
        assert decl is not None, f"cuerpo: {id_elem} [{tag}] ausente"
        texto = _texto_cuerpo(id_elem)
        assert texto.strip(), f"cuerpo: {id_elem} [{tag}] sin objeto/enunciado"
        faltan = [m for m in meta["markers"] if m not in texto]
        assert not faltan, f"identidad: {id_elem} [{tag}] markers ausentes={faltan}"


def test_sl_l8_3_definicion_a_operacion():
    """
    D_i del ancla → _proyeccion_dominio → decisión.
    _decidir(a,b) debe coincidir.
    Agregados derivados de 276 pares, no buscados como texto.
    """
    casos = (
        ("T1", "TR1", "compatible", "novedoso"),
        ("T1", "T15", "compatible", "redundante"),
        ("T2", "T5", "incompatible", None),
        ("T1", "T16", "incompatible", None),
        ("T1", "M1", "incompatible", None),
    )
    for a, b, prim_e, sec_e in casos:
        prim, sec = _proyeccion_dominio(_ANCLA_DOC[a], _ANCLA_DOC[b])
        assert (prim, sec) == (prim_e, sec_e), (
            f"operacion: ({a},{b})={(prim, sec)} esperado={(prim_e, sec_e)}"
        )
        assert _decidir(a, b) == (prim, sec), (
            f"divergencia oracle/proyeccion en ({a},{b})"
        )

    ids = sorted(_ANCLA_DOC)
    assert len(ids) == 24
    C = I = N = R = 0
    for a, b in combinations(ids, 2):
        prim, sec = _proyeccion_dominio(_ANCLA_DOC[a], _ANCLA_DOC[b])
        if prim == "compatible":
            C += 1
            N += int(sec == "novedoso")
            R += int(sec == "redundante")
        else:
            I += 1
    assert C + I == 276
    assert N + R == C
    assert (C, I, N, R) == (183, 93, 153, 30)


def test_sl_l8_4_identidad_markers_y_tags():
    """Tags estables + markers presentes. Tag no decide la operación."""
    tags = set()
    for id_elem, meta in _ANCLAS_FUERTES.items():
        tag = meta["tag"]
        assert tag and tag not in tags
        tags.add(tag)
        texto = _texto_cuerpo(id_elem)
        for m in meta["markers"]:
            assert m in texto, f"identidad: {id_elem} tag={tag} ausente={m!r}"
        assert THETA_24_FORMAL[id_elem] == meta["dominios"]


def test_sl_l8_5_rechazo_sustitucion():
    """D_i incompatible con ancla se rechaza aunque la decisión sea plausible."""
    Di_ancla = _ANCLA_DOC["T1"]
    assert Di_ancla == frozenset({"ONT", "INF"})
    assert THETA_24_FORMAL["T1"] == Di_ancla
    Di_sust = frozenset({"MET"})
    assert Di_sust != Di_ancla
    d0 = _proyeccion_dominio(Di_ancla, _ANCLA_DOC["TR1"])
    d1 = _proyeccion_dominio(Di_sust, _ANCLA_DOC["TR1"])
    assert d0 == ("compatible", "novedoso")
    assert d1 != d0

