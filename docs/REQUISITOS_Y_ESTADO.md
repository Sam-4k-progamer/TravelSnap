# Requisitos, usuarios, historias y estado de TravelSnap

En [`gestion-agil/`](gestion-agil/) dejamos nuestras épicas, el backlog de 52 objetivos, los criterios Gherkin, requisitos y DoD, historias de usuario/técnicas y planes de Sprint Planning.

En este documento registramos el alcance y el estado actual de TravelSnap. Comparamos cada punto con el código: **Hecho** significa que está implementado; **Parcial** significa que solo está cubierta una parte; **Pendiente** significa que todavía debemos desarrollarlo.

## 1. Alcance y tipos de usuario

| Tipo | Estado | Capacidades previstas |
|---|---|---|
| Visitante | Implementado parcialmente | Ver la portada con carrusel, consultar el feed público, registrarse e iniciar sesión. No puede crear interacciones ni publicar. |
| Viajero registrado | Implementado | Crear y cerrar sesión, consultar feed, publicar una foto por URL, comentar, dar/quitar likes, seguir/dejar de seguir cuentas, editar su nombre y borrar sus propias publicaciones. |
| Administrador | Fuera del alcance actual | Esta versión no tiene rol, panel administrativo ni permisos de moderación. |

No hay roles persistidos en la base actual. La separación de permisos se basa en visitante frente a usuario autenticado y en la propiedad del recurso.

## 2. Requisitos funcionales

### Visitante

- **RF-V01:** Al abrir TravelSnap, ver una portada identificable con fotografías de destinos que cambian automáticamente y controles para avanzar o registrarse/iniciar sesión.
- **RF-V02:** Consultar publicaciones públicas con fotografía, título, descripción, destino, autor y contador de likes.
- **RF-V03:** Crear cuenta indicando nombre, correo y contraseña; rechazar datos inválidos o correos duplicados.
- **RF-V04:** Iniciar sesión con correo y contraseña válidos y recibir una sesión de servidor.
- **RF-V05:** No poder publicar, comentar, dar likes, seguir cuentas ni cambiar datos de cuenta sin autenticarse.

### Viajero autenticado

- **RF-U01:** Cerrar sesión y revocar la sesión del servidor.
- **RF-U02:** Consultar el perfil propio básico y cambiar el nombre visible.
- **RF-U03:** Crear una publicación con URL HTTPS de imagen, título, descripción, ciudad y país; revisar la vista previa antes de confirmar.
- **RF-U04:** Eliminar publicaciones propias; no eliminar publicaciones de otra persona.
- **RF-U05:** Consultar y escribir comentarios asociados a la publicación y al autor autenticado.
- **RF-U06:** Dar y quitar un like por cuenta y publicación; mantener el contador coherente.
- **RF-U07:** Seguir/dejar de seguir a otra cuenta, sin duplicados ni auto-seguimiento.
- **RF-U08:** Buscar publicaciones cargadas por ciudad o país.

### Requisitos funcionales pendientes para ampliar el producto

- **RF-P01:** Editar publicaciones propias, incluyendo destino, texto y fotografía.
- **RF-P02:** Ver una ruta/pantalla de detalle por publicación.
- **RF-P03:** Feed personalizado por seguidos y paginación/carga progresiva.
- **RF-P04:** Buscar también por título, descripción, país, ciudad y términos turísticos con paginación del servidor.
- **RF-P05:** Subir archivos de imagen y guardarlos en almacenamiento seguro; la versión actual solo acepta una URL externa HTTPS.
- **RF-P06:** Ver perfiles ajenos y su lista de publicaciones con visibilidad definida.
- **RF-P07:** Recuperación de contraseña y verificación de correo.
- **RF-P08:** Moderación/administración solo cuando exista una necesidad definida y se añadan roles y controles.

## 3. Requisitos no funcionales

