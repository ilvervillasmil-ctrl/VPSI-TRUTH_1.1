# archivo — ESPARTACO
## Batería Adversarial · Cadena de Consistencia · Grafo de Dependencias

**SPEC:** TEST-ESPARTACO-CADENA-GRAFO-1.0 + TEST-ESPARTACO-MULTI-ATACANTE  
**Revisión:** 2026-08-11  
**CI de referencia:** #544 · VPSI-TRUTH_1.1  
**Resultado medido:** 813 passed · 1 skipped · 0 failed  

---

## 1. Qué verifica esta batería

Esta batería **verifica** lo siguiente, de forma literal y medible:

1. Que un artefacto legítimo firmado con la clave privada de la autoridad atraviesa **todos** los nodos de la cadena hasta `aceptacion` (`ok is True`).
2. Que un atacante que **posee la clave pública** y **no posee la clave privada** no puede producir `ok is True` sobre un artefacto mutado.
3. Que cada mutación hostil se **detiene en un nodo concreto** de la cadena de dependencias (primera inconsistencia verificable).
4. Que el detector de nodo es **determinista**: usa claves del SUT (`fallos`, `conceptos`, `pasos.*.ok`), no heurística de texto.
5. Que el Monte Carlo multi-atacante y el Monte Carlo de cadena reportan **BREACH = 0**, **EXCEPTION = 0**, **INDETERMINATE = 0**.
6. Que la autoridad legítima sigue verificando `ok is True` al final de la corrida (no se corrompe el SUT).

No se afirma ausencia absoluta de vulnerabilidades fuera del espacio de mutaciones ensayado.  
Se afirma lo que el CI midió: **cero aceptaciones no autorizadas** bajo los frentes, semillas y N ejecutados.

---

## 2. Tests que componen la batería Espartaco

| Archivo | Tests | CI #544 |
|---------|-------|---------|
| `tests/test_espartaco_cadena_grafo.py` | `test_00` … `test_04`, `test_99` | **6/6 PASSED** |
| `tests/test_espartaco_multi_atacante_montecarlo.py` | `test_00`, `test_01`, `test_99` | **3/3 PASSED** |
| `tests/test_conformidad_independiente.py` | reconocimiento + mutaciones + tabla final | **PASSED** |
| `tests/test_proteccion_adversarial.py` | mutaciones de cuerpo, firma, bytes, manifiesto | **PASSED** |
| `tests/test_proteccion_adversarial_demolicion.py` | demolición tipada, TOCTOU, hostiles | **PASSED** (1 skip tipado) |

**Suite global CI #544:** 813 passed · 1 skipped (`test_n_neutro_tipo_adversarial[3.0]`) · 0 failed.

---

## 3. Grafo de dependencias de la cadena

```
                    CLAVE PRIVADA (solo autoridad)
                            │
                            ▼
                    ┌───────────────┐
                    │  build()      │
                    │  firma Ed25519│
                    └───────┬───────┘
                            │
                            ▼
┌────────┐    ┌────────┐    ┌──────────┐    ┌─────────┐    ┌────────┐
│ datos  │───▶│ nucleo │───▶│  cuerpo  │───▶│canónico │───▶│ firma  │
└───┬────┘    └────────┘    └────┬─────┘    └─────────┘    └───┬────┘
    │                            │                             │
    │         ┌──────────────────┼──────────────────┐          │
    │         ▼                  ▼                  ▼          │
    │    canales_S          canales_Q           n_bytes        │
    │         └──────────────────┼──────────────────┘          │
    │                            │                             │
    │                            ▼                             │
    │                      manifiesto ◀────────────────────────┘
    │                            │
    │                            ▼
    │                      aceptacion
    │                            ▲
    └────────────────────────────┘
         (pub_bytes solo VERIFICA; no genera firma nueva)
```

### Aristas (dependencias)

| Origen | Destino | Significado |
|--------|---------|-------------|
| `datos` | `nucleo` | `nucleo = SHA-256(datos)` sellado en cuerpo |
| `datos` | `canales_S` / `canales_Q` | canales derivados del artefacto |
| `datos` | `n_bytes` | longitud autenticada |
| `nucleo` · `S` · `Q` · `n_bytes` | `cuerpo` | campos del cuerpo firmado |
| `cuerpo` | `canónico` | serialización determinista |
| `canónico` | `firma` | Ed25519 sobre el canónico |
| `firma` | `manifiesto` | contenedor `{cuerpo, firma}` |
| `manifiesto` | `aceptacion` | `ok is True` solo si toda la cadena cuadra |

