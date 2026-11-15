# TravelSnap

Estamos construyendo TravelSnap como una red social sencilla para viajeros. La idea es compartir fotos de lugares visitados, contar algo de cada destino y descubrir viajes a partir de lo que publican otras personas.

## Cómo empezó el proyecto

Al inicio organizamos la propuesta en siete épicas y quince historias de usuario. Priorizamos primero el acceso, los perfiles, las publicaciones y el feed. Con esa guía hicimos una primera portada con fotos cambiantes y después fuimos conectando la interfaz con una API y una base de datos local.

## Avances que llevamos

- La portada presenta destinos con un carrusel automático de fotografías.
- El registro, el inicio de sesión y el cierre de sesión usan la API del servidor.
- Las cuentas se guardan en SQLite y las contraseñas se almacenan con PBKDF2-HMAC-SHA256.
- El feed muestra publicaciones con foto, autor y datos del destino.
- Se pueden crear publicaciones con una URL HTTPS, dar y quitar likes, seguir viajeros y eliminar publicaciones propias.
- Ahora también se pueden leer y publicar comentarios. El servidor valida el texto y lo relaciona con la cuenta y la publicación.
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
| `GET /api/posts` / `POST /api/posts` | Consultar el feed o crear una publicación. |
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

## Diagramas

En [`docs/DIAGRAMAS.md`](docs/DIAGRAMAS.md) incluimos diagramas de arquitectura, casos de uso, secuencia y entidad-relación que se pueden ver directamente en GitHub. El ER también está disponible como archivo editable de draw.io en [`docs/diagrams/TravelSnap_ER.drawio`](docs/diagrams/TravelSnap_ER.drawio).

## Qué sigue

Todavía tenemos pendiente editar el perfil, abrir una vista de detalle de cada publicación, personalizar el feed según los viajeros seguidos, paginar resultados, buscar destinos y guardar las fotos en un almacenamiento propio. También falta completar pruebas, copias de seguridad y revisar rendimiento y compatibilidad en distintos navegadores.

La meta de este repositorio es que el equipo pueda revisar lo que ya construimos y escoger tareas pequeñas para seguir avanzando.
