# ===============================================================
# VPSI-TRUTH — modules/cache/INDCATION.md
# ===============================================================
#
# RD — Requisitos y plantilla del módulo CACHE (CH)
# Versión: 1.0
#
# ===============================================================

## 1. Qué es CACHE

CACHE (rol **CH**) es el **registrador universal de eventos** del sistema VPSI-TRUTH.

Es el **libro de actas** de cada ciclo de ejecución.

### Principio

Engine produce. Centinela verifica. CACHE registra. Analizadores futuros interpretan. Omega presenta.
### Qué hace

- Registrar exactamente lo que ocurrió durante la ejecución.
- Conservar evidencia objetiva (append-only).
- Exponer lecturas filtradas por campos del registro.
- Descubrir categorías de forma dinámica al depositar.

### Qué NO hace

- No interpreta.
- No deduce ni infiere.
- No reconstruye ciclos.
- No genera grafos ni árboles.
- No explica causas ni razonamientos.
- No calcula C, L, K, Tru_Ri ni Tru_total.
- No valida el significado del payload.
- No modifica, sobrescribe ni reordena evidencia depositada.

### Frase de diseño

> CACHE no sabe lo que ocurrió. Solo sabe qué fue registrado.

---

## 2. Arquitectura de archivos

modules/cache/ init.py ← infraestructura del registro (depositar, leer, filtrar) common.py ← vocabulario universal (estados, metadata común) fo.py ← diccionario oficial de FO ca.py ← diccionario oficial de CA ax.py ← … RD.md ← este documento
| Archivo        | Responsabilidad                                      |
|----------------|------------------------------------------------------|
| `__init__.py`  | Registro neutro. Única vía de escritura: `depositar`. |
| `common.py`    | Nombres compartidos por todos los módulos.           |
| `.py`     | Vocabulario oficial de un módulo. Sin lógica.        |
| `RD.md`        | Requisitos y plantilla.                              |

---

## 3. Registro neutro (cada evento)

Campos del registro:

| Campo          | Rol                                      |
|----------------|------------------------------------------|
| `seq`          | Orden de inserción (solo creciente).     |
| `timestamp`    | Momento del depósito (UTC).              |
| `event_id`     | Identificador estable del evento.        |
| `run_id`       | Identificador de la corrida.             |
| `ciclo_id`     | Identificador del ciclo.                 |
| `origen`       | Quién deposita.                          |
| `destino`      | Destino declarado (si aplica).           |
| `modulo`       | Módulo productor.                        |
| `capacidad`    | Capacidad involucrada.                   |
| `tipo`         | Tipo de evento (autoidentificable).      |
| `categoria`    | Categoría dinámica.                      |
| `estado`       | Estado del evento.                       |
| `payload`      | Datos del evento (dict).                 |

CACHE no interpreta ninguno de estos campos.

---

## 4. Reglas para diccionarios `cache/.py`

1. **Solo vocabulario.** Sin clases, sin funciones, sin lógica.
2. **Prefijo propio.** Todos los identificadores internos usan el prefijo del módulo (`FO_`, `CA_`, `AX_`, …).
3. **Valores autoidentificables.** Los strings registrados llevan el módulo: `fo.tru_total`, `ca.calculo`, `ax.axioma`.
4. **Sin colisiones.** Nunca reutilizar nombres genéricos (`ESTADO_OK`, `TIPO_RESULTADO`) sin prefijo.
5. **Esquema de payload.** Declarar obligatorios y opcionales por tipo de evento. CACHE no los valida; sirven a desarrolladores y analizadores futuros.
6. **Versión de eventos.** Cada archivo declara `VERSION_EVENTOS`.
7. **Común no se duplica.** Estados y metadata universales viven en `common.py`.

---

## 5. Plantilla (código borrador)

Copiar este archivo, renombrar y completar. Sustituir `XX` por el id del módulo en minúsculas y `XX`/`XX_` por el prefijo en mayúsculas.

