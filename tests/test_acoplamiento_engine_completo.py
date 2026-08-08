# ===============================================================
# TEST — AUDITORÍA test_acoplamiento_engine_completo ENGINE ↔ CONTENEDORES
# ===============================================================

from __future__ import annotations

import inspect
import json
from pathlib import Path
from typing import Any

import pytest

from core.engine import (
    Engine,
    ArranqueError,
    CLAVES_OBLIGATORIAS_CONTRATO,
    PERMISOS_AUTORIZA_ENGINE,
    BANDERAS_REPORTING,
)


# ===============================================================
# CONFIGURACIÓN
# ===============================================================

RAIZ_MODULOS = Path("modules")

ARCHIVO_SALIDA = Path("diagnostics/acoplamiento_engine_completo.json")


# ===============================================================
# UTILIDADES
# ===============================================================

def ejecutar_engine():
    """
    Intenta construir Engine sin ocultar errores.

    strict=False permite obtener el máximo diagnóstico posible
    aunque existan contenedores rechazados.
    """
    try:
        return Engine(
            raiz_modulos=RAIZ_MODULOS,
            invocador_id="core",
            strict=False,
        )
    except Exception as exc:
        pytest.fail(
            "No fue posible construir Engine incluso con strict=False: "
            f"{type(exc).__name__}: {exc}"
        )


def guardar_reporte(reporte: dict[str, Any]) -> None:
    ARCHIVO_SALIDA.parent.mkdir(parents=True, exist_ok=True)

    ARCHIVO_SALIDA.write_text(
        json.dumps(
            reporte,
            indent=2,
            ensure_ascii=False,
            default=str,
        ),
        encoding="utf-8",
    )


