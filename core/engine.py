# ==============================================================
# VPSI-TRUTH — core/engine.py DIRECTOR ARQUITECTO SIMBIOSIS MECANICA
# ===============================================================
#
# ENGINE
# Versión:            20.0
# Esquema contrato:   VPSI-CONTRACT-2.0
# API Engine:         1.0
#
# Función:
#   Agente ejecutor y director arquitectónico del sistema.
#
#   El Engine constituye la capa de coordinación entre los contratos
#   y las capacidades de los módulos. No sustituye la autoridad de
#   ningún módulo ni reproduce internamente las operaciones que el
#   contrato asigna a cada uno.
#
#   Descubre módulos. Lee contratos. Valida contratos.
#   Registra módulos. Resuelve dependencias.
#   Construye el grafo estructural.
#   Resuelve capacidades declaradas.
#   Ejecuta capacidades autorizadas.
#   Entrega el contenido al módulo correspondiente.
#   Recibe el resultado real producido por el módulo.
#   Registra trazas.
#   Registra el mapa de ruta de ejecución.
#   Consolida reportes.
#   Entrega paquete_omega().
#
#   Para la Fórmula de la Verdad, el Engine incorpora la capacidad
#   de evaluación global. Esta capacidad no reemplaza las funciones
#   matemáticas de Calculator ni de Formulas: coordina la evaluación
#   de los módulos, integra sus resultados y conduce la información
#   resultante por la cadena contractual hasta obtener la Verdad
#   Cuantificada.
#
#   La evaluación global se estructura de la siguiente manera:
#
#                         ENGINE
#                           │
#                        evaluar
#                           │
#             ┌─────────────┼─────────────┐
#             ▼             ▼             ▼
#           Módulo        Módulo        Módulo
#             │             │             │
#             └─────────────┼─────────────┘
#                           ▼
#                       Calculator
#                         C L K
#                           ▼
#                        Formulas
#                         Tru_Ri
#                           ▼
#                        Tru_total
#                           ▼
#                   VERDAD CUANTIFICADA
#
#   En esta arquitectura:
#
#     ENGINE
#       → dirige y coordina.
#
#     evaluar
#       → reúne y encadena la evaluación contractual necesaria.
#
#     MÓDULOS
#       → ejecutan sus propias capacidades y producen sus resultados.
#
#     Calculator
#       → calcula los factores C, L y K conforme a su contrato.
#
#     Formulas
#       → aplica las fórmulas de Tru_Ri y Tru_total conforme a su
#         contrato.
#
#     ENGINE
#       → recibe, registra, consolida y entrega el resultado final.
#
#   El Engine no inventa capacidades, parámetros, resultados ni
#   contratos. Toda operación debe existir y estar autorizada por
#   la arquitectura contractual correspondiente.
#
#   La capacidad de evaluación está limitada por la unión coherente
#   de los contratos, capacidades, entradas, salidas, dependencias
#   e invariantes declarados por los módulos.
#
# ===============================================================
# ===============================================================
# Parte 1 IMPORTACIONES
# ===============================================================

from __future__ import annotations

import importlib
import importlib.util
import inspect
import math
import pkgutil
import re
import sys
import time
from collections import defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from core.centinela import Centinela, Veredicto

# --- Igual que el otro repo (rutas VPSI) ---
from modules.formulas.formulas_omega.coherence import (
    CoherenceEngine as FormulaEngine,
    SessionStateOmega,
)
from modules.formulas.formulas_omega.constants import ALPHA, BETA, PHI, S_REF

ALPHA_VPSI = float(ALPHA)
BETA_VPSI = float(BETA)
EPSILON = 1e-12


# ===============================================================
# Parte 2 CONSTANTES /el esquema de contrato requerido,
#  la versión de contrato exigida y la API actual del Engine
# ===============================================================
VERSION_ENGINE = "20"
ESQUEMA_CONTRATO_REQUERIDO = "VPSI-CONTRACT-1.0"
VERSION_CONTRATO_REQUERIDA = "1.0"
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
    "esquema", "version_contrato",
    "version_modulo", "id", "nombre",
    "rol", "descripcion",
    "funcion", "no_hace", "autoridad",
    "conocimiento_exportable",
    "requiere", "autoriza_engine",
    "consultas_soportadas",
    "capacidades", "capacidades_meta",
    "reporting", "estados_validos",
    "invariantes", "estabilidad", "acceso",
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
    "inventariar", "alterar",
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
    "monitorear", "acceso_archivos", "ejecutar_total", 
    "inspeccionar", "registrar_inventario",
    "evaluar_universal",
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
    "validar_esquema", "evaluar_universal"
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
    "invariantes", "acceso_archivos",
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
class ContratoError(Exception):
    """Contrato CONTENEDOR inválido o capacidad no resoluble."""
    pass
class AgenciaMatematicaError(Exception):
    """Fallo de la pared matemática del Engine."""
    pass


class CapasInvalidasError(AgenciaMatematicaError):
    """Self no entregó capas utilizables."""
    pass


class FormulaNoDisponibleError(AgenciaMatematicaError):
    """FO no expone la capacidad matemática requerida."""
    pass

class PurposeAlignmentError(Exception):
    """Fricción distinta de cero en la capa L6 Propósito."""
    pass

class StructuralIntegrityError(Exception):
    """Violación de la invariancia estructural VPSI."""
    pass

class CircularityDetectedError(Exception):
    """Referencias o retroalimentación circular en fórmulas."""
    pass

# ===============================================================
# Parte 9.1 VALIDADOR ANTI-HACK
# Encargado de la integridad matemática, verificación de fricción
# y prevención de ciclos/manipulación.
# ===============================================================

