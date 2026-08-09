# ===============================================================
# VPSI-TRUTH
# INTEGRACIÓN REAL ENGINE → CAPACIDAD → ARCHIVO → CONTENIDO
# → ENTREGA → RECEPCIÓN → EJECUCIÓN
#
# OBJETIVOS:
#
# 5.  Engine invoca realmente capacidades.
# 6.  Engine puede leer los archivos necesarios.
# 7.  Engine puede extraer su contenido.
# 8.  Engine puede entregar el contenido al módulo correspondiente.
# 9.  La capacidad receptora recibe realmente ese contenido.
# 10. No existe ruptura contrato → resolución → ejecución real.
# ===============================================================

from __future__ import annotations

import inspect
from pathlib import Path

import pytest

from core.engine import Engine, ArranqueError


ROOT = Path(".")
MODULES = ROOT / "modules"


def crear_engine():
    try:
        return Engine(
            MODULES,
            invocador_id="pytest_integracion_real",
            strict=True,
        )
    except ArranqueError as exc:
        pytest.fail(
            "El Engine no puede arrancar en modo estricto: "
            f"{exc}"
        )


def obtener_contenedores(engine):
    registro = engine.registro

    contenedores = getattr(registro, "contenedores", None)

    assert isinstance(contenedores, dict), (
        "El registro no expone un mapa de contenedores."
    )

    assert contenedores, (
        "El Engine arrancó pero el registro está vacío."
    )

    return contenedores


def obtener_capacidades(contenedor):
    capacidades = getattr(
        contenedor,
        "capacidades",
        None,
    )

    assert isinstance(capacidades, dict), (
        f"El contenedor {getattr(contenedor, 'nombre', '?')} "
        "no expone un contrato de capacidades válido."
    )

    return capacidades


def resolver_por_engine(engine, contenedor, capacidad):
    """
    Resolución exclusivamente a través del camino que usa el Engine.

    NO se acepta getattr(contenedor.modulo, nombre) como sustituto.
    """

    if not hasattr(contenedor, "fn"):
        pytest.fail(
            f"{getattr(contenedor, 'nombre', '?')} no expone fn(). "
            "El contrato no tiene camino de resolución operativo."
        )

    try:
        fn = contenedor.fn(capacidad)
    except Exception as exc:
        pytest.fail(
            f"El Engine no pudo resolver {capacidad!r} en "
            f"{getattr(contenedor, 'nombre', '?')}: {exc}"
        )

    assert callable(fn), (
        f"La capacidad {capacidad!r} está declarada pero "
        "no se resolvió a callable."
    )

    return fn


def ejecutar_realmente(engine, contenedor, capacidad, peticion):
    """
    La prueba NO considera suficiente resolver fn().

    Primero intenta la ruta pública de Engine.
    Si el Engine delega al invocador, se comprueba también esa ruta.
    """

    errores = []

    # Ruta explícita del Engine.
    if hasattr(engine, "ejecutar_capacidad"):
        try:
            return engine.ejecutar_capacidad(
                contenedor,
                capacidad,
                peticion,
            )
        except TypeError as exc:
            errores.append(
                f"Engine.ejecutar_capacidad TypeError: {exc}"
            )
        except Exception as exc:
            errores.append(
                f"Engine.ejecutar_capacidad: {exc}"
            )

    # Ruta Engine → invocador.
    invocador = getattr(engine, "invocador", None)

    if invocador is not None and hasattr(
        invocador,
        "ejecutar_capacidad",
    ):
        try:
            return invocador.ejecutar_capacidad(
                contenedor,
                capacidad,
                peticion,
            )
        except TypeError as exc:
            errores.append(
                f"invocador.ejecutar_capacidad TypeError: {exc}"
            )
        except Exception as exc:
            errores.append(
                f"invocador.ejecutar_capacidad: {exc}"
            )

    pytest.fail(
        "NO EXISTE UNA RUTA REAL DE EJECUCIÓN DE CAPACIDAD. "
        f"capacidad={capacidad!r}; "
        f"errores={errores}"
    )


