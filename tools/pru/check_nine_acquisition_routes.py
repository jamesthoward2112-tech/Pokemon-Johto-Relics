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

# Actual shop endpoint, not just the global item definition.
# This source assertion establishes that the three items are in a live clerk's
# Goldenrod 2F inventory. Gameplay access and successful purchase remain ROM QA.
shop_script = (ROOT / "data/maps/GoldenrodCity_DepartmentStore_2F_hns/scripts.inc").read_text()
shop_map = json.loads((ROOT / "data/maps/GoldenrodCity_DepartmentStore_2F_hns/map.json").read_text())
clerk_script = "GoldenrodDeptStore2_EventScript_RockShop"
shop_table = "GoldenrodDeptStore2_RockShop"
advanced_table = "GoldenrodDeptStore2_RockShopFourBadges"
assert clerk_script in shop_script, "Goldenrod 2F Rock Shop clerk script disappeared"
clerk = shop_script.split(clerk_script + "::", 1)
assert len(clerk) == 2, "Goldenrod 2F shopkeeper definition disappeared"
assert ("pokemart " + shop_table) in clerk[1][:700], (
    "Goldenrod 2F shopkeeper no longer opens basic inventory"
)
assert ("pokemart " + advanced_table) in clerk[1][:1000], (
    "Goldenrod 2F shopkeeper no longer opens four-badge inventory"
)
assert "goto_if_set FLAG_BADGE04_GET" in clerk[1][:450]
basic = shop_script.split(shop_table + ":", 1)[1].split("pokemartlistend", 1)[0]
advanced = shop_script.split(advanced_table + ":", 1)[1].split("pokemartlistend", 1)[0]
for item in ("ITEM_FIRE_STONE", "ITEM_WATER_STONE"):
    assert ".2byte " + item in basic, f"Goldenrod basic Rock Shop missing {item}"
assert ".2byte ITEM_DEEP_SEA_SCALE" in advanced, "Goldenrod advanced Rock Shop missing Deep Sea Scale"
assert any(
    obj.get("script") == clerk_script and obj.get("flag") == "0"
    for obj in shop_map.get("object_events", [])
), "Goldenrod 2F clerk not freely visible on map"
held_config = (ROOT / "include/config/item.h").read_text()
assert "#define I_USE_EVO_HELD_ITEMS_FROM_BAG   TRUE" in held_config, (
    "Bag use of held evolution items disabled; Gorebyss direct-item route needs retesting"
)

print("PASS: nine acquisition targets retain evolution rules, initial wild sources, and item/engine/shop references")
print("NOTE: Mart/gift item accessibility, in-game evolution and caught-Dex registration require ROM QA")
