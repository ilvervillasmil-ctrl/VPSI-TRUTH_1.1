# -*- coding: utf-8 -*-
"""
VPSI-TRUTH --- core/engine.py
Version 12.0

Seccion activa: AX (modules/axiomas)
El rol se toma del CONTENEDOR del modulo.
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
        self.meta = dict(meta)

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
        self.ax_archivos_lista: List[str] = []
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
    # Autoridad del CONTENEDOR vivo del modulo (no una copia ciega).
    # Lee todos los archivos bajo modules/axiomas/.
    # Ejecuta solo capacidades declaradas y resolubles.
    # ===============================================================

    # ---------------------------------------------------------------
    # subsección: carga del modulo + contraste con CONTENEDOR vivo
    # ---------------------------------------------------------------
    def _ax_cargar_modulo(self) -> None:
        path = self.raiz / "axiomas" / "__init__.py"
        if not path.is_file():
            self.errores_arranque.append("AX: no existe {0}".format(path))
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
        requiere = list(meta.get("requiere") or [])
        caps_meta = meta.get("capacidades")

        if nombre != "axiomas":
            self.errores_arranque.append(
                "AX: nombre CONTENEDOR inesperado: {0}".format(nombre)
            )
            return

        if rol != "AX":
            self.errores_arranque.append(
                "AX: rol CONTENEDOR inesperado: {0}".format(rol)
            )
            return

        if not isinstance(caps_meta, dict) or not caps_meta:
            self.errores_arranque.append(
                "AX: CONTENEDOR sin capacidades dict"
            )
            return

        cont = Contenedor(
            nombre=str(nombre),
            rol=str(rol),
            version=version,
            modulo=mod,
            ruta=path,
            meta=meta,
        )
        self.ax_contenedor = cont

        # Capacidades del CONTENEDOR vivo: deben ser resolubles
        no_resolubles = [
            str(k) for k in caps_meta.keys() if not cont.tiene(str(k))
        ]
        if no_resolubles:
            self.errores_arranque.append(
                "AX/{0}: capacidades no resolubles: {1}".format(
                    cont.nombre, no_resolubles
                )
            )

        # Inventario total de archivos de la carpeta
        self.ax_archivos_lista = self._ax_archivos()

        # Constancia de version / requiere del CONTENEDOR vivo
        cont.version = version
        cont.requiere = requiere

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

    def ax_archivos(self) -> List[str]:
        """Inventario publico: todos los archivos de modules/axiomas/."""
        if self.ax_archivos_lista:
            return list(self.ax_archivos_lista)
        lista = self._ax_archivos()
        self.ax_archivos_lista = lista
        return list(lista)

    # ---------------------------------------------------------------
    # subsección: invocacion por contrato vivo
    # ---------------------------------------------------------------
    def _ax_capacidad(self, capacidad: str, *args: Any, **kwargs: Any) -> Any:
        cont = self._ax_contenedor()
        if cont is None:
            self.fallos.append({
                "seccion": "AX",
                "capacidad": capacidad,
                "razon": "modulo axiomas no cargado",
            })
            return None

        # Autoridad: solo lo declarado en el CONTENEDOR vivo
        if capacidad not in cont.capacidades:
            self.fallos.append({
                "seccion": "AX",
                "capacidad": capacidad,
                "razon": "capacidad fuera del CONTENEDOR vivo de axiomas",
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
            # Anexa inventario de archivos que Angie leyo
            out = dict(out)
            out["archivos_modulo"] = self.ax_archivos()
            out["archivos_n"] = len(out["archivos_modulo"])
            cont = self._ax_contenedor()
            if cont is not None:
                out["contrato_vivo"] = {
                    "nombre": cont.nombre,
                    "rol": cont.rol,
                    "version": cont.version,
                    "requiere": list(cont.requiere),
                    "capacidades": sorted(str(k) for k in cont.capacidades.keys()),
                }
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
            if not any("AX:" in e for e in self.errores_arranque):
                self.errores_arranque.append(
                    "AX: falta contenedor (modules/axiomas)"
                )
            return

        archivos = self.ax_archivos()
        if not archivos:
            self.errores_arranque.append(
                "AX/{0}: carpeta sin archivos legibles".format(cont.nombre)
            )

        # version / requiere del CONTENEDOR vivo quedan en cont
        # capacidades ya validadas en _ax_cargar_modulo

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
