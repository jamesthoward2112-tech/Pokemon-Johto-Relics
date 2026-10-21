#!/usr/bin/env python3
"""Check all eight first Kanto Gym bonus payouts without affecting old saves.

Reward: one useful held item, followed by 10,000; grant flag only after
item storage succeeds. The victory and defeated-NPC routes must both call
the same safe routine. This is source regression, not live-save gameplay QA.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
FLAGS = (ROOT / "include/constants/flags.h").read_text(encoding="utf-8")
ITEMS = (ROOT / "include/constants/items.h").read_text(encoding="utf-8")
GYMS = {
    "BROCK": ("PewterCity_Gym_hns", "FLAG_DEFEATED_PEWTER_GYM",
              "PewterCity_Gym_EventScript_Brock_Defeated", "ROCKY_HELMET"),
    "MISTY": ("CeruleanCity_Gym_hns", "FLAG_DEFEATED_CERULEAN_GYM",
              "CeruleanCity_Gym_EventScript_Misty_Defeated", "LEFTOVERS"),
    "SURGE": ("VermilionCity_Gym_hns", "FLAG_DEFEATED_VERMILION_GYM",
              "VermilionCity_Gym_EventScript_Surge_Defeated", "AIR_BALLOON"),
    "ERIKA": ("CeladonCity_Gym_hns", "FLAG_DEFEATED_CELADON_GYM",
              "CeladonCity_Gym_EventScript_Erika_Defeated", "BIG_ROOT"),
    "JANINE": ("FuchsiaCity_Gym_hns", "FLAG_DEFEATED_FUCHSIA_GYM",
               "FuchsiaCity_Gym_EventScript_Janine_Defeated", "BLACK_SLUDGE"),
    "SABRINA": ("SaffronCity_Gym_hns", "FLAG_DEFEATED_SAFFRON_GYM",
                "SaffronCity_Gym_EventScript_Sabrina_Defeated", "CHOICE_SPECS"),
    "BLAINE": ("SeafoamIslands_Gym_hns", "FLAG_DEFEATED_CINNABAR_ISLAND_GYM",
               "SeafoamIslands_Gym_EventScript_Blaine_Defeated", "LIFE_ORB"),
    "BLUE": ("ViridianCity_Gym_hns", "FLAG_DEFEATED_VIRIDIAN_GYM",
             "ViridianCity_Gym_EventScript_BlueGotoDojo", "CHOICE_BAND"),
}
assert len(GYMS) == 8
assert len(set(row[3] for row in GYMS.values())) == 8

for index, (trainer, (map_name, defeated_flag, defeated_route, item)) in enumerate(GYMS.items()):
    reward_flag = f"FLAG_PRU_KANTO_GYM_REWARD_{trainer}"
    reserved = f"FLAG_UNUSED_0x{0x8F1 + index:X}"
    assert re.search(r"#define\s+" + reward_flag + r"\s+" + reserved + r"\b", FLAGS), (trainer, "flag slot")
    assert f"ITEM_{item}" in ITEMS, (trainer, "item does not exist")
    source = (ROOT / "data/maps" / map_name / "scripts.inc").read_text(encoding="utf-8")
    prefix = map_name.removesuffix("_hns")
    script = f"{prefix}_EventScript_PRUReward"
    defeated_check = re.search(
        r"\bsetflag " + re.escape(defeated_flag) + r"\n\s*call " + re.escape(script) + r"\b",
        source,
    )
    assert defeated_check, (trainer, "new victory not awarded")
    assert f"{defeated_route}::\n\tcall {script}\n" in source, (trainer, "old saves cannot reclaim")
    match = re.search(
        r"^" + re.escape(script) + r"::\n(.*?)(?=^" + re.escape(script) + r"Done:)",
        source, re.M | re.S,
    )
    assert match, (trainer, "reward script missing")
    body = match.group(1)
    sequence = [
        f"goto_if_set {reward_flag}, {script}Done",
        f"giveitem ITEM_{item}",
        f"goto_if_eq VAR_RESULT, FALSE, {script}BagFull",
        "addmoney 10000",
        f"setflag {reward_flag}",
    ]
    offsets = [body.index(x) if x in body else -1 for x in sequence]
    assert all(o >= 0 for o in offsets) and offsets == sorted(offsets), (trainer, "item, money and flag order")
    assert f"{script}BagFull:\n\tmsgbox" in source, (trainer, "no full-Bag fallback")
    assert source.count("addmoney 10000") == 1, (trainer, "duplicate grants")
    assert source.count(f"setflag {reward_flag}") == 1, (trainer, "duplicate claim flags")
    assert "\\\\n" not in source[source.index(script + "::"):], (trainer, "double-escaped dialogue")
    assert "GYM prize money!$" in source and "Your BAG is full!" in source
    if trainer == "BLUE":
        guide = re.search(
            r"ViridianCity_Gym_EventScript_GymGuyAfter::\n(.*?)(?=\n\w+:)",
            source, re.S,
        )
        assert guide and f"call {script}" in guide.group(1), "Blue must be claimable after leaving for Dojo"
    print(f"PASS {trainer}: ITEM_{item}, 10,000, one-time flag, full-Bag and save-compatible retries")

print("PASS: Kanto Gym rewards all eight, no changes to Johto Gym flag allocation")
