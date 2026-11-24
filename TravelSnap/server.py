"""TravelSnap demo server: static frontend, JSON API, and SQLite storage."""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import re
import secrets
import sqlite3
import time
from http import HTTPStatus
from http.cookies import SimpleCookie
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
DB_PATH = DATA_DIR / "travelsnap.sqlite3"
HOST = "127.0.0.1"
PORT = 8000
SESSION_COOKIE = "travelsnap_session"
SESSION_TTL = 60 * 60 * 24 * 14
PASSWORD_ROUNDS = 310_000
MAX_BODY = 64 * 1024

def connect_db() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH, timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    schema = (ROOT / "database.sql").read_text(encoding="utf-8")
    with connect_db() as db:
        db.executescript(schema)
        db.execute("DELETE FROM sessions WHERE expires_at < ?", (int(time.time()),))


def user_payload(row: sqlite3.Row) -> dict:
    return {"id": row["id"], "name": row["name"], "email": row["email"], "handle": row["handle"], "avatar": row["avatar"]}


def hash_password(password: str, salt: bytes | None = None) -> tuple[bytes, bytes]:
    salt = salt or secrets.token_bytes(16)
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PASSWORD_ROUNDS)
    return salt, hashed


def valid_image_url(value: object) -> bool:
    if not isinstance(value, str) or not value or len(value) > 2048 or any(char.isspace() for char in value):
        return False
    try:
        parsed = urlparse(value)
        return parsed.scheme == "https" and bool(parsed.hostname) and not parsed.username and not parsed.password
    except ValueError:
        return False


class TravelSnapHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        super().end_headers()

    def send_json(self, status: int, data: object, extra_headers: list[tuple[str, str]] | None = None):
        raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        if extra_headers:
            for name, value in extra_headers:
                self.send_header(name, value)
        self.end_headers()
        self.wfile.write(raw)

    def read_json(self) -> dict:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            raise ValueError("Solicitud no válida.")
        if length <= 0 or length > MAX_BODY:
            raise ValueError("El formulario está vacío o es demasiado grande.")
        try:
            payload = json.loads(self.rfile.read(length))
        except (json.JSONDecodeError, UnicodeDecodeError):
            raise ValueError("Formato de solicitud no válido.")
        if not isinstance(payload, dict):
            raise ValueError("Formato de solicitud no válido.")
        return payload

    def cookie_token(self) -> str | None:
        cookie = SimpleCookie()
        try:
            cookie.load(self.headers.get("Cookie", ""))
            morsel = cookie.get(SESSION_COOKIE)
            return morsel.value if morsel else None
        except Exception:
            return None

    def current_user(self, db: sqlite3.Connection) -> sqlite3.Row | None:
        token = self.cookie_token()
        if not token:
            return None
        digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
        return db.execute(
            """SELECT u.* FROM sessions s JOIN users u ON u.id=s.user_id
               WHERE s.token_hash=? AND s.expires_at>?""",
            (digest, int(time.time())),
        ).fetchone()

    def require_user(self, db: sqlite3.Connection) -> sqlite3.Row | None:
        user = self.current_user(db)
        if user is None:
            self.send_json(HTTPStatus.UNAUTHORIZED, {"error": "Inicia sesión para continuar."})
        return user

    def create_session(self, db: sqlite3.Connection, user_id: str) -> str:
        token = secrets.token_urlsafe(32)
        digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
        db.execute("INSERT INTO sessions(token_hash,user_id,expires_at) VALUES(?,?,?)", (digest, user_id, int(time.time()) + SESSION_TTL))
        return f"{SESSION_COOKIE}={token}; Path=/; HttpOnly; SameSite=Strict; Max-Age={SESSION_TTL}"

    def do_GET(self):
        path = urlparse(self.path).path
        if not path.startswith("/api/"):
            public_files = {"/", "/index.html", "/app.js", "/styles.css"}
            if path not in public_files:
                return self.send_error(HTTPStatus.NOT_FOUND)
            self.path = "/index.html" if path == "/" else path
            return super().do_GET()
        with connect_db() as db:
            if path == "/api/me":
                user = self.current_user(db)
                if user is None:
                    return self.send_json(HTTPStatus.UNAUTHORIZED, {"error": "No hay una sesión activa."})
                return self.send_json(HTTPStatus.OK, {"user": user_payload(user)})
            if path == "/api/posts":
                user = self.current_user(db)
                rows = db.execute("""SELECT p.*,u.name,u.handle,u.avatar,
                    CASE WHEN l.user_id IS NULL THEN 0 ELSE 1 END AS liked_by_me,
                    CASE WHEN p.user_id=? THEN 1 ELSE 0 END AS owned_by_me
                    FROM posts p JOIN users u ON u.id=p.user_id
                    LEFT JOIN likes l ON l.post_id=p.id AND l.user_id=?
                    ORDER BY p.created_at DESC,p.id""", (user["id"] if user else "", user["id"] if user else "")).fetchall()
                posts = [{"id": r["id"], "name": r["name"], "handle": r["handle"], "avatar": r["avatar"],
                          "image": r["image_url"], "title": r["title"], "description": r["description"],
                          "city": r["city"], "country": r["country"], "likes": r["likes_count"],
                          "liked": bool(r["liked_by_me"]), "owner": "me" if r["owned_by_me"] else r["user_id"],
                          "date": r["display_date"]} for r in rows]
                return self.send_json(HTTPStatus.OK, {"posts": posts})
            if path.startswith("/api/posts/") and path.endswith("/comments"):
                post_id = path[len("/api/posts/"):-len("/comments")].strip("/")
                if not db.execute("SELECT 1 FROM posts WHERE id=?", (post_id,)).fetchone():
                    return self.send_json(HTTPStatus.NOT_FOUND, {"error": "La publicación no existe."})
                rows = db.execute("""SELECT c.id,c.body,c.created_at,u.name,u.handle,u.avatar
                    FROM comments c JOIN users u ON u.id=c.user_id
                    WHERE c.post_id=? ORDER BY c.created_at ASC,c.id ASC""", (post_id,)).fetchall()
                return self.send_json(HTTPStatus.OK, {"comments": [dict(row) for row in rows]})
            if path == "/api/suggestions":
                user = self.require_user(db)
                if user is None:
                    return
                rows = db.execute("""SELECT u.id,u.name,u.handle,u.avatar,
                    CASE WHEN f.follower_id IS NULL THEN 0 ELSE 1 END AS followed
                    FROM users u LEFT JOIN follows f ON f.followed_id=u.id AND f.follower_id=?
                    WHERE u.id LIKE 'seed_%' AND u.id<>? ORDER BY u.name""", (user["id"], user["id"])).fetchall()
                return self.send_json(HTTPStatus.OK, {"suggestions": [dict(r) | {"followed": bool(r["followed"])} for r in rows]})
            return self.send_json(HTTPStatus.NOT_FOUND, {"error": "No se encontró el recurso."})

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            payload = self.read_json()
        except ValueError as error:
            return self.send_json(HTTPStatus.BAD_REQUEST, {"error": str(error)})

        if path in ("/api/register", "/api/login"):
            email = str(payload.get("email", "")).strip().lower()
            password = payload.get("password", "")
            if not isinstance(password, str) or len(password) < 8 or len(password) > 256:
                return self.send_json(HTTPStatus.BAD_REQUEST, {"error": "La contraseña debe tener al menos 8 caracteres."})
            if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email) or len(email) > 254:
                return self.send_json(HTTPStatus.BAD_REQUEST, {"error": "Revisa el formato del correo electrónico."})
            with connect_db() as db:
                if path == "/api/register":
                    name = str(payload.get("name", "")).strip()
                    if len(name) < 2 or len(name) > 80:
                        return self.send_json(HTTPStatus.BAD_REQUEST, {"error": "Escribe un nombre de entre 2 y 80 caracteres."})
                    handle_base = re.sub(r"[^a-z0-9_]+", "_", email.split("@", 1)[0])[:24].strip("_") or "viajero"
                    handle = handle_base
                    suffix = 2
                    while db.execute("SELECT 1 FROM users WHERE handle=? COLLATE NOCASE", (handle,)).fetchone():
                        handle = f"{handle_base[:20]}{suffix}"
                        suffix += 1
                    salt, password_hash = hash_password(password)
                    user_id = secrets.token_hex(16)
                    try:
                        db.execute("INSERT INTO users(id,name,email,handle,password_salt,password_hash) VALUES(?,?,?,?,?,?)",
                                   (user_id, name, email, handle, salt, password_hash))
                    except sqlite3.IntegrityError:
                        return self.send_json(HTTPStatus.CONFLICT, {"error": "No se pudo crear la cuenta. Verifica si el correo ya está registrado."})
                    user = db.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
                else:
                    user = db.execute("SELECT * FROM users WHERE email=? COLLATE NOCASE", (email,)).fetchone()
                    if user is None or user["password_hash"] is None:
                        return self.send_json(HTTPStatus.UNAUTHORIZED, {"error": "Correo o contraseña incorrectos."})
                    candidate = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), user["password_salt"], PASSWORD_ROUNDS)
                    if not hmac.compare_digest(candidate, user["password_hash"]):
                        return self.send_json(HTTPStatus.UNAUTHORIZED, {"error": "Correo o contraseña incorrectos."})
                session_cookie = self.create_session(db, user["id"])
                return self.send_json(HTTPStatus.OK, {"user": user_payload(user)}, [("Set-Cookie", session_cookie)])

        if path == "/api/logout":
            token = self.cookie_token()
            if token:
                with connect_db() as db:
                    db.execute("DELETE FROM sessions WHERE token_hash=?", (hashlib.sha256(token.encode()).hexdigest(),))
            return self.send_json(HTTPStatus.OK, {"ok": True}, [("Set-Cookie", f"{SESSION_COOKIE}=; Path=/; HttpOnly; SameSite=Strict; Max-Age=0")])

        if path == "/api/posts":
            with connect_db() as db:
                user = self.require_user(db)
                if user is None:
                    return
                image = payload.get("image", "")
                title = str(payload.get("title", "")).strip()
                description = str(payload.get("description", "")).strip()
                city = str(payload.get("city", "")).strip()
                country = str(payload.get("country", "")).strip()
                if not valid_image_url(image) or not (1 <= len(title) <= 90) or not (1 <= len(description) <= 300) or not (1 <= len(city) <= 80) or not (1 <= len(country) <= 80):
                    return self.send_json(HTTPStatus.BAD_REQUEST, {"error": "Revisa la foto y los campos de la publicación."})
                post_id = secrets.token_hex(12)
                db.execute("INSERT INTO posts(id,user_id,image_url,title,description,city,country,display_date) VALUES(?,?,?,?,?,?,?,'ahora')",
                           (post_id, user["id"], image, title, description, city, country))
                return self.send_json(HTTPStatus.CREATED, {"id": post_id})

        if path.startswith("/api/posts/") and path.endswith("/comments"):
            with connect_db() as db:
                user = self.require_user(db)
                if user is None:
                    return
                post_id = path[len("/api/posts/"):-len("/comments")].strip("/")
                body = payload.get("body", "")
                if not isinstance(body, str):
                    return self.send_json(HTTPStatus.BAD_REQUEST, {"error": "Escribe un comentario válido."})
                body = body.strip()
                if not 1 <= len(body) <= 1000:
                    return self.send_json(HTTPStatus.BAD_REQUEST, {"error": "El comentario debe tener entre 1 y 1000 caracteres."})
                if not db.execute("SELECT 1 FROM posts WHERE id=?", (post_id,)).fetchone():
                    return self.send_json(HTTPStatus.NOT_FOUND, {"error": "La publicación no existe."})
                comment_id = secrets.token_hex(12)
                db.execute("INSERT INTO comments(id,user_id,post_id,body) VALUES(?,?,?,?)", (comment_id, user["id"], post_id, body))
                return self.send_json(HTTPStatus.CREATED, {"id": comment_id})

        if path.startswith("/api/posts/") and path.endswith("/likes"):
            with connect_db() as db:
                user = self.require_user(db)
                if user is None:
                    return
                post_id = path[len("/api/posts/"):-len("/likes")].strip("/")
                if not db.execute("SELECT 1 FROM posts WHERE id=?", (post_id,)).fetchone():
                    return self.send_json(HTTPStatus.NOT_FOUND, {"error": "La publicación no existe."})
                db.execute("INSERT OR IGNORE INTO likes(user_id,post_id) VALUES(?,?)", (user["id"], post_id))
                if db.execute("SELECT changes()").fetchone()[0]:
                    db.execute("UPDATE posts SET likes_count=likes_count+1 WHERE id=?", (post_id,))
                row = db.execute("SELECT likes_count FROM posts WHERE id=?", (post_id,)).fetchone()
                return self.send_json(HTTPStatus.OK, {"liked": True, "likes": row["likes_count"]})

        if path.startswith("/api/follows/"):
            with connect_db() as db:
                user = self.require_user(db)
                if user is None:
                    return
                handle = path.removeprefix("/api/follows/").strip("/")
                target = db.execute("SELECT id FROM users WHERE handle=? COLLATE NOCASE", (handle,)).fetchone()
                if target is None:
                    return self.send_json(HTTPStatus.NOT_FOUND, {"error": "No se encontró a ese viajero."})
                if target["id"] == user["id"]:
                    return self.send_json(HTTPStatus.BAD_REQUEST, {"error": "No puedes seguir tu propia cuenta."})
                db.execute("INSERT OR IGNORE INTO follows(follower_id,followed_id) VALUES(?,?)", (user["id"], target["id"]))
                return self.send_json(HTTPStatus.OK, {"following": True})

        return self.send_json(HTTPStatus.NOT_FOUND, {"error": "No se encontró el recurso."})

    def do_PATCH(self):
        path = urlparse(self.path).path
        if path != "/api/me":
            return self.send_json(HTTPStatus.NOT_FOUND, {"error": "No se encontró el recurso."})
        with connect_db() as db:
            user = self.require_user(db)
            if user is None:
                return
            try:
                payload = self.read_json()
            except ValueError as error:
                return self.send_json(HTTPStatus.BAD_REQUEST, {"error": str(error)})
            name = payload.get("name")
            if not isinstance(name, str):
                return self.send_json(HTTPStatus.BAD_REQUEST, {"error": "El nombre debe ser un texto válido."})
            name = name.strip()
            if not 2 <= len(name) <= 80:
                return self.send_json(HTTPStatus.BAD_REQUEST, {"error": "El nombre debe tener entre 2 y 80 caracteres."})
            # El ID proviene exclusivamente de la sesión autenticada.
            db.execute("UPDATE users SET name=? WHERE id=?", (name, user["id"]))
            updated = db.execute("SELECT * FROM users WHERE id=?", (user["id"],)).fetchone()
            return self.send_json(HTTPStatus.OK, {"user": user_payload(updated)})

    def do_DELETE(self):
        path = urlparse(self.path).path
        with connect_db() as db:
            user = self.require_user(db)
            if user is None:
                return
            if path.startswith("/api/posts/") and path.endswith("/likes"):
                post_id = path[len("/api/posts/"):-len("/likes")].strip("/")
                db.execute("DELETE FROM likes WHERE user_id=? AND post_id=?", (user["id"], post_id))
                if db.execute("SELECT changes()").fetchone()[0]:
                    db.execute("UPDATE posts SET likes_count=MAX(0,likes_count-1) WHERE id=?", (post_id,))
                row = db.execute("SELECT likes_count FROM posts WHERE id=?", (post_id,)).fetchone()
                if row is None:
                    return self.send_json(HTTPStatus.NOT_FOUND, {"error": "La publicación no existe."})
                return self.send_json(HTTPStatus.OK, {"liked": False, "likes": row["likes_count"]})
            if path.startswith("/api/posts/"):
                post_id = path.removeprefix("/api/posts/").strip("/")
                cursor = db.execute("DELETE FROM posts WHERE id=? AND user_id=?", (post_id, user["id"]))
                if cursor.rowcount == 0:
                    return self.send_json(HTTPStatus.NOT_FOUND, {"error": "No se encontró una publicación propia para eliminar."})
                return self.send_json(HTTPStatus.OK, {"ok": True})
            if path.startswith("/api/follows/"):
                handle = path.removeprefix("/api/follows/").strip("/")
                target = db.execute("SELECT id FROM users WHERE handle=? COLLATE NOCASE", (handle,)).fetchone()
                if target:
                    db.execute("DELETE FROM follows WHERE follower_id=? AND followed_id=?", (user["id"], target["id"]))
                return self.send_json(HTTPStatus.OK, {"following": False})
        return self.send_json(HTTPStatus.NOT_FOUND, {"error": "No se encontró el recurso."})

    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {self.address_string()} {format % args}")


if __name__ == "__main__":
    init_db()
    server = ThreadingHTTPServer((HOST, PORT), TravelSnapHandler)
    print(f"TravelSnap activo en http://localhost:{PORT}")
    print(f"Base de datos SQLite: {DB_PATH}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
    finally:
        server.server_close()