- **RNF-01 Seguridad:** contraseñas con PBKDF2-HMAC-SHA256, sales aleatorias y comparación constante; consultas SQL parametrizadas; validación en servidor; cookie de sesión `HttpOnly` y `SameSite=Strict`.
- **RNF-02 Integridad:** claves foráneas activadas por conexión, claves primarias y únicas, límites `CHECK`, cascada al borrar cuentas y claves compuestas para evitar likes/seguimientos duplicados.
- **RNF-03 Privacidad:** la base local y secretos no se incluyen en Git; las respuestas autenticadas no se cachean.
- **RNF-04 Facilidad de uso:** interfaz adaptable, navegación consistente, formularios con mensajes comprensibles y confirmación previa a publicar o borrar.
- **RNF-05 Rendimiento:** limitar filas por página y evitar descargar el feed completo; imágenes con dimensiones razonables y carga diferida.
- **RNF-06 Disponibilidad/recuperación:** copias de seguridad verificables, registros y despliegue documentado son objetivos pendientes.
- **RNF-07 Compatibilidad:** verificar navegadores modernos y móvil mediante pruebas reales antes de declarar compatibilidad.

## 4. Historias de usuario

| ID | Historia | Criterios de aceptación resumidos | Estado |
|---|---|---|---|
| HU01 | Como visitante, quiero ver una portada de viajes para entender la identidad del servicio. | Carrusel visible, cambia automáticamente y ofrece acceso a registro/login. | Hecha |
| HU02 | Como visitante, quiero explorar publicaciones para descubrir destinos. | Feed público muestra foto, destino, autor y contenido. | Hecha |
| HU03 | Como visitante, quiero crear una cuenta para participar. | Nombre, correo y clave validados; correo único; sesión iniciada al registrarme. | Hecha |
| HU04 | Como viajero, quiero entrar y salir de mi cuenta para proteger mi acceso. | Login correcto crea cookie; datos erróneos fallan; logout revoca cookie/sesión. | Parcial: login y logout existen; revisar endurecimiento de sesión. |
| HU05 | Como viajero, quiero cambiar mi nombre visible para mantener actualizado mi perfil. | 2–80 caracteres; solo modifica la cuenta de la sesión. | Hecha |
| HU06 | Como viajero, quiero previsualizar una imagen HTTPS antes de publicar. | Carga, error visible, revisión y confirmación explícita antes de guardar. | Hecha en esta copia |
| HU07 | Como viajero, quiero publicar una historia de viaje para compartirla. | URL, título, descripción, ciudad y país validados y guardados con autor. | Hecha (URL externa) |
| HU08 | Como viajero, quiero borrar mis publicaciones para administrar mi contenido. | Confirmación en UI; API verifica propietario; contenido asociado se elimina por cascada. | Hecha |
| HU09 | Como viajero, quiero comentar una publicación para conversar sobre el destino. | Comentario 1–1000 caracteres asociado al autor y al post. | Hecha |
| HU10 | Como viajero, quiero dar/quitar likes para expresar interés. | Una relación por usuario y publicación y contador actualizado. | Hecha |
| HU11 | Como viajero, quiero seguir o dejar de seguir a otros viajeros. | No seguirse a sí mismo; no duplicar vínculos; solo operación autenticada. | Hecha |
| HU12 | Como viajero, quiero filtrar el feed por ciudad o país. | Búsqueda sin distinguir mayúsculas/tildes y estado sin resultados. | Hecha en cliente, solo sobre filas cargadas |
| HU13 | Como viajero, quiero ver y editar mi perfil completo. | Mostrar publicaciones, avatar y biografía; permitir actualizar los campos propios. | Parcial (solo nombre y representación básica) |
| HU14 | Como viajero, quiero editar mis publicaciones para corregir datos. | Autor puede editar campos; otro usuario recibe rechazo; cambios persisten. | Hecha en esta copia |
| HU15 | Como viajero, quiero encontrar destinos y publicaciones por palabras clave. | Búsqueda en servidor por ciudad, país y texto con resultados paginados. | Parcial (cliente: ciudad/país) |
| HU16 | Como viajero, quiero abrir una publicación individual para consultar su conversación. | Ruta de detalle, autor, destino, imagen, likes y comentarios. | Pendiente |
| HU17 | Como viajero, quiero priorizar a quienes sigo en el feed. | Orden y regla de fallback documentados; paginación estable. | Pendiente |
| HU18 | Como visitante/usuario, quiero una interfaz adaptable para usar el sitio en móvil y escritorio. | Navegación y formularios utilizables en tamaños comunes y navegadores seleccionados. | Parcial; falta matriz de pruebas |

