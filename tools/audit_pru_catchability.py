#!/usr/bin/env python3
"""Report actual PRU/HNS wild slots independently of optional NPC gifts.

Static encounters, fossil revivals, eggs, trades and evolutions require a separate
review. Never interpret 'not in wild table' as 'unobtainable'.
"""
import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

# NPC awards are additional routes, not the only way to obtain a species.
# Extra lines are deliberately included to check other known story/gift cases.
GIFT_OR_STORY = {
    "PIKACHU": "Elm opening starter (only selectable initial partner)",
    "CHIKORITA": "Violet City aide gift",
    "CYNDAQUIL": "Azalea Town aide gift",
    "TOTODILE": "Goldenrod City aide gift",
    "TREECKO": "Steven Silph Co. choice",
    "TORCHIC": "Steven Silph Co. choice",
    "MUDKIP": "Steven Silph Co. choice",
    "TENTACOOL": "Cianwood Pokémon Center Fisher",
    "DRATINI": "Dragon's Den Elder",
    "TYROGUE": "Mt. Mortar Karate King",
    "WOOPER_PALDEA": "Sinjoh Elizabeth gift",
    "NOIBAT": "Alola Phant Egg",
    "TOGEPI": "Elm's original Togepi Egg (preserve)",
    "SCARABUB": "Johto Relic baby (former Elm post-League Egg)",
    "SKARMET": "Johto Relic baby (former Elm post-League Egg)",
    "MOOTINY": "Johto Relic baby (former Elm post-League Egg)",
    "PORYGON": "Goldenrod Game Corner prize / wild",
    "CASTFORM": "PJR catchability check",
    "BELDUM": "Donor optional/debug gift check",
    "LILEEP": "Fossil revival",
    "ANORITH": "Fossil revival",
    "OMANYTE": "Fossil revival",
    "KABUTO": "Fossil revival",
    "AERODACTYL": "Fossil revival",
}
FIELDS = ("species", "map", "variant", "encounter_type", "min_level", "max_level", "slot", "encounter_rate")


def rows_from_wild(data):
    for group in data["wild_encounter_groups"]:
        if not group.get("for_maps"):
            continue
        for entry in group.get("encounters", []):
            mapname = entry.get("map", "")
            variant = entry.get("base_label", "")
            # Official header generator keys HNS entries by their HNS label.
            if not (mapname.upper().endswith("_HNS")
                    and ("_hns" in variant.lower() or "_HNS" in variant)):
                continue
            for kind, table in entry.items():
                if not isinstance(table, dict) or not isinstance(table.get("mons"), list):
                    continue
                for n, mon in enumerate(table["mons"]):
                    species = mon["species"]
                    if not isinstance(species, str):
                        continue
                    yield {
                        "species": species.removeprefix("SPECIES_"),
                        "map": mapname,
                        "variant": variant,
                        "encounter_type": kind,
                        "min_level": mon.get("min_level", "?"),
                        "max_level": mon.get("max_level", "?"),
                        "slot": n + 1,
                        "encounter_rate": table.get("encounter_rate", "?"),
                    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument("--out", type=Path, default=Path("artifacts/pru-catchability"))
    args = p.parse_args()
    root, out = args.root.resolve(), args.out
    out.mkdir(parents=True, exist_ok=True)
    raw = json.loads((root / "src/data/wild_encounters.json").read_text())
    rows = list(rows_from_wild(raw))
    if not rows:
        raise SystemExit("No HNS wild slots detected: verify JSON schema / label selection")
    wild = defaultdict(list)
    for row in rows:
        wild[row["species"]].append(row)

    with (out / "PRU_HNS_WILD_SLOTS.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

    findings = []
    for species, description in sorted(GIFT_OR_STORY.items()):
        slots = wild.get(species, [])
        maps = sorted({r["map"] for r in slots})
        ways = sorted({r["encounter_type"] for r in slots})
        findings.append({
            "species": species,
            "npc_or_story": description,
            "independent_wild_slot": bool(slots),
            "map_count": len(maps),
            "maps": "; ".join(maps),
            "encounter_types": "; ".join(ways),
            "wild_slot_count": len(slots),
            "next_action": "Validate time, accessibility and actual catch in emulator"
                           if slots else
                           "Review separate evolution/static encounter; add wild access if no independent capture exists",
        })

    with (out / "PRU_GIFT_INDEPENDENCE.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(findings[0]))
        w.writeheader()
        w.writerows(findings)

    missing = [r for r in findings if not r["independent_wild_slot"]]
    summary = [
        "# PRU — gift-independent catchability source inventory",
        "",
        "**Source evidence, not emulator validation.** Registered HNS wild slots only.",
        "Gift, fossil, static, trade and evolution paths are intentionally NOT",
        "considered proof of an independent catchable route.",
        "",
        f"- Unique HNS wild species: **{len(wild)}**",
        f"- HNS wild encounter slots scanned: **{len(rows)}**",
        f"- Gift/story species with wild slots: **{len(findings) - len(missing)}/{len(findings)}**",
        f"- Needing separate encounter/evolution review: **{len(missing)}**",
        "",
        "| Species | Wild slot? | Maps |",
        "| --- | --- | --- |",
    ]
    for row in findings:
        loc = row["maps"] or "Not in HNS wild slots"
        summary.append(f"| {row['species']} | {'Yes' if row['independent_wild_slot'] else 'No'} | {loc} |")

    summary += [
        "",
        "## Important limitations",
        "",
        "- A listed wild species can still be inaccessible because of story/map gates, encounter variation, version, or mode.",
        "- An absent wild slot does NOT prove unobtainability: static battles and ordinary evolution may supply it.",
        "- A Pokémon Egg or NPC gift is allowed but does not replace independently catchable acquisition.",
        "- Regional forms and late-generation Relics must be audited by exact form ID, not only family name.",
        "- Test non-Surf early starters separately against actual day/night slots.",
        "- Legendary scripts, all evolution dependencies and full National Dex acquisition graph remain separate gates.",
        "",
    ]
    (out / "PRU_GIFT_INDEPENDENCE.md").write_text("\n".join(summary), encoding="utf-8")
    (out / "PRU_GIFT_INDEPENDENCE.json").write_text(
        json.dumps({"unique_hns_wild_species": len(wild), "slot_count": len(rows),
                    "species": findings}, indent=2) + "\n", encoding="utf-8")
    print(f"PASS: scanned {len(rows)} HNS wild slots ({len(wild)} unique species);"
          f" gift/story species with independent wild slots: {len(findings) - len(missing)}"
          f"/{len(findings)}; review: {len(missing)}")
    for row in missing:
        print(f"REVIEW {row['species']}: no HNS wild slot; check static/evolution")


if __name__ == "__main__":
    main()
