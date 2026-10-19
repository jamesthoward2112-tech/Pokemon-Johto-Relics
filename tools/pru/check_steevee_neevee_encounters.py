#!/usr/bin/env python3
"""Source regression for the five playable PRL Steevee/Neevee double battles."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
def read(path):
    return (ROOT / path).read_text()
def team_levels(party, name):
    expression = rf"^=== {name} ===\s*$(.*?)(?=^=== TRAINER_|\Z)"
    found = re.search(expression, party, re.M | re.S)
    assert found, name
    assert "Class: Twins Hns" in found.group(1)
    assert "Double Battle: Yes" in found.group(1)
    return [int(x) for x in re.findall(r"^Level:\s*(\d+)", found.group(1), re.M)]

slots = {
    "Route37": ("TRAINER_STEEVE_NEEVEE_ROUTE37_HNS", [(13,29), (14,29)], [30,30,31,32], "TRAINER_STEEVE_NEEVEE_ROUTE3_HNS"),
    "Route47": ("TRAINER_STEEVE_NEEVEE_ROUTE47_HNS", [(83,29), (84,29)], [38,38,39,40], "TRAINER_STEEVE_NEEVEE_SS_ANNE_HNS"),
    "Route44": ("TRAINER_STEEVE_NEEVEE_ROUTE44_HNS", [(65,15), (66,15)], [44,44,45,45,46,47], "TRAINER_STEEVE_NEEVEE_TOWER_HNS"),
    "Route3": ("TRAINER_STEEVE_NEEVEE_KANTO_ROUTE3_HNS", [(33,3), (34,3)], [61,61,62,62,63,64], "TRAINER_STEEVE_NEEVEE_ROUTE23_HNS"),
}
party = read("src/data/trainers_hns.party")
opponents = read("include/constants/opponents_hns.h")
battle = read("src/battle_setup.c")
transition = read("src/battle_transition.c")
for area,(alias,coords,levels,original) in slots.items():
    entry = json.loads(read(f"data/maps/{area}_hns/map.json"))
    script = read(f"data/maps/{area}_hns/scripts.inc")
    assert f"#define {alias} " in opponents and original in opponents.split(f"#define {alias} ",1)[1].splitlines()[0],alias
    assert team_levels(party,original)==levels,(area,team_levels(party,original))
    # Actual map block passability, not just non-overlap: prevent spawning
    # recurring trainers on impassable cliffs/water (Route 44 originally did).
    layout = next(
        item for item in json.loads(read("data/layouts/layouts.json"))["layouts"]
        if item["id"] == entry["layout"]
    )
    tiles = (ROOT / layout["blockdata_filepath"]).read_bytes()
    assert len(tiles) == layout["width"] * layout["height"] * 2, area
    for x, y in coords:
        assert 0 <= x < layout["width"] and 0 <= y < layout["height"], (area,x,y)
        offset = (y * layout["width"] + x) * 2
        block = int.from_bytes(tiles[offset:offset + 2], "little")
        assert (block >> 10) & 3 == 0, (area,x,y,"blocked collision")
        assert block >> 12 in (3,4), (area,x,y,"unexpected elevation")
    for name,xy in zip(("Steevee","Neevee"),coords):
        label=f"{area}_EventScript_{name}"
        obj=[o for o in entry["object_events"] if o["script"]==label]
        assert len(obj)==1,(area,label)
        event=obj[0]
        assert (event["x"],event["y"])==xy,(area,name)
        assert event["graphics_id"]=="OBJ_EVENT_GFX_TWIN_HNS",(area,name)
        assert event["flag"]=="0",(area,name)
        assert event["trainer_type"]=="TRAINER_TYPE_NORMAL",(area,name)
        assert f"{label}::" in script
        section=script.split(f"{label}::",1)[1].split("\n\tend",1)[0]
        assert f"trainerbattle_double {alias}," in section,(area,name)
        assert "Route104_Text_GinaNotEnoughMons" in section,(area,name)
    assert "STEEVEE:" in script and "NEEVEE:" in script,area
    assert f"case {original}:" in battle, original
assert "TRAINER_ANN_AND_ANNE_HNS" not in read("data/maps/Route37_hns/scripts.inc")
assert "return B_TRANSITION_EEVEE_TWINS;" in battle
assert "Task_PRL_EeveeTwins" in transition
for ext in ("4bpp", "bin", "gbapal"):
    assert f'graphics/battle_transitions/prl/eevee_twins.{ext}' in transition
assert "tools/pru/install_prl_duo_assets.py" in read(".github/workflows/pru-valkiri-final-build.yml")
assert team_levels(party,"TRAINER_ANN_AND_ANNE_HNS")==[30,30]  # original donor data retained

# Dragon's Den adds a fifth visit with its own trainer flag (679), rather than
# recycling Lea/Pia's defeated flag (393) or any of the four other visits.
den_map = json.loads(read("data/maps/DragonsDen_Cavern_hns/map.json"))
den_script = read("data/maps/DragonsDen_Cavern_hns/scripts.inc")
den_id = "TRAINER_STEEVE_NEEVEE_DRAGONS_DEN_HNS"
assert f"#define {den_id}     679" in opponents
assert "#define TRAINERS_COUNT_HNS                       680" in opponents
assert "case TRAINER_STEEVE_NEEVEE_DRAGONS_DEN_HNS:" in battle
assert team_levels(party, den_id) == [53,51,50,50,52,52]
den_team = party.split(f"=== {den_id} ===",1)[1]
assert "Drakeon @ Sitrus Berry" in den_team
assert "Name: STEEVEE" in den_team
for name, xy in (("Steevee",(7,31)),("Neevee",(7,32))):
    label = f"DragonsDen_Cavern_EventScript_{name}"
    actors = [o for o in den_map["object_events"] if o["script"] == label]
    assert len(actors) == 1, (name, actors)
    assert (actors[0]["x"],actors[0]["y"]) == xy
    assert actors[0]["graphics_id"] == "OBJ_EVENT_GFX_TWIN_HNS"
    assert actors[0]["trainer_type"] == "TRAINER_TYPE_NORMAL"
    assert f"trainerbattle_double {den_id}," in den_script.split(label+"::",1)[1].split("\n\tend",1)[0]
assert "DragonsDen_Cavern_EventScript_TwinLea" not in read("data/maps/DragonsDen_Cavern_hns/map.json")
assert "DragonsDen_Cavern_EventScript_TwinPia" not in read("data/maps/DragonsDen_Cavern_hns/map.json")
assert "TRAINER_LEA_AND_PIA_HNS" in opponents and team_levels(party,"TRAINER_LEA_AND_PIA_HNS") == [48,53,48,53]
assert "STEEVEE:" in den_script and "NEEVEE:" in den_script and "DRAKEON" in den_script

print("PRU_EEVEE_TWINS_PASS: five distinct save-stable double battles, Dragon\u0027s Den Drakeon, map NPCs, escalating teams, PRL intro")
