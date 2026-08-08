"""
VPSI-TRUTH --- modules/diagnostics/__init__.py

Rol DGS: diagnóstico sistémico / Omega Report.

Este módulo es reconocido directamente por el Engine como DGS.

No calcula Tru.
No recalcula C, L, K, Tru_Ri ni Tru_total.
No ejecuta módulos de dominio.
No modifica el estado del Engine.
No altera contratos.
No reconstruye evidencia.

Recibe información ya producida por el Engine y por los módulos,
valida su integridad estructural y genera el Omega Report.

La persistencia de evidencia corresponde a diagnostics/evidencia.py.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


# ===============================================================
# CONTENEDOR — CONTRATO VPSI
# ===============================================================

CONTENEDOR: Dict[str, Any] = {
    "nombre": "diagnostics",
    "rol": "DG",

    # -----------------------------------------------------------
    # IDENTIDAD CONTRACTUAL
    # -----------------------------------------------------------
    "esquema": "VPSI-CONTRACT-1.0",
    "version_contrato": "1.0",
    "version_modulo": "1.1",
    "id": "DGS",

    # -----------------------------------------------------------
    # FUNCIÓN
    # -----------------------------------------------------------
    "funcion": (
        "Diagnóstico sistémico y generación del Omega Report "
        "a partir de información real producida por el Engine "
        "y los módulos del sistema."
    ),

    # -----------------------------------------------------------
    # LÍMITES
    # -----------------------------------------------------------
    "no_hace": [
        "No calcula Tru.",
        "No recalcula C, L, K, Tru_Ri ni Tru_total.",
        "No vuelve a barrer axiomas.",
        "No ejecuta mecánica de dominio.",
        "No modifica el estado del Engine.",
        "No modifica contratos de otros módulos.",
        "No reconstruye registros de evidencia.",
        "No elimina claves de los registros recibidos.",
        "No decide por sí mismo la validez del sistema.",
    ],

    # -----------------------------------------------------------
    # AUTORIDAD
    # -----------------------------------------------------------
    "autoridad": "DG",

    "conocimiento_exportable": {
        "reportes": True,
        "evidencia": True,
        "diagnostico": True,
        "solo_lectura": True,
    },

    # -----------------------------------------------------------
    # AUTORIZACIÓN DEL ENGINE
    # -----------------------------------------------------------
    "autoriza_engine": {
        "registrar": True,
        "consultar": True,
        "reportar": True,
        "generar_reporte": True,
        "ejecutar": False,
        "modificar_estado": False,
        "modificar_contratos": False,
        "modificar_evidencia": False,
    },

    # -----------------------------------------------------------
    # CONSULTAS SOPORTADAS
    # -----------------------------------------------------------
    "consultas_soportadas": [
        "verificar",
        "inventario",
        "generar_reporte",
        "validar_entrada",
        "leer_evidencia",
    ],

    # -----------------------------------------------------------
    # CAPACIDADES META
    # -----------------------------------------------------------
    "capacidades_meta": {
        "observacion": True,
        "diagnostico": True,
        "presentacion": True,
        "actuacion": False,
        "mutacion_engine": False,
    },

    # -----------------------------------------------------------
    # REPORTING
    # -----------------------------------------------------------
    "reporting": {
        "produce_reporte": True,
        "nombre_reporte": "OMEGA REPORT",
        "solo_presentacion": True,
        "recalculo": False,
    },

    # -----------------------------------------------------------
    # ESTADOS
    # -----------------------------------------------------------
    "estados_validos": [
        "OPERATIVO",
        "RECHAZADO",
        "NO_INICIADO",
    ],

    # -----------------------------------------------------------
    # INVARIANTES
    # -----------------------------------------------------------
    "invariantes": [
        "No modifica el estado del Engine.",
        "No recalcula métricas.",
        "No altera evidencia recibida.",
        "No ejecuta lógica de dominio.",
        "No modifica contratos.",
        "Conserva la estructura de los registros recibidos.",
    ],

    # -----------------------------------------------------------
    # ESTABILIDAD
    # -----------------------------------------------------------
    "estabilidad": {
        "inmutable": True,
        "persistencia_externa": True,
        "compatible": True,
    },

    # -----------------------------------------------------------
    # COMPATIBILIDAD / API
    # -----------------------------------------------------------
    "compatible_desde": "1.0",
    "api_engine": "1.0",

    # -----------------------------------------------------------
    # DEPENDENCIAS
    # -----------------------------------------------------------
    "requiere": ["CT", "AX", "FO"],

    "descripcion": (
        "Contenedor de diagnóstico sistémico DGS. "
        "Recibe los informes reales producidos por el Engine "
        "y los módulos y genera el Omega Report sin recalcular "
        "ninguna métrica. Puede leer evidencia persistente, "
        "pero no la modifica directamente."
    ),

    # Se rellenan al final con callables reales.
    "capacidades": {},
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
# DATOS OBLIGATORIOS DEL ENGINE
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

    No calcula.
    No modifica.
    Solo valida presencia y estructura.
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
        c = datos["constantes"]

        if not isinstance(c, dict):
            faltas.append(
                "constantes debe ser dict"
            )
        elif "ALPHA" not in c or "BETA" not in c:
            faltas.append(
                "constantes debe contener ALPHA y BETA"
            )

    if "informe_axiomas" in datos:
        ia = datos["informe_axiomas"]

        if not isinstance(ia, dict):
            faltas.append(
                "informe_axiomas debe ser dict"
            )
        elif "coherente" not in ia:
            faltas.append(
                "informe_axiomas sin clave 'coherente'"
            )

    if "estado_engine" in datos:
        if datos["estado_engine"] not in (
            "OPERATIVO",
            "RECHAZADO",
            "NO_INICIADO",
        ):
            faltas.append(
                "estado_engine invalido: {0}".format(
                    datos["estado_engine"]
                )
            )

    if "resultados_evaluacion" in datos:
        if not isinstance(datos["resultados_evaluacion"], list):
            faltas.append(
                "resultados_evaluacion debe ser list"
            )

    return faltas


# ===============================================================
# EVIDENCIA PERSISTENTE
# ===============================================================

def _ruta_evaluaciones() -> Path:
    """
    diagnostics/ en la raíz del repositorio.

    modules/diagnostics/__init__.py
        parents[2]
            -> raíz del repo

    Por tanto:
        raíz/diagnostics/evaluaciones.json
    """
    raiz = Path(__file__).resolve().parents[2]
    return raiz / "diagnostics" / "evaluaciones.json"


def leer_evidencia() -> Dict[str, Any]:
    """
    Lee diagnostics/evaluaciones.json si existe.

    No escribe.
    No modifica.
    No fusiona.
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
            ruta.read_text(encoding="utf-8")
        )
    except Exception:
        return vacio

    if not isinstance(doc, dict):
        return vacio

    if not isinstance(doc.get("resultados"), list):
        return vacio

    return doc


