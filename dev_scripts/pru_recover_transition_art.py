#!/usr/bin/env python3
"""Recover missing PRL transition sprites from tracked trainer portraits.

Build-only fallback; if an original PRL transition source set exists, do not
overwrite it. Produces a 64x64 indexed PNG, a 32x32 BG tilemap and a 16-color
palette. It is *not* the original PRL artwork.
"""
from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageOps, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "graphics/battle_transitions/prl"
OUT.mkdir(parents=True, exist_ok=True)

def sprite(path):
    im = Image.open(ROOT / path).convert("RGBA")
    # Most Gen 3 trainer sprite PNGs are index-color with transparency in
    # the source or encoded as a solid top-left background.
    raw = Image.open(ROOT / path)
    if "transparency" not in raw.info and raw.mode == "P":
        rgba = Image.open(ROOT / path)
        rgba.putpalette(raw.getpalette())
        rgba.info["transparency"] = 0
        im = rgba.convert("RGBA")
    alpha = im.getchannel("A")
    bounds = alpha.getbbox()
    return im.crop(bounds) if bounds else im

def icon(name, sources, colors):
    path = OUT / f"{name}.png"
    tilemap = OUT / f"{name}.bin"
    palette = OUT / f"{name}.pal"
    if path.exists() and tilemap.exists() and palette.exists():
        print(f"Preserving original PRL art: {name}")
        return
    bg, outline, glow = colors
    im = Image.new("RGBA", (64,64), bg + (255,))
    draw = ImageDraw.Draw(im)
    draw.rounded_rectangle((2,2,61,61), radius=12, outline=glow + (255,), width=3)
    draw.rounded_rectangle((6,6,57,57), radius=8, outline=outline + (255,), width=2)
    draw.ellipse((7,47,57,59), fill=(0,0,0,110))
    for n, src in enumerate(sources):
        p = sprite(src)
        p.thumbnail((32,44),Image.Resampling.NEAREST)
        x = (2 if n == 0 else 32) + (30-p.width)//2
        y = 53-p.height
        im.alpha_composite(p, (x,y))
    # PNG with at most 16 colors, for GBA 4bpp tile converter.
    quant = im.convert("RGB").quantize(colors=16,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
    quant.save(path)
    # BG0 32x32 screen entries, palette bank 13, picture centred.
    import struct
    vals=[]
    for row in range(32):
        for col in range(32):
            tile = (row-8)*8+(col-12) if 8 <= row < 16 and 12 <= col < 20 else 0
            vals.append((13 << 12) | tile)
    tilemap.write_bytes(struct.pack("<1024H", *vals))
    # gbagfx auto-generates the corresponding .gbapal from PNG;
    # the .pal source ensures deterministic palette conversion.
    pal = quant.getpalette()[:48]
    palette.write_text("\n".join(f"{pal[i]} {pal[i+1]} {pal[i+2]}" for i in range(0,48,3))+"\n",encoding="utf-8")
    print(f"Reconstructed fallback {name} transition from in-repo trainer portraits")

icon("jessie_james", [
    "graphics/trainers/front_pics/jessie_hns.png",
    "graphics/trainers/front_pics/james_hns.png"
], ((36,26,69), (223,114,172), (253,223,97)))
icon("eevee_twins", [
    "graphics/trainers/front_pics/twins_hns.png",
    "graphics/trainers/front_pics/twins_hns.png"
], ((24,51,91), (137,201,254), (248,226,130)))
