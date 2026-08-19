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
# Identidad documental:
#     (modulo, id)
#
# El ID puede repetirse entre módulos.
# La repetición dentro de un mismo módulo sí requiere resolución
# contractual inequívoca.
# ===============================================================

_REGISTRO: List[Dict[str, Any]] = []


# ===============================================================
# SECCIÓN 18 — validar_declaracion
# ===============================================================

def _validar_declaracion(decl: Dict[str, Any]) -> List[str]:
    errores: List[str] = []

    if not isinstance(decl, dict):
        return ["declaracion debe ser dict"]

    tipo = decl.get("tipo")
    if not isinstance(tipo, str) or not tipo.strip():
        errores.append("falta campo obligatorio: tipo")
    elif tipo not in TIPOS_DECLARACION and not tipo.strip():
        errores.append("tipo de declaración inválido: {0}".format(tipo))

    for campo in CAMPOS_OBLIGATORIOS:
        if campo == "fuente":
            if not isinstance(decl.get("fuente"), str) or not decl.get("fuente").strip():
                if not isinstance(decl.get("fuente_modulo"), str) or not decl.get("fuente_modulo").strip():
                    errores.append("falta campo obligatorio: fuente")
            continue

        if campo == "id":
            if not isinstance(decl.get("id"), str) or not decl.get("id").strip():
                errores.append("falta campo obligatorio: id")
            continue

        valor = decl.get(campo)
        if valor is None or valor == "":
            errores.append("falta campo obligatorio: {0}".format(campo))

    modulo = (
        decl.get("modulo")
        or decl.get("fuente_modulo")
        or decl.get("fuente")
    )

    if not isinstance(modulo, str) or not modulo.strip():
        errores.append("falta campo obligatorio: modulo")

    return errores


# ===============================================================
# SECCIÓN 19 — normalizar_declaracion
# ===============================================================

def _normalizar_declaracion(decl: Dict[str, Any]) -> Dict[str, Any]:
    fuente = str(
        decl.get("fuente")
        or decl.get("fuente_modulo")
        or ""
    ).strip()

    modulo = str(
        decl.get("modulo")
        or decl.get("fuente_modulo")
        or fuente
        or ""
    ).strip()

    identificador = str(
        decl.get("id")
        or ""
    ).strip()

    out: Dict[str, Any] = {
        "id": identificador,
        "modulo": modulo,
        "tipo": decl.get("tipo"),
        "fuente": fuente,
        "fuente_modulo": modulo,
        "enunciado": decl.get("enunciado") or "",
        "descripcion": decl.get("descripcion") or "",
        "evidencia_ref": decl.get("evidencia_ref") or "",
    }

    for c in CAMPOS_OPCIONALES:
        if c in ("fuente_modulo", "modulo"):
            continue
        if c in decl and decl[c] is not None:
            out[c] = decl[c]

    if "relaciones" not in out:
        out["relaciones"] = list(decl.get("relaciones") or [])

    if "depende_de" not in out:
        out["depende_de"] = list(decl.get("depende_de") or [])

    return out


# ===============================================================
# SECCIÓN 19.1 — clave documental
# ===============================================================

def _clave_declaracion(decl: Dict[str, Any]) -> Tuple[str, str]:
    return (
        str(decl.get("modulo") or decl.get("fuente_modulo") or "").strip(),
        str(decl.get("id") or "").strip(),
    )


def _referencia_declaracion(decl: Dict[str, Any]) -> str:
    modulo, identificador = _clave_declaracion(decl)
    if modulo and identificador:
        return "{0}:{1}".format(modulo, identificador)
    return identificador or modulo


def _clave_peticion(peticion: Any) -> Tuple[Optional[str], Optional[str]]:
    if isinstance(peticion, dict):
        modulo = peticion.get("modulo") or peticion.get("fuente_modulo")
        identificador = peticion.get("id")
        return (
            str(modulo).strip() if modulo is not None and str(modulo).strip() else None,
            str(identificador).strip() if identificador is not None and str(identificador).strip() else None,
        )

    if isinstance(peticion, str):
        valor = peticion.strip()

        if ":" in valor:
            modulo, identificador = valor.split(":", 1)
            modulo = modulo.strip()
            identificador = identificador.strip()
            if modulo and identificador:
                return modulo, identificador

        return None, valor

    return None, None


# ===============================================================
# SECCIÓN 20 — RESOLUCIÓN / REGISTRO / CONSULTA BASE / limpiar_ciclo
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
# SECCIÓN 21 — REGISTRAR
# ===============================================================

def registrar(declaracion: Dict[str, Any]) -> Dict[str, Any]:
    """
    Incorpora una declaración pública al registro operativo.

    La identidad es (modulo, id).
    Un mismo id puede existir en módulos diferentes.
    Una declaración no puede sustituir silenciosamente a otra
    del mismo módulo.
    """
    errores = _validar_declaracion(declaracion)

    if errores:
        return {
            "ok": False,
            "errores": errores,
            "id": _ID,
        }

    normalizada = _normalizar_declaracion(declaracion)
    clave = _clave_declaracion(normalizada)

    if not clave[0] or not clave[1]:
        return {
            "ok": False,
            "errores": ["identidad documental incompleta: requiere modulo e id"],
            "id": _ID,
        }

    existentes = [
        d for d in _REGISTRO
        if _clave_declaracion(d) == clave
    ]

    if existentes:
        return {
            "ok": False,
            "errores": [
                "declaracion duplicada dentro del mismo modulo: {0}".format(
                    _referencia_declaracion(normalizada)
                )
            ],
            "id": _ID,
        }

    _REGISTRO.append(normalizada)

    return {
        "ok": True,
        "n": len(_REGISTRO),
        "declaracion": normalizada,
        "id": _ID,
        "modulo": clave[0],
        "clave": _referencia_declaracion(normalizada),
    }


# ===============================================================
# SECCIÓN 22 — RESOLVER
# ===============================================================

