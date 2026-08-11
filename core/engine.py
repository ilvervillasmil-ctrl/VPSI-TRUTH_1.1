# ===============================================================
# VPSI-TRUTH — core/engine.py DIRECTOR ARQUITECTO SIMBIOSIS MECANICA
# ===============================================================
#
# ENGINE
# Versión:            19.0
# Esquema contrato:   VPSI-CONTRACT-2.0
# API Engine:         1.0
#
# Función:
#   Agente ejecutor del sistema.
#   Descubre módulos. Lee contratos. Valida contratos.
#   Registra módulos. Resuelve dependencias.
#   Construye grafo estructural. Ejecuta capacidades declaradas.
#   Entrega contenido al módulo correspondiente.
#   Recibe el resultado real del módulo.
#   Registra trazas. Registra mapa de ruta de ejecución.
#   Consolida reportes. Entrega paquete_omega().
#
# Qué NO hace:
#   No inventa capacidades. No adivina 
#   No interpreta reportes.
#
# Principio:
#   Agencia limitada por la unión coherente de los contratos.
#
# ===============================================================
# ===============================================================
# Parte 1 IMPORTACIONES
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
# Parte 2 CONSTANTES /el esquema de contrato requerido,
#  la versión de contrato exigida y la API actual del Engine
# ===============================================================
VERSION_ENGINE = "19"
ESQUEMA_CONTRATO_REQUERIDO = "VPSI-CONTRACT-1.0"
VERSION_CONTRATO_REQUERIDA = ">=1.0"
API_ENGINE_ACTUAL = "1.0"


# ===============================================================
# Parte 3 ESTADOS CANÓNICOS/
#
# ===============================================================

ESTADO_NO_INICIADO = "NO_INICIADO"
ESTADO_OPERATIVO = "OPERATIVO"
ESTADO_DEGRADADO = "DEGRADADO"
ESTADO_RECHAZADO = "RECHAZADO"
ESTADOS_CANONICOS = (ESTADO_NO_INICIADO, ESTADO_OPERATIVO, ESTADO_DEGRADADO, ESTADO_RECHAZADO)


# ===============================================================
#  Parte 4 CLAVES OBLIGATORIAS DEL CONTRATO
# Enumera el conjunto de claves que todo contrato de módulo debe contener obligatoriamente.
# Sirve como referencia para la validación estructural posterior.
# ===============================================================

CLAVES_OBLIGATORIAS_CONTRATO = (
    "esquema",
    "version_contrato",
    "version_modulo",
    "id",
    "nombre",
    "rol",
    "descripcion",
    "funcion",
    "no_hace",
    "autoridad",
    "conocimiento_exportable",
    "requiere",
    "autoriza_engine",
    "consultas_soportadas",
    "capacidades",
    "capacidades_meta",
    "reporting",
    "estados_validos",
    "invariantes",
    "estabilidad", "acceso",
    "compatible_desde", "acceso_archivos",
    "api_engine", "validar_esquema",
)

# ===============================================================
#   Parte 5 PERMISOS AUTORIZADOS POR ENGINE
#  El Engine solo puede ejercer las acciones que el 
#  contrato autorice explícitamente.
# ===============================================================

PERMISOS_AUTORIZA_ENGINE = (
    "leer", "ejecutar",
    "consultar", "recombinar",
    "reportar", "auditar",
    "inventariar",
    "alterar",
    "metricas", "estado",
    "version", "salud",
    "inventario", "capacidades",
    "errores", "advertencias",
    "dependencias", "contrato",
    "conocimiento", "diagnostico",
    "reporte", "crear",
    "actualizar", "validar_esquema",
    "validar", "procesar",
    "analizar", "generar",
    "exportar","importar", "respaldar",
    "recuperar", "sincronizar",
    "monitorear", "acceso_archivos",
)



# ===============================================================
#  Parte 6 BANDERAS DE REPORTING/ Define las banderas booleanas
# que controlan qué información puede devolver un módulo cuando 
# se le solicita un reporte, diagnóstico o inventario.
# ===============================================================

BANDERAS_REPORTING = (
    "estado", "salud",
    "inventario", "capacidades",
    "errores", "advertencias",
    "dependencias", "version",
    "contrato", "conocimiento",
    "metricas", "diagnostico",
    "reporte", "acceso_archivos",
    "validar_esquema",
)

# ===============================================================
#  Parte 7 METADATOS DE CAPACIDADES/Especifica los campos obligatorios 
# que debe tener cada entrada dentro de capacidades meta
# descripción, entrada, salida, etc.
# ===============================================================

CLAVES_META_CAPACIDAD = (
    "descripcion", "entrada", "validar_esquema",
    "salida", "acceso_archivos",
)

# ===============================================================
# MAPA ESTRUCTURAL — CAPACIDADES Y CAPACIDADES META
# ===============================================================
#
# REPOSITORIO
#     │
#     ├── módulo A
#     │      └── capacidades
#     │
#     ├── módulo B
#     │      └── capacidades
#     │
#     └── axiomas
#            └── capacidades META
#                   │
#                   ├── detectan declaraciones
#                   ├── verifican capacidades
#                   ├── clasifican dominios
#                   └── verifican estructuras
#
# Las capacidades META no sustituyen las capacidades de los módulos.
# Actúan sobre las declaraciones, capacidades y estructuras existentes.
#
# Engine no inventa capacidades.
# Engine descubre, valida y ejerce únicamente lo declarado
# contractualmente por los módulos.
#
# ===============================================================
# ===============================================================
#  Parte 8 LISTAS OBLIGATORIAS DE STR obligaciones de CONTRATO  
# estan abajo en autorida de engine/Define qué campos del contrato
# deben ser listas de cadenas de texto.
# ===============================================================

LISTAS_STR_OBLIGATORIAS = (
    "no_hace", "autoridad", "validar_esquema",
    "conocimiento_exportable", "consultas_soportadas",
    "invariantes", "acceso_archivos", "capacidades",
)

