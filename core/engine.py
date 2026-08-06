# ==============================================================
# INICIO: core/engine.py — versión completa con ejecución del contrato
# ==============================================================

# ilver
"""
VPSI-TRUTH --- core/engine.py

Kernel estructural.
Lee el CONTENEDOR y ejecuta literalmente las capacidades que declara.
"""

from __future__ import annotations

import ast
import importlib.util
import sys
import time
from collections import defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


# ===============================================================
# SECCIÓN 1: EXCEPCIONES Y ESTRUCTURAS BASE
# ===============================================================
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
        self.meta = meta
        self.capacidades = meta.get("capacidades", {})
        self.requiere = list(meta.get("requiere", []))
        self._fn_custom = meta.get("fn") if callable(meta.get("fn")) else None

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
    VERSION = "17.1-ejecuta-contrato"

    def __init__(
        self,
        raiz_modulos: str | Path,
        invocador_id: str = "core",
        strict: bool = True,
    ) -> None:
        # 2.1 Parámetros
        self.raiz = Path(raiz_modulos).resolve()
        self.invocador_id = invocador_id
        self.strict = strict

        # 2.2 Estado
        self.estado = "NO_INICIADO"

        # 2.3 Atributos exigidos por auditoría
        self.registro = RegistroModulos()
        self.resultados_evaluacion: List[Any] = []
        self.errores_arranque: List[str] = []
        self.fallos: List[Dict[str, Any]] = []
        self.advertencias: List[str] = []

        # 2.4 Evidencia
        self._modulos_descubiertos: List[Path] = []
        self._exploracion: Dict[str, Any] = {}
        self._inspeccion: Dict[str, Any] = {}
        self._resolucion: Dict[str, Any] = {}
        self._ejecucion: Dict[str, Any] = {}
        self._auditoria: Dict[str, Any] = {}
        self._grafo: Dict[str, Any] = {}
        self._dependencias: Dict[str, Any] = {}
        self._indice_simbolos: Dict[str, Dict[str, Any]] = {}
        self._diagnosticos_causales: List[Dict[str, Any]] = []

        # 2.5 Flujo
        self._modulos_descubiertos = self._descubrir_modulos()
        self._cargar_y_validar()
        self._resolver_dependencias()
        self._construir_indice_simbolos()
        self._construir_grafo()

        # 2.6 Cierre
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
    # SECCIÓN 3: DESCUBRIDOR
    # ===========================================================
    def _descubrir_modulos(self) -> List[Path]:
        encontrados: List[Path] = []
        if not self.raiz.is_dir():
            return encontrados
        for path_dir in sorted(self.raiz.iterdir()):
            if path_dir.is_dir() and (path_dir / "__init__.py").is_file():
                encontrados.append(path_dir)
        return encontrados

    # ===========================================================
    # SECCIÓN 4: DIAGNÓSTICO CAUSAL
    # ===========================================================
    def _diagnosticar_import_error(self, path_dir: Path, error: Exception) -> Dict[str, Any]:
        mensaje = str(error)
        diag: Dict[str, Any] = {
            "modulo": path_dir.name,
            "fase": "Carga del contrato",
            "tipo_error": type(error).__name__,
            "mensaje": mensaje,
            "dependencia": None,
            "simbolo": None,
            "exportaciones_disponibles": [],
            "causa_raiz": None,
        }
        if isinstance(error, ImportError) and "cannot import name" in mensaje and " from " in mensaje:
            try:
                parte = mensaje.split("cannot import name ")[1]
                simbolo = parte.split("'")[1]
                modulo_origen = parte.split(" from '")[1].split("'")[0]
                diag["simbolo"] = simbolo
                diag["dependencia"] = modulo_origen
                try:
                    mod_destino = sys.modules.get(modulo_origen)
                    if mod_destino is None:
                        import importlib
                        mod_destino = importlib.import_module(modulo_origen)
                    diag["exportaciones_disponibles"] = [
                        n for n in dir(mod_destino) if not n.startswith("_")
                    ][:50]
                except Exception:
                    pass
                diag["causa_raiz"] = f"Símbolo '{simbolo}' no encontrado en '{modulo_origen}'."
            except Exception:
                diag["causa_raiz"] = "ImportError no parseable"
        else:
            diag["causa_raiz"] = f"{type(error).__name__}: {mensaje}"
        return diag

    # ===========================================================
    # SECCIÓN 5: LECTOR DE CONTRATO
    # ===========================================================
    def _leer_contrato(self, path_dir: Path) -> Optional[Dict[str, Any]]:
        init_path = path_dir / "__init__.py"
        nombre_mod = f"vpsi_dinamico_{path_dir.name}"
        try:
            spec = importlib.util.spec_from_file_location(
                nombre_mod, init_path, submodule_search_locations=[str(path_dir)]
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
            diag = self._diagnosticar_import_error(path_dir, e)
            self._diagnosticos_causales.append(diag)
            self.errores_arranque.append(
                f"{path_dir.name}: [{diag['tipo_error']}] "
                f"dep={diag.get('dependencia')} símbolo={diag.get('simbolo')} "
                f"→ {diag.get('causa_raiz')}"
            )
            return None

    # ===========================================================
    # SECCIÓN 6: VALIDADOR DE CONTRATO
    # ===========================================================
    def _validar_contrato(self, meta: Dict[str, Any], nombre_carpeta: str) -> List[str]:
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
            for k in caps:
                if not isinstance(k, str):
                    errores.append(f"{nombre_carpeta}: clave de capacidad no es str: {k}")
        return errores

    # ===========================================================
    # SECCIÓN 7: EXPLORADOR
    # ===========================================================
    def _explorar_modulo(self, path_dir: Path) -> Dict[str, Any]:
        archivos, subcarpetas = [], []
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
    # SECCIÓN 8: INSPECTOR AST
    # ===========================================================
    def _inspeccionar_archivo(self, archivo: Path) -> Dict[str, Any]:
        info: Dict[str, Any] = {
            "funciones": [], "clases": [], "constantes": [],
            "imports": [], "doc": None
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
        resultado = {}
        for py in path_dir.rglob("*.py"):
            rel = str(py.relative_to(self.raiz))
            resultado[rel] = self._inspeccionar_archivo(py)
        return resultado

    # ===========================================================
    # SECCIÓN 9: RESOLVER CAPACIDADES
    # ===========================================================
    def _resolver_capacidades(self, cont: Contenedor) -> Dict[str, Any]:
        resultado = {"resolubles": [], "no_resolubles": [], "total": 0}
        for clave in cont.capacidades:
            resultado["total"] += 1
            if callable(cont.fn(clave)):
                resultado["resolubles"].append(clave)
            else:
                resultado["no_resolubles"].append(clave)
        return resultado

    # ===========================================================
    # SECCIÓN 10: EJECUCIÓN LITERAL DEL CONTRATO
    # ===========================================================
    def _ejecutar_contrato(self, cont: Contenedor) -> Dict[str, Any]:
        """
        Ejecuta literalmente todas las capacidades declaradas en el CONTENEDOR.
        """
        resultados = {}
        for clave in cont.capacidades:
            fn = cont.fn(clave)
            if not callable(fn):
                resultados[clave] = {
                    "estado": "NO_CALLABLE",
                    "error": "La capacidad declarada no es ejecutable",
                }
                continue

            inicio = time.perf_counter()
            try:
                salida = fn()
                duracion = time.perf_counter() - inicio
                resultados[clave] = {
                    "estado": "EXITO",
                    "resultado": salida,
                    "duracion_s": round(duracion, 6),
                }
            except Exception as e:
                duracion = time.perf_counter() - inicio
                resultados[clave] = {
                    "estado": "ERROR_EJECUCION",
                    "error": f"{type(e).__name__}: {e}",
                    "duracion_s": round(duracion, 6),
                }
        return resultados

    # ===========================================================
    # SECCIÓN 11: AUDITOR
    # ===========================================================
    def _auditar(self, cont: Contenedor, resolucion: Dict, ejecucion: Dict) -> Dict[str, Any]:
        coherente = (
            len(resolucion.get("no_resolubles", [])) == 0
            and all(v.get("estado") == "EXITO" for v in ejecucion.values())
        )
        return {
            "nombre": cont.nombre,
            "rol": cont.rol,
            "version": cont.version,
            "requiere": list(cont.requiere),
            "resolucion": resolucion,
            "ejecucion": ejecucion,
            "coherente": coherente,
        }

    # ===========================================================
    # SECCIÓN 12: RESOLUCIÓN DE DEPENDENCIAS
    # ===========================================================
    def _resolver_dependencias(self) -> None:
        roles_presentes = set(self.registro.por_rol.keys())
        faltantes: Dict[str, List[str]] = defaultdict(list)
        grafo_dep: Dict[str, List[str]] = defaultdict(list)

        for nombre, cont in self.registro.contenedores.items():
            for dep in cont.requiere:
                grafo_dep[nombre].append(dep)
                if dep not in roles_presentes and dep not in self.registro.contenedores:
                    faltantes[nombre].append(dep)
                    self.errores_arranque.append(
                        f"{cont.rol}/{nombre}: dependencia inexistente → '{dep}'"
                    )

        in_degree = {n: 0 for n in self.registro.contenedores}
        for src, dests in grafo_dep.items():
            for d in dests:
                if d in in_degree:
                    in_degree[d] += 1

        cola = deque([n for n, deg in in_degree.items() if deg == 0])
        orden = []
        while cola:
            n = cola.popleft()
            orden.append(n)
            for d in grafo_dep.get(n, []):
                if d in in_degree:
                    in_degree[d] -= 1
                    if in_degree[d] == 0:
                        cola.append(d)

        ciclos = [n for n, deg in in_degree.items() if deg > 0]
        if ciclos:
            self.errores_arranque.append(f"Ciclos de dependencia detectados: {ciclos}")

        self._dependencias = {
            "grafo": dict(grafo_dep),
            "faltantes": dict(faltantes),
            "orden_topologico": orden,
            "ciclos": ciclos,
        }

    # ===========================================================
    # SECCIÓN 13: ÍNDICE DE SÍMBOLOS
    # ===========================================================
    def _construir_indice_simbolos(self) -> None:
        for nombre, cont in self.registro.contenedores.items():
            inspeccion = self._inspeccion.get(nombre, {})
            simbolos = {
                "clases": [],
                "funciones": [],
                "constantes": [],
                "capacidades": list(cont.capacidades.keys()),
            }
            for info in inspeccion.values():
                simbolos["clases"].extend(info.get("clases", []))
                simbolos["funciones"].extend(info.get("funciones", []))
                simbolos["constantes"].extend(info.get("constantes", []))
            for k in ("clases", "funciones", "constantes"):
                simbolos[k] = sorted(set(simbolos[k]))
            self._indice_simbolos[nombre] = simbolos

    # ===========================================================
    # SECCIÓN 14: GRAFO
    # ===========================================================
    def _construir_grafo(self) -> None:
        nodos, aristas = [], []
        for nombre, cont in self.registro.contenedores.items():
            nodos.append({"id": nombre, "tipo": "modulo", "rol": cont.rol})
            aristas.append({"from": nombre, "to": cont.rol, "tipo": "tiene_rol"})
            for cap in cont.capacidades:
                aristas.append({"from": nombre, "to": f"{nombre}.{cap}", "tipo": "declara_capacidad"})
            for dep in cont.requiere:
                aristas.append({"from": nombre, "to": dep, "tipo": "requiere"})
            for archivo in self._exploracion.get(nombre, {}).get("archivos", []):
                aristas.append({"from": nombre, "to": archivo, "tipo": "contiene_archivo"})
        self._grafo = {"nodos": nodos, "aristas": aristas}

    # ===========================================================
    # SECCIÓN 15: ORQUESTACIÓN (con ejecución del contrato)
    # ===========================================================
    def _cargar_y_validar(self) -> None:
        for path_dir in self._modulos_descubiertos:
            leido = self._leer_contrato(path_dir)
            if leido is None:
                continue

            meta = leido["meta"]
            nombre_carpeta = leido["nombre_carpeta"]

            errores = self._validar_contrato(meta, nombre_carpeta)
            if errores:
                self.errores_arranque.extend(errores)
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

            self._exploracion[nombre] = self._explorar_modulo(path_dir)
            self._inspeccion[nombre] = self._inspeccionar_modulo(path_dir)

            # 1. Resolver
            resolucion = self._resolver_capacidades(cont)
            self._resolucion[nombre] = resolucion

            # 2. Ejecutar el contrato
            ejecucion = self._ejecutar_contrato(cont)
            self._ejecucion[nombre] = ejecucion

            # 3. Auditar
            auditoria = self._auditar(cont, resolucion, ejecucion)
            self._auditoria[nombre] = auditoria

            if not auditoria["coherente"]:
                self.errores_arranque.append(
                    f"{rol}/{nombre}: fallo al ejecutar el contrato"
                )

    # ===========================================================
    # SECCIÓN 16: ESTADO GLOBAL
    # ===========================================================
    def estado_global(self) -> Dict[str, Any]:
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
            "resolucion": self._resolucion,
            "ejecucion": self._ejecucion,
            "auditoria": self._auditoria,
            "grafo": self._grafo,
            "dependencias": self._dependencias,
            "indice_simbolos": self._indice_simbolos,
            "diagnosticos_causales": self._diagnosticos_causales,
            "errores_arranque": list(self.errores_arranque),
            "advertencias": list(self.advertencias),
            "nota": (
                "Estado global. El Engine ejecuta literalmente "
                "las capacidades declaradas en cada CONTENEDOR."
            ),
        }

    # ===========================================================
    # SECCIÓN 17: COMPATIBILIDAD
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
        return self._ejecucion


# ==============================================================
# FIN: core/engine.py — versión completa con ejecución del contrato
# ==============================================================
