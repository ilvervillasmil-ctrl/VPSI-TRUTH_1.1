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

      # ---------------------------------------------------------------
    # subsección: Module Audit
    # ---------------------------------------------------------------
    #
    # Johnson puede llamar esto cuantas veces quiera
    # sobre cualquier contenedor / carpeta de modulo.
    #
    # Tres auditorias:
    #   1. Module Inspection
    #   2. Module Validation
    #   3. Source Audit
    #
    # No ejecuta la logica del modulo.
    # Solo inspecciona estructura, contrato y fuentes.
    # ---------------------------------------------------------------
    def _auditar_modulo(self, cont) -> Dict[str, Any]:
        from pathlib import Path

        informe = {
            "modulo": cont.nombre,
            "rol": cont.rol,
            "version": cont.version,
            "inspection": {},
            "validation": {},
            "source_audit": {},
        }

        # ==========================================================
        # 1. Module Inspection
        # ==========================================================
        raiz = Path(cont.ruta).resolve().parent

        archivos = sorted(
            str(p.relative_to(raiz))
            for p in raiz.rglob("*")
            if p.is_file()
        )

        informe["inspection"] = {
            "carpeta": str(raiz),
            "archivos": archivos,
            "n_archivos": len(archivos),
        }

        # ==========================================================
        # 2. Module Validation
        # ==========================================================
        errores = []

        if not cont.nombre:
            errores.append("CONTENEDOR.nombre ausente")

        if not cont.rol:
            errores.append("CONTENEDOR.rol ausente")

        if not cont.version:
            errores.append("CONTENEDOR.version ausente")

        if not isinstance(cont.capacidades, dict):
            errores.append("CONTENEDOR.capacidades no es dict")
        else:
            for capacidad in cont.capacidades:
                if not cont.tiene(capacidad):
                    errores.append(
                        "capacidad '{0}' no resoluble".format(capacidad)
                    )

        informe["validation"] = {
            "coherente": len(errores) == 0,
            "errores": errores,
            "requiere": list(getattr(cont, "requiere", []) or []),
            "capacidades": sorted(
                str(k) for k in (cont.capacidades or {}).keys()
            ),
        }

        # ==========================================================
        # 3. Source Audit
        # ==========================================================
        auditoria = []

        for archivo in archivos:
            ruta = raiz / archivo
            try:
                texto = ruta.read_text(encoding="utf-8", errors="ignore")
                auditoria.append({
                    "archivo": archivo,
                    "lineas": len(texto.splitlines()),
                    "bytes": ruta.stat().st_size,
                })
            except Exception as e:
                auditoria.append({
                    "archivo": archivo,
                    "error": str(e),
                })

        informe["source_audit"] = {
            "archivos": auditoria,
            "n_archivos": len(auditoria),
        }

        return informe

    def auditar_modulo(self, cont) -> Dict[str, Any]:
        """Entrada publica para Johnson: misma auditoria, cuantas veces quiera."""
        return self._auditar_modulo(cont)

    # ===============================================================
    # SECCIÓN: JOHNSON — conectividad del Engine
    # ===============================================================
    #
    # Pregunta de Johnson:
    #   ¿Puede el Engine llegar realmente hasta este modulo
    #   y ejecutar su contrato?
    #
    # Cadena por cada rol descubierto:
    #   ROL
    #     → CONTENEDOR encontrado
    #     → modulo importado
    #     → carpeta encontrada
    #     → archivos leidos
    #     → contrato leido
    #     → capacidades resueltas
    #     → dependencias (requiere) satisfechas
    #     → conectado al Engine
    #
    # Johnson reporta. No interpreta logica del modulo.
    # ===============================================================

    def auditar_conectividad_engine(self) -> Dict[str, Any]:
        from pathlib import Path

        informe_roles: Dict[str, Any] = {}
        cortes: List[Dict[str, Any]] = []

        # Roles presentes en el registro (descubiertos por CONTENEDOR)
        roles = sorted(self.registro.por_rol.keys())

        # Tambien roles que tienen contenedor aunque la clave este vacia
        for nombre, cont in self.registro.contenedores.items():
            if cont.rol not in roles:
                roles.append(cont.rol)
        roles = sorted(set(roles))

        for rol in roles:
            estado = {
                "rol": rol,
                "contenedor": False,
                "modulo_importado": False,
                "carpeta": False,
                "archivos": False,
                "contrato": False,
                "capacidades": False,
                "dependencias": False,
                "conectado": False,
                "detalle": {},
                "corte": None,
            }

            cont = self.registro.primero(rol)
            if cont is None:
                estado["corte"] = "sin contenedor"
                cortes.append({
                    "rol": rol,
                    "eslabon": "contenedor",
                    "razon": "CONTENEDOR no encontrado",
                })
                informe_roles[rol] = estado
                continue

            estado["contenedor"] = True
            estado["detalle"]["nombre"] = cont.nombre
            estado["detalle"]["version"] = cont.version
            estado["detalle"]["ruta"] = str(cont.ruta)

            # modulo importado
            if getattr(cont, "modulo", None) is not None:
                estado["modulo_importado"] = True
            else:
                estado["corte"] = "modulo no importado"
                cortes.append({
                    "rol": rol,
                    "eslabon": "modulo_importado",
                    "razon": "cont.modulo es None",
                })

            # carpeta + archivos
            carpeta = Path(cont.ruta).resolve().parent
            lista_archivos: List[str] = []
            if carpeta.is_dir():
                estado["carpeta"] = True
                lista_archivos = sorted(
                    str(p.relative_to(carpeta))
                    for p in carpeta.rglob("*")
                    if p.is_file()
                )
                if lista_archivos:
                    estado["archivos"] = True
                else:
                    if estado["corte"] is None:
                        estado["corte"] = "carpeta sin archivos"
                    cortes.append({
                        "rol": rol,
                        "eslabon": "archivos",
                        "razon": "carpeta vacia",
                    })
            else:
                if estado["corte"] is None:
                    estado["corte"] = "carpeta no encontrada"
                cortes.append({
                    "rol": rol,
                    "eslabon": "carpeta",
                    "razon": "no es directorio: {0}".format(carpeta),
                })

            estado["detalle"]["carpeta"] = str(carpeta)
            estado["detalle"]["archivos"] = lista_archivos
            estado["detalle"]["n_archivos"] = len(lista_archivos)

            # contrato
            caps = getattr(cont, "capacidades", None)
            if isinstance(caps, dict) and caps:
                estado["contrato"] = True
            else:
                if estado["corte"] is None:
                    estado["corte"] = "contrato invalido"
                cortes.append({
                    "rol": rol,
                    "eslabon": "contrato",
                    "razon": "capacidades no es dict o esta vacio",
                })

            # capacidades resueltas
            caps_ok = True
            caps_fallo: List[str] = []
            if isinstance(caps, dict):
                for cap in caps:
                    if not cont.tiene(cap):
                        caps_ok = False
                        caps_fallo.append(str(cap))
            else:
                caps_ok = False

            estado["capacidades"] = caps_ok
            estado["detalle"]["capacidades"] = (
                sorted(str(k) for k in caps.keys())
                if isinstance(caps, dict) else []
            )
            estado["detalle"]["capacidades_no_resolubles"] = caps_fallo

            if not caps_ok and estado["corte"] is None:
                estado["corte"] = "capacidad no resoluble"
                cortes.append({
                    "rol": rol,
                    "eslabon": "capacidades",
                    "razon": "no resolubles: {0}".format(caps_fallo),
                })

            # dependencias (requiere)
            requiere = list(getattr(cont, "requiere", []) or [])
            deps_ok = True
            deps_faltan: List[str] = []
            for req in requiere:
                req_s = str(req)
                # puede ser rol o nombre de modulo
                if self.registro.primero(req_s) is None:
                    if req_s not in self.registro.contenedores:
                        deps_ok = False
                        deps_faltan.append(req_s)

            estado["dependencias"] = deps_ok
            estado["detalle"]["requiere"] = requiere
            estado["detalle"]["dependencias_faltan"] = deps_faltan

            if not deps_ok and estado["corte"] is None:
                estado["corte"] = "dependencia faltante"
                cortes.append({
                    "rol": rol,
                    "eslabon": "dependencias",
                    "razon": "faltan: {0}".format(deps_faltan),
                })

            # conectado = cadena completa
            estado["conectado"] = all((
                estado["contenedor"],
                estado["modulo_importado"],
                estado["carpeta"],
                estado["archivos"],
                estado["contrato"],
                estado["capacidades"],
                estado["dependencias"],
            ))

            informe_roles[rol] = estado

        conectados = [r for r, e in informe_roles.items() if e["conectado"]]
        desconectados = [r for r, e in informe_roles.items() if not e["conectado"]]

        # primer corte = primer eslabon roto reportado
        primer_corte = cortes[0] if cortes else None

        return {
            "auditor": "Johnson",
            "tipo": "conectividad_engine",
            "roles_vistos": roles,
            "roles_n": len(roles),
            "roles_conectados": conectados,
            "roles_conectados_n": len(conectados),
            "roles_desconectados": desconectados,
            "roles_desconectados_n": len(desconectados),
            "cortes": cortes,
            "primer_corte": primer_corte,
            "por_rol": informe_roles,
            "coherente": len(desconectados) == 0,
        }

    # ===============================================================
    # FIN SECCIÓN: JOHNSON — conectividad del Engine
    # ===============================================================
