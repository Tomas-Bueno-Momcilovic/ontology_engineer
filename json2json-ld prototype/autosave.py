from pathlib import Path
from datetime import datetime

MAX_FILES = 5
ROOT = Path("autosaves")
ROOT.mkdir(exist_ok=True)
LAST = ROOT / "last.txt"

class AutoSaver:
    def __init__(self, folder: Path = ROOT, cap: int = MAX_FILES):
        self.folder = folder
        self.cap = cap

    def save(self, raw: str) -> Path:
        name = self.folder / f"{datetime.now():%Y%m%d%H%M%S}.json"
        name.write_text(raw)
        self._trim()
        LAST.write_text(str(name))
        return name

    def load_last(self) -> str | None:
        if LAST.exists():
            p = Path(LAST.read_text())
            if p.exists():
                return p.read_text()
        return None

    def _trim(self) -> None:
        files = sorted(self.folder.glob("*.json"))
        for f in files[:-self.cap]:
            f.unlink()