## 5. Priorización por valor y esfuerzo

Escala: prioridad **P0** bloquea seguridad o uso básico; **P1** aporta el núcleo social; **P2** mejora descubrimiento/escala; **P3** requiere operación o una decisión de producto. Esfuerzo: **S** pequeño, **M** mediano, **L** grande, **XL** infraestructura/servicio externo.

| Orden | Épica / entrega | Prioridad | Esfuerzo | Dependencias |
|---|---|---:|---:|---|
| 1 | Requisitos, roles, historias, arquitectura, ER y restricciones documentados | P0 | S | Ninguna |
| 2 | Registro, login/logout, sesiones y permisos por propiedad | P0 | M | Esquema users/sessions |
| 3 | Feed básico, crear/borrar publicación, comentarios y likes | P0 | M | Backend y esquema |
| 4 | Perfil completo y edición de publicaciones propias | P1 | M | API de usuarios/posts |
| 5 | Detalle de publicación y navegación por perfiles | P1 | M | Frontend y rutas API |
| 6 | Búsqueda en servidor, feed por seguidos y paginación | P1 | M/L | Índices y cursor estable |
| 7 | Carga real de imágenes | P2 | L/XL | Elegir almacenamiento, límites y configuración |
| 8 | Pruebas unitarias/integración/seguridad y compatibilidad | P1 | M/L | Flujos terminados |
| 9 | Copias, registros, monitoreo y mantenimiento | P2 | M | Entorno de operación |
| 10 | Producción, dominio, HTTPS y despliegue | P3 | XL | Hosting, secretos y dominio del equipo |

## 6. Estado auditado de los 52 puntos

