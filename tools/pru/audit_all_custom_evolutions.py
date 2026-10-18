#!/usr/bin/env python3
"""Source audit of ALL canonical PRU custom evolution targets, not just Ancient Stones.

Emits a detailed Markdown artifact from the exact current checkout. No external donors
are fetched: the canonical 444-species roster and current engine tables are authoritative.
This is source verification, NOT proof of in-game item use or a 444-slot Pokédex.
"""
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "src/data/pokemon/species_info"
CSV = ROOT / "data/pru/PRU_National_Pokedex_2026-10-16.csv"
FAMILIES = [DATA / f"gen_{i}_families.h" for i in range(1, 10)]
FAMILIES += [DATA / "pjr_families.h", DATA / "pru_custom.h"]
REPORT = ROOT / "PRU-All-Custom-Evolutions-Audit.md"

# These are the *start* of a family, not a missing evolution. Keep five
# catchable/obtainable roots independent. Noibat is Seviian in the PRU canon.
ROOT_CUSTOM = {"GEMLIN", "SCARABUB", "SKARMET", "MOOTINY", "NOIBAT"}
INDEPENDENT_SPECIAL = {"COELOSSUS", "MEWSION", "ASTRACHI", "ALPHORACLE"}
REMOVED_FROM_CANON = {"SUDOWARDEN"}
ANCIENT_LEVEL = 45

with CSV.open(newline="", encoding="utf-8-sig") as f:
    roster = list(csv.DictReader(f))
assert len(roster) == 444
assert [int(row["PRU_No"]) for row in roster] == list(range(1, 445))
canonical = {row["Species_Constant"].removeprefix("SPECIES_"): row for row in roster}
custom = {name: row for name, row in canonical.items()
          if row["Category"].startswith("PRU custom")}
assert len(custom) == 54, len(custom)

species_constants = (ROOT / "include/constants/species.h").read_text(encoding="utf-8")
items_constants = (ROOT / "include/constants/items.h").read_text(encoding="utf-8")
edges = []
records = set()
def_by_file = defaultdict(list)
pattern = re.compile(r"\[SPECIES_([A-Z0-9_]+)\]\s*=")
evo_pattern = re.compile(r"\{\s*(EVO_[A-Z0-9_]+)\s*,\s*([^,{}]+)\s*,\s*SPECIES_([A-Z0-9_]+)")
for path in FAMILIES:
    source = path.read_text(encoding="utf-8")
    hits = list(pattern.finditer(source))
    for ix, hit in enumerate(hits):
        base = hit.group(1)
        stop = hits[ix + 1].start() if ix + 1 < len(hits) else len(source)
        record = source[hit.end():stop]
        records.add(base)
        def_by_file[base].append(path.name)
        pos = record.find(".evolutions")
        if pos < 0:
            continue
        # The source block's EVOLUTION() may contain conditional branches;
        # list all potential branches but flag compile-time uncertainty in notes.
        evo = record[pos:pos + 5000]
        for match in evo_pattern.finditer(evo):
            method, param, target = match.groups()
            surrounding = evo[match.start():match.start() + 190]
            surrounding = " ".join(surrounding.split()).split("},")[0]
            edges.append(dict(base=base, method=method, param=param.strip(),
                              target=target, detail=surrounding, file=path.name))

# Macro-based PJR species definitions do not have an [SPECIES_] block.
pjr = (DATA / "pjr_families.h").read_text(encoding="utf-8")
for m in re.finditer(r"PJR_(?:RED|FINAL)_SPECIES\(SPECIES_([A-Z0-9_]+),", pjr):
    records.add(m.group(1))

incoming = defaultdict(list)
outgoing = defaultdict(list)
for edge in edges:
    incoming[edge["target"]].append(edge)
    outgoing[edge["base"]].append(edge)

errors = []
def require(ok, reason):
    if not ok:
        errors.append(reason)

require(len(records & set(canonical)) == 444,
        f"Canonical entries with species definitions: {len(records & set(canonical))}/444")
require(len(set(canonical)) == 444, "Duplicate canonical species constants")
for name, row in canonical.items():
    require(f"#define SPECIES_{name}" in species_constants or
            f"#define SPECIES_{name} " in species_constants,
            f"{name}: missing species constant")
