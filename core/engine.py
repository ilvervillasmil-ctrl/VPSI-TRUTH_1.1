# ===============================================================
# VPSI-TRUTH — core/engine.py
# ===============================================================
# ENGINE — VPSI-CONTRACT-1.0 / API 1.0
#
# Principio:
#   El Engine NO inventa capacidades. Ejecuta únicamente lo que
#   el contrato CONTENEDOR real de cada módulo declara y autoriza.
#
# Centinela:
#   Componente de PRIORIDAD ABSOLUTA para el cierre/verificación.
#
# IMPORTANTE:
#   Este archivo NO depende de core.paquete_contrato.
#   El contrato es el CONTENEDOR declarado por cada módulo.
# ===============================================================

from __future__ import annotations

import importlib.util
import inspect
import re
import sys
import time
from collections import defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from core.centinela import Centinela, Veredicto


# ===============================================================
# CONSTANTES
# ===============================================================

VERSION_ENGINE = "18.3"
ESQUEMA_CONTRATO_REQUERIDO = "VPSI-CONTRACT-1.0"
VERSION_CONTRATO_REQUERIDA = "1.0"
API_ENGINE_ACTUAL = "1.0"

ESTADO_NO_INICIADO = "NO_INICIADO"
ESTADO_OPERATIVO = "OPERATIVO"
ESTADO_DEGRADADO = "DEGRADADO"
ESTADO_RECHAZADO = "RECHAZADO"
ESTADOS_CANONICOS = (
    ESTADO_NO_INICIADO,
    ESTADO_OPERATIVO,
    ESTADO_DEGRADADO,
    ESTADO_RECHAZADO,
)

CLAVES_OBLIGATORIAS_CONTRATO = (
    "esquema", "version_contrato", "version_modulo", "id", "nombre",
    "rol", "descripcion", "funcion", "no_hace", "autoridad",
    "conocimiento_exportable", "requiere", "autoriza_engine",
    "consultas_soportadas", "capacidades", "capacidades_meta", "reporting",
    "estados_validos", "invariantes", "estabilidad", "compatible_desde",
    "api_engine",
)

PERMISOS_AUTORIZA_ENGINE = (
    "leer", "ejecutar", "consultar", "recombinar", "reportar", "auditar",
    "inventariar", "modificar", "alterar", "reescribir",
)

BANDERAS_REPORTING = (
    "estado", "salud", "inventario", "capacidades", "errores",
    "advertencias", "dependencias", "version", "contrato", "conocimiento",
    "metricas", "diagnostico",
)

CLAVES_META_CAPACIDAD = ("descripcion", "entrada", "salida")
LISTAS_STR_OBLIGATORIAS = (
    "no_hace", "autoridad", "conocimiento_exportable",
    "consultas_soportadas", "invariantes",
)


# ===============================================================
# DEFINICIONES
# ===============================================================

class ArranqueError(Exception):
    """Fallo estructural durante el arranque del Engine."""


class Contenedor:
    """Materialización del CONTENEDOR real declarado por un módulo."""

    def __init__(self, meta: Dict[str, Any], modulo: Any, ruta: Path) -> None:
        self.meta = meta
        self.modulo = modulo
        self.ruta = ruta
        self.id = str(meta.get("id", ""))
        self.nombre = str(meta.get("nombre", ""))
        self.rol = str(meta.get("rol", ""))
        self.version = str(meta.get("version_modulo", meta.get("version", "")))
        self.version_contrato = str(meta.get("version_contrato", ""))
        self.esquema = str(meta.get("esquema", ""))
        self.estabilidad = str(meta.get("estabilidad", ""))
        self.descripcion = str(meta.get("descripcion", ""))
        self.compatible_desde = str(meta.get("compatible_desde", ""))
        self.api_engine = str(meta.get("api_engine", ""))
        self.funcion = meta.get("funcion")
        self.no_hace = list(meta.get("no_hace") or [])
        self.autoridad = list(meta.get("autoridad") or [])
        self.conocimiento_exportable = list(meta.get("conocimiento_exportable") or [])
        self.consultas_soportadas = list(meta.get("consultas_soportadas") or [])
        self.invariantes = list(meta.get("invariantes") or [])
        self.requiere = list(meta.get("requiere") or [])
        self.autoriza_engine = dict(meta.get("autoriza_engine") or {})
        self.capacidades = dict(meta.get("capacidades") or {})
        self.capacidades_meta = dict(meta.get("capacidades_meta") or {})
        self.reporting = dict(meta.get("reporting") or {})
        self.estados_validos = list(meta.get("estados_validos") or [])

    def fn(self, clave: str) -> Any:
        ref = self.capacidades.get(clave)
        return ref if callable(ref) else None


