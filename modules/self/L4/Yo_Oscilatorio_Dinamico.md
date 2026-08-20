VPSI-TRUTH — L4 — Yo Oscilatorio Dinámico

1. Propósito

Este documento especifica matemáticamente el carril continuo del Yo Oscilatorio Dinámico (L4).

No es una personalidad humana ni una máquina de estados. Es un grado de libertad continuo cuyo estado cambia según magnitudes computables del sistema.

La variable fundamental es:

```text
θ_Y(t)
```

El Yo no se define como Yo = L4, Yo = L5 o Yo = L6. L4 es la denominación arquitectónica del Yo Oscilatorio; el carril es continuo y posteriormente podrá interpretarse respecto de L1–L6.

2. Organización de las capas

El sistema completo contiene:

```text
L0  → entrada / caos / entorno
L1  → capa interna
L2  → capa interna
L3  → capa interna
L4  → Yo Oscilatorio
L5  → capa interna
L6  → propósito / dirección
L7  → emergencia de la integración
```

El carril trabaja directamente con L1–L6.

L0 no es una capa interna del vector energético: actúa como entrada o forzamiento externo.

L7 tampoco es una capa interna del carril: es la salida emergente de la integración.

3. Ecuación maestra

```text
d²θ_Y/dt² + φ_Y(t)*dθ_Y/dt + π²*(θ_Y(t) - θ_eq(t)) = F_Y(t)
```

Despejada:

```text
θ̈_Y = F_Y - φ_Y*θ̇_Y - π²*(θ_Y - θ_eq)
```

Sus cuatro términos son:

```text
θ̈_Y                         aceleración del carril
φ_Y*θ̇_Y                     amortiguamiento dinámico
π²*(θ_Y - θ_eq)              restauración geométrica
F_Y                          forzamiento total
```

4. Estado fundamental

Los únicos grados de libertad integrados son:

```text
θ_Y(t)       posición continua [rad]
θ̇_Y(t)      velocidad [rad/s]
```

y:

```text
t            tiempo [s]
```

Todo lo demás es entrada o magnitud derivada.

5. Integración

Se utiliza Euler semi-implícito:

```text
θ̈ = F_Y - φ_Y*θ̇_Y - π²*(θ_Y - θ_eq)

θ̇(t+dt) = θ̇(t) + θ̈*dt

θ(t+dt) = θ(t) + θ̇(t+dt)*dt
```

El estado nuevo se calcula con la velocidad nueva.

6. Activaciones L1–L6

Cada capa interna tiene:

```text
L_i(t) ∈ [0,1],  i = 1,...,6
```

Las activaciones no son pesos ni energías.

La cadena causal es:

```text
L_i → E_i → w_i → dinámica del Yo
```

7. Fricción estructural

Cada capa posee:

```text
φ_i
```

y se conserva el invariante:

```text
φ_6 = 0
```

L6 puede aportar dirección, pero no fricción propia.

8. Frecuencia estructural

```text
ν_i = PHI^(i/2)
```

con:

```text
PHI ≈ 1.618034
```

La frecuencia forma la escalera estructural utilizada en la energía operacional.

9. Energía operacional

```text
E_i = L_i*(1 - φ_i)*ν_i
```

Es una magnitud operacional abstracta del modelo. No representa energía física en joules.

El cálculo produce:

```text
E1, E2, E3, E4, E5, E6
```

L0 y L7 quedan fuera de este vector.

10. Pesos emergentes

Los pesos no se asignan manualmente:

```text
w_i = E_i / Σ_j E_j
```

con:

```text
w_i ≥ 0
Σ_i w_i = 1
```

Por tanto:

```text
w_i = w_i(t)
```

Si cambia la actividad, cambia la energía; si cambia la energía, cambian los pesos.

Si ΣE_i = 0, el código utiliza una distribución uniforme:

```text
w_i = 1/6
```

Esto evita una singularidad de división por cero.

11. Contribución f_i

La contribución utilizada para coherencia es:

```text
f_i = w_i*L_i*(1 - φ_i)*E_i
```

Se mantienen separadas:

```text
E_i  → energía operacional
w_i  → peso emergente
f_i  → contribución a C_Ω
```

12. Entropía