def resolver(
    id_decl: Any,
    modulo: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Resuelve una declaración mediante identidad documental.

    Formas aceptadas:

        resolver("AX:T1")
        resolver("T1", modulo="AX")
        resolver({"modulo": "AX", "id": "T1"})

    Un ID sin módulo solamente puede resolverse si existe una única
    declaración con ese ID en las fuentes disponibles.

    Nunca selecciona arbitrariamente entre módulos.
    No inventa declaraciones.
    """

    modulo_pet, id_pet = _clave_peticion(id_decl)

    modulo_res = (
        str(modulo).strip()
        if modulo is not None and str(modulo).strip()
        else modulo_pet
    )

    clave = id_pet

    if not clave:
        return {
            "id": id_decl,
            "modulo": modulo_res,
            "resuelto": False,
            "declaracion": None,
            "nota": "id vacío",
        }

    candidatos = [
        d for d in _REGISTRO
        if d.get("id") == clave
        and (
            modulo_res is None
            or str(d.get("modulo") or d.get("fuente_modulo") or "").strip()
            == modulo_res
        )
        and d.get("enunciado")
    ]

    if len(candidatos) == 1:
        d = candidatos[0]
        return {
            "id": clave,
            "modulo": d.get("modulo"),
            "resuelto": True,
            "declaracion": d,
            "origen": "registro_ciclo",
            "nota": "resuelto desde registro operativo de CIT",
        }

    if len(candidatos) > 1:
        return {
            "id": clave,
            "modulo": modulo_res,
            "resuelto": False,
            "declaracion": None,
            "ambiguo": True,
            "candidatos": [
                _referencia_declaracion(d)
                for d in candidatos
            ],
            "nota": "id ambiguo: existen múltiples declaraciones resolubles",
        }

    # -----------------------------------------------------------
    # Puente a fuentes del sistema
    # -----------------------------------------------------------
    try:
        from modules.citacion.fuentes import ax as fuente_ax

        if modulo_res:
            r = fuente_ax.anunciar_id(
                clave,
                modulo=modulo_res,
                evidencia_ref="cit.resolver",
                registrar=False,
            )
        else:
            r = fuente_ax.anunciar_id(
                clave,
                evidencia_ref="cit.resolver",
                registrar=False,
            )

        if isinstance(r, dict) and r.get("resuelto") and r.get("cita"):
            c = r["cita"]

            decl = _normalizar_declaracion({
                "id": clave,
                "modulo": (
                    c.get("modulo")
                    or c.get("fuente_modulo")
                    or modulo_res
                    or c.get("fuente")
                ),
                "tipo": c.get("tipo") or "axioma",
                "fuente": c.get("fuente") or c.get("fuente_modulo") or "ax",
                "enunciado": c.get("enunciado"),
                "descripcion": c.get("descripcion"),
                "evidencia_ref": c.get("evidencia_ref"),
                "relaciones": c.get("relaciones") or [],
                "depende_de": c.get("depende_de") or [],
            })

            return {
                "id": clave,
                "modulo": decl.get("modulo"),
                "resuelto": True,
                "declaracion": decl,
                "origen": "fuente_sistema",
                "nota": "resuelto desde fuente de declaraciones del sistema",
            }

    except TypeError:
        # Compatibilidad con contratos de fuentes antiguas que todavía
        # no reciben modulo como argumento.
        try:
            from modules.citacion.fuentes import ax as fuente_ax

            r = fuente_ax.anunciar_id(
                clave,
                evidencia_ref="cit.resolver",
                registrar=False,
            )

            if isinstance(r, dict) and r.get("resuelto") and r.get("cita"):
                c = r["cita"]
                decl = _normalizar_declaracion({
                    "id": clave,
                    "modulo": (
                        c.get("modulo")
                        or c.get("fuente_modulo")
                        or modulo_res
                        or c.get("fuente")
                    ),
                    "tipo": c.get("tipo") or "axioma",
                    "fuente": c.get("fuente") or c.get("fuente_modulo") or "ax",
                    "enunciado": c.get("enunciado"),
                    "descripcion": c.get("descripcion"),
                    "evidencia_ref": c.get("evidencia_ref"),
                    "relaciones": c.get("relaciones") or [],
                    "depende_de": c.get("depende_de") or [],
                })

                if modulo_res and decl.get("modulo") != modulo_res:
                    return {
                        "id": clave,
                        "modulo": modulo_res,
                        "resuelto": False,
                        "declaracion": None,
                        "nota": (
                            "la fuente resolvió el id, pero no confirmó "
                            "el módulo solicitado"
                        ),
                    }

                return {
                    "id": clave,
                    "modulo": decl.get("modulo"),
                    "resuelto": True,
                    "declaracion": decl,
                    "origen": "fuente_sistema",
                    "nota": "resuelto desde fuente de declaraciones del sistema",
                }

        except Exception:
            pass

    except Exception:
        pass

    return {
        "id": clave,
        "modulo": modulo_res,
        "resuelto": False,
        "declaracion": None,
        "nota": (
            "sin declaración resoluble en registro ni fuentes cargadas"
        ),
    }


# ===============================================================
# SECCIÓN 24 — CITAR
# ===============================================================

def citar(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Representación citable de declaraciones.

    La cita conserva:
        modulo
        id
        tipo
        fuente
        enunciado
        relaciones
        depende_de

    CIT no modifica el contenido de la declaración.
    """
    pack = buscar(peticion)
    declaraciones = pack.get("declaraciones") or []

    citas: List[Dict[str, Any]] = []

    for d in declaraciones:
        n = _normalizar_declaracion(d)
        citas.append({
            "modulo": n.get("modulo"),
            "id": n.get("id"),
            "clave": _referencia_declaracion(n),
            "tipo": n.get("tipo"),
            "fuente": n.get("fuente"),
            "fuente_modulo": n.get("fuente_modulo"),
            "enunciado": n.get("enunciado"),
            "descripcion": n.get("descripcion"),
            "evidencia_ref": n.get("evidencia_ref"),
            "relaciones": list(n.get("relaciones") or []),
            "depende_de": list(n.get("depende_de") or []),
        })

    return {
        "id": _ID,
        "citas": citas,
        "n": len(citas),
        "nota": (
            "Cita documental basada en módulo e ID; "
            "sin recálculo ni modificación."
        ),
    }


# ===============================================================
# SECCIÓN 25 — RESOLVER ENUNCIADO
# ===============================================================

def resolver_enunciado(
    id_norma: str,
    modulo: Optional[str] = None,
) -> Dict[str, Any]:
    """Resolución de enunciado mediante módulo + ID."""
    r = resolver(id_norma, modulo=modulo)
    d = r.get("declaracion") or {}

    return {
        "id": id_norma,
        "modulo": r.get("modulo") or d.get("modulo"),
        "enunciado": d.get("enunciado") if r.get("resuelto") else None,
        "descripcion": d.get("descripcion") if r.get("resuelto") else None,
        "fuente": d.get("fuente") if r.get("resuelto") else None,
        "fuente_modulo": d.get("modulo") if r.get("resuelto") else None,
        "depende_de": d.get("depende_de") if r.get("resuelto") else [],
        "resuelto": bool(r.get("resuelto")),
        "ambiguo": bool(r.get("ambiguo")),
        "candidatos": r.get("candidatos") or [],
        "nota": r.get("nota"),
    }


# ===============================================================
# SECCIÓN 26 — RELACIONAR
# ===============================================================

def relacionar(
    id_a: str,
    relacion: str,
    id_b: str,
    modulo_a: Optional[str] = None,
    modulo_b: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Documenta una relación entre dos declaraciones resolubles.

    La relación conserva la identidad completa de ambos extremos.
    CIT registra la relación; no convierte la relación en verdad
    axiomática ni altera las declaraciones originales.
    """

    if relacion not in RELACIONES:
        return {
            "ok": False,
            "errores": [
                "relacion no admitida: {0}".format(relacion)
            ],
            "id": _ID,
        }

    ra = resolver(id_a, modulo=modulo_a)
    rb = resolver(id_b, modulo=modulo_b)

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

    da = ra["declaracion"]
    db = rb["declaracion"]

    ref_a = _referencia_declaracion(da)
    ref_b = _referencia_declaracion(db)

    enlace = {
        "id": "REL-{0}-{1}-{2}".format(
            ref_a,
            relacion,
            ref_b,
        ),
        "modulo": _NOMBRE,
        "tipo": "citacion",
        "fuente": _NOMBRE,
        "enunciado": "{0} {1} {2}".format(
            ref_a,
            relacion,
            ref_b,
        ),
        "descripcion": "Relación documental registrada por CIT.",
        "relaciones": [
            {
                "de": {
                    "modulo": da.get("modulo"),
                    "id": da.get("id"),
                },
                "relacion": relacion,
                "a": {
                    "modulo": db.get("modulo"),
                    "id": db.get("id"),
                },
            }
        ],
        "meta": {
            "a": ref_a,
            "b": ref_b,
            "modulo_a": da.get("modulo"),
            "id_a": da.get("id"),
            "modulo_b": db.get("modulo"),
            "id_b": db.get("id"),
            "relacion": relacion,
        },
    }

    return registrar(enlace)


# ===============================================================
# SECCIÓN 27 — CADENA
# ===============================================================

def cadena(
    ids: Optional[List[Any]] = None,
) -> Dict[str, Any]:
    """
    Construye una cadena documental a partir de referencias ordenadas.

    Cada referencia puede ser:
        "AX:T1"
        {"modulo": "AX", "id": "T1"}

    No inventa nodos.
    No determina verdad.
    No interpreta compatibilidad.
    """

    secuencia = list(ids or [])
    eslabones: List[Dict[str, Any]] = []
    faltantes: List[Any] = []
    ambiguos: List[Dict[str, Any]] = []

    for referencia in secuencia:
        r = resolver(referencia)

        if r.get("resuelto"):
            eslabones.append(r["declaracion"])
        elif r.get("ambiguo"):
            ambiguos.append({
                "referencia": referencia,
                "candidatos": r.get("candidatos") or [],
            })
        else:
            faltantes.append(referencia)

    completa = (
        len(faltantes) == 0
        and len(ambiguos) == 0
        and len(eslabones) > 0
    )

    return {
        "id": _ID,
        "cadena": eslabones,
        "n": len(eslabones),
        "faltantes": faltantes,
        "ambiguos": ambiguos,
        "completa": completa,
        "nota": (
            "Cadena documental basada en declaraciones resolubles "
            "por módulo e ID; sin recálculo."
        ),
    }


# ===============================================================
# SECCIÓN 28 — EXPLICAR
# ===============================================================

def explicar(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Explicación documental.

    Toda explicación procede de declaraciones existentes.
    CIT no agrega premisas ni interpreta el contenido matemático.
    """

    pet = peticion if isinstance(peticion, dict) else {}

    ids = pet.get("ids") or pet.get("cadena") or []

    if isinstance(ids, (str, dict)):
        ids = [ids]

    if ids:
        pack_cadena = cadena(list(ids))
    else:
        pack_busca = buscar(pet)

        declaraciones = pack_busca.get("declaraciones") or []

        pack_cadena = {
            "cadena": declaraciones,
            "n": len(declaraciones),
            "faltantes": [],
            "ambiguos": [],
            "completa": len(declaraciones) > 0,
        }

    return {
        "id": _ID,
        "explicacion": pack_cadena.get("cadena") or [],
        "n": pack_cadena.get("n", 0),
        "faltantes": pack_cadena.get("faltantes") or [],
        "ambiguos": pack_cadena.get("ambiguos") or [],
        "completa": bool(pack_cadena.get("completa")),
        "nota": (
            "Explicación = declaraciones existentes. "
            "CIT no interpreta ni calcula."
        ),
    }


# ===============================================================
# SECCIÓN 29 — ANUNCIO DE DECLARACIONES
# ===============================================================

def _anuncio_de_declaracion(
    decl: Dict[str, Any],
) -> Dict[str, Any]:
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
            "titulo": "[{0}:{1}]".format(
                c.get("modulo"),
                c.get("id"),
            ),
            "modulo": c.get("modulo"),
            "id": c.get("id"),
            "clave": _referencia_declaracion(c),
            "tipo": c.get("tipo"),
            "fuente": c.get("fuente"),
            "enunciado": c.get("enunciado"),
            "descripcion": c.get("descripcion"),
            "evidencia_ref": c.get("evidencia_ref"),
            "o_ref": c.get("o_ref"),
            "contexto_ciclo": c.get("contexto_ciclo"),
            "relaciones": c.get("relaciones") or [],
            "depende_de": c.get("depende_de") or [],
        },
    }


