#!/usr/bin/env python3
"""Stage missing canonical PRL sprites in an isolated PJR Ultimate import branch.

This stage copies ONLY original donor art assets. Species IDs, learnsets,
abilities, evolutions and graphics-table registrations are not changed until
the source compatibility checks have been finished. Do not claim a playable
all-Relic ROM from this stage.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path

DONOR_COMMIT = "6ee9b984521ac6f2beaf995f771a726379e55c88"
TO_IMPORT = (
    "EDENSAUR", "CHARAXIS", "FORTOTOISE", "KHANG", "NOLAX",
    "NUMEW", "GEMLIN", "VALKYVOIR", "SCEPTITAN", "SOLAZIKEN",
    "SWAMPLITH", "SKULBERUS", "GEMIGOYLE", "MAWYRM", "TORKALDERA",
    "CACTOMB", "TROPISAUR", "COELOSSUS", "ASTRACHI", "MILTITAN",
    "SHUCKOLOSSE", "DONPHALANX", "FAERANIUM", "PYROCLAST",
    "FERALODON", "DRAKEON", "GHOULBAT", "EEVEEON", "NIMBEON",
)
GRAPHICS = ("front.png", "back.png", "icon.png", "normal.pal", "shiny.pal")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--donor", type=Path, required=True)
    p.add_argument("--root", type=Path, default=Path("."))
    args = p.parse_args()
    root, donor = args.root.resolve(), args.donor.resolve()
    actual = subprocess.check_output(["git", "-C", str(donor), "rev-parse", "HEAD"], text=True).strip()
    if actual != DONOR_COMMIT:
        raise SystemExit(f"Wrong PRL donor: expected {DONOR_COMMIT}, got {actual}")

    results = []
    for species in TO_IMPORT:
        name = species.lower()
        src_dir = donor / "graphics" / "pokemon" / name
        dest_dir = root / "graphics" / "pokemon" / name
        missing = [asset for asset in GRAPHICS if not (src_dir / asset).is_file()]
        if missing:
            raise SystemExit(f"PRL donor sprite incomplete: {species}: {missing}")
        dest_dir.mkdir(parents=True, exist_ok=True)
        copied, preserved = [], []
        for asset in GRAPHICS:
            dest = dest_dir / asset
            if dest.exists():
                preserved.append(asset)
            else:
                shutil.copy2(src_dir / asset, dest)
                copied.append(asset)
        results.append({"species": species, "copied": copied, "preserved_original_PJR": preserved,
                        "registered_in_PJR_engine": False})
        print(f"{species}: added {len(copied)} art files, retained {len(preserved)} existing")

    summary = {
        "status": "donor_art_staged_not_gameplay_implemented",
        "prl_donor_repository": "jamesthoward2112-tech/Pokemon-Relic-Legacy",
        "prl_donor_commit": DONOR_COMMIT,
        "source": "src/data/pokemon/species_info/prl_custom.h",
        "custom_species_awaiting_port": len(results),
        "species": results,
        "next_requirements": [
            "merge the 29 missing species data entries without overwriting PJR's existing 22 entries",
            "add 16 absent numeric species constants while retaining all PJR numeric IDs",
            "register sprite symbols in the pokemon graphics table",
            "import / reconcile custom level-up and teachable learnsets",
            "reconcile special abilities, evolutions, forms, Dex entries and early Johto encounters",
            "compile, run source checks, then emulator-test fresh save end to end",
        ],
    }
    out = root / "docs" / "PRU_PRL_ARTWORK_IMPORT_MANIFEST.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Staged {len(results)} custom species art packs; wrote {out}")


if __name__ == "__main__":
    main()
