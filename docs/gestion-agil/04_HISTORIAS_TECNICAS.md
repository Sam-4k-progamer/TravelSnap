# Historias técnicas

Las historias técnicas habilitan historias de usuario o reducen riesgos. El estado describe la versión de TravelSnap revisada; el pipeline quedó configurado en este avance y su primer resultado remoto debe confirmarse.

| ID | Historia técnica | Aceptación en formato Dado/Cuando/Entonces | Relación | Estado |
|---|---|---|---|---|
| HT-01 | Como equipo, quiero inicializar SQLite desde un esquema versionado para recrear el entorno local. | Dado una carpeta sin DB, cuando inicio el servidor, entonces crea las tablas e índices documentados. | 06, 21 | Hecha |
| HT-02 | Como sistema, quiero activar y verificar FK, PK, UNIQUE y CHECK para evitar inconsistencias. | Dado una referencia inválida o duplicada, cuando se intenta insertar, entonces SQLite rechaza el dato. | 07, 12 | Hecha en esquema |
| HT-03 | Como sistema, quiero cerrar conexiones DB y delimitar transacciones para que los cambios sean visibles y no se filtren manejadores. | Dado una solicitud que modifica datos, cuando se confirma, entonces el cambio está disponible y la conexión se cierra. | 22 | Hecha; cubierta por pruebas recientes |
| HT-04 | Como sistema, quiero guardar solo hashes PBKDF2 con sales individuales. | Dado el registro de una cuenta, cuando se persisten credenciales, entonces no queda contraseña en claro y se genera sal aleatoria. | 24, 38 | Hecha |
| HT-05 | Como sistema, quiero guardar hash del token de sesión y expirar/revocar sesiones. | Dado login, expiración o logout, cuando una sesión se consulta, entonces solo token vigente autoriza y logout la revoca. | 25, 39 | Parcial; falta endurecimiento HTTPS de producción |
| HT-06 | Como API, quiero limitar tamaño JSON y validar campos antes de SQL. | Dado cuerpo demasiado grande o dato fuera de rango, cuando llega la petición, entonces devuelve error y no altera la DB. | 23, 30 | Hecha para rutas actuales; falta cobertura integral |
| HT-07 | Como API, quiero derivar el autor desde sesión y no confiar en IDs enviados por cliente. | Dado una operación protegida, cuando se procesa, entonces user_id se toma de la sesión autenticada. | 26–30, 40 | Hecha para rutas implementadas; falta revisión de seguridad formal |
| HT-08 | Como servidor, quiero confirmar cada mutación antes de responder éxito. | Dado una escritura aceptada, cuando la API responde, entonces una solicitud posterior observa el cambio confirmado. | 22–30 | Hecha |
| HT-09 | Como mantenedor, quiero un feed con cursor/limit e índices para no leer toda la tabla. | Dado más filas que el tamaño de página, cuando el cliente pide resultados, entonces recibe un lote estable y un cursor para continuar. | 18, 36 | Pendiente |
| HT-10 | Como equipo, quiero un almacenamiento de imágenes con límites y URLs controladas. | Dado un archivo no permitido o demasiado grande, cuando se carga, entonces se rechaza; una foto válida recibe referencia persistente. | 31 | Pendiente: falta decidir proveedor/política |
| HT-11 | Como aplicación, quiero migraciones explícitas para cambios compatibles con DB existentes. | Dado un esquema anterior, cuando se aplica una migración, entonces los datos se conservan y el esquema llega a la versión esperada. | 06–12, 32 | Pendiente |
| HT-12 | Como equipo, quiero pruebas unitarias de validadores y reglas de dominio. | Dado entradas válidas, inválidas y de límite, cuando se ejecutan tests unitarios, entonces se verifican los resultados esperados sin servicios externos. | 41 | Parcial |
| HT-13 | Como equipo, quiero pruebas HTTP contra SQLite temporal para verificar contratos. | Dado rutas de API principales, cuando corre la suite, entonces cubre autorización, persistencia, errores y relaciones. | 42 | Parcial; hay suite HTTP+SQLite de flujos centrales |
| HT-14 | Como equipo, quiero pruebas automatizadas de seguridad para rutas privadas y propiedad. | Dado usuario sin sesión o propietario distinto, cuando llama rutas protegidas, entonces obtiene rechazo y los datos no cambian. | 30, 40, 43 | Parcial; hay casos puntuales, falta matriz completa |
| HT-15 | Como usuario, quiero un frontend adaptable y accesible. | Dado viewport móvil/escritorio y teclado, cuando recorro flujos principales, entonces controles se ven, se enfocan y funcionan. | 13–20, 45 | Parcial; falta reporte cross-browser |
| HT-16 | Como equipo, quiero copias consistentes y restauración comprobada. | Dado una DB válida, cuando ejecuto respaldo y restauración de prueba, entonces integrity_check devuelve ok y los registros son recuperables. | 46 | Parcial; respaldo implementado, restauración aún manual/no automatizada |
| HT-17 | Como equipo, quiero logging y monitoreo sin exponer secretos. | Dado una falla o indisponibilidad, cuando ocurre, entonces queda un evento trazable y una alerta para el equipo. | 50 | Parcial; solo logs HTTP en consola |
| HT-18 | Como equipo, quiero configuración reproducible de producción y TLS. | Dado hosting y dominio aprobados, cuando se despliega, entonces secretos quedan fuera de Git y todo tráfico público usa HTTPS. | 47–49 | Pendiente: requiere infraestructura del equipo |
| HT-19 | Como mantenedor, quiero documentación coherente con código y base. | Dado una ruta, tabla o cambio de flujo, cuando se integra, entonces README/API/ER/arquitectura se actualizan. | 05–07, 51 | Hecha para alcance del prototipo |
| HT-20 | Como equipo, quiero un pipeline CI que ejecute pruebas al cambiar código. | Dado un push o pull request, cuando inicia CI, entonces corre `python -m unittest`, `py_compile` y `node --check`, y publica estado. | 41, 42, chat | CI configurada en `.github/workflows/ci.yml`; pendiente confirmar primer run |
| HT-21 | Como equipo, quiero conservar evidencias de aceptación por sprint. | Dado un criterio aceptado, cuando el equipo cierra la tarea, entonces adjunta enlace de commit/PR y captura o salida reproducible. | chat, DoD | Parcial: CI publica salida de pruebas como artifact; falta evidenciar aceptación por historia |
| HT-22 | Como equipo, quiero un proceso de revisión de dependencia y mantenimiento. | Dado una actualización propuesta, cuando se prepara release, entonces se revisa impacto, compatibilidad, tests, respaldo y plan de reversa. | 52 | Parcial; procedimiento inicial en MANTENIMIENTO.md |

## Guía de automatización propuesta

El workflow `.github/workflows/ci.yml` ejecuta GitHub Actions en push/PR a `main`: checkout, Python 3.12, Node 24, `python -m unittest discover -s tests -v`, `python -m py_compile server.py backup_database.py`, `node --check app.js` y guarda la salida de pruebas como artifact por 30 días. No despliega automáticamente ni necesita secretos.

## Plantilla de evidencia propuesta

Para cada historia: ID y criterio Gherkin; pasos reproducibles; resultado esperado/obtenido; salida de prueba o captura sin datos personales; enlace al commit/PR; fecha; integrante que verificó; defectos conocidos. No se debe afirmar una prueba manual que no se ejecutó.
