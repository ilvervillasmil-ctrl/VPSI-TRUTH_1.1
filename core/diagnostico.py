# ==============================================================
# INICIO: core/engine.py — versión reforzada (capas completas + validador)
# ==============================================================

# -*- coding: utf-8 -*-
"""
VPSI-TRUTH --- core/engine.py

Única autoridad estructural del sistema.
Conoce únicamente el Contrato Universal.
Todo lo demás se descubre, valida, inspecciona y construye automáticamente.
"""

from __future__ import annotations

import ast
import importlib.util
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


# ===============================================================
# SECCIÓN 1: EXCEPCIONES Y ESTRUCTURAS BASE
# ===============================================================
class ArranqueError(Exception):
    pass


class Contenedor:
    """Representación interna de un contrato válido."""

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
        self.meta = meta
        self.capacidades = meta.get("capacidades", {})
        self.requiere = meta.get("requiere", [])
        self._fn_custom = meta.get("fn") if callable(meta.get("fn")) else None

    def tiene(self, capacidad: str) -> bool:
        if capacidad not in self.capacidades:
            return False
        ref = self.capacidades[capacidad]
        if callable(ref):
            return True
        return self.modulo is not None and callable(getattr(self.modulo, str(ref), None))

    def fn(self, clave: str) -> Any:
        if self._fn_custom is not None:
            try:
                res = self._fn_custom(clave)
                if res is not None:
                    return res
            except Exception:
                pass
        ref = self.capacidades.get(clave)
        if callable(ref):
            return ref
        if isinstance(ref, str) and self.modulo is not None:
            return getattr(self.modulo, ref, None)
        return None


class RegistroModulos:
    def __init__(self) -> None:
        self.contenedores: Dict[str, Contenedor] = {}
        self.por_rol: Dict[str, List[Contenedor]] = {}

    def registrar(self, cont: Contenedor) -> None:
        self.contenedores[cont.nombre] = cont
        self.por_rol.setdefault(cont.rol, []).append(cont)

    def primero(self, clave: str) -> Optional[Contenedor]:
        if clave in self.contenedores:
            return self.contenedores[clave]
        lista = self.por_rol.get(clave)
        return lista[0] if lista else None

    def total(self) -> int:
        return len(self.contenedores)


