# RED NAME — TR1 GENERATIVIDAD
## Estudio formal · coherencia · trazabilidad · reconstrucción semántica independiente

**SPEC**
- TEST-GENERATIVIDAD-TR1
- TEST-TRAZABILIDAD-TR1
- TEST-ORACLE-SEMANTICO-TR1

**Revisión:** 2026-08-13  
**Commit CI de referencia:** `e98adb7b30e4a959e7238e7be61a68816b0b3c4e`  
**Resultado medido del run:** 742 passed · 0 failed · 0 skipped  

---

## 1. Objeto del estudio

Esta batería no constituye un único test ni una única afirmación.

Establece una cadena de verificación separada en niveles:

* **Nivel 1:** Coherencia contractual de los agregados publicados
* **Nivel 2:** Coherencia estructural e invariantes del universo operativo y de la capa canónica
* **Nivel 3:** Observabilidad de la decisión individual
* **Nivel 4:** Reconstrucción semántica independiente de las decisiones individuales mediante fuente formal externa a la implementación
* **Nivel 5:** Confrontación par-a-par entre decisión esperada y decisión publicada

El Nivel 5 constituye la verificación semántica individual máxima.

En el run de referencia, el Nivel 5 queda definido contractualmente, pero no puede ejecutarse sobre 276/276 porque la superficie pública actual no expone la decisión individual de cada par.

Eso no invalida los niveles anteriores.  
Tampoco convierte la ausencia de superficie de traza en un fallo semántico.

---

## 2. Qué significa coherencia en esta batería

El resultado:

**742 passed · 0 failed · 0 skipped**

no debe describirse únicamente como “los tests pasaron”.

La batería demuestra que el cuerpo contractual sometido a prueba mantiene simultáneamente sus relaciones internas bajo ejecución.

En particular:

$$C + I = T$$
$$N + R = C$$

y, para la capa canónica:

$$|\Theta| = 24$$
$$C(24,2) = 276$$
$$C = 183$$
$$I = 93$$
$$N = 153$$
$$R = 30$$

La ausencia de contradicciones entre estas relaciones no demuestra por sí sola la semántica externa de cada decisión.  
Tampoco es correcto reducir el resultado a una simple coincidencia numérica.

La batería utiliza el significado operacional de las categorías:  
**compatible** / **incompatible** / **novedoso** / **redundante**

para verificar invariantes, cobertura, identidad y consistencia entre capas.

La semántica de los objetos auditados es, por tanto, una condición necesaria para interpretar correctamente qué está siendo verificado.

---

## 3. Arquitectura de las capas

### 3.1 Capa operacional

Es el cuerpo real producido por el repositorio.

En el run de referencia:

* **theta_n:** 297
* **pares_totales:** 43956
* **pares_compatibles:** 11506
* **pares_novedosos:** 7047
* **pares_redundantes:** 4459
* **pares_incompatibles:** 32450

Esta capa representa el universo operacional completo del repositorio. No debe mezclarse con $\Theta_{24}$.

---

### 3.2 Capa canónica

La capa canónica fija el universo formal de TR1:

$$|\Theta| = 24$$
$$C(24,2) = 276$$

con los valores:

* **compatibles:** 183
* **incompatibles:** 93
* **novedosos:** 153
* **redundantes:** 30

La capa canónica funciona como superficie de comparación con la especificación formal.

---

### 3.3 Capa formal independiente

La reconstrucción semántica independiente no obtiene $D_i$ de:
- `gobierna`
- `_medir_pares`
- `generatividad()`
- `canonica["dominios_formales"]`

cuando cualquiera de ellos proceda de la misma ruta clasificadora que se pretende verificar.

Los $D_i$ se obtienen del cuerpo formal independiente:  
*Cuadro 4 — Principle of Structural Invariance*

y se aplica directamente la regla formal TR1/T15.

La independencia es la separación entre:

**FUENTE FORMAL**  
↓  
**$D_i$**  
↓  
**T15/TR1**  
↓  
**decisión esperada**  

y:

**IMPLEMENTACIÓN**  
↓  
**clasificador operacional**  
↓  
**decisión publicada**  

---

## 4. Reconstrucción semántica individual

La ausencia de `g["traza"]` no significa que la decisión individual sea conceptualmente irrecuperable.

La decisión puede reconstruirse independientemente para cada par.

Para cualquier **(A, B)**, se obtiene **$D_A, D_B$** desde la especificación formal independiente.