**Invariante:** mutar un origen sin reconstruir correctamente todos los destinos produce inconsistencia en el **primer nodo** que el pipeline evalúa.

---

## 4. Cómo funciona el detector (determinista)

El detector **no infiere por texto**. Lee claves del resultado de `P.verificar`:

```
fallos          → lista de estaciones que fallaron
conceptos       → {FIRMA_INVÁLIDA, INTEGRIDAD_COMPROMETIDA, ...}
pasos.manifiesto.ok
pasos.nucleo.ok
pasos.canales.ok
pasos.n_bytes.ok
```

Orden de detención (primera inconsistencia gana):

1. tipo de `datos`
2. forma de `manifiesto` / firma
3. `nucleo`
4. `canales`
5. `n_bytes`
6. `aceptacion` (solo legítimo o BREACH)

Clasificación de cada ataque:

| Clase | Condición |
|-------|-----------|
| **NO_OP** | mutación no cambió datos ni manifiesto |
| **BLOCKED** | `ok is False` |
| **BREACH** | ataque hostil con `ok is True` |
| **EXCEPTION** | excepción no capturada por el SUT |
| **INDETERMINATE** | resultado sin forma contractual |

Criterio de PASS del harness: `BREACH = 0` · `EXCEPTION = 0` · `INDETERMINATE = 0`.

---

## 5. Separación de claves (lo que el test verifica)

| Material | Quién lo tiene | Uso |
|----------|----------------|-----|
| **Clave privada** | Solo la autoridad, en el fixture, para `P.build` | Firmar el artefacto legítimo |
| **Clave pública (`pub_bytes`)** | Autoridad + todos los atacantes | Verificar firma; **no** genera firma Ed25519 nueva |

El atacante recibe: `pub_bytes`, `datos`, `manifiesto`.  
El atacante **no** recibe: `private_key`, ruta de `.key`, `Ed25519PrivateKey`.

`AtacanteCadena.tiene_solo_publica()` y `AtacanteMonteCarlo` comprueban esa restricción en cada escenario.

---

## 6. Fases del test de cadena

### Fase 0 — Procedencia
Identidad del harness (`SPEC_ID`, `SPEC_HASH`).

### Fase 1 — Cadena legítima completa
Artefacto firmado por la autoridad → `ok is True` → nodo `aceptacion` → trayectoria PASS en firma y nucleo.

### Fase 2 — Cambio de un byte (ejemplo del “53”)
Mutación de un byte en `datos` → `SHA-256` deja de coincidir → detención en **nucleo**.  
La firma del cuerpo intacto sigue PASS.  
**Verifica:** el atacante con pública no recompone la cadena solo cambiando bytes.

### Fase 3 — Rearme parcial sin privada
El atacante recalcula `nucleo` localmente, lo escribe en el cuerpo, **no puede re-firmar** → detención en **firma** (`FIRMA_INVÁLIDA`).  
**Verifica:** conocer el procedimiento y tener la pública no basta para producir aceptación.

### Fase 4 — Atacante solo con pública
Construcción del atacante + assert de ausencia de material privado + verificación legítima con esa misma pública.

### Fase 99 — Monte Carlo de cadena (grafo)
N atacantes (env `ESPARTACO_CADENA_N`, default 100000).  
Cada uno elige un frente, muta, se clasifica, se cuenta el **nodo de detención**.  
Reporta matriz `frente × nodo` y grafo de aristas.

---

## 7. Resultado medido del Monte Carlo de cadena (corrida local de calibración)

Con `ESPARTACO_CADENA_N=30000`, `MASTER_SEED=20260811`:

```
ATTACKERS_GENERATED  30000
NO_OP                463
ATTACKS_EXECUTED     29537
BLOCKED              29537
BREACH               0
EXCEPTION            0
INDETERMINATE        0
```

### Dónde se tranca el atacante

