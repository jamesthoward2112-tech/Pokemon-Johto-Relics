#!/usr/bin/env python3
"""Fail closed when the save-compatible PRU species import is incomplete."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


DONOR_COMMIT = "6ee9b984521ac6f2beaf995f771a726379e55c88"
NEW_SPECIES = (
    "GEMLIN", "VALKYVOIR", "SCEPTITAN", "SOLAZIKEN", "SWAMPLITH",
    "SKULBERUS", "GEMIGOYLE", "MAWYRM", "TORKALDERA", "CACTOMB",
    "TROPISAUR", "COELOSSUS", "ASTRACHI", "EEVEEON", "NIMBEON",
    "ADNOKANA", "CHEAUKING", "FRYTNING", "MEWSION",
)


def parse_species(path: Path) -> dict[str, int]:
    result: dict[str, int] = {}
    pattern = re.compile(r"^#define\s+(SPECIES_[A-Z0-9_]+)\s+(\d+)\s*$")
    for line in path.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line)
        if match:
            result[match.group(1)] = int(match.group(2))
    return result


def frozen_digest(constants: dict[str, int], maximum: int) -> tuple[int, str]:
    entries = sorted(
        ((name, value) for name, value in constants.items() if value <= maximum),
        key=lambda item: (item[1], item[0]),
    )
    payload = "\n".join(f"{name}={value}" for name, value in entries).encode()
    return len(entries), hashlib.sha256(payload).hexdigest()


def species_block(text: str, name: str) -> str:
    start = text.find(f"[SPECIES_{name}]")
    if start == -1:
        return ""
    end = text.find("\n[SPECIES_", start + 1)
    return text[start:end if end != -1 else None]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--donor", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    donor = args.donor.resolve()
    failures: list[str] = []

    donor_head = subprocess.check_output(
        ["git", "-C", str(donor), "rev-parse", "HEAD"], text=True
    ).strip()
    if donor_head != DONOR_COMMIT:
        failures.append(f"wrong pinned PRL donor: {donor_head}")

    baseline = json.loads(
        (root / "tools/pru/baselines/pjr_ids_through_1623.json").read_text()
    )
    constants = parse_species(root / "include/constants/species.h")
    count, digest = frozen_digest(constants, baseline["maximum_frozen_species_id"])
    if count != baseline["normalized_mapping_entry_count"] or digest != baseline["normalized_mapping_sha256"]:
        failures.append("existing species IDs through 1623 changed")
    for name, value in baseline["tail_anchors"].items():
        if constants.get(name) != value:
            failures.append(f"frozen anchor changed: {name}")

    for species_id, name in enumerate(NEW_SPECIES, start=1624):
        if constants.get(f"SPECIES_{name}") != species_id:
            failures.append(f"SPECIES_{name} must be {species_id}")
    if "SPECIES_NUMEW" in constants:
        failures.append("superseded nuMew must not be imported")

    index = (root / "src/data/pokemon/species_info.h").read_text(encoding="utf-8")
    if '#include "species_info/pru_custom.h"' not in index:
        failures.append("PRU custom species table is not included")
    custom_path = root / "src/data/pokemon/species_info/pru_custom.h"
    custom = custom_path.read_text(encoding="utf-8") if custom_path.exists() else ""
    graphics = (root / "src/data/graphics/pokemon.h").read_text(encoding="utf-8")
    for name in NEW_SPECIES:
        if not species_block(custom, name):
            failures.append(f"personal data missing: {name}")
        symbol = name.title().replace("_", "")
        for kind in ("FrontPic", "BackPic", "Palette", "ShinyPalette", "Icon"):
            if f"gMon{kind}_{symbol}" not in graphics:
                failures.append(f"graphics registration missing: {name} {kind}")
        for asset in ("front.png", "back.png", "icon.png", "normal.pal", "shiny.pal"):
            if not (root / "graphics/pokemon" / name.lower() / asset).is_file():
                failures.append(f"asset missing: {name}/{asset}")

    exact_fields = {
        "ADNOKANA": (".baseHP = 90", ".baseAttack = 115", ".baseDefense = 80", ".baseSpAttack = 75", ".baseSpDefense = 105", ".baseSpeed = 105", "TYPE_POISON, TYPE_STEEL"),
        "CHEAUKING": (".baseHP = 75", ".baseAttack = 105", ".baseDefense = 130", ".baseSpAttack = 100", ".baseSpDefense = 80", ".baseSpeed = 65", "TYPE_POISON, TYPE_DARK"),
        "FRYTNING": (".baseHP = 95", ".baseAttack = 65", ".baseDefense = 125", ".baseSpAttack = 90", ".baseSpDefense = 75", ".baseSpeed = 70", "TYPE_DARK, TYPE_ELECTRIC"),
        "MEWSION": (".baseHP = 106", ".baseAttack = 154", ".baseDefense = 90", ".baseSpAttack = 110", ".baseSpDefense = 90", ".baseSpeed = 130", "TYPE_DARK, TYPE_PSYCHIC"),
    }
    for name, fields in exact_fields.items():
        block = species_block(custom, name)
        for field in fields:
            if field not in block:
                failures.append(f"approved donor field missing: {name} {field}")

    gen2 = (root / "src/data/pokemon/species_info/gen_2_families.h").read_text(encoding="utf-8")
    for marker in ("[SPECIES_WOOPER]", "[SPECIES_QUAGSIRE]", "[SPECIES_WOOPER_PALDEA]", "[SPECIES_CLODSIRE]"):
        if marker not in gen2:
            failures.append(f"Wooper-family compatibility marker missing: {marker}")

    if failures:
        print("PRU species import verification FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("PRU species import verification passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
