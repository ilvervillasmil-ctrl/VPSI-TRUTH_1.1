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

import inspect
from typing import Any, Callable, Dict, List, Optional, Tuple

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
    # 5.7 — DEPENDENCIAS
    # ============================================================
    "requiere": [
    "CE", "AX", "FO", "SF",
    "CA", "CX", "DI", "RE", "VX",
    "TX", "CH", "CIT", "DGCO", "UI",
    "CC", "TT", "SC", "CT"
    ],

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
        "validar_esquema": True,
        "acceso_archivos": True,

        # --- BANDERAS NUEVAS (OBLIGATORIAS ENGINE) ---
        "ejecutar_total": True,
        "inspeccionar": True,
        "registrar_inventario": True,
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
        "ejecutar_total": "ejecutar_total",
        "inspeccionar": "inspeccionar",
        "registrar_inventario": "registrar_inventario",
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
            "descripcion": (
                "Inventario objetivo de mecánicas declaradas en la carpeta."
            ),
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
        "listar_mecanicas": {
            "descripcion": (
                "Lista todas las MECANICA descubiertas en la carpeta."
            ),
            "entrada": "ninguna",
            "validar_esquema": ["*"],
            "salida": "dict archivo → meta MECANICA",
            "acceso_archivos": ["*"],
        },
        "ejecutar_total": {
            "descripcion": (
                "Autoridad total de ENGINE sobre MC. "
                "Ejerce TODAS las unidades operativamente ejecutables "
                "del módulo conforme a su contrato e inventario. "
                "Todo es callable real. No inventa capacidades."
            ),
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["*"],
            "salida": "dict con resultados de todas las unidades ejecutadas",
            "acceso_archivos": ["*"],
        },
        "inspeccionar": {
            "descripcion": (
                "Capacidad meta de inspeccion estructural de MC. "
                "Expone constantes, capacidades, mecanicas y estado "
                "sin alterar el contrato ni calcular."
            ),
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["acceso_archivos"],
            "salida": "dict con estructura, capacidades y estado del modulo",
            "acceso_archivos": ["acceso_archivos"],
        },
        "registrar_inventario": {
            "descripcion": (
                "Registra el inventario estructural de MC "
                "como instantanea determinista. No altera evidencia."
            ),
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["acceso_archivos"],
            "salida": "dict con inventario registrado",
            "acceso_archivos": ["acceso_archivos"],
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
        "acceso_archivos": True,
        "validar_esquema": True,

        # --- BANDERAS NUEVAS (OBLIGATORIAS ENGINE) ---
        "ejecutar_total": True,
        "inspeccionar": True,
        "registrar_inventario": True,
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


# ===============================================================
# 1. LECTURA DE MECÁNICAS
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


# ===============================================================
# 2. RESOLUCIÓN DE NODOS
# ===============================================================

def _nodos(meta: Dict[str, Any]) -> List[str]:
    """
    Extrae el orden nativo declarado por una MECANICA.
    Una declaración sin orden legible no produce nodos.
    """
    if not isinstance(meta, dict):
        return []

    orden = meta.get("orden")

    if not isinstance(orden, (list, tuple)):
        return []

    return [str(nodo) for nodo in orden]


# ===============================================================
# 3. CONSTRUCCIÓN DE PRECEDENCIAS
# ===============================================================

def _precedencias(nodos: List[str]) -> List[Tuple[str, str]]:
    """
    Convierte un orden lineal de nodos en relaciones de precedencia.
    """
    return [
        (a, b)
        for i, a in enumerate(nodos)
        for b in nodos[i + 1:]
        if a != b
    ]


# ===============================================================
# 4. CONSTRUCCIÓN DE INFORME
# ===============================================================

def _informe(
    mecanica: List[str],
    choques: List[str],
    errores: List[str],
    hallado: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Construye el informe determinista de correlación mecánica.
    """
    limpio = not (choques or errores)

    return {
        "contenedor": NOMBRE_MODULO,
        "estado": APROBADO if limpio else RECHAZADO,
        "coherente": limpio,
        "choques": list(choques),
        "errores": list(errores),
        "mecanica": list(mecanica) if limpio else [],
        "archivos": sorted(hallado.keys()),
        "total_mecanicas": len(hallado),
    }


# ===============================================================
# 5. VALIDACIÓN ESTRUCTURAL DEL CONTRATO
# ===============================================================

def _validar_contrato(cont: Dict[str, Any]) -> None:
    """
    Valida la estructura del CONTENEDOR sin modificarlo,
    sin inventar campos y sin resolver capacidades.
    """
    if not isinstance(cont, dict):
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: CONTENEDOR debe ser dict"
        )

    obligatorias = (
        "esquema",
        "version_contrato",
        "version_modulo",
        "estabilidad",
        "compatible_desde",
        "api_engine",
        "id",
        "nombre",
        "rol",
        "descripcion",
        "funcion",
        "no_hace",
        "autoridad",
        "conocimiento_exportable",
        "acceso",
        "requiere",
        "acceso_archivos",
        "validar_esquema",
        "autoriza_engine",
        "consultas_soportadas",
        "capacidades",
        "capacidades_meta",
        "reporting",
        "estados_validos",
        "invariantes",
    )

    faltantes = [
        clave
        for clave in obligatorias
        if clave not in cont
    ]

    if faltantes:
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: CONTENEDOR incompleto. "
            f"Faltan: {faltantes}"
        )


# ===============================================================
# 6. VALIDACIÓN DE IDENTIDAD Y ESQUEMA
# ===============================================================

def _validar_identidad_contrato(cont: Dict[str, Any]) -> None:
    """
    Verifica que la identidad declarada corresponda al módulo.
    """
    if cont.get("esquema") != ESQUEMA_CONTRATO:
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: esquema incompatible: "
            f"{cont.get('esquema')}"
        )

    if str(cont.get("version_contrato")) != VERSION_CONTRATO:
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: version_contrato inválida: "
            f"{cont.get('version_contrato')}"
        )

    if cont.get("id") != ID_MODULO:
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: id contractual inválido: "
            f"{cont.get('id')}"
        )

    if cont.get("nombre") != NOMBRE_MODULO:
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: nombre contractual inválido: "
            f"{cont.get('nombre')}"
        )

    if cont.get("rol") != ROL_MODULO:
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: rol contractual inválido: "
            f"{cont.get('rol')}"
        )


# ===============================================================
# 7. VALIDACIÓN DE TIPOS CONTRACTUALES
# ===============================================================

def _validar_tipos_contrato(cont: Dict[str, Any]) -> None:
    """
    Verifica los tipos estructurales exigidos por el contrato.
    """
    campos_str = (
        "version_modulo",
        "estabilidad",
        "compatible_desde",
        "api_engine",
        "descripcion",
        "funcion",
    )

    for campo in campos_str:
        if not isinstance(cont.get(campo), str):
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: '{campo}' debe ser str"
            )

    campos_lista = (
        "no_hace",
        "autoridad",
        "conocimiento_exportable",
        "consultas_soportadas",
        "estados_validos",
        "invariantes",
    )

    for campo in campos_lista:
        if not isinstance(cont.get(campo), list):
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: '{campo}' debe ser list"
            )


# ===============================================================
# 8. VALIDACIÓN DE ACCESO CONTRACTUAL
# ===============================================================

def _validar_acceso_contrato(cont: Dict[str, Any]) -> None:
    """
    Verifica la estructura de acceso declarada por el módulo.
    """
    acceso = cont.get("acceso")

    if not isinstance(acceso, dict):
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: acceso debe ser dict"
        )

    if not isinstance(acceso.get("nivel"), str):
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: acceso.nivel debe ser str"
        )

    if not isinstance(acceso.get("descripcion"), str):
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: acceso.descripcion debe ser str"
        )

    acceso_archivos = cont.get("acceso_archivos")

    if not isinstance(acceso_archivos, list):
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: acceso_archivos debe ser list"
        )

    validar_esquema = cont.get("validar_esquema")

    if not isinstance(validar_esquema, list):
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: validar_esquema debe ser list"
        )


# ===============================================================
# 9. VALIDACIÓN DE BLOQUES CONTRACTUALES
# ===============================================================

def _validar_bloques_contrato(cont: Dict[str, Any]) -> None:
    """
    Verifica que los bloques contractuales principales existan
    con su estructura base.
    """
    autoriza_engine = cont.get("autoriza_engine")

    if not isinstance(autoriza_engine, dict):
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: autoriza_engine debe ser dict"
        )

    reporting = cont.get("reporting")

    if not isinstance(reporting, dict):
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: reporting debe ser dict"
        )

    capacidades = cont.get("capacidades")

    if not isinstance(capacidades, dict):
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: capacidades debe ser dict"
        )

    capacidades_meta = cont.get("capacidades_meta")

    if not isinstance(capacidades_meta, dict):
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: capacidades_meta debe ser dict"
        )


# ===============================================================
# 10. VALIDACIÓN 1:1 DE CAPACIDADES
# ===============================================================

def _validar_capacidades_meta(cont: Dict[str, Any]) -> None:
    """
    Garantiza correspondencia exacta 1:1 entre capacidades
    y capacidades_meta.
    """
    capacidades = cont["capacidades"]
    capacidades_meta = cont["capacidades_meta"]

    nombres_capacidades = set(capacidades.keys())
    nombres_meta = set(capacidades_meta.keys())

    faltantes = sorted(
        nombres_capacidades - nombres_meta
    )

    sobrantes = sorted(
        nombres_meta - nombres_capacidades
    )

    if faltantes:
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: capacidades sin capacidades_meta: "
            f"{faltantes}"
        )

    if sobrantes:
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: capacidades_meta sin capacidad declarada: "
            f"{sobrantes}"
        )


# ===============================================================
# 11. VALIDACIÓN DE REFERENCIAS DE CAPACIDADES
# ===============================================================

def _validar_referencias_capacidades(cont: Dict[str, Any]) -> None:
    """
    Verifica que cada capacidad posea una referencia resoluble
    como str o callable. La resolución efectiva corresponde a
    _resolver_capacidades().
    """
    for nombre, referencia in cont["capacidades"].items():
        if not isinstance(nombre, str) or not nombre.strip():
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: identificador de capacidad inválido"
            )

        if not isinstance(referencia, str) and not callable(referencia):
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: capacidad '{nombre}' "
                f"debe contener referencia str o callable"
            )


# ===============================================================
# 12. VALIDACIÓN DE METADATOS DE CAPACIDADES
# ===============================================================

def _validar_metadatos_capacidades(cont: Dict[str, Any]) -> None:
    """
    Verifica la estructura mínima determinista de cada metadata.
    """
    for nombre in sorted(cont["capacidades"]):
        meta = cont["capacidades_meta"][nombre]

        if not isinstance(meta, dict):
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: capacidades_meta['{nombre}'] "
                f"debe ser dict"
            )

        for campo in (
            "descripcion",
            "entrada",
            "salida",
        ):
            if campo not in meta:
                raise ContratoInvalido(
                    f"{NOMBRE_MODULO}: capacidades_meta['{nombre}'] "
                    f"requiere '{campo}'"
                )

            if not isinstance(meta[campo], str):
                raise ContratoInvalido(
                    f"{NOMBRE_MODULO}: capacidades_meta['{nombre}'] "
                    f"'{campo}' debe ser str"
                )

        if "validar_esquema" not in meta:
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: capacidades_meta['{nombre}'] "
                f"requiere 'validar_esquema'"
            )

        if not isinstance(meta["validar_esquema"], list):
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: capacidades_meta['{nombre}'] "
                f"'validar_esquema' debe ser list"
            )

        if "acceso_archivos" not in meta:
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: capacidades_meta['{nombre}'] "
                f"requiere 'acceso_archivos'"
            )

        if not isinstance(meta["acceso_archivos"], list):
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: capacidades_meta['{nombre}'] "
                f"'acceso_archivos' debe ser list"
            )


# ===============================================================
# 13. VALIDACIÓN CONTRACTUAL COMPLETA
# ===============================================================

def _validar_contrato_completo(cont: Dict[str, Any]) -> None:
    """
    Ejecuta todas las validaciones estructurales en orden determinista.
    No modifica el CONTENEDOR.
    """
    _validar_contrato(cont)
    _validar_identidad_contrato(cont)
    _validar_tipos_contrato(cont)
    _validar_acceso_contrato(cont)
    _validar_bloques_contrato(cont)
    _validar_capacidades_meta(cont)
    _validar_referencias_capacidades(cont)
    _validar_metadatos_capacidades(cont)


# ===============================================================
# FIN FUNCIONES PRIVADAS
# ===============================================================

# ===============================================================
# FUNCIONES PRIVADAS
# ===============================================================


# ===============================================================
# 1. LECTURA DETERMINISTA DE MECÁNICAS
# ===============================================================

def _leer() -> Dict[str, Any]:
    """
    Recorre determinísticamente todos los archivos .py de esta carpeta,
    excluye los archivos no declarativos y recoge únicamente MECANICA
    cuando su valor es un dict válido.
    """
    hallado: Dict[str, Any] = {}

    for archivo in sorted(_DIR.glob("*.py"), key=lambda p: p.name):
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


# ===============================================================
# 2. RESOLUCIÓN DETERMINISTA DE NODOS
# ===============================================================

def _nodos(meta: Dict[str, Any]) -> List[str]:
    """
    Extrae exclusivamente el orden nativo declarado por MECANICA.
    Una MECANICA sin orden iterable no produce nodos.
    """
    if not isinstance(meta, dict):
        return []

    orden = meta.get("orden")

    if not isinstance(orden, (list, tuple)):
        return []

    return [str(nodo) for nodo in orden]


# ===============================================================
# 3. CONSTRUCCIÓN DETERMINISTA DE PRECEDENCIAS
# ===============================================================

def _precedencias(nodos: List[str]) -> List[Tuple[str, str]]:
    """
    Convierte un orden lineal de nodos en relaciones de precedencia
    manteniendo exclusivamente pares distintos y su orden declarado.
    """
    return [
        (a, b)
        for i, a in enumerate(nodos)
        for b in nodos[i + 1:]
        if a != b
    ]


# ===============================================================
# 4. CONSTRUCCIÓN DETERMINISTA DEL INFORME
# ===============================================================

def _informe(
    mecanica: List[str],
    choques: List[str],
    errores: List[str],
    hallado: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Construye el informe sin modificar ninguna entrada.
    """
    choques_final = list(choques)
    errores_final = list(errores)
    limpio = not (choques_final or errores_final)

    return {
        "contenedor": NOMBRE_MODULO,
        "estado": APROBADO if limpio else RECHAZADO,
        "coherente": limpio,
        "choques": choques_final,
        "errores": errores_final,
        "mecanica": list(mecanica) if limpio else [],
        "archivos": sorted(hallado.keys()),
        "total_mecanicas": len(hallado),
    }


# ===============================================================
# 5. VALIDACIÓN DE ESTRUCTURA BASE DEL CONTRATO
# ===============================================================

def _validar_contrato(cont: Dict[str, Any]) -> None:
    """
    Verifica que CONTENEDOR exista como dict y contenga exactamente
    los bloques contractuales requeridos por este módulo.
    No resuelve capacidades ni modifica el contrato.
    """
    if not isinstance(cont, dict):
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: CONTENEDOR debe ser dict"
        )

    obligatorias = (
        "esquema",
        "version_contrato",
        "version_modulo",
        "estabilidad",
        "compatible_desde",
        "api_engine",
        "id",
        "nombre",
        "rol",
        "descripcion",
        "funcion",
        "no_hace",
        "autoridad",
        "conocimiento_exportable",
        "acceso",
        "requiere",
        "acceso_archivos",
        "validar_esquema",
        "autoriza_engine",
        "consultas_soportadas",
        "capacidades",
        "capacidades_meta",
        "reporting",
        "estados_validos",
        "invariantes",
    )

    faltantes = [
        clave
        for clave in obligatorias
        if clave not in cont
    ]

    if faltantes:
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: CONTENEDOR incompleto. "
            f"Faltan: {faltantes}"
        )


