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


# Keep the first PRL-style encounter at Slowpoke Well.
# Remove the duplicate Goldenrod Underground encounter while retaining object slots.
# The approved Radio Tower approach and retreat must remain untouched.
scenes=(
    ("SlowpokeWell_B1F_hns",(10,11,28),("10","11"),"TRAINER_GRUNT_21_HNS","FLAG_PJR_JESSIE_JAMES_1_DEFEATED","SlowpokeWell_B1F_EventScript_JessieJamesTrigger"),
    ("GoldenrodCity_RadioTower_4F_hns",(2,5,7),("LOCALID_RADIO4F_JAMES","LOCALID_RADIO4F_JESSIE"),"TRAINER_GRUNT_9_HNS","FLAG_PJR_JESSIE_JAMES_3_DEFEATED","GoldenrodCity_RadioTower_4F4_EventScript_JessieJamesTrigger"),
)
for name,ids,local_ids,trainer,flag,old_trigger in scenes:
    mapdata=map_file(name)
    script=read(f"data/maps/{name}/scripts.inc")
    james,jessie,meowth=(mapdata["object_events"][id-1] for id in ids)
    if name == "GoldenrodCity_RadioTower_4F_hns":
        # Unavoidable interception immediately after the LEFT 3F staircase.
        assert all(obj["flag"] == flag for obj in (james, jessie, meowth)), name
        assert all(obj["trainer_type"] == "TRAINER_TYPE_NONE" for obj in (james, jessie, meowth)), name
        assert all(obj["movement_type"] == "MOVEMENT_TYPE_FACE_UP" for obj in (james, jessie, meowth)), name
        assert all(obj["trainer_sight_or_berry_tree_id"] == "0" for obj in (james, jessie)), name
        assert [(o["x"], o["y"]) for o in (jessie, james, meowth)] == [(13, 11), (14, 11), (15, 11)]
        stair = {(10,5), (11,5), (9,6), (10,6), (11,6), (9,7), (10,7)}
        coords = {(e["x"], e["y"]) for e in mapdata["coord_events"]
                  if e["script"] == "GoldenrodCity_RadioTower_4F4_EventScript_JessieJamesStairIntercept"}
        assert coords == stair, coords
        assert all(e["var"] == "VAR_TEMP_3" and str(e["var_value"]) == "0"
                   for e in mapdata["coord_events"]
                   if e["script"] == "GoldenrodCity_RadioTower_4F4_EventScript_JessieJamesStairIntercept")
        assert "setvar VAR_TEMP_3, 0" in script  # reset on map transition
        assert "checktrainerflag " + trainer in script  # older saved victories
        assert "cleartrainerflag " + trainer not in script
        assert script.count("trainerbattle_double " + trainer + ",") == 1
        assert "localId=LOCALID_RADIO4F_JAMES" in script
        intercept = script.split("EventScript_JessieJamesStairIntercept::", 1)[1].split(
            "EventScript_NeedTwoPokemon::", 1)[0]
        assert "getplayerxy VAR_0x8000, VAR_0x8001" in intercept
        assert "goto_if_eq VAR_0x8001, 5," in intercept
        assert "goto_if_eq VAR_0x8001, 6," in intercept
        assert "goto_if_eq VAR_0x8000, 11," in intercept
        assert "HasEnoughMonsForDoubleBattle" in intercept
        for local_id in (2, 5, 7):
            for direction, steps in (("North", (3, 4, 5)), ("West", (3, 4))):
                for count in steps:
                    number = {3: "Three", 4: "Four", 5: "Five"}[count]
                    cmd = f"applymovement {local_id}, GoldenrodCity_RadioTower_4F4_Movement_{direction}{number}"
                    assert cmd in intercept, cmd
            assert f"turnobject {local_id}, DIR_NORTH" in intercept
        assert intercept.count("waitmovementall") == 2
        assert "turnobject OBJ_EVENT_ID_PLAYER, DIR_SOUTH" in intercept

        retreat = script.split("EventScript_JessieJamesAfterBattle::", 1)[1].split(
            "EventScript_JessieJamesAlreadyDefeated::", 1)[0]
        assert "setflag " + flag in retreat
        assert "goto_if_ne VAR_TEMP_3, 1," in retreat  # direct-interaction fallback
        assert "getplayerxy VAR_0x8000, VAR_0x8001" in retreat
        assert "goto_if_eq VAR_0x8000, 11," in retreat
        assert "goto_if_eq VAR_0x8001, 5," in retreat
        assert "goto_if_eq VAR_0x8001, 6," in retreat
        for local_id in (2, 5, 7):
            for direction, steps in (("East", (3, 4)), ("South", (3, 4, 5))):
                for count in steps:
                    number = {3: "Three", 4: "Four", 5: "Five"}[count]
                    cmd = f"applymovement {local_id}, GoldenrodCity_RadioTower_4F4_Movement_{direction}{number}"
                    assert cmd in retreat, cmd
            assert f"removeobject {local_id}" in retreat
        assert retreat.count("waitmovementall") == 2
        assert retreat.index("waitmovementall") < retreat.index("fadescreen FADE_TO_BLACK") < retreat.index("removeobject 5")
        for name, opcode, count in (
            ("NorthThree", "walk_up", 3), ("NorthFour", "walk_up", 4),
            ("NorthFive", "walk_up", 5), ("WestThree", "walk_left", 3),
            ("WestFour", "walk_left", 4), ("EastThree", "walk_faster_right", 3),
            ("EastFour", "walk_faster_right", 4), ("SouthThree", "walk_faster_down", 3),
            ("SouthFour", "walk_faster_down", 4), ("SouthFive", "walk_faster_down", 5),
        ):
            movement = script.split(f"GoldenrodCity_RadioTower_4F4_Movement_{name}:\\n".replace("\\n", "\n"), 1)[1].split("\tstep_end", 1)[0]
            assert movement.count("\t" + opcode + "\n") == count, (name, movement)

        # Collision and adjacency checks for every possible staircase landing:
        # At the end, Jessie or James must stand directly below the player.
        import struct
        blob = (ROOT / "data/layouts/GoldenrodCity_RadioTower_4F_hns/map.bin").read_bytes()
        assert len(blob) == 32 * 16 * 2
        aisle = {(x, y) for y in (6, 7, 8) for x in range(9, 16)}
        columns = {(x, y) for y in range(6, 12) for x in (13, 14, 15)}
        for xx, yy in sorted(stair | aisle | columns):
            tile, = struct.unpack_from("<H", blob, (yy * 32 + xx) * 2)
            assert (tile & 0xC00) == 0 and (tile >> 12) == 3, (xx, yy, hex(tile))
        for px, py in stair:
            line = (10, 11, 12) if px == 11 else (9, 10, 11)
            assert px in line[:2], (px, py, line)  # a trainer is 1 tile ahead
            assert all((xx, py + 1) in aisle for xx in line)

        continue
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

