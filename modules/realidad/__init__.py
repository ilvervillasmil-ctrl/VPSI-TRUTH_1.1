# ===============================================================
# VPSI-TRUTH — modules/realidad/__init__.py
# ===============================================================
#
# MÓDULO:              realidad
# ID:                  RE
# Rol:                 RE
# Versión módulo:      2.0
# Versión contrato:    1.0
# Esquema contrato:    VPSI-CONTRACT-1.0
# Estabilidad:         ESTABLE
# Compatible desde:    1.0
# API Engine:          >=1.0
#
# Función:
#   Anclar el acceso a representaciones de la realidad y dominios
#   de conocimiento, velar no-contradicción entre ellos y sostener
#   el contrato de simbiosis dominio ↔ Engine.
#
# Qué hace:
#   - Descubre FUNCION en *.py y subcarpetas de dominio.
#   - Exige claves mínimas (nombre, hace) y unicidad de nombre.
#   - Registra simbiosis: dominio pide evaluación; material solo
#     sube con aprobación del dominio.
#   - Expone canal de acceso (abrir / traer / cerrar) vía acceso.py.
#   - Reporta inventario, estado y diagnóstico propios.
#
# Qué NO hace:
#   - No calcula C, L, K, Tru_Ri ni Tru_total.
#   - No elige “qué es verdad” ni privilegia instituciones.
#   - No aprueba material en nombre de un dominio ajeno.
#   - No orquesta el ciclo completo del sistema.
#   - No deposita en Diagnóstico (Engine decide el destino).
#
# Responsabilidad:
#   Coherencia interna del módulo RE y contrato de simbiosis
#   dominio ↔ Engine sobre material de realidad.
#
# Autoridad:
#   - Declarar el oficio RE y el centinela de no-contradicción.
#   - Registrar cierre contractual de material (aprobado/rechazado).
#   - Reportar estado estructural del módulo.
#
# Conocimiento exportable:
#   - inventario
#   - reporte
#   - diagnostico
#   - funciones / dominios descubiertos
#   - estados de material
#   - contrato de simbiosis
#
# Relación con Engine:
#   Engine descubre este CONTENEDOR, ejecuta solo las capacidades
#   declaradas, puede inspeccionar archivos del módulo y consolida
#   el reporte que este módulo produce.
#
# Relación con Omega:
#   Omega no calcula nada de este módulo.
#   Solo presenta lo que Engine entrega.
#
# Observaciones:
#   Todo *.py del directorio (y un nivel de subcarpetas) con FUNCION
#   participa del descubrimiento. Sin FUNCION no declara, no pasa.
#   Canal puro: acceso.Canal. Dominios etiquetan material y piden
#   evaluación bajo su O; RE no recalcula.
#
# NOTAS DE ARQUITECTURA:
#   1. CONTENEDOR es la única interfaz pública para Engine.
#   2. Capacidades ↔ capacidades_meta en 1:1.
#   3. requiere y no_hace son obligatorias (pueden ser []).
#   4. No importa módulos de dominio; si necesita algo, requiere[].
#   5. Contrato positivo: qué ES y qué GARANTIZA.
#
# ===============================================================

# ===============================================================
# IMPORTACIONES
# ===============================================================
#
# Solo stdlib, tipado y canal local de este módulo.
# No importar AX, FO, CA, MC, CIT, … — Engine resuelve.
#

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from .acceso import Canal, hay_acceso, hay_dns, HAY_REQUESTS

# ===============================================================
# FIN IMPORTACIONES
# ===============================================================

# ===============================================================
# CONSTANTES
# ===============================================================

ID_MODULO = "RE"
NOMBRE_MODULO = "realidad"
ROL_MODULO = "RE"

VERSION_MODULO = "2.0"
VERSION_CONTRATO = "1.0"
ESQUEMA_CONTRATO = "VPSI-CONTRACT-1.0"

COMPATIBLE_DESDE = "1.0"
API_ENGINE = ">=1.0"
ESTABILIDAD = "ESTABLE"

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

CLAVES_FUNCION = ("nombre", "hace")

ESTADOS_MATERIAL = (
    "pendiente",
    "evaluado",
    "aprobado",
    "rechazado",
    "bloqueado_re",
)

INVARIANTES = (
    "el id del módulo nunca cambia",
    "el rol nunca cambia",
    "las capacidades declaradas son siempre callables tras la resolución",
    "este módulo no modifica el estado de otros módulos",
    "este módulo no inventa capacidades no declaradas en CONTENEDOR",
    "RE no calcula C/L/K/Tru",
    "material sin aprobación de dominio no debe usarse arriba",
    "barrer solo vela coherencia interna de RE, no del sistema completo",
)

