# Backlog de producto TravelSnap

## Cómo organizamos el backlog

Elegimos continuar con TravelSnap y ordenamos el trabajo en siete épicas y **52 objetivos**. En el repositorio están como issues #4–#55: B01 corresponde al issue #4 y B52 al #55. Los issues #1–#3 corresponden a las historias HU05, HU15 y HU06. En este documento agrupamos las tareas por área, prioridad y estado para que podamos escoger trabajo y revisar avances sin duplicarlo.

El equipo del proyecto está formado por **Samuel Arias, Santiago Mejía, Juan Sebastián Molina y Andrés Velásquez**. Repartimos responsables al organizar cada sprint.

## Épicas

| Código | Épica | Resultado esperado |
|---|---|---|
| E01 | Descubrir TravelSnap | Un visitante entiende el producto, explora el contenido público y puede registrarse o iniciar sesión. |
| E02 | Cuenta y perfil viajero | Una persona crea y protege su cuenta, consulta su perfil y administra sus datos. |
| E03 | Publicaciones de viaje | Una persona crea, consulta, edita y elimina sus historias con destino y fotografía. |
| E04 | Comunidad e interacción | Viajeros conversan, reaccionan y construyen relaciones de seguimiento. |
| E05 | Descubrimiento del feed | Una persona encuentra contenido, ve publicaciones relevantes y carga resultados de forma progresiva. |
| E06 | Plataforma, datos y seguridad | La aplicación valida operaciones y conserva datos íntegros con acceso autorizado. |
| E07 | Calidad y operación | El equipo verifica, documenta, respalda y prepara TravelSnap para uso sostenido. |

## Backlog de 52 objetivos

Prioridad: **P0** esencial para el prototipo seguro; **P1** funcionalidad principal; **P2** ampliación; **P3** operación/publicación. Estado basado en la copia local revisada el 23-11-2026: **Hecho**, **Parcial** o **Pendiente**. Los criterios de aceptación están en [`02_CRITERIOS_GHERKIN.feature`](02_CRITERIOS_GHERKIN.feature).

