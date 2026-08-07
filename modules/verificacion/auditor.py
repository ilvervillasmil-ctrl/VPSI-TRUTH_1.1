# ===============================================================
# VPSI-TRUTH — modules/verificacion/auditor.py
# ===============================================================
#
# Auditor estructural sobre representación AST.
#
# Oficio único:
#   Analizar una representación (AST) y producir evidencia.
#   No interpreta intención.
#   No calcula métricas.
#   No modifica el código.
#
# Flujo:
#   AST
#    ↓
#   recorrido
#    ↓
#   conjunto de reglas
#    ↓
#   hallazgos (evidencia uniforme)
#    ↓
#   VX clasifica / reporta
#
# Sintaxis inválida ≠ violación axiomática.
#   Error de sintaxis → estado NO_VERIFICABLE
#   Reglas ejecutadas  → coherente True/False + hallazgos
#
# ===============================================================

from __future__ import annotations

import ast
from typing import Any, Callable, Dict, List, Optional


# ===============================================================
# SECCIÓN 1 — TIPOS Y CONSTANTES
# ===============================================================

Severidad = str  # INFO | ADVERTENCIA | ERROR | CRITICO

_SEVERIDADES_VALIDAS = ("INFO", "ADVERTENCIA", "ERROR", "CRITICO")


# ===============================================================
# SECCIÓN 2 — EXCEPCIÓN (paro explícito, uso opcional)
# ===============================================================

class ContradiccionCodigoError(Exception):
    """
    Lanzado solo si el llamador pide fallo duro ante un hallazgo crítico.
    El barrido normal no lanza: devuelve evidencia.
    """

    def __init__(self, axioma_id: str, detalle: str, nodo_info: str) -> None:
        self.axioma_id = axioma_id
        self.detalle = detalle
        self.nodo_info = nodo_info
        super().__init__(
            "\n[PARO AXIOMÁTICO]\n"
            "  -> Axioma/Regla: {0}\n"
            "  -> Contradicción: {1}\n"
            "  -> Contexto de Código: {2}".format(axioma_id, detalle, nodo_info)
        )


# ===============================================================
# SECCIÓN 3 — REGISTRO ÚNICO DE EVIDENCIA
# ===============================================================

def _registrar_hallazgo(
    hallazgos: List[Dict[str, Any]],
    *,
    regla_id: str,
    categoria: str,
    severidad: Severidad,
    archivo: str,
    linea: Optional[int],
    razon: str,
    tipo_nodo: Optional[str] = None,
    nombre: Optional[str] = None,
    contexto: Optional[str] = None,
) -> None:
    """
    Única vía para construir evidencia.
    Todas las reglas generan exactamente la misma estructura.
    """
    sev = severidad if severidad in _SEVERIDADES_VALIDAS else "ERROR"
    hallazgos.append({
        "regla_id": str(regla_id),
        "categoria": str(categoria),
        "severidad": sev,
        "archivo": str(archivo),
        "linea": linea,
        "razon": str(razon),
        "tipo_nodo": tipo_nodo,
        "nombre": nombre,
        "contexto": contexto,
    })


# ===============================================================
# SECCIÓN 4 — CONTEXTO AST (ayuda a reportes futuros)
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


# ===============================================================
# SECCIÓN 5 — REGLAS INDEPENDIENTES
# ===============================================================
#
# Cada regla:
#   - recibe (subnodo, ruta, hallazgos)
#   - decide si aplica
#   - registra evidencia vía _registrar_hallazgo
#   - no interpreta, no corrige, no modifica
#
# Identificadores alineables a AX (ej. AX-PRECISION-001).
# ===============================================================

def regla_float(
    nodo: ast.AST,
    ruta: str,
    hallazgos: List[Dict[str, Any]],
) -> None:
    """
    AX-PRECISION-001 — Prohibición de float en código de verdad estructural.
    Piso estructural: Fraction.
    """
    if not isinstance(nodo, ast.Call):
        return
    nombre = _nombre_callable(nodo.func)
    if nombre != "float":
        return
    _registrar_hallazgo(
        hallazgos,
        regla_id="AX-PRECISION-001",
        categoria="precision",
        severidad="ERROR",
        archivo=ruta,
        linea=getattr(nodo, "lineno", None),
        razon=(
            "Uso de float detectado. "
            "Violación de precisión exacta (piso estructural: Fraction)."
        ),
        tipo_nodo="Call",
        nombre="float",
        contexto=_contexto_breve(nodo),
    )


