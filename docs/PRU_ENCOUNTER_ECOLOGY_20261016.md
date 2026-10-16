# PRU catchability and wild-encounter ecology — source implementation (16 October 2026)

**Status:** Source encounter-table changes committed on isolated branch `pru/encounter-ecology-20261016`; automated static regression workflow added. NOT a playable or emulator-tested ROM. Requires integration with the 19-species PRL/AlteRed/Kanto Ultimate branch, particularly `SPECIES_GEMLIN`.

## Goals and ordering (user-approved)

- Pokémon Relics Ultimate remains the standalone **Johto + Kanto** game. Use PKR/PRL Kanto, PHR Hoenn and PJR Johto habitats and source data as ecological references, **not** a wholesale transplant of Hoenn maps or level ranges.
- Ordinary first-route species (Pidgey, Rattata, Sentret, Hoothoot, etc.) should remain common. Do not put pseudo-legendaries such as Dratini/Larvitar/Bagon on beginner routes.
- The **nine original traditional starter lines** plus **Scarabub, Skarmet, Mootiny**, and now **Gemlin**, should have **low-level first-stage encounters early**. Their evolved original forms (Heracross, Skarmory, Miltank, Sableye) may occur in appropriately levelled wild areas.
- **Do not** place direct Relic evolutions (Skarmadon, Miltitan, Heracurion, Donphalanx, Valkyvoir, etc.) into random wild grass. The player obtains them through their approved species-specific **Ancient Stone / Ancient Emblem / Relic evolution** mechanic, or other previously established method. Do not change the evolution items or their timing merely to match wild-table convenience.
- Legends/Mythicals/unique guardians are **fully deferred**. Preserve every existing quest, level and map event; do not invent ticket grants, legendary wild rates, or generic catch locations.
- NPC gifts, Elm's original Togepi Egg, starters, breeding, fossils, trades and prizes remain valid *additional* acquisition routes. Keep a non-gift wild/evolution/static acquisition chain when required by the National Dex policy.
- Keep approved original Wooper **and** Quagsire while preserving Paldean Wooper/Clodsire as distinct, obtainable exceptions.

## Implemented wild-data corrections

Exact fields in `src/data/wild_encounters.json`, only `_HNS` Johto/Kanto variants modified:

| Area | Source change | Encounter range / rarity |
| --- | --- | --- |
| Existing 257 HNS day/night variants | Restore all 34 ordinary Wooper and all 119 Quagsire original PJR slots before selecting a few Paldean exceptions | Final original wild counts: **32 Wooper**, **116 Quagsire** slots |
| Route 32, day and night | Preserve common original Wooper and add Paldean Wooper as a **distinct** rare entry | Lv6–7, 1% land slot in each variant |
| Ruins of Alph outside, day and night | Keep original Wooper in suitable slots, add rare Paldean Wooper | Lv5–6, 1% land slot in each variant |
| Ruins of Alph water, both variants; Union Cave B2F water | Retain ordinary Quagsire in other water slots, allow rare Clodsire | Lv20–24, 1% water slot in each variant |
| Dark Cave south side (early Violet entrance) | Remove both inappropriate beginner **Larvitar Lv2–4** slots; add **Gemlin** and low-level Dunsparce | Gemlin Lv4–5, 4% land slot |
| Burned Tower B1F, night | Add a separate **wild Sableye**, retaining Magmar in remaining slots | Lv19–21, 1% land slot |
| Ruins of Alph outside, night | Add low-level **Cleffa**; retain existing Clefairy, Wooper and Unown elsewhere | Lv5–6, 1% land slot |
| Routes 26 and 27 (League approach) | Replace incongruous Lv5 starter first stages with appropriate fully evolved starters | Venusaur/Charizard/Blastoise/Meganium/Typhlosion/Feraligatr Lv38–41 |
| Mt. Silver late-game rooms | Retain late-game Larvitar/Pupitar availability while removing level outliers far below their Lv60+ neighbours | Larvitar Lv50–53; Pupitar Lv57–60 |

### Species counts and preservation

