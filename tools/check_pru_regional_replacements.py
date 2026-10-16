#!/usr/bin/env python3
"""PRU regional replacement static regression gate (not gameplay proof)."""
import json
from pathlib import Path

root=Path(__file__).resolve().parents[1]
jsonfile=root/"src/data/wild_encounters.json"
d=json.loads(jsonfile.read_text())
wild=[]
for group in d["wild_encounter_groups"]:
    for entry in group.get("encounters",[]):
        if not entry.get("map","").endswith("_HNS"):
            continue
        if "_hns" not in entry.get("base_label","").lower():
            continue
        for label,table in entry.items():
            if isinstance(table,dict) and isinstance(table.get("mons"),list):
                for mon in table["mons"]:
                    wild.append((entry["map"],label,mon["species"]))
species={mon for _,_,mon in wild}
for forbidden in ("SPECIES_WOOPER","SPECIES_QUAGSIRE"):
    assert forbidden not in species, "Vanilla species remains in HNS wild table: "+forbidden
for required in ("SPECIES_WOOPER_PALDEA","SPECIES_CLODSIRE","SPECIES_NOIBAT","SPECIES_NOIVERN"):
    assert required in species, "Missing required PRU wild species: "+required

party=(root/"src/data/trainers_hns.party").read_text()
import re
assert not re.search(r"(?m)^(?:Wooper|Quagsire)\b", party)
assert "Wooper-Paldea" in party and "Clodsire" in party
info=(root/"src/data/pokemon/species_info/gen_6_families.h").read_text()
for key in ("NOIBAT-S","NOIVERN-S","TYPE_ROCK, TYPE_GHOST",
            "ABILITY_LEVITATE, ABILITY_ROCK_HEAD, ABILITY_STURDY",
            "EVO_LEVEL, 36, SPECIES_NOIVERN"):
    assert key in info, "Sevii source property not set: "+key
wooper=(root/"src/data/pokemon/species_info/gen_2_families.h").read_text()
assert "SPECIES_WOOPER_PALDEA" in wooper and "SPECIES_CLODSIRE" in wooper
for label in ("noibat","noivern"):
    base=root/"graphics/pokemon"/label
    assert (base/"anim_front.png").is_file()
    assert (base/"back.png").is_file()
    assert (base/"normal.pal").is_file()
    assert (base/"shiny.pal").is_file()
print("PASS: PRU regional line species, HNS wild encounters, HNS trainer parties, battle graphics references")
