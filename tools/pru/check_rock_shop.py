#!/usr/bin/env python3
"""Source-only PRU Goldenrod 2F Rock Shop staged inventory regression gate.

This validates item IDs, inventory membership, clerk scripts and badge paths,
not gameplay collision, story flag timing or the compiled ROM.
"""
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = (ROOT / "data/maps/GoldenrodCity_DepartmentStore_2F_hns/scripts.inc").read_text()
DIRECTORY = (ROOT / "data/maps/GoldenrodCity_DepartmentStore_1F_hns/scripts.inc").read_text()
MAP = json.loads((ROOT / "data/maps/GoldenrodCity_DepartmentStore_2F_hns/map.json").read_text())
ITEM_IDS = (ROOT / "include/constants/items.h").read_text()
ITEM_DATA = (ROOT / "src/data/items.h").read_text()


def stock(label):
    match = re.search(r"(?m)^" + re.escape(label) + r":\s*\n(.*?)^\s*pokemartlistend", SCRIPT, re.S | re.M)
    assert match, f"Missing stock list: {label}"
    items = re.findall(r"\.2byte\s+(ITEM_[A-Z0-9_]+)", match.group(1))
    assert items and len(items) == len(set(items)), f"Empty/duplicate items: {label}"
    return set(items)


def names(csv):
    return {"ITEM_" + name for name in csv.split()}


initial = stock("GoldenrodDeptStore2_RockShop")
four = stock("GoldenrodDeptStore2_RockShopFourBadges")
eight = stock("GoldenrodDeptStore2_RockShopEightBadges")
supplies = stock("GoldenrodDeptStore2_Pokemart")

basics = names("FIRE_STONE WATER_STONE THUNDER_STONE LEAF_STONE MOON_STONE SUN_STONE")
mid = names("""
ICE_STONE SHINY_STONE DUSK_STONE DAWN_STONE OVAL_STONE
KINGS_ROCK METAL_COAT DRAGON_SCALE UPGRADE DEEP_SEA_TOOTH DEEP_SEA_SCALE LINKING_CORD
EXPERT_BELT SILVER_POWDER SOFT_SAND HARD_STONE POISON_BARB
DRAGON_FANG THICK_CLUB SPELL_TAG MIRACLE_SEED CHARCOAL MYSTIC_WATER
""")
late = names("""
DUBIOUS_DISC PROTECTOR ELECTIRIZER MAGMARIZER PRISM_SCALE REAPER_CLOTH
RAZOR_CLAW RAZOR_FANG GALARICA_CUFF GALARICA_WREATH BLACK_AUGURITE PEAT_BLOCK
ANCIENT_SHELL FOSSIL_BARK ANCIENT_TUSK FROST_MIRROR ANCIENT_HORN
ANCIENT_PLUME ANCIENT_BELL
""")
assert len(basics) == 6 and len(mid) == 23 and len(late) == 19
assert initial == basics, f"Early inventory is not only basic stones: {sorted(initial ^ basics)}"
assert four == basics | mid, f"Four-badge inventory mismatch: {sorted(four ^ (basics | mid))}"
assert eight == basics | mid | late, f"Eight-badge inventory mismatch: {sorted(eight ^ (basics | mid | late))}"
assert (len(initial), len(four), len(eight)) == (6, 29, 48)
assert not (initial & late or four & late), "Late-game special/Relic items sold before eight badges"
assert "ITEM_ANCIENT_RAINBOW_CREST" not in eight, "The story crest must remain unavailable"
assert "ITEM_ANCIENT_CANDY" not in eight, "Ancient Candy must not be sold"

ordinary = names("""
POKE_BALL GREAT_BALL ULTRA_BALL POTION SUPER_POTION HYPER_POTION
MAX_POTION REVIVE ANTIDOTE PARALYZE_HEAL BURN_HEAL ICE_HEAL
AWAKENING FULL_HEAL ESCAPE_ROPE REPEL SUPER_REPEL MAX_REPEL
""")
assert supplies == ordinary, "Existing general goods clerk inventory changed"
assert not (supplies & eight), "Evolution stock duplicated at general clerk"

clerk = "GoldenrodDeptStore2_EventScript_RockShop"
branch = SCRIPT.split(clerk + "::", 1)
assert len(branch) == 2, "Missing Rock Shop clerk event"
logic = branch[1].split("GoldenrodDeptStore2_Text_RockShopWelcome:", 1)[0]
assert "goto_if_set FLAG_BADGE08_GET, GoldenrodDeptStore2_EventScript_RockShopAllStock" in logic
assert "goto_if_set FLAG_BADGE04_GET, GoldenrodDeptStore2_EventScript_RockShopExpandedStock" in logic
for label in ("GoldenrodDeptStore2_RockShop", "GoldenrodDeptStore2_RockShopFourBadges", "GoldenrodDeptStore2_RockShopEightBadges"):
    assert "pokemart " + label in logic, f"Shop selector cannot reach {label}"
assert logic.index("FLAG_BADGE08_GET") < logic.index("FLAG_BADGE04_GET"), "Badge checks ordered incorrectly"
assert "pokemart GoldenrodDeptStore2_Pokemart" in SCRIPT, "General shop lost interaction"
assert "2F MARKET / ROCK SHOP" in SCRIPT and "2F MARKET / ROCK SHOP" in DIRECTORY

rock_npcs = [e for e in MAP["object_events"] if e["script"] == clerk]
regular_npcs = [e for e in MAP["object_events"] if e["script"] == "GoldenrodDeptStore2_EventScript_Clerk"]
assert len(rock_npcs) == 1 and len(regular_npcs) == 1, "Clerk duplicated or removed"
assert (rock_npcs[0]["x"], rock_npcs[0]["y"]) == (17, 11), "Rock clerk misplaced"
assert (regular_npcs[0]["x"], regular_npcs[0]["y"]) == (14, 11), "Ordinary clerk displaced"
assert rock_npcs[0]["flag"] == "0", "Rock Shop clerk hidden by an event flag"

for item in eight | supplies:
    assert re.search(r"\b" + item + r"\b", ITEM_IDS), f"Missing item ID: {item}"
    assert re.search(r"\[" + item + r"\]\s*=", ITEM_DATA) or (
        "PJR_CATALYST_ITEM(" + item in ITEM_DATA
    ), f"Missing item definition: {item}"

print("PASS: Goldenrod Rock Shop stock staged 6 / 29 / 48 at arrival / 4 / 8 badges")
print("PASS: no early Relic catalysts, story items or Ancient Candy")
print("PASS: regular shop and both NPCs preserved")
print("NOTE: actual purchases, badge unlocking and item usage still require ROM/emulator QA")
