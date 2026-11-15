-- TravelSnap: esquema SQL de la base SQLite.
-- Ejecutar desde la carpeta del proyecto con: sqlite3 data/travelsnap.sqlite3 ".read database.sql"

PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL COLLATE NOCASE UNIQUE,
    handle TEXT NOT NULL COLLATE NOCASE UNIQUE,
    avatar TEXT NOT NULL DEFAULT '',
    password_salt BLOB,
    password_hash BLOB,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS sessions (
    token_hash TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    expires_at INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS sessions_expiry ON sessions(expires_at);

CREATE TABLE IF NOT EXISTS posts (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    image_url TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    city TEXT NOT NULL,
    country TEXT NOT NULL,
    likes_count INTEGER NOT NULL DEFAULT 0 CHECK (likes_count >= 0),
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    display_date TEXT NOT NULL DEFAULT 'ahora'
);
CREATE INDEX IF NOT EXISTS posts_created ON posts(created_at DESC);

CREATE TABLE IF NOT EXISTS likes (
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    post_id TEXT NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    PRIMARY KEY (user_id, post_id)
);

CREATE TABLE IF NOT EXISTS follows (
    follower_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    followed_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    PRIMARY KEY (follower_id, followed_id),
    CHECK (follower_id <> followed_id)
);

CREATE TABLE IF NOT EXISTS comments (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    post_id TEXT NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    body TEXT NOT NULL CHECK (length(body) BETWEEN 1 AND 1000),
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Perfiles ficticios para que el feed de demostración tenga contenido inicial.
INSERT OR IGNORE INTO users(id, name, email, handle, avatar) VALUES
('seed_lucia', 'Lucía Fernández', 'lucia.viaja@travelsnap.demo', 'lucia.viaja', 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=120&q=80'),
('seed_andres', 'Andrés Mora', 'andresenruta@travelsnap.demo', 'andresenruta', 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=120&q=80'),
('seed_sofia', 'Sofía Ramírez', 'sofi.explora@travelsnap.demo', 'sofi.explora', 'https://images.unsplash.com/photo-1524504388940-b1c1722653e1?auto=format&fit=crop&w=120&q=80'),
('seed_mariana', 'Mariana Torres', 'mariana.enruta@travelsnap.demo', 'mariana.enruta', 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=120&q=80'),
('seed_nicolas', 'Nicolás Rojas', 'nicolasexplora@travelsnap.demo', 'nicolasexplora', 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=120&q=80'),
('seed_camila', 'Camila Vega', 'camila.va@travelsnap.demo', 'camila.va', 'https://images.unsplash.com/photo-1531123897727-8f129e1688ce?auto=format&fit=crop&w=120&q=80');

INSERT OR IGNORE INTO posts
(id, user_id, image_url, title, description, city, country, likes_count, display_date) VALUES
('p1', 'seed_lucia', 'https://images.unsplash.com/photo-1516483638261-f4dbaf036963?auto=format&fit=crop&w=1200&q=85', 'Un rincón para perder la noción del tiempo', 'Cinque Terre tiene ese ritmo lento que te recuerda por qué viajar también es detenerse un momento. 💛', 'Manarola', 'Italia', 248, 'hace 2 horas'),
('p2', 'seed_andres', 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1200&q=85', 'Despertar entre montañas', 'A las 5 de la mañana el frío casi me gana… pero ver salir el sol sobre estos picos hizo que valiera cada paso.', 'El Cocuy', 'Colombia', 192, 'hace 5 horas'),
('p3', 'seed_sofia', 'https://images.unsplash.com/photo-1533105079780-92b9be482077?auto=format&fit=crop&w=1200&q=85', 'Azul por todas partes', 'Una tarde sin planes en las islas griegas. A veces los mejores recuerdos aparecen cuando no tienes itinerario.', 'Oia, Santorini', 'Grecia', 376, 'ayer');
