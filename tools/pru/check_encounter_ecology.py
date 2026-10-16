#!/usr/bin/env python3
"""PRU HNS wild-encounter ecology regression gate.

Checks source encounter data only; it does NOT replace a GBA compile or mGBA
walkthrough. Merging this branch requires SPECIES_GEMLIN to be engine-registered.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path

STARTERS = {
    "MAP_ROUTE29_HNS": ("CHIKORITA", "MOOTINY"),
    "MAP_ROUTE30_HNS": ("CYNDAQUIL", "TREECKO"),
    "MAP_ROUTE31_HNS": ("BULBASAUR", "SCARABUB"),
    "MAP_ROUTE32_HNS": ("SQUIRTLE",),
    "MAP_ROUTE33_HNS": ("TORCHIC",),
    "MAP_ROUTE46_HNS": ("CHARMANDER", "SKARMET"),
    "MAP_SLOWPOKE_WELL_B1F_HNS": ("TOTODILE",),
    "MAP_UNION_CAVE_B1F_HNS": ("MUDKIP",),
    "MAP_DARK_CAVE_SOUTH_SIDE_HNS": ("GEMLIN",),
}

RELIC_WILD_BAN = {
    "EDENSAUR", "CHARAXIS", "FORTOTOISE", "KHANG", "NOLAX",
    "NOXICHU", "GHOULBAT", "OSTEODIAN", "MAROGHOST",
    "ADNOKANA", "CHEAUKING", "FRYTNING",
    "EEVEEON", "NIMBEON", "CHAMPEON", "LEPIDEON",
    "SPHYNXEON", "GUARDEON", "OBSIDEON", "TOXEON",
    "OMEON", "DRAKEON", "MYSTYNX", "PINSIREX",
    "FAERANIUM", "PYROCLAST", "FERALODON", "GRIMFOWL",
    "SUNFLORID", "KABLOWFISH", "SHUCKOLOSSE",
    "HERACURION", "JOLLIBIRD", "SKARMADON",
    "DONPHALANX", "MILTITAN", "SCEPTITAN", "SOLAZIKEN",
    "SWAMPLITH", "SKULBERUS", "VALKYVOIR", "GEMIGOYLE",
    "MAWYRM", "TORKALDERA", "CACTOMB", "TROPISAUR",
}

LEGENDARY_WILD_BAN = {
    "ARTICUNO", "ZAPDOS", "MOLTRES", "MEWTWO", "MEW",
    "MEWSION", "RAIKOU", "ENTEI", "SUICUNE", "LUGIA", "HO_OH",
    "ALPHORACLE", "CELEBI", "REGIROCK", "REGICE", "REGISTEEL",
    "LATIAS", "LATIOS", "KYOGRE", "GROUDON", "RAYQUAZA",
    "COELOSSUS", "JIRACHI", "ASTRACHI", "DEOXYS",
}

EARLY_MAPS = {
    "MAP_ROUTE29_HNS", "MAP_ROUTE30_HNS", "MAP_ROUTE31_HNS",
    "MAP_ROUTE32_HNS", "MAP_ROUTE33_HNS", "MAP_ROUTE46_HNS",
    "MAP_DARK_CAVE_SOUTH_SIDE_HNS",
}
EARLY_PSEUDOS = {
    "LARVITAR", "PUPITAR", "TYRANITAR", "DRATINI",
    "DRAGONAIR", "DRAGONITE", "BAGON", "SHELGON", "SALAMENCE",
    "BELDUM", "METANG", "METAGROSS", "GIBLE", "GABITE",
    "GARCHOMP", "DEINO", "DREEPY", "JANGMO_O",
}


def require(ok: bool, message: str) -> None:
    if not ok:
        raise AssertionError(message)


def check(path: Path, require_engine: bool) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    main = next(group for group in data["wild_encounter_groups"]
                if group["label"] == "gWildMonHeaders")
    entries = [e for e in main["encounters"] if e["map"].endswith("_HNS")]
    require(len(entries) == 257, f"Expected existing 257 HNS day/night variants, got {len(entries)}")
    mons = []
    land = {}
    for entry in entries:
        row = []
        for field in ("land_mons", "water_mons", "rock_smash_mons", "fishing_mons"):
            for mon in entry.get(field, {}).get("mons", []):
                require(1 <= mon["min_level"] <= mon["max_level"] <= 100,
                        f"Invalid encounter level: {entry['map']} {mon}")
                name = mon["species"].removeprefix("SPECIES_")
                mons.append(name)
                if field == "land_mons":
                    row.append((name, mon["min_level"], mon["max_level"]))
        land.setdefault(entry["map"], []).append(row)

    counts = Counter(mons)
    for name in sorted(RELIC_WILD_BAN | LEGENDARY_WILD_BAN):
        require(not counts[name], f"Reserved Relic / legendary illegally wild: {name}")

    for name in ("WOOPER", "QUAGSIRE", "WOOPER_PALDEA", "CLODSIRE"):
        require(counts[name] > 0, f"Missing distinct original/Paldean line: {name}")
    require(counts["WOOPER"] >= 30 and counts["QUAGSIRE"] >= 100,
            "Most original Wooper/Quagsire habitats must remain intact")
    require(counts["WOOPER_PALDEA"] <= 8 and counts["CLODSIRE"] <= 8,
            "Paldean line should be a rare distinct encounter, not blanket replacement")

    for map_id, wanted in STARTERS.items():
        rows = land.get(map_id, [])
        require(rows, f"Missing early encounter table: {map_id}")
        for name in wanted:
            require(any(n == name and 2 <= lo <= hi <= 9 for row in rows
                        for n, lo, hi in row),
                    f"Early unobtainable pre-evolution: {name} ({map_id})")
    for map_id in EARLY_MAPS:
        for row in land.get(map_id, []):
            for name, lo, hi in row:
                require(name not in EARLY_PSEUDOS,
                        f"Pseudo-legendary on novice route {map_id}: {name}")

    for map_id in ("MAP_ROUTE26_HNS", "MAP_ROUTE27_HNS"):
        for row in land[map_id]:
            require(all(lo >= 30 for name, lo, hi in row),
                    f"Under-level wild slot on League approach: {map_id}")
    for map_id, rows in land.items():
        if map_id.startswith("MAP_MT_SILVER_"):
            for row in rows:
                for name, lo, hi in row:
                    if name in ("LARVITAR", "PUPITAR"):
                        require(lo >= 50, f"Under-level {name} on Mt Silver")

    if require_engine:
        species = (path.parents[2] / "include/constants/species.h").read_text()
        require("#define SPECIES_GEMLIN " in species,
                "SPECIES_GEMLIN must be imported before compiling this encounter branch")

    print(f"PASS: {len(entries)} HNS encounter variants, {len(counts)} unique species symbols")
    for name in ("WOOPER", "QUAGSIRE", "WOOPER_PALDEA", "CLODSIRE",
                 "GEMLIN", "SCARABUB", "SKARMET", "MOOTINY", "LARVITAR"):
        print(f"  {name}: {counts[name]} encounter slots")
    print("Legendary/static encounters are excluded from this wild-table test.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=Path, default=Path("src/data/wild_encounters.json"))
    parser.add_argument("--require-engine", action="store_true")
    args = parser.parse_args()
    check(args.file, args.require_engine)
