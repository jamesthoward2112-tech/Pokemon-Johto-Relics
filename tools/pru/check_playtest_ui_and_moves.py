#!/usr/bin/env python3
"""Prevent regression of the 18-Oct PRU playtest fixes."""
from pathlib import Path
import re
import struct

def read(path):
    return Path(path).read_text(encoding="utf-8")

moves = read("src/data/moves_info.h")
old = 'PRL signature move.'
assert old.lower() not in moves.lower(), "generic PRL move placeholder still displayed"

# Only the five outstanding PRL literal placeholders needed replacement;
# check every one now carries real behaviour-specific copy.
descriptions = {
    "AMBER_BLADE": ("high-crit", "Defense", "criticalHitStage = 1"),
    "SUN_RITE": ("Speed", "blazing", "MOVE_EFFECT_SPD_PLUS_1"),
    "TECTONIC_TIDE": ("Defense", "tidal", "MOVE_EFFECT_DEF_MINUS_1"),
    "EPOCH_CRASH": ("Defense", "ancient", "MOVE_EFFECT_DEF_MINUS_1"),
    "RELIC_WISH": ("fairy", "ancient", "power = 100"),
}
for name, (word1, word2, mechanic) in descriptions.items():
    m = re.search(r"^\s*\[MOVE_" + name + r"\]\s*=\s*\{([\s\S]*?)^\s*\},", moves, re.M)
    assert m, name
    block = m.group(1)
    desc = re.search(r'\.description = COMPOUND_STRING\("([^"]+)"\)', block)
    assert desc and len(desc.group(1)) >= 25, name
    assert word1.lower() in desc.group(1).lower(), name
    assert word2.lower() in desc.group(1).lower(), name
    assert mechanic in block, name
# Remaining in-game custom moves must have their own description fields.
custom = moves.split("    [MOVE_AMBER_BLADE] =", 1)[1]
for match in re.finditer(r"^\s*\[MOVE_([A-Z0-9_]+)\]\s*=\s*\{([\s\S]*?)^\s*\},", custom, re.M):
    assert ".description = " in match.group(2), match.group(1)

custom_levels = read("src/data/pokemon/level_up_learnsets/pru.h")
skulberus = custom_levels.split("sSkulberusLevelUpLearnset[]", 1)[1].split("LEVEL_UP_END", 1)[0]
assert "LEVEL_UP_MOVE(0, MOVE_SHADOW_FANGS)" in skulberus, "missing Skulberus on-evolution attack"

ability = read("src/data/abilities.h")
assert 'COMPOUND_STRING("Dark moves strike first\\nat full HP.")' in ability

relearner = read("src/move_relearner.c")
assert "gMoveRelearnerState == MOVE_RELEARNER_LEVEL_UP_MOVES" in relearner
assert "GetBoxMonData(boxmon, MON_DATA_SPECIES_OR_EGG) == SPECIES_GARDEVOIR" in relearner
assert "priorityMoves[] = { MOVE_HYPER_VOICE, MOVE_ROUND }" in relearner
assert "currentLevel < requiredLevel || BoxMonKnowsMove(boxmon, move)" in relearner

# Original repo icons are already normalised to the shared GBA icon palettes.
slugs = ("champeon", "lepideon", "guardeon", "obsideon", "toxeon",
         "sphynxeon", "omeon", "drakeon", "eeveeon", "nimbeon")
gfx = read("src/data/graphics/pjr.h") + read("src/data/graphics/pru_pokemon.h")
sync = read("tools/pru/sync_prl_authoritative_sprites.py")
for slug in slugs:
    sym = slug.capitalize()
    expect = 'gMonIcon_' + sym + '[] = INCBIN_U8("graphics/pokemon/' + slug + '/icon.4bpp")'
    assert expect in gfx, f"party icon needs normalised GBA art: {slug}"
    path = Path("graphics/pokemon") / slug / "icon.png"
    data = path.read_bytes()
    assert data[:8] == b"\\x89PNG\\r\\n\\x1a\\n", slug
    width, height, depth, color_type, _compression, _filter, _interlace = struct.unpack(">IIBBBBB", data[16:29])
    assert (width, height) == (32, 64), (slug, width, height)
    assert color_type == 3 and depth <= 4, (slug, depth, color_type)
    assert f'"{slug}"' in sync, f"donor sync bypass missing {slug}"
assert 'kind == "Icon" and slug in NORMALIZED_EEVEE_ICONS' in sync

print("PRU_PLAYTEST_FIXES_PASS: 5 move descriptions, Skulberus evolution, voice relearning, Stygian Rush summary, 10 Eeveelution party icons")
