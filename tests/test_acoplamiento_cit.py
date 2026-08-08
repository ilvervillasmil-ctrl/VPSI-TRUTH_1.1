# ===============================================================
# VPSI-TRUTH — tests/test_acoplamiento_cit.py
# ===============================================================
#
# TEST DE ACOPLAMIENTO CONTRACTUAL — CIT
#
# Objetivo:
#   Verificar que CIT no solamente exista, sino que esté realmente
#   acoplado al Engine conforme a su CONTENEDOR.
#
# Se comprueba:
#   1. Descubrimiento
#   2. Registro
#   3. Identidad
#   4. Contrato
#   5. Dependencias
#   6. Capacidades
#   7. capacidades_meta
#   8. autorización Engine
#   9. invocación real
#  10. reporting real
#  11. modo Engine de CIT
#
# ===============================================================

from __future__ import annotations

from pathlib import Path

import pytest

from core.engine import Engine


# ===============================================================
# CONTEXTO
# ===============================================================

RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
RAIZ_MODULOS = RAIZ_PROYECTO / "modules"


@pytest.fixture
def engine_cit() -> Engine:
    """
    Construye el Engine contra el directorio real de módulos.

    strict=True es deliberado:
    cualquier discrepancia estructural debe hacer fallar
    el test en lugar de ocultarla.
    """
    return Engine(
        raiz_modulos=RAIZ_MODULOS,
        invocador_id="acoplamiento_cit",
        strict=True,
    )


@pytest.fixture
def cit(engine_cit):
    """
    Recupera CIT exclusivamente a través del registro del Engine.

    Esto es importante:
    el test no considera suficiente importar CIT directamente.
    Debe existir como Contenedor dentro del Engine.
    """
    cont = engine_cit.registro.primero("CIT")

    assert cont is not None, (
        "CIT no está registrado en el Engine. "
        "El módulo puede existir físicamente pero no estar acoplado."
    )

    return cont


# ===============================================================
# 1. DESCUBRIMIENTO
# ===============================================================

def test_cit_es_descubierto(engine_cit: Engine):
    """
    CIT debe ser descubierto por el mecanismo normal del Engine.
    """
    nombres = {
        path.name
        for path in engine_cit._modulos_descubiertos
    }

    assert "citacion" in nombres, (
        "La carpeta modules/citacion existe pero Engine no la descubre."
    )


# ===============================================================
# 2. REGISTRO
# ===============================================================

def test_cit_esta_registrado(engine_cit: Engine, cit):
    """
    CIT debe existir simultáneamente en los índices canónicos
    del RegistroModulos.
    """
    assert cit.nombre == "citacion"

    assert engine_cit.registro.contenedores["citacion"] is cit

    assert engine_cit.registro.por_id["CIT"] is cit

    assert engine_cit.registro.por_rol["CIT"][0] is cit


# ===============================================================
# 3. IDENTIDAD CONTRACTUAL
# ===============================================================

def test_cit_identidad_coherente(cit):
    """
    La identidad declarada por CIT debe ser internamente coherente.
    """
    assert cit.id == "CIT"
    assert cit.nombre == "citacion"
    assert cit.rol == "CIT"
    assert cit.version == "2.0"
    assert cit.version_contrato == "1.0"
    assert cit.esquema == "VPSI-CONTRACT-1.0"
    assert cit.compatible_desde == "1.0"
    assert cit.api_engine == ">=1.0"
    assert cit.estabilidad == "ESTABLE"


# ===============================================================
# 4. DEPENDENCIAS
# ===============================================================

def test_cit_no_declara_dependencias_inexistentes(engine_cit: Engine, cit):
    """
    CIT declara requiere=[].

    Por tanto, el Engine no debe inventarle dependencias ni
    registrar faltantes para CIT.
    """
    assert cit.requiere == []

    faltantes = engine_cit._dependencias.get("faltantes", {})

    assert "citacion" not in faltantes


