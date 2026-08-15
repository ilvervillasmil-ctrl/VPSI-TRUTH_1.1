# ===============================================================
# VPSI-TRUTH — modules/cache/__init__.py
# ===============================================================
#
# MÓDULO:              cache
# ID:                  CH
# Rol:                 CH
# Versión módulo:      4.1
# Versión contrato:    1.0
# Esquema contrato:    VPSI-CONTRACT-1.0
# Estabilidad:         ESTABLE
# Compatible desde:    1.0
# API Engine:          >=1.0
#
# Función:
#   Registrador universal de eventos.
#   Libro de actas del sistema.
#   Mapeo estructural completo del código accesible.
#   Clasificación de IDs por módulo y detección de duplicados.
#
#   CACHE no interpreta semántica.
#   CACHE no deduce causas.
#   CACHE conserva evidencia y estructura.
#
# Principio:
#   Engine produce.
#   Centinela verifica.
#   CACHE conserva y mapea.
#   (Futuro) Analizadores interpretan.
#   Omega presenta.
#
# ===============================================================


# ===============================================================
# PARTE 1 — PRINCIPIOS, BANDERAS Y ESPECIFICACIONES PRECISAS
# ===============================================================

# ===============================================================
# 1.1 — IMPORTACIONES
# ===============================================================

from __future__ import annotations

import ast
import copy
import importlib.util
import sys
import threading
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# ===============================================================
# FIN 1.1
# ===============================================================


# ===============================================================
# 1.2 — IDENTIDAD
# ===============================================================

ID_MODULO = "CH"
NOMBRE_MODULO = "cache"
ROL_MODULO = "CH"

# ===============================================================
# FIN 1.2
# ===============================================================


# ===============================================================
# 1.3 — VERSIONES Y ESTABILIDAD
# ===============================================================

VERSION_MODULO = "4.1"
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
# 1.5 — CAMPOS DEL REGISTRO NEUTRO
# ===============================================================

CAMPOS_REGISTRO = (
    "seq",
    "timestamp",
    "run_id",
    "ciclo_id",
    "origen",
    "destino",
    "modulo",
    "capacidad",
    "tipo",
    "categoria",
    "estado",
    "payload",
)

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
    "este módulo no calcula",
    "este módulo no interpreta",
    "este módulo no deduce ni infiere",
    "este módulo no reconstruye ni genera grafos interpretativos",
    "la evidencia depositada nunca se modifica",
    "la evidencia depositada nunca se sobrescribe",
    "la evidencia depositada nunca se reordena",
    "la evidencia depositada nunca desaparece durante el ciclo",
    "toda información nueva se incorpora solo como evento nuevo",
    "las categorías son dinámicas; no hay lista fija de dominios",
    "este módulo no inventa capacidades no declaradas en CONTENEDOR",
    "el mapeo estructural no ejecuta funciones descubiertas",
    "un ID duplicado se clasifica, no se borra ni se interpreta como error automático",
)

# ===============================================================
# FIN 1.6
# ===============================================================


# ===============================================================
# 1.7 — CONFIGURACIÓN DE RUTAS
# ===============================================================

_DIR = Path(__file__).resolve().parent
# Raíz de modules/ (hermano de cache)
_MODULES_ROOT = _DIR.parent

# ===============================================================
# FIN 1.7
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


class CacheError(Exception):
    """Error de forma o de integridad del módulo cache."""
    pass


class CacheInmutableError(CacheError):
    """Intento de modificar evidencia ya depositada."""
    pass

# ===============================================================
# FIN 4.1
# ===============================================================


# ===============================================================
# 4.2 — REGISTRO DE EVENTOS (APPEND-ONLY)
# ===============================================================

