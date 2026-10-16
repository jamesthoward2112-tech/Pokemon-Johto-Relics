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

# For transparent QA: unresolved previously inherited PJR event problems.
warnings = []
if "clearflag FLAG_CAUGHT_MEW" in hof:
    warnings.append("Hall of Fame repeats reset caught-Mew flag; fix as separate legendary/league progression task.")
if "clearflag FLAG_CAUGHT_ENTEI" in hof or "clearflag FLAG_CAUGHT_RAIKOU" in hof:
    warnings.append("Hall of Fame reinitialises caught roaming beast flags; guard against repeat grants.")
if "giveitem ITEM_ANCIENT_RAINBOW_CREST\n\tsetflag FLAG_PJR_GOT_RAINBOW_CREST" in crest:
    warnings.append("Red's Ancient Rainbow Crest handoff does not check bag-full outcome.")
if "setflag FLAG_IS_KANTO_CHAMPION" in hof:
    warnings.append("Confirm rematch promotion to Kanto Champion is gated by 16 badges, not only a replay.")

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
print(f"PASS: first-adventure opening, passive fossils, Pikachu, original egg and relic order; scanned {len(active_files)} HNS map scripts.")
for line in warnings:
    print("TRACKED:", line)
print("Wrote PRU-Pretest-Story-Scan.md")
