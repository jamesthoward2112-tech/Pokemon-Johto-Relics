#!/usr/bin/env python3
"""PRU regression gate for unified Relic evolutions, Goldenrod stones and move services."""
from pathlib import Path
import re

def read(path):
    return Path(path).read_text(encoding="utf-8")

base = Path("src/data/pokemon/species_info")
groups = {
    "gen_1_families.h": ["MYSTYNX", "ADNOKANA", "CHEAUKING", "CHARAXIS", "EDENSAUR", "FORTOTOISE", "KHANG", "NOLAX"],
    "gen_2_families.h": [
        "FAERANIUM", "PYROCLAST", "FERALODON",
        "KABLOWFISH", "SHUCKOLOSSE", "HERACURION", "SKARMADON",
        "DONPHALANX", "MILTITAN",
    ],
    "gen_3_families.h": [
        "VALKYVOIR", "SCEPTITAN", "SOLAZIKEN", "SWAMPLITH",
        "SKULBERUS", "GEMIGOYLE", "MAWYRM", "TORKALDERA",
        "CACTOMB", "TROPISAUR",
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
assert "#define SPECIES_CHARAXIS" in read("include/constants/species.h")
assert "PJR_RED_SPECIES(SPECIES_CHARAXIS" in read("src/data/pokemon/species_info/pjr_families.h")
assert "ABILITY_GALE_WINGS, \"Charaxis\"" in read("src/data/pokemon/species_info/pjr_families.h")
assert "IF_MIN_LEVEL," in enums
assert "case IF_MIN_LEVEL:" in engine
assert "GetMonData(mon, MON_DATA_LEVEL) >= params[i].arg1" in engine
pokedex = read("src/pokedex_plus_hgss.c")
assert "case IF_MIN_LEVEL:" in pokedex
assert 'COMPOUND_STRING("Lv ")' in pokedex
# Pikachu has a separate Moon Stone route, not subject to the Relic Lv45 restriction.
assert "{EVO_ITEM, ITEM_MOON_STONE, SPECIES_NOXICHU}" in read(base / "gen_1_families.h")
assert "{EVO_ITEM, ITEM_THUNDER_STONE, SPECIES_RAICHU" in read(base / "gen_1_families.h")
# Excluded or independent species are not ordinary stone evolutions.
assert "SPECIES_COELOSSUS" not in read(base / "gen_3_families.h")
assert "SPECIES_SUDOWARDEN" not in read(base / "gen_2_families.h")
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

# Check the entire HNS machine catalogue without changing non-HNS engine labels.
import subprocess
subprocess.run(["python3", "tools/pru/check_tm_full_names.py"], check=True)

print("PASS: 27 canonical level-45 Ancient Stone Relic evolutions, Eevee/Frytning preserved,")
print("      legacy catalysts off Mart shelves, Moon/Ancient Stones available,")
print("      free Egg/Tutor eligibility gates removed, 92 TMs and 8 HMs show number and move.")
print("PASS: Charizard -> Charaxis and 26 other canonical Lv45 Ancient Stone evolutions.")
print("PASS: Pikachu -> Noxichu by Moon Stone; separate Coelossus and removed Sudowarden.")