# ===============================================================
# SECCIÓN 2: ENGINE
# ===============================================================
class Engine:
    VERSION = "14.0-reforzado"

    # Capacidades que sí pueden ejecutarse automáticamente en el arranque
    CAPACIDADES_INSPECCION = frozenset({
        "verificar", "barrer", "evaluar", "inventario", "meta", "axiomas"
    })

    def __init__(
        self,
        raiz_modulos: str | Path,
        invocador_id: str = "core",
        strict: bool = True,
    ) -> None:
        self.raiz = Path(raiz_modulos).resolve()
        self.invocador_id = invocador_id
        self.strict = strict
        self.estado = "NO_INICIADO"
        self.errores_arranque: List[str] = []
        self.advertencias: List[str] = []
        self.registro = RegistroModulos()
        self.resultados_evaluacion: List[Any] = []

        # Evidencia de las capas
        self._modulos_descubiertos: List[Path] = []
        self._exploracion: Dict[str, Any] = {}
        self._inspeccion: Dict[str, Any] = {}
        self._auditoria: Dict[str, Any] = {}
        self._grafo: Dict[str, Any] = {}

        # Flujo de capas (una sola pasada de descubrimiento)
        self._modulos_descubiertos = self._descubrir_modulos()
        self._validar_y_cargar()
        self._construir_grafo()

        if self.errores_arranque:
            self.estado = "RECHAZADO"
            if self.strict:
                raise ArranqueError(
                    "Engine no pudo arrancar:\n  - "
                    + "\n  - ".join(self.errores_arranque)
                )
        else:
            self.estado = "OPERATIVO"

    # ===========================================================
    # CAPA 1: DESCUBRIDOR
    # ===========================================================
    def _descubrir_modulos(self) -> List[Path]:
        """Busca todas las carpetas que contienen __init__.py."""
        encontrados: List[Path] = []
        if not self.raiz.is_dir():
            return encontrados
        for path_dir in sorted(self.raiz.iterdir()):
            if path_dir.is_dir() and (path_dir / "__init__.py").is_file():
                encontrados.append(path_dir)
        return encontrados

    # ===========================================================
    # CAPA 2: LECTOR DE CONTRATO
    # ===========================================================
    def _leer_contrato(self, path_dir: Path) -> Optional[Dict[str, Any]]:
        """Lee exclusivamente el CONTENEDOR. No interpreta lógica."""
        init_path = path_dir / "__init__.py"
        nombre_mod = f"vpsi_dinamico_{path_dir.name}"
        try:
            spec = importlib.util.spec_from_file_location(
                nombre_mod,
                init_path,
                submodule_search_locations=[str(path_dir)],
            )
            if spec is None or spec.loader is None:
                return None
            mod = importlib.util.module_from_spec(spec)
            sys.modules[nombre_mod] = mod
            spec.loader.exec_module(mod)
            meta = getattr(mod, "CONTENEDOR", None)
            if not isinstance(meta, dict):
                return None
            return {
                "meta": meta,
                "modulo": mod,
                "ruta": init_path,
                "nombre_carpeta": path_dir.name,
            }
        except Exception as e:
            self.errores_arranque.append(
                f"{path_dir.name}: fallo al leer contrato: {type(e).__name__}: {e}"
            )
            return None

    # ===========================================================
    # CAPA 3: VALIDADOR DE CONTRATO (nueva)
    # ===========================================================
    def _validar_contrato(self, meta: Dict[str, Any], nombre_carpeta: str) -> List[str]:
        """Valida la forma mínima del Contrato Universal. Devuelve lista de errores."""
        errores = []
        if not isinstance(meta.get("nombre"), str) or not meta["nombre"]:
            errores.append(f"{nombre_carpeta}: 'nombre' debe ser str no vacío")
        if not isinstance(meta.get("rol"), str) or not meta["rol"]:
            errores.append(f"{nombre_carpeta}: 'rol' debe ser str no vacío")
        if not isinstance(meta.get("version"), str):
            errores.append(f"{nombre_carpeta}: 'version' debe ser str")
        if not isinstance(meta.get("requiere"), list):
            errores.append(f"{nombre_carpeta}: 'requiere' debe ser list")
        caps = meta.get("capacidades")
        if not isinstance(caps, dict):
            errores.append(f"{nombre_carpeta}: 'capacidades' debe ser dict")
        else:
            for k in caps.keys():
                if not isinstance(k, str):
                    errores.append(f"{nombre_carpeta}: clave de capacidad no es str: {k}")
        return errores

    # ===========================================================
    # CAPA 4: EXPLORADOR
    # ===========================================================
    def _explorar_modulo(self, path_dir: Path) -> Dict[str, Any]:
        """Recorre la estructura completa del módulo."""
        archivos = []
        subcarpetas = []
        for p in path_dir.rglob("*"):
            if p.is_file():
                archivos.append(str(p.relative_to(self.raiz)))
            elif p.is_dir() and p != path_dir:
                subcarpetas.append(str(p.relative_to(self.raiz)))
        return {
            "archivos": sorted(archivos),
            "subcarpetas": sorted(subcarpetas),
            "total_archivos": len(archivos),
            "total_subcarpetas": len(subcarpetas),
        }

    # ===========================================================
    # CAPA 5: INSPECTOR AST
    # ===========================================================
    def _inspeccionar_archivo(self, archivo: Path) -> Dict[str, Any]:
        """Inspecciona un archivo Python sin ejecutarlo."""
        info: Dict[str, Any] = {
            "funciones": [],
            "clases": [],
            "constantes": [],
            "imports": [],
            "doc": None,
        }
        try:
            fuente = archivo.read_text(encoding="utf-8")
            tree = ast.parse(fuente, filename=str(archivo))
            info["doc"] = ast.get_docstring(tree)
            for node in tree.body:
                if isinstance(node, ast.FunctionDef):
                    info["funciones"].append(node.name)
                elif isinstance(node, ast.ClassDef):
                    info["clases"].append(node.name)
                elif isinstance(node, ast.Assign):
                    for t in node.targets:
                        if isinstance(t, ast.Name) and t.id.isupper():
                            info["constantes"].append(t.id)
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    info["imports"].append(ast.dump(node))
        except Exception:
            pass
        return info

    def _inspeccionar_modulo(self, path_dir: Path) -> Dict[str, Any]:
        """Inspecciona todos los archivos .py del módulo."""
        resultado = {}
        for py in path_dir.rglob("*.py"):
            rel = str(py.relative_to(self.raiz))
            resultado[rel] = self._inspeccionar_archivo(py)
        return resultado

    # ===========================================================
    # CAPA 6: RESOLVER
    # ===========================================================
    def _resolver_capacidades(self, cont: Contenedor) -> Dict[str, Any]:
        """Verifica que cada capacidad declarada sea resoluble y callable."""
        resultado = {"resolubles": [], "no_resolubles": [], "total": 0}
        for clave in cont.capacidades.keys():
            resultado["total"] += 1
            fn = cont.fn(clave)
            if callable(fn):
                resultado["resolubles"].append(clave)
            else:
                resultado["no_resolubles"].append(clave)
        return resultado

    # ===========================================================
    # CAPA 7: EJECUTOR (solo capacidades de inspección)
    # ===========================================================
    def _ejecutar_capacidades_inspeccion(self, cont: Contenedor) -> Dict[str, Any]:
        """
        Ejecuta únicamente las capacidades de inspección (verificar, inventario, etc.).
        Las capacidades funcionales se registran pero no se ejecutan en el arranque.
        """
        resultados = {}
        for clave in cont.capacidades.keys():
            if clave not in self.CAPACIDADES_INSPECCION:
                resultados[clave] = {"estado": "REGISTRADA_NO_EJECUTADA"}
                continue
            fn = cont.fn(clave)
            if not callable(fn):
                resultados[clave] = {"estado": "NO_CALLABLE"}
                continue
            try:
                salida = fn()
                resultados[clave] = {"estado": "EXITO", "resultado": salida}
            except Exception as e:
                resultados[clave] = {
                    "estado": "ERROR_EJECUCION",
                    "error": f"{type(e).__name__}: {e}",
                }
        return resultados

    # ===========================================================
    # CAPA 8: AUDITOR (conserva evidencia completa)
    # ===========================================================
    def _auditar(
        self,
        cont: Contenedor,
        resolucion: Dict[str, Any],
        ejecucion: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Recoge evidencia completa. No reduce a un simple booleano."""
        evidencia_modulos = {}
        for clave, datos in ejecucion.items():
            if datos.get("estado") == "EXITO" and isinstance(datos.get("resultado"), dict):
                evidencia_modulos[clave] = datos["resultado"]

        coherente = (
            len(resolucion.get("no_resolubles", [])) == 0
            and all(
                v.get("estado") in ("EXITO", "REGISTRADA_NO_EJECUTADA")
                for v in ejecucion.values()
            )
        )

        return {
            "nombre": cont.nombre,
            "rol": cont.rol,
            "version": cont.version,
            "requiere": list(cont.requiere),
            "resolucion": resolucion,
            "ejecucion": ejecucion,
            "evidencia": evidencia_modulos,
            "coherente": coherente,
        }

    # ===========================================================
    # CAPA 9: CONSTRUCTOR DEL GRAFO (enriquecido)
    # ===========================================================
    def _construir_grafo(self) -> None:
        """Construye relaciones ricas entre módulos, roles, capacidades y archivos."""
        nodos = []
        aristas = []

        for nombre, cont in self.registro.contenedores.items():
            nodos.append({"id": nombre, "tipo": "modulo", "rol": cont.rol})

            # módulo → rol
            aristas.append({"from": nombre, "to": cont.rol, "tipo": "tiene_rol"})

            # módulo → capacidades
            for cap in cont.capacidades.keys():
                aristas.append({"from": nombre, "to": f"{nombre}.{cap}", "tipo": "declara_capacidad"})

            # módulo → dependencias
            for dep in cont.requiere:
                aristas.append({"from": nombre, "to": dep, "tipo": "requiere"})

            # módulo → archivos (desde exploración)
            exploracion = self._exploracion.get(nombre, {})
            for archivo in exploracion.get("archivos", []):
                aristas.append({"from": nombre, "to": archivo, "tipo": "contiene_archivo"})

        self._grafo = {"nodos": nodos, "aristas": aristas}

    # ===========================================================
    # ORQUESTACIÓN DE CAPAS
    # ===========================================================
    def _validar_y_cargar(self) -> None:
        """Orquesta todas las capas en orden correcto."""
        for path_dir in self._modulos_descubiertos:
            leido = self._leer_contrato(path_dir)
            if leido is None:
                continue

            meta = leido["meta"]
            nombre_carpeta = leido["nombre_carpeta"]

            # Validación formal del contrato
            errores_contrato = self._validar_contrato(meta, nombre_carpeta)
            if errores_contrato:
                self.errores_arranque.extend(errores_contrato)
                continue

            nombre = meta["nombre"]
            rol = meta["rol"]
            version = str(meta.get("version", "1.0"))

            cont = Contenedor(
                nombre=nombre,
                rol=rol,
                version=version,
                modulo=leido["modulo"],
                ruta=leido["ruta"],
                meta=meta,
            )
            self.registro.registrar(cont)

            # Exploración de estructura
            exploracion = self._explorar_modulo(path_dir)
            self._exploracion[nombre] = exploracion

            # Inspección AST de todos los .py
            inspeccion = self._inspeccionar_modulo(path_dir)
            self._inspeccion[nombre] = inspeccion

            # Resolución de capacidades
            resolucion = self._resolver_capacidades(cont)

            # Ejecución solo de capacidades de inspección
            ejecucion = self._ejecutar_capacidades_inspeccion(cont)

            # Auditoría completa (conserva evidencia)
            auditoria = self._auditar(cont, resolucion, ejecucion)
            self._auditoria[nombre] = auditoria

            if not auditoria["coherente"]:
                self.errores_arranque.append(
                    f"{rol}/{nombre}: contrato o capacidades con problemas"
                )

    # ===========================================================
    # ESTADO GLOBAL (espejo completo)
    # ===========================================================
    def estado_global(self) -> Dict[str, Any]:
        """Espejo completo del sistema. Única fuente de verdad estructural."""
        return {
            "tipo": "estado_global",
            "version_engine": self.VERSION,
            "estado": self.estado,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_contenedores": self.registro.total(),
            "roles": {
                rol: [c.nombre for c in lista]
                for rol, lista in self.registro.por_rol.items()
            },
            "cargados": [
                {
                    "nombre": c.nombre,
                    "rol": c.rol,
                    "version": c.version,
                    "requiere": list(c.requiere),
                    "capacidades_declaradas": list(c.capacidades.keys()),
                }
                for c in self.registro.contenedores.values()
            ],
            "exploracion": self._exploracion,
            "inspeccion": self._inspeccion,
            "auditoria": self._auditoria,
            "grafo": self._grafo,
            "errores_arranque": list(self.errores_arranque),
            "advertencias": list(self.advertencias),
            "nota": (
                "Estado global construido exclusivamente por el Engine "
                "mediante sus capas internas a partir del Contrato Universal."
            ),
        }

    # ===========================================================
    # MÉTODOS PÚBLICOS DE COMPATIBILIDAD
    # ===========================================================
    def censar(self) -> dict:
        eg = self.estado_global()
        return {
            "total": eg["total_contenedores"],
            "roles": eg["roles"],
            "roles_vacios": [],
            "rechazados": eg["errores_arranque"],
            "cargados": eg["cargados"],
        }

    def ejecutar_contratos_y_explorar(self) -> Dict[str, Any]:
        return self._auditoria


# ===============================================================
# SECCIÓN 3: ALIAS UNIVERSALES MÍNIMOS
# ===============================================================
UNIVERSAL_CAPACIDADES_MAP = {
    "verificar": "barrer",
    "barrer": "barrer",
    "evaluar": "barrer",
}


def obtener_funcion_universal(capacidad_clave: str) -> str:
    return UNIVERSAL_CAPACIDADES_MAP.get(capacidad_clave, capacidad_clave)


# ==============================================================
# FIN: core/engine.py — versión reforzada (capas completas + validador)
# (Pegue aquí cualquier código nuevo que se agregue en el futuro)
# ==============================================================
