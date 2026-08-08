"""
VPSI-TRUTH --- diagnostics/evidencia.py

Depositario unico de evidencia de evaluacion.

======================================================================
PRINCIPIO

Omega no evalua: solo lee diagnostics/evaluaciones.json.

Quien evalua deposita aqui.

Este modulo es el UNICO escritor canonico de la evidencia persistente de
evaluacion.

Los productores pueden ser:

    - tests
    - auditoria de contratos
    - Engine
    - otros procesos autorizados de evaluacion

Cada productor deposita sus registros identificados mediante `origen`.

El deposito fusiona por origen:

    - conserva los registros de otros origenes
    - reemplaza solamente los registros del origen que deposita
    - no reconstruye registros
    - no recalcula factores
    - no interpreta Tru
    - no modifica el contenido interno de `resultado`

======================================================================
PROBLEMA QUE RESUELVE

El paso "Auditoria estructural de contratos" del CI escribia directamente
evaluaciones.json con write_text() despues de "Run tests".

Eso provocaba que la evidencia producida por los tests pudiera quedar
sobrescrita antes de que Omega la leyera.

Este modulo centraliza la escritura.

Ningun productor debe escribir directamente:

    diagnostics/evaluaciones.json

Los productores deben utilizar:

    depositar(...)
    depositar_desde_engine(...)

======================================================================
CONTRATO DE CONSERVACION — INVIOLABLE

Este modulo:

    SI:
      - valida el identificador de origen
      - copia profundamente cada registro
      - conserva las claves existentes
      - anade `origen` al nivel superior
      - conserva `invocador_id` si ya existe
      - deposita `estado_engine` a nivel documental
      - rehace `secuencia` global
      - fusiona registros por origen

    NO:
      - reconstruye registros
      - elimina claves
      - elimina sujetos
      - elimina n_sujetos
      - modifica `resultado`
      - calcula C
      - calcula L
      - calcula K
      - calcula Tru_Ri
      - calcula Tru_total
      - interpreta taxonomias
      - interpreta citaciones
      - evalua axiomas
      - ejecuta capacidades del Engine

La evidencia recibida se conserva estructuralmente.

======================================================================
VERSIONES

1.0  write_text plano; podia pisar evidencia previa.
1.1  fusion por origen + normalizacion de origen.
1.2  deepcopy + conservacion estructural del registro.
1.3  depositario canonico unico + contrato explicito de conservacion.

======================================================================
"""

from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List, Optional


# ===============================================================
# SEGMENTO 1 --- IDENTIDAD
# ===============================================================

DIAGNOSTICS_DIR = Path(__file__).resolve().parent
RUTA = DIAGNOSTICS_DIR / "evaluaciones.json"

TIPO = "evidencia_evaluacion"
VERSION = "1.3"

_ORIGEN_RE = re.compile(
    r"^[A-Za-z0-9][A-Za-z0-9_\-.]{0,63}$"
)


# ===============================================================
# SEGMENTO 2 --- NORMALIZACION DE ORIGEN
# ===============================================================

def _normalizar_origen(origen: Any) -> str:
    """
    Exige un identificador de origen estable.

    El origen:

      - no puede ser None
      - no puede estar vacio
      - no puede contener comas
      - solo admite letras, digitos, _, -, .
      - longitud maxima: 64 caracteres

    El origen identifica al PRODUCTOR de la evidencia.
    """
    if origen is None:
        raise ValueError(
            "depositar() exige un origen declarado"
        )

    s = str(origen).strip()

    if not s:
        raise ValueError(
            "origen no puede ser vacio"
        )

    if "," in s:
        raise ValueError(
            "origen no puede contener comas "
            "(se usa como separador de lista)"
        )

    if not _ORIGEN_RE.match(s):
        raise ValueError(
            "origen debe ser identificador simple "
            "(letras/digitos/_/-/., max 64 chars): {0!r}".format(s)
        )

    return s


