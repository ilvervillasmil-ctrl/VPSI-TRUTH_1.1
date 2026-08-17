# ===============================================================
# VPSI-TRUTH — modules/capacidades_engine/__init__.py
# ===============================================================
#
# MÓDULO:              capacidades_engine
# ID:                  CE
# Rol:                 CE
# Versión módulo:      1.3
# Versión contrato:    1.0
# Esquema contrato:    VPSI-CONTRACT-1.0
# Estabilidad:         ESTABLE
# Compatible desde:   1.0
# API Engine:          >=1.0
#
# ===============================================================
# PARTE 1 — IDENTIDAD, ESTRUCTURA Y CONTRATO BASE
# ===============================================================

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional


# ===============================================================
# 1.1 — RUTAS E IDENTIDAD DEL MÓDULO
# ===============================================================

_DIR = Path(__file__).resolve().parent
_CAP = _DIR

_ID = "CE"
_NOMBRE = "capacidades_engine"
_ROL = "CE"

_VERSION = "1.3"
_VERSION_CONTRATO = "1.0"
_ESQUEMA = "VPSI-CONTRACT-1.0"
_ESTABILIDAD = "ESTABLE"
_COMPATIBLE_DESDE = "1.0"
_API_ENGINE = ">=1.0"


# ===============================================================
# 1.2 — ESTADOS VÁLIDOS
# ===============================================================

_ESTADOS_VALIDOS = [
    "NO_INICIADO",
    "OPERATIVO",
    "DEGRADADO",
    "RECHAZADO",
]


# ===============================================================
# 1.3 — BANDERAS CONTRACTUALES Y DE ENGINE
# ===============================================================

_AUTORIZA_ENGINE = {
    "leer": True,
    "ejecutar": True,
    "consultar": True,
    "recombinar": True,
    "reportar": True,
    "auditar": True,
    "inventariar": True,
    "alterar": False,
    "crear": True,
    "actualizar": False,
    "validar": True,
    "procesar": True,
    "analizar": True,
    "generar": True,
    "exportar": True,
    "importar": True,
    "respaldar": True,
    "recuperar": True,
    "sincronizar": True,
    "monitorear": True,
    "metricas": True,
    "diagnostico": True,
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
    "validar_esquema": True,
    "acceso_archivos": True,
}


_REPORTING = {
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
}


_REQUIERE = [
    "CT",
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
    "TT",
    "CE",
    "CC",
]


_CONSULTAS_SOPORTADAS = [
    "listar_skills",
    "listar_ids",
    "obtener_por_id",
    "listar_archivos",
    "obtener_inventario",
    "verificar_coherencia",
]


# ===============================================================
# PARTE 2 — CAPACIDADES CONTRACTUALES
# ===============================================================

# ===============================================================
# 2.1 — UNIVERSO CANÓNICO DE CAPACIDADES
# ===============================================================
#
# Estas son las capacidades que CE declara.
# No se descubren por heurística.
# No se generan dinámicamente.
#
# Las tres capacidades arquitectónicas son obligatorias:
#   ejecutar_total
#   inspeccionar
#   registrar_inventario
#
# Las capacidades históricas de CE se conservan.
# ===============================================================

_CAPACIDADES_CANONICAS = (
    "verificar",
    "barrer",
    "inventario",
    "skills",
    "ids",
    "por_id",
    "listar_archivos",
    "verificar_salida",
    "ejecutar_total",
    "inspeccionar",
    "registrar_inventario",
)


# ===============================================================
# 2.2 — METADATOS CONTRACTUALES DE CAPACIDADES
# ===============================================================