class _RegistroEventos:
    """
    Almacén append-only de registros neutros.
    No interpreta. No indexa relaciones semánticas. Solo guarda y filtra.
    """

    # -----------------------------------------------------------
    # 4.2.1 — Inicialización
    # -----------------------------------------------------------
    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._eventos: List[Dict[str, Any]] = []
        self._seq = 0
        self._categorias: set = set()

    # -----------------------------------------------------------
    # 4.2.2 — Append (única vía de escritura)
    # -----------------------------------------------------------
    def append(self, datos: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(datos, dict):
            raise CacheError("datos debe ser dict")
        with self._lock:
            self._seq += 1
            categoria = datos.get("categoria")
            if categoria is not None:
                self._categorias.add(str(categoria))
            entrada = {
                "seq": self._seq,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "run_id": datos.get("run_id"),
                "ciclo_id": datos.get("ciclo_id"),
                "origen": datos.get("origen"),
                "destino": datos.get("destino"),
                "modulo": datos.get("modulo"),
                "capacidad": datos.get("capacidad"),
                "tipo": datos.get("tipo") or "evento",
                "categoria": categoria,
                "estado": datos.get("estado"),
                "payload": copy.deepcopy(datos.get("payload") or {}),
            }
            if isinstance(entrada["payload"], dict):
                for k in CAMPOS_REGISTRO:
                    entrada["payload"].pop(k, None)
            self._eventos.append(entrada)
            return copy.deepcopy(entrada)

    # -----------------------------------------------------------
    # 4.2.3 — Filtrar
    # -----------------------------------------------------------
    def filtrar(
        self,
        *,
        ciclo_id: Optional[str] = None,
        run_id: Optional[str] = None,
        modulo: Optional[str] = None,
        tipo: Optional[str] = None,
        categoria: Optional[str] = None,
        capacidad: Optional[str] = None,
        origen: Optional[str] = None,
        destino: Optional[str] = None,
        estado: Optional[str] = None,
        desde_seq: Optional[int] = None,
        hasta_seq: Optional[int] = None,
        desde_timestamp: Optional[str] = None,
        hasta_timestamp: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        with self._lock:
            out: List[Dict[str, Any]] = []
            for e in self._eventos:
                if ciclo_id is not None and str(e.get("ciclo_id")) != str(ciclo_id):
                    continue
                if run_id is not None and str(e.get("run_id")) != str(run_id):
                    continue
                if modulo is not None and str(e.get("modulo")) != str(modulo):
                    continue
                if tipo is not None and e.get("tipo") != tipo:
                    continue
                if categoria is not None and str(e.get("categoria")) != str(categoria):
                    continue
                if capacidad is not None and str(e.get("capacidad")) != str(capacidad):
                    continue
                if origen is not None and str(e.get("origen")) != str(origen):
                    continue
                if destino is not None and str(e.get("destino")) != str(destino):
                    continue
                if estado is not None and str(e.get("estado")) != str(estado):
                    continue
                seq = int(e.get("seq") or 0)
                if desde_seq is not None and seq < int(desde_seq):
                    continue
                if hasta_seq is not None and seq > int(hasta_seq):
                    continue
                ts = e.get("timestamp") or ""
                if desde_timestamp is not None and ts < str(desde_timestamp):
                    continue
                if hasta_timestamp is not None and ts > str(hasta_timestamp):
                    continue
                out.append(copy.deepcopy(e))
            return out

    # -----------------------------------------------------------
    # 4.2.4 — Categorías conocidas
    # -----------------------------------------------------------
    def categorias_conocidas(self) -> List[str]:
        with self._lock:
            return sorted(self._categorias)

    # -----------------------------------------------------------
    # 4.2.5 — Resumen
    # -----------------------------------------------------------
    def resumen(self) -> Dict[str, Any]:
        with self._lock:
            por_tipo: Dict[str, int] = defaultdict(int)
            por_cat: Dict[str, int] = defaultdict(int)
            ciclos: set = set()
            for e in self._eventos:
                por_tipo[str(e.get("tipo"))] += 1
                if e.get("categoria") is not None:
                    por_cat[str(e.get("categoria"))] += 1
                if e.get("ciclo_id") is not None:
                    ciclos.add(str(e.get("ciclo_id")))
            return {
                "total_eventos": len(self._eventos),
                "ciclos": len(ciclos),
                "seq_actual": self._seq,
                "por_tipo": dict(por_tipo),
                "por_categoria": dict(por_cat),
                "categorias": sorted(self._categorias),
                "inmutable": True,
            }

    # -----------------------------------------------------------
    # 4.2.6 — Verificar integridad
    # -----------------------------------------------------------
    def verificar_integridad(self) -> List[str]:
        errores: List[str] = []
        with self._lock:
            seq_prev = 0
            for i, e in enumerate(self._eventos):
                if not isinstance(e, dict):
                    errores.append("evento[{0}] no es dict".format(i))
                    continue
                for campo in ("seq", "timestamp", "tipo", "payload"):
                    if campo not in e:
                        errores.append(
                            "evento[{0}] sin campo '{1}'".format(i, campo)
                        )
                seq = e.get("seq")
                if not isinstance(seq, int):
                    errores.append("evento[{0}] seq no es int".format(i))
                elif seq <= seq_prev:
                    errores.append(
                        "evento[{0}] seq no creciente: {1} <= {2}".format(
                            i, seq, seq_prev
                        )
                    )
                else:
                    seq_prev = seq
                if not e.get("timestamp"):
                    errores.append("evento[{0}] sin timestamp".format(i))
                if not isinstance(e.get("payload"), dict):
                    errores.append(
                        "evento[{0}] payload no es dict".format(i)
                    )
        return errores

    # -----------------------------------------------------------
    # 4.2.7 — Barreras de inmutabilidad
    # -----------------------------------------------------------
    def intentar_modificar(self, *args: Any, **kwargs: Any) -> None:
        raise CacheInmutableError(
            "CACHE no modifica evidencia depositada; solo registra"
        )

    def intentar_borrar_evento(self, *args: Any, **kwargs: Any) -> None:
        raise CacheInmutableError(
            "CACHE no borra evidencia en operación normal (append-only)"
        )

# ===============================================================
# FIN 4.2
# ===============================================================


# ===============================================================
# 4.3 — INSTANCIA GLOBAL DEL REGISTRO
# ===============================================================

_registro = _RegistroEventos()

# ===============================================================
# FIN 4.3
# ===============================================================


# ===============================================================
# 4.4 — INVENTARIO ESTRUCTURAL INTERNO
# ===============================================================
#
# Conserva apariciones sin sobrescribirlas.
# El mismo ID puede aparecer en varios módulos.
#

_inventario_estructural: Dict[str, Any] = {
    "modulos": {},      # nombre_modulo → {archivos, ids, funciones, clases, callables, capacidades}
    "ids": {},          # id → [modulos donde aparece]
    "funciones": {},    # nombre_calificado → {modulo, archivo, linea}
    "clases": {},       # nombre_calificado → {modulo, archivo, linea, metodos}
    "callables": {},    # nombre_calificado → {modulo, archivo, tipo}
    "capacidades": {},  # nombre_modulo → [capacidades declaradas]
    "actualizado": None,
}

# ===============================================================
# FIN 4.4
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
        "Registrador universal de eventos. Libro de actas del sistema. "
        "Mapeo estructural del código accesible. "
        "Clasificación de IDs por módulo y detección de duplicados. "
        "Conserva evidencia objetiva. Categorías dinámicas. "
        "No interpreta. No deduce. No reconstruye semánticamente. No calcula."
    ),

    # ============================================================
    # 5.3 — PROPÓSITO
    # ============================================================
    "funcion": (
        "Registrar exactamente lo que ocurrió durante la ejecución, "
        "exponer lecturas filtradas por campos del registro, "
        "mapear la estructura del código accesible y "
        "clasificar IDs por módulo incluyendo duplicados. "
        "Nada más."
    ),
    "no_hace": [
        "No interpreta",
        "No deduce ni infiere",
        "No reconstruye ciclos semánticamente",
        "No genera grafos interpretativos ni árboles de causalidad",
        "No explica razonamientos ni causas",
        "No calcula C / L / K / Tru",
        "No descubre relaciones semánticas",
        "No altera evidencia depositada",
        "No inicia operaciones de otros módulos",
        "No envía reportes a otros módulos",
        "No ejecuta funciones descubiertas durante el mapeo",
    ],

    # ============================================================
    # 5.4 — AUTORIDAD
    # ============================================================
    "autoridad": [
        "Registrar eventos depositados por Engine o Centinela",
        "Entregar lecturas filtradas por campos del registro",
        "Exponer categorías descubiertas dinámicamente",
        "Verificar integridad del registro (forma, no contenido)",
        "Mapear estructura del código accesible",
        "Clasificar IDs por módulo y reportar duplicados",
        "Reportar estado, inventario y diagnóstico propios",
    ],

    # ============================================================
    # 5.5 — CONOCIMIENTO EXPORTABLE
    # ============================================================
    "conocimiento_exportable": [
        "depositar",
        "leer",
        "leer_eventos",
        "leer_por_ciclo",
        "leer_por_modulo",
        "leer_por_tipo",
        "leer_por_categoria",
        "leer_por_capacidad",
        "leer_por_origen",
        "leer_por_destino",
        "leer_por_estado",
        "leer_por_seq",
        "leer_por_timestamp",
        "categorias",
        "inventario",
        "reporte",
        "diagnostico",
        "backend_para_centinela",
        "ejecutar_total",
        "inspeccionar",
        "registrar_inventario",
        "mapear_codigo",
        "clasificar_ids",
    ],

    # ============================================================
    # 5.6 — ACCESO
    # ============================================================
    "acceso": {
        "nivel": "completo",
        "descripcion": "Acceso total a recursos del módulo y al árbol modules/",
    },

    # ============================================================
    # 5.7 — DEPENDENCIAS
    # ============================================================
    "requiere": [
        "CT", "AX", "FO", "MC", "SF", "CA", "CX", "CC",
        "DI", "RE", "VX", "TX", "CIT", "TT", "CE",
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
    # 5.10 — CONSULTAS SOPORTADAS
    # ============================================================
    "consultas_soportadas": [
        "depositar_evento",
        "leer_eventos",
        "filtrar_por_campo",
        "listar_categorias",
        "obtener_inventario",
        "obtener_reporte",
        "obtener_diagnostico",
        "verificar_integridad_registro",
        "mapear_codigo",
        "clasificar_ids",
    ],

    # ============================================================
    # 5.11 — AUTORIZACIÓN AL ENGINE
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
        "alterar": False,
        "crear": True,
        "actualizar": False,

        # --- PERMISOS DE PROCESAMIENTO ---
        "validar": True,
        "procesar": True,
        "analizar": True,
        "generar": True,

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

        # --- PERMISOS OBLIGATORIOS ---
        "validar_esquema": True,
        "acceso_archivos": True,

        # --- BANDERAS NUEVAS (OBLIGATORIAS ENGINE) ---
        "ejecutar_total": True,
        "inspeccionar": True,
        "registrar_inventario": True,
    },

    # ============================================================
    # 5.12 — CAPACIDADES (solo unidades ejecutables)
    # ============================================================
    "capacidades": {
        "verificar": "barrer",
        "barrer": "barrer",
        "depositar": "depositar",
        "leer": "leer",
        "leer_eventos": "leer_eventos",
        "leer_por_ciclo": "leer_por_ciclo",
        "leer_por_modulo": "leer_por_modulo",
        "leer_por_tipo": "leer_por_tipo",
        "leer_por_categoria": "leer_por_categoria",
        "leer_por_capacidad": "leer_por_capacidad",
        "leer_por_origen": "leer_por_origen",
        "leer_por_destino": "leer_por_destino",
        "leer_por_estado": "leer_por_estado",
        "leer_por_seq": "leer_por_seq",
        "leer_por_timestamp": "leer_por_timestamp",
        "categorias": "categorias",
        "inventario": "inventario",
        "reporte": "reporte",
        "diagnostico": "diagnostico",
        "verificar_salida": "verificar_salida",
        "backend_para_centinela": "backend_para_centinela",
        "ejecutar_total": "ejecutar_total",
        "inspeccionar": "inspeccionar",
        "registrar_inventario": "registrar_inventario",
        "mapear_codigo": "mapear_codigo",
        "clasificar_ids": "clasificar_ids",
    },

    # ============================================================
    # 5.13 — METADATOS DE CAPACIDADES (1:1)
    # ============================================================
    "capacidades_meta": {
        "verificar": {
            "descripcion": "Alias de barrer. Integridad formal del registro.",
            "entrada": "ninguna",
            "validar_esquema": ["*"],
            "salida": "dict con coherente, inmutable, errores, resumen",
            "acceso_archivos": ["*"],
        },
        "barrer": {
            "descripcion": (
                "Verifica forma del registro: seq creciente, timestamps, "
                "payload dict. No interpreta contenido. No mapea código."
            ),
            "entrada": "ninguna",
            "validar_esquema": ["*"],
            "salida": "dict con coherente, inmutable, errores, resumen",
            "acceso_archivos": ["*"],
        },
        "depositar": {
            "descripcion": (
                "Registra un evento neutro. Única vía de escritura. "
                "Append-only. Categorías se descubren al depositar."
            ),
            "entrada": (
                "tipo, payload, ciclo_id?, run_id?, origen?, destino?, "
                "modulo?, capacidad?, categoria?, estado?"
            ),
            "validar_esquema": ["*"],
            "salida": "dict del evento registrado",
            "acceso_archivos": ["*"],
        },
        "leer": {
            "descripcion": "Lectura genérica con filtros opcionales por campo.",
            "entrada": "filtros opcionales por campo del registro",
            "validar_esquema": ["*"],
            "salida": "list[dict]",
            "acceso_archivos": ["*"],
        },
        "leer_eventos": {
            "descripcion": "Alias de leer sin filtros (todos los eventos).",
            "entrada": "ninguna",
            "validar_esquema": ["*"],
            "salida": "list[dict]",
            "acceso_archivos": ["*"],
        },
        "leer_por_ciclo": {
            "descripcion": "Eventos de un ciclo_id.",
            "entrada": "ciclo_id: str",
            "validar_esquema": ["*"],
            "salida": "list[dict]",
            "acceso_archivos": ["*"],
        },
        "leer_por_modulo": {
            "descripcion": "Eventos de un módulo.",
            "entrada": "modulo: str, ciclo_id?",
            "validar_esquema": ["*"],
            "salida": "list[dict]",
            "acceso_archivos": ["*"],
        },
        "leer_por_tipo": {
            "descripcion": "Eventos de un tipo.",
            "entrada": "tipo: str, ciclo_id?",
            "validar_esquema": ["*"],
            "salida": "list[dict]",
            "acceso_archivos": ["*"],
        },
        "leer_por_categoria": {
            "descripcion": "Eventos de una categoría (dinámica).",
            "entrada": "categoria: str, ciclo_id?",
            "validar_esquema": ["*"],
            "salida": "list[dict]",
            "acceso_archivos": ["*"],
        },
        "leer_por_capacidad": {
            "descripcion": "Eventos de una capacidad.",
            "entrada": "capacidad: str, ciclo_id?",
            "validar_esquema": ["*"],
            "salida": "list[dict]",
            "acceso_archivos": ["*"],
        },
        "leer_por_origen": {
            "descripcion": "Eventos con un origen dado.",
            "entrada": "origen: str, ciclo_id?",
            "validar_esquema": ["*"],
            "salida": "list[dict]",
            "acceso_archivos": ["*"],
        },
        "leer_por_destino": {
            "descripcion": "Eventos con un destino dado.",
            "entrada": "destino: str, ciclo_id?",
            "validar_esquema": ["*"],
            "salida": "list[dict]",
            "acceso_archivos": ["*"],
        },
        "leer_por_estado": {
            "descripcion": "Eventos con un estado dado.",
            "entrada": "estado: str, ciclo_id?",
            "validar_esquema": ["*"],
            "salida": "list[dict]",
            "acceso_archivos": ["*"],
        },
        "leer_por_seq": {
            "descripcion": "Eventos en un rango de seq.",
            "entrada": "desde_seq?, hasta_seq?",
            "validar_esquema": ["*"],
            "salida": "list[dict]",
            "acceso_archivos": ["*"],
        },
        "leer_por_timestamp": {
            "descripcion": "Eventos en un rango de timestamp.",
            "entrada": "desde_timestamp?, hasta_timestamp?",
            "validar_esquema": ["*"],
            "salida": "list[dict]",
            "acceso_archivos": ["*"],
        },
        "categorias": {
            "descripcion": "Categorías descubiertas dinámicamente hasta ahora.",
            "entrada": "ninguna",
            "validar_esquema": ["*"],
            "salida": "list[str]",
            "acceso_archivos": ["*"],
        },
        "inventario": {
            "descripcion": (
                "Inventario del módulo, resumen del registro y, "
                "si disponible, inventario estructural mapeado."
            ),
            "entrada": "ninguna",
            "validar_esquema": ["*"],
            "salida": "dict con id, version, memoria, categorias, capacidades, estructura",
            "acceso_archivos": ["*"],
        },
        "reporte": {
            "descripcion": "Reporte interno de estado del módulo CH.",
            "entrada": "ninguna",
            "validar_esquema": ["*"],
            "salida": "dict con estado, coherente, memoria, capacidades",
            "acceso_archivos": ["*"],
        },
        "diagnostico": {
            "descripcion": "Diagnóstico de integridad formal del registro.",
            "entrada": "ninguna",
            "validar_esquema": ["*"],
            "salida": "dict con estado, problemas, advertencias, recomendaciones",
            "acceso_archivos": ["*"],
        },
        "verificar_salida": {
            "descripcion": "Comprueba forma de una salida de barrer o depósito.",
            "entrada": "salida: dict",
            "validar_esquema": ["*"],
            "salida": "bool",
            "acceso_archivos": ["*"],
        },
        "backend_para_centinela": {
            "descripcion": (
                "Adaptador estable CacheBackend para Centinela. "
                "Centinela no conoce la implementación interna."
            ),
            "entrada": "ninguna",
            "validar_esquema": ["*"],
            "salida": "CacheBackend",
            "acceso_archivos": ["*"],
        },
        "ejecutar_total": {
            "descripcion": (
                "Operación arquitectónica genérica. "
                "Ejerce la totalidad de las unidades operativamente "
                "ejecutables del módulo conforme a su contrato e inventario."
            ),
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["*"],
            "salida": "dict con resultados de las unidades ejecutadas",
            "acceso_archivos": ["*"],
        },
        "inspeccionar": {
            "descripcion": (
                "Capacidad meta de inspección estructural del módulo. "
                "Expone capacidades contractuales, callables reales, "
                "estructura descubierta, IDs y duplicados."
            ),
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["acceso_archivos"],
            "salida": "dict con estructura, capacidades y estado del módulo",
            "acceso_archivos": ["acceso_archivos"],
        },
        "registrar_inventario": {
            "descripcion": (
                "Registra el inventario estructural del módulo "
                "sin alterar evidencia depositada."
            ),
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["acceso_archivos"],
            "salida": "dict con inventario registrado",
            "acceso_archivos": ["acceso_archivos"],
        },
        "mapear_codigo": {
            "descripcion": (
                "Recorre el código accesible a CACHE y obtiene la estructura "
                "real: módulos, archivos, IDs, funciones, métodos, clases, "
                "callables y capacidades declaradas. No interpreta semántica. "
                "No ejecuta funciones descubiertas."
            ),
            "entrada": "peticion opcional (dict con raiz?)",
            "validar_esquema": ["*"],
            "salida": "dict con inventario estructural completo",
            "acceso_archivos": ["*"],
        },
        "clasificar_ids": {
            "descripcion": (
                "Clasifica IDs por módulo a partir del inventario estructural. "
                "Separa IDs únicos de IDs duplicados. "
                "Un duplicado es clasificación estructural, no error automático."
            ),
            "entrada": "peticion opcional (dict)",
            "validar_esquema": ["*"],
            "salida": (
                "dict con ids_por_modulo, ids_unicos, ids_duplicados, "
                "id_a_modulos"
            ),
            "acceso_archivos": ["*"],
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
        "mapear_codigo": True,
        "clasificar_ids": True,
    },

    # ============================================================
    # 5.15 — ESTADOS VÁLIDOS E INVARIANTES
    # ============================================================
    "estados_validos": list(ESTADOS_VALIDOS),
    "invariantes": list(INVARIANTES),
}

# ===============================================================
# FIN PARTE 5
# ===============================================================


# ===============================================================
# PARTE 7 — VALIDACIÓN DEL CONTRATO
# ===============================================================

# ===============================================================
# 7.1 — VALIDAR CONTRATO
# ===============================================================

def _validar_contrato(cont: Dict[str, Any]) -> None:
    """
    Valida que el CONTENEDOR cumpla el esquema contractual.
    Comprueba claves obligatorias, 1:1 capacidades ↔ meta,
    y tipos mínimos de capacidades_meta.
    """
    obligatorias = (
        "esquema", "version_contrato", "version_modulo",
        "id", "nombre", "rol", "descripcion",
        "funcion", "no_hace", "autoridad",
        "conocimiento_exportable", "requiere",
        "autoriza_engine", "consultas_soportadas",
        "capacidades", "capacidades_meta",
        "reporting", "estados_validos", "invariantes",
        "estabilidad", "compatible_desde", "api_engine",
        "acceso_archivos", "validar_esquema",
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
    if str(cont.get("version_contrato")) != VERSION_CONTRATO:
        raise ContratoInvalido(
            "{0}: version_contrato inválida: {1}".format(
                NOMBRE_MODULO, cont.get("version_contrato")
            )
        )

    caps = cont.get("capacidades") or {}
    meta_caps = cont.get("capacidades_meta") or {}
    if set(caps.keys()) != set(meta_caps.keys()):
        solo_caps = set(caps.keys()) - set(meta_caps.keys())
        solo_meta = set(meta_caps.keys()) - set(caps.keys())
        raise ContratoInvalido(
            "{0}: desajuste capacidades/capacidades_meta. "
            "solo_en_capacidades={1} solo_en_meta={2}".format(
                NOMBRE_MODULO, solo_caps, solo_meta
            )
        )

    for nombre_cap, entrada in meta_caps.items():
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

# ===============================================================
# FIN 7.1
# ===============================================================

# ===============================================================
# FIN PARTE 7
# ===============================================================


# ===============================================================
# PARTE 8 — CAPACIDADES PÚBLICAS
# ===============================================================

# ===============================================================
# 8.1 — DEPOSITAR
# ===============================================================

def depositar(
    tipo: str,
    payload: Optional[Dict[str, Any]] = None,
    *,
    ciclo_id: Optional[str] = None,
    run_id: Optional[str] = None,
    origen: Optional[str] = None,
    destino: Optional[str] = None,
    modulo: Optional[str] = None,
    capacidad: Optional[str] = None,
    categoria: Optional[str] = None,
    estado: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Registra un evento neutro. Única vía de escritura.
    Append-only. Categorías se descubren al depositar.
    """
    if not tipo or not isinstance(tipo, str):
        raise CacheError("tipo debe ser str no vacío")
    if payload is None:
        payload = {}
    if not isinstance(payload, dict):
        raise CacheError("payload debe ser dict")
    return _registro.append({
        "tipo": tipo,
        "payload": payload,
        "ciclo_id": ciclo_id,
        "run_id": run_id,
        "origen": origen or "desconocido",
        "destino": destino,
        "modulo": modulo,
        "capacidad": capacidad,
        "categoria": categoria,
        "estado": estado,
    })

# ===============================================================
# FIN 8.1
# ===============================================================


# ===============================================================
# 8.2 — LECTURAS
# ===============================================================

def leer(
    ciclo_id: Optional[str] = None,
    run_id: Optional[str] = None,
    modulo: Optional[str] = None,
    tipo: Optional[str] = None,
    categoria: Optional[str] = None,
    capacidad: Optional[str] = None,
    origen: Optional[str] = None,
    destino: Optional[str] = None,
    estado: Optional[str] = None,
    desde_seq: Optional[int] = None,
    hasta_seq: Optional[int] = None,
    desde_timestamp: Optional[str] = None,
    hasta_timestamp: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Lectura genérica. Solo filtros. Sin interpretación."""
    return _registro.filtrar(
        ciclo_id=ciclo_id,
        run_id=run_id,
        modulo=modulo,
        tipo=tipo,
        categoria=categoria,
        capacidad=capacidad,
        origen=origen,
        destino=destino,
        estado=estado,
        desde_seq=desde_seq,
        hasta_seq=hasta_seq,
        desde_timestamp=desde_timestamp,
        hasta_timestamp=hasta_timestamp,
    )


def leer_eventos() -> List[Dict[str, Any]]:
    return leer()


def leer_por_ciclo(ciclo_id: str) -> List[Dict[str, Any]]:
    if not ciclo_id:
        raise CacheError("ciclo_id obligatorio")
    return leer(ciclo_id=str(ciclo_id))


def leer_por_modulo(
    modulo: str, ciclo_id: Optional[str] = None
) -> List[Dict[str, Any]]:
    if not modulo:
        raise CacheError("modulo obligatorio")
    return leer(modulo=str(modulo), ciclo_id=ciclo_id)


def leer_por_tipo(
    tipo: str, ciclo_id: Optional[str] = None
) -> List[Dict[str, Any]]:
    if not tipo:
        raise CacheError("tipo obligatorio")
    return leer(tipo=str(tipo), ciclo_id=ciclo_id)


def leer_por_categoria(
    categoria: str, ciclo_id: Optional[str] = None
) -> List[Dict[str, Any]]:
    if not categoria:
        raise CacheError("categoria obligatoria")
    return leer(categoria=str(categoria), ciclo_id=ciclo_id)


def leer_por_capacidad(
    capacidad: str, ciclo_id: Optional[str] = None
) -> List[Dict[str, Any]]:
    if not capacidad:
        raise CacheError("capacidad obligatoria")
    return leer(capacidad=str(capacidad), ciclo_id=ciclo_id)


def leer_por_origen(
    origen: str, ciclo_id: Optional[str] = None
) -> List[Dict[str, Any]]:
    if not origen:
        raise CacheError("origen obligatorio")
    return leer(origen=str(origen), ciclo_id=ciclo_id)


def leer_por_destino(
    destino: str, ciclo_id: Optional[str] = None
) -> List[Dict[str, Any]]:
    if not destino:
        raise CacheError("destino obligatorio")
    return leer(destino=str(destino), ciclo_id=ciclo_id)


def leer_por_estado(
    estado: str, ciclo_id: Optional[str] = None
) -> List[Dict[str, Any]]:
    if not estado:
        raise CacheError("estado obligatorio")
    return leer(estado=str(estado), ciclo_id=ciclo_id)


def leer_por_seq(
    desde_seq: Optional[int] = None,
    hasta_seq: Optional[int] = None,
) -> List[Dict[str, Any]]:
    return leer(desde_seq=desde_seq, hasta_seq=hasta_seq)


def leer_por_timestamp(
    desde_timestamp: Optional[str] = None,
    hasta_timestamp: Optional[str] = None,
) -> List[Dict[str, Any]]:
    return leer(
        desde_timestamp=desde_timestamp,
        hasta_timestamp=hasta_timestamp,
    )


def categorias() -> List[str]:
    """Categorías descubiertas dinámicamente hasta ahora."""
    return _registro.categorias_conocidas()

# ===============================================================
# FIN 8.2
# ===============================================================

# ===============================================================
# 8.3 — MAPEO ESTRUCTURAL (mapear_codigo)
# ===============================================================

def _escanear_archivo_py(archivo: Path, nombre_modulo: str) -> Dict[str, Any]:
    """
    Escaneo estructural de un .py mediante AST.
    No importa. No ejecuta. No instancia. No llama código descubierto.

    Extrae:
      - funciones (nombre, linea)
      - clases y métodos (nombre, linea)
      - IDs contractuales: ID_MODULO / ID / id_modulo (Assign y AnnAssign)
        y CONTENEDOR["id"]
      - claves de CONTENEDOR["capacidades"] cuando sean determinables por AST

    Distingue:
      - error_lectura: el archivo no pudo leerse
      - errores_parse: el contenido no pudo parsearse como AST
    """
    resultado: Dict[str, Any] = {
        "archivo": str(archivo),
        "funciones": [],
        "clases": [],
        "metodos": [],
        "ids_declarados": [],
        "capacidades_keys": [],
        "error_lectura": None,
        "errores_parse": None,
    }

    # -----------------------------------------------------------
    # Lectura del archivo (separada del parseo AST)
    # -----------------------------------------------------------
    try:
        fuente = archivo.read_text(encoding="utf-8")
    except Exception as e:
        resultado["error_lectura"] = "{0}: {1}".format(type(e).__name__, e)
        return resultado

    # -----------------------------------------------------------
    # Parseo AST
    # -----------------------------------------------------------
    try:
        arbol = ast.parse(fuente, filename=str(archivo))
    except Exception as e:
        resultado["errores_parse"] = "{0}: {1}".format(type(e).__name__, e)
        return resultado

    # -----------------------------------------------------------
    # 1. Funciones y clases de nivel módulo (no anidadas)
    # -----------------------------------------------------------
    for nodo in arbol.body:
        if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)):
            resultado["funciones"].append({
                "nombre": nodo.name,
                "linea": nodo.lineno,
                "async": isinstance(nodo, ast.AsyncFunctionDef),
            })
        elif isinstance(nodo, ast.ClassDef):
            metodos = []
            for item in nodo.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    metodos.append({
                        "nombre": item.name,
                        "linea": item.lineno,
                    })
            resultado["clases"].append({
                "nombre": nodo.name,
                "linea": nodo.lineno,
                "metodos": metodos,
            })
            resultado["metodos"].extend([
                {
                    "clase": nodo.name,
                    "nombre": m["nombre"],
                    "linea": m["linea"],
                }
                for m in metodos
            ])

    # -----------------------------------------------------------
    # 2. IDs: Assign y AnnAssign de ID_MODULO / ID / id_modulo
    # -----------------------------------------------------------
    def _extraer_id_constante(valor_nodo: Any) -> Optional[str]:
        if isinstance(valor_nodo, ast.Constant) and isinstance(
            valor_nodo.value, str
        ):
            val = valor_nodo.value.strip()
            return val if val else None
        return None

    for nodo in arbol.body:
        # Assign: ID_MODULO = "XX"
        if isinstance(nodo, ast.Assign):
            for target in nodo.targets:
                if not isinstance(target, ast.Name):
                    continue
                if target.id not in ("ID_MODULO", "ID", "id_modulo"):
                    continue
                val = _extraer_id_constante(nodo.value)
                if val and val not in resultado["ids_declarados"]:
                    resultado["ids_declarados"].append(val)

        # AnnAssign: ID_MODULO: str = "XX"
        elif isinstance(nodo, ast.AnnAssign):
            if not isinstance(nodo.target, ast.Name):
                continue
            if nodo.target.id not in ("ID_MODULO", "ID", "id_modulo"):
                continue
            if nodo.value is None:
                continue
            val = _extraer_id_constante(nodo.value)
            if val and val not in resultado["ids_declarados"]:
                resultado["ids_declarados"].append(val)

    # -----------------------------------------------------------
    # 3. CONTENEDOR: "id" y "capacidades" vía AST (sin ejecutar)
    # -----------------------------------------------------------
    for nodo in arbol.body:
        valor = None
        # AnnAssign: CONTENEDOR: Dict[str, Any] = {...}
        if isinstance(nodo, ast.AnnAssign) and isinstance(nodo.target, ast.Name):
            if nodo.target.id == "CONTENEDOR":
                valor = nodo.value
        # Assign: CONTENEDOR = {...}
        elif isinstance(nodo, ast.Assign):
            for target in nodo.targets:
                if isinstance(target, ast.Name) and target.id == "CONTENEDOR":
                    valor = nodo.value
                    break
        if valor is None or not isinstance(valor, ast.Dict):
            continue

        for key_node, val_node in zip(valor.keys, valor.values):
            if not isinstance(key_node, ast.Constant):
                continue
            if not isinstance(key_node.value, str):
                continue
            clave = key_node.value

            # CONTENEDOR["id"] = "XX"
            if clave == "id":
                val = _extraer_id_constante(val_node)
                if val and val not in resultado["ids_declarados"]:
                    resultado["ids_declarados"].append(val)

            # CONTENEDOR["capacidades"] = { "k": ..., ... }
            if clave == "capacidades" and isinstance(val_node, ast.Dict):
                for ck in val_node.keys:
                    if isinstance(ck, ast.Constant) and isinstance(ck.value, str):
                        k = ck.value.strip()
                        if k and k not in resultado["capacidades_keys"]:
                            resultado["capacidades_keys"].append(k)

    return resultado


def mapear_codigo(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Recorre el árbol accesible (_MODULES_ROOT o peticion["raiz"]) y
    construye el inventario estructural completo mediante AST.

    No importa. No ejecuta. No instancia. No llama código descubierto.
    Conserva todas las apariciones (módulo, archivo, línea).
    Actualiza _inventario_estructural con el snapshot de esta ejecución.
    """
    global _inventario_estructural

    # -----------------------------------------------------------
    # 1. Resolver raíz
    # -----------------------------------------------------------
    raiz = _MODULES_ROOT
    if isinstance(peticion, dict) and peticion.get("raiz"):
        candidata = Path(str(peticion["raiz"]))
        if candidata.exists() and candidata.is_dir():
            raiz = candidata

    # -----------------------------------------------------------
    # 2. Estructuras de acumulación (listas = sin sobrescritura)
    # -----------------------------------------------------------
    modulos: Dict[str, Any] = {}
    ids: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    funciones: List[Dict[str, Any]] = []
    clases: List[Dict[str, Any]] = []
    callables: List[Dict[str, Any]] = []
    capacidades: Dict[str, List[str]] = {}

    # Corrección: debe existir Y ser directorio
    if not raiz.exists() or not raiz.is_dir():
        _inventario_estructural = {
            "modulos": {},
            "ids": {},
            "funciones": [],
            "clases": [],
            "callables": [],
            "capacidades": {},
            "actualizado": datetime.now(timezone.utc).isoformat(),
            "raiz": str(raiz),
            "error": "raiz_inexistente",
        }
        return {
            "id": ID_MODULO,
            "operacion": "mapear_codigo",
            "error": "raiz_inexistente",
            "raiz": str(raiz),
            "modulos": {},
            "total_modulos": 0,
            "total_ids": 0,
            "total_funciones": 0,
            "total_clases": 0,
            "total_callables": 0,
            "total_capacidades": 0,
        }

    # -----------------------------------------------------------
    # 3. Recorrer cada subdirectorio = módulo candidato
    # -----------------------------------------------------------
    for sub in sorted(raiz.iterdir()):
        if not sub.is_dir():
            continue
        if sub.name.startswith(("_", ".")):
            continue

        nombre_mod = sub.name
        archivos_info: List[Dict[str, Any]] = []
        ids_mod: List[str] = []
        caps_mod: List[str] = []
        funcs_mod: List[str] = []
        clases_mod: List[str] = []

        for py in sorted(sub.glob("**/*.py")):
            esc = _escanear_archivo_py(py, nombre_mod)
            archivos_info.append(esc)

            # --- IDs (todas las apariciones) ---
            for idv in esc.get("ids_declarados") or []:
                if idv not in ids_mod:
                    ids_mod.append(idv)
                ids[idv].append({
                    "modulo": nombre_mod,
                    "archivo": esc["archivo"],
                })

            # --- Capacidades (AST de CONTENEDOR) ---
            for ck in esc.get("capacidades_keys") or []:
                if ck not in caps_mod:
                    caps_mod.append(ck)

            # --- Funciones ---
            for f in esc.get("funciones") or []:
                funciones.append({
                    "modulo": nombre_mod,
                    "archivo": esc["archivo"],
                    "nombre": f["nombre"],
                    "linea": f["linea"],
                    "async": f.get("async", False),
                })
                callables.append({
                    "modulo": nombre_mod,
                    "archivo": esc["archivo"],
                    "nombre": f["nombre"],
                    "linea": f["linea"],
                    "tipo": "funcion",
                })
                if f["nombre"] not in funcs_mod:
                    funcs_mod.append(f["nombre"])

            # --- Clases y métodos ---
            for c in esc.get("clases") or []:
                clases.append({
                    "modulo": nombre_mod,
                    "archivo": esc["archivo"],
                    "nombre": c["nombre"],
                    "linea": c["linea"],
                    "metodos": [m["nombre"] for m in c.get("metodos") or []],
                })
                callables.append({
                    "modulo": nombre_mod,
                    "archivo": esc["archivo"],
                    "nombre": c["nombre"],
                    "linea": c["linea"],
                    "tipo": "clase",
                })
                if c["nombre"] not in clases_mod:
                    clases_mod.append(c["nombre"])
                for m in c.get("metodos") or []:
                    callables.append({
                        "modulo": nombre_mod,
                        "archivo": esc["archivo"],
                        "nombre": m["nombre"],
                        "clase": c["nombre"],
                        "linea": m["linea"],
                        "tipo": "metodo",
                    })

        if caps_mod:
            capacidades[nombre_mod] = list(caps_mod)

        modulos[nombre_mod] = {
            "archivos": [a["archivo"] for a in archivos_info],
            "ids": ids_mod,
            "funciones": funcs_mod,
            "clases": clases_mod,
            "capacidades": list(caps_mod),
            "detalle_archivos": archivos_info,
        }

    # -----------------------------------------------------------
    # 4. Snapshot completo → _inventario_estructural
    # -----------------------------------------------------------
    ahora = datetime.now(timezone.utc).isoformat()
    _inventario_estructural = {
        "modulos": modulos,
        "ids": dict(ids),
        "funciones": funciones,
        "clases": clases,
        "callables": callables,
        "capacidades": capacidades,
        "actualizado": ahora,
        "raiz": str(raiz),
    }

    total_caps = sum(len(v) for v in capacidades.values())

    return {
        "id": ID_MODULO,
        "operacion": "mapear_codigo",
        "raiz": str(raiz),
        "total_modulos": len(modulos),
        "total_ids": len(ids),
        "total_funciones": len(funciones),
        "total_clases": len(clases),
        "total_callables": len(callables),
        "total_capacidades": total_caps,
        "modulos": sorted(modulos.keys()),
        "capacidades_por_modulo": {
            m: list(cs) for m, cs in capacidades.items()
        },
        "actualizado": ahora,
        "nota": (
            "Mapeo estructural puro por AST. "
            "No ejecuta código descubierto. "
            "No interpreta semántica. "
            "Todas las apariciones se conservan."
        ),
    }

# ===============================================================
# FIN 8.3
# ===============================================================# ===============================================================

# ===============================================================
# 8.4 — CLASIFICACIÓN DE IDs
# ===============================================================

def clasificar_ids(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Clasifica IDs por módulo a partir del inventario estructural.
    Si el inventario no está actualizado, ejecuta mapear_codigo primero.

    _inventario_estructural["ids"] conserva:
        id → [ {modulo, archivo}, ... ]   (apariciones; no se modifica)

    Esta capacidad deriva:
        id_a_modulos   — id → [módulos únicos ordenados]
        ids_por_modulo — módulo → [ids]
        ids_unicos     — ids presentes en exactamente un módulo
        ids_duplicados — id → [módulos] cuando el ID aparece en >1 módulo

    Duplicado = el mismo ID declarado en más de un módulo.
    Es clasificación estructural, no error automático.
    """
    if not _inventario_estructural.get("modulos"):
        mapear_codigo(peticion)

    inv = _inventario_estructural

    # -----------------------------------------------------------
    # 1. id → apariciones {modulo, archivo}
    #    Derivar id → módulos únicos (sin repetir el mismo módulo)
    # -----------------------------------------------------------
    id_a_modulos: Dict[str, List[str]] = {}
    for idv, apariciones in (inv.get("ids") or {}).items():
        mods: List[str] = []
        vistos: Set[str] = set()
        for ap in apariciones:
            if not isinstance(ap, dict):
                continue
            m = ap.get("modulo")
            if m is None:
                continue
            m = str(m)
            if m not in vistos:
                vistos.add(m)
                mods.append(m)
        id_a_modulos[idv] = sorted(mods)

    # -----------------------------------------------------------
    # 2. módulo → lista de IDs
    # -----------------------------------------------------------
    ids_por_modulo: Dict[str, List[str]] = {}
    for nombre_mod, info in (inv.get("modulos") or {}).items():
        ids_por_modulo[nombre_mod] = list(info.get("ids") or [])

    # -----------------------------------------------------------
    # 3. Únicos vs duplicados (por cantidad de módulos, no de apariciones)
    # -----------------------------------------------------------
    ids_unicos: List[str] = sorted(
        i for i, mods in id_a_modulos.items() if len(mods) == 1
    )
    ids_duplicados: Dict[str, List[str]] = {
        i: mods for i, mods in id_a_modulos.items() if len(mods) > 1
    }

    return {
        "id": ID_MODULO,
        "operacion": "clasificar_ids",
        "ids_por_modulo": ids_por_modulo,
        "id_a_modulos": id_a_modulos,
        "ids_unicos": ids_unicos,
        "ids_duplicados": ids_duplicados,
        "total_ids": len(id_a_modulos),
        "total_unicos": len(ids_unicos),
        "total_duplicados": len(ids_duplicados),
        "nota": (
            "Duplicado = el mismo ID aparece en más de un módulo. "
            "Es clasificación estructural, no violación contractual automática."
        ),
    }

# ===============================================================
# FIN 8.4
# ===============================================================
# ===============================================================
# 8.5 — INTEGRIDAD DEL REGISTRO (barrer / verificar)
# ===============================================================

def barrer() -> Dict[str, Any]:
    """
    Integridad formal del registro de eventos.
    No interpreta contenido. No mapea código.
    """
    errores = _registro.verificar_integridad()
    res = _registro.resumen()
    return {
        "contenedor": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "coherente": not errores,
        "inmutable": True,
        "errores": errores,
        "resumen": res,
        "version": VERSION_MODULO,
    }


def verificar() -> Dict[str, Any]:
    """Alias contractual de barrer."""
    return barrer()


def verificar_salida(salida: Dict[str, Any]) -> bool:
    if not isinstance(salida, dict):
        return False
    if "coherente" in salida:
        if not isinstance(salida["coherente"], bool):
            return False
        if "errores" in salida and not isinstance(salida["errores"], list):
            return False
        return True
    if "seq" in salida:
        return isinstance(salida.get("seq"), int)
    if "memoria" in salida:
        return isinstance(salida["memoria"], dict)
    return False

# ===============================================================
# FIN 8.5
# ===============================================================

# ===============================================================
# 8.6 — INVENTARIO
# ===============================================================

def inventario(peticion: Any = None) -> Dict[str, Any]:
    """
    Inventario del módulo CH + resumen del registro +
    estructura mapeada e IDs clasificados si existen.
    """
    clasif = clasificar_ids(peticion)
    return {
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "funcion": (
            "Registrador universal de eventos. Libro de actas. "
            "Mapeo estructural. Clasificación de IDs. Append-only."
        ),
        "memoria": _registro.resumen(),
        "categorias": _registro.categorias_conocidas(),
        "campos_registro": list(CAMPOS_REGISTRO),
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "invariantes": CONTENEDOR.get("invariantes"),
        "estructura": {
            "total_modulos": len(_inventario_estructural.get("modulos") or {}),
            "total_ids": clasif.get("total_ids"),
            "total_unicos": clasif.get("total_unicos"),
            "total_duplicados": clasif.get("total_duplicados"),
            "ids_duplicados": clasif.get("ids_duplicados"),
            "actualizado": _inventario_estructural.get("actualizado"),
        },
        "nota": (
            "CACHE no sabe lo que ocurrió. Solo sabe qué fue registrado "
            "y qué estructura encontró. Análisis semántico: módulo futuro."
        ),
    }

# ===============================================================
# FIN 8.6
# ===============================================================
# ===============================================================
# 8.7 — CAPACIDADES ARQUITECTÓNICAS
# ===============================================================

def ejecutar_total(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Ejerce las unidades operativas declaradas del módulo CH.
    No inventa capacidades. No ejecuta funciones arbitrarias del escaneo.
    """
    res_barrer = barrer()
    res_mapa = mapear_codigo(peticion)
    res_clasif = clasificar_ids(peticion)
    res_inv = inventario(peticion)
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "operacion": "ejecutar_total",
        "estado": (
            ESTADO_OPERATIVO
            if res_barrer.get("coherente")
            else ESTADO_DEGRADADO
        ),
        "barrer": res_barrer,
        "mapear_codigo": {
            "total_modulos": res_mapa.get("total_modulos"),
            "total_ids": res_mapa.get("total_ids"),
            "total_funciones": res_mapa.get("total_funciones"),
            "total_clases": res_mapa.get("total_clases"),
        },
        "clasificar_ids": {
            "total_ids": res_clasif.get("total_ids"),
            "total_unicos": res_clasif.get("total_unicos"),
            "total_duplicados": res_clasif.get("total_duplicados"),
            "ids_duplicados": res_clasif.get("ids_duplicados"),
        },
        "inventario": {
            "capacidades": res_inv.get("capacidades"),
            "memoria": res_inv.get("memoria"),
        },
        "capacidades_declaradas": list(CONTENEDOR.get("capacidades", {}).keys()),
        "nota": (
            "ejecutar_total ejerce solo unidades contractuales de CACHE. "
            "No interpreta. No altera evidencia."
        ),
    }


def inspeccionar(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Inspección estructural de CACHE.
    Expone: capacidades contractuales, callables reales,
    estructura descubierta, IDs y duplicados.
    """
    res = _registro.resumen()
    clasif = clasificar_ids(peticion)
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
            "CAMPOS_REGISTRO": list(CAMPOS_REGISTRO),
        },
        "capacidades_contractuales": list(
            CONTENEDOR.get("capacidades", {}).keys()
        ),
        "capacidades_meta": list(
            CONTENEDOR.get("capacidades_meta", {}).keys()
        ),
        "registro": res,
        "estructura_descubierta": {
            "total_modulos": len(_inventario_estructural.get("modulos") or {}),
            "total_ids": clasif.get("total_ids"),
            "ids_unicos": clasif.get("ids_unicos"),
            "ids_duplicados": clasif.get("ids_duplicados"),
            "actualizado": _inventario_estructural.get("actualizado"),
        },
        "autoriza_engine": CONTENEDOR.get("autoriza_engine"),
        "reporting": CONTENEDOR.get("reporting"),
        "invariantes": list(INVARIANTES),
        "nota": (
            "inspeccionar expone contrato, callables y estructura "
            "sin alterar evidencia ni ejecutar código descubierto."
        ),
    }


def registrar_inventario(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Registra el inventario estructural de CACHE como evento append-only.
    No modifica evidencia previa.
    """
    inv = inventario(peticion)
    entrada = _registro.append({
        "origen": ID_MODULO,
        "destino": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "capacidad": "registrar_inventario",
        "tipo": "inventario",
        "categoria": "estructura",
        "estado": ESTADO_OPERATIVO,
        "payload": inv,
        "run_id": (peticion or {}).get("run_id") if isinstance(peticion, dict) else None,
        "ciclo_id": (peticion or {}).get("ciclo_id") if isinstance(peticion, dict) else None,
    })
    return {
        "id": ID_MODULO,
        "operacion": "registrar_inventario",
        "registrado": True,
        "evento": entrada,
        "inventario": inv,
    }

# ===============================================================
# FIN 8.7
# ===============================================================

# ===============================================================
# 8.8 — BACKEND CENTINELA
# ===============================================================

class CacheBackend:
    """
    Adaptador estable para Centinela.
    Solo deposita veredictos (evento nuevo) y consulta registros.
    Nunca modifica evidencia previa. Nunca interpreta.
    """

    def guardar(self, registro: Dict[str, Any]) -> None:
        if not isinstance(registro, dict):
            raise CacheError("registro debe ser dict")
        tipo = str(registro.get("tipo") or "veredicto_centinela")
        depositar(
            tipo,
            registro,
            ciclo_id=(
                str(registro.get("ciclo_id"))
                if registro.get("ciclo_id") is not None
                else None
            ),
            run_id=(
                str(registro.get("run_id"))
                if registro.get("run_id") is not None
                else None
            ),
            origen=str(registro.get("origen") or "centinela"),
            modulo=str(registro.get("modulo") or "centinela"),
            capacidad=registro.get("capacidad"),
            categoria=registro.get("categoria"),
            estado=registro.get("estado"),
        )

    def obtener(self, ciclo_id: str) -> Optional[Dict[str, Any]]:
        regs = leer_por_ciclo(str(ciclo_id))
        if not regs:
            return None
        return regs[-1]


def backend_para_centinela() -> CacheBackend:
    return CacheBackend()

# ===============================================================
# FIN 8.8
# ===============================================================

# ===============================================================
# FIN PARTE 8
# ===============================================================


# ===============================================================
# PARTE 9 — REPORTING INTERNO
# ===============================================================

# ===============================================================
# 9.1 — REPORTE
# ===============================================================

def reporte() -> Dict[str, Any]:
    r = barrer()
    caps = list(CONTENEDOR["capacidades"].keys())
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "estado": (
            ESTADO_OPERATIVO if r.get("coherente") else ESTADO_DEGRADADO
        ),
        "coherente": r.get("coherente"),
        "inmutable": True,
        "errores": r.get("errores"),
        "memoria": r.get("resumen"),
        "categorias": _registro.categorias_conocidas(),
        "capacidades": caps,
        "capacidades_meta": list(
            CONTENEDOR.get("capacidades_meta", {}).keys()
        ),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "autoridad": CONTENEDOR.get("autoridad"),
        "conocimiento_exportable": CONTENEDOR.get(
            "conocimiento_exportable"
        ),
        "consultas_soportadas": CONTENEDOR.get("consultas_soportadas"),
        "operaciones_arquitectonicas": {
            "ejecutar_total": "ejecutar_total" in CONTENEDOR.get("capacidades", {}),
            "inspeccionar": "inspeccionar" in CONTENEDOR.get("capacidades", {}),
            "registrar_inventario": "registrar_inventario" in CONTENEDOR.get("capacidades", {}),
            "mapear_codigo": "mapear_codigo" in CONTENEDOR.get("capacidades", {}),
            "clasificar_ids": "clasificar_ids" in CONTENEDOR.get("capacidades", {}),
        },
    }

# ===============================================================
# FIN 9.1
# ===============================================================


# ===============================================================
# 9.2 — DIAGNÓSTICO
# ===============================================================

def diagnostico() -> Dict[str, Any]:
    r = barrer()
    res = r.get("resumen") or {}
    problemas: List[Dict[str, Any]] = []
    advertencias: List[str] = []
    recomendaciones: List[str] = []

    if r.get("errores"):
        problemas.append({
            "tipo": "integridad_registro",
            "detalle": r["errores"],
        })
        recomendaciones.append(
            "Revisar integridad formal del registro de eventos"
        )

    if res.get("total_eventos", 0) == 0:
        advertencias.append(
            "Registro vacío (legítimo al inicio del ciclo)"
        )

    estado = ESTADO_OPERATIVO if r.get("coherente") else ESTADO_DEGRADADO

    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "estado": estado,
        "problemas": problemas,
        "advertencias": advertencias,
        "recomendaciones": recomendaciones,
        "coherente": r.get("coherente"),
        "inmutable": True,
        "total_eventos": res.get("total_eventos", 0),
        "ciclos": res.get("ciclos", 0),
        "seq_actual": res.get("seq_actual", 0),
        "categorias_n": len(res.get("categorias") or []),
    }

# ===============================================================
# FIN 9.2
# ===============================================================

# ===============================================================
# FIN PARTE 9
# ===============================================================


# ===============================================================
# PARTE 10 — RESOLUCIÓN ESTRICTA Y EXPORTACIONES
# ===============================================================

# ===============================================================
# 10.1 — MAPA DE CAPACIDADES
# ===============================================================

_CAP_MAP = {
    "barrer": barrer,
    "verificar": verificar,
    "depositar": depositar,
    "leer": leer,
    "leer_eventos": leer_eventos,
    "leer_por_ciclo": leer_por_ciclo,
    "leer_por_modulo": leer_por_modulo,
    "leer_por_tipo": leer_por_tipo,
    "leer_por_categoria": leer_por_categoria,
    "leer_por_capacidad": leer_por_capacidad,
    "leer_por_origen": leer_por_origen,
    "leer_por_destino": leer_por_destino,
    "leer_por_estado": leer_por_estado,
    "leer_por_seq": leer_por_seq,
    "leer_por_timestamp": leer_por_timestamp,
    "categorias": categorias,
    "inventario": inventario,
    "reporte": reporte,
    "diagnostico": diagnostico,
    "verificar_salida": verificar_salida,
    "backend_para_centinela": backend_para_centinela,
    "ejecutar_total": ejecutar_total,
    "inspeccionar": inspeccionar,
    "registrar_inventario": registrar_inventario,
    "mapear_codigo": mapear_codigo,
    "clasificar_ids": clasificar_ids,
}

# ===============================================================
# FIN 10.1
# ===============================================================


# ===============================================================
# 10.2 — RESOLUCIÓN DE CAPACIDADES
# ===============================================================

def _resolver_capacidades(cont: Dict[str, Any]) -> None:
    """
    Transforma referencias declarativas (str) en callables reales.
    Engine exige callables en CONTENEDOR["capacidades"].
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
                    "{0}: '{1}' no es callable".format(NOMBRE_MODULO, ref)
                )
            resueltas[nombre] = fn
            continue
        raise ContratoInvalido(
            "{0}: capacidad '{1}' tiene tipo inválido: {2}".format(
                NOMBRE_MODULO, nombre, type(ref).__name__
            )
        )
    cont["capacidades"] = resueltas

# ===============================================================
# FIN 10.2
# ===============================================================


# ===============================================================
# 10.3 — EJECUCIÓN DE VALIDACIÓN Y RESOLUCIÓN
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
    "CAMPOS_REGISTRO",
    "CacheError",
    "CacheInmutableError",
    "ContratoInvalido",
    "depositar",
    "leer",
    "leer_eventos",
    "leer_por_ciclo",
    "leer_por_modulo",
    "leer_por_tipo",
    "leer_por_categoria",
    "leer_por_capacidad",
    "leer_por_origen",
    "leer_por_destino",
    "leer_por_estado",
    "leer_por_seq",
    "leer_por_timestamp",
    "categorias",
    "inventario",
    "verificar",
    "barrer",
    "verificar_salida",
    "reporte",
    "diagnostico",
    "CacheBackend",
    "backend_para_centinela",
    "ejecutar_total",
    "inspeccionar",
    "registrar_inventario",
    "mapear_codigo",
    "clasificar_ids",
]

# ===============================================================
# FIN 10.4
# ===============================================================

# ===============================================================
# FIN PARTE 10
# ===============================================================


# ===============================================================
# FIN DEL MÓDULO
# ===============================================================