def test_cit_dependencias_son_coherentes(engine_cit: Engine, cit):
    """
    Si CIT declara dependencias en el futuro, cada una deberá poder
    resolverse mediante el mecanismo canónico del RegistroModulos.

    Actualmente CIT declara ninguna.
    """
    for dependencia in cit.requiere:
        assert engine_cit.registro.primero(dependencia) is not None, (
            f"CIT declara dependencia '{dependencia}' pero Engine "
            f"no puede resolverla."
        )


# ===============================================================
# 5. CAPACIDADES CONTRACTUALES
# ===============================================================

def test_cit_capacidades_son_callables(cit):
    """
    Cada capacidad declarada en CONTENEDOR debe haber llegado al
    Contenedor como callable.
    """
    assert cit.capacidades

    for nombre, fn in cit.capacidades.items():
        assert callable(fn), (
            f"CIT declara capacidad '{nombre}' pero no es callable."
        )


def test_cit_capacidades_meta_cubre_todas_las_capacidades(cit):
    """
    Toda capacidad declarada debe poseer su metadato contractual.
    """
    capacidades = set(cit.capacidades)
    capacidades_meta = set(cit.capacidades_meta)

    faltantes = capacidades - capacidades_meta

    assert not faltantes, (
        "CIT declara capacidades sin capacidades_meta: "
        f"{sorted(faltantes)}"
    )


def test_cit_capacidades_meta_tiene_estructura_completa(cit):
    """
    Cada capacidad debe tener exactamente los campos mínimos que
    exige el Engine: descripcion, entrada y salida.
    """
    for capacidad, meta in cit.capacidades_meta.items():
        assert isinstance(meta, dict), (
            f"CIT: capacidades_meta['{capacidad}'] no es dict."
        )

        for campo in ("descripcion", "entrada", "salida"):
            assert campo in meta, (
                f"CIT: capacidad '{capacidad}' carece de '{campo}'."
            )

            assert isinstance(meta[campo], str), (
                f"CIT: capacidades_meta['{capacidad}']['{campo}'] "
                f"debe ser str."
            )


# ===============================================================
# 6. AUTORIZACIÓN ENGINE
# ===============================================================

def test_cit_autorizacion_engine(cit):
    """
    Verifica que CIT tenga la matriz contractual completa.
    """
    esperados = {
        "leer": True,
        "ejecutar": True,
        "consultar": True,
        "recombinar": True,
        "reportar": True,
        "auditar": True,
        "inventariar": True,
        "modificar": False,
        "alterar": False,
        "reescribir": False,
    }

    assert cit.autoriza_engine == esperados


# ===============================================================
# 7. ENGINE PUEDE INVOCAR CAPACIDADES BÁSICAS
# ===============================================================

@pytest.mark.parametrize(
    "capacidad",
    [
        "inventario",
        "reporte",
        "diagnostico",
        "barrer",
        "verificar",
    ],
)
def test_engine_puede_invocar_capacidades_cit(
    engine_cit: Engine,
    cit,
    capacidad: str,
):
    """
    Las capacidades contractuales estándar de reporting/verificación
    deben poder ejecutarse atravesando exclusivamente el Engine.
    """
    assert capacidad in cit.capacidades

    resultado = engine_cit.ejecutar_capacidad(
        "CIT",
        capacidad,
    )

    assert resultado["estado"] == "EXITO", (
        f"Engine no pudo ejecutar CIT.{capacidad}: "
        f"{resultado}"
    )

    assert resultado["modulo"] == "citacion"
    assert resultado["capacidad"] == capacidad


# ===============================================================
# 8. REPORTING REAL
# ===============================================================

def test_cit_entrega_reporte_a_traves_del_engine(engine_cit: Engine):
    """
    El Engine debe poder consolidar el reporte de CIT.
    """
    resultado = engine_cit.ejecutar_reporte("CIT")

    assert resultado["estado"] == "EXITO"

    reporte = resultado["resultado"]

    assert isinstance(reporte, dict)
    assert reporte["id"] == "CIT"
    assert reporte["nombre"] == "citacion"
    assert reporte["rol"] == "CIT"
    assert reporte["estado"] == "OPERATIVO"