Después se aplica T15:

* **$D_A \cap D_B = \emptyset$** $\rightarrow$ incompatible
* **$D_A \cap D_B \neq \emptyset$** $\rightarrow$ compatible
* **compatible** y **$(D_A \cup D_B \supset D_A)$** y **$(D_A \cup D_B \supset D_B)$** $\rightarrow$ novedoso
* **compatible** en cualquier otro caso $\rightarrow$ redundante

Por tanto, el oracle no solamente produce cinco números finales.  
Produce una decisión semántica individual para cada uno de los:

$$C(24,2) = 276$$

pares.

Cada decisión tiene la forma:

**(A, B)**  
↓  
**$D_A, D_B$**  
↓  
**TR1 / T15**  
↓  
**primaria / secundaria**  

Los agregados **183 / 93 / 153 / 30** son consecuencias de esas 276 decisiones. No son la fuente primaria de la reconstrucción.

---

## 5. Independencia semántica

La independencia exigida no significa que los conceptos de TR1/T15 sean desconocidos por el repositorio.

Significa que la derivación que produce la decisión esperada no depende del clasificador cuya salida se pretende auditar.

El oracle no debe:
- importar `generatividad()`
- importar `_medir_pares`
- reutilizar el clasificador operacional
- utilizar `gobierna` como sustituto de $D_i$
- utilizar una estructura producida por la misma ruta semántica

El oracle debe efectuar una derivación independiente:

**fuente formal**  
↓  
**dominios $D_i$**  
↓  
**intersección**  
↓  
**unión**  
↓  
**regla T15**  
↓  
**clasificación esperada**  

---

## 6. Nivel 1 — Coherencia contractual

**Test:** `tests/test_generatividad_tr1.py`  
**Pregunta:** ¿La implementación publica agregados que satisfacen sus invariantes contractuales?

**Verifica:**
- `theta_n`
- `pares_totales`
- `pares_compatibles`
- `pares_incompatibles`
- `pares_novedosos`
- `pares_redundantes`
- `im_vs_theta`
- `identidad_pares`
- `identidad_compatibles`

**Invariantes:**

$$C + I = T$$
$$N + R = C$$

También verifica la capa canónica:  
**24 / 276 / 183 / 153 / 30 / 93**

Este nivel demuestra coherencia contractual. No constituye todavía una demostración par-a-par.

---

## 7. Nivel 2 — Observabilidad y trazabilidad

**Tests:**
- `tests/test_2trazabilidad_tr1.py`
- `tests/test_trazabilidad_tr1.py`

**Pregunta:** ¿La superficie pública permite seguir una decisión individual?

La estructura requerida es:

**(A, B)**  
↓  
**decisión primaria**  
↓  
**decisión secundaria**  
↓  
**agregación**  

La superficie pública actual no expone `id_a`, `id_b`, `primaria`, `secundaria` por cada par.

Por ello, **TRAZABILIDAD INDIVIDUAL NO OBSERVABLE** es un hallazgo arquitectónico de auditabilidad.

No debe etiquetarse como:
- fallo semántico
- contradicción
- inconsistencia de producción

---

## 8. Nivel 3 — Reconstrucción formal independiente

**Test:** `tests/test_3oracle_semantico_tr1.py`

Este nivel responde una pregunta distinta:  
*Si no se utiliza el clasificador de producción, ¿puede derivarse independientemente qué debería ocurrir con cada uno de los 276 pares?*

Respuesta medida: **sí**.

El oracle:
1. fija $\Theta_{24}$ formal;
2. asigna $D_i$ desde la fuente formal independiente;
3. enumera $C(24,2) = 276$ pares;
4. aplica T15 a cada par;
5. produce una decisión esperada individual;
6. deriva los agregados de esas decisiones.

**Resultado:**
- **decisiones:** 276
- **compatibles:** 183
- **incompatibles:** 93
- **novedosas:** 153
- **redundantes:** 30

---

## 9. Validación cruzada de agregados

Una vez construidas independientemente las 276 decisiones, sus agregados producen:  
**276 / 183 / 93 / 153 / 30**

La capa canónica de producción publica exactamente:  
**276 / 183 / 93 / 153 / 30**

Por tanto:

**ORACLE INDEPENDIENTE**  
↓  
**276 decisiones**  
↓  
**agregación**  
↓  
**276 / 183 / 93 / 153 / 30**  
↕  
**CAPA CANÓNICA**  
↓  
**276 / 183 / 93 / 153 / 30**  

