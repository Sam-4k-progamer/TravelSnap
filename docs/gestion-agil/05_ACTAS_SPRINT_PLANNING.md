# Actas de Sprint Planning (propuesta)

## Nota de honestidad sobre el registro

El chat de WhatsApp no contiene una reunión formal de Sprint Planning ni acuerdos de fechas, duración, capacidad, estimaciones, responsables o Sprint Goals. Las siguientes actas son **propuestas de planificación preparadas a partir del estado del producto y los pedidos que aparecen en el chat**; no son actas de reuniones que hayan ocurrido. Deben revisarse con el equipo y el profesor antes de presentarlas como acuerdos oficiales.

El chat sí registra que el equipo eligió continuar con TravelSnap por falta de tiempo; que había una posibilidad de intercambiar proyectos pero no se registra la decisión final del profesor; que se pidió un mínimo de 50 tareas; y que se solicitó automatización y evidencias. También se dice que Andrés había implementado “las tres primeras tareas” con otro código/puerto, pero los audios e imágenes omitidos no permiten identificar sus IDs. Por eso no se marca ningún B01–B03 como terminado por ese mensaje. El estado del código actual está en el backlog.

**Integrantes nombrados:** Samuel Arias, Santiago Mejía, Juan Sebastián Molina y Andrés Velásquez. La asistencia efectiva a estas planificaciones no está confirmada. Responsable de cada tarea: por asignar en equipo.

## Acta propuesta — Sprint 1: Base verificable

- **Fecha:** por acordar. **Duración/capacidad:** por acordar. **Participantes esperados:** equipo TravelSnap. **Facilitador:** por definir.
- **Sprint Goal:** dejar documentado y ejecutable el núcleo técnico para que el equipo pueda demostrar cómo se estructura TravelSnap y cómo inicia sesión.
- **Criterio de éxito del objetivo:** requisitos, actores, historias, prioridades, ER y arquitectura coherentes; el servidor local inicia; registro/login y persistencia pasan las verificaciones existentes.
- **Sprint Backlog completo:**
  - Producto: B01, B02, B03, B04, B05, B06, B07, B12, B13, B15, B16, B21, B22, B23, B24, B38, B39.
  - Técnico: HT-01, HT-02, HT-03, HT-04, HT-05, HT-06, HT-08, HT-19.
- **Dependencias/riesgos:** confirmar si existe una permuta oficial de proyecto; el chat deja este punto abierto. Definir quién revisa requisitos/ER. Sesión HTTPS de producción queda fuera del objetivo local.
- **Estado actual:** muchos criterios ya están hechos en la copia; revisar la columna Estado antes de trasladar las tareas al sprint real y no reabrir trabajo completado.
- **Decisiones por registrar en la reunión real:** duración, estimaciones, responsables y qué evidencia acepta el profesor.

## Acta propuesta — Sprint 2: Comunidad y contenido

- **Fecha:** por acordar. **Duración/capacidad:** por acordar. **Participantes esperados:** equipo TravelSnap. **Facilitador:** por definir.
- **Sprint Goal:** permitir que un viajero mantenga su perfil y administre publicaciones e interacciones de forma segura.
- **Criterio de éxito del objetivo:** creación/lectura/edición/borrado de contenido propio; comentarios, likes y follows coherentes; operaciones ajenas bloqueadas; navegación a perfil y feed definida.
- **Sprint Backlog completo:**
  - Producto: B08, B09, B10, B11, B14, B17, B18, B19, B20, B25, B26, B27, B28, B29, B30, B32, B37, B40.
  - Técnico: HT-07.
- **Dependencias/riesgos:** definir qué campos completan el perfil y quién puede ver perfiles ajenos; definir si las fotografías continúan por URL mientras se decide un almacenamiento.
- **Estado actual:** varias historias de este sprint ya están implementadas; las de perfil completo, sesión robusta y permisos exhaustivos son parciales. No planificar de nuevo lo que el código ya cumple.
- **Decisiones por registrar:** campos de perfil, visibilidad, regla de orden del feed y estimaciones.

## Acta propuesta — Sprint 3: Descubrimiento, pruebas y evidencia automatizada

- **Fecha:** por acordar. **Duración/capacidad:** por acordar. **Participantes esperados:** equipo TravelSnap. **Facilitador:** por definir.
- **Sprint Goal:** facilitar encontrar contenido y dar evidencia repetible de calidad antes de presentar el avance.
- **Criterio de éxito del objetivo:** vista de detalle y feed paginado/personalizado o alcance reducido aprobado; suite automatizada cubre integración y acceso no autorizado; CI informa resultado; cada historia cerrada tiene evidencia enlazada.
- **Sprint Backlog completo:**
  - Producto: B31, B33, B34, B35, B36, B41, B42, B43, B44, B45.
  - Técnico: HT-09, HT-10, HT-11, HT-12, HT-13, HT-14, HT-15, HT-20, HT-21.
- **Dependencias/riesgos:** B31 requiere escoger proveedor y límites de archivo; B44 requiere definir volumen y umbrales; B45 requiere acordar navegadores. La automatización y evidencias fueron mencionadas explícitamente en el chat, pero su formato final no está acordado.
- **Decisiones por registrar:** proveedor de imágenes (o mantener URL), umbrales de rendimiento, navegador/móvil objetivo y ubicación de evidencias.

## Acta propuesta — Sprint 4: Respaldo y entrega operativa

- **Fecha:** por acordar. **Duración/capacidad:** por acordar. **Participantes esperados:** equipo TravelSnap. **Facilitador:** por definir.
- **Sprint Goal:** dejar definido cómo se recupera, publica y mantiene TravelSnap sin exponer información privada.
- **Criterio de éxito del objetivo:** respaldo restaurado en prueba; logging y alertas acordados; despliegue reproducible con HTTPS y dominio configurado si el equipo dispone de infraestructura; guía técnica actualizada.
- **Sprint Backlog completo:**
  - Producto: B46, B47, B48, B49, B50, B51, B52.
  - Técnico: HT-16, HT-17, HT-18, HT-22.
- **Dependencias/riesgos:** B47–B49 dependen de hosting, dominio, credenciales y presupuesto aprobados. No comprometer despliegue si el equipo no cuenta con ellos. La copia actual es local y SQLite.
- **Decisiones por registrar:** proveedor/plan de alojamiento, responsable operativo, periodicidad de respaldos, ubicación externa segura y política de mantenimiento.

## Plantilla para cerrar el acta después de reunirse

Completar sin borrar la planificación propuesta: fecha/hora real; participantes presentes; Sprint Goal aprobado; Sprint Backlog final (IDs retirados/añadidos y motivo); estimación/capacidad acordadas; dependencias; responsable por tarea si el equipo lo acuerda; evidencia al cierre; impedimentos y decisión del profesor respecto a eventual intercambio de proyecto.