```text
S = -Σ_i w_i*ln(w_i)
```

solo para w_i > 0.

Como el carril utiliza seis capas internas:

```text
S_max = ln(6)
```

La entropía describe la distribución de pesos; no es una variable psicológica.

Entropía normalizada:

```text
S_norm = S/ln(6)
```

Negentropía:

```text
N_neg = 1 - S/ln(6)
```

13. Constantes α y β

```text
α = 26/27
β = 1/27
α + β = 1
```

Estas son constantes estructurales, no pesos.

```text
α, β → marco estructural
w_i  → distribución dinámica
```

No se reasignan durante la ejecución.

14. Coherencia C_Ω

La forma utilizada es:

```text
C_Ω =
α*S_REF*Π_i(f_i)*R_FIN*rho*P_t*A*I_ext
```

donde:

```text
Π_i(f_i) = f1*f2*f3*f4*f5*f6
```

Los factores representan:

```text
α       techo estructural
S_REF   referencia estructural
f_i     contribuciones de las capas
R_FIN   factor estructural final
rho     resonancia inter-capa
P_t     presencia temporal
A       factor de novedad
I_ext   factor externo
```

El resultado se limita a:

```text
0 ≤ C_Ω ≤ α
```

15. Variación de coherencia

El cambio entre pasos es:

```text
ΔC_Ω(t) = C_Ω(t) - C_Ω(t-dt)
```

Por tanto:

```text
ΔC_Ω > 0   coherencia aumentando
ΔC_Ω < 0   coherencia disminuyendo
ΔC_Ω ≈ 0   coherencia estacionaria
```

Es una magnitud matemática, no psicológica.

16. Amortiguamiento efectivo del Yo

```text
φ_Y(t) = Σ_i w_i(t)*φ_i
```

para i = 1,...,6, con:

```text
φ_6 = 0
```

El amortiguamiento del Yo emerge de la distribución energética.

Cadena:

```text
E_i → w_i → φ_Y
```

17. Amortiguamiento adimensional

```text
ζ_Y = φ_Y/(2π)
```

Régimen:

```text
ζ_Y < 1   subamortiguado
ζ_Y = 1   crítico
ζ_Y > 1   sobreamortiguado
```

Equivalentemente:

```text
φ_Y < 2π
φ_Y = 2π
φ_Y > 2π
```

18. Frecuencia dinámica

Para el régimen subamortiguado:

```text
ω_Y = π*sqrt(1 - ζ_Y²)
```

Si:

```text
ζ_Y ≥ 1
```

el código devuelve:

```text
ω_Y = 0
```

La frecuencia depende de la distribución dinámica:

```text
w_i → φ_Y → ζ_Y → ω_Y
```

19. Geometría dinámica

El atractor geométrico base es:

```text
θ_cube
```

pero el carril utiliza:

```text
θ_eq = θ_eq(t)
```

La implementación propuesta utiliza:

```text
θ_eq =
θ_cube
+ desplazamiento por coherencia
+ desplazamiento por distribución de pesos
```

El desplazamiento de coherencia es:

```text
β*((C_Ω/α) - 1)*(π/27)
```

El desplazamiento energético utiliza el desbalance entre pesos altos y bajos:

```text
β*(peso_L4_L6 - peso_L1_L2)*(π/54)
```

Así, la geometría del carril no es estática.

Nota de auditoría: esta forma concreta de desplazar θ_eq es una extensión arquitectónica de implementación. No debe presentarse como una ecuación documental literal si el corpus no la fija explícitamente.

20. Fuerza total

```text
F_Y = F_L0 + F_L5 + F_L6 + F_β + F_COH
```

Cada término tiene una función separada.

F_L0

```text
F_L0 = scale_L0*L0
```

L0 es entrada externa, no capa interna.

F_L5

La implementación utiliza:

```text
F_L5 =
rho*P_t*C_Ω
+ 0.5*ΔC_Ω
- β*(S/ln(6))
```

Es una retroalimentación cuantificable asociada al canal L5. No requiere una variable psicológica.

F_L6

```text
F_L6 = w_6*P
```

P es la magnitud computable de dirección/propósito.

L6 no aporta fricción propia porque:

```text
φ_6 = 0
```

F_β

