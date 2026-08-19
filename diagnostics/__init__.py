"""
VPSI-TRUTH --- modules/diagnostics/__init__.py

MÓDULO:              diagnostics
ID:                  DGS
Rol:                 DG
Versión módulo:      1.1
Versión contrato:    1.0
Esquema contrato:    VPSI-CONTRACT-1.0
Estabilidad:         ESTABLE
Compatible desde:   1.0
API Engine:          >=1.0

Función:
    Recibir, validar y presentar información diagnóstica producida
    por el Engine y por los módulos del sistema.

Qué hace:
    - Valida la estructura de los datos recibidos.
    - Lee evidencia persistente de evaluaciones.
    - Genera el Omega Report a partir de información ya producida.
    - Expone inventario y estado estructural.
    - Conserva la estructura de los registros recibidos.

Qué no hace:
    - No calcula Tru.
    - No recalcula C, L, K, Tru_Ri ni Tru_total.
    - No vuelve a barrer axiomas.
    - No ejecuta lógica de dominio.
    - No modifica el estado del Engine.
    - No modifica contratos.
    - No reconstruye registros de evidencia.

Responsabilidad:
    Diagnóstico sistémico de recepción y presentación.
    Este módulo observa, valida y presenta información existente.

Autoridad:
    - Validar la estructura de información diagnóstica recibida.
    - Presentar información producida por el sistema.
    - Reportar el estado estructural del diagnóstico.
    - Inventariar sus capacidades y contrato.

Conocimiento exportable:
    - inventario
    - reporte
    - diagnostico
    - estado
    - salud
    - capacidades
    - errores
    - advertencias
    - dependencias
    - versión
    - contrato
    - conocimiento
    - métricas
    - evidencia
    - omega_report

Relación con Engine:
    Engine descubre este CONTENEDOR y ejecuta únicamente las
    capacidades declaradas.

Relación con Omega:
    Omega recibe información ya producida por Engine.
    Este módulo no recalcula los valores que presenta.
"""

# ===============================================================
# IMPORTACIONES
# ===============================================================

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


from typing import Any, Dict, List, Optional



# ===============================================================
# IDENTIDAD Y VERSIONADO
# ===============================================================

ID_MODULO = "DGS"
NOMBRE_MODULO = "diagnostics"
ROL_MODULO = "DG"

VERSION_MODULO = "1.1"
VERSION_CONTRATO = "1.0"
ESQUEMA_CONTRATO = "VPSI-CONTRACT-1.0"

COMPATIBLE_DESDE = "1.0"
API_ENGINE = ">=1.0"

ESTABILIDAD = "ESTABLE"


# ===============================================================
# ESTADOS
# ===============================================================

ESTADO_NO_INICIADO = "NO_INICIADO"
ESTADO_OPERATIVO = "OPERATIVO"
ESTADO_DEGRADADO = "DEGRADADO"
ESTADO_RECHAZADO = "RECHAZADO"

ESTADOS_VALIDOS = (
    ESTADO_NO_INICIADO,
    ESTADO_OPERATIVO,
    ESTADO_DEGRADADO,
    ESTADO_RECHAZADO,
)


# ===============================================================
# INVARIANTES
# ===============================================================

INVARIANTES = (
    "el id del módulo nunca cambia",
    "el rol nunca cambia",
    "las capacidades declaradas son siempre callables tras la resolución",
    "este módulo no modifica el estado de otros módulos",
    "este módulo no recalcula métricas recibidas",
    "este módulo conserva la estructura de los registros recibidos",
    "este módulo no inventa capacidades no declaradas en CONTENEDOR",
)


# ===============================================================
# RUTAS
# ===============================================================

_DIR = Path(__file__).resolve()

# modules/diagnostics/__init__.py
# parents[0] = diagnostics
# parents[1] = modules
# parents[2] = raíz del repositorio
RAIZ_REPO = _DIR.parents[1]

