Axiomas — Guía para desarrolladores

¿Qué es este módulo?

El módulo Axiomas es el repositorio estructural de los axiomas declarados dentro del sistema VPSI-TRUTH.

Su responsabilidad es registrar, organizar, consultar y verificar los axiomas que forman parte del conocimiento estructural del sistema.

No interpreta los axiomas ni calcula métricas de verdad; únicamente administra y expone el conocimiento axiomático mediante un contrato estable.

⸻

¿Qué es un axioma?

Un axioma es una afirmación aceptada como fundamento del sistema.

Los demás módulos pueden utilizar los axiomas como base para sus procesos de razonamiento, auditoría o validación.

⸻

Responsabilidades del módulo

El módulo puede:

* Registrar axiomas.
* Organizar declaraciones.
* Filtrar por dominio.
* Buscar por identificador.
* Generar inventarios.
* Generar reportes.
* Ejecutar diagnósticos.
* Verificar consistencia estructural.
* Recolectar declaraciones desde distintas fuentes.

El módulo no debe:

* Modificar la lógica del Engine.
* Calcular Tru.
* Interpretar resultados.
* Tomar decisiones de auditoría.
* Alterar otros módulos.

⸻

Contrato de capacidades

Toda capacidad publicada en:

CONTENEDOR["capacidades"]

debe tener una entrada correspondiente en:

CONTENEDOR["capacidades_meta"]

La relación es obligatoriamente 1:1.

Ejemplo:

capacidades
    verificar
    barrer
    reporte
↓
capacidades_meta
    verificar
    barrer
    reporte

Cada entrada de capacidades_meta debe contener:

* descripcion
* entrada
* salida

Todos estos campos deben ser cadenas (str).

⸻

Regla de desarrollo

Cada vez que se agregue una nueva capacidad al módulo, deberá agregarse simultáneamente su definición en capacidades_meta.

No se aceptarán capacidades sin metadatos.

⸻

Objetivo

El contrato permite que el Engine conozca completamente las capacidades del módulo sin inspeccionar el código fuente.

Esto facilita:

* validación automática,
* documentación automática,
* integración entre módulos,
* auditoría estructural,
* mantenimiento del sistema.

⸻

Principio

Las capacidades describen lo que el módulo puede hacer.

Las capacidades_meta describen el contrato de cada capacidad.

Ambas forman una única interfaz pública y deben mantenerse siempre sincronizadas.