| ID | Épica | Objetivo / historia resumida | Tipo | Prioridad | Estado |
|---:|---|---|---|---:|---|
| 01 | E06 | Definir requisitos funcionales y no funcionales. | Análisis | P0 | Hecho |
| 02 | E01 | Identificar visitante y viajero; documentar si habrá administrador. | Análisis | P0 | Hecho |
| 03 | E01 | Definir historias de usuario con valor y aceptación. | Análisis | P0 | Hecho |
| 04 | E07 | Priorizar el backlog por valor, riesgo y esfuerzo. | Análisis | P0 | Hecho |
| 05 | E06 | Documentar arquitectura y comunicación frontend/API/SQLite. | Técnico | P0 | Hecho |
| 06 | E06 | Definir motor y esquema de almacenamiento local. | Técnico | P0 | Hecho |
| 07 | E06 | Diseñar ER con entidades, atributos, claves y cardinalidades. | Técnico | P0 | Hecho |
| 08 | E02 | Guardar nombre, contacto, descripción, destino y registro del usuario. | Técnico | P1 | Parcial: faltan biografía/destino de perfil |
| 09 | E03 | Guardar foto, descripción y autor de la publicación. | Técnico | P1 | Parcial: se guarda URL, no archivo |
| 10 | E04 | Relacionar comentarios con publicación y autor. | Técnico | P1 | Hecho |
| 11 | E04 | Guardar likes y relaciones seguidor/seguido sin duplicados. | Técnico | P1 | Hecho |
| 12 | E06 | Aplicar PK, FK, unicidad, validaciones y reglas de integridad. | Técnico | P0 | Hecho |
| 13 | E01 | Mostrar portada reconocible con carrusel temático. | UX | P1 | Hecho |
| 14 | E01 | Navegar entre inicio y perfil de forma clara. | UX | P1 | Parcial: navegación básica, faltan vistas de detalle/perfil público |
| 15 | E02 | Diseñar y validar registro. | UX/API | P0 | Hecho |
| 16 | E02 | Diseñar y validar inicio de sesión. | UX/API | P0 | Hecho |
| 17 | E02 | Mostrar perfil, nombre, foto y publicaciones del viajero. | UX | P1 | Parcial: perfil propio básico |
| 18 | E05 | Diseñar feed y carga progresiva de publicaciones. | UX/API | P1 | Parcial: feed actual sin paginar |
| 19 | E03 | Crear publicación con foto, título, descripción y destino. | UX/API | P1 | Parcial: admite URL, no carga archivo |
| 20 | E04 | Leer y publicar comentarios desde la interfaz. | UX/API | P1 | Hecho |
| 21 | E06 | Configurar servidor HTTP local y rutas API. | Técnico | P0 | Hecho para prototipo local |
| 22 | E06 | Conectar backend a SQLite para operaciones CRUD. | Técnico | P0 | Hecho |
| 23 | E02 | Validar registro y rechazar cuentas duplicadas. | API | P0 | Hecho |
| 24 | E02 | Autenticar credenciales usando hash seguro. | API | P0 | Hecho |
| 25 | E06 | Mantener, expirar y cerrar sesiones. | API/Seguridad | P0 | Parcial: falta endurecimiento de producción |
| 26 | E03 | Crear API CRUD de publicaciones ligada a su autor. | API | P1 | Hecho para CRUD; paginación/detalle son ítems separados |
| 27 | E04 | Crear y consultar comentarios ligados a autor y publicación. | API | P1 | Hecho |
| 28 | E04 | Dar/quitar likes únicos y actualizar contador. | API | P1 | Hecho |
| 29 | E04 | Seguir/dejar de seguir evitando duplicados y auto-seguimiento. | API | P1 | Hecho |
| 30 | E06 | Validar entradas, sesión y permisos de cada operación. | API/Seguridad | P0 | Parcial: ampliar cobertura y controles antiabuso |
| 31 | E03 | Subir y almacenar fotos de forma segura. | Técnico/API | P2 | Pendiente |
| 32 | E02 | Editar nombre, biografía y foto de perfil propios. | API/UX | P1 | Parcial: solo nombre visible |
| 33 | E03 | Abrir vista individual de una publicación. | UX/API | P1 | Pendiente |
| 34 | E05 | Personalizar feed priorizando cuentas seguidas. | API | P2 | Pendiente |
| 35 | E05 | Buscar publicaciones por destinos y palabras clave. | API/UX | P1 | Parcial: filtro cliente por ciudad/país cargados |
| 36 | E05 | Paginar feed para limitar filas por solicitud. | Técnico/API | P1 | Pendiente |
| 37 | E03 | Editar y borrar publicaciones propias con control de propiedad. | API/UX | P1 | Hecho |
| 38 | E06 | Derivar contraseñas con sales individuales y algoritmo resistente. | Seguridad | P0 | Hecho: PBKDF2-HMAC-SHA256 |
| 39 | E06 | Fortalecer sesión con cookie segura, expiración y revocación. | Seguridad | P0 | Parcial: Secure requiere HTTPS de producción |
| 40 | E06 | Autorizar operaciones solo sobre recursos permitidos. | Seguridad | P0 | Parcial: reglas básicas existen; falta revisión sistemática |
| 41 | E07 | Crear pruebas unitarias de validadores y lógica. | QA | P1 | Parcial: pruebas actuales son principalmente integración |
| 42 | E07 | Probar integración frontend/API/base de datos. | QA | P1 | Parcial: pruebas HTTP+SQLite, falta navegador/E2E |
| 43 | E07 | Revisar seguridad de entradas, sesiones y acceso. | QA/Seguridad | P1 | Pendiente |
| 44 | E07 | Medir y optimizar consultas, feed e imágenes. | Rendimiento | P2 | Pendiente |
| 45 | E07 | Verificar adaptación en dispositivos y navegadores. | QA/UX | P1 | Parcial: diseño adaptable sin matriz de verificación |
| 46 | E07 | Crear y probar respaldo y recuperación. | Operación | P2 | Parcial: respaldo verificado; restauración manual |
| 47 | E07 | Preparar configuración de producción y secretos. | Operación | P3 | Pendiente |
| 48 | E07 | Configurar dominio y TLS/HTTPS. | Operación | P3 | Pendiente |
| 49 | E07 | Desplegar y comprobar frontend, backend y datos. | Operación | P3 | Pendiente |
| 50 | E07 | Registrar errores y monitorear disponibilidad. | Operación | P2 | Parcial: log HTTP en consola, sin alertas |
| 51 | E07 | Documentar arquitectura, esquema, API, instalación y uso. | Documentación | P1 | Hecho para prototipo académico |
| 52 | E07 | Acordar mantenimiento y evolución del producto. | Proceso | P2 | Parcial: guía inicial, faltan responsables/calendario |

## Tareas técnicas transversales

Además del backlog de producto, incluimos dos tareas técnicas para automatizar las verificaciones y conservar evidencias reproducibles. Se identifican aparte para mantener los 52 IDs del backlog sin cambios.

| ID técnico | Historia técnica | Criterio de aceptación | Estado |
|---|---|---|---|
| TT-01 | Como equipo, queremos ejecutar automáticamente verificaciones al integrar cambios para detectar regresiones antes de exponer. | Dado un cambio en una rama, cuando se ejecuta el flujo automatizado, entonces se ejecutan pruebas y verificaciones de sintaxis y queda visible el resultado. | Hecha: workflow ejecutado con éxito en GitHub Actions |
| TT-02 | Como equipo, queremos conservar evidencias reproducibles para mostrar avances al profesor. | Dado un sprint terminado, cuando se prepara su evidencia, entonces se enlazan commit/PR, captura o salida de pruebas y criterios aceptados, sin datos personales ni credenciales. | Parcial: CI guarda salida de pruebas; falta adjuntar evidencia por historia/sprint y asignar responsable |

## Definition of Ready resumida

Una historia entra al Sprint Backlog cuando tiene ID, usuario/valor o resultado técnico claro, aceptación verificable, prioridad acordada, dependencias visibles y tamaño/capacidad revisados por el equipo. Si falta una decisión (por ejemplo, proveedor de imágenes o hosting), queda como pendiente de refinamiento, no se estima como comprometida.
