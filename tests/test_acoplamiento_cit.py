# test_citacion.py
# ===============================================================
# PRUEBAS UNITARIAS PARA EL MÓDULO CITACIÓN (CIT)
# ===============================================================

import pytest
from modules.citacion import (
    CONTENEDOR,
    anunciar,
    anunciar_todo,
    barrer,
    buscar,
    cadena,
    citar,
    diagnostico,
    explicar,
    inventario,
    limpiar_ciclo,
    registrar,
    relacionar,
    reporte,
    resolver,
    verificar,
    verificar_salida,
)


@pytest.fixture(autouse=True)
def preparar_entorno():
    """Limpia el registro operativo antes de cada test."""
    limpiar_ciclo()
    yield
    limpiar_ciclo()


# ===============================================================
# 1. PRUEBAS DE REGISTRO Y RESOLUCIÓN
# ===============================================================

def test_registrar_y_resolver_declaracion():
    decl = {
        "id": "AX-101",
        "tipo": "axioma",
        "fuente": "modulo_base",
        "enunciado": "El orden del ciclo no afecta el resultado.",
        "descripcion": "Axioma de estabilidad"
    }
    
    # 1. Registrar
    res_reg = registrar(decl)
    assert res_reg["ok"] is True
    assert res_reg["n"] == 1
    assert res_reg["id"] == "CIT"

    # 2. Resolver por ID
    res_sol = resolver("AX-101")
    assert res_sol["resuelto"] is True
    assert res_sol["origen"] == "registro_ciclo"
    assert res_sol["declaracion"]["id"] == "AX-101"
    assert res_sol["declaracion"]["enunciado"] == "El orden del ciclo no afecta el resultado."


def test_registrar_declaracion_invalida():
    decl_invalida = {
        "id": "AX-102",
        "tipo": "tipo_desconocido_no_existente",
        # Falta 'fuente' y 'enunciado'
    }
    
    res = registrar(decl_invalida)
    assert res["ok"] is False
    assert "errores" in res
    assert len(res["errores"]) > 0


# ===============================================================
# 2. PRUEBAS DE BÚSQUEDA Y CITACIÓN (USO DE PETICIÓN DICI)
# ===============================================================

def test_buscar_con_filtros():
    registrar({
        "id": "DEF-1",
        "tipo": "definicion",
        "fuente": "modulo_a",
        "enunciado": "Definicion A"
    })
    registrar({
        "id": "DEF-2",
        "tipo": "teorema",
        "fuente": "modulo_b",
        "enunciado": "Teorema B"
    })

    # Filtrar por tipo
    res_tipo = buscar({"tipo": "definicion"})
    assert res_tipo["n"] == 1
    assert res_tipo["declaraciones"][0]["id"] == "DEF-1"

    # Filtrar por texto
    res_texto = buscar({"texto": "Teorema"})
    assert res_texto["n"] == 1
    assert res_texto["declaraciones"][0]["id"] == "DEF-2"


def test_citar_estructura_diccionario():
    registrar({
        "id": "AX-1",
        "tipo": "axioma",
        "fuente": "AX",
        "enunciado": "Axioma base"
    })

    # La función 'citar' espera una petición dict (opcional) y devuelve un dict
    res_citas = citar({"tipo": "axioma"})
    
    assert isinstance(res_citas, dict)
    assert res_citas["id"] == "CIT"
    assert "citas" in res_citas
    assert res_citas["n"] == 1
    assert res_citas["citas"][0]["id"] == "AX-1"


# ===============================================================
# 3. PRUEBAS DE RELACIONES Y CADENAS NORMATIVAS
# ===============================================================

def test_relacionar_declaraciones():
    registrar({"id": "AX-1", "tipo": "axioma", "fuente": "AX", "enunciado": "Base 1"})
    registrar({"id": "TEO-1", "tipo": "teorema", "fuente": "TEO", "enunciado": "Derivado 1"})

    res_rel = relacionar("TEO-1", "deriva_de", "AX-1")
    assert res_rel["ok"] is True
    assert res_rel["declaracion"]["id"] == "REL-TEO-1-deriva_de-AX-1"


def test_cadena_normativa():
    registrar({"id": "AX-1", "tipo": "axioma", "fuente": "AX", "enunciado": "Paso 1"})
    registrar({"id": "AX-2", "tipo": "axioma", "fuente": "AX", "enunciado": "Paso 2"})

    # Cadena completa
    res_cadena = cadena(["AX-1", "AX-2"])
    assert res_cadena["completa"] is True
    assert res_cadena["n"] == 2
    assert len(res_cadena["faltantes"]) == 0

    # Cadena incompleta
    res_incompleta = cadena(["AX-1", "NO_EXISTE"])
    assert res_incompleta["completa"] is False
    assert "NO_EXISTE" in res_incompleta["faltantes"]


# ===============================================================
# 4. PRUEBAS DE INTEGRIDAD DEL CONTRATO Y BARRIDO
# ===============================================================

def test_verificar_e_invariantes():
    res_barrer = barrer()
    assert res_barrer["coherente"] is True
    assert len(res_barrer["errores"]) == 0
    assert len(res_barrer["choques"]) == 0


def test_verificar_salida():
    salida_valida = {"id": "CIT", "coherente": True}
    salida_invalida = "Esto no es un diccionario"
    
    assert verificar_salida(salida_valida) is True
    assert verificar_salida(salida_invalida) is False


def test_inventario_y_reporte():
    inv = inventario()
    rep = reporte()
    diag = diagnostico()

    assert inv["id"] == "CIT"
    assert "capacidades" in inv
    assert rep["estado"] == "OPERATIVO"
    assert diag["coherente"] is True