# ===============================================================
# SECCIÓN 30 — ANUNCIAR TODO
# ===============================================================

def anunciar_todo(
    filtro: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
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
        "nota": (
            "Capacidad total de anuncio sobre declaraciones resolubles; "
            "cada declaración conserva módulo e ID."
        ),
    }

# ===============================================================
# SECCIÓN 31 — INVENTARIO
# ===============================================================

def inventario(peticion: Any = None) -> Dict[str, Any]:
    """
    Inventario contractual de CIT.

    Expone exclusivamente la infraestructura declarada por el módulo:
    identidad, contrato, esquema, capacidades, tipos, relaciones y
    campos obligatorios.

    No ejecuta otras capacidades.
    No consulta autoridades externas.
    No modifica conocimiento.
    """
    capacidades = list(CONTENEDOR["capacidades"].keys()) if isinstance(CONTENEDOR.get("capacidades"), dict) else []

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
        "capacidades": capacidades,
        "registro_n": len(_REGISTRO),
        "funcion": (
            "Autoridad de fundamentación documental. "
            "Resuelve, organiza, relaciona, explica y cita declaraciones "
            "públicas identificadas por módulo e ID. "
            "No modifica conocimiento de origen ni recalcula valores."
        ),
        "modos": ["engine", "consulta"],
        "requiere": [],
    }