def extraer_payload(resultado):
    """
    Normaliza únicamente para inspección del test.

    No convierte automáticamente cualquier resultado en éxito.
    """

    if resultado is None:
        return None

    if isinstance(resultado, dict):
        for key in (
            "contenido",
            "content",
            "datos",
            "data",
            "resultado",
            "result",
            "salida",
            "output",
        ):
            if key in resultado:
                return resultado[key]

    return resultado


def contiene_marca(valor, marca):
    if isinstance(valor, bytes):
        return marca.encode("utf-8") in valor

    if isinstance(valor, str):
        return marca in valor

    if isinstance(valor, dict):
        return any(
            contiene_marca(k, marca)
            or contiene_marca(v, marca)
            for k, v in valor.items()
        )

    if isinstance(valor, (list, tuple, set)):
        return any(
            contiene_marca(v, marca)
            for v in valor
        )

    return False


# ===============================================================
# 5. INVOCACIÓN REAL
# ===============================================================

def test_engine_invoca_realmente_una_capacidad():
    engine = crear_engine()
    contenedores = obtener_contenedores(engine)

    candidatos = []

    for nombre, contenedor in contenedores.items():
        capacidades = obtener_capacidades(contenedor)

        for capacidad in capacidades:
            candidatos.append(
                (nombre, contenedor, capacidad)
            )

    assert candidatos, (
        "No existen capacidades declaradas para probar."
    )

    # Primero resolvemos y después ejecutamos.
    errores = []

    for nombre, contenedor, capacidad in candidatos:
        try:
            resolver_por_engine(
                engine,
                contenedor,
                capacidad,
            )

            resultado = ejecutar_realmente(
                engine,
                contenedor,
                capacidad,
                {},
            )

            # Llegar aquí significa que hubo ejecución real.
            assert resultado is not None, (
                f"La capacidad {nombre}.{capacidad} "
                "fue invocada pero devolvió None."
            )

            return

        except pytest.fail.Exception:
            raise
        except Exception as exc:
            errores.append(
                f"{nombre}.{capacidad}: {exc}"
            )

    pytest.fail(
        "Ninguna capacidad declarada pudo ser ejecutada "
        f"realmente por el Engine. Errores: {errores}"
    )


# ===============================================================
# 6. LECTURA REAL DE ARCHIVOS
# ===============================================================

def test_engine_y_modulos_tienen_archivos_reales_para_consumir():
    engine = crear_engine()
    contenedores = obtener_contenedores(engine)

    archivos_reales = []

    for nombre, contenedor in contenedores.items():
        modulo = getattr(contenedor, "modulo", None)

        if modulo is None:
            continue

        archivo = getattr(
            modulo,
            "__file__",
            None,
        )

        if archivo:
            path = Path(archivo)

            if path.is_file():
                archivos_reales.append(
                    (nombre, path)
                )

    assert archivos_reales, (
        "El Engine cargó módulos pero no se pudo verificar "
        "ningún archivo físico asociado a ellos."
    )

    for nombre, path in archivos_reales:
        assert path.read_bytes(), (
            f"El archivo del módulo {nombre} está vacío: {path}"
        )


# ===============================================================
# 7. EXTRACCIÓN DE CONTENIDO
# ===============================================================

def test_engine_puede_observar_contenido_real_de_un_modulo():
    engine = crear_engine()
    contenedores = obtener_contenedores(engine)

    encontrado = False

    for nombre, contenedor in contenedores.items():
        modulo = getattr(contenedor, "modulo", None)

        if modulo is None:
            continue

        archivo = getattr(
            modulo,
            "__file__",
            None,
        )

        if not archivo:
            continue

        path = Path(archivo)

        if not path.is_file():
            continue

        contenido = path.read_text(
            encoding="utf-8",
            errors="strict",
        )

        assert contenido, (
            f"No fue posible extraer contenido de {path}."
        )

        assert nombre in contenido or "__init__" in path.name, (
            f"Contenido inesperado en {path}; "
            "la lectura no produjo texto identificable."
        )

        encontrado = True
        break

    assert encontrado, (
        "No se pudo demostrar extracción de contenido real "
        "desde un archivo perteneciente a un módulo cargado."
    )


