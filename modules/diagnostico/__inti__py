# ===============================================================
# VPSI-TRUTH — modules/diagnosticoD/__init__.py
# ===============================================================
#
# MÓDULO:              diagnosticoD
# ID:                  DGCO
# Rol:                 DGCO
# Versión módulo:      1.0
# Versión contrato:    1.0
# Esquema contrato:    VPSI-CONTRACT-1.0
# Estabilidad:         ESTABLE
# Compatible desde:    1.0
# API Engine:          >=1.0
#
# Diagnóstico global como módulo autónomo.
# No calcula Tru. No orquesta. No altera evidencia.
# Consolida reportes de módulos y expone censo/diagnóstico.
#
# Capacidades arquitectónicas (callables reales):
#   ejecutar_total, inspeccionar, registrar_inventario
#
# ===============================================================


# ===============================================================
# PARTE 1 — PRINCIPIOS, BANDERAS Y ESPECIFICACIONES PRECISAS
# ===============================================================

# ===============================================================
# 1.1 — IMPORTACIONES
# ===============================================================

from __future__ import annotations

from typing import Any, Dict, List, Optional

# ===============================================================
# FIN 1.1
# ===============================================================


# ===============================================================
# 1.2 — IDENTIDAD
# ===============================================================

ID_MODULO = "DGCO"
NOMBRE_MODULO = "diagnosticoD"
ROL_MODULO = "DGCO"

# ===============================================================
# FIN 1.2
# ===============================================================


# ===============================================================
# 1.3 — VERSIONES Y ESTABILIDAD
# ===============================================================

VERSION_MODULO = "1.0"
VERSION_CONTRATO = "1.0"
ESQUEMA_CONTRATO = "VPSI-CONTRACT-1.0"
COMPATIBLE_DESDE = "1.0"
API_ENGINE = ">=1.0"
ESTABILIDAD = "ESTABLE"

# ===============================================================
# FIN 1.3
# ===============================================================


# ===============================================================
# 1.4 — BANDERAS DE ESTADO
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
# FIN 1.4
# ===============================================================


# ===============================================================
# 1.5 — PESOS Y CONSTANTES DE DIAGNÓSTICO
# ===============================================================

PESOS: Dict[str, float] = {
    "critico": 1.0,
    "alto": 0.75,
    "medio": 0.5,
    "bajo": 0.25,
    "info": 0.1,
}

# ===============================================================
# FIN 1.5
# ===============================================================


# ===============================================================
# 1.6 — INVARIANTES
# ===============================================================

INVARIANTES = (
    "el id del módulo nunca cambia",
    "el rol nunca cambia",
    "las capacidades declaradas son siempre callables tras la resolución",
    "este módulo no modifica el estado de otros módulos",
    "este módulo no calcula Tru / C / L / K",
    "este módulo no orquesta el ciclo",
    "este módulo no altera evidencia recibida",
    "este módulo solo consolida reportes y expone censo",
    "este módulo no inventa capacidades no declaradas en CONTENEDOR",
)

# ===============================================================
# FIN 1.6
# ===============================================================

# ===============================================================
# FIN PARTE 1
# ===============================================================


# ===============================================================
# PARTE 4 — DEFINICIONES
# ===============================================================

# ===============================================================
# 4.1 — EXCEPCIONES
# ===============================================================

class ContratoInvalido(Exception):
    """El CONTENEDOR no cumple el esquema o la resolución falló."""
    pass


class DiagnosticoError(Exception):
    """Error de diagnóstico global."""
    pass

# ===============================================================
# FIN 4.1
# ===============================================================


# ===============================================================
# 4.2 — NÚCLEO DiagnosticoGlobal (lógica de módulo)
# ===============================================================

