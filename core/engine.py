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
    # ===============================================================
    # SECCIÓN: DI
    # ===============================================================
    #
    # Origen
    #   modules/diccionario/__init__.py
    #
    # CONTENEDOR
    #   nombre      : diccionario
    #   rol         : DI
    #   version     : 1.0
    #   requiere    : []
    #   capacidades :
    #     verificar
    #     barrer
    #     inventario
    #     axiomas
    #     resolver
    #     listar
    #     cargar
    #     cargar_todos
    #     definir
    #     significado
    #     inyectar_en_peticion
    #
    # Autoridad
    #   - Lee el CONTENEDOR de modules/diccionario/
    #   - Lee todos los archivos de modules/diccionario/
    #   - Ejecuta solo las capacidades del CONTENEDOR
    #
    # El modulo no calcula Tru ni C/L/K.
    # No clasifica O. No orquesta.
    #
    # ---------------------------------------------------------------
    # subsección: carga del modulo
    # ---------------------------------------------------------------
    def _di_cargar(self) -> None:
        path = self.raiz / "diccionario" / "__init__.py"
        if not path.is_file():
            self.errores_arranque.append(
                "DI: no existe {0}".format(path)
            )
            return

        directorio = path.parent
        nombre_mod = "vpsi_diccionario"
        spec = importlib.util.spec_from_file_location(
            nombre_mod,
            path,
            submodule_search_locations=[str(directorio)],
        )
        if spec is None or spec.loader is None:
            self.errores_arranque.append("DI: no se pudo crear spec")
            return

        mod = importlib.util.module_from_spec(spec)
        sys.modules[nombre_mod] = mod
        try:
            spec.loader.exec_module(mod)
        except Exception as e:
            self.errores_arranque.append(
                "DI: import fallo: {0}: {1}".format(type(e).__name__, e)
            )
            return

        meta = getattr(mod, "CONTENEDOR", None)
        if not isinstance(meta, dict):
            self.errores_arranque.append("DI: sin CONTENEDOR")
            return

        if meta.get("nombre") != "diccionario":
            self.errores_arranque.append(
                "DI: nombre inesperado: {0}".format(meta.get("nombre"))
            )
            return

        if meta.get("rol") != "DI":
            self.errores_arranque.append(
                "DI: rol inesperado: {0}".format(meta.get("rol"))
            )
            return

        caps = meta.get("capacidades")
        if not isinstance(caps, dict) or not caps:
            self.errores_arranque.append("DI: sin capacidades")
            return

        self._di_mod = mod
        self._di_meta = dict(meta)
        self._di_ruta = path
        self._di_caps = dict(caps)

        for nombre, ref in self._di_caps.items():
            fn = ref if callable(ref) else getattr(mod, str(ref), None)
            if not callable(fn):
                self.errores_arranque.append(
                    "DI: capacidad no resoluble: {0}".format(nombre)
                )

    # ---------------------------------------------------------------
    # subsección: todos los archivos del modulo
    # ---------------------------------------------------------------
    def _di_listar_archivos(self) -> List[str]:
        if self._di_ruta is None:
            return []
        directorio = Path(self._di_ruta).resolve().parent
        return sorted(
            str(p.relative_to(directorio))
            for p in directorio.rglob("*")
            if p.is_file()
        )

    def di_archivos(self) -> List[str]:
        if not getattr(self, "_di_archivos", None):
            self._di_archivos = self._di_listar_archivos()
        return list(self._di_archivos)

    # ---------------------------------------------------------------
    # subsección: invocacion por contrato
    # ---------------------------------------------------------------
    def _di_fn(self, capacidad: str):
        if capacidad not in getattr(self, "_di_caps", {}):
            return None
        ref = self._di_caps[capacidad]
        if callable(ref):
            return ref
        if getattr(self, "_di_mod", None) is None:
            return None
        return getattr(self._di_mod, str(ref), None)

    def _di_ejecutar(self, capacidad: str, *args, **kwargs):
        fn = self._di_fn(capacidad)
        if not callable(fn):
            self.fallos.append({
                "seccion": "DI",
                "capacidad": capacidad,
                "razon": "no resoluble",
            })
            return None
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            self.fallos.append({
                "seccion": "DI",
                "capacidad": capacidad,
                "razon": "{0}: {1}".format(type(e).__name__, e),
                "traza": traceback.format_exc(limit=3),
            })
            return None

    # ---------------------------------------------------------------
    # subsección: capacidad — barrer
    # ---------------------------------------------------------------
    def di_barrer(self):
        out = self._di_ejecutar("barrer")
        return out if isinstance(out, dict) else None

    # ---------------------------------------------------------------
    # subsección: capacidad — verificar
    # ---------------------------------------------------------------
    def di_verificar(self):
        out = self._di_ejecutar("verificar")
        return out if isinstance(out, dict) else None

    # ---------------------------------------------------------------
    # subsección: capacidad — inventario
    # ---------------------------------------------------------------
    def di_inventario(self, peticion=None):
        out = self._di_ejecutar("inventario", peticion)
        if not isinstance(out, dict):
            return None
        out = dict(out)
        out["archivos_modulo"] = self.di_archivos()
        out["archivos_n"] = len(out["archivos_modulo"])
        out["contrato"] = {
            "nombre": self._di_meta.get("nombre"),
            "rol": self._di_meta.get("rol"),
            "version": self._di_meta.get("version"),
            "requiere": list(self._di_meta.get("requiere") or []),
            "capacidades": sorted(self._di_caps.keys()),
        }
        return out

    # ---------------------------------------------------------------
    # subsección: capacidad — axiomas
    # ---------------------------------------------------------------
    def di_axiomas(self):
        out = self._di_ejecutar("axiomas")
        return list(out) if isinstance(out, list) else []

    # ---------------------------------------------------------------
    # subsección: capacidad — resolver
    # ---------------------------------------------------------------
    def di_resolver(self, peticion=None):
        out = self._di_ejecutar("resolver", peticion)
        return out if isinstance(out, dict) else None

    # ---------------------------------------------------------------
    # subsección: capacidad — listar
    # ---------------------------------------------------------------
    def di_listar(self):
        out = self._di_ejecutar("listar")
        return list(out) if isinstance(out, list) else []

    # ---------------------------------------------------------------
    # subsección: capacidad — cargar
    # ---------------------------------------------------------------
    def di_cargar(self, nombre):
        return self._di_ejecutar("cargar", nombre)

    # ---------------------------------------------------------------
    # subsección: capacidad — cargar_todos
    # ---------------------------------------------------------------
    def di_cargar_todos(self):
        out = self._di_ejecutar("cargar_todos")
        return out if isinstance(out, dict) else {}

    # ---------------------------------------------------------------
    # subsección: capacidad — definir
    # ---------------------------------------------------------------
    def di_definir(self, palabra, *nombres):
        out = self._di_ejecutar("definir", palabra, *nombres)
        return out if isinstance(out, dict) else None

    # ---------------------------------------------------------------
    # subsección: capacidad — significado
    # ---------------------------------------------------------------
    def di_significado(self, palabra, *nombres):
        out = self._di_ejecutar("significado", palabra, *nombres)
        return out if isinstance(out, str) else None

    # ---------------------------------------------------------------
    # subsección: capacidad — inyectar_en_peticion
    # ---------------------------------------------------------------
    def di_inyectar_en_peticion(
        self,
        peticion=None,
        *nombres,
        clave="diccionario",
    ):
        out = self._di_ejecutar(
            "inyectar_en_peticion",
            peticion,
            *nombres,
            clave=clave,
        )
        return out if isinstance(out, dict) else None

    # ---------------------------------------------------------------
    # subsección: compuerta
    # ---------------------------------------------------------------
    def _di_compuerta(self) -> None:
        if getattr(self, "_di_mod", None) is None:
            if not any(e.startswith("DI:") for e in self.errores_arranque):
                self.errores_arranque.append("DI: modulo no cargado")
            return

        self._di_archivos = self._di_listar_archivos()
        if not self._di_archivos:
            self.errores_arranque.append("DI: carpeta sin archivos")

        informe = self.di_barrer()
        if informe is None:
            informe = self.di_verificar()

        if informe is None:
            self.errores_arranque.append("DI: barrer/verificar no resolvio")
            return

        if not informe.get("coherente", False):
            self.errores_arranque.append(
                "DI: incoherente errores={0}".format(
                    len(informe.get("errores") or [])
                )
            )

    # ===============================================================
    # FIN SECCIÓN: DI
    # ===============================================================
