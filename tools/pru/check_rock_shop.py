#!/usr/bin/env python3
"""Validate PRU's Goldenrod Rock Shop without claiming emulator gameplay.

Run from repository root:
    python3 tools/pru/check_rock_shop.py
"""
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = (ROOT / "data/maps/GoldenrodCity_DepartmentStore_2F_hns/scripts.inc").read_text()
FIRST_FLOOR = (ROOT / "data/maps/GoldenrodCity_DepartmentStore_1F_hns/scripts.inc").read_text()
MAP = json.loads((ROOT / "data/maps/GoldenrodCity_DepartmentStore_2F_hns/map.json").read_text())
ITEM_CONSTS = (ROOT / "include/constants/items.h").read_text()
ITEM_DATA = (ROOT / "src/data/items.h").read_text()


def stock(symbol):
    block = re.search(r"(?m)^" + re.escape(symbol) + r":\s*\n(.*?)^\s*pokemartlistend", SCRIPTS, re.S | re.M)
    assert block, f"Missing shop inventory: {symbol}"
    names = re.findall(r"\.2byte\s+(ITEM_[A-Z0-9_]+)", block.group(1))
    assert names, f"No items listed in {symbol}"
    assert len(names) == len(set(names)), f"Duplicate item in {symbol}"
    return set(names)


rock = stock("GoldenrodDeptStore2_RockShop")
supply = stock("GoldenrodDeptStore2_Pokemart")

required_stones = {
    "FIRE_STONE", "WATER_STONE", "THUNDER_STONE", "LEAF_STONE",
    "ICE_STONE", "MOON_STONE", "SUN_STONE", "SHINY_STONE",
    "DUSK_STONE", "DAWN_STONE", "OVAL_STONE",
}
required_trade = {
    "KINGS_ROCK", "METAL_COAT", "DRAGON_SCALE", "UPGRADE", "DUBIOUS_DISC",
    "PROTECTOR", "ELECTIRIZER", "MAGMARIZER", "PRISM_SCALE",
    "REAPER_CLOTH", "RAZOR_CLAW", "RAZOR_FANG",
    "DEEP_SEA_TOOTH", "DEEP_SEA_SCALE", "LINKING_CORD",
}
required_habitats = {"GALARICA_CUFF", "GALARICA_WREATH", "BLACK_AUGURITE", "PEAT_BLOCK"}
required_relics = {
    "ANCIENT_SHELL", "FOSSIL_BARK", "ANCIENT_TUSK", "FROST_MIRROR",
    "ANCIENT_HORN", "ANCIENT_PLUME", "ANCIENT_BELL",
}
required_special = {
    "EXPERT_BELT", "SILVER_POWDER", "SOFT_SAND", "HARD_STONE",
    "POISON_BARB", "DRAGON_FANG", "THICK_CLUB", "SPELL_TAG",
    "MIRACLE_SEED", "CHARCOAL", "MYSTIC_WATER",
}
expected = {"ITEM_" + x for x in (
    required_stones | required_trade | required_habitats
    | required_relics | required_special
)}
assert expected == rock, f"Rock Shop stock mismatch: missing={sorted(expected - rock)} unexpected={sorted(rock - expected)}"

expected_supplies = {
    "POKE_BALL", "GREAT_BALL", "ULTRA_BALL",
    "POTION", "SUPER_POTION", "HYPER_POTION", "MAX_POTION",
    "REVIVE", "ANTIDOTE", "PARALYZE_HEAL", "BURN_HEAL",
    "ICE_HEAL", "AWAKENING", "FULL_HEAL", "ESCAPE_ROPE",
    "REPEL", "SUPER_REPEL", "MAX_REPEL",
}
assert {"ITEM_" + x for x in expected_supplies} == supply, "Ordinary supplies changed or missing"
assert not rock & supply, "Duplicate ordinary and Rock Shop counter inventory"

# As PRL integration adds more species-specific items, extend the shop *without*
# relocating plot-specific key items or early access to Ancient Candy.
assert "ITEM_ANCIENT_RAINBOW_CREST" not in rock, "Story crest cannot be purchased"
assert "ITEM_ANCIENT_CANDY" not in rock, "Ancient Candy progression cannot be bypassed"
for item in sorted(rock | supply):
    assert re.search(r"\b" + item + r"\b", ITEM_CONSTS), f"Item enum missing: {item}"
    assert re.search(r"\[" + item + r"\]\s*=", ITEM_DATA) or (
        "PJR_CATALYST_ITEM(" + item in ITEM_DATA
    ), f"Item data missing: {item}"

rock_npcs = [e for e in MAP["object_events"] if e["script"] == "GoldenrodDeptStore2_EventScript_RockShop"]
supply_npcs = [e for e in MAP["object_events"] if e["script"] == "GoldenrodDeptStore2_EventScript_Clerk"]
assert len(rock_npcs) == 1 and len(supply_npcs) == 1, "Rock Shop or existing general clerk missing"
assert (rock_npcs[0]["x"], rock_npcs[0]["y"]) == (17, 11), "Rock Shop counter position changed"
assert (supply_npcs[0]["x"], supply_npcs[0]["y"]) == (14, 11), "General shop counter moved"
assert "pokemart GoldenrodDeptStore2_RockShop" in SCRIPTS, "Rock Shop purchase interaction missing"
assert "pokemart GoldenrodDeptStore2_Pokemart" in SCRIPTS, "Original supplies interaction missing"
assert "2F MARKET / ROCK SHOP" in SCRIPTS, "2F Rock Shop floor sign missing"
assert "2F MARKET / ROCK SHOP" in FIRST_FLOOR, "First-floor directory missing Rock Shop label"

print(f"PASS: Goldenrod 2F Rock Shop has {len(rock)} distinct evolution-related items")
print(f"PASS: Ordinary counter independently retains {len(supply)} supplies")
print("NOTE: NPC collision, item-sale behavior and evolution timing need emulator QA")