# ===============================================================
# FIN CONSTANTES
# ===============================================================

# ===============================================================
# CONFIGURACIÓN
# ===============================================================

_DIR = Path(__file__).parent

# ===============================================================
# FIN CONFIGURACIÓN
# ===============================================================

# ===============================================================
# DEFINICIONES
# ===============================================================

class ContratoInvalido(Exception):
    """El CONTENEDOR no cumple el esquema o la resolución falló."""

# ===============================================================
# FIN DEFINICIONES
# ===============================================================

# ===============================================================
# CONTRATO OFICIAL DEL MÓDULO
# ===============================================================

CONTENEDOR: Dict[str, Any] = {
    # ----- ESQUEMA -----
    "esquema": ESQUEMA_CONTRATO,
    "version_contrato": VERSION_CONTRATO,
    "version_modulo": VERSION_MODULO,
    "estabilidad": ESTABILIDAD,
    "compatible_desde": COMPATIBLE_DESDE,
    "api_engine": API_ENGINE,

    # ----- IDENTIDAD -----
    "id": ID_MODULO,
    "nombre": NOMBRE_MODULO,
    "rol": ROL_MODULO,
    "descripcion": (
        "Contenedor de realidad (RE). Ancla de contraste con "
        "representaciones de la realidad y dominios de conocimiento. "
        "Canal de acceso + dominios que declaran oficio y O de evaluación. "
        "Simbiosis: Engine aplica la fórmula bajo ese O; el material solo "
        "sube si el dominio aprueba; este módulo vela no-contradicción "
        "entre funciones del directorio. No calcula Tru."
    ),

    # ----- PROPÓSITO -----
    "funcion": (
        "Descubrir y validar dominios/funciones del módulo; sostener "
        "el contrato de simbiosis dominio↔Engine; registrar aprobación "
        "o rechazo de material; reportar estado estructural propio."
    ),
    "no_hace": [
        "No calcula C, L, K, Tru_Ri ni Tru_total",
        "No elige qué es verdad ni privilegia instituciones",
        "No aprueba material en nombre de un dominio ajeno",
        "No orquesta el ciclo completo del sistema",
        "No deposita reportes en Diagnóstico",
        "No sustituye el visto bueno de cada dominio",
    ],

    # ----- AUTORIDAD -----
    "autoridad": [
        "Descubrir FUNCION en archivos y subcarpetas de dominio",
        "Velar no-contradicción y unicidad de nombres de función",
        "Registrar cierre contractual de material (aprobado/rechazado)",
        "Exponer estado del canal de acceso",
        "Reportar inventario, reporte y diagnóstico propios",
    ],

    # ----- CONOCIMIENTO EXPORTABLE -----
    "conocimiento_exportable": [
        "inventario",
        "reporte",
        "diagnostico",
        "funciones",
        "dominios_simbiosis",
        "estados_material",
        "contrato_simbiosis",
        "acceso",
    ],

    # ----- DEPENDENCIAS -----
    "requiere": [],

    # ----- AUTORIZACIÓN AL ENGINE -----
    "autoriza_engine": {
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
    },

    # ----- CONSULTAS SOPORTADAS -----
    "consultas_soportadas": [
        "verificar",
        "barrer",
        "inventario",
        "reporte",
        "diagnostico",
        "registrar_resultado_dominio",
    ],

    # ----- CAPACIDADES -----
    "capacidades": {
        "verificar": "verificar",
        "barrer": "barrer",
        "inventario": "inventario",
        "reporte": "reporte",
        "diagnostico": "diagnostico",
        "registrar_resultado_dominio": "registrar_resultado_dominio",
        "verificar_salida": "verificar_salida",
    },

    # ----- METADATOS DE CAPACIDADES (1:1) -----
    "capacidades_meta": {
        "verificar": {
            "descripcion": (
                "Garantiza la coherencia interna de RE "
                "(alias de barrer)."
            ),
            "entrada": "ninguna",
            "salida": "dict con coherente, choques, errores, funciones",
        },
        "barrer": {
            "descripcion": (
                "Centinela de no-contradicción entre dominios/funciones "
                "y registro de simbiosis dominio↔Engine."
            ),
            "entrada": "ninguna",
            "salida": (
                "dict con coherente, choques, errores, funciones, "
                "dominios_simbiosis, estados_material, notas"
            ),
        },
        "inventario": {
            "descripcion": "Enumeración de funciones, simbiosis y canal.",
            "entrada": "peticion opcional",
            "salida": (
                "dict con id, version, funciones, coherente, acceso, "
                "contrato_simbiosis"
            ),
        },
        "reporte": {
            "descripcion": "Estado actual del módulo RE.",
            "entrada": "ninguna",
            "salida": "dict con estado, version, capacidades, coherente",
        },
        "diagnostico": {
            "descripcion": "Problemas, advertencias y recomendaciones de RE.",
            "entrada": "ninguna",
            "salida": (
                "dict con estado, problemas, advertencias, recomendaciones"
            ),
        },
        "registrar_resultado_dominio": {
            "descripcion": (
                "Cierra el tramo de simbiosis para un material: "
                "registra aprobación o rechazo del dominio tras "
                "resultado de Engine. No recalcula Tru."
            ),
            "entrada": (
                "nombre_dominio: str, material_id: str, "
                "resultado_engine: dict, aprobacion_dominio: bool"
            ),
            "salida": "dict con ok, estado, nota",
        },
        "verificar_salida": {
            "descripcion": "Forma mínima de una salida de RE.",
            "entrada": "salida: dict",
            "salida": "bool",
        },
    },

    # ----- REPORTING -----
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
    },

    # ----- ESTADOS VÁLIDOS -----
    "estados_validos": list(ESTADOS_VALIDOS),

    # ----- INVARIANTES -----
    "invariantes": list(INVARIANTES),
}