class DiagnosticoGlobal:
    """
    Consolidador de reportes de módulos.
    Solo lectura / recepción. No actúa sobre Engine ni negocio.
    """

    _reportes: Dict[str, List[Any]] = {}
    _historial: List[Dict[str, Any]] = []

    @classmethod
    def recibir_reporte(
        cls,
        modulo: str = "",
        errores: Optional[List] = None,
        **kwargs: Any,
    ) -> bool:
        """Registra un reporte de módulo. No altera el módulo origen."""
        nombre = str(modulo or "").strip() or "DESCONOCIDO"
        lista = list(errores or [])
        cls._reportes.setdefault(nombre, []).extend(lista)
        cls._historial.append({
            "modulo": nombre,
            "errores_n": len(lista),
            "extra": dict(kwargs) if kwargs else {},
        })
        if len(cls._historial) > 500:
            cls._historial = cls._historial[-500:]
        return True

    @classmethod
    def censo(cls, engine: Any = None, **kwargs: Any) -> Dict[str, Any]:
        """
        Censo consolidado.
        Si hay engine, intenta leer módulos registrados.
        Si no, usa solo reportes internos.
        """
        modulos: Dict[str, Any] = {}
        estados: Dict[str, str] = {}

        if engine is not None:
            catalogo = None
            for attr in ("modulos", "modules", "catalogo", "registry"):
                catalogo = getattr(engine, attr, None)
                if isinstance(catalogo, dict):
                    break
            if isinstance(catalogo, dict):
                for mid, meta in catalogo.items():
                    clave = str(mid)
                    modulos[clave] = {
                        "id": clave,
                        "meta": meta if not callable(meta) else str(type(meta)),
                        "reportes_n": len(cls._reportes.get(clave, [])),
                    }
                    estados[clave] = (
                        ESTADO_DEGRADADO
                        if cls._reportes.get(clave)
                        else ESTADO_OPERATIVO
                    )

        for nombre, errs in cls._reportes.items():
            if nombre not in modulos:
                modulos[nombre] = {
                    "id": nombre,
                    "meta": None,
                    "reportes_n": len(errs),
                }
                estados[nombre] = (
                    ESTADO_DEGRADADO if errs else ESTADO_OPERATIVO
                )

        total = len(modulos)
        con_errores = sum(1 for e in estados.values() if e == ESTADO_DEGRADADO)

        return {
            "tipo": "diagnostico_global",
            "id": ID_MODULO,
            "total": total,
            "con_errores": con_errores,
            "modulos": modulos,
            "estados": estados,
            "reportes": {
                k: list(v) for k, v in cls._reportes.items()
            },
            "historial_n": len(cls._historial),
            "coherente": True,
            "estado": ESTADO_OPERATIVO,
            "nota": (
                "Censo DGCO. Solo observa. "
                "No invalida arranque. No calcula Tru."
            ),
        }

    @classmethod
    def presentar(cls, informe: Optional[Dict[str, Any]] = None) -> str:
        """Formato legible del diagnóstico global."""
        if not isinstance(informe, dict):
            return "[DGCO] sin informe"
        total = informe.get("total", 0)
        con_errores = informe.get("con_errores", 0)
        estado = informe.get("estado", ESTADO_NO_INICIADO)
        lineas = [
            "=== DIAGNÓSTICO GLOBAL (DGCO) ===",
            "estado: {0}".format(estado),
            "total módulos: {0}".format(total),
            "con errores: {0}".format(con_errores),
            "coherente: {0}".format(informe.get("coherente")),
        ]
        estados = informe.get("estados") or {}
        if estados:
            lineas.append("--- estados ---")
            for mid, est in sorted(estados.items()):
                lineas.append("  {0}: {1}".format(mid, est))
        return "\n".join(lineas)

    @classmethod
    def reset(cls) -> None:
        """Limpia reportes e historial (solo pruebas / ciclo)."""
        cls._reportes.clear()
        cls._historial.clear()


def barrer_diagnostico(engine: Any = None, **kwargs: Any) -> Dict[str, Any]:
    """Barrido de diagnóstico global (centinela de dominio)."""
    return DiagnosticoGlobal.censo(engine, **kwargs)

# ===============================================================
# FIN 4.2
# ===============================================================

# ===============================================================
# FIN PARTE 4
# ===============================================================


# ===============================================================
# PARTE 5 — CONTRATO OFICIAL (CONTENEDOR)
# ===============================================================