def regla_eval(
    nodo: ast.AST,
    ruta: str,
    hallazgos: List[Dict[str, Any]],
) -> None:
    """AX-SEGURIDAD-001 — Prohibición de eval."""
    if not isinstance(nodo, ast.Call):
        return
    nombre = _nombre_callable(nodo.func)
    if nombre != "eval":
        return
    _registrar_hallazgo(
        hallazgos,
        regla_id="AX-SEGURIDAD-001",
        categoria="seguridad",
        severidad="CRITICO",
        archivo=ruta,
        linea=getattr(nodo, "lineno", None),
        razon="Uso de eval detectado. Ejecución dinámica no permitida.",
        tipo_nodo="Call",
        nombre="eval",
        contexto=_contexto_breve(nodo),
    )


def regla_exec(
    nodo: ast.AST,
    ruta: str,
    hallazgos: List[Dict[str, Any]],
) -> None:
    """AX-SEGURIDAD-002 — Prohibición de exec."""
    if not isinstance(nodo, ast.Call):
        return
    nombre = _nombre_callable(nodo.func)
    if nombre != "exec":
        return
    _registrar_hallazgo(
        hallazgos,
        regla_id="AX-SEGURIDAD-002",
        categoria="seguridad",
        severidad="CRITICO",
        archivo=ruta,
        linea=getattr(nodo, "lineno", None),
        razon="Uso de exec detectado. Ejecución dinámica no permitida.",
        tipo_nodo="Call",
        nombre="exec",
        contexto=_contexto_breve(nodo),
    )


# Conjunto activo de reglas (activar/desactivar sin tocar el recorrido).
_REGLAS: List[Callable[[ast.AST, str, List[Dict[str, Any]]], None]] = [
    regla_float,
    regla_eval,
    regla_exec,
]


# ===============================================================
# SECCIÓN 6 — MOTOR: RECORRIDO + APLICACIÓN DE REGLAS
# ===============================================================

def _aplicar_reglas(
    nodo: ast.AST,
    ruta: str,
    hallazgos: List[Dict[str, Any]],
) -> None:
    for regla in _REGLAS:
        regla(nodo, ruta, hallazgos)


def _recorrer_ast(
    arbol: ast.AST,
    ruta: str,
    hallazgos: List[Dict[str, Any]],
) -> None:
    for subnodo in ast.walk(arbol):
        _aplicar_reglas(subnodo, ruta, hallazgos)


# ===============================================================
# SECCIÓN 7 — AUDITOR
# ===============================================================

class AuditorAxiomatico:
    """
    Analiza AST del código fuente y produce hallazgos uniformes.

    No clasifica choques estructurales finales (eso es VX).
    No interpreta intención.
    No calcula Tru / C / L / K.
    No modifica el código.
    """

    def ejecutar_barrido_transversal(
        self,
        archivos_codigo: Dict[str, str],
        axiomas_sistema: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Barrido transversal.

        Returns
        -------
        dict
            estado: "VERIFICADO" | "NO_VERIFICABLE"
            coherente: bool
            hallazgos: list[dict]   # evidencia uniforme
            no_verificables: list   # sintaxis u otros bloqueos de análisis
            reglas_aplicadas: list[str]
            nota: str

        axiomas_sistema se acepta por firma (Engine / VX pueden inyectar
        contexto); las reglas actuales son estructurales y no dependen
        aún de ese diccionario.
        """
        hallazgos: List[Dict[str, Any]] = []
        no_verificables: List[Dict[str, Any]] = []

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
                "reglas_aplicadas": [r.__name__ for r in _REGLAS],
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
                # Sintaxis inválida ≠ violación axiomática.
                no_verificables.append({
                    "archivo": str(ruta),
                    "error": "Error de sintaxis: {0}".format(e),
                    "tipo": "sintaxis",
                    "linea": getattr(e, "lineno", None),
                })
                continue

            _recorrer_ast(arbol, str(ruta), hallazgos)

        if no_verificables and not hallazgos:
            # Hubo bloqueo de análisis y ninguna regla llegó a correr
            # sobre esos archivos fallidos.
            estado = "NO_VERIFICABLE"
            coherente = False
        elif no_verificables and hallazgos:
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
            "reglas_aplicadas": [r.__name__ for r in _REGLAS],
            "nota": (
                "Hallazgos = evidencia uniforme de reglas AST. "
                "VX clasifica choques estructurales. "
                "Sintaxis inválida se reporta como NO_VERIFICABLE, "
                "no como hallazgo axiomático."
            ),
        }


# ===============================================================
# SECCIÓN 8 — EXPORTS
# ===============================================================

__all__ = [
    "AuditorAxiomatico",
    "ContradiccionCodigoError",
]
