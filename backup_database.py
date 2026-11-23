"""Crea una copia consistente de la base de datos SQLite local."""

from datetime import datetime
from contextlib import closing
from pathlib import Path
import sqlite3
import sys

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "data" / "travelsnap.sqlite3"
BACKUP_DIR = ROOT / "backups"


def main() -> int:
    if not SOURCE.is_file():
        print(f"No existe la base de datos: {SOURCE}", file=sys.stderr)
        return 1
    BACKUP_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")
    destination = BACKUP_DIR / f"travelsnap-{timestamp}.sqlite3"
    try:
        with closing(sqlite3.connect(SOURCE)) as source, closing(sqlite3.connect(destination)) as target:
            source.backup(target)
            target.commit()
            result = target.execute("PRAGMA integrity_check").fetchone()[0]
            if result != "ok":
                raise sqlite3.DatabaseError(f"integrity_check: {result}")
    except Exception as error:
        destination.unlink(missing_ok=True)
        print(f"No se pudo completar la copia: {error}", file=sys.stderr)
        return 1
    print(f"Copia verificada: {destination}")
    print("Para recuperarla, detén el servidor y sigue docs/MANTENIMIENTO.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
