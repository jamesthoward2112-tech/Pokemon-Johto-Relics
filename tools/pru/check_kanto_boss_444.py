#!/usr/bin/env python3
"""Require Kanto Gym/Rocket boss teams to use canonical PRU species only.

Legacy "X Relic" labels are battle-only appearances of an eligible Gen 1-3
base species, not new National Dex entries. This does not audit all of Johto.
"""
import csv
import re
from pathlib import Path

DEX = Path("data/pru/PRU_National_Pokedex_2026-10-16.csv")
PARTY = Path("src/data/trainers_hns.party")
TRAINERS = {
    "BROCK", "MISTY", "LTSURGE", "ERIKA", "JANINE", "SABRINA",
    "BLAINE", "BLUE", "GIOVANNI", "BROCK_POSTOBC",
    "MISTY_POSTOBC", "LTSURGE_POSTOBC", "ERIKA_POSTOBC",
    "JANINE_POSTOBC", "SABRINA_POSTOBC", "BLAINE_POSTOBC",
    "BLUE_POSTOBC", "KOGA_POSTOBC",
}

def normalize(s):
    return re.sub(r"[^A-Z0-9]", "", s.upper())

with DEX.open(encoding="utf-8-sig", newline="") as stream:
    rows = list(csv.DictReader(stream))
assert len(rows) == 444
allowed = {normalize(r["Name"]) for r in rows}
# Keep approved internal species constants as aliases for renamed custom mons
# (e.g. Valkiri is still compiled as SPECIES_VALKYVOIR).
allowed |= {normalize(r["Species_Constant"].removeprefix("SPECIES_")) for r in rows}
text = PARTY.read_text(encoding="utf-8")
blocks = re.split(r"(?=^=== TRAINER_)", text, flags=re.M)
seen = set()
errors = []
checked = 0
for block in blocks:
    m = re.match(r"=== TRAINER_(\w+)_HNS ===", block)
    if not m or m.group(1) not in TRAINERS:
        continue
    trainer = m.group(1)
    seen.add(trainer)
    lines = block.splitlines()
    for i, line in enumerate(lines):
        if not re.match(r"^Level:\s*\d+", line.strip()):
            continue
        j = i - 1
        while j >= 0 and re.match(r"^(?:Ability|Gender|Shiny|Nature|IVs|EVs|Happiness|Ball|Tera Type):", lines[j].strip()):
            j -= 1
        if j < 0:
            continue
        species = lines[j].strip().split(" @ ")[0].strip()
        base = re.sub(r"\s+Relic$", "", species, flags=re.I)
        checked += 1
        if normalize(base) not in allowed:
            errors.append(f"{trainer}: {species}")

assert seen, "No Kanto Gym/Rocket boss teams found"
if errors:
    raise SystemExit("Kanto boss species not in PRU 444:\n" + "\n".join(errors))
print(f"PRU_KANTO_BOSS_444_PASS: {len(seen)} teams; {checked} Pokémon, canonical species/forms")
