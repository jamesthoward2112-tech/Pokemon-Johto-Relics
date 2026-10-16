#!/usr/bin/env python3
"""Inventory every registered HNS map's player-facing dialogue for standalone PRU.

The report is a review queue, NOT proof that a text block is reachable or that
an identified term is a contradiction. Use the original PJR flags and map
scripts when deciding whether a rewrite is safe.
"""
import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

STRING = re.compile(r'^\s*\.string\s+"((?:[^"\\]|\\.)*)"')
LABEL = re.compile(r'^([A-Za-z_][A-Za-z_0-9.]*)::?\s*$')
COMMAND = re.compile(r'^\s*(giveegg|givemon|createmon|setflag|clearflag|setvar|wildbattle|trainerbattle\w*)\b', re.I)
CATEGORIES = (
    ("P0_review_prior_game", re.compile(
        r'\b(?:PKR|PHR|PJR|PRL)\b|(?:previous|earlier|last)\s+(?:adventure|journey|region|ROM|game)|'
        r'(?:two|2)\s+years\s+(?:after|since)|(?:returning|former)\s+(?:KANTO|HOENN)\s+CHAMPION|'
        r'RELIC\s+LEGACY|S[.]S[.]\s+LEGACY', re.I)),
    ("P0_review_transfer", re.compile(
        r'(?:transfer|donat|box|bank|reset)\w*.{0,55}(?:POK[eÉ]MON|PARTY|BAG|ITEMS|MONEY|HOENN)|'
        r'(?:HOENN|KANTO).{0,55}(?:transfer|donat|box|bank|reset)\w*', re.I)),
    ("P0_review_starter", re.compile(
        r'(?:choose|pick|take)\s+(?:one of|from)\s+(?:these|the three|three)|'
        r'(?:other|remaining|different)\s+(?:two|starter|partner|egg)s?', re.I)),
    ("P1_review_timeline", re.compile(
        r'GIOVANNI|TEAM ROCKET|ARCHER|SILPH|GOLDEN BIRD|FOURTH BIRD|'
        r'KANTO CHAMPION|HOENN CHAMPION|HOENN LEAGUE|BIRCH|RELICANTH', re.I)),
    ("P1_review_relic_lore", re.compile(
        r'RELIC|RESONANCE|RUINS OF ALPH|ALPHORACLE|HO-OH|ANCIENT RAINBOW|'
        r'MEGA RING|SINJOH|UNOWN', re.I)),
    ("P2_review_gifts", re.compile(r'\b(?:GIFT|EGG|STARTER|GIVE YOU|TAKE THIS POK[eÉ]MON)\b', re.I)),
)
GRANT = re.compile(r'\bSPECIES_([A-Z0-9_]+)', re.I)
FLAGS = re.compile(r'\b(?:FLAG_(?:PJR_|IS_CHAMPION|IS_KANTO_CHAMPION)|VAR_(?:STARTER|NEWBARK))\w*')
CONTROLS = re.compile(r'\\[npl]')


def text_entries(file_path, root):
    """Yield complete adjacent .string chunks with source label and start line."""
    lines = file_path.read_text(encoding="utf-8", errors="replace").splitlines()
    label = ""
    chunk = []
    start = 0
    for n, line in enumerate(lines, 1):
        match = STRING.search(line)
        if match:
            if not chunk:
                start = n
            chunk.append(match.group(1))
            continue
        if chunk:
            yield start, label, "".join(chunk).replace("\\n", " ").replace("\\p", " ").replace("\\l", " ")
            chunk = []
        found = LABEL.match(line)
        if found:
            label = found.group(1)
    if chunk:
        yield start, label, "".join(chunk).replace("\\n", " ").replace("\\p", " ").replace("\\l", " ")