Esta coincidencia constituye una validación cruzada independiente de los agregados.

Debe quedar explícitamente establecido:  
**coincidencia de agregados $\neq$ comparación individual de producción**

---

## 10. Nivel 4 — Trazabilidad semántica reconstruida

Este nivel distingue dos hechos:  
**A.** La decisión esperada puede reconstruirse.  
**B.** La decisión publicada por producción no puede actualmente observarse par-a-par.

Estado actual:

**(A, B)**  
↓  
**$D_A, D_B$**  
↓  
**T15**  
↓  
**decisión esperada**  
↓  
**[superficie pública ausente]**  
**X**  
**decisión publicada**  

La **X** representa una limitación de observabilidad, no una contradicción semántica.

La reconstrucción independiente ya existe. Lo que falta es una superficie contractual que permita poner ambos resultados uno frente al otro.

---

## 11. Nivel 5 — Verificación semántica par-a-par

Este es el nivel máximo de la batería.

La afirmación que debe verificarse es que para todo par (A, B) perteneciente a C(Θ_24, 2):

decisión_publicada(A, B) == decisión_esperada(A, B)

donde:
- decisión_esperada(A, B) se obtiene exclusivamente de D_A, D_B, T15/TR1
- decisión_publicada(A, B) debe proceder de la capa canónica de producción

La comparación no debe utilizar la capa operativa de 297 elementos, porque su universo no es Θ_24.

La comparación correcta es:

ORACLE Θ_24  
↕  
CANÓNICA Θ_24  

---

## 12. Condiciones necesarias para ejecutar el Nivel 5

Cuando exista `canonica["traza"]`, el TEST 3 deberá exigir simultáneamente:

- len(traza) == 276
- cobertura exacta de los 24 IDs
- cobertura exacta de C(24,2)
- ausencia de pares duplicados
- ausencia de pares fuera de Θ_24
- presencia de id_a, id_b, primaria, secundaria

y, para cada par individual:

primaria_publicada == primaria_esperada
secundaria_publicada == secundaria_esperada

**No basta con que los agregados continúen siendo**:
**183 / 93 / 153 / 30**

En este nivel, los agregados deben ser consecuencias directas de las 276 comparaciones individuales.

---

## 13. Por qué los agregados no son evidencia primaria del Nivel 5

Dos sistemas diferentes podrían producir 183 compatibles, 93 incompatibles, 153 novedosos y 30 redundantes, y, sin embargo, diferir en cuáles pares recibieron cada clasificación.

Por tanto:

* **Igualdad de agregados:** Coincidencia global.
* **Igualdad de las 276 decisiones:** Correspondencia individual.

El Nivel 5 exige la segunda.

---

## 14. Cadena completa de demostración

**CUERPO FORMAL INDEPENDIENTE**  
*(Cuadro 4 / $\Theta_{24}$)*  
↓  
**$D_A , D_B$**  
↓  
**Regla T15/TR1**  
↓  
**DECISIÓN ESPERADA**  
↓ *(comparación individual)*  
↕  
**DECISIÓN PUBLICADA (CAPA CANÓNICA)**  
↓  
**276 verificaciones**  
↓  
**agregación secundaria**  
↓  
**183 / 93 / 153 / 30**  

En el run actual, la cadena llega hasta:

**decisión esperada**  
↓  
**agregados oracle**  
↕  
**agregados canónicos**  

La arista **decisión esperada $\leftrightarrow$ decisión publicada** queda definida, pero no ejecutable por falta de exposición contractual de la decisión individual.

---

## 15. Resultados del run de referencia

### Capa operativa
* **theta_n:** 297
* **pares_totales:** 43956
* **pares_compatibles:** 11506
* **pares_novedosos:** 7047
* **pares_redundantes:** 4459
* **pares_incompatibles:** 32450
* **im_vs_theta:** GENERATIVO
* **u1_proxy:** NO_STAGNANT
* **identidad_pares:** True
* **identidad_compatibles:** True

### Capa canónica
* **theta_n:** 24
* **pares_totales:** 276
* **pares_compatibles:** 183
* **pares_novedosos:** 153
* **pares_redundantes:** 30
* **pares_incompatibles:** 93
* **im_vs_theta:** GENERATIVO
* **identidad_pares:** True
* **identidad_compatibles:** True
* **coincide_paper:** True
* **ids_presentes:** 24
* **ids_faltantes:** []

