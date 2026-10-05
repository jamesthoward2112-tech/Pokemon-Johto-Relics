"""Rebuild the PJR front sprites sourced from Pokémon Insurgence without squashing.

The published Insurgence battlers are 2x nearest-neighbour renders.  We crop the
actual opaque artwork, return it to its native pixel grid, uniformly fit it into
the 64x64 GBA front-sprite frame, then remap to the already-locked PJR palette.
Back sprites/icons/palettes are deliberately untouched.
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "assets" / "insurgence_front_sources"
TARGET_ROOT = ROOT / "graphics" / "pokemon" / "pjr_locked"

# These five current PJR fronts are the Insurgence-derived imports that need the
# crop/scale repair.  Feralodon is the later locked Mega-Y visual and Heracurion
# uses the normal Mega Heracross asset, so neither is overwritten here.
SOURCES = {
    "miltitan": "miltitan_donor.png",
    "sudowarden": "sudowarden_donor.png",
    "donphalanx": "donphalanx_donor.png",
    "faeranium": "faeranium_donor.png",
    "pyroclast": "pyroclast_donor.png",
}

MAX_W = 64
MAX_H = 60
BOTTOM_MARGIN = 1

def load_jasc_palette(path: Path):
    lines = [x.strip() for x in path.read_text(encoding="ascii").splitlines() if x.strip()]
    assert lines[:2] == ["JASC-PAL", "0100"], path
    count = int(lines[2])
    assert 2 <= count <= 16, (path, count)
    cols = [tuple(map(int, line.split())) for line in lines[3:3 + count]]
    assert len(cols) == count
    # GBA OBJ palettes always have 16 slots. Index 0 is transparent even when
    # the donor palette stores a visible RGB value there.
    cols.extend([(0, 0, 0)] * (16 - len(cols)))
    return cols

def palette_bytes(cols):
    out = []
    for r, g, b in cols:
        out.extend([r, g, b])
    out.extend([0] * (768 - len(out)))
    return out

def fit_size(w, h):
    scale = min(MAX_W / w, MAX_H / h)
    return max(1, round(w * scale)), max(1, round(h * scale))

def convert_one(name, source_name):
    src = Image.open(SOURCE_DIR / source_name).convert("RGBA")
    bbox = src.getchannel("A").getbbox()
    if not bbox:
        raise ValueError(f"{name}: source has no opaque pixels")
    art = src.crop(bbox)

    # Insurgence wiki battlers are published at exactly 2x their pixel grid.
    if art.width % 2 or art.height % 2:
        raise ValueError(f"{name}: unexpected donor dimensions {art.size}")
    art = art.resize((art.width // 2, art.height // 2), Image.Resampling.NEAREST)

    new_w, new_h = fit_size(art.width, art.height)
    art = art.resize((new_w, new_h), Image.Resampling.NEAREST)

    target_dir = TARGET_ROOT / name
    colors = load_jasc_palette(target_dir / "normal.pal")
    out = Image.new("P", (64, 64), 0)
    out.putpalette(palette_bytes(colors))
    src_px = art.load()
    dst_px = out.load()

    def nearest(rgb):
        return min(
            range(1, 16),
            key=lambda i: sum((rgb[c] - colors[i][c]) ** 2 for c in range(3)),
        )

    ox = (64 - new_w) // 2
    oy = 64 - BOTTOM_MARGIN - new_h
    for y in range(new_h):
        for x in range(new_w):
            r, g, b, a = src_px[x, y]
            if a:
                dst_px[ox + x, oy + y] = nearest((r, g, b))

    target = target_dir / "front.png"
    out.save(target, transparency=0)
    print(f"{name}: donor {bbox[2]-bbox[0]}x{bbox[3]-bbox[1]} -> native {bbox[2]//2-bbox[0]//2}x{bbox[3]//2-bbox[1]//2} -> GBA {new_w}x{new_h}")

for species, source in SOURCES.items():
    convert_one(species, source)
