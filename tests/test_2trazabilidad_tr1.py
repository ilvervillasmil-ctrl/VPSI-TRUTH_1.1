# ===============================================================
# tests/test_2trazabilidad_tr1.py
# VPSI-TRUTH — AXIOMAS — auditoría de trazabilidad individual TR1
#
# ---------------------------------------------------------------
# AUTORÍA
#   Escrito a petición de Ilver Villasmil sobre
#   modules/axiomas/__init__.py. Audita; no diseña.
# ---------------------------------------------------------------
#
# SEPARACIÓN DE CAPAS (no mezclar)
#   TEST 1  test_generatividad_tr1.py
#           → conteos agregados, invariantes, capa canónica formal
#   TEST 2  test_trazabilidad_tr1.py   (este archivo)
#           → trazabilidad estructural + determinismo de la decisión
#             publicada en la superficie operativa
#   TEST 3  (futuro, archivo distinto)
#           → oracle semántico independiente
#             par → dominios reales → regla TR1 → decisión esperada
#             ↔ decisión publicada en la traza
#
# LO QUE ESTE TEST CERTIFICA
#   La superficie operativa de TR1 tiene trazabilidad individual
#   determinista:
#     universo real (independiente de la traza)
#          → C(n,2) pares esperados
#          → g["traza"]
#          → unicidad / cobertura / no degenerados
#          → primaria / secundaria válidas
#          → partición C/I y N/R
#          → reconstrucción exacta de C,I,N,R publicados
#          → mismo par → misma decisión entre ejecuciones
#
# LO QUE ESTE TEST NO CERTIFICA
#   Que cada etiqueta sea semánticamente correcta respecto a un
#   oracle independiente. Eso es TEST 3.
#   Que la capa canónica exponga traza individual: hoy es opcional.
#   Si canonica expone "traza", se audita; si no, no se inventa ni
#   se convierte en obligación arquitectónica desde el test.
#
# REGLAS
#   - Universo esperado NUNCA se deriva de la traza.
#   - Clave contractual exacta: g["traza"]. Sin heurística abierta.
#   - NO reimplementar _medir_pares ni la semántica TR1.
#   - NO inventar campos. NO modificar producción.
#   - NO Monte Carlo. Auditoría exhaustiva y determinista.
# ===============================================================

from __future__ import annotations

from itertools import combinations
from typing import Any, Dict, List, Optional, Set, Tuple

from modules.axiomas import generatividad, recolectar


# ---------------------------------------------------------------------------
# Universo canónico TR1 (especificación del paper — fuente independiente)
# Coincide con THETA_CANONICO en modules/axiomas/__init__.py
# T1–T17 (17) + U0,U1,M1,M.1,B-Canonical,TT.6.1,TR1 (7) = 24
# ---------------------------------------------------------------------------
THETA_CANONICO_IDS: Tuple[str, ...] = (
    "T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10",
    "T11", "T12", "T13", "T14", "T15", "T16", "T17",
    "U0", "U1", "M1", "M.1", "B-Canonical", "TT.6.1", "TR1",
)


# ---------------------------------------------------------------------------
# Utilidades de auditoría
# ---------------------------------------------------------------------------

def _clave_par(item: Dict[str, Any]) -> Tuple[str, str]:
    """
    Identidad no ordenada del par. (A,B) == (B,A).
    Solo normaliza para auditar. No recalcula clasificación.
    """
    a = str(item["id_a"]).strip()
    b = str(item["id_b"]).strip()
    assert a, f"id_a vacío en entrada de traza: {item!r}"
    assert b, f"id_b vacío en entrada de traza: {item!r}"
    assert a != b, f"par degenerado (A,A) en traza: {item!r}"
    return tuple(sorted((a, b)))


