# ===============================================================
# VPSI-TRUTH — modules/contexto/__init__.py
# ===============================================================
#
# MÓDULO:              contexto
# ID:                  CX
# Rol:                 CX
# Versión módulo:      2.3
# Versión contrato:    1.0
# Esquema contrato:    VPSI-CONTRACT-1.0
# Estabilidad:         ESTABLE
# Compatible desde:    1.0
# API Engine:          >=1.0
#
# Función:
#   Representar operativamente el marco evaluable O_context.
#
# Qué hace:
#   - Genera el registro O a partir de la petición.
#   - Clasifica estado, evento, ligaduras y modo_entrada.
#   - Determina permite_k y pedir_anuncio.
#   - Garantiza la coherencia estructural del dominio.
#   - Descubre, carga y valida automáticamente cada archivo *.py del módulo.
#   - Expone inventario, reporte, diagnóstico y axiomas del dominio.
#
# Responsabilidad:
#   Garantizar una representación coherente del marco O y mantener
#   la integridad estructural de su dominio.
#
# Autoridad:
#   - Declarar el registro O y permite_k.
#   - Clasificar el contexto evaluable.
#   - Validar la estructura y el dominio de los archivos internos.
#   - Reportar el estado estructural del módulo.
#
# Conocimiento exportable:
#   - O_context
#   - registro
#   - permite_k
#   - pedir_anuncio
#   - tipos_peticion
#   - inventario
#   - reporte
#   - diagnostico
#   - axiomas
#
# Relación con Engine:
#   Engine descubre este CONTENEDOR, ejecuta únicamente las
#   capacidades declaradas, puede inspeccionar todos los archivos
#   del módulo y consolida el reporte producido por este.
#
# Relación con Omega:
#   Omega no calcula información de este módulo.
#   Solo presenta los resultados entregados por Engine.
#
# Observaciones:
#   Todo archivo *.py del directorio forma parte del dominio del
#   módulo y puede ser descubierto, validado y auditado
#   automáticamente mediante el centinela.
#
# ===============================================================


# ===============================================================
# IMPORTACIONES
# ===============================================================

from __future__ import annotations

import os
import sys
import json
import math
import copy
import time
import types
import logging
import hashlib
import inspect
import itertools
import functools
import traceback
import importlib
import importlib.util
from pathlib import Path

from dataclasses import dataclass, field
from collections import defaultdict, deque
from typing import Any, Dict, List, Tuple, Set, Optional, Iterable, Callable

# ===============================================================
# FIN IMPORTACIONES
# ===============================================================


# ===============================================================
# CONSTANTES
# ===============================================================

ID_MODULO = "CX"
NOMBRE_MODULO = "contexto"
ROL_MODULO = "CX"

VERSION_MODULO = "2.3"
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
    "este módulo no inventa capacidades no declaradas en CONTENEDOR",
    "todo *.py interno se valida por estructura y dominio",
    "permite_k exige registro con estado=estable, O_id y enunciado_O",
    "pedir_anuncio verdadero implica tipos_peticion no vacío",
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
    """El CONTENEDOR no cumple el esquema o la resolución de capacidades falló."""


class ContextoError(Exception):
    """Error de forma o de regla contextual."""


class _Undefined:
    __slots__ = ()

    def __repr__(self) -> str:
        return "UNDEFINED"

    def __bool__(self) -> bool:
        raise TypeError("UNDEFINED no admite conversión a booleano")

    def __eq__(self, other: object) -> bool:
        return isinstance(other, _Undefined)

    def __hash__(self) -> int:
        return hash("VPSI_UNDEFINED")


UNDEFINED = _Undefined()