"""
modules/diccionario/__init__.py
===============================

Rol DI — Diccionario (biblioteca de definiciones / invariante de significado).

FUNCIÓN
  Herramienta de definiciones para contrastar y correlacionar a nivel
  léxico-significado. Materia prima: palabra → definición → significado.

  Busca definiciones. No crea el contexto (eso es CX).
  No correlaciona numéricamente (eso es CA/K).
  Entrega la definición para que el resto del sistema pueda
  armar contexto y correlacionar con base léxica explícita.

  Lee automáticamente todos los archivos bajo este módulo
  (fuentes/ y *.py del directorio que declaren DICCIONARIO).
  No hace falta editar este init al agregar un idioma, un glosario
  o más entradas.

AGENCIA DE ENGINE
  Engine tiene libertad de solicitar definiciones y llevarlas a
  cualquier módulo según el contexto del ciclo (CX, CA, RE, CIT, …).
  Eso no convierte a Engine en dueño del significado: el resultado
  final (C, L, K, Tru) no depende de que Engine invente definiciones.
  Depende de los contratos de cada módulo y de la materia prima que
  DI entrega. Análogo: poner la fórmula de la verdad al alcance de
  Engine no hace que Engine “sea” FO; solo la invoca. Aquí igual:
  Engine invoca definiciones; DI las posee como invariante.

NO HACE
  - Calcular C, L, K, Tru_Ri ni Tru_total.
  - Clasificar O_context (CX).
  - Traer material externo de dominios (RE).
  - Orquestar el ciclo (Engine).
  - Sustituir AX, MC, CA, FO, CIT.

CONTRATO DE FUENTES (archivos debajo)
  Cada archivo puede declarar:
    META        dict  → nombre, idioma, tipo, version, descripcion
    DICCIONARIO dict  → {
        "palabra": {
            "definicion": str,
            "significado": str,   # opcional
            "tipo": str,          # opcional
        },
        ...
    }

  Tipo habitual:
    - definiciones   → diccionario literal de un idioma (es, en, …)
    - glosario_invariante → términos del repositorio (glosario_vpsi)

  El init valida forma mínima. Archivo incoherente → error en barrer;
  no tumba el resto de fuentes.

Las fuentes base viajan con el paquete (offline / CI).
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

try:
    from core.diagnostico import DiagnosticoGlobal
except Exception:  # pragma: no cover
    class DiagnosticoGlobal:
        @staticmethod
        def recibir_reporte(*args, **kwargs):
            pass

_DIR = Path(__file__).parent
_FUENTES = _DIR / "fuentes"

VERSION = "1.0"

# ===============================================================
# ESTADO (se llena solo por descubrimiento — nada arriba nombra abajo)
# ===============================================================
_REGISTRO: Dict[str, Any] = {}
_META: Dict[str, Dict[str, Any]] = {}
_CARGADO = False


# ===============================================================
# NORMALIZACIÓN
# ===============================================================
def _norm_nombre(nombre: str) -> str:
    return (nombre or "").strip().lower().replace("-", "_").replace(" ", "_")


def _norm_palabra(p: str) -> str:
    return (p or "").strip().lower()


def _extraer_definicion(entrada: Any) -> Optional[str]:
    if entrada is None:
        return None
    if isinstance(entrada, str):
        return entrada.strip() or None
    if isinstance(entrada, dict):
        for k in ("definicion", "definición", "def", "meaning", "significado"):
            v = entrada.get(k)
            if v is not None and str(v).strip():
                return str(v).strip()
    return None


def _extraer_significado(entrada: Any) -> Optional[str]:
    if not isinstance(entrada, dict):
        return _extraer_definicion(entrada)
    for k in ("significado", "meaning", "interpretacion", "interpretación"):
        v = entrada.get(k)
        if v is not None and str(v).strip():
            return str(v).strip()
    return _extraer_definicion(entrada)


# ===============================================================
# DESCUBRIMIENTO — lee todos los archivos debajo del módulo
# ===============================================================
def _cargar_modulo(path: Path, clave: str) -> Optional[Any]:
    spec = importlib.util.spec_from_file_location(clave, path)
    if spec is None or spec.loader is None:
        return None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[clave] = mod
    try:
        spec.loader.exec_module(mod)
    except Exception:
        return None
    return mod


def _descubrir() -> None:
    """
    Recorre fuentes/ y *.py del directorio del módulo.
    Registra todo lo que declare DICCIONARIO.
    No hay lista manual de archivos en este init.
    """
    global _CARGADO
    if _CARGADO:
        return

    candidatos: List[Path] = []
    if _FUENTES.is_dir():
        candidatos.extend(sorted(_FUENTES.glob("*.py")))
    candidatos.extend(sorted(_DIR.glob("*.py")))

    vistos: Set[Path] = set()
    for f in candidatos:
        if f.name == "__init__.py" or f.name.startswith("_"):
            continue
        resolved = f.resolve()
        if resolved in vistos:
            continue
        vistos.add(resolved)

        clave = "diccionario_{0}".format(f.stem)
        mod = _cargar_modulo(f, clave)
        if mod is None:
            _META[f.stem] = {"error": "carga fallida", "archivo": f.name}
            continue

        datos = getattr(mod, "DICCIONARIO", None)
        if datos is None:
            continue

        meta = getattr(mod, "META", None)
        nombre = None
        if isinstance(meta, dict):
            nombre = meta.get("nombre")
        if not nombre:
            nombre = f.stem
        key = _norm_nombre(str(nombre))

        _REGISTRO[key] = datos
        if isinstance(meta, dict):
            _META[key] = dict(meta)
            _META[key]["archivo"] = f.name
        else:
            _META[key] = {"nombre": key, "archivo": f.name}

    _CARGADO = True


def _asegurar() -> None:
    _descubrir()


# ===============================================================
# API — materia prima de definiciones
# ===============================================================
def listar() -> List[str]:
    """Nombres de todos los diccionarios/glosarios descubiertos debajo."""
    _asegurar()
    return sorted(_REGISTRO.keys())


def listar_por_idioma(idioma: str) -> List[str]:
    _asegurar()
    idioma = (idioma or "").strip().lower()
    out = []
    for k, m in _META.items():
        if k in _REGISTRO and str(m.get("idioma", "")).lower() == idioma:
            out.append(k)
    return sorted(out)


def meta(nombre: str) -> Optional[Dict[str, Any]]:
    _asegurar()
    return _META.get(_norm_nombre(nombre))


def cargar(nombre: str) -> Any:
    """Devuelve el DICCIONARIO crudo de una fuente (tal cual está)."""
    _asegurar()
    key = _norm_nombre(nombre)
    if key not in _REGISTRO:
        raise KeyError(
            "diccionario no encontrado: {0!r}. Disponibles: {1}".format(
                nombre, listar()
            )
        )
    return _REGISTRO[key]


def cargar_todos() -> Dict[str, Any]:
    """Todos los diccionarios descubiertos (nombre → datos)."""
    _asegurar()
    return {k: _REGISTRO[k] for k in sorted(_REGISTRO)}


def cargar_idioma(idioma: str) -> Dict[str, Any]:
    return {n: cargar(n) for n in listar_por_idioma(idioma)}


def definir(palabra: str, *nombres: str) -> Optional[Dict[str, Any]]:
    """
    Busca la definición de una palabra.

    Si se pasan nombres de fuentes, solo busca ahí.
    Si no, busca en todos los diccionarios descubiertos.

    Retorno:
      {
        "palabra": str,
        "definicion": str | None,
        "significado": str | None,
        "fuente": str | None,
        "entrada": ...,
      }
    o None si no hay entrada.
    """
    _asegurar()
    p = _norm_palabra(palabra)
    if not p:
        return None

    fuentes = list(nombres) if nombres else listar()
    for nombre in fuentes:
        try:
            datos = cargar(nombre)
        except KeyError:
            continue

        if isinstance(datos, dict):
            for k, v in datos.items():
                if _norm_palabra(str(k)) == p:
                    return {
                        "palabra": p,
                        "definicion": _extraer_definicion(v),
                        "significado": _extraer_significado(v),
                        "fuente": _norm_nombre(nombre),
                        "entrada": v,
                    }
        elif isinstance(datos, (set, frozenset, list, tuple)):
            if p in {_norm_palabra(str(x)) for x in datos}:
                return {
                    "palabra": p,
                    "definicion": None,
                    "significado": None,
                    "fuente": _norm_nombre(nombre),
                    "entrada": p,
                    "nota": "término presente sin definición textual",
                }
    return None


def significado(palabra: str, *nombres: str) -> Optional[str]:
    """Atajo: texto de significado o definición."""
    r = definir(palabra, *nombres)
    if r is None:
        return None
    return r.get("significado") or r.get("definicion")


def palabras(*nombres: str) -> Set[str]:
    """Conjunto de lemas de las fuentes indicadas (o de todas)."""
    _asegurar()
    fuentes = list(nombres) if nombres else listar()
    out: Set[str] = set()
    for nombre in fuentes:
        try:
            datos = cargar(nombre)
        except KeyError:
            continue
        if isinstance(datos, dict):
            out |= {_norm_palabra(str(k)) for k in datos if k}
        elif isinstance(datos, (set, frozenset, list, tuple)):
            out |= {_norm_palabra(str(x)) for x in datos if x}
    return out


def inyectar_en_peticion(
    peticion: Optional[Dict[str, Any]] = None,
    *nombres: str,
    clave: str = "diccionario",
) -> Dict[str, Any]:
    """
    Entrega materia prima léxica a una petición.
    Engine (u otro módulo) puede usar esto para pasar definiciones/lemas
    al resto del ciclo. No calcula. No clasifica O.
    """
    base = dict(peticion or {})
    lemas = sorted(palabras(*nombres))
    base[clave] = lemas
    base["_diccionario_meta"] = {
        "nombres": list(nombres) if nombres else listar(),
        "size": len(lemas),
        "version": VERSION,
        "modulo": "diccionario",
        "rol": "DI",
    }
    return base


# ===============================================================
# CENTINELA
# ===============================================================
def barrer() -> Dict[str, Any]:
    """
    Coherencia interna de DI.
    Descubre fuentes, exige forma legible, reporta errores de carga.
    No calcula Tru.
    """
    _asegurar()
    errores: List[str] = []
    notas: List[str] = []
    por_idioma: Dict[str, List[str]] = {}

    for k, m in sorted(_META.items()):
        if m.get("error"):
            errores.append("{0}: {1}".format(k, m["error"]))
            continue
        if k not in _REGISTRO:
            continue
        idioma = str(m.get("idioma") or "?").lower()
        por_idioma.setdefault(idioma, []).append(k)
        datos = _REGISTRO[k]
        if not isinstance(datos, (dict, set, frozenset, list, tuple)):
            errores.append(
                "{0}: DICCIONARIO debe ser dict (definiciones) "
                "o set/list (términos)".format(k)
            )

    if not _REGISTRO:
        notas.append(
            "ningún diccionario declarado todavía "
            "(vacío legítimo hasta montar fuentes)"
        )

    if errores:
        try:
            DiagnosticoGlobal.recibir_reporte(
                modulo="diccionario",
                errores=[{"tipo": "error", "detalle": e} for e in errores],
            )
        except Exception:
            pass

    return {
        "contenedor": "diccionario",
        "rol": "DI",
        "coherente": not errores,
        "errores": errores,
        "diccionarios": listar(),
        "total": len(_REGISTRO),
        "por_idioma": por_idioma,
        "notas": notas,
    }


def verificar_salida(salida: Dict[str, Any]) -> bool:
    return bool(salida.get("coherente", False))


def inventario(peticion: Any = None) -> Dict[str, Any]:
    b = barrer()
    detalle = []
    for n in listar():
        m = meta(n) or {}
        datos = _REGISTRO.get(n)
        if isinstance(datos, dict):
            size = len(datos)
            tipo = m.get("tipo") or "definiciones"
        elif isinstance(datos, (set, frozenset, list, tuple)):
            size = len(datos)
            tipo = m.get("tipo") or "terminos"
        else:
            size = None
            tipo = m.get("tipo")
        detalle.append({
            "nombre": n,
            "idioma": m.get("idioma"),
            "tipo": tipo,
            "size": size,
            "version": m.get("version"),
            "archivo": m.get("archivo"),
        })
    return {
        "contenedor": "diccionario",
        "version": VERSION,
        "rol": "DI",
        "total": b.get("total"),
        "diccionarios": detalle,
        "por_idioma": b.get("por_idioma"),
        "coherente": b.get("coherente"),
        "funcion": (
            "Biblioteca de definiciones (materia prima léxica). "
            "Engine puede solicitar y distribuir definiciones según contexto; "
            "el resultado final no depende de que Engine invente significados. "
            "Auto-carga todo lo que está debajo. No calcula Tru. No clasifica O."
        ),
    }


def axiomas() -> List[Dict[str, Any]]:
    return [
        {
            "id": "DI-OP-1",
            "tipo": "axioma",
            "sujeto": "diccionario",
            "relacion": "es",
            "objeto": "herramienta_de_definiciones",
            "polaridad": True,
            "enunciado": (
                "DI es la herramienta de definiciones para contrastar y "
                "correlacionar a nivel léxico-significado. Materia prima: "
                "palabra → definición → significado."
            ),
            "depende_de": [],
            "gobierna": ["diccionario"],
        },
        {
            "id": "DI-OP-2",
            "tipo": "axioma",
            "sujeto": "diccionario",
            "relacion": "no_calcula",
            "objeto": "Tru_ni_C_L_K",
            "polaridad": True,
            "enunciado": (
                "DI no calcula Tru_Ri, Tru_total, C, L ni K. "
                "Entrega definición; el cálculo preciso es oficio de CA/FO."
            ),
            "depende_de": [],
            "gobierna": ["diccionario"],
        },
        {
            "id": "DI-OP-3",
            "tipo": "axioma",
            "sujeto": "diccionario",
            "relacion": "no_clasifica",
            "objeto": "O_context",
            "polaridad": True,
            "enunciado": (
                "DI no clasifica O_context (oficio CX). "
                "Puede aportar definiciones sin asumir el rol de clasificación."
            ),
            "depende_de": [],
            "gobierna": ["diccionario", "contexto"],
        },
        {
            "id": "DI-OP-4",
            "tipo": "axioma",
            "sujeto": "fuentes_de_diccionario",
            "relacion": "se_leen",
            "objeto": "automaticamente",
            "polaridad": True,
            "enunciado": (
                "Todo archivo bajo el módulo que declare DICCIONARIO se carga solo. "
                "No hace falta editar el init al agregar idioma o glosario."
            ),
            "depende_de": [],
            "gobierna": ["diccionario"],
        },
        {
            "id": "DI-OP-5",
            "tipo": "axioma",
            "sujeto": "Engine",
            "relacion": "puede_distribuir",
            "objeto": "definiciones_segun_contexto",
            "polaridad": True,
            "enunciado": (
                "Engine tiene libertad de solicitar definiciones a DI y "
                "llevarlas a cualquier módulo según el contexto del ciclo. "
                "Eso no hace a Engine dueño del significado: el resultado "
                "final no depende de que Engine invente definiciones."
            ),
            "depende_de": [],
            "gobierna": ["diccionario", "engine"],
        },
        {
            "id": "DI-OP-6",
            "tipo": "axioma",
            "sujeto": "resultado_final",
            "relacion": "no_depende_de",
            "objeto": "invencion_de_significados_por_Engine",
            "polaridad": True,
            "enunciado": (
                "C, L, K y Tru se calculan bajo contratos de CA/FO y el marco O. "
                "Engine enruta definiciones; no sustituye la materia prima de DI "
                "ni la fórmula de FO."
            ),
            "depende_de": ["DI-OP-5"],
            "gobierna": ["diccionario", "engine", "calculator", "formulas"],
        },
    ]


def resolver(peticion: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Entrega de definiciones / materia prima.
    No clasificación de O. No cálculo de Tru.

    peticion puede traer:
      - palabra / termino → define esa palabra
      - idioma → limita fuentes
      - diccionarios / nombres → fuentes concretas
    """
    peticion = dict(peticion or {})
    palabra = peticion.get("palabra") or peticion.get("termino")
    idioma = peticion.get("idioma")
    nombres = peticion.get("diccionarios") or peticion.get("nombres")

    if palabra:
        if nombres:
            if isinstance(nombres, str):
                nombres = [nombres]
            r = definir(str(palabra), *nombres)
        elif idioma:
            r = definir(str(palabra), *listar_por_idioma(str(idioma)))
        else:
            r = definir(str(palabra))
        return {
            "ok": r is not None,
            "modulo": "diccionario",
            "rol": "DI",
            "resultado": r,
            "coherente": True,
            "notas": [
                "Definición entregada. No se calculó Tru ni se clasificó O. "
                "Engine puede distribuir este resultado según contexto."
            ],
        }

    if idioma and not nombres:
        datos = cargar_idioma(str(idioma))
        usados = list(datos.keys())
    elif nombres:
        if isinstance(nombres, str):
            nombres = [nombres]
        datos = {n: cargar(n) for n in nombres}
        usados = list(nombres)
    else:
        datos = cargar_todos()
        usados = list(datos.keys())

    return {
        "ok": True,
        "modulo": "diccionario",
        "rol": "DI",
        "diccionarios_usados": usados,
        "palabras_n": len(palabras(*usados)),
        "inventario": inventario(),
        "coherente": True,
        "notas": [
            "Materia prima entregada. No se calculó Tru ni se clasificó O. "
            "Engine puede distribuir definiciones a voluntad según contexto."
        ],
    }


