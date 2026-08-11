# ===============================================================
# VPSI-TRUTH — modules/correlacion_mecanica/__init__.py
# ===============================================================
#
# MÓDULO:              correlacion_mecanica
# ID:                  MC
# Rol:                 MC
# Versión módulo:      1.3
# Versión contrato:    1.0
# Esquema contrato:    VPSI-CONTRACT-1.0
# Estabilidad:         ESTABLE
# Compatible desde:    1.0
# API Engine:          >=1.0
#
# Función:
#   Núcleo de correlación mecánica del sistema completo.
#   Contiene y expone todos los órdenes causales / mecánicos
#   declarados en sus archivos internos (cualquier .py con MECANICA).
#
# Qué hace:
#   - Lee absolutamente todos los archivos .py de la carpeta
#   - Recoge toda declaración MECANICA
#   - Calcula el orden resultante
#   - Detecta contradicciones de orden y ciclos
#   - Reporta estado, inventario y diagnóstico propios
#   - Notifica a DiagnosticoGlobal cuando hay choques o errores
#
# Qué NO hace:
#   - No calcula Tru_total ni Tru_Ri
#   - No clasifica entrada de usuario
#   - No orquesta el sistema (eso es Engine)
#   - No modifica otros módulos
#
# Responsabilidad:
#   Ser la fuente objetiva de los órdenes mecánicos del sistema
#   y de su coherencia causal.
#
# Autoridad:
#   - Exponer todos los órdenes mecánicos declarados
#   - Detectar choques, ciclos y errores de lectura
#   - Reportar estado, inventario y diagnóstico propios
#
# Conocimiento exportable:
#   mecanicas, orden, choques, ciclos, declaraciones,
#   inventario, estado, reporte, diagnóstico
#
# Relación con Engine:
#   Engine descubre este CONTENEDOR, ejecuta solo las capacidades
#   declaradas y consolida el reporte que este módulo produce.
#
# Relación con Omega:
#   Omega no calcula nada de MC. Solo presenta lo que Engine entrega.
#
# ===============================================================


# ===============================================================
# IMPORTACIONES
# ===============================================================

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

try:
    from core.diagnostico import DiagnosticoGlobal  # type: ignore
except Exception:  # noqa: BLE001
    DiagnosticoGlobal = None  # type: ignore

# ===============================================================
# FIN IMPORTACIONES
# ===============================================================


# ===============================================================
# CONSTANTES
# ===============================================================

ID_MODULO = "MC"
NOMBRE_MODULO = "correlacion_mecanica"
ROL_MODULO = "MC"

VERSION_MODULO = "1.3"
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

INVARIANTES = (
    "el id del módulo nunca cambia",
    "el rol nunca cambia",
    "las capacidades declaradas son siempre callables tras la resolución",
    "este módulo no modifica el estado de otros módulos",
    "este módulo no inventa mecánicas no declaradas en archivos",
    "este módulo siempre puede reportar su propio estado",
)

APROBADO = "APROBADO"
RECHAZADO = "RECHAZADO"

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
    pass


DECLARACIONES = [
    {
        "id": "CORR_SEQ_01",
        "tipo": "axioma",
        "sujeto": "mecanica_declarada",
        "relacion": "se_lee_en",
        "objeto": "orden_nativo",
        "polaridad": True,
        "enunciado": (
            "Principio de Secuencia Transversal: Los objetos de la carpeta "
            "se leen en su orden nativo para verificar que la transición "
            "entre estados cumpla la continuidad causal."
        ),
    },
    {
        "id": "CORR_SEQ_02",
        "tipo": "axioma",
        "sujeto": "colision_sobre_un_nodo",
        "relacion": "permite_el_paso",
        "objeto": "mecanica",
        "polaridad": False,
        "enunciado": (
            "Criterio de No Contradicción Cruzada: Si dos declaraciones de "
            "archivos distintos colisionan sobre el mismo nodo, el paso se "
            "bloquea y se reportan los identificadores en desacuerdo."
        ),
    },
]

# ===============================================================
# FIN DEFINICIONES
# ===============================================================
# ===============================================================
# CONTRATO OFICIAL DEL MÓDULO
# ===============================================================

