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


# Three Rocket encounters are automatic, invisible step triggers.
# Physical templates remain for stable local IDs but are NEVER rendered.
scenes = (
    ("SlowpokeWell_B1F_hns", (10, 11, 28), "VAR_TEMP_0",
     "SlowpokeWell_B1F_EventScript_JessieJamesTrigger", "TRAINER_GRUNT_21_HNS",
     "FLAG_PJR_JESSIE_JAMES_1_DEFEATED", 3),
    ("GoldenrodCity_UndergroundSwitches_hns", (3, 6, 11), "VAR_TEMP_3",
     "GoldenrodCity_UndergroundSwitches_EventScript_JessieJamesTrigger", "TRAINER_GRUNT_10_HNS",
     "FLAG_PJR_JESSIE_JAMES_2_DEFEATED", 4),
    ("GoldenrodCity_RadioTower_4F_hns", (2, 5, 7), "VAR_TEMP_3",
     "GoldenrodCity_RadioTower_4F4_EventScript_JessieJamesTrigger", "TRAINER_GRUNT_9_HNS",
     "FLAG_PJR_JESSIE_JAMES_3_DEFEATED", 7),
)
for map_name, local_ids, var, trigger_name, trainer_id, win_flag, expected_coords in scenes:
    data = map_file(map_name)
    script = read(f"data/maps/{map_name}/scripts.inc")
    events = [data["object_events"][i-1] for i in local_ids]
    assert all(ev["flag"] == "FLAG_TEMP_1" for ev in events), map_name
    assert all(ev["trainer_type"] == "TRAINER_TYPE_NONE" for ev in events), map_name
    triggers = [e for e in data["coord_events"] if e.get("script") == trigger_name]
    assert len(triggers) == expected_coords, (map_name, len(triggers))
    assert all(e["var"] == var and str(e["var_value"]) == "0" for e in triggers), map_name
    assert "setflag FLAG_TEMP_1" in script, map_name
    assert "clearflag FLAG_TEMP_1" not in script, f"Rocket sprite reveal must never happen: {map_name}"
    for local_id in local_ids:
        # No movement/removal/forced facing, no summoned actor.
        assert f"addobject {local_id}\\n" not in script.split("EventScript_JessieJamesTrigger::",1)[1].split("EventScript_JessieJamesAlreadyDefeated::",1)[0], map_name
    assert f"checktrainerflag {trainer_id}" in script, f"previous-win compatibility: {map_name}"
    assert f"cleartrainerflag {trainer_id}" not in script, f"do not rearm old saves: {map_name}"
    assert script.count(f"trainerbattle_double {trainer_id},") == 1, map_name
    battle = script.split("EventScript_JessieJamesBattle::",1)[1].split("EventScript_JessieJamesAfterBattle::",1)[0]
    assert "EventScript_JessieJamesAfterBattle" in battle, map_name
    victory = script.split("EventScript_JessieJamesAfterBattle::",1)[1].split("EventScript_JessieJamesAlreadyDefeated::",1)[0]
    assert f"setflag {win_flag}" in victory, map_name
    assert "applymovement" not in victory and "turnobject" not in victory and "removeobject" not in victory, map_name
    assert "releaseall" in victory, map_name

battle_setup = read("src/battle_setup.c")
trainer_scripts = read("data/scripts/trainer_battle.inc")
event_headers = read("include/event_scripts.h")
block = battle_setup.split("case TRAINER_BATTLE_CONTINUE_SCRIPT_DOUBLE:",1)[1].split("return EventScript_TryDoDoubleTrainerBattle;",1)[0]
for trainer_id in ("TRAINER_GRUNT_21_HNS", "TRAINER_GRUNT_10_HNS", "TRAINER_GRUNT_9_HNS"):
    assert f"case {trainer_id}:" in block, trainer_id
assert "return EventScript_TryDoInvisibleRocketDoubleBattle;" in block
assert "#if IS_HNS" in block
assert "EventScript_TryDoInvisibleRocketDoubleBattle[]" in event_headers
intro = trainer_scripts.split("EventScript_TryDoInvisibleRocketDoubleBattle::",1)[1].split("EventScript_TryDoDoubleTrainerBattle::",1)[0]
assert "lockall" in intro and "HasEnoughMonsForDoubleBattle" in intro
assert "EventScript_ShowTrainerIntroMsg" in intro and "GetTrainerFlag" in intro
assert "faceplayer" not in intro and "reveal_trainer" not in intro and "SetTrainerFacingDirection" not in intro
assert "EventScript_NotEnoughMonsForInvisibleRocketDoubleBattle::" in intro
assert "releaseall" in intro and "gotopostbattlescript" in intro

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

print("PASS: all 3 Johto Rocket encounters trigger invisible double battles, retain PRL intro, and never spawn/walk NPCs (live-save QA pending).")
