#!/usr/bin/env python3
"""Source-only inspection of PRU's rare gift replacements and catchable paths."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
def source(path):
    return (ROOT/path).read_text(errors="replace")

violet = source("data/maps/VioletCity_hns/scripts.inc")
vmap = json.loads(source("data/maps/VioletCity_hns/map.json"))
steven = source("data/maps/SaffronCity_SilphCo_hns/scripts.inc")
menu = source("src/data/script_menu.h")
assert "givemon SPECIES_RALTS, 8" in violet
assert "FLAG_PJR_GOT_CHIKORITA" in violet  # stable legacy save flag
assert "MON_GIVEN_TO_PC" in violet and "MON_GIVEN_TO_PARTY" in violet
assert "setflag FLAG_PJR_GOT_CHIKORITA" in violet
assert any(x.get("graphics_id") == "OBJ_EVENT_GFX_MON_BASE+SPECIES_RALTS"
           and x.get("script") == "VioletCity_EventScript_PJRGiftChikoritaMon"
           for x in vmap["object_events"])
for pokemon in ("TREECKO", "BELDUM", "BAGON"):
    assert f"givemon SPECIES_{pokemon}," in steven
    assert f'COMPOUND_STRING("{pokemon}")' in menu
for unwanted in ("TORCHIC", "MUDKIP"):
    assert f"givemon SPECIES_{unwanted}" not in steven
assert "SaffronCity_SilphCo_EventScript_CheckGiftSuccess::" in steven
assert "MON_GIVEN_TO_PC" in steven and "MON_GIVEN_TO_PARTY" in steven
assert steven.index("SaffronCity_SilphCo_EventScript_CheckGiftSuccess::") < steven.index("SaffronCity_SilphCo_EventScript_AfterStarterGiven::")

# Report independent encounter registration, not just an NPC giver.
wild = source("src/data/wild_encounters.json")
for pokemon in ("RALTS", "TREECKO", "BELDUM", "BAGON"):
    count = wild.count('"SPECIES_' + pokemon + '"')
    print(f"WILD_ROUTE_SCAN {pokemon}: {count} encounter slots (all regions; review Johto/Kanto accessibility)")
    if not count:
        print(f"WARNING: {pokemon} has no direct wild encounter in current live encounters. Do not claim independent catchability yet.")
print("PASS: Violet Ralts gift + Steven Treecko/Beldum/Bagon choices and full-storage retry safeguards are in source")
