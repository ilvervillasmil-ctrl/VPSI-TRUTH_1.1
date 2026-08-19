#===============================================================
# VPSI-TRUTH — modules/citacion/__init__.py
# ===============================================================
#
# MÓDULO:              citacion
# ID:                  CIT
# Rol:                 CIT
# Versión módulo:      2.0
# Versión contrato:    1.0
# Esquema contrato:    VPSI-CONTRACT-1.0
# Estabilidad:         ESTABLE
# Compatible desde:    1.0
# API Engine:          >=1.0
#
# ---------------------------------------------------------------
# PRINCIPIO FUNDAMENTAL
# ---------------------------------------------------------------
#
# CIT no calcula.
# CIT no decide.
# CIT no interpreta.
# CIT no modifica.
# CIT no crea conocimiento.
#
# CIT conoce, resuelve, relaciona y cita.
#
# Toda declaración formal del VPSI debe poder ser resuelta por CIT.
#
# ---------------------------------------------------------------
# DEFINICIÓN
# ---------------------------------------------------------------
#
# CIT es la autoridad universal de fundamentación del VPSI.
#
# Conserva conocimiento resoluble de todas las declaraciones
# públicas existentes dentro del sistema.
#
# Puede resolver, relacionar y citar cualquier axioma, teorema,
# definición, corolario, fórmula, contexto, regla, correlación
# o declaración formal proveniente de cualquier módulo presente
# o futuro.
#
# Su autoridad es absoluta sobre la fundamentación.
# No posee autoridad para alterar el conocimiento.
#
# ---------------------------------------------------------------
# MODELO CONCEPTUAL
# ---------------------------------------------------------------
#
#   Declaración
#        ↓
#   Resolución
#        ↓
#   Relación
#        ↓
#   Cadena normativa
#        ↓
#   Citación
#        ↓
#   Explicación
#
# Internamente CIT administra declaraciones.
# Las citas son únicamente una representación de esas declaraciones.
#
# ---------------------------------------------------------------
# OFICIO ÚNICO
# ---------------------------------------------------------------
#
# Resolver, organizar, relacionar y citar cualquier declaración
# pública perteneciente al VPSI.
#
# ---------------------------------------------------------------
# RESTRICCIÓN ÚNICA
# ---------------------------------------------------------------
#
# Ninguna capacidad de CIT puede modificar el conocimiento declarado.
#
# ---------------------------------------------------------------
# DOS MODOS
# ---------------------------------------------------------------
#
# Modo Engine
#   Engine solicita fundamentación del ciclo.
#   CIT devuelve la cadena documental utilizada.
#
# Modo Consulta
#   Se solicita conocimiento ("Cítame TA-7", "¿Qué dice Def-5.3.1?").
#   El mismo motor responde.
#
# ---------------------------------------------------------------
# ESCALABILIDAD
# ---------------------------------------------------------------
#
# CIT nunca crece en lógica.
# Crece únicamente en conocimiento declarado.
# Todo módulo presente o futuro puede registrar declaraciones
# públicas; CIT las incorpora sin modificar este INIT.
#
# ===============================================================

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

# ===============================================================
# SECCIÓN 1 — IDENTIDAD
# ===============================================================

_ID = "CIT"
_NOMBRE = "citacion"
_ROL = "CIT"
_VERSION = "2.0"
_VERSION_CONTRATO = "1.0"
_ESQUEMA = "VPSI-CONTRACT-1.0"
_ESTABILIDAD = "ESTABLE"
_COMPATIBLE_DESDE = "1.0"
_API_ENGINE = ">=1.0"


# ===============================================================
# SECCIÓN 2 — UNIVERSO DECLARATIVO (forma de declaración / cita)
# ===============================================================
#
# Tipos abiertos: no lista cerrada de módulos.
# Cualquier fuente presente o futura puede aportar declaraciones.
#

TIPOS_DECLARACION = (
    "axioma",
    "teorema",
    "definicion",
    "corolario",
    "lema",
    "regla",
    "principio",
    "formula",
    "correlacion",
    "contexto",
    "limite",
    "factor",
    "procedimiento",
    "contrato",
    "invariante",
    "capacidad",
    "evidencia",
    "citacion",
    # compatibilidad con tipos legados de ciclo
    "ax",
    "mc",
    "cx",
    "tx",
    "ca",
    "fo",
    "re",
    "ct",
    "ch",
    "sf",
)
# ===============================================================
# SECCIÓN 3 — 
# ===============================================================
RELACIONES = (
    "depende_de",
    "fundamenta",
    "contradice",
    "extiende",
    "deriva_de",
    "correlaciona_con",
    "limita",
    "activa",
    "desactiva",
    "requiere",
    "gobierna",
)
# ===============================================================
# SECCIÓN 4 —
# ===============================================================
CAMPOS_OBLIGATORIOS = (
    "id",
    "tipo",
    "fuente",
    "enunciado",
)

# ===============================================================
# SECCIÓN 4
# ===============================================================
CAMPOS_OBLIGATORIOS = (
    "descripcion",
    "evidencia_ref",
    "o_ref",
    "contexto_ciclo",
    "meta",
    "relaciones",
    "fuente_modulo",  # legado
)



# ===============================================================
# SECCIÓN 5
# ===============================================================