# ===============================================================
# 6. VALIDACIÓN DE IDENTIDAD CONTRACTUAL
# ===============================================================

def _validar_identidad_contrato(cont: Dict[str, Any]) -> None:
    """
    Verifica que los identificadores contractuales correspondan
    exclusivamente a las constantes declaradas por este módulo.
    """
    if cont.get("esquema") != ESQUEMA_CONTRATO:
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: esquema incompatible: "
            f"{cont.get('esquema')}"
        )

    if str(cont.get("version_contrato")) != VERSION_CONTRATO:
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: version_contrato inválida: "
            f"{cont.get('version_contrato')}"
        )

    if cont.get("id") != ID_MODULO:
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: id contractual inválido: "
            f"{cont.get('id')}"
        )

    if cont.get("nombre") != NOMBRE_MODULO:
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: nombre contractual inválido: "
            f"{cont.get('nombre')}"
        )

    if cont.get("rol") != ROL_MODULO:
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: rol contractual inválido: "
            f"{cont.get('rol')}"
        )


# ===============================================================
# 7. VALIDACIÓN DE TIPOS CONTRACTUALES
# ===============================================================

def _validar_tipos_contrato(cont: Dict[str, Any]) -> None:
    """
    Verifica los tipos estructurales mínimos del contrato.
    """
    campos_str = (
        "version_modulo",
        "estabilidad",
        "compatible_desde",
        "api_engine",
        "descripcion",
        "funcion",
    )

    for campo in campos_str:
        if not isinstance(cont.get(campo), str):
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: '{campo}' debe ser str"
            )

    campos_lista = (
        "no_hace",
        "autoridad",
        "conocimiento_exportable",
        "consultas_soportadas",
        "estados_validos",
        "invariantes",
        "requiere",
        "acceso_archivos",
        "validar_esquema",
    )

    for campo in campos_lista:
        if not isinstance(cont.get(campo), list):
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: '{campo}' debe ser list"
            )


