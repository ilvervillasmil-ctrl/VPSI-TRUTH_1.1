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
#   TEST 2  test_2trazabilidad_tr1.py   (este archivo)
#           → ¿existe superficie contractual de traza individual?
#             Si existe: auditar exhaustivamente par→decisión→agregación.
#             Si no existe: certificar el hallazgo de no-observabilidad
#             sin inventar API ni obligar un cambio de arquitectura.
#   TEST 3  (futuro, archivo distinto)
#           → oracle semántico independiente
#             THETA formal → D_i,D_j → regla T15 → decisión esperada
#             ↔ decisión publicada (cuando exista traza pública)
#
# HALLAZGO CONTRACTUAL ACTUAL (inspección de generatividad())
#   Superficie pública observada:
#     theta_n, pares_totales, pares_compatibles, pares_novedosos,
#     pares_redundantes, pares_incompatibles, im_vs_theta,
#     identidad_*, u1_proxy, dominios, canonica{...}
#   canonica incluye dominios_formales (ID → dominios formales),
#   coincide_paper, identidad_pares / identidad_compatibles.
#   NO incluye:
#     "traza", lista de {id_a, id_b, primaria, secundaria}
#   La decisión individual par→clasificación permanece interna
#   a _medir_pares (solo incrementa contadores; no retiene el par).
#
# LO QUE ESTE TEST CERTIFICA
#   1. Universo operativo independiente (recolectar + filtro contractual).
#   2. Agregados operativos coherentes y deterministas.
#   3. Capa canónica anclada a 24/276/183/153/30/93.
#   4. Veredicto de observabilidad individual:
#        TRAZABILIDAD INDIVIDUAL NO OBSERVABLE
#      desde la superficie pública actual.
#
# LO QUE ESTE TEST NO HACE
#   - No inventa g["traza"].
#   - No modifica generatividad(), Engine, CONTENEDOR ni THETA.
#   - No usa gobierna como D_i semántico de TR1.
#   - No reimplementa _medir_pares.
#   - No confunde no-observabilidad con fallo semántico.
# ===============================================================

from __future__ import annotations

from typing import Any, Dict, List, Set, Tuple

from modules.axiomas import generatividad, recolectar


# Claves de agregación contractual (superficie ya certificada por TEST 1).
_CLAVES_AGREGADO = (
    "theta_n",
    "pares_totales",
    "pares_compatibles",
    "pares_novedosos",
    "pares_redundantes",
    "pares_incompatibles",
    "im_vs_theta",
)

# Nombres que, de existir como lista de dicts con forma de par clasificado,
# constituirían traza individual contractual. No se inventan; solo se buscan.
_CLAVES_TRAZA_CONTRACTUALES = (
    "traza",
    "pares_detalle",
    "clasificaciones",
    "detalle_pares",
    "evaluaciones",
)


