# ==============================================================
# diagnostics/omega_report.py
# OMEGA REPORT — Renderizador puro (contrato v12+)
# ==============================================================
#
# Principio absoluto:
#   Omega NO pertenece al sistema de razonamiento.
#   Omega es únicamente el renderizador oficial del estado del sistema.
#   Todo el conocimiento vive en Engine.
#
# Regla de oro:
#   Si un dato aparece aquí, Engine debió haberlo entregado.
#   Si no viene → "NO ENTREGADO POR ENGINE"
#
# ==============================================================

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

CURRENT_FILE = Path(__file__).resolve()
DIAGNOSTICS_DIR = CURRENT_FILE.parent
REPO_ROOT = DIAGNOSTICS_DIR.parent

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

VERSION = "12.2-puro"

# Iconografía fija (mismo significado siempre)
ICON_OK = "✅"
ICON_FAIL = "❌"
ICON_PEND = "⚪"
ICON_WARN = "⚠️"
ICON_INFO = "ℹ️"
ICON_READ = "📖"
ICON_CIT = "📎"
ICON_REPO = "🗂"
ICON_MOD = "📦"
ICON_SUB = "👤"
ICON_REJ = "🚫"
ICON_CONTRACT = "📜"
ICON_CAP = "⚙️"
ICON_REPORT = "📋"
ICON_LAYER = "🧩"
ICON_RUN = "▶️"
ICON_STOP = "⛔"
ICON_SKIP = "⏭️"
ICON_DOT = "•"


def _fmt(v: Any) -> str:
    if v is None:
        return "NO ENTREGADO POR ENGINE"
    if isinstance(v, bool):
        return "True" if v else "False"
    s = str(v).strip()
    return s if s else "NO ENTREGADO POR ENGINE"


def _linea_campo(nombre: str, valor: Any, indent: int = 0) -> List[str]:
    """Una línea por campo. Nunca junta muchas cosas."""
    pref = "  " * indent
    if isinstance(valor, dict):
        out = [f"{pref}{nombre}:"]
        for k, v in valor.items():
            out.extend(_linea_campo(str(k), v, indent + 1))
        return out
    if isinstance(valor, list):
        out = [f"{pref}{nombre}:"]
        if not valor:
            out.append(f"{pref}  []")
            return out
        for i, item in enumerate(valor):
            if isinstance(item, dict):
                out.append(f"{pref}  [{i}]")
                for k, v in item.items():
                    out.extend(_linea_campo(str(k), v, indent + 2))
            else:
                out.append(f"{pref}  {ICON_DOT} {_fmt(item)}")
        return out
    return [f"{pref}{nombre}: {_fmt(valor)}"]


def _bloque_seccion(titulo: str, contenido: Any) -> List[str]:
    """Bloque visual limpio para una sección."""
    lineas = [
        "═" * 70,
        f"  {titulo}",
        "═" * 70,
    ]
    if contenido is None:
        lineas.append(f"  {ICON_PEND}  NO ENTREGADO POR ENGINE")
    else:
        if isinstance(contenido, dict):
            for k, v in contenido.items():
                lineas.extend(_linea_campo(str(k), v, indent=1))
        elif isinstance(contenido, list):
            for i, item in enumerate(contenido):
                if isinstance(item, dict):
                    lineas.append(f"  [{i}]")
                    for k, v in item.items():
                        lineas.extend(_linea_campo(str(k), v, indent=2))
                else:
                    lineas.append(f"  {ICON_DOT} {_fmt(item)}")
        else:
            lineas.append(f"  {_fmt(contenido)}")
    lineas.append("")
    return lineas


