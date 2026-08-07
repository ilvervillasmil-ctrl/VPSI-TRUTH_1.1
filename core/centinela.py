# ===============================================================
# VPSI-TRUTH — core/centinela.py
# ===============================================================
#
# Centinela — intérprete genérico del expediente de CACHE.
#
# NO contiene conocimiento de dominio.
# NO conoce variables (C, L, K, Tru, …).
# NO importa FO, CT, AX, MC ni ningún módulo.
# NO hardcodea fórmulas, cadenas ni listas de claves de cálculo.
#
# Autoridad única: el expediente registrado en CACHE.
#
# Algoritmo:
#   1. Recibe el paquete (salida determinista de Engine).
#   2. Lee TODO el expediente del ciclo.
#   3. Descubre módulos, capacidades, contratos, versiones,
#      dependencias, secuencia, variables y resultados
#      únicamente desde el expediente.
#   4. Verifica coherencia, autorizaciones, dependencias,
#      orden causal, versiones e integridad.
#   5. Si hay invocador, reproduce solo las capacidades
#      que el expediente registra como ejecutadas.
#   6. Compara cada transición.
#   7. Emite veredicto y lo registra en CACHE.
#
# Si mañana aparecen módulos o variables nuevas, Centinela
# no se modifica: los descubre en el expediente.
#
# ===============================================================

from __future__ import annotations

import copy
import hashlib
import json
import time
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from fractions import Fraction
from typing import Any, Dict, List, Optional, Protocol, Set, Tuple

from core.paquete_contrato import (
    PKG_CICLO_ID,
    PKG_CONTEXTO,
    PKG_ESTADO,
    PKG_ESTADO_OK,
    PKG_ESTADO_PARCIAL,
    PKG_ESTADO_UNDEFINED,
    PKG_ESTADOS_VALIDOS,
    PKG_O_CONTEXT,
)
from modules.cache.cs import (
    CS_CAMPO_CICLO_ID,
    CS_CAMPO_ESTADO,
    CS_CAMPO_MOTIVOS,
    CS_CAMPO_PAQUETE_REF,
    CS_CAMPO_VEREDICTO,
    CS_CATEGORIA_VEREDICTO,
    CS_ESTADO_APROBADO,
    CS_ESTADO_PARCIAL,
    CS_ESTADO_RETENIDO,
    CS_ESTADOS,
    CS_TIPO_VEREDICTO,
    MODULO as CS_MODULO,
    VERSION_EVENTOS as CS_VERSION_EVENTOS,
)
from modules.cache.en import (
    EN_CAMPO_PAQUETE,
    EN_CATEGORIA_SALIDA,
    EN_TIPO_CICLO_FIN,
    MODULO as EN_MODULO,
)


# ===============================================================
# IDENTIDAD
# ===============================================================

CS_ID = "CS"
CS_NOMBRE = "centinela"
CS_ROL = "CS"
CS_VERSION = "4.0"
CS_ESQUEMA = "VPSI-CONTRACT-1.0"
CS_VERSION_CONTRATO = "1.0"

CS_FUNCION = (
    "Intérprete genérico del expediente de CACHE. "
    "Certifica que la salida de Engine está respaldada por "
    "toda la evidencia registrada. Sin conocimiento de dominio."
)

CS_NO_HACE = (
    "No orquesta el ciclo",
    "No modifica factores ni contexto",
    "No inventa evidencia",
    "No reconstruye evidencia inexistente",
    "No hardcodea variables, fórmulas ni módulos de dominio",
    "No importa FO, CT, AX, MC ni ningún módulo de cálculo",
)

CS_AUTORIDAD = (
    "Consultar el expediente completo del ciclo en CACHE",
    "Descubrir módulos, contratos, capacidades y variables desde el expediente",
    "Verificar coherencia, autorizaciones, dependencias, secuencia y versiones",
    "Reproducir capacidades autorizadas vía invocador dinámico",
    "Emitir veredicto APROBADO | RETENIDO | PARCIAL",
    "Registrar el veredicto en CACHE",
)

# Solo forma estructural del paquete (no variables de dominio).
_CLAVES_FORMA_PAQUETE = (
    PKG_CICLO_ID,
    PKG_ESTADO,
    PKG_O_CONTEXT,
    PKG_CONTEXTO,
)


# ===============================================================
# PROTOCOLOS
# ===============================================================

class CacheEvidencia(Protocol):
    def guardar(self, registro: Dict[str, Any]) -> None: ...
    def leer_ciclo(self, ciclo_id: str) -> List[Dict[str, Any]]: ...


class InvocadorCapacidades(Protocol):
    def invocar(
        self,
        modulo: str,
        capacidad: str,
        *args: Any,
        **kwargs: Any,
    ) -> Any: ...


# ===============================================================
# ADAPTADORES DE CACHE
# ===============================================================

class _CacheMemoriaLocal:
    def __init__(self) -> None:
        self._regs: List[Dict[str, Any]] = []

    def guardar(self, registro: Dict[str, Any]) -> None:
        self._regs.append(dict(registro))

    def leer_ciclo(self, ciclo_id: str) -> List[Dict[str, Any]]:
        return [
            dict(r)
            for r in self._regs
            if str(r.get(PKG_CICLO_ID)) == str(ciclo_id)
        ]