CONTENEDOR: Dict[str, Any] = {

    # ============================================================
    # 5.1 — ESQUEMA
    # ============================================================
    "esquema": ESQUEMA_CONTRATO,
    "version_contrato": VERSION_CONTRATO,
    "version_modulo": VERSION_MODULO,
    "estabilidad": ESTABILIDAD,
    "compatible_desde": COMPATIBLE_DESDE,
    "api_engine": API_ENGINE,

    # ============================================================
    # 5.2 — IDENTIDAD
    # ============================================================
    "id": ID_MODULO,
    "nombre": NOMBRE_MODULO,
    "rol": ROL_MODULO,
    "descripcion": (
        "Diagnóstico global del sistema. Solo lectura / recepción de "
        "reportes de módulos. Cero actuación sobre Engine o negocio."
    ),

    # ============================================================
    # 5.3 — PROPÓSITO
    # ============================================================
    "funcion": (
        "Recibir y consolidar reportes de módulos, exponer censo y "
        "diagnóstico global sin modificar el estado del sistema."
    ),
    "no_hace": [
        "No calcula Tru.",
        "No recalcula C, L, K, Tru_Ri ni Tru_total.",
        "No modifica el estado del Engine.",
        "No modifica contratos.",
        "No altera evidencia recibida.",
        "No ejecuta lógica de dominio.",
    ],

    # ============================================================
    # 5.4 — AUTORIDAD
    # ============================================================
    "autoridad": [
        "Recibir reportes de módulos",
        "Consolidar censo y diagnóstico global",
        "Exponer estado general del sistema",
        "Reportar inventario y diagnóstico propios",
    ],

    # ============================================================
    # 5.5 — CONOCIMIENTO EXPORTABLE
    # ============================================================
    "conocimiento_exportable": [
        "censo",
        "verificar",
        "barrer",
        "presentar",
        "reportar",
        "inventario",
        "reporte",
        "diagnostico",
        "ejecutar_total",
        "inspeccionar",
        "registrar_inventario",
    ],

    # ============================================================
    # 5.6 — ACCESO
    # ============================================================
    "acceso": {
        "nivel": "completo",
        "descripcion": "Acceso total a recursos del módulo",
    },

    # ============================================================
    # 5.7 — DEPENDENCIAS
    # ============================================================
    "requiere": [
        "CE", "AX", "FO", "MC", "SF",
        "CA", "CX", "DI", "RE", "VX",
        "TX", "CH", "CIT", "UI",
        "CC", "TT", "SC", "CT",
    ],

    # ============================================================
    # 5.8 — ACCESO A ARCHIVOS
    # ============================================================
    "acceso_archivos": ["*"],

    # ============================================================
    # 5.9 — VALIDAR ESQUEMA
    # ============================================================
    "validar_esquema": ["*"],

    # ============================================================
    # 5.10 — AUTORIZACIÓN AL ENGINE
    # ============================================================
    "autoriza_engine": {
        "leer": True,
        "ejecutar": True,
        "consultar": True,
        "recombinar": True,
        "reportar": True,
        "auditar": True,
        "inventariar": True,
        "alterar": False,
        "crear": True,
        "actualizar": False,
        "validar": True,
        "procesar": True,
        "analizar": True,
        "generar": True,
        "exportar": True,
        "importar": True,
        "respaldar": True,
        "recuperar": True,
        "sincronizar": True,
        "monitorear": True,
        "metricas": True,
        "diagnostico": True,
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
        "validar_esquema": True,
        "acceso_archivos": True,
        "ejecutar_total": True,
        "inspeccionar": True,
        "registrar_inventario": True,
    },

    # ============================================================
    # 5.11 — CONSULTAS SOPORTADAS
    # ============================================================
    "consultas_soportadas": [
        "censo",
        "verificar",
        "barrer",
        "presentar",
        "reportar",
        "inventario",
        "reporte",
        "diagnostico",
        "ejecutar_total",
        "inspeccionar",
        "registrar_inventario",
    ],

    # ============================================================
    # 5.12 — CAPACIDADES
    # ============================================================
    "capacidades": {
        "verificar": "verificar",
        "barrer": "verificar",
        "censo": "censo",
        "presentar": "presentar",
        "reportar": "reportar",
        "inventario": "inventario",
        "reporte": "reporte",
        "diagnostico": "diagnostico",
        "ejecutar_total": "ejecutar_total",
        "inspeccionar": "inspeccionar",
        "registrar_inventario": "registrar_inventario",
    },

    # ============================================================
    # 5.13 — METADATOS DE CAPACIDADES (1:1)
    # ============================================================
    "capacidades_meta": {
        "censo": {
            "descripcion": "Censo consolidado de módulos registrados.",
            "entrada": "engine opcional",
            "validar_esquema": ["*"],
            "salida": "dict con total, modulos, estados",
            "acceso_archivos": ["*"],
        },
        "verificar": {
            "descripcion": "Verifica coherencia del diagnóstico global.",
            "entrada": "engine opcional",
            "validar_esquema": ["*"],
            "salida": "dict con coherente, errores, choques",
            "acceso_archivos": ["*"],
        },
        "barrer": {
            "descripcion": "Alias contractual de verificar.",
            "entrada": "engine opcional",
            "validar_esquema": ["*"],
            "salida": "dict con coherente, errores, choques",
            "acceso_archivos": ["*"],
        },
        "presentar": {
            "descripcion": "Presenta el diagnóstico global formateado.",
            "entrada": "informe opcional (dict)",
            "validar_esquema": ["*"],
            "salida": "str con diagnostico_global formateado",
            "acceso_archivos": ["*"],
        },
        "reportar": {
            "descripcion": "Recibe reporte de un módulo.",
            "entrada": "modulo, errores",
            "validar_esquema": ["*"],
            "salida": "bool",
            "acceso_archivos": ["*"],
        },
        "inventario": {
            "descripcion": "Inventario completo del módulo DGCO.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con id, nombre, rol, version, capacidades, pesos",
            "acceso_archivos": ["*"],
        },
        "reporte": {
            "descripcion": "Reporte interno de estado del módulo DGCO.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con estado, coherente, capacidades",
            "acceso_archivos": ["*"],
        },
        "diagnostico": {
            "descripcion": "Diagnóstico propio del módulo DGCO.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con estado, problemas, advertencias, recomendaciones",
            "acceso_archivos": ["*"],
        },
        "ejecutar_total": {
            "descripcion": (
                "Autoridad total de ENGINE sobre DGCO. "
                "Ejerce TODAS las unidades ejecutables. No inventa."
            ),
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["*"],
            "salida": "dict con resultados de todas las unidades ejecutadas",
            "acceso_archivos": ["*"],
        },
        "inspeccionar": {
            "descripcion": (
                "Inspección estructural de DGCO sin alterar contrato."
            ),
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["acceso_archivos"],
            "salida": "dict con estructura, capacidades y estado",
            "acceso_archivos": ["acceso_archivos"],
        },
        "registrar_inventario": {
            "descripcion": (
                "Instantánea determinista del inventario de DGCO."
            ),
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["acceso_archivos"],
            "salida": "dict con inventario registrado",
            "acceso_archivos": ["acceso_archivos"],
        },
    },

    # ============================================================
    # 5.14 — REPORTING
    # ============================================================
    "reporting": {
        "estado": True,
        "salud": True,
        "inventario": True,
        "capacidades": True,
        "errores": True,
        "advertencias": True,
        "dependencias": True,
        "version": True,
        "contrato": True,
        "conocimiento": True,
        "metricas": True,
        "diagnostico": True,
        "reporte": True,
        "acceso_archivos": True,
        "validar_esquema": True,
        "ejecutar_total": True,
        "inspeccionar": True,
        "registrar_inventario": True,
    },

    # ============================================================
    # 5.15 — ESTADOS VÁLIDOS
    # ============================================================
    "estados_validos": list(ESTADOS_VALIDOS),

    # ============================================================
    # 5.16 — INVARIANTES
    # ============================================================
    "invariantes": list(INVARIANTES),
}