_CAPACIDADES_META: Dict[str, Dict[str, Any]] = {

    # -----------------------------------------------------------
    # 2.2.1 — verificar
    # -----------------------------------------------------------
    "verificar": {
        "descripcion": (
            "Alias contractual real de barrer. "
            "Verifica la coherencia estructural del inventario CE."
        ),
        "entrada": "*",
        "validar_esquema": ["*"],
        "salida": "dict estructurado de coherencia CE",
        "acceso_archivos": ["*"],
        "arquitectonica": False,
    },

    # -----------------------------------------------------------
    # 2.2.2 — barrer
    # -----------------------------------------------------------
    "barrer": {
        "descripcion": (
            "Centinela determinista de integridad de CE. "
            "Descubre y valida el inventario de skills sin ejecutarlos."
        ),
        "entrada": "*",
        "validar_esquema": ["*"],
        "salida": "dict estructurado de coherencia CE",
        "acceso_archivos": ["*"],
        "arquitectonica": False,
    },

    # -----------------------------------------------------------
    # 2.2.3 — inventario
    # -----------------------------------------------------------
    "inventario": {
        "descripcion": (
            "Inventario estructural y operativo de CE."
        ),
        "entrada": "*",
        "validar_esquema": ["*"],
        "salida": "dict de inventario contractual",
        "acceso_archivos": ["*"],
        "arquitectonica": False,
    },

    # -----------------------------------------------------------
    # 2.2.4 — skills
    # -----------------------------------------------------------
    "skills": {
        "descripcion": (
            "Lista los skills válidos descubiertos por CE."
        ),
        "entrada": "*",
        "validar_esquema": ["*"],
        "salida": "list[dict]",
        "acceso_archivos": ["*"],
        "arquitectonica": False,
    },

    # -----------------------------------------------------------
    # 2.2.5 — ids
    # -----------------------------------------------------------
    "ids": {
        "descripcion": (
            "Obtiene los identificadores de los skills válidos."
        ),
        "entrada": "*",
        "validar_esquema": ["*"],
        "salida": "list[str]",
        "acceso_archivos": ["*"],
        "arquitectonica": False,
    },

    # -----------------------------------------------------------
    # 2.2.6 — por_id
    # -----------------------------------------------------------
    "por_id": {
        "descripcion": (
            "Obtiene un skill por su identificador canónico."
        ),
        "entrada": "skill_id",
        "validar_esquema": ["*"],
        "salida": "dict del skill o None",
        "acceso_archivos": ["*"],
        "arquitectonica": False,
    },

    # -----------------------------------------------------------
    # 2.2.7 — listar_archivos
    # -----------------------------------------------------------
    "listar_archivos": {
        "descripcion": (
            "Lista los archivos Python físicos del directorio CE."
        ),
        "entrada": "*",
        "validar_esquema": ["*"],
        "salida": "list[str]",
        "acceso_archivos": ["*"],
        "arquitectonica": False,
    },

    # -----------------------------------------------------------
    # 2.2.8 — verificar_salida
    # -----------------------------------------------------------
    "verificar_salida": {
        "descripcion": (
            "Verifica estructuralmente una salida de CE."
        ),
        "entrada": "salida",
        "validar_esquema": ["*"],
        "salida": "bool",
        "acceso_archivos": ["*"],
        "arquitectonica": False,
    },

    # -----------------------------------------------------------
    # 2.2.9 — ejecutar_total
    # -----------------------------------------------------------
    "ejecutar_total": {
        "descripcion": (
            "Autoridad operativa de Engine sobre las capacidades "
            "ejecutables propias de CE. Ejecuta las capacidades "
            "contractualmente resueltas sin ejecutar recursivamente "
            "el propio orquestador."
        ),
        "entrada": "peticion opcional",
        "validar_esquema": ["*"],
        "salida": "dict con resultados y errores de ejecución",
        "acceso_archivos": ["*"],
        "arquitectonica": True,
    },

    # -----------------------------------------------------------
    # 2.2.10 — inspeccionar
    # -----------------------------------------------------------
    "inspeccionar": {
        "descripcion": (
            "Inspección estructural de CE. Expone contrato, "
            "capacidades, APIs y estado sin ejecutar skills."
        ),
        "entrada": "peticion opcional",
        "validar_esquema": ["*"],
        "salida": "dict de inspección estructural",
        "acceso_archivos": ["*"],
        "arquitectonica": True,
    },

    # -----------------------------------------------------------
    # 2.2.11 — registrar_inventario
    # -----------------------------------------------------------
    "registrar_inventario": {
        "descripcion": (
            "Genera una instantánea determinista del inventario CE. "
            "No modifica el inventario ni el estado de los skills."
        ),
        "entrada": "peticion opcional",
        "validar_esquema": ["*"],
        "salida": "dict con instantánea de inventario",
        "acceso_archivos": ["*"],
        "arquitectonica": True,
    },
}


# ===============================================================
# 2.3 — VALIDACIÓN ESTRUCTURAL DE METADATOS
# ===============================================================

def _validar_meta_capacidades() -> List[str]:
    errores: List[str] = []

    declaradas = set(_CAPACIDADES_CANONICAS)
    meta = set(_CAPACIDADES_META.keys())

    faltantes = sorted(declaradas - meta)
    extras = sorted(meta - declaradas)

    for nombre in faltantes:
        errores.append(
            "capacidad '{0}' declarada sin capacidades_meta".format(nombre)
        )

    for nombre in extras:
        errores.append(
            "capacidades_meta '{0}' no declarada en capacidades".format(nombre)
        )

    for nombre in sorted(declaradas & meta):
        meta_item = _CAPACIDADES_META.get(nombre)

        if not isinstance(meta_item, dict):
            errores.append(
                "capacidad '{0}': metadato no es dict".format(nombre)
            )
            continue

        if not str(meta_item.get("descripcion") or "").strip():
            errores.append(
                "capacidad '{0}': descripcion vacia".format(nombre)
            )

        if "salida" not in meta_item:
            errores.append(
                "capacidad '{0}': falta salida contractual".format(nombre)
            )

    return errores


# ===============================================================
# PARTE 3 — ESTADO INTERNO DE DESCUBRIMIENTO
# ===============================================================

# Registro interno de errores del descubrimiento.
_ERRORES_DESCUBRIMIENTO: List[Dict[str, Any]] = []


# ===============================================================
# 3.1 — EXTRAER METADATOS DE SKILL
# ===============================================================