class _CachePublicoAdapter:
    def guardar(self, registro: Dict[str, Any]) -> None:
        from modules.cache import depositar

        tipo = str(registro.get("tipo") or CS_TIPO_VEREDICTO)
        omitir = {
            "tipo",
            PKG_CICLO_ID,
            "origen",
            "modulo",
            "categoria",
            "estado",
            "capacidad",
        }
        payload = {k: v for k, v in registro.items() if k not in omitir}
        depositar(
            tipo,
            payload,
            ciclo_id=registro.get(PKG_CICLO_ID),
            origen=registro.get("origen"),
        )

    def leer_ciclo(self, ciclo_id: str) -> List[Dict[str, Any]]:
        try:
            from modules.cache import leer_por_ciclo
            return list(leer_por_ciclo(str(ciclo_id)))
        except Exception:
            pass
        try:
            from modules.cache import secuencia
            return list(secuencia(str(ciclo_id)))
        except Exception:
            pass
        from modules.cache import leer
        return list(leer(ciclo_id=str(ciclo_id)))


def _resolver_cache(
    cache: Optional[CacheEvidencia] = None,
) -> CacheEvidencia:
    if cache is not None:
        return cache
    try:
        return _CachePublicoAdapter()
    except Exception:
        return _CacheMemoriaLocal()


# ===============================================================
# ERRORES / VEREDICTO / STATS
# ===============================================================

class CentinelaError(Exception):
    """Error de forma del centinela, no de negocio."""


@dataclass
class Veredicto:
    estado: str
    ciclo_id: str
    motivos: List[str] = field(default_factory=list)
    advertencias: List[str] = field(default_factory=list)
    id_verificacion: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )
    hash_expediente: Optional[str] = None
    meta_verificacion: Dict[str, Any] = field(default_factory=dict)
    valores_paquete: Dict[str, Optional[str]] = field(
        default_factory=dict
    )
    valores_evidencia: Dict[str, Optional[str]] = field(
        default_factory=dict
    )
    contratos: List[Dict[str, Any]] = field(default_factory=list)
    reproducciones: List[Dict[str, Any]] = field(default_factory=list)
    arbol_auditoria: List[Dict[str, Any]] = field(default_factory=list)
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def a_dict(self) -> Dict[str, Any]:
        return asdict(self)


class _Estadisticas:
    def __init__(self) -> None:
        self.verificaciones = 0
        self.aprobadas = 0
        self.retenidas = 0
        self.parciales = 0
        self.advertencias = 0
        self.duraciones_s: List[float] = []
        self.modulos_vistos: set = set()
        self.capacidades_vistas: set = set()

    def registrar(
        self,
        estado: str,
        duracion_s: float,
        modulos: List[str],
        capacidades: List[str],
        n_adv: int,
    ) -> None:
        self.verificaciones += 1
        if estado == CS_ESTADO_APROBADO:
            self.aprobadas += 1
        elif estado == CS_ESTADO_RETENIDO:
            self.retenidas += 1
        elif estado == CS_ESTADO_PARCIAL:
            self.parciales += 1
        self.duraciones_s.append(duracion_s)
        self.modulos_vistos.update(modulos)
        self.capacidades_vistas.update(capacidades)
        self.advertencias += n_adv

    def resumen(self) -> Dict[str, Any]:
        n = len(self.duraciones_s)
        avg = sum(self.duraciones_s) / n if n else 0.0
        return {
            "verificaciones": self.verificaciones,
            "aprobadas": self.aprobadas,
            "retenidas": self.retenidas,
            "parciales": self.parciales,
            "advertencias": self.advertencias,
            "tiempo_promedio_s": round(avg, 6),
            "modulos_vistos": sorted(self.modulos_vistos),
            "capacidades_vistas": sorted(self.capacidades_vistas),
        }


_STATS = _Estadisticas()


# ===============================================================
# HELPERS GENÉRICOS
# ===============================================================

def _frac(x: Any) -> Optional[Fraction]:
    if x is None:
        return None
    if isinstance(x, Fraction):
        return x
    if isinstance(x, bool):
        return None
    if isinstance(x, float):
        raise CentinelaError("float rechazado en centinela")
    if isinstance(x, int):
        return Fraction(x)
    if isinstance(x, str):
        s = x.strip()
        if s.upper() in ("NONE", "UNDEFINED", ""):
            return None
        try:
            return Fraction(s)
        except Exception:
            return None
    return None


def _str_frac(x: Optional[Fraction]) -> Optional[str]:
    return str(x) if x is not None else None


def _paquete_minimo_ok(paquete: Dict[str, Any]) -> List[str]:
    faltas: List[str] = []
    if not isinstance(paquete, dict):
        return ["paquete no es dict"]
    if not paquete.get(PKG_CICLO_ID):
        faltas.append("falta ciclo_id")
    if PKG_O_CONTEXT not in paquete and PKG_CONTEXTO not in paquete:
        faltas.append("falta O_context/contexto en paquete")
    estado = str(paquete.get(PKG_ESTADO) or "").upper()
    if estado not in PKG_ESTADOS_VALIDOS:
        faltas.append("estado desconocido: {0}".format(estado))
    return faltas


def _es_clave_forma(clave: str) -> bool:
    return clave in _CLAVES_FORMA_PAQUETE or clave in (
        "tipo",
        "origen",
        "modulo",
        "capacidad",
        "categoria",
        "seq",
        "timestamp",
        "payload",
        "ciclo_id",
        "estado",
        "error",
        "errores",
        "advertencias",
        "notas",
        "mensaje",
        "mensajes",
    )