| Nodo de detención | Conteo |
|-------------------|--------|
| **firma** | 17315 |
| **nucleo** | 12222 |
| datos / manifiesto / canales / n_bytes / aceptacion | 0 |

### Matriz causal (frente → nodo)

| Frente | nucleo | firma |
|--------|--------|-------|
| intercepta_byte | sí | — |
| intercepta_region | sí | — |
| intercepta_longitud | sí | — |
| intercepta_nucleo | — | sí |
| intercepta_canal_S | — | sí |
| intercepta_canal_Q | — | sí |
| intercepta_firma | — | sí |
| intercepta_cuerpo | — | sí |
| rearma_parcial | — | sí |

**Lectura:**  
- Mutar bytes del artefacto → la cadena se rompe en **nucleo** (primera ronda de integridad).  
- Mutar cuerpo / canales / firma o rearmar sin privada → la cadena se rompe en **firma**.  
- Nadie llegó a `aceptacion` de forma no autorizada.

El test es **determinista** (semilla + RNG por atacante).  
Escalar a 100M o 300M es cuestión de `ESPARTACO_CADENA_N` / tiempo de CI; la lógica de detención en la primera inconsistencia ya está demostrada en las fases calibradas y en el Monte Carlo medido.

---

## 8. Lectura unificada de todos los Espartaco

```
                    ┌─────────────────────────────────────┐
                    │     AUTORIDAD (clave privada)       │
                    │     build → artefacto + manifiesto  │
                    └─────────────────┬───────────────────┘
                                      │
              ┌───────────────────────┼───────────────────────┐
              ▼                       ▼                       ▼
     test_conformidad          test_proteccion          test_espartaco_*
     independiente             adversarial*             cadena + multi
              │                       │                       │
              │                       │                       │
              └───────────────────────┼───────────────────────┘
                                      ▼
                    P.verificar(..., modo=MODO_PROTEGIDO)
                                      │
                    ┌─────────────────┼─────────────────┐
                    ▼                 ▼                 ▼
              BLOCKED            BREACH=0          EXCEPTION=0
           (nodo concreto)     (CI medido)        (CI medido)
```

Lo que el conjunto **verifica**:

- Mutación de `artifact_id`, `nucleo`, `S`, `Q`, `n_bytes`, `n_neutro`, `valuaciones`, `firma`, bytes del artefacto, manifiesto incompleto, firma fabricada, recomposición, TOCTOU tipado, claves públicas hostiles, datos extremos → **rechazo** en el nodo correspondiente.
- Atacante con solo pública → **no** produce `ok is True` en los frentes ensayados.
- Pipeline legítimo → **sí** produce `ok is True`.

---

## 9. Cómo se ejecuta

```bash
# Cadena / grafo (N configurable)
ESPARTACO_CADENA_N=100000 ESPARTACO_CADENA_SEED=20260811 \
  pytest tests/test_espartaco_cadena_grafo.py -s -v

# Multi-atacante Monte Carlo previo
MULTI_ATTACK_N=100000 \
  pytest tests/test_espartaco_multi_atacante_montecarlo.py -s -v

# Suite adversarial completa
pytest tests/test_espartaco_*.py tests/test_proteccion_adversarial*.py \
       tests/test_conformidad_independiente.py -q
```

---

## 10. Estado contractual (CI #544)

| Ítem | Valor medido |
|------|----------------|
| Tests totales | 814 collected |
| Passed | **813** |
| Failed | **0** |
| Skipped | **1** (`n_neutro_tipo_adversarial[3.0]`) |
| Espartaco cadena | **6/6 PASSED** |
| Espartaco multi-atacante | **3/3 PASSED** |
| BREACH (cadena + multi) | **0** |
| Tiempo pytest | 44.94 s |

---

## 11. Conclusión operativa

El grafo de la cadena está definido.  
Los detectores leen claves del SUT.  
Los atacantes operan con clave pública y sin privada.  
Las mutaciones de la batería se detienen en el **primer nodo inconsistente** (nucleo o firma según el frente).  
El CI #544 registró **813 passed, 0 failed** e incluye el PASS de `test_espartaco_cadena_grafo` y de `test_espartaco_multi_atacante_montecarlo`.

Eso es lo que esta batería **verifica**.

---

*Documento vivo. Actualizar solo con salidas de CI o corridas con semilla declarada.*