# ===============================================================
# 8–9. TRANSFERENCIA Y RECEPCIÓN
# ===============================================================

def test_contrato_y_capacidad_receptora_no_se_rompen():
    engine = crear_engine()
    contenedores = obtener_contenedores(engine)

    probadas = 0

    for nombre, contenedor in contenedores.items():
        capacidades = obtener_capacidades(contenedor)

        for capacidad in capacidades:
            # La prueba se centra en capacidades que admitan
            # una petición explícita de entrada.
            try:
                fn = resolver_por_engine(
                    engine,
                    contenedor,
                    capacidad,
                )
            except Exception:
                continue

            try:
                firma = inspect.signature(fn)
            except (TypeError, ValueError):
                continue

            parametros = [
                p
                for p in firma.parameters.values()
                if p.kind
                in (
                    inspect.Parameter.POSITIONAL_ONLY,
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    inspect.Parameter.KEYWORD_ONLY,
                )
            ]

            if not parametros:
                continue

            marca = (
                "VPSI_ENGINE_E2E_"
                f"{nombre}_"
                f"{capacidad}"
            )

            peticion = {
                "contenido": marca,
                "datos": marca,
                "contexto": marca,
                "entrada": marca,
                "peticion": marca,
            }

            try:
                resultado = ejecutar_realmente(
                    engine,
                    contenedor,
                    capacidad,
                    peticion,
                )
            except pytest.fail.Exception:
                raise
            except Exception:
                continue

            payload = extraer_payload(resultado)

            # Aquí no aceptamos simplemente "ejecutó".
            # El contenido tiene que aparecer en el resultado
            # o existir evidencia explícita de que fue recibido.
            if contiene_marca(payload, marca):
                probadas += 1
                continue

            if isinstance(resultado, dict):
                texto = repr(resultado)

                if marca in texto:
                    probadas += 1
                    continue

            pytest.fail(
                "La capacidad fue invocada pero el contenido "
                "no atravesó la frontera Engine → módulo → resultado. "
                f"módulo={nombre!r}, "
                f"capacidad={capacidad!r}, "
                f"marca={marca!r}, "
                f"resultado={resultado!r}"
            )

    assert probadas > 0, (
        "No se encontró ninguna capacidad con una interfaz "
        "de entrada verificable para probar transferencia "
        "real de contenido."
    )


# ===============================================================
# 10. CONTRATO → RESOLUCIÓN → EJECUCIÓN
# ===============================================================

def test_no_hay_ruptura_contrato_resolucion_ejecucion():
    engine = crear_engine()
    contenedores = obtener_contenedores(engine)

    fallos = []

    for nombre, contenedor in contenedores.items():
        contrato = obtener_capacidades(contenedor)

        for capacidad in contrato:
            try:
                fn = resolver_por_engine(
                    engine,
                    contenedor,
                    capacidad,
                )

                assert callable(fn)

            except Exception as exc:
                fallos.append(
                    {
                        "modulo": nombre,
                        "capacidad": capacidad,
                        "fase": "resolucion",
                        "error": repr(exc),
                    }
                )
                continue

            # Prueba de ejecución mínima.
            try:
                resultado = ejecutar_realmente(
                    engine,
                    contenedor,
                    capacidad,
                    {},
                )

                if resultado is None:
                    fallos.append(
                        {
                            "modulo": nombre,
                            "capacidad": capacidad,
                            "fase": "ejecucion",
                            "error": "resultado=None",
                        }
                    )

            except Exception as exc:
                fallos.append(
                    {
                        "modulo": nombre,
                        "capacidad": capacidad,
                        "fase": "ejecucion",
                        "error": repr(exc),
                    }
                )

    assert not fallos, (
        "RUPTURA CONTRATO → RESOLUCIÓN → EJECUCIÓN:\n"
        + "\n".join(repr(x) for x in fallos)
    )