```python
# ===============================================================
# VPSI-TRUTH — modules/cache/xx.py
# ===============================================================
#
# Diccionario oficial de eventos XX () para CACHE.
#
# No interpreta.
# No calcula.
# No deposita.
# Solo declara el vocabulario oficial de XX.
#
# Prefijo interno: XX_
# Valores registrados: xx.*  (autoidentificables)
#
# CACHE permanece neutro: recibe el evento tal cual.
# ===============================================================

# ===============================================================
# IDENTIDAD
# ===============================================================

MODULO = "XX"
NOMBRE = ""
ROL = "XX"

# ===============================================================
# VERSIÓN DEL ESQUEMA DE EVENTOS XX
# ===============================================================

VERSION_EVENTOS = "1.0"

# ===============================================================
# TIPOS DE EVENTO (valores autoidentificables)
# ===============================================================

XX_TIPO_EJEMPLO = "xx.ejemplo"
XX_TIPO_RESULTADO = "xx.resultado"
XX_TIPO_ERROR = "xx.error"
XX_TIPO_RECHAZO = "xx.rechazo"

XX_TIPOS = (
    XX_TIPO_EJEMPLO,
    XX_TIPO_RESULTADO,
    XX_TIPO_ERROR,
    XX_TIPO_RECHAZO,
)

# ===============================================================
# CATEGORÍAS (valores autoidentificables)
# ===============================================================

XX_CATEGORIA_DOMINIO = "xx.dominio"

XX_CATEGORIAS = (
    XX_CATEGORIA_DOMINIO,
)

# ===============================================================
# CAPACIDADES XX EN EL REGISTRO
# ===============================================================

XX_CAP_PRINCIPAL = "xx.principal"
XX_CAP_BARRER = "xx.barrer"
XX_CAP_INVENTARIO = "xx.inventario"
XX_CAP_REPORTE = "xx.reporte"
XX_CAP_DIAGNOSTICO = "xx.diagnostico"

XX_CAPACIDADES = (
    XX_CAP_PRINCIPAL,
    XX_CAP_BARRER,
    XX_CAP_INVENTARIO,
    XX_CAP_REPORTE,
    XX_CAP_DIAGNOSTICO,
)

# ===============================================================
# ESTADOS ESPECÍFICOS XX
# (los globales viven en cache/common.py)
# ===============================================================

XX_ESTADO_OK = "xx.ok"
XX_ESTADO_ERROR = "xx.error"
XX_ESTADO_RECHAZADO = "xx.rechazado"
XX_ESTADO_DESCARTADO = "xx.descartado"

XX_ESTADOS = (
    XX_ESTADO_OK,
    XX_ESTADO_ERROR,
    XX_ESTADO_RECHAZADO,
    XX_ESTADO_DESCARTADO,
)

# ===============================================================
# CAMPOS DE PAYLOAD XX
# ===============================================================

XX_CAMPO_ENTRADA = "entrada"
XX_CAMPO_SALIDA = "salida"
XX_CAMPO_RESULTADO = "resultado"
XX_CAMPO_ERROR = "error"
XX_CAMPO_DETALLE = "detalle"

XX_CAMPOS_PAYLOAD = (
    XX_CAMPO_ENTRADA,
    XX_CAMPO_SALIDA,
    XX_CAMPO_RESULTADO,
    XX_CAMPO_ERROR,
    XX_CAMPO_DETALLE,
)

# ===============================================================
# PAYLOAD OBLIGATORIO / OPCIONAL (por tipo de evento)
# CACHE no valida estos esquemas.
# ===============================================================

XX_PAYLOAD_OBLIGATORIO_RESULTADO = (
    XX_CAMPO_RESULTADO,
)

XX_PAYLOAD_OPCIONAL_RESULTADO = (
    XX_CAMPO_DETALLE,
)

XX_PAYLOAD_OBLIGATORIO_ERROR = (
    XX_CAMPO_ERROR,
)

XX_PAYLOAD_OPCIONAL_ERROR = (
    XX_CAMPO_DETALLE,
    XX_CAMPO_ENTRADA,
)

# ===============================================================
# ESQUEMA DE EVENTOS XX
# ===============================================================

XX_ESQUEMA_EVENTOS = {
    XX_TIPO_RESULTADO: {
        "obligatorios": XX_PAYLOAD_OBLIGATORIO_RESULTADO,
        "opcionales": XX_PAYLOAD_OPCIONAL_RESULTADO,
    },
    XX_TIPO_ERROR: {
        "obligatorios": XX_PAYLOAD_OBLIGATORIO_ERROR,
        "opcionales": XX_PAYLOAD_OPCIONAL_ERROR,
    },
    XX_TIPO_RECHAZO: {
        "obligatorios": (XX_CAMPO_ERROR,),
        "opcionales": (XX_CAMPO_DETALLE, XX_CAMPO_ENTRADA),
    },
    XX_TIPO_EJEMPLO: {
        "obligatorios": (XX_CAMPO_ENTRADA, XX_CAMPO_SALIDA),
        "opcionales": (XX_CAMPO_DETALLE,),
    },
}

# ===============================================================
# CAMPOS DE METADATA ESPECÍFICOS XX
# ===============================================================

XX_META_VERSION_EVENTOS = "version_eventos"
XX_META_MODULO = "modulo"
XX_META_ROL = "rol"

XX_CAMPOS_METADATA = (
    XX_META_VERSION_EVENTOS,
    XX_META_MODULO,
    XX_META_ROL,
)

# ===============================================================
# FIN DEL ARCHIVO
# ===============================================================

6. Cómo usar la plantilla
	1	Copiar la plantilla a modules/cache/.py (ejemplo: ax.py).
	2	Sustituir XX / xx por el id del módulo (AX / ax).
	3	Completar NOMBRE y ROL.
	4	Declarar tipos, categorías, capacidades y campos reales del módulo.
	5	Definir XX_ESQUEMA_EVENTOS con obligatorios y opcionales por tipo.
	6	No añadir funciones ni clases.
	7	No importar Engine, Calculator ni otros módulos de cálculo.

7. Ejemplo de depósito (referencia)
from modules.cache import depositar
from modules.cache.fo import (
    MODULO,
    VERSION_EVENTOS,
    FO_TIPO_TRU_TOTAL,
    FO_CAP_TRU_TOTAL,
    FO_CATEGORIA_VERDAD,
    FO_ESTADO_OK,
    FO_CAMPO_C,
    FO_CAMPO_L,
    FO_CAMPO_K,
    FO_CAMPO_ALPHA,
    FO_CAMPO_BETA,
    FO_CAMPO_RESULTADO,
)

depositar(
    tipo=FO_TIPO_TRU_TOTAL,
    payload={
        FO_CAMPO_C: C,
        FO_CAMPO_L: L,
        FO_CAMPO_K: K,
        FO_CAMPO_ALPHA: alpha,
        FO_CAMPO_BETA: beta,
        FO_CAMPO_RESULTADO: tru_total,
        "version_eventos": VERSION_EVENTOS,
    },
    ciclo_id=ciclo_id,
    run_id=run_id,
    origen="engine",
    modulo=MODULO,
    capacidad=FO_CAP_TRU_TOTAL,
    categoria=FO_CATEGORIA_VERDAD,
    estado=FO_ESTADO_OK,
)
CACHE solo almacena. No valida el esquema FO.

8. Prioridades
	1	Prefijos en todos los identificadores internos.
	2	Valores autoidentificables (fo.*, ca.*, …).
	3	Vocabulario común en common.py sin duplicar.
	4	Esquemas de payload (obligatorios / opcionales).
	5	event_id estable en el registro (infraestructura __init__.py).
	6	CACHE siempre agnóstico respecto al significado de lo registrado.

9. Cierre
Este RD define el estándar de CACHE y de sus diccionarios de vocabulario.
Todo archivo nuevo bajo modules/cache/ debe cumplir esta plantilla y estas reglas.
# ===============================================================
# FIN DEL RD
# ===============================================================

**Archivo:** `modules/cache/RD.md`

Incluye:
1. Qué es CACHE  
2. Arquitectura de archivos  
3. Registro neutro  
4. Reglas de vocabulario  
5. **Plantilla completa** (código borrador)  
6. Cómo usarla  
7. Ejemplo de depósito  
8. Prioridades
