#!/usr/bin/env python3
"""Source-level catchability gate for the nine PRU acquisition-review Pokémon.

This verifies routes/items/evolution definitions, NOT a GBA compile or emulator run.
Use with check_encounter_ecology.py to preserve Johto ecology while integrating PRL.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def must(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)

def species_block(source: str, name: str) -> str:
    marker = f"[SPECIES_{name}] ="
    start = source.find(marker)
    must(start >= 0, f"Missing species definition: {name}")
    end = source.find("\n    [SPECIES_", start + len(marker))
    return source[start:end if end >= 0 else len(source)]

def expect_evolution(source: str, parent: str, target: str, methods: tuple[str, ...]) -> None:
    body = species_block(source, parent)
    fragments = [line.strip() for line in body.splitlines()
                 if f"SPECIES_{target}" in line and "{" in line]
    must(any(all(method in fragment for method in methods) for fragment in fragments),
         f"{parent} -> {target}: missing evolution {methods}; found {fragments}")

def main() -> None:
    data = json.loads((ROOT / "src/data/wild_encounters.json").read_text(encoding="utf-8"))
    table = next(g for g in data["wild_encounter_groups"]
                 if g["label"] == "gWildMonHeaders")
    records = [e for e in table["encounters"] if e.get("map", "").endswith("_HNS")]

    def staged(mon: str, map_id: str, method: str = "land_mons",
               low: int | None = None, high: int | None = None) -> None:
        matched = [m for e in records if e["map"] == map_id
                   for m in e.get(method, {}).get("mons", [])
                   if m["species"] == f"SPECIES_{mon}"
                   and (low is None or m["min_level"] >= low)
                   and (high is None or m["max_level"] <= high)]
        must(bool(matched), f"{mon} missing from {map_id} ({method})")

    staged("TYROGUE", "MAP_MT_MORTAR_1F_SOUTH_HNS", low=18, high=20)
    staged("EEVEE", "MAP_ROUTE29_HNS", low=2, high=4)
    staged("WURMPLE", "MAP_ILEX_FOREST_HNS", low=8, high=9)
    staged("NINCADA", "MAP_UNION_CAVE_1F_HNS", low=8, high=9)
    staged("CLAMPERL", "MAP_ROUTE20_HNS", method="fishing_mons")

    one = (ROOT / "src/data/pokemon/species_info/gen_1_families.h").read_text()
    three = (ROOT / "src/data/pokemon/species_info/gen_3_families.h").read_text()
    expect_evolution(one, "TYROGUE", "HITMONLEE",
                     ("EVO_LEVEL", "20", "IF_ATK_GT_DEF"))
    expect_evolution(one, "TYROGUE", "HITMONTOP",
                     ("EVO_LEVEL", "20", "IF_ATK_EQ_DEF"))
    expect_evolution(one, "EEVEE", "VAPOREON", ("EVO_ITEM", "ITEM_WATER_STONE"))
    expect_evolution(one, "EEVEE", "FLAREON", ("EVO_ITEM", "ITEM_FIRE_STONE"))
    expect_evolution(one, "EEVEE", "ESPEON",
                     ("EVO_LEVEL", "IF_MIN_FRIENDSHIP", "IF_NOT_TIME", "TIME_NIGHT"))
    expect_evolution(one, "EEVEE", "UMBREON",
                     ("EVO_LEVEL", "IF_MIN_FRIENDSHIP", "IF_TIME", "TIME_NIGHT"))
    expect_evolution(three, "WURMPLE", "CASCOON",
                     ("EVO_LEVEL", "7", "IF_PID_UPPER_MODULO_10_LT"))
    expect_evolution(three, "NINCADA", "SHEDINJA",
                     ("EVO_SPLIT_FROM_EVO", "SPECIES_NINJASK"))
    expect_evolution(three, "CLAMPERL", "GOREBYSS",
                     ("EVO_ITEM", "ITEM_DEEP_SEA_SCALE"))

    market = (ROOT / "data/maps/GoldenrodCity_DepartmentStore_2F_hns/scripts.inc").read_text()
    shop = market.split("GoldenrodDeptStore2_RockShop:", 1)[1].split("pokemartlistend", 1)[0]
    for item in ("WATER_STONE", "FIRE_STONE", "DEEP_SEA_SCALE", "DEEP_SEA_TOOTH"):
        must(f"ITEM_{item}" in shop, f"Goldenrod 2F Rock Shop missing ITEM_{item}")
    config = (ROOT / "include/config/pokemon.h").read_text()
    must("P_SHEDINJA_BALL" in config, "Shedinja evolution ball rule absent")

    print("PASS: all nine have specified source evolutions, catchable base species")
    print("PASS: Goldenrod Rock Shop sells required stones and both Deep Sea items")
    print("NOTE: friendship time, Nincada spare-party/ball, Wurmple PID, and")
    print("      item evolution still require actual emulator gameplay testing.")

if __name__ == "__main__":
    main()
