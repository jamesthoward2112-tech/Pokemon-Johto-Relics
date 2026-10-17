#!/usr/bin/env python3
"""PRU first-adventure static regression/Relic dialogue source audit.

Does NOT substitute for ROM/emulator or every live-scene gameplay check.
Run: python3 tools/pru/check_pretest_story.py
"""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[2]
map_dir = root / "data" / "maps"
lab = (map_dir / "NewBarkTown_Lab_hns" / "scripts.inc").read_text()
data = json.loads((map_dir / "NewBarkTown_Lab_hns" / "map.json").read_text())
alph = (map_dir / "RuinsOfAlph_Lab_hns" / "scripts.inc").read_text()
oak = (map_dir / "PalletTown_Lab_hns" / "scripts.inc").read_text()
crest = (map_dir / "MtSilver_SummitDay_hns" / "scripts.inc").read_text()
hof = (map_dir / "PokemonLeague_HallOfFame_hns" / "scripts.inc").read_text()

assert len([x for x in data["object_events"] if "FossilDisplay_" in x.get("script", "")]) == 3
for key in ("NewBarkTown_Lab_EventScript_FossilDisplay_Helix",
            "NewBarkTown_Lab_EventScript_FossilDisplay_Dome",
            "NewBarkTown_Lab_EventScript_FossilDisplay_Amber"):
    assert key + "::" in lab, key
    assert any(x.get("script") == key and x["flag"] == "0" for x in data["object_events"])
assert not any("OBJ_EVENT_GFX_POKE_BALL" == x["graphics_id"] for x in data["object_events"])
assert all("FOSSIL" in x["graphics_id"] or "AMBER" in x["graphics_id"]
           for x in data["object_events"] if "FossilDisplay_" in x.get("script", ""))

give_start = lab.index("NewBarkTown_Lab_EventScript_ElmChoosePokemon::")
give_end = lab.index("NewBarkTown_Lab_EventScript_TriggerReturnPlayer::", give_start)
give = lab[give_start:give_end]
assert "setvar PLAYER_STARTER_SPECIES, SPECIES_PIKACHU" in give
assert "setvar VAR_STARTER_MON, 0" in give
assert "goto NewBarkTown_Lab_EventScript_ChoseStarter" in give
assert "MSGBOX_YESNO" not in give
assert "SPECIES_PIKACHU, 5," in lab
assert "NewBarkTown_Lab_EventScript_GiveStarter_Chikorita" in lab
assert "removeobject VAR_LAST_TALKED" not in lab
assert "didn't choose at the start" not in lab
assert "NewBarkTown_Lab_EventScript_PoliceEpisode::" in lab
assert "removeitem ITEM_MYSTERY_EGG" in lab
assert "NewBarkTown_Lab_EventScript_Elm_Togepi_Seen::" in lab
assert "giveegg SPECIES_TOGEPI" in (map_dir / "VioletCity_PokemonCenter_hns" / "scripts.inc").read_text()
assert "These fossils also give" in lab

# Elm's fixed Pikachu starter must match Silver's live first-rival Cyndaquil team.
silver = (map_dir / "CherrygroveCity_hns" / "scripts.inc").read_text()
assert "goto_if_eq VAR_STARTER_MON, 0, CherryGroveCity_Silver_Battle_Cyndaquil" in silver
assert "trainerbattle_no_intro TRAINER_RIVAL_CYNDAQUIL_1_HNS" in silver

flags = (
    "FLAG_PJR_RELIC_RAIKOU", "FLAG_PJR_RELIC_ENTEI",
    "FLAG_PJR_RELIC_LUGIA", "FLAG_PJR_RELIC_UNOWN_I",
    "FLAG_PJR_RELIC_CELEBI", "FLAG_PJR_RELIC_SUICUNE",
    "FLAG_PJR_RELIC_ALPHORACLE",
)
positions = [alph.index("goto_if_unset " + flag + ",") for flag in flags]
assert positions == sorted(positions), "R-E-L-I-C-S order changed"
assert "goto_if_set FLAG_PJR_RELIC_HO_OH, RuinsOfAlph_Lab_EventScript_RelicsFullyComplete" in alph
assert "goto_if_unset FLAG_PJR_GOT_RAINBOW_CREST, RuinsOfAlph_Lab_EventScript_RelicNeedsCrest" in alph
assert "RuinsOfAlph_Lab_Text_RelicsFullyComplete:" in alph
assert "the TIN TOWER roof" in alph
assert "FLAG_PJR_GOT_RAINBOW_CREST" in crest
assert "goto_if_eq VAR_RESULT, FALSE, MtSilver_SummitDay_EventScript_CrestFullBag" in crest
assert "goto_if_unset FLAG_PJR_GOT_RAINBOW_CREST, MtSilver_SummitDay_EventScript_ContinueClear" in crest
assert "MtSilver_SummitDay_EventScript_CheckPendingCrest::" in crest
assert "MtSilver_SummitDay_EventScript_RedBattleNormal::" in crest
trail = (map_dir / "BellchimeTrail_hns" / "scripts.inc").read_text()
assert "EcruteakBellchimeTrail_EventScript_RelicShortcut::" in trail
assert "EcruteakBellchimeTrail_EventScript_RelicShortcutBackfill" not in trail
assert "EcruteakBellchimeTrail_EventScript_RelicShortcutCrestBackfill" not in trail
assert "setflag FLAG_PJR_RELIC_ALPHORACLE" not in trail
assert "setflag FLAG_PJR_GOT_RAINBOW_CREST" not in trail
assert "PalletTown_Lab_Text_OakResonanceResearch:" in oak
assert "msgbox PalletTown_Lab_Text_OakResonanceResearch" in oak
assert "FLAG_IS_CHAMPION" in hof