def _recolectar_valores_dinamicos(
    obj: Any,
    destino: Dict[str, List[Fraction]],
) -> None:
    """
    Descubre cualquier valor convertible a Fraction.
    No usa lista fija de variables de dominio.
    """
    if isinstance(obj, dict):
        for k, v in obj.items():
            if _es_clave_forma(str(k)):
                _recolectar_valores_dinamicos(v, destino)
                continue
            fr = None
            try:
                fr = _frac(v)
            except CentinelaError:
                fr = None
            if fr is not None:
                destino.setdefault(str(k), []).append(fr)
            else:
                _recolectar_valores_dinamicos(v, destino)
    elif isinstance(obj, list):
        for item in obj:
            _recolectar_valores_dinamicos(item, destino)


def _valores_desde(obj: Any) -> Dict[str, List[Fraction]]:
    destino: Dict[str, List[Fraction]] = {}
    _recolectar_valores_dinamicos(obj, destino)
    return destino


def _sin_contradiccion(valores: List[Fraction]) -> bool:
    if len(valores) <= 1:
        return True
    base = valores[0]
    return all(v == base for v in valores)


def _ultimo(valores: List[Fraction]) -> Optional[Fraction]:
    return valores[-1] if valores else None


def _descubrir_campo(
    eventos: List[Dict[str, Any]], campo: str
) -> List[str]:
    hallados: set = set()
    for ev in eventos:
        v = ev.get(campo)
        if v is not None and str(v).strip():
            hallados.add(str(v))
        p = ev.get("payload")
        if isinstance(p, dict):
            v2 = p.get(campo)
            if v2 is not None and str(v2).strip():
                hallados.add(str(v2))
    return sorted(hallados)


def _hash_obj(obj: Any) -> str:
    try:
        raw = json.dumps(
            obj, sort_keys=True, default=str, ensure_ascii=True
        )
    except Exception:
        raw = str(obj)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _payload(ev: Dict[str, Any]) -> Dict[str, Any]:
    p = ev.get("payload")
    return p if isinstance(p, dict) else {}