def test_cit_entrega_diagnostico_a_traves_del_engine(engine_cit: Engine):
    """
    El diagnóstico propio de CIT debe ser accesible mediante Engine.
    """
    resultado = engine_cit.ejecutar_diagnostico("CIT")

    assert resultado["estado"] == "EXITO"

    diagnostico = resultado["resultado"]

    assert isinstance(diagnostico, dict)
    assert diagnostico["id"] == "CIT"
    assert diagnostico["coherente"] is True


def test_cit_entrega_inventario_a_traves_del_engine(engine_cit: Engine):
    """
    El inventario propio de CIT debe ser accesible mediante Engine.
    """
    resultado = engine_cit.ejecutar_inventario("CIT")

    assert resultado["estado"] == "EXITO"

    inventario = resultado["resultado"]

    assert isinstance(inventario, dict)
    assert inventario["id"] == "CIT"
    assert inventario["nombre"] == "citacion"
    assert inventario["rol"] == "CIT"


# ===============================================================
# 9. CAPACIDADES ESPECÍFICAS DE CIT
# ===============================================================

def test_engine_puede_invocar_resolver_de_cit(engine_cit: Engine):
    """
    Comprueba que resolver() no solamente esté declarado:
    debe poder atravesar el Engine.
    """
    resultado = engine_cit.ejecutar_capacidad(
        "CIT",
        "resolver",
        "ID_QUE_NO_EXISTE",
    )

    assert resultado["estado"] == "EXITO"

    salida = resultado["resultado"]

    assert isinstance(salida, dict)
    assert salida["id"] == "ID_QUE_NO_EXISTE"
    assert salida["resuelto"] is False


def test_engine_puede_invocar_registrar_de_cit(engine_cit: Engine):
    """
    Verifica el puente Engine → CIT.registrar().
    """
    declaracion = {
        "id": "TEST-CIT-001",
        "tipo": "evidencia",
        "fuente": "test_acoplamiento_cit",
        "enunciado": "Declaración de prueba de acoplamiento.",
    }

    resultado = engine_cit.ejecutar_capacidad(
        "CIT",
        "registrar",
        declaracion,
    )

    assert resultado["estado"] == "EXITO"

    salida = resultado["resultado"]

    assert salida["ok"] is True
    assert salida["declaracion"]["id"] == "TEST-CIT-001"


def test_engine_puede_invocar_citar(engine_cit: Engine):
    """
    Comprueba que CIT.citar() sea realmente accesible desde Engine.
    """
    resultado_registro = engine_cit.ejecutar_capacidad(
        "CIT",
        "registrar",
        {
            "id": "TEST-CIT-002",
            "tipo": "evidencia",
            "fuente": "test_acoplamiento_cit",
            "enunciado": "Declaración citable de prueba.",
        },
    )

    assert resultado_registro["estado"] == "EXITO"

    resultado_cita = engine_cit.ejecutar_capacidad(
        "CIT",
        "citar",
        {"id": "TEST-CIT-002"},
    )

    assert resultado_cita["estado"] == "EXITO"

    salida = resultado_cita["resultado"]

    assert salida["id"] == "CIT"
    assert salida["n"] >= 1


# ===============================================================
# 10. PRUEBA CRÍTICA:
#     MODO ENGINE DECLARADO POR CIT
# ===============================================================

def test_cit_declara_modo_engine_real(cit):
    """
    CIT declara explícitamente una capacidad destinada al modo Engine.

    El objetivo de este test es detectar una futura discrepancia entre
    lo que CIT declara y lo que el Engine reconoce.
    """
    assert "anunciar" in cit.capacidades
    assert callable(cit.capacidades["anunciar"])

    assert "evaluar" in cit.capacidades
    assert callable(cit.capacidades["evaluar"])


def test_engine_puede_invocar_anunciar_de_cit(engine_cit: Engine):
    """
    Prueba mínima del puente funcional:

        Engine → CIT.anunciar()

    No se importa CIT directamente para ejecutar la capacidad.
    """
    declaracion = {
        "id": "TEST-CIT-ENGINE-001",
        "tipo": "evidencia",
        "fuente": "test_acoplamiento_cit",
        "enunciado": "Prueba del modo Engine de CIT.",
    }

    resultado = engine_cit.ejecutar_capacidad(
        "CIT",
        "anunciar",
        declaracion,
    )

    assert resultado["estado"] == "EXITO"

    salida = resultado["resultado"]

    assert isinstance(salida, dict)
    assert salida["ok"] is True


