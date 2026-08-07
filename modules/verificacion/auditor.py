# ===============================================================
# VPSI-TRUTH — modules/verificacion/auditor.py
# ===============================================================
#
# Motor de auditoría estructural sobre representación AST.
#
# Oficio único:
#   Recorrer AST → aplicar catálogo de reglas → producir evidencia.
#   No interpreta intención.
#   No calcula métricas.
#   No modifica el código.
#   No clasifica choques finales (eso es VX).
#
# Flujo:
#   AST
#    ↓
#   recorrido
#    ↓
#   regla → return Hallazgo | None
#    ↓
#   motor registra (hallazgo_id, forma uniforme)
#    ↓
#   evidencia → VX
#
# Nomenclatura:
#   AuditorEstructural — compara reglas AST, no axiomas.
#   Los axiomas viven en AX. VX conecta estructura ↔ AX.
#   Alias: AuditorAxiomatico (compatibilidad con INIT actual).
#
# Sintaxis inválida ≠ violación:
#   Error de sintaxis → estado NO_VERIFICABLE
#   Reglas ejecutadas  → VERIFICADO + hallazgos
#
# ===============================================================

from __future__ import annotations

import ast
import itertools
from typing import Any, Callable, Dict, List, Optional, TypedDict


# ===============================================================
# SECCIÓN 1 — TIPOS
# ===============================================================

class HallazgoDict(TypedDict, total=False):
    hallazgo_id: str
    regla_id: str
    categoria: str
    severidad: str
    autoridad: str
    archivo: str
    linea: Optional[int]
    razon: str
    recomendacion: str
    tipo_nodo: Optional[str]
    nombre: Optional[str]
    contexto: Optional[str]


class MetaRegla(TypedDict, total=False):
    id: str
    categoria: str
    autoridad: str
    descripcion: str
    severidad_default: str
    requiere: List[str]
    usa_ast: bool
    usa_axiomas: bool
    ejecutar: Callable[..., Optional[HallazgoDict]]


Severidad = str  # INFO | ADVERTENCIA | ERROR | CRITICO
_SEVERIDADES = ("INFO", "ADVERTENCIA", "ERROR", "CRITICO")


# ===============================================================
# SECCIÓN 2 — EXCEPCIÓN (paro duro opcional)
# ===============================================================

class ContradiccionCodigoError(Exception):
    """Uso opcional si el llamador pide fallo duro ante hallazgo crítico."""

    def __init__(self, axioma_id: str, detalle: str, nodo_info: str) -> None:
        self.axioma_id = axioma_id
        self.detalle = detalle
        self.nodo_info = nodo_info
        super().__init__(
            "\n[PARO ESTRUCTURAL]\n"
            "  -> Regla: {0}\n"
            "  -> Detalle: {1}\n"
            "  -> Contexto: {2}".format(axioma_id, detalle, nodo_info)
        )


# ===============================================================
# SECCIÓN 3 — HELPERS AST
# ===============================================================

def _nombre_callable(nodo: ast.AST) -> Optional[str]:
    if isinstance(nodo, ast.Name):
        return nodo.id
    if isinstance(nodo, ast.Attribute):
        return nodo.attr
    return None


def _contexto_breve(nodo: ast.AST) -> str:
    try:
        return ast.dump(nodo, annotate_fields=False)[:120]
    except Exception:
        return type(nodo).__name__


def _hallazgo(
    *,
    regla_id: str,
    categoria: str,
    severidad: Severidad,
    autoridad: str,
    archivo: str,
    linea: Optional[int],
    razon: str,
    recomendacion: str = "",
    tipo_nodo: Optional[str] = None,
    nombre: Optional[str] = None,
    contexto: Optional[str] = None,
) -> HallazgoDict:
    """Fábrica de hallazgo (sin id; el motor asigna hallazgo_id)."""
    sev = severidad if severidad in _SEVERIDADES else "ERROR"
    return {
        "regla_id": str(regla_id),
        "categoria": str(categoria),
        "severidad": sev,
        "autoridad": str(autoridad),
        "archivo": str(archivo),
        "linea": linea,
        "razon": str(razon),
        "recomendacion": str(recomendacion or ""),
        "tipo_nodo": tipo_nodo,
        "nombre": nombre,
        "contexto": contexto,
    }


# ===============================================================
# SECCIÓN 4 — REGLAS (solo detectan; no registran)
# ===============================================================
#
# Cada regla:
#   - recibe (nodo, ruta)
#   - devuelve HallazgoDict | None
#   - no conoce el motor ni la lista global de evidencia
#
# ===============================================================

