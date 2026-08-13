# ===============================================================
# tests/test_generatividad_tr1.py
# VPSI-TRUTH — AXIOMAS — certificado contractual AX / TR1
#
# ---------------------------------------------------------------
# AUTORÍA
#   Escrito a petición de Ilver Villasmil sobre
#   modules/axiomas/__init__.py (autoría y arquitectura de
#   Ilver Villasmil). Este archivo audita; no diseña el módulo.
# ---------------------------------------------------------------
#
# QUÉ ES TR1
#   universo Θ
#        ↓
#   pares
#        ↓
#   clasificación semántica:
#        compatible / incompatible
#        novedoso / redundante
#        ↓
#   conteos agregados + identidades
#        ↓
#   Im(⊕) vs |Θ|
#        ↓
#   GENERATIVO / ESTANCADO
#
#   La clasificación semántica es el contenido de TR1.
#   Los campos pares_compatibles, pares_incompatibles,
#   pares_novedosos y pares_redundantes son resultados de esa
#   clasificación, no números aritméticos vacíos de significado.
#
# QUÉ CERTIFICA ESTE TEST
#   1. Universo operativo válido (carga, coherencia, IDs, gobierna).
#   2. Generación correcta del número de pares: T = n(n-1)/2.
#   3. Salida agregada de la clasificación semántica TR1:
#        C = pares clasificados compatibles
#        I = pares clasificados incompatibles
#        N = compatibles clasificados novedosos
#        R = compatibles clasificados redundantes
#   4. Conservación de esa clasificación:
#        C + I = T
#        N + R = C
#   5. Consecuencia generativa:
#        im_vs_theta coherente con novedosos > theta_n.
#   6. Proxy de actividad (u1_proxy) respaldado por novedosos > 0.
#   7. Capa canónica: clasificación TR1 sobre THETA_24 produce
#        exactamente 24 / 276 / 183 / 153 / 30 / 93.
#   8. ids_presentes / ids_faltantes contrastados con recolectar().
#   9. Separación operativa / canónica.
#  10. Determinismo.
#
# LIMITACIÓN DE OBSERVABILIDAD (no de significado)
#   La API pública expone la clasificación de TR1 en forma agregada
#   (conteos). Este test verifica esos resultados agregados, sus
#   identidades y su consecuencia en im_vs_theta.
#
#   La API no expone la traza par-a-par, por lo que este test no
#   reconstruye externamente qué clasificación recibió cada par
#   individual sin reimplementar la lógica privada.
#
#   Eso limita la trazabilidad externa.
#   NO niega, NO elimina y NO pone fuera de alcance la clasificación
#   semántica que generatividad() produce y reporta.
#
#   VALIDAR EL RESULTADO AGREGADO
#          ≠
#   RECONSTRUIR EXTERNAMENTE CADA CLASIFICACIÓN INDIVIDUAL
#
# REGLAS
#   - No reimplementar _medir_pares.
#   - No inventar campos públicos inexistentes.
#   - No modificar Engine, CONTENEDOR, THETA_24 ni módulos ajenos.
# ===============================================================

from __future__ import annotations

from modules.axiomas import generatividad, THETA_24, recolectar, barrer