# ===============================================================
# FIN CONTRATO
# ===============================================================

# ===============================================================
# FUNCIONES PRIVADAS
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
    if not isinstance(cont.get("capacidades"), dict):
        raise ContratoInvalido(
            "{0}: 'capacidades' debe ser dict".format(NOMBRE_MODULO)
        )
    if not isinstance(cont.get("requiere"), list):
        raise ContratoInvalido(
            "{0}: 'requiere' debe ser list".format(NOMBRE_MODULO)
        )
    if not isinstance(cont.get("no_hace"), list):
        raise ContratoInvalido(
            "{0}: 'no_hace' debe ser list".format(NOMBRE_MODULO)
        )
    meta_caps = cont.get("capacidades_meta") or {}
    if not isinstance(meta_caps, dict):
        raise ContratoInvalido(
            "{0}: 'capacidades_meta' debe ser dict".format(NOMBRE_MODULO)
        )
    for nombre_cap in cont["capacidades"]:
        if nombre_cap not in meta_caps:
            raise ContratoInvalido(
                "{0}: capacidad '{1}' sin capacidades_meta".format(
                    NOMBRE_MODULO, nombre_cap
                )
            )
        entrada = meta_caps[nombre_cap]
        if not isinstance(entrada, dict):
            raise ContratoInvalido(
                "{0}: capacidades_meta['{1}'] debe ser dict".format(
                    NOMBRE_MODULO, nombre_cap
                )
            )
        for campo in ("descripcion", "entrada", "salida"):
            if campo not in entrada or not isinstance(entrada[campo], str):
                raise ContratoInvalido(
                    "{0}: capacidades_meta['{1}'] requiere '{2}: str'".format(
                        NOMBRE_MODULO, nombre_cap, campo
                    )
                )


def _descubrir() -> Dict[str, Dict[str, Any]]:
    """
    Recorre la carpeta y un nivel de subcarpetas.
    Solo archivos con FUNCION (dict) participan.
    """
    registro: Dict[str, Dict[str, Any]] = {}
    candidatos = list(sorted(_DIR.glob("*.py")))
    for sub in sorted(_DIR.iterdir()):
        if sub.is_dir() and not sub.name.startswith("_"):
            candidatos.extend(sorted(sub.glob("*.py")))

    for f in candidatos:
        if f.name.startswith("_") or f.name == "__init__.py":
            continue
        try:
            rel = f.relative_to(_DIR)
        except ValueError:
            rel = Path(f.name)
        clave = "realidad_{0}".format(
            str(rel).replace("/", "_").replace("\\", "_")
        )
        if clave.endswith(".py"):
            clave = clave[:-3]

        spec = importlib.util.spec_from_file_location(clave, str(f))
        if spec is None or spec.loader is None:
            continue
        mod = importlib.util.module_from_spec(spec)
        sys.modules[clave] = mod
        try:
            spec.loader.exec_module(mod)
        except Exception as e:
            registro[str(rel)] = {
                "archivo": str(rel),
                "error": "{0}: {1}".format(type(e).__name__, e),
            }
            continue

        meta = getattr(mod, "FUNCION", None)
        if not isinstance(meta, dict):
            continue

        entrada: Dict[str, Any] = {
            "archivo": str(rel),
            "nombre": meta.get("nombre"),
            "hace": meta.get("hace"),
            "provee": list(meta.get("provee") or []),
        }
        if meta.get("o_evaluacion") is not None:
            entrada["o_evaluacion"] = meta.get("o_evaluacion")
        if meta.get("pide_evaluacion_engine") is not None:
            entrada["pide_evaluacion_engine"] = bool(
                meta.get("pide_evaluacion_engine")
            )
        if meta.get("requiere_aprobacion_dominio") is not None:
            entrada["requiere_aprobacion_dominio"] = bool(
                meta.get("requiere_aprobacion_dominio")
            )
        else:
            entrada["requiere_aprobacion_dominio"] = bool(
                entrada.get("pide_evaluacion_engine")
            )
        registro[str(rel)] = entrada
    return registro