# ===============================================================
# 8. VALIDACIÓN DE ACCESO CONTRACTUAL
# ===============================================================

def _validar_acceso_contrato(cont: Dict[str, Any]) -> None:
    """
    Verifica los bloques de acceso sin reinterpretar sus permisos.
    """
    acceso = cont.get("acceso")

    if not isinstance(acceso, dict):
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: acceso debe ser dict"
        )

    if not isinstance(acceso.get("nivel"), str):
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: acceso.nivel debe ser str"
        )

    if not isinstance(acceso.get("descripcion"), str):
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: acceso.descripcion debe ser str"
        )


# ===============================================================
# 9. VALIDACIÓN DE BLOQUES CONTRACTUALES
# ===============================================================

def _validar_bloques_contrato(cont: Dict[str, Any]) -> None:
    """
    Verifica que los bloques operativos principales posean
    el tipo estructural requerido.
    """
    bloques_dict = (
        "autoriza_engine",
        "reporting",
        "capacidades",
        "capacidades_meta",
    )

    for bloque in bloques_dict:
        if not isinstance(cont.get(bloque), dict):
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: '{bloque}' debe ser dict"
            )


# ===============================================================
# 10. VALIDACIÓN EXACTA 1:1 DE CAPACIDADES
# ===============================================================