for name in custom:
    if name in ROOT_CUSTOM:
        require(not incoming[name], f"{name}: intentional base family unexpectedly evolved into")
    else:
        require(bool(incoming[name]), f"{name}: custom target is unreachable by any species evolution")

stone = [x for x in edges if x["method"] == "EVO_ITEM"
         and x["param"] == "ITEM_ANCIENT_STONE"
         and "IF_MIN_LEVEL, 45" in x["detail"]]
stone_custom = [x for x in stone if x["target"] in custom]
require(len(stone_custom) == 27, f"Expected 27 canonical Lv45 Ancient Stone routes; found {len(stone_custom)}")
for x in stone_custom:
    require(x["base"] in canonical, f"{x['base']} Ancient Stone source not in 444")
for source, target, item in [
    ("PIKACHU", "NOXICHU", "ITEM_MOON_STONE"),
    ("PIKACHU", "RAICHU", "ITEM_THUNDER_STONE"),
    ("WEEZING", "FRYTNING", "ITEM_THUNDER_STONE"),
    ("EEVEE", "EEVEEON", "ITEM_ANCIENT_STONE"),
]:
    require(any(x["base"] == source and x["target"] == target
                and x["method"] == "EVO_ITEM" and x["param"] == item for x in edges),
            f"Missing {source} to {target} using {item}")
for x in edges:
    if x["base"] in canonical and x["target"] in custom and x["method"] == "EVO_ITEM":
        require(f"#define {x['param']}" in items_constants or
                re.search(r"^#define\s+" + re.escape(x["param"]) + r"\s", items_constants, re.M),
                f"{x['base']} to {x['target']}: item constant {x['param']} missing")

for name in INDEPENDENT_SPECIAL | REMOVED_FROM_CANON:
    require(not incoming[name], f"{name}: forbidden ordinary evolution route present")

require(any(x["base"] == "NOIBAT" and x["target"] == "NOIVERN"
            and x["param"] == "36" for x in edges),
        "Noibat -> Noivern must have a level-36 HNS route")
require(any(x["base"] == "SCARABUB" and x["target"] == "HERACROSS"
            for x in edges), "Scarabub family chain missing")
require(any(x["base"] == "SKARMET" and x["target"] == "SKARMORY"
            for x in edges), "Skarmet family chain missing")
require(any(x["base"] == "MOOTINY" and x["target"] == "MILTANK"
            for x in edges), "Mootiny family chain missing")
require(any(x["base"] == "GEMLIN" and x["target"] == "SABLEYE"
            for x in edges), "Gemlin family chain missing")
for target in ["EDENSAUR", "FORTOTOISE", "KHANG", "NOLAX", "CHARAXIS"]:
    require(any(x["target"] == target and x in stone_custom for x in edges),
            f"Missing approved Lv45 Ancient Stone evolution to {target}")

def fmt(edge):
    text = f'{edge["base"].title()} → {edge["target"].title()} — {edge["method"]}, {edge["param"]}'
    if "IF_MIN_LEVEL, 45" in edge["detail"]:
        text += ", min Lv45"
    if "CONDITIONS" in edge["detail"] and "IF_MIN_LEVEL" not in edge["detail"]:
        text += " (conditional)"
    return text

summary = [
    "# PRU — Full canonical custom evolution audit",
    "",
    "Generated directly from the 444 approved species CSV and 11 live species-family source tables.",
    f"**{len(roster)} canonical entries | {len(custom)} canonical custom entries | "
    f"{len(edges)} source evolution branches | {len(stone_custom)} canonical Ancient Stone Lv45 routes**",
    "",
    "Compiled-source checks do **not** prove an item triggers an evolution in an emulator, "
    "that a scene is reachable, or that graphics/learnsets are donor-accurate.",
    "",
    "## Every approved custom species (#001–#419)",
    "",
    "| PRU # | Species | How it is obtained by evolution | Audit |",
    "|---:|---|---|---|",
]
for name, row in custom.items():
    ins = incoming[name]
    status = ("Initial family member" if name in ROOT_CUSTOM
              else ("Source-linked" if ins else "MISSING EVOLUTION"))
    descriptions = "; ".join(fmt(x) for x in ins) if ins else "No incoming evolution (intentional)" if name in ROOT_CUSTOM else "NO ROUTE"
    summary.append(f'| {row["PRU_No"]} | {row["Name"]} | {descriptions} | {status} |')

