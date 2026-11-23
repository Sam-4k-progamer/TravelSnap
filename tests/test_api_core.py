"""Pruebas de integración HTTP + SQLite para los flujos sociales centrales."""

import json
import sys
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import server


class CoreApiIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory(prefix="travelsnap_core_")
        server.DATA_DIR = Path(cls.tmp.name)
        server.DB_PATH = server.DATA_DIR / "travelsnap.sqlite3"
        server.init_db()
        cls.http = ThreadingHTTPServer(("127.0.0.1", 0), server.TravelSnapHandler)
        cls.base = f"http://127.0.0.1:{cls.http.server_port}"
        cls.thread = threading.Thread(target=cls.http.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.http.shutdown()
        cls.http.server_close()
        cls.thread.join(timeout=5)
        cls.tmp.cleanup()

    @classmethod
    def req(cls, path, method="GET", data=None, cookie=None):
        raw = json.dumps(data).encode("utf-8") if data is not None else None
        headers = {"Content-Type": "application/json"} if raw is not None else {}
        if cookie:
            headers["Cookie"] = cookie
        request = Request(cls.base + path, data=raw, headers=headers, method=method)
        try:
            response = urlopen(request, timeout=8)
        except HTTPError as error:
            response = error
        with response:
            return response.status, json.loads(response.read()), response.headers.get("Set-Cookie", "").split(";")[0]

    def register(self, suffix):
        status, data, cookie = self.req("/api/register", "POST", {
            "name": f"Viajero {suffix}",
            "email": f"traveler{suffix}@example.test",
            "password": "Password123!",
        })
        self.assertEqual(status, 200)
        return data["user"], cookie

    def test_registration_duplicate_email_and_logout_revokes_session(self):
        payload = {"name": "Persona Uno", "email": "unique@example.test", "password": "Password123!"}
        status, _, cookie = self.req("/api/register", "POST", payload)
        self.assertEqual(status, 200)
        status, _, _ = self.req("/api/register", "POST", payload)
        self.assertEqual(status, 409)
        status, _, _ = self.req("/api/logout", "POST", {}, cookie)
        self.assertEqual(status, 200)
        status, _, _ = self.req("/api/me", cookie=cookie)
        self.assertEqual(status, 401)

    def test_comments_require_auth_and_are_linked_to_author_and_post(self):
        status, _, _ = self.req("/api/posts/p1/comments", "POST", {"body": "Hola"})
        self.assertEqual(status, 401)
        user, cookie = self.register("comments")
        status, result, _ = self.req("/api/posts/p1/comments", "POST", {"body": "  ¿Qué tal el viaje?  "}, cookie)
        self.assertEqual(status, 201)
        status, result_list, _ = self.req("/api/posts/p1/comments")
        self.assertEqual(status, 200)
        comment = next(item for item in result_list["comments"] if item["id"] == result["id"])
        self.assertEqual(comment["body"], "¿Qué tal el viaje?")
        self.assertEqual(comment["handle"], user["handle"])

    def test_like_is_unique_and_counter_reverses_on_unlike(self):
        _, cookie = self.register("likes")
        status, first, _ = self.req("/api/posts/p1/likes", "POST", {}, cookie)
        self.assertEqual(status, 200)
        status, duplicate, _ = self.req("/api/posts/p1/likes", "POST", {}, cookie)
        self.assertEqual(status, 200)
        self.assertEqual(first["likes"], duplicate["likes"])
        status, removed, _ = self.req("/api/posts/p1/likes", "DELETE", cookie=cookie)
        self.assertEqual(status, 200)
        self.assertEqual(removed["likes"], first["likes"] - 1)

    def test_follow_rejects_self_and_duplicate_does_not_duplicate_relation(self):
        user, cookie = self.register("follow")
        status, _, _ = self.req(f"/api/follows/{user['handle']}", "POST", {}, cookie)
        self.assertEqual(status, 400)
        status, _, _ = self.req("/api/follows/lucia.viaja", "POST", {}, cookie)
        self.assertEqual(status, 200)
        status, _, _ = self.req("/api/follows/lucia.viaja", "POST", {}, cookie)
        self.assertEqual(status, 200)
        with server.connect_db() as db:
            count = db.execute("SELECT COUNT(*) FROM follows WHERE follower_id=? AND followed_id='seed_lucia'", (user["id"],)).fetchone()[0]
        self.assertEqual(count, 1)

    def test_only_owner_can_delete_post(self):
        _, cookie = self.register("delete")
        status, _, _ = self.req("/api/posts/p1", "DELETE", cookie=cookie)
        self.assertEqual(status, 404)
        status, feed, _ = self.req("/api/posts")
        self.assertEqual(status, 200)
        self.assertIn("p1", [post["id"] for post in feed["posts"]])

    def test_owner_can_edit_own_post_but_not_another_posts(self):
        _, cookie = self.register("editpost")
        payload = {
            "image": "https://images.example.test/trip.jpg",
            "title": "Mi viaje",
            "description": "Una historia breve",
            "city": "Quito",
            "country": "Ecuador",
        }
        status, created, _ = self.req("/api/posts", "POST", payload, cookie)
        self.assertEqual(status, 201)
        updated = payload | {"title": "Título corregido"}
        status, _, _ = self.req(f"/api/posts/{created['id']}", "PATCH", updated, cookie)
        self.assertEqual(status, 200)
        status, _, _ = self.req("/api/posts/p1", "PATCH", updated, cookie)
        self.assertEqual(status, 404)
        status, feed, _ = self.req("/api/posts")
        own_post = next(post for post in feed["posts"] if post["id"] == created["id"])
        self.assertEqual(own_post["title"], "Título corregido")


if __name__ == "__main__":
    unittest.main()