def _extraer_meta(mod: Any) -> Optional[Dict[str, Any]]:
    """
    Acepta SKILL / CAPACIDAD como dict o SKILLS / CAPACIDADES
    como lista.

    Mantiene compatibilidad con los mandatos históricos existentes.

    No convierte un archivo en capacidad CE.
    Solo extrae metadatos declarados por el archivo.
    """
    for attr in ("SKILL", "CAPACIDAD", "SKILLS", "CAPACIDADES"):
        raw = getattr(mod, attr, None)

        candidatos: List[Dict[str, Any]] = []

        if isinstance(raw, dict):
            candidatos = [raw]
        elif isinstance(raw, list):
            candidatos = [
                x for x in raw
                if isinstance(x, dict)
            ]

        for meta in candidatos:
            sid = str(meta.get("id") or "").strip().lower()

            if not sid:
                continue

            meta = dict(meta)

            if not str(meta.get("descripcion") or "").strip():
                for alt in (
                    "enunciado",
                    "descripcion_larga",
                    "nota",
                ):
                    valor = str(meta.get(alt) or "").strip()

                    if valor:
                        meta["descripcion"] = valor
                        break

            if not str(meta.get("nombre") or "").strip():
                meta["nombre"] = sid

            if not str(meta.get("version") or "").strip():
                meta["version"] = "1.0"

            if not str(meta.get("descripcion") or "").strip():
                meta["descripcion"] = (
                    "skill nativo del Engine: {0}".format(sid)
                )

            return meta

    return None


# ===============================================================
# 3.2 — CARGAR SKILLS
# ===============================================================

def _cargar_skills() -> Dict[str, Dict[str, Any]]:
    """
    Descubre los archivos *.py físicos de CE.

    Cada archivo debe declarar explícitamente un skill mediante
    SKILL, CAPACIDAD, SKILLS o CAPACIDADES.

    CE no ejecuta el skill descubierto.
    La importación solamente permite obtener su declaración
    contractual existente.
    """
    hallado: Dict[str, Dict[str, Any]] = {}

    if not _CAP.is_dir():
        return hallado

    for f in sorted(_CAP.glob("*.py")):

        if f.name.startswith("_"):
            continue

        clave = "ce_skill_{0}".format(f.stem)

        spec = importlib.util.spec_from_file_location(
            clave,
            str(f),
        )

        if spec is None or spec.loader is None:
            hallado[f.stem] = {
                "archivo": f.name,
                "error": "spec_invalido",
            }
            continue

        mod = importlib.util.module_from_spec(spec)
        sys.modules[clave] = mod

        try:
            spec.loader.exec_module(mod)
        except Exception as e:  # noqa: BLE001
            hallado[f.stem] = {
                "archivo": f.name,
                "error": "{0}: {1}".format(
                    type(e).__name__,
                    e,
                ),
            }
            continue

        meta = _extraer_meta(mod)

        if meta is None:
            hallado[f.stem] = {
                "archivo": f.name,
                "error": "sin SKILL/CAPACIDAD con id",
            }
            continue

        sid = str(meta["id"]).strip().lower()

        if sid in hallado:
            anterior = hallado[sid]

            if isinstance(anterior, dict):
                anterior_archivo = anterior.get("archivo")

                hallado.setdefault(
                    "_duplicados",
                    {
                        "archivo": "?",
                        "error": "ids duplicados",
                    },
                )

                hallado[f"{sid}__{f.stem}"] = {
                    "archivo": f.name,
                    "id": sid,
                    "nombre": meta.get("nombre"),
                    "version": str(
                        meta.get("version") or "1.0"
                    ),
                    "descripcion": str(
                        meta.get("descripcion") or ""
                    ),
                    "oficio": meta.get("oficio"),
                    "material": meta.get("material"),
                    "requiere_catalogo": meta.get(
                        "requiere_catalogo"
                    ),
                    "raw": meta,
                    "duplicado_de": anterior_archivo,
                }
            continue

        hallado[sid] = {
            "archivo": f.name,
            "id": sid,
            "nombre": meta.get("nombre"),
            "version": str(
                meta.get("version") or "1.0"
            ),
            "descripcion": str(
                meta.get("descripcion") or ""
            ),
            "oficio": meta.get("oficio"),
            "material": meta.get("material"),
            "requiere_catalogo": meta.get(
                "requiere_catalogo"
            ),
            "raw": meta,
        }

    return hallado


# ===============================================================
# 3.3 — VALIDAR SKILLS DESCUBIERTOS
# ===============================================================

def _validar_skills(
    hallado: Dict[str, Dict[str, Any]],
) -> List[str]:

    errores: List[str] = []
    por_id: Dict[str, List[str]] = {}

    for sid, meta in sorted(hallado.items()):

        if not isinstance(meta, dict):
            errores.append(
                "{0}: metadata no es dict".format(sid)
            )
            continue

        if meta.get("error"):

            error_texto = str(meta.get("error"))

            if "sin SKILL" not in error_texto:
                errores.append(
                    "{0}: {1}".format(
                        sid,
                        error_texto,
                    )
                )

            continue

        for campo in (
            "id",
            "nombre",
            "version",
            "descripcion",
        ):
            if not str(meta.get(campo) or "").strip():
                errores.append(
                    "skill '{0}': falta '{1}'".format(
                        sid,
                        campo,
                    )
                )

        archivo = meta.get("archivo") or sid
        por_id.setdefault(sid, []).append(archivo)

    for sid, archivos in sorted(por_id.items()):

        if len(archivos) > 1:
            errores.append(
                "id '{0}' repetido en {1}".format(
                    sid,
                    archivos,
                )
            )

    return errores