# ===============================================================
# EXTRACCIÓN DE FACTORES
# ===============================================================

def _extraer_factores(entrada: Any) -> Dict[str, Any]:
    """
    Normaliza una fila de evaluación.

    No calcula ningún valor.
    Solo lee claves ya existentes.
    """
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

    r = (
        entrada.get("resultado")
        if isinstance(entrada.get("resultado"), dict)
        else entrada
    )

    def _get(*claves: str) -> Any:
        for k in claves:
            if k in r and r[k] is not None:
                return r[k]

            if k in entrada and entrada[k] is not None:
                return entrada[k]

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
    """
    Bloque de presentación.

    No calcula.
    """
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
# RESUMEN DE EVALUACIONES
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

    origenes = sorted({
        str(e.get("origen"))
        for e in evaluaciones
        if isinstance(e, dict)
        and e.get("origen")
    })

    sistema_filas = [
        e
        for e in evaluaciones
        if isinstance(e, dict)
        and not str(
            e.get("origen") or ""
        ).startswith("test_")
    ]

    if not sistema_filas:
        sistema_filas = (
            [evaluaciones[0]]
            if evaluaciones
            else []
        )

    test_filas = [
        e
        for e in evaluaciones
        if isinstance(e, dict)
        and str(
            e.get("origen") or ""
        ).startswith("test_")
    ]

    ultimo = (
        test_filas[-1]
        if test_filas
        else (
            evaluaciones[-1]
            if evaluaciones
            else {}
        )
    )

    sistema_ref = (
        sistema_filas[-1]
        if sistema_filas
        else {}
    )

    return {
        "sistema": _bloque_calculo(
            "Auditoria del VPSI",
            _extraer_factores(sistema_ref),
        ),
        "ultimo_test": _bloque_calculo(
            "Ultimo test",
            _extraer_factores(ultimo),
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
    """
    Genera el Omega Report.

    No ejecuta barrer().
    No llama a tru_ri().
    No llama a tru_total().
    No recalcula métricas.
    """
    faltas = validar_entrada(datos)

    if faltas:
        raise EntradaIncompletaError(
            "No se puede generar Omega Report. "
            "Faltan datos reales del sistema:\n  - "
            + "\n  - ".join(faltas)
        )

    evals_memoria = list(
        datos.get("resultados_evaluacion") or []
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
        evidencia.get("resultados") or []
    )

    todas = evals_memoria + evals_disco

    resumen = _resumen_evaluaciones(todas)

    reporte: Dict[str, Any] = {
        "titulo": "OMEGA REPORT - VPSI-TRUTH",
        "version_dg": CONTENEDOR["version_modulo"],
        "id_dg": CONTENEDOR["id"],
        "generado": datetime.now(
            timezone.utc
        ).isoformat(),

        "estado_engine": datos["estado_engine"],

        "constantes": datos["constantes"],

        "axiomas": {
            "coherente": datos[
                "informe_axiomas"
            ].get("coherente"),

            "declaraciones": datos[
                "informe_axiomas"
            ].get("declaraciones"),

            "choques": len(
                datos[
                    "informe_axiomas"
                ].get("choques") or []
            ),

            "errores": len(
                datos[
                    "informe_axiomas"
                ].get("errores") or []
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

        "calculo_sistema": resumen[
            "sistema"
        ],

        "calculo_ultimo_test": resumen[
            "ultimo_test"
        ],

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
            "origenes": evidencia.get(
                "origenes"
            ) or [],
            "version": evidencia.get(
                "version"
            ),
        },

        "errores_arranque": datos.get(
            "errores_arranque"
        ) or [],

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
            "contenedor": CONTENEDOR["nombre"],
            "id": CONTENEDOR["id"],
            "rol": CONTENEDOR["rol"],
            "estado": "APROBADO",
            "coherente": True,
            "mensaje": (
                "DGS listo. Esperando datos reales "
                "del Engine."
            ),
            "evidencia_disponible": (
                _ruta_evaluaciones().exists()
            ),
        }

    faltas = validar_entrada(datos)

    return {
        "contenedor": CONTENEDOR["nombre"],
        "id": CONTENEDOR["id"],
        "rol": CONTENEDOR["rol"],
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
        "contenedor": CONTENEDOR["nombre"],
        "id": CONTENEDOR["id"],
        "version": CONTENEDOR["version_modulo"],
        "rol": CONTENEDOR["rol"],
        "esquema": CONTENEDOR["esquema"],
        "version_contrato": CONTENEDOR[
            "version_contrato"
        ],
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
# CONTENEDOR — CAPACIDADES REALES
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