def renderizar(paquete: Dict[str, Any]) -> str:
    """
    Única función de presentación.
    Recibe el paquete exacto de Engine e imprime.
    No interpreta. No calcula. No completa.
    """
    lineas: List[str] = []

    # Encabezado mínimo (solo versión de Omega; el resto debe venir de Engine)
    lineas += [
        "═" * 70,
        f"{ICON_INFO}  OMEGA REPORT — RENDERIZADOR PURO",
        f"  Versión Omega: {VERSION}",
        "  Omega no crea datos. Solo imprime el paquete entregado por Engine.",
        "═" * 70,
        "",
    ]

    if not isinstance(paquete, dict) or not paquete:
        lineas.append(f"{ICON_PEND}  NO ENTREGADO POR ENGINE")
        lineas.append("")
        return "\n".join(lineas)

    # metadata (si Engine la envía)
    metadata = paquete.get("metadata")
    if metadata is not None:
        lineas.extend(_bloque_seccion(f"{ICON_RUN}  INFORMACIÓN DEL RUN", metadata))

    # reportes: lista ordenada por Engine
    reportes = paquete.get("reportes")
    if isinstance(reportes, list):
        for reporte in reportes:
            if not isinstance(reporte, dict):
                lineas.append(_fmt(reporte))
                lineas.append("")
                continue
            titulo = reporte.get("titulo") or reporte.get("id") or "SECCIÓN"
            contenido = reporte.get("contenido")
            lineas.extend(_bloque_seccion(str(titulo), contenido))
    else:
        # Si Engine no envió lista "reportes", imprimir el resto tal cual
        for clave, valor in paquete.items():
            if clave in ("metadata", "reportes"):
                continue
            lineas.extend(_bloque_seccion(str(clave), valor))

    # Cierre (sin resumen, sin cálculo, sin interpretación)
    lineas += [
        "═" * 70,
        "  CIERRE",
        "═" * 70,
        f"  Versión Omega : {VERSION}",
        "  Todo el contenido mostrado fue entregado por Engine.",
        "  Omega no realizó cálculos.",
        "  Fin del reporte.",
        "═" * 70,
    ]

    return "\n".join(lineas)


def cargar_paquete() -> Dict[str, Any]:
    """
    Única fuente legítima: Engine.paquete_omega()
    Si no existe o falla, se reporta el error estructurado
    sin inventar el resto del contenido.
    """
    try:
        from core.engine import Engine
    except Exception as e:
        return {
            "metadata": {
                "error": f"No se pudo importar Engine: {type(e).__name__}: {e}"
            },
            "reportes": [],
        }

    try:
        eng = Engine(
            raiz_modulos=str(REPO_ROOT / "modules"),
            invocador_id="omega_report",
            strict=False,
        )
    except Exception as e:
        return {
            "metadata": {
                "error": f"Engine no arrancó: {type(e).__name__}: {e}"
            },
            "reportes": [],
        }

    if not hasattr(eng, "paquete_omega"):
        return {
            "metadata": {
                "error": "Engine no expone el método paquete_omega()",
                "estado_engine": getattr(eng, "estado", None),
                "nota": (
                    "Omega no construye el paquete. "
                    "Engine debe implementar paquete_omega()."
                ),
            },
            "reportes": [],
        }

    try:
        paquete = eng.paquete_omega()
    except Exception as e:
        return {
            "metadata": {
                "error": f"Engine.paquete_omega() falló: {type(e).__name__}: {e}"
            },
            "reportes": [],
        }

    if not isinstance(paquete, dict):
        return {
            "metadata": {
                "error": "Engine.paquete_omega() no devolvió dict",
                "tipo_recibido": str(type(paquete)),
            },
            "reportes": [],
        }

    return paquete


def main() -> None:
    paquete = cargar_paquete()
    texto = renderizar(paquete)
    print(texto)

    DIAGNOSTICS_DIR.mkdir(parents=True, exist_ok=True)
    out_json = DIAGNOSTICS_DIR / "omega_report_data.json"
    out_json.write_text(
        json.dumps(paquete, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8",
    )
    print(f"\nJSON: {out_json}")


if __name__ == "__main__":
    main()