### Reconstrucción independiente
* **pares derivados:** 276
* **compatibles:** 183
* **incompatibles:** 93
* **novedosos:** 153
* **redundantes:** 30
* **igualdad oracle $\leftrightarrow$ canónica:** True
* **comparación individual:** NO OBSERVABLE

---

## 16. Determinismo

La batería no depende de muestreo aleatorio.

El universo $\Theta_{24}$ se enumera exhaustivamente:

$$C(24,2) = 276$$

La reconstrucción formal es determinista. La producción también se somete a comprobaciones de determinismo en sus superficies agregadas.

Esto permite distinguir:

* **Determinismo de agregados:** Medido (`identidad_pares`, `identidad_compatibles`)
* **Determinismo de decisión individual:** No certificable directamente sin decisión individual observable

---

## 17. Independencia y exclusiones

Para preservar independencia semántica, **TEST 3** excluye:
- `_medir_pares`
- `generatividad()` como clasificador
- `gobierna` como $D_i$
- clasificadores privados
- rutas de producción que ya hayan generado la decisión

Tampoco utiliza `canonica["dominios_formales"]` como fuente independiente si dicha estructura procede de la misma ruta semántica que se pretende contrastar.

La capa canónica se utiliza como superficie de comparación, no como fuente del oracle.

---

## 18. Estado actual de cada nivel

* **Nivel 1 (¿Los agregados cumplen el contrato?):** DEMOSTRADO
* **Nivel 2 (¿Las capas mantienen invariantes y determinismo?):** DEMOSTRADO
* **Nivel 3 (¿La decisión individual es públicamente observable?):** NO OBSERVABLE
* **Nivel 4 (¿Puede reconstruirse independientemente la decisión para cada par?):** DEMOSTRADO
* **Nivel 5 (¿Cada decisión independiente coincide con la decisión publicada?):** DEFINIDO / NO EJECUTADO PAR-A-PAR

La razón del estado del Nivel 5 es exclusivamente la ausencia de una superficie pública contractual que permita observar la decisión individual de producción.

---

## 19. Qué demuestra realmente el run

El run demuestra simultáneamente:
1. Coherencia contractual de la implementación.
2. Coherencia de las invariantes.
3. Estabilidad/determinismo de las superficies auditadas.
4. Correspondencia de la capa canónica con los valores formales.
5. Existencia de una reconstrucción semántica independiente.
6. Reproducción independiente de los 276 pares.
7. Coincidencia de los agregados independientes con la capa canónica.
8. Existencia de una especificación precisa para la verificación semántica individual de Nivel 5.

No debe afirmarse todavía: *las 276 decisiones de producción fueron verificadas individualmente contra el oracle* porque la superficie contractual actual no permite observarlas.

La afirmación correcta es: *las 276 decisiones esperadas pueden reconstruirse independientemente y sus agregados coinciden exactamente con la capa canónica; la confrontación individual queda definida contractualmente para cuando la decisión publicada sea observable.*

---

## 20. Criterio de cierre del Nivel 5

El Nivel 5 solamente podrá declararse **DEMOSTRADO** cuando:
1. 276/276 pares estén publicados;
2. cada par aparezca exactamente una vez;
3. cada par pertenezca a $\Theta_{24}$;
4. cada entrada contenga la decisión primaria y secundaria;
5. $D_A$ y $D_B$ procedan de la fuente independiente;
6. T15 produzca la decisión esperada;
7. $\text{decisión esperada} == \text{decisión publicada}$ para los 276 pares.

Solamente después de completar esas 276 comparaciones podrá afirmarse: **VERIFICACIÓN SEMÁNTICA INDIVIDUAL 276/276**.

Los agregados (**183 / 93 / 153 / 30**) deberán entonces recalcularse desde esas 276 decisiones verificadas, no utilizarse como sustituto de ellas.

---

## 21. Integridad arquitectónica

**TEST 3** no modifica:
- `Engine`
- `CONTENEDOR`
- `THETA`
- `generatividad()`
- `_medir_pares`
- contratos existentes

La ausencia de traza pública tampoco obliga a introducir una nueva API como parte de esta batería.

La eventual exposición de una traza individual es una decisión arquitectónica independiente de la auditoría.

El test debe auditar la superficie existente y no diseñar la arquitectura que le gustaría tener.

---

## 22. Conclusión formal