# ===============================================================
# Parte 9 DEFINICIONES/Una vez validado, lo convierte 
# en un objeto Contenedor. Todas las operaciones posteriores (registro,
# resolución de dependencias, ejecución de capacidades, construcción del grafo, etc.)
# operan sobre instancias de esta clase. En resumen: la sección 
# DEFINICIONES crea las dos piezas que permiten al Engine pasar de “contrato validado” a “objeto operativo interno”
# ===============================================================

class ArranqueError(Exception):
    """Fallo estructural durante el arranque del Engine."""
    pass
# ===============================================================
# Parte 10 LIBRERIAS DEL SISTEMA PARA CONTRATOS MODULOS
# ===============================================================

class Contenedor:
    """
    Materialización de un CONTENEDOR.

    El Engine no completa ni inventa campos del contrato.
    """

    def __init__(self, meta: Dict[str, Any], modulo: Any, ruta: Path) -> None:
        self.meta = meta
        self.modulo = modulo
        self.ruta = ruta

        # -------------------------------------------------------
        # Parte 10.1 IDENTIDAD DE CADA MODULO EN EL CONTRATO
        # -------------------------------------------------------

        self.id: str = str(meta.get("id", ""))
        self.nombre: str = str(meta.get("nombre", ""))
        self.rol: str = str(meta.get("rol", ""))

        # -------------------------------------------------------
        # Parte 10.2 VERSIONES Y PALABRAS CLAVE DEL CONTRATO
        # -------------------------------------------------------

        self.version: str = str(meta.get("version_modulo", meta.get("version", "")))
        self.version_contrato: str = str(meta.get("version_contrato", ""))
        self.esquema: str = str(meta.get("esquema", ""))
        self.estabilidad: str = str(meta.get("estabilidad", ""))
        self.compatible_desde: str = str(meta.get("compatible_desde", ""))
        self.api_engine: str = str(meta.get("api_engine", ""))

        # -------------------------------------------------------
        # Parte 10.3 DESCRIPCIÓN Y AUTORIDAD DE ENGINE EN CADA CONTRATO
        # -------------------------------------------------------

        self.descripcion: str = str(meta.get("descripcion", ""))
        self.funcion = meta.get("funcion")
        self.no_hace: List[str] = list(meta.get("no_hace") or [])
        self.autoridad: List[str] = list(meta.get("autoridad") or [])
        self.conocimiento_exportable: List[str] = list(meta.get("conocimiento_exportable") or [])
        self.consultas_soportadas: List[str] = list(meta.get("consultas_soportadas") or [])
        self.invariantes: List[str] = list(meta.get("invariantes") or [])
        self.acceso_archivos: List[str] = list(meta.get("acceso_archivos") or [])

        # -------------------------------------------------------
        # Parte 10.4 CONTRATO OPERATIVO Y UTILIZACIÓN VARIABLE
        # -------------------------------------------------------

        self.requiere: List[str] = list(meta.get("requiere") or [])
        self.autoriza_engine: Dict[str, Any] = dict(meta.get("autoriza_engine") or {})
        self.capacidades: Dict[str, Any] = dict(meta.get("capacidades") or {})
        self.capacidades_meta: Dict[str, Any] = dict(meta.get("capacidades_meta") or {})
        self.reporting: Dict[str, Any] = dict(meta.get("reporting") or {})
        self.estados_validos: List[str] = list(meta.get("estados_validos") or [])
        self.validar_esquema: List[str] = list(meta.get("validar_esquema") or [])

        # -------------------------------------------------------
        # FIN DE LIBRERIAS Y CLAVES DE CONTRATO
        # -------------------------------------------------------

    # -----------------------------------------------------------
    # Parte 10.5 RESOLUCIÓN DE CAPACIDADES
    # -----------------------------------------------------------

    def fn(self, clave: str) -> Any:
        """Devuelve únicamente la capacidad declarada y callable."""
        ref = self.capacidades.get(clave)
        return ref if callable(ref) else None

    pass
    


# ===============================================================
# Parte 11 — DEF DE REGISTROS CONTRATOS
# ===============================================================

from typing import Any, Dict, List, Optional


class RegistroModulos:
    """
    Registro central de Contenedores.
    Mantiene índices por nombre, por id y por rol.
    El rol es único por definición: solo un módulo puede ocuparlo.
    No inventa datos. Solo almacena lo que el Engine le entrega
    tras la validación contractual.
    """

    def __init__(self) -> None:
        # -------------------------------------------------------
        # Parte 11.1 — Índices internos
        # -------------------------------------------------------
        self.contenedores: Dict[str, Contenedor] = {}
        self.por_id: Dict[str, Contenedor] = {}
        self.por_rol: Dict[str, List[Contenedor]] = {}

    # -----------------------------------------------------------
    # Parte 11.2 — Registro
    # -----------------------------------------------------------

    def registrar(self, cont: Contenedor) -> List[str]:
        """
        Intenta registrar un Contenedor.
        Devuelve lista de errores de duplicidad.
        Si la lista está vacía, el registro fue exitoso.
        """
        errores: List[str] = []

        nombre = cont.nombre
        id_mod = cont.id
        rol = cont.rol

        # -------------------------------------------------------
        # Parte 11.2.1 — Validación de campos obligatorios
        # -------------------------------------------------------
        if not nombre:
            errores.append("nombre vacío o nulo")
            return errores

        # -------------------------------------------------------
        # Parte 11.2.2 — Validación de duplicados
        # -------------------------------------------------------
        if nombre in self.contenedores:
            errores.append(f"duplicado de nombre: '{nombre}' ya registrado")

        if id_mod and id_mod in self.por_id:
            errores.append(
                f"duplicado de id: '{id_mod}' ya registrado "
                f"(módulo {self.por_id[id_mod].nombre})"
            )

        if rol and rol in self.por_rol and self.por_rol[rol]:
            existente = self.por_rol[rol][0].nombre
            errores.append(
                f"duplicado de rol: '{rol}' ya ocupado por '{existente}'"
            )

        if errores:
            return errores

        # -------------------------------------------------------
        # Parte 11.2.3 — Materialización en los índices
        # -------------------------------------------------------
        self.contenedores[nombre] = cont

        if id_mod:
            self.por_id[id_mod] = cont

        if rol:
            self.por_rol.setdefault(rol, []).append(cont)

        return []

    # -----------------------------------------------------------
    # Parte 11.3 — Consultas
    # -----------------------------------------------------------

    def primero(self, clave: Any) -> Optional[Contenedor]:
        """
        Resuelve un Contenedor por nombre, por id o por rol.
        Dado que el rol es único, devuelve el único módulo
        que lo ocupa (si existe).
        """
        if not isinstance(clave, str):
            return None

        clave = clave.strip()

        # 1. Búsqueda por nombre
        if clave in self.contenedores:
            return self.contenedores[clave]

        # 2. Búsqueda por id
        if clave in self.por_id:
            return self.por_id[clave]

        # 3. Búsqueda por rol (único)
        lista = self.por_rol.get(clave)
        return lista[0] if lista else None

    def total(self) -> int:
        """Número total de Contenedores registrados."""
        return len(self.contenedores)
        
