#!/usr/bin/env python3
"""Prepare the four approved RGBA donor sprite packs for PJR's indexed 4bpp PNG pipeline.

This operates on the CI checkout, not on the checked-in source assets.
PJR's gbagfx rejects truecolor/RGBA PNGs.  The source donor files are
intentionally retained exactly, and image rendering remains an emulator QA gate.
"""
from __future__ import annotations

from collections import Counter
from pathlib import Path
from PIL import Image

ROOT = Path("graphics/pokemon")
EXTERNAL_DONORS = ("adnokana", "cheauking", "frytning", "mewsion")


def load_jasc(path: Path) -> list[tuple[int, int, int]]:
    rows = path.read_text().splitlines()
    if rows[:3] != ["JASC-PAL", "0100", "16"]:
        raise ValueError(f"Unexpected 16-colour donor palette: {path}")
    colors = [tuple(map(int, row.split())) for row in rows[3:19]]
    if len(colors) != 16 or any(len(c) != 3 or any(v > 255 or v < 0 for v in c) for c in colors):
        raise ValueError(f"Invalid GBA palette: {path}")
    return colors


def icon_colors(pixels: list[tuple[int, int, int, int]]) -> tuple[list[tuple[int, int, int]], int]:
    counts = Counter(rgb[:3] for rgb in pixels if rgb[3] >= 128)
    # Index zero is transparent. The icon RGB palette is provisional: the fixed
    # PJR icon-palIndex mapping must be inspected visually in the emulator.
    colors = [rgb for rgb, _ in counts.most_common(15)]
    return [(0, 0, 0)] + colors, len(counts)


def normalize(path: Path, kind: str, palette: list[tuple[int, int, int]] | None) -> None:
    with Image.open(path) as source:
        if source.size != ((32, 64) if kind == "icon" else (64, 64)):
            raise ValueError(f"Unexpected sprite size: {path}: {source.size}")
        if source.mode == "P" and (max(source.getdata()) < 16):
            print(f"PASS already indexed: {path}")
            return
        pixels = list(source.convert("RGBA").getdata())

    if palette is None:
        palette, colors_found = icon_colors(pixels)
    else:
        colors_found = len({p[:3] for p in pixels if p[3] >= 128})

    if len(palette) > 16:
        raise ValueError(f"More than 16 palette entries: {path}")
    # 4bpp index zero is transparent in the ROM, irrespective of the PNG alpha.
    # Use the exact donor JASC palette for front/back. Never blindly replace it
    # with an unrelated quantized palette (which would alter in-game colours).
    candidates = palette[1:]
    if not candidates:
        raise ValueError(f"Empty colour palette: {path}")
    cache: dict[tuple[int, int, int], int] = {}
    indices: list[int] = []
    worst_distance = 0
    for r, g, b, a in pixels:
        if a < 128:
            indices.append(0)
            continue
        rgb = (r, g, b)
        if rgb not in cache:
            index = 1 + min(
                range(len(candidates)),
                key=lambda i: sum((rgb[c] - candidates[i][c]) ** 2 for c in range(3)),
            )
            cache[rgb] = index
            target = palette[index]
            worst_distance = max(worst_distance, max(abs(rgb[c] - target[c]) for c in range(3)))
        indices.append(cache[rgb])

    indexed = Image.new("P", ((32, 64) if kind == "icon" else (64, 64)))
    indexed.putpalette([v for triplet in palette for v in triplet] + [0] * (768 - len(palette) * 3))
    indexed.putdata(indices)
    indexed.save(path, format="PNG", optimize=False)
    with Image.open(path) as verify:
        if verify.mode != "P" or max(verify.getdata()) >= 16:
            raise ValueError(f"4bpp sprite round-trip failed: {path}")
    print(f"PASS converted RGBA -> 4bpp indexed: {path}; "
          f"source visible RGB colours={colors_found}; max RGB channel delta={worst_distance}"
          + ("; icon palette visual QA still required" if kind == "icon" else ""))


def main() -> None:
    for name in EXTERNAL_DONORS:
        folder = ROOT / name
        palette = load_jasc(folder / "normal.pal")
        for kind in ("front", "back", "icon"):
            normalize(folder / f"{kind}.png", kind, None if kind == "icon" else palette)
    print("All four external donor packs are valid indexed PNG inputs for gbagfx.")


if __name__ == "__main__":
    main()
