# ===============================================================
# VPSI-TRUTH — modules/contexto/__init__.py
# ===============================================================
#
# MÓDULO:              contexto
# ID:                  CX
# Rol:                 CX
# Versión módulo:      2.0
# Versión contrato:    1.0
# Esquema contrato:    VPSI-CONTRACT-1.0
# Estabilidad:         ESTABLE
# Compatible desde:    1.0
# API Engine:          >=1.0
#
# Función:
#   Clasificar y amarrar el marco evaluable O_context.
#   Centinela interno: auto-carga y valida cada *.py del directorio.
#
# Qué hace:
#   - Clasifica registro O (estado, evento, ligaduras, modo_entrada)
#   - Determina permite_k y pedir_anuncio desde el propio registro
#   - Auto-carga clasificadores internos y valida forma y dominio
#   - Expone inventario, reporte y diagnóstico propios
#
# Qué NO hace:
#   - No calcula Tru_Ri / Tru_total / C / L / K
#   - No importa ni invoca código ajeno a este directorio
#   - No declara dependencias
#   - No orquesta el ciclo
#   - No emite cadena auditable
#
# Responsabilidad:
#   Entregar el marco O clasificado. Cero cálculo de verdad.
#
# Autoridad:
#   - Declarar el registro O y permite_k
#   - Validar clasificadores internos
#   - Reportar estado, inventario y diagnóstico propios
#
# Conocimiento exportable:
#   O_context, registro, permite_k, pedir_anuncio, tipos_peticion,
#   inventario, reporte, diagnostico, axiomas operativos
#
# Relación con Engine:
#   Engine descubre este CONTENEDOR, ejecuta solo las capacidades
#   declaradas y consolida el reporte que este módulo produce.
#
# Relación con Omega:
#   Omega solo presenta lo que Engine entrega de este módulo.
#
# ===============================================================


# ===============================================================
# IMPORTACIONES
# ===============================================================

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

ID_MODULO = "CX"
NOMBRE_MODULO = "contexto"
ROL_MODULO = "CX"

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

INVARIANTES = (
    "el id del módulo nunca cambia",
    "el rol nunca cambia",
    "las capacidades declaradas son siempre callables tras la resolución",
    "este módulo no modifica el estado de otros módulos",
    "este módulo no calcula Tru / C / L / K",
    "este módulo no importa código ajeno a su directorio",
    "este módulo no declara dependencias",
    "este módulo no orquesta el ciclo",
    "todo *.py interno se valida por centinela de módulo",
    "este módulo no inventa capacidades no declaradas en CONTENEDOR",
)

MODOS_ENTRADA = (
    "conversacion",
    "afirmacion",
    "teorema",
    "auditoria",
    "texto_libre",
    "repositorio",
)

ESTADOS_O = ("estable", "cambio", "indefinido")
EVENTOS = ("mismo_O", "expansion", "cambio", "indefinido")

TIPOS_PETICION = (
    "por_que_valor",
    "dame_O",
    "dame_evidencia",
    "dame_normas",
    "dame_limites",
    "dame_cadena_completa",
)

_CLAVES_PEDIR_ANUNCIO = (
    "pedir_anuncio",
    "pedir_cita",
    "anuncio",
    "citar",
    "cadena_auditable",
    "dame_por_que",
)

REGLA_CAMPOS_OBLIGATORIOS = ("id", "nombre", "version", "descripcion")