class RegistroModulos:
    def __init__(self) -> None:
        self.contenedores: Dict[str, Contenedor] = {}
        self.por_id: Dict[str, Contenedor] = {}
        self.por_rol: Dict[str, List[Contenedor]] = {}

    def registrar(self, cont: Contenedor) -> List[str]:
        errores: List[str] = []
        if cont.nombre in self.contenedores:
            errores.append(f"duplicado de nombre: '{cont.nombre}' ya registrado")
        if cont.id and cont.id in self.por_id:
            errores.append(
                f"duplicado de id: '{cont.id}' ya registrado "
                f"(módulo {self.por_id[cont.id].nombre})"
            )
        if cont.rol in self.por_rol and self.por_rol[cont.rol]:
            errores.append(
                f"duplicado de rol: '{cont.rol}' ya ocupado por "
                f"'{self.por_rol[cont.rol][0].nombre}'"
            )
        if errores:
            return errores
        self.contenedores[cont.nombre] = cont
        if cont.id:
            self.por_id[cont.id] = cont
        self.por_rol.setdefault(cont.rol, []).append(cont)
        return []

    def primero(self, clave: str) -> Optional[Contenedor]:
        if clave in self.contenedores:
            return self.contenedores[clave]
        if clave in self.por_id:
            return self.por_id[clave]
        lista = self.por_rol.get(clave)
        return lista[0] if lista else None

    def total(self) -> int:
        return len(self.contenedores)


# ===============================================================
# ENGINE
# ===============================================================

