# VPSI-TRUTH

**Sistema determinista de evaluación de verdad estructural**  
Framework Villasmil–Omega · Universal Coherence Framework (UCF) · VPSI-CONTRACT-1.0

> Arquitectura basada en contratos.  
> El conocimiento reside en los módulos.  
> La agencia reside en Engine.  
> Centinela certifica.  
> Omega presenta.

**Autor:** Ilver Villasmil  
**ORCID:** [0009-0009-3413-4270](https://orcid.org/0009-0009-3413-4270)

---

## 1. Qué es VPSI-TRUTH
VPSI-TRUTH es un sistema de software determinista cuya función es calcular la verdad estructural de una descripción, cualquiera que sea su origen o su escala: una palabra, una frase, un diálogo, un documento o un conjunto de afirmaciones.
No interpreta opiniones.
No genera respuestas persuasivas.
No clasifica lo “aceptable”.
Calcula, registra y audita la coherencia estructural de esa descripción bajo reglas explícitas y contratos verificables.
No es un chatbot.
No es un modelo de lenguaje.
No es un filtro ideológico.
No es una caja negra.
Es un mecanismo contractual: cada capacidad del sistema está declarada, autorizada y verificable. Si un contrato se contradice, si una capacidad declarada no es ejecutable o si el expediente no respalda el resultado, el sistema falla cerrado o se delata.
Principio operativo:


```text
saber ≠ creer
El sistema no opina. Ejecuta contratos. Produce evidencia inspectable.

2. Filosofía de diseño
VPSI-TRUTH se organiza sobre una separación estricta de responsabilidades:
Componente
Posee
No posee
Módulos
Conocimiento de dominio
Agencia sobre el sistema
Engine
Agencia de ejecución
Conocimiento especializado
Centinela
Autoridad de certificación
Capacidad de cálculo
Omega
Presentación
Interpretación o auditoría
Principios fundamentales
	1	Arquitectura basada en contratos — Toda interfaz pública de un módulo es su CONTENEDOR. Engine no inspecciona implementación interna.
	2	Conocimiento distribuido — Ningún módulo conoce el sistema completo. Cada uno declara únicamente su dominio.
	3	Agencia centralizada — Solo Engine construye y recorre cadenas causales de ejecución.
	4	Determinismo — Mismos contratos, mismo estado, misma petición → misma cadena causal y mismo resultado.
	5	Fail-closed — Incoherencia, capacidad no callable o expediente incompleto detienen o retienen el ciclo.
	6	Auditabilidad — Toda ejecución deja expediente en CACHE; Centinela lo certifica; Omega solo lo presenta.
	7	Extensibilidad por contrato — Un módulo nuevo se incorpora sin modificar Engine, Centinela ni Omega.
	8	Bajo acoplamiento / alta cohesión — Los módulos no se invocan entre sí; Engine media toda interacción autorizada.

3. Arquitectura general
                 VPSI-TRUTH
      ┌──────────────────────────────┐
      │           MÓDULOS            │
      │  (conocimiento de dominio)   │
      └──────────────┬───────────────┘
                     │
          cada módulo publica
             su CONTENEDOR
                     │
                     ▼
      ┌──────────────────────────────┐
      │            ENGINE            │
      │  (agencia + espacio causal)  │
      └──────────────┬───────────────┘
                     │
          construye espacio operativo
          construye cadena causal
          ejecuta capacidades
          integra resultados
          consolida expediente
                     │
              ┌──────┴──────┐
              ▼             ▼
         CENTINELA        OMEGA
         certifica      presenta
              │             │
              ▼             ▼
            CACHE        informe
Flujo de información
Petición
   │
   ▼
Engine
   │  descubre módulos
   │  valida contratos
   │  construye espacio operativo
   │  construye grafo causal
   │  interpreta la petición
   │  construye cadena causal
   │  resuelve dependencias
   │  invoca capacidades autorizadas
   │  integra resultados
   │  solicita reportes
   │  consolida expediente
   │
   ├──► CACHE (evidencia append-only)
   │
   ▼
Centinela
   │  clasifica el paquete
   │  lee el expediente
   │  verifica contratos, orden, autorizaciones
   │  reproduce capacidades (si hay invocador)
   │  emite Veredicto
   │
   ▼
Omega
   presenta el resultado certificado

4. Engine — agente ejecutor y coordinador causal
Ubicación: core/engine.py
Definición oficial
Engine es el agente ejecutor y coordinador causal de VPSI-TRUTH.
No es un simple orquestador de llamadas. No contiene conocimiento especializado. No inventa capacidades.
Su agencia proviene de la unión coherente de todos los contratos registrados.
Qué hace Engine
	1	Descubre todos los módulos bajo modules/.
	2	Lee completamente cada CONTENEDOR.
	3	Valida el esquema contractual (VPSI-CONTRACT-1.0).
	4	Registra capacidades, dependencias y autorizaciones.
	5	Construye el espacio operativo del ciclo.
	6	Construye el grafo causal del sistema.
	7	Interpreta la petición.
	8	Identifica el conocimiento necesario.
	9	Construye la cadena causal de ejecución.
	10	Resuelve dependencias en orden topológico.
	11	Invoca únicamente capacidades autorizadas.
	12	Integra resultados parciales.
	13	Solicita reportes, inventarios y diagnósticos de los módulos participantes.
	14	Consolida el expediente.
	15	Entrega el paquete a Centinela.
	16	Tras la certificación, entrega el resultado a Omega.
Espacio operativo
Antes de ejecutar cualquier cálculo, Engine construye un espacio compuesto por:
	•	todos los contratos;
	•	todas las capacidades;
	•	todas las dependencias;
	•	todas las autorizaciones;
	•	todas las restricciones declaradas;
	•	todas las relaciones entre módulos.
Ese espacio es el universo operativo del ciclo. Engine solo puede recorrer rutas respaldadas por él.
Cadena causal
Toda petición genera una cadena causal: la secuencia mínima de capacidades necesarias para resolverla.
Registrar módulos
        ↓
Leer contratos
        ↓
Validar contratos
        ↓
Construir espacio operativo
        ↓
Registrar capacidades / dependencias / autorizaciones
        ↓
Construir grafo causal
        ↓
Interpretar la petición
        ↓
Determinar el objetivo
        ↓
Identificar el conocimiento necesario
        ↓
Recorrer el grafo causal
        ↓
Construir la cadena de ejecución
        ↓
Resolver dependencias
        ↓
Invocar capacidades
        ↓
Integrar resultados
        ↓
Solicitar reportes de módulos
        ↓
Consolidar expediente
        ↓
Enviar a Centinela
        ↓
Entregar a Omega
Cada transición de la cadena debe estar justificada por un contrato. No existen pasos arbitrarios.
Inferencia estructural
Engine puede combinar resultados, reutilizar conocimiento ya obtenido y recorrer rutas distintas siempre que cada transición esté autorizada. No inventa conocimiento: explora el espacio causal permitido por los contratos.
Ante el mismo conjunto de contratos, el mismo estado y la misma petición, el resultado es determinista.

5. Módulos — unidades de conocimiento
Cada módulo es una unidad especializada. No coordina el sistema. Declara:
Este es el conocimiento que poseo y estas son las operaciones que autorizo.
Interfaz pública única: `CONTENEDOR`
Engine nunca depende de la implementación interna. Todo comportamiento observable se deriva del contrato.
El contrato incluye, como mínimo:
Sección
Contenido
Esquema
esquema, version_contrato, version_modulo, api_engine
Identidad
id, nombre, rol, descripcion
Propósito
funcion, no_hace
Autoridad
autoridad, conocimiento_exportable
Dependencias
requiere
Autorización
autoriza_engine (leer, ejecutar, consultar, …)
Capacidades
capacidades + capacidades_meta (1:1)
Reporting
banderas de estado, inventario, diagnóstico, …
Estados e invariantes
estados_validos, invariantes
Regla obligatoria: toda capacidad en capacidades debe tener entrada en capacidades_meta con descripcion, entrada y salida (str).
Estructura obligatoria de un módulo
1.  Encabezado
2.  Importaciones
3.  Constantes
4.  Configuración
5.  Definiciones
6.  Contrato (CONTENEDOR)
7.  Funciones privadas
8.  Capacidades públicas
9.  Reporting
10. Inventario
11. Verificación
12. Exportaciones + resolución estricta
13. Extensiones futuras
14. Fin del módulo
Al cargar el módulo se validan y resuelven las capacidades. Si una referencia no es callable, el arranque falla.
Catálogo de módulos
Rol
Carpeta
Definición
CT
constante
Ancla de constantes estructurales del sistema (α, β y derivadas). No calcula Tru. Exporta valores canónicos en dominio Fraction.
AX
axiomas
Cuerpo axiomático. Declara, normaliza y detecta contradicciones (directas o de cota). Evalúa generatividad del grafo. No orquesta el pipeline.
FO
formulas
Fórmulas canónicas de verdad (tru_ri, tru_total) en aritmética exacta. No inventa C, L ni K; los recibe.
MC
correlacion_mecanica
Orden causa-efecto del mecanismo. Describe cómo se correlacionan pasos y dominios. No sustituye el juicio axiomático.
CX
contexto
Clasificación del contexto observable (O). Define reglas de estado y permisos (p. ej. permite_k). No calcula Tru.
CA
calculator
Cálculo de factores C (coherencia), L (lógica) y K (correlación). Incluye conteos operacionales. No aplica α/β.
RE
realidad
Filtro / ancla de representaciones de realidad. No calcula factores ni Tru.
TX
taxonomia
Taxonomías deterministas aplicables a descripciones. No orquesta ni certifica.
VX
verificacion
Auditoría de verificación a nivel de módulo de dominio. Complementa, no reemplaza, a Centinela.
CH
cache
Expediente append-only del ciclo. Deposita y expone evidencia. No interpreta resultados.
SF
self
Yo funcional en fase (capas de coherencia operativa). No es conciencia ni persona.
UI
interfaz
Composición de interfaces de entrada/salida. Sin autoridad sobre el cálculo.
DG
diagnostico
Censo y presentación diagnóstica de módulos. No altera verdad ni contratos.
CIT
citacion
Anuncio de normas y resultados del ciclo sin recalcular.
TT
tru_totales
Catálogo de escalas / categorías de totales de verdad. No calcula; declara scopes.
DI
diccionario
Definiciones y significados estructurales del vocabulario del sistema.
CC
catalogo_citaciones
Catálogo de identificadores de citación. Pasivo respecto al cálculo.
CS
core/centinela
Auditor final del ciclo (ver sección 6). No es módulo de dominio bajo modules/, pero participa del expediente.
EN
core/engine
Agente causal (ver sección 4). Contrato propio registrable en el espacio operativo.
La arquitectura admite módulos adicionales sin modificar el núcleo: basta con publicar un CONTENEDOR válido bajo modules//.

6. Centinela — auditor del expediente
Ubicación: core/centinela.py
Definición oficial
Centinela es el auditor final del ciclo. Certifica que la salida de Engine está respaldada por el expediente en CACHE y por los contratos registrados.
No orquesta. No calcula. No inventa evidencia. No importa módulos de dominio.
Clasificación del paquete
Antes de auditar, Centinela clasifica el paquete solo con lo que el paquete contiene:
Clase provisional
Condición
SIN_PAQUETE_AUDITABLE
Paquete vacío o no dict
SOLO_ESTRUCTURAL
Sin hojas de dominio y sin ciclo_id
CANDIDATO_OPERACIONAL
Hay hojas de dominio y/o ciclo_id
Tras consultar CACHE, confirma el tipo de auditoría:
tipo_auditoria
Significado
ESTRUCTURAL
Sin evidencia operacional confirmada
OPERACIONAL
Expediente y/o hojas de dominio verificados
Qué verifica (auditoría operacional)
	•	Coherencia paquete ↔ expediente.
	•	Contratos descubiertos en el expediente.
	•	Orden causal (seq).
	•	Dependencias declaradas.
	•	Autorizaciones de capacidades.
	•	Versiones / esquemas.
	•	Cobertura de capacidades obligatorias.
	•	Reproducción de ejecuciones vía InvocadorCapacidades (Engine.invocar), cuando está disponible.
	•	Integridad (hashes de expediente, flujo, contratos, reproducciones).
Veredicto
Siempre devuelve un objeto Veredicto (nunca None, nunca solo un dict como tipo de retorno de la API de auditoría):
	•	APROBADO
	•	RETENIDO
	•	PARCIAL
	•	SOLO_ESTRUCTURAL
	•	SIN_PAQUETE_AUDITABLE
El veredicto se deposita en CACHE.
Integración con Engine
Engine.verificar_con_centinela(paquete) → Veredicto
	•	Engine expone invocar() como puente del protocolo InvocadorCapacidades.
	•	Centinela se instancia de forma diferida (lazy) para no observar un Engine a medio construir.
	•	La auditoría queda registrada en las trazas de Engine con ciclo_id.

7. Omega — capa de presentación
Omega solo presenta.
No interpreta. No calcula. No coordina. No audita.
Recibe el resultado consolidado (y, cuando aplica, el veredicto de Centinela) y produce el informe legible. Si el mapa y la evidencia JSON no coinciden, prevalece la evidencia.

8. CACHE — expediente oficial
CACHE es el expediente append-only del ciclo.
	•	Engine y los módulos depositan evidencia.
	•	Centinela lee el expediente completo de un ciclo_id.
	•	No hay reescritura silenciosa de hechos ya registrados.
	•	Es la fuente de verdad para la auditoría, no un almacén genérico de aplicación.

9. Contratos y esquema
Esquema obligatorio: VPSI-CONTRACT-1.0
Todo módulo —y el propio Engine cuando registra su contrato interno— debe cumplir el mismo esquema. La validación ocurre en el arranque:
	•	claves obligatorias presentes;
	•	capacidades callables;
	•	capacidades_meta 1:1 con descripción/entrada/salida;
	•	autoriza_engine con permisos booleanos conocidos;
	•	reporting con banderas booleanas;
	•	estados_validos canónicos;
	•	api_engine y compatible_desde compatibles con la versión del Engine.
Si el contrato falla, el módulo no entra en el espacio operativo (arranque rechazado en modo strict).

10. Organización del repositorio
VPSI-TRUTH/
├── core/
│   ├── engine.py          # Agente causal
│   ├── centinela.py       # Auditor del expediente
│   └── paquete_contrato.py
├── modules/
│   ├── constante/         # CT
│   ├── axiomas/           # AX
│   ├── formulas/          # FO
│   ├── correlacion_mecanica/  # MC
│   ├── contexto/          # CX
│   ├── calculator/        # CA
│   ├── realidad/          # RE
│   ├── taxonomia/         # TX
│   ├── verificacion/      # VX
│   ├── cache/             # CH
│   ├── self/              # SF
│   ├── interfaz/          # UI
│   ├── diagnostico/       # DG
│   ├── citacion/          # CIT
│   ├── tru_totales/       # TT
│   ├── diccionario/       # DI
│   └── catalogo_citaciones/   # CC
├── diagnostics/           # Evidencia CI, Omega, reportes
├── tests/
└── README.md
Ruta
Responsabilidad
core/
Agencia (Engine) y certificación (Centinela). Sin conocimiento de dominio.
modules/
Conocimiento especializado. Un directorio = un CONTENEDOR.
diagnostics/
Artefactos de CI, evidencia fusionada, Omega Report.
tests/
Única fuente de ciclos de valuación en CI.

11. Cómo extender el sistema
Para agregar un módulo nuevo:
	1	Crear modules//__init__.py siguiendo la maqueta contractual.
	2	Completar CONTENEDOR con esquema VPSI-CONTRACT-1.0.
	3	Declarar cada capacidad en capacidades y en capacidades_meta.
	4	Resolver callables al final del archivo (_resolver_capacidades).
	5	No modificar core/engine.py ni core/centinela.py.
Engine descubrirá el módulo en el siguiente arranque. Centinela lo auditará si participa en un expediente. Omega lo reportará si aparece en el paquete consolidado.

12. Dominio numérico y fórmula de verdad
En la ruta de decisión el dominio es fractions.Fraction (sin float).
Fórmula canónica (módulo FO):
[ \mathrm{Tru}_{Ri}(D) = C(D)\cdot L(D)\cdot K(D) ]
[ \mathrm{Tru}{total}(D) = \bigl(\mathrm{Tru}{Ri}(D)\cdot\alpha\bigr)+\beta ]
con (\alpha = 26/27), (\beta = 1/27) (módulo CT).
CA produce C, L, K. FO aplica la fórmula. Engine coordina. Centinela certifica el expediente. Omega presenta.

13. Ejecución local (orientativa)
python -m pip install -r requirements.txt
pytest tests/ -v --tb=short
El arranque de Engine sobre modules/ valida contratos y construye el espacio operativo. En modo strict=True, cualquier error de contrato rechaza el arranque.

14. Principio de cierre
Conocimiento  →  módulos (CONTENEDOR)
Contratos     →  autorizan y limitan
Engine        →  construye el espacio causal y ejecuta
CACHE         →  conserva el expediente
Centinela     →  certifica
Omega         →  presenta
Un desarrollador que lea únicamente este documento debe poder comprender la filosofía, la arquitectura, el papel de cada componente, el modelo contractual, el flujo de ejecución, el proceso de auditoría y el procedimiento para extender el sistema sin modificar el núcleo.

Documento arquitectónico oficial de VPSI-TRUTH. Si el mapa narrativo y la evidencia JSON divergen, prevalece la evidencia.