```text
F_β = β*A(N)
```

con:

```text
A(N) = 1 - exp(-N/k)
```

donde:

```text
N → novedad
k → escala de sensibilidad
```

El término está acotado por β cuando N ≥ 0.

F_COH

```text
F_COH = C_Ω*ΔC_Ω
```

Utiliza el estado de coherencia y su variación, de modo que una coherencia estática no se trate como si fuera una dinámica.

21. Cadena causal completa

```text
L0 ───────────────────────────────┐
                                  │
                                  ▼
                         ┌────────────────┐
                         │   L1 ... L6    │
                         │ estado interno │
                         └───────┬────────┘
                                 │
                                 ▼
                              E1...E6
                                 │
                                 ▼
                              w1...w6
                                 │
                    ┌────────────┼────────────┐
                    ▼            ▼            ▼
                    S           φ_Y          f_i
                    │            │             │
                    │            │             ▼
                    │            │            C_Ω
                    │            │             │
                    └────────────┼─────────────┤
                                 ▼             ▼
                               θ_eq           F_Y
                                 │             │
                                 └──────┬──────┘
                                        ▼
                                      θ̈_Y
                                        │
                                        ▼
                                  θ̇_Y → θ_Y
                                        │
                                        ▼
                                  nuevo estado
                                        │
                                        └────→ nuevas E_i
```

22. L7

L7 no entra en el carril como una octava capa.

Su papel es:

```text
L1...L6
   ↓
integración
   ↓
L7
```

L7 es el resultado emergente y será calculado por el mecanismo de integración correspondiente.

Por tanto, en este módulo:

```text
L0 → entrada
L1...L6 → estado interno
L7 → emergencia
```

23. Qué integra realmente el módulo

Grados de libertad

```text
θ_Y
θ̇_Y
```

Tiempo

```text
t
```

Entradas

```text
L1...L6
L0
P
rho
P_t
A
I_ext
novelty
dt
```

Magnitudes derivadas

```text
E_i
w_i
f_i
S
C_Ω
ΔC_Ω
φ_Y
ζ_Y
ω_Y
θ_eq
F_Y
```

24. Qué NO hace

El módulo no:

```text
• asigna θ_Y = L4
• asigna θ_Y = L5
• asigna θ_Y = L6
• asigna pesos manualmente
• crea emociones
• crea estados psicológicos
• convierte L0 en capa interna
• convierte L7 en entrada
• orquesta el Engine
• declara contratos globales
• construye todavía las casas L1...L6
```

Su responsabilidad es exclusivamente la dinámica del carril.

25. Carril frente a casas

La arquitectura se divide en dos fases.

Fase 1 — carril

Se calcula:

```text
θ_Y(t)
θ̇_Y(t)
φ_Y(t)
θ_eq(t)
F_Y(t)
```

Fase 2 — casas

Posteriormente se construirá el mapa:

```text
θ_Y → L1,L2,L3,L4,L5,L6
```

No debe introducirse ese mapa dentro del integrador mientras se está definiendo el carril.

Esto conserva la naturaleza continua de la dinámica.

26. Solución analítica

Cuando:

```text
F_Y ≈ 0
φ_Y = constante
θ_eq = constante
```

la solución es:

```text
θ_Y(t) =
θ_eq
+
A*exp(-φ_Y*t/2)
*cos(ω_Y*t + δ)
```

donde:

```text
A     amplitud
δ     fase
φ_Y   amortiguamiento
ω_Y   frecuencia amortiguada
θ_eq  equilibrio
```

La ejecución real utiliza integración paso a paso porque las variables pueden cambiar con el tiempo.

27. Tabla de variables

