from pathlib import Path
import orjson as json

STATE_DIR = Path("data/.state")
STATE_DIR.mkdir(parents=True, exist_ok=True)

def _path(name: str) -> Path:
    return STATE_DIR / f"{name}.json"

def load(name: str) -> dict:
    p = _path(name)
    if p.exists():
        return json.loads(p.read_bytes())
    return {}

def save(name: str, data: dict):
    _path(name).write_bytes(json.dumps(data))