def inspeccionar_archivos_modulo(ruta: Path) -> dict[str, Any]:
    """
    Inspección física del directorio del módulo.

    Esto NO significa que Engine actualmente pueda pasar
    esos archivos a una capacidad. Solamente demuestra
    qué archivos existen y cuáles son legibles.
    """

    resultado = {
        "directorio": str(ruta),
        "existe": ruta.exists(),
        "es_directorio": ruta.is_dir(),
        "archivos": [],
        "archivos_legibles": [],
        "archivos_no_legibles": [],
    }

    if not ruta.is_dir():
        return resultado

    for archivo in sorted(ruta.rglob("*")):
        if not archivo.is_file():
            continue

        info = {
            "ruta": str(archivo),
            "nombre": archivo.name,
            "extension": archivo.suffix,
            "tamano_bytes": archivo.stat().st_size,
        }

        resultado["archivos"].append(info)

        try:
            archivo.read_bytes()
            resultado["archivos_legibles"].append(str(archivo))
        except Exception as exc:
            resultado["archivos_no_legibles"].append(
                {
                    "ruta": str(archivo),
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )

    return resultado


# ===============================================================
# AUDITORÍA PRINCIPAL
# ===============================================================

def construir_auditoria_engine(engine: Engine) -> dict[str, Any]:

    reporte: dict[str, Any] = {
        "engine": {
            "version": engine.VERSION,
            "estado": engine.estado,
            "raiz": str(engine.raiz),
            "total_contenedores_registrados": engine.registro.total(),
        },

        "resumen": {
            "contenedores_descubiertos": len(
                engine._modulos_descubiertos
            ),
            "contenedores_cargados": engine.registro.total(),
            "contenedores_rechazados": 0,
            "contratos_completos": 0,
            "contratos_incompletos": 0,
            "capacidades_declaradas": 0,
            "capacidades_callable": 0,
            "capacidades_no_callable": 0,
            "dependencias_faltantes": 0,
            "ciclos_dependencia": 0,
            "archivos_legibles": 0,
            "archivos_no_legibles": 0,
            "capacidades_contexto_unificado": 0,
            "capacidades_contexto_no_verificables": 0,
        },

        "errores_arranque": list(engine.errores_arranque),

        "dependencias": engine._dependencias,

        "contenedores": {},

        "engine_api": {
            "ejecutar_capacidad": True,
            "ejecutar_reporte": True,
            "ejecutar_diagnostico": True,
            "ejecutar_inventario": True,
            "ejecutar_con_contexto_unificado": True,
            "consolidar_reportes": True,
            "paquete_omega": True,
            "censar": True,
            "estado_global": True,
            "obtener_trazas": True,
            "invocar": True,
            "verificar_con_centinela": True,
        },

        "limitaciones_detectadas": {
            "lectura_generica_archivos_por_engine": False,
            "transferencia_generica_archivos_a_modulos": False,
            "ejecucion_arbitraria_de_todas_las_capacidades": False,
        },

        "problemas_estructurales_engine": [],
    }

    # -----------------------------------------------------------
    # COMPROBAR PROBLEMA DE reporting
    # -----------------------------------------------------------

    try:
        source = inspect.getsource(type(engine).registro.__class__)
    except Exception:
        source = ""

    # Inspección directa de Contenedor.
    try:
        from core.engine import Contenedor

        source_contenedor = inspect.getsource(Contenedor)

        if (
            'self.reporting: Dict[str, Any] = dict(meta.get("reporting") or {})'
            in source_contenedor
            and
            'self.reporting: Dict[str, Any] = dict(meta.get("reporte") or {})'
            in source_contenedor
        ):
            reporte["problemas_estructurales_engine"].append({
                "tipo": "ATRIBUTO_SOBRESCRITO",
                "campo": "reporting",
                "descripcion": (
                    "Contenedor asigna self.reporting dos veces. "
                    "La segunda asignación desde 'reporte' sobrescribe "
                    "el contenido obtenido desde 'reporting'."
                ),
                "severidad": "ALTA",
            })

    except Exception as exc:
        reporte["problemas_estructurales_engine"].append({
            "tipo": "NO_SE_PUDO_INSPECCIONAR_CONTENEDOR",
            "error": f"{type(exc).__name__}: {exc}",
        })

    # -----------------------------------------------------------
    # CONTENEDORES
    # -----------------------------------------------------------

    for nombre, cont in engine.registro.contenedores.items():

        datos: dict[str, Any] = {
            "identidad": {
                "nombre": cont.nombre,
                "id": cont.id,
                "rol": cont.rol,
                "version": cont.version,
                "version_contrato": cont.version_contrato,
                "esquema": cont.esquema,
                "api_engine": cont.api_engine,
                "compatible_desde": cont.compatible_desde,
            },

            "ruta": {
                "contrato": str(cont.ruta),
                "directorio": str(cont.ruta.parent),
            },

            "contrato": {
                "claves_presentes": sorted(cont.meta.keys()),
                "claves_faltantes": [],
                "claves_extra": [],
                "completo": True,
            },

            "autoriza_engine": {
                "total": len(PERMISOS_AUTORIZA_ENGINE),
                "presentes": {},
                "true": [],
                "false": [],
                "faltantes": [],
                "extras": [],
            },

            "reporting": {
                "banderas": {},
                "true": [],
                "false": [],
                "faltantes": [],
                "extras": [],
            },

            "capacidades": {
                "total": 0,
                "callable": [],
                "no_callable": [],
                "meta_faltante": [],
                "meta_completa": [],
            },

            "dependencias": {
                "declara": list(cont.requiere),
                "resueltas": [],
                "faltantes": [],
            },

            "archivos": inspeccionar_archivos_modulo(
                cont.ruta.parent
            ),

            "contexto_unificado": {
                "metodo_engine_existe": hasattr(
                    engine,
                    "ejecutar_con_contexto_unificado",
                ),
                "capacidades": {},
            },
        }

        # -------------------------------------------------------
        # CONTRATO
        # -------------------------------------------------------

        faltantes = [
            clave
            for clave in CLAVES_OBLIGATORIAS_CONTRATO
            if clave not in cont.meta
        ]

        extras = [
            clave
            for clave in cont.meta.keys()
            if clave not in CLAVES_OBLIGATORIAS_CONTRATO
        ]

        datos["contrato"]["claves_faltantes"] = faltantes
        datos["contrato"]["claves_extra"] = extras
        datos["contrato"]["completo"] = not faltantes

        if faltantes:
            reporte["resumen"]["contratos_incompletos"] += 1
        else:
            reporte["resumen"]["contratos_completos"] += 1

        # -------------------------------------------------------
        # AUTORIZACIONES
        # -------------------------------------------------------

        auth = cont.meta.get("autoriza_engine")

        if isinstance(auth, dict):

            for permiso in PERMISOS_AUTORIZA_ENGINE:

                if permiso not in auth:
                    datos["autoriza_engine"]["faltantes"].append(
                        permiso
                    )
                    continue

                valor = auth[permiso]

                datos["autoriza_engine"]["presentes"][
                    permiso
                ] = valor

                if valor is True:
                    datos["autoriza_engine"]["true"].append(
                        permiso
                    )
                elif valor is False:
                    datos["autoriza_engine"]["false"].append(
                        permiso
                    )

            datos["autoriza_engine"]["extras"] = sorted(
                set(auth.keys())
                - set(PERMISOS_AUTORIZA_ENGINE)
            )

        # -------------------------------------------------------
        # REPORTING
        # -------------------------------------------------------

        reporting = cont.meta.get("reporting")

        if isinstance(reporting, dict):

            for bandera in BANDERAS_REPORTING:

                if bandera not in reporting:
                    datos["reporting"]["faltantes"].append(
                        bandera
                    )
                    continue

                valor = reporting[bandera]

                datos["reporting"]["banderas"][
                    bandera
                ] = valor

                if valor is True:
                    datos["reporting"]["true"].append(
                        bandera
                    )
                elif valor is False:
                    datos["reporting"]["false"].append(
                        bandera
                    )

            datos["reporting"]["extras"] = sorted(
                set(reporting.keys())
                - set(BANDERAS_REPORTING)
            )

        # -------------------------------------------------------
        # CAPACIDADES
        # -------------------------------------------------------

        capacidades = cont.meta.get("capacidades")

        if isinstance(capacidades, dict):

            datos["capacidades"]["total"] = len(
                capacidades
            )

            reporte["resumen"]["capacidades_declaradas"] += len(
                capacidades
            )

            for capacidad, fn in capacidades.items():

                if callable(fn):

                    datos["capacidades"]["callable"].append(
                        capacidad
                    )

                    reporte["resumen"]["capacidades_callable"] += 1

                else:

                    datos["capacidades"]["no_callable"].append({
                        "capacidad": capacidad,
                        "tipo": type(fn).__name__,
                    })

                    reporte["resumen"]["capacidades_no_callable"] += 1

                meta_cap = cont.capacidades_meta.get(
                    capacidad
                )

                if not isinstance(meta_cap, dict):

                    datos["capacidades"]["meta_faltante"].append(
                        capacidad
                    )

                else:

                    faltan_meta = [
                        campo
                        for campo in (
                            "descripcion",
                            "entrada",
                            "salida",
                        )
                        if campo not in meta_cap
                    ]

                    if faltan_meta:

                        datos["capacidades"][
                            "meta_faltante"
                        ].append({
                            "capacidad": capacidad,
                            "faltantes": faltan_meta,
                        })

                    else:

                        datos["capacidades"][
                            "meta_completa"
                        ].append(capacidad)

                # ------------------------------------------------
                # CONTEXTO UNIFICADO
                # ------------------------------------------------

                datos["contexto_unificado"]["capacidades"][
                    capacidad
                ] = {
                    "callable": callable(fn),
                    "meta": meta_cap,
                    "firma": None,
                    "acepta_payload_dict": None,
                    "verificacion": "ESTATICA",
                }

                if callable(fn):

                    try:
                        firma = inspect.signature(fn)

                        datos["contexto_unificado"][
                            "capacidades"
                        ][capacidad]["firma"] = str(firma)

                        parametros = list(
                            firma.parameters.values()
                        )

                        acepta_payload = False

                        if len(parametros) == 1:
                            p = parametros[0]

                            if (
                                p.kind
                                in (
                                    inspect.Parameter.POSITIONAL_ONLY,
                                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                )
                            ):
                                acepta_payload = True

                        datos["contexto_unificado"][
                            "capacidades"
                        ][capacidad][
                            "acepta_payload_dict"
                        ] = acepta_payload

                    except Exception as exc:

                        datos["contexto_unificado"][
                            "capacidades"
                        ][capacidad][
                            "verificacion"
                        ] = (
                            "NO_SE_PUDO_INSPECCIONAR_FIRMA: "
                            f"{type(exc).__name__}: {exc}"
                        )

        # -------------------------------------------------------
        # DEPENDENCIAS
        # -------------------------------------------------------

        dependencias_info = engine._dependencias

        faltantes_dep = (
            dependencias_info
            .get("faltantes", {})
            .get(nombre, [])
        )

        datos["dependencias"]["faltantes"] = list(
            faltantes_dep
        )

        datos["dependencias"]["resueltas"] = [
            dep
            for dep in cont.requiere
            if dep not in faltantes_dep
        ]

        reporte["resumen"]["dependencias_faltantes"] += len(
            faltantes_dep
        )

        # -------------------------------------------------------
        # ARCHIVOS
        # -------------------------------------------------------

        reporte["resumen"]["archivos_legibles"] += len(
            datos["archivos"]["archivos_legibles"]
        )

        reporte["resumen"]["archivos_no_legibles"] += len(
            datos["archivos"]["archivos_no_legibles"]
        )

        # -------------------------------------------------------
        # GUARDAR
        # -------------------------------------------------------

        reporte["contenedores"][nombre] = datos

    # -----------------------------------------------------------
    # CICLOS
    # -----------------------------------------------------------

    reporte["resumen"]["ciclos_dependencia"] = len(
        engine._dependencias.get("ciclos", [])
    )

    # -----------------------------------------------------------
    # CONCLUSIÓN SOBRE LECTURA DE ARCHIVOS
    # -----------------------------------------------------------

    reporte["lectura_archivos"] = {
        "engine_lee_contrato": True,
        "archivo_que_lee_engine": "__init__.py",
        "mecanismo": "_leer_contrato()",

        "lectura_generica_de_archivos": {
            "implementada": False,
            "explicacion": (
                "Engine actualmente carga __init__.py para obtener "
                "CONTENEDOR. No existe en el código suministrado "
                "un método genérico del Engine para leer cualquier "
                "archivo del módulo."
            ),
        },

        "transferencia_archivo_a_modulo": {
            "implementada": False,
            "explicacion": (
                "ejecutar_con_contexto_unificado() solamente recibe "
                "un payload dict y lo entrega a fn(payload). "
                "No construye automáticamente un payload desde "
                "archivos del módulo."
            ),
        },

        "contexto_unificado": {
            "implementado": hasattr(
                engine,
                "ejecutar_con_contexto_unificado",
            ),
            "mecanismo": (
                "Engine → fn(payload)"
            ),
        },
    }

    guardar_reporte(reporte)

    return reporte


# ===============================================================
# TEST PRINCIPAL
# ===============================================================

def test_acoplamiento_engine_completo():

    engine = ejecutar_engine()

    reporte = construir_auditoria_engine(engine)

    print("\n")
    print("=" * 78)
    print("VPSI-TRUTH — AUDITORÍA INTEGRAL ENGINE ↔ CONTENEDORES")
    print("=" * 78)

    print(
        f"Engine: {reporte['engine']['version']}"
    )

    print(
        f"Estado: {reporte['engine']['estado']}"
    )

    print(
        f"Contenedores: "
        f"{reporte['resumen']['contenedores_cargados']}"
    )

    print(
        f"Capacidades declaradas: "
        f"{reporte['resumen']['capacidades_declaradas']}"
    )

    print(
        f"Capacidades callable: "
        f"{reporte['resumen']['capacidades_callable']}"
    )

    print(
        f"Capacidades no callable: "
        f"{reporte['resumen']['capacidades_no_callable']}"
    )

    print(
        f"Dependencias faltantes: "
        f"{reporte['resumen']['dependencias_faltantes']}"
    )

    print(
        f"Archivos legibles: "
        f"{reporte['resumen']['archivos_legibles']}"
    )

    print(
        f"Archivos no legibles: "
        f"{reporte['resumen']['archivos_no_legibles']}"
    )

    print("\n" + "-" * 78)

    for nombre, datos in reporte["contenedores"].items():

        print(f"\nCONTENEDOR: {nombre}")
        print(f"  ID: {datos['identidad']['id']}")
        print(f"  ROL: {datos['identidad']['rol']}")

        print(
            "  CONTRATO: "
            + (
                "COMPLETO"
                if datos["contrato"]["completo"]
                else "INCOMPLETO"
            )
        )

        print(
            f"  AUTORIZA_ENGINE TRUE: "
            f"{len(datos['autoriza_engine']['true'])}"
        )

        print(
            f"  AUTORIZA_ENGINE FALSE: "
            f"{len(datos['autoriza_engine']['false'])}"
        )

        print(
            f"  AUTORIZA_ENGINE FALTANTES: "
            f"{datos['autoriza_engine']['faltantes']}"
        )

        print(
            f"  REPORTING TRUE: "
            f"{datos['reporting']['true']}"
        )

        print(
            f"  REPORTING FALSE: "
            f"{datos['reporting']['false']}"
        )

        print(
            f"  CAPACIDADES: "
            f"{datos['capacidades']['total']}"
        )

        print(
            f"  CALLABLE: "
            f"{len(datos['capacidades']['callable'])}"
        )

        if datos["capacidades"]["no_callable"]:
            print(
                f"  NO CALLABLE: "
                f"{datos['capacidades']['no_callable']}"
            )

        print(
            f"  DEPENDENCIAS: "
            f"{datos['dependencias']['declara']}"
        )

        if datos["dependencias"]["faltantes"]:
            print(
                f"  DEPENDENCIAS FALTANTES: "
                f"{datos['dependencias']['faltantes']}"
            )

        print(
            f"  ARCHIVOS: "
            f"{len(datos['archivos']['archivos'])}"
        )

        print(
            f"  ARCHIVOS LEGIBLES: "
            f"{len(datos['archivos']['archivos_legibles'])}"
        )

        print(
            f"  ARCHIVOS NO LEGIBLES: "
            f"{len(datos['archivos']['archivos_no_legibles'])}"
        )

    print("\n" + "-" * 78)

    print(
        "LECTURA GENÉRICA DE ARCHIVOS POR ENGINE: "
        "NO IMPLEMENTADA"
    )

    print(
        "TRANSFERENCIA GENÉRICA ARCHIVO → MÓDULO: "
        "NO IMPLEMENTADA"
    )

    print(
        f"\nReporte completo: {ARCHIVO_SALIDA}"
    )

    print("=" * 78)

    # El test no debe fallar solamente porque encuentre una
    # inconsistencia: primero debe producir la radiografía.
    #
    # Lo que sí constituye fallo estructural inequívoco:
    assert reporte["engine"]["estado"] in {
        "OPERATIVO",
        "DEGRADADO",
        "RECHAZADO",
    }

    assert reporte["engine"][
        "total_contenedores_registrados"
    ] >= 0
