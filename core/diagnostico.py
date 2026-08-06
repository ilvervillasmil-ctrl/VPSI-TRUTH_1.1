# ==============================================================
# INICIO: core/diagnostico.py — observador mínimo definitivo
# ==============================================================

"""
core/diagnostico.py
===================
Observador puro del estado global construido por el Engine.

No reconstruye información.
No conoce la estructura interna del Engine.
No calcula.
No decide.
Solo observa y presenta.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple


class DiagnosticoError(Exception):
    """Error de forma de entrada del observador."""


class DiagnosticoGlobal:
    """Observador mínimo. Toda la inteligencia estructural reside en el Engine."""

    @staticmethod
    def censo(engine: Any, **kwargs: Any) -> Dict[str, Any]:
        """
        Devuelve el estado global tal como lo construyó el Engine.
        Solo añade timestamp de observación.
        """
        if engine is None:
            raise DiagnosticoError("engine es obligatorio")

        if not hasattr(engine, "estado_global"):
            raise DiagnosticoError(
                "El Engine no expone estado_global(). "
                "La autoridad estructural debe residir en el Engine."
            )

        estado = engine.estado_global()
        if not isinstance(estado, dict):
            raise DiagnosticoError("estado_global() debe devolver un dict")

        # Única intervención del observador: registrar cuándo se observó
        estado = dict(estado)
        estado["timestamp_observacion"] = datetime.now(timezone.utc).isoformat()
        return estado

    @staticmethod
    def presentar(informe: Dict[str, Any]) -> str:
        """Presentación textual del estado recibido del Engine."""
        if not isinstance(informe, dict):
            return "[DG] informe inválido"

        lineas: List[str] = [
            "=" * 80,
            "DIAGNÓSTICO GLOBAL (observador mínimo)",
            "=" * 80,
            f"  timestamp_observacion : {informe.get('timestamp_observacion')}",
            f"  version_engine        : {informe.get('version_engine')}",
            f"  estado                : {informe.get('estado')}",
            f"  total_contenedores    : {informe.get('total_contenedores')}",
            f"  roles                 : {list((informe.get('roles') or {}).keys())}",
            f"  rechazados            : {len(informe.get('rechazados') or [])}",
            "",
            f"  nota: {informe.get('nota')}",
            "=" * 80,
        ]

        errores = informe.get("errores_arranque") or []
        if errores:
            lineas.append("")
            lineas.append("  Errores de arranque (fuente Engine):")
            for i, err in enumerate(errores[:15], 1):
                lineas.append(f"    {i}. {err}")
            if len(errores) > 15:
                lineas.append(f"    … y {len(errores) - 15} más")

        return "\n".join(lineas)

    @staticmethod
    def censo_y_texto(engine: Any, **kwargs: Any) -> Tuple[Dict[str, Any], str]:
        inf = DiagnosticoGlobal.censo(engine, **kwargs)
        return inf, DiagnosticoGlobal.presentar(inf)


def barrer_diagnostico(engine: Any, **kwargs: Any) -> Dict[str, Any]:
    return DiagnosticoGlobal.censo(engine, **kwargs)


__all__ = [
    "DiagnosticoGlobal",
    "DiagnosticoError",
    "barrer_diagnostico",
]

# ==============================================================
# FIN: core/diagnostico.py — observador mínimo definitivo
# (Pegue aquí cualquier código nuevo que se agregue en el futuro)
# ==============================================================
