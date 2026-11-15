# Diagramas de TravelSnap

Estos diagramas describen el estado actual del prototipo. El esquema entidad-relación editable también está en [formato draw.io](diagrams/TravelSnap_ER.drawio).

Versiones editables: [arquitectura](diagrams/TravelSnap_Architecture.drawio), [casos de uso](diagrams/TravelSnap_UseCases.drawio) y [secuencia de comentarios](diagrams/TravelSnap_CommentsSequence.drawio).

## 1. Arquitectura actual

```mermaid
flowchart LR
    V[Visitante o usuario] --> B[Navegador<br/>HTML · CSS · JavaScript]
    B -->|HTTP y JSON, mismo origen| API[Servidor Python<br/>API local]
    API --> DB[(SQLite<br/>travelsnap.sqlite3)]
    B -->|URLs de recursos| EXT[Unsplash y Google Fonts]
    API --> AUTH[Sesiones y validaciones]
    AUTH --> DB
```

## 2. Entidad-relación

```mermaid
erDiagram
    USERS ||--o{ SESSIONS : inicia
    USERS ||--o{ POSTS : publica
    USERS ||--o{ LIKES : da
    POSTS ||--o{ LIKES : recibe
    USERS ||--o{ FOLLOWS : follower_id
    USERS ||--o{ FOLLOWS : followed_id
    USERS ||--o{ COMMENTS : escribe
    POSTS ||--o{ COMMENTS : contiene

    USERS {
        TEXT id PK
        TEXT name
        TEXT email UK
        TEXT handle UK
        TEXT avatar
        BLOB password_salt
        BLOB password_hash
        TEXT created_at
    }
    SESSIONS {
        TEXT token_hash PK
        TEXT user_id FK
        INTEGER expires_at
    }
    POSTS {
        TEXT id PK
        TEXT user_id FK
        TEXT image_url
        TEXT title
        TEXT description
        TEXT city
        TEXT country
        INTEGER likes_count
        TEXT created_at
        TEXT display_date
    }
    LIKES {
        TEXT user_id PK, FK
        TEXT post_id PK, FK
        TEXT created_at
    }
    FOLLOWS {
        TEXT follower_id PK, FK
        TEXT followed_id PK, FK
        TEXT created_at
    }
    COMMENTS {
        TEXT id PK
        TEXT user_id FK
        TEXT post_id FK
        TEXT body
        TEXT created_at
    }
```

## 3. Casos de uso principales

```mermaid
flowchart LR
    Visitante([Visitante])
    Usuario([Usuario registrado])
    Registro[Crear cuenta]
    Login[Iniciar sesión]
    Portada[Ver destinos y carrusel]
    Feed[Consultar publicaciones]
    Perfil[Ver perfil propio]
    Publicar[Crear publicación]
    Like[Dar o quitar like]
    Seguir[Seguir o dejar de seguir]
    Comentar[Leer o escribir comentario]
    Eliminar[Eliminar publicación propia]
    Salir[Cerrar sesión]

    Visitante --> Registro
    Visitante --> Login
    Visitante --> Portada
    Usuario --> Feed
    Usuario --> Perfil
    Usuario --> Publicar
    Usuario --> Like
    Usuario --> Seguir
    Usuario --> Comentar
    Usuario --> Eliminar
    Usuario --> Salir
```

## 4. Secuencia: comentar una publicación

```mermaid
sequenceDiagram
    actor U as Usuario
    participant W as Navegador
    participant S as Servidor Python
    participant D as SQLite
    U->>W: Abre comentarios de una publicación
    W->>S: GET /api/posts/{id}/comments
    S->>D: Busca comentarios y sus autores
    D-->>S: Lista ordenada de comentarios
    S-->>W: JSON con los comentarios
    W-->>U: Muestra la conversación
    U->>W: Escribe y envía un comentario
    W->>S: POST /api/posts/{id}/comments + cookie de sesión
    S->>S: Valida sesión, publicación y longitud del texto
    S->>D: Inserta el comentario asociado al autor y post
    D-->>S: Confirmación
    S-->>W: 201 Created
    W->>S: GET /api/posts/{id}/comments
    S-->>W: Comentario actualizado
    W-->>U: Muestra el nuevo comentario
```