- Main source pre-change: **257** HNS encounter variants on **165** unique map names.
- The 34 Wooper and 119 Quagsire PJR wild entries had been replaced 1:1 with Paldean Wooper / Clodsire on the earlier PRU branch. The selective correction preserves the original habitats instead of removing the Paldean line.
- Final HNS source counts after edits: **Wooper 32, Quagsire 116, Paldean Wooper 4, Clodsire 3**, plus **Gemlin 1, Cleffa 1, Scarabub 2, Skarmet 2, Mootiny 2**; Sableye rises from 3 to 4 slots; Larvitar remains in **5** late-game slots.
- All 12 previously approved traditional/PJR starter-stage catch locations remain in early Johto at Lv2–9, including day/night where defined; their original low-level locations were not displaced. A new Gemlin early location is staged.
- Normal Kanto Pidgey/Rattata early-species habitats and late-game progression are intact; **no legendary encounter script or overworld event was edited**.
- Existing optional gifts, eggs, event flags, trainers and all non-`_HNS` wild tables were untouched.

## Regression checks

`tools/pru/check_encounter_ecology.py` and `.github/workflows/pru-encounter-ecology.yml` protect:
- The count and levels of Johto/Kanto encounter variants.
- Starter/pre-evolution early availability.
- No pseudo-legendary in Route 29–33, Route 46, early Dark Cave.
- No **direct wild Relic evolutions** and no **wild legendary special encounters**.
- Standard and Paldean Wooper/Quagsire/Clodsire **all independently obtainable** in planned wild encounters, without blanket replacement.
- Appropriate League approach Route 26/27 and Mt. Silver Larvitar/Pupitar levels.

Use `python3 tools/pru/check_encounter_ecology.py` to test source-only constraints.

**Important:** `python3 tools/pru/check_encounter_ecology.py --require-engine` additionally verifies the Gemlin species ID exists. This is an **expected failure** until Work's separately-developed species integration has been merged. Do not claim this branch alone compiles as a ROM.

## Remaining nonlegendary catchability gates (no user decisions needed)

1. Merge the complete 19-species import including Gemlin, and make sure all 444 National Pokédex entries can be obtained through wild catch, breeding, known evolutionary routes, static events, or independently available items; do **not** make evolved Relic species wild.
2. Verify donor evolutions and availability of the Ancient Stone, Ancient Emblem, Shiny Stone, other approved evolution items, and special moves/conditions; item timing belongs to species progression rather than wild ecology.
3. Preserve and test static **Snorlax (Vermilion)** and **Sudowoodo (Route 36)**. Both have encounter scripts, not random wild tables; confirm recovery behaviour if fainted/escaped.
4. Verify Eevee → Umbreon happiness/time, Cleffa from wild and/or breeding, and standard/Paldean Wooper evolution outcomes. Normal Quagsire should never be replaced by Clodsire.
5. Validate every encounter in a real game: reachability, grass/day/night/surf/fishing method, special map warps, levels, evolution and caught-Dex flags.
6. Audit optional gifts, fossils, trades and prize Pokémon separately; keep them as bonus routes while preserving independent access.
7. **Legendary/unique Pokémon excluded by user decision.** Separate story-led location audit needed, including Mew, Mewtwo, Mewsion, Hoenn legends, Johto RELICS and Deoxys. No change in this branch.

## Merge handoff to the interrupted Work integration

- This is deliberately a separate branch to avoid interfering with unpushed Work changes on the local `pru/complete-selective-integration-20261016` branch.
- Cherry-pick the source commits or merge the entire encounter branch **only after** current Work's source is committed and pushed.
- Keep the wild-file changes, regression gate and source comparison alongside the complete species/moves/abilities/Bleeding/Fear/Eerie Fog import; update the [PRU resume checkpoint](https://github.com/jamesthoward2112-tech/Pokemon-Johto-Relics/blob/pru/consolidated-prl-battle-import-20261016/docs/PRU_WORK_RESUME_CHECKPOINT.md) with final merged SHA.
- This document describes **source changes** and static checks, not completed compilation or emulator gameplay.

## Provenance / boundaries

- Johto and Kanto level bands from the PJR `pjr-rebuild` and PRU `pru/ultimate-pokedex-encounters-20261016` wild-source tables.
- Kanto species and mechanics should be reconciled to approved PRL/PR108 donor; PHR Hoenn ecological roles guide placement within accessible PRU maps. Actual original PHR route tables are not present as a complete independently fetchable wild-source file in the PHR repository: do not pretend a direct one-to-one port exists.
- National Dex: PRU canonical 444-species spreadsheet/CSV and Notion source-of-truth dated 2026-10-16.
