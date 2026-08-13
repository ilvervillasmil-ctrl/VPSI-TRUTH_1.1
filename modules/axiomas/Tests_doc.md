Esa comparación individual requiere una decisión obtenida por la vía operacional mapeable al mismo par.  
En este run esa superficie pública no está presente; el Nivel 5 queda definido, no ejecutado sobre 276/276.

Cuando exista `canonica["traza"]`, el TEST 3 ya exige:

- comparación **solo** contra la capa canónica (no contra traza operativa)
- `len(traza) == 276`
- cobertura exacta de Θ24
- esquema completo por entrada
- igualdad par-a-par de primaria y secundaria

Los agregados `183/93/153/30` pasan entonces a ser **consecuencia** de las 276 verificaciones individuales, no evidencia primaria.

---

## 4. Valores medidos en el run de referencia

### Capa operativa (cuerpo real del repo)

| Campo | Valor |
|-------|------:|
| `theta_n` | 297 |
| `pares_totales` | 43956 |
| `pares_compatibles` | 11506 |
| `pares_novedosos` | 7047 |
| `pares_redundantes` | 4459 |
| `pares_incompatibles` | 32450 |
| `im_vs_theta` | GENERATIVO |
| `u1_proxy` | NO_STAGNANT |
| `identidad_pares` | True |
| `identidad_compatibles` | True |

### Capa canónica TR1

| Campo | Valor |
|-------|------:|
| `theta_n` | 24 |
| `pares_totales` | 276 |
| `pares_compatibles` | 183 |
| `pares_novedosos` | 153 |
| `pares_redundantes` | 30 |
| `pares_incompatibles` | 93 |
| `im_vs_theta` | GENERATIVO |
| `identidad_pares` | True |
| `identidad_compatibles` | True |
| `coincide_paper` | True |
| `ids_presentes` | 24 |
| `ids_faltantes` | [] |

### Oracle independiente (TEST 3)

| Campo | Valor |
|-------|------:|
| pares enumerados | 276 |
| compatibles | 183 |
| incompatibles | 93 |
| novedosos | 153 |
| redundantes | 30 |
| igualdad de agregados con `canonica` | True |

---

## 5. Determinismo

Los tests TR1 son deterministas:

- no usan muestreo aleatorio
- no usan semillas variables
- enumeran el universo canónico completo (`C(24,2) = 276`)
- comparan valores publicados por `generatividad()` contra constantes formales y contra el oracle

En el run medido: `identidad_pares = True`, `identidad_compatibles = True`.

---

## 6. Separación de conceptos que no deben confundirse

| Concepto | Estado en este run |
|----------|--------------------|
| Observabilidad de traza pública | No existe (`canonica["traza"]` ausente) |
| Reconstrucción independiente de la decisión | Sí existe (Cuadro 4 + T15 → 276 decisiones) |
| Igualdad de agregados oracle ↔ `canonica` | Demostrada |
| Igualdad par-a-par oracle ↔ producción | Definida como Nivel 5; no ejecutada sin decisión obtenida comparable |
| Uso de `gobierna` o `dominios_formales` de producción como \(D_i\) | Excluido (circularidad de fuente) |
| Comparación de oracle Θ24 contra traza operativa | Excluida (universos distintos) |

---

## 7. Cadena contractual
