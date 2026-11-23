# language: es
# Criterios de aceptación del backlog. Los escenarios describen el resultado esperado;
# los marcados como pendientes no implican que esa funcionalidad esté implementada.

Característica: Definición del producto
  Escenario: B01 requisitos claros
    Dado el alcance de TravelSnap
    Cuando el equipo revisa la especificación
    Entonces encuentra requisitos funcionales y no funcionales con estado verificable

  Escenario: B02 tipos de usuario identificados
    Dado el diseño de acceso
    Cuando se consulta la definición de actores
    Entonces se distinguen visitante y viajero autenticado y se indica si existe rol administrador

  Escenario: B03 historias de usuario refinadas
    Dado una necesidad del viajero
    Cuando se añade al backlog
    Entonces se registra actor, valor, prioridad y criterio de aceptación

  Escenario: B04 backlog priorizado
    Dado el conjunto de historias y tareas técnicas
    Cuando el equipo prepara un sprint
    Entonces puede ordenar trabajo por valor, riesgo, dependencias y esfuerzo

  Escenario: B05 arquitectura entendible
    Dado el navegador, API y almacenamiento
    Cuando una persona consulta la arquitectura
    Entonces identifica responsabilidades, protocolo y flujo de datos entre componentes

  Escenario: B06 motor de datos definido
    Dado el entorno de demostración
    Cuando se inicializa TravelSnap
    Entonces el motor y el archivo de esquema documentan cómo crear la base

  Escenario: B07 modelo ER verificable
    Dado el esquema relacional
    Cuando se revisa el diagrama ER
    Entonces cada entidad y relación corresponde a tablas, claves y cardinalidades documentadas

Característica: Persistencia e integridad
  Escenario: B08 datos del usuario
    Dado un usuario registrado
    Cuando se consulta su registro
    Entonces se conservan los campos de perfil definidos y su fecha de creación

  Escenario: B09 publicación y fotografía
    Dado un viajero autenticado
    Cuando publica una historia válida
    Entonces se guardan referencia de foto, descripción, destino y autor asociado

  Escenario: B10 comentario relacionado
    Dado un comentario creado sobre una publicación existente
    Cuando se consulta la conversación
    Entonces el comentario muestra su autor y publicación relacionados

  Escenario: B11 interacciones sin duplicar
    Dado un usuario y una publicación
    Cuando intenta registrar dos veces el mismo like o seguimiento
    Entonces la base conserva una sola relación

  Escenario: B12 integridad referencial
    Dado una operación con una clave relacionada inexistente
    Cuando se intenta guardar
    Entonces la base rechaza la operación y mantiene los datos consistentes

Característica: Experiencia de navegación
  Escenario: B13 portada de TravelSnap
    Dado un visitante que abre la aplicación
    Cuando carga la página inicial
    Entonces ve la identidad del producto y fotografías de destinos en un carrusel

  Escenario: B14 navegación entre secciones
    Dado un viajero autenticado
    Cuando elige Inicio o Mi perfil
    Entonces llega a la sección solicitada y puede volver a la otra sección

  Escenario: B15 registro
    Dado un visitante con nombre, correo y contraseña válidos
    Cuando envía el formulario de registro
    Entonces se crea una cuenta única y se informa el resultado

  Escenario: B16 inicio de sesión
    Dado una cuenta existente con contraseña correcta
    Cuando envía el formulario de acceso
    Entonces se autentica y accede a las opciones de usuario

  Escenario: B17 perfil consultable
    Dado un viajero que abre un perfil
    Cuando se muestra la información de la cuenta
    Entonces aparecen identidad, datos de perfil y publicaciones permitidas

  Escenario: B18 feed usable
    Dado un conjunto de publicaciones
    Cuando el viajero abre Inicio
    Entonces ve tarjetas legibles y una cantidad de resultados controlada por carga

  Escenario: B19 formulario de publicación
    Dado un viajero autenticado
    Cuando completa foto, título, descripción y destino
    Entonces puede revisar los datos y confirmar la publicación válida

  Escenario: B20 comentarios desde la interfaz
    Dado una publicación existente
    Cuando el viajero abre comentarios y envía texto válido
    Entonces ve el comentario relacionado a esa publicación y a su cuenta

Característica: API y autenticación
  Escenario: B21 servidor local
    Dado las dependencias estándar instaladas
    Cuando se ejecuta el comando de inicio documentado
    Entonces el servidor local responde a páginas estáticas y rutas API

  Escenario: B22 persistencia desde API
    Dado una solicitud válida de creación o actualización
    Cuando la API la procesa
    Entonces el cambio se refleja en SQLite y sobrevive a una nueva consulta

  Escenario: B23 validación de registro
    Dado un correo ya registrado o campos inválidos
    Cuando se intenta crear otra cuenta
    Entonces la API rechaza el registro sin duplicar usuarios

  Escenario: B24 verificación de credenciales
    Dado una cuenta registrada
    Cuando se envían credenciales válidas o inválidas
    Entonces solo la contraseña correcta autentica sin revelar cuál campo falló

  Escenario: B25 ciclo de sesión
    Dado un usuario autenticado
    Cuando vence la sesión o solicita salir
    Entonces la sesión deja de autorizar solicitudes protegidas

  Escenario: B26 ciclo CRUD de publicación
    Dado el autor de una publicación
    Cuando crea, consulta, edita o elimina su historia
    Entonces la API persiste la operación y comprueba la propiedad en cambios destructivos

  Escenario: B27 API de comentarios
    Dado una publicación existente
    Cuando se consulta o crea un comentario autorizado
    Entonces la API devuelve la lista o confirma la inserción con sus relaciones correctas

  Escenario: B28 API de likes
    Dado un usuario autenticado y una publicación
    Cuando agrega o quita su like
    Entonces cambia su estado una sola vez y el contador refleja las relaciones

  Escenario: B29 API de seguimiento
    Dado dos cuentas distintas
    Cuando una sigue o deja de seguir a la otra
    Entonces se conserva una relación única y se prohíbe el auto-seguimiento

  Escenario: B30 permisos y validaciones
    Dado una operación con sesión ausente, campos incorrectos o recurso ajeno
    Cuando se llama la API
    Entonces se devuelve un error apropiado y no se modifica información no autorizada

