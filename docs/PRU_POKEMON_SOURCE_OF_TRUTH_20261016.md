# PRU — Pokémon Canon: PRL Kanto/Hoenn + PJR Johto + RR replacements

**Current authority date:** 2026-10-16. **Status:** source-of-truth reference and implementation staging, **not** completed ROM integration.

## Source order
1. PRU's current explicit user decisions override older lore/specs. PRU is standalone, Johto first, Pikachu is the only selectable opening partner, gifts are optional, and all Pokémon need independent acquisition routes.
2. **Kanto / Hoenn:** most recent approved PRL ROM/source, including updated movesets, types, stats, abilities, learnsets, TM/tutor/egg compatibility and correct **battle fronts, backs, normal/shiny palettes, party icons, sprite positioning**. Do **not** use an older PJR Noxichu or Eeveelution icon when PRL corrected it.
3. **Johto:** latest PJR true Johto Relics, custom species, Johto story and RELICS event implementation. If PRL has a newer specifically approved sprite for a Johto species, adopt that new sprite only after comparing exact pointers and pixel source.
4. **Regional overrides:** Radical Red **Seviian Noibat/Noivern** replace PRU ordinary Noibat/Noivern in their encounters/gifts. Radical Red **Paldean Wooper/Clodsire** replaces the old Paldean form/evolution battle data; regular Johto Wooper/Quagsire is separate.
5. Preserve trainer-only sprites as battle skins and normal species IDs. Explicitly retired variants (such as Hyenadon superseded by Skulberus) cannot be resurrected by old donor data.

## Canonical library outputs
All files are available under **ChatGPT Library** folder `/Pokémon Relics Ultimate/Canonical Data/`:
- `PRU_Pokemon_Canonical_Data_Pack_20261016.zip` — one Markdown + one JSON per Pokémon/form, **1,417** records and archived donor input.
- `PRU_Pokemon_Data_2026-10-16.txt` — consolidated human-readable complete source priority reference.
- `PRU_Species_Source_Registry_2026-10-16.json` — machine-readable registry.
- `PRU_Sprite_Directory_Manifest_2026-10-16.csv` — **7,085** filename/asset provenance lines.
- `PRU_Migration_And_QA_Gates.md` — blocked/unverified integration.
Notion: https://app.notion.com/p/3fb4939d431681afa46fdeb97cf8c79b

## Reproducible source audit
- PRL commit `6ee9b984521ac6f2beaf995f771a726379e55c88` is pinned for initial PRU reconciliation (PR108).
- The per-Pokémon generator is `tools/pru/generate_species_registry.py`.
- GitHub workflow `.github/workflows/pru-pokemon-source.yml` checks out pinned PRL + current PRU, derives level-up moves and actual source graphic SHA256 and exports `PRU-Pokemon-Data-Source-20261016` as an artifact.
- **These scripts do not copy the 1,417 Pokémon into the ROM**: after review, an explicit importer is required and must preserve save compatibility and species IDs.

## Specific up-to-date asset decisions
- **Noxichu:** `PRL/graphics/pokemon/noxichu/{front.png,back.png,icon.png,normal.pal,shiny.pal}` replaces older PJR/PHR art. Keep approved lowered/cropped back, correct icon palette, latest PRL `sNoxichuLevelUpLearnset`.
- **Eeveeon / Nimbeon / Toxeon:** use latest PRL `graphics/pokemon/<slug>/` if sourced, with front/back/icon normal/shiny source files and corrected party icon palettes; reject previous outdated PJR icons.
- **Skulberus:** current PRL source supersedes Hyenadon. Keep all current approved Hoenn Relics and base-pokémon rebalances.
- **RR Seviian Noibat/Noivern:** Rock/Ghost, Levitate/Rock Head/Sturdy (HA), evolves level 36; use the Radical Red level-up and verified variant sprites/icons rather than standard Flying/Dragon.
- **RR Paldean Wooper/Clodsire:** Poison/Ground, Unaware/Poison Point/Water Absorb (HA); level 20 evolution; Clodsire learns Megahorn Lv34 and Earthquake Lv44 under the RR source.
- **Legendary cosmetics, gym/E4/Rocket ace sprites:** maintain species-vs-battle-form semantics, never globalize NPC-only skins without a global user lock.

## Blocking gates
- Pinned PRL has a Noxichu **species symbol, level-up learnset, and graphics** but an actual `SPECIES_NOXICHU` species-info implementation body was not found; approved design stats/type/ability from the older canonical PRL registry are retained but runtime wiring is not validated.
- Eeveeon and Nimbeon `normal.pal` and `shiny.pal` currently hash identically; authentic distinct shiny palettes not yet source-verified.
- Radical Red regional battle sprites/party icons/shiny assets and TM/tutor/egg move compatibility are not verified/ported. Don't claim source concept is a live ROM implementation.
- Every species must have independent wild/evolution/static/legendary acquisition in Johto or Kanto, including the new regional forms; original gift events should remain available.
- Complete fresh-save gameplay, back/party icon palette and evolution tests before release; standalone Relic dialogue audit remains separate.

**Do not overwrite `pjr-rebuild`, alter PKR 2.0, or import PRL's Kanto-first/Hoenn-transfer storyline.**