def _regla_float(nodo: ast.AST, ruta: str) -> Optional[HallazgoDict]:
    if not isinstance(nodo, ast.Call):
        return None
    nombre = _nombre_callable(nodo.func)
    if nombre != "float":
        return None
    return _hallazgo(
        regla_id="AX-PRECISION-001",
        categoria="precision",
        severidad="ERROR",
        autoridad="AX",
        archivo=ruta,
        linea=getattr(nodo, "lineno", None),
        razon=(
            "Uso de float detectado. "
            "Violación de precisión exacta (piso estructural: Fraction)."
        ),
        recomendacion="Use Fraction en lugar de float.",
        tipo_nodo="Call",
        nombre="float",
        contexto=_contexto_breve(nodo),
    )


def _regla_eval(nodo: ast.AST, ruta: str) -> Optional[HallazgoDict]:
    if not isinstance(nodo, ast.Call):
        return None
    nombre = _nombre_callable(nodo.func)
    if nombre != "eval":
        return None
    return _hallazgo(
        regla_id="AX-SEGURIDAD-001",
        categoria="seguridad",
        severidad="CRITICO",
        autoridad="AX",
        archivo=ruta,
        linea=getattr(nodo, "lineno", None),
        razon="Uso de eval detectado. Ejecución dinámica no permitida.",
        recomendacion="Elimine eval; use rutas explícitas y tipadas.",
        tipo_nodo="Call",
        nombre="eval",
        contexto=_contexto_breve(nodo),
    )


def _regla_exec(nodo: ast.AST, ruta: str) -> Optional[HallazgoDict]:
    if not isinstance(nodo, ast.Call):
        return None
    nombre = _nombre_callable(nodo.func)
    if nombre != "exec":
        return None
    return _hallazgo(
        regla_id="AX-SEGURIDAD-002",
        categoria="seguridad",
        severidad="CRITICO",
        autoridad="AX",
        archivo=ruta,
        linea=getattr(nodo, "lineno", None),
        razon="Uso de exec detectado. Ejecución dinámica no permitida.",
        recomendacion="Elimine exec; use composición explícita de funciones.",
        tipo_nodo="Call",
        nombre="exec",
        contexto=_contexto_breve(nodo),
    )


# ===============================================================
# SECCIÓN 5 — CATÁLOGO DE REGLAS (metadatos + ejecutar)
# ===============================================================

def cargar_reglas() -> List[MetaRegla]:
    """
    Único punto donde se listan las reglas activas.
    Agregar una regla = definir función + una entrada aquí.
    El motor (recorrido) no se modifica.
    """
    return [
        {
            "id": "AX-PRECISION-001",
            "categoria": "precision",
            "autoridad": "AX",
            "descripcion": (
                "Prohibición de float en código de verdad estructural. "
                "Piso: Fraction."
            ),
            "severidad_default": "ERROR",
            "requiere": [],
            "usa_ast": True,
            "usa_axiomas": False,
            "ejecutar": _regla_float,
        },
        {
            "id": "AX-SEGURIDAD-001",
            "categoria": "seguridad",
            "autoridad": "AX",
            "descripcion": "Prohibición de eval.",
            "severidad_default": "CRITICO",
            "requiere": [],
            "usa_ast": True,
            "usa_axiomas": False,
            "ejecutar": _regla_eval,
        },
        {
            "id": "AX-SEGURIDAD-002",
            "categoria": "seguridad",
            "autoridad": "AX",
            "descripcion": "Prohibición de exec.",
            "severidad_default": "CRITICO",
            "requiere": [],
            "usa_ast": True,
            "usa_axiomas": False,
            "ejecutar": _regla_exec,
        },
    ]


def listar_reglas() -> List[Dict[str, Any]]:
    """Metadatos de reglas sin el callable (consultable por VX/Engine)."""
    out: List[Dict[str, Any]] = []
    for r in cargar_reglas():
        out.append({
            "id": r.get("id"),
            "categoria": r.get("categoria"),
            "autoridad": r.get("autoridad"),
            "descripcion": r.get("descripcion"),
            "severidad_default": r.get("severidad_default"),
            "requiere": list(r.get("requiere") or []),
            "usa_ast": bool(r.get("usa_ast", True)),
            "usa_axiomas": bool(r.get("usa_axiomas", False)),
        })
    return out


# ===============================================================
# SECCIÓN 6 — MOTOR (recorrido + registro; no conoce reglas a mano)
# ===============================================================

class _ContadorHallazgos:
    def __init__(self) -> None:
        self._seq = itertools.count(1)

    def next_id(self) -> str:
        return "H-{0:04d}".format(next(self._seq))