Característica: Funciones de producto y seguridad
  Escenario: B31 almacenamiento de fotos
    Dado un archivo que cumple formato y tamaño permitidos
    Cuando un usuario autenticado lo carga
    Entonces se almacena de forma controlada y la publicación conserva una referencia segura

  Escenario: B32 edición de perfil
    Dado el propietario de una cuenta
    Cuando actualiza nombre, biografía o avatar válidos
    Entonces los cambios se guardan y se reflejan en su perfil

  Escenario: B33 detalle de publicación
    Dado el identificador de una publicación
    Cuando una persona abre su detalle
    Entonces ve fotografía, descripción, destino, autor, likes y comentarios

  Escenario: B34 feed personalizado
    Dado un usuario que sigue viajeros
    Cuando solicita el feed personalizado
    Entonces primero aparecen publicaciones de cuentas seguidas según el orden acordado

  Escenario: B35 búsqueda
    Dado términos de ciudad, país o palabras clave
    Cuando el viajero busca contenido
    Entonces recibe únicamente coincidencias relevantes y una indicación si no hay resultados

  Escenario: B36 paginación
    Dado más publicaciones que el límite de una página
    Cuando se solicita una página y luego la siguiente
    Entonces se entregan lotes ordenados sin duplicados ni saltos

  Escenario: B37 administración de publicaciones propias
    Dado un autor autenticado y una publicación propia
    Cuando edita o elimina su contenido
    Entonces los cambios se guardan; si el recurso es ajeno, no se modifica

  Escenario: B38 almacenamiento de contraseñas
    Dado dos cuentas con contraseñas iguales
    Cuando se guardan sus credenciales
    Entonces cada hash usa una sal individual y la base no contiene la contraseña en claro

  Escenario: B39 protección de sesión
    Dado una sesión activa en un entorno HTTPS
    Cuando se emite la cookie
    Entonces contiene atributos seguros, vencimiento y puede revocarse al cerrar sesión

  Escenario: B40 autorización por recurso
    Dado un usuario que solicita cambiar un recurso ajeno
    Cuando la API comprueba la sesión y propiedad
    Entonces deniega la acción y deja intacto el recurso

Característica: Calidad, producción y mantenimiento
  Escenario: B41 pruebas unitarias
    Dado validadores y reglas de dominio
    Cuando se ejecuta la suite unitaria
    Entonces los casos válidos, inválidos y límites reportan resultados reproducibles

  Escenario: B42 pruebas de integración
    Dado frontend, API y base de datos conectados
    Cuando se ejecuta un flujo de extremo a extremo
    Entonces la operación iniciada en la interfaz persiste y se muestra correctamente

  Escenario: B43 verificación de seguridad
    Dado un conjunto documentado de amenazas y casos negativos
    Cuando se ejecuta la revisión de seguridad
    Entonces se registran hallazgos, severidad, evidencia y correcciones

  Escenario: B44 rendimiento
    Dado una carga de referencia definida
    Cuando se mide feed, API y fotografías
    Entonces los tiempos y consultas cumplen umbrales acordados por el equipo

  Escenario: B45 compatibilidad
    Dado navegadores y tamaños de pantalla acordados
    Cuando se ejecutan los recorridos principales
    Entonces navegación y formularios funcionan sin defectos bloqueantes

  Escenario: B46 respaldo y recuperación
    Dado una base de datos con información válida
    Cuando se genera una copia y se restaura en un entorno de prueba
    Entonces la integridad se verifica y los datos se recuperan

  Escenario: B47 configuración de producción
    Dado el entorno de alojamiento aprobado
    Cuando se configura una instancia nueva
    Entonces dependencias, variables y secretos se suministran sin incluirlos en Git

  Escenario: B48 dominio y HTTPS
    Dado un dominio controlado por el equipo
    Cuando se habilita TLS
    Entonces el sitio es accesible por HTTPS y redirige el tráfico HTTP

  Escenario: B49 despliegue
    Dado frontend, backend y base configurados
    Cuando se publica una versión
    Entonces los recorridos principales funcionan en el entorno de producción

  Escenario: B50 observabilidad
    Dado un error o caída del servicio
    Cuando ocurre en el entorno desplegado
    Entonces queda un registro útil y una alerta permite detectar el incidente

  Escenario: B51 documentación de entrega
    Dado una persona nueva en el equipo
    Cuando sigue la documentación
    Entonces puede instalar, iniciar, entender arquitectura/datos/API y usar el sistema

  Escenario: B52 mantenimiento
    Dado una solicitud de cambio o actualización
    Cuando el equipo aplica el proceso acordado
    Entonces revisa impacto, pruebas, documentación, respaldo y responsable de seguimiento
