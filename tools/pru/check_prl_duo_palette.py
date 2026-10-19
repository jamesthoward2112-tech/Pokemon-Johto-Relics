#!/usr/bin/env python3
"""Regression: 4bpp Jessie & James intro must not erase white as BG index zero.

Requires tools/pru/install_prl_duo_assets.py to run first (as in CI).
Verifies BOTH asset semantics and preservation of the donor's other colours.
"""
from collections import Counter
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[2]
folder = ROOT / "graphics/battle_transitions/prl"
tiles = (folder / "jessie_james.4bpp").read_bytes()
tilemap = (folder / "jessie_james.bin").read_bytes()
palette_bytes = (folder / "jessie_james.gbapal").read_bytes()
assert len(tiles) == 16384 and len(tilemap) == 2048 and len(palette_bytes) == 32
palette = struct.unpack("<16H", palette_bytes)
assert palette[0] == palette[14] == 0x0000, "Transparent/black index mismatch"
assert palette[15] == 0x77BD, "Near-white highlight no longer visible"
assert len(set(palette)) == 15, "A donor colour was lost in the remap"
indices = Counter(n for b in tiles for n in (b & 15, b >> 4))
assert indices[0] == 0, "A GBA-transparent nibble remains in full-screen artwork"
assert indices[15] > 0, "White pixels missing from tile graphics"
map_entries = struct.unpack("<1024H", tilemap)
assert all((m >> 12) == 13 and (m & 1023) < 512 for m in map_entries)
print(f"PASS: Jessie & James transition has {indices[15]} opaque white pixel "
      f"references, 15/15 original visible colours, zero transparent pixels.")