def _validar_capacidades_meta(cont: Dict[str, Any]) -> None:
    """
    Garantiza correspondencia exacta 1:1 entre capacidades declaradas
    y sus metadatos. No permite faltantes ni sobrantes.
    """
    capacidades = cont["capacidades"]
    capacidades_meta = cont["capacidades_meta"]

    nombres_capacidades = set(capacidades.keys())
    nombres_meta = set(capacidades_meta.keys())

    faltantes = sorted(
        nombres_capacidades - nombres_meta
    )

    sobrantes = sorted(
        nombres_meta - nombres_capacidades
    )

    if faltantes:
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: capacidades sin capacidades_meta: "
            f"{faltantes}"
        )

    if sobrantes:
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: capacidades_meta sin capacidad declarada: "
            f"{sobrantes}"
        )


# ===============================================================
# 11. VALIDACIÓN DE IDENTIFICADORES DE CAPACIDADES
# ===============================================================

def _validar_identificadores_capacidades(
    cont: Dict[str, Any],
) -> None:
    """
    Verifica que cada identificador de capacidad sea una cadena
    no vacía y determinista.
    """
    for nombre in cont["capacidades"]:
        if not isinstance(nombre, str) or not nombre.strip():
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: identificador de capacidad inválido"
            )


# ===============================================================
# 12. VALIDACIÓN DE REFERENCIAS CALLABLE
# ===============================================================

def _validar_referencias_capacidades(
    cont: Dict[str, Any],
) -> None:
    """
    Verifica que cada capacidad tenga una referencia válida.
    Una referencia callable debe ser realmente callable.
    Una referencia str debe ser no vacía y deberá resolverse
    posteriormente mediante _resolver_capacidades().
    """
    for nombre, referencia in cont["capacidades"].items():
        if not isinstance(referencia, str) and not callable(referencia):
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: capacidad '{nombre}' "
                f"debe contener referencia str o callable"
            )

        if isinstance(referencia, str) and not referencia.strip():
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: capacidad '{nombre}' "
                f"contiene referencia str vacía"
            )


# ===============================================================
# 13. VALIDACIÓN DE METADATOS DE CAPACIDADES
# ===============================================================

def _validar_metadatos_capacidades(
    cont: Dict[str, Any],
) -> None:
    """
    Verifica la estructura completa de metadata de cada capacidad.
    Cada capacidad debe declarar descripción, entrada, salida,
    validar_esquema y acceso_archivos.
    """
    for nombre in sorted(cont["capacidades"]):
        meta = cont["capacidades_meta"][nombre]

        if not isinstance(meta, dict):
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: capacidades_meta['{nombre}'] "
                f"debe ser dict"
            )

        campos_str = (
            "descripcion",
            "entrada",
            "salida",
        )

        for campo in campos_str:
            if campo not in meta:
                raise ContratoInvalido(
                    f"{NOMBRE_MODULO}: capacidades_meta['{nombre}'] "
                    f"requiere '{campo}'"
                )

            if not isinstance(meta[campo], str):
                raise ContratoInvalido(
                    f"{NOMBRE_MODULO}: capacidades_meta['{nombre}'] "
                    f"'{campo}' debe ser str"
                )

        if "validar_esquema" not in meta:
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: capacidades_meta['{nombre}'] "
                f"requiere 'validar_esquema'"
            )

        if not isinstance(meta["validar_esquema"], list):
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: capacidades_meta['{nombre}'] "
                f"'validar_esquema' debe ser list"
            )

        if "acceso_archivos" not in meta:
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: capacidades_meta['{nombre}'] "
                f"requiere 'acceso_archivos'"
            )

        if not isinstance(meta["acceso_archivos"], list):
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: capacidades_meta['{nombre}'] "
                f"'acceso_archivos' debe ser list"
            )


# ===============================================================
# 14. VALIDACIÓN DE PERMISOS DEL ENGINE
# ===============================================================

def _validar_autorizacion_engine(
    cont: Dict[str, Any],
) -> None:
    """
    Verifica que las autorizaciones declaradas para Engine sean
    booleanas. No agrega, elimina ni interpreta permisos.
    """
    autoriza_engine = cont["autoriza_engine"]

    for permiso, valor in autoriza_engine.items():
        if not isinstance(permiso, str) or not permiso.strip():
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: identificador de permiso inválido"
            )

        if not isinstance(valor, bool):
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: permiso Engine '{permiso}' "
                f"debe ser bool"
            )


# ===============================================================
# 15. VALIDACIÓN DE REPORTING
# ===============================================================

def _validar_reporting(
    cont: Dict[str, Any],
) -> None:
    """
    Verifica que todas las banderas declaradas en reporting
    sean booleanas y posean identificadores válidos.
    """
    reporting = cont["reporting"]

    for nombre, valor in reporting.items():
        if not isinstance(nombre, str) or not nombre.strip():
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: identificador reporting inválido"
            )

        if not isinstance(valor, bool):
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: reporting['{nombre}'] "
                f"debe ser bool"
            )


# ===============================================================
# 16. VALIDACIÓN CONTRACTUAL COMPLETA
# ===============================================================

def _validar_contrato_completo(
    cont: Dict[str, Any],
) -> None:
    """
    Ejecuta todas las validaciones estructurales en orden fijo.
    No modifica CONTENEDOR, no resuelve capacidades y no introduce
    ninguna premisa externa al contrato.
    """
    _validar_contrato(cont)
    _validar_identidad_contrato(cont)
    _validar_tipos_contrato(cont)
    _validar_acceso_contrato(cont)
    _validar_bloques_contrato(cont)
    _validar_capacidades_meta(cont)
    _validar_identificadores_capacidades(cont)
    _validar_referencias_capacidades(cont)
    _validar_metadatos_capacidades(cont)
    _validar_autorizacion_engine(cont)
    _validar_reporting(cont)