class AntiHackValidation:
    """Capa Anti-Hack para validación estricta de entradas y prevención de manipulación."""

    @staticmethod
    def is_finite_number(value: Any) -> bool:
        return isinstance(value, (int, float)) and math.isfinite(value)

    @classmethod
    def detect_reference_cycle(cls, obj: Any, seen: Optional[set] = None, path: str = "root") -> None:
        if seen is None:
            seen = set()
        if isinstance(obj, (dict, list, tuple, set)):
            obj_id = id(obj)
            if obj_id in seen:
                raise CircularityDetectedError(f"Referencia circular detectada en {path}.")
            seen.add(obj_id)
            if isinstance(obj, dict):
                for k, v in obj.items():
                    cls.detect_reference_cycle(v, seen, f"{path}.{k}")
            else:
                for i, v in enumerate(obj):
                    cls.detect_reference_cycle(v, seen, f"{path}[{i}]")
            seen.remove(obj_id)

    @classmethod
    def validate_layer_data(cls, layers_data: List[Dict[str, Any]]) -> None:
        cls.detect_reference_cycle(layers_data)
        if not isinstance(layers_data, list) or len(layers_data) != 7:
            raise ValueError("layers_data debe ser una lista de exactamente 7 capas.")

        for i, layer in enumerate(layers_data):
            if not isinstance(layer, dict) or "L" not in layer or "phi" not in layer:
                raise KeyError(f"La capa L{i} debe incluir 'L' y 'phi'.")

            L, phi = layer["L"], layer["phi"]
            if not cls.is_finite_number(L) or not cls.is_finite_number(phi):
                raise StructuralIntegrityError(f"Valores no finitos en L{i}: L={L}, phi={phi}.")
            if not (0.0 <= L <= 1.0) or not (0.0 <= phi <= 1.0):
                raise StructuralIntegrityError(f"Valores fuera del dominio [0,1] en L{i}.")

        if layers_data[6]["phi"] != 0.0:
            raise PurposeAlignmentError(
                f"La capa L6 debe tener fricción phi = 0.0, obtenido {layers_data[6]['phi']}."
            )

    @classmethod
    def assert_truth_formula(cls, C: float, L: float, K: float, truth_value: float) -> None:
        # Fórmula: (C * L * K * ALPHA_VPSI) + BETA_VPSI
        expected = (C * L * K * ALPHA_VPSI) + BETA_VPSI
        if abs(truth_value - expected) > EPSILON:
            raise StructuralIntegrityError(
                f"Violación de fórmula de verdad: esperado {expected}, obtenido {truth_value}."
            )
        if not (BETA_VPSI - EPSILON <= truth_value <= 1.0 + EPSILON):
            raise StructuralIntegrityError(
                f"Valor de verdad fuera de límites [{BETA_VPSI}, 1.0]: {truth_value}."
            )

    @classmethod
    def detect_formula_circularity(cls, c_omega: float, truth_value: float) -> None:
        if abs(c_omega - truth_value) <= EPSILON and c_omega not in (0.0, 1.0):
            raise CircularityDetectedError("Colapso circular detectado entre CΩ y Truth_total.")


# ===============================================================
# ROLES
# ===============================================================
ROLES: Tuple[str, ...] = (
    "CT", "AX", "FO", "MC", "SF", "CA", "CX", "DI",
    "RE", "VX", "TX", "CH", "CIT",
)
OBLIGATORIOS: Tuple[str, ...] = ("CT", "AX", "FO", "MC", "SF")  

# ===============================================================
# Parte 10 CONTENEDOR LIBRERIAS Y CONTRATO Y ESPECIDICACIONES 
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
# Parte 11 — DEF/ REGISTROS DE MODULOS EN  CONTRATOS
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
        # Parte 11.2.2 — NO SE ACEPTAN duplicados DE MODULO
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

        # 11.3.1 Búsqueda por nombre
        if clave in self.contenedores:
            return self.contenedores[clave]

        # 11.3.2 Búsqueda por id
        if clave in self.por_id:
            return self.por_id[clave]

        # 11.3.3 Búsqueda por rol (único)
        lista = self.por_rol.get(clave)
        return lista[0] if lista else None

    def total(self) -> int:
        """Número total de Contenedores registrados."""
        return len(self.contenedores)
        
# ===============================================================
# Parte 12 ENGINE AQUI SE DEFINEN LAS DECLARACIONES
# ===============================================================

