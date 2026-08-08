"""
VPSI-TRUTH — modules/diagnostics/__init__.py

Rol: DG — Diagnóstico / Omega Report.

Este módulo NO calcula Tru.
Este módulo NO recalcula C, L, K, Tru_Ri ni Tru_total.
Este módulo NO orquesta el Engine.
Este módulo recibe y presenta información ya producida por el sistema.

Contrato:
    VPSI-CONTRACT-1.0
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


# ===============================================================
# CONTRATO VPSI-CONTRACT-1.0
# ===============================================================

CONTRATO: Dict[str, Any] = {
    "esquema": "VPSI-CONTRACT-1.0",
    "version_contrato": "1.0",
    "version_modulo": "1.1",

    "id": "diagnostics",

    "funcion": (
        "Recibir, validar y presentar información diagnóstica "
        "producida previamente por el Engine y los módulos."
    ),

    "no_hace": [
        "No calcula C.",
        "No calcula L.",
        "No calcula K.",
        "No calcula Tru_Ri.",
        "No calcula Tru_total.",
        "No recalcula axiomas.",
        "No recalcula mecánica.",
        "No altera estados del Engine.",
        "No modifica contadores.",
        "No escribe evidencia persistente.",
        "No sustituye al Centinela.",
        "No sustituye al Omega.",
    ],

    "autoridad": {
        "nivel": "DG",
        "fuente": "Engine",
        "alcance": "diagnostico_presentacion",
        "solo_lectura": True,
    },

    "conocimiento_exportable": {
        "tipo": "diagnostico",
        "exporta": [
            "estado_engine",
            "constantes",
            "informe_axiomas",
            "resultados_evaluacion",
            "informe_formulas",
            "informe_mecanica",
            "informe_self",
            "errores_arranque",
            "registro_modulos",
            "tests",
            "contratos",
            "citacion",
            "taxonomia",
            "evidencia_persistente",
        ],
    },

    "autoriza_engine": {
        "lectura": True,
        "escritura": False,
        "mutacion_estado": False,
        "orquestacion": False,
        "ejecucion_negocio": False,
    },

    "consultas_soportadas": [
        "verificar",
        "inventario",
        "generar_reporte",
        "validar_entrada",
        "leer_evidencia",
    ],

    "capacidades_meta": {
        "verificar": "Verifica suficiencia estructural de una entrada.",
        "inventario": "Expone identidad, contrato y capacidades del módulo.",
        "generar_reporte": "Genera el Omega Report sin recalcular métricas.",
        "validar_entrada": "Valida presencia y forma de los datos recibidos.",
        "leer_evidencia": "Lee evidencia persistente en modo solo lectura.",
    },

    "reporting": {
        "produce": [
            "omega_report",
            "diagnostico_global",
        ],
        "formato": "dict",
        "solo_presentacion": True,
        "recalcula_metricas": False,
    },

    "estados_validos": [
        "OPERATIVO",
        "RECHAZADO",
        "NO_INICIADO",
    ],

    "invariantes": [
        "No modifica el estado del Engine.",
        "No recalcula C.",
        "No recalcula L.",
        "No recalcula K.",
        "No recalcula Tru_Ri.",
        "No recalcula Tru_total.",
        "No modifica evaluaciones persistentes.",
        "No sustituye la autoridad del Engine.",
        "Los datos del reporte proceden de fuentes ya producidas.",
    ],

    "estabilidad": {
        "tipo": "ESTABLE",
        "compatibilidad": "BACKWARD_COMPATIBLE",
        "estado": "ACTIVO",
    },

    "compatible_desde": "1.0",

    "api_engine": [
        "verificar",
        "inventario",
        "generar_reporte",
        "validar_entrada",
        "leer_evidencia",
    ],
}


# ===============================================================
# CONTENEDOR
# ===============================================================

CONTENEDOR: Dict[str, Any] = {
    "nombre": "diagnostics",
    "rol": "DG",
    "version": "1.1",
    "requiere": ["CT", "AX", "FO"],
    "descripcion": (
        "Contenedor de diagnóstico. Rol DG. "
        "Recibe los informes reales producidos por el Engine y los módulos "
        "y genera el Omega Report sin recalcular nada. "
        "Lee evidencia persistente si existe; no la escribe."
    ),
    "capacidades": {},
    "contrato": CONTRATO,
}


# ===============================================================
# ERRORES
# ===============================================================

class DiagnosticoError(Exception):
    """Error en la capa de diagnóstico."""
    pass


class EntradaIncompletaError(DiagnosticoError):
    """Faltan informes obligatorios para generar el reporte."""
    pass


# ===============================================================
# DATOS EXIGIDOS AL ENGINE
# ===============================================================

CAMPOS_OBLIGATORIOS = (
    "estado_engine",
    "constantes",
    "informe_axiomas",
    "resultados_evaluacion",
)

CAMPOS_OPCIONALES = (
    "informe_formulas",
    "informe_mecanica",
    "informe_self",
    "errores_arranque",
    "registro_modulos",
    "tests",
    "contratos",
    "citacion",
    "taxonomia",
)


# ===============================================================
# VALIDACIÓN DE ENTRADA
# ===============================================================

def validar_entrada(datos: Dict[str, Any]) -> List[str]:
    """
    Verifica que el Engine haya pasado la información mínima real.

    No calcula ninguna métrica.
    """

    faltas: List[str] = []

    if not isinstance(datos, dict):
        return ["entrada no es dict"]

    for campo in CAMPOS_OBLIGATORIOS:
        if campo not in datos:
            faltas.append(
                "falta campo obligatorio: {0}".format(campo)
            )

    if "constantes" in datos:
        constantes = datos["constantes"]

        if (
            not isinstance(constantes, dict)
            or "ALPHA" not in constantes
            or "BETA" not in constantes
        ):
            faltas.append(
                "constantes debe contener ALPHA y BETA"
            )

    if "informe_axiomas" in datos:
        informe_axiomas = datos["informe_axiomas"]

        if not isinstance(informe_axiomas, dict):
            faltas.append(
                "informe_axiomas debe ser dict"
            )

        elif "coherente" not in informe_axiomas:
            faltas.append(
                "informe_axiomas sin clave 'coherente'"
            )

    if "estado_engine" in datos:
        if datos["estado_engine"] not in ESTADOS_VALIDOS:
            faltas.append(
                "estado_engine invalido: {0}".format(
                    datos["estado_engine"]
                )
            )

    if "resultados_evaluacion" in datos:
        if not isinstance(
            datos["resultados_evaluacion"],
            list,
        ):
            faltas.append(
                "resultados_evaluacion debe ser list"
            )

    return faltas


# ===============================================================
# EVIDENCIA PERSISTENTE
# ===============================================================

def _ruta_evaluaciones() -> Path:
    """
    modules/diagnostics/__init__.py
    parents[2] = raíz del repositorio.

    La evidencia está en:
        diagnostics/evaluaciones.json

    No es:
        modules/diagnostics/evaluaciones.json
    """

    raiz = Path(__file__).resolve().parents[2]

    return (
        raiz
        / "diagnostics"
        / "evaluaciones.json"
    )


def leer_evidencia() -> Dict[str, Any]:
    """
    Lee diagnostics/evaluaciones.json.

    Solo lectura.
    No escribe.
    No fusiona.
    No recalcula.
    """

    vacio: Dict[str, Any] = {
        "tipo": "evidencia_evaluacion",
        "version": None,
        "origen": None,
        "origenes": [],
        "n": 0,
        "resultados": [],
    }

    ruta = _ruta_evaluaciones()

    if not ruta.exists():
        return vacio

    try:
        doc = json.loads(
            ruta.read_text(
                encoding="utf-8"
            )
        )
    except Exception:
        return vacio

    if (
        not isinstance(doc, dict)
        or not isinstance(
            doc.get("resultados"),
            list,
        )
    ):
        return vacio

    return doc


# ===============================================================
# EXTRACCIÓN DE FACTORES
# ===============================================================

def _extraer_factores(
    entrada: Any,
) -> Dict[str, Any]:

    if not isinstance(entrada, dict):
        return {
            "C": None,
            "L": None,
            "K": None,
            "Tru_Ri": None,
            "Tru_total": None,
            "estado": None,
            "taxonomia": None,
            "citas": None,
        }

    resultado = entrada.get("resultado")

    if isinstance(resultado, dict):
        r = resultado
    else:
        r = entrada

    def _get(*claves: str) -> Any:

        for clave in claves:

            if (
                clave in r
                and r[clave] is not None
            ):
                return r[clave]

            if (
                clave in entrada
                and entrada[clave] is not None
            ):
                return entrada[clave]

        return None

    return {
        "C": _get("C", "c"),
        "L": _get("L", "l"),
        "K": _get("K", "k"),
        "Tru_Ri": _get(
            "Tru_Ri",
            "tru_ri",
            "TruRi",
        ),
        "Tru_total": _get(
            "Tru_total",
            "tru_total",
            "TruTotal",
        ),
        "estado": _get(
            "estado",
            "state",
        ),
        "taxonomia": _get(
            "taxonomia",
            "taxonomia_tx",
            "TX",
        ),
        "citas": _get(
            "citas",
            "citacion",
            "ids_cx_relevantes",
            "teoremas",
        ),
    }


# ===============================================================
# BLOQUE DE PRESENTACIÓN
# ===============================================================

def _bloque_calculo(
    titulo: str,
    factores: Dict[str, Any],
) -> Dict[str, Any]:

    return {
        "titulo": titulo,
        "C": factores.get("C"),
        "L": factores.get("L"),
        "K": factores.get("K"),
        "Tru_Ri": factores.get("Tru_Ri"),
        "Tru_total": factores.get("Tru_total"),
        "estado": factores.get("estado"),
        "taxonomia": (
            factores.get("taxonomia")
            if factores.get("taxonomia") is not None
            else "none"
        ),
        "citas": factores.get("citas"),
    }


# ===============================================================
# RESUMEN
# ===============================================================

def _resumen_evaluaciones(
    evaluaciones: List[Any],
) -> Dict[str, Any]:

    if not evaluaciones:
        return {
            "sistema": _bloque_calculo(
                "Auditoria del VPSI",
                {},
            ),
            "ultimo_test": _bloque_calculo(
                "Ultimo test",
                {},
            ),
            "n": 0,
            "origenes": [],
        }

    origenes = sorted(
        {
            str(e.get("origen"))
            for e in evaluaciones
            if (
                isinstance(e, dict)
                and e.get("origen")
            )
        }
    )

    sistema_filas = [
        e
        for e in evaluaciones
        if (
            isinstance(e, dict)
            and not str(
                e.get("origen") or ""
            ).startswith("test_")
        )
    ]

    if not sistema_filas:
        sistema_filas = [
            evaluaciones[0]
        ]

    test_filas = [
        e
        for e in evaluaciones
        if (
            isinstance(e, dict)
            and str(
                e.get("origen") or ""
            ).startswith("test_")
        )
    ]

    ultimo = (
        test_filas[-1]
        if test_filas
        else evaluaciones[-1]
    )

    sistema_ref = (
        sistema_filas[-1]
        if sistema_filas
        else {}
    )

    return {
        "sistema": _bloque_calculo(
            "Auditoria del VPSI",
            _extraer_factores(
                sistema_ref
            ),
        ),
        "ultimo_test": _bloque_calculo(
            "Ultimo test",
            _extraer_factores(
                ultimo
            ),
        ),
        "n": len(evaluaciones),
        "origenes": origenes,
    }


# ===============================================================
# GENERACIÓN DEL OMEGA REPORT
# ===============================================================

def generar_reporte(
    datos: Dict[str, Any],
    salida: Optional[Path] = None,
    incluir_evidencia: bool = True,
) -> Dict[str, Any]:

    faltas = validar_entrada(datos)

    if faltas:
        raise EntradaIncompletaError(
            "No se puede generar Omega Report. "
            "Faltan datos reales del sistema:\n  - "
            + "\n  - ".join(faltas)
        )

    evals_memoria = list(
        datos.get(
            "resultados_evaluacion"
        ) or []
    )

    if incluir_evidencia:
        evidencia = leer_evidencia()
    else:
        evidencia = {
            "n": 0,
            "resultados": [],
            "origenes": [],
        }

    evals_disco = list(
        evidencia.get(
            "resultados"
        ) or []
    )

    todas = (
        evals_memoria
        + evals_disco
    )

    resumen = _resumen_evaluaciones(
        todas
    )

    reporte: Dict[str, Any] = {
        "titulo": (
            "OMEGA REPORT - VPSI-TRUTH"
        ),

        "version_dg": (
            CONTENEDOR["version"]
        ),

        "generado": (
            datetime.now(
                timezone.utc
            ).isoformat()
        ),

        "estado_engine": (
            datos["estado_engine"]
        ),

        "constantes": (
            datos["constantes"]
        ),

        "axiomas": {
            "coherente": (
                datos[
                    "informe_axiomas"
                ].get("coherente")
            ),
            "declaraciones": (
                datos[
                    "informe_axiomas"
                ].get("declaraciones")
            ),
            "choques": len(
                datos[
                    "informe_axiomas"
                ].get("choques")
                or []
            ),
            "errores": len(
                datos[
                    "informe_axiomas"
                ].get("errores")
                or []
            ),
        },

        "formulas": datos.get(
            "informe_formulas"
        ),

        "mecanica": datos.get(
            "informe_mecanica"
        ),

        "contratos": datos.get(
            "contratos"
        ),

        "calculo_sistema": (
            resumen["sistema"]
        ),

        "calculo_ultimo_test": (
            resumen["ultimo_test"]
        ),

        "evaluaciones": {
            "n": resumen["n"],
            "origenes": resumen[
                "origenes"
            ],
            "memoria_n": len(
                evals_memoria
            ),
            "disco_n": len(
                evals_disco
            ),
            "filas": todas,
        },

        "evidencia_persistente": {
            "path": str(
                _ruta_evaluaciones()
            ),
            "n": evidencia.get(
                "n",
                0,
            ),
            "origenes": (
                evidencia.get(
                    "origenes"
                )
                or []
            ),
            "version": evidencia.get(
                "version"
            ),
        },

        "errores_arranque": (
            datos.get(
                "errores_arranque"
            )
            or []
        ),

        "modulos": datos.get(
            "registro_modulos"
        ),

        "tests": datos.get(
            "tests"
        ),

        "citacion": datos.get(
            "citacion"
        ),

        "taxonomia": datos.get(
            "taxonomia"
        ),

        "valido": (
            datos["estado_engine"]
            == "OPERATIVO"
        ),
    }

    if salida is not None:

        salida = Path(salida)

        salida.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        salida.write_text(
            json.dumps(
                reporte,
                indent=2,
                ensure_ascii=False,
                default=str,
            ),
            encoding="utf-8",
        )

    return reporte


# ===============================================================
# VERIFICACIÓN DEL MÓDULO
# ===============================================================

def verificar(
    datos: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:

    if datos is None:
        return {
            "contenedor": (
                CONTENEDOR["nombre"]
            ),
            "estado": "APROBADO",
            "coherente": True,
            "mensaje": (
                "Modulo DG listo. "
                "Esperando datos reales del Engine."
            ),
            "evidencia_disponible": (
                _ruta_evaluaciones().exists()
            ),
        }

    faltas = validar_entrada(
        datos
    )

    return {
        "contenedor": (
            CONTENEDOR["nombre"]
        ),
        "estado": (
            "APROBADO"
            if not faltas
            else "RECHAZADO"
        ),
        "coherente": not faltas,
        "faltas": faltas,
        "evidencia_disponible": (
            _ruta_evaluaciones().exists()
        ),
    }


# ===============================================================
# INVENTARIO
# ===============================================================

def inventario(
    peticion: Any = None,
) -> Dict[str, Any]:

    return {
        "contenedor": (
            CONTENEDOR["nombre"]
        ),
        "version": (
            CONTENEDOR["version"]
        ),
        "rol": (
            CONTENEDOR["rol"]
        ),
        "requiere": list(
            CONTENEDOR["requiere"]
        ),
        "campos_obligatorios": list(
            CAMPOS_OBLIGATORIOS
        ),
        "campos_opcionales": list(
            CAMPOS_OPCIONALES
        ),
        "capacidades": list(
            CONTENEDOR[
                "capacidades"
            ].keys()
        ),
        "evidencia_path": str(
            _ruta_evaluaciones()
        ),
    }


# ===============================================================
# CAPACIDADES REALES
# ===============================================================

CONTENEDOR["capacidades"] = {
    "verificar": verificar,
    "inventario": inventario,
    "generar_reporte": generar_reporte,
    "validar_entrada": validar_entrada,
    "leer_evidencia": leer_evidencia,
}


# ===============================================================
# EXPORTACIÓN
# ===============================================================

__all__ = [
    "CONTRATO",
    "CONTENEDOR",
    "verificar",
    "inventario",
    "generar_reporte",
    "validar_entrada",
    "leer_evidencia",
    "DiagnosticoError",
    "EntradaIncompletaError",
    "CAMPOS_OBLIGATORIOS",
    "CAMPOS_OPCIONALES",
]
