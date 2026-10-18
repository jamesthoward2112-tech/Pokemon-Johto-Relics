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


# PRL donor pattern: individual trainers, one double-battle opponent, with
# explicit localId= per actor. No scripted walk-in, forced facing or run-away.
scenes=(
    ("SlowpokeWell_B1F_hns",(10,11,28),("10","11"),"TRAINER_GRUNT_21_HNS","FLAG_PJR_JESSIE_JAMES_1_DEFEATED","SlowpokeWell_B1F_EventScript_JessieJamesTrigger"),
    ("GoldenrodCity_UndergroundSwitches_hns",(3,6,11),("LOCALID_UNDERGROUND_JAMES","LOCALID_UNDERGROUND_JESSIE"),"TRAINER_GRUNT_10_HNS","FLAG_PJR_JESSIE_JAMES_2_DEFEATED","GoldenrodCity_UndergroundSwitches_EventScript_JessieJamesTrigger"),
    ("GoldenrodCity_RadioTower_4F_hns",(2,5,7),("LOCALID_RADIO4F_JAMES","LOCALID_RADIO4F_JESSIE"),"TRAINER_GRUNT_9_HNS","FLAG_PJR_JESSIE_JAMES_3_DEFEATED","GoldenrodCity_RadioTower_4F4_EventScript_JessieJamesTrigger"),
)
for name,ids,local_ids,trainer,flag,old_trigger in scenes:
    mapdata=map_file(name)
    script=read(f"data/maps/{name}/scripts.inc")
    james,jessie,meowth=(mapdata["object_events"][id-1] for id in ids)
    assert all(obj["flag"]==flag for obj in (james,jessie,meowth)),name
    assert all(obj["trainer_type"]=="TRAINER_TYPE_NORMAL" for obj in (james,jessie)),name
    assert meowth["trainer_type"]=="TRAINER_TYPE_NONE",name
    assert all(obj["movement_type"].startswith("MOVEMENT_TYPE_FACE_") for obj in (james,jessie,meowth)),name
    assert all(int(obj["trainer_sight_or_berry_tree_id"])>=1 for obj in (james,jessie)),name
    assert not any(e.get("script")==old_trigger for e in mapdata["coord_events"]),name
    assert f"checktrainerflag {trainer}" in script,name
    assert f"cleartrainerflag {trainer}" not in script,name
    assert script.count(f"trainerbattle_double {trainer},")==2,(name,"battle count")
    for local_id in local_ids:
        assert f"localId={local_id}" in script,(name,local_id)
    assert f"setflag {flag}" in script
    victory=script.split("EventScript_JessieJamesAfterBattle::",1)[1].split("\n\tend",1)[0]
    assert "removeobject" in victory and "applymovement" not in victory,name
    assert "setflag "+flag in victory,name

macro=read("asm/macros/event.inc")
block=macro.split(".macro trainerbattle_double ",1)[1].split(".endm",1)[0]
assert "localId=LOCALID_NONE" in block
assert all((mode+", \\localId") in block for mode in (
    "TRAINER_BATTLE_DOUBLE","TRAINER_BATTLE_CONTINUE_SCRIPT_DOUBLE","TRAINER_BATTLE_CONTINUE_SCRIPT_DOUBLE_NO_MUSIC"))
source=read("src/battle_setup.c")
step=source.split("case TRAINER_BATTLE_CONTINUE_SCRIPT_DOUBLE:",1)[1].split("return EventScript_TryDoDoubleTrainerBattle;",1)[0]
assert "EventScript_TryDoInvisibleRocketDoubleBattle" not in step
assert "SetMapVarsToTrainerA();" in step
assert "EventScript_TryDoInvisibleRocketDoubleBattle" not in read("include/event_scripts.h")

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

print("PASS: three Johto Rocket encounters use PRL-style individual trainer actors sharing each duo's double battle ID; no forced movement (live-save QA pending).")
