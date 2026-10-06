"""Static safety check for the final Tin Tower shortcut and Rocket ambush."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
maps = root / "data" / "maps"
first = json.loads((maps / "TinTower_1F_hns" / "map.json").read_text())
statues = {(7, 16), (11, 16), (7, 17), (11, 17)}
wired = {
    (event["x"], event["y"])
    for event in first["bg_events"]
    if event.get("script") == "EcruteakBellchimeTrail_EventScript_RelicShortcut"
}
assert wired == statues, (wired, statues)

shortcut = (maps / "BellchimeTrail_hns" / "scripts.inc").read_text()
assert "goto_if_set FLAG_PJR_RELIC_HO_OH" in shortcut
assert "goto_if_set FLAG_DEFEATED_RED" in shortcut
assert "warp MAP_TIN_TOWER_ROOF_DAY_HNS, 10, 13" in shortcut

for suffix in ("RoofDay", "RoofNight"):
    map_data = json.loads((maps / f"TinTower_{suffix}_hns" / "map.json").read_text())
    npcs = [obj for obj in map_data["object_events"] if obj.get("local_id") in
            ("LOCALID_TINTOWER8F_JESSIE", "LOCALID_TINTOWER8F_JAMES")]
    assert len(npcs) == 2, suffix
    assert all(obj["y"] == 11 for obj in npcs), suffix
    assert any(o.get("script") == "TinTower_RoofDay_EventScript_HoOh"
               for o in map_data["object_events"]), suffix
    scripts = (maps / f"TinTower_{suffix}_hns" / "scripts.inc").read_text()
    assert "MAP_SCRIPT_ON_FRAME_TABLE, TinTower_RoofDay_OnFrame" in scripts

roof = (maps / "TinTower_RoofDay_hns" / "scripts.inc").read_text()
assert "map_script_2 VAR_TEMP_0, 1, TinTower_8F_EventScript_JessieJamesBattle" in roof
party = (root / "src" / "data" / "trainers_hns.party").read_text().split(
    "=== TRAINER_JESSIE_JAMES_TINTOWER_HNS ===", 1)[1].split("===", 1)[0]
assert "Ghoulbat @ Life Orb" in party
assert "Meowth @" not in party
assert "Pikachu @ Light Ball" in party
print("PASS: both statues lead directly to rooftop; save backfill, Rocket ambush and Ho-Oh retained")

generic = (maps / "RuinsOfAlph_PuzzleAndRewardChambers_hns" / "scripts.inc").read_text()
assert "specialvar VAR_RESULT, IsPjrTinTowerEntranceStatue" in generic
assert "goto_if_eq VAR_RESULT, TRUE, EcruteakBellchimeTrail_EventScript_RelicShortcut" in generic
special = (root / "src/field_specials.c").read_text()
assert "MAP_GROUP(MAP_TIN_TOWER_1F_HNS)" in special
assert "MAP_NUM(MAP_TIN_TOWER_1F_HNS)" in special
assert "x -= MAP_OFFSET;" in special and "y -= MAP_OFFSET;" in special
assert "def_special IsPjrTinTowerEntranceStatue" in (root / "data/specials.inc").read_text()
print("PASS: runtime generic statue fallback resolves entrance statues only")