La batería TR1 establece una separación entre cuatro hechos que no deben confundirse:
- **COHERENCIA**
- **OBSERVABILIDAD**
- **RECONSTRUCCIÓN INDEPENDIENTE**
- **VERIFICACIÓN INDIVIDUAL**

La implementación ha sido sometida a una batería que alcanza **742 tests pasados sin fallos**.

La capa canónica reproduce:
- $\Theta_{24}$
- 276 pares
- 183 compatibles
- 93 incompatibles
- 153 novedosos
- 30 redundantes

Un cuerpo formal independiente reconstruye las mismas 276 decisiones sin reutilizar el clasificador de producción y obtiene exactamente los mismos agregados.

Por tanto, existe una vía independiente de reconstrucción semántica.

El último salto no es reconstruir la semántica.  
El último salto es observar simultáneamente **decisión esperada** y **decisión publicada** para el mismo par $(A, B)$.

Ese salto constituye el Nivel 5:

**(A, B)**  
→  
**$D_A, D_B$**  
→  
**TR1 / T15**  
→  
**decisión esperada**  
↔  
**decisión publicada**  
→  
**276 / 276**  

El run actual deja este último enlace formalmente definido, pero no ejecutado par-a-par debido a la ausencia de la superficie contractual de traza individual.

*Fin del estudio.*

---

# ANEXO A — GLOSARIO DE TÉRMINOS Y SÍMBOLOS
## RED NAME — TR1 GENERATIVIDAD