# ===============================================================
# FIN FUNCIONES PRIVADAS
# ===============================================================

# ===============================================================
# CAPACIDADES PÚBLICAS — CORRELACIÓN MECÁNICA (MC)
# ===============================================================
# Todas son funciones reales y callables.
# Todas operan sobre el contenido real del módulo.
# Ninguna inventa mecánicas.
# Ninguna modifica archivos.
# Ninguna modifica otros módulos.
# La ejecución total se resuelve desde CONTENEDOR["capacidades"].
# ===============================================================


# ===============================================================
# 16. BARRER
# ===============================================================

def barrer() -> Dict[str, Any]:
    """
    Ejecuta el barrido determinista completo del módulo.

    Descubre todas las MECANICA declaradas en los archivos del módulo,
    valida su estructura, extrae sus órdenes nativos, construye las
    precedencias globales, detecta contradicciones y ciclos, resuelve
    el orden mecánico y construye el mapa causal global a partir de
    los documentos realmente descubiertos.

    El barrido no modifica evidencia, archivos, declaraciones ni otros
    módulos. No notifica a DiagnosticoGlobal ni comunica directamente
    con DGCO. Engine consume el informe resultante.
    """

    # -----------------------------------------------------------
    # 1. DESCUBRIMIENTO COMPLETO
    # -----------------------------------------------------------
    hallado = _leer()

    choques: List[str] = []
    errores: List[str] = []

    precede: Dict[Tuple[str, str], List[str]] = {}

    if not hallado:
        errores.append(
            f"{NOMBRE_MODULO}: no se encontró ninguna declaración "
            "MECANICA válida en el contenido del módulo"
        )

        return _informe(
            mecanica=[],
            choques=choques,
            errores=errores,
            hallado=hallado,
        )

    # -----------------------------------------------------------
    # 2. VALIDACIÓN Y EXTRACCIÓN DE NODOS
    # -----------------------------------------------------------
    por_archivo: Dict[str, List[str]] = {}

    for archivo, meta in sorted(hallado.items()):

        if not isinstance(meta, dict):
            errores.append(
                f"{archivo}: MECANICA debe ser dict"
            )
            continue

        nodos = _nodos(meta)

        if not nodos:
            errores.append(
                f"{archivo}: MECANICA sin orden nativo legible"
            )
            continue

        nodos_vistos: set[str] = set()

        for posicion, nodo in enumerate(nodos):

            nodo = str(nodo)

            if not nodo.strip():
                errores.append(
                    f"{archivo}: nodo vacío en posición {posicion}"
                )
                continue

            if nodo in nodos_vistos:
                errores.append(
                    f"{archivo}: nodo duplicado en orden nativo: "
                    f"'{nodo}'"
                )
                continue

            nodos_vistos.add(nodo)

        if len(nodos_vistos) != len(nodos):
            continue

        por_archivo[archivo] = nodos

    # -----------------------------------------------------------
    # 3. PRECEDENCIAS GLOBALES
    # -----------------------------------------------------------
    for archivo, nodos in sorted(por_archivo.items()):

        relaciones = _precedencias(nodos)

        for relacion in relaciones:
            precede.setdefault(relacion, []).append(archivo)

    for relacion in sorted(precede):
        precede[relacion] = sorted(
            set(precede[relacion])
        )

    # -----------------------------------------------------------
    # 4. CONTRADICCIONES
    # -----------------------------------------------------------
    contradicciones_vistas: set[Tuple[str, str]] = set()

    for a, b in sorted(precede):

        inversa = (b, a)

        if inversa not in precede:
            continue

        par = tuple(sorted((a, b)))

        if par in contradicciones_vistas:
            continue

        contradicciones_vistas.add(par)

        origen_directo = precede[(a, b)]
        origen_inverso = precede[(b, a)]

        choques.append(
            f"nodo '{a}'/'{b}': "
            f"{origen_directo} establece '{a}' antes de '{b}', "
            f"mientras {origen_inverso} establece "
            f"'{b}' antes de '{a}'"
        )

    # -----------------------------------------------------------
    # 5. CONSTRUCCIÓN DEL ORDEN MECÁNICO
    # -----------------------------------------------------------
    universo: set[str] = set()

    for a, b in precede:
        universo.add(a)
        universo.add(b)

    pendientes = set(universo)
    mecanica: List[str] = []

    while pendientes:

        libres = sorted(
            nodo
            for nodo in pendientes
            if not any(
                (origen, nodo) in precede
                for origen in pendientes
                if origen != nodo
            )
        )

        if not libres:

            ciclo = sorted(pendientes)

            choques.append(
                f"nodos {ciclo}: "
                "la secuencia contiene un ciclo de precedencia; "
                "no existe orden mecánico válido"
            )

            mecanica = []
            pendientes.clear()
            break

        mecanica.extend(libres)
        pendientes.difference_update(libres)

    # -----------------------------------------------------------
    # 6. BARRIDO CAUSAL PROFUNDO
    # -----------------------------------------------------------
    #
    # El mapa causal se construye exclusivamente sobre la evidencia
    # documental ya descubierta. No crea nodos, IDs ni relaciones
    # externas a lo declarado por el módulo.
    #
    # La información disponible para esta capa es:
    #
    #   hallado
    #   por_archivo
    #   precede
    #   mecanica
    #
    # Por tanto, esta sección debe utilizar únicamente las estructuras
    # y declaraciones que el módulo ya expone.
    #
    # -----------------------------------------------------------

    causal: Dict[str, Any] = {
        "archivos": sorted(por_archivo),
        "nodos": sorted(universo),
        "precedencias": {
            f"{a}->{b}": sorted(origenes)
            for (a, b), origenes in sorted(precede.items())
        },
        "orden": list(mecanica),
    }

    # -----------------------------------------------------------
    # 7. GRADO CAUSAL
    # -----------------------------------------------------------
    grado: Dict[str, Dict[str, Any]] = {}

    for nodo in sorted(universo):

        entrantes = sorted(
            origen
            for origen, destino in precede
            if destino == nodo
        )

        salientes = sorted(
            destino
            for origen, destino in precede
            if origen == nodo
        )

        grado[nodo] = {
            "entrantes": entrantes,
            "salientes": salientes,
            "grado_entrante": len(entrantes),
            "grado_saliente": len(salientes),
            "grado_total": len(
                set(entrantes) | set(salientes)
            ),
        }

    causal["grado"] = grado

    # -----------------------------------------------------------
    # 8. INFORME DETERMINISTA
    # -----------------------------------------------------------
    informe = _informe(
        mecanica=mecanica,
        choques=choques,
        errores=errores,
        hallado=hallado,
    )

    if isinstance(informe, dict):
        informe["causal"] = causal

    return informe

