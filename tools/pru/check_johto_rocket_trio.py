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
# Template actors must spawn close enough to render when the trigger fires.
assert (well["object_events"][9]["x"], well["object_events"][9]["y"]) == (28, 13)
assert (well["object_events"][10]["x"], well["object_events"][10]["y"]) == (27, 13)
assert (well["object_events"][27]["x"], well["object_events"][27]["y"]) == (27, 12)
coords = {
    (ev["x"], ev["y"]) for ev in well["coord_events"]
    if ev.get("script") == "SlowpokeWell_B1F_EventScript_JessieJamesTrigger"
}
assert coords == {(26, 15), (27, 15), (28, 15)}, coords
assert "getplayerxy VAR_0x8004, VAR_0x8005" in well_script
assert "setobjectxy 10, VAR_0x8004, 13" in well_script
assert "setobjectxy 11, VAR_0x8006, 13" in well_script
assert "setobjectxy 28, VAR_0x8004, 12" in well_script
assert well_script.count("applymovement 28, ") == 2
approach_steps = well_script.split("SlowpokeWell_B1F_Movement_JessieJamesRunIn:\n", 1)[1].split("\tstep_end", 1)[0]
assert approach_steps == "\twalk_faster_down\n", approach_steps
assert "SlowpokeWell_B1F_Movement_JessieJamesRunOut" not in well_script
assert "applymovement 10, SlowpokeWell_B1F_Movement_JessieJamesRunOut" not in well_script
assert "fadescreen FADE_TO_BLACK\n\tremoveobject 10\n\tremoveobject 11\n\tremoveobject 28" in well_script
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
for local_id, x in ((5, 17), (2, 18), (7, 19)):
    actor = radio["object_events"][local_id - 1]
    assert (actor["x"], actor["y"]) == (x, 7)
    assert actor["flag"] == "FLAG_TEMP_1"
    assert actor["trainer_type"] == "TRAINER_TYPE_NONE"
    assert actor["movement_type"] == "MOVEMENT_TYPE_FACE_LEFT"
stair_tiles = {(10, 5), (11, 5), (9, 6), (10, 6), (11, 6), (9, 7), (10, 7)}
actual_tiles = {(e["x"], e["y"]) for e in radio["coord_events"] if e.get("script") == "GoldenrodCity_RadioTower_4F4_EventScript_JessieJamesTrigger"}
assert actual_tiles == stair_tiles
assert "MAP_SCRIPT_ON_LOAD, GoldenrodCity_RadioTower_4F4_EventScript_JessieJamesLoad" in radio_script
assert "GoldenrodCity_RadioTower_4F4_EventScript_JessieJamesLoad::\n\tsetflag FLAG_TEMP_1" in radio_script
assert "checktrainerflag TRAINER_GRUNT_9_HNS" in radio_script
assert "cleartrainerflag TRAINER_GRUNT_9_HNS" not in radio_script
assert radio_script.count("trainerbattle_double TRAINER_GRUNT_9_HNS") == 1
# Validate every tile of the approach AND retreat against map collision bits,
# including the final position. Static source text alone previously missed this.
import struct
layout = (ROOT / "data/layouts/GoldenrodCity_RadioTower_4F_hns/map.bin").read_bytes()
assert len(layout) == 1024
for x in range(12, 22):
    word, = struct.unpack_from("<H", layout, (32*7+x)*2)
    assert (word & 0xC00) == 0 and (word >> 12) == 3, (x, 7, hex(word))
for name, direction, count in (("Approach", "walk_faster_left", 5), ("RunOffscreen", "walk_faster_right", 7)):
    seq = radio_script.split(f"GoldenrodCity_RadioTower_4F4_Movement_{name}:\n", 1)[1].split("\tstep_end", 1)[0]
    assert seq.count("\t" + direction + "\n") == count, (name, seq)
trigger = radio_script.split("GoldenrodCity_RadioTower_4F4_EventScript_JessieJamesTrigger::", 1)[1].split("GoldenrodRaidoTower4_EventScript_Grunt28::", 1)[0]
assert "removeobject 5\n\tremoveobject 2\n\tremoveobject 7\n\tclearflag FLAG_TEMP_1\n\taddobject 5\n\taddobject 2\n\taddobject 7" in trigger
assert trigger.index("applymovement 5,") < trigger.index("applymovement 2,") < trigger.index("applymovement 7,")
retreat = radio_script.split("GoldenrodCity_RadioTower_4F4_EventScript_JessieJamesAfterBattle::", 1)[1].split("GoldenrodCity_RadioTower_4F4_EventScript_JessieJamesAlreadyDefeated::", 1)[0]
assert "FADE_TO_BLACK" not in retreat
assert retreat.index("setflag FLAG_PJR_JESSIE_JAMES_3_DEFEATED") < retreat.index("applymovement 7,")
assert retreat.index("applymovement 7,") < retreat.index("applymovement 2,") < retreat.index("applymovement 5,")
for id in (2, 5, 7):
    assert f"removeobject {id}" in retreat
    assert f"applymovement {id}, GoldenrodCity_RadioTower_4F4_Movement_RunOffscreen" in retreat
