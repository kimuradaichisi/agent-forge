#!/usr/bin/env python3
from pathlib import Path
import subprocess, zipfile
ROOT=Path(__file__).resolve().parents[1]
subprocess.run(['python3',str(ROOT/'scripts/validate.py')],check=True)
out=ROOT.parent/f'agent-forge-{(ROOT/"VERSION").read_text().strip()}.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
    for p in ROOT.rglob('*'):
        if p.is_file() and '.git' not in p.parts: z.write(p,Path('agent-forge')/p.relative_to(ROOT))
print(out)
