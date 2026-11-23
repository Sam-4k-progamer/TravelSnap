# TravelSnap

Estamos construyendo TravelSnap como una red social sencilla para viajeros. La idea es compartir fotos de lugares visitados, contar algo de cada destino y descubrir viajes a partir de lo que publican otras personas.

## Cómo empezó el proyecto

Al inicio organizamos la propuesta en siete épicas y quince historias de usuario. Priorizamos primero el acceso, los perfiles, las publicaciones y el feed. Con esa guía hicimos una primera portada con fotos cambiantes y después fuimos conectando la interfaz con una API y una base de datos local.

## Equipo del proyecto

Según los nombres compartidos en el chat del equipo: **Samuel Arias, Santiago Mejía, Juan Sebastián Molina y Andrés Velásquez**. Los responsables por historia y los usuarios de GitHub individuales quedan por confirmar entre nosotros.

## Avances que llevamos

- La portada presenta destinos con un carrusel automático de fotografías.
- El registro, el inicio de sesión y el cierre de sesión usan la API del servidor.
- Las cuentas se guardan en SQLite y las contraseñas se almacenan con PBKDF2-HMAC-SHA256.
- El feed muestra publicaciones con foto, autor y datos del destino.
- Se pueden crear publicaciones con una URL HTTPS, dar y quitar likes, seguir viajeros y eliminar publicaciones propias.
- Quien publicó una historia también puede editar su foto (URL), título, descripción y destino; el servidor valida la sesión y comprueba que sea la publicación propia.
- Ahora también se pueden leer y publicar comentarios. El servidor valida el texto y lo relaciona con la cuenta y la publicación.
- La historia HU06 está implementada en esta copia: al escribir una URL HTTPS se comprueba si la imagen carga, se presenta una vista previa, se muestran errores y antes de guardar se exige revisar y confirmar la publicación.
- La historia HU05 permite editar el nombre visible desde **Mi perfil** (2 a 80 caracteres) con validación en cliente y servidor y sin posibilidad de editar perfiles ajenos.
- La historia HU15 incorpora búsqueda instantánea de publicaciones por ciudad o país, sin distinguir mayúsculas o tildes, con opción de limpiar y mensaje cuando no hay resultados.
- Dejamos el esquema de la base en SQL y dibujamos el modelo entidad-relación.

Este es un prototipo académico. Seguimos trabajando sobre varias historias del README original; al final explicamos qué falta.

## Tecnologías

- **Frontend:** HTML, CSS y JavaScript sin framework.
- **Servidor y API:** Python usando su biblioteca estándar.
- **Base de datos:** SQLite. El esquema está en [`database.sql`](database.sql) y los datos locales se crean en `data/travelsnap.sqlite3` al iniciar el servidor.
- **Fotografías y tipografías:** recursos externos; por ahora las publicaciones reciben una URL de foto en vez de subir el archivo.

Las sesiones usan una cookie `HttpOnly` y `SameSite=Strict`. El frontend no guarda sesiones, cuentas, likes ni publicaciones en `localStorage`. El archivo de base de datos queda en el equipo y está excluido de Git.

## API disponible

| Método y ruta | Uso |
|---|---|
| `POST /api/register` | Crear una cuenta y abrir sesión. |
| `POST /api/login` / `POST /api/logout` | Iniciar o cerrar sesión. |
| `GET /api/me` | Consultar la cuenta de la sesión actual. |
| `PATCH /api/me` | Actualizar el nombre de la cuenta autenticada. |
| `GET /api/posts` / `POST /api/posts` | Consultar el feed o crear una publicación. |
| `PATCH /api/posts/{id}` | Editar foto URL, título, descripción, ciudad y país de una publicación propia. |
| `DELETE /api/posts/{id}` | Eliminar una publicación propia. |
| `POST` / `DELETE /api/posts/{id}/likes` | Añadir o quitar el like de la sesión. |
| `GET /api/posts/{id}/comments` | Consultar comentarios de una publicación. |
| `POST /api/posts/{id}/comments` | Crear un comentario con sesión iniciada. |
| `POST` / `DELETE /api/follows/{handle}` | Seguir o dejar de seguir a un viajero. |

La API se sirve desde el mismo origen que el frontend para mantener sencilla la configuración local.

## Ejecutar en el computador

Se necesita Python 3.10 o superior. Desde la carpeta del proyecto:

```powershell
python server.py
```

Luego abre <http://localhost:8000>. Para detener el servidor, usa `Ctrl+C` en la terminal.

Para generar una copia verificada de la base local ejecuta `python backup_database.py`. Las instrucciones de recuperación y mantenimiento están en [`docs/MANTENIMIENTO.md`](docs/MANTENIMIENTO.md); las carpetas de datos y copias se excluyen de Git.

## Probar HU06: vista previa y confirmación