CONTENEDOR: Dict[str, Any] = {
    # ============================================================
    # ESQUEMA
    # ============================================================
    "esquema": ESQUEMA_CONTRATO,
    "version_contrato": VERSION_CONTRATO,
    "version_modulo": VERSION_MODULO,
    "estabilidad": ESTABILIDAD,
    "compatible_desde": COMPATIBLE_DESDE,
    "api_engine": API_ENGINE,

    # ============================================================
    # IDENTIDAD
    # ============================================================
    "id": ID_MODULO,
    "nombre": NOMBRE_MODULO,
    "rol": ROL_MODULO,
    "descripcion": (
        "Núcleo de correlación mecánica del sistema completo. "
        "Contiene y expone todos los órdenes causales declarados "
        "en los archivos de esta carpeta mediante la variable MECANICA."
    ),

    # ============================================================
    # PROPÓSITO
    # ============================================================
    "funcion": (
        "Leer todos los archivos del módulo, recoger MECANICA, "
        "calcular orden resultante, detectar contradicciones o ciclos "
        "y reportar estado, inventario y diagnóstico."
    ),
    "no_hace": [
        "No calcula Tru_total ni Tru_Ri",
        "No clasifica entrada de usuario",
        "No orquesta el sistema (eso es Engine)",
        "No modifica otros módulos",
    ],

    # ============================================================
    # AUTORIDAD
    # ============================================================
    "autoridad": [
        "Exponer todos los órdenes mecánicos declarados en la carpeta",
        "Detectar choques de orden y ciclos",
        "Reportar estado, inventario y diagnóstico propios",
        "Notificar a DiagnosticoGlobal cuando hay choques o errores",
    ],

    # ============================================================
    # CONOCIMIENTO EXPORTABLE
    # ============================================================
    "conocimiento_exportable": [
        "mecanicas",
        "orden",
        "choques",
        "ciclos",
        "declaraciones",
        "inventario",
        "estado",
        "reporte",
        "diagnostico",
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

    # ============================================================
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
    },

    # ============================================================
    # CONSULTAS SOPORTADAS
    # ============================================================
    "consultas_soportadas": [
        "verificar_coherencia",
        "obtener_orden",
        "obtener_inventario",
        "obtener_reporte",
        "obtener_diagnostico",
        "listar_mecanicas",
        "listar_declaraciones",
    ],

    # ============================================================
    # CAPACIDADES
    # ============================================================
    "capacidades": {
        "verificar": "barrer",
        "barrer": "barrer",
        "evaluar": "barrer",
        "axiomas": "axiomas",
        "inventario": "inventario",
        "verificar_salida": "verificar_salida",
        "reporte": "reporte",
        "diagnostico": "diagnostico",
        "listar_mecanicas": "listar_mecanicas",
    },

    # ============================================================
    # METADATOS DE CAPACIDADES (1:1 OBLIGATORIO)
    # ============================================================
    "capacidades_meta": {
    "verificar": {
        "descripcion": "Alias de barrer. Verifica coherencia mecánica.",
        "entrada": "ninguna",
        "validar_esquema": ["*"],
        "salida": "dict con coherente, choques, errores, mecanica, archivos",
        "acceso_archivos": ["*"],
    },

    "barrer": {
        "descripcion": (
            "Lee todas las MECANICA de la carpeta, calcula orden, "
            "detecta contradicciones o ciclos y notifica a DiagnosticoGlobal."
        ),
        "entrada": "ninguna",
        "validar_esquema": ["*"],
        "salida": (
            "dict con estado, coherente, choques, errores, "
            "mecanica, archivos"
        ),
        "acceso_archivos": ["*"],
    },

    "evaluar": {
        "descripcion": "Alias de barrer. Evalúa coherencia del núcleo MC.",
        "entrada": "ninguna",
        "validar_esquema": ["*"],
        "salida": (
            "dict con estado, coherente, choques, errores, mecanica"
        ),
        "acceso_archivos": ["*"],
    },

    "axiomas": {
        "descripcion": (
            "Declaraciones internas de correlación "
            "(CORR_SEQ_01, CORR_SEQ_02)."
        ),
        "entrada": "ninguna",
        "validar_esquema": ["*"],
        "salida": "list[dict] de declaraciones",
        "acceso_archivos": ["*"],
    },

    "inventario": {
        "descripcion": "Inventario objetivo de mecánicas declaradas en la carpeta.",
        "entrada": "ninguna",
        "validar_esquema": ["*"],
        "salida": "dict con total_mecanicas, archivos, declaran",
        "acceso_archivos": ["*"],
    },

    "verificar_salida": {
        "descripcion": "Comprueba si una salida de barrer es coherente.",
        "entrada": "salida: dict",
        "validar_esquema": ["*"],
        "salida": "bool",
        "acceso_archivos": ["*"],
    },

    "reporte": {
        "descripcion": "Reporte interno de estado del módulo MC.",
        "entrada": "ninguna",
        "validar_esquema": ["*"],
        "salida": (
            "dict con estado, coherente, choques, errores, capacidades"
        ),
        "acceso_archivos": ["*"],
    },

    "diagnostico": {
        "descripcion": "Diagnóstico: qué falta, qué está mal en MC.",
        "entrada": "ninguna",
        "validar_esquema": ["*"],
        "salida": (
            "dict con estado, problemas, advertencias, recomendaciones"
        ),
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

        # --- BANDERAS OBLIGATORIAS SEGÚN ENGINE ---
        "acceso_archivos": True,      # ← AGREGADA
        "validar_esquema": True,      # ← AGREGADA
    },


    # ============================================================
    # ESTADOS VÁLIDOS
    # ============================================================
    "estados_validos": list(ESTADOS_VALIDOS),

    # ============================================================
    # INVARIANTES
    # ============================================================
    "invariantes": list(INVARIANTES),

}  # <--- CIERRE FINAL

# ===============================================================
# FIN CONTRATO
# ===============================================================
# ===============================================================
# FUNCIONES PRIVADAS
# ===============================================================

def _leer() -> Dict[str, Any]:
    """
    Recorre absolutamente todos los archivos .py de esta carpeta
    y recoge cualquier declaración MECANICA que encuentre.
    """
    hallado: Dict[str, Any] = {}
    for archivo in sorted(_DIR.glob("*.py")):
        if archivo.name.startswith("_") or archivo.name == "__init__.py":
            continue

        clave = f"mecanica_{archivo.stem}"
        spec = importlib.util.spec_from_file_location(clave, archivo)
        if spec is None or spec.loader is None:
            continue

        mod = importlib.util.module_from_spec(spec)
        sys.modules[clave] = mod
        try:
            spec.loader.exec_module(mod)
        except Exception:
            continue

        meta = getattr(mod, "MECANICA", None)
        if isinstance(meta, dict):
            hallado[archivo.name] = meta

    return hallado


def _nodos(meta: Dict[str, Any]) -> List[str]:
    orden = meta.get("orden", [])
    if isinstance(orden, (list, tuple)):
        return [str(x) for x in orden]
    return []


def _precedencias(nodos: List[str]) -> List[Tuple[str, str]]:
    return [(a, b) for i, a in enumerate(nodos) for b in nodos[i + 1:]]


def _informe(
    mecanica: List[str],
    choques: List[str],
    errores: List[str],
    hallado: Dict[str, Any],
) -> Dict[str, Any]:
    limpio = not (choques or errores)
    return {
        "contenedor": NOMBRE_MODULO,
        "estado": APROBADO if limpio else RECHAZADO,
        "coherente": limpio,
        "choques": choques,
        "errores": errores,
        "mecanica": mecanica if limpio else [],
        "archivos": sorted(hallado.keys()),
        "total_mecanicas": len(hallado),
    }


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
            f"{NOMBRE_MODULO}: CONTENEDOR incompleto. Faltan: {faltantes}"
        )
    if cont.get("esquema") != ESQUEMA_CONTRATO:
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: esquema incompatible: {cont.get('esquema')}"
        )
    if str(cont.get("version_contrato")) != VERSION_CONTRATO:
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: version_contrato inválida: {cont.get('version_contrato')}"
        )
    meta_caps = cont.get("capacidades_meta") or {}
    for nombre_cap in cont.get("capacidades") or {}:
        if nombre_cap not in meta_caps:
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: capacidad '{nombre_cap}' sin capacidades_meta"
            )
        entrada = meta_caps[nombre_cap]
        if not isinstance(entrada, dict):
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: capacidades_meta['{nombre_cap}'] debe ser dict"
            )
        for campo in ("descripcion", "entrada", "salida"):
            if campo not in entrada or not isinstance(entrada[campo], str):
                raise ContratoInvalido(
                    f"{NOMBRE_MODULO}: capacidades_meta['{nombre_cap}'] "
                    f"requiere '{campo}: str'"
                )

