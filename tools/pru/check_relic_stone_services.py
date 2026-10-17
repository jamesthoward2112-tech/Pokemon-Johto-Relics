#!/usr/bin/env python3
"""PRU regression gate for unified Relic evolutions, Goldenrod stones and move services."""
from pathlib import Path
import re

def read(path):
    return Path(path).read_text(encoding="utf-8")

base = Path("src/data/pokemon/species_info")
groups = {
    "gen_1_families.h": ["MYSTYNX", "ADNOKANA", "CHEAUKING"],
    "gen_2_families.h": [
        "FAERANIUM", "PYROCLAST", "FERALODON", "SUDOWARDEN",
        "KABLOWFISH", "SHUCKOLOSSE", "HERACURION", "SKARMADON",
        "DONPHALANX", "MILTITAN",
    ],
    "gen_3_families.h": [
        "VALKYVOIR", "SCEPTITAN", "SOLAZIKEN", "SWAMPLITH",
        "SKULBERUS", "GEMIGOYLE", "MAWYRM", "TORKALDERA",
        "CACTOMB", "TROPISAUR", "COELOSSUS",
    ],
}
for file, targets in groups.items():
    data = read(base / file)
    for target in targets:
        evo = f"{{EVO_ITEM, ITEM_ANCIENT_STONE, SPECIES_{target}, CONDITIONS({{IF_MIN_LEVEL, 45}})}}"
        assert data.count(evo) == 1, (file, target, "missing or duplicate stone evo")
for old in (
    "ITEM_ANCIENT_SHELL", "ITEM_FOSSIL_BARK", "ITEM_ANCIENT_TUSK",
    "ITEM_FROST_MIRROR", "ITEM_ANCIENT_HORN", "ITEM_ANCIENT_PLUME",
    "ITEM_ANCIENT_BELL",
):
    for file in groups:
        assert old not in read(base / file), (file, old)

enums = read("include/constants/pokemon.h")
engine = read("src/pokemon.c")
assert "IF_MIN_LEVEL," in enums
assert "case IF_MIN_LEVEL:" in engine
assert "GetMonData(mon, MON_DATA_LEVEL) >= params[i].arg1" in engine
# Keep the previously verified unique Eeveeon evolution and the Thunder Stone Frytning alternative.
gen1 = read(base / "gen_1_families.h")
assert "{EVO_ITEM, ITEM_ANCIENT_STONE, SPECIES_EEVEEON}" in gen1
assert "{EVO_ITEM, ITEM_THUNDER_STONE, SPECIES_FRYTNING}" in gen1

mart = read("data/maps/GoldenrodCity_DepartmentStore_2F_hns/scripts.inc")
assert mart.count(".2byte ITEM_ANCIENT_STONE") == 1
assert mart.count(".2byte ITEM_MOON_STONE") == 1
for legacy in (
    "ANCIENT_SHELL", "FOSSIL_BARK", "ANCIENT_TUSK", "FROST_MIRROR",
    "ANCIENT_HORN", "ANCIENT_PLUME", "ANCIENT_BELL",
):
    assert (".2byte ITEM_" + legacy) not in mart, legacy

relearner = read("src/move_relearner.c")
for category in ("EGG_MOVES", "TUTOR_MOVES"):
    assert f"if (!FlagGet(P_FLAG_{category}) && !P_ENABLE_MOVE_RELEARNERS)" not in relearner
assert "GetRelearnerEggMoves(boxmon" in relearner
assert "GetRelearnerTutorMoves(boxmon" in relearner
assert "sBulbasaurEggMoveLearnset[]" in read("src/data/pokemon/egg_moves.h")

items = read("src/data/items.h")
pattern = r'\[ITEM_(TM|HM)_([A-Z0-9_]+)\]\s*=\s*\{\s*\.name\s*=\s*ITEM_NAME\("([^"]+)"\)'
named = [(kind, name, value) for kind, name, value in re.findall(pattern, items) if name != "CASE"]
assert len(named) == 59, len(named)
for kind, name, value in named:
    assert value == name.replace("_", " "), (kind, name, value)
    assert len(value) <= 14, (kind, name, value)
assert "TM CASE" in items

print("PASS: 24 level-45 Ancient Stone Relic evolutions, Eevee/Frytning preserved,")
print("      legacy catalysts off Mart shelves, Moon/Ancient Stones available,")
print("      free Egg/Tutor eligibility gates removed, 59 TMs/HMs show move names.")
print("NOTE: Charizard permanent Relic evolution is not included: no target species exists.")