# ===============================================================
# SECCIÓN 32 — REPORTE
# ===============================================================

def reporte(peticion: Any = None) -> Dict[str, Any]:
    """
    Reporte operativo de CIT.

    El reporte describe el estado observable del módulo y de su registro
    operativo. No declara coherencia matemática del corpus ni sustituye
    el diagnóstico de otro módulo.
    """
    errores: List[str] = []
    advertencias: List[str] = []

    if not isinstance(_REGISTRO, list):
        errores.append("registro operativo inválido")

    capacidades = CONTENEDOR.get("capacidades")
    if not isinstance(capacidades, dict):
        errores.append("contenedor de capacidades inválido")
        capacidades_n = 0
    else:
        capacidades_n = len(capacidades)

    if isinstance(_REGISTRO, list):
        for i, decl in enumerate(_REGISTRO):
            if not isinstance(decl, dict):
                errores.append(
                    "declaración inválida en registro operativo: índice {0}".format(i)
                )
                continue
            errores.extend(
                "registro[{0}]: {1}".format(i, e)
                for e in _validar_declaracion(decl)
            )

    coherente = not errores

    if not _REGISTRO:
        advertencias.append("registro operativo vacío")

    return {
        "id": _ID,
        "nombre": _NOMBRE,
        "rol": _ROL,
        "version": _VERSION,
        "estado": "OPERATIVO" if coherente else "ERROR",
        "coherente": coherente,
        "errores": errores,
        "advertencias": advertencias,
        "registro_n": len(_REGISTRO) if isinstance(_REGISTRO, list) else 0,
        "capacidades": (
            list(capacidades.keys())
            if isinstance(capacidades, dict)
            else []
        ),
        "capacidades_n": capacidades_n,
        "nota": (
            "CIT documenta y fundamenta declaraciones existentes. "
            "El reporte evalúa únicamente su estado operativo local; "
            "no determina la coherencia del corpus ni modifica declaraciones."
        ),
    }


# ===============================================================
# SECCIÓN 33 — DIAGNÓSTICO
# ===============================================================

