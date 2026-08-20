# ===============================================================
# VPSI-TRUTH — modules/taxonomia/__init__.py
# ===============================================================
#
# MÓDULO:              taxonomia
# ID:                  TX
# Rol:                 TX
# Versión módulo:      2.0
# Versión contrato:    1.0
# Esquema contrato:    VPSI-CONTRACT-1.0
# Estabilidad:         ESTABLE
# Compatible desde:    1.0
# API Engine:          >=1.0
#
# Función:
#   Definir y auditar reglas deterministas de estructura para medir
#   tácticas (T1–T15). Aplicar coincidencia estructural sobre una
#   descripción bajo O_context cuando Engine lo invoca.
#
# Qué hace:
#   - Descubre TACTICA (dict) o TACTICAS (list) en *.py del directorio.
#   - Audita cada declaración (id, nombre, degrada, enunciado).
#   - Filtra: si no pasa, no sale ni se aplica.
#   - Detecta choques de id/nombre duplicados.
#   - Aplica coincidencia estructural (sin interpretación).
#   - Reporta inventario, estado y diagnóstico propios.
#
# Qué NO hace:
#   - No interpreta contenido semántico libre.
#   - No calcula C, L, K, Tru_Ri ni Tru_total.
#   - No orquesta el ciclo del sistema.
#   - No deposita en Diagnóstico (Engine decide el destino).
#
# Responsabilidad:
#   Coherencia interna del catálogo de tácticas y medición
#   estructural determinista cuando Engine la solicita.
#
# Autoridad:
#   - Declarar y filtrar tácticas metodológicas.
#   - Aplicar coincidencia por estructura explícita.
#   - Reportar estado estructural del módulo.
#
# Conocimiento exportable:
#   - inventario
#   - reporte
#   - diagnostico
#   - tacticas válidas
#   - axiomas TX
#
# Relación con Engine:
#   Engine descubre este CONTENEDOR, ejecuta solo las capacidades
#   declaradas y consolida el reporte que este módulo produce.
#   La aplicación de taxonomía ocurre cuando el contrato y MC
#   lo autorizan; Engine es quien invoca.
#
# Relación con Omega:
#   Omega no calcula nada de este módulo.
#   Solo presenta lo que Engine entrega.
#
# Observaciones:
#   Archivos *.py con TACTICA o TACTICAS participan.
#   Sin declaración válida, el archivo no aporta tácticas.
#   degrada ∈ {C, L, K, A}; Tru lo calculan CA/FO bajo el mismo O.
#
# ===============================================================

# ===============================================================
# IMPORTACIONES
# ===============================================================
#
# Solo stdlib y tipado.
# No importar módulos de dominio (CX, MC, CA, …).
# Si hace falta algo, se declara en requiere[]; Engine resuelve.
#

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# ===============================================================
# FIN IMPORTACIONES
# ===============================================================

# ===============================================================
# CONSTANTES
# ===============================================================

ID_MODULO = "TX"
NOMBRE_MODULO = "taxonomia"
ROL_MODULO = "TX"

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

CLAVES_TACTICA = ("id", "nombre", "degrada", "enunciado")
FACTORES_DEGRADA = frozenset({"C", "L", "K", "A"})

