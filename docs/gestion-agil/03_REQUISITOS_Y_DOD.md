# Requerimientos y Definition of Done

## Roles

- **Visitante:** ve portada/feed público, se registra o inicia sesión. No realiza acciones privadas.
- **Viajero autenticado:** administra su cuenta y sus publicaciones, comenta, da likes y sigue viajeros.
- **Administrador:** no está implementado ni se confirmó en el chat. No se debe asignar permisos admin hasta acordar sus responsabilidades.

## Requerimientos funcionales

| ID | Requerimiento | Backlog | Prioridad |
|---|---|---|---:|
| RF-01 | El visitante puede entender la propuesta en la portada y explorar publicaciones públicas. | 13, 18 | P1 |
| RF-02 | Una persona puede registrarse con datos válidos y correo no repetido. | 15, 23 | P0 |
| RF-03 | El viajero puede iniciar/cerrar sesión; las rutas privadas requieren sesión vigente. | 16, 24, 25 | P0 |
| RF-04 | El viajero puede consultar y editar su perfil según campos permitidos. | 17, 32 | P1 |
| RF-05 | El viajero puede crear, consultar, editar y borrar sus propias publicaciones. | 19, 26, 37 | P1 |
| RF-06 | El viajero puede leer y escribir comentarios ligados a la publicación y cuenta correctas. | 20, 27 | P1 |
| RF-07 | El viajero puede dar/quitar un like, con una relación única y contador coherente. | 11, 28 | P1 |
| RF-08 | El viajero puede seguir/dejar de seguir otras cuentas sin duplicar relaciones ni seguirse a sí mismo. | 11, 29 | P1 |
| RF-09 | El viajero puede buscar publicaciones y obtener feed con orden/carga definidos. | 18, 34, 35, 36 | P1 |
| RF-10 | La API valida entradas, sesión, autorización y propiedad antes de mutar información. | 30, 40 | P0 |
| RF-11 | El sistema recibe y conserva fotos en un almacenamiento acordado. | 31 | P2 |
| RF-12 | El equipo puede instalar, operar, respaldar y recuperar la aplicación según el entorno aprobado. | 46–52 | P2/P3 |

## Requerimientos no funcionales

| ID | Requerimiento | Verificación / relación |
|---|---|---|
| RNF-01 Seguridad de credenciales | No guardar claves en claro; usar hash con sal individual; comparar credenciales de forma segura. | B24, B38, revisión de base y pruebas negativas. |
| RNF-02 Seguridad de sesión | Token no predecible, almacenamiento no reversible, expiración, revocación y atributos seguros en HTTPS. | B25, B39. |
| RNF-03 Autorización | Cada escritura usa identidad de sesión; recursos propios verifican propietario; denegar por defecto. | B30, B37, B40. |
| RNF-04 Integridad | PK/FK, unicidad, checks y transacciones; ninguna referencia huérfana. | B07, B10–B12, pruebas SQL. |
| RNF-05 Privacidad | No subir bases de usuarios, copias, secretos ni datos de prueba personales a GitHub. | Revisión `.gitignore` y checklist de release. |
| RNF-06 Rendimiento | Feed paginado con orden estable; imágenes limitadas y carga progresiva; objetivo medido se debe acordar. | B18, B36, B44. |
| RNF-07 Usabilidad/accesibilidad | Formularios entendibles, mensajes de error, navegación por teclado y diseño móvil. | B13–B20, B45. |
| RNF-08 Mantenibilidad | Funciones/rutas y esquema documentados; cambios con pruebas, revisión y migraciones. | B05, B51, B52. |
| RNF-09 Recuperación | Copias verificadas y procedimiento restaurado en entorno de prueba. | B46. |
| RNF-10 Operación | Despliegue reproducible, HTTPS, registro de errores y monitoreo una vez acordado hosting. | B47–B50. |

## Definition of Ready (DoR)

Una tarea puede entrar al sprint si tiene: ID único; resultado o usuario beneficiario; criterios aceptables y comprobables; prioridad; dependencias y datos necesarios; y tamaño/capacidad estimados por el equipo. Si requiere proveedor, dominio, política de datos o decisión del profesor, esa dependencia debe estar resuelta o declarada como riesgo.

## Definition of Done (DoD) de historia de software

Una historia se considera terminada solo cuando:

1. Cumple todos sus escenarios Gherkin aceptados y el alcance queda reflejado en la interfaz/API.
2. Se valida en servidor todo dato no confiable y se comprueba sesión/propiedad cuando corresponde.
3. Cambios de persistencia tienen esquema/migración, restricciones y diagrama actualizados.
4. Pruebas relevantes pasan; las de seguridad cubren también accesos no autorizados y datos límite.
5. Cambios de interfaz se revisan al menos en escritorio y móvil; se registran capturas/evidencias sin datos personales.
6. Código se revisa por otro integrante o se registra que la revisión queda pendiente antes de cerrar el issue.
7. README/API/arquitectura/ER se actualizan cuando cambia el comportamiento.
8. No quedan secretos, base local, respaldos ni archivos temporales en el commit.
9. El commit/PR enlaza el ID de backlog y conserva evidencia reproducible (prueba, captura o salida de CI).

## DoD de documentación / análisis

El documento identifica alcance y fuentes; separa hechos del chat de propuestas; tiene IDs consistentes; criterios verificables; estado actual no exagerado; relaciones con el backlog; y aprobación/revisión del equipo pendiente o registrada. Las actas de sprint de este paquete son **propuestas**: el chat no aporta fechas, estimaciones ni evidencia de que esas reuniones ocurrieran.

## Requisitos de entrega académica derivados del chat

- README con integrantes, idea, requerimientos funcionales/épicas, requisitos no funcionales/DoD e historias técnicas.
- Modelo ER para presentar y revisar.
- Backlog de al menos 50 objetivos: aquí se conserva la lista de 52 del plan de producto.
- Automatización de verificación y evidencias de avance. Son necesidades mencionadas en el chat, pero el pipeline y la plantilla de evidencia aún no están instalados.
