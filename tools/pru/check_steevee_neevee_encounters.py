#!/usr/bin/env python3
"""Source regression for the four playable PRL Steevee/Neevee double battles."""
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
    "Route44": ("TRAINER_STEEVE_NEEVEE_ROUTE44_HNS", [(61,13), (62,13)], [44,44,45,45,46,47], "TRAINER_STEEVE_NEEVEE_TOWER_HNS"),
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
print("PRU_EEVEE_TWINS_PASS: four distinct save-stable double battles, map NPCs, escalating teams, PRL transition wiring")
