# -*- coding: utf-8 -*-
"""
VPSI-TRUTH --- core/engine.py

Nucleo del repositorio.
Integra cada modulo solo a partir de su CONTENEDOR.
"""

from __future__ import annotations

import importlib.util
import sys
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional

# ===============================================================
# EXCEPCIONES Y REGISTRO
# ===============================================================
class ArranqueError(Exception):
    pass


class Contenedor:
    def __init__(self, nombre: str, rol: str, version: str, modulo: Any, ruta: Path, meta: Dict[str, Any]) -> None:
        self.nombre = nombre
        self.rol = rol
        self.version = version
        self.modulo = modulo
        self.ruta = ruta
        self.meta = meta
        self.capacidades = meta.get("capacidades", {})
        self.requiere = meta.get("requiere", [])

    def tiene(self, capacidad: str) -> bool:
        if capacidad not in self.capacidades:
            return False
        ref = self.capacidades[capacidad]
        if callable(ref):
            return True
        return self.modulo is not None and callable(getattr(self.modulo, str(ref), None))


class RegistroModulos:
    def __init__(self) -> None:
        self.contenedores: Dict[str, Contenedor] = {}
        self.por_rol: Dict[str, List[Contenedor]] = {}

    def registrar(self, cont: Contenedor) -> None:
        self.contenedores[cont.nombre] = cont
        self.por_rol.setdefault(cont.rol, []).append(cont)

    def primero(self, clave_rol_o_nombre: str) -> Optional[Contenedor]:
        if clave_rol_o_nombre in self.contenedores:
            return self.contenedores[clave_rol_o_nombre]
        lista = self.por_rol.get(clave_rol_o_nombre)
        return lista[0] if lista else None

    def total(self) -> int:
        return len(self.contenedores)


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
        
        # Inicialización del registro central
        self.registro = RegistroModulos()

        # Carga automática de todos los módulos mediante su CONTENEDOR
        self._cargar_modulos_automaticos()

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
    # CARGADOR DE MÓDULOS / CONTENEDORES
    # ===============================================================
    def _cargar_modulos_automaticos(self) -> None:
        """Escanea dinámicamente la carpeta de módulos y registra cualquier CONTENEDOR válido."""
        if not self.raiz.is_dir():
            return

        for path_dir in sorted(self.raiz.iterdir()):
            if not path_dir.is_dir():
                continue
            
            init_path = path_dir / "__init__.py"
            if not init_path.is_file():
                continue

            nombre_mod = f"vpsi_dinamico_{path_dir.name}"
            spec = importlib.util.spec_from_file_location(
                nombre_mod,
                init_path,
                submodule_search_locations=[str(path_dir)],
            )
            if spec is None or spec.loader is None:
                continue

            mod = importlib.util.module_from_spec(spec)
            sys.modules[nombre_mod] = mod
            try:
                spec.loader.exec_module(mod)
            except Exception as e:
                self.errores_arranque.append(
                    f"{path_dir.name}: import fallo: {type(e).__name__}: {e}"
                )
                continue

            meta = getattr(mod, "CONTENEDOR", None)
            if not isinstance(meta, dict):
                continue

            nombre = meta.get("nombre", path_dir.name)
            rol = meta.get("rol", "GEN")
            version = str(meta.get("version", "1.0"))

            contenedor = Contenedor(
                nombre=nombre,
                rol=rol,
                version=version,
                modulo=mod,
                ruta=init_path,
                meta=meta,
            )
            self.registro.registrar(contenedor)

            caps = meta.get("capacidades", {})
            fn_validar = caps.get("verificar") or caps.get("barrer") or caps.get("evaluar")
            if fn_validar:
                fn = fn_validar if callable(fn_validar) else getattr(mod, str(fn_validar), None)
                if callable(fn):
                    try:
                        informe = fn()
                        if isinstance(informe, dict) and not informe.get("coherente", True):
                            self.errores_arranque.append(
                                f"{rol}: módulo incoherente según su contrato"
                            )
                    except Exception as e:
                        self.errores_arranque.append(
                            f"{rol}: error ejecutando validación: {type(e).__name__}: {e}"
                        )

            # ==========================================================
# INICIO: Método censar() para la clase Engine
# ==========================================================
    def censar(self) -> dict:
        """Devuelve un censo estructurado de los contenedores y roles cargados dinámicamente."""
        cargados = []
        roles_dict = {}
        for nombre, cont in self.registro.contenedores.items():
            cargados.append({"nombre": cont.nombre, "rol": cont.rol, "version": cont.version})
            roles_dict.setdefault(cont.rol, []).append(cont.nombre)
            
        return {
            "total": self.registro.total() if hasattr(self.registro, "total") else len(self.registro.contenedores),
            "roles": roles_dict,
            "roles_vacios": [],
            "rechazados": [],
            "cargados": cargados,
        }
# ==========================================================
# FIN: Método censar() para la clase Engine
# ==========================================================

   # ==========================================================
# INICIO: Atributo resultados_evaluacion en core/engine.py
# ==========================================================
        self.resultados_evaluacion = []
# ==========================================================
# FIN: Atributo resultados_evaluacion en core/engine.py
# ==========================================================
    