class Engine:

    VERSION = VERSION_ENGINE

    # ===========================================================
    # DECLARACIÓN PROPÓSITO FUNDAMENTAL (MANDATO INVARIABLE)
    # ===========================================================
    
    PROPOSITO_FUNDAMENTAL = "Calcular la verdad de cualquier descripcion"
    CLAVE_PROPOSITO = "evaluar_universal"
    
    def __init__(self, raiz_modulos: str | Path, invocador_id: str = "core", strict: bool = True) -> None:
        # =======================================================
        # Parte 12.1 CONFIGURACIÓN BÁSICA
        # =======================================================
        self._layers = {}
        self._memory_layer = None
        self._L7_emergent = 1.0 

        self.raiz = Path(raiz_modulos).resolve()
        self.invocador_id = invocador_id
        self.strict = strict

        # Propósito parametrizable o fijado por instancia
        self.proposito: str = self.PROPOSITO_FUNDAMENTAL
        self.clave_proposito: str = self.CLAVE_PROPOSITO

        # =======================================================
        # Parte 12.2 ESTADO
        # =======================================================

        self.estado = ESTADO_NO_INICIADO
        self.registro = RegistroModulos()
        self.errores_arranque: List[str] = []
        self.advertencias: List[str] = []
        self.fallos: List[Dict[str, Any]] = []
        self.resultados_evaluacion: List[Any] = []

                     # Estado y capas del Teorema VPSI
        self._layers: Dict[int, Dict[str, float]] = {}
        self._memory_layer: Optional[Dict[str, Any]] = None
        self._L7_emergent: float = 1.0

        # =======================================================
        # Parte 12.2 TRAZAS
        # =======================================================

        self._trazas: List[Dict[str, Any]] = []
        self._traza_seq: int = 0

        # =======================================================
        # Parte 12.3 MAPA DE RUTA
        # =======================================================

        self._mapa_ruta: List[Dict[str, Any]] = []
        self._ruta_seq: int = 0

        # =======================================================
        # Parte 12.4 CENTINELA — PRIORIDAD ABSOLUTA
        # =======================================================

        self._centinela: Optional[Centinela] = None

        # =======================================================
        # Parte 12.5 ESTRUCTURAS INTERNAS
        # =======================================================

        self._modulos_descubiertos: List[Path] = []
        self._reportes_modulos: Dict[str, Any] = {}
        self._diagnosticos: Dict[str, Any] = {}
        self._inventarios: Dict[str, Any] = {}
        self._dependencias: Dict[str, Any] = {}
        self._grafo: Dict[str, Any] = {}

        # =======================================================
        # Parte 12.6 ARRANQUE
        # =======================================================

        self._modulos_descubiertos = self._descubrir_modulos()
        self._cargar_y_validar()
        self._resolver_dependencias()
        self._construir_grafo()
        self._extraer_y_entregar_comentarios()

        # =======================================================
        # Parte 12.7 ESTADO FINAL
        # =======================================================

        if self.errores_arranque:
            self.estado = ESTADO_RECHAZADO
            if self.strict:
                raise ArranqueError("Engine no pudo arrancar:\n  - " + "\n  - ".join(self.errores_arranque))
        else:
            self.estado = ESTADO_OPERATIVO

    # ===========================================================
    # Parte 12.8 DESCUBRIMIENTO
    # ===========================================================

    def _descubrir_modulos(self) -> List[Path]:
        if not self.raiz.is_dir(): return []
        return [p for p in sorted(self.raiz.iterdir()) if p.is_dir() and (p / "__init__.py").is_file()]

    # ===========================================================
    # Métodos de validación de Propósito
    # ===========================================================

    def obtener_proposito(self) -> Dict[str, str]:
        """Devuelve la declaración explicita del propósito del Engine."""
        return {
            "proposito": self.proposito,
            "clave": self.clave_proposito
        }
    # ===========================================================
    # Parte 12.9 EJECUCIÓN DEL PROPÓSITO FUNDAMENTAL
    # ===========================================================

    def ejecutar_proposito(
        self,
        entrada: Any,
        *args: Any,
        **kwargs: Any
    ) -> Any:
        """
        Ejecuta el propósito fundamental del Engine:

            CALCULAR LA VERDAD

        La ejecución se delega íntegramente en la capacidad
        declarada contractualmente por los módulos del sistema.
        """

        if self.estado != ESTADO_OPERATIVO:
            raise RuntimeError(
                f"El Engine no está operativo. Estado actual: {self.estado}"
            )

        existencia = self.resolver_existencia(
            self.clave_proposito
        )

        if existencia.get("estado") != "EXISTE":
            raise RuntimeError(
                f"La capacidad fundamental "
                f"'{self.clave_proposito}' no existe "
                f"en el repertorio contractual."
            )

        modulo = existencia.get("modulo")
        capacidad = existencia.get("capacidad")

        if not modulo or not capacidad:
            raise RuntimeError(
                f"No se pudo resolver la capacidad ejecutable "
                f"del propósito '{self.clave_proposito}'."
            )

        resultado = self.ejecutar_capacidad(
            modulo,
            capacidad,
            entrada,
            *args,
            **kwargs
        )

        self.resultados_evaluacion.append({
            "clave_proposito": self.clave_proposito,
            "proposito": self.proposito,
            "entrada": entrada,
            "modulo": modulo,
            "capacidad": capacidad,
            "resultado": resultado,
        })

       
    # ============================================================
    # ANTI-HACK / STRUCTURAL GUARD
    # ============================================================

    def _is_finite_number(self, value):
        return isinstance(value, (int, float)) and math.isfinite(value)

    def _detect_reference_cycle(self, obj, seen=None, path="root"):
        """
        Detecta circularidad real de objetos:
        ejemplo: a = []; a.append(a)
        """
        if seen is None:
            seen = set()

        if isinstance(obj, (dict, list, tuple, set)):
            obj_id = id(obj)

            if obj_id in seen:
                raise CircularityDetectedError(
                    f"Circular reference detected at {path}."
                )

            seen.add(obj_id)

            if isinstance(obj, dict):
                for key, value in obj.items():
                    self._detect_reference_cycle(value, seen, f"{path}.{key}")
            else:
                for i, value in enumerate(obj):
                    self._detect_reference_cycle(value, seen, f"{path}[{i}]")

            seen.remove(obj_id)

    def _validate_layer_data(self, layers_data):
        """
        Valida que layers_data cumpla estructura base:
        - lista
        - exactamente 7 capas
        - cada capa es dict
        - cada capa tiene L y phi
        - L y phi son números finitos
        - L ∈ [0,1]
        - phi ∈ [0,1]
        """
        self._detect_reference_cycle(layers_data)

        if not isinstance(layers_data, list):
            raise TypeError("layers_data must be a list of 7 layer dictionaries.")

        if len(layers_data) != 7:
            raise ValueError(
                f"layers_data must contain exactly 7 layers, got {len(layers_data)}."
            )

        for i, layer in enumerate(layers_data):
            if not isinstance(layer, dict):
                raise TypeError(f"Layer L{i} must be a dictionary.")

            if "L" not in layer:
                raise KeyError(f"Layer L{i} is missing required key 'L'.")

            if "phi" not in layer:
                raise KeyError(f"Layer L{i} is missing required key 'phi'.")

            L = layer["L"]
            phi = layer["phi"]

            if not self._is_finite_number(L):
                raise StructuralIntegrityError(
                    f"Layer L{i} activation must be a finite number, got {L}."
                )

            if not self._is_finite_number(phi):
                raise StructuralIntegrityError(
                    f"Layer L{i} friction phi must be a finite number, got {phi}."
                )

            if not 0.0 <= L <= 1.0:
                raise StructuralIntegrityError(
                    f"Layer L{i} activation violates domain [0,1], got {L}."
                )

            if not 0.0 <= phi <= 1.0:
                raise StructuralIntegrityError(
                    f"Layer L{i} friction phi violates domain [0,1], got {phi}."
                )

        if layers_data[6]["phi"] != 0.0:
            raise PurposeAlignmentError(
                f"L6 Purpose layer must have friction phi = 0.0, got {layers_data[6]['phi']}."
            )

    def _validate_external_inputs(self, C1, C2, theta):
        for name, value in {"C1": C1, "C2": C2, "theta": theta}.items():
            if not self._is_finite_number(value):
                raise StructuralIntegrityError(
                    f"{name} must be a finite number, got {value}."
                )

        if C1 < 0.0 or C2 < 0.0:
            raise StructuralIntegrityError(
                f"External coherences must be non-negative, got C1={C1}, C2={C2}."
            )

    def _assert_truth_formula(self, C, L, K, truth_value):
        """
        Anti-manipulación:
        verifica que la salida cumpla exactamente la fórmula base:

        Truth_total = beta + alpha * C * L * K
        """
        expected = BETA_VPSI + (ALPHA_VPSI * C * L * K)

        if abs(truth_value - expected) > EPSILON:
            raise StructuralIntegrityError(
                f"Truth formula violation: expected {expected}, got {truth_value}."
            )

        if truth_value < BETA_VPSI - EPSILON:
            raise StructuralIntegrityError(
                f"Truth value below structural floor beta: {truth_value}."
            )

        if truth_value > 1.0 + EPSILON:
            raise StructuralIntegrityError(
                f"Truth value above structural ceiling 1: {truth_value}."
            )

    def _detect_formula_circularity(self, c_omega, truth_value):
        """
        Detecta circularidad funcional simple:
        el sistema no debe usar Truth_total como si fuera C_omega de entrada.
        """
        if abs(c_omega - truth_value) <= EPSILON and c_omega not in (0.0, 1.0):
            raise CircularityDetectedError(
                "Formula circularity detected: CΩ and Truth_total collapsed into same value."
            )

    # ============================================================
    # LAYERS
    # ============================================================

    def _init_layers_silent(self):
        try:
            layer_files = list(LAYERS_DIR.rglob("*.py"))
            for file_path in layer_files:
                if file_path.parent.name.startswith("L") or file_path.name.startswith("L"):
                    layer_name = file_path.stem.replace("_", "")
                    spec = importlib.util.spec_from_file_location(layer_name, file_path)
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[layer_name] = module
                    spec.loader.exec_module(module)

                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if callable(attr) and (
                            attr_name.endswith("Layer") or attr_name.startswith("L")
                        ):
                            instance = attr()
                            layer_data = {
                                "instance": instance,
                                "L": getattr(instance, "L", 1.0),
                                "phi": getattr(instance, "phi", 0.0),
                            }
                            if "memory" in layer_name.lower():
                                self._memory_layer = instance
                            self._layers[layer_name] = layer_data
                            break
        except Exception:
            pass

    def _update_live_layers_silent(self):
        if self._memory_layer:
            try:
                memories = self._memory_layer.retrieve("coherencia")
                context_L = min(1.0, len(memories) * 0.1)

                for layer_data in self._layers.values():
                    instance = layer_data["instance"]
                    if hasattr(instance, "activate"):
                        instance.activate(context_L, layer_data["phi"])
                        layer_data["L"] = getattr(instance, "L", 1.0)
            except Exception:
                pass

    def _compute_L7_silent(self):
        try:
            base_layers = [
                l for n, l in self._layers.items()
                if n.startswith("L") and int(n[1]) <= 6
            ]
        except Exception:
            return 1.0

        if len(base_layers) < 6:
            return 1.0

        product = 1.0
        for layer in base_layers:
            contrib = layer["L"] * (1.0 - layer["phi"])
            product *= max(0.0, contrib)

        return min(ALPHA_VPSI, product)

    # ============================================================
    # VPSI TRUTH THEOREM
    # ============================================================

    def apply_vpsi_truth(self, C, L=1.0, K=1.0):
        """
        Truth_total(D) = beta + alpha * C(D) * L(D) * K(D)
        """
        for name, value in {"C": C, "L": L, "K": K}.items():
            if not self._is_finite_number(value):
                raise StructuralIntegrityError(
                    f"{name} must be a finite number, got {value}."
                )

            if not 0.0 <= value <= 1.0:
                raise StructuralIntegrityError(
                    f"{name} violates domain [0,1], got {value}."
                )

        ri = C * L * K
        truth_total = BETA_VPSI + (ALPHA_VPSI * ri)

        self._assert_truth_formula(C, L, K, truth_total)

        return float(truth_total)

    # ============================================================
    # LEGACY METHODS
    # ============================================================

    def calculate_harmony(self, entropy, s_max=1.0):
        if not self._is_finite_number(entropy):
            raise StructuralIntegrityError(f"entropy must be finite, got {entropy}.")

        if not self._is_finite_number(s_max):
            raise StructuralIntegrityError(f"s_max must be finite, got {s_max}.")

        if s_max == 0:
            return 0.0

        return float(1.0 - (entropy / s_max))

    def calculate_external_coherence(self, C1, C2, theta):
        self._validate_external_inputs(C1, C2, theta)

        theta_rad = math.radians(theta)
        inner = C1**2 + C2**2 + 2.0 * C1 * C2 * math.cos(theta_rad)

        return float(math.sqrt(max(0.0, inner)))

    def compute_coherence(self, layers_data, C1=1.0, C2=1.0, theta=0.0):
        """
        Core deterministic computation.
        Siempre retorna float si las entradas respetan la estructura.
        """
        self._validate_layer_data(layers_data)
        self._validate_external_inputs(C1, C2, theta)

        if HAS_LAYERS:
            self._update_live_layers_silent()
            self._L7_emergent = self._compute_L7_silent()

        activations = [float(ld["L"]) for ld in layers_data]
        frictions = [float(ld["phi"]) for ld in layers_data]

        if all(a == 0.0 for a in activations):
            return 0.0

        external_coherences = None
        if C1 != 1.0 or C2 != 1.0 or theta != 0.0:
            i_ext = self.calculate_external_coherence(C1, C2, theta)
            external_coherences = [i_ext]

        c_omega = self.state.update(
            activations=activations,
            frictions=frictions,
            external_coherences=external_coherences,
        )

        if not self._is_finite_number(c_omega):
            raise StructuralIntegrityError(f"CΩ must be finite, got {c_omega}.")

        c_omega = min(ALPHA_VPSI, max(0.0, float(c_omega)))

        l_val = activations[1] if len(activations) > 1 else 1.0
        k_val = activations[2] if len(activations) > 2 else 1.0

        truth_val = self.apply_vpsi_truth(c_omega, l_val, k_val)

        self._detect_formula_circularity(c_omega, truth_val)

        # No doble escalado de CΩ.
        # CΩ ya viene escalado desde formulas.coherence.
        # Aquí solo se aplica VPSI + L7 emergente.
        result = truth_val * self._L7_emergent
        result = min(1.0, max(0.0, result))

        return float(result)

    def compute_live_coherence(self):
        if not HAS_LAYERS or not self._layers:
            return {
                "coherence": 1.0,
                "layers": 0,
                "mode": "NO_LAYERS",
            }

        self._update_live_layers_silent()
        L7 = self._compute_L7_silent()

        activations = [float(l["L"]) for l in self._layers.values()]
        frictions = [float(l["phi"]) for l in self._layers.values()]

        c_omega = self.state.update(
            activations=activations,
            frictions=frictions,
        )

        c_omega = min(ALPHA_VPSI, max(0.0, float(c_omega)))

        structural_truth = self.apply_vpsi_truth(c_omega)

        self._detect_formula_circularity(c_omega, structural_truth)

        result = structural_truth * L7
        result = min(1.0, max(0.0, result))

        

    # ===========================================================
    # Parte 13 LECTURA DEL CONTRATO
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
    # Parte 13.1 CARGA VALIDACION DEL REGISTRO
    # ===========================================================

    def _cargar_y_validar(self) -> None:

        for path_dir in self._modulos_descubiertos:

            # ---------------------------------------------------
            # Parte 13.1.1 LEER CONTRATO Y MATERIALIZAR MÓDULO
            # ---------------------------------------------------

            leido = self._leer_contrato(path_dir)

            if leido is None:
                continue

            meta = leido["meta"]
            nombre = meta.get("nombre") or leido["nombre_carpeta"]
            mod = leido["modulo"]

            # ---------------------------------------------------
            # Parte 13.1.3 ARCHIVOS PY
            # ---------------------------------------------------

            archivos_py = sorted(
                p for p in path_dir.rglob("*.py")
                if p.is_file()
            )

            # ---------------------------------------------------
            # Parte 13.1.4 CONTEXTO ESTRUCTURAL DEL MÓDULO
            # ---------------------------------------------------

            setattr(
                mod,
                "ARCHIVOS_PY",
                archivos_py,
            )

            # ---------------------------------------------------
            # Parte 13.1.5 VALIDACIÓN DEL CONTRATO
            # ---------------------------------------------------

            errores = self._validar_esquema(
                meta,
                nombre,
            )

            if errores:
                self.errores_arranque.extend(errores)
                continue

            # ---------------------------------------------------
            # Parte 13.1.7 MATERIALIZACIÓN DEL CONTENEDOR
            # ---------------------------------------------------

            cont = Contenedor(
                meta=meta,
                modulo=mod,
                ruta=leido["ruta"],
            )

            # ---------------------------------------------------
            # Parte 13.1.8 REGISTRO DEL MÓDULO
            # ---------------------------------------------------

            errores_dup = self.registro.registrar(cont)
            if errores_dup:
                for error in errores_dup:
                    self.errores_arranque.append(f"{nombre}: {error}")

    # ===========================================================
    # Parte 14 DECLARACIÓN 1 — RESOLUCIÓN POR EXISTENCIA CONTRACTUAL
    # Esta capacidad determina si un elemento X está presente en 
    # el repertorio completo de declaraciones disponibles en el sistema.
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
        # Parte 14.1 REPERTORIO CONTRACTUAL COMPLETO
        # -------------------------------------------------------

        for cont in self.registro.contenedores.values():

            # ---------------------------------------------------
            # Parte 14.1.1 CAPACIDADES DECLARADAS/EXISTE → X está registrado 
            # en alguna capacidad, declaración, consulta, 
            # autoridad o invariante de algún Contenedor.
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
            # Parte 14.1.2 DECLARACIONES CONTRACTUALES
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
        # Parte 14.1.3 X NO EXISTE/NO_EXISTE → X no está registrado en ningún lugar.
        # -------------------------------------------------------

        return {
            "estado": "NO_EXISTE",
            "existe": False,
            "peticion": x,
            "razon": "NO_EXISTE",
        }

    # ===========================================================
    # Parte 14.2 DECLARACIÓN 2 — RESOLUCIÓN DE PETICIÓN
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
    # Parte 15 VALIDACIÓN DE LISTAS STR
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
    # Parte 16 VERSIONES capacidad de identificar las versiones de casa modulo
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
    # Parte 17 VALIDACIÓN DEL ESQUEMA DEL CONTRATO
    # ===========================================================

    def _validar_esquema(
        self,
        meta: Dict[str, Any],
        nombre: str
    ) -> List[str]:

        errores: List[str] = []

       
        # =======================================================
        # Parte 17.1 ESQUEMA
        # =======================================================

        if meta.get("esquema") != ESQUEMA_CONTRATO_REQUERIDO:
            errores.append(
                f"{nombre}: esquema '{meta.get('esquema')}' != '{ESQUEMA_CONTRATO_REQUERIDO}'"
            )

        # =======================================================
        # Parte 17.2 VERSIÓN DEL CONTRATO
        # =======================================================

        vc = meta.get("version_contrato")

        if str(vc) != VERSION_CONTRATO_REQUERIDA:
            errores.append(
                f"{nombre}: version_contrato '{vc}' != '{VERSION_CONTRATO_REQUERIDA}'"
            )

        # =======================================================
        # Parte 17.3 VERSIÓN DEL MÓDULO
        # =======================================================

        vm = meta.get("version_modulo")

        if not isinstance(vm, str) or not vm.strip():
            errores.append(
                f"{nombre}: version_modulo debe ser str no vacío, es {type(vm).__name__}"
            )

        # =======================================================
        # Parte 17.4 CLAVES OBLIGATORIAS
        # =======================================================

        for clave in CLAVES_OBLIGATORIAS_CONTRATO:

            if clave not in meta:
                errores.append(
                    f"{nombre}: falta clave obligatoria '{clave}'"
                )

        # =======================================================
        # Parte 17.5 LISTAS DE STR OBLIGATORIAS
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
        # Parte 17.6 DEPENDENCIAS (requiere)
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
        # Parte 17.7 CAPACIDADES
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
        # Parte 17.8 METADATOS DE CAPACIDADES
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

                    elif not isinstance(entrada_meta[campo], (str, list)):    # ← ACEPTA str O list

                        errores.append(
                            f"{nombre}: capacidades_meta['{k}']['{campo}'] debe ser str o list"
                        )

        # =======================================================
        # Parte 17.9 AUTORIZACIÓN ENGINE
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
        # Parte 17.10 REPORTING
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
        # Parte 17.11 ESTADOS VÁLIDOS
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
        # Parte 17.12 API ENGINE
        # =======================================================

        err_api = self._comparar_api(
            str(meta.get("api_engine", ""))
        )

        if err_api:
            errores.append(f"{nombre}: {err_api}")

        # =======================================================
        # Parte 17.13 COMPATIBILIDAD
        # =======================================================

        err_cd = self._comparar_compatible_desde(
            str(meta.get("compatible_desde", "")),
            nombre
        )

        if err_cd:
            errores.append(err_cd)

        return errores

    # ===========================================================
    # Parte 18 DEPENDENCIAS
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
        # Parte 18.1 DETECCIÓN DE DEPENDENCIAS
        # -------------------------------------------------------

        for nombre, cont in self.registro.contenedores.items():

            for dep in cont.requiere:

                grafo_dep[nombre].append(dep)

                # ---------------------------------------------------
                # El comodín "*" no es una dependencia inexistente.
                # Es una declaración especial que será expandida
                # posteriormente en la Parte 18.5.
                # ---------------------------------------------------

                if dep == "*":
                    continue

                if dep not in presentes:

                    faltantes[nombre].append(dep)

                    self.errores_arranque.append(
                        f"{cont.rol}/{nombre}: dependencia inexistente → '{dep}'"
                    )

        # -------------------------------------------------------
        # Parte 18.2 RESOLUCIÓN TOPOLÓGICA
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
        # Parte 18.3 DETECCIÓN DE CICLOS
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
        # Parte 18.4 REGISTRO DE DEPENDENCIAS
        # -------------------------------------------------------

        self._dependencias = {
            "grafo": dict(grafo_dep),
            "faltantes": dict(faltantes),
            "orden_topologico": orden,
            "ciclos": ciclos
        }

        # -------------------------------------------------------
        # Parte 18.5 RESOLUCIÓN DE COMODÍN "*"
        # -------------------------------------------------------
        # El comodín "*" en "requiere" significa que el módulo
        # depende de TODOS los módulos disponibles.
        #
        # No representa un módulo llamado "*".
        # Se expande contra el conjunto real de módulos registrados.
        #
        # El propio módulo se excluye de la expansión para evitar
        # crear una dependencia autorreferente.
        # -------------------------------------------------------

        for modulo, dependencias in list(grafo_dep.items()):

            nuevas_deps: List[str] = []

            for dep in dependencias:

                # ---------------------------------------------------
                # 18.5.1 COMODÍN GLOBAL
                # ---------------------------------------------------

                if dep == "*":

                    for otro in sorted(presentes):

                        if otro != modulo and otro not in nuevas_deps:
                            nuevas_deps.append(otro)

                # ---------------------------------------------------
                # 18.5.2 DEPENDENCIA EXPLÍCITA
                # ---------------------------------------------------

                else:

                    if dep not in nuevas_deps:
                        nuevas_deps.append(dep)

            # -------------------------------------------------------
            # 18.5.3 MATERIALIZAR DEPENDENCIAS EXPANDIDAS
            # -------------------------------------------------------

            grafo_dep[modulo] = nuevas_deps

        # -------------------------------------------------------
        # Parte 18.6 RECALCULAR DEPENDENCIAS FALTANTES
        # -------------------------------------------------------
        # Después de expandir "*", ninguna dependencia legítima
        # debe conservar el literal "*".
        #
        # Solo se reportan como inexistentes las dependencias
        # reales que no existen en el registro.
        # -------------------------------------------------------

        faltantes.clear()

        for nombre, dependencias in grafo_dep.items():

            for dep in dependencias:

                if dep not in presentes:

                    faltantes.setdefault(nombre, []).append(dep)

                    # "*" ya fue expandido.
                    if dep != "*":

                        contenedor = self.registro.contenedores.get(nombre)

                        rol = (
                            contenedor.rol
                            if contenedor is not None
                            else nombre
                        )

                        self.errores_arranque.append(
                            f"{rol}/{nombre}: "
                            f"dependencia inexistente → '{dep}'"
                        )

        # -------------------------------------------------------
        # Parte 18.7 GUARDAR RESULTADO DE RESOLUCIÓN
        # -------------------------------------------------------
        # El grafo almacenado ya contiene las dependencias reales.
        # Un módulo con ["*"] aparecerá conectado con todos los
        # demás módulos registrados, excepto consigo mismo.
        # -------------------------------------------------------

        self._dependencias = {
            "grafo": dict(grafo_dep),
            "faltantes": dict(faltantes),
            "orden_topologico": orden,
            "ciclos": ciclos,
              "ciclos": ciclos,
        }
    # ===========================================================
    # Parte 19 GRAFO
    # ===========================================================

    def _construir_grafo(self) -> None:

        nodos: List[Dict[str, Any]] = []
        aristas: List[Dict[str, Any]] = []

        # -------------------------------------------------------
        # Parte 19.1 NODOS DE MÓDULOS
        # -------------------------------------------------------

        for nombre, cont in self.registro.contenedores.items():

            nodos.append({
                "id": cont.id or nombre,
                "nombre": nombre,
                "rol": cont.rol,
                "tipo": "modulo"
            })

            # ---------------------------------------------------
            # Parte 19.2 ARISTAS DE DEPENDENCIAS
            # ---------------------------------------------------

            for dep in cont.requiere:

                aristas.append({
                    "from": nombre,
                    "to": dep,
                    "tipo": "requiere"
                })

            # ---------------------------------------------------
            # Parte 19.3 NODOS Y ARISTAS DE CAPACIDADES
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
        # Parte 19.4 CONSOLIDACIÓN DEL GRAFO
        # -------------------------------------------------------

        self._grafo = {
            "nodos": nodos,
            "aristas": aristas
        }

    # ===========================================================
    # Parte 20 ENTREGA DE COMENTARIOS AL MÓDULO CONTEXTO
    # ===========================================================

    def _extraer_y_entregar_comentarios(self) -> Dict[str, Any]:
        """Extrae comentarios de todos los módulos y los entrega a 'contexto'."""
        paquetes: Dict[str, Any] = {}

        # -------------------------------------------------------
        # Parte 1 — Recorrido de módulos
        # -------------------------------------------------------
        for path_dir in self._modulos_descubiertos:
            nombre_modulo = path_dir.name
            archivos_paquete: Dict[str, Any] = {}

            # ---------------------------------------------------
            # Parte 2 — Recorrido de archivos .py
            # ---------------------------------------------------
            for archivo in sorted(p for p in path_dir.rglob("*.py") if p.is_file()):
                try:
                    texto = archivo.read_text(encoding="utf-8")
                except Exception:
                    continue

                comentarios: List[str] = []
                lineas = texto.splitlines()
                i = 0
                while i < len(lineas):
                    stripped = lineas[i].strip()
                    if stripped.startswith("#"):
                        comentarios.append(stripped)
                        i += 1
                        continue
                    if stripped.startswith('"""') or stripped.startswith("'''"):
                        comilla = stripped[:3]
                        bloque = [stripped]
                        i += 1
                        if not (stripped.endswith(comilla) and len(stripped) > 3):
                            while i < len(lineas):
                                bloque.append(lineas[i])
                                if lineas[i].strip().endswith(comilla):
                                    i += 1
                                    break
                                i += 1
                        comentarios.append("\n".join(bloque))
                        continue
                    i += 1

                archivos_paquete[str(archivo.relative_to(path_dir))] = {
                    "ruta": str(archivo),
                    "total_comentarios": len(comentarios),
                    "comentarios": comentarios
                }

            # ---------------------------------------------------
            # Parte 3 — Empaquetado del módulo
            # ---------------------------------------------------
            paquetes[nombre_modulo] = {
                "modulo": nombre_modulo,
                "ruta": str(path_dir),
                "total_archivos": len(archivos_paquete),
                "archivos": archivos_paquete
            }

        # -------------------------------------------------------
        # Parte 4 — Entrega al módulo contexto
        # -------------------------------------------------------
        if not paquetes:
            return {"estado": "SIN_COMENTARIOS", "total_modulos": 0}

        resultado = self.ejecutar_capacidad("contexto", "recibir_comentarios", paquetes)
        return {
            "estado": "ENTREGADO",
            "total_modulos": len(paquetes),
            "resultado_contexto": resultado
        }
        
    # ===========================================================
    # Parte 21 CENSO
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
    # Parte 22 TRAZAS DE EJECUCIÓN
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
    # 23 MAPA DE RUTA DE EJECUCIÓN
    # ===========================================================

    def obtener_mapa_ruta(self) -> Tuple[Dict[str, Any], ...]:

        return tuple(
            dict(ruta)
            for ruta in self._mapa_ruta
        )

    # ===========================================================
    # Parte 24 RESOLUCIÓN DE CONTENEDOR
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
    # Parte 25 VALIDACIÓN DE ENTRADA DE CAPACIDAD
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
    # Parte 26 EJECUCIÓN CONTRACTUAL
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
    # Parte 27 ATAJOS DE CAPACIDADES
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
    # Parte 28 INVOCADOR
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
    # Parte 29 — AGENCIA MATEMÁTICA INTERNA + EVALUAR_UNIVERSAL
    # ===========================================================
    #
    # Adaptación de OmegaEngine (compute_coherence / apply_vpsi_truth)
    # al modelo contractual VPSI.
    #
    # Reglas:
    #   - Capas → Self (SF)
    #   - Cálculo → Formulas (FO)
    #   - Engine no escribe ALPHA, BETA ni Tru
    #   - evaluar_universal se ejerce en TODOS los módulos que la declaren
    #
    # ===========================================================

    def _exigir_operativo(self) -> None:
        if self.estado != ESTADO_OPERATIVO:
            raise AgenciaMatematicaError(
                "Engine no operativo (estado={0})".format(self.estado)
            )

    def _exigir_contenedor(self, clave: str, etiqueta: str) -> Contenedor:
        cont = self.registro.primero(clave)
        if cont is None:
            raise AgenciaMatematicaError(
                "{0} ausente en el registro".format(etiqueta)
            )
        return cont

    def _exigir_capacidad(self, cont: Contenedor, nombre: str) -> None:
        if not callable(cont.fn(nombre)):
            raise FormulaNoDisponibleError(
                "{0} no declara capacidad callable '{1}'".format(
                    cont.nombre, nombre
                )
            )

    def _resultado_exito(self, salida: Dict[str, Any], contexto: str) -> Any:
        if not isinstance(salida, dict):
            raise AgenciaMatematicaError(
                "{0}: salida no es dict".format(contexto)
            )
        if salida.get("estado") != "EXITO":
            raise AgenciaMatematicaError(
                "{0}: {1}".format(
                    contexto,
                    salida.get("error") or "ejecución no exitosa",
                )
            )
        return salida.get("resultado")

    # -----------------------------------------------------------
    # CAPAS (Self)
    # -----------------------------------------------------------

    def obtener_capas_self(self) -> Any:
        """
        Capas desde SF.
        Equivalente a layers_data del OmegaEngine original.
        """
        self._exigir_operativo()
        sf = self._exigir_contenedor("SF", "Self (SF)")

        if callable(sf.fn("capas")):
            capacidad = "capas"
        elif callable(sf.fn("estado_self")):
            capacidad = "estado_self"
        else:
            raise FormulaNoDisponibleError(
                "SF no declara 'capas' ni 'estado_self'"
            )

        salida = self.ejecutar_capacidad("SF", capacidad)
        capas = self._resultado_exito(salida, "SF.{0}".format(capacidad))
        if capas is None:
            raise CapasInvalidasError("SF devolvió capas vacías")
        return capas

    # -----------------------------------------------------------
    # COHERENCIA (FO)
    # -----------------------------------------------------------

    def calcular_coherencia(
        self,
        capas: Optional[Any] = None,
        externos: Optional[Dict[str, Any]] = None,
        meta: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Equivalente contractual de OmegaEngine.compute_coherence.
        Capas → SF | Cálculo → FO.evaluar_coherencia
        """
        self._exigir_operativo()
        fo = self._exigir_contenedor("FO", "Formulas (FO)")
        self._exigir_capacidad(fo, "evaluar_coherencia")

        if capas is None:
            capas = self.obtener_capas_self()

        salida = self.ejecutar_capacidad(
            "FO",
            "evaluar_coherencia",
            {
                "capas": capas,
                "externos": dict(externos or {}),
                "meta": dict(meta or {}),
            },
        )
        resultado = self._resultado_exito(salida, "FO.evaluar_coherencia")

        return {
            "estado": "EXITO",
            "operacion": "calcular_coherencia",
            "modulo": fo.nombre,
            "capacidad": "evaluar_coherencia",
            "capas": capas,
            "resultado": resultado,
        }

    # -----------------------------------------------------------
    # VERDAD (FO)
    # -----------------------------------------------------------

    def aplicar_verdad(
        self,
        payload: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Equivalente contractual de OmegaEngine.apply_vpsi_truth.
        Engine no escribe la fórmula: FO.tru_total o propósito.
        """
        self._exigir_operativo()
        fo = self._exigir_contenedor("FO", "Formulas (FO)")
        data = dict(payload or {})

        if callable(fo.fn("tru_total")):
            salida = self.ejecutar_capacidad("FO", "tru_total", data)
            resultado = self._resultado_exito(salida, "FO.tru_total")
            return {
                "estado": "EXITO",
                "operacion": "aplicar_verdad",
                "modulo": fo.nombre,
                "capacidad": "tru_total",
                "resultado": resultado,
            }

        resultado = self.ejecutar_proposito(data)
        return {
            "estado": "EXITO",
            "operacion": "aplicar_verdad",
            "modulo": "PROPOSITO",
            "capacidad": self.clave_proposito,
            "resultado": resultado,
        }

    # -----------------------------------------------------------
    # CICLO OMEGA
    # -----------------------------------------------------------

    def ciclo_omega(
        self,
        capas: Optional[Any] = None,
        externos: Optional[Dict[str, Any]] = None,
        meta: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Pipeline activo:
          SF (capas) → FO (coherencia) → FO (verdad)
        """
        self._exigir_operativo()

        if capas is None:
            capas = self.obtener_capas_self()

        bloque_coh = self.calcular_coherencia(
            capas=capas,
            externos=externos,
            meta=meta,
        )
        if bloque_coh.get("estado") != "EXITO":
            return bloque_coh

        res_coh = bloque_coh.get("resultado")

        bloque_truth = self.aplicar_verdad(
            {
                "coherencia": res_coh,
                "capas": capas,
                "externos": dict(externos or {}),
                "meta": dict(meta or {}),
            }
        )

        return {
            "estado": "EXITO",
            "operacion": "ciclo_omega",
            "capas": capas,
            "coherencia": res_coh,
            "verdad": bloque_truth.get("resultado"),
            "detalle_coherencia": {
                "modulo": bloque_coh.get("modulo"),
                "capacidad": bloque_coh.get("capacidad"),
            },
            "detalle_verdad": {
                "modulo": bloque_truth.get("modulo"),
                "capacidad": bloque_truth.get("capacidad"),
            },
        }

    # -----------------------------------------------------------
    # EVALUAR_UNIVERSAL — TODOS LOS MÓDULOS
    # -----------------------------------------------------------


    # =========================================================================
    # FÓRMULA 1 — COHERENCIA DEL CARRIL (C_Ω)
    # =========================================================================
   
    def calcular_coherencia(
        self,
        capas: Optional[Any] = None,
        externos: Optional[Dict[str, Any]] = None,
        meta: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Equivalente contractual de OmegaEngine.compute_coherence.
        Capas → SF | Cálculo → FO.evaluar_coherencia (Fórmula 1 - C_Ω)
        
        Entrada: Activaciones L0..L6 desde el módulo Self (SF).
        Salida: Escalar c_omega.
        """
        self._exigir_operativo()
        fo = self._exigir_contenedor("FO", "Formulas (FO)")
        self._exigir_capacidad(fo, "evaluar_coherencia")

        if capas is None:
            capas = self.obtener_capas_self()

        salida = self.ejecutar_capacidad(
            "FO",
            "evaluar_coherencia",
            {
                "capas": capas,
                "externos": dict(externos or {}),
                "meta": dict(meta or {}),
            },
        )
        c_omega = self._resultado_exito(salida, "FO.evaluar_coherencia")

        return {
            "estado": "EXITO",
            "formula": "FORMULA_1_C_OMEGA",
            "operacion": "calcular_coherencia",
            "modulo": fo.nombre,
            "capacidad": "evaluar_coherencia",
            "capas": capas,
            "c_omega": c_omega,
        }

    # =========================================================================
    # FÓRMULA 2 — EVALUACIÓN DE VERDAD (TRU)
    # =========================================================================
    def calcular_verdad(
        self,
        C: Any,
        L: Any,
        K: Any,
        alpha: Optional[Any] = None,
        beta: Optional[Any] = None,
        externos: Optional[Dict[str, Any]] = None,
        meta: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Capacidad contractual para la Fórmula 2 — Verdad (Tru).
        Factores de Dominio (CA/Conteos) → FO.evaluar_verdad
        
        Entrada: C, L, K (Fraction / factores de dominio).
        Salida: Tru_Ri y Tru_total.
        
        Aislamiento: No consume ni conoce las capas L0..L6 del módulo SF.
        """
        self._exigir_operativo()
        fo = self._exigir_contenedor("FO", "Formulas (FO)")
        self._exigir_capacidad(fo, "evaluar_verdad")

        salida = self.ejecutar_capacidad(
            "FO",
            "evaluar_verdad",
            {
                "C": C,
                "L": L,
                "K": K,
                "alpha": alpha,
                "beta": beta,
                "externos": dict(externos or {}),
                "meta": dict(meta or {}),
            },
        )
        resultado_tru = self._resultado_exito(salida, "FO.evaluar_verdad")

        return {
            "estado": "EXITO",
            "formula": "FORMULA_2_TRU",
            "operacion": "calcular_verdad",
            "modulo": fo.nombre,
            "capacidad": "evaluar_verdad",
            "factores": {"C": C, "L": L, "K": K},
            "resultado": resultado_tru,
        }


    def ciclo_omega_universal(
        self,
        capas: Optional[Any] = None,
        externos: Optional[Dict[str, Any]] = None,
        meta: Optional[Dict[str, Any]] = None,
        peticion_universal: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Ciclo completo:
          1. ciclo_omega (SF + FO)
          2. evaluar_universal en todos los módulos que la declaran
        """
        omega = self.ciclo_omega(
            capas=capas,
            externos=externos,
            meta=meta,
        )
        universal = self.evaluar_universal_todos(
            peticion=peticion_universal,
        )

        return {
            "estado": (
                "EXITO"
                if omega.get("estado") == "EXITO"
                and universal.get("estado") in ("EXITO", "PARCIAL")
                else "ERROR"
            ),
            "operacion": "ciclo_omega_universal",
            "omega": omega,
            "evaluar_universal": universal,
        }
 
    # ===========================================================
    # Parte 29 CONSOLIDACIÓN
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
    # Parte 30 PAQUETE OMEGA
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
    # Parte 31 ESTADO GLOBAL
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
    # Parte 32 CENTINELA
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
# Parte 33 — EJECUCIÓN CONTRACTUAL COMPLETA
# ===========================================================

def ejecutar_contrato(
    self,
    modulo_o_rol: Any,
    capacidad: Optional[str] = None,
    *args: Any,
    **kwargs: Any
) -> Any:
    """
    Ejecuta una capacidad declarada por el contrato del módulo.

    Si se especifica 'capacidad', ejecuta únicamente esa capacidad.

    Si no se especifica 'capacidad', ejecuta todas las capacidades
    ejecutables declaradas por el contrato.

    La ejecución material delega en ejecutar_capacidad(), que constituye
    el núcleo único de invocación del Engine.
    """

    cont, error = self._resolver_contenedor(modulo_o_rol)

    if cont is None:
        raise KeyError(error)

    # -------------------------------------------------------
    # EJECUCIÓN DE UNA CAPACIDAD ESPECÍFICA
    # -------------------------------------------------------

    if capacidad is not None:

        if capacidad not in cont.capacidades:
            raise AttributeError(
                f"El módulo '{cont.nombre}' no declara "
                f"la capacidad '{capacidad}'."
            )

        return self.ejecutar_capacidad(
            cont,
            capacidad,
            *args,
            **kwargs
        )

    # -------------------------------------------------------
    # EJECUCIÓN DE TODAS LAS CAPACIDADES DECLARADAS
    # -------------------------------------------------------

    resultados: Dict[str, Any] = {}

    for nombre_capacidad in cont.capacidades.keys():

        resultados[nombre_capacidad] = self.ejecutar_capacidad(
            cont,
            nombre_capacidad,
            *args,
            **kwargs
        )

    return {
        "estado": "EXITO",
        "modulo": cont.nombre,
        "rol": cont.rol,
        "id": cont.id,
        "capacidades_ejecutadas": list(resultados.keys()),
        "resultados": resultados,
    }

# ===========================================================
# Parte 34 EXPORTACIONES
# ===========================================================

__all__ = [
    # Núcleo
    "Engine",
    "Contenedor",
    "RegistroModulos",
    # Errores
    "ArranqueError",
    "ContratoError",
    "AgenciaMatematicaError",
    "CapasInvalidasError",
    "FormulaNoDisponibleError",
    "PurposeAlignmentError",
    "StructuralIntegrityError",
    "CircularityDetectedError",
    # Validación
    "AntiHackValidation",
    # Constantes de motor
    "VERSION_ENGINE",
    "ESQUEMA_CONTRATO_REQUERIDO",
    "VERSION_CONTRATO_REQUERIDA",
    "API_ENGINE_ACTUAL",
    "ALPHA_VPSI",
    "BETA_VPSI",
    "EPSILON",
    # Estados / roles
    "ESTADO_NO_INICIADO",
    "ESTADO_OPERATIVO",
    "ESTADO_DEGRADADO",
    "ESTADO_RECHAZADO",
    "ROLES",
    "OBLIGATORIOS",
]


# ===========================================================
# FIN DEL MÓDULO ENGINE
# ===========================================================