def diagnostico(peticion: Any = None) -> Dict[str, Any]:
    """
    Diagnóstico propio y determinista de CIT.

    Solo inspecciona invariantes internas de CIT:
    - registro operativo;
    - declaraciones registradas;
    - capacidades declaradas;
    - contrato básico.

    No consulta ni suplanta AX, CX, CA, FO, CT, MC, límite u otros
    módulos. Una declaración de otro módulo no se considera duplicada
    simplemente por compartir ID: la identidad documental es
    (fuente/módulo, ID).
    """
    problemas: List[Dict[str, Any]] = []
    advertencias: List[Dict[str, Any]] = []
    recomendaciones: List[str] = []

    if not isinstance(_REGISTRO, list):
        problemas.append({
            "tipo": "registro_invalido",
            "detalle": "El registro operativo no es una lista.",
        })
    else:
        for i, decl in enumerate(_REGISTRO):
            if not isinstance(decl, dict):
                problemas.append({
                    "tipo": "declaracion_invalida",
                    "indice": i,
                    "detalle": "La entrada no es un dict.",
                })
                continue

            errores_decl = _validar_declaracion(decl)
            for error in errores_decl:
                problemas.append({
                    "tipo": "declaracion_invalida",
                    "indice": i,
                    "id": decl.get("id"),
                    "fuente": decl.get("fuente") or decl.get("fuente_modulo"),
                    "detalle": error,
                })

    capacidades = CONTENEDOR.get("capacidades")
    if not isinstance(capacidades, dict):
        problemas.append({
            "tipo": "capacidades_invalidas",
            "detalle": "CONTENEDOR['capacidades'] debe ser un dict.",
        })
    else:
        for nombre in capacidades.keys():
            if not isinstance(nombre, str) or not nombre.strip():
                problemas.append({
                    "tipo": "capacidad_invalida",
                    "detalle": "Existe una capacidad sin nombre válido.",
                })

    if not TIPOS_DECLARACION:
        advertencias.append({
            "tipo": "tipos_declaracion_vacios",
            "detalle": "No existen tipos de declaración registrados.",
        })

    if not RELACIONES:
        advertencias.append({
            "tipo": "relaciones_vacias",
            "detalle": "No existen relaciones documentales registradas.",
        })

    if not _REGISTRO:
        advertencias.append({
            "tipo": "registro_vacio",
            "detalle": "No existen declaraciones en el registro operativo.",
        })

    if problemas:
        recomendaciones.append(
            "Corregir las inconsistencias internas del registro o del contrato de CIT."
        )

    if advertencias:
        recomendaciones.append(
            "Verificar si el estado del ciclo justifica la ausencia de declaraciones."
        )

    return {
        "id": _ID,
        "nombre": _NOMBRE,
        "rol": _ROL,
        "estado": "OPERATIVO" if not problemas else "ERROR",
        "problemas": problemas,
        "advertencias": advertencias,
        "recomendaciones": recomendaciones,
        "coherente": not problemas,
        "registro_n": len(_REGISTRO) if isinstance(_REGISTRO, list) else 0,
        "capacidades": (
            list(CONTENEDOR["capacidades"].keys())
            if isinstance(CONTENEDOR.get("capacidades"), dict)
            else []
        ),
        "nota": (
            "Diagnóstico local de CIT. "
            "No determina la verdad ni la coherencia de declaraciones "
            "pertenecientes a otros módulos. "
            "La identidad documental se determina por módulo/fuente + ID; "
            "un mismo ID puede existir legítimamente en módulos diferentes."
        ),
    }

# ===============================================================
# SECCIÓN 34 — BARRER
# ===============================================================