# ===============================================================
# FIN FUNCIONES PRIVADAS
# ===============================================================

# ===============================================================
# CAPACIDADES PÚBLICAS
# ===============================================================

def barrer() -> Dict[str, Any]:
    """
    Centinela RE: no-contradicción entre dominios y simbiosis.
    No calcula Tru. No aprueba material en nombre de un dominio.
    No deposita en Diagnóstico.
    """
    hallado = _descubrir()
    choques: List[str] = []
    errores: List[str] = []
    notas: List[str] = []
    dominios_con_simbiosis: List[str] = []

    for archivo, meta in sorted(hallado.items()):
        if "error" in meta:
            errores.append("{0}: {1}".format(archivo, meta["error"]))
            continue
        for clave in CLAVES_FUNCION:
            if not meta.get(clave):
                errores.append(
                    "{0}: FUNCION sin '{1}'".format(archivo, clave)
                )
        if meta.get("pide_evaluacion_engine"):
            dominios_con_simbiosis.append(meta.get("nombre") or archivo)
            if not meta.get("requiere_aprobacion_dominio", True):
                choques.append(
                    "{0}: pide_evaluacion_engine=True pero "
                    "requiere_aprobacion_dominio=False — "
                    "el material no puede subir solo por el cálculo".format(
                        archivo
                    )
                )

    por_nombre: Dict[str, List[str]] = {}
    for archivo, meta in sorted(hallado.items()):
        if "error" in meta:
            continue
        n = meta.get("nombre")
        if n:
            por_nombre.setdefault(str(n), []).append(archivo)
    for nombre, archivos in sorted(por_nombre.items()):
        if len(archivos) > 1:
            choques.append(
                "funcion '{0}' reclamada por {1}".format(nombre, archivos)
            )

    if not hallado:
        notas.append("ninguna funcion declarada todavía (vacío legítimo)")
    if dominios_con_simbiosis:
        notas.append(
            "simbiosis activa: {0}".format(
                sorted(set(dominios_con_simbiosis))
            )
        )

    return {
        "id": ID_MODULO,
        "contenedor": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "coherente": not (choques or errores),
        "choques": choques,
        "errores": errores,
        "funciones": sorted(por_nombre),
        "dominios_simbiosis": sorted(set(dominios_con_simbiosis)),
        "estados_material": list(ESTADOS_MATERIAL),
        "notas": notas,
    }


def verificar() -> Dict[str, Any]:
    """Alias de barrer — coherencia interna de RE."""
    return barrer()


def inventario(peticion: Any = None) -> Dict[str, Any]:
    """Qué existe en RE. No diagnostica el sistema completo."""
    hallado = _descubrir()
    b = barrer()
    return {
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "funciones": {
            m["nombre"]: m
            for m in hallado.values()
            if m.get("nombre") and "error" not in m
        },
        "coherente": b.get("coherente"),
        "dominios_simbiosis": b.get("dominios_simbiosis"),
        "acceso": {
            "canal": "acceso.Canal",
            "hay_requests": HAY_REQUESTS,
            "hay_acceso": hay_acceso(timeout=2),
        },
        "contrato_simbiosis": {
            "quien_calcula": "Engine bajo O declarado por el dominio",
            "quien_aprueba_material": "el dominio que pidió la evaluación",
            "quien_vela_modulo": "realidad.barrer (no-contradicción)",
            "material_sin_aprobacion": "no sube",
        },
        "funcion": CONTENEDOR.get("funcion"),
        "autoridad": CONTENEDOR.get("autoridad"),
        "conocimiento_exportable": CONTENEDOR.get("conocimiento_exportable"),
        "invariantes": CONTENEDOR.get("invariantes"),
    }