DIAGNOSTICS_DIR = RAIZ_REPO / "diagnostics"
RUTA_EVIDENCIA = DIAGNOSTICS_DIR / "evaluaciones.json"


# ===============================================================
# ERRORES
# ===============================================================

class ContratoInvalido(Exception):
    """El CONTENEDOR no cumple el esquema contractual."""


class DiagnosticoError(Exception):
    """Error en la capa de diagnóstico."""


class EntradaIncompletaError(DiagnosticoError):
    """Faltan informes obligatorios para generar el reporte."""


# ===============================================================
# CAMPOS DEL DIAGNÓSTICO
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
# CONTRATO OFICIAL
# ===============================================================

CONTENEDOR: Dict[str, Any] = {

    # -----------------------------------------------------------
    # ESQUEMA / VERSIONADO
    # -----------------------------------------------------------

    "esquema": ESQUEMA_CONTRATO,
    "version_contrato": VERSION_CONTRATO,
    "version_modulo": VERSION_MODULO,
    "estabilidad": ESTABILIDAD,
    "compatible_desde": COMPATIBLE_DESDE,
    "api_engine": API_ENGINE,

    # -----------------------------------------------------------
    # IDENTIDAD
    # -----------------------------------------------------------

    "id": ID_MODULO,
    "nombre": NOMBRE_MODULO,
    "rol": ROL_MODULO,

    "descripcion": (
        "Contenedor de diagnóstico sistémico que recibe, valida y "
        "presenta información producida por el Engine y los módulos."
    ),

    # -----------------------------------------------------------
    # PROPÓSITO
    # -----------------------------------------------------------

    "funcion": (
        "Validar estructuralmente información diagnóstica existente "
        "y generar una representación objetiva del estado del sistema "
        "sin recalcular sus métricas."
    ),

    "no_hace": [
        "No calcula Tru.",
        "No recalcula C, L, K, Tru_Ri ni Tru_total.",
        "No vuelve a barrer axiomas.",
        "No ejecuta lógica de dominio.",
        "No modifica el estado del Engine.",
        "No modifica contratos.",
        "No altera evidencia recibida.",
        "No reconstruye registros recibidos.",
    ],

    # -----------------------------------------------------------
    # AUTORIDAD
    # -----------------------------------------------------------

    "autoridad": [
        "Validar la estructura de información diagnóstica recibida.",
        "Presentar información producida por el sistema.",
        "Reportar el estado estructural del diagnóstico.",
        "Inventariar el módulo y sus capacidades.",
    ],

    # -----------------------------------------------------------
    # CONOCIMIENTO EXPORTABLE
    # -----------------------------------------------------------

    "conocimiento_exportable": [
        "inventario",
        "reporte",
        "diagnostico",
        "estado",
        "salud",
        "capacidades",
        "errores",
        "advertencias",
        "dependencias",
        "version",
        "contrato",
        "conocimiento",
        "metricas",
        "evidencia",
        "omega_report",
    ],

    # ============================================================
    # ACCESO (obligatorio en el esquema)
    # ============================================================
    "acceso": {
        "nivel": "completo",
        "descripcion": "Acceso total a recursos del módulo"
    },

    # ============================================================
    # DEPENDENCIAS
    # ============================================================
    "requiere": ["*"],

    # ============================================================
    # ACCESO A ARCHIVOS (AGREGADO — obligatorio en el esquema)
    # ============================================================
    "acceso_archivos": ["*"],

    # ============================================================
    # VALIDAR ESQUEMA A NIVEL MÓDULO (AGREGADO — obligatorio en el esquema)
    # ============================================================
    "validar_esquema": ["*"],

    #============================================================
    # AUTORIZACIÓN AL ENGINE (SOLO PERMISOS)
    # ============================================================
    "autoriza_engine": {
        # --- PERMISOS BASE ---
        "leer": True,
        "ejecutar": True,
        "consultar": True,
        "recombinar": True,
        "reportar": True,
        "auditar": True,
        "inventariar": True,

        # --- PERMISOS DE ESCRITURA ---
        # "modificar": False,    # ← ELIMINADO (no permitido)
        "alterar": False,
        # "reescribir": False,   # ← ELIMINADO (no permitido)
        "crear": True,
        # "eliminar": False,     # ← ELIMINADO (no permitido)
        "actualizar": False,

        # --- PERMISOS DE PROCESAMIENTO ---
        "validar": True,
        "procesar": True,
        "analizar": True,
        "generar": True,
        # "transformar": False,  # ← ELIMINADO (no permitido)

        # --- PERMISOS DE DATOS ---
        "exportar": True,
        "importar": True,
        "respaldar": True,
        "recuperar": True,
        "sincronizar": True,

        # --- PERMISOS DE MONITOREO ---
        "monitorear": True,
        "metricas": True,
        "diagnostico": True,

        # --- PERMISOS DE ESTADO ---
        "estado": True,
        "version": True,
        "salud": True,
        "inventario": True,
        "capacidades": True,
        "errores": True,
        "advertencias": True,
        "dependencias": True,
        "contrato": True,
        "conocimiento": True,
        "reporte": True,

        # --- PERMISOS AGREGADOS (OBLIGATORIOS) ---
        "validar_esquema": True,     # ← AGREGADO
        "acceso_archivos": True,     # ← AGREGADO
    

        # --- CAPACIDADES ARQUITECTÓNICAS ---
        "ejecutar_total": True,
        "inspeccionar": True,
        "registrar_inventario": True,
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
 # ===============================================================
# EN capacidades — 
# ===============================================================
    "capacidades": {
        "verificar": "verificar",
        "inventario": "inventario",
        "generar_reporte": "generar_reporte",
        "validar_entrada": "validar_entrada",
        "leer_evidencia": "leer_evidencia",
        "reporte": "reporte",
        "diagnostico": "diagnostico",
        "ejecutar_total": "ejecutar_total",
        "inspeccionar": "inspeccionar",
        "registrar_inventario": "registrar_inventario",
    },
    # ============================================================
    # METADATOS DE CAPACIDADES (1:1 OBLIGATORIO)
    # ============================================================

    "capacidades_meta": {

        "verificar": {
            "descripcion": (
                "Valida que la información recibida sea suficiente "
                "y estructuralmente coherente."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con estado, coherente, faltas y evidencia",
            "acceso_archivos": ["*"],
        },

        "inventario": {
            "descripcion": (
                "Expone la identidad, contrato, dependencias y "
                "capacidades declaradas por DGS."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con inventario contractual del módulo",
            "acceso_archivos": ["*"],
        },

        "generar_reporte": {
            "descripcion": (
                "Genera el Omega Report utilizando únicamente "
                "información ya producida por el sistema."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con Omega Report",
            "acceso_archivos": ["*"],
        },

        "validar_entrada": {
            "descripcion": (
                "Comprueba la presencia y estructura de los campos "
                "obligatorios recibidos."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "list de faltas estructurales",
            "acceso_archivos": ["*"],
        },

        "leer_evidencia": {
            "descripcion": (
                "Lee la evidencia persistente de evaluaciones "
                "sin modificarla."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con evidencia persistente",
            "acceso_archivos": ["*"],
        },

        "reporte": {
            "descripcion": "Reporte de estado de DGS.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con id, estado, capacidades",
            "acceso_archivos": ["*"],
        },

        "diagnostico": {
            "descripcion": "Diagnóstico propio de DGS.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con estado, problemas, advertencias",
            "acceso_archivos": ["*"],
        },

        "ejecutar_total": {
            "descripcion": (
                "Ejecuta todas las capacidades públicas de DGS "
                "excepto ejecutar_total."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con resultados por capacidad",
            "acceso_archivos": ["*"],
        },

        "inspeccionar": {
            "descripcion": (
                "Meta-inspección estructural de contrato y callables."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con resolubles, errores, coherente",
            "acceso_archivos": ["*"],
        },

        "registrar_inventario": {
            "descripcion": (
                "Instantánea determinista del inventario. "
                "No altera evidencia."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con inventario registrado",
            "acceso_archivos": ["*"],
        },
    },
    
    # ============================================================
    # REPORTING (OBLIGATORIO EN EL ESQUEMA)
    # ============================================================
    "reporting": {
        # --- BANDERAS DE ESTADO Y SALUD ---
        "estado": True,
        "salud": True,

        # --- BANDERAS DE INVENTARIO Y CAPACIDADES ---
        "inventario": True,
        "capacidades": True,

        # --- BANDERAS DE ERRORES Y ADVERTENCIAS ---
        "errores": True,
        "advertencias": True,

        # --- BANDERAS DE DEPENDENCIAS Y VERSION ---
        "dependencias": True,
        "version": True,

        # --- BANDERAS DE CONTRATO Y CONOCIMIENTO ---
        "contrato": True,
        "conocimiento": True,

        # --- BANDERAS DE METRICAS Y DIAGNOSTICO ---
        "metricas": True,
        "diagnostico": True,

        # --- BANDERA DE REPORTE ---
        "reporte": True,

        # --- BANDERAS OBLIGATORIAS ENGINE ---
        "acceso_archivos": True,      # ← AGREGADA
        "validar_esquema": True,      # ← AGREGADA

        # --- CAPACIDADES ARQUITECTÓNICAS ---
        "ejecutar_total": True,
        "inspeccionar": True,
        "registrar_inventario": True,
    },
    

    # -----------------------------------------------------------
    # ESTADOS
    # -----------------------------------------------------------

    "estados_validos": list(ESTADOS_VALIDOS),

    # -----------------------------------------------------------
    # INVARIANTES
    # -----------------------------------------------------------

    "invariantes": list(INVARIANTES),

}  # <--- CIERRE FINAL


# ===============================================================
# VALIDACIÓN DEL CONTRATO
# ===============================================================
def _validar_contrato(cont: Dict[str, Any]) -> None:
    """
    Autoauditoría del contrato DGS.
    Fail-closed: cualquier incumplimiento impide cargar el módulo.
    """

    obligatorias = (
        "esquema",
        "version_contrato",
        "version_modulo",
        "id",
        "nombre",
        "rol",
        "descripcion",
        "funcion",
        "no_hace",
        "autoridad",
        "conocimiento_exportable",
        "requiere",
        "autoriza_engine",
        "consultas_soportadas",
        "capacidades",
        "capacidades_meta",
        "reporting",
        "estados_validos",
        "invariantes",
        "estabilidad",
        "compatible_desde",
        "api_engine",
    )

    faltantes = [
        clave
        for clave in obligatorias
        if clave not in cont
    ]

    if faltantes:
        raise ContratoInvalido(
            "{0}: CONTENEDOR incompleto. Faltan: {1}".format(
                NOMBRE_MODULO,
                faltantes,
            )
        )

    if cont.get("esquema") != ESQUEMA_CONTRATO:
        raise ContratoInvalido(
            "{0}: esquema incompatible: {1}".format(
                NOMBRE_MODULO,
                cont.get("esquema"),
            )
        )

    if str(cont.get("version_contrato")) != VERSION_CONTRATO:
        raise ContratoInvalido(
            "{0}: version_contrato inválida: {1}".format(
                NOMBRE_MODULO,
                cont.get("version_contrato"),
            )
        )

    if not isinstance(cont.get("no_hace"), list):
        raise ContratoInvalido(
            "{0}: 'no_hace' debe ser list".format(NOMBRE_MODULO)
        )

    if not isinstance(cont.get("autoridad"), list):
        raise ContratoInvalido(
            "{0}: 'autoridad' debe ser list".format(NOMBRE_MODULO)
        )

    if not isinstance(cont.get("conocimiento_exportable"), list):
        raise ContratoInvalido(
            "{0}: 'conocimiento_exportable' debe ser list".format(
                NOMBRE_MODULO
            )
        )

    if not isinstance(cont.get("requiere"), list):
        raise ContratoInvalido(
            "{0}: 'requiere' debe ser list".format(NOMBRE_MODULO)
        )

    if not isinstance(cont.get("capacidades"), dict):
        raise ContratoInvalido(
            "{0}: 'capacidades' debe ser dict".format(NOMBRE_MODULO)
        )

    if not isinstance(cont.get("capacidades_meta"), dict):
        raise ContratoInvalido(
            "{0}: 'capacidades_meta' debe ser dict".format(NOMBRE_MODULO)
        )

    # -----------------------------------------------------------
    # Regla 1:1 capacidades ↔ capacidades_meta
    # -----------------------------------------------------------

    for nombre_cap in cont["capacidades"]:

        if nombre_cap not in cont["capacidades_meta"]:
            raise ContratoInvalido(
                "{0}: capacidad '{1}' sin capacidades_meta".format(
                    NOMBRE_MODULO,
                    nombre_cap,
                )
            )

        meta = cont["capacidades_meta"][nombre_cap]

        if not isinstance(meta, dict):
            raise ContratoInvalido(
                "{0}: capacidades_meta['{1}'] debe ser dict".format(
                    NOMBRE_MODULO,
                    nombre_cap,
                )
            )

        for campo in (
            "descripcion",
            "entrada",
            "salida",
        ):
            if (
                campo not in meta
                or not isinstance(meta[campo], str)
            ):
                raise ContratoInvalido(
                    "{0}: capacidades_meta['{1}'] requiere "
                    "'{2}: str'".format(
                        NOMBRE_MODULO,
                        nombre_cap,
                        campo,
                    )
                )

    # -----------------------------------------------------------
    # Estados
    # -----------------------------------------------------------

    if not isinstance(cont.get("estados_validos"), list):
        raise ContratoInvalido(
            "{0}: 'estados_validos' debe ser list".format(
                NOMBRE_MODULO
            )
        )

    # -----------------------------------------------------------
    # Reporting
    # -----------------------------------------------------------

    if not isinstance(cont.get("reporting"), dict):
        raise ContratoInvalido(
            "{0}: 'reporting' debe ser dict".format(
                NOMBRE_MODULO
            )
        )


# ===============================================================
# LECTURA DE EVIDENCIA
# ===============================================================

def _ruta_evaluaciones() -> Path:
    return RUTA_EVIDENCIA


def leer_evidencia() -> Dict[str, Any]:
    """
    Lee diagnostics/evaluaciones.json.

    No escribe.
    No recalcula.
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

    if (
        not isinstance(doc, dict)
        or not isinstance(doc.get("resultados"), list)
    ):
        return vacio

    return doc


# ===============================================================
# VALIDACIÓN DE ENTRADA
# ===============================================================

def validar_entrada(
    datos: Dict[str, Any],
) -> List[str]:
    """
    Comprueba únicamente presencia y estructura.
    No calcula ningún factor.
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
        axiomas = datos["informe_axiomas"]

        if not isinstance(axiomas, dict):
            faltas.append(
                "informe_axiomas debe ser dict"
            )

        elif "coherente" not in axiomas:
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
        if not isinstance(
            datos["resultados_evaluacion"],
            list,
        ):
            faltas.append(
                "resultados_evaluacion debe ser list"
            )

    return faltas


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

    resultado = (
        entrada.get("resultado")
        if isinstance(
            entrada.get("resultado"),
            dict,
        )
        else entrada
    )

    def _get(*claves: str) -> Any:
        for clave in claves:

            if (
                clave in resultado
                and resultado[clave] is not None
            ):
                return resultado[clave]

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
        if (
            isinstance(e, dict)
            and e.get("origen")
        )
    })

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
        sistema_filas = (
            [evaluaciones[0]]
            if evaluaciones
            else []
        )

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

    No calcula Tru.
    No recalcula C/L/K.
    No ejecuta barridos.
    Solo valida, lee y presenta.
    """

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

    evidencia = (
        leer_evidencia()
        if incluir_evidencia
        else {
            "n": 0,
            "resultados": [],
            "origenes": [],
        }
    )

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

        "titulo":
            "OMEGA REPORT - VPSI-TRUTH",

        "id_modulo":
            ID_MODULO,

        "version_dg":
            CONTENEDOR["version_modulo"],

        "generado":
            datetime.now(
                timezone.utc
            ).isoformat(),

        "estado_engine":
            datos["estado_engine"],

        "constantes":
            datos["constantes"],

        "axiomas": {
            "coherente":
                datos[
                    "informe_axiomas"
                ].get("coherente"),

            "declaraciones":
                datos[
                    "informe_axiomas"
                ].get("declaraciones"),

            "choques":
                len(
                    datos[
                        "informe_axiomas"
                    ].get("choques") or []
                ),

            "errores":
                len(
                    datos[
                        "informe_axiomas"
                    ].get("errores") or []
                ),
        },

        "formulas":
            datos.get(
                "informe_formulas"
            ),

        "mecanica":
            datos.get(
                "informe_mecanica"
            ),

        "contratos":
            datos.get(
                "contratos"
            ),

        "calculo_sistema":
            resumen["sistema"],

        "calculo_ultimo_test":
            resumen["ultimo_test"],

        "evaluaciones": {
            "n":
                resumen["n"],

            "origenes":
                resumen["origenes"],

            "memoria_n":
                len(evals_memoria),

            "disco_n":
                len(evals_disco),

            "filas":
                todas,
        },

        "evidencia_persistente": {
            "path":
                str(_ruta_evaluaciones()),

            "n":
                evidencia.get("n", 0),

            "origenes":
                evidencia.get(
                    "origenes"
                ) or [],

            "version":
                evidencia.get(
                    "version"
                ),
        },

        "errores_arranque":
            datos.get(
                "errores_arranque"
            ) or [],

        "modulos":
            datos.get(
                "registro_modulos"
            ),

        "tests":
            datos.get(
                "tests"
            ),

        "citacion":
            datos.get(
                "citacion"
            ),

        "taxonomia":
            datos.get(
                "taxonomia"
            ),

        "valido":
            datos["estado_engine"]
            == "OPERATIVO",
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
# CAPACIDAD: VERIFICAR
# ===============================================================

def verificar(
    datos: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Verificación estructural de DGS.

    No diagnostica todo el sistema.
    """

    if datos is None:
        return {
            "id": ID_MODULO,
            "contenedor": NOMBRE_MODULO,
            "estado": "APROBADO",
            "coherente": True,
            "mensaje": (
                "Módulo DGS listo. "
                "Esperando datos reales del Engine."
            ),
            "evidencia_disponible":
                _ruta_evaluaciones().exists(),
        }

    faltas = validar_entrada(
        datos
    )

    return {
        "id": ID_MODULO,
        "contenedor": NOMBRE_MODULO,
        "estado":
            (
                "APROBADO"
                if not faltas
                else "RECHAZADO"
            ),
        "coherente":
            not faltas,
        "faltas":
            faltas,
        "evidencia_disponible":
            _ruta_evaluaciones().exists(),
    }


# ===============================================================
# CAPACIDAD: INVENTARIO
# ===============================================================

def inventario(
    peticion: Any = None,
) -> Dict[str, Any]:

    return {
        "id":
            ID_MODULO,

        "nombre":
            NOMBRE_MODULO,

        "rol":
            ROL_MODULO,

        "version":
            VERSION_MODULO,

        "version_contrato":
            VERSION_CONTRATO,

        "esquema":
            ESQUEMA_CONTRATO,

        "estabilidad":
            ESTABILIDAD,

        "capacidades":
            list(
                CONTENEDOR[
                    "capacidades"
                ].keys()
            ),

        "requiere":
            list(
                CONTENEDOR.get(
                    "requiere"
                ) or []
            ),

        "autoridad":
            CONTENEDOR.get(
                "autoridad"
            ),

        "conocimiento_exportable":
            CONTENEDOR.get(
                "conocimiento_exportable"
            ),

        "consultas_soportadas":
            CONTENEDOR.get(
                "consultas_soportadas"
            ),

        "invariantes":
            CONTENEDOR.get(
                "invariantes"
            ),

        "evidencia_path":
            str(
                _ruta_evaluaciones()
            ),
    }
# ===============================================================
# REPORTING
# ===============================================================

def reporte() -> Dict[str, Any]:
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "estado": ESTADO_OPERATIVO,
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "autoridad": CONTENEDOR.get("autoridad"),
        "conocimiento_exportable": CONTENEDOR.get("conocimiento_exportable"),
        "consultas_soportadas": CONTENEDOR.get("consultas_soportadas"),
    }


def diagnostico() -> Dict[str, Any]:
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "estado": ESTADO_OPERATIVO,
        "problemas": [],
        "advertencias": [],
        "recomendaciones": [],
    }

# ===============================================================
# FIN REPORTING
# ===============================================================


# ===============================================================
# EJECUTAR_TOTAL
# ===============================================================

def ejecutar_total(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    pet = dict(peticion) if isinstance(peticion, dict) else {}
    caps = list((CONTENEDOR.get("capacidades") or {}).keys())
    resultados: Dict[str, Any] = {}
    ejecutadas: List[str] = []
    errores_ejecucion: List[Dict[str, Any]] = []

    for nombre in caps:
        if nombre == "ejecutar_total":
            continue

        fn = CONTENEDOR["capacidades"].get(nombre)
        if not callable(fn):
            errores_ejecucion.append({
                "capacidad": nombre,
                "error": "no resoluble a callable",
            })
            continue

        try:
            if nombre == "verificar":
                resultados[nombre] = fn(pet if pet else None)
            elif nombre == "validar_entrada":
                resultados[nombre] = fn(pet)
            elif nombre == "generar_reporte":
                resultados[nombre] = {
                    "omitido": True,
                    "nota": "requiere datos reales del Engine",
                }
            else:
                resultados[nombre] = fn()
            ejecutadas.append(nombre)
        except Exception as exc:
            errores_ejecucion.append({
                "capacidad": nombre,
                "error": "{0}: {1}".format(type(exc).__name__, exc),
            })

    coherente = len(errores_ejecucion) == 0
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "operacion": "ejecutar_total",
        "estado": ESTADO_OPERATIVO if coherente else ESTADO_DEGRADADO,
        "coherente": coherente,
        "capacidades_ejecutadas": ejecutadas,
        "errores_ejecucion": errores_ejecucion,
        "resultados": resultados,
        "capacidades_declaradas": caps,
    }

# ===============================================================
# FIN EJECUTAR_TOTAL
# ===============================================================


# ===============================================================
# INSPECCIONAR
# ===============================================================

def inspeccionar(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    capacidades = CONTENEDOR.get("capacidades") or {}
    metas = CONTENEDOR.get("capacidades_meta") or {}
    errores: List[str] = []

    resolubles = [n for n, r in capacidades.items() if callable(r)]
    no_resolubles = [n for n in capacidades if n not in resolubles]
    sin_meta = [n for n in capacidades if n not in metas]
    metas_sin = [n for n in metas if n not in capacidades]

    for n in no_resolubles:
        errores.append("capacidad no resoluble: {0}".format(n))
    for n in sin_meta:
        errores.append("capacidad sin meta: {0}".format(n))
    for n in metas_sin:
        errores.append("meta sin capacidad: {0}".format(n))

    coherente = not errores
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "operacion": "inspeccionar",
        "estado": ESTADO_OPERATIVO if coherente else ESTADO_DEGRADADO,
        "coherente": coherente,
        "capacidades_contractuales": list(capacidades.keys()),
        "capacidades_meta": list(metas.keys()),
        "capacidades_resolubles": resolubles,
        "capacidades_no_resolubles": no_resolubles,
        "errores": errores,
        "autoriza_engine": CONTENEDOR.get("autoriza_engine"),
        "reporting": CONTENEDOR.get("reporting"),
        "invariantes": CONTENEDOR.get("invariantes"),
    }

# ===============================================================
# FIN INSPECCIONAR
# ===============================================================


# ===============================================================
# REGISTRAR_INVENTARIO
# ===============================================================

def registrar_inventario(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    return {
        "id": ID_MODULO,
        "operacion": "registrar_inventario",
        "registrado": True,
        "inventario": inventario(),
        "nota": (
            "Instantánea determinista del inventario de DGS. "
            "No modifica evidencia."
        ),
    }

# ===============================================================
# FIN REGISTRAR_INVENTARIO
# ===============================================================


# ===============================================================
# MAPA DE CAPACIDADES
# ===============================================================

_CAP_MAP = {
    "verificar": verificar,
    "inventario": inventario,
    "generar_reporte": generar_reporte,
    "validar_entrada": validar_entrada,
    "leer_evidencia": leer_evidencia,
    "reporte": reporte,
    "diagnostico": diagnostico,
    "ejecutar_total": ejecutar_total,
    "inspeccionar": inspeccionar,
    "registrar_inventario": registrar_inventario,
}

# ===============================================================
# FIN MAPA DE CAPACIDADES
# ===============================================================


# ===============================================================
# RESOLUCIÓN ESTRICTA
# ===============================================================

def _resolver_capacidades(cont: Dict[str, Any]) -> None:
    resueltas: Dict[str, Any] = {}

    for nombre, ref in cont["capacidades"].items():
        if callable(ref):
            resueltas[nombre] = ref
            continue

        if isinstance(ref, str):
            if ref not in _CAP_MAP or not callable(_CAP_MAP[ref]):
                raise ContratoInvalido(
                    "{0}: capacidad '{1}' no resoluble: '{2}'".format(
                        NOMBRE_MODULO, nombre, ref
                    )
                )
            resueltas[nombre] = _CAP_MAP[ref]
            continue

        raise ContratoInvalido(
            "{0}: capacidad '{1}' tipo inválido: {2}".format(
                NOMBRE_MODULO, nombre, type(ref).__name__
            )
        )

    cont["capacidades"] = resueltas

# ===============================================================
# FIN RESOLUCIÓN ESTRICTA
# ===============================================================


# ===============================================================
# VALIDACIÓN + RESOLUCIÓN
# ===============================================================

_validar_contrato(CONTENEDOR)
_resolver_capacidades(CONTENEDOR)

# ===============================================================
# FIN VALIDACIÓN + RESOLUCIÓN
# ===============================================================


# ===============================================================
# EXPORTACIONES
# ===============================================================

__all__ = [
    "CONTENEDOR",
    "ID_MODULO",
    "NOMBRE_MODULO",
    "ROL_MODULO",
    "VERSION_MODULO",
    "VERSION_CONTRATO",
    "ESQUEMA_CONTRATO",
    "ESTABILIDAD",
    "ContratoInvalido",
    "DiagnosticoError",
    "EntradaIncompletaError",
    "CAMPOS_OBLIGATORIOS",
    "CAMPOS_OPCIONALES",
    "verificar",
    "inventario",
    "reporte",
    "diagnostico",
    "generar_reporte",
    "validar_entrada",
    "leer_evidencia",
    "ejecutar_total",
    "inspeccionar",
    "registrar_inventario",
]

# ===============================================================
# FIN DEL MÓDULO DGS
# ===============================================================
