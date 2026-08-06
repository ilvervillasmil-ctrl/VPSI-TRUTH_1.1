# -*- coding: utf-8 -*-
"""
VPSI-TRUTH --- core/engine.py

Nucleo del repositorio.
Integra cada modulo solo a partir de su CONTENEDOR.

Una seccion por modulo.
La seccion de un modulo queda autorizada a:
  - leer su CONTENEDOR
  - leer todos los archivos de su carpeta
  - ejecutar las capacidades que ese CONTENEDOR declara

No inventa oficios.
No sustituye la logica del modulo.
El calculo y el conocimiento viven en cada modulo;
este archivo solo activa lo que cada contrato autoriza.

Seccion presente:
  AX — modules/axiomas
"""

from __future__ import annotations

import importlib.util
import sys
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional

# ===============================================================
# EXCEPCIONES
# ===============================================================
class ArranqueError(Exception):
    pass

# ===============================================================
# ENGINE
# ===============================================================
class Engine:
    VERSION = "12.0"

    def __init__(
        self,
        raiz_modulos: str | Path,
        invocador_id: str = "core",
        strict: bool = True,
    ) -> None:
        self.raiz = Path(raiz_modulos).resolve()
        self.invocador_id = invocador_id
        self.strict = strict
        self.fallos: List[Dict[str, Any]] = []
        self.errores_arranque: List[str] = []
        self.informe_axiomas: Optional[Dict[str, Any]] = None
        self.estado = "NO_INICIADO"

        self._ax_mod = None
        self._ax_meta: Dict[str, Any] = {}
        self._ax_ruta: Optional[Path] = None
        self._ax_caps: Dict[str, Any] = {}
        self._ax_archivos: List[str] = []

        self._ax_cargar()
        self._ax_compuerta()

        if self.errores_arranque:
            self.estado = "RECHAZADO"
            if self.strict:
                raise ArranqueError(
                    "Engine no pudo arrancar:\n  - "
                    + "\n  - ".join(self.errores_arranque)
                )
        else:
            self.estado = "OPERATIVO"

    # ===============================================================
    # SECCIÓN: AX
    # ===============================================================
    #
    # Origen
    #   modules/axiomas/__init__.py
    #
    # CONTENEDOR del modulo
    #   nombre      : axiomas
    #   rol         : AX
    #   version     : 9.5
    #   requiere    : []
    #   capacidades :
    #     verificar
    #     barrer
    #     inventario
    #     axiomas
    #     generatividad
    #
    # El modulo vigila declaraciones
    # (axioma | lema | teorema | corolario | definicion),
    # detecta contradiccion_directa y contradiccion_de_cota,
    # y responde coherente=False si hay choque o error de carga.
    # No calcula Tru_total. No clasifica O de entrada.
    #
    # Esta seccion:
    #   - carga el CONTENEDOR de axiomas
    #   - lee todos los archivos de modules/axiomas/
    #   - ejecuta solo las capacidades del CONTENEDOR
    # ===============================================================

    def _ax_cargar(self) -> None:
        path = self.raiz / "axiomas" / "__init__.py"
        if not path.is_file():
            self.errores_arranque.append(
                "AX: no existe {0}".format(path)
            )
            return

        directorio = path.parent
        nombre_mod = "vpsi_axiomas"
        spec = importlib.util.spec_from_file_location(
            nombre_mod,
            path,
            submodule_search_locations=[str(directorio)],
        )
        if spec is None or spec.loader is None:
            self.errores_arranque.append("AX: no se pudo crear spec")
            return

        mod = importlib.util.module_from_spec(spec)
        sys.modules[nombre_mod] = mod
        try:
            spec.loader.exec_module(mod)
        except Exception as e:
            self.errores_arranque.append(
                "AX: import fallo: {0}: {1}".format(type(e).__name__, e)
            )
            return

        meta = getattr(mod, "CONTENEDOR", None)
        if not isinstance(meta, dict):
            self.errores_arranque.append("AX: sin CONTENEDOR")
            return

        if meta.get("nombre") != "axiomas":
            self.errores_arranque.append(
                "AX: nombre inesperado: {0}".format(meta.get("nombre"))
            )
            return

        if meta.get("rol") != "AX":
            self.errores_arranque.append(
                "AX: rol inesperado: {0}".format(meta.get("rol"))
            )
            return

        caps = meta.get("capacidades")
        if not isinstance(caps, dict) or not caps:
            self.errores_arranque.append("AX: sin capacidades")
            return

        self._ax_mod = mod
        self._ax_meta = dict(meta)
        self._ax_ruta = path
        self._ax_caps = dict(caps)
        self._ax_archivos = sorted(
            str(p.relative_to(directorio))
            for p in directorio.rglob("*")
            if p.is_file()
        )

        for nombre, ref in self._ax_caps.items():
            fn = ref if callable(ref) else getattr(mod, str(ref), None)
            if not callable(fn):
                self.errores_arranque.append(
                    "AX: capacidad no resoluble: {0}".format(nombre)
                )

    def _ax_fn(self, capacidad: str) -> Any:
        if capacidad not in self._ax_caps:
            return None
        ref = self._ax_caps[capacidad]
        if callable(ref):
            return ref
        if self._ax_mod is None:
            return None
        return getattr(self._ax_mod, str(ref), None)

    def _ax_ejecutar(self, capacidad: str, *args: Any, **kwargs: Any) -> Any:
        fn = self._ax_fn(capacidad)
        if not callable(fn):
            self.fallos.append({
                "seccion": "AX",
                "capacidad": capacidad,
                "razon": "no resoluble",
            })
            return None
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            self.fallos.append({
                "seccion": "AX",
                "capacidad": capacidad,
                "razon": "{0}: {1}".format(type(e).__name__, e),
                "traza": traceback.format_exc(limit=3),
            })
            return None

    def ax_barrer(self, declaraciones_externas=None):
        out = self._ax_ejecutar("barrer", declaraciones_externas)
        if isinstance(out, dict):
            self.informe_axiomas = out
            return out
        return None

    def ax_verificar(self, declaraciones_externas=None):
        out = self._ax_ejecutar("verificar", declaraciones_externas)
        if isinstance(out, dict):
            self.informe_axiomas = out
            return out
        return None

    def ax_axiomas(self, declaraciones_externas=None):
        out = self._ax_ejecutar("axiomas", declaraciones_externas)
        return list(out) if isinstance(out, list) else []

    def ax_inventario(self, peticion=None):
        out = self._ax_ejecutar("inventario", peticion)
        if not isinstance(out, dict):
            return None
        out = dict(out)
        out["archivos_modulo"] = list(self._ax_archivos)
        out["archivos_n"] = len(self._ax_archivos)
        out["contrato"] = {
            "nombre": self._ax_meta.get("nombre"),
            "rol": self._ax_meta.get("rol"),
            "version": self._ax_meta.get("version"),
            "requiere": list(self._ax_meta.get("requiere") or []),
            "capacidades": sorted(self._ax_caps.keys()),
        }
        return out

    def ax_generatividad(self):
        out = self._ax_ejecutar("generatividad")
        return out if isinstance(out, dict) else None

    def ax_archivos(self):
        return list(self._ax_archivos)

    def _ax_compuerta(self) -> None:
        if self._ax_mod is None:
            if not any(e.startswith("AX:") for e in self.errores_arranque):
                self.errores_arranque.append("AX: modulo no cargado")
            return

        if not self._ax_archivos:
            self.errores_arranque.append("AX: carpeta sin archivos")

        informe = self.ax_barrer()
        if informe is None:
            informe = self.ax_verificar()

        if informe is None:
            self.errores_arranque.append("AX: barrer/verificar no resolvio")
            return

        self.informe_axiomas = informe
        if not informe.get("coherente", False):
            self.errores_arranque.append(
                "AX: incoherente choques={0} errores={1}".format(
                    len(informe.get("choques") or []),
                    len(informe.get("errores") or []),
                )
            )

    # ===============================================================
    # FIN SECCIÓN: AX
    # ===============================================================