assert "releaseall" in retreat

# Jessie and James retain their trainer/overworld art; Meowth uses the normal
# species overworld sheet, so these scenes do not alter wild Meowth.
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

# PRL's approved duo-introduction art and transition routing.
transition_ids = read("include/battle_transition.h")
transition_src = read("src/battle_transition.c")
battle_setup = read("src/battle_setup.c")
for token in ("B_TRANSITION_JESSIE_JAMES", "B_TRANSITION_EEVEE_TWINS"):
    assert token in transition_ids, token
    assert token in transition_src, token
for asset in ("jessie_james", "eevee_twins"):
    for suffix in ("4bpp", "bin", "gbapal"):
        assert f'graphics/battle_transitions/prl/{asset}.{suffix}' in transition_src
assert (ROOT / "assets/prl_duo_20261011.json").is_file()
assert (ROOT / "tools/pru/install_prl_duo_assets.py").is_file()
for trainer in (
    "TRAINER_GRUNT_21_HNS", "TRAINER_GRUNT_10_HNS", "TRAINER_GRUNT_9_HNS",
    "TRAINER_JESSIE_JAMES_TINTOWER_HNS",
):
    assert f"case {trainer}:" in battle_setup, trainer

# Steevee and Neevee are the recurring PRL trainer twins, not species. Their
# signature Eeveelutions already occupy collision-free PRU IDs in the 444-dex;
# this phase connects the missing donor evolutions, teams and duo transition.
opponents = read("include/constants/opponents_hns.h")
species = read("include/constants/species.h")
eevee_family = read("src/data/pokemon/species_info/gen_1_families.h")
item_ids = read("include/constants/items.h")
item_data = read("src/data/items.h")
assert "ITEM_ANCIENT_STONE" in item_ids
assert "[ITEM_ANCIENT_STONE]" in item_data
assert "ItemUseOutOfBattle_EvolutionStone" in item_data
assert ["#define", "SPECIES_EEVEEON", "1637"] in [line.split() for line in species.splitlines()]
assert ["#define", "SPECIES_NIMBEON", "1638"] in [line.split() for line in species.splitlines()]
assert "{EVO_ITEM, ITEM_ANCIENT_STONE, SPECIES_EEVEEON}" in eevee_family
assert "{EVO_LEVEL, 0, SPECIES_NIMBEON, CONDITIONS({IF_NOT_TIME, TIME_NIGHT}, {IF_HOLD_ITEM, ITEM_SHARP_BEAK})}" in eevee_family
for filename in (
    "graphics/pokemon/eeveeon/front.png", "graphics/pokemon/eeveeon/back.png",
    "graphics/pokemon/eeveeon/icon.png", "graphics/pokemon/eeveeon/normal.pal",
    "graphics/pokemon/eeveeon/shiny.pal", "graphics/pokemon/nimbeon/front.png",
    "graphics/pokemon/nimbeon/back.png", "graphics/pokemon/nimbeon/icon.png",
    "graphics/pokemon/nimbeon/normal.pal", "graphics/pokemon/nimbeon/shiny.pal",
):
    assert (ROOT / filename).is_file(), filename
for trainer in (
    "TRAINER_STEEVE_NEEVEE_ROUTE3_HNS", "TRAINER_STEEVE_NEEVEE_SS_ANNE_HNS",
    "TRAINER_STEEVE_NEEVEE_TOWER_HNS", "TRAINER_STEEVE_NEEVEE_ROUTE23_HNS",
):
    assert trainer in opponents, trainer
    block = party.split(f"=== {trainer} ===", 1)[1].split("=== ", 1)[0]
    assert "Name: STEEVEE" in block, trainer
    assert "Class: Twins Hns" in block, trainer
    assert "Double Battle: Yes" in block, trainer
    assert f"case {trainer}:" in battle_setup, trainer
assert "Nimbeon @ Sitrus Berry" in party
assert "Eeveeon @ Sitrus Berry" in party

print("PASS: Johto Rockets including invisible Radio Tower 4F stair ambush and physical escape; PRL intro and twins wired (in-game scene QA still required).")
