#!/usr/bin/env python3
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRS = {".git", ".venv", "dist", "build", "__pycache__", ".ruff_cache", ".pytest_cache", ".mypy_cache", ".tmp"}


def is_packaged(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    if EXCLUDED_DIRS.intersection(rel.parts):
        return False
    return path.is_file() and not path.name.endswith("Zone.Identifier") and path.suffix not in {".pyc", ".zip"}


def main() -> int:
    subprocess.run([sys.executable, str(ROOT / "scripts/validate.py")], check=True)
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    out = ROOT / "dist" / f"agent-forge-{version}.zip"
    out.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(ROOT.rglob("*")):
            if is_packaged(p):
                z.write(p, Path("agent-forge") / p.relative_to(ROOT))
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
