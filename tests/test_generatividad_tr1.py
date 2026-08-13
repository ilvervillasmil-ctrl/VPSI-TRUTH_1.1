# ===============================================================
# tests/test_generatividad_tr1.py
# VPSI-TRUTH — AXIOMAS — certificado contractual AX / TR1
#
# ---------------------------------------------------------------
# AUTORÍA
#   Batería de prueba: escrita a petición de Ilver Villasmil sobre
#   el módulo modules/axiomas/__init__.py — cuya autoría,
#   arquitectura y diseño son de Ilver Villasmil.
#
#   Rol de este archivo: certificado único de que AX carga
#   correctamente, que su universo es coherente, que el universo
#   operativo de TR1 está estructuralmente sano, y que
#   generatividad() implementa TR1 (operativa + canónica) de
#   forma determinista. No diseña el módulo; lo audita.
# ---------------------------------------------------------------
#
# CADENA CERTIFICADA
#   cuerpos → recolectar() → barrer()
#   cuerpos → recolectar() → universo operativo → generatividad()
#   THETA_24 → generatividad() → capa canónica TR1
#
# INVARIANTES BAJO PRUEBA
#   1. recolectar() sin errores de carga.
#   2. barrer() reporta coherente (0 choques, 0 errores).
#   3. Toda declaración axioma/teorema tiene id, tipo y estructura
#      mínima válida (antes de filtrar por gobierna).
#   4. IDs de axiomas/teoremas son únicos.
#   5. Universo TR1 operativo = axioma/teorema con gobierna no vacío.
#   6. theta_n operativo = tamaño real de ese universo.
#   7. Métricas son int >= 0 y ninguna es None.
#   8. pares_totales == n*(n-1)//2  (ambas capas).
#   9. C+I=T  y  N+R=C  (ambas capas).
#  10. 0 <= novedosos,redundantes <= compatibles.
#  11. im_vs_theta == GENERATIVO (ambas capas).
#  12. u1_proxy == NO_STAGNANT y está respaldado por novedosos > 0.
#  13. Capa canónica: 24 / 276 / 183 / 153 / 30 / 93.
#  14. coincide_paper is True.
#  15. Capas separadas; ids_presentes/faltantes no alteran Θ.
#  16. Determinismo entre dos ejecuciones.
#
# FUERA DE ALCANCE
#   - No calcula Tru_total / Tru_Ri.
#   - No demuestra U1 como teorema (solo proxy de actividad).
#   - No reimplementa _medir_pares.
#   - No modifica CONTENEDOR, Engine ni THETA_24.
#   - No congela el tamaño operativo (puede crecer).
#   - No valida letra por letra el Cuadro 4 del PDF
#     (valida que la implementación produce los números formales).
#
# ESTADO CONOCIDO AL ENTREGAR
#   Capa canónica: 24/276/183/153/30/93, identidades True,
#   coincide_paper True. Capa operativa ~297 con identidades
#   completas. barrer coherente, 521 declaraciones.
# ===============================================================

from __future__ import annotations

from modules.axiomas import generatividad, THETA_24, recolectar, barrer


