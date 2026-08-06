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

from __future__ import annotations

import importlib.util
import sys
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class ArranqueError(Exception):
    pass


ROLES: Tuple[str, ...] = (
    "CT", "AX", "FO", "MC", "SF", "DG", "CA", "CX", "DI",
    "RE", "VX", "TX", "CH", "CIT", "UI", "GL", "TT", "CC", "CE",
)


class Contenedor:
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


class Registro:
    def __init__(self) -> None:
        self.contenedores: Dict[str, Contenedor] = {}
        self.por_rol: Dict[str, List[Contenedor]] = {r: [] for r in ROLES}
        self.rechazados: List[Dict[str, Any]] = []

    def registrar(self, cont: Contenedor) -> None:
        if cont.nombre in self.contenedores:
            return
        self.contenedores[cont.nombre] = cont
        if cont.rol in self.por_rol:
            self.por_rol[cont.rol].append(cont)

    def primero(self, rol: str) -> Optional[Contenedor]:
        lista = self.por_rol.get(rol) or []
        return lista[0] if lista else None


class Engine:
    """Orquestador por secciones de contrato. Seccion AX activa."""

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
        self.registro = Registro()
        self.fallos: List[Dict[str, Any]] = []
        self.errores_arranque: List[str] = []
        self.informe_axiomas: Optional[Dict[str, Any]] = None
        self.estado = "NO_INICIADO"

        self._descubrir()
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

    def _descubrir(self) -> None:
        if not self.raiz.exists():
            self.errores_arranque.append(
                "Raiz de modulos no existe: {0}".format(self.raiz)
            )
            return
        for path in sorted(self.raiz.rglob("__init__.py")):
            try:
                rel = path.relative_to(self.raiz)
            except ValueError:
                continue
            if len(rel.parts) != 2:
                continue
            cont = self._cargar_modulo(path)
            if cont is not None:
                self.registro.registrar(cont)

    def _cargar_modulo(self, path: Path) -> Optional[Contenedor]:
        directorio = path.parent
        nombre_mod = "vpsi_{0}".format(directorio.name)
        spec = importlib.util.spec_from_file_location(
            nombre_mod,
            path,
            submodule_search_locations=[str(directorio)],
        )
        if spec is None or spec.loader is None:
            return None
        mod = importlib.util.module_from_spec(spec)
        sys.modules[nombre_mod] = mod
        try:
            spec.loader.exec_module(mod)
        except Exception as e:
            self.registro.rechazados.append({
                "ruta": str(path),
                "razon": "{0}: {1}".format(type(e).__name__, e),
            })
            return None
        meta = getattr(mod, "CONTENEDOR", None)
        if not isinstance(meta, dict):
            return None
        nombre = meta.get("nombre")
        rol = meta.get("rol")
        if not nombre or not rol or rol not in ROLES:
            return None
        return Contenedor(
            nombre=str(nombre),
            rol=str(rol),
            version=str(meta.get("version", "0.0")),
            modulo=mod,
            ruta=path,
            meta=meta,
        )

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
    # rol             : AX
    # version         : 9.5
    # requiere        : []
    # capacidades     : verificar, barrer, inventario, axiomas, generatividad
    #
    # Autoridad de engine sobre este modulo:
    #   - Lee el CONTENEDOR de modules/axiomas/
    #   - Lee absolutamente TODOS los archivos bajo modules/axiomas/
    #   - Ejecuta todas las capacidades que el CONTENEDOR declara
    #   - No inventa oficios. No sustituye la logica del modulo.
    #   - No calcula Tru_total. No clasifica O de entrada.
    #
    # Prueba:
    #   Esta seccion se valida directamente contra modules/axiomas/
    #
    # ---------------------------------------------------------------
    # subsección: metadatos del contrato
    # ---------------------------------------------------------------
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
    # subsección: contenedor
    # ---------------------------------------------------------------
    def _ax_contenedor(self) -> Optional[Contenedor]:
        return self.registro.primero("AX")

    # ---------------------------------------------------------------
    # subsección: todos los archivos del modulo
    # ---------------------------------------------------------------
    def _ax_archivos(self) -> List[str]:
        """
        Lee absolutamente TODOS los archivos bajo modules/axiomas/.
        Autoridad total de Angie sobre el contenido de la carpeta.
        """
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
        """
        Ejecuta una capacidad declarada en el CONTENEDOR de axiomas.
        Solo lo que el contrato autoriza.
        """
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
                "razon": "rol AX sin contenedor cargado",
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
        """CONTENEDOR.capacidades['barrer'] → barrer()"""
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
        """CONTENEDOR.capacidades['verificar'] → barrer()"""
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
        """CONTENEDOR.capacidades['axiomas'] → axiomas()"""
        out = self._ax_capacidad("axiomas", declaraciones_externas)
        if isinstance(out, list):
            return out
        return []

    # ---------------------------------------------------------------
    # subsección: capacidad — inventario
    # ---------------------------------------------------------------
    def ax_inventario(self, peticion: Any = None) -> Optional[Dict[str, Any]]:
        """CONTENEDOR.capacidades['inventario'] → inventario()"""
        out = self._ax_capacidad("inventario", peticion)
        if isinstance(out, dict):
            return out
        return None

    # ---------------------------------------------------------------
    # subsección: capacidad — generatividad
    # ---------------------------------------------------------------
    def ax_generatividad(self) -> Optional[Dict[str, Any]]:
        """CONTENEDOR.capacidades['generatividad'] → generatividad()"""
        out = self._ax_capacidad("generatividad")
        if isinstance(out, dict):
            return out
        return None

    # ---------------------------------------------------------------
    # subsección: compuerta de arranque
    # ---------------------------------------------------------------
    def _ax_compuerta(self) -> None:
        """
        Arranque AX contra modules/axiomas/:
          1. Contenedor presente.
          2. Archivos de la carpeta legibles.
          3. barrer/verificar resuelve.
          4. coherente=True (fail-closed del modulo).
        """
        cont = self._ax_contenedor()
        if cont is None:
            self.errores_arranque.append(
                "AX: falta contenedor obligatorio (modules/axiomas)"
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