* **$\Theta$:** Universo formal de teoremas del framework. En la capa canónica, $|\Theta| = 24$.
* **$\Theta_{24}$:** Conjunto canónico de 24 elementos: T1–T17, U0, U1, M1, M.1, B-Canonical, TT.6.1, TR1.
* **$|\Theta|$:** Cardinalidad de $\Theta$. Valor canónico: 24.
* **$C(n, 2)$:** Número de pares no ordenados de $n$ elementos. $C(24,2) = 276$.
* **T:** `pares_totales`. Número total de pares del universo considerado.
* **C:** `pares_compatibles`. Pares con intersección de dominios no vacía.
* **I:** `pares_incompatibles`. Pares con intersección de dominios vacía.
* **N:** `pares_novedosos`. Compatibles cuya unión crece estrictamente respecto de ambos dominios.
* **R:** `pares_redundantes`. Compatibles sin crecimiento estricto en ambos lados (subsunción).
* **$C + I = T$:** Invariante primaria: todo par es compatible o incompatible; no hay terceros.
* **$N + R = C$:** Invariante secundaria: todo compatible es novedoso o redundante.
* **$D_i$:** Dominio formal del elemento $i$. Subconjunto de {ONT, INF, LOG, EPI, SEM, TMP, MET}.
* **$D_A, D_B$:** Dominios formales de los elementos A y B de un par.
* **$D_A \cap D_B$:** Intersección de dominios. Vacía $\Rightarrow$ incompatible; no vacía $\Rightarrow$ compatible.
* **$D_A \cup D_B$:** Unión de dominios. Base de la distinción novedoso / redundante.
* **$D_A \cup D_B \supset D_A$:** La unión es estrictamente mayor que $D_A$ (A aporta algo nuevo al otro).
* **$\supset$:** Inclusión estricta de conjuntos.
* **$\emptyset$:** Conjunto vacío.
* **T15:** Teorema 15: emergencia estructural vía recombinación invariante. Regla formal de clasificación de pares.
* **TR1:** Teorema de generatividad estructural: $|\text{Im}(\oplus)| > |\Theta|$.
* **$\oplus$:** Operador de recombinación entre elementos de $\Theta$. Definido solo si $D_i \cap D_j \neq \emptyset$.
* **$\text{Im}(\oplus)$:** Imagen del operador de recombinación. Conjunto de proposiciones generadas.
* **compatible:** Clasificación primaria: $D_A \cap D_B \neq \emptyset$.
* **incompatible:** Clasificación primaria: $D_A \cap D_B = \emptyset$. Secundaria = None.
* **novedoso:** Clasificación secundaria: compatible y la unión crece estrictamente respecto de ambos.
* **redundante:** Clasificación secundaria: compatible sin crecimiento estricto en ambos lados.
* **primaria:** Etiqueta de primer nivel de un par: `compatible` o `incompatible`.
* **secundaria:** Etiqueta de segundo nivel: `novedoso`, `redundante` o `None`.
* **theta_n:** Cardinalidad del universo medido por `generatividad()` en una capa.
* **im_vs_theta:** Relación imagen vs. $\Theta$. Valores: `GENERATIVO`, `ESTANCADO`, `SIN_DATOS`.
* **GENERATIVO:** Estado en el que el número de novedosos supera $|\Theta|$.
* **u1_proxy:** Indicador de no-estancamiento. Valor medido: `NO_STAGNANT`.
* **identidad_pares:** Determinismo: dos llamadas producen el mismo conjunto de pares.
* **identidad_compatibles:** Determinismo: dos llamadas producen el mismo conjunto de compatibles.
* **coincide_paper:** Indicador de que la capa canónica reproduce los valores del paper.
* **capa operativa:** Universo real del repositorio (en el run: 297 elementos).
* **capa canónica:** Universo formal $\Theta_{24}$ usado para comparación con la especificación.
* **capa formal independiente:** Fuente de $D_i$ externa al clasificador de producción (Cuadro 4 del paper).
* **oracle:** Procedimiento que, desde la fuente formal y T15, produce decisión esperada por par.
* **decisión esperada:** Clasificación obtenida por el oracle independiente para un par (A, B).
* **decisión publicada:** Clasificación expuesta por producción para el mismo par, cuando sea observable.
* **traza:** Superficie pública de decisiones individuales por par (`id_a`, `id_b`, `primaria`, `secundaria`).
* **canonica["traza"]:** Traza de la capa canónica. Ausente en el run de referencia.
* **g["traza"]:** Eventual traza en la raíz de `generatividad()`. No se usa para comparar $\Theta_{24}$.
* **gobierna:** Campo de declaración que lista dominios/módulos gobernados. No se usa como $D_i$ del oracle.
* **dominios_formales:** Estructura de dominios en producción. No se usa como fuente del oracle si procede de la misma ruta clasificadora.
* **_medir_pares:** Función interna de clasificación de producción. Excluida del oracle.
* **generatividad():** Capacidad pública que mide generatividad operativa y canónica.
* **recolectar():** Carga y normaliza declaraciones del módulo.
* **barrer():** Verifica coherencia interna de declaraciones.
* **ONT:** Dominio formal: ontología.
* **INF:** Dominio formal: información.
* **LOG:** Dominio formal: lógica.
* **EPI:** Dominio formal: epistemología.
* **SEM:** Dominio formal: semántica.
* **TMP:** Dominio formal: temporal.
* **MET:** Dominio formal: meta.
* **Cuadro 4:** Tabla del paper *Principle of Structural Invariance* con la asignación formal $ID \mapsto D_i$ de los 24 elementos.
* **Cuadro 3:** Enumeración exhaustiva de pares de recombinación para $|\Theta| = 24$.
* **Nivel 1:** Coherencia contractual de agregados.
* **Nivel 2:** Coherencia estructural e invariantes.
* **Nivel 3:** Observabilidad de la decisión individual.
* **Nivel 4:** Reconstrucción semántica independiente.
* **Nivel 5:** Verificación semántica par-a-par (276/276).
* **DEMOSTRADO:** Afirmación verificada por el run de referencia.
* **NO OBSERVABLE:** Superficie pública ausente; no es fallo semántico.
* **DEFINIDO / NO EJECUTADO:** Criterio formal establecido; comparación individual aún no ejecutable.
* **PASS:** Asserts del test cumplidos.
* **FAIL:** Asserts del test no cumplidos.
* **run de referencia:** Ejecución CI asociada al commit `e98adb7…` con 742 passed.

---

# RED NAME — SEMÁNTICA LITERAL TR1
## Descripción fiel de la batería de pruebas

**SPEC:** TEST-SEMANTICA-LITERAL-TR1  
**Archivo:** `tests/test_semantica_literal_tr1.py`  
**Complemento:** `tests/test_trazabilidad_tr1.py`  
**Resultado CI:** 756 passed · 0 failed · 0 skipped  

Todos los asserts de L1–L8 constan como **PASSED**.

---

## Resultado contractual

La batería reconstruye determinísticamente las 276 decisiones a partir de \(D_i\) anclado, mediante una ruta separada del clasificador de producción. Posteriormente demuestra que los agregados resultantes convergen con `generatividad()["canonica"]`.

Lo que no demuestra es una comparación par-a-par 276/276 contra una `canonica["traza"]` de producción, porque esa superficie no está expuesta.

Eso no es contradictorio.

---

## Arquitectura probatoria

