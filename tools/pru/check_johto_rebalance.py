#!/usr/bin/env python3
"""Guard PRU's 18 October 2026 Johto difficulty rebalance.

This verifies first-encounter party levels, unaffected Gym Leaders, representative
wild encounter tables, and preservation of early starters. It does not claim
save-file gameplay tests or prove encounter ecology for all 444 species.
"""
import json
import re
from pathlib import Path

trainers = Path("src/data/trainers_hns.party").read_text()
encounters = json.loads(Path("src/data/wild_encounters.json").read_text())
def party(trainer):
    match = re.search(
        r"^=== TRAINER_" + re.escape(trainer) + r"_HNS ===\s*$(.*?)(?=^=== TRAINER_|\Z)",
        trainers, re.MULTILINE | re.DOTALL
    )
    assert match, f"Missing trainer {trainer}"
    values = [int(x) for x in re.findall(r"^Level:\s*(\d+)", match.group(1), re.MULTILINE)]
    assert values, f"Trainer {trainer} has no team"
    return values

for area, members, floor in [
    ("Route30", ("JOEY", "MIKEY", "DON"), 5),
    ("Route32", ("JUSTIN", "RALPH", "HENRY", "ALBERT", "GORDON", "ROLAND", "LIZ", "PETER"), 12),
    ("Route34", ("SAMUEL", "IAN", "TODD", "GINA", "KEITH", "BRANDON", "IRENE", "JENN", "KATE"), 19),
    ("Route35", ("IVAN", "ELLIOT", "BROOKE", "KIM", "BRYAN", "IRWIN", "ARNIE", "WALT", "DIRK"), 24),
    ("NationalPark", ("JACK", "BEVERLY", "WILLIAM", "KRISE"), 25),
    ("Route37", ("ANN_AND_ANNE", "GREG"), 28),
    ("Route38", ("TOBY", "CHAD", "DANA", "VALERIE", "HARRY", "OLIVIA"), 30),
    ("CianwoodGym", ("YOSHI", "LAO", "NOB", "LUNG"), 34),
    ("RocketHideout", ("JED", "GRUNT_13", "GRUNT_14", "GRUNT_15", "GRUNT_16", "GRUNT_29", "ROSS", "MITCH"), 34),
    ("Route44", ("WILTON", "EDGAR", "VANCE", "PHIL", "ZACH", "ALLEN", "CYBIL"), 39),
    ("Route45", ("ERIK", "MICHAEL", "PARRY", "TIMOTHY", "KENJI", "RYAN", "KELLY", "QUENTIN"), 43),
    ("BlackthornGym", ("CODY", "FRAN", "PAUL", "MIKE", "LOLA"), 46),
    ("DragonsDen", ("DARIN", "CARA", "LEA_AND_PIA"), 48),
    ("Route26", ("JAKE", "GAVEN", "JOYCE", "BETH", "RICHARD"), 47),
    ("Route27", ("BLAKE", "BRIAN", "REENA", "MEGAN", "GILBERT", "JOSE", "SCOTT"), 47),
]:
    for member in members:
        found = party(member)
        assert min(found) >= floor, f"{area} {member}: {found}, expected floor {floor}"

assert party("WHITNEY_1") == [23, 24, 24, 25, 27], "Whitney first fight changed"
assert party("MORTY_1") == [29, 30, 30, 31, 33], "Morty first fight changed"

hns = {}
for group in encounters["wild_encounter_groups"]:
    if group.get("for_maps"):
        for entry in group.get("encounters", []):
            if entry.get("map", "").endswith("_HNS"):
                hns.setdefault(entry["map"], []).append(entry)
for m, min_level, max_level in [
    ("MAP_ROUTE34_HNS", 16, 22),
    ("MAP_ROUTE35_HNS", 21, 27),
    ("MAP_NATIONAL_PARK_NORMAL_HNS", 22, 28),
    ("MAP_ROUTE37_HNS", 24, 29),
    ("MAP_ROUTE38_HNS", 27, 32),
    ("MAP_ROUTE42_HNS", 28, 34),
    ("MAP_ROUTE43_HNS", 30, 37),
    ("MAP_ROUTE44_HNS", 36, 43),
    ("MAP_ICE_PATH_1F_HNS", 38, 43),
    ("MAP_ROUTE45_HNS", 40, 46),
    ("MAP_ROUTE26_HNS", 44, 51),
    ("MAP_ROUTE27_HNS", 44, 51),
]:
    variants = hns.get(m, [])
    assert variants, f"Missing day/night map {m}"
    for variant in variants:
        land = variant.get("land_mons", {}).get("mons", [])
        if not land:
            continue
        assert all(min_level <= slot["min_level"] <= slot["max_level"] <= max_level for slot in land), m

# Do not break approved starter / relic early-access encounters (Route29-33).
for m, species in [
    ("MAP_ROUTE29_HNS", "SPECIES_CHIKORITA"),
    ("MAP_ROUTE30_HNS", "SPECIES_CYNDAQUIL"),
    ("MAP_ROUTE31_HNS", "SPECIES_BULBASAUR"),
    ("MAP_ROUTE32_HNS", "SPECIES_SQUIRTLE"),
    ("MAP_ROUTE33_HNS", "SPECIES_TORCHIC"),
]:
    assert any(
        slot["species"] == species
        for variant in hns.get(m, [])
        for slot in variant.get("land_mons", {}).get("mons", [])
    ), f"Lost early acquisition: {species} at {m}"

print("PRU_JOHTO_REBALANCE_PASS: ordinary trainer levels, Gym leaders, wild encounter tiers, early starters")