summary += [
    "",
    "## Approved split families and independent encounters",
    "",
    "- **Pikachu:** Thunder Stone → Raichu; Moon Stone → Noxichu. No Lv45 gate on Noxichu.",
    "- **Kanto Relic forms:** Venusaur → Edensaur, Charizard → Charaxis, "
      "Blastoise → Fortotoise, Kangaskhan → Khang, Snorlax → Nolax at Lv45+ using Ancient Stone.",
    "- **Weezing:** Ancient Stone at Lv45+ → Cheauking; Thunder Stone → Frytning.",
    "- **Eevee:** Ancient Stone → Eeveeon is an Eeveelution exception. "
      "Other custom Eeveelutions keep their established level/time/held-item/stone methods.",
    "- **Baby/new roots:** Gemlin, Scarabub, Skarmet, Mootiny, Seviian Noibat start families; "
      "do not invent an incoming evolution.",
    "- **Coelossus:** must remain an independently encounterable Sealed Chamber guardian. "
      "Relicanth is not its pre-evolution.",
    "- **Sudowarden:** remains an internal registered species but is excluded from the canonical "
      "444. Sudowoodo must not evolve into it.",
    "- **Mewsion/Astrachi/Alphoracle:** special encounters, not ordinary evolution targets.",
    "- **Seviian Noibat → Noivern:** PRU uses Lv36, but exact Rock/Ghost forms/art are NOT yet "
      "verified in the compiled game.",
    "",
    "## Evolution definitions into targets outside the canonical 444",
    "",
    "The following source definitions are present in the same codebase. "
    "Some belong to disabled game-generation families or conditional form paths; "
    "they must not be treated as proof of extra playable PRU entries.",
    "",
]
extraneous = [e for e in edges if e["base"] in canonical and e["target"] not in canonical]
summary += [f"- {fmt(x)} (source: {x['file']})" for x in extraneous[:200]]
if len(extraneous) > 200:
    summary.append(f"- …plus {len(extraneous)-200} additional source-level paths")
summary += [
    "",
    "## QA still required in a playable ROM",
    "",
    "1. **Moon Stone on Pikachu:** verify target selection, Noxichu graphics, stone consumption, "
    "and that Thunder Stone still evolves to Raichu.",
    "2. **Ancient Stone:** test a Pokémon at Lv44 and Lv45, especially new Kanto forms "
    "and both Weezing routes, with correct stone deductions.",
    "3. **Custom non-stone:** test Marowak daytime/night held-item splits, each Eeveelution, "
    "Ghoulbat, Grimfowl, Sunflorid, Pinsirex and Annihilape's move-use condition.",
    "4. **Family roots:** verify four custom baby Pokémon appear where intended and can "
    "evolve to their middle stage, and Seviian Noibat/Noivern is actually custom art/type.",
    "5. **Donor parity and UI:** independent Pokédex seen/caught flag tracking for 444 species "
    "remains unfinished; artwork, special movesets, signature effects and event accessibility "
    "require separate QA.",
    "",
    "## Source audit status",
    "",
]
summary += ["- FAIL: " + e for e in errors] if errors else ["- PASS: All 54 canonical custom species have a source route or are approved family roots."]
summary += ["", f"**Result: {'FAIL' if errors else 'PASS'} — {len(errors)} blocking discrepancies.**", ""]
REPORT.write_text("\n".join(summary), encoding="utf-8")
print("\n".join(summary[:7]))
print(f"FULL_EVOLUTION_AUDIT: {'FAIL' if errors else 'PASS'}, blockers={len(errors)}, "
      f"canonical_ancient_stone={len(stone_custom)}, additional_out_of_roster_source_edges={len(extraneous)}")
for e in errors:
    print("AUDIT_ERROR:", e)
if errors:
    sys.exit(1)