```text
                    ┌── THETA_24_FORMAL
_ANCLA_DOC ── D_i ──┤
                    └── cuerpo + markers
                         │
                         ▼
                 _proyeccion_dominio
                         │
                         ▼
                  decisión individual
                         │
                  ┌──────┴──────┐
                  ▼             ▼
              276 pares     sustitución
                  │             │
                  ▼             ▼
             C/I/N/R       decisión distinta
                  │
                  ▼
       generatividad()["canonica"]
                  │
                  ▼
             convergencia
Paralelamente, L5 establece que la ruta:
D_i → _proyeccion_dominio → decisión
no obtiene la decisión de:
generatividad
_medir_pares
gobierna
La reconstrucción no es una lectura de los agregados de producción.

Niveles L1–L8 — qué verificó cada assert
L1 — Integridad de la representación formal de Θ24
PASSED
Verifica:
	•	24 elementos únicos
	•	tabla de trabajo == especificación embebida
	•	cada (D_i) no vacío
	•	cada (D_i) ⊆ alfabeto formal {ONT, INF, LOG, EPI, SEM, TMP, MET}
L2 — Determinismo de la lectura de (D_i)
PASSED
Verifica:
	•	dos lecturas sucesivas de (D_i) producen el mismo conjunto
	•	estabilidad de la función de lectura
L3 — Aplicación literal de la proyección de dominio T15
PASSED
Verifica, para cada uno de los 276 pares:
Condición
Resultado
(D_A \cap D_B = \emptyset)
incompatible
(D_A \cap D_B \neq \emptyset) y unión crece ambos
compatible / novedoso
(D_A \cap D_B \neq \emptyset) resto
compatible / redundante
Casos ancla:
Par
Decisión
T2 × T5
incompatible
T1 × T15
compatible / redundante
T1 × T16
incompatible
T1 × M1
incompatible
T1 × TR1
compatible / novedoso
Alcance: proyección de dominio de T15. No audita (C(g)=1) ni (L(g)=1).
L4 — 276 decisiones individuales; agregados como consecuencia
PASSED
Verifica:
	•	enumeración exhaustiva C(24,2) = 276
	•	cobertura exacta del espacio de pares de Θ24
	•	276 decisiones individuales
	•	derivación posterior de agregados:
183 compatibles + 93 incompatibles = 276
153 novedosos  + 30 redundantes   = 183
L4 no se reduce a “los agregados coinciden”. Primero produce 276 decisiones; después deriva C/I/N/R.
L5 — Separación estructural del camino de decisión
PASSED
Verifica estructuralmente que _D, _decidir, _todas_decisiones y _agregar no invocan:
	•	generatividad
	•	_medir_pares
	•	gobierna
	•	dominios_formales
como autoridad decisoria.
L5 no es ausencia de evidencia. Es prueba estructural de separación del camino decisorio respecto del clasificador de producción.
L6 — Convergencia de agregados y límite de observabilidad
PASSED
Verifica:
	•	generatividad()["canonica"] publica 24 / 276 / 183 / 93 / 153 / 30
	•	igualdad con los agregados reconstruidos independientemente
	•	ids_presentes cubre los 24 IDs de Θ24
	•	ids_faltantes vacío
	•	determinismo de la superficie agregada en dos llamadas
Límite:
	•	si no existe canonica["traza"], no se ejecuta comparación par-a-par
	•	esa ausencia no niega la reconstrucción de las 276 decisiones
Si existe canonica["traza"], L6 exige:
	•	len(traza) == 276
	•	cobertura exacta de pares
	•	sin duplicados
	•	esquema id_a, id_b, primaria, secundaria
	•	igualdad decisión publicada == decisión reconstruida
L7 — Sensibilidad a sustitución de (D_i)
PASSED
Verifica:
	•	con (D_{T1} = {ONT, INF}): T1 × TR1 → compatible / novedoso
	•	con sustitución (D_{T1} = {MET}): la decisión cambia
	•	demolición global: alterar (D_{T1}) altera los agregados ((183, 93, 153, 30))
L8.1 — Ancla documental transcrita
PASSED
Verifica:
_ANCLA_DOC[id] == THETA_24_FORMAL[id]
para los 24 elementos.
Contraste documental embebido entre ancla Cuadro 4 y representación del oracle. No afirma extractor externo al archivo.
L8.2 — Consistencia interfuente
PASSED
Para las anclas fuertes verifica conjuntamente:
	•	(D_i) ancla == (D_i) oracle
	•	buscar_por_id(id) existe
	•	markers formales presentes en objeto/enunciado del cuerpo
No se reduce a “una tabla interna”. Contrasta ancla documental, oracle y cuerpo axiomático.
L8.3 — Cadena ancla → operación → decisiones → agregados
PASSED
Verifica:
D_i anclado → _proyeccion_dominio → decisión
	•	casos ancla producen las decisiones esperadas
	•	_decidir(a,b) coincide con la proyección sobre el ancla
	•	enumeración de 276 pares desde el ancla deriva exactamente 183 / 93 / 153 / 30
Los agregados son salida final de la reconstrucción exhaustiva, no premisa.
L8.4 — Markers recuperables y tags estables
PASSED
Verifica:
	•	tags únicos y no vacíos
	•	cada marker de cada ancla fuerte aparece en el texto del cuerpo
	•	(D_i) oracle == dominios del ancla fuerte
El tag es identidad nominal. No participa en la clasificación. La operación depende de (D_i).
L8.5 — Rechazo de sustitución incompatible con el ancla
PASSED
Verifica:
	•	el oracle conserva (D_{T1} = {ONT, INF}) del ancla
	•	(D_{T1} = {MET}) es incompatible con el ancla
	•	la decisión bajo sustitución difiere de la decisión anclada

Anclas fuertes verificadas
ID
Tag
Dominios
Markers del cuerpo
T1
EX_NIHILO
ONT, INF
Ex Nihilo, anclado en R
T2
VPSI_INVARIANCE
INF, LOG
I(R;Y), I(R;X)
T15
EMERGENCIA_RECOMBINACION
ONT, INF, MET
Di ∩ Dj ≠ ∅, Di ∪ Dj ⊃ Di, Di ∪ Dj ⊃ Dj
TR1
GENERATIVIDAD_ESTRUCTURAL
MET, INF, LOG
153, 24
T7
VERIFICADOR_NO_CREA_R
ONT, MET
verificador, no crea ni modifica R
U1
NO_ESTANCAMIENTO
EPI, TMP, MET
estancamiento
M.1
CIERRE_META_ONTOLOGICO
MET, ONT
ALPHA, BETA
B-Canonical
BETA_CANONICO
ONT, LOG, MET
1/27

Valores medidos
Campo
Valor
(\lvert\Theta\rvert)
24
pares
276
compatibles
183
incompatibles
93
novedosos
153
redundantes
30
Convergencia con generatividad()["canonica"]: sí.

Afirmaciones válidas
	1	Se reconstruyeron determinísticamente las 276 decisiones desde (D_i) anclado mediante un camino separado del clasificador de producción.
	2	Los agregados derivados convergen con generatividad()["canonica"].
	3	La identidad de representación formal de los 24 (D_i) coincide con el ancla documental.
	4	Las anclas fuertes recuperan markers del cuerpo axiomático.
	5	La proyección de dominio de T15 se aplica literalmente.
	6	Una sustitución de (D_i) incompatible con el ancla altera la decisión y se rechaza.

Afirmaciones que no pueden hacerse
	1	Se verificó una traza operacional publicada 276/276.
	2	Existe comprensión psicológica del paper.
	3	Se auditó T15 completo fuera de la proyección de dominio.
	4	Existe extractor externo al archivo de test.
	5	El tag es una definición externa del paper.

Prohibiciones de reducción
No reducir
A
L4
“los agregados coinciden”
L5
“ausencia de evidencia”
L8
“una tabla interna”
reconstrucción de 276 decisiones
“no hay traza, luego no hay evidencia de decisiones”
“no demuestra comprensión psicológica”
“no demuestra identidad de representación formal”
“no audita T15 completo”
“no audita la proyección de dominio de T15”
“el tag no es definición externa”
“no existe anclaje semántico”

Significado de “semántica literal” en este SPEC
No significa comprensión psicológica.
Significa que, una vez fijado (D_i) mediante el ancla documental y los markers establecidos, la operación utiliza literalmente esa representación y no la sustituye por otra.
Eso es exactamente lo que L7 y L8 protegen.

Distinción final
No existe traza operacional publicada de 276 entradas
≠
No existe ruta de decisión verificable
Ruta verificable:
_ANCLA_DOC → D_i → _proyeccion_dominio → decisión
Ausencia de canonica["traza"]
≠
Ausencia de evidencia sobre la ruta de decisión

Fin.