_PROHIBIDOS_EN_DESCRIPCION = (
    "calcula tru",
    "calcular tru",
    "tru_total",
    "tru_ri",
    "asigna k numérico",
    "asigna k numerico",
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


class ContextoError(Exception):
    """Error de coherencia o de regla contextual."""


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
    "descripcion": (
        "Clasificación operativa de O_context. "
        "Auto-carga y valida cada *.py interno. "
        "No calcula Tru. No declara dependencias."
    ),

    # ----- PROPÓSITO -----
    "funcion": (
        "Clasificar el marco evaluable O_context: registro, estado, "
        "evento, ligaduras, permite_k, pedir_anuncio. Validar "
        "clasificadores internos sin listarlos por nombre."
    ),
    "no_hace": [
        "No calcula Tru_Ri / Tru_total / C / L / K",
        "No importa código ajeno a su directorio",
        "No declara dependencias",
        "No orquesta el ciclo",
        "No emite cadena auditable",
        "No asigna K numérico",
    ],

    # ----- AUTORIDAD -----
    "autoridad": [
        "Declarar el registro O y permite_k",
        "Clasificar modo_entrada, estado y evento",
        "Validar forma y dominio de cada *.py interno",
        "Reportar estado, inventario y diagnóstico propios",
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
        "resolver_contexto",
        "obtener_registro_O",
        "consultar_permite_k",
        "obtener_inventario",
        "obtener_reporte",
        "obtener_diagnostico",
        "verificar_coherencia",
        "listar_axiomas_operativos",
    ],

    # ----- CAPACIDADES -----
    "capacidades": {
        "verificar": "barrer",
        "barrer": "barrer",
        "evaluar": "resolver",
        "resolver": "resolver",
        "inventario": "inventario",
        "axiomas": "axiomas",
        "reporte": "reporte",
        "diagnostico": "diagnostico",
        "verificar_salida": "verificar_salida",
    },

    # ----- METADATOS DE CAPACIDADES (1:1 obligatorio) -----
    "capacidades_meta": {
        "verificar": {
            "descripcion": "Alias de barrer. Verifica coherencia de este módulo.",
            "entrada": "peticion opcional dict",
            "salida": "dict con coherente, errores, registro, permite_k",
        },
        "barrer": {
            "descripcion": (
                "Evalúa coherencia de clasificadores internos. "
                "No calcula Tru."
            ),
            "entrada": "peticion opcional dict",
            "salida": "dict con coherente, errores, reglas_internas",
        },
        "evaluar": {
            "descripcion": "Alias de resolver. Clasifica O_context.",
            "entrada": "peticion: dict | None",
            "salida": "dict con O_context, registro, permite_k, coherente",
        },
        "resolver": {
            "descripcion": (
                "Clasifica el marco O: registro, estado, evento, "
                "permite_k, pedir_anuncio. Centinela auto-valida *.py."
            ),
            "entrada": "peticion: dict | None",
            "salida": "dict con O_context, registro, permite_k, errores, notas",
        },
        "inventario": {
            "descripcion": "Inventario de modos, estados, reglas internas y centinela.",
            "entrada": "peticion opcional",
            "salida": "dict con id, version, reglas_internas, modos_entrada",
        },
        "axiomas": {
            "descripcion": "Declaraciones operativas de este módulo.",
            "entrada": "ninguna",
            "salida": "list[dict] de declaraciones",
        },
        "reporte": {
            "descripcion": "Reporte interno de estado de este módulo.",
            "entrada": "ninguna",
            "salida": "dict con estado, coherente, errores, capacidades",
        },
        "diagnostico": {
            "descripcion": "Diagnóstico: qué falta o está mal en este módulo.",
            "entrada": "ninguna",
            "salida": "dict con estado, problemas, advertencias, recomendaciones",
        },
        "verificar_salida": {
            "descripcion": "Comprueba si una salida de resolver/barrer es coherente.",
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
    tipos: List[str] = []
    if isinstance(raw, str):
        for p in raw.replace(";", ",").split(","):
            p = p.strip()
            if p in TIPOS_PETICION and p not in tipos:
                tipos.append(p)
    elif isinstance(raw, (list, tuple, set)):
        for x in raw:
            s = str(x).strip()
            if s in TIPOS_PETICION and s not in tipos:
                tipos.append(s)
    return tipos


def _normalizar_registro(peticion: Dict[str, Any]) -> Dict[str, Any]:
    reg = _registro_vacio()

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

    if estado_decl in ESTADOS_O:
        reg["estado"] = estado_decl
    elif reg["O_id"] and reg["enunciado_O"]:
        reg["estado"] = "estable"
    else:
        reg["estado"] = "indefinido"

    evento = peticion.get("evento")
    if evento in EVENTOS:
        reg["evento"] = evento
    elif reg["estado"] == "estable":
        reg["evento"] = "mismo_O"
    else:
        reg["evento"] = "indefinido"

    pedir = False
    for k in _CLAVES_PEDIR_ANUNCIO:
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
    """Solo mira el propio registro."""
    if registro.get("estado") != "estable":
        return False
    if not registro.get("O_id") or not registro.get("enunciado_O"):
        return False
    return True


def _validar_regla_meta(stem: str, regla: Any) -> List[str]:
    errs: List[str] = []
    if not isinstance(regla, dict):
        return ["{0}: REGLA debe ser dict".format(stem)]

    for k in REGLA_CAMPOS_OBLIGATORIOS:
        if k not in regla or not str(regla.get(k, "")).strip():
            errs.append(
                "{0}: REGLA sin campo obligatorio '{1}'".format(stem, k)
            )

    rid = str(regla.get("id", "")).strip()
    if rid and not (
        rid.startswith("CX-")
        or rid.startswith("CX_R")
        or "CX" in rid.upper()
    ):
        anclas = regla.get("anclas_cx") or regla.get("anclas") or []
        if not anclas:
            errs.append(
                "{0}: id '{1}' no anclado a dominio CX "
                "(use prefijo CX- o anclas_cx/anclas)".format(stem, rid)
            )

    desc = str(regla.get("descripcion", "")).lower()
    for frag in _PROHIBIDOS_EN_DESCRIPCION:
        if frag in desc:
            errs.append(
                "{0}: descripcion declara oficio prohibido ({1!r}); "
                "este módulo no calcula Tru ni asigna K numérico".format(
                    stem, frag
                )
            )
    return errs


def _validar_clasificacion(stem: str, cls: Any) -> List[str]:
    errs: List[str] = []
    if not isinstance(cls, dict):
        return ["{0}: clasificar() debe devolver dict".format(stem)]

    for k in ("Tru_Ri", "Tru_total", "tru_ri", "tru_total", "C", "L", "K"):
        if k in cls and cls[k] is not None:
            if k == "K" and not isinstance(cls.get("K"), bool):
                errs.append(
                    "{0}: clasificar() no debe asignar K numérico".format(stem)
                )
            if k.lower().startswith("tru"):
                errs.append(
                    "{0}: clasificar() no debe emitir {1}".format(stem, k)
                )

    if "estado" in cls and cls["estado"] is not None:
        if cls["estado"] not in ESTADOS_O:
            errs.append(
                "{0}: estado {1!r} no ∈ {2}".format(
                    stem, cls["estado"], ESTADOS_O
                )
            )
    if "evento" in cls and cls["evento"] is not None:
        if cls["evento"] not in EVENTOS:
            errs.append(
                "{0}: evento {1!r} no ∈ {2}".format(
                    stem, cls["evento"], EVENTOS
                )
            )

    tps = cls.get("tipos_peticion")
    if tps is not None:
        if not isinstance(tps, list):
            errs.append("{0}: tipos_peticion debe ser list".format(stem))
        else:
            for t in tps:
                if t not in TIPOS_PETICION:
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
            "{0}: sin REGLA ni validar()/clasificar() — "
            "no es clasificador de este módulo".format(stem)
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
        nombre_mod = "contexto_regla_{0}".format(archivo.stem)
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

def resolver(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Clasifica el contexto aplicable + centinela de archivos internos.
    No calcula Tru. No asigna K numérico.
    """
    peticion = dict(peticion or {})
    reglas = _cargar_reglas(peticion if peticion else None)
    choques_reglas = _detectar_choques_reglas(reglas)

    errores: List[str] = []
    if choques_reglas:
        errores.extend(choques_reglas)

    for nombre, datos in reglas.items():
        if "error" in datos:
            errores.append("regla '{0}': {1}".format(nombre, datos["error"]))
        for ec in datos.get("errores_centinela") or []:
            if ec not in errores:
                errores.append("centinela '{0}': {1}".format(nombre, ec))

    if not peticion:
        salida = {
            "O_context": None,
            "registro": None,
            "permite_k": False,
            "pedir_anuncio": False,
            "tipos_peticion": [],
            "coherente": not errores,
            "escala": "macro",
            "modo_entrada": "repositorio",
            "reglas_internas": {
                "total": len(reglas),
                "choques": choques_reglas,
                "detalle": reglas,
            },
            "errores": errores,
            "notas": [
                "sin petición: solo centinela de archivos internos; "
                "K no reclamable sin registro O estable"
            ],
            "ids_cx_relevantes": ["CX-A1", "CX-C4"],
        }
    else:
        registro = _normalizar_registro(peticion)
        errores.extend(_conflicto_ligaduras(registro.get("ligaduras") or {}))

        if (
            registro.get("modo_entrada")
            and registro["modo_entrada"] not in MODOS_ENTRADA
        ):
            errores.append(
                "modo_entrada no reconocido: {0!r} (admitidos: {1})".format(
                    registro["modo_entrada"], MODOS_ENTRADA
                )
            )

        for nombre, datos in reglas.items():
            cls = datos.get("clasificacion")
            if not isinstance(cls, dict):
                continue
            if cls.get("estado") in ESTADOS_O:
                registro["estado"] = cls["estado"]
            if cls.get("evento") in EVENTOS:
                registro["evento"] = cls["evento"]
            if cls.get("pedir_anuncio") is True:
                registro["pedir_anuncio"] = True
            tps = cls.get("tipos_peticion")
            if isinstance(tps, list) and tps:
                seen = set(registro.get("tipos_peticion") or [])
                for t in tps:
                    if t in TIPOS_PETICION and t not in seen:
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

        ids = ["CX-A14", "CX-A1", "CX-C4"]
        if registro["estado"] != "estable":
            ids.extend(["CX-A10", "CX-T13"])
        if registro.get("ligaduras"):
            ids.extend(["CX-A15", "CX-T12"])
        if registro.get("evento") == "cambio":
            ids.extend(["CX-A8", "CX-T6"])
        if registro.get("pedir_anuncio"):
            ids.extend(["PA-A1", "PA-A2", "PA-T1", "PA-C2"])

        salida = {
            "O_context": o_ctx if not es_undefined(o_ctx) else UNDEFINED,
            "registro": registro,
            "permite_k": permite,
            "pedir_anuncio": bool(registro.get("pedir_anuncio")),
            "tipos_peticion": list(registro.get("tipos_peticion") or []),
            "coherente": not errores,
            "escala": "micro+macro",
            "modo_entrada": registro.get("modo_entrada"),
            "reglas_internas": {
                "total": len(reglas),
                "choques": choques_reglas,
                "detalle": reglas,
            },
            "errores": errores,
            "notas": [],
            "ids_cx_relevantes": ids,
        }
        if not registro.get("O_id") or not registro.get("enunciado_O"):
            salida["notas"].append(
                "registro incompleto: sin O_id o enunciado_O → estado indefinido; "
                "no reclamar Tru/K completo"
            )
        if not permite:
            salida["notas"].append(
                "permite_k=False: O no estable o registro incompleto"
            )
        if registro.get("pedir_anuncio"):
            salida["notas"].append(
                "pedir_anuncio=True: solicitud de cadena clasificada; "
                "no implica permite_k ni Tru"
            )

    if not reglas:
        salida["notas"].append(
            "sin archivos de regla internos "
            "(vacío legítimo hasta montar clasificadores)"
        )

    return salida


def barrer(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    r = resolver(peticion)
    return {
        "contenedor": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "coherente": r.get("coherente", False),
        "errores": r.get("errores") or [],
        "reglas_internas": r.get("reglas_internas"),
        "registro": r.get("registro"),
        "permite_k": r.get("permite_k"),
        "pedir_anuncio": r.get("pedir_anuncio"),
        "notas": r.get("notas") or [],
        "version": VERSION_MODULO,
    }


def verificar_salida(salida: Dict[str, Any]) -> bool:
    if not isinstance(salida, dict):
        return False
    if "coherente" not in salida:
        return False
    return bool(salida.get("coherente", False))


def inventario(peticion: Any = None) -> Dict[str, Any]:
    reglas = _cargar_reglas()
    n_centinela = sum(
        1 for d in reglas.values() if d.get("errores_centinela")
    )
    return {
        "id": ID_MODULO,
        "nombre": NOMBRE_MODULO,
        "rol": ROL_MODULO,
        "version": VERSION_MODULO,
        "version_contrato": VERSION_CONTRATO,
        "esquema": ESQUEMA_CONTRATO,
        "estabilidad": ESTABILIDAD,
        "reglas_internas": list(reglas.keys()),
        "total_reglas": len(reglas),
        "reglas_con_alerta_centinela": n_centinela,
        "modos_entrada": list(MODOS_ENTRADA),
        "estados_O": list(ESTADOS_O),
        "eventos": list(EVENTOS),
        "tipos_peticion": list(TIPOS_PETICION),
        "centinela": {
            "regla_campos_obligatorios": list(REGLA_CAMPOS_OBLIGATORIOS),
            "auto_carga": True,
            "rechaza_tru_en_clasificar": True,
            "choque_id_nombre": True,
        },
        "capacidades": list(CONTENEDOR["capacidades"].keys()),
        "requiere": list(CONTENEDOR.get("requiere") or []),
        "invariantes": CONTENEDOR.get("invariantes"),
        "funcion": (
            "Clasifica O_context (registro, modo, ligaduras, evento, "
            "permite_k, pedir_anuncio). Centinela auto-valida cada *.py "
            "interno. No calcula Tru."
        ),
    }


def axiomas() -> List[Dict[str, Any]]:
    return [
        {
            "id": "CX-OP-1",
            "tipo": "axioma",
            "sujeto": "contexto_modulo",
            "relacion": "clasifica_y_no_calcula",
            "objeto": "Tru_Ri_ni_Tru_total",
            "polaridad": True,
            "enunciado": (
                "Este módulo clasifica el marco O; "
                "no calcula Tru_Ri ni Tru_total."
            ),
            "depende_de": [],
            "gobierna": ["contexto"],
        },
        {
            "id": "CX-OP-2",
            "tipo": "axioma",
            "sujeto": "K",
            "relacion": "requiere",
            "objeto": "registro_O_estable",
            "polaridad": True,
            "enunciado": (
                "Sin registro O estable, K no es reclamable."
            ),
            "depende_de": [],
            "gobierna": ["contexto"],
        },
        {
            "id": "CX-OP-3",
            "tipo": "axioma",
            "sujeto": "reglas_internas",
            "relacion": "no_deben",
            "objeto": "contradecirse",
            "polaridad": True,
            "enunciado": (
                "Los archivos de regla de este módulo no pueden contradecirse; "
                "el init vela id/nombre únicos y forma de dominio."
            ),
            "depende_de": [],
            "gobierna": ["contexto"],
        },
        {
            "id": "CX-OP-4",
            "tipo": "axioma",
            "sujeto": "pedir_anuncio",
            "relacion": "clasifica_y_no_emite",
            "objeto": "cadena_auditable",
            "polaridad": True,
            "enunciado": (
                "pedir_anuncio clasifica la solicitud de cadena; "
                "no calcula Tru."
            ),
            "depende_de": [],
            "gobierna": ["contexto"],
        },
        {
            "id": "CX-OP-5",
            "tipo": "axioma",
            "sujeto": "centinela_contexto",
            "relacion": "rechaza",
            "objeto": "archivo_mal_formado",
            "polaridad": True,
            "enunciado": (
                "Todo *.py interno se carga automáticamente; "
                "si incumple forma REGLA, oficio o unicidad id/nombre, "
                "el módulo marca error y coherente=False."
            ),
            "depende_de": ["CX-OP-3"],
            "gobierna": ["contexto"],
        },
    ]


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
        "estado": (
            ESTADO_OPERATIVO if r.get("coherente") else ESTADO_DEGRADADO
        ),
        "coherente": r.get("coherente"),
        "errores": r.get("errores"),
        "reglas_internas": r.get("reglas_internas"),
        "permite_k": r.get("permite_k"),
        "pedir_anuncio": r.get("pedir_anuncio"),
        "notas": r.get("notas"),
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
    problemas: List[Dict[str, Any]] = []
    advertencias: List[str] = []
    recomendaciones: List[str] = []

    if r.get("errores"):
        problemas.append({
            "tipo": "errores_contexto",
            "detalle": r["errores"],
        })
        recomendaciones.append(
            "Corregir clasificadores internos con errores de forma o carga"
        )

    reglas = (r.get("reglas_internas") or {}).get("total", 0)
    if not reglas:
        advertencias.append(
            "Sin clasificadores internos "
            "(legítimo hasta montar archivos de regla)"
        )

    estado = ESTADO_OPERATIVO if r.get("coherente") else ESTADO_DEGRADADO
    if not reglas and not problemas:
        estado = ESTADO_NO_INICIADO

    return {
        "id": ID_MODULO,
        "modulo": NOMBRE_MODULO,
        "estado": estado,
        "problemas": problemas,
        "advertencias": advertencias,
        "recomendaciones": recomendaciones,
        "coherente": r.get("coherente"),
        "errores_n": len(r.get("errores") or []),
        "reglas_n": reglas,
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
    "resolver": resolver,
    "evaluar": resolver,
    "inventario": inventario,
    "axiomas": axiomas,
    "reporte": reporte,
    "diagnostico": diagnostico,
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
    "MODOS_ENTRADA",
    "ESTADOS_O",
    "EVENTOS",
    "TIPOS_PETICION",
    "resolver",
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
# Toda capacidad nueva DEBE agregarse simultáneamente en:
#   1. capacidades
#   2. capacidades_meta  (descripcion, entrada, salida: str)
#   3. _CAP_MAP
#   4. VERSION_MODULO
#
# Todo clasificador nuevo: agregar archivo *.py en este directorio
# con REGLA y/o clasificar()/validar(). Este INIT lo descubre solo.
#
# ===============================================================
# FIN EXTENSIONES FUTURAS
# ===============================================================


# ===============================================================
# FIN DEL MÓDULO
# ===============================================================
