#!/usr/bin/env python3
"""Fail fast on unavailable PRU move identifiers before a full 5+ minute GBA build.

Do not use vanilla stand-ins or placeholder enums: missing authentic move data
must be implemented with its correct effect and animation before ROM release.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

PATHS = (
    Path("src/data/pokemon/level_up_learnsets/pru.h"),
    Path("src/data/pokemon/teachable_learnsets/pru.h"),
)
MOVE_CONSTANTS = Path("include/constants/moves.h")
MOVE_INFO = Path("src/data/moves_info.h")
PATTERN = re.compile(r"\bMOVE_[A-Z0-9_]+\b")


def check(root: Path) -> tuple[list[str], list[str]]:
    names = set()
    for path in PATHS:
        names.update(PATTERN.findall((root / path).read_text()))
    declarations = set(PATTERN.findall((root / MOVE_CONSTANTS).read_text()))
    data = (root / MOVE_INFO).read_text()
    missing = sorted(names - declarations)
    no_move_data = sorted(m for m in names & declarations if f"[{m}]" not in data)
    # A legacy enum alias may exist without a literal table entry. Name these
    # separately and review; neither category is silently made 'implemented'.
    return missing, no_move_data


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path("."))
    ap.add_argument("--report-only", action="store_true")
    args = ap.parse_args()
    undefined, incomplete = check(args.root)
    print(f"PRU learnsets: {len(undefined)} undeclared custom move identifiers")
    for name in undefined:
        print(f"  MISSING_CONSTANT {name}")
    print(f"PRU learnsets: {len(incomplete)} declared names without literal move-table entries")
    for name in incomplete:
        print(f"  CHECK_MOVE_INFO {name}")
    if undefined and not args.report_only:
        print("FAIL: authentic move integration required before expensive ROM compilation")
        return 1
    if incomplete:
        print("NOTE: review alias/conditional lookup before declaring move data complete")
    else:
        print("PASS: every referenced move constant has a data entry")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
