#!/usr/bin/env python3
"""Static PRU Johto Rocket trio scene regression check.

Checks the source-level scene contract. A green result is not a gameplay
emulator test; the workflow compiles the full HNS ROM separately.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read(rel):
    return (ROOT / rel).read_text()


def map_file(name):
    return json.loads(read(f"data/maps/{name}/map.json"))


def assert_actor(events, local_id, graphics):
    assert events[local_id - 1]["graphics_id"] == graphics, (local_id, graphics)


well = map_file("SlowpokeWell_B1F_hns")
well_script = read("data/maps/SlowpokeWell_B1F_hns/scripts.inc")
assert len(well["object_events"]) == 28
assert_actor(well["object_events"], 10, "OBJ_EVENT_GFX_JAMES_HNS")
assert_actor(well["object_events"], 11, "OBJ_EVENT_GFX_JESSIE_HNS")
assert_actor(well["object_events"], 28, "OBJ_EVENT_GFX_MON_BASE+SPECIES_MEOWTH")
assert well["object_events"][27]["flag"] == "FLAG_TEMP_1"
coords = {
    (ev["x"], ev["y"]) for ev in well["coord_events"]
    if ev.get("script") == "SlowpokeWell_B1F_EventScript_JessieJamesTrigger"
}
assert coords == {(26, 15), (27, 15), (28, 15)}, coords
assert "getplayerxy VAR_0x8004, VAR_0x8005" in well_script
assert "setobjectxy 10, VAR_0x8004, 8" in well_script
assert "setobjectxy 11, VAR_0x8006, 8" in well_script
assert "setobjectxy 28, VAR_0x8004, 7" in well_script
assert well_script.count("applymovement 28, ") >= 3
assert "trainerbattle_double TRAINER_GRUNT_21_HNS" in well_script
assert "setflag FLAG_PJR_JESSIE_JAMES_1_DEFEATED" in well_script
assert "removeobject 28" in well_script
assert "SlowpokeWell_B1F_EventScript_LegacyRocketRescue" in well_script
assert "SlowpokeWell_B1F_EventScript_Proton" in well_script

underground = map_file("GoldenrodCity_UndergroundSwitches_hns")
underground_script = read("data/maps/GoldenrodCity_UndergroundSwitches_hns/scripts.inc")
assert len(underground["object_events"]) == 11
assert_actor(underground["object_events"], 11, "OBJ_EVENT_GFX_MON_BASE+SPECIES_MEOWTH")
assert underground["object_events"][10]["flag"] == "FLAG_TEMP_1"
assert "trainerbattle_double TRAINER_GRUNT_10_HNS" in underground_script
assert "setflag FLAG_PJR_JESSIE_JAMES_2_DEFEATED" in underground_script
assert "applymovement 11, GoldenrodCity_UndergroundSwitches_Movement_MeowthRunIn" in underground_script
assert underground_script.count("removeobject 11") >= 2

radio = map_file("GoldenrodCity_RadioTower_4F_hns")
radio_script = read("data/maps/GoldenrodCity_RadioTower_4F_hns/scripts.inc")
assert_actor(radio["object_events"], 7, "OBJ_EVENT_GFX_MON_BASE+SPECIES_MEOWTH")
assert (radio["object_events"][6]["x"], radio["object_events"][6]["y"]) == (16, 11)
assert radio["object_events"][6]["flag"] == "FLAG_PJR_JESSIE_JAMES_3_DEFEATED"
assert radio_script.count("trainerbattle_double TRAINER_GRUNT_9_HNS") == 2
assert radio_script.count("removeobject 7") == 2

# The existing James trainer art is the PRL combined Jessie & James picture;
# their animated overworld pictures and Meowth source sprite are all retained.
party = read("src/data/trainers_hns.party")
gfx = read("src/data/graphics/trainers.h")
for trainer in ("TRAINER_GRUNT_21_HNS", "TRAINER_GRUNT_10_HNS", "TRAINER_GRUNT_9_HNS"):
    block = party.split(f"=== {trainer} ===", 1)[1].split("=== ", 1)[0]
    assert "Class: Jessie James Hns" in block, trainer
    assert "Pic: James Hns" in block, trainer
    assert "Double Battle: Yes" in block, trainer
assert 'graphics/trainers/front_pics/james_hns.4bpp.smol' in gfx
for filename in (
    "graphics/trainers/front_pics/james_hns.png",
    "graphics/trainers/front_pics/jessie_hns.png",
    "graphics/object_events/pics/people/rockets/james_hns.png",
    "graphics/object_events/pics/people/rockets/jessie_hns.png",
    "graphics/pokemon/meowth/overworld.png",
):
    assert (ROOT / filename).is_file(), filename

print("PASS: Slowpoke, Underground and Radio Tower Rocket trio scenes have PRL art, Meowth and persistent double-battle wiring.")