# ===============================================================
# FIN BARRER
# ===============================================================

# ===============================================================
# 17. AXIOMAS
# ===============================================================

def axiomas() -> List[Dict[str, Any]]:
    """
    Expone las declaraciones axiomáticas internas de MC.
    No filtra, modifica ni interpreta las declaraciones.
    """
    return list(DECLARACIONES)


# ===============================================================
# 18. LISTAR MECÁNICAS
# ===============================================================

def listar_mecanicas() -> Dict[str, Any]:
    """
    Expone todas las MECANICA descubiertas en el contenido real
    del módulo.
    """
    hallado = _leer()

    return {
        archivo: dict(meta) if isinstance(meta, dict) else meta
        for archivo, meta in sorted(hallado.items())
    }


# ===============================================================
# 19. INVENTARIO
# ===============================================================

def inventario(
    peticion: Any = None,
) -> Dict[str, Any]:
    """
    Construye una instantánea determinista del inventario mecánico
    y contractual del módulo.
    """
    hallado = _leer()
    resultado = barrer()

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
                "nombre": (
                    meta.get("nombre")
                    if isinstance(meta, dict)
                    else None
                ),
                "version": (
                    meta.get("version")
                    if isinstance(meta, dict)
                    else None
                ),
                "n_nodos": (
                    len(_nodos(meta))
                    if isinstance(meta, dict)
                    else 0
                ),
            }
            for archivo, meta in sorted(hallado.items())
        },
        "coherente": resultado.get("coherente"),
        "choques": resultado.get("choques"),
        "errores": resultado.get("errores"),
        "mecanica": resultado.get("mecanica"),
        "capacidades": list(
            CONTENEDOR.get("capacidades", {}).keys()
        ),
        "requiere": list(
            CONTENEDOR.get("requiere") or []
        ),
        "invariantes": CONTENEDOR.get("invariantes"),
        "declaraciones_n": len(DECLARACIONES),
    }


# ===============================================================
# 20. VERIFICAR SALIDA
# ===============================================================

def verificar_salida(
    salida: Dict[str, Any],
) -> bool:
    """
    Verifica la forma estructural mínima de una salida de barrer().
    No interpreta semánticamente sus contenidos.
    """
    if not isinstance(salida, dict):
        return False

    campos_bool = ("coherente",)

    for campo in campos_bool:
        if campo not in salida:
            return False

        if not isinstance(salida[campo], bool):
            return False

    campos_str = (
        "contenedor",
        "estado",
    )

    for campo in campos_str:
        if campo in salida and not isinstance(
            salida[campo],
            str,
        ):
            return False

    campos_lista = (
        "choques",
        "errores",
        "mecanica",
        "archivos",
    )

    for campo in campos_lista:
        if campo in salida and not isinstance(
            salida[campo],
            list,
        ):
            return False

    if "total_mecanicas" in salida:
        if not isinstance(
            salida["total_mecanicas"],
            int,
        ):
            return False

        if salida["total_mecanicas"] < 0:
            return False

    return True


# ===============================================================
# 21. REPORTE
# ===============================================================

def reporte() -> Dict[str, Any]:
    """
    Produce una única instantánea determinista del estado operativo
    y contractual de MC.
    """
    resultado = barrer()

    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "estado": (
            ESTADO_OPERATIVO
            if resultado.get("coherente")
            else ESTADO_DEGRADADO
        ),
        "coherente": resultado.get("coherente"),
        "choques": resultado.get("choques"),
        "errores": resultado.get("errores"),
        "mecanica": resultado.get("mecanica"),
        "archivos": resultado.get("archivos"),
        "total_mecanicas": resultado.get(
            "total_mecanicas"
        ),
        "capacidades": list(
            CONTENEDOR.get("capacidades", {}).keys()
        ),
        "requiere": list(
            CONTENEDOR.get("requiere") or []
        ),
        "autoridad": CONTENEDOR.get("autoridad"),
        "conocimiento_exportable": CONTENEDOR.get(
            "conocimiento_exportable"
        ),
        "consultas_soportadas": CONTENEDOR.get(
            "consultas_soportadas"
        ),
    }


# ===============================================================
# 22. DIAGNÓSTICO
# ===============================================================

def diagnostico() -> Dict[str, Any]:
    """
    Construye el diagnóstico estructural de MC a partir del resultado
    determinista de barrer().
    """
    resultado = barrer()

    problemas: List[Dict[str, Any]] = []
    advertencias: List[str] = []
    recomendaciones: List[str] = []

    errores = resultado.get("errores") or []
    choques = resultado.get("choques") or []

    if errores:
        problemas.append({
            "tipo": "errores_lectura",
            "detalle": list(errores),
        })

        recomendaciones.append(
            "Revisar las declaraciones MECANICA que presentan "
            "errores estructurales o de carga"
        )

    if choques:
        problemas.append({
            "tipo": "choques_orden",
            "detalle": list(choques),
        })

        recomendaciones.append(
            "Resolver contradicciones o ciclos de precedencia "
            "entre las mecánicas declaradas"
        )

    total = resultado.get("total_mecanicas", 0)

    if not total:
        advertencias.append(
            "Ninguna mecánica declarada en el contenido del módulo"
        )

        recomendaciones.append(
            "Agregar declaraciones MECANICA válidas al módulo"
        )

    if resultado.get("coherente"):
        estado = ESTADO_OPERATIVO
    else:
        estado = ESTADO_DEGRADADO

    if not total and not problemas:
        estado = ESTADO_NO_INICIADO

    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "estado": estado,
        "problemas": problemas,
        "advertencias": advertencias,
        "recomendaciones": recomendaciones,
        "coherente": resultado.get("coherente"),
        "choques_n": len(choques),
        "errores_n": len(errores),
        "total_mecanicas": total,
    }