INVARIANTES = (
    "el id del módulo nunca cambia",
    "el rol nunca cambia",
    "las capacidades declaradas son siempre callables tras la resolución",
    "este módulo no modifica el estado de otros módulos",
    "este módulo no inventa capacidades no declaradas en CONTENEDOR",
    "TX no calcula Tru_total",
    "solo tácticas que pasan el filtro se aplican",
    "medición por estructura explícita, no por interpretación",
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
        "Taxonomía metodológica (TX). Reglas deterministas de estructura "
        "para medir tácticas (T1–T15). Sin interpretación. No calcula "
        "Tru_total. El init audita cada táctica; si no pasa el filtro, "
        "no sale. Engine aplica esta taxonomía sobre un O_context cuando "
        "el contrato y la correlación mecánica lo autorizan."
    ),

    # ----- PROPÓSITO -----
    "funcion": (
        "Auditar declaraciones de táctica; filtrar las inválidas; "
        "aplicar coincidencia estructural determinista; reportar "
        "estado propio del catálogo TX."
    ),
    "no_hace": [
        "No interpreta contenido semántico libre",
        "No calcula C, L, K, Tru_Ri ni Tru_total",
        "No orquesta el ciclo del sistema",
        "No deposita reportes en Diagnóstico",
        "No aplica tácticas que no pasaron el filtro interno",
    ],

    # ----- AUTORIDAD -----
    "autoridad": [
        "Declarar y filtrar tácticas metodológicas por estructura",
        "Detectar id/nombre duplicados entre archivos",
        "Aplicar coincidencia estructural sobre una descripción",
        "Reportar inventario, reporte y diagnóstico propios",
    ],

    # ----- CONOCIMIENTO EXPORTABLE -----
    "conocimiento_exportable": [
        "inventario",
        "reporte",
        "diagnostico",
        "tacticas",
        "axiomas",
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
    "requiere": [
    "CE", "AX", "FO", "MC", "SF",
    "CA", "CX", "DI", "RE", "VX", 
    "CH", "CIT", "DGCO", "UI",
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
        "validar_esquema": True,          # ← AGREGADO
        "acceso_archivos": True,          # ← AGREGADO
        "avaluar_universal": True,

        # --- BANDERAS NUEVAS (OBLIGATORIAS ENGINE) ---
        "ejecutar_total": True,           # ← AGREGADO
        "inspeccionar": True,             # ← AGREGADO
        "registrar_inventario": True,     # ← AGREGADO
    },
    
    # ============================================================
    # CONSULTAS SOPORTADAS
    # ============================================================
    "consultas_soportadas": [
        # --- CENTINELA ---
        "verificar",
        "barrer",
        "verificar_salida",

        # --- MEDICIÓN ---
        "aplicar",
        "axiomas",

        # --- INVENTARIO Y REPORTING ---
        "inventario",
        "reporte",
        "diagnostico",

        # --- CAPACIDADES ARQUITECTÓNICAS ---
        "ejecutar_total",
        "inspeccionar",
        "registrar_inventario",
    ],

    # ============================================================
    # CAPACIDADES
    # ============================================================
    "capacidades": {
        # --- CENTINELA ---
        "verificar": "verificar",
        "barrer": "barrer",
        "verificar_salida": "verificar_salida",

        # --- MEDICIÓN ---
        "aplicar": "aplicar",
        "axiomas": "axiomas",

        # --- INVENTARIO Y REPORTING ---
        "inventario": "inventario",
        "reporte": "reporte",
        "diagnostico": "diagnostico",

        # --- CAPACIDADES ARQUITECTÓNICAS (OBLIGATORIAS ENGINE) ---
        "ejecutar_total": "ejecutar_total",
        "inspeccionar": "inspeccionar",
        "registrar_inventario": "registrar_inventario",
        "evaluar_universal": "evaluar_universal",
    },

    # ============================================================
    # METADATOS DE CAPACIDADES (1:1 OBLIGATORIO)
    # ============================================================

    "capacidades_meta": {
        "verificar": {
            "descripcion": (
                "Coherencia interna de TX (alias de barrer)."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con coherente, choques, errores, tacticas"
            ),
            "acceso_archivos": ["*"],
        },

        "barrer": {
            "descripcion": (
                "Audita tácticas, detecta choques y filtra inválidas."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con coherente, choques, errores, tacticas, "
                "total_declaradas, total_validas, notas"
            ),
            "acceso_archivos": ["*"],
        },

        "aplicar": {
            "descripcion": (
                "Aplica coincidencia estructural de tácticas válidas "
                "sobre una descripción. No calcula Tru."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con aplicadas, total, tacticas_disponibles, O_context"
            ),
            "acceso_archivos": ["*"],
        },

        "inventario": {
            "descripcion": (
                "Enumeración de tácticas que pasaron el filtro."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con id, version, tacticas, total_validas"
            ),
            "acceso_archivos": ["*"],
        },

        "reporte": {
            "descripcion": (
                "Estado actual del módulo TX."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con estado, version, capacidades, coherente"
            ),
            "acceso_archivos": ["*"],
        },

        "diagnostico": {
            "descripcion": (
                "Problemas, advertencias y recomendaciones de TX."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con estado, problemas, advertencias, "
                "recomendaciones"
            ),
            "acceso_archivos": ["*"],
        },

        "axiomas": {
            "descripcion": (
                "Declaraciones axiomáticas del oficio TX."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "lista de dicts axiomáticos",
            "acceso_archivos": ["*"],
        },

                "verificar_salida": {
            "descripcion": (
                "Forma mínima de una salida de TX."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "bool",
            "acceso_archivos": ["*"],
        },

        # --- CAPACIDADES ARQUITECTÓNICAS (OBLIGATORIAS ENGINE) ---
        "ejecutar_total": {
            "descripcion": (
                "Autoridad total de ENGINE sobre TX. "
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
                "Capacidad meta de inspeccion estructural de TX. "
                "Expone constantes, capacidades, tacticas y estado "
                "sin alterar el contrato ni calcular."
            ),
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["acceso_archivos"],
            "salida": "dict con estructura, capacidades y estado del modulo",
            "acceso_archivos": ["acceso_archivos"],
        },
        "registrar_inventario": {
            "descripcion": (
                "Registra el inventario estructural de TX "
                "como instantanea determinista. No altera evidencia."
            ),
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["acceso_archivos"],
            "salida": "dict con inventario registrado",
            "acceso_archivos": ["acceso_archivos"],
        },
        "evaluar_universal": {
            "descripcion": (
                "Evalúa las capacidades reales de este módulo "
                "cuya firma se satisfaga con los hechos de entrada. "
                "Engine entrega la entrada; este callable solo aplica lo local."
           ),
          "entrada": "hechos: dict",
          "validar_esquema": ["*"],
          "salida": "dict con hechos, traza, ejecutadas",
          "acceso_archivos": ["*"],
         },
    },
    # ============================================================
    # REPORTING (OBLIGATORIO EN EL ESQUEMA)
    # ============================================================
    "reporting": {

        # ========================================================
        # BANDERAS DE ESTADO Y SALUD
        # ========================================================
        "estado": True,
        "salud": True,

        # ========================================================
        # BANDERAS DE INVENTARIO Y CAPACIDADES
        # ========================================================
        "inventario": True,
        "capacidades": True,

        # ========================================================
        # BANDERAS DE ERRORES Y ADVERTENCIAS
        # ========================================================
        "errores": True,
        "advertencias": True,

        # ========================================================
        # BANDERAS DE DEPENDENCIAS Y VERSION
        # ========================================================
        "dependencias": True,
        "version": True,

        # ========================================================
        # BANDERAS DE CONTRATO Y CONOCIMIENTO
        # ========================================================
        "contrato": True,
        "conocimiento": True,

        # ========================================================
        # BANDERAS DE METRICAS Y DIAGNOSTICO
        # ========================================================
        "metricas": True,
        "diagnostico": True,

        # ========================================================
        # BANDERA DE REPORTE
        # ========================================================
        "reporte": True,

        # ========================================================
        # BANDERAS OBLIGATORIAS SEGÚN ENGINE
        # ========================================================
        "acceso_archivos": True,          # ← AGREGADA
        "validar_esquema": True,          # ← AGREGADA

        # ========================================================
        # BANDERAS NUEVAS (OBLIGATORIAS ENGINE)
        # ========================================================
        "ejecutar_total": True,           # ← AGREGADA
        "inspeccionar": True,             # ← AGREGADA
        "registrar_inventario": True,     # ← AGREGADA
        "evaluar_universal": True,
    },


    # ============================================================
    # ESTADOS VÁLIDOS
    # ============================================================
    "estados_validos": list(ESTADOS_VALIDOS),

    # ============================================================
    # INVARIANTES
    # ============================================================
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


def _validar_tactica(meta: Dict[str, Any], origen: str) -> List[str]:
    """Audita una declaración de táctica. Errores ⇒ no sale."""
    errores: List[str] = []
    if not isinstance(meta, dict):
        return ["{0}: TACTICA no es dict".format(origen)]

    for clave in CLAVES_TACTICA:
        val = meta.get(clave)
        if val is None or val == "" or val == []:
            errores.append("{0}: falta o vacío '{1}'".format(origen, clave))

    tid = meta.get("id")
    if tid is not None and not isinstance(tid, str):
        errores.append("{0}: 'id' debe ser str".format(origen))

    nombre = meta.get("nombre")
    if nombre is not None and not isinstance(nombre, str):
        errores.append("{0}: 'nombre' debe ser str".format(origen))

    degrada = meta.get("degrada")
    if degrada is not None:
        if not isinstance(degrada, (list, tuple)):
            errores.append("{0}: 'degrada' debe ser lista".format(origen))
        else:
            for d in degrada:
                if d not in FACTORES_DEGRADA:
                    errores.append(
                        "{0}: factor '{1}' no permitido en degrada".format(
                            origen, d
                        )
                    )

    estructura = meta.get("estructura")
    if estructura is not None and not isinstance(estructura, dict):
        errores.append("{0}: 'estructura' debe ser dict".format(origen))

    return errores


def _descubrir() -> Dict[str, Dict[str, Any]]:
    """
    Recorre la carpeta.
    Acepta TACTICAS (lista) o TACTICA (dict).
    Cada táctica se audita; si no pasa, se registra con error.
    """
    registro: Dict[str, Dict[str, Any]] = {}

    for f in sorted(_DIR.glob("*.py")):
        if f.name.startswith("_") or f.name == "__init__.py":
            continue

        clave = "taxonomia_{0}".format(f.stem)
        spec = importlib.util.spec_from_file_location(clave, str(f))
        if spec is None or spec.loader is None:
            continue

        mod = importlib.util.module_from_spec(spec)
        sys.modules[clave] = mod
        try:
            spec.loader.exec_module(mod)
        except Exception as e:
            registro[f.name] = {
                "archivo": f.name,
                "error": "{0}: {1}".format(type(e).__name__, e),
            }
            continue

        lista = getattr(mod, "TACTICAS", None)
        if isinstance(lista, list):
            for i, item in enumerate(lista):
                origen = "{0}[{1}]".format(f.name, i)
                errs = _validar_tactica(
                    item if isinstance(item, dict) else {}, origen
                )
                if errs:
                    registro["{0}#{1}".format(f.name, i)] = {
                        "archivo": f.name,
                        "error": "; ".join(errs),
                    }
                    continue
                tid = str(item.get("id"))
                registro["{0}#{1}".format(f.name, tid)] = {
                    "archivo": f.name,
                    "id": tid,
                    "nombre": item.get("nombre"),
                    "degrada": list(item.get("degrada") or []),
                    "enunciado": item.get("enunciado"),
                    "estructura": item.get("estructura") or {},
                }
            continue

        meta = getattr(mod, "TACTICA", None)
        if meta is None:
            registro[f.name] = {
                "archivo": f.name,
                "error": "sin TACTICA ni TACTICAS",
            }
            continue

        errs = _validar_tactica(
            meta if isinstance(meta, dict) else {}, f.name
        )
        if errs:
            registro[f.name] = {
                "archivo": f.name,
                "error": "; ".join(errs),
            }
            continue

        registro[f.name] = {
            "archivo": f.name,
            "id": str(meta.get("id")),
            "nombre": meta.get("nombre"),
            "degrada": list(meta.get("degrada") or []),
            "enunciado": meta.get("enunciado"),
            "estructura": meta.get("estructura") or {},
        }

    return registro


def _detectar_choques(hallado: Dict[str, Dict[str, Any]]) -> List[str]:
    choques: List[str] = []
    por_id: Dict[str, List[str]] = {}
    por_nombre: Dict[str, List[str]] = {}

    for clave, meta in hallado.items():
        if "error" in meta:
            continue
        tid = str(meta.get("id") or "").strip()
        nom = str(meta.get("nombre") or "").strip()
        if tid:
            por_id.setdefault(tid, []).append(clave)
        if nom:
            por_nombre.setdefault(nom, []).append(clave)

    for tid, archivos in por_id.items():
        if len(archivos) > 1:
            choques.append(
                "id de táctica '{0}' repetido en {1}".format(tid, archivos)
            )
    for nom, archivos in por_nombre.items():
        if len(archivos) > 1:
            choques.append(
                "nombre de táctica '{0}' repetido en {1}".format(nom, archivos)
            )
    return choques


def _solo_validas(
    hallado: Dict[str, Dict[str, Any]],
) -> Dict[str, Dict[str, Any]]:
    return {
        k: v
        for k, v in hallado.items()
        if "error" not in v and v.get("id")
    }

# ===============================================================
# FIN FUNCIONES PRIVADAS
# ===============================================================

# ===============================================================
# CAPACIDADES PÚBLICAS
# ===============================================================

def barrer() -> Dict[str, Any]:
    """
    Coherencia interna de la taxonomía.
    Audita, filtra, detecta choques.
    No deposita en Diagnóstico.
    """
    hallado = _descubrir()
    errores: List[str] = []
    notas: List[str] = []

    for clave, meta in sorted(hallado.items()):
        if "error" in meta:
            errores.append("{0}: {1}".format(clave, meta["error"]))

    choques = _detectar_choques(hallado)
    validas = _solo_validas(hallado)

    if not hallado:
        notas.append("sin archivos de táctica (vacío legítimo)")
    elif not validas and hallado:
        notas.append("hay archivos pero ninguna táctica pasó el filtro")

    return {
        "id": ID_MODULO,
        "contenedor": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "coherente": not (choques or errores),
        "choques": choques,
        "errores": errores,
        "tacticas": sorted(str(m.get("id")) for m in validas.values()),
        "total_declaradas": len(hallado),
        "total_validas": len(validas),
        "notas": notas,
    }


def verificar() -> Dict[str, Any]:
    """Alias de barrer — coherencia interna de TX."""
    return barrer()


def aplicar(
    descripcion: Dict[str, Any],
    contexto: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Aplica la taxonomía por estructura, no por opinión.
    Solo tácticas que pasaron el filtro.
    No emite Tru_total.
    """
    if not isinstance(descripcion, dict):
        return {
            "id": ID_MODULO,
            "contenedor": NOMBRE_MODULO,
            "aplicadas": [],
            "total": 0,
            "errores": ["descripcion debe ser dict"],
        }

    hallado = _descubrir()
    validas = _solo_validas(hallado)
    contexto = contexto or {}
    o_ctx = contexto.get("O_context") or contexto.get("contexto")

    coincidencias: List[Dict[str, Any]] = []
    for clave, meta in sorted(validas.items()):
        estructura = meta.get("estructura") or {}
        ok = True
        evidencia: List[str] = []

        if isinstance(estructura, dict) and estructura:
            for k, esperado in estructura.items():
                actual = descripcion.get(k)
                if actual is None or actual != esperado:
                    ok = False
                    break
                evidencia.append("{0}={1}".format(k, actual))
        else:
            ok = False

        if ok:
            coincidencias.append({
                "id": meta.get("id"),
                "nombre": meta.get("nombre"),
                "degrada": meta.get("degrada", []),
                "enunciado": meta.get("enunciado"),
                "evidencia": evidencia,
                "archivo": meta.get("archivo"),
            })

    return {
        "id": ID_MODULO,
        "contenedor": NOMBRE_MODULO,
        "O_context": o_ctx,
        "aplicadas": coincidencias,
        "total": len(coincidencias),
        "tacticas_disponibles": len(validas),
        "nota": (
            "Medición estructural. Sin interpretación. "
            "Solo tácticas que pasaron el filtro. "
            "Tru_total lo calculan CA/FO bajo el mismo O_context."
        ),
    }


def inventario(peticion: Any = None) -> Dict[str, Any]:
    """Qué existe en TX. Solo tácticas válidas."""
    hallado = _descubrir()
    validas = _solo_validas(hallado)
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
        "tacticas": {
            str(m.get("id")): {
                "nombre": m.get("nombre"),
                "degrada": m.get("degrada"),
            }
            for m in validas.values()
        },
        "total_validas": len(validas),
        "funcion": CONTENEDOR.get("funcion"),
        "autoridad": CONTENEDOR.get("autoridad"),
        "conocimiento_exportable": CONTENEDOR.get("conocimiento_exportable"),
        "invariantes": CONTENEDOR.get("invariantes"),
    }


def axiomas() -> List[Dict[str, Any]]:
    """Declaraciones axiomáticas del oficio TX."""
    return [
        {
            "id": "TX-1",
            "tipo": "axioma",
            "sujeto": "taxonomia",
            "relacion": "mide_por",
            "objeto": "estructura",
            "polaridad": True,
            "enunciado": (
                "Cada táctica se reconoce por criterios estructurales "
                "explícitos, no por interpretación libre."
            ),
            "depende_de": [],
            "gobierna": ["taxonomia"],
        },
        {
            "id": "TX-2",
            "tipo": "axioma",
            "sujeto": "taxonomia",
            "relacion": "no_calcula",
            "objeto": "Tru_total",
            "polaridad": True,
            "enunciado": (
                "TX no calcula Tru_total. Degrada factores (C, L, K, A) "
                "cuando la estructura coincide; CA/FO calculan bajo O_context."
            ),
            "depende_de": [],
            "gobierna": ["taxonomia"],
        },
        {
            "id": "TX-3",
            "tipo": "axioma",
            "sujeto": "init_taxonomia",
            "relacion": "filtra",
            "objeto": "tacticas_internas",
            "polaridad": True,
            "enunciado": (
                "Toda táctica declarada se audita. "
                "Si no pasa el filtro, no sale ni se aplica."
            ),
            "depende_de": [],
            "gobierna": ["taxonomia"],
        },
    ]


def verificar_salida(salida: Any) -> bool:
    if not isinstance(salida, dict):
        return False
    return (
        "coherente" in salida
        or "id" in salida
        or "aplicadas" in salida
        or "tacticas" in salida
    )



# ===============================================================
# CAPACIDADES ARQUITECTÓNICAS (OBLIGATORIAS ENGINE)
# ===============================================================

def ejecutar_total(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Autoridad total de ENGINE sobre TX.
    Fuente única: CONTENEDOR["capacidades"].
    No inventa. No autoinvoca. Todo callable real.
    """
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
            "rol": ROL_MODULO,
            "version": VERSION_MODULO,
            "operacion": "ejecutar_total",
            "estado": ESTADO_DEGRADADO,
            "coherente": False,
            "capacidades_ejecutadas": [],
            "errores_ejecucion": [
                f"{NOMBRE_MODULO}: CONTENEDOR['capacidades'] no es dict"
            ],
            "resultados": {},
            "capacidades_declaradas": [],
        }

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
                    raise ContratoInvalido(
                        f"'{referencia}' no es callable"
                    )
            else:
                raise ContratoInvalido(
                    f"tipo inválido: {type(referencia).__name__}"
                )

            if nombre == "aplicar":
                resultados[nombre] = fn(
                    descripcion=(
                        peticion_normalizada.get("descripcion")
                        if isinstance(
                            peticion_normalizada.get("descripcion"),
                            dict,
                        )
                        else {}
                    ),
                    contexto=peticion_normalizada.get("contexto"),
                )
            elif nombre == "verificar_salida":
                resultados[nombre] = fn(
                    peticion_normalizada.get("salida")
                    if "salida" in peticion_normalizada
                    else {}
                )
            elif nombre in ("inventario",):
                resultados[nombre] = fn(peticion_normalizada)
            else:
                resultados[nombre] = fn()
        except Exception as exc:
            errores_ejecucion.append(f"{nombre}: {exc}")
            resultados[nombre] = None

    barrido = resultados.get("barrer")
    coherente = (
        isinstance(barrido, dict) and bool(barrido.get("coherente"))
    )
    ejecutadas = sorted(
        n for n, r in resultados.items() if r is not None
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
        "capacidades_declaradas": sorted(capacidades.keys()),
    }


def inspeccionar(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Inspección estructural de TX.
    Expone contrato, tácticas y estado sin calcular ni alterar.
    """
    b = barrer()
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
            "CLAVES_TACTICA": list(CLAVES_TACTICA),
            "FACTORES_DEGRADA": sorted(FACTORES_DEGRADA),
        },
        "capacidades_contractuales": sorted(
            CONTENEDOR.get("capacidades", {}).keys()
        ),
        "capacidades_meta": sorted(
            CONTENEDOR.get("capacidades_meta", {}).keys()
        ),
        "integridad": {
            "coherente": b.get("coherente"),
            "choques": b.get("choques"),
            "errores": b.get("errores"),
            "tacticas": b.get("tacticas"),
            "total_declaradas": b.get("total_declaradas"),
            "total_validas": b.get("total_validas"),
            "notas": b.get("notas"),
        },
        "autoriza_engine": CONTENEDOR.get("autoriza_engine"),
        "reporting": CONTENEDOR.get("reporting"),
        "invariantes": list(INVARIANTES),
        "nota": (
            "inspeccionar expone estructura de TX sin calcular "
            "ni alterar el contrato ni las tácticas."
        ),
    }


def registrar_inventario(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Instantánea determinista del inventario de TX.
    No altera evidencia ni tácticas.
    """
    inv = inventario(peticion)
    return {
        "id": ID_MODULO,
        "operacion": "registrar_inventario",
        "registrado": True,
        "inventario": inv,
        "nota": (
            "Instantánea determinista del inventario de TX. "
            "No modifica tácticas ni evidencia."
        ),
    }

# ===============================================================
# FIN CAPACIDADES ARQUITECTÓNICAS
# ===============================================================
# ===============================================================
# FIN CAPACIDADES PÚBLICAS
# ===============================================================
# ===============================================================
# EVALUAR_UNIVERSAL
# ===============================================================

def evaluar_universal(
    hechos: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Engine entrega hechos.
    Este callable ejecuta las capacidades REALES de ESTE módulo
    (CONTENEDOR['capacidades'] ya resuelto a callables).
    Punto fijo local. No se llama a sí mismo. No toca otros módulos.
    """
    hechos_out: Dict[str, Any] = dict(hechos or {})
    traza: List[Dict[str, Any]] = []
    ejecutadas: set = set()

    capacidades = CONTENEDOR.get("capacidades") or {}

    while True:
        nuevos = 0

        for nombre, fn in capacidades.items():
            if nombre == "evaluar_universal":
                continue
            if not callable(fn):
                continue
            if nombre in ejecutadas:
                continue

            try:
                sig = inspect.signature(fn)
            except (TypeError, ValueError):
                continue

            requeridos = []
            opcionales = []
            for pname, p in sig.parameters.items():
                if p.kind not in (
                    inspect.Parameter.POSITIONAL_ONLY,
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    inspect.Parameter.KEYWORD_ONLY,
                ):
                    continue
                if p.default is inspect.Parameter.empty:
                    requeridos.append(pname)
                else:
                    opcionales.append(pname)

            # --- resolución de argumentos (universal, sin nombres inventados) ---
            argumentos: Dict[str, Any] = {}

            if not requeridos:
                # firma vacía o solo opcionales: usar opcionales presentes en hechos
                for p in opcionales:
                    if p in hechos_out:
                        argumentos[p] = hechos_out[p]
                try:
                    salida = fn(**argumentos) if argumentos else fn()
                except Exception as ex:
                    ejecutadas.add(nombre)
                    traza.append({
                        "capacidad": nombre,
                        "estado": "ERROR",
                        "detalle": "{0}: {1}".format(type(ex).__name__, ex),
                    })
                    continue

            elif all(r in hechos_out for r in requeridos):
                # todos los requeridos existen como claves en hechos
                for p in requeridos + opcionales:
                    if p in hechos_out:
                        argumentos[p] = hechos_out[p]
                try:
                    salida = fn(**argumentos)
                except Exception as ex:
                    ejecutadas.add(nombre)
                    traza.append({
                        "capacidad": nombre,
                        "estado": "ERROR",
                        "detalle": "{0}: {1}".format(type(ex).__name__, ex),
                    })
                    continue

            elif len(requeridos) == 1:
                # patrón real del repo: calcular(peticion), verificar(datos), etc.
                # se entrega el dict de hechos completo en ese único parámetro
                argumentos[requeridos[0]] = hechos_out
                for p in opcionales:
                    if p in hechos_out:
                        argumentos[p] = hechos_out[p]
                try:
                    salida = fn(**argumentos)
                except Exception as ex:
                    ejecutadas.add(nombre)
                    traza.append({
                        "capacidad": nombre,
                        "estado": "ERROR",
                        "detalle": "{0}: {1}".format(type(ex).__name__, ex),
                    })
                    continue
            else:
                # varios requeridos ausentes: no aplicable aún
                continue

            ejecutadas.add(nombre)
            publicados: List[str] = []

            if isinstance(salida, dict):
                for clave, valor in salida.items():
                    if clave.startswith("_"):
                        continue
                    if clave not in hechos_out:
                        hechos_out[clave] = valor
                        publicados.append(clave)
                        nuevos += 1

            traza.append({
                "capacidad": nombre,
                "estado": "EXITO",
                "argumentos": sorted(argumentos.keys()),
                "publica": publicados,
            })

        if nuevos == 0:
            break

    return {
        "hechos": hechos_out,
        "traza": traza,
        "ejecutadas": sorted(ejecutadas),
    }

# ===============================================================
# FIN EVALUAR_UNIVERSAL
# ===============================================================
# ===============================================================
# PARTE 9 — REPORTING INTERNO
# ===============================================================

# ===============================================================
# 9.1 — REPORTE
# ===============================================================

def reporte() -> Dict[str, Any]:
    """Estado actual de TX. No diagnostica el sistema."""
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
        "tacticas": b.get("tacticas"),
        "total_validas": b.get("total_validas"),
        "autoridad": CONTENEDOR.get("autoridad"),
        "conocimiento_exportable": CONTENEDOR.get(
            "conocimiento_exportable"
        ),
        "operaciones_arquitectonicas": {
            "ejecutar_total": True,
            "inspeccionar": True,
            "registrar_inventario": True,
        },
    }

# ===============================================================
# FIN 9.1
# ===============================================================


# ===============================================================
# 9.2 — DIAGNÓSTICO
# ===============================================================

def diagnostico() -> Dict[str, Any]:
    """Problemas y advertencias propios de TX."""
    b = barrer()
    problemas = list(b.get("choques") or []) + list(
        b.get("errores") or []
    )
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
# FIN 9.2
# ===============================================================

# ===============================================================
# FIN PARTE 9
# ===============================================================


# ===============================================================
# PARTE 10 — VALIDACIÓN, RESOLUCIÓN Y EXPORTACIONES
# ===============================================================

# ===============================================================
# 10.1 — MAPA DE CAPACIDADES
# ===============================================================

_CAP_MAP = {
    # --- CENTINELA ---
    "verificar": verificar,
    "barrer": barrer,
    "verificar_salida": verificar_salida,

    # --- MEDICIÓN ---
    "aplicar": aplicar,
    "axiomas": axiomas,

    # --- INVENTARIO Y REPORTING ---
    "inventario": inventario,
    "reporte": reporte,
    "diagnostico": diagnostico,

    # --- CAPACIDADES ARQUITECTÓNICAS (OBLIGATORIAS ENGINE) ---
    "ejecutar_total": ejecutar_total,
    "inspeccionar": inspeccionar,
    "registrar_inventario": registrar_inventario,
    "evaluar_universal": evaluar_universal,
    
}

# ===============================================================
# FIN 10.1
# ===============================================================


# ===============================================================
# 10.2 — RESOLUCIÓN DE CAPACIDADES
# ===============================================================

def _resolver_capacidades(cont: Dict[str, Any]) -> None:
    """
    Resuelve referencias str → callables reales.
    MUTA CONTENEDOR["capacidades"] para que Engine reciba callables.
    """
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
                    "{0}: '{1}' no es callable".format(
                        NOMBRE_MODULO, ref
                    )
                )
            resueltas[nombre] = fn
            continue
        raise ContratoInvalido(
            "{0}: capacidad '{1}' tipo inválido: {2}".format(
                NOMBRE_MODULO, nombre, type(ref).__name__
            )
        )
    cont["capacidades"] = resueltas

# ===============================================================
# FIN 10.2
# ===============================================================


# ===============================================================
# 10.3 — VALIDAR Y RESOLVER AL IMPORTAR
# ===============================================================

_validar_contrato(CONTENEDOR)
_resolver_capacidades(CONTENEDOR)

# ===============================================================
# FIN 10.3
# ===============================================================


# ===============================================================
# 10.4 — EXPORTACIONES
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
    "verificar",
    "barrer",
    "aplicar",
    "inventario",
    "reporte",
    "diagnostico",
    "axiomas",
    "verificar_salida",
    "ejecutar_total",
    "inspeccionar",
    "registrar_inventario",
    "ContratoInvalido",
    "evaluar_universal",

]

# ===============================================================
# FIN 10.4
# ===============================================================

# ===============================================================
# FIN PARTE 10
# ===============================================================