# PRU championship progression: do not turn a Johto League replay into a
# Kanto victory before every Kanto Gym badge has actually been earned.
champions_room = (map_dir / "PokemonLeague_ChampionsRoom_hns" / "scripts.inc").read_text()
all_kanto_badges = [f"FLAG_BADGE{n:02d}_GET" for n in range(9, 17)]
hof_clear = hof.split("PokemonLeague_HallOfFame_EventScript_SetGameClearFlags::", 1)[1].split(
    "PokemonLeague_HallOfFame_EventScript_SpawnAlolaMons::", 1)[0]
for badge in all_kanto_badges:
    assert (f"goto_if_unset {badge}, PokemonLeague_HallOfFame_EventScript_KantoAlreadyAwarded"
            in hof_clear), badge
    assert (f"goto_if_unset {badge}, PokemonLeague_HallOfFame_EventScript_JohtoRematchText"
            in hof), badge
    assert (f"goto_if_unset {badge}, PokemonLeague_WillsRoom_EventScript_LanceRematchJohto"
            in champions_room), badge
    assert (f"goto_if_unset {badge}, PokemonLeague_ChampionsRoom_EventScript_JohtoRematchInterview"
            in champions_room), badge
assert "goto_if_set FLAG_IS_KANTO_CHAMPION, PokemonLeague_HallOfFame_EventScript_KantoAlreadyAwarded" in hof_clear
assert hof_clear.index("goto_if_unset FLAG_BADGE16_GET") < hof_clear.index("setflag FLAG_IS_KANTO_CHAMPION")
assert "PokemonLeague_HallOfFame_JohtoRematch_LanceText:" in hof
assert "PokemonLeague_ChampionsRoom_Text_JohtoRematchBattleIntro:" in champions_room
assert "PokemonLeague_ChampionsRoom_Text_JohtoRematchMaryInterview:" in champions_room
# GBA script strings use exactly one literal backslash for text/control escapes.
for segment in (hof.split("@ Johto League rematches are allowed", 1)[1],
                champions_room.split("@ Replays of the Johto championship", 1)[1]):
    assert not any(chr(92) * 2 in line for line in segment.splitlines()
                   if ".string" in line), "Incorrectly doubled script text escape"
for permanent in ("FLAG_CAUGHT_MEW", "FLAG_CAUGHT_ENTEI", "FLAG_CAUGHT_RAIKOU",
                  "FLAG_BATTLED_DEOXYS", "FLAG_DEFEATED_DEOXYS",
                  "FLAG_SUMMONED_MTMOON_JIRACHI"):
    assert f"clearflag {permanent}" not in hof, permanent

# For transparent QA: unresolved previously inherited PJR event problems.
warnings = []
if "giveitem ITEM_ANCIENT_RAINBOW_CREST\n\tsetflag FLAG_PJR_GOT_RAINBOW_CREST" in crest:
    warnings.append("Red's Ancient Rainbow Crest handoff does not check bag-full outcome.")

# Machine-scan EVERY HNS map dialogue file for dead Kanto-first or sequel phrases.
candidates = {
    "inter-ROM transfer": ("boxed your pokemon for hoenn", "donated all your items",
                           "your kanto pokemon are in storage", "next adventure in hoenn"),
    "starter choice remnants": ("two partners you didn't choose", "three pokeballs",
                                "the left poke ball holds pikachu"),
    "Kanto-first prior champion": ("you already beat the kanto league",
                                   "before you came to johto, you were champion"),
}
hits = []
active_files = list(map_dir.glob("*_hns/scripts.inc"))
for file in active_files:
    source = file.read_text(errors="replace").lower()
    for category, phrases in candidates.items():
        for phrase in phrases:
            if phrase in source:
                hits.append((str(file.relative_to(root)), category, phrase))
