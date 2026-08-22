from __future__ import annotations

import os
import time
from pathlib import Path


class FileSessionHandler:
    """File-backed session handler matching Laravel's lifecycle methods."""

    def __init__(self, path: str | Path, minutes: int) -> None:
        self.path = Path(path)
        self.minutes = minutes

    def open(self, save_path: str, session_name: str) -> bool:
        self.path.mkdir(parents=True, exist_ok=True)
        return True

    def close(self) -> bool:
        return True

    def read(self, session_id: str) -> str:
        path = self._session_path(session_id)
        if not path.is_file():
            return ""
        if path.stat().st_mtime < time.time() - self.minutes * 60:
            return ""
        return path.read_text(encoding="utf-8")

    def write(self, session_id: str, data: str) -> bool:
        path = self._session_path(session_id)
        self.path.mkdir(parents=True, exist_ok=True)
        temporary = path.with_name(f".{path.name}.tmp")
        temporary.write_text(data, encoding="utf-8")
        os.replace(temporary, path)
        return True

    def destroy(self, session_id: str) -> bool:
        self._session_path(session_id).unlink(missing_ok=True)
        return True

    def gc(self, lifetime: int) -> int:
        cutoff = time.time() - lifetime
        deleted = 0
        for path in self.path.iterdir() if self.path.is_dir() else ():
            if path.is_file() and path.stat().st_mtime <= cutoff:
                path.unlink()
                deleted += 1
        return deleted

    def _session_path(self, session_id: str) -> Path:
        if not session_id or Path(session_id).name != session_id:
            raise ValueError("Invalid session identifier.")
        return self.path / session_id