# ===============================================================
# CONTENEDOR (contrato con Engine — al final)
# ===============================================================
CONTENEDOR = {
    "nombre": "diccionario",
    "rol": "DI",
    "version": VERSION,
    "requiere": [],
    "descripcion": (
        "Biblioteca de definiciones. Rol DI. "
        "Materia prima léxica: palabra → definición → significado. "
        "Herramienta para contrastar y correlacionar a nivel de significado. "
        "Auto-carga todos los archivos debajo (es, en, glosario_vpsi, …). "
        "Engine puede solicitar y distribuir definiciones a cualquier módulo "
        "según el contexto del ciclo; el resultado final (C, L, K, Tru) no "
        "depende de que Engine invente significados. "
        "No calcula Tru. No clasifica O. No trae dominios externos (RE)."
    ),
    "capacidades": {
        "verificar": barrer,
        "barrer": barrer,
        "inventario": inventario,
        "axiomas": axiomas,
        "resolver": resolver,
        "listar": listar,
        "cargar": cargar,
        "cargar_todos": cargar_todos,
        "definir": definir,
        "significado": significado,
        "inyectar_en_peticion": inyectar_en_peticion,
    },
    "agencia": (
        "Total para entregar definiciones presentes en las fuentes. "
        "Nula sobre valores de C/L/K/Tru y sobre clasificación de O."
    ),
    "agencia_engine": (
        "Engine puede invocar DI y llevar definiciones a otros módulos "
        "según contexto. No sustituye la materia prima ni la fórmula de FO."
    ),
}