def barrer(peticion: Any = None) -> Dict[str, Any]:
    """
    Auditoría estructural determinista de CIT.

    Principios:
    - CIT documenta; no calcula.
    - CIT no modifica conocimiento de origen.
    - CIT no sustituye a AX, MC, CX, CA, FO, TT ni Engine.
    - Las declaraciones se identifican por (modulo, id).
    - Un mismo id puede existir legítimamente en módulos diferentes.
    - Un id repetido dentro del mismo módulo sí constituye duplicidad.
    - Las dependencias se resuelven siempre dentro de su módulo cuando
      la declaración proporciona módulo explícito.
    - Una dependencia sin módulo puede resolverse contra el módulo
      de origen de la declaración.
    - No se inventan declaraciones ni dependencias.
    - No se interpreta el contenido matemático de una declaración.
    - No se convierte una ausencia documental en contradicción axiomática.
    - El barrido inspecciona la infraestructura declarada por CIT.
    """

    errores: List[Dict[str, Any]] = []
    advertencias: List[Dict[str, Any]] = []
    dependencias: List[Dict[str, Any]] = []
    declaraciones: List[Dict[str, Any]] = []
    capacidades: List[Dict[str, Any]] = []
    modulos: List[Dict[str, Any]] = []
    duplicados: List[Dict[str, Any]] = []
    relaciones: List[Dict[str, Any]] = []
    cadenas: List[Dict[str, Any]] = []

    # -----------------------------------------------------------
    # 1. CONTRATO BASE DE CIT
    # -----------------------------------------------------------

    contrato = {
        "id": _ID,
        "nombre": _NOMBRE,
        "rol": _ROL,
        "version": _VERSION,
        "version_contrato": _VERSION_CONTRATO,
        "esquema": _ESQUEMA,
        "estabilidad": _ESTABILIDAD,
        "compatible_desde": _COMPATIBLE_DESDE,
        "api_engine": _API_ENGINE,
    }

    for campo in (
        "id",
        "nombre",
        "rol",
        "version",
        "version_contrato",
        "esquema",
        "estabilidad",
        "compatible_desde",
        "api_engine",
    ):
        valor = contrato.get(campo)
        if valor is None or str(valor).strip() == "":
            errores.append({
                "tipo": "campo_contrato_ausente",
                "campo": campo,
                "modulo": _NOMBRE,
            })

    # -----------------------------------------------------------
    # 2. TIPOS
    # -----------------------------------------------------------

    tipos_validos: List[str] = []

    for tipo in TIPOS_DECLARACION:
        if not isinstance(tipo, str) or not tipo.strip():
            errores.append({
                "tipo": "tipo_declaracion_invalido",
                "valor": tipo,
            })
        else:
            tipos_validos.append(tipo.strip())

    # -----------------------------------------------------------
    # 3. CAMPOS OBLIGATORIOS
    # -----------------------------------------------------------

    campos_obligatorios: List[str] = []

    for campo in CAMPOS_OBLIGATORIOS:
        if not isinstance(campo, str) or not campo.strip():
            errores.append({
                "tipo": "campo_obligatorio_invalido",
                "valor": campo,
            })
        else:
            campos_obligatorios.append(campo.strip())

    # -----------------------------------------------------------
    # 4. RELACIONES
    # -----------------------------------------------------------

    relaciones_validas: List[str] = []

    for relacion in RELACIONES:
        if not isinstance(relacion, str) or not relacion.strip():
            errores.append({
                "tipo": "relacion_invalida",
                "valor": relacion,
            })
        else:
            relaciones_validas.append(relacion.strip())

    # -----------------------------------------------------------
    # 5. CAPACIDADES DECLARADAS POR CIT
    # -----------------------------------------------------------

    capacidades_contenedor = CONTENEDOR.get("capacidades")

    if not isinstance(capacidades_contenedor, dict):
        errores.append({
            "tipo": "contenedor_capacidades_invalido",
            "detalle": "CONTENEDOR['capacidades'] debe ser dict",
        })
        capacidades_contenedor = {}

    for nombre, referencia in sorted(
        capacidades_contenedor.items(),
        key=lambda x: str(x[0]),
    ):
        if not isinstance(nombre, str) or not nombre.strip():
            errores.append({
                "tipo": "capacidad_sin_nombre",
                "valor": nombre,
            })
            continue

        capacidades.append({
            "nombre": nombre,
            "referencia": (
                referencia.__name__
                if callable(referencia)
                and hasattr(referencia, "__name__")
                else str(referencia)
            ),
            "callable": bool(callable(referencia)),
        })

        if not callable(referencia):
            advertencias.append({
                "tipo": "capacidad_no_callable",
                "capacidad": nombre,
                "referencia": str(referencia),
            })

    # -----------------------------------------------------------
    # 6. REGISTRO OPERATIVO LOCAL
    # -----------------------------------------------------------

    registro_local = list(_REGISTRO)

    # identidad documental:
    # (fuente_modulo/fuente, id)
    indice_local: Dict[Tuple[str, str], List[Dict[str, Any]]] = {}

    for decl in registro_local:
        if not isinstance(decl, dict):
            errores.append({
                "tipo": "registro_no_dict",
                "valor": repr(decl),
            })
            continue

        did = decl.get("id")
        fuente = (
            decl.get("fuente_modulo")
            or decl.get("fuente")
            or _NOMBRE
        )

        if did is None or not str(did).strip():
            errores.append({
                "tipo": "declaracion_sin_id",
                "fuente_modulo": str(fuente),
            })
            continue

        did = str(did).strip()
        fuente = str(fuente).strip()

        clave = (fuente, did)

        indice_local.setdefault(clave, []).append(decl)

        errores_decl = _validar_declaracion(decl)

        if errores_decl:
            errores.append({
                "tipo": "declaracion_invalida",
                "modulo": fuente,
                "id": did,
                "errores": list(errores_decl),
            })

        declaraciones.append({
            "modulo": fuente,
            "id": did,
            "tipo": decl.get("tipo"),
            "enunciado": decl.get("enunciado"),
            "descripcion": decl.get("descripcion"),
            "evidencia_ref": decl.get("evidencia_ref"),
            "relaciones": list(decl.get("relaciones") or []),
        })

    # -----------------------------------------------------------
    # 7. DUPLICIDAD CORRECTA
    #
    # MISMO ID EN DISTINTO MÓDULO = LEGÍTIMO
    # MISMO ID EN MISMO MÓDULO = DUPLICADO
    # -----------------------------------------------------------

    for (fuente, did), items in sorted(indice_local.items()):
        if len(items) > 1:
            duplicados.append({
                "tipo": "id_duplicado_en_modulo",
                "modulo": fuente,
                "id": did,
                "cantidad": len(items),
            })

    # -----------------------------------------------------------
    # 8. RELACIONES DEL REGISTRO
    # -----------------------------------------------------------

    for decl in registro_local:
        if not isinstance(decl, dict):
            continue

        fuente_a = (
            decl.get("fuente_modulo")
            or decl.get("fuente")
            or _NOMBRE
        )
        id_a = decl.get("id")

        if id_a is None:
            continue

        for rel in decl.get("relaciones") or []:
            if not isinstance(rel, dict):
                advertencias.append({
                    "tipo": "relacion_forma_invalida",
                    "modulo": fuente_a,
                    "id": id_a,
                    "relacion": rel,
                })
                continue

            id_b = rel.get("a") or rel.get("id_b") or rel.get("hacia")
            tipo_rel = rel.get("relacion") or rel.get("tipo")

            if not id_b:
                advertencias.append({
                    "tipo": "relacion_sin_destino",
                    "modulo": fuente_a,
                    "id": id_a,
                })
                continue

            relaciones.append({
                "desde": {
                    "modulo": str(fuente_a),
                    "id": str(id_a),
                },
                "relacion": tipo_rel,
                "hacia": {
                    "modulo": str(
                        rel.get("fuente_modulo")
                        or rel.get("fuente")
                        or fuente_a
                    ),
                    "id": str(id_b),
                },
            })

            if (
                tipo_rel is not None
                and str(tipo_rel) not in relaciones_validas
            ):
                advertencias.append({
                    "tipo": "relacion_no_catalogada",
                    "modulo": fuente_a,
                    "id": id_a,
                    "relacion": tipo_rel,
                })

    # -----------------------------------------------------------
    # 9. RESOLUCIÓN DE DEPENDENCIAS
    #
    # La dependencia siempre conserva su identidad de módulo.
    # -----------------------------------------------------------

    for decl in registro_local:
        if not isinstance(decl, dict):
            continue

        modulo = str(
            decl.get("fuente_modulo")
            or decl.get("fuente")
            or _NOMBRE
        ).strip()

        did = decl.get("id")

        if did is None:
            continue

        did = str(did).strip()

        deps = decl.get("depende_de") or []

        if not isinstance(deps, (list, tuple)):
            advertencias.append({
                "tipo": "depende_de_forma_invalida",
                "modulo": modulo,
                "id": did,
                "valor": deps,
            })
            continue

        for dep in deps:
            dep_modulo = modulo
            dep_id = None

            if isinstance(dep, dict):
                dep_id = (
                    dep.get("id")
                    or dep.get("id_decl")
                    or dep.get("declaracion")
                )
                dep_modulo = str(
                    dep.get("fuente_modulo")
                    or dep.get("fuente")
                    or modulo
                ).strip()
            else:
                dep_id = str(dep).strip()

            if not dep_id:
                advertencias.append({
                    "tipo": "dependencia_sin_id",
                    "modulo": modulo,
                    "id": did,
                })
                continue

            clave_dep = (dep_modulo, str(dep_id))

            encontrada = clave_dep in indice_local

            dependencias.append({
                "desde": {
                    "modulo": modulo,
                    "id": did,
                },
                "hacia": {
                    "modulo": dep_modulo,
                    "id": str(dep_id),
                },
                "estado": (
                    "encontrada"
                    if encontrada
                    else "no_resuelta_en_registro"
                ),
            })

    # -----------------------------------------------------------
    # 10. CADENAS LOCALES
    # -----------------------------------------------------------

    grafo: Dict[Tuple[str, str], List[Tuple[str, str]]] = {}

    for item in dependencias:
        origen = (
            item["desde"]["modulo"],
            item["desde"]["id"],
        )
        destino = (
            item["hacia"]["modulo"],
            item["hacia"]["id"],
        )

        if item["estado"] == "encontrada":
            grafo.setdefault(origen, []).append(destino)

    def _cadena(
        origen: Tuple[str, str],
    ) -> Tuple[List[Tuple[str, str]], bool]:
        visitados: Set[Tuple[str, str]] = set()
        camino: List[Tuple[str, str]] = []
        ciclo = False

        def _dfs(nodo: Tuple[str, str]) -> None:
            nonlocal ciclo

            if nodo in camino:
                ciclo = True
                return

            if nodo in visitados:
                return

            visitados.add(nodo)
            camino.append(nodo)

            for destino in sorted(
                grafo.get(nodo, []),
                key=lambda x: (str(x[0]), str(x[1])),
            ):
                _dfs(destino)

            camino.pop()

        _dfs(origen)

        return sorted(visitados), ciclo

    ciclos: List[List[Dict[str, str]]] = []

    for origen in sorted(grafo.keys()):
        alcanzables, hay_ciclo = _cadena(origen)

        cadenas.append({
            "origen": {
                "modulo": origen[0],
                "id": origen[1],
            },
            "alcanzables": [
                {
                    "modulo": modulo,
                    "id": did,
                }
                for modulo, did in alcanzables
                if (modulo, did) != origen
            ],
            "ciclo": hay_ciclo,
        })

        if hay_ciclo:
            ciclos.append([
                {
                    "modulo": modulo,
                    "id": did,
                }
                for modulo, did in alcanzables
            ])

    # -----------------------------------------------------------
    # 11. INSPECCIÓN DE MÓDULOS DISPONIBLES
    #
    # Se utiliza la infraestructura de CONTENEDORES del sistema
    # cuando está disponible. CIT no inventa módulos.
    # -----------------------------------------------------------

    try:
        registro_engine = globals().get("REGISTRO_MODULOS")
        if registro_engine is None:
            registro_engine = globals().get("_REGISTRO_MODULOS")

        contenedores = getattr(
            registro_engine,
            "contenedores",
            {},
        )

        if isinstance(contenedores, dict):
            for nombre, cont in sorted(
                contenedores.items(),
                key=lambda x: str(x[0]),
            ):
                meta = getattr(cont, "meta", {})
                if not isinstance(meta, dict):
                    meta = {}

                modulo_info = {
                    "nombre": str(
                        getattr(cont, "nombre", None)
                        or meta.get("nombre")
                        or nombre
                    ),
                    "id": str(
                        getattr(cont, "id", None)
                        or meta.get("id")
                        or ""
                    ),
                    "rol": str(
                        getattr(cont, "rol", None)
                        or meta.get("rol")
                        or ""
                    ),
                    "version": str(
                        getattr(cont, "version", None)
                        or meta.get("version")
                        or ""
                    ),
                    "ruta": str(
                        getattr(cont, "ruta", "")
                        or meta.get("ruta")
                        or ""
                    ),
                    "requiere": list(
                        getattr(cont, "requiere", None)
                        or meta.get("requiere")
                        or []
                    ),
                    "capacidades": sorted(
                        list(
                            getattr(cont, "capacidades", None)
                            or meta.get("capacidades", {})
                            or {}
                        )
                    ),
                }

                modulos.append(modulo_info)

    except Exception as exc:
        advertencias.append({
            "tipo": "inventario_modulos_no_disponible",
            "error": "{0}: {1}".format(
                type(exc).__name__,
                exc,
            ),
        })

    # -----------------------------------------------------------
    # 12. DEPENDENCIAS ENTRE MÓDULOS
    # -----------------------------------------------------------

    dependencias_modulo: List[Dict[str, Any]] = []

    for modulo in modulos:
        nombre = modulo.get("nombre")
        rol = modulo.get("rol")
        for requerido in modulo.get("requiere") or []:
            requerido = str(requerido).strip()

            destino = None

            for candidato in modulos:
                if (
                    candidato.get("nombre") == requerido
                    or candidato.get("id") == requerido
                    or candidato.get("rol") == requerido
                ):
                    destino = candidato
                    break

            dependencias_modulo.append({
                "desde": {
                    "modulo": nombre,
                    "rol": rol,
                },
                "hacia": requerido,
                "estado": (
                    "encontrada"
                    if destino is not None
                    else "no_resuelta"
                ),
            })

    # -----------------------------------------------------------
    # 13. VALIDACIÓN DE CAPACIDADES CONTRACTUALES
    # -----------------------------------------------------------

    capacidades_requeridas = {
        "anunciar",
        "anunciar_todo",
        "citar",
        "registrar",
        "resolver_enunciado",
        "inventario",
        "barrer",
        "verificar",
        "limpiar_ciclo",
    }

    capacidades_presentes = set(
        str(x.get("nombre"))
        for x in capacidades
    )

    for capacidad in sorted(
        capacidades_requeridas - capacidades_presentes
    ):
        errores.append({
            "tipo": "capacidad_contractual_ausente",
            "capacidad": capacidad,
        })

    # -----------------------------------------------------------
    # 14. RESTRICCIONES NEGATIVAS DEL OFICIO CIT
    # -----------------------------------------------------------

    prohibidas = (
        "calcular_C",
        "calcular_L",
        "calcular_K",
        "calcular_Tru",
        "fijar_O",
        "evaluar_verdad_personal",
        "interpretar_estados_mentales",
        "orquestar_modulos",
        "aprobar_material_realidad",
    )

    nombres_capacidades = {
        str(x.get("nombre")).lower()
        for x in capacidades
    }

    for prohibida in prohibidas:
        if prohibida.lower() in nombres_capacidades:
            errores.append({
                "tipo": "capacidad_prohibida",
                "capacidad": prohibida,
            })

    # -----------------------------------------------------------
    # 15. ESTADO ESTRUCTURAL
    # -----------------------------------------------------------

    coherente = not errores

    estado = "OPERATIVO" if coherente else "INCONSISTENTE"

    # -----------------------------------------------------------
    # 16. SALIDA COMPLETA
    # -----------------------------------------------------------

    return {
        "id": _ID,
        "nombre": _NOMBRE,
        "rol": _ROL,
        "version": _VERSION,
        "version_contrato": _VERSION_CONTRATO,

        "estado": estado,
        "coherente": coherente,

        "contrato": contrato,

        "errores": errores,
        "errores_n": len(errores),

        "advertencias": advertencias,
        "advertencias_n": len(advertencias),

        "modulos": modulos,
        "modulos_n": len(modulos),

        "capacidades": capacidades,
        "capacidades_n": len(capacidades),

        "declaraciones": declaraciones,
        "declaraciones_n": len(declaraciones),

        "duplicados": duplicados,
        "duplicados_n": len(duplicados),

        "relaciones": relaciones,
        "relaciones_n": len(relaciones),

        "dependencias": dependencias,
        "dependencias_n": len(dependencias),

        "dependencias_modulo": dependencias_modulo,
        "dependencias_modulo_n": len(dependencias_modulo),

        "cadenas": cadenas,
        "ciclos": ciclos,
        "ciclos_n": len(ciclos),

        "tipos_declaracion": tipos_validos,
        "campos_obligatorios": campos_obligatorios,
        "relaciones_validas": relaciones_validas,

        "registro_n": len(registro_local),

        "reglas": {
            "identidad_declaracion": "(fuente_modulo, id)",
            "duplicidad": (
                "El mismo id en módulos diferentes es válido; "
                "el mismo id repetido dentro del mismo módulo es duplicado."
            ),
            "dependencias": (
                "Se resuelven por módulo + id; no se inventan nodos."
            ),
            "ciclos": (
                "Un ciclo estructural se informa como ciclo; "
                "no se convierte automáticamente en contradicción."
            ),
            "ausencia": (
                "Una dependencia ausente se informa como no resuelta; "
                "no se convierte en contradicción ni en premisa."
            ),
            "citacion": (
                "CIT documenta declaraciones existentes y sus relaciones; "
                "no recalcula su contenido."
            ),
        },

        "nota": (
            "Barrer estructural de CIT. La identidad documental es "
            "(modulo,id), por lo que la reutilización de un mismo ID "
            "entre módulos no constituye duplicidad. El barrido inspecciona "
            "contrato, capacidades, declaraciones, relaciones, dependencias "
            "y cadenas sin modificar conocimiento de origen."
        ),
    }