# ===============================================================
# PARTE 4 — API PÚBLICA DE SKILLS
# ===============================================================

# ===============================================================
# 4.1 — SKILLS
# ===============================================================

def skills() -> List[Dict[str, Any]]:
    """
    Devuelve todos los skills válidos descubiertos por CE.

    CE descubre y expone.
    Engine ejecuta.
    """
    hallado = _cargar_skills()

    out: List[Dict[str, Any]] = []

    for sid, meta in sorted(hallado.items()):

        if not isinstance(meta, dict):
            continue

        if meta.get("error"):
            continue

        out.append({
            "id": meta.get("id"),
            "nombre": meta.get("nombre"),
            "version": meta.get("version"),
            "descripcion": meta.get("descripcion"),
            "archivo": meta.get("archivo"),
            "oficio": meta.get("oficio"),
            "material": meta.get("material"),
        })

    return out


# ===============================================================
# 4.2 — IDS
# ===============================================================

def ids() -> List[str]:
    """Devuelve los IDs de todos los skills válidos."""
    return [
        s["id"]
        for s in skills()
        if s.get("id")
    ]


# ===============================================================
# 4.3 — POR ID
# ===============================================================

def por_id(
    skill_id: str,
) -> Optional[Dict[str, Any]]:

    if skill_id is None:
        return None

    clave = str(skill_id).strip().lower()

    if not clave:
        return None

    for skill in skills():
        if skill.get("id") == clave:
            return skill

    return None


# ===============================================================
# 4.4 — LISTAR ARCHIVOS
# ===============================================================

def listar_archivos() -> List[str]:
    """
    Devuelve los archivos Python físicos no privados del
    directorio CE en orden determinista.
    """
    if not _CAP.is_dir():
        return []

    return [
        p.name
        for p in sorted(_CAP.glob("*.py"))
        if not p.name.startswith("_")
    ]


# ===============================================================
# PARTE 5 — CENTINELA
# ===============================================================

# ===============================================================
# 5.1 — BARRER
# ===============================================================

def barrer() -> Dict[str, Any]:
    """
    Centinela estructural de CE.

    Verifica:
      1. integridad del directorio;
      2. declaraciones de skills;
      3. IDs;
      4. duplicados;
      5. metadatos mínimos;
      6. contrato interno de capacidades.

    No ejecuta skills.
    No selecciona skills.
    No interpreta peticiones.
    No coordina ciclos.
    """

    errores: List[str] = []

    errores.extend(_validar_meta_capacidades())

    directorio_ok = _CAP.is_dir()

    if not directorio_ok:
        errores.append(
            "directorio CE no existe: {0}".format(_CAP)
        )

    hallado = _cargar_skills()
    errores.extend(_validar_skills(hallado))

    lista_ids = [
        sid
        for sid, meta in sorted(hallado.items())
        if isinstance(meta, dict)
        and not meta.get("error")
        and sid != "_duplicados"
    ]

    archivos = listar_archivos()

    notas: List[str] = []

    if directorio_ok and not lista_ids:
        notas.append(
            "ningún skill válido; archivos en CE: {0}".format(
                archivos or "(ninguno)"
            )
        )

        for sid, meta in sorted(hallado.items()):
            if isinstance(meta, dict) and meta.get("error"):
                notas.append(
                    "{0}: {1}".format(
                        sid,
                        meta["error"],
                    )
                )

    coherente = (
        directorio_ok
        and not errores
    )

    estado = (
        "OPERATIVO"
        if coherente
        else "DEGRADADO"
    )

    return {
        "id": _ID,
        "nombre": _NOMBRE,
        "contenedor": _NOMBRE,
        "rol": _ROL,
        "version": _VERSION,
        "version_contrato": _VERSION_CONTRATO,
        "esquema": _ESQUEMA,
        "estabilidad": _ESTABILIDAD,
        "estado": estado,
        "coherente": coherente,
        "errores": errores,
        "choques": [],
        "ids": lista_ids,
        "n": len(lista_ids),
        "archivos": archivos,
        "notas": notas,
        "ruta_capacidades": str(_CAP),
        "capacidades_contractuales": list(
            _CAPACIDADES_CANONICAS
        ),
        "capacidades_meta_n": len(
            _CAPACIDADES_META
        ),
        "nota": (
            "CE descubre, valida y expone skills. "
            "Engine es la autoridad que ejecuta los skills."
        ),
    }


# ===============================================================
# 5.2 — VERIFICAR
# ===============================================================

def verificar() -> Dict[str, Any]:
    """
    Alias contractual real de barrer.

    No duplica lógica.
    """
    return barrer()


# ===============================================================
# PARTE 6 — INVENTARIO Y VERIFICACIÓN DE SALIDA
# ===============================================================

# ===============================================================
# 6.1 — INVENTARIO
# ===============================================================