def _universo_operativo() -> List[str]:
    """
    Fuente independiente del universo operativo.

    Criterio contractual idéntico al de generatividad():
      tipo ∈ {axioma, teorema}
      AND gobierna no vacío
      AND id presente

    NO se deriva de la traza.
    NO es un oracle semántico; solo fija el universo de pares.
    """
    decls, errores = recolectar()
    assert not errores, (
        f"recolectar() reportó errores; no se puede fijar el universo: "
        f"{errores[:3]!r}"
    )
    ids = sorted({
        str(d["id"]).strip()
        for d in decls
        if d.get("tipo") in ("axioma", "teorema")
        and (d.get("gobierna") or [])
        and d.get("id")
    })
    assert ids, "universo operativo vacío tras recolectar()"
    return ids


def _snapshot_decisiones(
    traza: List[Dict[str, Any]],
) -> Dict[Tuple[str, str], Tuple[str, Optional[str]]]:
    """
    Mapa inmutable par → (primaria, secundaria).
    Rechaza duplicados. No muta la lista original.
    """
    mapa: Dict[Tuple[str, str], Tuple[str, Optional[str]]] = {}
    for item in traza:
        clave = _clave_par(item)
        assert clave not in mapa, (
            f"par duplicado al construir snapshot: {clave}"
        )
        primaria = item["primaria"]
        secundaria = item.get("secundaria")
        if secundaria == "":
            secundaria = None
        mapa[clave] = (primaria, secundaria)
    return mapa


def _auditar_traza(
    traza: List[Dict[str, Any]],
    ids_universo: List[str],
    agregados: Dict[str, Any],
    etiqueta_capa: str,
) -> Dict[Tuple[str, str], Tuple[str, Optional[str]]]:
    """
    Auditoría exhaustiva de una traza individual.

    Cadena:
      universo real → C(n,2) esperados → traza → unicidad → cobertura
      → primaria/secundaria → partición C/I → partición N/R
      → reconstrucción ≡ agregados publicados
    """
    n = len(ids_universo)
    t_esperado = n * (n - 1) // 2

    assert len(traza) == t_esperado, (
        f"{etiqueta_capa}: len(traza)={len(traza)} != C({n},2)={t_esperado}"
    )

    claves = [_clave_par(item) for item in traza]
    assert len(claves) == len(set(claves)), (
        f"{etiqueta_capa}: pares duplicados "
        f"(len={len(claves)} únicos={len(set(claves))})"
    )
    assert all(a != b for a, b in claves), (
        f"{etiqueta_capa}: existe par degenerado (A,A)"
    )

    expected_pairs: Set[Tuple[str, str]] = {
        tuple(sorted((a, b)))
        for a, b in combinations(ids_universo, 2)
    }
    actual_pairs = set(claves)
    faltantes = expected_pairs - actual_pairs
    extras = actual_pairs - expected_pairs
    assert not faltantes and not extras, (
        f"{etiqueta_capa}: cobertura incompleta — "
        f"faltantes={sorted(faltantes)[:5]} "
        f"extras={sorted(extras)[:5]} "
        f"(n_faltan={len(faltantes)} n_extra={len(extras)})"
    )
    assert actual_pairs == expected_pairs

    C_t = I_t = N_t = R_t = 0
    for item in traza:
        par = _clave_par(item)
        primaria = item["primaria"]
        assert primaria in ("compatible", "incompatible"), (
            f"{etiqueta_capa}: primaria inválida para par={par}: {primaria!r}"
        )
        secundaria = item.get("secundaria")
        if secundaria == "":
            secundaria = None

        if primaria == "compatible":
            C_t += 1
            assert secundaria in ("novedoso", "redundante"), (
                f"{etiqueta_capa}: compatible sin secundaria válida "
                f"para par={par}: {secundaria!r}"
            )
            if secundaria == "novedoso":
                N_t += 1
            else:
                R_t += 1
        else:
            I_t += 1
            assert secundaria is None, (
                f"{etiqueta_capa}: incompatible con secundaria "
                f"para par={par}: {secundaria!r}"
            )

    assert C_t + I_t == len(traza), (
        f"{etiqueta_capa}: C_trace+I_trace != |traza| "
        f"({C_t}+{I_t} != {len(traza)})"
    )
    assert N_t + R_t == C_t, (
        f"{etiqueta_capa}: N_trace+R_trace != C_trace "
        f"({N_t}+{R_t} != {C_t})"
    )

    assert C_t == agregados["pares_compatibles"], (
        f"{etiqueta_capa}: C_trace={C_t} != "
        f"pares_compatibles={agregados['pares_compatibles']}"
    )
    assert I_t == agregados["pares_incompatibles"], (
        f"{etiqueta_capa}: I_trace={I_t} != "
        f"pares_incompatibles={agregados['pares_incompatibles']}"
    )
    assert N_t == agregados["pares_novedosos"], (
        f"{etiqueta_capa}: N_trace={N_t} != "
        f"pares_novedosos={agregados['pares_novedosos']}"
    )
    assert R_t == agregados["pares_redundantes"], (
        f"{etiqueta_capa}: R_trace={R_t} != "
        f"pares_redundantes={agregados['pares_redundantes']}"
    )
    assert len(traza) == agregados["pares_totales"], (
        f"{etiqueta_capa}: |traza|={len(traza)} != "
        f"pares_totales={agregados['pares_totales']}"
    )

    mapa = _snapshot_decisiones(traza)

    compatibles = {
        par for par, dec in mapa.items() if dec[0] == "compatible"
    }
    incompatibles = {
        par for par, dec in mapa.items() if dec[0] == "incompatible"
    }
    assert compatibles.isdisjoint(incompatibles), (
        f"{etiqueta_capa}: C e I no son disjuntos"
    )
    assert compatibles | incompatibles == expected_pairs, (
        f"{etiqueta_capa}: C ∪ I no cubre exactamente todos los pares"
    )

    novedosos = {
        par for par, dec in mapa.items() if dec == ("compatible", "novedoso")
    }
    redundantes = {
        par for par, dec in mapa.items()
        if dec == ("compatible", "redundante")
    }
    assert novedosos.isdisjoint(redundantes), (
        f"{etiqueta_capa}: N y R no son disjuntos"
    )
    assert novedosos | redundantes == compatibles, (
        f"{etiqueta_capa}: N ∪ R no cubre exactamente los compatibles"
    )

    return mapa


