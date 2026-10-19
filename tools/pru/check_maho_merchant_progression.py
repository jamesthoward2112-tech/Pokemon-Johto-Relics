#!/usr/bin/env python3
"""Regression: recovered Radio Tower story must pass Route 42->Mahogany for old saves."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
def read(p): return (ROOT / p).read_text()
town = read("data/maps/Mahoganytown_hns/scripts.inc")
gym = read("data/maps/MahoganyTown_Gym_hns/scripts.inc")
golden = read("data/maps/GoldenrodCity_hns/scripts.inc")
chuck = read("data/maps/CianwoodGym_hns/scripts.inc")
jasmine = read("data/maps/OlivineCity_Gym_hns/scripts.inc")
director = read("data/maps/GoldenrodCity_RadioTower_5F_hns/scripts.inc")
route42 = read("data/maps/Route42_hns/map.json")

def block(s, label, until=None):
    a=s.index(label+"::")
    return s[a:(s.index(until+"::",a+len(label)+2) if until else a+1000)]

# The exact affected 19 Oct save has Mahogany=16, Goldenrod=6, wing=2,
# Elm trigger=2, and NO TRAINER_ARCHER_HNS flag. The previous slot was 17/11.
# Keep these anonymised field values, NEVER commit the user save itself.
assert '"map": "MAP_MAHOGANYTOWN_HNS"' in route42
assert '"x": 93' in route42
assert "setvar VAR_LUGIA_OR HOOH" not in director  # spelling guard
assert "setvar VAR_LUGIA_OR_HOOH, 1" in director
assert "setvar VAR_LUGIA_OR_HOOH, 2" in director
assert "setvar VAR_MAHOGANY_TOWN_STATE, 17" in director
assert "setvar VAR_GOLDENROD_CITY_STATE, 11" in director
assert "map_script MAP_SCRIPT_ON_LOAD, Mahoganytown_OnLoad" in town
onload=block(town, "Mahoganytown_OnLoad", "MahoganyTown_EventScript_RepairRocketTakeoverTrigger")
for wing in (1,2):
    assert f"call_if_eq VAR_LUGIA_OR_HOOH, {wing}, MahoganyTown_EventScript_RestoreAfterArcher" in onload
# Do not call trainerflag on map loading. The affected save lacks that flag.
assert "checktrainerflag TRAINER_ARCHER_HNS" not in town
assert "checktrainerflag TRAINER_ARCHER_HNS" not in gym
assert "call MahoganyTown_EventScript_RepairClearedRadioTowerState" in golden
repair=block(town,"MahoganyTown_EventScript_RepairClearedRadioTowerState","MahoganyTown_EventScript_FixTree")
for wing in (1,2):
    assert f"goto_if_eq VAR_LUGIA_OR_HOOH, {wing}, MahoganyTown_EventScript_RestoreAfterArcher" in repair
for cmd in (
    "setvar VAR_MAHOGANY_TOWN_STATE, 17",
    "setvar VAR_GOLDENROD_CITY_STATE, 11",
    "setvar VAR_TRIGGER_ELM_ROCKET_CALL, 2",
    "setflag FLAG_HIDE_GOLDENROD_ROCKETS",
    "clearflag FLAG_HIDE_GOLDENROD_NPCS",
):
    assert cmd in repair,cmd
for label,until,target in (
    ("MahoganyTown_EventScript_RepairRocketTakeoverTrigger","MahoganyTown_EventScript_RepairClearedRadioTowerState","MahoganyTown_EventScript_RepairRocketTakeoverDone"),
    ("Mahoganytown_EventScript_RocketTrigger","Mahoganytown_EventScript_RocketAlreadyCleared","Mahoganytown_EventScript_RocketAlreadyCleared"),
    ("MahoganyTown_EventScript_MerchantTrigger","MahoganyTown_EventScript_MerchantAllowPassage","MahoganyTown_EventScript_MerchantAllowPassage"),
    ("MahoganyTown_EventScript_Merchant","MahoganyTown_EventScript_MerchantRefused","MahoganyTown_EventScript_MerchantAfter"),
):
    s=block(town,label,until)
    for wing in (1,2): assert f"goto_if_eq VAR_LUGIA_OR_HOOH, {wing}, {target}" in s
helper=block(gym,"MahoganyTown_Gym_EventScript_SetupElmRocketCall","MahoganyTown_Gym_EventScript_OlivineCheckCianwood")
for wing in (1,2):
    assert f"goto_if_eq VAR_LUGIA_OR_HOOH, {wing}, MahoganyTown_Gym_EventScript_RocketCallAlreadyCleared" in helper
assert "goto_if_ge VAR_GOLDENROD_CITY_STATE, 10" in helper
assert "goto_if_set FLAG_DEFEATED_MAHOGANY_TOWN_GYM, MahoganyTown_EventScript_MerchantAllowPassage" in town
for script in (chuck,jasmine):
    assert "call_if_eq VAR_NUM_BADGES, 7, MahoganyTown_Gym_EventScript_SetupElmRocketCall" in script

def simulate(wing,mahogany,goldenrod,elm):
    # No wing choice before Director = NEVER skip the storyline.
    if wing in (1,2): return 17,11,2,True
    return mahogany,goldenrod,elm,False
assert simulate(2,16,6,2)==(17,11,2,True)  # uploaded save
assert simulate(2,17,11,2)==(17,11,2,True) # previous save slot
assert simulate(1,16,6,2)==(17,11,2,True)
assert simulate(0,1,1,0)==(1,1,0,False)   # fresh story remains intact
print("PASS: Route42/Mahogany old-save recovery uses Director wing and cannot rerun Rocket takeover")
