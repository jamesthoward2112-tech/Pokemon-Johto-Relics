#!/usr/bin/env python3
"""Fit the original approved twin Chansey trainer picture inside its 64x64 slot.

Preserves the approved source picture and ALL existing 4bpp palette colours.
Only reduces/re-centres the composition, with nearest-neighbour pixel art scaling.
"""
from pathlib import Path
from PIL import Image
import hashlib

SOURCE = Path("graphics/trainers/front_pics/pru_chansey_twins.png")
QA = Path("PRU-QA")
QA.mkdir(exist_ok=True)

with Image.open(SOURCE) as file:
    art = file.copy()
assert art.mode == "P" and art.size == (64, 64), (art.mode, art.size)
assert len(art.getcolors()) <= 16, "Trainer artwork must be <=16 colours"
palette = art.getpalette()
transparency = art.info.get("transparency", 0)
assert transparency == 0, f"Expected index-0 transparency, got {transparency}"
( QA / "chansey-before.png").write_bytes(SOURCE.read_bytes())
# Index zero is the transparent GBA palette colour.
mask = Image.frombytes("L", art.size, bytes(255 if pixel else 0 for pixel in art.getdata()))
bbox = mask.getbbox()
assert bbox, "Chansey picture unexpectedly empty"
cropped = art.crop(bbox)
w, h = cropped.size
# Keep 4px side and bottom clear; limit tall art to 52px.
ratio = min(56 / w, 52 / h, 1)
dw, dh = max(1, round(w * ratio)), max(1, round(h * ratio))
if (dw, dh) != (w, h):
    cropped = cropped.resize((dw, dh), Image.Resampling.NEAREST)
canvas = Image.new("P", (64, 64), 0)
canvas.putpalette(palette)
x, y = (64 - dw) // 2, 60 - dh
canvas.paste(cropped, (x, y))
canvas.info["transparency"] = 0
canvas.save(SOURCE, transparency=0, optimize=False)
canvas.save(QA / "chansey-fitted.png", transparency=0, optimize=False)
canvas.resize((512, 512), Image.Resampling.NEAREST).save(QA / "chansey-fitted-preview.png", transparency=0)
assert canvas.getcolors() and len(canvas.getcolors()) <= 16
assert x >= 4 and (x + dw) <= 60 and y >= 4 and y + dh <= 60
print(f"PRU_CHANSEY_FIT_PASS: approved palette unchanged; original bounding box {bbox}; fitted sprite ({x},{y})-({x + dw},{y + dh})")
print("PRU_CHANSEY_FIT_SHA256:", hashlib.sha256(SOURCE.read_bytes()).hexdigest())
