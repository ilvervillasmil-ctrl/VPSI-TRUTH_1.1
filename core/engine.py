# -*- coding: utf-8 -*-
"""
VPSI-TRUTH --- core/engine.py
Version 12.0

Descripcion
  El Engine es el nucleo del repositorio. Integra los modulos del sistema
  a partir de los contratos que cada uno declara en su CONTENEDOR.

  Estructura
    Una seccion del Engine por modulo/rol.
    Cada seccion se construye desde el __init__ y el CONTENEDOR de ese modulo.
    La seccion queda autorizada a todo lo que ese modulo declara y contiene.
    El contrato de la seccion es el contrato del modulo.

  Que hace
    - Descubre cada carpeta de modulo y lee su __init__.
    - Registra el CONTENEDOR (rol, capacidades, requiere, version).
    - Conecta las capacidades declaradas.
    - Calcula e invoca mediante esas capacidades: lo que el modulo permite,
      el Engine lo puede usar (C, L, K, Tru, marco, mandatos, etc.).
    - No inventa oficios fuera del contrato.
    - No sustituye la logica interna del modulo: la ejecuta por contrato.

  Principio
    El conocimiento y la logica viven en cada modulo.
    El Engine activa lo que cada contrato autoriza.
    Nuevos modulos o roles = nuevas secciones, sin reescribir el resto.
"""

# -*- coding: utf-8 -*-
"""
VPSI-TRUTH --- core/engine.py
Version 12.0

Seccion activa: AX (modules/axiomas)
El rol se toma del CONTENEDOR del modulo, no de una lista inventada aqui.
"""

from __future__ import annotations

import importlib.util
import sys
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional


class ArranqueError(Exception):
    pass