def _registrar(
    contador: _ContadorHallazgos,
    hallazgos: List[HallazgoDict],
    bruto: HallazgoDict,
) -> None:
    item: HallazgoDict = dict(bruto)
    item["hallazgo_id"] = contador.next_id()
    hallazgos.append(item)


def _aplicar_reglas_nodo(
    nodo: ast.AST,
    ruta: str,
    reglas: List[MetaRegla],
    contador: _ContadorHallazgos,
    hallazgos: List[HallazgoDict],
) -> None:
    for meta in reglas:
        fn = meta.get("ejecutar")
        if not callable(fn):
            continue
        resultado = fn(nodo, ruta)
        if resultado is None:
            continue
        if isinstance(resultado, dict):
            _registrar(contador, hallazgos, resultado)


def _recorrer_ast(
    arbol: ast.AST,
    ruta: str,
    reglas: List[MetaRegla],
    contador: _ContadorHallazgos,
    hallazgos: List[HallazgoDict],
) -> None:
    for subnodo in ast.walk(arbol):
        _aplicar_reglas_nodo(subnodo, ruta, reglas, contador, hallazgos)


# ===============================================================
# SECCIÓN 7 — AUDITOR ESTRUCTURAL
# ===============================================================

class AuditorEstructural:
    """
    Motor de auditoría estructural (AST → hallazgos).

    No compara axiomas (AX es la autoridad del conocimiento).
    No clasifica choques finales (VX).
    No interpreta, no corrige, no modifica código.
    """

    def ejecutar_barrido_transversal(
        self,
        archivos_codigo: Dict[str, str],
        axiomas_sistema: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Returns
        -------
        estado: "VERIFICADO" | "NO_VERIFICABLE"
        coherente: bool
        hallazgos: list[HallazgoDict]   # con hallazgo_id
        no_verificables: list
        reglas_aplicadas: list[str]     # ids
        catalogo_reglas: list[dict]     # metadatos sin callable
        nota: str
        """
        hallazgos: List[HallazgoDict] = []
        no_verificables: List[Dict[str, Any]] = []
        contador = _ContadorHallazgos()
        reglas = cargar_reglas()
        ids_reglas = [str(r.get("id") or "") for r in reglas]

        if not isinstance(archivos_codigo, dict):
            return {
                "estado": "NO_VERIFICABLE",
                "coherente": False,
                "hallazgos": [],
                "no_verificables": [
                    {
                        "error": "archivos_codigo debe ser dict[str, str]",
                        "tipo": "entrada_invalida",
                    }
                ],
                "reglas_aplicadas": ids_reglas,
                "catalogo_reglas": listar_reglas(),
                "nota": "Entrada inválida: no se pudo iniciar el barrido.",
            }

        for ruta, codigo in archivos_codigo.items():
            if not isinstance(codigo, str):
                no_verificables.append({
                    "archivo": str(ruta),
                    "error": "contenido no es str",
                    "tipo": "entrada_invalida",
                })
                continue
            try:
                arbol = ast.parse(codigo, filename=str(ruta))
            except SyntaxError as e:
                no_verificables.append({
                    "archivo": str(ruta),
                    "error": "Error de sintaxis: {0}".format(e),
                    "tipo": "sintaxis",
                    "linea": getattr(e, "lineno", None),
                })
                continue

            _recorrer_ast(arbol, str(ruta), reglas, contador, hallazgos)

        if no_verificables:
            estado = "NO_VERIFICABLE"
            coherente = False
        else:
            estado = "VERIFICADO"
            coherente = len(hallazgos) == 0

        return {
            "estado": estado,
            "coherente": coherente,
            "hallazgos": hallazgos,
            "no_verificables": no_verificables,
            "reglas_aplicadas": ids_reglas,
            "catalogo_reglas": listar_reglas(),
            "nota": (
                "Hallazgos = evidencia uniforme (hallazgo_id asignado por el motor). "
                "Reglas solo detectan y devuelven; no registran. "
                "Sintaxis inválida → NO_VERIFICABLE, no hallazgo. "
                "VX clasifica choques. AX posee el conocimiento axiomático."
            ),
        }


# Compatibilidad con modules/verificacion/__init__.py
AuditorAxiomatico = AuditorEstructural


# ===============================================================
# SECCIÓN 8 — EXPORTS
# ===============================================================

__all__ = [
    "AuditorEstructural",
    "AuditorAxiomatico",
    "ContradiccionCodigoError",
    "cargar_reglas",
    "listar_reglas",
]
