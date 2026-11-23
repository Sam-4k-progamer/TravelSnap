# Bitácora de acuerdos y avances

En esta bitácora llevamos el registro de las decisiones, avances y tareas de seguimiento de TravelSnap. La actualizamos cuando acordamos un cambio, cerramos una historia o aparece un nuevo pendiente. El backlog detallado está en [`01_BACKLOG_Y_EPICAS.md`](01_BACKLOG_Y_EPICAS.md) y la planeación de los sprints en [`05_ACTAS_SPRINT_PLANNING.md`](05_ACTAS_SPRINT_PLANNING.md).

## Integrantes

Trabajamos en el proyecto **Samuel Arias, Santiago Mejía, Juan Sebastián Molina y Andrés Velásquez**. Asignamos responsables al repartir las historias de cada sprint.

## Registro de acuerdos y avances

| Fecha | Tema | Acuerdo o avance | Seguimiento |
|---|---|---|---|
| 25 oct 2026 | Elección del proyecto | Decidimos continuar con TravelSnap, que ya tenía una primera versión, para aprovechar el tiempo y avanzar sobre el trabajo existente. | Acordado. |
| 25 oct 2026 | Entrega inicial del curso | Organizamos el README con integrantes, idea, épicas e historias, requerimientos funcionales/no funcionales e historias técnicas. También preparamos el modelo entidad-relación. | Documentado en README y diagramas. |
| 25 oct 2026 | Integrantes | Registramos a Samuel Arias, Santiago Mejía y Juan Sebastián Molina junto al responsable del proyecto, Andrés Velásquez. | Nombres incorporados en el README. |
| 26 oct 2026 | Modelo ER | Revisamos el diagrama y aceptamos los ajustes de presentación para que quedara más claro. | Diagrama editable conservado en `docs/diagrams/TravelSnap_ER.drawio`. |
| 27 oct 2026 | Posible intercambio de proyectos | Se planteó la posibilidad de trabajar sobre el proyecto de otro grupo. | Continuamos organizando TravelSnap; si el curso confirma un cambio, actualizamos este registro y el alcance. |
| 10 nov 2026 | Presentación del avance | Nos preparamos para explicar el repositorio, la estructura del programa y el estado de la base de datos. | Mantener disponibles el demo local, README, esquema SQL y diagrama ER. |
| 15–16 nov 2026 | Acceso al repositorio | Compartimos usuarios de GitHub para que los integrantes puedan colaborar. | Repositorio de trabajo: [Sam-4k-progamer/TravelSnap](https://github.com/Sam-4k-progamer/TravelSnap). Revisar acceso de cada integrante en GitHub. |
| 17 nov 2026 | Automatización y evidencias | Incorporamos al plan la ejecución automatizada de pruebas y la conservación de evidencia de los avances. | GitHub Actions ejecuta pruebas y sintaxis; sigue pendiente adjuntar evidencia de aceptación por historia y sprint. |
| 17–19 nov 2026 | Lista de tareas | Organizamos las tareas del producto y registramos el objetivo de contar con al menos 50. | Tenemos 52 issues de producto (#4–#55), vinculados con B01–B52 en el backlog. |
| 18–23 nov 2026 | Primeras tareas implementadas | Se reportó la implementación de tres tareas en otra versión del código y en otro puerto. | Antes de integrarlas, relacionamos cada una con su ID exacto y verificamos qué código debe conservarse. |
| 23 nov 2026 | Actualización de TravelSnap | Actualizamos la versión del proyecto con edición de publicaciones propias, documentación, pruebas y respaldo local. | Código subido a `main`; commit `379ef5a`. Las pruebas automatizadas pasan. |
| 23 nov 2026 | Gestión ágil | Organizamos épicas, historias de usuario y técnicas, criterios Gherkin, requerimientos, DoD y planes de sprint. | Documentos en [`docs/gestion-agil/`](./). CI comprobada en [GitHub Actions](https://github.com/Sam-4k-progamer/TravelSnap/actions). |

## Acuerdos vigentes

- El producto que estamos desarrollando es **TravelSnap**.
- Usamos el repositorio [Sam-4k-progamer/TravelSnap](https://github.com/Sam-4k-progamer/TravelSnap) y dejamos la rama `main` como rama de entrega.
- Mantenemos un backlog de 52 objetivos, con épicas, prioridades, estado y criterios Gherkin.
- Antes de cerrar una historia, comprobamos sus criterios, actualizamos la documentación y enlazamos la evidencia disponible.
- Las reuniones de Sprint Planning dejan un Sprint Goal y el Sprint Backlog que vamos a trabajar.

## Seguimiento

- Asociar las tres tareas implementadas en la versión/puerto anterior con sus IDs y decidir si integramos ese código o conservamos la implementación actual.
- Completar en cada acta la fecha, capacidad, estimaciones y responsables definidos para el sprint.
- Adjuntar evidencia de aceptación por historia, además del resultado automático de CI.
- Confirmar el acceso al repositorio de los cuatro integrantes.
- Si se confirma el intercambio de proyecto, registrar la decisión, el nuevo alcance y los cambios al backlog antes de continuar.