def _universo_operativo() -> List[str]:
    """
    Fuente independiente del universo operativo.

    Criterio contractual idéntico al de generatividad():
      tipo ∈ {axioma, teorema}
      AND gobierna no vacío
      AND id presente

    gobierna aquí solo filtra pertenencia al universo operativo
    (como hace generatividad). NO se interpreta como D_i de TR1.
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


def _es_entrada_traza(obj: Any) -> bool:
    """Forma mínima de una decisión individual publicada."""
    if not isinstance(obj, dict):
        return False
    if "id_a" not in obj or "id_b" not in obj:
        return False
    if "primaria" not in obj:
        return False
    return True


def _buscar_traza_contractual(contenedor: Dict[str, Any]) -> str | None:
    """
    Busca únicamente claves contractuales candidatas conocidas.
    No acepta 'cualquier lista que parezca traza'.
    Devuelve el nombre de la clave si la encuentra; None si no.
    """
    for nombre in _CLAVES_TRAZA_CONTRACTUALES:
        valor = contenedor.get(nombre)
        if isinstance(valor, list) and valor and _es_entrada_traza(valor[0]):
            return nombre
    return None


def test_trazabilidad_tr1_individual():
    """
    TEST 2 — observabilidad de trazabilidad individual TR1.

    Pregunta estricta:
      ¿Existe superficie pública contractual que permita seguir
      cada par hasta su decisión y reconstruir C/I/N/R desde ella?

    Si la respuesta es no, el veredicto es:
      TRAZABILIDAD INDIVIDUAL NO OBSERVABLE
    y el test PASA como medición de auditabilidad.
    No convierte la ausencia en fallo semántico.
    No inventa la superficie.
    """

    # ---------------------------------------------------------------
    # 1. Universo operativo independiente (no desde traza)
    # ---------------------------------------------------------------
    ids_op = _universo_operativo()
    n_op = len(ids_op)
    t_op_esperado = n_op * (n_op - 1) // 2

    # ---------------------------------------------------------------
    # 2. Dos ejecuciones — determinismo de lo que SÍ se publica
    # ---------------------------------------------------------------
    g1 = generatividad()
    g2 = generatividad()
    assert isinstance(g1, dict) and isinstance(g2, dict)

    assert g1["theta_n"] == n_op, (
        f"theta_n publicado ({g1['theta_n']}) != "
        f"|universo operativo independiente| ({n_op})"
    )
    assert g1["pares_totales"] == t_op_esperado, (
        f"pares_totales ({g1['pares_totales']}) != C({n_op},2)={t_op_esperado}"
    )

    # Invariantes agregados (no sustituyen traza individual)
    C = g1["pares_compatibles"]
    I = g1["pares_incompatibles"]
    N = g1["pares_novedosos"]
    R = g1["pares_redundantes"]
    T = g1["pares_totales"]
    assert C + I == T, f"C+I != T ({C}+{I} != {T})"
    assert N + R == C, f"N+R != C ({N}+{R} != {C})"

    # Determinismo de agregados entre ejecuciones
    for clave in _CLAVES_AGREGADO:
        assert clave in g1 and clave in g2, f"falta clave agregada '{clave}'"
        assert g1[clave] == g2[clave], (
            f"determinismo agregado: '{clave}' cambió "
            f"({g1[clave]} != {g2[clave]})"
        )

    # ---------------------------------------------------------------
    # 3. Capa canónica — anclaje formal (TEST 1 también lo cubre)
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

    for clave in (
        "theta_n",
        "pares_totales",
        "pares_compatibles",
        "pares_novedosos",
        "pares_redundantes",
        "pares_incompatibles",
        "im_vs_theta",
    ):
        assert c1.get(clave) == c2.get(clave), (
            f"canónica/determinismo: '{clave}' cambió"
        )

    # dominios_formales es asignación ID→dominios, no traza de pares.
    # Se registra su presencia como material útil para TEST 3, no como traza.
    if "dominios_formales" in c1:
        assert isinstance(c1["dominios_formales"], dict)
        assert len(c1["dominios_formales"]) >= 1

    # ---------------------------------------------------------------
    # 4. ¿Existe traza individual contractual?
    # ---------------------------------------------------------------
    clave_traza_op = _buscar_traza_contractual(g1)
    clave_traza_can = _buscar_traza_contractual(c1)

    if clave_traza_op is None and clave_traza_can is None:
        # -----------------------------------------------------------
        # VEREDICTO: TRAZABILIDAD INDIVIDUAL NO OBSERVABLE
        # -----------------------------------------------------------
        # Hallazgo (no fallo semántico):
        #   generatividad() publica conteos e identidades agregadas.
        #   No publica par → (primaria, secundaria).
        #   La decisión individual permanece encapsulada en
        #   _medir_pares (privado): clasifica en el bucle y solo
        #   incrementa contadores; no retiene ni expone el par.
        #
        # Por tanto TEST 2 no puede:
        #   - reconstruir C/I/N/R desde decisiones individuales
        #   - verificar unicidad/cobertura par-a-par
        #   - demostrar determinismo de decisión por par
        #
        # Eso queda bloqueado hasta que el contrato exponga una
        # superficie pública de traza. Ese cambio es decisión de
        # arquitectura, no corrección de este test.
        #
        # TEST 3 (oracle) comparará, cuando exista traza pública:
        #   decisión_publicada ↔ decisión_esperada(T15, D_i, D_j)
        assert clave_traza_op is None
        assert clave_traza_can is None
        return

    # ---------------------------------------------------------------
    # 5. Rama defensiva: si en el futuro existe traza contractual,
    #    auditarla exhaustivamente (sin reimplementar semántica).
    # ---------------------------------------------------------------
    # Esta rama solo se ejecuta si producción expone una clave
    # contractual real. Hoy no debería entrar.
    from itertools import combinations

    def _clave_par(item: Dict[str, Any]) -> Tuple[str, str]:
        a = str(item["id_a"]).strip()
        b = str(item["id_b"]).strip()
        assert a and b and a != b, f"par inválido en traza: {item!r}"
        return tuple(sorted((a, b)))

    def _auditar(traza, ids_universo, agregados, etiqueta):
        n = len(ids_universo)
        t_esp = n * (n - 1) // 2
        assert len(traza) == t_esp, (
            f"{etiqueta}: len(traza)={len(traza)} != C({n},2)={t_esp}"
        )
        claves = [_clave_par(x) for x in traza]
        assert len(claves) == len(set(claves)), f"{etiqueta}: duplicados"
        expected = {
            tuple(sorted((a, b)))
            for a, b in combinations(ids_universo, 2)
        }
        assert set(claves) == expected, (
            f"{etiqueta}: cobertura incompleta "
            f"faltan={sorted(expected - set(claves))[:5]} "
            f"extra={sorted(set(claves) - expected)[:5]}"
        )
        C_t = I_t = N_t = R_t = 0
        for item in traza:
            prim = item["primaria"]
            assert prim in ("compatible", "incompatible"), (
                f"{etiqueta}: primaria inválida {_clave_par(item)}={prim!r}"
            )
            sec = item.get("secundaria") or None
            if sec == "":
                sec = None
            if prim == "compatible":
                C_t += 1
                assert sec in ("novedoso", "redundante"), (
                    f"{etiqueta}: secundaria inválida {_clave_par(item)}={sec!r}"
                )
                if sec == "novedoso":
                    N_t += 1
                else:
                    R_t += 1
            else:
                I_t += 1
                assert sec is None, (
                    f"{etiqueta}: incompatible con secundaria "
                    f"{_clave_par(item)}={sec!r}"
                )
        assert C_t + I_t == len(traza)
        assert N_t + R_t == C_t
        assert C_t == agregados["pares_compatibles"]
        assert I_t == agregados["pares_incompatibles"]
        assert N_t == agregados["pares_novedosos"]
        assert R_t == agregados["pares_redundantes"]
        assert len(traza) == agregados["pares_totales"]
        return {
            _clave_par(x): (x["primaria"], x.get("secundaria") or None)
            for x in traza
        }

    if clave_traza_op is not None:
        mapa1 = _auditar(g1[clave_traza_op], ids_op, g1, "operativa")
        mapa2 = _auditar(g2[clave_traza_op], ids_op, g2, "operativa/2")
        assert set(mapa1) == set(mapa2)
        for par in mapa1:
            assert mapa1[par] == mapa2[par], (
                f"determinismo: par={par} e1={mapa1[par]} e2={mapa2[par]}"
            )

    if clave_traza_can is not None:
        ids_can = sorted(c1.get("dominios_formales", {}).keys()) or sorted(
            str(x) for x in (
                "T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10",
                "T11", "T12", "T13", "T14", "T15", "T16", "T17",
                "U0", "U1", "M1", "M.1", "B-Canonical", "TT.6.1", "TR1",
            )
        )
        assert len(ids_can) == 24
        mapa_c1 = _auditar(c1[clave_traza_can], ids_can, c1, "canonica")
        mapa_c2 = _auditar(c2[clave_traza_can], ids_can, c2, "canonica/2")
        assert set(mapa_c1) == set(mapa_c2)
        for par in mapa_c1:
            assert mapa_c1[par] == mapa_c2[par], (
                f"canónica/determinismo: par={par} "
                f"e1={mapa_c1[par]} e2={mapa_c2[par]}"
            )