1. Inicia el servidor con `python server.py`, abre `http://localhost:8000` e inicia sesión.
2. Haz clic en **Publicar**. Si la URL HTTPS apunta a una imagen que el navegador puede cargar, aparecerá la vista previa y se habilitará **Revisar publicación**.
3. Cambia la URL por un enlace incorrecto o una URL `http://`: aparecerá un error y no podrás avanzar. Luego coloca una imagen HTTPS accesible.
4. Completa título, descripción, ciudad y país, y pulsa **Revisar publicación**. Todavía no se habrá guardado nada.
5. Puedes **Volver a editar** o pulsar **Confirmar y publicar**. Solo la segunda acción envía `POST /api/posts`.

La vista previa comprueba desde el navegador si la imagen se puede cargar en ese momento; no garantiza que el enlace siga funcionando en el futuro. El servidor sigue validando los campos y exige una URL HTTPS bien formada. Esta función no sube archivos ni almacena las imágenes en el servidor.

## Probar HU05: editar el nombre del perfil

1. Inicia sesión y entra en **Mi perfil** → **Editar nombre**.
2. Guarda un nombre válido (entre 2 y 80 caracteres) y comprueba que cambia en el encabezado, el perfil y las publicaciones de tu cuenta.
3. Prueba un nombre de un carácter o uno de más de 80: se rechaza. La API obtiene la identidad directamente de la cookie de sesión: no acepta un ID de otro usuario.
4. Cierra sesión y vuelve a iniciar sesión para comprobar que el nuevo nombre quedó guardado.

## Probar HU15: buscar por ciudad o país

1. Entra en **Inicio**. Usa el campo **Buscar publicaciones por ciudad o país**.
2. Escribe `colombia`, `COLOMBIA` o `italia`. Las publicaciones se filtran en tiempo real, sin diferenciar mayúsculas ni tildes.
3. Escribe un lugar sin publicaciones: se muestra **Sin resultados**.
4. Pulsa **Limpiar**: reaparece el feed completo. Esta primera versión busca entre las publicaciones ya cargadas por la API; no requiere modificar la base de datos.

## Pruebas automatizadas

Para comprobar los flujos HTTP y SQLite (registro y correo duplicado, logout, comentarios, likes repetidos, seguimiento, edición/borrado de publicaciones propias y edición del perfil), desde la carpeta del proyecto ejecuta:

```powershell
python -m unittest discover -s tests -v
```

GitHub Actions ejecuta estas pruebas y las comprobaciones de sintaxis en cada push o pull request a `main`; la salida queda disponible como evidencia del workflow por 30 días. Ver [ci.yml](.github/workflows/ci.yml).

La búsqueda HU15 se puede verificar con los pasos manuales anteriores; funciona en el navegador con las publicaciones ya recuperadas por la API. Estas pruebas de integración no reemplazan pruebas de navegador, carga, seguridad especializada ni compatibilidad.

## Diagramas

En [`docs/DIAGRAMAS.md`](docs/DIAGRAMAS.md) incluimos diagramas de arquitectura, casos de uso, secuencia y entidad-relación que se pueden ver directamente en GitHub. El ER también está disponible como archivo editable de draw.io en [`docs/diagrams/TravelSnap_ER.drawio`](docs/diagrams/TravelSnap_ER.drawio).

## Requisitos y arquitectura

La definición de visitantes y viajeros, requisitos funcionales/no funcionales, historias de usuario, prioridades y auditoría de los 52 puntos está en [`docs/REQUISITOS_Y_ESTADO.md`](docs/REQUISITOS_Y_ESTADO.md). La comunicación entre navegador, servidor Python y SQLite, el flujo de una solicitud, las restricciones de datos y los límites del prototipo están en [`docs/ARQUITECTURA.md`](docs/ARQUITECTURA.md).

El paquete de gestión ágil basado en el chat del equipo está en [`docs/gestion-agil/`](docs/gestion-agil/): épicas y backlog de 52 objetivos, [historias de usuario](docs/gestion-agil/06_HISTORIAS_DE_USUARIO.md), criterios de aceptación Gherkin, requerimientos/DoD, historias técnicas y cuatro actas propuestas de Sprint Planning. El chat no registra las reuniones, fechas ni estimaciones; las actas son borradores para validar, no actas históricas.

## Qué sigue

Todavía tenemos pendiente abrir una vista de detalle de cada publicación, personalizar el feed según los viajeros seguidos, paginar resultados y guardar las fotos en un almacenamiento propio. La edición del nombre, la búsqueda por ciudad/país y la vista previa de las imágenes ya están implementadas en esta versión local. También falta completar pruebas, copias de seguridad y revisar rendimiento y compatibilidad en distintos navegadores.

La meta de este repositorio es que el equipo pueda revisar lo que ya construimos y escoger tareas pequeñas para seguir avanzando.

## Tareas pequeñas para el equipo

- [HU05: editar el nombre del perfil](https://github.com/Sam-4k-progamer/TravelSnap/issues/1) — implementada en esta versión local; pendiente de integrar y cerrar en GitHub.
- [HU15: buscar por ciudad o país](https://github.com/Sam-4k-progamer/TravelSnap/issues/2) — implementada en esta versión local; pendiente de integrar y cerrar en GitHub.
- [HU06: previsualizar la foto antes de publicar](https://github.com/Sam-4k-progamer/TravelSnap/issues/3) — implementada en esta versión local; pendiente de integrar y cerrar en GitHub.