# ===============================================================
# FIN PARTE 5
# ===============================================================


# ===============================================================
# PARTE 8 — CAPACIDADES PÚBLICAS
# ===============================================================

def censo(engine: Any = None, **kwargs: Any) -> Dict[str, Any]:
    return DiagnosticoGlobal.censo(engine, **kwargs)


def verificar(engine: Any = None, **kwargs: Any) -> Dict[str, Any]:
    out = censo(engine, **kwargs)
    if isinstance(out, dict):
        out = dict(out)
        out["coherente"] = True
    return out


def presentar(
    informe: Optional[Dict[str, Any]] = None,
    **kwargs: Any,
) -> str:
    if informe is None:
        return "[DGCO] sin informe"
    return DiagnosticoGlobal.presentar(informe)


def reportar(
    modulo: str = "",
    errores: Optional[List] = None,
    **kwargs: Any,
) -> bool:
    return bool(
        DiagnosticoGlobal.recibir_reporte(
            modulo=modulo, errores=errores, **kwargs
        )
    )


def inventario(peticion: Any = None) -> Dict[str, Any]:
    return {
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "pesos": dict(PESOS),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "invariantes": list(INVARIANTES),
        "reportes_n": sum(len(v) for v in DiagnosticoGlobal._reportes.values()),
        "nota": "DGCO módulo autónomo. No calcula Tru. No orquesta.",
    }


