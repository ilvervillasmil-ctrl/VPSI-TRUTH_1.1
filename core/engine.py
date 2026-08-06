# -*- coding: utf-8 -*-
"""
VPSI-TRUTH --- core/engine.py
Version 12.0

Seccion activa: AX — modules/axiomas/__init__.py (CONTENEDOR v9.5)
Rol solo el del modulo: AX.
Autoridad: CONTENEDOR vivo + todos los archivos de la carpeta.
"""

from __future__ import annotations

import importlib.util
import sys
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


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

        # Instancia del modulo AX (nombre distinto al metodo)
        self._ax_cont: Optional[Contenedor] = None
        self._ax_archivos_lista: List[str] = []
        self._ax_reporte_capacidades: List[Dict[str, Any]] = []

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
                "seccion": "AX",
                "contenedor": cont.nombre,
                "capacidad": capacidad,
                "razon": "no callable",
            })
            return None
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            self.fallos.append({
                "seccion": "AX",
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
    # Contrato vivo: modules/axiomas/__init__.py → CONTENEDOR
    #   nombre      : axiomas
    #   rol         : AX
    #   version     : 9.5
    #   requiere    : []
    #   capacidades : verificar, barrer, inventario, axiomas, generatividad
    #
    # AX es el juez del grafo (segun el propio modulo).
    # Engine no reimplementa contradicciones ni recolectar:
    # ejecuta lo que el CONTENEDOR declara y valida el enlace
    # nombre → implementacion callable del modulo.
    #
    # ===============================================================

    # ---------------------------------------------------------------
    # subsección: validacion detallada de cada capacidad del contrato
    # ---------------------------------------------------------------
    def _ax_validar_capacidades(
        self,
        cont: Contenedor,
    ) -> List[Dict[str, Any]]:
        """
        Por cada entrada de CONTENEDOR['capacidades']:
          - existe en el dict del contrato
          - el valor es callable o nombre de atributo del modulo
          - el resolvido final es callable
          - si es callable directo, opcionalmente coincide con
            atributo homonimo del modulo cuando exista
        """
        reporte: List[Dict[str, Any]] = []
        mod = cont.modulo

        for nombre_cap, ref in cont.capacidades.items():
            nombre_cap = str(nombre_cap)
            entrada: Dict[str, Any] = {
                "capacidad": nombre_cap,
                "ref_tipo": type(ref).__name__,
                "en_contrato": True,
                "resoluble": False,
                "callable": False,
                "atributo_modulo": None,
                "mismo_objeto_que_atributo": None,
                "error": None,
            }

            attr = getattr(mod, nombre_cap, None)
            entrada["atributo_modulo"] = (
                "callable" if callable(attr)
                else ("existe_no_callable" if attr is not None else "ausente")
            )

            fn = None
            if callable(ref):
                fn = ref
                if callable(attr):
                    entrada["mismo_objeto_que_atributo"] = attr is ref
            elif isinstance(ref, str):
                fn = getattr(mod, ref, None)
                if fn is None:
                    entrada["error"] = (
                        "ref string '{0}' no existe en el modulo".format(ref)
                    )
            else:
                entrada["error"] = (
                    "ref de capacidad no es callable ni str: {0}".format(
                        type(ref).__name__
                    )
                )

            if callable(fn):
                entrada["resoluble"] = True
                entrada["callable"] = True
                entrada["fn_nombre"] = getattr(fn, "__name__", str(fn))
            elif entrada["error"] is None:
                entrada["error"] = "no resolvio a callable"

            reporte.append(entrada)

            if not entrada["resoluble"]:
                self.errores_arranque.append(
                    "AX/{0}: capacidad '{1}' no resoluble ({2})".format(
                        cont.nombre,
                        nombre_cap,
                        entrada.get("error") or "sin callable",
                    )
                )

        # Capacidades esperadas por el contrato documentado del modulo
        esperadas = {
            "verificar", "barrer", "inventario", "axiomas", "generatividad"
        }
        declaradas = {str(k) for k in cont.capacidades.keys()}
        faltan = sorted(esperadas - declaradas)
        extra = sorted(declaradas - esperadas)
        if faltan:
            self.errores_arranque.append(
                "AX/{0}: CONTENEDOR no declara capacidades esperadas: {1}".format(
                    cont.nombre, faltan
                )
            )
        if extra:
            # no es error de arranque: el modulo puede ampliar contrato
            self.fallos.append({
                "seccion": "AX",
                "razon": "capacidades extra en CONTENEDOR: {0}".format(extra),
            })

        return reporte

    # ---------------------------------------------------------------
    # subsección: carga del modulo axiomas (solo rol AX del CONTENEDOR)
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
        caps = meta.get("capacidades")

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

        if not isinstance(caps, dict) or not caps:
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
        cont.requiere = requiere
        self._ax_cont = cont

        # Todos los archivos de la carpeta
        self._ax_archivos_lista = self._ax_listar_archivos()

        # Validacion detallada contrato ↔ implementacion
        self._ax_reporte_capacidades = self._ax_validar_capacidades(cont)

    # ---------------------------------------------------------------
    # subsección: contenedor (metodo ≠ atributo)
    # ---------------------------------------------------------------
    def _ax_contenedor(self) -> Optional[Contenedor]:
        return self._ax_cont

    # ---------------------------------------------------------------
    # subsección: todos los archivos bajo modules/axiomas/
    # ---------------------------------------------------------------
    def _ax_listar_archivos(self) -> List[str]:
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
        if not self._ax_archivos_lista:
            self._ax_archivos_lista = self._ax_listar_archivos()
        return list(self._ax_archivos_lista)

    def ax_reporte_capacidades(self) -> List[Dict[str, Any]]:
        return list(self._ax_reporte_capacidades)

    # ---------------------------------------------------------------
    # subsección: invocacion — solo CONTENEDOR vivo
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

        if capacidad not in cont.capacidades:
            self.fallos.append({
                "seccion": "AX",
                "capacidad": capacidad,
                "razon": "fuera del CONTENEDOR vivo",
            })
            return None

        if not cont.tiene(capacidad):
            self.fallos.append({
                "seccion": "AX",
                "contenedor": cont.nombre,
                "capacidad": capacidad,
                "razon": "declarada pero no resoluble a callable",
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
        if not isinstance(out, dict):
            return None
        out = dict(out)
        cont = self._ax_contenedor()
        out["archivos_modulo"] = self.ax_archivos()
        out["archivos_n"] = len(out["archivos_modulo"])
        out["reporte_capacidades"] = self.ax_reporte_capacidades()
        if cont is not None:
            out["contrato_vivo"] = {
                "nombre": cont.nombre,
                "rol": cont.rol,
                "version": cont.version,
                "requiere": list(cont.requiere),
                "descripcion": cont.descripcion,
                "capacidades": sorted(str(k) for k in cont.capacidades.keys()),
            }
        return out

    # ---------------------------------------------------------------
    # subsección: capacidad — generatividad
    # ---------------------------------------------------------------
    def ax_generatividad(self) -> Optional[Dict[str, Any]]:
        out = self._ax_capacidad("generatividad")
        if isinstance(out, dict):
            return out
        return None

    # ---------------------------------------------------------------
    # subsección: compuerta de arranque (juez del grafo via barrer)
    # ---------------------------------------------------------------
    def _ax_compuerta(self) -> None:
        cont = self._ax_contenedor()
        if cont is None:
            if not any(e.startswith("AX:") for e in self.errores_arranque):
                self.errores_arranque.append(
                    "AX: falta contenedor (modules/axiomas)"
                )
            return

        if not self.ax_archivos():
            self.errores_arranque.append(
                "AX/{0}: carpeta sin archivos legibles".format(cont.nombre)
            )

        # Si alguna capacidad del contrato no resolvio, ya esta en errores
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
