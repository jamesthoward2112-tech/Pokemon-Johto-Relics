#!/usr/bin/env python3
"""Verify PRU custom backsprite grounding and exact indexed Swamplith icon colours."""
from pathlib import Path
import re
from PIL import Image

root = Path(__file__).resolve().parents[2]
species_file = (root / "src/data/pokemon/species_info/pru_custom.h").read_text()
pjr_file = (root / "src/data/pokemon/species_info/pjr_families.h").read_text()
icon_source = (root / "src/pokemon_icon.c").read_text()
graphics_source = (root / "src/data/graphics/pru_pokemon.h").read_text()

for species_id, sprite, slug in (
    ("VALKYVOIR", "Valkyvoir", "valkyvoir"),
    ("SWAMPLITH", "Swamplith", "swamplith"),
):
    match = re.search(r"\[SPECIES_" + species_id + r"\]\s*=\s*\{(.*?)\n\},", species_file, re.S)
    assert match, f"Missing PRU species: {species_id}"
    body = match.group(1)
    assert re.search(r"\.backPic\s*=\s*gMonBackPic_" + sprite + r",\s*\.backPicSize\s*=\s*MON_COORDS_SIZE\(64,\s*64\),\s*\.backPicYOffset\s*=\s*6\b", body), f"{species_id} back offset regressed"
    png = root / "graphics/pokemon/prl_authoritative" / slug / "back.png"
    img = Image.open(png).convert("RGBA")
    assert img.size == (64, 64), f"Wrong back image size for {species_id}"
    print(f"{species_id}: offset=6, alpha bounds={img.getchannel('A').getbbox()}")

swamp = re.search(r"\[SPECIES_SWAMPLITH\]\s*=\s*\{(.*?)\n\},", species_file, re.S).group(1)
assert ".iconSprite = gMonIcon_Swamplith, .iconPalIndex = 0" in swamp  # 3-bit SpeciesInfo field
assert "static u8 GetPruCustomIconPaletteIndex" in icon_source
assert "if (species == SPECIES_SWAMPLITH)" in icon_source
assert "return 8;" in icon_source
assert 'graphics/pokemon/prl_authoritative/swamplith/icon.4bpp' in graphics_source
assert "{ sPRUSwamplithIconPalette, POKE_ICON_BASE_PAL_TAG + 8 }" in icon_source
palette_block = re.search(r"static const u16 sPRUSwamplithIconPalette\[16\]\s*=\s*\{(.*?)\};", icon_source, re.S)
assert palette_block, "Missing custom Swamplith palette"
actual = [tuple(map(int, p)) for p in re.findall(r"RGB\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)", palette_block.group(1))]
im = Image.open(root / "graphics/pokemon/prl_authoritative/swamplith/icon.png")
assert im.mode == "P" and im.size == (32, 64)
colors = im.getpalette()
expected = [tuple(colors[3*i + j] // 8 for j in range(3)) for i in range(16)]
assert actual == expected, f"Swamplith icon palette drift: expected {expected}; actual {actual}"
print("Swamplith: green PRL icon exact 16-color donor palette PASS")

# Audit the larger legacy issue without automatically moving flying/levitating sprites.
for label, data in (("new PRU", species_file), ("PJR custom", pjr_file)):
    offsets = re.findall(r"\.backPicYOffset\s*=\s*(\d+)\b", data)
    print(f"{label}: {len(offsets)} explicit numeric back offsets, {offsets.count('0')} still at zero; manual placement review needed")
print("PRU_CUSTOM_SPRITE_GROUNDING_PASS")
