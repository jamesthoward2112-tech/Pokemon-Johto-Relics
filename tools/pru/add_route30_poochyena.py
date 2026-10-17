#!/usr/bin/env python3
"""PRU: add an early-game Poochyena grass encounter to every Route 30 table.

This small overlay intentionally patches wild_encounters.json *before* the hns
ROM is compiled, without copying/reformatting the huge upstream encounter file
in Git. It preserves other maps, rates, time-of-day tables and rare spawns.
"""
from pathlib import Path
import json

PATH = Path("src/data/wild_encounters.json")
ROUTE = "MAP_ROUTE30_HNS"
SPECIES = "SPECIES_POOCHYENA"
COMMON = {
    "SPECIES_RATTATA", "SPECIES_SENTRET", "SPECIES_PIDGEY",
    "SPECIES_HOOTHOOT", "SPECIES_CATERPIE", "SPECIES_WEEDLE"
}

def records(node):
    if isinstance(node, dict):
        if node.get("map") == ROUTE:
            yield node
        for value in node.values():
            yield from records(value)
    elif isinstance(node, list):
        for value in node:
            yield from records(value)

def main():
    data = json.loads(PATH.read_text(encoding="utf-8"))
    found = list(records(data))
    if not found:
        raise SystemExit(f"Route 30 encounter records not found for {ROUTE}")
    changed = 0
    for record in found:
        land = record.get("land_mons")
        if not isinstance(land, dict) or not isinstance(land.get("mons"), list):
            continue
        mons = land["mons"]
        if not mons:
            continue
        if any(slot.get("species") == SPECIES for slot in mons):
            print("Route 30 grass already contains Poochyena; no duplicate")
            continue
        # Prefer a mid-weight common encounter rather than removing rare babies.
        candidates = [
            i for i, slot in enumerate(mons)
            if isinstance(slot, dict) and slot.get("species") in COMMON
        ]
        preferred = [i for i in candidates if 2 <= i <= 7]
        if preferred:
            index = preferred[0]
        elif candidates:
            index = candidates[0]
        else:
            raise SystemExit(
                "Route 30 has no common Rattata/Sentret/Pidgey/Hoothoot slot;"
                " do not overwrite unknown/rare Pokémon automatically."
            )
        slot = mons[index]
        previous = slot["species"]
        slot["species"] = SPECIES
        # Route 30 is an early-game location, even in late-game ROM builds.
        if "min_level" in slot:
            slot["min_level"] = 3
        if "max_level" in slot:
            slot["max_level"] = 5
        changed += 1
        print(f"Route 30 grass [{record.get('base_label', 'default')}] "
              f"slot {index}: {previous} -> {SPECIES}, Lv 3-5")
    if changed == 0 and not any(
        isinstance(r.get("land_mons"), dict)
        and any(m.get("species") == SPECIES
                for m in r["land_mons"].get("mons", []))
        for r in found
    ):
        raise SystemExit("Route 30 has no grass encounter tables")
    PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"PASS: Route 30 Poochyena encounter patch; {changed} tables changed")

if __name__ == "__main__":
    main()