# ===============================================================
# SEGMENTO 3 --- DOCUMENTO VACIO
# ===============================================================

def _documento_vacio() -> Dict[str, Any]:
    """
    Construye un documento vacio canonico.

    No contiene resultados sinteticos.
    """
    return {
        "tipo": TIPO,
        "version": VERSION,
        "origen": None,
        "origenes": [],
        "invocador_id": None,
        "estado_engine": None,
        "n": 0,
        "resultados": [],
    }


# ===============================================================
# SEGMENTO 4 --- LECTURA
# ===============================================================

def leer() -> Dict[str, Any]:
    """
    Devuelve el documento actual.

    Si el archivo no existe, no es JSON valido o no contiene la
    estructura minima esperada, devuelve un documento vacio.

    No modifica el archivo.
    """
    if not RUTA.exists():
        return _documento_vacio()

    try:
        doc = json.loads(
            RUTA.read_text(encoding="utf-8")
        )
    except Exception:
        return _documento_vacio()

    if not isinstance(doc, dict):
        return _documento_vacio()

    if not isinstance(doc.get("resultados"), list):
        return _documento_vacio()

    return doc


# ===============================================================
# SEGMENTO 5 --- NORMALIZACION DE FILAS EXISTENTES
# ===============================================================

def _con_origen(
    doc: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Obtiene las filas del documento conservando su estructura.

    Si una fila no tiene origen, hereda el origen documental.

    Se realiza deepcopy para impedir que el documento cargado y las
    estructuras devueltas compartan referencias mutables.
    """
    heredado = doc.get("origen") or "desconocido"

    if isinstance(heredado, str) and "," in heredado:
        heredado = "desconocido"

    filas: List[Dict[str, Any]] = []

    for registro in doc.get("resultados", []):
        if not isinstance(registro, dict):
            continue

        fila = deepcopy(registro)

        if not fila.get("origen"):
            fila["origen"] = heredado

        filas.append(fila)

    return filas


# ===============================================================
# SEGMENTO 6 --- CONSULTA POR ORIGEN
# ===============================================================

def resultados_de(
    origen: str,
) -> List[Dict[str, Any]]:
    """
    Devuelve exclusivamente la evidencia depositada por `origen`.

    No modifica el documento.
    """
    origen = _normalizar_origen(origen)

    return [
        registro
        for registro in _con_origen(leer())
        if registro.get("origen") == origen
    ]


# ===============================================================
# SEGMENTO 7 --- CONSERVACION ESTRUCTURAL
# ===============================================================

def _conservar_registro(
    r: Dict[str, Any],
    origen: str,
    invocador_id: Optional[str],
) -> Dict[str, Any]:
    """
    Conserva el registro recibido sin reconstruirlo.

    La unica modificacion estructural permitida es:

        origen

    y, si no existe previamente:

        invocador_id

    No se modifica `resultado` ni ninguna de sus claves.
    """
    fila = deepcopy(r)

    fila["origen"] = origen

    if invocador_id is not None:
        fila.setdefault(
            "invocador_id",
            invocador_id,
        )

    return fila


# ===============================================================
# SEGMENTO 8 --- ESCRITURA CANONICA
# ===============================================================

def _escribir(
    resultados: List[Dict[str, Any]],
    doc: Dict[str, Any],
    invocador_id: Optional[str] = None,
    estado_engine: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Escritura unica y canonica del documento.

    Esta funcion:

      - copia profundamente los registros
      - rehace la secuencia global
      - reconstruye unicamente la envoltura documental
      - no reconstruye el contenido de los registros

    No interpreta evidencia.
    """

    filas = [
        deepcopy(r)
        for r in resultados
        if isinstance(r, dict)
    ]

    for i, registro in enumerate(filas, 1):
        registro["secuencia"] = i

    origenes = sorted({
        str(registro.get("origen"))
        for registro in filas
        if registro.get("origen")
    })

    salida = {
        "tipo": TIPO,
        "version": VERSION,
        "origen": (
            ", ".join(origenes)
            if origenes
            else None
        ),
        "origenes": origenes,
        "invocador_id": (
            invocador_id
            if invocador_id is not None
            else doc.get("invocador_id")
        ),
        "estado_engine": (
            estado_engine
            if estado_engine is not None
            else doc.get("estado_engine")
        ),
        "n": len(filas),
        "resultados": filas,
    }

    DIAGNOSTICS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    RUTA.write_text(
        json.dumps(
            salida,
            indent=2,
            ensure_ascii=False,
            default=str,
        ),
        encoding="utf-8",
    )

    return salida


# ===============================================================
# SEGMENTO 9 --- DEPOSITO POR ORIGEN
# ===============================================================

def depositar(
    resultados: List[Dict[str, Any]],
    origen: str,
    invocador_id: Optional[str] = None,
    estado_engine: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Deposita evidencia bajo un origen concreto.

    Regla de fusion:

        otros origenes -> se conservan
        mismo origen   -> se reemplaza

    Esto evita que un productor pise evidencia perteneciente a otro
    productor.

    Cada registro recibido se copia profundamente antes de almacenarse.
    """

    origen = _normalizar_origen(origen)

    doc = leer()

    previos = [
        registro
        for registro in _con_origen(doc)
        if registro.get("origen") != origen
    ]

    nuevos: List[Dict[str, Any]] = []

    for registro in resultados or []:
        if not isinstance(registro, dict):
            continue

        nuevos.append(
            _conservar_registro(
                registro,
                origen,
                invocador_id,
            )
        )

    fusionados = previos + nuevos

    return _escribir(
        fusionados,
        doc,
        invocador_id=invocador_id,
        estado_engine=estado_engine,
    )


# ===============================================================
# SEGMENTO 10 --- DEPOSITO DESDE ENGINE
# ===============================================================

def depositar_desde_engine(
    eng: Any,
    origen: str,
    desde: int = 0,
) -> Dict[str, Any]:
    """
    Deposita la evidencia acumulada por el Engine.

    Si el Engine expone:

        get_resultados_evaluacion()

    se utiliza ese contrato.

    Como compatibilidad secundaria se acepta:

        resultados_evaluacion

    `desde` permite seleccionar solamente las evaluaciones producidas
    desde una posicion concreta.
    """

    if hasattr(
        eng,
        "get_resultados_evaluacion",
    ):
        evaluaciones = list(
            eng.get_resultados_evaluacion() or []
        )
    else:
        evaluaciones = list(
            getattr(
                eng,
                "resultados_evaluacion",
                [],
            ) or []
        )

    if desde < 0:
        desde = 0

    return depositar(
        evaluaciones[desde:],
        origen=origen,
        invocador_id=getattr(
            eng,
            "invocador_id",
            None,
        ),
        estado_engine=getattr(
            eng,
            "estado",
            None,
        ),
    )


# ===============================================================
# SEGMENTO 11 --- LIMPIEZA POR ORIGEN
# ===============================================================

def limpiar(
    origen: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Limpia evidencia.

    Sin `origen`:
        elimina todos los registros.

    Con `origen`:
        elimina solamente los registros de ese origen.

    La evidencia perteneciente a otros origenes permanece intacta.
    """

    doc = leer()

    if origen is None:
        quedan: List[Dict[str, Any]] = []

    else:
        origen = _normalizar_origen(origen)

        quedan = [
            registro
            for registro in _con_origen(doc)
            if registro.get("origen") != origen
        ]

    return _escribir(
        quedan,
        doc,
    )


# ===============================================================
# SEGMENTO 12 --- EXPORTACIONES
# ===============================================================

__all__ = [
    "TIPO",
    "VERSION",
    "RUTA",
    "leer",
    "resultados_de",
    "depositar",
    "depositar_desde_engine",
    "limpiar",
]
