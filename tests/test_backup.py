"""Verifica que la utilidad produce una copia SQLite íntegra."""

import sqlite3
import sys
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import backup_database


class DatabaseBackupTests(unittest.TestCase):
    def test_creates_integrity_checked_copy(self):
        with tempfile.TemporaryDirectory(prefix="travelsnap_backup_test_") as temp:
            root = Path(temp)
            source = root / "data" / "travelsnap.sqlite3"
            source.parent.mkdir()
            with closing(sqlite3.connect(source)) as db:
                db.execute("CREATE TABLE sample (value TEXT NOT NULL)")
                db.execute("INSERT INTO sample VALUES ('TravelSnap')")
                db.commit()
            backup_dir = root / "backups"
            with patch.object(backup_database, "SOURCE", source), patch.object(backup_database, "BACKUP_DIR", backup_dir):
                self.assertEqual(backup_database.main(), 0)
            copies = list(backup_dir.glob("travelsnap-*.sqlite3"))
            self.assertEqual(len(copies), 1)
            with closing(sqlite3.connect(copies[0])) as db:
                self.assertEqual(db.execute("PRAGMA integrity_check").fetchone()[0], "ok")
                self.assertEqual(db.execute("SELECT value FROM sample").fetchone()[0], "TravelSnap")


if __name__ == "__main__":
    unittest.main()
