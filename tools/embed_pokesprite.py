#!/usr/bin/env python3
"""Embed 381 vanilla Pokémon sprites from the owner's pinned PokéSprite fork."""
import base64
import json
from pathlib import Path
import sys

site=Path(sys.argv[1]); mapping=Path(sys.argv[2]); fork=Path(sys.argv[3])
html=site.read_text(encoding="utf-8")
marker='<script id="data" type="application/json">'
start=html.index(marker)+len(marker)
end=html.index("</script>",start)
data=json.loads(html[start:end]); mons={int(m["id"]):m for m in data["mons"]}
rows=json.loads(mapping.read_text(encoding="utf-8"))
errors=[]
for num,relative in rows:
    path=fork/relative
    if not path.is_file():
        errors.append((num,relative))
        continue
    raw=path.read_bytes()
    if not raw.startswith(b'\x89PNG\r\n\x1a\n'):
        errors.append((num,"not PNG: "+relative))
        continue
    m=mons[int(num)]
    m["image"]="data:image/png;base64,"+base64.b64encode(raw).decode("ascii")
    m["spriteSource"]="User PokéSprite fork at c5aaa610ff2acdf7fd8e2dccd181bca8be9fcb3e: "+relative+" (embedded)"
    m["art"]="Embedded"
if errors:
    raise SystemExit(f"Missing/invalid PokéSprite fork sprites ({len(errors)}): {errors[:30]}")
assert len(rows)==381,len(rows)
assert len(data["mons"])==444,len(data["mons"])
assert all(m.get("image","").startswith("data:image/png;base64,") for m in data["mons"])
site.write_text(html[:start]+json.dumps(data,ensure_ascii=False,separators=(",",":"))+html[end:],encoding="utf-8")
print(f"Embedded {len(rows)} vanilla sprites from the verified PokéSprite fork; all 444 Pokémon images self-contained.")
