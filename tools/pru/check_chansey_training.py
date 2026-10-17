#!/usr/bin/env python3
"""Source-only audit for repeatable, nurse-side Chansey double training."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[2]
MAPS = ROOT / "data/maps"
MAP_TIERS = {
    "CherrygroveCity_PokemonCenter_hns": 7,
    "VioletCity_PokemonCenter_hns": 12,
    "Route32_PokemonCenter_hns": 15,
    "AzaleaTown_PokemonCenter_hns": 20,
    "GoldenrodCity_PokemonCenter_hns": 26,
    "EcruteakCity_PokemonCenter_hns": 31,
    "OlivineCity_PokemonCenter_hns": 37,
    "CianwoodPokecenter_hns": 40,
    "MahoganyTown_PokemonCenter_hns": 44,
    "BlackthornCity_PokemonCenter_hns": 50,
    "IndigoPlateau_PokemonCenter_hns": 60,
    "PewterCity_PokemonCenter_hns": 64,
    "Route4_PokemonCenter_hns": 64,
    "CeruleanCity_PokemonCenter_hns": 68,
    "Route9_PokemonCenter_hns": 68,
    "VermilionCity_PokemonCenter_hns": 71,
    "SaffronCity_PokemonCenter_hns": 75,
    "LavenderTown_PokemonCenter_hns": 75,
    "CeladonCity_PokemonCenter_hns": 78,
    "FuchsiaCity_PokemonCenter_hns": 82,
    "SafariZoneGate_PokemonCenter_hns": 82,
    "CinnabarIsland_PokemonCenter_hns": 85,
    "ViridianCity_PokemonCenter_hns": 90,
    "MtSilver_PokemonCenter_hns": 95,
    "NewSinjoh_PokemonCenter_hns": 95,
    "BattleFrontier_PokemonCenter_1F_hns": 100
}
HANDLERS = (MAPS / "CherrygroveCity_PokemonCenter_hns/scripts.inc").read_text()
PARTIES = (ROOT / "src/data/trainers_hns.party").read_text()
OPPONENTS = (ROOT / "include/constants/opponents_hns.h").read_text()

levels = sorted(set(MAP_TIERS.values()))
for mapname, level in MAP_TIERS.items():
    data = json.loads((MAPS / mapname / "map.json").read_text())
    chansey = [o for o in data["object_events"] if o["graphics_id"] == "OBJ_EVENT_GFX_NURSE_CHANSEY_HNS"]
    assert len(chansey) == 1, (mapname, "expected exactly one Chansey by nurse")
    handler = "CherryGrove_Pokecenter_Chansey" if level == 7 else f"PRU_ChanseyTrainer_Lv{level:02d}"
    assert chansey[0]["script"] == handler, (mapname, chansey[0]["script"], handler)
    assert handler + "::" in HANDLERS, handler
for index, level in enumerate(levels):
    code = f"TRAINER_PRU_CHANSEY_{level:02d}_HNS"
    assert f"#define {code}" in OPPONENTS
    assert re.search(rf"#define\s+{code}\s+{654+index}\b", OPPONENTS), code
    section = PARTIES.split(f"=== {code} ===", 1)[1].split("=== ", 1)[0]
    assert "Double Battle: Yes" in section, code
    assert section.count("\nChansey\n") == 2, code
    assert section.count(f"Level: {level}") == 2, code
    for line in section.splitlines():
        if line.startswith("- "):
            assert line in ("- Memento", "- Heal Pulse"), (code, line)
    assert f"cleartrainerflag {code}" in HANDLERS, code
    assert f"trainerbattle_double {code}," in HANDLERS, code
assert "#define TRAINERS_COUNT_HNS                       675" in OPPONENTS
# Prevent the specific in-game regression: the old one-line "Chaan! Sii!"
# must never be compiled as the active Chansey greeting again.
assert 'CHANSEY: Chaan! Sii!' not in HANDLERS
assert 'CHANSEY wants to train!' in HANDLERS
assert 'CherryGrove_Pokecenter_Chansey::' in HANDLERS
assert 'call PRU_ChanseyTrainer_Offer' in HANDLERS
assert "MSGBOX_YESNO" in HANDLERS
assert "trainerbattle_double" in HANDLERS  # engine checks usable double-battle party
assert "PRU_ChanseyTrainer_Text_NeedTwo" in HANDLERS
assert "PRU_ChanseyTrainer_Text_After" in HANDLERS
# Scan *every* compiled map, not only the curated tier list.
# A stray nurse-side Chansey with an old greeting must be found before make.
unexpected = []
for path in sorted(MAPS.glob("*/map.json")):
    info = json.loads(path.read_text())
    for object_event in info.get("object_events", []):
        if object_event.get("graphics_id") != "OBJ_EVENT_GFX_NURSE_CHANSEY_HNS":
            continue
        if info["name"] == "TestMap1_hns":
            continue
        script = object_event.get("script", "")
        if script != "CherryGrove_Pokecenter_Chansey" and not script.startswith("PRU_ChanseyTrainer_"):
            unexpected.append((info["name"], script))
if unexpected:
    for name, script in unexpected:
        print(f"UNWIRED_CHANSEY_MAP: {name} -> {script}")
    raise SystemExit(f"FAIL: {len(unexpected)} unused/old Chansey dialogue scripts")
print(f"PASS: {len(MAP_TIERS)} existing nurse-side Chansey, {len(levels)} repeatable two-Chansey double-battle tiers, no extra NPCs")
