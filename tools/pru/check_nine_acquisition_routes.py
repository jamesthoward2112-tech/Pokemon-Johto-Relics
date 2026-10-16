#!/usr/bin/env python3
"""PRU source regression gate: nine nonlegendary acquisition routes.

This is NOT an in-game proof of reachability, item purchase or evolution.
Run from repository root: python3 tools/pru/check_nine_acquisition_routes.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GEN1 = (ROOT / "src/data/pokemon/species_info/gen_1_families.h").read_text()
GEN3 = (ROOT / "src/data/pokemon/species_info/gen_3_families.h").read_text()
ITEMS = (ROOT / "src/data/items.h").read_text()
CONFIG = (ROOT / "include/config/pokemon.h").read_text()
ENGINE = (ROOT / "src/evolution_scene.c").read_text()
WILD = json.loads((ROOT / "src/data/wild_encounters.json").read_text())


def species_section(text, species):
    marker = "[SPECIES_" + species + "] ="
    start = text.find(marker)
    assert start >= 0, f"Missing source species: {species}"
    end = text.find("\n    [SPECIES_", start + len(marker))
    if end == -1:
        end = len(text)
    return text[start:end]


def evolution(source, base, required):
    section = species_section(source, base)
    pos = section.find(".evolutions =")
    assert pos >= 0, f"No evolution table for {base}"
    table = section[pos:]
    for snippet in required:
        assert snippet in table, f"{base} evolution table missing {snippet}"


# Use exact source definitions. Do not replace branching rules with wild evolved forms.
evolution(GEN1, "TYROGUE", [
    "SPECIES_HITMONLEE, CONDITIONS({IF_ATK_GT_DEF})",
    "SPECIES_HITMONTOP, CONDITIONS({IF_ATK_EQ_DEF})",
])
evolution(GEN1, "EEVEE", [
    "{EVO_ITEM, ITEM_WATER_STONE, SPECIES_VAPOREON}",
    "{EVO_ITEM, ITEM_FIRE_STONE, SPECIES_FLAREON}",
    "SPECIES_ESPEON, CONDITIONS({IF_MIN_FRIENDSHIP, FRIENDSHIP_EVO_THRESHOLD}, {IF_NOT_TIME, TIME_NIGHT})",
    "SPECIES_UMBREON, CONDITIONS({IF_MIN_FRIENDSHIP, FRIENDSHIP_EVO_THRESHOLD}, {IF_TIME, TIME_NIGHT})",
])
evolution(GEN3, "WURMPLE", [
    "{EVO_LEVEL, 7, SPECIES_CASCOON, CONDITIONS({IF_PID_UPPER_MODULO_10_LT, 5})}",
])
evolution(GEN3, "NINCADA", [
    "{EVO_LEVEL, 20, SPECIES_NINJASK}",
    "EVO_SPLIT_FROM_EVO, SPECIES_NINJASK, SPECIES_SHEDINJA",
])
evolution(GEN3, "CLAMPERL", [
    "{EVO_ITEM, ITEM_DEEP_SEA_SCALE, SPECIES_GOREBYSS}",
])

assert "#define P_SHEDINJA_BALL" in CONFIG, "No Shedinja Poké Ball generation rule"
split_fn = ENGINE.split("static void CreateShedinja(", 1)
assert len(split_fn) == 2, "Shedinja creation missing"
for condition in ("gPlayerPartyCount < GetMaxPartySize()", "ITEM_POKE_BALL", "RemoveBagItem(ball, 1)"):
    assert condition in split_fn[1][:2100], f"Shedinja creation missing {condition}"

for stone in ("FIRE_STONE", "WATER_STONE"):
    body = ITEMS.split("[ITEM_" + stone + "] =", 1)
    assert len(body) == 2, f"Missing item {stone}"
    assert ".fieldUseFunc = ItemUseOutOfBattle_EvolutionStone" in body[1][:500], f"{stone} is not party-usable"
scale = ITEMS.split("[ITEM_DEEP_SEA_SCALE] =", 1)
assert len(scale) == 2 and ".effect = gItemEffect_EvoItem" in scale[1][:800], "Deep Sea Scale item effect absent"

# Every target's pre-evolution must have at least one *real* Johto/Kanto HNS wild path.
expected = {
    "TYROGUE": "MAP_MT_MORTAR_1F_SOUTH_HNS",
    "EEVEE": "MAP_ROUTE29_HNS",
    "WURMPLE": "MAP_ILEX_FOREST_HNS",
    "NINCADA": "MAP_UNION_CAVE_1F_HNS",
    "CLAMPERL": "MAP_ROUTE20_HNS",
}
main = next(g for g in WILD["wild_encounter_groups"] if g["label"] == "gWildMonHeaders")
for species, map_id in expected.items():
    found = []
    for encounter in main["encounters"]:
        if not encounter.get("map", "").endswith("_HNS"):
            continue
        for field in ("land_mons", "water_mons", "rock_smash_mons", "fishing_mons"):
            for mon in encounter.get(field, {}).get("mons", []):
                if mon["species"] == "SPECIES_" + species:
                    found.append(encounter["map"])
    assert map_id in found, f"{species} lost required wild source {map_id}"

print("PASS: nine acquisition targets retain evolution rules, initial wild sources, and item/engine definitions")
print("NOTE: Mart/gift item accessibility, in-game evolution and caught-Dex registration require ROM QA")