# ===============================================================
# 11. CONSOLIDACIÓN
# ===============================================================

def test_cit_participa_en_consolidacion_del_engine(
    engine_cit: Engine,
):
    """
    CIT debe aparecer en la consolidación estándar del Engine.
    """
    consolidado = engine_cit.consolidar_reportes()

    assert "citacion" in consolidado["reportes"]
    assert "citacion" in consolidado["diagnosticos"]
    assert "citacion" in consolidado["inventarios"]


# ===============================================================
# 12. GRAFO ESTRUCTURAL
# ===============================================================

def test_cit_aparece_en_grafo_del_engine(engine_cit: Engine, cit):
    """
    CIT debe existir como nodo estructural del grafo.
    """
    nodos = engine_cit._grafo["nodos"]

    nodo_cit = [
        n
        for n in nodos
        if n.get("id") == "CIT"
        or n.get("nombre") == "citacion"
    ]

    assert nodo_cit, "CIT no aparece en el grafo estructural del Engine."


def test_cit_capacidades_aparecen_en_grafo(
    engine_cit: Engine,
    cit,
):
    """
    Las capacidades declaradas por CIT deben aparecer como nodos
    subordinados al módulo.
    """
    nodos = engine_cit._grafo["nodos"]

    for capacidad in cit.capacidades:
        cap_id = f"citacion.{capacidad}"

        assert any(
            n.get("id") == cap_id
            for n in nodos
        ), (
            f"CIT declara capacidad '{capacidad}' pero Engine no "
            f"la representa en su grafo."
        )


# ===============================================================
# 13. PAQUETE OMEGA
# ===============================================================

def test_cit_aparece_en_paquete_omega(engine_cit: Engine):
    """
    El módulo acoplado debe llegar hasta el expediente Omega.
    """
    paquete = engine_cit.paquete_omega()

    reportes = paquete["reportes"]

    modulo_cit = [
        r
        for r in reportes
        if r.get("id") == "CIT"
    ]

    assert modulo_cit, (
        "CIT fue registrado por Engine pero no llegó al paquete Omega."
    )

    contenido = modulo_cit[0]["contenido"]

    assert contenido["id"] == "CIT"
    assert contenido["nombre"] == "citacion"
    assert contenido["rol"] == "CIT"


# ===============================================================
# 14. PRUEBA FINAL DE ACOPLAMIENTO
# ===============================================================

def test_acoplamiento_cit_completo(engine_cit: Engine, cit):
    """
    Prueba resumen.

    Esta prueba representa la condición mínima:

        carpeta
          ↓
        descubrimiento
          ↓
        registro
          ↓
        contrato
          ↓
        capacidades
          ↓
        invocación
          ↓
        reporting
          ↓
        Omega
    """
    assert engine_cit.estado == "OPERATIVO"

    assert cit.id == "CIT"
    assert cit.nombre == "citacion"
    assert cit.rol == "CIT"

    assert cit.requiere == []

    assert cit.capacidades
    assert all(
        callable(fn)
        for fn in cit.capacidades.values()
    )

    assert set(cit.capacidades).issubset(
        set(cit.capacidades_meta)
    )

    assert cit.autoriza_engine["ejecutar"] is True
    assert cit.autoriza_engine["consultar"] is True
    assert cit.autoriza_engine["reportar"] is True

    reporte = engine_cit.ejecutar_reporte("CIT")
    diagnostico = engine_cit.ejecutar_diagnostico("CIT")
    inventario = engine_cit.ejecutar_inventario("CIT")

    assert reporte["estado"] == "EXITO"
    assert diagnostico["estado"] == "EXITO"
    assert inventario["estado"] == "EXITO"

    paquete = engine_cit.paquete_omega()

    assert any(
        r.get("id") == "CIT"
        for r in paquete["reportes"]
    )
