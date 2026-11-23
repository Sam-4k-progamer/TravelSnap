# Historias de usuario de TravelSnap

Agrupamos nuestras historias por épica y las vinculamos con los objetivos B del backlog. Mantenemos los IDs HU05, HU06 y HU15 que ya usamos para editar el nombre, previsualizar antes de publicar y buscar publicaciones. Las funciones futuras aparecen marcadas como pendientes.

| ID | Épica | Historia de usuario | Backlog | Estado |
|---|---|---|---|---|
| HU01 | E01 | Como visitante, quiero ver una portada atractiva y explorar historias públicas para entender TravelSnap y descubrir destinos. | B13, B18 | Parcial: portada terminada; feed público sin paginar. |
| HU02 | E02 | Como visitante, quiero registrarme con nombre, correo y contraseña para participar en la comunidad. | B15, B23 | Hecha |
| HU03 | E02 | Como viajero, quiero iniciar y cerrar sesión para acceder a las funciones privadas y proteger mi cuenta. | B16, B24, B25, B39 | Parcial: login/logout funcionan; refuerzo de producción pendiente. |
| HU04 | E02 | Como viajero, quiero consultar mi perfil para ver mis datos y publicaciones en un solo lugar. | B17 | Parcial: vista básica del perfil propio. |
| HU05 | E02 | Como viajero, quiero editar mi nombre visible para mantener mi perfil actualizado. | B08, B32 | Hecha para el nombre visible; biografía/avatar aún no incluidos. |
| HU06 | E03 | Como viajero, quiero previsualizar una imagen y revisar mi historia antes de confirmarla para evitar publicar un enlace equivocado. | B19 | Hecha para URL HTTPS; la carga del archivo es una historia aparte. |
| HU07 | E03 | Como viajero, quiero crear una publicación con título, descripción, foto y destino para compartir una experiencia. | B09, B19 | Hecha con URL de foto; archivo local/almacenamiento pendiente. |
| HU08 | E03 | Como autor, quiero eliminar una publicación propia para retirar contenido que ya no deseo compartir. | B26, B37 | Hecha |
| HU09 | E04 | Como viajero, quiero leer y escribir comentarios para conversar sobre los destinos publicados. | B10, B20, B27 | Hecha |
| HU10 | E04 | Como viajero, quiero dar o quitar un like para reaccionar sin duplicar la interacción. | B11, B28 | Hecha |
| HU11 | E04 | Como viajero, quiero seguir o dejar de seguir a otras cuentas para construir mi comunidad. | B11, B29 | Hecha |
| HU12 | E03 | Como autor, quiero editar mi publicación para corregir su foto, título, descripción o destino. | B26, B37 | Hecha |
| HU13 | E03 | Como lector, quiero abrir una publicación individual para consultar su contenido y conversación completa. | B33 | Pendiente |
| HU14 | E05 | Como viajero, quiero priorizar a quienes sigo y cargar más resultados para explorar un feed relevante. | B34, B36 | Pendiente |
| HU15 | E05 | Como viajero, quiero buscar por ciudad o país para encontrar publicaciones de un destino. | B35 | Parcial: filtro de cliente sobre publicaciones ya cargadas; no busca el servidor completo. |
| HU16 | E02 | Como viajero, quiero completar mi perfil con biografía y avatar para presentarme a la comunidad. | B08, B17, B32 | Parcial |
| HU17 | E03 | Como viajero, quiero subir fotos desde mi dispositivo para no depender de enlaces externos. | B31 | Pendiente |
| HU18 | E01 | Como persona que usa móvil o escritorio, quiero una interfaz adaptable para recorrer TravelSnap cómodamente. | B14, B45 | Parcial: CSS responsive; falta matriz de pruebas. |
| HU19 | E07 | Como equipo, queremos conservar pruebas y evidencias de avances para explicar al profesor qué se terminó. | B41, B42, B51, TT-01, TT-02 | Parcial: CI ejecutada; falta adjuntar evidencia por historia y sprint. |

## Alcance fuera de esta versión

- En esta versión trabajamos con visitantes y viajeros autenticados; dejamos por fuera el rol administrador y sus permisos.
- Recuperación de clave, verificación de correo y moderación quedan para una versión posterior si hacen parte del alcance del curso.
