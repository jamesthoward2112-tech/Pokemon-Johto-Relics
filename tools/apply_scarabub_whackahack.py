from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "pjr_whackahack" / "scarabub_xiros_source.png"
FRONT = ROOT / "graphics" / "pokemon" / "pjr_locked" / "scarabub" / "front.png"

src = Image.open(SOURCE).convert("RGBA")
assert src.size == (39, 44)

old = Image.open(FRONT)
palette_bytes = old.getpalette()
palette = [tuple(palette_bytes[i:i + 3]) for i in range(0, 48, 3)]

def nearest(rgb):
    return min(
        range(1, 16),
        key=lambda i: sum((rgb[j] - palette[i][j]) ** 2 for j in range(3)),
    )

out = Image.new("P", (64, 64), 0)
out.putpalette(palette_bytes)
sp = src.load()
op = out.load()

# Keep the submitted pixel art at native size; only convert its palette and
# position it on the GBA 64x64 front-sprite canvas.
ox, oy = 12, 15
for y in range(src.height):
    for x in range(src.width):
        r, g, b, a = sp[x, y]
        if a:
            op[ox + x, oy + y] = nearest((r, g, b))

out.save(FRONT, transparency=0)
print(f"Wrote {FRONT}")