def test_generatividad_tr1_contract():
    """
    Certificado único AX / TR1.

    Cadena verificada:
      1. Carga sin errores
      2. Coherencia axiomática (barrer)
      3. Integridad del universo de axiomas/teoremas
      4. Universo operativo de TR1 bien formado
      5. Métricas e identidades operativas
      6. Capa canónica reproduce enumeración formal
      7. Separación de capas
      8. Determinismo

    No reimplementa lógica de producción.
    Solo consume capacidades públicas.
    """

    # -----------------------------------------------------------
    # BLOQUE 1 — Carga sin errores
    # -----------------------------------------------------------
    decls, errores = recolectar()
    assert not errores, (
        "recolectar() reportó errores de carga: "
        f"{errores[:3]}{'...' if len(errores) > 3 else ''}"
    )
    assert decls, "recolectar() no devolvió declaraciones"

    # -----------------------------------------------------------
    # BLOQUE 2 — Coherencia axiomática (barrer)
    # -----------------------------------------------------------
    # Este test no sustituye a un test dedicado de contradicciones,
    # pero el certificado global exige que el universo esté coherente
    # antes de medir TR1 sobre él.
    r = barrer()
    assert r.get("coherente") is True, (
        "barrer(): módulo no coherente — "
        f"choques={len(r.get('choques') or [])} "
        f"errores={len(r.get('errores') or [])}"
    )
    assert not r.get("errores"), (
        f"barrer() reportó errores: {r.get('errores')[:3]}"
    )
    assert not r.get("choques"), (
        f"barrer() reportó choques: {len(r.get('choques') or [])}"
    )

    # -----------------------------------------------------------
    # BLOQUE 3 — Universo de axiomas/teoremas (antes de gobierna)
    # -----------------------------------------------------------
    # Se audita TODO axioma/teorema, no solo los que tienen gobierna.
    # Un axioma sin gobierna no entra a TR1, pero debe ser estructuralmente válido.
    axiomas_teoremas = [
        d for d in decls
        if d.get("tipo") in ("axioma", "teorema")
    ]
    assert axiomas_teoremas, (
        "no hay declaraciones de tipo axioma/teorema"
    )

    for d in axiomas_teoremas:
        assert d.get("id"), (
            f"axioma/teorema sin id: {d}"
        )
        assert str(d["id"]).strip(), (
            f"axioma/teorema con id vacío: {d}"
        )
        assert d.get("tipo") in ("axioma", "teorema"), (
            f"tipo inválido: id={d.get('id')} tipo={d.get('tipo')}"
        )

    ids_at = [d["id"] for d in axiomas_teoremas]
    assert len(ids_at) == len(set(ids_at)), (
        "IDs de axiomas/teoremas duplicados: "
        f"{[i for i in ids_at if ids_at.count(i) > 1][:5]}"
    )

    # -----------------------------------------------------------
    # BLOQUE 4 — Universo TR1 operativo (con gobierna)
    # -----------------------------------------------------------
    operativas = [
        d for d in axiomas_teoremas
        if d.get("gobierna")
    ]
    assert operativas, (
        "no hay declaraciones operativas (axioma/teorema + gobierna)"
    )

    for d in operativas:
        gob = d.get("gobierna")
        assert isinstance(gob, (list, tuple, set)) and len(gob) > 0, (
            f"gobierna vacío o tipo inválido: id={d.get('id')}"
        )

    ids_op = [d["id"] for d in operativas]
    assert len(ids_op) == len(set(ids_op)), (
        "IDs operativos duplicados: "
        f"{[i for i in ids_op if ids_op.count(i) > 1][:5]}"
    )

    # -----------------------------------------------------------
    # BLOQUE 5 — Existencia y forma de generatividad()
    # -----------------------------------------------------------
    g = generatividad()
    assert isinstance(g, dict), "generatividad() debe retornar dict"

    claves_minimas = (
        "theta_n",
        "pares_totales",
        "pares_compatibles",
        "pares_novedosos",
        "pares_redundantes",
        "pares_incompatibles",
        "im_vs_theta",
        "identidad_pares",
        "identidad_compatibles",
        "u1_proxy",
        "canonica",
    )
    for clave in claves_minimas:
        assert clave in g, (
            f"generatividad(): falta clave de contrato '{clave}'"
        )

    # -----------------------------------------------------------
    # BLOQUE 6 — theta_n operativo = cuerpo real
    # -----------------------------------------------------------
    assert g["theta_n"] == len(operativas), (
        "capa operativa: theta_n no coincide con universo real "
        f"axioma/teorema+gobierna: "
        f"{g['theta_n']} != {len(operativas)}"
    )
    assert g["theta_n"] > 0

    # -----------------------------------------------------------
    # BLOQUE 7 — Métricas operativas: tipo, rango, no-None
    # -----------------------------------------------------------
    metricas_op = (
        "theta_n",
        "pares_totales",
        "pares_compatibles",
        "pares_novedosos",
        "pares_redundantes",
        "pares_incompatibles",
    )
    for clave in metricas_op:
        assert g[clave] is not None, (
            f"capa operativa: '{clave}' no puede ser None"
        )
        assert isinstance(g[clave], int), (
            f"capa operativa: '{clave}' debe ser int, "
            f"es {type(g[clave]).__name__}"
        )
        assert g[clave] >= 0, (
            f"capa operativa: '{clave}' no puede ser negativo"
        )

    assert g["identidad_pares"] is not None
    assert g["identidad_compatibles"] is not None
    assert g["im_vs_theta"] is not None
    assert g["u1_proxy"] is not None

    # -----------------------------------------------------------
    # BLOQUE 8 — Fórmula de pares e identidades operativas
    # -----------------------------------------------------------
    n = g["theta_n"]
    assert g["pares_totales"] == n * (n - 1) // 2, (
        "capa operativa: pares_totales != n*(n-1)//2 — "
        f"{g['pares_totales']} != {n * (n - 1) // 2}"
    )
    assert g["identidad_pares"] is True, (
        "capa operativa: identidad_pares debe ser True"
    )
    assert g["identidad_compatibles"] is True, (
        "capa operativa: identidad_compatibles debe ser True"
    )
    assert (
        g["pares_compatibles"] + g["pares_incompatibles"]
        == g["pares_totales"]
    ), (
        "capa operativa: se rompe C+I=T"
    )
    assert (
        g["pares_novedosos"] + g["pares_redundantes"]
        == g["pares_compatibles"]
    ), (
        "capa operativa: se rompe N+R=C"
    )
    assert 0 <= g["pares_novedosos"] <= g["pares_compatibles"]
    assert 0 <= g["pares_redundantes"] <= g["pares_compatibles"]

    # -----------------------------------------------------------
    # BLOQUE 9 — im_vs_theta y u1_proxy (estado actual)
    # -----------------------------------------------------------
    # Este repositorio debe estar en régimen GENERATIVO.
    # u1_proxy es indicador de actividad, no demostración de U1.
    assert g["im_vs_theta"] == "GENERATIVO", (
        f"capa operativa: im_vs_theta debe ser GENERATIVO, "
        f"es {g['im_vs_theta']}"
    )
    assert g["u1_proxy"] == "NO_STAGNANT", (
        f"u1_proxy debe ser NO_STAGNANT, es {g['u1_proxy']}"
    )
    assert (
        g["pares_novedosos"] > 0
    ), (
        "u1_proxy=NO_STAGNANT exige pares_novedosos > 0 "
        "en al menos una capa (operativa verificada aquí; "
        "canónica se verifica más abajo)"
    )

    # -----------------------------------------------------------
    # BLOQUE 10 — Forma de la capa canónica
    # -----------------------------------------------------------
    c = g["canonica"]
    assert isinstance(c, dict), "canonica debe ser dict"

    claves_canonica = (
        "theta_n",
        "pares_totales",
        "pares_compatibles",
        "pares_novedosos",
        "pares_redundantes",
        "pares_incompatibles",
        "im_vs_theta",
        "identidad_pares",
        "identidad_compatibles",
        "ids_presentes",
        "ids_faltantes",
        "dominios_formales",
        "coincide_paper",
    )
    for clave in claves_canonica:
        assert clave in c, (
            f"canonica: falta clave '{clave}'"
        )

    metricas_can = (
        "theta_n",
        "pares_totales",
        "pares_compatibles",
        "pares_novedosos",
        "pares_redundantes",
        "pares_incompatibles",
    )
    for clave in metricas_can:
        assert c[clave] is not None, (
            f"canonica: '{clave}' no puede ser None"
        )
        assert isinstance(c[clave], int), (
            f"canonica: '{clave}' debe ser int"
        )
        assert c[clave] >= 0, (
            f"canonica: '{clave}' no puede ser negativo"
        )

    # -----------------------------------------------------------
    # BLOQUE 11 — THETA_24 formal y dominios
    # -----------------------------------------------------------
    assert len(THETA_24) == 24, (
        f"THETA_24 debe tener 24 elementos, tiene {len(THETA_24)}"
    )
    assert c["theta_n"] == 24, (
        f"canonica: theta_n debe ser 24, es {c['theta_n']}"
    )
    assert set(c["dominios_formales"]) == set(THETA_24), (
        "dominios_formales no coincide con THETA_24 de producción"
    )
    for tid, dominios in THETA_24.items():
        assert dominios, (
            f"THETA_24['{tid}'] no puede tener dominios vacíos"
        )
        assert set(c["dominios_formales"][tid]) == set(dominios), (
            f"dominios_formales['{tid}'] no coincide con THETA_24"
        )

    # -----------------------------------------------------------
    # BLOQUE 12 — Enumeración canónica formal (Cuadro 3/4)
    # -----------------------------------------------------------
    assert c["pares_totales"] == 276, (
        f"TR1 canónica: pares_totales {c['pares_totales']} != 276"
    )
    assert c["pares_compatibles"] == 183, (
        f"TR1 canónica: compatibles {c['pares_compatibles']} != 183"
    )
    assert c["pares_novedosos"] == 153, (
        f"TR1 canónica: novedosos {c['pares_novedosos']} != 153"
    )
    assert c["pares_redundantes"] == 30, (
        f"TR1 canónica: redundantes {c['pares_redundantes']} != 30"
    )
    assert c["pares_incompatibles"] == 93, (
        f"TR1 canónica: incompatibles {c['pares_incompatibles']} != 93"
    )
    assert c["coincide_paper"] is True, (
        "TR1 canónica: coincide_paper debe ser True"
    )

    # Fórmula e identidades canónicas
    assert c["pares_totales"] == 24 * 23 // 2
    assert c["identidad_pares"] is True
    assert c["identidad_compatibles"] is True
    assert (
        c["pares_compatibles"] + c["pares_incompatibles"]
        == c["pares_totales"]
    )
    assert (
        c["pares_novedosos"] + c["pares_redundantes"]
        == c["pares_compatibles"]
    )
    assert 0 <= c["pares_novedosos"] <= c["pares_compatibles"]
    assert 0 <= c["pares_redundantes"] <= c["pares_compatibles"]
    assert c["im_vs_theta"] == "GENERATIVO", (
        f"canonica: im_vs_theta debe ser GENERATIVO, "
        f"es {c['im_vs_theta']}"
    )

    # -----------------------------------------------------------
    # BLOQUE 13 — Separación de capas + ids presentes/faltantes
    # -----------------------------------------------------------
    assert c["theta_n"] == 24, (
        "separación: canónica debe permanecer en 24"
    )
    # No se congela el tamaño operativo.

    presentes = set(c["ids_presentes"])
    faltantes = set(c["ids_faltantes"])
    assert presentes.isdisjoint(faltantes), (
        "ids_presentes e ids_faltantes no deben solaparse"
    )
    assert presentes | faltantes == set(THETA_24), (
        "unión presentes+faltantes debe cubrir exactamente THETA_24"
    )
    assert len(presentes) + len(faltantes) == 24

    # -----------------------------------------------------------
    # BLOQUE 14 — u1_proxy respaldado también por capa canónica
    # -----------------------------------------------------------
    assert (
        g["pares_novedosos"] > 0 or c["pares_novedosos"] > 0
    ), (
        "u1_proxy=NO_STAGNANT sin pares novedosos en ninguna capa"
    )

    # -----------------------------------------------------------
    # BLOQUE 15 — Determinismo
    # -----------------------------------------------------------
    g2 = generatividad()
    for clave in metricas_op + (
        "identidad_pares",
        "identidad_compatibles",
        "im_vs_theta",
        "u1_proxy",
    ):
        assert g[clave] == g2[clave], (
            f"determinismo: '{clave}' cambió "
            f"({g[clave]} != {g2[clave]})"
        )
    assert g["canonica"] == g2["canonica"], (
        "determinismo: capa canónica cambió entre ejecuciones"
    )