def audit(root):
    groups_file = root / "data/maps/map_groups.json"
    data = json.loads(groups_file.read_text(encoding="utf-8"))
    groups = {key: value for key, value in data.items()
              if key != "group_order" and key.endswith("_Hns") and isinstance(value, list)}
    registered = sorted({name for maps in groups.values() for name in maps})
    paths = []
    missing = []
    for name in registered:
        folder = root / "data/maps" / name
        if not (folder / "map.json").is_file():
            missing.append(name + ":map.json")
        incs = sorted(folder.rglob("*.inc")) if folder.is_dir() else []
        if not incs:
            missing.append(name + ":scripts")
        paths.extend(("registered-HNS-map", file) for file in incs)
    # Common scripts can be invoked by a live HNS map; they need their own
    # reachability check before any purported previous-ROM text is edited.
    for folder in (root / "data/scripts", root / "data/text"):
        if folder.is_dir():
            paths.extend(("shared-unverified", p) for p in sorted(folder.rglob("*.inc")))

    results = []
    for scope, file_path in paths:
        rel = file_path.relative_to(root).as_posix()
        for line, label, displayed in text_entries(file_path, root):
            for category, regex in CATEGORIES:
                if regex.search(displayed):
                    results.append(dict(scope=scope, category=category,
                                        path=rel, line=line, label=label,
                                        text=displayed.strip()))
        for line, raw in enumerate(file_path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            command = COMMAND.search(raw)
            if command and (command.group(1).lower() in ("giveegg", "givemon", "createmon", "wildbattle")
                            or FLAGS.search(raw)):
                results.append(dict(scope=scope, category="P1_review_events_flags",
                                    path=rel, line=line, label="",
                                    text=raw.strip()))

    return registered, paths, missing, results


def write(root, out):
    out.mkdir(parents=True, exist_ok=True)
    registered, paths, missing, rows = audit(root)
    fields = ("scope", "category", "path", "line", "label", "text")
    with (out / "PRU_DIALOGUE_INVENTORY.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    (out / "PRU_DIALOGUE_INVENTORY.json").write_text(
        json.dumps({"registered_hns_maps": len(registered),
                    "scanned_inc_files": len(paths), "missing": missing,
                    "findings": rows}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    counts = Counter(row["category"] for row in rows)
    md = [
        "# PRU dialogue inventory — machine-generated review queue",
        "",
        "This is exhaustive over .inc text in registered *_Hns map groups,",
        "plus shared .inc scripts. It is NOT an exhaustive semantic sign-off,",
        "and code may have unreachable strings. FRLG/HNSEmerald donor maps",
        "are excluded unless included in a registered HNS group.",
        "A hit is a review candidate, not an automatic defect.",
        "",
        "## Coverage",
        "",
        "- Registered HNS maps: " + str(len(registered)),
        "- Scanned HNS/shared .inc files: " + str(len(paths)),
        "- Missing map/scripts paths: " + str(len(missing)),
        "- Review hits: " + str(len(rows)),
        "",
        "## Categories",
        "",
    ]
    md += ["- " + cat + ": " + str(counts[cat]) for cat, _ in CATEGORIES]
    md += ["- P1_review_events_flags: " + str(counts["P1_review_events_flags"]), ""]
    if missing:
        md += ["## Missing paths (must investigate)", ""] + ["- " + name for name in missing] + [""]
    for cat, _ in CATEGORIES:
        subset = [item for item in rows if item["category"] == cat]
        md += ["## " + cat + " (" + str(len(subset)) + " hits)", ""]
        for item in subset[:100]:
            snippet = item["text"].replace("\n", " ").replace("|", "/")[:180]
            md.append("- " + item["path"] + ":" + str(item["line"]) +
                      " (" + item["label"] + "): " + snippet)
        if len(subset) > 100:
            md.append("- ... see full CSV for the other " + str(len(subset)-100) + " hits")
        md.append("")
    md += ["## Manual sign-off still required", "",
           "1. Determine runtime reachability and quest order for flagged labels.",
           "2. Rewrite actual previous-ROM assumptions without changing map events blindly.",
           "3. Map new Relic dialogue to unique event flags and verify catch/retry flows.",
           "4. Resolve all custom-species NPC hints and live Kanto destinations.",
           "5. Emulator-test fresh save, first League, Rocket, Kanto, RELICS, Ho-Oh and Sinjoh.",
           ""]
    (out / "PRU_DIALOGUE_INVENTORY.md").write_text("\n".join(md), encoding="utf-8")
    print("PRU audit: " + str(len(registered)) + " registered HNS maps; " +
          str(len(paths)) + " .inc files; " + str(len(rows)) +
          " review hits; " + str(len(missing)) + " missing paths")
    if missing:
        raise SystemExit("Incomplete HNS map coverage; inspect PRU_DIALOGUE_INVENTORY.md")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--out", type=Path, default=Path("artifacts/pru-dialogue-audit"))
    args = parser.parse_args()
    write(args.root.resolve(), args.out)