# Underground switch puzzle, rival battle, grunts and items are untouched.
# The retired trio retains the same local IDs, but must never appear or battle,
# even when loading a saved game from inside this room.
underground_map = map_file("GoldenrodCity_UndergroundSwitches_hns")
underground_script = read("data/maps/GoldenrodCity_UndergroundSwitches_hns/scripts.inc")
assert len(underground_map["object_events"]) == 11
for local_id, graphics in (
    (3, "OBJ_EVENT_GFX_JAMES_HNS"),
    (6, "OBJ_EVENT_GFX_JESSIE_HNS"),
    (11, "OBJ_EVENT_GFX_MON_BASE+SPECIES_MEOWTH"),
):
    actor = underground_map["object_events"][local_id - 1]
    assert actor["graphics_id"] == graphics, local_id
    assert actor["flag"] == "FLAG_PJR_JESSIE_JAMES_2_DEFEATED", local_id
    assert actor["script"] == "NULL", local_id
    assert actor["trainer_type"] == "TRAINER_TYPE_NONE", local_id
    assert actor["trainer_sight_or_berry_tree_id"] == "0", local_id
head = underground_script.split("GoldenrodUnderground1_JessieJamesTransition::",1)[1].split("GoldenrodUnderground1_OnLoad::",1)[0]
load = underground_script.split("GoldenrodUnderground1_OnLoad::",1)[1].split("GoldenrodUnderground1_ClearTheWay::",1)[0]
assert "setflag FLAG_PJR_JESSIE_JAMES_2_DEFEATED" in head
assert "setflag FLAG_PJR_JESSIE_JAMES_2_DEFEATED" in load
for local_id in ("LOCALID_UNDERGROUND_JAMES", "LOCALID_UNDERGROUND_JESSIE", "11"):
    assert f"removeobject {local_id}" in load
assert "trainerbattle_double TRAINER_GRUNT_10_HNS" not in underground_script
for label in (
    "GoldenrodCity_UndergroundSwitches_EventScript_JessieJamesInteract",
    "GoldenrodCity_UndergroundSwitches_EventScript_JessieJamesJessie",
    "GoldenrodCity_UndergroundSwitches_EventScript_JessieJamesAfterBattle",
):
    assert underground_script.split(label+"::",1)[1].lstrip().startswith("end")
assert "trainerbattle_single TRAINER_GRUNT_11_HNS" in underground_script
assert "GoldenrodCity_UndergroundSwitches_EventScript_SilverTriggerTop::" in underground_script
assert "GoldenrodCity_UndergroundSwitches_EventScript_Panel1::" in underground_script

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