# ---------------------------------------------------------------------------
# Test principal
# ---------------------------------------------------------------------------

def test_trazabilidad_tr1_individual():
    """
    Certificado de trazabilidad operativa TR1.

    Afirmación que este test hace:
      La superficie operativa de generatividad() expone una traza
      individual determinista que cubre exactamente el universo real,
      particiona C/I y N/R, y reconstruye los agregados publicados.

    Afirmación que este test no hace:
      Que cada decisión sea semánticamente correcta (TEST 3).
      Que la capa canónica deba exponer traza (hoy opcional).
    """

    # ---------------------------------------------------------------
    # Universo operativo — fuente independiente (NO desde la traza)
    # ---------------------------------------------------------------
    ids_op = _universo_operativo()

    # ---------------------------------------------------------------
    # Dos ejecuciones independientes
    # ---------------------------------------------------------------
    g1 = generatividad()
    g2 = generatividad()
    assert isinstance(g1, dict) and isinstance(g2, dict)

    assert g1["theta_n"] == len(ids_op), (
        f"theta_n publicado ({g1['theta_n']}) != "
        f"|universo operativo independiente| ({len(ids_op)})"
    )

    # ---------------------------------------------------------------
    # Clave contractual exacta — sin heurística
    # ---------------------------------------------------------------
    assert "traza" in g1, (
        "TRAZABILIDAD OPERATIVA: falta g['traza']. "
        "La superficie pública debe exponer la traza individual en "
        "generatividad()['traza'] como lista de "
        "{id_a, id_b, primaria, secundaria?}."
    )
    assert "traza" in g2, (
        "TRAZABILIDAD OPERATIVA: segunda ejecución no expone g['traza']"
    )

    traza1 = g1["traza"]
    traza2 = g2["traza"]
    assert isinstance(traza1, list) and isinstance(traza2, list)
    assert traza1, "g['traza'] está vacía"
    assert traza2, "g['traza'] (2ª ejecución) está vacía"

    for item in traza1:
        assert isinstance(item, dict), f"entrada de traza no es dict: {item!r}"
        assert "id_a" in item and "id_b" in item and "primaria" in item, (
            f"entrada de traza incompleta (faltan id_a/id_b/primaria): {item!r}"
        )

    # ---------------------------------------------------------------
    # Auditoría exhaustiva operativa
    # ---------------------------------------------------------------
    mapa1 = _auditar_traza(
        traza=traza1,
        ids_universo=ids_op,
        agregados=g1,
        etiqueta_capa="operativa",
    )

    # ---------------------------------------------------------------
    # Determinismo: mismo par → misma decisión (no el orden de lista)
    # ---------------------------------------------------------------
    mapa2 = _snapshot_decisiones(traza2)

    assert set(mapa1) == set(mapa2), (
        "determinismo: conjunto de pares cambió entre ejecuciones — "
        f"solo_en_1={sorted(set(mapa1) - set(mapa2))[:5]} "
        f"solo_en_2={sorted(set(mapa2) - set(mapa1))[:5]}"
    )
    for par in mapa1:
        assert mapa1[par] == mapa2[par], (
            f"determinismo: par={par} cambió de decisión — "
            f"ejecución_1={mapa1[par]} ejecución_2={mapa2[par]}"
        )

    for clave in (
        "theta_n",
        "pares_totales",
        "pares_compatibles",
        "pares_novedosos",
        "pares_redundantes",
        "pares_incompatibles",
        "im_vs_theta",
    ):
        assert clave in g1 and clave in g2, f"falta clave agregada '{clave}'"
        assert g1[clave] == g2[clave], (
            f"determinismo agregado: '{clave}' cambió "
            f"({g1[clave]} != {g2[clave]})"
        )

    # ---------------------------------------------------------------
    # Capa canónica
    # ---------------------------------------------------------------
    # Los agregados formales 24/276/183/153/30/93 se anclan aquí y
    # también en test_generatividad_tr1.py.
    #
    # canonica["traza"] NO forma parte del contrato actual.
    # Si la capa la expone voluntariamente, se audita.
    # Si no, no se inventa ni se convierte en obligación desde el test.
    # ---------------------------------------------------------------
    c1 = g1.get("canonica")
    c2 = g2.get("canonica")
    assert isinstance(c1, dict), "canonica debe ser dict"
    assert isinstance(c2, dict), "canonica (2ª ejecución) debe ser dict"

    assert c1.get("theta_n") == 24
    assert c1.get("pares_totales") == 276
    assert c1.get("pares_compatibles") == 183
    assert c1.get("pares_novedosos") == 153
    assert c1.get("pares_redundantes") == 30
    assert c1.get("pares_incompatibles") == 93

    if "traza" in c1:
        assert "traza" in c2, (
            "canónica: segunda ejecución no expone canonica['traza']"
        )
        ids_can = list(THETA_CANONICO_IDS)
        assert len(ids_can) == 24

        mapa_c1 = _auditar_traza(
            traza=c1["traza"],
            ids_universo=ids_can,
            agregados=c1,
            etiqueta_capa="canonica",
        )
        mapa_c2 = _snapshot_decisiones(c2["traza"])
        assert set(mapa_c1) == set(mapa_c2), (
            "canónica/determinismo: conjunto de pares cambió"
        )
        for par in mapa_c1:
            assert mapa_c1[par] == mapa_c2[par], (
                f"canónica/determinismo: par={par} cambió — "
                f"e1={mapa_c1[par]} e2={mapa_c2[par]}"
            )
        for clave in (
            "theta_n",
            "pares_totales",
            "pares_compatibles",
            "pares_novedosos",
            "pares_redundantes",
            "pares_incompatibles",
            "im_vs_theta",
        ):
            assert c1[clave] == c2[clave], (
                f"canónica/determinismo agregado: '{clave}' cambió"
            )
