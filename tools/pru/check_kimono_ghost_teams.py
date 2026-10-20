#!/usr/bin/env python3
"""PRU eight-badge Kimono Girl replacement-team and progression regression.

This source-level check does not substitute for testing the user's eight-badge
save, the five-battle gauntlet, the Legendary event or a full emulator playthrough.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
parties = (ROOT / "src/data/trainers_hns.party").read_text()
theater = (ROOT / "data/maps/EcruteakCity_Theater_hns/scripts.inc").read_text()
elm = (ROOT / "data/maps/NewBarkTown_Lab_hns/scripts.inc").read_text()
gate = (ROOT / "data/maps/ReceptionGate_hns/scripts.inc").read_text()
moves = (ROOT / "src/data/moves_info.h").read_text()

expected = {
    "ZUKI": "Gengar",
    "NAOKO": "Misdreavus",
    "MIKI": "Banette",
    "SAYO": "Sableye",
    "KUNI": "Dusclops",
}
eeveelution_signatures = {
    "Eevee", "Flareon", "Jolteon", "Vaporeon", "Umbreon", "Espeon",
    "Leafeon", "Glaceon", "Sylveon", "Omeon", "Lepideon", "Champeon",
    "Guardeon", "Drakeon", "Eeveeon", "Nimbeon", "Toxeon",
}
party_begins = list(re.finditer(r"^=== TRAINER_([^\\n]+?) ===$", parties, flags=re.MULTILINE))
party_map = {}
for i, match in enumerate(party_begins):
    key = match.group(1)
    end = party_begins[i + 1].start() if i + 1 < len(party_begins) else len(parties)
    party_map[key] = parties[match.start():end]

for name, species in expected.items():
    key = name + "_HNS"
    assert key in party_map, f"Missing Kimono Girl trainer: {key}"
    block = party_map[key]
    assert "Class: Kimono Girl Hns" in block
    assert "Double Battle: No" in block, f"Changed the original five-battle format: {key}"
    assert re.search(rf"^{re.escape(species)}\\s*$", block, flags=re.MULTILINE), f"Wrong species for {key}"
    assert len(re.findall(r"^Level:\\s*48$", block, flags=re.MULTILINE)) == 1, f"Unexpected party size/level for {key}"
    assert "- Eerie Fog" in block, f"{key} cannot summon Eerie Fog"
    species_lines = re.findall(r"^([A-Za-z][A-Za-z '-]+)\\nLevel: [0-9]+", block, flags=re.MULTILINE)
    assert len(species_lines) == 1, f"Multiple/missing Pokémon in {key}: {species_lines}"
    assert not (set(species_lines) & eeveelution_signatures), f"Eeveelution present in {key}"
    assert f"trainerbattle_no_intro TRAINER_{key}," in theater, f"Missing gauntlet battle {key}"

assert "[MOVE_EERIE_FOG]" in moves, "PRL Eerie Fog move definition missing"
assert ".weatherType = BATTLE_WEATHER_FOG" in moves, "Fog move no longer has its intended weather"
assert "NewBarkTown_Lab_EventScript_ElmMasterBall::" in elm
assert "setvar VAR_ECRUTEAK_CITY_THEATER, 4" in elm, "Elm must still point to Dance Theatre"
assert "NewBarkTown_Lab_Text_KimonoWaiting:" in elm
assert "EcruteakCity_Theater_EventScript_LegendaryCutscene::" in theater
assert "setvar VAR_ECRUTEAK_CITY_THEATER, 6" in theater, "Theatre gauntlet state changed"
assert "setvar VAR_ECRUTEAK_CITY_THEATER, 7" in theater, "Legendary release state changed"
assert "setvar VAR_ECRUTEAK_CITY_THEATER, 8" not in theater, "Do not skip the Legendary battle"
assert "goto_if_lt VAR_ECRUTEAK_CITY_THEATER, 8, ReceptionGate_EventScript_Kimono" in gate
for trainer in ("MIHARU", "YOUKO", "SHIZUKO"):
    assert f"TRAINER_{trainer}_HNS" in parties, "Later Sinjoh Kimono encounters must remain intact"

print("PASS: five distinct Ghost / Eerie Fog Kimono singles, original Elm/Legendary gate preserved")