def verificar_salida(salida: Any) -> bool:
    """
    Verificación contractual de la salida producida por barrer.

    No interpreta verdad matemática.
    Solo verifica que la salida tenga la estructura mínima
    producida por el barrido CIT.
    """
    if not isinstance(salida, dict):
        return False

    campos = (
        "id",
        "nombre",
        "rol",
        "version",
        "estado",
        "coherente",
        "errores",
        "advertencias",
        "modulos",
        "capacidades",
        "declaraciones",
        "duplicados",
        "relaciones",
        "dependencias",
        "dependencias_modulo",
        "cadenas",
        "ciclos",
    )

    if any(campo not in salida for campo in campos):
        return False

    if not isinstance(salida.get("coherente"), bool):
        return False

    for campo in campos:
        if campo in (
            "errores",
            "advertencias",
            "modulos",
            "capacidades",
            "declaraciones",
            "duplicados",
            "relaciones",
            "dependencias",
            "dependencias_modulo",
            "cadenas",
            "ciclos",
        ):
            if not isinstance(salida.get(campo), list):
                return False

    if salida.get("coherente") and salida.get("errores"):
        return False

    if not salida.get("coherente") and not salida.get("errores"):
        return False

    return True


def verificar(peticion: Any = None) -> Dict[str, Any]:
    """
    Alias contractual de barrer.
    Una única implementación de auditoría.
    """
    return barrer(peticion)


# ===============================================================
# FIN SECCIÓN 34
# ===============================================================

# ===============================================================
# 35 ejecutar_total
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


# ===============================================================
# 36 inspeccionar
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
        "errores": errores,
        "autoriza_engine": CONTENEDOR.get("autoriza_engine"),
        "reporting": CONTENEDOR.get("reporting"),
        "invariantes": CONTENEDOR.get("invariantes"),
    }


# ===============================================================
# 37 registrar_inventario
# ===============================================================

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
# 38 RESOLUCIÓN Y EXPORTACIONES
# ===============================================================

_CAP_MAP = {
    # --- CENTINELA ---
    "verificar": verificar,
    "barrer": barrer,
    "verificar_salida": verificar_salida,

    # --- INVENTARIO Y REPORTING ---
    "inventario": inventario,
    "reporte": reporte,
    "diagnostico": diagnostico,

    # --- OPERACIONES DE CITACIÓN ---
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

    # --- COMPATIBILIDAD ENGINE ---
    "evaluar": anunciar,

    # --- CAPACIDADES ARQUITECTÓNICAS ---
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
# FIN RESOLUCIÓN Y EXPORTACIONES
# ===============================================================