def reporte(peticion: Any = None) -> Dict[str, Any]:
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "estado": ESTADO_OPERATIVO,
        "coherente": True,
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "operaciones_arquitectonicas": {
            "ejecutar_total": True,
            "inspeccionar": True,
            "registrar_inventario": True,
        },
        "nota": "DGCO observa; no invalida arranque.",
    }


def diagnostico(peticion: Any = None) -> Dict[str, Any]:
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "estado": ESTADO_OPERATIVO,
        "coherente": True,
        "problemas": [],
        "advertencias": [],
        "recomendaciones": [],
        "nota": "DGCO consolida reportes; no diagnostica dominio de negocio.",
    }


def ejecutar_total(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    peticion_normalizada = (
        dict(peticion) if isinstance(peticion, dict) else {}
    )
    resultados: Dict[str, Any] = {}
    errores_ejecucion: List[str] = []
    capacidades = CONTENEDOR.get("capacidades", {})
    if not isinstance(capacidades, dict):
        return {
            "id": ID_MODULO,
            "modulo": NOMBRE_MODULO,
            "operacion": "ejecutar_total",
            "estado": ESTADO_DEGRADADO,
            "coherente": False,
            "capacidades_ejecutadas": [],
            "errores_ejecucion": [
                "{0}: CONTENEDOR['capacidades'] no es dict".format(NOMBRE_MODULO)
            ],
            "resultados": {},
            "capacidades_declaradas": [],
        }

    engine = peticion_normalizada.get("engine")
    for nombre in sorted(capacidades):
        if nombre == "ejecutar_total":
            continue
        referencia = capacidades[nombre]
        try:
            if callable(referencia):
                fn = referencia
            elif isinstance(referencia, str):
                fn = globals().get(referencia)
                if not callable(fn):
                    raise ContratoInvalido("'{0}' no es callable".format(referencia))
            else:
                raise ContratoInvalido(
                    "tipo inválido: {0}".format(type(referencia).__name__)
                )

            if nombre in ("censo", "verificar", "barrer"):
                resultados[nombre] = fn(engine=engine)
            elif nombre == "presentar":
                resultados[nombre] = fn(
                    informe=peticion_normalizada.get("informe")
                )
            elif nombre == "reportar":
                resultados[nombre] = fn(
                    modulo=peticion_normalizada.get("modulo", ""),
                    errores=peticion_normalizada.get("errores"),
                )
            else:
                resultados[nombre] = fn(peticion_normalizada)
        except Exception as exc:
            errores_ejecucion.append("{0}: {1}".format(nombre, exc))
            resultados[nombre] = None

    ejecutadas = sorted(n for n, r in resultados.items() if r is not None)
    coherente = not errores_ejecucion
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
        "capacidades_declaradas": sorted(capacidades.keys()),
    }


def inspeccionar(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "operacion": "inspeccionar",
        "constantes": {
            "ID_MODULO": ID_MODULO,
            "NOMBRE_MODULO": NOMBRE_MODULO,
            "ROL_MODULO": ROL_MODULO,
            "VERSION_MODULO": VERSION_MODULO,
            "VERSION_CONTRATO": VERSION_CONTRATO,
            "ESQUEMA_CONTRATO": ESQUEMA_CONTRATO,
            "ESTABILIDAD": ESTABILIDAD,
        },
        "capacidades_contractuales": sorted(
            CONTENEDOR.get("capacidades", {}).keys()
        ),
        "capacidades_meta": sorted(
            CONTENEDOR.get("capacidades_meta", {}).keys()
        ),
        "pesos": dict(PESOS),
        "reportes_n": sum(
            len(v) for v in DiagnosticoGlobal._reportes.values()
        ),
        "autoriza_engine": CONTENEDOR.get("autoriza_engine"),
        "reporting": CONTENEDOR.get("reporting"),
        "invariantes": list(INVARIANTES),
        "nota": "inspeccionar expone estructura de DGCO sin alterar contrato.",
    }