report = root / "PRU-Pretest-Story-Scan.md"
report.write_text(
    "# PRU pre-test source dialogue regression scan\n\n"
    f"Scanned {len(active_files)} live HNS map-script files.\n\n"
    "## Critical lexical conflicts\n"
    + ("\n".join(f"- `{p}`: {cat}: `{phrase}`" for p, cat, phrase in hits)
       if hits else "None of the tracked direct sequel/choice claims found.\n")
    + "\n\n## Other source-identified issues still requiring work\n"
    + "\n".join("- " + w for w in warnings)
    + "\n\nA clean lexical scan is NOT an exhaustive semantic or emulator audit.\n",
    encoding="utf-8"
)
assert not hits, hits
print(f"PASS: first-adventure opening, passive fossils, Pikachu, egg, relic order, Kanto badge gates and permanent legend flags; scanned {len(active_files)} HNS map scripts.")
for line in warnings:
    print("TRACKED:", line)
print("Wrote PRU-Pretest-Story-Scan.md")

# Gift inventory: find real HNS event sources, rather than assuming the old
# PRL/Kanto gift spreadsheet describes this Johto-first playable branch.
import re
gift_species = re.compile(r"SPECIES_(?:CHIKORITA|TORCHIC|MUDKIP|TREECKO)\b")
gift_ops = re.compile(r"\b(?:givemon|giveegg|createmon)\b")
gift_matches = 0
for gift_map in sorted(map_dir.glob("*/scripts.inc")):
    gift_lines = gift_map.read_text(errors="replace").splitlines()
    for number, gift_line in enumerate(gift_lines, 1):
        if gift_species.search(gift_line):
            gift_matches += 1
            print(f"GIFT_SPECIES_SCAN {gift_map.relative_to(root)}:{number}: {gift_line.strip()[:180]}")
        elif gift_map.parent.name.endswith("_hns") and gift_ops.search(gift_line) and not gift_line.strip().startswith("@"):
            print(f"GIFT_OP_SCAN {gift_map.relative_to(root)}:{number}: {gift_line.strip()[:120]}")
print(f"GIFT_SCAN_COMPLETE target_species_lines={gift_matches}")

# Repeated nurse-side Chansey service: genuine two-Pokémon double battle,
# level tiers are bound per centre, never gives money or saves defeat flags.
chansey_source = (map_dir / "CherrygroveCity_PokemonCenter_hns" / "scripts.inc").read_text()
chansey_parties = (root / "src" / "data" / "trainers_hns.party").read_text()
chansey_ids = (root / "include" / "constants" / "opponents_hns.h").read_text()
chansey_levels = [7, 12, 15, 20, 26, 31, 37, 40, 44, 50, 60, 64, 68, 71, 75, 78, 82, 85, 90, 95, 100]
for level in chansey_levels:
    name = f"TRAINER_PRU_CHANSEY_{level:02d}_HNS"
    assert f"cleartrainerflag {name}" in chansey_source, name
    assert f"trainerbattle_double {name}, " in chansey_source, name
    assert name in chansey_ids
    part = chansey_parties.split(f"=== {name} ===", 1)[1].split("=== ", 1)[0]
    assert part.count("\nChansey\n") == 2, name
    assert "Double Battle: Yes" in part, name
    assert part.count("- Memento") == 2 and part.count("- Heal Pulse") == 2, name
for loc in ("CherrygroveCity", "VioletCity", "AzaleaTown", "GoldenrodCity"):
    m = json.loads((map_dir / f"{loc}_PokemonCenter_hns" / "map.json").read_text())
    chanseys = [o for o in m["object_events"] if o["graphics_id"] == "OBJ_EVENT_GFX_NURSE_CHANSEY_HNS"]
    assert len(chanseys) == 1, loc
    assert chanseys[0]["script"] == "CherryGrove_Pokecenter_Chansey" or chanseys[0]["script"].startswith("PRU_ChanseyTrainer_Lv"), loc
money = (root / "src" / "battle_script_commands.c").read_text()
assert "trainerId >= TRAINER_PRU_CHANSEY_07_HNS && trainerId <= TRAINER_PRU_CHANSEY_100_HNS" in money
assert "TRAINER_PRU_CHANSEY_100_HNS           674" in chansey_ids
for expected_id, trainer in enumerate((
    "TRAINER_STEEVE_NEEVEE_ROUTE3_HNS",
    "TRAINER_STEEVE_NEEVEE_SS_ANNE_HNS",
    "TRAINER_STEEVE_NEEVEE_TOWER_HNS",
    "TRAINER_STEEVE_NEEVEE_ROUTE23_HNS",
), start=675):
    assert f"#define {trainer}" in chansey_ids and str(expected_id) in chansey_ids.split(trainer, 1)[1].splitlines()[0]
assert "TRAINERS_COUNT_HNS                       679" in chansey_ids
print("PASS: 21 nurse-side Chansey tiers: repeatable genuine double battles, 2 Chansey each, no money.")

