# Operación local y mantenimiento

## Copia de seguridad y recuperación de SQLite

La base local está en `data/travelsnap.sqlite3` y las copias quedan en `backups/`; ambas carpetas están excluidas de Git porque pueden contener datos personales.

1. Ejecuta `python backup_database.py` desde la carpeta raíz del proyecto.
2. Comprueba el mensaje `Copia verificada` y conserva la copia en otro disco o almacenamiento del equipo. Guardarla únicamente junto a la aplicación no protege contra pérdida del computador.
3. Para recuperar, detén TravelSnap con `Ctrl+C`. Renombra la base dañada como respaldo de diagnóstico, copia el archivo elegido desde `backups/` a `data/travelsnap.sqlite3` y conserva ese nombre exacto.
4. Inicia el servidor y confirma login, feed y creación/lectura de un comentario. No borres la copia recuperada hasta validar el resultado.

La aplicación no programa respaldos automáticos ni cifra copias. El equipo debe escoger periodicidad, custodio y ubicación segura según los datos que use.

## Mantenimiento del proyecto

- Antes de cambiar el esquema, guarda una copia y conserva una migración SQL revisable; no dependas de `CREATE TABLE IF NOT EXISTS` para modificar tablas existentes.
- Ejecuta `python -m unittest discover -s tests -v`, `python -m py_compile server.py` y `node --check app.js` después de cambios en backend o frontend.
- Revisa dependencias (actualmente no hay paquetes externos de Python), enlaces externos de imágenes y Google Fonts; registra cambios de comportamiento en `README.md`.
- Para cada funcionalidad nueva, crea historia y criterios de aceptación, implementa validación del servidor y permiso por sesión, añade cobertura y actualiza arquitectura/ER si cambia la persistencia.
- Antes de uso público, definir responsable de actualizaciones, frecuencia de revisión de seguridad, política de retención, monitoreo, incidentes, restauración y entorno de despliegue. Esos procedimientos aún no están operativos.
