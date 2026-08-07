# ===============================================================
# VPSI-TRUTH — modules/cache/__init__.py
# ===============================================================
#
# MÓDULO:              cache
# ID:                  CH
# Rol:                 CH
# Versión módulo:      4.0
# Versión contrato:    1.0
# Esquema contrato:    VPSI-CONTRACT-1.0
# Estabilidad:         ESTABLE
# Compatible desde:    1.0
# API Engine:          >=1.0
#
# Función:
#   Registrador universal de eventos.
#   Libro de actas del sistema.
#
#   CACHE no sabe lo que ocurrió.
#   Solo sabe qué fue registrado.
#
# Principio:
#   Engine produce.
#   Centinela verifica.
#   CACHE conserva.
#   (Futuro) Analizadores interpretan.
#   Omega presenta.
#
# Qué hace:
#   - Registrar exactamente lo que ocurrió durante la ejecución
#   - Conservar evidencia objetiva (append-only)
#   - Exponer lecturas filtradas por campos del registro
#   - Descubrir categorías dinámicamente al depositar
#
# Qué NO hace:
#   - No interpreta
#   - No deduce
#   - No reconstruye
#   - No infiere
#   - No calcula
#   - No descubre relaciones
#   - No genera grafos ni árboles
#   - No explica razonamientos
#   - No responde "por qué", "qué significa", "cuál fue la causa"
#
# Registro neutro (cada evento):
#   seq, timestamp, run_id, ciclo_id, origen, destino,
#   modulo, capacidad, tipo, categoria, estado, payload
#
# Categorías:
#   Dinámicas. Si Engine deposita categoria="predicciones",
#   CACHE la registra. No hay lista fija de dominios.
#
# Lecturas:
#   Solo filtros sobre lo registrado.
#   Nunca reconstrucciones ni proyecciones interpretativas.
#
# Relación con Engine:
#   Engine deposita. Engine lee. CACHE no inicia operaciones.
#
# Relación con Centinela:
#   Centinela consulta y deposita veredicto como evento nuevo.
#   Nunca modifica evidencia previa.
#
# Relación con Omega:
#   Omega solo presenta lo que Engine entrega.
#
# Futuro:
#   Un módulo analizador de trazabilidad leerá CACHE
#   para grafos, rutas, causalidad y explicaciones.
#   Ese análisis no pertenece a este módulo.
#
# ===============================================================


# ===============================================================
# IMPORTACIONES
# ===============================================================

from __future__ import annotations

import copy
import threading
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

# ===============================================================
# FIN IMPORTACIONES
# ===============================================================


# ===============================================================
# CONSTANTES
# ===============================================================

ID_MODULO = "CH"
NOMBRE_MODULO = "cache"
ROL_MODULO = "CH"

VERSION_MODULO = "4.0"
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

# Campos del registro neutro
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

INVARIANTES = (
    "el id del módulo nunca cambia",
    "el rol nunca cambia",
    "las capacidades declaradas son siempre callables tras la resolución",
    "este módulo no modifica el estado de otros módulos",
    "este módulo no calcula",
    "este módulo no interpreta",
    "este módulo no deduce ni infiere",
    "este módulo no reconstruye ni genera grafos",
    "la evidencia depositada nunca se modifica",
    "la evidencia depositada nunca se sobrescribe",
    "la evidencia depositada nunca se reordena",
    "la evidencia depositada nunca desaparece durante el ciclo",
    "toda información nueva se incorpora solo como evento nuevo",
    "las categorías son dinámicas; no hay lista fija de dominios",
    "este módulo no inventa capacidades no declaradas en CONTENEDOR",
)

# ===============================================================
# FIN CONSTANTES
# ===============================================================


# ===============================================================
# CONFIGURACIÓN
# ===============================================================

# Carpetas físicas futuras: solo datos, sin lógica.
# cache/ciclos/run_x/ciclo_001/registros/ ...

# ===============================================================
# FIN CONFIGURACIÓN
# ===============================================================


# ===============================================================
# DEFINICIONES
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


class _RegistroEventos:
    """
    Almacén append-only de registros neutros.
    No interpreta. No indexa relaciones. Solo guarda y filtra.
    """

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._eventos: List[Dict[str, Any]] = []
        self._seq = 0
        self._categorias: set = set()

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

    def categorias_conocidas(self) -> List[str]:
        with self._lock:
            return sorted(self._categorias)

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

    def intentar_modificar(self, *args: Any, **kwargs: Any) -> None:
        raise CacheInmutableError(
            "CACHE no modifica evidencia depositada; solo registra"
        )

    def intentar_borrar_evento(self, *args: Any, **kwargs: Any) -> None:
        raise CacheInmutableError(
            "CACHE no borra evidencia en operación normal (append-only)"
        )


