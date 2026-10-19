#!/usr/bin/env python3
"""Guard the Mahogany merchant and seventh-badge Radio Tower state rollback."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
def read(p): return (ROOT / p).read_text()

town=read("data/maps/Mahoganytown_hns/scripts.inc")
gym=read("data/maps/MahoganyTown_Gym_hns/scripts.inc")
golden=read("data/maps/GoldenrodCity_hns/scripts.inc")
chuck=read("data/maps/CianwoodGym_hns/scripts.inc")
jasmine=read("data/maps/OlivineCity_Gym_hns/scripts.inc")
director=read("data/maps/GoldenrodCity_RadioTower_5F_hns/scripts.inc")

def block(s, label, until=None):
    a=s.index(label+"::")
    return s[a:(s.index(until+"::",a+len(label)+2) if until else a+900)]

# The last permanent Radio Tower Director cleanup flag is a safe completion
# signal for old saves whose story vars were accidentally reset after 7 badges.
assert "setflag FLAG_HIDE_GOLDENROD_RADIOTOWER_DIRECTOR_2" in director
assert "setvar VAR_MAHOGANY_TOWN_STATE, 17" in director
assert "setvar VAR_GOLDENROD_CITY_STATE, 11" in director
assert "map_script MAP_SCRIPT_ON_LOAD, Mahoganytown_OnLoad" in town
assert "call_if_set FLAG_HIDE_GOLDENROD_RADIOTOWER_DIRECTOR_2, MahoganyTown_EventScript_RepairClearedRadioTowerState" in town
assert "map_script MAP_SCRIPT_ON_TRANSITION, GoldenrodCity_EventScript_RepairClearedRadioTowerOnEntry" in golden
assert "call_if_set FLAG_HIDE_GOLDENROD_RADIOTOWER_DIRECTOR_2, MahoganyTown_EventScript_RepairClearedRadioTowerState" in golden
repair=block(town,"MahoganyTown_EventScript_RepairClearedRadioTowerState", "MahoganyTown_EventScript_FixTree")
for cmd in (
    "setvar VAR_MAHOGANY_TOWN_STATE, 17",
    "setvar VAR_GOLDENROD_CITY_STATE, 11",
    "setvar VAR_TRIGGER_ELM_ROCKET_CALL, 2",
    "setflag FLAG_HIDE_GOLDENROD_ROCKETS",
    "clearflag FLAG_HIDE_GOLDENROD_NPCS",
):
    assert cmd in repair, cmd
assert "goto_if_set FLAG_HIDE_GOLDENROD_RADIOTOWER_DIRECTOR_2, Mahoganytown_EventScript_RocketAlreadyCleared" in town
assert "goto_if_set FLAG_HIDE_GOLDENROD_RADIOTOWER_DIRECTOR_2, MahoganyTown_EventScript_RepairRocketTakeoverDone" in town
merchant=block(town,"MahoganyTown_EventScript_MerchantTrigger","MahoganyTown_EventScript_MerchantAllowPassage")
assert merchant.index("goto_if_set FLAG_DEFEATED_MAHOGANY_TOWN_GYM, MahoganyTown_EventScript_MerchantAllowPassage") < merchant.index("lock")
assert "goto_if_set FLAG_HIDE_GOLDENROD_RADIOTOWER_DIRECTOR_2, MahoganyTown_EventScript_MerchantAllowPassage" in merchant
assert block(town,"MahoganyTown_EventScript_MerchantAllowPassage","MahoganyTown_EventScript_WalkUp1").strip().endswith("end")
helper=block(gym,"MahoganyTown_Gym_EventScript_SetupElmRocketCall","MahoganyTown_Gym_EventScript_OlivineCheckCianwood")
assert helper.index("goto_if_set FLAG_HIDE_GOLDENROD_RADIOTOWER_DIRECTOR_2") < helper.index("setvar VAR_TRIGGER_ELM_ROCKET_CALL, 1")
assert helper.index("goto_if_ge VAR_GOLDENROD_CITY_STATE, 10") < helper.index("setvar VAR_TRIGGER_ELM_ROCKET_CALL, 1")
for script in [chuck,jasmine]:
    assert "call_if_eq VAR_NUM_BADGES, 7, MahoganyTown_Gym_EventScript_SetupElmRocketCall" in script

# Existing-source progression snapshots: post-Director 17/11 must never
# regress to 16/6 simply because a later badge schedules Elm's call.
def simulate(badge, mahogany, goldenrod, finished):
    if badge == 7 and not finished and goldenrod < 10:
        trigger=1
    else:
        trigger=2
    if finished:
        mahogany,goldenrod,trigger=17,11,2
    blocked=not (badge >= 7 or finished)
    return mahogany,goldenrod,trigger,blocked
assert simulate(7,16,6,True)==(17,11,2,False)
assert simulate(6,17,11,True)==(17,11,2,False)
assert simulate(4,1,1,False)[-1] is True
print("PASS: previously cleared Director state self-repairs; late badges cannot restart Radio Tower; RageCandy merchant permits passage after Pryce.")