def inventario(
    peticion: Any = None,
) -> Dict[str, Any]:
    """
    Inventario determinista de CE.

    No modifica skills ni historial.
    """
    b = barrer()

    return {
        "id": _ID,
        "nombre": _NOMBRE,
        "contenedor": _NOMBRE,
        "rol": _ROL,
        "version": _VERSION,
        "version_contrato": _VERSION_CONTRATO,
        "esquema": _ESQUEMA,
        "estabilidad": _ESTABILIDAD,
        "compatible_desde": _COMPATIBLE_DESDE,
        "api_engine": _API_ENGINE,
        "estado": b.get("estado"),
        "coherente": b.get("coherente"),
        "ids": list(b.get("ids") or []),
        "n": b.get("n", 0),
        "archivos": list(b.get("archivos") or []),
        "skills": skills(),
        "capacidades": list(
            _CAPACIDADES_CANONICAS
        ),
        "capacidades_meta": dict(
            _CAPACIDADES_META
        ),
        "autoriza_engine": dict(
            _AUTORIZA_ENGINE
        ),
        "reporting": dict(
            _REPORTING
        ),
        "errores": list(
            b.get("errores") or []
        ),
        "funcion": (
            "Capacidad estructural del Engine que mantiene "
            "el inventario operativo de skills nativos. "
            "CE descubre, valida y expone; Engine ejecuta."
        ),
    }


# ===============================================================
# 6.2 — VERIFICAR SALIDA
# ===============================================================

def verificar_salida(
    salida: Any,
) -> bool:
    """
    Verificación estructural estricta de una salida CE.

    No acepta un dict arbitrario por la mera presencia de
    una clave aislada.
    """

    if not isinstance(salida, dict):
        return False

    campos_obligatorios = (
        "id",
        "nombre",
        "rol",
        "version",
        "version_contrato",
        "esquema",
        "coherente",
        "ids",
        "n",
        "archivos",
    )

    if any(
        campo not in salida
        for campo in campos_obligatorios
    ):
        return False

    if salida.get("id") != _ID:
        return False

    if salida.get("nombre") != _NOMBRE:
        return False

    if salida.get("rol") != _ROL:
        return False

    if salida.get("version") != _VERSION:
        return False

    if salida.get("version_contrato") != _VERSION_CONTRATO:
        return False

    if salida.get("esquema") != _ESQUEMA:
        return False

    if not isinstance(
        salida.get("coherente"),
        bool,
    ):
        return False

    ids_salida = salida.get("ids")

    if not isinstance(ids_salida, list):
        return False

    if any(
        not isinstance(x, str)
        for x in ids_salida
    ):
        return False

    n_salida = salida.get("n")

    if not isinstance(n_salida, int):
        return False

    if n_salida != len(ids_salida):
        return False

    archivos = salida.get("archivos")

    if not isinstance(archivos, list):
        return False

    if any(
        not isinstance(x, str)
        for x in archivos
    ):
        return False

    errores = salida.get("errores")

    if errores is not None and not isinstance(
        errores,
        list,
    ):
        return False

    return True


# ===============================================================
# PARTE 7 — INSPECCIÓN ESTRUCTURAL
# ===============================================================

# ===============================================================
# 7.1 — INSPECCIONAR
# ===============================================================