# ===============================================================
# FIN FUNCIONES PRIVADAS
# ===============================================================


# ===============================================================
# CAPACIDADES PÚBLICAS
# ===============================================================

def axiomas() -> List[Dict[str, Any]]:
    return list(DECLARACIONES)


def barrer() -> Dict[str, Any]:
    """
    Lee todas las MECANICA declaradas en la carpeta,
    calcula el orden resultante, detecta contradicciones o ciclos
    y notifica a DiagnosticoGlobal si hay problemas.
    """
    hallado = _leer()
    choques: List[str] = []
    errores: List[str] = []

    if not hallado:
        errores.append("ninguna mecánica declarada en la carpeta")
        informe = _informe([], choques, errores, hallado)
        _notificar_diagnostico(choques, errores)
        return informe

    precede: Dict[Tuple[str, str], List[str]] = {}

    for archivo, meta in sorted(hallado.items()):
        nodos = _nodos(meta)
        if len(nodos) < 2:
            errores.append(f"{archivo}: sin orden nativo legible")
            continue
        for a, b in _precedencias(nodos):
            precede.setdefault((a, b), []).append(archivo)

    for (a, b), quienes in sorted(precede.items()):
        contrarios = precede.get((b, a))
        if contrarios and (a, b) < (b, a):
            choques.append(
                f"nodo '{a}'/'{b}': {quienes} lo ponen en un orden y "
                f"{contrarios} en el contrario"
            )

    universo = {x for par in precede for x in par}
    pendientes = set(universo)
    mecanica: List[str] = []

    while pendientes:
        libres = sorted(
            n for n in pendientes
            if not any((o, n) in precede for o in pendientes if o != n)
        )
        if not libres:
            choques.append(
                f"nodos {sorted(pendientes)}: la secuencia se muerde la cola, "
                "no hay orden posible"
            )
            break
        mecanica.extend(libres)
        pendientes -= set(libres)

    informe = _informe(mecanica, choques, errores, hallado)
    _notificar_diagnostico(choques, errores)
    return informe