def registrar_resultado_dominio(
    nombre_dominio: str,
    material_id: str,
    resultado_engine: Dict[str, Any],
    aprobacion_dominio: bool,
) -> Dict[str, Any]:
    """
    Cierra el tramo de simbiosis para un material.
    RE no recalcula. Solo registra estado contractual.
    """
    if not nombre_dominio or not material_id:
        return {
            "ok": False,
            "id": ID_MODULO,
            "estado": "bloqueado_re",
            "error": "nombre_dominio y material_id son obligatorios",
        }
    if not isinstance(resultado_engine, dict):
        return {
            "ok": False,
            "id": ID_MODULO,
            "estado": "bloqueado_re",
            "error": "resultado_engine debe ser dict (salida de Engine)",
        }
    estado = "aprobado" if aprobacion_dominio else "rechazado"
    return {
        "ok": True,
        "id": ID_MODULO,
        "estado": estado,
        "nombre_dominio": nombre_dominio,
        "material_id": material_id,
        "aprobacion_dominio": bool(aprobacion_dominio),
        "resultado_engine_presente": True,
        "nota": (
            "Material {0} por dominio '{1}'. "
            "Sin aprobación del dominio el material no debe usarse arriba."
        ).format(estado, nombre_dominio),
    }


def verificar_salida(salida: Any) -> bool:
    if not isinstance(salida, dict):
        return False
    return (
        "coherente" in salida
        or "id" in salida
        or "estado" in salida
        or "ok" in salida
    )

# ===============================================================
# FIN CAPACIDADES PÚBLICAS
# ===============================================================

# ===============================================================
# REPORTING INTERNO
# ===============================================================

def reporte() -> Dict[str, Any]:
    """Estado actual de RE. No diagnostica el sistema."""
    b = barrer()
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "estado": (
            ESTADO_OPERATIVO if b.get("coherente") else ESTADO_DEGRADADO
        ),
        "coherente": b.get("coherente"),
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "funciones": b.get("funciones"),
        "dominios_simbiosis": b.get("dominios_simbiosis"),
        "autoridad": CONTENEDOR.get("autoridad"),
        "conocimiento_exportable": CONTENEDOR.get("conocimiento_exportable"),
    }


def diagnostico() -> Dict[str, Any]:
    """Problemas y advertencias propios de RE."""
    b = barrer()
    problemas = list(b.get("choques") or []) + list(b.get("errores") or [])
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "estado": (
            ESTADO_OPERATIVO if b.get("coherente") else ESTADO_DEGRADADO
        ),
        "problemas": problemas,
        "advertencias": list(b.get("notas") or []),
        "recomendaciones": [],
        "coherente": b.get("coherente"),
    }

# ===============================================================
# FIN REPORTING
# ===============================================================

# ===============================================================
# EXPORTACIONES + RESOLUCIÓN ESTRICTA
# ===============================================================

_CAP_MAP = {
    "verificar": verificar,
    "barrer": barrer,
    "inventario": inventario,
    "reporte": reporte,
    "diagnostico": diagnostico,
    "registrar_resultado_dominio": registrar_resultado_dominio,
    "verificar_salida": verificar_salida,
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
    "ESTADOS_MATERIAL",
    "Canal",
    "hay_acceso",
    "hay_dns",
    "HAY_REQUESTS",
    "verificar",
    "barrer",
    "inventario",
    "reporte",
    "diagnostico",
    "registrar_resultado_dominio",
    "verificar_salida",
    "ContratoInvalido",
]

# ===============================================================
# FIN EXPORTACIONES
# ===============================================================

# ===============================================================
# EXTENSIONES FUTURAS
# ===============================================================
#
# Capacidad nueva:
#   1. Implementar función
#   2. _CAP_MAP
#   3. CONTENEDOR["capacidades"]
#   4. CONTENEDOR["capacidades_meta"] 1:1
#   5. consultas_soportadas / conocimiento_exportable si aplica
#   6. VERSION_MODULO
#   7. _validar_contrato / _resolver_capacidades
#
# Dominio nuevo:
#   - *.py en este directorio o subcarpeta con FUNCION = {...}
#   - El init lo descubre; no listar por nombre
#
# Engine y Omega no requieren cambios de código para capacidades nuevas.
#
# ===============================================================
# FIN DEL MÓDULO
# ===============================================================