def test_generatividad_tr1_contract():
    """
    Certificado contractual AX / TR1.

    Verifica el universo operativo, la generación de pares, la salida
    agregada de la clasificación semántica TR1, sus identidades, la
    consecuencia en im_vs_theta, la capa canónica formal y el
    determinismo.

    No reimplementa _medir_pares.
    No inventa campos.
    No niega el significado semántico de los conteos reportados.
    """

    # -----------------------------------------------------------
    # NIVEL 1 — Universo
    # -----------------------------------------------------------
    decls, errores = recolectar()
    assert not errores, (
        "recolectar() reportó errores de carga: "
        f"{errores[:3]}{'...' if len(errores) > 3 else ''}"
    )
    assert decls, "recolectar() no devolvió declaraciones"

    ids_universo = {
        str(d.get("id", "")).strip()
        for d in decls
        if d.get("id")
    }
    assert ids_universo, "universo de IDs vacío tras recolectar()"

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

    axiomas_teoremas = [
        d for d in decls
        if d.get("tipo") in ("axioma", "teorema")
    ]
    assert axiomas_teoremas, (
        "no hay declaraciones de tipo axioma/teorema"
    )

    for d in axiomas_teoremas:
        assert d.get("id"), f"axioma/teorema sin id: {d}"
        assert str(d["id"]).strip(), (
            f"axioma/teorema con id vacío: {d}"
        )
        assert d.get("tipo") in ("axioma", "teorema"), (
            f"tipo inválido: id={d.get('id')} tipo={d.get('tipo')}"
        )

    ids_at = [str(d["id"]).strip() for d in axiomas_teoremas]
    assert len(ids_at) == len(set(ids_at)), (
        "IDs de axiomas/teoremas duplicados: "
        f"{[i for i in ids_at if ids_at.count(i) > 1][:5]}"
    )

    operativas = []
    for d in axiomas_teoremas:
        gob = d.get("gobierna")
        if not gob:
            continue
        assert isinstance(gob, (list, tuple, set)), (
            f"gobierna tipo inválido: id={d.get('id')} "
            f"tipo={type(gob).__name__}"
        )
        assert len(gob) > 0, f"gobierna vacío: id={d.get('id')}"
        for ref in gob:
            ref_s = str(ref).strip()
            assert ref_s, (
                f"gobierna contiene referencia vacía: id={d.get('id')}"
            )
            assert ref_s in ids_universo, (
                f"gobierna referencia inexistente: "
                f"id={d.get('id')} ref='{ref_s}'"
            )
        operativas.append(d)

    assert operativas, (
        "no hay declaraciones operativas (axioma/teorema + gobierna)"
    )
    ids_op = [str(d["id"]).strip() for d in operativas]
    assert len(ids_op) == len(set(ids_op)), (
        "IDs operativos duplicados: "
        f"{[i for i in ids_op if ids_op.count(i) > 1][:5]}"
    )

    # -----------------------------------------------------------
    # Forma de generatividad()
    # -----------------------------------------------------------
    g = generatividad()
    assert isinstance(g, dict), "generatividad() debe retornar dict"

    for clave in (
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
    ):
        assert clave in g, (
            f"generatividad(): falta clave de contrato '{clave}'"
        )

    # Cardinalidad del universo operativo
    assert g["theta_n"] == len(operativas), (
        "capa operativa: theta_n no coincide con |universo operativo| "
        f"{g['theta_n']} != {len(operativas)}"
    )
    assert g["theta_n"] > 0

    # -----------------------------------------------------------
    # NIVEL 2 — Generación de pares
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

    n = g["theta_n"]
    assert g["pares_totales"] == n * (n - 1) // 2, (
        "capa operativa: pares_totales != n*(n-1)//2 — "
        f"{g['pares_totales']} != {n * (n - 1) // 2}"
    )

    # -----------------------------------------------------------
    # NIVEL 3 — Clasificación TR1 agregada (resultado semántico)
    # -----------------------------------------------------------
    # C, I, N, R son resultados de la clasificación semántica
    # que generatividad() realizó sobre los pares del universo.
    # Se verifican como tales, no como números vacíos.
    C = g["pares_compatibles"]
    I = g["pares_incompatibles"]
    N = g["pares_novedosos"]
    R = g["pares_redundantes"]
    T = g["pares_totales"]

    assert C >= 0 and I >= 0 and N >= 0 and R >= 0
    assert g["identidad_pares"] is True
    assert g["identidad_compatibles"] is True
    assert C + I == T, (
        "capa operativa: la clasificación agregada no conserva C+I=T "
        f"({C}+{I} != {T})"
    )
    assert N + R == C, (
        "capa operativa: la clasificación agregada no conserva N+R=C "
        f"({N}+{R} != {C})"
    )
    assert 0 <= N <= C
    assert 0 <= R <= C

    # -----------------------------------------------------------
    # NIVEL 4 — Consecuencia generativa
    # -----------------------------------------------------------
    esperado_im = (
        "GENERATIVO"
        if n > 0 and N > n
        else ("ESTANCADO" if n > 0 else "SIN_DATOS")
    )
    assert g["im_vs_theta"] == esperado_im, (
        "capa operativa: im_vs_theta inconsistente con "
        f"novedosos > theta_n — im={g['im_vs_theta']} "
        f"esperado={esperado_im} (N={N}, theta_n={n})"
    )
    assert g["im_vs_theta"] == "GENERATIVO", (
        f"estado actual del repo: se espera GENERATIVO, "
        f"es {g['im_vs_theta']}"
    )

    # -----------------------------------------------------------
    # NIVEL 5 — Proxy de actividad
    # -----------------------------------------------------------
    assert g["u1_proxy"] == "NO_STAGNANT", (
        f"u1_proxy debe ser NO_STAGNANT, es {g['u1_proxy']}"
    )
    assert N > 0, (
        "u1_proxy=NO_STAGNANT exige pares_novedosos > 0 "
        "en capa operativa"
    )

    # -----------------------------------------------------------
    # NIVEL 6 — Capa canónica (clasificación TR1 sobre THETA_24)
    # -----------------------------------------------------------
    c = g["canonica"]
    assert isinstance(c, dict), "canonica debe ser dict"

    for clave in (
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
    ):
        assert clave in c, f"canonica: falta clave '{clave}'"

    for clave in (
        "theta_n",
        "pares_totales",
        "pares_compatibles",
        "pares_novedosos",
        "pares_redundantes",
        "pares_incompatibles",
    ):
        assert c[clave] is not None
        assert isinstance(c[clave], int)
        assert c[clave] >= 0

    assert len(THETA_24) == 24
    assert c["theta_n"] == 24
    assert set(c["dominios_formales"]) == set(THETA_24)
    for tid, dominios in THETA_24.items():
        assert dominios, f"THETA_24['{tid}'] dominios vacíos"
        assert set(c["dominios_formales"][tid]) == set(dominios), (
            f"dominios_formales['{tid}'] != THETA_24"
        )

    # Salida agregada de la clasificación TR1 sobre THETA_24
    assert c["pares_totales"] == 276
    assert c["pares_compatibles"] == 183
    assert c["pares_novedosos"] == 153
    assert c["pares_redundantes"] == 30
    assert c["pares_incompatibles"] == 93
    assert c["coincide_paper"] is True

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

    esperado_im_c = (
        "GENERATIVO"
        if c["theta_n"] > 0 and c["pares_novedosos"] > c["theta_n"]
        else ("ESTANCADO" if c["theta_n"] > 0 else "SIN_DATOS")
    )
    assert c["im_vs_theta"] == esperado_im_c, (
        "canonica: im_vs_theta inconsistente con novedosos > theta_n"
    )
    assert c["im_vs_theta"] == "GENERATIVO"

    # ids_presentes / ids_faltantes vs universo real
    presentes = set(c["ids_presentes"])
    faltantes = set(c["ids_faltantes"])
    assert presentes.isdisjoint(faltantes)
    assert presentes | faltantes == set(THETA_24)
    assert len(presentes) + len(faltantes) == 24

    presentes_esperados = set(THETA_24) & ids_universo
    faltantes_esperados = set(THETA_24) - ids_universo
    assert presentes == presentes_esperados, (
        "ids_presentes no coincide con THETA_24 ∩ IDs reales: "
        f"extra={presentes - presentes_esperados} "
        f"faltan={presentes_esperados - presentes}"
    )
    assert faltantes == faltantes_esperados, (
        "ids_faltantes no coincide con THETA_24 − IDs reales"
    )

    # Separación de capas
    assert c["theta_n"] == 24, (
        "separación: canónica debe permanecer en 24"
    )

    # Proxy respaldado por alguna capa
    assert (
        g["pares_novedosos"] > 0 or c["pares_novedosos"] > 0
    ), "u1_proxy=NO_STAGNANT sin novedosos en ninguna capa"

    # -----------------------------------------------------------
    # NIVEL 7 — Determinismo
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