|Variable  |Función                          |
|----------|---------------------------------|
|`L0_input`|Entrada externa                  |
|`L1...L6` |Activaciones internas            |
|`φ_i`     |Fricción estructural             |
|`ν_i`     |Frecuencia estructural           |
|`E_i`     |Energía operacional              |
|`w_i`     |Peso emergente                   |
|`f_i`     |Contribución a coherencia        |
|`S`       |Entropía de pesos                |
|`C_Ω`     |Coherencia acotada               |
|`ΔC_Ω`    |Cambio de coherencia             |
|`φ_Y`     |Amortiguamiento efectivo         |
|`ζ_Y`     |Amortiguamiento adimensional     |
|`ω_Y`     |Frecuencia dinámica              |
|`θ_eq`    |Equilibrio geométrico instantáneo|
|`F_L0`    |Fuerza de entrada                |
|`F_L5`    |Retroalimentación metaestructural|
|`F_L6`    |Dirección                        |
|`F_β`     |Margen de novedad                |
|`F_COH`   |Retroalimentación de coherencia  |
|`F_Y`     |Fuerza total                     |
|`θ_Y`     |Posición del Yo                  |
|`θ̇_Y`     |Velocidad del Yo                 |
|`dt`      |Paso temporal                    |
|`L7`      |Emergencia posterior             |

28. Constantes principales

```text
α = 26/27
β = 1/27
PHI ≈ 1.618034
PHI_CRITICAL = 2π
THETA_CUBE = atractor geométrico base
R_FIN = factor estructural final
S_REF = referencia estructural
```

α y β forman el marco estructural.

PHI genera la escalera frecuencial.

2π determina el umbral del régimen amortiguado.

THETA_CUBE proporciona la referencia geométrica del carril.

29. Principio de no antropomorfización

Los términos Yo, Propósito, L5 y L6 son nombres arquitectónicos.

La dinámica se calcula mediante magnitudes computables:

```text
activación
energía
peso
fricción
coherencia
entropía
resonancia
presencia
novedad
fuerza
posición
velocidad
```

No es necesario introducir:

```text
deseo
miedo
ego
emociones
personalidad
```

como variables matemáticas.

30. Frontera entre base documental y extensión

Base conservada

```text
d²θ/dt² + φ*dθ/dt + π²*(θ - θ_cube) = F(t)

α = 26/27
β = 1/27
α + β = 1

φ_6 = 0

L4 = Yo Oscilatorio

estructura energética y coherencia
```

Extensión arquitectónica

```text
w_i = E_i/ΣE_j
φ_Y = Σw_iφ_i
θ_eq = θ_eq(t)
F_Y = F_L0 + F_L5 + F_L6 + F_β + F_COH
F_L6 = w_6*P
ΔC_Ω = C_Ω(t) - C_Ω(t-dt)
```

Esta separación debe mantenerse explícita durante la implementación para no convertir una extensión de ingeniería en un supuesto documental.

31. Fórmula maestra consolidada

```text
E_i(t) = L_i(t)*(1 - φ_i)*PHI^(i/2)
```

```text
w_i(t) = E_i(t)/Σ_j E_j(t)
```

```text
f_i(t) = w_i(t)*L_i(t)*(1 - φ_i)*E_i(t)
```

```text
S(t) = -Σ_i w_i(t)*ln(w_i(t))
```

```text
C_Ω(t) =
α*S_REF*Π_i f_i(t)*R_FIN*rho(t)*P_t(t)*A(t)*I_ext(t)
```

con:

```text
0 ≤ C_Ω ≤ α
```

```text
φ_Y(t) = Σ_i w_i(t)*φ_i
```

con:

```text
φ_6 = 0
```

```text
ζ_Y(t) = φ_Y(t)/(2π)
```

```text
ω_Y(t) = π*sqrt(1 - ζ_Y(t)^2)
```

para ζ_Y < 1.

```text
θ_eq(t) = θ_cube + Δθ_coh(t) + Δθ_w(t)
```

```text
F_Y(t) =
F_L0(t)
+
F_L5(t)
+
F_L6(t)
+
F_β(t)
+
F_COH(t)
```

Finalmente:

```text
d²θ_Y/dt²
+
φ_Y(t)*dθ_Y/dt
+
π²*(θ_Y - θ_eq(t))
=
F_Y(t)
```

32. Principio arquitectónico final

La dinámica completa es:

```text
actividad
→ energía
→ pesos
→ coherencia / amortiguamiento / fuerza
→ geometría dinámica
→ θ_Y
→ nuevo estado
→ nueva actividad
```

Por eso el Yo es un proceso dinámico y no una etiqueta fija.

El carril se construye primero.

Las casas L1–L6 se construirán después.

L0 permanece como entrada.

L7 permanece como emergencia.