class Engine:
    VERSION = VERSION_ENGINE

    def __init__(self, raiz_modulos: str | Path, invocador_id: str = "core", strict: bool = True) -> None:
        self.raiz = Path(raiz_modulos).resolve()
        self.invocador_id = invocador_id
        self.strict = strict
        self.estado = ESTADO_NO_INICIADO
        self.registro = RegistroModulos()
        self.errores_arranque: List[str] = []
        self.advertencias: List[str] = []
        self.fallos: List[Dict[str, Any]] = []
        self.resultados_evaluacion: List[Any] = []
        self._trazas: List[Dict[str, Any]] = []
        self._traza_seq = 0
        self._mapa_ruta: List[Dict[str, Any]] = []
        self._ruta_seq = 0

        # PRIORIDAD ABSOLUTA. Creación diferida para evitar un Engine parcial.
        self._centinela: Optional[Centinela] = None

        self._modulos_descubiertos: List[Path] = []
        self._reportes_modulos: Dict[str, Any] = {}
        self._diagnosticos: Dict[str, Any] = {}
        self._inventarios: Dict[str, Any] = {}
        self._dependencias: Dict[str, Any] = {}
        self._grafo: Dict[str, Any] = {}

        self._modulos_descubiertos = self._descubrir_modulos()
        self._cargar_y_validar()
        self._resolver_dependencias()
        self._construir_grafo()

        if self.errores_arranque:
            self.estado = ESTADO_RECHAZADO
            if self.strict:
                raise ArranqueError(
                    "Engine no pudo arrancar:\n  - " + "\n  - ".join(self.errores_arranque)
                )
        else:
            self.estado = ESTADO_OPERATIVO

    # -----------------------------------------------------------
    # DESCUBRIMIENTO / LECTURA
    # -----------------------------------------------------------
    def _descubrir_modulos(self) -> List[Path]:
        if not self.raiz.is_dir():
            return []
        return [
            p for p in sorted(self.raiz.iterdir())
            if p.is_dir() and (p / "__init__.py").is_file()
        ]

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
                self.errores_arranque.append(
                    f"{path_dir.name}: CONTENEDOR ausente o no es dict"
                )
                return None
            return {
                "meta": meta,
                "modulo": mod,
                "ruta": init_path,
                "nombre_carpeta": path_dir.name,
            }
        except Exception as e:
            self.errores_arranque.append(
                f"{path_dir.name}: error al cargar → {type(e).__name__}: {e}"
            )
            return None

    # -----------------------------------------------------------
    # VERSIONES / CONTRATO
    # -----------------------------------------------------------
    @staticmethod
    def _parse_version(s: str) -> Optional[Tuple[int, ...]]:
        m = re.match(r"^(\d+(?:\.\d+)*)", str(s).strip())
        if not m:
            return None
        try:
            return tuple(int(x) for x in m.group(1).split("."))
        except ValueError:
            return None

    def _comparar_api(self, declarado: str) -> Optional[str]:
        raw = str(declarado).strip()
        if not raw:
            return "api_engine vacío"
        exacto = not raw.startswith(">=")
        ver_str = raw[2:].strip() if raw.startswith(">=") else raw
        requerida = self._parse_version(ver_str)
        actual = self._parse_version(API_ENGINE_ACTUAL)
        if requerida is None:
            return f"api_engine no parseable: '{declarado}'"
        if actual is None:
            return f"API_ENGINE_ACTUAL inválida: '{API_ENGINE_ACTUAL}'"
        n = max(len(requerida), len(actual))
        requerida += (0,) * (n - len(requerida))
        actual += (0,) * (n - len(actual))
        if exacto and actual != requerida:
            return f"api_engine exige exactamente {ver_str}, Engine es {API_ENGINE_ACTUAL}"
        if not exacto and actual < requerida:
            return f"api_engine exige >={ver_str}, Engine es {API_ENGINE_ACTUAL}"
        return None

    def _comparar_compatible_desde(self, declarado: str, nombre: str) -> Optional[str]:
        raw = str(declarado).strip()
        if not raw:
            return f"{nombre}: compatible_desde vacío"
        requerida = self._parse_version(raw)
        actual = self._parse_version(VERSION_ENGINE)
        if requerida is None:
            return f"{nombre}: compatible_desde no parseable: '{declarado}'"
        if actual is None:
            return None
        n = max(len(requerida), len(actual))
        requerida += (0,) * (n - len(requerida))
        actual += (0,) * (n - len(actual))
        if actual < requerida:
            return f"{nombre}: compatible_desde={raw} pero Engine es {VERSION_ENGINE}"
        return None

    def _validar_lista_str(self, meta: Dict[str, Any], clave: str, nombre: str) -> List[str]:
        errores: List[str] = []
        val = meta.get(clave)
        if not isinstance(val, list):
            return [f"{nombre}: '{clave}' debe ser list"]
        for i, item in enumerate(val):
            if not isinstance(item, str):
                errores.append(f"{nombre}: '{clave}[{i}]' debe ser str, es {type(item).__name__}")
        return errores

    def _validar_esquema(self, meta: Dict[str, Any], nombre: str) -> List[str]:
        errores: List[str] = []
        if meta.get("esquema") != ESQUEMA_CONTRATO_REQUERIDO:
            errores.append(f"{nombre}: esquema '{meta.get('esquema')}' != '{ESQUEMA_CONTRATO_REQUERIDO}'")
        if str(meta.get("version_contrato")) != VERSION_CONTRATO_REQUERIDA:
            errores.append(f"{nombre}: version_contrato '{meta.get('version_contrato')}' != '{VERSION_CONTRATO_REQUERIDA}'")
        vm = meta.get("version_modulo")
        if not isinstance(vm, str) or not vm.strip():
            errores.append(f"{nombre}: version_modulo debe ser str no vacío, es {type(vm).__name__}")
        for clave in CLAVES_OBLIGATORIAS_CONTRATO:
            if clave not in meta:
                errores.append(f"{nombre}: falta clave obligatoria '{clave}'")
        for clave in LISTAS_STR_OBLIGATORIAS:
            if clave in meta:
                errores.extend(self._validar_lista_str(meta, clave, nombre))

        requiere = meta.get("requiere")
        if not isinstance(requiere, list):
            errores.append(f"{nombre}: 'requiere' debe ser list")
        else:
            for i, item in enumerate(requiere):
                if not isinstance(item, str):
                    errores.append(f"{nombre}: 'requiere[{i}]' debe ser str, es {type(item).__name__}")

        caps = meta.get("capacidades")
        if not isinstance(caps, dict):
            errores.append(f"{nombre}: 'capacidades' debe ser dict")
            caps = {}
        else:
            for k, v in caps.items():
                if not callable(v):
                    errores.append(f"{nombre}: capacidad '{k}' no es callable (tipo={type(v).__name__})")

        meta_caps = meta.get("capacidades_meta")
        if not isinstance(meta_caps, dict):
            errores.append(f"{nombre}: 'capacidades_meta' debe ser dict")
        else:
            for k in caps:
                if k not in meta_caps:
                    errores.append(f"{nombre}: capacidad '{k}' sin entrada en capacidades_meta")
                    continue
                item = meta_caps[k]
                if not isinstance(item, dict):
                    errores.append(f"{nombre}: capacidades_meta['{k}'] debe ser dict, es {type(item).__name__}")
                    continue
                for campo in CLAVES_META_CAPACIDAD:
                    if campo not in item:
                        errores.append(f"{nombre}: capacidades_meta['{k}'] falta '{campo}'")
                    elif not isinstance(item[campo], str):
                        errores.append(f"{nombre}: capacidades_meta['{k}']['{campo}'] debe ser str")

        auth = meta.get("autoriza_engine")
        if not isinstance(auth, dict):
            errores.append(f"{nombre}: 'autoriza_engine' debe ser dict")
        else:
            for permiso in PERMISOS_AUTORIZA_ENGINE:
                if permiso not in auth:
                    errores.append(f"{nombre}: autoriza_engine falta permiso '{permiso}'")
                elif not isinstance(auth[permiso], bool):
                    errores.append(f"{nombre}: autoriza_engine['{permiso}'] debe ser bool, es {type(auth[permiso]).__name__}")
            extras = set(auth) - set(PERMISOS_AUTORIZA_ENGINE)
            if extras:
                errores.append(f"{nombre}: autoriza_engine permisos desconocidos: {sorted(extras)}")

        reporting = meta.get("reporting")
        if not isinstance(reporting, dict):
            errores.append(f"{nombre}: 'reporting' debe ser dict")
        else:
            for bandera in BANDERAS_REPORTING:
                if bandera not in reporting:
                    errores.append(f"{nombre}: reporting falta bandera '{bandera}'")
                elif not isinstance(reporting[bandera], bool):
                    errores.append(f"{nombre}: reporting['{bandera}'] debe ser bool, es {type(reporting[bandera]).__name__}")

        ev = meta.get("estados_validos")
        if not isinstance(ev, list):
            errores.append(f"{nombre}: 'estados_validos' debe ser list")
        elif not ev:
            errores.append(f"{nombre}: 'estados_validos' no puede estar vacío")
        else:
            for i, est in enumerate(ev):
                if not isinstance(est, str):
                    errores.append(f"{nombre}: estados_validos[{i}] debe ser str")
                elif est not in ESTADOS_CANONICOS:
                    errores.append(f"{nombre}: estados_validos[{i}]='{est}' no es canónico. Admitidos: {ESTADOS_CANONICOS}")

        err = self._comparar_api(str(meta.get("api_engine", "")))
        if err:
            errores.append(f"{nombre}: {err}")
        err = self._comparar_compatible_desde(str(meta.get("compatible_desde", "")), nombre)
        if err:
            errores.append(err)
        return errores

    def _cargar_y_validar(self) -> None:
        for path_dir in self._modulos_descubiertos:
            leido = self._leer_contrato(path_dir)
            if leido is None:
                continue
            meta = leido["meta"]
            nombre = meta.get("nombre") or leido["nombre_carpeta"]
            errores = self._validar_esquema(meta, nombre)
            if errores:
                self.errores_arranque.extend(errores)
                continue
            cont = Contenedor(meta, leido["modulo"], leido["ruta"])
            for error in self.registro.registrar(cont):
                self.errores_arranque.append(f"{nombre}: {error}")

    # -----------------------------------------------------------
    # DEPENDENCIAS / GRAFO
    # -----------------------------------------------------------
    def _resolver_dependencias(self) -> None:
        presentes = set(self.registro.por_rol) | set(self.registro.por_id) | set(self.registro.contenedores)
        faltantes: Dict[str, List[str]] = defaultdict(list)
        grafo_dep: Dict[str, List[str]] = defaultdict(list)
        for nombre, cont in self.registro.contenedores.items():
            for dep in cont.requiere:
                grafo_dep[nombre].append(dep)
                if dep not in presentes:
                    faltantes[nombre].append(dep)
                    self.errores_arranque.append(f"{cont.rol}/{nombre}: dependencia inexistente → '{dep}'")
        in_degree = {n: 0 for n in self.registro.contenedores}
        for dests in grafo_dep.values():
            for d in dests:
                if d in in_degree:
                    in_degree[d] += 1
        cola = deque(n for n, deg in in_degree.items() if deg == 0)
        orden: List[str] = []
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

    def _construir_grafo(self) -> None:
        nodos: List[Dict[str, Any]] = []
        aristas: List[Dict[str, Any]] = []
        for nombre, cont in self.registro.contenedores.items():
            nodos.append({"id": cont.id or nombre, "nombre": nombre, "rol": cont.rol, "tipo": "modulo"})
            for dep in cont.requiere:
                aristas.append({"from": nombre, "to": dep, "tipo": "requiere"})
            for cap in cont.capacidades:
                cap_id = f"{nombre}.{cap}"
                nodos.append({"id": cap_id, "nombre": cap, "tipo": "capacidad", "modulo": nombre})
                aristas.append({"from": nombre, "to": cap_id, "tipo": "declara_capacidad"})
        self._grafo = {"nodos": nodos, "aristas": aristas}

    # -----------------------------------------------------------
    # CENSO / TRAZAS / RUTA
    # -----------------------------------------------------------
    def censar(self) -> Dict[str, Any]:
        return {
            "total": self.registro.total(),
            "roles": {rol: [c.nombre for c in lista] for rol, lista in self.registro.por_rol.items()},
            "roles_vacios": [],
            "rechazados": list(self.errores_arranque),
            "cargados": [
                {"id": c.id, "nombre": c.nombre, "rol": c.rol, "version": c.version,
                 "esquema": c.esquema, "estabilidad": c.estabilidad,
                 "capacidades": list(c.capacidades)}
                for c in self.registro.contenedores.values()
            ],
        }

    def _registrar_traza(self, modulo: str, capacidad: str, estado: str,
                         duracion_s: float, error: Optional[str] = None, **extras: Any) -> None:
        self._traza_seq += 1
        entrada: Dict[str, Any] = {
            "id_traza": self._traza_seq,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "modulo": modulo,
            "capacidad": capacidad,
            "estado": estado,
            "duracion_s": duracion_s,
        }
        if error is not None:
            entrada["error"] = error
        for clave, valor in extras.items():
            if valor is not None:
                entrada[clave] = valor
        self._trazas.append(entrada)

    def obtener_trazas(self) -> Tuple[Dict[str, Any], ...]:
        return tuple(dict(t) for t in self._trazas)

    def _registrar_ruta(self, *, modulo: str, rol: str, id_modulo: str,
                        capacidad: str, entrada: Any, estado: str,
                        contenedor_resuelto: bool, contrato_resuelto: bool,
                        capacidad_resuelta: bool, funcion_invocada: bool,
                        contenido_entregado: bool, contenido_recibido: bool,
                        resultado: Any = None, error: Optional[str] = None) -> None:
        self._ruta_seq += 1
        ruta: Dict[str, Any] = {
            "id_ruta": self._ruta_seq,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "modulo": modulo,
            "rol": rol,
            "id_modulo": id_modulo,
            "capacidad": capacidad,
            "estado": estado,
            "frontera": {
                "engine": True,
                "contenedor_resuelto": contenedor_resuelto,
                "contrato_resuelto": contrato_resuelto,
                "capacidad_resuelta": capacidad_resuelta,
                "funcion_invocada": funcion_invocada,
                "contenido_entregado": contenido_entregado,
                "contenido_recibido": contenido_recibido,
                "resultado_producido": resultado is not None,
            },
            "entrada": entrada,
            "resultado": resultado,
        }
        if error is not None:
            ruta["error"] = error
        self._mapa_ruta.append(ruta)

    def obtener_mapa_ruta(self) -> Tuple[Dict[str, Any], ...]:
        return tuple(dict(r) for r in self._mapa_ruta)

    # -----------------------------------------------------------
    # RESOLUCIÓN / EJECUCIÓN CONTRACTUAL
    # -----------------------------------------------------------
    def _resolver_contenedor(self, modulo_o_rol: Any) -> Tuple[Optional[Contenedor], Optional[str]]:
        if isinstance(modulo_o_rol, Contenedor):
            return modulo_o_rol, None
        if not isinstance(modulo_o_rol, str):
            return None, f"Módulo/rol no encontrado: {modulo_o_rol}"
        cont = self.registro.primero(modulo_o_rol)
        if cont is None:
            return None, f"Módulo/rol no encontrado: {modulo_o_rol}"
        return cont, None

    def _validar_entrada_capacidad(self, cont: Contenedor, capacidad: str,
                                   args: Tuple[Any, ...], kwargs: Dict[str, Any]) -> Optional[str]:
        fn = cont.fn(capacidad)
        if not callable(fn):
            return f"Capacidad '{capacidad}' no es ejecutable en {cont.nombre}"
        try:
            inspect.signature(fn).bind(*args, **kwargs)
        except ValueError:
            pass
        except TypeError as e:
            return f"Entrada incompatible con capacidad '{capacidad}': {e}"
        return None

    def ejecutar_capacidad(self, modulo_o_rol: Any, capacidad: str, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """Ejecuta SOLO una capacidad declarada y autorizada por el contrato real."""
        entrada = {"args": args, "kwargs": kwargs}
        cont, error = self._resolver_contenedor(modulo_o_rol)
        if cont is None:
            self._registrar_ruta(modulo=str(modulo_o_rol), rol="", id_modulo="", capacidad=capacidad,
                                 entrada=entrada, estado="ERROR", contenedor_resuelto=False,
                                 contrato_resuelto=False, capacidad_resuelta=False,
                                 funcion_invocada=False, contenido_entregado=False,
                                 contenido_recibido=False, error=error)
            return {"estado": "ERROR", "error": error}

        # Autorización positiva: solamente True autoriza.
        if cont.autoriza_engine.get("ejecutar") is not True:
            error = f"{cont.nombre}: el contrato no autoriza la ejecución por Engine"
            self._registrar_ruta(modulo=cont.nombre, rol=cont.rol, id_modulo=cont.id,
                                 capacidad=capacidad, entrada=entrada, estado="RECHAZADO",
                                 contenedor_resuelto=True, contrato_resuelto=False,
                                 capacidad_resuelta=False, funcion_invocada=False,
                                 contenido_entregado=False, contenido_recibido=False, error=error)
            return {"estado": "RECHAZADO", "modulo": cont.nombre, "rol": cont.rol,
                    "id": cont.id, "capacidad": capacidad, "error": error}

        # La capacidad debe existir en el contrato y ser callable.
        fn = cont.fn(capacidad)
        if not callable(fn):
            error = f"{cont.nombre}: la capacidad '{capacidad}' no es callable"
            self._registrar_ruta(modulo=cont.nombre, rol=cont.rol, id_modulo=cont.id,
                                 capacidad=capacidad, entrada=entrada, estado="RECHAZADO",
                                 contenedor_resuelto=True, contrato_resuelto=True,
                                 capacidad_resuelta=False, funcion_invocada=False,
                                 contenido_entregado=False, contenido_recibido=False, error=error)
            return {"estado": "RECHAZADO", "modulo": cont.nombre, "rol": cont.rol,
                    "id": cont.id, "capacidad": capacidad, "error": error}

        error_entrada = self._validar_entrada_capacidad(cont, capacidad, args, kwargs)
        if error_entrada:
            self._registrar_ruta(modulo=cont.nombre, rol=cont.rol, id_modulo=cont.id,
                                 capacidad=capacidad, entrada=entrada, estado="ERROR_ENTRADA",
                                 contenedor_resuelto=True, contrato_resuelto=True,
                                 capacidad_resuelta=True, funcion_invocada=False,
                                 contenido_entregado=False, contenido_recibido=False,
                                 error=error_entrada)
            return {"estado": "ERROR_ENTRADA", "modulo": cont.nombre, "rol": cont.rol,
                    "id": cont.id, "capacidad": capacidad, "error": error_entrada}

        contenido_entregado = bool(args) or bool(kwargs)
        inicio = time.perf_counter()
        funcion_invocada = False
        self._registrar_ruta(modulo=cont.nombre, rol=cont.rol, id_modulo=cont.id,
                             capacidad=capacidad, entrada=entrada, estado="ENTRADA_VALIDADA",
                             contenedor_resuelto=True, contrato_resuelto=True,
                             capacidad_resuelta=True, funcion_invocada=False,
                             contenido_entregado=contenido_entregado, contenido_recibido=False)
        try:
            funcion_invocada = True
            self._registrar_ruta(modulo=cont.nombre, rol=cont.rol, id_modulo=cont.id,
                                 capacidad=capacidad, entrada=entrada, estado="INVOCANDO",
                                 contenedor_resuelto=True, contrato_resuelto=True,
                                 capacidad_resuelta=True, funcion_invocada=True,
                                 contenido_entregado=contenido_entregado, contenido_recibido=False)
            resultado = fn(*args, **kwargs)
            duracion = round(time.perf_counter() - inicio, 6)
            self._registrar_ruta(modulo=cont.nombre, rol=cont.rol, id_modulo=cont.id,
                                 capacidad=capacidad, entrada=entrada, resultado=resultado,
                                 estado="RESULTADO_RECIBIDO", contenedor_resuelto=True,
                                 contrato_resuelto=True, capacidad_resuelta=True,
                                 funcion_invocada=True, contenido_entregado=contenido_entregado,
                                 contenido_recibido=True)
            self._registrar_traza(cont.nombre, capacidad, "EXITO", duracion)
            salida = {"estado": "EXITO", "modulo": cont.nombre, "rol": cont.rol,
                      "id": cont.id, "capacidad": capacidad, "resultado": resultado,
                      "duracion_s": duracion}
            self.resultados_evaluacion.append(salida)
            return salida
        except Exception as e:
            duracion = round(time.perf_counter() - inicio, 6)
            error_msg = f"{type(e).__name__}: {e}"
            self._registrar_traza(cont.nombre, capacidad, "ERROR_EJECUCION", duracion, error_msg)
            self._registrar_ruta(modulo=cont.nombre, rol=cont.rol, id_modulo=cont.id,
                                 capacidad=capacidad, entrada=entrada, estado="ERROR_EJECUCION",
                                 contenedor_resuelto=True, contrato_resuelto=True,
                                 capacidad_resuelta=True, funcion_invocada=funcion_invocada,
                                 contenido_entregado=contenido_entregado,
                                 contenido_recibido=False, error=error_msg)
            salida = {"estado": "ERROR_EJECUCION", "modulo": cont.nombre, "rol": cont.rol,
                      "id": cont.id, "capacidad": capacidad, "error": error_msg,
                      "duracion_s": duracion}
            self.resultados_evaluacion.append(salida)
            return salida

    def ejecutar_reporte(self, modulo_o_rol: Any) -> Dict[str, Any]:
        return self.ejecutar_capacidad(modulo_o_rol, "reporte")

    def ejecutar_diagnostico(self, modulo_o_rol: Any) -> Dict[str, Any]:
        return self.ejecutar_capacidad(modulo_o_rol, "diagnostico")

    def ejecutar_inventario(self, modulo_o_rol: Any) -> Dict[str, Any]:
        return self.ejecutar_capacidad(modulo_o_rol, "inventario")

    def ejecutar_con_contexto_unificado(self, modulo_o_rol: Any, capacidad: str,
                                        payload: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(payload, dict):
            return {"estado": "ERROR", "error": f"payload debe ser dict, es {type(payload).__name__}"}
        return self.ejecutar_capacidad(modulo_o_rol, capacidad, payload)

    # -----------------------------------------------------------
    # INVOCADOR OFICIAL
    # -----------------------------------------------------------
    def invocar(self, modulo: Any, capacidad: str, *args: Any, **kwargs: Any) -> Any:
        """Frontera oficial usada por Centinela; nunca importa módulos de dominio directamente."""
        salida = self.ejecutar_capacidad(modulo, capacidad, *args, **kwargs)
        if isinstance(salida, dict) and salida.get("estado") == "EXITO":
            return salida.get("resultado")
        if isinstance(salida, dict) and "error" in salida:
            raise RuntimeError(str(salida.get("error")))
        return salida

    # -----------------------------------------------------------
    # CONSOLIDACIÓN
    # -----------------------------------------------------------
    def consolidar_reportes(self) -> Dict[str, Any]:
        for nombre, cont in self.registro.contenedores.items():
            if "reporte" in cont.capacidades:
                r = self.ejecutar_capacidad(nombre, "reporte")
                self._reportes_modulos[nombre] = (
                    r.get("resultado") if r.get("estado") == "EXITO"
                    else {"error": r.get("error"), "estado": "NO ENTREGADO POR MODULO"}
                )
            if "diagnostico" in cont.capacidades:
                d = self.ejecutar_capacidad(nombre, "diagnostico")
                if d.get("estado") == "EXITO":
                    self._diagnosticos[nombre] = d.get("resultado")
            if "inventario" in cont.capacidades:
                inv = self.ejecutar_capacidad(nombre, "inventario")
                if inv.get("estado") == "EXITO":
                    self._inventarios[nombre] = inv.get("resultado")
        return {"reportes": self._reportes_modulos, "diagnosticos": self._diagnosticos,
                "inventarios": self._inventarios}

    # -----------------------------------------------------------
    # PAQUETE OMEGA
    # -----------------------------------------------------------
    def paquete_omega(self) -> Dict[str, Any]:
        if not self._reportes_modulos:
            self.consolidar_reportes()
        reportes: List[Dict[str, Any]] = [{
            "id": "metadata", "titulo": "INFORMACIÓN DEL RUN", "orden": 0,
            "contenido": {
                "version_engine": self.VERSION,
                "esquema_contrato": ESQUEMA_CONTRATO_REQUERIDO,
                "version_contrato_requerida": VERSION_CONTRATO_REQUERIDA,
                "api_engine": API_ENGINE_ACTUAL, "estado_engine": self.estado,
                "invocador_id": self.invocador_id, "total_modulos": self.registro.total(),
                "errores_arranque": list(self.errores_arranque),
                "advertencias": list(self.advertencias),
                "trazas_n": len(self._trazas), "rutas_n": len(self._mapa_ruta),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        }]
        orden = 1
        for nombre in sorted(self.registro.contenedores):
            cont = self.registro.contenedores[nombre]
            reportes.append({
                "id": cont.id or nombre,
                "titulo": f"MÓDULO {cont.rol}/{nombre}",
                "orden": orden,
                "contenido": {
                    "id": cont.id, "nombre": cont.nombre, "rol": cont.rol,
                    "version": cont.version, "version_contrato": cont.version_contrato,
                    "esquema": cont.esquema, "estabilidad": cont.estabilidad,
                    "compatible_desde": cont.compatible_desde, "api_engine": cont.api_engine,
                    "descripcion": cont.descripcion, "funcion": cont.funcion,
                    "no_hace": cont.no_hace, "autoridad": cont.autoridad,
                    "conocimiento_exportable": cont.conocimiento_exportable,
                    "consultas_soportadas": cont.consultas_soportadas,
                    "requiere": cont.requiere, "autoriza_engine": cont.autoriza_engine,
                    "capacidades": list(cont.capacidades),
                    "capacidades_meta": cont.capacidades_meta,
                    "reporting": cont.reporting,
                    "estados_validos": cont.estados_validos,
                    "invariantes": cont.invariantes,
                    "reporte": self._reportes_modulos.get(nombre),
                    "diagnostico": self._diagnosticos.get(nombre),
                    "inventario": self._inventarios.get(nombre),
                },
            })
            orden += 1
        reportes.extend([
            {"id": "dependencias", "titulo": "DEPENDENCIAS", "orden": orden, "contenido": self._dependencias},
            {"id": "grafo", "titulo": "GRAFO ESTRUCTURAL", "orden": orden + 1, "contenido": self._grafo},
            {"id": "trazas", "titulo": "TRAZAS DE EJECUCIÓN", "orden": orden + 2, "contenido": list(self._trazas)},
            {"id": "mapa_ruta", "titulo": "MAPA DE RUTA DE EJECUCIÓN", "orden": orden + 3, "contenido": list(self._mapa_ruta)},
        ])
        return {
            "metadata": {
                "version_engine": self.VERSION, "estado_engine": self.estado,
                "esquema_contrato": ESQUEMA_CONTRATO_REQUERIDO,
                "total_modulos": self.registro.total(), "trazas_n": len(self._trazas),
                "rutas_n": len(self._mapa_ruta),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
            "reportes": reportes,
        }

    # -----------------------------------------------------------
    # ESTADO GLOBAL
    # -----------------------------------------------------------
    def estado_global(self) -> Dict[str, Any]:
        return {
            "tipo": "estado_global", "version_engine": self.VERSION,
            "esquema_contrato": ESQUEMA_CONTRATO_REQUERIDO, "estado": self.estado,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_contenedores": self.registro.total(),
            "errores_arranque": list(self.errores_arranque),
            "advertencias": list(self.advertencias), "trazas_n": len(self._trazas),
            "rutas_n": len(self._mapa_ruta), "dependencias": self._dependencias,
            "grafo": self._grafo,
        }

    # -----------------------------------------------------------
    # CENTINELA — PRIORIDAD ABSOLUTA
    # -----------------------------------------------------------
    @property
    def centinela(self) -> Centinela:
        """Auditor único y oficial; se instancia después del arranque del Engine."""
        if self._centinela is None:
            self._centinela = Centinela(invocador=self)
        return self._centinela

    def verificar_con_centinela(self, paquete: Dict[str, Any], *,
                                depositar_salida: bool = True) -> Veredicto:
        """Cierre: Engine ejecuta → consolida → paquete → Centinela → Veredicto."""
        if not isinstance(paquete, dict):
            raise TypeError("paquete debe ser dict")
        inicio = time.perf_counter()
        ciclo_id = paquete.get("ciclo_id")
        try:
            veredicto = self.centinela.verificar(
                paquete, depositar_salida=depositar_salida
            )
            duracion = round(time.perf_counter() - inicio, 6)
            self._registrar_traza(
                modulo="ENGINE", capacidad="verificar_con_centinela",
                estado=str(veredicto.estado), duracion_s=duracion,
                ciclo_id=ciclo_id,
            )
            return veredicto
        except Exception as e:
            duracion = round(time.perf_counter() - inicio, 6)
            error = f"{type(e).__name__}: {e}"
            self._registrar_traza(
                modulo="ENGINE", capacidad="verificar_con_centinela",
                estado="ERROR_AUDITORIA", duracion_s=duracion,
                error=error, ciclo_id=ciclo_id,
            )
            raise


# ===============================================================
# EXPORTACIONES
# ===============================================================

__all__ = [
    "Engine", "ArranqueError", "Contenedor", "RegistroModulos",
    "VERSION_ENGINE", "ESQUEMA_CONTRATO_REQUERIDO", "VERSION_CONTRATO_REQUERIDA",
]

# ===============================================================
# FIN DEL MÓDULO ENGINE
# ===============================================================