def es_undefined(v: Any) -> bool:
    return v is UNDEFINED or isinstance(v, _Undefined)

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
    "dominio": "CX",
    "prefijo_reglas": "CX",
    "descripcion": (
        "Representación operativa del marco evaluable O_context."
    ),

    # ----- PROPÓSITO -----
    "funcion": (
        "Generar el marco O a partir de la petición y garantizar "
        "la coherencia estructural de su dominio."
    ),
    "no_hace": [
        "No calcula valores de verdad",
        "No asigna magnitudes numéricas de correlación",
        "No importa código ajeno a su directorio",
        "No declara dependencias de dominio",
        "No orquesta ciclos",
        "No emite cadenas auditables",
    ],

    # ----- AUTORIDAD -----
    "autoridad": [
        "Declarar el registro O y permite_k",
        "Clasificar el contexto evaluable",
        "Validar la estructura y el dominio de los archivos internos",
        "Reportar el estado estructural del módulo",
    ],

    # ----- CONOCIMIENTO EXPORTABLE -----
    "conocimiento_exportable": [
        "O_context",
        "registro",
        "permite_k",
        "pedir_anuncio",
        "tipos_peticion",
        "inventario",
        "reporte",
        "diagnostico",
        "axiomas",
    ],

    # ----- DEPENDENCIAS (clave obligatoria del esquema) -----
    "requiere": ["DG"],

    # ----- DOMINIO -----
    "modos_entrada": [
        "conversacion",
        "afirmacion",
        "teorema",
        "auditoria",
        "texto_libre",
        "repositorio",
    ],
    "estados_O": ["estable", "cambio", "indefinido"],
    "eventos": ["mismo_O", "expansion", "cambio", "indefinido"],
    "tipos_peticion": [
        "por_que_valor",
        "dame_O",
        "dame_evidencia",
        "dame_normas",
        "dame_limites",
        "dame_cadena_completa",
    ],
    "claves_pedir_anuncio": [
        "pedir_anuncio",
        "pedir_cita",
        "anuncio",
        "citar",
        "cadena_auditable",
        "dame_por_que",
    ],
    "regla_campos_obligatorios": ["id", "nombre", "version", "descripcion"],
    "claves_fuera_de_dominio": [
        "Tru_Ri", "Tru_total", "tru_ri", "tru_total",
        "C", "L", "K",
        "alpha", "beta", "ALPHA", "BETA",
    ],

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
        "resolver",
        "centinela",
        "inventario",
        "reporte",
        "diagnostico",
        "verificar",
        "axiomas",
    ],

    # ----- CAPACIDADES -----
    "capacidades": {
        "resolver": "resolver",
        "evaluar": "resolver",
        "centinela": "centinela",
        "verificar": "barrer",
        "barrer": "barrer",
        "inventario": "inventario",
        "reporte": "reporte",
        "diagnostico": "diagnostico",
        "axiomas": "axiomas",
        "verificar_salida": "verificar_salida",
    },

    # ----- METADATOS DE CAPACIDADES (1:1) -----
    "capacidades_meta": {
        "resolver": {
            "descripcion": "Garantiza el marco O clasificado a partir de la petición.",
            "entrada": "peticion: dict | None",
            "salida": "dict con O_context, registro, permite_k, coherente, errores",
        },
        "evaluar": {
            "descripcion": "Alias de resolver.",
            "entrada": "peticion: dict | None",
            "salida": "dict con O_context, registro, permite_k, coherente",
        },
        "centinela": {
            "descripcion": "Garantiza la coherencia estructural del dominio.",
            "entrada": "ninguna",
            "salida": "dict con coherente, total, choques, detalle, errores",
        },
        "verificar": {
            "descripcion": "Alias de barrer.",
            "entrada": "ninguna",
            "salida": "dict con coherente, errores, reglas_internas",
        },
        "barrer": {
            "descripcion": "Garantiza la coherencia de los clasificadores internos.",
            "entrada": "ninguna",
            "salida": "dict con coherente, errores, reglas_internas",
        },
        "inventario": {
            "descripcion": "Garantiza la enumeración de lo que existe en el módulo.",
            "entrada": "ninguna",
            "salida": "dict con id, version, reglas_internas, modos, estados, capacidades",
        },
        "reporte": {
            "descripcion": "Garantiza el estado actual del módulo.",
            "entrada": "ninguna",
            "salida": "dict con estado, coherente, version, reglas_n",
        },
        "diagnostico": {
            "descripcion": "Garantiza problemas, advertencias y recomendaciones.",
            "entrada": "ninguna",
            "salida": "dict con estado, problemas, advertencias, recomendaciones",
        },
        "axiomas": {
            "descripcion": "Garantiza las declaraciones operativas del dominio.",
            "entrada": "ninguna",
            "salida": "list[dict]",
        },
        "verificar_salida": {
            "descripcion": "Garantiza la validez estructural de una salida del módulo.",
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

def _cfg(clave: str, default: Any = None) -> Any:
    return CONTENEDOR.get(clave, default)


def _registro_vacio() -> Dict[str, Any]:
    return {
        "O_id": None,
        "escala": None,
        "enunciado_O": None,
        "ligaduras": {},
        "estado": "indefinido",
        "modo_entrada": None,
        "evento": "indefinido",
        "pedir_anuncio": False,
        "tipos_peticion": [],
    }


def _truthy_pedir(v: Any) -> bool:
    if v is True:
        return True
    if v is False or v is None:
        return False
    if isinstance(v, (int, float)):
        return v != 0
    s = str(v).strip().lower()
    return s in ("1", "true", "si", "sí", "yes", "on", "citar", "anuncio")


def _normalizar_tipos_peticion(raw: Any) -> List[str]:
    admitidos = set(_cfg("tipos_peticion") or [])
    tipos: List[str] = []
    if isinstance(raw, str):
        for p in raw.replace(";", ",").split(","):
            p = p.strip()
            if p in admitidos and p not in tipos:
                tipos.append(p)
    elif isinstance(raw, (list, tuple, set)):
        for x in raw:
            s = str(x).strip()
            if s in admitidos and s not in tipos:
                tipos.append(s)
    return tipos


def _normalizar_registro(peticion: Dict[str, Any]) -> Dict[str, Any]:
    reg = _registro_vacio()
    estados = set(_cfg("estados_O") or [])
    eventos = set(_cfg("eventos") or [])
    claves_pedir = tuple(_cfg("claves_pedir_anuncio") or [])

    o_id = peticion.get("O_id") or peticion.get("o_id")
    enunciado = (
        peticion.get("enunciado_O")
        or peticion.get("enunciado")
        or peticion.get("contexto")
        or peticion.get("O_context")
    )
    escala = peticion.get("escala")
    modo = peticion.get("modo_entrada") or peticion.get("modo")
    ligaduras = peticion.get("ligaduras") or {}
    estado_decl = peticion.get("estado")

    if isinstance(ligaduras, dict):
        reg["ligaduras"] = {
            str(k).strip(): str(v).strip()
            for k, v in ligaduras.items()
            if str(k).strip() and str(v).strip()
        }
    else:
        reg["ligaduras"] = {}

    reg["O_id"] = str(o_id).strip() if o_id else None
    reg["enunciado_O"] = str(enunciado).strip() if enunciado else None
    reg["escala"] = str(escala).strip() if escala else None
    reg["modo_entrada"] = str(modo).strip() if modo else None

    if estado_decl in estados:
        reg["estado"] = estado_decl
    elif reg["O_id"] and reg["enunciado_O"]:
        reg["estado"] = "estable"
    else:
        reg["estado"] = "indefinido"

    evento = peticion.get("evento")
    if evento in eventos:
        reg["evento"] = evento
    elif reg["estado"] == "estable":
        reg["evento"] = "mismo_O"
    else:
        reg["evento"] = "indefinido"

    pedir = False
    for k in claves_pedir:
        if k in peticion and _truthy_pedir(peticion.get(k)):
            pedir = True
            break

    tipos = _normalizar_tipos_peticion(
        peticion.get("tipos_peticion") or peticion.get("tipo_peticion")
    )
    if tipos and not pedir:
        pedir = True
    if pedir and not tipos:
        tipos = ["dame_cadena_completa"]

    reg["pedir_anuncio"] = pedir
    reg["tipos_peticion"] = tipos
    return reg


def _conflicto_ligaduras(ligaduras: Dict[str, str]) -> List[str]:
    errs: List[str] = []
    for forma, d in ligaduras.items():
        if not forma or not d:
            errs.append(
                "ligadura inválida: forma={0!r} D={1!r}".format(forma, d)
            )
    return errs


def _permite_k(registro: Dict[str, Any]) -> bool:
    if registro.get("estado") != "estable":
        return False
    if not registro.get("O_id") or not registro.get("enunciado_O"):
        return False
    return True


def _id_anclado(rid: str, regla: Dict[str, Any]) -> bool:
    prefijo = str(_cfg("prefijo_reglas") or _cfg("dominio") or "")
    if not rid:
        return False
    if prefijo and (
        rid.startswith(prefijo + "-")
        or rid.startswith(prefijo + "_")
        or prefijo.upper() in rid.upper()
    ):
        return True
    if regla.get("anclas_cx") or regla.get("anclas"):
        return True
    return False


def _validar_regla_meta(stem: str, regla: Any) -> List[str]:
    errs: List[str] = []
    if not isinstance(regla, dict):
        return ["{0}: REGLA debe ser dict".format(stem)]

    for k in (_cfg("regla_campos_obligatorios") or []):
        if k not in regla or not str(regla.get(k, "")).strip():
            errs.append(
                "{0}: REGLA sin campo obligatorio '{1}'".format(stem, k)
            )

    rid = str(regla.get("id", "")).strip()
    if rid and not _id_anclado(rid, regla):
        errs.append(
            "{0}: id '{1}' sin anclaje al dominio {2}".format(
                stem, rid, _cfg("dominio")
            )
        )

    fuera = set(_cfg("claves_fuera_de_dominio") or [])
    for clave in fuera:
        if clave in regla and regla[clave] is not None:
            errs.append(
                "{0}: REGLA contiene clave fuera de dominio: '{1}'".format(
                    stem, clave
                )
            )
    return errs


def _validar_clasificacion(stem: str, cls: Any) -> List[str]:
    errs: List[str] = []
    if not isinstance(cls, dict):
        return ["{0}: clasificar() debe devolver dict".format(stem)]

    fuera = set(_cfg("claves_fuera_de_dominio") or [])
    for clave in fuera:
        if clave in cls and cls[clave] is not None:
            if clave == "K" and isinstance(cls.get("K"), bool):
                continue
            errs.append(
                "{0}: clasificar() emite clave fuera de dominio: '{1}'".format(
                    stem, clave
                )
            )

    estados = set(_cfg("estados_O") or [])
    eventos = set(_cfg("eventos") or [])
    tipos_ok = set(_cfg("tipos_peticion") or [])

    if "estado" in cls and cls["estado"] is not None:
        if cls["estado"] not in estados:
            errs.append(
                "{0}: estado {1!r} no admitido".format(stem, cls["estado"])
            )
    if "evento" in cls and cls["evento"] is not None:
        if cls["evento"] not in eventos:
            errs.append(
                "{0}: evento {1!r} no admitido".format(stem, cls["evento"])
            )

    tps = cls.get("tipos_peticion")
    if tps is not None:
        if not isinstance(tps, list):
            errs.append("{0}: tipos_peticion debe ser list".format(stem))
        else:
            for t in tps:
                if t not in tipos_ok:
                    errs.append(
                        "{0}: tipo_peticion no admitido: {1!r}".format(stem, t)
                    )
    return errs


def _centinela_archivo(
    stem: str,
    mod: Any,
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    entrada: Dict[str, Any] = {"archivo": "{0}.py".format(stem)}
    errores_c: List[str] = []

    meta = getattr(mod, "REGLA", None)
    validador = getattr(mod, "validar", None)
    clasificador = getattr(mod, "clasificar", None)

    if meta is None and not callable(validador) and not callable(clasificador):
        errores_c.append(
            "{0}: sin REGLA ni validar()/clasificar()".format(stem)
        )
        entrada["error"] = errores_c[-1]
        entrada["errores_centinela"] = errores_c
        return entrada

    if meta is not None:
        entrada["regla"] = meta if isinstance(meta, dict) else {"raw": str(meta)}
        errores_c.extend(_validar_regla_meta(stem, meta))

    if callable(clasificador) and peticion is not None:
        try:
            cls = clasificador(peticion)
            entrada["clasificacion"] = cls
            errores_c.extend(_validar_clasificacion(stem, cls))
        except Exception as e:
            errores_c.append(
                "{0}: clasificar: {1}: {2}".format(
                    stem, type(e).__name__, e
                )
            )
            entrada["error"] = errores_c[-1]
    elif callable(validador):
        try:
            entrada["resultado"] = validador()
        except Exception as e:
            errores_c.append(
                "{0}: validar: {1}: {2}".format(
                    stem, type(e).__name__, e
                )
            )
            entrada["error"] = errores_c[-1]

    if errores_c:
        entrada["errores_centinela"] = errores_c
        if "error" not in entrada:
            entrada["error"] = errores_c[0]
    return entrada


def _cargar_reglas(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    registro: Dict[str, Any] = {}
    for archivo in sorted(_DIR.glob("*.py")):
        if archivo.name == "__init__.py" or archivo.name.startswith("_"):
            continue
        nombre_mod = "{0}_regla_{1}".format(NOMBRE_MODULO, archivo.stem)
        spec = importlib.util.spec_from_file_location(nombre_mod, archivo)
        if spec is None or spec.loader is None:
            registro[archivo.stem] = {
                "error": "spec_from_file_location falló",
                "errores_centinela": ["carga imposible"],
            }
            continue
        mod = importlib.util.module_from_spec(spec)
        sys.modules[nombre_mod] = mod
        try:
            spec.loader.exec_module(mod)
        except Exception as e:
            registro[archivo.stem] = {
                "error": "{0}: {1}".format(type(e).__name__, e),
                "errores_centinela": ["import: {0}".format(e)],
            }
            continue
        registro[archivo.stem] = _centinela_archivo(
            archivo.stem, mod, peticion
        )
    return registro


def _detectar_choques_reglas(reglas: Dict[str, Any]) -> List[str]:
    choques: List[str] = []
    por_id: Dict[str, List[str]] = {}
    por_nombre: Dict[str, List[str]] = {}

    for clave, datos in reglas.items():
        if datos.get("errores_centinela") and "regla" not in datos:
            continue
        regla = datos.get("regla") or {}
        if not isinstance(regla, dict):
            continue
        rid = str(regla.get("id", "")).strip()
        nom = str(regla.get("nombre", "")).strip()
        if rid:
            por_id.setdefault(rid, []).append(clave)
        if nom:
            por_nombre.setdefault(nom, []).append(clave)

    for rid, archivos in por_id.items():
        if len(archivos) > 1:
            choques.append(
                "id de regla '{0}' repetido en {1}".format(rid, archivos)
            )
    for nom, archivos in por_nombre.items():
        if len(archivos) > 1:
            choques.append(
                "nombre de regla '{0}' repetido en {1}".format(nom, archivos)
            )
    return choques


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

def centinela() -> Dict[str, Any]:
    reglas = _cargar_reglas(None)
    choques = _detectar_choques_reglas(reglas)
    errores: List[str] = list(choques)

    for nombre, datos in reglas.items():
        if "error" in datos:
            errores.append("regla '{0}': {1}".format(nombre, datos["error"]))
        for ec in datos.get("errores_centinela") or []:
            if ec not in errores:
                errores.append("centinela '{0}': {1}".format(nombre, ec))

    return {
        "contenedor": NOMBRE_MODULO,
        "dominio": _cfg("dominio"),
        "coherente": not errores,
        "total": len(reglas),
        "choques": choques,
        "detalle": reglas,
        "errores": errores,
        "version": VERSION_MODULO,
    }


def resolver(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    peticion = dict(peticion or {})
    modos = set(_cfg("modos_entrada") or [])
    estados = set(_cfg("estados_O") or [])
    eventos = set(_cfg("eventos") or [])
    tipos_ok = set(_cfg("tipos_peticion") or [])

    if not peticion:
        audit = centinela()
        return {
            "O_context": None,
            "registro": None,
            "permite_k": False,
            "pedir_anuncio": False,
            "tipos_peticion": [],
            "coherente": audit.get("coherente", False),
            "escala": "macro",
            "modo_entrada": "repositorio",
            "reglas_internas": {
                "total": audit.get("total", 0),
                "choques": audit.get("choques") or [],
            },
            "errores": list(audit.get("errores") or []),
            "notas": ["sin petición: solo auditoría de clasificadores"],
        }

    reglas = _cargar_reglas(peticion)
    choques = _detectar_choques_reglas(reglas)
    errores: List[str] = list(choques)

    for nombre, datos in reglas.items():
        if "error" in datos:
            errores.append("regla '{0}': {1}".format(nombre, datos["error"]))
        for ec in datos.get("errores_centinela") or []:
            if ec not in errores:
                errores.append("centinela '{0}': {1}".format(nombre, ec))

    registro = _normalizar_registro(peticion)
    errores.extend(_conflicto_ligaduras(registro.get("ligaduras") or {}))

    if registro.get("modo_entrada") and registro["modo_entrada"] not in modos:
        errores.append(
            "modo_entrada no reconocido: {0!r}".format(
                registro["modo_entrada"]
            )
        )

    for nombre, datos in reglas.items():
        cls = datos.get("clasificacion")
        if not isinstance(cls, dict):
            continue
        if cls.get("estado") in estados:
            registro["estado"] = cls["estado"]
        if cls.get("evento") in eventos:
            registro["evento"] = cls["evento"]
        if cls.get("pedir_anuncio") is True:
            registro["pedir_anuncio"] = True
        tps = cls.get("tipos_peticion")
        if isinstance(tps, list) and tps:
            seen = set(registro.get("tipos_peticion") or [])
            for t in tps:
                if t in tipos_ok and t not in seen:
                    registro.setdefault("tipos_peticion", []).append(t)
                    seen.add(t)
            if registro.get("tipos_peticion") and not registro.get(
                "pedir_anuncio"
            ):
                registro["pedir_anuncio"] = True
        if cls.get("error"):
            errores.append(
                "clasificacion '{0}': {1}".format(nombre, cls["error"])
            )

    if registro.get("pedir_anuncio") and not registro.get("tipos_peticion"):
        registro["tipos_peticion"] = ["dame_cadena_completa"]

    permite = _permite_k(registro)
    o_ctx = registro.get("enunciado_O") or registro.get("O_id") or UNDEFINED

    notas: List[str] = []
    if not registro.get("O_id") or not registro.get("enunciado_O"):
        notas.append("registro incompleto: sin O_id o enunciado_O")
    if not permite:
        notas.append("permite_k=False")
    if registro.get("pedir_anuncio"):
        notas.append("pedir_anuncio=True")
    if not reglas:
        notas.append("sin clasificadores internos")

    return {
        "O_context": o_ctx if not es_undefined(o_ctx) else UNDEFINED,
        "registro": registro,
        "permite_k": permite,
        "pedir_anuncio": bool(registro.get("pedir_anuncio")),
        "tipos_peticion": list(registro.get("tipos_peticion") or []),
        "coherente": not errores,
        "escala": "micro",
        "modo_entrada": registro.get("modo_entrada"),
        "reglas_internas": {
            "total": len(reglas),
            "choques": choques,
        },
        "errores": errores,
        "notas": notas,
    }


def barrer() -> Dict[str, Any]:
    audit = centinela()
    return {
        "contenedor": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "dominio": _cfg("dominio"),
        "coherente": audit.get("coherente", False),
        "errores": audit.get("errores") or [],
        "reglas_internas": {
            "total": audit.get("total", 0),
            "choques": audit.get("choques") or [],
        },
        "version": VERSION_MODULO,
    }


def verificar() -> Dict[str, Any]:
    return barrer()


def verificar_salida(salida: Dict[str, Any]) -> bool:
    if not isinstance(salida, dict):
        return False
    if "coherente" not in salida or not isinstance(salida["coherente"], bool):
        return False
    if "errores" in salida and not isinstance(salida["errores"], list):
        return False
    if "notas" in salida and not isinstance(salida["notas"], list):
        return False

    estados = set(_cfg("estados_O") or [])
    eventos = set(_cfg("eventos") or [])
    tipos_ok = set(_cfg("tipos_peticion") or [])

    if "registro" in salida:
        reg = salida["registro"]
        if reg is not None:
            if not isinstance(reg, dict):
                return False
            if "estado" in reg and reg["estado"] not in estados:
                return False
            if "evento" in reg and reg["evento"] not in eventos:
                return False
            if "tipos_peticion" in reg:
                if not isinstance(reg["tipos_peticion"], list):
                    return False
                for t in reg["tipos_peticion"]:
                    if t not in tipos_ok:
                        return False
            if "pedir_anuncio" in reg and not isinstance(
                reg["pedir_anuncio"], bool
            ):
                return False

        if "permite_k" not in salida or not isinstance(
            salida["permite_k"], bool
        ):
            return False

        if salida.get("permite_k") is True:
            if not isinstance(reg, dict):
                return False
            if reg.get("estado") != "estable":
                return False
            if not reg.get("O_id") or not reg.get("enunciado_O"):
                return False

        if isinstance(reg, dict) and reg.get("pedir_anuncio") is True:
            if not (reg.get("tipos_peticion") or []):
                return False

        if "pedir_anuncio" in salida and not isinstance(
            salida["pedir_anuncio"], bool
        ):
            return False

        if "tipos_peticion" in salida:
            if not isinstance(salida["tipos_peticion"], list):
                return False
            for t in salida["tipos_peticion"]:
                if t not in tipos_ok:
                    return False
    return True


def inventario(peticion: Any = None) -> Dict[str, Any]:
    reglas = _cargar_reglas()
    return {
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "dominio": CONTENEDOR.get("dominio"),
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "reglas_internas": sorted(reglas.keys()),
        "total_reglas": len(reglas),
        "modos_entrada": list(_cfg("modos_entrada") or []),
        "estados_O": list(_cfg("estados_O") or []),
        "eventos": list(_cfg("eventos") or []),
        "tipos_peticion": list(_cfg("tipos_peticion") or []),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "autoridad": CONTENEDOR.get("autoridad"),
        "conocimiento_exportable": CONTENEDOR.get("conocimiento_exportable"),
        "consultas_soportadas": CONTENEDOR.get("consultas_soportadas"),
        "invariantes": CONTENEDOR.get("invariantes"),
    }


def axiomas() -> List[Dict[str, Any]]:
    return [
        {
            "id": "CX-OP-1",
            "tipo": "axioma",
            "sujeto": "contexto",
            "relacion": "genera",
            "objeto": "marco_O",
            "polaridad": True,
            "enunciado": (
                "Este módulo genera el marco evaluable O a partir "
                "de la petición."
            ),
            "depende_de": [],
            "gobierna": ["contexto"],
        },
        {
            "id": "CX-OP-2",
            "tipo": "axioma",
            "sujeto": "permite_k",
            "relacion": "exige",
            "objeto": "registro_O_estable",
            "polaridad": True,
            "enunciado": (
                "permite_k es verdadero solo con registro estable "
                "que tenga O_id y enunciado_O."
            ),
            "depende_de": [],
            "gobierna": ["contexto"],
        },
        {
            "id": "CX-OP-3",
            "tipo": "axioma",
            "sujeto": "reglas_internas",
            "relacion": "unicidad",
            "objeto": "id_y_nombre",
            "polaridad": True,
            "enunciado": (
                "Los clasificadores internos no comparten id ni nombre."
            ),
            "depende_de": [],
            "gobierna": ["contexto"],
        },
        {
            "id": "CX-OP-4",
            "tipo": "axioma",
            "sujeto": "pedir_anuncio",
            "relacion": "implica",
            "objeto": "tipos_peticion_no_vacio",
            "polaridad": True,
            "enunciado": (
                "pedir_anuncio verdadero implica tipos_peticion no vacío."
            ),
            "depende_de": [],
            "gobierna": ["contexto"],
        },
        {
            "id": "CX-OP-5",
            "tipo": "axioma",
            "sujeto": "centinela",
            "relacion": "garantiza",
            "objeto": "coherencia_estructural_del_dominio",
            "polaridad": True,
            "enunciado": (
                "Todo *.py interno se valida por estructura, dominio "
                "y unicidad según el CONTENEDOR."
            ),
            "depende_de": ["CX-OP-3"],
            "gobierna": ["contexto"],
        },
    ]

# ===============================================================
# FIN CAPACIDADES PÚBLICAS
# ===============================================================


# ===============================================================
# REPORTING INTERNO
# ===============================================================

def reporte() -> Dict[str, Any]:
    audit = centinela()
    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "dominio": CONTENEDOR.get("dominio"),
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "estado": (
            ESTADO_OPERATIVO if audit.get("coherente") else ESTADO_DEGRADADO
        ),
        "coherente": audit.get("coherente"),
        "reglas_n": audit.get("total", 0),
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "autoridad": CONTENEDOR.get("autoridad"),
        "conocimiento_exportable": CONTENEDOR.get("conocimiento_exportable"),
        "consultas_soportadas": CONTENEDOR.get("consultas_soportadas"),
    }


def diagnostico() -> Dict[str, Any]:
    audit = centinela()
    problemas: List[Dict[str, Any]] = []
    advertencias: List[str] = []
    recomendaciones: List[str] = []

    if audit.get("errores"):
        problemas.append({
            "tipo": "errores_clasificadores",
            "detalle": audit["errores"],
        })
        recomendaciones.append(
            "Corregir archivos internos con errores de forma o carga"
        )

    total = audit.get("total", 0)
    if not total:
        advertencias.append("Sin clasificadores internos")

    if audit.get("choques"):
        problemas.append({
            "tipo": "choques_id_nombre",
            "detalle": audit["choques"],
        })
        recomendaciones.append(
            "Unificar o renombrar reglas con id/nombre duplicado"
        )

    estado = ESTADO_OPERATIVO if audit.get("coherente") else ESTADO_DEGRADADO
    if not total and not problemas:
        estado = ESTADO_NO_INICIADO

    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "estado": estado,
        "problemas": problemas,
        "advertencias": advertencias,
        "recomendaciones": recomendaciones,
        "coherente": audit.get("coherente"),
        "errores_n": len(audit.get("errores") or []),
        "reglas_n": total,
    }

# ===============================================================
# FIN REPORTING
# ===============================================================


# ===============================================================
# EXPORTACIONES + RESOLUCIÓN ESTRICTA DEL CONTRATO
# ===============================================================

_CAP_MAP = {
    "resolver": resolver,
    "evaluar": resolver,
    "centinela": centinela,
    "barrer": barrer,
    "verificar": verificar,
    "inventario": inventario,
    "reporte": reporte,
    "diagnostico": diagnostico,
    "axiomas": axiomas,
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
    "UNDEFINED",
    "es_undefined",
    "ContextoError",
    "ContratoInvalido",
    "resolver",
    "centinela",
    "barrer",
    "verificar",
    "verificar_salida",
    "inventario",
    "axiomas",
    "reporte",
    "diagnostico",
]

# ===============================================================
# FIN EXPORTACIONES
# ===============================================================


# ===============================================================
# EXTENSIONES FUTURAS
# ===============================================================
#
# Capacidad nueva → capacidades + capacidades_meta + _CAP_MAP
# + VERSION_MODULO
#
# Clasificador nuevo → *.py en este directorio con REGLA
# y/o clasificar()/validar(). Descubrimiento automático.
#
# ===============================================================
# FIN EXTENSIONES FUTURAS
# ===============================================================


# ===============================================================
# FIN DEL MÓDULO
# ===============================================================
