# Actas de Sprint Planning

Organizamos el trabajo en cuatro sprints para avanzar desde la base del sistema hasta la calidad y la operación. Cada acta incluye el Sprint Goal, el criterio para revisar el objetivo, y el Sprint Backlog de producto y técnico. En la reunión de planeación completamos fecha, capacidad, estimaciones y responsables con los acuerdos del equipo.

**Equipo TravelSnap:** Samuel Arias, Santiago Mejía, Juan Sebastián Molina y Andrés Velásquez.

## Sprint 1 — Base verificable

- **Fecha:** completar en la planeación. **Duración/capacidad:** registrar lo acordado. **Participantes:** equipo TravelSnap.
- **Sprint Goal:** dejar documentado y ejecutable el núcleo técnico para que el equipo pueda demostrar cómo se estructura TravelSnap y cómo inicia sesión.
- **Criterio de éxito del objetivo:** requisitos, actores, historias, prioridades, ER y arquitectura coherentes; el servidor local inicia; registro/login y persistencia pasan las verificaciones existentes.
- **Sprint Backlog completo:**
  - Producto: B01, B02, B03, B04, B05, B06, B07, B12, B13, B15, B16, B21, B22, B23, B24, B38, B39.
  - Técnico: HT-01, HT-02, HT-03, HT-04, HT-05, HT-06, HT-08, HT-19.
- **Dependencias/riesgos:** revisar coherencia entre requisitos, ER y código. La sesión HTTPS de producción queda fuera del objetivo local.
- **Preparación:** revisar la columna Estado y seleccionar solo el trabajo que siga pendiente al iniciar el sprint.
- **Acuerdos de planeación:** registrar duración, estimaciones, responsables y evidencia de aceptación.

## Sprint 2 — Comunidad y contenido

- **Fecha:** completar en la planeación. **Duración/capacidad:** registrar lo acordado. **Participantes:** equipo TravelSnap.
- **Sprint Goal:** permitir que un viajero mantenga su perfil y administre publicaciones e interacciones de forma segura.
- **Criterio de éxito del objetivo:** creación/lectura/edición/borrado de contenido propio; comentarios, likes y follows coherentes; operaciones ajenas bloqueadas; navegación a perfil y feed definida.
- **Sprint Backlog completo:**
  - Producto: B08, B09, B10, B11, B14, B17, B18, B19, B20, B25, B26, B27, B28, B29, B30, B32, B37, B40.
  - Técnico: HT-07.
- **Dependencias/riesgos:** definir qué campos completan el perfil y quién puede ver perfiles ajenos; definir si las fotografías continúan por URL mientras se decide un almacenamiento.
- **Preparación:** revisar el estado de las historias implementadas y seleccionar el trabajo pendiente.
- **Acuerdos de planeación:** definir campos del perfil, visibilidad, orden del feed y estimaciones.

## Sprint 3 — Descubrimiento, pruebas y evidencia automatizada

- **Fecha:** completar en la planeación. **Duración/capacidad:** registrar lo acordado. **Participantes:** equipo TravelSnap.
- **Sprint Goal:** facilitar encontrar contenido y dar evidencia repetible de calidad antes de presentar el avance.
- **Criterio de éxito del objetivo:** vista de detalle y feed paginado/personalizado o alcance reducido aprobado; suite automatizada cubre integración y acceso no autorizado; CI informa resultado; cada historia cerrada tiene evidencia enlazada.
- **Sprint Backlog completo:**
  - Producto: B31, B33, B34, B35, B36, B41, B42, B43, B44, B45.
  - Técnico: HT-09, HT-10, HT-11, HT-12, HT-13, HT-14, HT-15, HT-20, HT-21.
- **Dependencias/riesgos:** B31 requiere escoger proveedor y límites de archivo; B44 requiere definir volumen y umbrales; B45 requiere acordar navegadores.
- **Acuerdos de planeación:** definir proveedor de imágenes (o mantener URL), umbrales de rendimiento, navegador/móvil objetivo y ubicación de evidencias.

## Sprint 4 — Respaldo y entrega operativa

- **Fecha:** completar en la planeación. **Duración/capacidad:** registrar lo acordado. **Participantes:** equipo TravelSnap.
- **Sprint Goal:** dejar definido cómo se recupera, publica y mantiene TravelSnap sin exponer información privada.
- **Criterio de éxito del objetivo:** respaldo restaurado en prueba; logging y alertas acordados; despliegue reproducible con HTTPS y dominio configurado si el equipo dispone de infraestructura; guía técnica actualizada.
- **Sprint Backlog completo:**
  - Producto: B46, B47, B48, B49, B50, B51, B52.
  - Técnico: HT-16, HT-17, HT-18, HT-22.
- **Dependencias/riesgos:** B47–B49 dependen de hosting, dominio, credenciales y presupuesto aprobados. No comprometer despliegue si el equipo no cuenta con ellos. La copia actual es local y SQLite.
- **Decisiones por registrar:** proveedor/plan de alojamiento, responsable operativo, periodicidad de respaldos, ubicación externa segura y política de mantenimiento.

## Plantilla para cerrar el acta después de reunirse

Al cerrar cada sesión, actualizamos fecha y participantes; Sprint Goal aprobado; Sprint Backlog final (IDs retirados/añadidos y motivo); estimación y capacidad acordadas; responsables; dependencias; evidencia de cierre; e impedimentos.