# ===============================================================
# 23. RESOLUCIÓN REAL DE CAPACIDADES
# ===============================================================

def _resolver_capacidad(
    nombre: str,
    referencia: Any,
) -> Callable[..., Any]:
    """
    Resuelve una capacidad contractual hasta una función callable real.

    Una capacidad puede estar declarada mediante una referencia callable
    directa o mediante el nombre de una función existente en este módulo.

    No crea funciones ni sustituye referencias inexistentes.
    """
    if callable(referencia):
        return referencia

    if isinstance(referencia, str):
        funcion = globals().get(referencia)

        if callable(funcion):
            return funcion

    raise ContratoInvalido(
        f"{NOMBRE_MODULO}: capacidad '{nombre}' "
        "no resuelve a una función callable real"
    )


# ===============================================================
# 24. EJECUCIÓN REAL DE UNA CAPACIDAD
# ===============================================================

def _ejecutar_capacidad(
    nombre: str,
    referencia: Any,
    peticion: Any,
) -> Any:
    """
    Ejecuta una capacidad contractual real.

    La firma de la función determina de forma determinista si acepta
    una petición explícita o si debe ejecutarse sin argumentos.

    Una capacidad con parámetros obligatorios distintos de una única
    petición no es ejecutable mediante la interfaz contractual y
    produce error en lugar de recibir argumentos inventados.
    """
    funcion = _resolver_capacidad(
        nombre=nombre,
        referencia=referencia,
    )

    firma = inspect.signature(funcion)

    parametros = list(
        firma.parameters.values()
    )

    obligatorios = [
        parametro
        for parametro in parametros
        if parametro.kind
        in (
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
        )
        and parametro.default
        is inspect.Parameter.empty
    ]

    if not obligatorios:
        return funcion()

    if len(obligatorios) == 1 and len(parametros) == 1:
        return funcion(peticion)

    raise ContratoInvalido(
        f"{NOMBRE_MODULO}: capacidad '{nombre}' "
        "no posee una firma compatible con la interfaz contractual"
    )


# ===============================================================
# 25. EJECUTAR TOTAL
# ===============================================================

def ejecutar_total(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Ejecuta todas las capacidades declaradas en el contrato de MC.

    La autoridad no mantiene una lista manual de capacidades.
    La fuente única de verdad es:

        CONTENEDOR["capacidades"]

    Cada entrada debe resolver a una función callable real.

    Una falla de una capacidad no impide intentar las restantes.
    Ninguna capacidad inexistente se inventa o sustituye.
    """
    peticion_normalizada = (
        dict(peticion)
        if isinstance(peticion, dict)
        else {}
    )

    resultados: Dict[str, Any] = {}
    errores_ejecucion: List[str] = []

    capacidades = CONTENEDOR.get(
        "capacidades",
        {},
    )

    if not isinstance(capacidades, dict):
        return {
            "id": ID_MODULO,
            "modulo": NOMBRE_MODULO,
            "rol": ROL_MODULO,
            "version": VERSION_MODULO,
            "operacion": "ejecutar_total",
            "estado": ESTADO_DEGRADADO,
            "coherente": False,
            "capacidades_ejecutadas": [],
            "errores_ejecucion": [
                f"{NOMBRE_MODULO}: CONTENEDOR['capacidades'] "
                "no es dict"
            ],
            "resultados": {},
            "capacidades_declaradas": [],
        }

    for nombre in sorted(capacidades):

        referencia = capacidades[nombre]

        try:
            resultados[nombre] = _ejecutar_capacidad(
                nombre=nombre,
                referencia=referencia,
                peticion=peticion_normalizada,
            )

        except Exception as exc:
            errores_ejecucion.append(
                f"{nombre}: {exc}"
            )

            resultados[nombre] = None

    barrido = resultados.get("barrer")

    coherente = (
        isinstance(barrido, dict)
        and bool(barrido.get("coherente"))
    )

    ejecutadas = sorted(
        nombre
        for nombre, resultado in resultados.items()
        if resultado is not None
    )

    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "operacion": "ejecutar_total",
        "estado": (
            ESTADO_OPERATIVO
            if coherente and not errores_ejecucion
            else ESTADO_DEGRADADO
        ),
        "coherente": coherente and not errores_ejecucion,
        "capacidades_ejecutadas": ejecutadas,
        "errores_ejecucion": errores_ejecucion,
        "resultados": resultados,
        "capacidades_declaradas": sorted(
            capacidades.keys()
        ),
    }


# ===============================================================
# 26. INSPECCIONAR
# ===============================================================

def inspeccionar(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Expone el estado estructural del módulo sin modificarlo.
    """
    hallado = _leer()
    resultado = barrer()

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
            "APROBADO": APROBADO,
            "RECHAZADO": RECHAZADO,
        },
        "capacidades_contractuales": sorted(
            CONTENEDOR.get(
                "capacidades",
                {},
            ).keys()
        ),
        "capacidades_meta": sorted(
            CONTENEDOR.get(
                "capacidades_meta",
                {},
            ).keys()
        ),
        "integridad": {
            "coherente": resultado.get("coherente"),
            "estado": resultado.get("estado"),
            "choques": resultado.get("choques"),
            "errores": resultado.get("errores"),
            "mecanica": resultado.get("mecanica"),
            "total_mecanicas": resultado.get(
                "total_mecanicas"
            ),
            "archivos": resultado.get("archivos"),
        },
        "mecanicas_descubiertas": sorted(
            hallado.keys()
        ),
        "declaraciones": list(DECLARACIONES),
        "autoriza_engine": CONTENEDOR.get(
            "autoriza_engine"
        ),
        "reporting": CONTENEDOR.get(
            "reporting"
        ),
        "invariantes": list(INVARIANTES),
    }


# ===============================================================
# 27. REGISTRAR INVENTARIO
# ===============================================================