_registro = _RegistroEventos()

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
        "Registrador universal de eventos. Libro de actas del sistema. "
        "Conserva evidencia objetiva. Categorías dinámicas. "
        "No interpreta. No deduce. No reconstruye. No calcula."
    ),

    # ----- PROPÓSITO -----
    "funcion": (
        "Registrar exactamente lo que ocurrió durante la ejecución "
        "y exponer lecturas filtradas por campos del registro. "
        "Nada más."
    ),
    "no_hace": [
        "No interpreta",
        "No deduce ni infiere",
        "No reconstruye ciclos",
        "No genera grafos ni árboles",
        "No explica razonamientos ni causas",
        "No calcula C / L / K / Tru",
        "No descubre relaciones",
        "No altera evidencia depositada",
        "No inicia operaciones",
        "No envía reportes a otros módulos",
    ],

    # ----- AUTORIDAD -----
    "autoridad": [
        "Registrar eventos depositados por Engine o Centinela",
        "Entregar lecturas filtradas por campos del registro",
        "Exponer categorías descubiertas dinámicamente",
        "Verificar integridad del registro (forma, no contenido)",
        "Reportar estado, inventario y diagnóstico propios",
    ],

    # ----- CONOCIMIENTO EXPORTABLE -----
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
        "depositar_evento",
        "leer_eventos",
        "filtrar_por_campo",
        "listar_categorias",
        "obtener_inventario",
        "obtener_reporte",
        "obtener_diagnostico",
        "verificar_integridad_registro",
    ],

    # ----- CAPACIDADES -----
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
    },

    # ----- METADATOS DE CAPACIDADES (1:1 obligatorio) -----
    "capacidades_meta": {
        "verificar": {
            "descripcion": "Alias de barrer. Integridad formal del registro.",
            "entrada": "ninguna",
            "salida": "dict con coherente, inmutable, errores, resumen",
        },
        "barrer": {
            "descripcion": (
                "Verifica forma del registro: seq creciente, timestamps, "
                "payload dict. No interpreta contenido."
            ),
            "entrada": "ninguna",
            "salida": "dict con coherente, inmutable, errores, resumen",
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
            "salida": "dict del evento registrado",
        },
        "leer": {
            "descripcion": "Lectura genérica con filtros opcionales por campo.",
            "entrada": "filtros opcionales por campo del registro",
            "salida": "list[dict]",
        },
        "leer_eventos": {
            "descripcion": "Alias de leer sin filtros (todos los eventos).",
            "entrada": "ninguna",
            "salida": "list[dict]",
        },
        "leer_por_ciclo": {
            "descripcion": "Eventos de un ciclo_id.",
            "entrada": "ciclo_id: str",
            "salida": "list[dict]",
        },
        "leer_por_modulo": {
            "descripcion": "Eventos de un módulo.",
            "entrada": "modulo: str, ciclo_id?",
            "salida": "list[dict]",
        },
        "leer_por_tipo": {
            "descripcion": "Eventos de un tipo.",
            "entrada": "tipo: str, ciclo_id?",
            "salida": "list[dict]",
        },
        "leer_por_categoria": {
            "descripcion": "Eventos de una categoría (dinámica).",
            "entrada": "categoria: str, ciclo_id?",
            "salida": "list[dict]",
        },
        "leer_por_capacidad": {
            "descripcion": "Eventos de una capacidad.",
            "entrada": "capacidad: str, ciclo_id?",
            "salida": "list[dict]",
        },
        "leer_por_origen": {
            "descripcion": "Eventos con un origen dado.",
            "entrada": "origen: str, ciclo_id?",
            "salida": "list[dict]",
        },
        "leer_por_destino": {
            "descripcion": "Eventos con un destino dado.",
            "entrada": "destino: str, ciclo_id?",
            "salida": "list[dict]",
        },
        "leer_por_estado": {
            "descripcion": "Eventos con un estado dado.",
            "entrada": "estado: str, ciclo_id?",
            "salida": "list[dict]",
        },
        "leer_por_seq": {
            "descripcion": "Eventos en un rango de seq.",
            "entrada": "desde_seq?, hasta_seq?",
            "salida": "list[dict]",
        },
        "leer_por_timestamp": {
            "descripcion": "Eventos en un rango de timestamp.",
            "entrada": "desde_timestamp?, hasta_timestamp?",
            "salida": "list[dict]",
        },
        "categorias": {
            "descripcion": "Categorías descubiertas dinámicamente hasta ahora.",
            "entrada": "ninguna",
            "salida": "list[str]",
        },
        "inventario": {
            "descripcion": "Inventario del módulo y resumen del registro.",
            "entrada": "ninguna",
            "salida": "dict con id, version, memoria, categorias, capacidades",
        },
        "reporte": {
            "descripcion": "Reporte interno de estado del módulo CH.",
            "entrada": "ninguna",
            "salida": "dict con estado, coherente, memoria, capacidades",
        },
        "diagnostico": {
            "descripcion": "Diagnóstico de integridad formal del registro.",
            "entrada": "ninguna",
            "salida": "dict con estado, problemas, advertencias, recomendaciones",
        },
        "verificar_salida": {
            "descripcion": "Comprueba forma de una salida de barrer o depósito.",
            "entrada": "salida: dict",
            "salida": "bool",
        },
        "backend_para_centinela": {
            "descripcion": (
                "Adaptador estable CacheBackend para Centinela. "
                "Centinela no conoce la implementación interna."
            ),
            "entrada": "ninguna",
            "salida": "CacheBackend",
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
    if str(cont.get("version_contrato")) != VERSION_CONTRATO:
        raise ContratoInvalido(
            "{0}: version_contrato inválida: {1}".format(
                NOMBRE_MODULO, cont.get("version_contrato")
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

# ===============================================================
# FIN FUNCIONES PRIVADAS
# ===============================================================


# ===============================================================
# CAPACIDADES PÚBLICAS
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


def inventario(peticion: Any = None) -> Dict[str, Any]:
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
            "Append-only. No interpreta."
        ),
        "memoria": _registro.resumen(),
        "categorias": _registro.categorias_conocidas(),
        "campos_registro": list(CAMPOS_REGISTRO),
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "invariantes": CONTENEDOR.get("invariantes"),
        "nota": (
            "CACHE no sabe lo que ocurrió. Solo sabe qué fue registrado. "
            "Análisis de trazabilidad: módulo futuro, no este."
        ),
    }


def barrer() -> Dict[str, Any]:
    """Integridad formal del registro. No interpreta contenido."""
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


class CacheBackend:
    """
    Adaptador estable para Centinela.
    Solo deposita veredictos (evento nuevo) y consulta registros.
    Nunca modifica evidencia previa. Nunca interpreta.
    """

    def guardar(self, registro: Dict[str, Any]) -> None:
        tipo = str(registro.get("tipo") or "veredicto_centinela")
        depositar(
            tipo,
            registro if isinstance(registro, dict) else {},
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
        # último registro del ciclo; sin interpretación de contenido
        return regs[-1]


def backend_para_centinela() -> CacheBackend:
    return CacheBackend()

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
        "estado": (
            ESTADO_OPERATIVO if r.get("coherente") else ESTADO_DEGRADADO
        ),
        "coherente": r.get("coherente"),
        "inmutable": True,
        "errores": r.get("errores"),
        "memoria": r.get("resumen"),
        "categorias": _registro.categorias_conocidas(),
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "autoridad": CONTENEDOR.get("autoridad"),
        "conocimiento_exportable": CONTENEDOR.get(
            "conocimiento_exportable"
        ),
        "consultas_soportadas": CONTENEDOR.get("consultas_soportadas"),
    }


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
# FIN REPORTING
# ===============================================================


# ===============================================================
# EXPORTACIONES + RESOLUCIÓN ESTRICTA
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
            "{0}: capacidad '{1}' tiene tipo inválido: {2}".format(
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
    "CAMPOS_REGISTRO",
    "CacheError",
    "CacheInmutableError",
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
    "ContratoInvalido",
]

# ===============================================================
# FIN EXPORTACIONES
# ===============================================================


# ===============================================================
# EXTENSIONES FUTURAS
# ===============================================================
#
# Carpetas físicas: solo datos, sin lógica.
# Analizador de trazabilidad: módulo futuro, no este.
#
# Toda capacidad nueva DEBE agregarse simultáneamente en:
#   1. capacidades
#   2. capacidades_meta
#   3. _CAP_MAP
#   4. VERSION_MODULO
#
# ===============================================================
# FIN EXTENSIONES FUTURAS
# ===============================================================


# ===============================================================
# FIN DEL MÓDULO
# ===============================================================