def inspeccionar(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Inspección estructural de CE.

    No ejecuta skills.
    No selecciona skills.
    No modifica el contrato.
    """

    barrido = barrer()

    return {
        "id": _ID,
        "modulo": _NOMBRE,
        "rol": _ROL,
        "version": _VERSION,
        "version_contrato": _VERSION_CONTRATO,
        "esquema": _ESQUEMA,
        "estabilidad": _ESTABILIDAD,
        "compatible_desde": _COMPATIBLE_DESDE,
        "api_engine": _API_ENGINE,
        "constantes": {
            "ID": _ID,
            "NOMBRE": _NOMBRE,
            "ROL": _ROL,
            "VERSION": _VERSION,
            "VERSION_CONTRATO": _VERSION_CONTRATO,
            "ESQUEMA": _ESQUEMA,
            "ESTABILIDAD": _ESTABILIDAD,
            "COMPATIBLE_DESDE": _COMPATIBLE_DESDE,
            "API_ENGINE": _API_ENGINE,
        },
        "capacidades": list(
            _CAPACIDADES_CANONICAS
        ),
        "capacidades_meta": dict(
            _CAPACIDADES_META
        ),
        "autoriza_engine": dict(
            _AUTORIZA_ENGINE
        ),
        "reporting": dict(
            _REPORTING
        ),
        "consultas_soportadas": list(
            _CONSULTAS_SOPORTADAS
        ),
        "dependencias": list(
            _REQUIERE
        ),
        "estado": barrido.get("estado"),
        "coherente": barrido.get("coherente"),
        "errores": list(
            barrido.get("errores") or []
        ),
        "ids": list(
            barrido.get("ids") or []
        ),
        "archivos": list(
            barrido.get("archivos") or []
        ),
        "nota": (
            "Inspección estructural de CE. "
            "No ejecuta skills ni modifica el contrato."
        ),
    }


# ===============================================================
# PARTE 8 — REGISTRO DE INVENTARIO
# ===============================================================

# ===============================================================
# 8.1 — REGISTRAR INVENTARIO
# ===============================================================

def registrar_inventario(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Genera una instantánea determinista del inventario CE.

    No modifica:
      - CONTENEDOR
      - skills
      - archivos
      - estado externo
    """

    inv = inventario(peticion)

    return {
        "id": _ID,
        "modulo": _NOMBRE,
        "operacion": "registrar_inventario",
        "registrado": True,
        "inventario": inv,
        "nota": (
            "Instantánea estructural del inventario CE. "
            "No modifica el estado del módulo."
        ),
    }


# ===============================================================
# PARTE 9 — EJECUCIÓN TOTAL
# ===============================================================

# ===============================================================
# 9.1 — MAPA LOCAL DE CALLABLES
# ===============================================================
#
# El mapa se construye DESPUÉS de definir todas las funciones.
# Esto evita referencias adelantadas y NameError estructurales.
# ===============================================================

_CAP_MAP: Dict[str, Callable[..., Any]] = {
    "verificar": verificar,
    "barrer": barrer,
    "inventario": inventario,
    "skills": skills,
    "ids": ids,
    "por_id": por_id,
    "listar_archivos": listar_archivos,
    "verificar_salida": verificar_salida,
    "ejecutar_total": None,          # resuelto después de definirla
    "inspeccionar": inspeccionar,
    "registrar_inventario": registrar_inventario,
}


# ===============================================================
# 9.2 — RESOLUCIÓN DE CAPACIDADES
# ===============================================================

def _resolver_capacidades() -> Dict[str, Callable[..., Any]]:
    """
    Resuelve exclusivamente las capacidades canónicas de CE.

    Toda capacidad debe terminar apuntando a un callable real.
    No se aceptan capacidades desconocidas.
    """

    errores = _validar_meta_capacidades()

    if errores:
        raise RuntimeError(
            "Contrato de capacidades inválido: {0}".format(
                errores
            )
        )

    resueltas: Dict[str, Callable[..., Any]] = {}

    for nombre in _CAPACIDADES_CANONICAS:

        fn = _CAP_MAP.get(nombre)

        if nombre == "ejecutar_total":
            fn = ejecutar_total

        if not callable(fn):
            raise RuntimeError(
                "Capacidad '{0}' no es callable".format(
                    nombre
                )
            )

        resueltas[nombre] = fn

    return resueltas


# ===============================================================
# 9.3 — EJECUTAR TOTAL
# ===============================================================

def ejecutar_total(
    peticion: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Autoridad operativa de Engine sobre CE.

    Ejecuta todas las capacidades contractualmente declaradas
    y resolubles, excepto el propio ejecutar_total para impedir
    recursión infinita.

    No ejecuta los skills descubiertos por CE:
    Engine es quien los ejecuta.

    La enumeración procede del contrato canónico y no de una
    lista manual independiente.
    """

    peticion_dict = (
        dict(peticion)
        if isinstance(peticion, dict)
        else {}
    )

    resultados: Dict[str, Any] = {}
    errores: List[Dict[str, Any]] = []
    capacidades_ejecutadas: List[str] = []
    capacidades_rechazadas: List[str] = []

    # -----------------------------------------------------------
    # 9.3.1 — Resolver capacidades
    # -----------------------------------------------------------

    try:
        capacidades = _resolver_capacidades()
    except Exception as e:  # noqa: BLE001
        return {
            "id": _ID,
            "modulo": _NOMBRE,
            "rol": _ROL,
            "version": _VERSION,
            "operacion": "ejecutar_total",
            "estado": "RECHAZADO",
            "coherente": False,
            "capacidades_ejecutadas": [],
            "capacidades_rechazadas": list(
                _CAPACIDADES_CANONICAS
            ),
            "errores_ejecucion": [
                {
                    "capacidad": "resolucion",
                    "tipo": type(e).__name__,
                    "detalle": str(e),
                }
            ],
            "resultados": {},
            "capacidades_declaradas": list(
                _CAPACIDADES_CANONICAS
            ),
        }

    # -----------------------------------------------------------
    # 9.3.2 — Ejecutar capacidades contractuales
    # -----------------------------------------------------------

    for nombre in _CAPACIDADES_CANONICAS:

        # El propio orquestador no puede invocarse a sí mismo.
        if nombre == "ejecutar_total":
            capacidades_rechazadas.append(nombre)
            continue

        fn = capacidades.get(nombre)

        if not callable(fn):
            capacidades_rechazadas.append(nombre)
            errores.append({
                "capacidad": nombre,
                "tipo": "CallableInvalido",
                "detalle": (
                    "capacidad resuelta sin callable real"
                ),
            })
            continue

        try:

            if nombre in (
                "por_id",
            ):
                resultado = fn(
                    peticion_dict.get("skill_id")
                    or peticion_dict.get("id")
                )

            elif nombre in (
                "verificar_salida",
            ):
                resultado = fn(
                    peticion_dict.get("salida")
                )

            elif nombre in (
                "inventario",
                "inspeccionar",
                "registrar_inventario",
            ):
                resultado = fn(peticion_dict)

            else:
                resultado = fn()

            resultados[nombre] = resultado
            capacidades_ejecutadas.append(nombre)

        except Exception as e:  # noqa: BLE001

            capacidades_rechazadas.append(nombre)

            errores.append({
                "capacidad": nombre,
                "tipo": type(e).__name__,
                "detalle": str(e),
            })

            resultados[nombre] = None

    # -----------------------------------------------------------
    # 9.3.3 — Coherencia final
    # -----------------------------------------------------------

    coherente = (
        not errores
        and not capacidades_rechazadas
    )

    estado = (
        "OPERATIVO"
        if coherente
        else "DEGRADADO"
    )

    return {
        "id": _ID,
        "modulo": _NOMBRE,
        "rol": _ROL,
        "version": _VERSION,
        "version_contrato": _VERSION_CONTRATO,
        "esquema": _ESQUEMA,
        "operacion": "ejecutar_total",
        "estado": estado,
        "coherente": coherente,
        "capacidades_ejecutadas": list(
            capacidades_ejecutadas
        ),
        "capacidades_rechazadas": list(
            capacidades_rechazadas
        ),
        "errores_ejecucion": list(
            errores
        ),
        "resultados": resultados,
        "capacidades_declaradas": list(
            _CAPACIDADES_CANONICAS
        ),
        "capacidades_resueltas": sorted(
            capacidades.keys()
        ),
        "nota": (
            "ejecutar_total ejerce autoridad de Engine sobre "
            "las capacidades propias de CE. El propio "
            "ejecutar_total no se invoca recursivamente. "
            "Los skills descubiertos no son ejecutados por CE."
        ),
    }


# Resolver la referencia del propio orquestador ahora que existe.
_CAP_MAP["ejecutar_total"] = ejecutar_total


# ===============================================================
# PARTE 10 — CONTENEDOR CONTRACTUAL
# ===============================================================

# ===============================================================
# 10.1 — VALIDACIÓN 1:1 DE CAPACIDADES
# ===============================================================

def _validar_resolucion_capacidades() -> List[str]:
    """
    Demuestra la cadena:

        capacidades
            ↓
        capacidades_meta
            ↓
        _CAP_MAP
            ↓
        callable real
    """

    errores: List[str] = []

    declaradas = set(_CAPACIDADES_CANONICAS)
    meta = set(_CAPACIDADES_META.keys())
    mapa = set(_CAP_MAP.keys())

    for nombre in sorted(declaradas - meta):
        errores.append(
            "capacidad '{0}' sin capacidades_meta".format(
                nombre
            )
        )

    for nombre in sorted(declaradas - mapa):
        errores.append(
            "capacidad '{0}' sin entrada en _CAP_MAP".format(
                nombre
            )
        )

    for nombre in sorted(meta - declaradas):
        errores.append(
            "capacidades_meta '{0}' no declarada".format(
                nombre
            )
        )

    for nombre in sorted(mapa - declaradas):
        errores.append(
            "_CAP_MAP contiene capacidad no declarada '{0}'".format(
                nombre
            )
        )

    for nombre in sorted(declaradas & mapa):
        if not callable(_CAP_MAP.get(nombre)):
            errores.append(
                "capacidad '{0}' no apunta a callable real".format(
                    nombre
                )
            )

    return errores


# ===============================================================
# 10.2 — CONTENEDOR
# ===============================================================

CONTENEDOR: Dict[str, Any] = {

    # ============================================================
    # 10.2.1 — ESQUEMA E IDENTIDAD
    # ============================================================

    "esquema": _ESQUEMA,
    "version_contrato": _VERSION_CONTRATO,
    "version_modulo": _VERSION,
    "estabilidad": _ESTABILIDAD,
    "compatible_desde": _COMPATIBLE_DESDE,
    "api_engine": _API_ENGINE,

    "id": _ID,
    "nombre": _NOMBRE,
    "rol": _ROL,

    # ============================================================
    # 10.2.2 — DESCRIPCIÓN
    # ============================================================

    "descripcion": (
        "Capacidad estructural del Engine que agrupa múltiples "
        "skills nativos. Los archivos son implementación física; "
        "los skills son competencias operativas; el mandato es "
        "la forma en que Engine los invoca. CE descubre, valida "
        "y expone skills. Engine es la autoridad de ejecución."
    ),

    # ============================================================
    # 10.2.3 — FUNCIÓN DEL MÓDULO
    # ============================================================

    "funcion": (
        "Mantener el inventario operativo de skills nativos "
        "del Engine, descubrir sus declaraciones, validar "
        "su estructura y exponerlas a Engine."
    ),

    # ============================================================
    # 10.2.4 — LO QUE CE NO HACE
    # ============================================================

    "no_hace": [
        "No toma decisiones",
        "No selecciona skills",
        "No ejecuta skills",
        "No coordina ciclos",
        "No interpreta peticiones",
        "No calcula C / L / K / Tru",
        "No deposita evidencia",
        "No orquesta el sistema",
        "No compite con módulos de dominio",
    ],

    # ============================================================
    # 10.2.5 — AUTORIDAD
    # ============================================================

    "autoridad": [
        "Mantener inventario operativo de skills nativos",
        "Descubrir skills declarados",
        "Validar estructura mínima de skills",
        "Exponer skills e IDs a Engine",
        "Reportar estado e inventario propios",
    ],

    # ============================================================
    # 10.2.6 — CONOCIMIENTO EXPORTABLE
    # ============================================================

    "conocimiento_exportable": list(
        _CAPACIDADES_CANONICAS
    ),

    # ============================================================
    # 10.2.7 — ACCESO
    # ============================================================

    "acceso": {
        "nivel": "completo",
        "descripcion": "Acceso total a recursos del módulo",
    },

    # ============================================================
    # 10.2.8 — DEPENDENCIAS
    # ============================================================

    "requiere": list(_REQUIERE),

    # ============================================================
    # 10.2.9 — ACCESO A ARCHIVOS
    # ============================================================

    "acceso_archivos": ["*"],

    # ============================================================
    # 10.2.10 — VALIDACIÓN DE ESQUEMA
    # ============================================================

    "validar_esquema": ["*"],

    # ============================================================
    # 10.2.11 — AUTORIZACIÓN DE ENGINE
    # ============================================================

    "autoriza_engine": dict(
        _AUTORIZA_ENGINE
    ),

    # ============================================================
    # 10.2.12 — CONSULTAS SOPORTADAS
    # ============================================================

    "consultas_soportadas": list(
        _CONSULTAS_SOPORTADAS
    ),

    # ============================================================
    # 10.2.13 — CAPACIDADES
    # ============================================================
    #
    # Aquí quedan referencias CALLABLE reales.
    # No son strings.
    # ============================================================

    "capacidades": dict(_CAP_MAP),

    # ============================================================
    # 10.2.14 — METADATOS DE CAPACIDADES
    # ============================================================

    "capacidades_meta": dict(
        _CAPACIDADES_META
    ),

    # ============================================================
    # 10.2.15 — REPORTING
    # ============================================================

    "reporting": dict(
        _REPORTING
    ),

    # ============================================================
    # 10.2.16 — ESTADOS VÁLIDOS
    # ============================================================

    "estados_validos": list(
        _ESTADOS_VALIDOS
    ),

    # ============================================================
    # 10.2.17 — INVARIANTES
    # ============================================================

    "invariantes": [
        "el id del módulo nunca cambia",
        "el rol nunca cambia",
        "CE es una capacidad estructural",
        "los skills son competencias operativas",
        "Engine es la autoridad que ejecuta los skills",
        "CE descubre, valida y expone skills",
        "CE no toma decisiones",
        "CE no selecciona skills",
        "CE no coordina ciclos",
        "CE no interpreta peticiones",
        "las capacidades contractuales son callables reales",
        "no existen capacidades contractuales fuera del universo canónico",
        "no existen capacidades canónicas sin resolución callable",
        "este módulo no modifica el estado de otros módulos",
        "este módulo no inventa capacidades",
        "este módulo siempre puede reportar su propio estado",
        "inventario incluye identidad contractual del módulo",
    ],
}


# ===============================================================
# PARTE 11 — VALIDACIÓN FINAL DEL CONTRATO
# ===============================================================

# ===============================================================
# 11.1 — VALIDACIÓN DE ESTRUCTURA
# ===============================================================

def _validar_contrato_local() -> None:
    errores: List[str] = []

    errores.extend(
        _validar_meta_capacidades()
    )

    errores.extend(
        _validar_resolucion_capacidades()
    )

    capacidades = CONTENEDOR.get(
        "capacidades"
    )

    if not isinstance(capacidades, dict):
        errores.append(
            "CONTENEDOR['capacidades'] no es dict"
        )
    else:

        declaradas = set(
            _CAPACIDADES_CANONICAS
        )

        actuales = set(
            capacidades.keys()
        )

        for nombre in sorted(
            declaradas - actuales
        ):
            errores.append(
                "capacidad '{0}' falta en CONTENEDOR".format(
                    nombre
                )
            )

        for nombre in sorted(
            actuales - declaradas
        ):
            errores.append(
                "CONTENEDOR contiene capacidad no declarada '{0}'".format(
                    nombre
                )

        for nombre in sorted(
            declaradas & actuales
        ):
            if not callable(
                capacidades.get(nombre)
            ):
                errores.append(
                    "CONTENEDOR capacidad '{0}' no es callable".format(
                        nombre
                    )
                )

    if errores:
        raise RuntimeError(
            "Contrato CE inválido: {0}".format(
                errores
            )
        )


# ===============================================================
# 11.2 — EJECUCIÓN DE VALIDACIÓN
# ===============================================================

_validar_contrato_local()


# ===============================================================
# PARTE 12 — EXPORTACIONES
# ===============================================================

__all__ = [
    "CONTENEDOR",
    "skills",
    "ids",
    "por_id",
    "listar_archivos",
    "barrer",
    "verificar",
    "inventario",
    "verificar_salida",
    "ejecutar_total",
    "inspeccionar",
    "registrar_inventario",
]


# ===============================================================
# FIN PARTE 12
# ===============================================================

# ===============================================================
# FIN DEL MÓDULO
# ===============================================================