def _notificar_diagnostico(choques: List[str], errores: List[str]) -> None:
    if not (choques or errores):
        return
    if DiagnosticoGlobal is None:
        return
    try:
        DiagnosticoGlobal.recibir_reporte(
            modulo=NOMBRE_MODULO,
            errores=(
                [{"tipo": "choque", "detalle": c} for c in choques]
                + [{"tipo": "error", "detalle": e} for e in errores]
            ),
        )
    except Exception:  # noqa: BLE001
        pass


def inventario() -> Dict[str, Any]:
    hallado = _leer()
    return {
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "total_mecanicas": len(hallado),
        "archivos": sorted(hallado.keys()),
        "declaran": {
            archivo: {
                "nombre": meta.get("nombre", "Sin nombre"),
                "longitud_orden": len(meta.get("orden", [])),
            }
            for archivo, meta in sorted(hallado.items())
        },
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "invariantes": CONTENEDOR.get("invariantes"),
    }


def verificar_salida(salida: Dict[str, Any]) -> bool:
    return bool(salida.get("coherente", False))


def listar_mecanicas() -> Dict[str, Any]:
    return _leer()


def verificar() -> Dict[str, Any]:
    return barrer()

# ===============================================================
# FIN CAPACIDADES PÚBLICAS
# ===============================================================