CONTENEDOR: Dict[str, Any] = {
    "esquema": _ESQUEMA,
    "version_contrato": _VERSION_CONTRATO,
    "version_modulo": _VERSION,
    "id": _ID,
    "nombre": _NOMBRE,
    "rol": _ROL,
    "estabilidad": _ESTABILIDAD,
    "compatible_desde": _COMPATIBLE_DESDE,
    "api_engine": _API_ENGINE,
# ===============================================================
# SECCIÓN 5.1
# ===============================================================

    "descripcion": (
        "Autoridad universal de fundamentación del VPSI. "
        "Conserva conocimiento resoluble de todas las declaraciones "
        "públicas del sistema. Puede resolver, relacionar y citar "
        "cualquier declaración formal proveniente de cualquier módulo "
        "presente o futuro. Autoridad absoluta sobre la fundamentación, "
        "la resolución, la citación, la cadena normativa y la explicación "
        "documental. No altera el conocimiento declarado."
    ),
# ===============================================================
# SECCIÓN 5.2
# ===============================================================
    "funcion": (
        "Resolver, organizar, relacionar y citar cualquier declaración "
        "pública perteneciente al VPSI. "
        "Modo Engine: cadena documental del ciclo. "
        "Modo Consulta: resolución y explicación bajo demanda."
    ),
# ===============================================================
# SECCIÓN 5.3
# ===============================================================
    "no_hace": [
        "Ninguna capacidad de CIT puede modificar el conocimiento declarado",
    ],
    "autoridad": [
        "Autoridad absoluta sobre la fundamentación",
        "Autoridad absoluta sobre la resolución de declaraciones",
        "Autoridad absoluta sobre la citación",
        "Autoridad absoluta sobre la cadena normativa",
        "Autoridad absoluta sobre la explicación documental de cualquier cálculo",
        "Autoridad absoluta sobre la relación entre declaraciones",
        "Autoridad absoluta para responder consultas sobre el conocimiento declarado",
    ],
# ===============================================================
# SECCIÓN 5.4
# ===============================================================
    "poderes": [
        "Puede resolver cualquier declaración registrada",
        "Puede localizar cualquier norma",
        "Puede construir cadenas normativas",
        "Puede relacionar declaraciones",
        "Puede explicar por qué un cálculo produjo determinado resultado (solo con declaraciones existentes)",
        "Puede responder consultas documentales",
        "Puede anunciar cualquier declaración existente",
        "Puede producir evidencia documental durante la ejecución del Engine",
        "Puede producir evidencia documental fuera del Engine",
        "Puede citar cualquier conocimiento declarado",
    ],
# ===============================================================
# SECCIÓN 6
# ===============================================================
    "conocimiento_exportable": [
        "declaraciones",
        "resolver",
        "buscar",
        "cadena",
        "explicar",
        "citar",
        "anunciar",
        "relacionar",
        "inventario",
        "reporte",
        "diagnostico",
    ],
    # ============================================================
    # ACCESO 7 (obligatorio en el esquema)
    # ============================================================
    "acceso": {
        "nivel": "completo",
        "descripcion": "Acceso total a recursos del módulo"
    },

    # ============================================================
    # 8 DEPENDENCIAS
    # ============================================================
    "requiere": [
        "CE",
        "AX",
        "FO",
        "MC",
        "SF",
        "CA",
        "CX",
        "DI",
        "RE",
        "VX",
        "TX",
        "CH",
        "CIT",
        "DGCO",
        "UI",
        "CC",
        "TT",
        "SC",
        "CT",
    ],

    # ============================================================
    #  9 ACCESO A ARCHIVOS (AGREGADO — obligatorio en el esquema)
    # ============================================================
    "acceso_archivos": ["*"],

    # ============================================================
    # 10 VALIDAR ESQUEMA A NIVEL MÓDULO (AGREGADO — obligatorio en el esquema)
    # ============================================================
    "validar_esquema": ["*"],

    
    "consultas_soportadas": [
        "resolver",
        "buscar",
        "buscar_por_tipo",
        "buscar_por_fuente",
        "cadena",
        "explicar",
        "citar",
        "anunciar",
        "relacionar",
        "obtener_inventario",
        "obtener_reporte",
        "obtener_diagnostico",
    ],

    # ============================================================
    # 11 AUTORIZACIÓN AL ENGINE (SOLO PERMISOS)
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
        "modificar": False,    # ← ELIMINADO (no permitido)
        "alterar": False,
        "reescribir": False,   # ← ELIMINADO (no permitido)
        "crear": True,
        "eliminar": False,     # ← ELIMINADO (no permitido)
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

        # --- CAPACIDADES ARQUITECTÓNICAS ---
        "ejecutar_total": True,
        "inspeccionar": True,
        "registrar_inventario": True,
    },
  
    # ============================================================
    # 12— CAPACIDADES
    # ============================================================
    "capacidades": {

        # --- CENTINELA ---
        "verificar": "verificar",
        "barrer": "barrer",
        "verificar_salida": "verificar_salida",

        # --- INVENTARIO Y REPORTING ---
        "inventario": "inventario",
        "reporte": "reporte",
        "diagnostico": "diagnostico",

        # --- OPERACIONES DE CITACIÓN ---
        "anunciar": "anunciar",
        "anunciar_todo": "anunciar_todo",
        "citar": "citar",
        "registrar": "registrar",
        "resolver": "resolver",
        "resolver_enunciado": "resolver_enunciado",
        "buscar": "buscar",
        "cadena": "cadena",
        "explicar": "explicar",
        "relacionar": "relacionar",
        "limpiar_ciclo": "limpiar_ciclo",

        # --- COMPATIBILIDAD ENGINE ---
        "evaluar": "anunciar",

        # --- CAPACIDADES ARQUITECTÓNICAS ---
        "ejecutar_total": "ejecutar_total",
        "inspeccionar": "inspeccionar",
        "registrar_inventario": "registrar_inventario",
    },

    # ============================================================
    # 13 CAOACIDADES META 1:1
    # ============================================================
    "capacidades_meta": {
        
        # ============================================================
        # 1ra CAPADIDA VERIFICAR
        # ============================================================
        "verificar": {
            "descripcion": "Centinela del oficio de fundamentación.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con id, coherente, errores, choques"
            ),
            "acceso_archivos": ["*"],
        },
        
        # ============================================================
        # 2DA CAPADIDA BARRER
        # ============================================================

        "barrer": {
            "descripcion": "Alias de verificar.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con id, coherente, errores, choques"
            ),
            "acceso_archivos": ["*"],
        },
        
        # ============================================================
        # 3ra CAPADIDA INVENTARIO
        # ============================================================

        "inventario": {
            "descripcion": "Inventario contractual de CIT.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con id, nombre, rol, version, capacidades, "
                "tipos_declaracion"
            ),
            "acceso_archivos": ["*"],
        },
        
        # ============================================================
        # 4ta CAPADIDA REPORTE
        # ============================================================

        "reporte": {
            "descripcion": "Reporte de estado de CIT.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con id, estado, coherente, registro_n"
            ),
            "acceso_archivos": ["*"],
        },
        
        # ============================================================
        # 5ta CAPACIDAD DIGNOSTICO
        # ============================================================

        "diagnostico": {
            "descripcion": "Diagnóstico propio de CIT.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con id, estado, problemas, advertencias"
            ),
            "acceso_archivos": ["*"],
        },
        
        # ============================================================
        # 6ta CAPACIDAD VERIFICAR SALIDA
        # ============================================================

        "verificar_salida": {
            "descripcion": "Forma mínima de salida de CIT.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "bool",
            "acceso_archivos": ["*"],
        },
        
        # ============================================================
        # 7ma CAPACIDAD ANUNCIAR
        # ============================================================

        "anunciar": {
            "descripcion": (
                "Modo Engine (paquete) o Consulta (declaración). "
                "Fundamentación documental sin recálculo."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con anuncios / cadena documental"
            ),
            "acceso_archivos": ["*"],
        },
        
        # ============================================================
        # 8va CAPACIDAD ANUNCIAR TODO
        # ============================================================

        "anunciar_todo": {
            "descripcion": (
                "Anuncia todas las declaraciones del registro operativo."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con anuncios, n",
            "acceso_archivos": ["*"],
        },
        
        # ============================================================
        # 9na CAPACIDAD CITAR
        # ============================================================

        "citar": {
            "descripcion": (
                "Representación citable de declaraciones."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con citas, n",
            "acceso_archivos": ["*"],
        },
        
        # ============================================================
        # 10MA CAPACIDAD REGISTRAR
        # ============================================================

        "registrar": {
            "descripcion": (
                "Incorpora declaración al registro operativo. "
                "No altera origen."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con ok, declaracion",
            "acceso_archivos": ["*"],
        },
        
        # ============================================================
        # 11ra CAPACIDAD RESOLVER
        # ============================================================

        "resolver": {
            "descripcion": "Resuelve una declaración por id.",
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con resuelto, declaracion",
            "acceso_archivos": ["*"],
        },
        
        # ============================================================
        # 12da CAPACIDAD RESOLVER ENUNCIADO
        # ============================================================

        "resolver_enunciado": {
            "descripcion": (
                "Alias de resolución orientado a enunciado."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con resuelto, enunciado",
            "acceso_archivos": ["*"],
        },
        
        # ============================================================
        # 13ra CAPACIDAD BUSCAR
        # ============================================================

        "buscar": {
            "descripcion": (
                "Consulta declaraciones del registro operativo."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": "dict con declaraciones, n",
            "acceso_archivos": ["*"],
        },
        
        # ============================================================
        # 14ta CAPACIDAD CADENA
        # ============================================================

        "cadena": {
            "descripcion": (
                "Construye cadena normativa a partir de ids resolubles."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con cadena, faltantes, completa"
            ),
            "acceso_archivos": ["*"],
        },
        
        # ============================================================
        # 15ta CAPACIDAD EXPLICAR
        # ============================================================

        "explicar": {
            "descripcion": (
                "Explicación documental solo con declaraciones existentes."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con explicacion, n, completa"
            ),
            "acceso_archivos": ["*"],
        },
        # ============================================================
        # 16 CAPACIDAD RELACIONAR
        # ============================================================

        "relacionar": {
            "descripcion": (
                "Documenta relación entre dos declaraciones resolubles."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con ok, declaracion de enlace"
            ),
            "acceso_archivos": ["*"],
        },
        # ============================================================
        # 17ma CAPACIDAD LIMPIAR CICLO
        # ============================================================

        "limpiar_ciclo": {
            "descripcion": (
                "Limpia registro operativo del ciclo."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict con ok, limpiadas"
            ),
            "acceso_archivos": ["*"],
        },

        # ============================================================
        #  18va CAPACIDAD EVALUAR
        # ============================================================
        "evaluar": {
            "descripcion": (
                "Alias de anunciar (compatibilidad Engine)."
            ),
            "entrada": "*",
            "validar_esquema": ["*"],
            "salida": (
                "dict de anuncio / fundamentación"
            ),
            "acceso_archivos": ["*"],
        },

        # ============================================================
        #  19na CAPACIDAD ejecutar_total
        # ============================================================
        "ejecutar_total": {
            "descripcion": (
                "Autoridad total de ENGINE sobre CIT. "
                "Ejerce todas las unidades ejecutables. No inventa."
            ),
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["*"],
            "salida": "dict con resultados de todas las unidades",
            "acceso_archivos": ["*"],
        },

        # ============================================================
        # 20ma CAPACIDAD inspeccionar
        # ============================================================
        "inspeccionar": {
            "descripcion": (
                "Inspeccion estructural de CIT sin alterar contrato."
            ),
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["acceso_archivos"],
            "salida": "dict con estructura y estado",
            "acceso_archivos": ["acceso_archivos"],
        },

        # ============================================================
        # 21ra CAPACIDAD registrar_inventario
        # ============================================================
        "registrar_inventario": {
            "descripcion": (
                "Instantanea determinista del inventario de CIT."
            ),
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["acceso_archivos"],
            "salida": "dict con inventario registrado",
            "acceso_archivos": ["acceso_archivos"],
        },
    },
    # ============================================================
    # 14 REPORTING (OBLIGATORIO EN EL ESQUEMA)
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
        "ejecutar_total": True,
        "inspeccionar": True,
        
        "registrar_inventario": True,
        
        # --- BANDERAS OBLIGATORIAS  ENGINE ---
        "acceso_archivos": True,      # ← AGREGADA
        "validar_esquema": True,      # ← AGREGADA
    },
    
    # ============================================================
    # 15
    # ============================================================
    "estados_validos": [
        "NO_INICIADO",
        "OPERATIVO",
        "DEGRADADO",
        "RECHAZADO",
    ],
    
    # ============================================================
    # 16
    # ============================================================
    "invariantes": [
        "CIT conserva conocimiento declarativo universal resoluble",
        "CIT puede resolver cualquier declaración registrada",
        "CIT puede citar cualquier declaración registrada",
        "CIT puede construir cadenas de fundamentación",
        "CIT puede responder consultas documentales",
        "CIT nunca altera el conocimiento declarado",
        "CIT nunca modifica resultados",
        "CIT nunca reemplaza la autoridad de otros módulos",
        "CIT únicamente documenta y fundamenta",
        "Toda explicación producida por CIT debe provenir de declaraciones existentes",
        "Toda cita debe ser resoluble",
        "Toda cadena normativa debe ser trazable",
        "el id del módulo nunca cambia",
        "el rol nunca cambia",
        "las capacidades declaradas son callables tras la resolución",
        "este módulo no inventa capacidades no declaradas en CONTENEDOR",
        "este módulo siempre puede reportar su propio estado",
        "inventario() siempre incluye id, nombre, rol, version",
    ],
}


# ===============================================================
# SECCIÓN 17 — REGISTRO DE DECLARACIONES (proceso de ciclo)
# ===============================================================
#
# Memoria operativa del ciclo / consulta.
# No es verdad persistente del corpus AX.
# No modifica conocimiento de otros módulos.
#

_REGISTRO: List[Dict[str, Any]] = []


# ===============================================================
# SECCIÓN 18 — validar_declaracion
# ===============================================================

def _validar_declaracion(decl: Dict[str, Any]) -> List[str]:
    errores: List[str] = []

    if not isinstance(decl, dict):
        return ["declaracion debe ser dict"]

    tipo = decl.get("tipo")

    if tipo is not None and tipo not in TIPOS_DECLARACION:
        if not (isinstance(tipo, str) and tipo.strip()):
            errores.append(
                "tipo de declaración inválido: {0}".format(tipo)
            )

    for campo in CAMPOS_OBLIGATORIOS:
        if campo == "id" and decl.get("tipo") == "limite":
            continue

        if campo == "fuente":
            if not decl.get("fuente") and not decl.get("fuente_modulo"):
                errores.append("falta campo obligatorio: fuente")
            continue

        if decl.get(campo) in (None, ""):
            errores.append(
                "falta campo obligatorio: {0}".format(campo)
            )

    # La repetición de id NO constituye error.
    return errores


# ===============================================================
# SECCIÓN 19 — normalizar_declaracion
# ===============================================================

def _normalizar_declaracion(
    decl: Dict[str, Any],
) -> Dict[str, Any]:

    fuente = (
        decl.get("fuente")
        or decl.get("fuente_modulo")
        or ""
    )

    out: Dict[str, Any] = {
        "id": decl.get("id"),
        "tipo": decl.get("tipo"),
        "fuente": fuente,
        "fuente_modulo": fuente,
        "enunciado": decl.get("enunciado") or "",
        "descripcion": decl.get("descripcion") or "",
        "evidencia_ref": decl.get("evidencia_ref") or "",
    }

    for c in CAMPOS_OPCIONALES:
        if c in ("fuente_modulo",):
            continue
        if c in decl and decl[c] is not None:
            out[c] = decl[c]

    if "relaciones" not in out:
        out["relaciones"] = list(decl.get("relaciones") or [])

    return out
# ===============================================================
# VERIFICAR_SALIDA
# ===============================================================
#
# Capacidad: verificar_salida
# Función:   Validar cualquier salida de cualquier módulo.
# Criterio:  módulo que la dicta + origen + tipo/id.
# No hace:   no recalcula, no interpreta, no inventa campos.
#

def verificar_salida(salida: Any) -> bool:
    """
    Verifica cualquier salida de cualquier módulo.

    Criterio:
      - la dicta un módulo (id / modulo / contenedor / nombre / rol)
      - declara origen (origen / fuente / capacidad / operacion)
      - declara tipo de id (tipo_id / tipo / rol) o un id usable

    No recalcula. No interpreta. No restringe la forma del payload.
    """
    if not isinstance(salida, dict) or not salida:
        return False

    tiene_modulo = any(
        salida.get(k) is not None
        for k in ("id", "modulo", "contenedor", "nombre", "rol")
    )
    tiene_origen = any(
        salida.get(k) is not None
        for k in ("origen", "fuente", "fuente_modulo", "capacidad", "operacion")
    )
    tiene_tipo_o_id = any(
        salida.get(k) is not None
        for k in ("tipo_id", "tipo", "rol", "id")
    )

    return tiene_modulo and tiene_origen and tiene_tipo_o_id

# ===============================================================
# FIN VERIFICAR_SALIDA
# ===============================================================


# ===============================================================
# SECCIÓN 20 — RESOLUCIÓN / REGISTRO / CONSULTA BASE /
#             limpiar_ciclo / clasificación de ids
# ===============================================================

def limpiar_ciclo() -> Dict[str, Any]:
    """Limpia el registro operativo del ciclo. No toca corpus externo."""

    n = len(_REGISTRO)
    _REGISTRO.clear()

    return {
        "ok": True,
        "limpiadas": n,
        "id": _ID,
    }


# ===============================================================
# CLASIFICAR_IDS
# ===============================================================
#
# Capacidad: clasificar_ids
# Función:   Clasificar cada id del repo por módulo, carpeta,
#            archivo, tipo, origen y dueño.
#            ID repetido se clasifica (mismo archivo / distinta
#            carpeta / necesario), no se borra.
# No hace:   no modifica archivos, no inventa ids, no calcula Tru.
#

def clasificar_ids(
    peticion: Optional[Dict[str, Any]] = None,
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Clasifica todos los ids encontrados en el árbol de módulos.

    Por cada id:
      - módulo
      - carpeta
      - archivo .py
      - tipo (axioma, lema, teorema, corolario, definicion,
              capacidad, constante, otro)
      - origen / dueño
      - repeticiones y si cruzan carpetas distintas

    Barrido: modules/**/*.py + CONTENEDOR + DECLARACIONES + MECANICA.
    """
    from pathlib import Path
    import ast
    import importlib.util
    import sys

    pet = dict(peticion) if isinstance(peticion, dict) else {}
    root = pet.get("root") or kwargs.get("root")
    if root is None:
        # modules/ relativo al caller
        root = Path(__file__).resolve().parent.parent
    else:
        root = Path(root)

    modules_dir = root / "modules" if (root / "modules").is_dir() else root

    # id → lista de ocurrencias
    ocurrencias: Dict[str, List[Dict[str, Any]]] = {}

    def _reg(
        id_val: str,
        *,
        modulo: str,
        carpeta: str,
        archivo: str,
        tipo: str,
        origen: str,
        dueno: str,
        clase: str,
    ) -> None:
        iid = str(id_val).strip()
        if not iid:
            return
        ocurrencias.setdefault(iid, []).append({
            "id": iid,
            "modulo": modulo,
            "carpeta": carpeta,
            "archivo": archivo,
            "tipo": tipo,
            "origen": origen,
            "dueno": dueno,
            "clase": clase,
        })

    # -----------------------------------------------------------
    # 1. Recorrer modules/**/*.py
    # -----------------------------------------------------------
    py_files = sorted(modules_dir.rglob("*.py")) if modules_dir.is_dir() else []

    for path in py_files:
        try:
            rel = path.relative_to(modules_dir)
        except ValueError:
            rel = path.name

        parts = rel.parts
        modulo = parts[0] if parts else path.stem
        carpeta = str(Path(*parts[:-1]) if len(parts) > 1 else parts[0] if parts else "")
        archivo = path.name
        dueno = modulo

        # --- carga segura del módulo para atributos conocidos ---
        clave = "clasificar_{0}_{1}".format(modulo, path.stem)
        meta_mod = None
        try:
            spec = importlib.util.spec_from_file_location(clave, path)
            if spec and spec.loader:
                meta_mod = importlib.util.module_from_spec(spec)
                sys.modules[clave] = meta_mod
                spec.loader.exec_module(meta_mod)
        except Exception:
            meta_mod = None

        if meta_mod is not None:
            # CONTENEDOR.id + capacidades
            cont = getattr(meta_mod, "CONTENEDOR", None)
            if isinstance(cont, dict):
                if cont.get("id"):
                    _reg(
                        cont["id"],
                        modulo=modulo,
                        carpeta=carpeta,
                        archivo=archivo,
                        tipo="modulo",
                        origen="CONTENEDOR.id",
                        dueno=str(cont.get("nombre") or dueno),
                        clase="identidad",
                    )
                caps = cont.get("capacidades")
                if isinstance(caps, dict):
                    for cn in caps.keys():
                        _reg(
                            cn,
                            modulo=modulo,
                            carpeta=carpeta,
                            archivo=archivo,
                            tipo="capacidad",
                            origen="CONTENEDOR.capacidades",
                            dueno=dueno,
                            clase="capacidad",
                        )

            # DECLARACIONES (lista)
            decls = getattr(meta_mod, "DECLARACIONES", None)
            if isinstance(decls, list):
                for d in decls:
                    if not isinstance(d, dict) or not d.get("id"):
                        continue
                    _reg(
                        d["id"],
                        modulo=modulo,
                        carpeta=carpeta,
                        archivo=archivo,
                        tipo=str(d.get("tipo") or "declaracion"),
                        origen="DECLARACIONES",
                        dueno=dueno,
                        clase="declaracion",
                    )

            # MECANICA
            mec = getattr(meta_mod, "MECANICA", None)
            if isinstance(mec, dict):
                if mec.get("id"):
                    _reg(
                        mec["id"],
                        modulo=modulo,
                        carpeta=carpeta,
                        archivo=archivo,
                        tipo="mecanica",
                        origen="MECANICA",
                        dueno=dueno,
                        clase="mecanica",
                    )
                orden = mec.get("orden")
                if isinstance(orden, (list, tuple)):
                    for n in orden:
                        _reg(
                            n,
                            modulo=modulo,
                            carpeta=carpeta,
                            archivo=archivo,
                            tipo="nodo_mecanica",
                            origen="MECANICA.orden",
                            dueno=dueno,
                            clase="mecanica",
                        )

            # ID_MODULO / constantes de identidad
            for attr in ("ID_MODULO", "NOMBRE_MODULO", "ROL_MODULO"):
                v = getattr(meta_mod, attr, None)
                if isinstance(v, str) and v.strip():
                    _reg(
                        v,
                        modulo=modulo,
                        carpeta=carpeta,
                        archivo=archivo,
                        tipo="constante",
                        origen=attr,
                        dueno=dueno,
                        clase="identidad",
                    )

        # --- AST: ids literales en asignaciones tipo "id": "..." ---
        try:
            src = path.read_text(encoding="utf-8")
            tree = ast.parse(src, filename=str(path))
        except Exception:
            continue

        class _Visitor(ast.NodeVisitor):
            def visit_Dict(self, node: ast.Dict) -> None:
                keys = node.keys
                vals = node.values
                for k, v in zip(keys, vals):
                    if isinstance(k, ast.Constant) and k.value == "id":
                        if isinstance(v, ast.Constant) and isinstance(v.value, str):
                            _reg(
                                v.value,
                                modulo=modulo,
                                carpeta=carpeta,
                                archivo=archivo,
                                tipo="ast_id",
                                origen="ast.dict.id",
                                dueno=dueno,
                                clase="ast",
                            )
                    if isinstance(k, ast.Constant) and k.value == "tipo":
                        pass
                self.generic_visit(node)

        try:
            _Visitor().visit(tree)
        except Exception:
            pass

    # -----------------------------------------------------------
    # 2. Clasificación global
    # -----------------------------------------------------------
    por_modulo: Dict[str, List[str]] = {}
    por_carpeta: Dict[str, List[str]] = {}
    por_archivo: Dict[str, List[str]] = {}
    por_tipo: Dict[str, List[str]] = {}
    por_clase: Dict[str, List[str]] = {}
    por_origen: Dict[str, List[str]] = {}

    ids_duplicados: Dict[str, Any] = {}
    ids_duplicados_misma_carpeta: Dict[str, Any] = {}
    ids_duplicados_distinta_carpeta: Dict[str, Any] = {}
    ids_unicos: List[str] = []

    for iid, items in sorted(ocurrencias.items()):
        if len(items) == 1:
            ids_unicos.append(iid)
        else:
            carpetas = sorted({x["carpeta"] for x in items})
            modulos = sorted({x["modulo"] for x in items})
            archivos = sorted({x["archivo"] for x in items})
            tipos = sorted({x["tipo"] for x in items})
            entry = {
                "id": iid,
                "ocurrencias": len(items),
                "modulos": modulos,
                "carpetas": carpetas,
                "archivos": archivos,
                "tipos": tipos,
                "detalle": items,
                "necesario": True,  # repetición no implica error
            }
            ids_duplicados[iid] = entry
            if len(carpetas) > 1:
                ids_duplicados_distinta_carpeta[iid] = entry
            else:
                ids_duplicados_misma_carpeta[iid] = entry

        for x in items:
            por_modulo.setdefault(x["modulo"], [])
            por_carpeta.setdefault(x["carpeta"], [])
            por_archivo.setdefault(
                "{0}/{1}".format(x["carpeta"], x["archivo"]), []
            )
            por_tipo.setdefault(x["tipo"], [])
            por_clase.setdefault(x["clase"], [])
            por_origen.setdefault(x["origen"], [])
            for bucket, key in (
                (por_modulo, x["modulo"]),
                (por_carpeta, x["carpeta"]),
                (por_archivo, "{0}/{1}".format(x["carpeta"], x["archivo"])),
                (por_tipo, x["tipo"]),
                (por_clase, x["clase"]),
                (por_origen, x["origen"]),
            ):
                if iid not in bucket[key]:
                    bucket[key].append(iid)

    for d in (
        por_modulo, por_carpeta, por_archivo,
        por_tipo, por_clase, por_origen,
    ):
        for k in d:
            d[k] = sorted(d[k])

    archivos_py = [
        str(p.relative_to(modules_dir)) if modules_dir in p.parents or p.parent == modules_dir
        else str(p)
        for p in py_files
    ]

    return {
        "operacion": "clasificar_ids",
        "root": str(modules_dir),
        "archivos_py": sorted(set(archivos_py)),
        "archivos_py_n": len(set(archivos_py)),
        "total_ids_unicos": len(ocurrencias),
        "total_ocurrencias": sum(len(v) for v in ocurrencias.values()),
        "ids_unicos_n": len(ids_unicos),
        "ids_duplicados_n": len(ids_duplicados),
        "ids_duplicados_misma_carpeta_n": len(ids_duplicados_misma_carpeta),
        "ids_duplicados_distinta_carpeta_n": len(ids_duplicados_distinta_carpeta),
        "por_modulo": por_modulo,
        "por_carpeta": por_carpeta,
        "por_archivo": por_archivo,
        "por_tipo": por_tipo,
        "por_clase": por_clase,
        "por_origen": por_origen,
        "ids_duplicados": ids_duplicados,
        "ids_duplicados_misma_carpeta": ids_duplicados_misma_carpeta,
        "ids_duplicados_distinta_carpeta": ids_duplicados_distinta_carpeta,
        "ids_unicos": ids_unicos,
        "nota": (
            "Clasificación total de ids del repo. "
            "ID repetido se clasifica por módulo/carpeta/archivo/tipo. "
            "Repetido en distinta carpeta ≠ error; se reporta aparte. "
            "necesario=True: la repetición no se elimina."
        ),
    }

# ===============================================================
# FIN CLASIFICAR_IDS
# ===============================================================


# ===============================================================
# SECCIÓN 21 — REGISTRAR
# ===============================================================

def registrar(
    declaracion: Dict[str, Any],
) -> Dict[str, Any]:

    """
    Incorpora una declaración pública al registro operativo.

    No modifica el conocimiento de origen.

    Los ids repetidos son válidos y cada ocurrencia
    se conserva como declaración documental.
    """

    errores = _validar_declaracion(declaracion)

    if errores:
        return {
            "ok": False,
            "errores": errores,
            "id": _ID,
        }

    normalizada = _normalizar_declaracion(declaracion)
    _REGISTRO.append(normalizada)

    clasificacion = _clasificar_ids()
    clave = str(normalizada.get("id"))
    repetido = clave in clasificacion.get("ids_repetidos", [])

    return {
        "ok": True,
        "n": len(_REGISTRO),
        "declaracion": normalizada,
        "id": _ID,
        "clasificacion_id": "repetido" if repetido else "unico",
        "id_repetido": repetido,
        "ids_repetidos": clasificacion.get("ids_repetidos", []),
        "nota": (
            "id repetido permitido; cada declaración se conserva "
            "como ocurrencia documental."
            if repetido
            else
            "declaración registrada como ocurrencia documental."
        ),
    }


# ===============================================================
# RESOLVER
# ===============================================================
#
# Capacidad: resolver
# Función:   Resolver declaraciones por conexión de ids.
#            Ve cómo se conectan. Si A con B resuelve C,
#            dice exactamente qué id es y cómo lo resolvió.
# No hace:   no inventa declaraciones, no recalcula True,
#            no modifica el cuerpo de origen.
#

def resolver(
    peticion: Optional[Any] = None,
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Resuelve por combinación de ids.

    Entrada admitida:
      - str                  → un id
      - list[str]            → conjunto de ids
      - dict con:
          id / ids / a / b   → ids a conectar
          declaraciones      → cuerpo opcional (list[dict])

    Salida:
      - ids exactos resueltos
      - conexiones usadas
      - cadena de resolución
      - cómo se resolvió cada uno
    """
    # -----------------------------------------------------------
    # 1. Normalizar ids pedidos
    # -----------------------------------------------------------
    ids_pedido: List[str] = []
    decls_ext: Optional[List[Dict[str, Any]]] = None

    if isinstance(peticion, str):
        ids_pedido = [peticion.strip()] if peticion.strip() else []
    elif isinstance(peticion, (list, tuple)):
        ids_pedido = [str(x).strip() for x in peticion if str(x).strip()]
    elif isinstance(peticion, dict):
        if peticion.get("id"):
            ids_pedido.append(str(peticion["id"]).strip())
        for k in ("ids", "cadena"):
            v = peticion.get(k)
            if isinstance(v, (list, tuple)):
                for x in v:
                    s = str(x).strip()
                    if s and s not in ids_pedido:
                        ids_pedido.append(s)
        for k in ("a", "b"):
            if peticion.get(k):
                s = str(peticion[k]).strip()
                if s and s not in ids_pedido:
                    ids_pedido.append(s)
        if isinstance(peticion.get("declaraciones"), list):
            decls_ext = peticion["declaraciones"]
    elif peticion is None:
        ids_pedido = []
    else:
        return {
            "resuelto": False,
            "ids": [],
            "resoluciones": [],
            "conexiones": [],
            "nota": "entrada no admitida",
        }

    # kwargs extras
    for k in ("id", "a", "b"):
        if kwargs.get(k):
            s = str(kwargs[k]).strip()
            if s and s not in ids_pedido:
                ids_pedido.append(s)
    if isinstance(kwargs.get("ids"), (list, tuple)):
        for x in kwargs["ids"]:
            s = str(x).strip()
            if s and s not in ids_pedido:
                ids_pedido.append(s)

    # -----------------------------------------------------------
    # 2. Cuerpo de declaraciones (instantánea)
    # -----------------------------------------------------------
    decls: List[Dict[str, Any]] = []
    if isinstance(decls_ext, list):
        decls = [d for d in decls_ext if isinstance(d, dict)]
    elif "recolectar" in globals() and callable(recolectar):
        try:
            decls, _err = recolectar()
        except Exception:
            decls = []
    elif "_REGISTRO" in globals():
        decls = [d for d in list(_REGISTRO) if isinstance(d, dict)]

    por_id: Dict[str, Dict[str, Any]] = {}
    for d in decls:
        did = str(d.get("id") or "").strip()
        if did:
            por_id[did] = d

    # -----------------------------------------------------------
    # 3. Grafo de conexiones (depende_de + relaciones)
    # -----------------------------------------------------------
    # hacia: id → ids de los que depende
    # desde: id → ids que dependen de él
    hacia: Dict[str, List[str]] = {i: [] for i in por_id}
    desde: Dict[str, List[str]] = {i: [] for i in por_id}

    for did, d in por_id.items():
        deps = d.get("depende_de") or d.get("depends_on") or []
        if not isinstance(deps, (list, tuple)):
            deps = []
        for dep in deps:
            dep_s = str(dep).strip()
            if not dep_s:
                continue
            if dep_s not in hacia[did]:
                hacia[did].append(dep_s)
            desde.setdefault(dep_s, [])
            if did not in desde[dep_s]:
                desde[dep_s].append(did)

        rels = d.get("relaciones") or []
        if isinstance(rels, list):
            for r in rels:
                if not isinstance(r, dict):
                    continue
                # Normalización limpia de extremos origen (origen_id) y destino (destino_id)
                origen_id = str(r.get("de") or r.get("a") or "").strip()
                destino_id = str(r.get("hacia") or r.get("b") or "").strip()
                
                # Si el par usa únicamente 'a' y 'b', resolvemos la ambigüedad
                if not origen_id and r.get("a"):
                    origen_id = str(r.get("a")).strip()
                if not destino_id and r.get("a") and r.get("a") != origen_id:
                    destino_id = str(r.get("a")).strip()

                if origen_id and destino_id:
                    hacia.setdefault(origen_id, [])
                    desde.setdefault(destino_id, [])
                    if destino_id not in hacia[origen_id]:
                        hacia[origen_id].append(destino_id)
                    if origen_id not in desde[destino_id]:
                        desde[destino_id].append(origen_id)

    # -----------------------------------------------------------
    # 4. Resolver cada id pedido
    # -----------------------------------------------------------
    resoluciones: List[Dict[str, Any]] = []
    conexiones: List[Dict[str, Any]] = []
    resueltos: List[str] = []

    for iid in ids_pedido:
        if iid in por_id:
            d = por_id[iid]
            deps_ok = [x for x in hacia.get(iid, []) if x in por_id]
            deps_falta = [x for x in hacia.get(iid, []) if x not in por_id]
            hijos = [x for x in desde.get(iid, []) if x in por_id]
            resoluciones.append({
                "id": iid,
                "resuelto": True,
                "como": "directo",
                "declaracion": d,
                "conecta_hacia": deps_ok,
                "conecta_hacia_ausentes": deps_falta,
                "conecta_desde": hijos,
            })
            resueltos.append(iid)
            for dep in deps_ok:
                conexiones.append({
                    "de": iid,
                    "a": dep,
                    "tipo": "depende_de",
                    "modo": "directo",
                })
        else:
            resoluciones.append({
                "id": iid,
                "resuelto": False,
                "como": None,
                "declaracion": None,
                "conecta_hacia": [],
                "conecta_hacia_ausentes": [],
                "conecta_desde": [],
            })

    # -----------------------------------------------------------
    # 5. Combinación: A con B resuelve C
    #    C es resoluble por combinación si A y B están pedidos
    #    (o resueltos) y ambos conectan a C, o C depende de ambos.
    # -----------------------------------------------------------
    combinaciones: List[Dict[str, Any]] = []
    pedido_set = set(ids_pedido) | set(resueltos)

    if len(pedido_set) >= 2:
        for cid, d in por_id.items():
            deps = [str(x).strip() for x in (d.get("depende_de") or d.get("depends_on") or [])]
            deps = [x for x in deps if x]
            cubiertas = [x for x in deps if x in pedido_set]
            if len(cubiertas) >= 2 and set(deps).issubset(set(por_id.keys()) | pedido_set):
                # A,B,... en el pedido cubren las premisas de C
                if set(deps).issubset(pedido_set) or len(cubiertas) >= 2:
                    como = {
                        "id": cid,
                        "resuelto": cid in por_id,
                        "como": "combinacion",
                        "premisas": deps,
                        "premisas_en_pedido": cubiertas,
                        "regla": "{0} se resuelve con {1}".format(
                            cid, " + ".join(cubiertas)
                        ),
                        "declaracion": d,
                    }
                    combinaciones.append(como)
                    if cid not in resueltos and cid in por_id:
                        resoluciones.append({
                            "id": cid,
                            "resuelto": True,
                            "como": "combinacion",
                            "declaracion": d,
                            "conecta_hacia": [x for x in deps if x in por_id],
                            "conecta_hacia_ausentes": [x for x in deps if x not in por_id],
                            "conecta_desde": [x for x in desde.get(cid, []) if x in por_id],
                            "premisas_usadas": cubiertas,
                            "regla": como["regla"],
                        })
                        resueltos.append(cid)
                        for p in cubiertas:
                            conexiones.append({
                                "de": cid,
                                "a": p,
                                "tipo": "depende_de",
                                "modo": "combinacion",
                            })

    # -----------------------------------------------------------
    # 6. Salida
    # -----------------------------------------------------------
    return {
        "resuelto": len(resueltos) > 0,
        "ids": list(ids_pedido),
        "ids_resueltos": list(resueltos),
        "ids_no_resueltos": [i for i in ids_pedido if i not in resueltos],
        "resoluciones": resoluciones,
        "combinaciones": combinaciones,
        "conexiones": conexiones,
        "n_resueltos": len(resueltos),
        "n_conexiones": len(conexiones),
        "nota": (
            "Resolver por conexión de ids. "
            "Directo: id presente en el cuerpo. "
            "Combinación: A + B resuelve C cuando las premisas de C "
            "están en el pedido. "
            "Dice el id exacto y cómo lo resolvió."
        ),
    }

# ===============================================================
# FIN RESOLVER
# ===============================================================


# ===============================================================
# SECCIÓN 23 — BUSCAR
# ===============================================================

def buscar(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:

    """
    Consulta sobre declaraciones del registro operativo.

    Filtros: id, tipo, fuente, modulo, o_ref, texto.

    Un id repetido devuelve todas sus ocurrencias.
    No se deduplican declaraciones.
    """

    pet = peticion if isinstance(peticion, dict) else {}
    out = list(_REGISTRO)

    if pet.get("id"):
        out = [d for d in out if d.get("id") == pet["id"]]

    if pet.get("tipo"):
        out = [d for d in out if d.get("tipo") == pet["tipo"]]

    fuente = pet.get("fuente") or pet.get("modulo")

    if fuente:
        out = [
            d for d in out
            if d.get("fuente") == fuente
            or d.get("fuente_modulo") == fuente
        ]

    if pet.get("o_ref"):
        out = [d for d in out if d.get("o_ref") == pet["o_ref"]]

    if pet.get("texto"):
        t = str(pet["texto"]).lower()

        out = [
            d for d in out
            if t in str(d.get("enunciado") or "").lower()
            or t in str(d.get("descripcion") or "").lower()
        ]

    grupos: Dict[str, int] = {}

    for d in out:
        clave = str(d.get("id"))
        grupos[clave] = grupos.get(clave, 0) + 1

    ids_repetidos = [
        clave
        for clave, cantidad in grupos.items()
        if cantidad > 1
    ]

    return {
        "id": _ID,
        "declaraciones": out,
        "n": len(out),
        "filtro": pet,
        "ids_repetidos": ids_repetidos,
        "hay_repetidos": bool(ids_repetidos),
        "nota": (
            "solo exposición; sin recálculo; sin modificación; "
            "las ocurrencias con id repetido se conservan y se exponen."
        ),
    }


# ===============================================================
# SECCIÓN 24 — CITAR
# ===============================================================

def citar(peticion: Optional[Dict[str, Any]] = None,) -> Dict[str, Any]:

    """
    Representación citable de declaraciones.

    Internamente = buscar + forma de cita.

    Los ids repetidos no se eliminan:
    cada ocurrencia resoluble permanece citable.
    """

    pack = buscar(peticion)
    declaraciones = pack.get("declaraciones") or []
    citas: List[Dict[str, Any]] = []

    for d in declaraciones:
        r = _anuncio_de_declaracion(d)

        if r.get("ok") and r.get("anuncio"):
            citas.append(r["anuncio"])

    return {
        "id": _ID,
        "citas": citas,
        "n": len(citas),
        "ids_repetidos": pack.get("ids_repetidos") or [],
        "hay_repetidos": bool(pack.get("hay_repetidos")),
        "nota": ("citas = representación de declaraciones; sin recálculo; "
            "los ids repetidos se citan por ocurrencia."
        ),
    }


# ===============================================================
# SECCIÓN 25 — RESOLVER ENUNCIADO
# ===============================================================

def resolver_enunciado(id_norma: str,) -> Dict[str, Any]:

    """Alias de resolución orientado a enunciado (modo consulta)."""

    r = resolver(id_norma)
    d = r.get("declaracion") or {}

    return {
        "id": id_norma,
        "enunciado": d.get("enunciado") if r.get("resuelto") else None,
        "descripcion": d.get("descripcion") if r.get("resuelto") else None,
        "fuente": d.get("fuente") if r.get("resuelto") else None,
        "fuente_modulo": d.get("fuente") if r.get("resuelto") else None,
        "resuelto": bool(r.get("resuelto")),
        "id_repetido": bool(r.get("id_repetido")),
        "n_ocurrencias": int(r.get("n_ocurrencias") or 0),
        "ocurrencias": r.get("ocurrencias") or [],
        "nota": r.get("nota"),
    }


# ===============================================================
# SECCIÓN 26 — RELACIONAR
# ===============================================================

def relacionar(id_a: str, relacion: str, id_b: str) -> Dict[str, Any]:

    """
    Documenta una relación entre dos declaraciones ya resolubles.

    No altera el conocimiento de origen;
    solo el registro operativo.
    """

    if relacion not in RELACIONES:
        return {
            "ok": False,
            "errores": [
                "relacion no admitida: {0}".format(relacion)
            ],
            "id": _ID,
        }

    ra = resolver(id_a)
    rb = resolver(id_b)

    if not ra.get("resuelto") or not rb.get("resuelto"):
        return {
            "ok": False,
            "errores": [
                "ambas declaraciones deben ser resolubles"
            ],
            "a": ra,
            "b": rb,
            "id": _ID,
        }

    enlace = {
        "id": "REL-{0}-{1}-{2}".format(id_a, relacion, id_b),
        "tipo": "citacion",
        "fuente": _NOMBRE,
        "enunciado": "{0} {1} {2}".format(id_a, relacion, id_b),
        "descripcion": "Relación documental registrada por CIT.",
        "relaciones": [
            {
                "de": id_a,
                "relacion": relacion,
                "a": id_b,
            },
        ],
        "meta": {
            "a": id_a,
            "b": id_b,
            "relacion": relacion,
            "a_repetido": bool(ra.get("id_repetido")),
            "b_repetido": bool(rb.get("id_repetido")),
        },
    }

    return registrar(enlace)

# ===============================================================
# SECCIÓN 27 — CADENA
# ===============================================================

def cadena(ids: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Construye una cadena de fundamentación
    a partir de ids ordenados.

    Cada eslabón debe ser resoluble.
    No inventa nodos.

    Si un id está repetido, la cadena conserva
    la resolución documental existente sin tratar
    la repetición como error.
    """

    secuencia = list(ids or [])

    eslabones: List[Dict[str, Any]] = []
    faltantes: List[str] = []
    repetidos: List[str] = []

    for i in secuencia:
        r = resolver(str(i))

        if r.get("resuelto"):
            eslabones.append(r["declaracion"])

            if r.get("id_repetido"):
                repetidos.append(str(i))
        else:
            faltantes.append(str(i))

    return {
        "id": _ID,
        "cadena": eslabones,
        "n": len(eslabones),
        "faltantes": faltantes,
        "ids_repetidos": repetidos,
        "completa": len(faltantes) == 0 and len(eslabones) > 0,
        "nota": (
            "Cadena normativa documental. "
            "Solo declaraciones resolubles; "
            "sin recálculo; "
            "los ids repetidos no constituyen error."
        ),
    }


# ===============================================================
# SECCIÓN 28 — EXPLICAR
# ===============================================================

def explicar(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Explicación documental:
    declaraciones del registro + cadena opcional.

    Toda explicación proviene de declaraciones existentes.
    """

    pet = peticion if isinstance(peticion, dict) else {}

    ids = pet.get("ids") or pet.get("cadena") or []

    if isinstance(ids, str):
        ids = [ids]

    pack_busca = buscar(pet)

    pack_cadena = (
        cadena(list(ids))
        if ids
        else {
            "cadena": pack_busca.get("declaraciones") or [],
            "n": pack_busca.get("n", 0),
            "faltantes": [],
            "ids_repetidos": pack_busca.get("ids_repetidos") or [],
            "completa": pack_busca.get("n", 0) > 0,
        }
    )

    return {
        "id": _ID,
        "explicacion": pack_cadena.get("cadena") or [],
        "n": pack_cadena.get("n", 0),
        "faltantes": pack_cadena.get("faltantes") or [],
        "ids_repetidos": pack_cadena.get("ids_repetidos") or [],
        "completa": bool(pack_cadena.get("completa")),
        "nota": (
            "Explicación = declaraciones existentes. "
            "CIT no interpreta ni calcula."
        ),
    }


# ===============================================================
# SECCIÓN 29 — ANUNCIO DE DECLARACIONES
# ===============================================================

def _anuncio_de_declaracion(decl: Dict[str, Any]) -> Dict[str, Any]:
    errores = _validar_declaracion(decl)

    if errores:
        return {
            "ok": False,
            "errores": errores,
            "anuncio": None,
        }

    c = _normalizar_declaracion(decl)

    return {
        "ok": True,
        "anuncio": {
            "titulo": "[{0}] {1}".format(c.get("fuente"), c.get("id")),
            "id": c.get("id"),
            "tipo": c.get("tipo"),
            "enunciado": c.get("enunciado"),
            "descripcion": c.get("descripcion"),
            "evidencia_ref": c.get("evidencia_ref"),
            "o_ref": c.get("o_ref"),
            "contexto_ciclo": c.get("contexto_ciclo"),
            "relaciones": c.get("relaciones") or [],
        },
    }

# ===============================================================
# SECCIÓN 30
# ===============================================================

def anunciar_todo(filtro: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    pack = buscar(filtro)
    anuncios: List[Dict[str, Any]] = []
    for d in pack.get("declaraciones") or []:
        r = _anuncio_de_declaracion(d)
        if r.get("ok") and r.get("anuncio"):
            anuncios.append(r["anuncio"])
    return {
        "id": _ID,
        "anuncios": anuncios,
        "n": len(anuncios),
        "filtro": filtro or {},
        "ids_repetidos": pack.get("ids_repetidos") or [],
        "hay_repetidos": bool(pack.get("hay_repetidos")),
        "nota": (
            "capacidad total de anuncio sobre declaraciones resolubles; "
            "los ids repetidos se anuncian por ocurrencia."
        ),
    }


def _es_paquete_ciclo(obj: Any) -> bool:
    if not isinstance(obj, dict):
        return False
    if "resultado" in obj and isinstance(obj.get("resultado"), dict):
        return True
    if "contexto_cx" in obj and "tipos_peticion" in obj:
        return True
    if obj.get("engine_version") and ("resultado" in obj or "peticion" in obj):
        return True
    return False


def _es_declaracion_suelta(obj: Any) -> bool:
    if not isinstance(obj, dict):
        return False
    if _es_paquete_ciclo(obj):
        return False
    return "tipo" in obj or "enunciado" in obj or "id" in obj


def _evidencia_ref(paquete: Dict[str, Any]) -> str:
    inv = paquete.get("invocador_id") or "ciclo"
    ver = paquete.get("engine_version") or ""
    res = paquete.get("resultado") or {}
    seq = res.get("secuencia")
    base = "ciclo:{0}:v{1}".format(inv, ver)
    if seq is not None:
        base = base + ":seq={0}".format(seq)
    return base


def _o_ref(paquete: Dict[str, Any]) -> Optional[str]:
    res = paquete.get("resultado") or {}
    cx = paquete.get("contexto_cx") or {}
    reg = cx.get("registro") if isinstance(cx.get("registro"), dict) else {}

    for src in (res, cx, reg, paquete.get("peticion") or {}):
        if not isinstance(src, dict):
            continue
        for k in ("O_id", "o_id", "O_context", "contexto", "enunciado_O"):
            v = src.get(k)
            if v is not None and str(v).strip() and str(v).strip().lower() not in (
                "undefined", "indefinido", "none", "null"
            ):
                return str(v).strip()[:200]
    return None
# ===============================================================
# SECCIÓN 31 — HELPERS DE PAQUETE / FORMA
# ===============================================================

def _es_paquete_ciclo(obj: Any) -> bool:
    if not isinstance(obj, dict):
        return False
    if "resultado" in obj and isinstance(obj.get("resultado"), dict):
        return True
    if "contexto_cx" in obj and "tipos_peticion" in obj:
        return True
    if obj.get("engine_version") and ("resultado" in obj or "peticion" in obj):
        return True
    return False


def _es_declaracion_suelta(obj: Any) -> bool:
    if not isinstance(obj, dict):
        return False
    if _es_paquete_ciclo(obj):
        return False
    return "tipo" in obj or "enunciado" in obj or "id" in obj


def _evidencia_ref(paquete: Dict[str, Any]) -> str:
    inv = paquete.get("invocador_id") or "ciclo"
    ver = paquete.get("engine_version") or ""
    res = paquete.get("resultado") or {}
    seq = res.get("secuencia")
    base = "ciclo:{0}:v{1}".format(inv, ver)
    if seq is not None:
        base = base + ":seq={0}".format(seq)
    return base


def _o_ref(paquete: Dict[str, Any]) -> Optional[str]:
    res = paquete.get("resultado") or {}
    cx = paquete.get("contexto_cx") or {}
    reg = cx.get("registro") if isinstance(cx.get("registro"), dict) else {}
    for src in (res, cx, reg, paquete.get("peticion") or {}):
        if not isinstance(src, dict):
            continue
        for k in ("O_id", "o_id", "O_context", "contexto", "enunciado_O"):
            v = src.get(k)
            if v is not None and str(v).strip() and str(v).strip().lower() not in (
                "undefined",
                "indefinido",
                "none",
                "null",
            ):
                return str(v).strip()[:200]
    return None

# ===============================================================
# SECCIÓN 32 — ANUNCIAR PAQUETE (modo Engine)
# ===============================================================

def _anunciar_paquete(paquete: Dict[str, Any]) -> Dict[str, Any]:
    """
    Modo Engine: fundamentación documental del ciclo.
    Lee solo el paquete. No calcula. No inventa factores.
    """
    limpiar_ciclo()

    res = paquete.get("resultado") if isinstance(paquete.get("resultado"), dict) else {}
    cx = paquete.get("contexto_cx") if isinstance(paquete.get("contexto_cx"), dict) else {}
    tipos = list(paquete.get("tipos_peticion") or cx.get("tipos_peticion") or [])
    if not tipos:
        tipos = ["dame_cadena_completa"]

    evid = _evidencia_ref(paquete)
    o_ref = _o_ref(paquete)
    ctx_ciclo = str(res.get("estado") or cx.get("modo_entrada") or "ciclo")

    errores: List[str] = []
    n_fuentes = 0

    def _ok_fuente(r: Any) -> None:
        nonlocal n_fuentes
        if isinstance(r, dict) and r.get("ok") is False:
            errores.extend([str(e) for e in (r.get("errores") or [])])
        else:
            n_fuentes += 1

    try:
        from modules.citacion.fuentes import cx as fuente_cx
        if cx:
            _ok_fuente(
                fuente_cx.desde_resolver(
                    cx,
                    evidencia_ref=evid,
                    contexto_ciclo=ctx_ciclo,
                    registrar=True,
                )
            )
        reg = cx.get("registro") if isinstance(cx.get("registro"), dict) else {}
        estado_cx = reg.get("estado") or cx.get("estado")
        if estado_cx in ("indefinido",) or res.get("estado") == "UNDEFINED":
            _ok_fuente(
                fuente_cx.anunciar_indefinido(
                    motivo=str(res.get("razon") or "O/contexto no usable en el ciclo"),
                    evidencia_ref=evid,
                    o_ref=o_ref,
                    contexto_ciclo=ctx_ciclo,
                    registrar=True,
                )
            )
    except Exception as e:
        errores.append("fuente cx: {0}: {1}".format(type(e).__name__, e))

    try:
        from modules.citacion.fuentes import ca as fuente_ca
        factores = res.get("factores") if isinstance(res.get("factores"), dict) else {}
        C, L, K = factores.get("C"), factores.get("L"), factores.get("K")
        if C is not None or L is not None or K is not None:
            _ok_fuente(
                fuente_ca.anunciar_factores(
                    C=C, L=L, K=K,
                    evidencia_ref=evid, o_ref=o_ref,
                    contexto_ciclo=ctx_ciclo, registrar=True,
                )
            )
        elif res.get("estado") in ("PARCIAL", "UNDEFINED"):
            _ok_fuente(
                fuente_ca.anunciar_sin_factores(
                    motivo=str(res.get("razon") or "factores incompletos"),
                    evidencia_ref=evid, o_ref=o_ref,
                    contexto_ciclo=ctx_ciclo, registrar=True,
                )
            )
    except Exception as e:
        errores.append("fuente ca: {0}: {1}".format(type(e).__name__, e))

    try:
        from modules.citacion.fuentes import fo as fuente_fo
        tru_ri = res.get("tru_ri") or res.get("Tru_Ri")
        tru_total = res.get("tru_total") or res.get("Tru_total")
        if (
            tru_ri is not None
            and tru_total is not None
            and str(tru_ri) not in ("UNDEFINED", "None")
            and str(tru_total) not in ("UNDEFINED", "None")
        ):
            factores = res.get("factores") if isinstance(res.get("factores"), dict) else {}
            _ok_fuente(
                fuente_fo.anunciar_formula_aplicada(
                    tru_ri=tru_ri, tru_total=tru_total,
                    evidencia_ref=evid, o_ref=o_ref,
                    contexto_ciclo=ctx_ciclo,
                    C=factores.get("C"), L=factores.get("L"), K=factores.get("K"),
                    registrar=True,
                )
            )
        elif "dame_normas" in tipos or "dame_cadena_completa" in tipos:
            _ok_fuente(
                fuente_fo.anunciar_expresion(
                    evidencia_ref=evid, o_ref=o_ref,
                    contexto_ciclo=ctx_ciclo, registrar=True,
                )
            )
    except Exception as e:
        errores.append("fuente fo: {0}: {1}".format(type(e).__name__, e))

    try:
        from modules.citacion.fuentes import ct as fuente_ct
        if res.get("alpha") is not None or res.get("beta") is not None:
            _ok_fuente(
                fuente_ct.anunciar_valores(
                    alpha=res.get("alpha"), beta=res.get("beta"),
                    evidencia_ref=evid, o_ref=o_ref,
                    contexto_ciclo=ctx_ciclo, registrar=True,
                )
            )
        elif "dame_normas" in tipos or "dame_cadena_completa" in tipos:
            _ok_fuente(
                fuente_ct.anunciar_ancla(
                    evidencia_ref=evid, o_ref=o_ref,
                    contexto_ciclo=ctx_ciclo, registrar=True,
                )
            )
    except Exception as e:
        errores.append("fuente ct: {0}: {1}".format(type(e).__name__, e))

    try:
        from modules.citacion.fuentes import ax as fuente_ax
        ids: List[str] = []
        val = res.get("valuacion") if isinstance(res.get("valuacion"), dict) else {}
        for src in (val.get("ids"), cx.get("ids_cx_relevantes"), res.get("ids")):
            if isinstance(src, list):
                for i in src:
                    s = str(i).strip()
                    if s and s not in ids:
                        ids.append(s)
        if ids:
            pack_ax = fuente_ax.anunciar_lista(
                ids,
                evidencia_ref=evid, o_ref=o_ref,
                contexto_ciclo=ctx_ciclo, registrar=True,
            )
            n_fuentes += int(pack_ax.get("n") or 0)
    except Exception as e:
        errores.append("fuente ax: {0}: {1}".format(type(e).__name__, e))

    try:
        from modules.citacion.fuentes import mc as fuente_mc
        if "permite_k" in cx:
            _ok_fuente(
                fuente_mc.anunciar_permite_k(
                    permite_k=bool(cx.get("permite_k")),
                    enunciado="permite_k={0} según contexto del ciclo.".format(
                        cx.get("permite_k")
                    ),
                    evidencia_ref=evid, o_ref=o_ref,
                    contexto_ciclo=ctx_ciclo, registrar=True,
                )
            )
        informe_mc = paquete.get("informe_mecanica") or res.get("informe_mecanica")
        if isinstance(informe_mc, dict):
            _ok_fuente(
                fuente_mc.desde_informe_barrer(
                    informe_mc,
                    evidencia_ref=evid, o_ref=o_ref,
                    contexto_ciclo=ctx_ciclo, registrar=True,
                )
            )
    except Exception as e:
        errores.append("fuente mc: {0}: {1}".format(type(e).__name__, e))

    try:
        from modules.citacion.fuentes import limite as fuente_lim
        factores = res.get("factores") if isinstance(res.get("factores"), dict) else {}
        tiene_factores = all(
            factores.get(k) is not None
            and str(factores.get(k)) not in ("UNDEFINED", "None", "")
            for k in ("C", "L", "K")
        )
        permite_k = cx.get("permite_k")
        reg = cx.get("registro") if isinstance(cx.get("registro"), dict) else {}
        o_estado = reg.get("estado")
        if res.get("estado") == "UNDEFINED":
            o_estado = o_estado or "indefinido"
        pack_lim = fuente_lim.anunciar_desde_ciclo(
            evidencia_ref=evid, o_ref=o_ref, contexto_ciclo=ctx_ciclo,
            permite_k=permite_k if isinstance(permite_k, bool) else None,
            tiene_factores=tiene_factores, o_estado=o_estado, registrar=True,
        )
        if pack_lim.get("citas"):
            n_fuentes += len(pack_lim.get("citas") or [])
    except Exception as e:
        errores.append("fuente limite: {0}: {1}".format(type(e).__name__, e))

    try:
        from modules.citacion.esquema import plantilla
        cita_self = plantilla(
            id="CIT-CICLO",
            tipo="citacion",
            fuente_modulo=_NOMBRE,
            enunciado=(
                "CIT fundamentó el ciclo; estado_resultado={0}; "
                "tipos_peticion={1}.".format(res.get("estado"), tipos)
            ),
            descripcion=(
                "Declaración del oficio de fundamentación; "
                "no calcula; documenta el cierre de anuncio."
            ),
            evidencia_ref=evid,
            o_ref=o_ref,
            contexto_ciclo=ctx_ciclo,
            meta={"tipos_peticion": tipos, "estado": res.get("estado")},
        )
        registrar(cita_self)
        n_fuentes += 1
    except Exception as e:
        errores.append("declaracion fractal: {0}: {1}".format(type(e).__name__, e))

    anuncios_pack = anunciar_todo()
    clasif = _clasificar_ids_registro()

    return {
        "id": _ID,
        "estado": "OK" if n_fuentes > 0 else "VACIO",
        "ok": n_fuentes > 0,
        "n_declaraciones": len(_REGISTRO),
        "n_citas": len(_REGISTRO),
        "n_anuncios": anuncios_pack.get("n", 0),
        "anuncios": anuncios_pack.get("anuncios") or [],
        "clasificacion_ids": clasif,
        "tipos_peticion": tipos,
        "evidencia_ref": evid,
        "o_ref": o_ref,
        "errores": errores,
        "engine_version": paquete.get("engine_version"),
        "nota": (
            "CIT: autoridad universal de fundamentación sobre el paquete; "
            "cero agencia sobre valores numéricos; sin recálculo; "
            "sin modificación del conocimiento declarado; "
            "ids repetidos se clasifican, no se rechazan."
        ),
    }

# ===============================================================
# SECCIÓN 33 — ANUNCIAR (entrada única)
# ===============================================================

def anunciar(arg: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Entrada única — modo Engine y modo Consulta.
    - paquete de ciclo → cadena documental completa
    - declaración suelta → registro + anuncio de forma
    - None → anunciar_todo() del registro actual
    """
    if arg is None:
        return anunciar_todo()

    if _es_paquete_ciclo(arg):
        return _anunciar_paquete(arg)

    if _es_declaracion_suelta(arg):
        reg = registrar(arg)
        if not reg.get("ok"):
            return {
                "ok": False,
                "errores": reg.get("errores") or ["declaracion inválida"],
                "anuncio": None,
                "id": _ID,
            }
        return _anuncio_de_declaracion(reg.get("declaracion") or arg)

    return {
        "ok": False,
        "estado": "ERROR_FORMA",
        "errores": [
            "anunciar: se esperaba paquete de ciclo o una declaración "
            "con tipo/enunciado/id"
        ],
        "anuncio": None,
        "id": _ID,
    }

# ===============================================================
# SECCIÓN 34 — REPORTING ESTÁNDAR
# ===============================================================

def inventario(peticion: Any = None) -> Dict[str, Any]:
    clasif = _clasificar_ids_registro()
    return {
        "id": _ID,
        "nombre": _NOMBRE,
        "rol": _ROL,
        "version": _VERSION,
        "version_contrato": _VERSION_CONTRATO,
        "esquema": _ESQUEMA,
        "estabilidad": _ESTABILIDAD,
        "compatible_desde": _COMPATIBLE_DESDE,
        "api_engine": _API_ENGINE,
        "tipos_declaracion": list(TIPOS_DECLARACION),
        "relaciones": list(RELACIONES),
        "campos_obligatorios": list(CAMPOS_OBLIGATORIOS),
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "registro_n": len(_REGISTRO),
        "clasificacion_ids": clasif,
        "funcion": (
            "Autoridad universal de fundamentación. "
            "Resuelve, organiza, relaciona y cita cualquier declaración "
            "pública del VPSI. No modifica conocimiento."
        ),
        "modos": ["engine", "consulta"],
        "requiere": list(CONTENEDOR.get("requiere") or []),
    }


def reporte(peticion: Any = None) -> Dict[str, Any]:
    clasif = _clasificar_ids_registro()
    return {
        "id": _ID,
        "nombre": _NOMBRE,
        "rol": _ROL,
        "version": _VERSION,
        "estado": "OPERATIVO",
        "coherente": True,
        "registro_n": len(_REGISTRO),
        "ids_duplicados_n": clasif.get("total_duplicados", 0),
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "nota": (
            "CIT documenta y fundamenta. "
            "No calcula. No altera declaraciones de origen. "
            "ID repetido no es error."
        ),
    }


def diagnostico(peticion: Any = None) -> Dict[str, Any]:
    clasif = _clasificar_ids_registro()
    return {
        "id": _ID,
        "nombre": _NOMBRE,
        "rol": _ROL,
        "estado": "OPERATIVO",
        "problemas": [],
        "advertencias": [],
        "recomendaciones": [],
        "coherente": True,
        "registro_n": len(_REGISTRO),
        "ids_duplicados_n": clasif.get("total_duplicados", 0),
        "nota": (
            "Diagnóstico propio de CIT. "
            "ID repetido se clasifica, no se reporta como problema."
        ),
    }


def barrer(peticion: Any = None) -> Dict[str, Any]:
    errores: List[str] = []
    choques: List[str] = []

    for t in TIPOS_DECLARACION:
        if not isinstance(t, str) or not t:
            errores.append("tipo inválido en TIPOS_DECLARACION")

    for cap in CONTENEDOR["capacidades"]:
        nombre = str(cap).lower()
        if any(x in nombre for x in ("modificar", "alterar", "reescribir", "borrar_corpus")):
            choques.append(
                "capacidad incompatible con restricción única de CIT: {0}".format(cap)
            )

    clasif = _clasificar_ids_registro()
    coherente = not errores and not choques
    return {
        "id": _ID,
        "nombre": _NOMBRE,
        "rol": _ROL,
        "version": _VERSION,
        "coherente": coherente,
        "choques": choques,
        "errores": errores,
        "registro_n": len(_REGISTRO),
        "clasificacion_ids": clasif,
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "nota": (
            "Centinela CIT: integridad del oficio de fundamentación. "
            "Sin juicio de verdad numérica. "
            "ID repetido no es choque."
        ),
    }

# ===============================================================
# VERIFICAR — IDs + CALLABLE REAL POR MÓDULO
# ===============================================================

def verificar(engine: Any = None, **kwargs: Any) -> Dict[str, Any]:
    resultados: Dict[str, Any] = {}
    total_ids = 0
    total_callables = 0
    total_faltantes = 0

    catalogo = None

    if engine is not None:
        for attr in ("modulos", "modules", "catalogo", "registry"):
            catalogo = getattr(engine, attr, None)
            if isinstance(catalogo, dict):
                break

    if not isinstance(catalogo, dict):
        return {
            "id": ID_MODULO if "ID_MODULO" in globals() else "DGCO",
            "operacion": "verificar",
            "coherente": False,
            "estado": "DEGRADADO",
            "total_modulos": 0,
            "total_ids": 0,
            "callables": 0,
            "faltantes": 0,
            "modulos": {},
        }

    for mid, meta in catalogo.items():

        if isinstance(meta, dict) and isinstance(meta.get("contenedor"), dict):
            cont = meta["contenedor"]
        elif isinstance(meta, dict) and "capacidades" in meta:
            cont = meta
        else:
            cont = getattr(meta, "CONTENEDOR", None)

        mid_s = str(mid)

        if not isinstance(cont, dict):
            resultados[mid_s] = {
                "id_modulo": mid_s,
                "ids": [],
                "n": 0,
                "callables": [],
                "callables_n": 0,
                "faltantes": [],
                "faltantes_n": 0,
                "coherente": False,
            }
            continue

        id_modulo = str(cont.get("id") or mid_s)
        capacidades = cont.get("capacidades")

        if not isinstance(capacidades, dict):
            resultados[mid_s] = {
                "id_modulo": id_modulo,
                "ids": [],
                "n": 0,
                "callables": [],
                "callables_n": 0,
                "faltantes": [],
                "faltantes_n": 0,
                "coherente": False,
            }
            continue

        ids: List[str] = []
        callables: List[str] = []
        faltantes: List[str] = []

        for nombre, ref in capacidades.items():
            nombre_s = str(nombre)
            ids.append(nombre_s)

            if callable(ref):
                callables.append(nombre_s)
            else:
                faltantes.append(nombre_s)

        total_ids += len(ids)
        total_callables += len(callables)
        total_faltantes += len(faltantes)

        resultados[mid_s] = {
            "id_modulo": id_modulo,
            "ids": ids,
            "n": len(ids),
            "callables": callables,
            "callables_n": len(callables),
            "faltantes": faltantes,
            "faltantes_n": len(faltantes),
            "coherente": len(faltantes) == 0 and len(ids) > 0,
        }

    coherente = total_faltantes == 0 and total_ids > 0

    return {
        "id": ID_MODULO if "ID_MODULO" in globals() else "DGCO",
        "operacion": "verificar",
        "estado": "OPERATIVO" if coherente else "DEGRADADO",
        "coherente": coherente,
        "total_modulos": len(resultados),
        "total_ids": total_ids,
        "callables": total_callables,
        "faltantes": total_faltantes,
        "modulos": resultados,
    }
# ===============================================================
# SECCIÓN 35 — CAPACIDADES ARQUITECTÓNICAS
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
            if nombre in (
                "verificar", "barrer", "inventario", "reporte",
                "diagnostico", "anunciar", "anunciar_todo", "buscar",
                "citar", "resolver_enunciado", "explicar",
                "limpiar_ciclo", "evaluar", "inspeccionar",
                "registrar_inventario",
            ):
                resultados[nombre] = fn(pet)
            elif nombre == "verificar_salida":
                resultados[nombre] = fn(pet.get("salida"))
            elif nombre == "registrar":
                resultados[nombre] = fn(pet.get("declaracion"))
            elif nombre == "resolver":
                resultados[nombre] = fn(pet.get("id"))
            elif nombre == "cadena":
                resultados[nombre] = fn(pet.get("ids"))
            elif nombre == "relacionar":
                resultados[nombre] = fn(
                    pet.get("id_a"),
                    pet.get("relacion"),
                    pet.get("id_b"),
                )
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
        "id": _ID,
        "modulo": _NOMBRE,
        "rol": _ROL,
        "version": _VERSION,
        "operacion": "ejecutar_total",
        "estado": "OPERATIVO" if coherente else "DEGRADADO",
        "coherente": coherente,
        "capacidades_ejecutadas": ejecutadas,
        "errores_ejecucion": errores_ejecucion,
        "resultados": resultados,
        "capacidades_declaradas": caps,
    }


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

    clasif = _clasificar_ids_registro()
    coherente = not errores
    return {
        "id": _ID,
        "modulo": _NOMBRE,
        "rol": _ROL,
        "version": _VERSION,
        "operacion": "inspeccionar",
        "estado": "OPERATIVO" if coherente else "DEGRADADO",
        "coherente": coherente,
        "capacidades_contractuales": list(capacidades.keys()),
        "capacidades_meta": list(metas.keys()),
        "capacidades_resolubles": resolubles,
        "capacidades_no_resolubles": no_resolubles,
        "clasificacion_ids": clasif,
        "errores": errores,
        "autoriza_engine": CONTENEDOR.get("autoriza_engine"),
        "reporting": CONTENEDOR.get("reporting"),
        "invariantes": CONTENEDOR.get("invariantes"),
    }


def registrar_inventario(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    inv = inventario(peticion)
    return {
        "id": _ID,
        "operacion": "registrar_inventario",
        "registrado": True,
        "inventario": inv,
        "nota": (
            "Instantanea determinista del inventario de CIT. "
            "No modifica conocimiento declarado."
        ),
    }

# ===============================================================
# SECCIÓN 36 — RESOLUCIÓN Y EXPORTACIONES
# ===============================================================

_CAP_MAP = {
    "verificar": verificar,
    "barrer": barrer,
    "verificar_salida": verificar_salida,
    "inventario": inventario,
    "reporte": reporte,
    "diagnostico": diagnostico,
    "anunciar": anunciar,
    "anunciar_todo": anunciar_todo,
    "citar": citar,
    "registrar": registrar,
    "resolver": resolver,
    "resolver_enunciado": resolver_enunciado,
    "buscar": buscar,
    "cadena": cadena,
    "explicar": explicar,
    "relacionar": relacionar,
    "limpiar_ciclo": limpiar_ciclo,
    "evaluar": anunciar,
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
                raise RuntimeError(
                    "{0}: capacidad '{1}' referencia inexistente: '{2}'".format(
                        _NOMBRE, nombre, ref
                    )
                )
            fn = _CAP_MAP[ref]
            if not callable(fn):
                raise RuntimeError(
                    "{0}: '{1}' no es callable".format(_NOMBRE, ref)
                )
            resueltas[nombre] = fn
            continue
        raise RuntimeError(
            "{0}: capacidad '{1}' tipo inválido: {2}".format(
                _NOMBRE, nombre, type(ref).__name__
            )
        )
    cont["capacidades"] = resueltas


_resolver_capacidades(CONTENEDOR)

__all__ = [
    "CONTENEDOR",
    "TIPOS_DECLARACION",
    "RELACIONES",
    "CAMPOS_OBLIGATORIOS",
    "CAMPOS_OPCIONALES",
    "verificar",
    "barrer",
    "verificar_salida",
    "inventario",
    "reporte",
    "diagnostico",
    "anunciar",
    "anunciar_todo",
    "citar",
    "registrar",
    "resolver",
    "resolver_enunciado",
    "buscar",
    "cadena",
    "explicar",
    "relacionar",
    "limpiar_ciclo",
    "evaluar",
    "ejecutar_total",
    "inspeccionar",
    "registrar_inventario",
]

# ===============================================================
# FIN DEL MÓDULO
# ===============================================================