def registrar_inventario(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Produce una instantánea registrable del inventario.
    No modifica las mecánicas ni la evidencia.
    """
    resultado = inventario(peticion)

    return {
        "id": ID_MODULO,
        "operacion": "registrar_inventario",
        "registrado": True,
        "inventario": resultado,
    }


# ===============================================================
# FIN CAPACIDADES PÚBLICAS — CORRELACIÓN MECÁNICA
# ===============================================================
# ===============================================================
# PARTE 10 — RESOLUCIÓN ESTRICTA Y EXPORTACIONES
# ===============================================================

# ===============================================================
# 10.0 — IMPORTS REQUERIDOS
# ===============================================================

# ===============================================================
# FIN 10.0
# ===============================================================


# ===============================================================
# 10.1 — MAPA DE CAPACIDADES PÚBLICAS
# ===============================================================

def _mapa_capacidades() -> Dict[str, Callable[..., Any]]:
    """
    Construye exclusivamente el mapa de capacidades públicas
    realmente definidas en este módulo.

    No ejecuta capacidades.
    No modifica CONTENEDOR.
    No crea referencias externas.
    No inventa capacidades.
    """
    mapa: Dict[str, Callable[..., Any]] = {
        "barrer": barrer,
        "verificar": verificar,
        "evaluar": evaluar,
        "axiomas": axiomas,
        "inventario": inventario,
        "verificar_salida": verificar_salida,
        "listar_mecanicas": listar_mecanicas,
        "reporte": reporte,
        "diagnostico": diagnostico,
        "ejecutar_total": ejecutar_total,
        "inspeccionar": inspeccionar,
        "registrar_inventario": registrar_inventario,
    }

    for nombre, funcion in sorted(mapa.items()):
        if not inspect.isroutine(funcion):
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: capacidad pública '{nombre}' "
                "no es una función callable real"
            )

    return mapa

# ===============================================================
# FIN 10.1
# ===============================================================


# ===============================================================
# 10.2 — RESOLUCIÓN DETERMINISTA DE CAPACIDADES
# ===============================================================

def _resolver_capacidades(
    cont: Dict[str, Any],
) -> Dict[str, Callable[..., Any]]:
    """
    Resuelve todas las referencias declaradas en
    CONTENEDOR["capacidades"] hacia funciones reales del módulo.

    La función:
        - no ejecuta ninguna capacidad.
        - no modifica cont.
        - no modifica otras estructuras.
        - no inventa capacidades.
        - no acepta referencias externas.
        - devuelve un mapa completo y determinista.

    La mutación contractual de CONTENEDOR se realiza exclusivamente
    en la sección 10.3.
    """
    capacidades = cont.get("capacidades")

    if not isinstance(capacidades, dict):
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: capacidades debe ser dict"
        )

    mapa = _mapa_capacidades()
    resueltas: Dict[str, Callable[..., Any]] = {}

    for nombre in sorted(capacidades):

        if not isinstance(nombre, str) or not nombre.strip():
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: identificador de capacidad inválido"
            )

        referencia = capacidades[nombre]

        if isinstance(referencia, str):

            if referencia not in mapa:
                raise ContratoInvalido(
                    f"{NOMBRE_MODULO}: capacidad '{nombre}' "
                    f"referencia inexistente: '{referencia}'"
                )

            funcion = mapa[referencia]

            if not inspect.isroutine(funcion):
                raise ContratoInvalido(
                    f"{NOMBRE_MODULO}: capacidad '{nombre}' "
                    f"resuelve '{referencia}', pero no es función callable real"
                )

            resueltas[nombre] = funcion
            continue

        if inspect.isroutine(referencia):

            if referencia not in mapa.values():
                raise ContratoInvalido(
                    f"{NOMBRE_MODULO}: capacidad '{nombre}' "
                    "apunta a una función no perteneciente al mapa "
                    "público del módulo"
                )

            resueltas[nombre] = referencia
            continue

        if callable(referencia):
            raise ContratoInvalido(
                f"{NOMBRE_MODULO}: capacidad '{nombre}' "
                "es callable pero no una función válida del módulo"
            )

        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: capacidad '{nombre}' "
            f"tiene tipo inválido: {type(referencia).__name__}"
        )

    return resueltas

# ===============================================================
# FIN 10.2
# ===============================================================


# ===============================================================
# 10.3 — VALIDACIÓN Y ASIGNACIÓN CONTRACTUAL
# ===============================================================

_validar_contrato_completo(CONTENEDOR)

_CAPACIDADES_RESUELTAS = _resolver_capacidades(CONTENEDOR)

if set(_CAPACIDADES_RESUELTAS.keys()) != set(
    CONTENEDOR["capacidades"].keys()
):
    raise ContratoInvalido(
        f"{NOMBRE_MODULO}: resolución incompleta de capacidades"
    )

CONTENEDOR["capacidades"] = _CAPACIDADES_RESUELTAS

# ===============================================================
# FIN 10.3
# ===============================================================


# ===============================================================
# 10.4 — VERIFICACIÓN FINAL DE RESOLUCIÓN
# ===============================================================

if not isinstance(CONTENEDOR.get("capacidades"), dict):
    raise ContratoInvalido(
        f"{NOMBRE_MODULO}: capacidades no quedó como dict"
    )

for _nombre_capacidad in sorted(CONTENEDOR["capacidades"]):

    _funcion_capacidad = CONTENEDOR["capacidades"][
        _nombre_capacidad
    ]

    if not inspect.isroutine(_funcion_capacidad):
        raise ContratoInvalido(
            f"{NOMBRE_MODULO}: capacidad '{_nombre_capacidad}' "
            "no quedó resuelta a una función callable real"
        )

# ===============================================================
# FIN 10.4
# ===============================================================


# ===============================================================
# 10.5 — EXPORTACIONES PÚBLICAS
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
    "DECLARACIONES",
    "axiomas",
    "barrer",
    "verificar",
    "evaluar",
    "inventario",
    "verificar_salida",
    "listar_mecanicas",
    "reporte",
    "diagnostico",
    "ejecutar_total",
    "inspeccionar",
    "registrar_inventario",
    "APROBADO",
    "RECHAZADO",
    "ContratoInvalido",
]

# ===============================================================
# FIN 10.5
# ===============================================================


# ===============================================================
# FIN PARTE 10
# ===============================================================


# ===============================================================
# FIN DEL MÓDULO
# ===============================================================
