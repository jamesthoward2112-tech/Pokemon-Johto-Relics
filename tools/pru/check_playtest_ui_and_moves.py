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

# One shared window fix must cover every original and custom ability, not
# shorten just the ability observed during the playtest.
summary = read("src/pokemon_summary_screen.c")
assert "WrapPruAbilitySummaryText(gAbilitiesInfo[ability].description)" in summary
assert "GetStringWidth(FONT_SMALL_NARROWER, &sPruAbilitySummaryText[lineStart], 0)" in summary
assert "PrintTextOnWindowWithFont(windowId, sPruAbilitySummaryText, 0, 14, 0, 0, FONT_SMALL_NARROWER)" in summary
assert "sPruAbilitySummaryText[breakAt] = CHAR_NEWLINE" in summary
assert "if (IS_HNS)" in summary
assert re.search(r"\[PSS_DATA_WINDOW_INFO_ABILITY\][\s\S]*?\.height = 5,[\s\S]*?\.baseBlock = 503", summary)
assert re.search(r"\[PSS_DATA_WINDOW_INFO_MEMO\][\s\S]*?\.baseBlock = 593", summary)
abilities = read("src/data/abilities.h")
assert len(re.findall(r"^\s*\[ABILITY_[A-Z0-9_]+\]\s*=", abilities, re.M)) > 300

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
    assert data[:8] == bytes.fromhex("89504e470d0a1a0a"), slug
    width, height, depth, color_type, _compression, _filter, _interlace = struct.unpack(">IIBBBBB", data[16:29])
    assert (width, height) == (32, 64), (slug, width, height)
    assert color_type == 3 and depth in (1, 2, 4, 8), (slug, depth, color_type)
    assert f'"{slug}"' in sync, f"donor sync bypass missing {slug}"
assert 'kind == "Icon" and slug in NORMALIZED_EEVEE_ICONS' in sync


# Temporary Feralodon art must be the full in-repo Mega Feraligatr sprite set.
# No new species ID, base Feraligatr art or battle mechanics are modified.
for asset in ("front.4bpp.smol", "back.4bpp.smol", "normal.gbapal", "shiny.gbapal", "icon.4bpp"):
    assert "graphics/pokemon/feraligatr/mega/" + asset in gfx
assert 'PRU_VISUAL_OVERRIDES = {"feralodon"}' in sync
assert 'if slug in PRU_VISUAL_OVERRIDES:' in sync
for kind in ("front", "back", "icon"):
    path = Path("graphics/pokemon/feraligatr/mega") / (kind + ".png")
    data = path.read_bytes()
    assert data[:8] == bytes.fromhex("89504e470d0a1a0a"), kind
    w, h, depth, color_type, *_ = struct.unpack(">IIBBBBB", data[16:29])
    assert (w, h) == ((32, 64) if kind == "icon" else (64, 64)), (kind, w, h)
    assert color_type == 3 and depth in (1, 2, 4, 8), (kind, depth, color_type)

# Every PRU canonical species and move must use the same display casing.
for gen in (1, 2, 3):
    families = read(f"src/data/pokemon/species_info/gen_{gen}_families.h")
    names = re.findall(r'\.speciesName\s*=\s*_\("([^"]+)"\)', families)
    assert names and not any(n.isupper() and any(c.isalpha() for c in n) for n in names), f"Gen {gen} species uppercase"
pjr = read("src/data/pokemon/species_info/pjr_families.h")
assert '.speciesName = _("Scarabub")' in pjr
assert '"Feralodon", CRY_FERALIGATR' in pjr
# PJR's six Red Relics use macro-injected species names, not .speciesName
# literals.  Existing save party data stores NOXICHU in uppercase; the
# GetBoxMonData nickname getter will now show Noxichu, not NOXICHU.
red_relics = {
    "EDENSAUR": "Edensaur", "CHARAXIS": "Charaxis",
    "FORTOTOISE": "Fortotoise", "KHANG": "Khang",
    "NOLAX": "Nolax", "NOXICHU": "Noxichu",
}
for token, proper in red_relics.items():
    expr = rf'PJR_RED_SPECIES\(SPECIES_{token},[\s\S]*?ABILITY_[A-Z0-9_]+, "([^"]+)", CRY_'
    matched = re.search(expr, pjr)
    assert matched and matched.group(1) == proper, (token, matched.group(1) if matched else None)

assert not re.search(r'\.speciesName\s*=\s*_\("[A-Z][A-Z -]*"\)', pjr), "legacy PJR allcaps species"
pru = read("src/data/pokemon/species_info/pru_custom.h")
assert '.speciesName = _("Valkiri")' in pru
assert '.speciesName = _("Skulberus")' in pru
move_names = re.findall(r'\.name\s*=\s*(?:COMPOUND_STRING|_)\("([^"]+)"\)', moves)
assert len(move_names) >= 950
assert all(name == name.upper() for name in move_names), "some move names not uppercase"
pokemon_src = read("src/pokemon.c")
assert "PruNameMatchesSpeciesIgnoringCase" in pokemon_src
assert "field == MON_DATA_NICKNAME && boxMon->language == GAME_LANGUAGE" in pokemon_src
assert "if (PruNameMatchesSpeciesIgnoringCase(data, canonical))" in pokemon_src
assert "PruNameMatchesSpeciesIgnoringCase(GetSpeciesName(oldSpecies), gStringVar1)" in pokemon_src
assert "lines < 3" in summary


# Scary Face is a true Fear-causing status move, not a mere Speed drop.
scary_face = re.search(r'^\s*\[MOVE_SCARY_FACE\]\s*=\s*\{([\s\S]*?)^\s*\},', moves, re.M)
assert scary_face, "Scary Face missing"
assert ".effect = EFFECT_SPEED_DOWN_2" in scary_face.group(1), "Speed -2 must remain"
assert "inflicts Fear on the target" in scary_face.group(1), "missing Fear tooltip"
battle_script = read("data/battle_scripts_1.s")
fear_part = battle_script.split("BattleScript_StatDownEnd::", 1)[1].split("BattleScript_MirrorArmorReflect::", 1)[0]
assert "MOVE_SCARY_FACE, BattleScript_PRU_ScaryFaceFear" in fear_part
assert "seteffectprimary BS_ATTACKER, BS_TARGET, MOVE_EFFECT_FEAR" in fear_part

# User-approved PRU Boomburst: 140 BP spread sound to both enemies only.
# TARGET_FOES_AND_ALLY must never be used here; TARGET_BOTH is enemy-only.
boomburst = re.search(r'^\s*\[MOVE_BOOMBURST\]\s*=\s*\{([\s\S]*?)^\s*\},', moves, re.M)
assert boomburst, "BOOMBURST missing"
bb = boomburst.group(1)
assert ".power = 140" in bb
assert ".target = TARGET_BOTH" in bb
assert ".target = TARGET_FOES_AND_ALLY" not in bb
assert ".soundMove = TRUE" in bb
assert "Blasts both opposing foes" in bb
battle_util = read("src/battle_util.c")
assert "case TARGET_BOTH:" in battle_util and "case TARGET_FOES_AND_ALLY:" in battle_util

print("PRU_PLAYTEST_FIXES_PASS: 5 move descriptions, Skulberus evolution, voice relearning, Stygian Rush summary, 10 Eeveelution party icons")