# ===============================================================
# ENGINE AQUI SE DEFINEN LAS DECLARACIONES
# ===============================================================

class Engine:

    VERSION = VERSION_ENGINE

    def __init__(self, raiz_modulos: str | Path, invocador_id: str = "core", strict: bool = True) -> None:

        # =======================================================
        # CONFIGURACIÓN BÁSICA
        # =======================================================

        self.raiz = Path(raiz_modulos).resolve()
        self.invocador_id = invocador_id
        self.strict = strict

        # =======================================================
        # ESTADO
        # =======================================================

        self.estado = ESTADO_NO_INICIADO
        self.registro = RegistroModulos()
        self.errores_arranque: List[str] = []
        self.advertencias: List[str] = []
        self.fallos: List[Dict[str, Any]] = []
        self.resultados_evaluacion: List[Any] = []

        # =======================================================
        # TRAZAS
        # =======================================================

        self._trazas: List[Dict[str, Any]] = []
        self._traza_seq: int = 0

        # =======================================================
        # MAPA DE RUTA
        # =======================================================

        self._mapa_ruta: List[Dict[str, Any]] = []
        self._ruta_seq: int = 0

        # =======================================================
        # CENTINELA — PRIORIDAD ABSOLUTA
        # =======================================================

        self._centinela: Optional[Centinela] = None

        # =======================================================
        # ESTRUCTURAS INTERNAS
        # =======================================================

        self._modulos_descubiertos: List[Path] = []
        self._reportes_modulos: Dict[str, Any] = {}
        self._diagnosticos: Dict[str, Any] = {}
        self._inventarios: Dict[str, Any] = {}
        self._dependencias: Dict[str, Any] = {}
        self._grafo: Dict[str, Any] = {}

        # =======================================================
        # ARRANQUE
        # =======================================================

        self._modulos_descubiertos = self._descubrir_modulos()
        self._cargar_y_validar()
        self._resolver_dependencias()
        self._construir_grafo()

        # =======================================================
        # ESTADO FINAL
        # =======================================================

        if self.errores_arranque:
            self.estado = ESTADO_RECHAZADO
            if self.strict:
                raise ArranqueError("Engine no pudo arrancar:\n  - " + "\n  - ".join(self.errores_arranque))
        else:
            self.estado = ESTADO_OPERATIVO

    # ===========================================================
    # DESCUBRIMIENTO
    # ===========================================================

    def _descubrir_modulos(self) -> List[Path]:
        if not self.raiz.is_dir():
            return []
        return [p for p in sorted(self.raiz.iterdir()) if p.is_dir() and (p / "__init__.py").is_file()]

    # ===========================================================
    # LECTURA DEL CONTRATO
    # ===========================================================

    def _leer_contrato(self, path_dir: Path) -> Optional[Dict[str, Any]]:
        init_path = path_dir / "__init__.py"
        nombre_mod = f"vpsi_dinamico_{path_dir.name}"

        try:
            spec = importlib.util.spec_from_file_location(
                nombre_mod,
                init_path,
                submodule_search_locations=[str(path_dir)]
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
                "nombre_carpeta": path_dir.name
            }

        except Exception as e:
            self.errores_arranque.append(
                f"{path_dir.name}: error al cargar → {type(e).__name__}: {e}"
            )
            return None

    # ===========================================================
    # CARGA Y REGISTRO
    # ===========================================================

    def _cargar_y_validar(self) -> None:

        for path_dir in self._modulos_descubiertos:

            # ---------------------------------------------------
            # LEER CONTRATO Y MATERIALIZAR MÓDULO
            # ---------------------------------------------------

            leido = self._leer_contrato(path_dir)

            if leido is None:
                continue

            meta = leido["meta"]
            nombre = meta.get("nombre") or leido["nombre_carpeta"]
            mod = leido["modulo"]

            # ---------------------------------------------------
            # ARCHIVOS PY
            # ---------------------------------------------------

            archivos_py = sorted(
                p for p in path_dir.rglob("*.py")
                if p.is_file()
            )

            # ---------------------------------------------------
            # CONTEXTO ESTRUCTURAL DEL MÓDULO
            # ---------------------------------------------------

            setattr(
                mod,
                "ARCHIVOS_PY",
                archivos_py,
            )

            # ---------------------------------------------------
            # VALIDACIÓN DEL CONTRATO
            # ---------------------------------------------------

            errores = self._validar_esquema(
                meta,
                nombre,
            )

            if errores:
                self.errores_arranque.extend(errores)
                continue

            # ---------------------------------------------------
            # MATERIALIZACIÓN DEL CONTENEDOR
            # ---------------------------------------------------

            cont = Contenedor(
                meta=meta,
                modulo=mod,
                ruta=leido["ruta"],
            )

            # ---------------------------------------------------
            # REGISTRO DEL MÓDULO
            # ---------------------------------------------------

            errores_dup = self.registro.registrar(cont)
            if errores_dup:
                for error in errores_dup:
                    self.errores_arranque.append(f"{nombre}: {error}")

    # ===========================================================
    # DECLARACIÓN 1 — RESOLUCIÓN POR EXISTENCIA CONTRACTUAL
    # ===========================================================

    def resolver_existencia(self, peticion: Any) -> Dict[str, Any]:
        """
        Determina si X puede resolverse utilizando el repertorio
        contractual completo registrado por Engine.

        El repertorio es la unión de las declaraciones y capacidades
        existentes en todos los Contenedor registrados.

        Si X puede ser atendida por las capacidades disponibles:
            EXISTE

        Si ninguna capacidad disponible puede atender X:
            NO_EXISTE

        NO_EXISTE no es un error.
        """

        if not isinstance(peticion, str):
            return {
                "estado": "NO_EXISTE",
                "existe": False,
                "peticion": peticion,
            }

        x = peticion.strip()

        if not x:
            return {
                "estado": "NO_EXISTE",
                "existe": False,
                "peticion": peticion,
            }

        # -------------------------------------------------------
        # REPERTORIO CONTRACTUAL COMPLETO
        # -------------------------------------------------------

        for cont in self.registro.contenedores.values():

            # ---------------------------------------------------
            # CAPACIDADES DECLARADAS
            # ---------------------------------------------------

            for capacidad in cont.capacidades:

                if str(capacidad).strip() == x:
                    return {
                        "estado": "EXISTE",
                        "existe": True,
                        "peticion": x,
                        "modulo": cont.nombre,
                        "rol": cont.rol,
                        "id": cont.id,
                        "capacidad": capacidad,
                    }

            # ---------------------------------------------------
            # DECLARACIONES CONTRACTUALES
            # ---------------------------------------------------

            for declaracion in cont.conocimiento_exportable:
                if isinstance(declaracion, str) and declaracion.strip() == x:
                    return {
                        "estado": "EXISTE",
                        "existe": True,
                        "peticion": x,
                        "modulo": cont.nombre,
                        "rol": cont.rol,
                        "id": cont.id,
                        "tipo": "conocimiento_exportable",
                    }

            for consulta in cont.consultas_soportadas:
                if isinstance(consulta, str) and consulta.strip() == x:
                    return {
                        "estado": "EXISTE",
                        "existe": True,
                        "peticion": x,
                        "modulo": cont.nombre,
                        "rol": cont.rol,
                        "id": cont.id,
                        "tipo": "consulta_soportada",
                    }

            for autoridad in cont.autoridad:
                if isinstance(autoridad, str) and autoridad.strip() == x:
                    return {
                        "estado": "EXISTE",
                        "existe": True,
                        "peticion": x,
                        "modulo": cont.nombre,
                        "rol": cont.rol,
                        "id": cont.id,
                        "tipo": "autoridad",
                    }

            for invariante in cont.invariantes:
                if isinstance(invariante, str) and invariante.strip() == x:
                    return {
                        "estado": "EXISTE",
                        "existe": True,
                        "peticion": x,
                        "modulo": cont.nombre,
                        "rol": cont.rol,
                        "id": cont.id,
                        "tipo": "invariante",
                    }

        # -------------------------------------------------------
        # X NO EXISTE
        # -------------------------------------------------------

        return {
            "estado": "NO_EXISTE",
            "existe": False,
            "peticion": x,
            "razon": "NO_EXISTE",
        }

    # ===========================================================
    # DECLARACIÓN 2 — RESOLUCIÓN DE PETICIÓN
    # ===========================================================

    def resolver_peticion(
        self,
        peticion: Any,
        *args: Any,
        **kwargs: Any,
    ) -> Dict[str, Any]:

        existencia = self.resolver_existencia(peticion)

        if existencia["estado"] == "NO_EXISTE":
            return existencia

        capacidad = existencia.get("capacidad")

        if capacidad is None:
            return {
                "estado": "NO_EXISTE",
                "existe": False,
                "peticion": existencia.get("peticion"),
                "razon": "NO_EXISTE",
            }

        return self.ejecutar_capacidad(
            existencia["modulo"],
            capacidad,
            *args,
            **kwargs,
        )

    # ===========================================================
    # VALIDACIÓN DE LISTAS STR
    # ===========================================================

    def _validar_lista_str(
        self,
        meta: Dict[str, Any],
        clave: str,
        nombre: str
    ) -> List[str]:

        errores: List[str] = []
        val = meta.get(clave)

        if not isinstance(val, list):
            errores.append(f"{nombre}: '{clave}' debe ser list")
            return errores

        for i, item in enumerate(val):

            if not isinstance(item, str):
                errores.append(
                    f"{nombre}: '{clave}[{i}]' debe ser str, es {type(item).__name__}"
                )

        return errores

    # ===========================================================
    # VERSIONES
    # ===========================================================

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

        exacto, ver_str = (
            (False, raw[2:].strip())
            if raw.startswith(">=")
            else (True, raw)
        )

        requerida = self._parse_version(ver_str)

        if requerida is None:
            return f"api_engine no parseable: '{declarado}'"

        actual = self._parse_version(API_ENGINE_ACTUAL)

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

    def _comparar_compatible_desde(
        self,
        declarado: str,
        nombre: str
    ) -> Optional[str]:

        raw = str(declarado).strip()

        if not raw:
            return f"{nombre}: compatible_desde vacío"

        requerida = self._parse_version(raw)

        if requerida is None:
            return f"{nombre}: compatible_desde no parseable: '{declarado}'"

        actual = self._parse_version(VERSION_ENGINE)

        if actual is None:
            return None

        n = max(len(requerida), len(actual))
        requerida += (0,) * (n - len(requerida))
        actual += (0,) * (n - len(actual))

        if actual < requerida:
            return f"{nombre}: compatible_desde={raw} pero Engine es {VERSION_ENGINE}"

        return None

    # ===========================================================
    # VALIDACIÓN DEL ESQUEMA DEL CONTRATO
    # ===========================================================

    def _validar_esquema(
        self,
        meta: Dict[str, Any],
        nombre: str
    ) -> List[str]:

        errores: List[str] = []

        # =======================================================
        # 1. ESQUEMA
        # =======================================================

        if meta.get("esquema") != ESQUEMA_CONTRATO_REQUERIDO:
            errores.append(
                f"{nombre}: esquema '{meta.get('esquema')}' != '{ESQUEMA_CONTRATO_REQUERIDO}'"
            )

        # =======================================================
        # 2. VERSIÓN DEL CONTRATO
        # =======================================================

        vc = meta.get("version_contrato")

        if str(vc) != VERSION_CONTRATO_REQUERIDA:
            errores.append(
                f"{nombre}: version_contrato '{vc}' != '{VERSION_CONTRATO_REQUERIDA}'"
            )

        # =======================================================
        # 3. VERSIÓN DEL MÓDULO
        # =======================================================

        vm = meta.get("version_modulo")

        if not isinstance(vm, str) or not vm.strip():
            errores.append(
                f"{nombre}: version_modulo debe ser str no vacío, es {type(vm).__name__}"
            )

        # =======================================================
        # 4. CLAVES OBLIGATORIAS
        # =======================================================

        for clave in CLAVES_OBLIGATORIAS_CONTRATO:

            if clave not in meta:
                errores.append(
                    f"{nombre}: falta clave obligatoria '{clave}'"
                )

        # =======================================================
        # 5. LISTAS DE STR OBLIGATORIAS
        # =======================================================

        for clave in LISTAS_STR_OBLIGATORIAS:

            val = meta.get(clave)

            if not isinstance(val, list):
                errores.append(
                    f"{nombre}: '{clave}' debe ser list"
                )
                continue

            for i, item in enumerate(val):

                if not isinstance(item, str):
                    errores.append(
                        f"{nombre}: '{clave}[{i}]' debe ser str, es {type(item).__name__}"
                    )

        # =======================================================
        # 6. DEPENDENCIAS (requiere)
        # =======================================================

        requiere = meta.get("requiere")

        if not isinstance(requiere, list):
            errores.append(
                f"{nombre}: 'requiere' debe ser list"
            )

        else:

            for i, item in enumerate(requiere):

                if not isinstance(item, str):
                    errores.append(
                        f"{nombre}: 'requiere[{i}]' debe ser str, es {type(item).__name__}"
                    )

        # =======================================================
        # 7. CAPACIDADES
        # =======================================================

        caps = meta.get("capacidades")

        if not isinstance(caps, dict):

            errores.append(
                f"{nombre}: 'capacidades' debe ser dict"
            )

        else:

            for k, v in caps.items():

                if not callable(v):
                    errores.append(
                        f"{nombre}: capacidad '{k}' no es callable (tipo={type(v).__name__})"
                    )

        # =======================================================
        # 8. METADATOS DE CAPACIDADES
        # =======================================================

        meta_caps = meta.get("capacidades_meta")

        if not isinstance(meta_caps, dict):

            errores.append(
                f"{nombre}: 'capacidades_meta' debe ser dict"
            )

        elif isinstance(caps, dict):

            for k in caps:

                if k not in meta_caps:

                    errores.append(
                        f"{nombre}: capacidad '{k}' sin entrada en capacidades_meta"
                    )
                    continue

                entrada_meta = meta_caps[k]

                if not isinstance(entrada_meta, dict):

                    errores.append(
                        f"{nombre}: capacidades_meta['{k}'] debe ser dict, es {type(entrada_meta).__name__}"
                    )
                    continue

                for campo in CLAVES_META_CAPACIDAD:

                    if campo not in entrada_meta:

                        errores.append(
                            f"{nombre}: capacidades_meta['{k}'] falta '{campo}'"
                        )

                    elif not isinstance(entrada_meta[campo], str):

                        errores.append(
                            f"{nombre}: capacidades_meta['{k}']['{campo}'] debe ser str"
                        )

        # =======================================================
        # 9. AUTORIZACIÓN ENGINE
        # =======================================================

        auth = meta.get("autoriza_engine")

        if not isinstance(auth, dict):

            errores.append(
                f"{nombre}: 'autoriza_engine' debe ser dict"
            )

        else:

            for permiso in PERMISOS_AUTORIZA_ENGINE:

                if permiso not in auth:

                    errores.append(
                        f"{nombre}: autoriza_engine falta permiso '{permiso}'"
                    )

                elif not isinstance(auth[permiso], bool):

                    errores.append(
                        f"{nombre}: autoriza_engine['{permiso}'] debe ser bool, es {type(auth[permiso]).__name__}"
                    )

            extras = set(auth) - set(PERMISOS_AUTORIZA_ENGINE)

            if extras:

                errores.append(
                    f"{nombre}: autoriza_engine permisos desconocidos: {sorted(extras)}"
                )

        # =======================================================
        # 10. REPORTING
        # =======================================================

        reporting = meta.get("reporting")

        if not isinstance(reporting, dict):

            errores.append(
                f"{nombre}: 'reporting' debe ser dict"
            )

        else:

            for bandera in BANDERAS_REPORTING:

                if bandera not in reporting:

                    errores.append(
                        f"{nombre}: reporting falta bandera '{bandera}'"
                    )

                elif not isinstance(reporting[bandera], bool):

                    errores.append(
                        f"{nombre}: reporting['{bandera}'] debe ser bool, es {type(reporting[bandera]).__name__}"
                    )

        # =======================================================
        # 11. ESTADOS VÁLIDOS
        # =======================================================

        ev = meta.get("estados_validos")

        if not isinstance(ev, list):

            errores.append(
                f"{nombre}: 'estados_validos' debe ser list"
            )

        elif not ev:

            errores.append(
                f"{nombre}: 'estados_validos' no puede estar vacío"
            )

        else:

            for i, est in enumerate(ev):

                if not isinstance(est, str):

                    errores.append(
                        f"{nombre}: estados_validos[{i}] debe ser str"
                    )

                elif est not in ESTADOS_CANONICOS:

                    errores.append(
                        f"{nombre}: estados_validos[{i}]='{est}' no es canónico. Admitidos: {ESTADOS_CANONICOS}"
                    )

        # =======================================================
        # 12. API ENGINE
        # =======================================================

        err_api = self._comparar_api(
            str(meta.get("api_engine", ""))
        )

        if err_api:
            errores.append(f"{nombre}: {err_api}")

        # =======================================================
        # 13. COMPATIBILIDAD
        # =======================================================

        err_cd = self._comparar_compatible_desde(
            str(meta.get("compatible_desde", "")),
            nombre
        )

        if err_cd:
            errores.append(err_cd)

        return errores

    # ===========================================================
    # DEPENDENCIAS
    # ===========================================================

    def _resolver_dependencias(self) -> None:

        presentes = (
            set(self.registro.por_rol.keys())
            | set(self.registro.por_id.keys())
            | set(self.registro.contenedores.keys())
        )

        faltantes: Dict[str, List[str]] = defaultdict(list)
        grafo_dep: Dict[str, List[str]] = defaultdict(list)

        # -------------------------------------------------------
        # DETECCIÓN DE DEPENDENCIAS
        # -------------------------------------------------------

        for nombre, cont in self.registro.contenedores.items():

            for dep in cont.requiere:

                grafo_dep[nombre].append(dep)

                if dep not in presentes:

                    faltantes[nombre].append(dep)

                    self.errores_arranque.append(
                        f"{cont.rol}/{nombre}: dependencia inexistente → '{dep}'"
                    )

        # -------------------------------------------------------
        # RESOLUCIÓN TOPOLÓGICA
        # -------------------------------------------------------

        in_degree = {
            n: 0
            for n in self.registro.contenedores
        }

        for src, dests in grafo_dep.items():

            for d in dests:

                if d in in_degree:

                    in_degree[d] += 1

        cola = deque(
            n
            for n, deg in in_degree.items()
            if deg == 0
        )

        orden: List[str] = []

        while cola:

            n = cola.popleft()
            orden.append(n)

            for d in grafo_dep.get(n, []):

                if d in in_degree:

                    in_degree[d] -= 1

                    if in_degree[d] == 0:
                        cola.append(d)

        # -------------------------------------------------------
        # DETECCIÓN DE CICLOS
        # -------------------------------------------------------

        ciclos = [
            n
            for n, deg in in_degree.items()
            if deg > 0
        ]

        if ciclos:

            self.errores_arranque.append(
                f"Ciclos de dependencia detectados: {ciclos}"
            )

        # -------------------------------------------------------
        # REGISTRO DE DEPENDENCIAS
        # -------------------------------------------------------

        self._dependencias = {
            "grafo": dict(grafo_dep),
            "faltantes": dict(faltantes),
            "orden_topologico": orden,
            "ciclos": ciclos
        }

    # ===========================================================
    # GRAFO
    # ===========================================================

    def _construir_grafo(self) -> None:

        nodos: List[Dict[str, Any]] = []
        aristas: List[Dict[str, Any]] = []

        # -------------------------------------------------------
        # NODOS DE MÓDULOS
        # -------------------------------------------------------

        for nombre, cont in self.registro.contenedores.items():

            nodos.append({
                "id": cont.id or nombre,
                "nombre": nombre,
                "rol": cont.rol,
                "tipo": "modulo"
            })

            # ---------------------------------------------------
            # ARISTAS DE DEPENDENCIAS
            # ---------------------------------------------------

            for dep in cont.requiere:

                aristas.append({
                    "from": nombre,
                    "to": dep,
                    "tipo": "requiere"
                })

            # ---------------------------------------------------
            # NODOS Y ARISTAS DE CAPACIDADES
            # ---------------------------------------------------

            for cap in cont.capacidades:

                cap_id = f"{nombre}.{cap}"

                nodos.append({
                    "id": cap_id,
                    "nombre": cap,
                    "tipo": "capacidad",
                    "modulo": nombre
                })

                aristas.append({
                    "from": nombre,
                    "to": cap_id,
                    "tipo": "declara_capacidad"
                })

        # -------------------------------------------------------
        # CONSOLIDACIÓN DEL GRAFO
        # -------------------------------------------------------

        self._grafo = {
            "nodos": nodos,
            "aristas": aristas
        }

    # ===========================================================
    # CENSO
    # ===========================================================

    def censar(self) -> Dict[str, Any]:

        return {
            "total": self.registro.total(),
            "roles": {
                rol: [c.nombre for c in lista]
                for rol, lista in self.registro.por_rol.items()
            },
            "roles_vacios": [],
            "rechazados": list(self.errores_arranque),
            "cargados": [
                {
                    "id": c.id,
                    "nombre": c.nombre,
                    "rol": c.rol,
                    "version": c.version,
                    "esquema": c.esquema,
                    "estabilidad": c.estabilidad,
                    "capacidades": list(c.capacidades.keys())
                }
                for c in self.registro.contenedores.values()
            ]
        }

    # ===========================================================
    # TRAZAS DE EJECUCIÓN
    # ===========================================================

    def _registrar_traza(
        self,
        modulo: str,
        capacidad: str,
        estado: str,
        duracion_s: float,
        error: Optional[str] = None,
        **extras: Any
    ) -> None:

        self._traza_seq += 1

        entrada: Dict[str, Any] = {
            "id_traza": self._traza_seq,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "modulo": modulo,
            "capacidad": capacidad,
            "estado": estado,
            "duracion_s": duracion_s
        }

        if error:
            entrada["error"] = error

        for clave, valor in extras.items():

            if valor is not None:
                entrada[clave] = valor

        self._trazas.append(entrada)

    def obtener_trazas(self) -> Tuple[Dict[str, Any], ...]:

        return tuple(
            dict(traza)
            for traza in self._trazas
        )

    # ===========================================================
    # MAPA DE RUTA DE EJECUCIÓN
    # ===========================================================

    def obtener_mapa_ruta(self) -> Tuple[Dict[str, Any], ...]:

        return tuple(
            dict(ruta)
            for ruta in self._mapa_ruta
        )

    # ===========================================================
    # RESOLUCIÓN DE CONTENEDOR
    # ===========================================================

    def _resolver_contenedor(
        self,
        modulo_o_rol: Any
    ) -> Tuple[Optional[Contenedor], Optional[str]]:

        if isinstance(modulo_o_rol, Contenedor):
            return modulo_o_rol, None

        cont = self.registro.primero(modulo_o_rol)

        if cont is None:
            return None, f"Módulo/rol no encontrado: {modulo_o_rol}"

        return cont, None

    # ===========================================================
    # VALIDACIÓN DE ENTRADA DE CAPACIDAD
    # ===========================================================

    def _validar_entrada_capacidad(
        self,
        cont: Contenedor,
        capacidad: str,
        args: Tuple[Any, ...],
        kwargs: Dict[str, Any]
    ) -> Optional[str]:

        fn = cont.fn(capacidad)

        if not callable(fn):
            return f"Capacidad '{capacidad}' no es ejecutable en {cont.nombre}"

        try:

            firma = inspect.signature(fn)
            firma.bind(*args, **kwargs)

        except ValueError:

            pass

        except TypeError as e:

            return f"Entrada incompatible con capacidad '{capacidad}': {e}"

        return None

    # ===========================================================
    # EJECUCIÓN CONTRACTUAL
    # ===========================================================

    def ejecutar_capacidad(
        self,
        modulo_o_rol: Any,
        capacidad: str,
        *args: Any,
        **kwargs: Any
    ) -> Dict[str, Any]:

        cont, error = self._resolver_contenedor(
            modulo_o_rol
        )

        if cont is None:
            return {
                "estado": "ERROR",
                "error": error
            }

        if cont.autoriza_engine.get("ejecutar") is not True:

            error = (
                f"{cont.nombre}: el contrato no autoriza "
                f"la ejecución por Engine"
            )

            return {
                "estado": "ERROR",
                "modulo": cont.nombre,
                "rol": cont.rol,
                "id": cont.id,
                "capacidad": capacidad,
                "error": error
            }

        fn = cont.fn(capacidad)

        if not callable(fn):

            error = (
                f"{cont.nombre}: la capacidad "
                f"'{capacidad}' no es callable"
            )

            return {
                "estado": "ERROR",
                "modulo": cont.nombre,
                "rol": cont.rol,
                "id": cont.id,
                "capacidad": capacidad,
                "error": error
            }

        error_entrada = self._validar_entrada_capacidad(
            cont,
            capacidad,
            args,
            kwargs
        )

        if error_entrada:

            return {
                "estado": "ERROR_ENTRADA",
                "modulo": cont.nombre,
                "rol": cont.rol,
                "id": cont.id,
                "capacidad": capacidad,
                "error": error_entrada
            }

        inicio = time.perf_counter()
        funcion_invocada = False

        try:

            funcion_invocada = True
            resultado = fn(*args, **kwargs)

            duracion = round(
                time.perf_counter() - inicio,
                6
            )

            self._registrar_traza(
                modulo=cont.nombre,
                capacidad=capacidad,
                estado="EXITO",
                duracion_s=duracion
            )

            salida = {
                "estado": "EXITO",
                "modulo": cont.nombre,
                "rol": cont.rol,
                "id": cont.id,
                "capacidad": capacidad,
                "resultado": resultado,
                "duracion_s": duracion
            }

            self.resultados_evaluacion.append(salida)

            return salida

        except Exception as e:

            duracion = round(
                time.perf_counter() - inicio,
                6
            )

            error_msg = f"{type(e).__name__}: {e}"

            self._registrar_traza(
                modulo=cont.nombre,
                capacidad=capacidad,
                estado="ERROR_EJECUCION",
                duracion_s=duracion,
                error=error_msg
            )

            salida = {
                "estado": "ERROR_EJECUCION",
                "modulo": cont.nombre,
                "rol": cont.rol,
                "id": cont.id,
                "capacidad": capacidad,
                "error": error_msg,
                "duracion_s": duracion
            }

            self.resultados_evaluacion.append(salida)

            return salida

    # ===========================================================
    # ATAJOS DE CAPACIDADES
    # ===========================================================

    def ejecutar_reporte(self, modulo_o_rol: Any) -> Dict[str, Any]:
        return self.ejecutar_capacidad(
            modulo_o_rol,
            "reporte"
        )

    def ejecutar_diagnostico(self, modulo_o_rol: Any) -> Dict[str, Any]:
        return self.ejecutar_capacidad(
            modulo_o_rol,
            "diagnostico"
        )

    def ejecutar_inventario(self, modulo_o_rol: Any) -> Dict[str, Any]:
        return self.ejecutar_capacidad(
            modulo_o_rol,
            "inventario"
        )

    def ejecutar_con_contexto_unificado(
        self,
        modulo_o_rol: Any,
        capacidad: str,
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:

        if not isinstance(payload, dict):

            return {
                "estado": "ERROR",
                "error": f"payload debe ser dict, es {type(payload).__name__}"
            }

        return self.ejecutar_capacidad(
            modulo_o_rol,
            capacidad,
            payload
        )

    # ===========================================================
    # INVOCADOR
    # ===========================================================

    def invocar(
        self,
        modulo: Any,
        capacidad: str,
        *args: Any,
        **kwargs: Any
    ) -> Any:

        salida = self.ejecutar_capacidad(
            modulo,
            capacidad,
            *args,
            **kwargs
        )

        if isinstance(salida, dict) and salida.get("estado") == "EXITO":
            return salida.get("resultado")

        if isinstance(salida, dict) and "error" in salida:
            raise RuntimeError(
                str(salida.get("error"))
            )

        return salida

    # ===========================================================
    # CONSOLIDACIÓN
    # ===========================================================

    def consolidar_reportes(self) -> Dict[str, Any]:

        for nombre, cont in self.registro.contenedores.items():

            if "reporte" in cont.capacidades:

                r = self.ejecutar_capacidad(
                    nombre,
                    "reporte"
                )

                self._reportes_modulos[nombre] = (
                    r.get("resultado")
                    if r.get("estado") == "EXITO"
                    else {
                        "error": r.get("error"),
                        "estado": "NO ENTREGADO POR MODULO"
                    }
                )

            if "diagnostico" in cont.capacidades:

                d = self.ejecutar_capacidad(
                    nombre,
                    "diagnostico"
                )

                if d.get("estado") == "EXITO":
                    self._diagnosticos[nombre] = d.get("resultado")

            if "inventario" in cont.capacidades:

                inv = self.ejecutar_capacidad(
                    nombre,
                    "inventario"
                )

                if inv.get("estado") == "EXITO":
                    self._inventarios[nombre] = inv.get("resultado")

        return {
            "reportes": self._reportes_modulos,
            "diagnosticos": self._diagnosticos,
            "inventarios": self._inventarios
        }

    # ===========================================================
    # PAQUETE OMEGA
    # ===========================================================

    def paquete_omega(self) -> Dict[str, Any]:

        if not self._reportes_modulos:
            self.consolidar_reportes()

        reportes_lista: List[Dict[str, Any]] = []

        reportes_lista.append({
            "id": "metadata",
            "titulo": "INFORMACIÓN DEL RUN",
            "orden": 0,
            "contenido": {
                "version_engine": self.VERSION,
                "esquema_contrato": ESQUEMA_CONTRATO_REQUERIDO,
                "version_contrato_requerida": VERSION_CONTRATO_REQUERIDA,
                "api_engine": API_ENGINE_ACTUAL,
                "estado_engine": self.estado,
                "invocador_id": self.invocador_id,
                "total_modulos": self.registro.total(),
                "errores_arranque": list(self.errores_arranque),
                "advertencias": list(self.advertencias),
                "trazas_n": len(self._trazas),
                "rutas_n": len(self._mapa_ruta),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        })

        orden = 1

        for nombre in sorted(
            self.registro.contenedores.keys()
        ):

            cont = self.registro.contenedores[nombre]

            reportes_lista.append({
                "id": cont.id or nombre,
                "titulo": f"MÓDULO {cont.rol}/{nombre}",
                "orden": orden,
                "contenido": {
                    "id": cont.id,
                    "nombre": cont.nombre,
                    "rol": cont.rol,
                    "version": cont.version,
                    "version_contrato": cont.version_contrato,
                    "esquema": cont.esquema,
                    "estabilidad": cont.estabilidad,
                    "compatible_desde": cont.compatible_desde,
                    "api_engine": cont.api_engine,
                    "descripcion": cont.descripcion,
                    "funcion": cont.funcion,
                    "no_hace": cont.no_hace,
                    "autoridad": cont.autoridad,
                    "conocimiento_exportable": cont.conocimiento_exportable,
                    "consultas_soportadas": cont.consultas_soportadas,
                    "requiere": cont.requiere,
                    "autoriza_engine": cont.autoriza_engine,
                    "capacidades": list(cont.capacidades.keys()),
                    "capacidades_meta": cont.capacidades_meta,
                    "estados_validos": cont.estados_validos,
                    "invariantes": cont.invariantes,
                    "reporte": self._reportes_modulos.get(nombre),
                    "diagnostico": self._diagnosticos.get(nombre),
                    "inventario": self._inventarios.get(nombre)
                }
            })

            orden += 1

        reportes_lista.append({
            "id": "dependencias",
            "titulo": "DEPENDENCIAS",
            "orden": orden,
            "contenido": self._dependencias
        })

        orden += 1

        reportes_lista.append({
            "id": "grafo",
            "titulo": "GRAFO ESTRUCTURAL",
            "orden": orden,
            "contenido": self._grafo
        })

        orden += 1

        reportes_lista.append({
            "id": "trazas",
            "titulo": "TRAZAS DE EJECUCIÓN",
            "orden": orden,
            "contenido": list(self._trazas)
        })

        orden += 1

        reportes_lista.append({
            "id": "mapa_ruta",
            "titulo": "MAPA DE RUTA DE EJECUCIÓN",
            "orden": orden,
            "contenido": list(self._mapa_ruta)
        })

        return {
            "metadata": {
                "version_engine": self.VERSION,
                "estado_engine": self.estado,
                "esquema_contrato": ESQUEMA_CONTRATO_REQUERIDO,
                "total_modulos": self.registro.total(),
                "trazas_n": len(self._trazas),
                "rutas_n": len(self._mapa_ruta),
                "timestamp": datetime.now(timezone.utc).isoformat()
            },
            "reportes": reportes_lista
        }

    # ===========================================================
    # ESTADO GLOBAL
    # ===========================================================

    def estado_global(self) -> Dict[str, Any]:

        return {
            "tipo": "estado_global",
            "version_engine": self.VERSION,
            "esquema_contrato": ESQUEMA_CONTRATO_REQUERIDO,
            "estado": self.estado,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_contenedores": self.registro.total(),
            "errores_arranque": list(self.errores_arranque),
            "advertencias": list(self.advertencias),
            "trazas_n": len(self._trazas),
            "rutas_n": len(self._mapa_ruta),
            "dependencias": self._dependencias,
            "grafo": self._grafo
        }

    # ===========================================================
    # CENTINELA
    # ===========================================================

    @property
    def centinela(self) -> Centinela:

        if self._centinela is None:
            self._centinela = Centinela(
                invocador=self
            )

        return self._centinela

    def verificar_con_centinela(
        self,
        paquete: Dict[str, Any],
        *,
        depositar_salida: bool = True
    ) -> Veredicto:

        inicio = time.perf_counter()

        try:

            veredicto = self.centinela.verificar(
                paquete,
                depositar_salida=depositar_salida
            )

            duracion = round(
                time.perf_counter() - inicio,
                6
            )

            self._registrar_traza(
                modulo="ENGINE",
                capacidad="verificar_con_centinela",
                estado=str(veredicto.estado),
                duracion_s=duracion
            )

            return veredicto

        except Exception as e:

            duracion = round(
                time.perf_counter() - inicio,
                6
            )

            error = f"{type(e).__name__}: {e}"

            self._registrar_traza(
                modulo="ENGINE",
                capacidad="verificar_con_centinela",
                estado="ERROR_AUDITORIA",
                duracion_s=duracion,
                error=error
            )

            raise


# ===========================================================
# EXPORTACIONES
# ===========================================================

__all__ = [
    "Engine",
    "ArranqueError",
    "Contenedor",
    "RegistroModulos",
    "VERSION_ENGINE",
    "ESQUEMA_CONTRATO_REQUERIDO",
    "VERSION_CONTRATO_REQUERIDA"
]


# ===========================================================
# FIN DEL MÓDULO ENGINE
# ===========================================================