class Contenedor:
    """Contenedor leido desde el CONTENEDOR del modulo."""

    def __init__(
        self,
        nombre: str,
        rol: str,
        version: str,
        modulo: Any,
        ruta: Path,
        meta: Dict[str, Any],
    ) -> None:
        self.nombre = nombre
        self.rol = rol
        self.version = version
        self.modulo = modulo
        self.ruta = ruta
        self.requiere = list(meta.get("requiere") or [])
        self.descripcion = str(meta.get("descripcion") or "")
        raw = meta.get("capacidades") or {}
        self.capacidades = dict(raw) if isinstance(raw, dict) else {}

    def fn(self, nombre: str) -> Any:
        ref = self.capacidades.get(nombre)
        if ref is None:
            return None
        if callable(ref):
            return ref
        if isinstance(ref, str):
            return getattr(self.modulo, ref, None)
        return None

    def tiene(self, nombre: str) -> bool:
        return callable(self.fn(nombre))


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
        self.ax_contenedor: Optional[Contenedor] = None
        self.estado = "NO_INICIADO"

        self._ax_cargar_modulo()
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

    def _ejecutar_capacidad(
        self,
        cont: Contenedor,
        capacidad: str,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        fn = cont.fn(capacidad)
        if not callable(fn):
            self.fallos.append({
                "contenedor": cont.nombre,
                "capacidad": capacidad,
                "razon": "no callable",
            })
            return None
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            self.fallos.append({
                "contenedor": cont.nombre,
                "capacidad": capacidad,
                "razon": "{0}: {1}".format(type(e).__name__, e),
                "traza": traceback.format_exc(limit=3),
            })
            return None

    # ===============================================================
    # SECCIÓN: AX
    # ===============================================================
    #
    # Contrato origen : modules/axiomas/__init__.py
    # nombre          : axiomas
    # rol             : AX   ← solo este rol, el del propio modulo
    # version         : 9.5
    # requiere        : []
    # capacidades     : verificar, barrer, inventario, axiomas, generatividad
    #
    # Autoridad:
    #   - Lee el CONTENEDOR de modules/axiomas/
    #   - Lee absolutamente TODOS los archivos bajo modules/axiomas/
    #   - Ejecuta todas las capacidades que el CONTENEDOR declara
    #   - Acepta el rol que el CONTENEDOR declara (AX)
    #   - No inventa oficios. No sustituye la logica del modulo.
    #
    # Prueba: contra modules/axiomas/
    # ===============================================================

    AX_CONTRATO = {
        "nombre": "axiomas",
        "rol": "AX",
        "version": "9.5",
        "requiere": [],
        "capacidades": (
            "verificar",
            "barrer",
            "inventario",
            "axiomas",
            "generatividad",
        ),
        "carpeta": "modules/axiomas",
    }

    # ---------------------------------------------------------------
    # subsección: carga del modulo (solo axiomas / rol AX)
    # ---------------------------------------------------------------
    def _ax_cargar_modulo(self) -> None:
        """
        Carga modules/axiomas/__init__.py.
        El rol aceptado es el que trae el CONTENEDOR del archivo (AX).
        """
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
            self.errores_arranque.append("AX: sin CONTENEDOR dict")
            return

        nombre = meta.get("nombre")
        rol = meta.get("rol")
        version = str(meta.get("version", "0.0"))

        if nombre != self.AX_CONTRATO["nombre"]:
            self.errores_arranque.append(
                "AX: nombre CONTENEDOR inesperado: {0}".format(nombre)
            )
            return

        # Solo se acepta el rol que declara ESTE modulo
        if rol != self.AX_CONTRATO["rol"]:
            self.errores_arranque.append(
                "AX: rol CONTENEDOR inesperado: {0}".format(rol)
            )
            return

        self.ax_contenedor = Contenedor(
            nombre=str(nombre),
            rol=str(rol),
            version=version,
            modulo=mod,
            ruta=path,
            meta=meta,
        )

    # ---------------------------------------------------------------
    # subsección: contenedor
    # ---------------------------------------------------------------
    def _ax_contenedor(self) -> Optional[Contenedor]:
        return self.ax_contenedor

    # ---------------------------------------------------------------
    # subsección: todos los archivos del modulo
    # ---------------------------------------------------------------
    def _ax_archivos(self) -> List[str]:
        """Lee absolutamente TODOS los archivos bajo modules/axiomas/."""
        cont = self._ax_contenedor()
        if cont is None:
            return []
        dir_mod = Path(cont.ruta).resolve().parent
        return sorted(
            str(p.relative_to(dir_mod))
            for p in dir_mod.rglob("*")
            if p.is_file()
        )

    # ---------------------------------------------------------------
    # subsección: invocacion por contrato
    # ---------------------------------------------------------------
    def _ax_capacidad(self, capacidad: str, *args: Any, **kwargs: Any) -> Any:
        if capacidad not in self.AX_CONTRATO["capacidades"]:
            self.fallos.append({
                "seccion": "AX",
                "capacidad": capacidad,
                "razon": "capacidad fuera del CONTENEDOR de axiomas",
            })
            return None

        cont = self._ax_contenedor()
        if cont is None:
            self.fallos.append({
                "seccion": "AX",
                "capacidad": capacidad,
                "razon": "modulo axiomas no cargado",
            })
            return None

        if not cont.tiene(capacidad):
            self.fallos.append({
                "seccion": "AX",
                "contenedor": cont.nombre,
                "capacidad": capacidad,
                "razon": "capacidad no resoluble en el modulo",
            })
            return None

        return self._ejecutar_capacidad(cont, capacidad, *args, **kwargs)

    # ---------------------------------------------------------------
    # subsección: capacidad — barrer
    # ---------------------------------------------------------------
    def ax_barrer(
        self,
        declaraciones_externas: Optional[Dict[str, List[Dict]]] = None,
    ) -> Optional[Dict[str, Any]]:
        out = self._ax_capacidad("barrer", declaraciones_externas)
        if isinstance(out, dict):
            self.informe_axiomas = out
            return out
        return None

    # ---------------------------------------------------------------
    # subsección: capacidad — verificar
    # ---------------------------------------------------------------
    def ax_verificar(
        self,
        declaraciones_externas: Optional[Dict[str, List[Dict]]] = None,
    ) -> Optional[Dict[str, Any]]:
        out = self._ax_capacidad("verificar", declaraciones_externas)
        if isinstance(out, dict):
            self.informe_axiomas = out
            return out
        return None

    # ---------------------------------------------------------------
    # subsección: capacidad — axiomas
    # ---------------------------------------------------------------
    def ax_axiomas(
        self,
        declaraciones_externas: Optional[Dict[str, List[Dict]]] = None,
    ) -> List[Dict[str, Any]]:
        out = self._ax_capacidad("axiomas", declaraciones_externas)
        if isinstance(out, list):
            return out
        return []

    # ---------------------------------------------------------------
    # subsección: capacidad — inventario
    # ---------------------------------------------------------------
    def ax_inventario(self, peticion: Any = None) -> Optional[Dict[str, Any]]:
        out = self._ax_capacidad("inventario", peticion)
        if isinstance(out, dict):
            return out
        return None

    # ---------------------------------------------------------------
    # subsección: capacidad — generatividad
    # ---------------------------------------------------------------
    def ax_generatividad(self) -> Optional[Dict[str, Any]]:
        out = self._ax_capacidad("generatividad")
        if isinstance(out, dict):
            return out
        return None

    # ---------------------------------------------------------------
    # subsección: compuerta de arranque
    # ---------------------------------------------------------------
    def _ax_compuerta(self) -> None:
        cont = self._ax_contenedor()
        if cont is None:
            self.errores_arranque.append(
                "AX: falta contenedor (modules/axiomas)"
            )
            return

        archivos = self._ax_archivos()
        if not archivos:
            self.errores_arranque.append(
                "AX/{0}: carpeta sin archivos legibles".format(cont.nombre)
            )

        informe = self.ax_barrer()
        if informe is None:
            informe = self.ax_verificar()

        if informe is None:
            self.errores_arranque.append(
                "AX/{0}: barrer/verificar no resolvio".format(cont.nombre)
            )
            return

        self.informe_axiomas = informe

        if not informe.get("coherente", False):
            self.errores_arranque.append(
                "AX/{0}: incoherente choques={1} errores={2}".format(
                    cont.nombre,
                    len(informe.get("choques") or []),
                    len(informe.get("errores") or []),
                )
            )

    # ===============================================================
    # FIN SECCIÓN: AX
    # ===============================================================