| Nº | Estado actual | Evidencia o brecha principal |
|---:|---|---|
| 1 | Hecho | Requisitos funcionales y no funcionales descritos arriba. |
| 2 | Hecho | Visitante y viajero definidos; administrador fuera del alcance actual. |
| 3 | Hecho | Historias con criterios resumidos y estado. |
| 4 | Hecho | Priorización por valor, prioridad, esfuerzo y dependencias. |
| 5 | Hecho | Arquitectura actual documentada en `ARQUITECTURA.md` y `DIAGRAMAS.md`. |
| 6 | Hecho | SQLite local, inicializada desde `database.sql`; no hay servidor DB remoto. |
| 7 | Hecho | ER descrito en `DIAGRAMAS.md` y editable en draw.io. |
| 8 | Parcial | La tabla almacena nombre, email, usuario, avatar y fecha; no incluye biografía, destino preferido ni fecha de viaje. Solo se registra el nombre editable. |
| 9 | Hecho para URL | Tabla `posts` guarda URL de imagen y campos de publicación, no el binario de una foto. |
| 10 | Hecho | `comments` relaciona autor y publicación con claves foráneas. |
| 11 | Hecho | `likes` y `follows`, claves compuestas; contador de likes guardado en posts. |
| 12 | Hecho | PK, FK, UNIQUE, CHECK y `PRAGMA foreign_keys=ON`; revisar integridad en pruebas. |
| 13 | Hecho | Portada con marca TravelSnap, mensaje y carrusel. |
| 14 | Parcial | Navegación por tabs/acciones en la SPA; no hay vistas completas de perfil/detalle. |
| 15 | Hecho | Formulario de registro con nombre/correo/clave y validación de servidor. |
| 16 | Hecho | Formulario de login con validación. |
| 17 | Parcial | Modal de perfil propio básico y edición de nombre; sin perfil público completo, biografía o avatar editable. |
| 18 | Parcial | Feed visible; descarga todos los posts, sin paginación ni límite de tiempo. |
| 19 | Hecho para URL | Formulario pide título, descripción, ciudad, país e imagen HTTPS; no carga archivos. |
| 20 | Hecho | Modal de lectura y creación de comentarios. |
| 21 | Hecho en modo local | Servidor HTTP de Python y rutas API; aún no lo configuramos para producción. |
| 22 | Hecho | `sqlite3`, conexión por solicitud, inicialización desde SQL. |
| 23 | Hecho | Valida correo/nombre/clave y unicidad en DB; handle generado. |
| 24 | Hecho | Verifica PBKDF2 y usa comparación constante. |
| 25 | Parcial | Token aleatorio hash guardado, expiración 14 días, cookie HttpOnly/SameSite; falta `Secure` en HTTPS y limpieza más sistemática. |
| 26 | Hecho para CRUD | API permite consultar feed, crear, editar y eliminar con controles de propietario; paginación y detalle se controlan en los puntos 33 y 36. |
| 27 | Hecho básico | GET y POST de comentarios con sesión para crear. |
| 28 | Hecho | POST/DELETE, clave única evita likes repetidos y contador se ajusta. |
| 29 | Hecho básico | POST/DELETE y control de duplicados/autoseguimiento. |
| 30 | Parcial | Validaciones y login para escrituras; falta cobertura sistemática y control de abuso/rate limiting. |
| 31 | Pendiente | Solo URL HTTPS; no hay recepción ni almacenamiento de archivo. |
| 32 | Parcial | PATCH permite cambiar nombre; no biografía/avatar u otros datos. |
| 33 | Pendiente | No hay vista ni endpoint de detalle individual dedicado. |
| 34 | Pendiente | El feed es cronológico global, no prioriza seguidos. |
| 35 | Parcial | Filtro cliente por ciudad/país en los posts ya cargados; no consulta servidor/títulos/descripción. |
| 36 | Pendiente | API devuelve todas las publicaciones; no hay cursor/limit. |
| 37 | Hecho | Edición y borrado propios validan sesión y propiedad; los campos editables se validan en cliente y servidor. |
| 38 | Hecho | PBKDF2-HMAC-SHA256, sal individual aleatoria de 16 bytes y 310.000 iteraciones. |
| 39 | Parcial | Hash de token, vencimiento, revocación al salir, HttpOnly y SameSite; falta Secure en producción, rotación/limpieza y revisión CSRF según despliegue. |
| 40 | Parcial | Backend toma identidad de sesión y protege PATCH de cuenta/delete post/acciones; ampliar pruebas negativas para todos los endpoints/recursos. |
| 41 | Parcial | Hay una prueba automatizada de HU05; falta cobertura unitaria de validadores, auth, likes, follows, posts y comentarios. |
| 42 | Parcial | La prueba HU05 atraviesa HTTP y SQLite temporal; falta cobertura de flujos frontend/API/DB y regresión amplia. |
| 43 | Pendiente | No hay pruebas de seguridad documentadas ni análisis sistemático. |
| 44 | Pendiente | No existe medición o perfilado; feed sin paginar. |
| 45 | Parcial | CSS adaptable; no hay matriz documentada de navegador/dispositivo validada. |
| 46 | Parcial | `backup_database.py` crea una copia consistente y la verifica; la recuperación es manual y no hay programación automática ni réplica externa. |
| 47 | Pendiente | Solo entorno local; no hay configuración de despliegue/secretos. |
| 48 | Pendiente | No hay dominio ni TLS de producción. |
| 49 | Pendiente | No está desplegado; SQLite es local. |
| 50 | Parcial | Accesos HTTP se imprimen a consola; no hay log persistente, métricas ni alertas. |
| 51 | Hecho para el prototipo | README, instalación, API, requisitos, historias, arquitectura, esquema, ER, pruebas y límites están documentados. |
| 52 | Parcial | Hay un procedimiento inicial en `MANTENIMIENTO.md`; faltan responsables y calendario operativo del equipo. |

## 7. Decisiones y límites de alcance

- El prototipo usa SQLite porque es local, no requiere instalación de un servicio y permite demostrar relaciones y restricciones. Para producción con múltiples instancias habría que migrar y probar un motor servidor.
- Las fotografías son URL HTTPS externas. Para aceptar archivos se debe elegir almacenamiento, tamaño/formato máximo, escaneo, políticas de retención y secretos; no se simula esa capacidad.
- Las funciones que necesitan cuentas de hosting, credenciales, dominio, almacenamiento externo o una decisión del equipo (roles admin, moderación, recuperación de contraseña) quedan como trabajo pendiente y requieren configuración real.
- No subimos la base local al repositorio; `database.sql` crea el esquema y los datos de demostración.
