#!/usr/bin/env python3
"""Audit the PRU 444-entry canonical species order against the active engine tree.

Run: python3 tools/pru/check_444_species_dex.py
No network access or third-party packages required; suitable for GitHub Actions.
This is a SOURCE audit, not a compiled-ROM or emulator certificate.
"""
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CANON = ROOT / "data/pru/PRU_National_Pokedex_2026-10-16.csv"
HEADER = ROOT / "include/constants/species.h"
ORDER = ROOT / "src/data/pokemon/pru_dex_order.h"
ENGINE = ROOT / "src/pokemon.c"
SPECIES_INFO = ROOT / "src/data/pokemon/species_info.h"
ENABLED = ROOT / "include/config/species_enabled.h"

with CANON.open(encoding="utf-8-sig", newline="") as handle:
    canonical = list(csv.DictReader(handle))
assert len(canonical) == 444, f"canonical count: {len(canonical)}"
assert [int(r["PRU_No"]) for r in canonical] == list(range(1, 445)), "canonical numbers are not 1..444"
names = [r["Name"] for r in canonical]
ids = [r["Species_Constant"] for r in canonical]
assert len(set(ids)) == 444, "duplicate source species constants"
assert len(set(names)) == 444, "duplicate species names"

definitions = HEADER.read_text(encoding="utf-8")
missing_constants = [c for c in ids if not re.search(r"^#define\s+" + re.escape(c) + r"\s+", definitions, re.M)]
assert not missing_constants, f"Missing engine species constants: {missing_constants}"

# Castform and Deoxys have canonical base aliases with *_NORMAL real species slots.
base_aliases = {"SPECIES_CASTFORM": "SPECIES_CASTFORM_NORMAL",
                "SPECIES_DEOXYS": "SPECIES_DEOXYS_NORMAL"}
family_paths = [
    ROOT / f"src/data/pokemon/species_info/gen_{gen}_families.h"
    for gen in range(1, 10)
]
family_paths += [
    ROOT / "src/data/pokemon/species_info/pjr_families.h",
    ROOT / "src/data/pokemon/species_info/pru_custom.h",
]
data = {p.name: p.read_text(encoding="utf-8") for p in family_paths}
missing_entries = []
locations = {}
for r in canonical:
    name, constant = r["Name"], r["Species_Constant"]
    slot = base_aliases.get(constant, constant)
    direct_pattern = r"\[\s*" + re.escape(slot) + r"\s*\]\s*="
    macro_pattern = r"\bPJR_[A-Z_]*SPECIES\s*\(\s*" + re.escape(slot) + r"\s*,"
    owners = [p.name for p in family_paths
              if re.search(direct_pattern, data[p.name]) or re.search(macro_pattern, data[p.name])]
    if len(owners) != 1:
        missing_entries.append((r["PRU_No"], name, slot, owners))
    else:
        locations[constant] = owners[0]
assert not missing_entries, f"Missing/duplicate species definitions: {missing_entries}"

info = SPECIES_INFO.read_text(encoding="utf-8")
assert '#include "species_info/pjr_families.h"' in info
assert '#include "species_info/pru_custom.h"' in info
for gen in range(1, 10):
    assert f'#include "species_info/gen_{gen}_families.h"' in info

enabled = ENABLED.read_text(encoding="utf-8")
for gen in (1, 2, 3, 4, 6):
    assert re.search(rf"^#define P_GEN_{gen}_POKEMON\s+TRUE\b", enabled, re.M), f"Gen {gen} is disabled"

header = ORDER.read_text(encoding="utf-8")
assert "#define PRU_DEX_COUNT 444" in header
listed = [(m.group(1), int(m.group(2))) for m in
          re.finditer(r"^\s*(SPECIES_[A-Z0-9_]+),\s*//\s*(\d{3})\b", header, re.M)]
assert listed == list(zip(ids, range(1, 445))), "Engine HNS summary numbering differs from the canonical list"

engine = ENGINE.read_text(encoding="utf-8")
assert '#include "data/pokemon/pru_dex_order.h"' in engine
summary = engine[engine.index("u16 SpeciesToPokedexNum(u16 species)"):].split("\n}\n", 1)[0]
assert "if (IS_HNS)" in summary
assert "sPruDexSpecies[i] == originalSpecies" in summary
assert "return i + 1;" in summary
assert "sPruDexSpecies[i] == baseSpecies" in summary

for name, expected in [("Charaxis", 8), ("Grovyle", 285),
                       ("Mightyena", 297), ("Gardevoir", 318),
                       ("Mewsion", 425), ("Deoxys", 444)]:
    assert canonical[expected - 1]["Name"] == name, name

print(f"PASS: {len(canonical)}/444 canonical species constants exist and have exactly one SpeciesInfo record")
print("PASS: active engine includes all nine generation family files and PJR/PRU extensions")
print("PASS: canonical PRU #001-#444 maps to the HNS summary number lookup without duplicates")
print("PASS: #008 Charaxis, #285 Grovyle, #297 Mightyena, #318 Gardevoir")
print("NOTE: these checks validate source registry/summary numbering, NOT gameplay or graphics.")
print("OPEN: HGSS in-game Pokédex list and save seen/caught flags still use old National/Johto mapping.")
print("OPEN: Seviian Noibat/Noivern use standard species records; approved variant art and unique mechanics are not verified.")
print("OPEN: encounter availability, especially legendaries and mythicals, requires a separate audit.")