def _extraer_contratos(
    eventos: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Descubre contratos depositados en el expediente.
    Acepta cualquier estructura que declare id/nombre + capacidades
    o campos típicos de CONTENEDOR. No asume módulos concretos.
    """
    contratos: List[Dict[str, Any]] = []
    vistos: Set[str] = set()

    for ev in eventos:
        candidatos = [ev, _payload(ev)]
        for c in candidatos:
            if not isinstance(c, dict):
                continue
            # contrato explícito
            cont = c.get("contrato") or c.get("CONTENEDOR") or c.get("contenedor")
            if isinstance(cont, dict):
                cid = str(
                    cont.get("id")
                    or cont.get("nombre")
                    or cont.get("rol")
                    or ""
                )
                if cid and cid not in vistos:
                    vistos.add(cid)
                    contratos.append(dict(cont))
                continue
            # evento que parece un contrato (tiene capacidades + nombre/rol)
            if (
                "capacidades" in c
                and ("nombre" in c or "rol" in c or "id" in c)
            ):
                cid = str(c.get("id") or c.get("nombre") or c.get("rol") or "")
                if cid and cid not in vistos:
                    vistos.add(cid)
                    contratos.append(dict(c))
    return contratos


def _capacidades_de_contrato(contrato: Dict[str, Any]) -> Set[str]:
    caps = contrato.get("capacidades")
    if isinstance(caps, dict):
        return {str(k) for k in caps.keys()}
    if isinstance(caps, (list, tuple, set)):
        return {str(x) for x in caps}
    return set()


def _requiere_de_contrato(contrato: Dict[str, Any]) -> List[str]:
    req = contrato.get("requiere")
    if isinstance(req, list):
        return [str(x) for x in req]
    return []


def _autoriza_ejecutar(contrato: Dict[str, Any]) -> Optional[bool]:
    auth = contrato.get("autoriza_engine")
    if isinstance(auth, dict) and "ejecutar" in auth:
        return bool(auth.get("ejecutar"))
    return None


def _ejecuciones_registradas(
    eventos: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for ev in eventos:
        p = _payload(ev)
        modulo = ev.get("modulo") or p.get("modulo")
        capacidad = ev.get("capacidad") or p.get("capacidad")
        if not modulo and not capacidad:
            continue
        out.append({
            "seq": ev.get("seq"),
            "timestamp": ev.get("timestamp"),
            "tipo": ev.get("tipo"),
            "modulo": str(modulo) if modulo is not None else None,
            "capacidad": str(capacidad) if capacidad is not None else None,
            "estado": ev.get("estado") or p.get("estado"),
            "payload": p,
            "resultado": p.get("resultado"),
            "entrada": p.get("entrada"),
            "contrato_ref": p.get("contrato") or p.get("version_contrato"),
            "version_modulo": p.get("version_modulo") or p.get("version"),
            "esquema": p.get("esquema"),
            "requiere": p.get("requiere"),
        })
    # orden causal por seq si existe
    out.sort(
        key=lambda e: (
            e["seq"] is None,
            e["seq"] if isinstance(e["seq"], int) else 0,
        )
    )
    return out


def _verificar_secuencia(
    ejecuciones: List[Dict[str, Any]],
) -> List[str]:
    motivos: List[str] = []
    prev_seq: Optional[int] = None
    for ej in ejecuciones:
        seq = ej.get("seq")
        if not isinstance(seq, int):
            continue
        if prev_seq is not None and seq < prev_seq:
            motivos.append(
                "orden causal inválido: seq {0} después de {1}".format(
                    seq, prev_seq
                )
            )
        prev_seq = seq
    return motivos


def _verificar_dependencias(
    ejecuciones: List[Dict[str, Any]],
    contratos: List[Dict[str, Any]],
    modulos_presentes: Set[str],
) -> List[str]:
    motivos: List[str] = []
    # dependencias declaradas en contratos
    for cont in contratos:
        nombre = str(
            cont.get("nombre") or cont.get("id") or cont.get("rol") or ""
        )
        for dep in _requiere_de_contrato(cont):
            if dep not in modulos_presentes and dep != nombre:
                # la dependencia debe aparecer como módulo en el expediente
                if dep not in modulos_presentes:
                    motivos.append(
                        "dependencia no satisfecha: {0} requiere {1}".format(
                            nombre or "?", dep
                        )
                    )
    # dependencias registradas en ejecuciones
    for ej in ejecuciones:
        req = ej.get("requiere")
        if isinstance(req, list):
            for dep in req:
                if str(dep) not in modulos_presentes:
                    motivos.append(
                        "dependencia de ejecución no satisfecha: "
                        "{0}.{1} requiere {2}".format(
                            ej.get("modulo"),
                            ej.get("capacidad"),
                            dep,
                        )
                    )
    return motivos


def _verificar_autorizaciones(
    ejecuciones: List[Dict[str, Any]],
    contratos: List[Dict[str, Any]],
) -> List[str]:
    motivos: List[str] = []
    if not contratos:
        return motivos

    # índice por nombre / id / rol
    indice: Dict[str, Dict[str, Any]] = {}
    for cont in contratos:
        for key in ("nombre", "id", "rol"):
            val = cont.get(key)
            if val is not None:
                indice[str(val)] = cont

    for ej in ejecuciones:
        mod = ej.get("modulo")
        cap = ej.get("capacidad")
        if not mod or not cap:
            continue
        cont = indice.get(str(mod))
        if cont is None:
            # contrato no depositado: advertencia, no necesariamente retención
            continue
        caps = _capacidades_de_contrato(cont)
        if caps and str(cap) not in caps:
            motivos.append(
                "capacidad no declarada en contrato: {0}.{1}".format(
                    mod, cap
                )
            )
        auth = _autoriza_ejecutar(cont)
        if auth is False:
            motivos.append(
                "capacidad ejecutada sin autorización: {0}.{1}".format(
                    mod, cap
                )
            )
    return motivos


def _verificar_versiones(
    eventos: List[Dict[str, Any]],
    contratos: List[Dict[str, Any]],
) -> Tuple[List[str], List[str]]:
    motivos: List[str] = []
    advertencias: List[str] = []
    esquemas: Set[str] = set()
    versiones_contrato: Set[str] = set()

    for cont in contratos:
        if cont.get("esquema"):
            esquemas.add(str(cont["esquema"]))
        if cont.get("version_contrato"):
            versiones_contrato.add(str(cont["version_contrato"]))
        elif cont.get("version"):
            versiones_contrato.add(str(cont["version"]))

    for ev in eventos:
        p = _payload(ev)
        if p.get("esquema"):
            esquemas.add(str(p["esquema"]))
        if p.get("version_contrato"):
            versiones_contrato.add(str(p["version_contrato"]))

    if len(esquemas) > 1:
        motivos.append(
            "esquemas inconsistentes en el ciclo: {0}".format(
                sorted(esquemas)
            )
        )
    if len(versiones_contrato) > 1:
        advertencias.append(
            "versiones de contrato mixtas en el ciclo: {0}".format(
                sorted(versiones_contrato)
            )
        )
    return motivos, advertencias


def _arbol_desde_ejecuciones(
    ejecuciones: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Árbol lineal de auditoría por orden causal (seq)."""
    arbol: List[Dict[str, Any]] = []
    for ej in ejecuciones:
        arbol.append({
            "seq": ej.get("seq"),
            "modulo": ej.get("modulo"),
            "capacidad": ej.get("capacidad"),
            "estado": ej.get("estado"),
            "tipo": ej.get("tipo"),
        })
    return arbol


def _igual_valor(a: Any, b: Any) -> bool:
    if a is None and b is None:
        return True
    try:
        fa = _frac(a)
        fb = _frac(b)
        if fa is not None and fb is not None:
            return fa == fb
    except CentinelaError:
        pass
    return a == b


# ===============================================================
# NÚCLEO
# ===============================================================

class Centinela:
    def __init__(
        self,
        cache: Optional[CacheEvidencia] = None,
        invocador: Optional[InvocadorCapacidades] = None,
    ) -> None:
        self._cache: CacheEvidencia = _resolver_cache(cache)
        self._invocador: Optional[InvocadorCapacidades] = invocador
        self._ultimo_veredicto: Optional[Veredicto] = None

    def entrar_modulo(self, *args: Any, **kwargs: Any) -> None:
        raise CentinelaError(
            "Centinela no tiene agencia para entrar en módulos"
        )

    def modificar_factores(self, *args: Any, **kwargs: Any) -> None:
        raise CentinelaError(
            "Centinela no modifica factores ni contexto"
        )

    def orquestar(self, *args: Any, **kwargs: Any) -> None:
        raise CentinelaError(
            "Centinela no orquesta; solo certifica la salida"
        )

    def verificar(
        self,
        paquete: Dict[str, Any],
        *,
        depositar_salida: bool = True,
    ) -> Veredicto:
        t0 = time.perf_counter()
        ts_inicio = datetime.now(timezone.utc).isoformat()

        if not isinstance(paquete, dict):
            raise CentinelaError("paquete debe ser dict")

        p = copy.deepcopy(paquete)
        ciclo_id = str(p.get(PKG_CICLO_ID) or "")
        motivos: List[str] = []
        advertencias: List[str] = []
        id_ver = str(uuid.uuid4())
        reproducciones: List[Dict[str, Any]] = []

        # ----------------------------------------------------------
        # 0) registrar salida presentada
        # ----------------------------------------------------------
        if depositar_salida and ciclo_id:
            try:
                self._cache.guardar({
                    "tipo": EN_TIPO_CICLO_FIN,
                    PKG_CICLO_ID: ciclo_id,
                    "origen": EN_MODULO,
                    "modulo": EN_MODULO,
                    "categoria": EN_CATEGORIA_SALIDA,
                    EN_CAMPO_PAQUETE: p,
                })
            except Exception as e:
                advertencias.append(
                    "cache_salida: {0}: {1}".format(
                        type(e).__name__, e
                    )
                )

        # ----------------------------------------------------------
        # 1) forma estructural del paquete (no variables de dominio)
        # ----------------------------------------------------------
        faltas = _paquete_minimo_ok(p)
        if faltas:
            return self._emitir(
                estado=CS_ESTADO_RETENIDO,
                ciclo_id=ciclo_id or "sin_ciclo",
                motivos=[
                    "paquete_incompleto: {0}".format(f) for f in faltas
                ],
                advertencias=advertencias,
                id_verificacion=id_ver,
                t0=t0,
                ts_inicio=ts_inicio,
                paquete=p,
            )

        estado_eng = str(p.get(PKG_ESTADO) or "").upper()

        # ----------------------------------------------------------
        # 2) variables del paquete — descubrimiento dinámico
        # ----------------------------------------------------------
        vals_p_lists = _valores_desde(p)
        valores_p: Dict[str, Optional[Fraction]] = {
            k: _ultimo(v) for k, v in vals_p_lists.items()
        }

        # ----------------------------------------------------------
        # 3) expediente completo
        # ----------------------------------------------------------
        try:
            eventos = self._cache.leer_ciclo(ciclo_id)
        except Exception as e:
            return self._emitir(
                estado=CS_ESTADO_RETENIDO,
                ciclo_id=ciclo_id,
                motivos=motivos + [
                    "cache_lectura: {0}: {1}".format(
                        type(e).__name__, e
                    )
                ],
                advertencias=advertencias,
                id_verificacion=id_ver,
                t0=t0,
                ts_inicio=ts_inicio,
                paquete=p,
                valores_paquete={
                    k: _str_frac(v) for k, v in valores_p.items()
                },
            )

        modulos = _descubrir_campo(eventos, "modulo")
        capacidades = _descubrir_campo(eventos, "capacidad")
        tipos = _descubrir_campo(eventos, "tipo")
        categorias = _descubrir_campo(eventos, "categoria")
        hash_exp = _hash_obj(eventos)
        contratos = _extraer_contratos(eventos)
        ejecuciones = _ejecuciones_registradas(eventos)
        arbol = _arbol_desde_ejecuciones(ejecuciones)
        modulos_set: Set[str] = set(modulos)

        meta_exp = {
            "ciclo_id": ciclo_id,
            "total_eventos": len(eventos),
            "modulos": modulos,
            "capacidades": capacidades,
            "tipos": tipos,
            "categorias": categorias,
            "contratos_n": len(contratos),
            "ejecuciones_n": len(ejecuciones),
            "hash_expediente": hash_exp,
        }

        if not eventos:
            motivos.append("expediente vacío en CACHE")
            if estado_eng == PKG_ESTADO_OK:
                return self._emitir(
                    estado=CS_ESTADO_RETENIDO,
                    ciclo_id=ciclo_id,
                    motivos=motivos + [
                        "estado OK sin expediente en CACHE"
                    ],
                    advertencias=advertencias,
                    id_verificacion=id_ver,
                    t0=t0,
                    ts_inicio=ts_inicio,
                    paquete=p,
                    valores_paquete={
                        k: _str_frac(v) for k, v in valores_p.items()
                    },
                    hash_expediente=hash_exp,
                    meta_extra=meta_exp,
                    modulos=modulos,
                    capacidades=capacidades,
                    contratos=contratos,
                    arbol_auditoria=arbol,
                )

        # ----------------------------------------------------------
        # 4) variables de evidencia — descubrimiento dinámico
        # ----------------------------------------------------------
        vals_e_lists = _valores_desde(eventos)
        for clave, lista in vals_e_lists.items():
            if not _sin_contradiccion(lista):
                motivos.append(
                    "evidencia contradictoria en '{0}'".format(clave)
                )
        if any(
            not _sin_contradiccion(lista)
            for lista in vals_e_lists.values()
        ):
            return self._emitir(
                estado=CS_ESTADO_RETENIDO,
                ciclo_id=ciclo_id,
                motivos=motivos,
                advertencias=advertencias,
                id_verificacion=id_ver,
                t0=t0,
                ts_inicio=ts_inicio,
                paquete=p,
                valores_paquete={
                    k: _str_frac(v) for k, v in valores_p.items()
                },
                valores_evidencia={
                    k: _str_frac(_ultimo(v))
                    for k, v in vals_e_lists.items()
                },
                hash_expediente=hash_exp,
                meta_extra=meta_exp,
                modulos=modulos,
                capacidades=capacidades,
                contratos=contratos,
                arbol_auditoria=arbol,
            )

        valores_e: Dict[str, Optional[Fraction]] = {
            k: _ultimo(v) for k, v in vals_e_lists.items()
        }

        # ----------------------------------------------------------
        # 5) paquete ≡ evidencia (intersección dinámica de claves)
        # ----------------------------------------------------------
        comunes = set(valores_p.keys()) & set(valores_e.keys())
        for clave in sorted(comunes):
            vp = valores_p.get(clave)
            ve = valores_e.get(clave)
            if vp is not None and ve is not None and vp != ve:
                motivos.append(
                    "divergencia {0}: paquete={1} evidencia={2}".format(
                        clave, vp, ve
                    )
                )
        if any(
            valores_p.get(k) is not None
            and valores_e.get(k) is not None
            and valores_p.get(k) != valores_e.get(k)
            for k in comunes
        ):
            return self._emitir(
                estado=CS_ESTADO_RETENIDO,
                ciclo_id=ciclo_id,
                motivos=motivos,
                advertencias=advertencias,
                id_verificacion=id_ver,
                t0=t0,
                ts_inicio=ts_inicio,
                paquete=p,
                valores_paquete={
                    k: _str_frac(v) for k, v in valores_p.items()
                },
                valores_evidencia={
                    k: _str_frac(v) for k, v in valores_e.items()
                },
                hash_expediente=hash_exp,
                meta_extra=meta_exp,
                modulos=modulos,
                capacidades=capacidades,
                contratos=contratos,
                arbol_auditoria=arbol,
            )

        # ----------------------------------------------------------
        # 6) orden causal
        # ----------------------------------------------------------
        motivos.extend(_verificar_secuencia(ejecuciones))

        # ----------------------------------------------------------
        # 7) dependencias
        # ----------------------------------------------------------
        motivos.extend(
            _verificar_dependencias(
                ejecuciones, contratos, modulos_set
            )
        )

        # ----------------------------------------------------------
        # 8) autorizaciones (si el expediente trae contratos)
        # ----------------------------------------------------------
        motivos.extend(
            _verificar_autorizaciones(ejecuciones, contratos)
        )

        # ----------------------------------------------------------
        # 9) versiones / esquemas
        # ----------------------------------------------------------
        m_ver, a_ver = _verificar_versiones(eventos, contratos)
        motivos.extend(m_ver)
        advertencias.extend(a_ver)

        if motivos:
            return self._emitir(
                estado=CS_ESTADO_RETENIDO,
                ciclo_id=ciclo_id,
                motivos=motivos,
                advertencias=advertencias,
                id_verificacion=id_ver,
                t0=t0,
                ts_inicio=ts_inicio,
                paquete=p,
                valores_paquete={
                    k: _str_frac(v) for k, v in valores_p.items()
                },
                valores_evidencia={
                    k: _str_frac(v) for k, v in valores_e.items()
                },
                reproducciones=reproducciones,
                hash_expediente=hash_exp,
                meta_extra=meta_exp,
                modulos=modulos,
                capacidades=capacidades,
                contratos=contratos,
                arbol_auditoria=arbol,
            )

        # ----------------------------------------------------------
        # 10) reproducción dinámica de capacidades del expediente
        # ----------------------------------------------------------
        if self._invocador is not None and ejecuciones:
            for ej in ejecuciones:
                mod = ej.get("modulo")
                cap = ej.get("capacidad")
                if not mod or not cap:
                    continue
                entrada = ej.get("entrada")
                resultado_reg = ej.get("resultado")
                try:
                    if isinstance(entrada, dict):
                        resultado_nuevo = self._invocador.invocar(
                            mod, cap, **entrada
                        )
                    elif isinstance(entrada, (list, tuple)):
                        resultado_nuevo = self._invocador.invocar(
                            mod, cap, *entrada
                        )
                    elif entrada is not None:
                        resultado_nuevo = self._invocador.invocar(
                            mod, cap, entrada
                        )
                    else:
                        resultado_nuevo = self._invocador.invocar(
                            mod, cap
                        )
                except Exception as e:
                    motivos.append(
                        "reproduccion {0}.{1}: {2}: {3}".format(
                            mod, cap, type(e).__name__, e
                        )
                    )
                    reproducciones.append({
                        "modulo": mod,
                        "capacidad": cap,
                        "estado": "ERROR",
                        "error": "{0}: {1}".format(
                            type(e).__name__, e
                        ),
                    })
                    continue

                coincide = True
                if resultado_reg is not None:
                    coincide = _igual_valor(
                        resultado_reg, resultado_nuevo
                    )
                    if not coincide:
                        motivos.append(
                            "reproduccion diverge {0}.{1}: "
                            "registrado={2} reproducido={3}".format(
                                mod,
                                cap,
                                resultado_reg,
                                resultado_nuevo,
                            )
                        )

                reproducciones.append({
                    "modulo": mod,
                    "capacidad": cap,
                    "estado": "OK" if coincide else "DIVERGE",
                    "resultado_registrado": (
                        str(resultado_reg)
                        if resultado_reg is not None
                        else None
                    ),
                    "resultado_reproducido": (
                        str(resultado_nuevo)
                        if resultado_nuevo is not None
                        else None
                    ),
                })

            if any(
                r.get("estado") in ("ERROR", "DIVERGE")
                for r in reproducciones
            ):
                return self._emitir(
                    estado=CS_ESTADO_RETENIDO,
                    ciclo_id=ciclo_id,
                    motivos=motivos,
                    advertencias=advertencias,
                    id_verificacion=id_ver,
                    t0=t0,
                    ts_inicio=ts_inicio,
                    paquete=p,
                    valores_paquete={
                        k: _str_frac(v) for k, v in valores_p.items()
                    },
                    valores_evidencia={
                        k: _str_frac(v) for k, v in valores_e.items()
                    },
                    reproducciones=reproducciones,
                    hash_expediente=hash_exp,
                    meta_extra=meta_exp,
                    modulos=modulos,
                    capacidades=capacidades,
                    contratos=contratos,
                    arbol_auditoria=arbol,
                )
        elif ejecuciones and self._invocador is None:
            advertencias.append(
                "invocador no disponible; verificación por "
                "consistencia de expediente"
            )

        # ----------------------------------------------------------
        # 11) cobertura: capacidades del contrato vs ejecutadas
        # ----------------------------------------------------------
        if contratos:
            caps_ejecutadas = {
                str(e.get("capacidad"))
                for e in ejecuciones
                if e.get("capacidad")
            }
            for cont in contratos:
                nombre = str(
                    cont.get("nombre")
                    or cont.get("id")
                    or cont.get("rol")
                    or "?"
                )
                declaradas = _capacidades_de_contrato(cont)
                # no se exige ejecutar todas; solo se advierte
                no_usadas = declaradas - caps_ejecutadas
                if no_usadas:
                    advertencias.append(
                        "contrato {0}: capacidades no ejercidas "
                        "en este ciclo: {1}".format(
                            nombre, sorted(no_usadas)
                        )
                    )

        # ----------------------------------------------------------
        # 12) parcial si el paquete declara estado no-OK
        # ----------------------------------------------------------
        if estado_eng in (PKG_ESTADO_UNDEFINED, PKG_ESTADO_PARCIAL):
            return self._emitir(
                estado=CS_ESTADO_PARCIAL,
                ciclo_id=ciclo_id,
                motivos=motivos + [
                    "estado de paquete no-OK: {0}".format(estado_eng)
                ],
                advertencias=advertencias,
                id_verificacion=id_ver,
                t0=t0,
                ts_inicio=ts_inicio,
                paquete=p,
                valores_paquete={
                    k: _str_frac(v) for k, v in valores_p.items()
                },
                valores_evidencia={
                    k: _str_frac(v) for k, v in valores_e.items()
                },
                reproducciones=reproducciones,
                hash_expediente=hash_exp,
                meta_extra=meta_exp,
                modulos=modulos,
                capacidades=capacidades,
                contratos=contratos,
                arbol_auditoria=arbol,
            )

        # ----------------------------------------------------------
        # 13) APROBADO
        # ----------------------------------------------------------
        return self._emitir(
            estado=CS_ESTADO_APROBADO,
            ciclo_id=ciclo_id,
            motivos=motivos or [
                "expediente coherente; paquete respaldado; "
                "proceso auditado"
            ],
            advertencias=advertencias,
            id_verificacion=id_ver,
            t0=t0,
            ts_inicio=ts_inicio,
            paquete=p,
            valores_paquete={
                k: _str_frac(v) for k, v in valores_p.items()
            },
            valores_evidencia={
                k: _str_frac(v) for k, v in valores_e.items()
            },
            reproducciones=reproducciones,
            hash_expediente=hash_exp,
            meta_extra=meta_exp,
            modulos=modulos,
            capacidades=capacidades,
            contratos=contratos,
            arbol_auditoria=arbol,
        )

    def _emitir(
        self,
        *,
        estado: str,
        ciclo_id: str,
        motivos: List[str],
        advertencias: List[str],
        id_verificacion: str,
        t0: float,
        ts_inicio: str,
        paquete: Dict[str, Any],
        valores_paquete: Optional[Dict[str, Optional[str]]] = None,
        valores_evidencia: Optional[Dict[str, Optional[str]]] = None,
        reproducciones: Optional[List[Dict[str, Any]]] = None,
        hash_expediente: Optional[str] = None,
        meta_extra: Optional[Dict[str, Any]] = None,
        modulos: Optional[List[str]] = None,
        capacidades: Optional[List[str]] = None,
        contratos: Optional[List[Dict[str, Any]]] = None,
        arbol_auditoria: Optional[List[Dict[str, Any]]] = None,
    ) -> Veredicto:
        ts_fin = datetime.now(timezone.utc).isoformat()
        duracion = round(time.perf_counter() - t0, 6)
        mods = list(modulos or [])
        caps = list(capacidades or [])
        conts = list(contratos or [])
        arbol = list(arbol_auditoria or [])

        meta = {
            "id_verificacion": id_verificacion,
            "version_centinela": CS_VERSION,
            "version_contrato": CS_VERSION_CONTRATO,
            "esquema": CS_ESQUEMA,
            "version_eventos_cs": CS_VERSION_EVENTOS,
            "modulos_en_expediente": mods,
            "capacidades_en_expediente": caps,
            "contratos_n": len(conts),
            "timestamp_inicio": ts_inicio,
            "timestamp_fin": ts_fin,
            "duracion_s": duracion,
            "hash_expediente": hash_expediente,
            "invocador_disponible": self._invocador is not None,
        }
        if meta_extra:
            meta["expediente"] = meta_extra

        v = Veredicto(
            estado=estado,
            ciclo_id=ciclo_id,
            motivos=list(motivos),
            advertencias=list(advertencias),
            id_verificacion=id_verificacion,
            hash_expediente=hash_expediente,
            meta_verificacion=meta,
            valores_paquete=dict(valores_paquete or {}),
            valores_evidencia=dict(valores_evidencia or {}),
            contratos=conts,
            reproducciones=list(reproducciones or []),
            arbol_auditoria=arbol,
            timestamp=ts_fin,
        )
        self._depositar_veredicto(v, paquete)
        self._ultimo_veredicto = v
        _STATS.registrar(
            estado, duracion, mods, caps, len(advertencias)
        )
        return v

    def _depositar_veredicto(
        self, v: Veredicto, paquete: Dict[str, Any]
    ) -> None:
        try:
            self._cache.guardar({
                "tipo": CS_TIPO_VEREDICTO,
                PKG_CICLO_ID: v.ciclo_id,
                "origen": CS_MODULO,
                "modulo": CS_MODULO,
                "categoria": CS_CATEGORIA_VEREDICTO,
                "estado": v.estado,
                CS_CAMPO_VEREDICTO: v.a_dict(),
                CS_CAMPO_CICLO_ID: v.ciclo_id,
                CS_CAMPO_ESTADO: v.estado,
                CS_CAMPO_MOTIVOS: list(v.motivos),
                CS_CAMPO_PAQUETE_REF: {
                    PKG_ESTADO: paquete.get(PKG_ESTADO),
                    PKG_O_CONTEXT: paquete.get(
                        PKG_O_CONTEXT, paquete.get(PKG_CONTEXTO)
                    ),
                },
            })
        except Exception:
            pass

    def estado(self) -> Dict[str, Any]:
        return {
            "id": CS_ID,
            "nombre": CS_NOMBRE,
            "rol": CS_ROL,
            "version": CS_VERSION,
            "esquema": CS_ESQUEMA,
            "operativo": True,
        }

    def salud(self) -> Dict[str, Any]:
        s = _STATS.resumen()
        return {
            "id": CS_ID,
            "coherente": True,
            "verificaciones": s["verificaciones"],
            "aprobadas": s["aprobadas"],
            "retenidas": s["retenidas"],
            "parciales": s["parciales"],
        }

    def inventario(self) -> Dict[str, Any]:
        return {
            "id": CS_ID,
            "nombre": CS_NOMBRE,
            "rol": CS_ROL,
            "version": CS_VERSION,
            "funcion": CS_FUNCION,
            "no_hace": list(CS_NO_HACE),
            "autoridad": list(CS_AUTORIDAD),
            "capacidades": [
                "verificar",
                "reporte",
                "inventario",
                "diagnostico",
                "estado",
                "salud",
                "estadisticas",
            ],
        }

    def reporte(self) -> Dict[str, Any]:
        return {
            "id": CS_ID,
            "nombre": CS_NOMBRE,
            "version": CS_VERSION,
            "estado": self.estado(),
            "salud": self.salud(),
            "estadisticas": _STATS.resumen(),
            "ultimo_veredicto": (
                self._ultimo_veredicto.a_dict()
                if self._ultimo_veredicto
                else None
            ),
        }

    def diagnostico(self) -> Dict[str, Any]:
        s = _STATS.resumen()
        advertencias: List[str] = []
        if s["retenidas"] > 0:
            advertencias.append(
                "ciclos retenidos: {0}".format(s["retenidas"])
            )
        return {
            "id": CS_ID,
            "estado": "OPERATIVO",
            "problemas": [],
            "advertencias": advertencias,
            "estadisticas": s,
        }

    def estadisticas(self) -> Dict[str, Any]:
        return _STATS.resumen()


# ===============================================================
# API DE CORE
# ===============================================================

def verificar_salida_paquete(
    paquete: Dict[str, Any],
    cache: Optional[CacheEvidencia] = None,
    invocador: Optional[InvocadorCapacidades] = None,
) -> Dict[str, Any]:
    return (
        Centinela(cache=cache, invocador=invocador)
        .verificar(paquete)
        .a_dict()
    )


def verificar_salida(salida: Any) -> bool:
    if not isinstance(salida, dict):
        return False
    if PKG_ESTADO in salida and salida[PKG_ESTADO] in CS_ESTADOS:
        return salida[PKG_ESTADO] == CS_ESTADO_APROBADO
    return False


__all__ = [
    "Centinela",
    "Veredicto",
    "CentinelaError",
    "CacheEvidencia",
    "InvocadorCapacidades",
    "CS_ID",
    "CS_NOMBRE",
    "CS_ROL",
    "CS_VERSION",
    "CS_ESTADO_APROBADO",
    "CS_ESTADO_RETENIDO",
    "CS_ESTADO_PARCIAL",
    "CS_ESTADOS",
    "verificar_salida_paquete",
    "verificar_salida",
]

# ===============================================================
# FIN DEL ARCHIVO
# ===============================================================