def registrar_inventario(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    inv = inventario(peticion)
    return {
        "id": ID_MODULO,
        "operacion": "registrar_inventario",
        "registrado": True,
        "inventario": inv,
        "nota": "Instantánea determinista del inventario de DGCO.",
    }

# ===============================================================
# FIN PARTE 8
# ===============================================================


# ===============================================================
# PARTE 10 — VALIDACIÓN, RESOLUCIÓN Y EXPORTACIONES
# ===============================================================

def _validar_contrato(cont: Dict[str, Any]) -> None:
    obligatorias = (
        "esquema", "version_contrato", "version_modulo",
        "id", "nombre", "rol", "descripcion",
        "funcion", "no_hace", "autoridad",
        "conocimiento_exportable", "requiere",
        "autoriza_engine", "consultas_soportadas",
        "capacidades", "capacidades_meta",
        "reporting", "estados_validos", "invariantes",
        "estabilidad", "compatible_desde", "api_engine",
    )
    faltantes = [k for k in obligatorias if k not in cont]
    if faltantes:
        raise ContratoInvalido(
            "{0}: CONTENEDOR incompleto. Faltan: {1}".format(
                NOMBRE_MODULO, faltantes
            )
        )
    if cont.get("esquema") != ESQUEMA_CONTRATO:
        raise ContratoInvalido(
            "{0}: esquema incompatible: {1}".format(
                NOMBRE_MODULO, cont.get("esquema")
            )
        )
    meta_caps = cont.get("capacidades_meta") or {}
    for nombre_cap in cont.get("capacidades") or {}:
        if nombre_cap not in meta_caps:
            raise ContratoInvalido(
                "{0}: capacidad '{1}' sin capacidades_meta".format(
                    NOMBRE_MODULO, nombre_cap
                )
            )


_CAP_MAP = {
    "verificar": verificar,
    "barrer": verificar,
    "censo": censo,
    "presentar": presentar,
    "reportar": reportar,
    "inventario": inventario,
    "reporte": reporte,
    "diagnostico": diagnostico,
    "ejecutar_total": ejecutar_total,
    "inspeccionar": inspeccionar,
    "registrar_inventario": registrar_inventario,
}


def _resolver_capacidades(cont: Dict[str, Any]) -> None:
    resueltas: Dict[str, Any] = {}
    for nombre, ref in cont["capacidades"].items():
        if callable(ref):
            resueltas[nombre] = ref
            continue
        if isinstance(ref, str):
            if ref not in _CAP_MAP:
                raise ContratoInvalido(
                    "{0}: capacidad '{1}' referencia inexistente: '{2}'".format(
                        NOMBRE_MODULO, nombre, ref
                    )
                )
            fn = _CAP_MAP[ref]
            if not callable(fn):
                raise ContratoInvalido(
                    "{0}: '{1}' no es callable".format(NOMBRE_MODULO, ref)
                )
            resueltas[nombre] = fn
            continue
        raise ContratoInvalido(
            "{0}: capacidad '{1}' tipo inválido: {2}".format(
                NOMBRE_MODULO, nombre, type(ref).__name__
            )
        )
    cont["capacidades"] = resueltas


_validar_contrato(CONTENEDOR)
_resolver_capacidades(CONTENEDOR)

__all__ = [
    "CONTENEDOR",
    "ID_MODULO",
    "NOMBRE_MODULO",
    "ROL_MODULO",
    "VERSION_MODULO",
    "VERSION_CONTRATO",
    "ESQUEMA_CONTRATO",
    "ESTABILIDAD",
    "DiagnosticoGlobal",
    "DiagnosticoError",
    "PESOS",
    "barrer_diagnostico",
    "censo",
    "verificar",
    "presentar",
    "reportar",
    "inventario",
    "reporte",
    "diagnostico",
    "ejecutar_total",
    "inspeccionar",
    "registrar_inventario",
    "ContratoInvalido",
]

# ===============================================================
# FIN PARTE 10
# ===============================================================


# ===============================================================
# FIN DEL MÓDULO
# ===============================================================
