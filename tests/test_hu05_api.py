"""Pruebas locales de HU05 sin dependencias externas: python -m unittest discover -s tests."""

import json
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import server


class EditProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory(prefix='travelsnap_test_')
        server.DATA_DIR = Path(cls.tmp.name)
        server.DB_PATH = server.DATA_DIR / 'travelsnap.sqlite3'
        server.init_db()
        cls.http = ThreadingHTTPServer(('127.0.0.1', 0), server.TravelSnapHandler)
        cls.base = f'http://127.0.0.1:{cls.http.server_port}'
        cls.thread = threading.Thread(target=cls.http.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.http.shutdown()
        cls.http.server_close()
        cls.thread.join(timeout=5)
        cls.tmp.cleanup()

    @classmethod
    def req(cls, path, method='GET', data=None, cookie=None):
        payload = json.dumps(data).encode('utf-8') if data is not None else None
        headers = {'Content-Type': 'application/json'} if payload is not None else {}
        if cookie:
            headers['Cookie'] = cookie
        try:
            res = urlopen(Request(cls.base + path, data=payload, headers=headers, method=method), timeout=5)
        except HTTPError as exc:
            res = exc
        with res:
            return res.status, json.loads(res.read()), res.headers.get('Set-Cookie', '').split(';')[0]

    def test_restrictions_and_persistence(self):
        status, _, _ = self.req('/api/me', 'PATCH', {'name': 'Cambiar'})
        self.assertEqual(status, 401)
        first = {'email': 'travel_test1@example.org', 'name': 'Usuario Uno', 'password': 'Password123!'}
        second = {'email': 'travel_test2@example.org', 'name': 'Usuario Dos', 'password': 'Password123!'}
        status, data1, cookie1 = self.req('/api/register', 'POST', first)
        self.assertEqual(status, 200)
        status, data2, cookie2 = self.req('/api/register', 'POST', second)
        self.assertEqual(status, 200)
        for invalid in ['A', ' ' * 4, 'a' * 81, None, 3]:
            status, _, _ = self.req('/api/me', 'PATCH', {'name': invalid}, cookie1)
            self.assertEqual(status, 400)
        status, updated, _ = self.req('/api/me', 'PATCH', {'name': '  María López  ', 'user_id': data2['user']['id']}, cookie1)
        self.assertEqual(status, 200)
        self.assertEqual(updated['user']['name'], 'María López')
        self.assertEqual(updated['user']['id'], data1['user']['id'])
        status, other, _ = self.req('/api/me', cookie=cookie2)
        self.assertEqual(status, 200)
        self.assertEqual(other['user']['name'], 'Usuario Dos')
        status, current, _ = self.req('/api/me', cookie=cookie1)
        self.assertEqual(status, 200)
        self.assertEqual(current['user']['name'], 'María López')


if __name__ == '__main__':
    unittest.main()