# ===============================================================
# REPORTING INTERNO
# ===============================================================

def reporte() -> Dict[str, Any]:
    r = barrer()
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "estado": ESTADO_OPERATIVO if r.get("coherente") else ESTADO_DEGRADADO,
        "coherente": r.get("coherente"),
        "choques": r.get("choques"),
        "errores": r.get("errores"),
        "mecanica": r.get("mecanica"),
        "archivos": r.get("archivos"),
        "total_mecanicas": r.get("total_mecanicas"),
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "autoridad": CONTENEDOR.get("autoridad"),
        "conocimiento_exportable": CONTENEDOR.get("conocimiento_exportable"),
        "consultas_soportadas": CONTENEDOR.get("consultas_soportadas"),
    }


def diagnostico() -> Dict[str, Any]:
    r = barrer()
    problemas = []
    advertencias = []
    recomendaciones = []

    if r.get("errores"):
        problemas.append({"tipo": "errores_lectura", "detalle": r["errores"]})
        recomendaciones.append("Revisar archivos MECANICA con errores")

    if r.get("choques"):
        problemas.append({"tipo": "choques_orden", "detalle": r["choques"]})
        recomendaciones.append("Resolver contradicciones o ciclos de orden")

    if not r.get("total_mecanicas"):
        advertencias.append("Ninguna mecánica declarada en la carpeta")
        recomendaciones.append("Agregar archivos .py con variable MECANICA")

    estado = ESTADO_OPERATIVO if r.get("coherente") else ESTADO_DEGRADADO
    if not r.get("total_mecanicas") and not problemas:
        estado = ESTADO_NO_INICIADO

    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "estado": estado,
        "problemas": problemas,
        "advertencias": advertencias,
        "recomendaciones": recomendaciones,
        "coherente": r.get("coherente"),
        "choques_n": len(r.get("choques") or []),
        "errores_n": len(r.get("errores") or []),
        "total_mecanicas": r.get("total_mecanicas"),
    }

# ===============================================================
# FIN REPORTING
# ===============================================================


# ===============================================================
# VERIFICACIÓN / INVENTARIO
# ===============================================================

# verificar() e inventario() en CAPACIDADES PÚBLICAS

# ===============================================================
# FIN VERIFICACIÓN / INVENTARIO
# ===============================================================


# ===============================================================
# EXPORTACIONES + RESOLUCIÓN ESTRICTA
# ===============================================================

_CAP_MAP = {
    "barrer": barrer,
    "axiomas": axiomas,
    "inventario": inventario,
    "verificar_salida": verificar_salida,
    "reporte": reporte,
    "diagnostico": diagnostico,
    "listar_mecanicas": listar_mecanicas,
    "verificar": verificar,
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
                    f"{NOMBRE_MODULO}: capacidad '{nombre}' "
                    f"referencia inexistente: '{ref}'"
                )
            fn = _CAP_MAP[ref]
            if not callable(fn):
                raise ContratoInvalido(
                    f"{NOMBRE_MODULO}: '{ref}' no es callable"
                )
            resueltas[nombre] = fn
            continue
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: capacidad '{nombre}' "
            f"tiene tipo inválido: {type(ref).__name__}"
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
    "DECLARACIONES",
    "axiomas",
    "barrer",
    "inventario",
    "verificar_salida",
    "listar_mecanicas",
    "verificar",
    "reporte",
    "diagnostico",
    "APROBADO",
    "RECHAZADO",
    "ContratoInvalido",
]

# ===============================================================
# FIN EXPORTACIONES
# ===============================================================


# ===============================================================
# EXTENSIONES FUTURAS
# ===============================================================
#
# Toda capacidad nueva DEBE agregarse simultáneamente en:
#   1. capacidades
#   2. capacidades_meta  (descripcion, entrada, salida: str)
#   3. _CAP_MAP
#   4. VERSION_MODULO
#
# ===============================================================
# FIN EXTENSIONES FUTURAS
# ===============================================================


# ===============================================================
# FIN DEL MÓDULO
# ===============================================================
