# PRU full Relic integration gate — 16 October 2026

Source code donor for Kanto: `Pokemon-Relic-Legacy` commit `6ee9b984521ac6f2beaf995f771a726379e55c88` (PR108). Do not substitute the old default `main` branch. PJR map/story donor: `Pokemon-Johto-Relics` `pjr-rebuild`. Preserve the existing compiled early-starter branch PR #6.

## Verified species-data inventory

- Latest PRL `src/data/pokemon/species_info/prl_custom.h`: **50** active entries.
- Existing PJR `src/data/pokemon/species_info/pjr_families.h`: **22** active entries.
- **21** species-data entries overlap. **29** PRL definitions are not in active PJR data, despite some IDs already being reserved and some sprites sitting in dormant folders.
- PJR also has `RELIC_HO_OH` as a distinct non-overlap. Do not overwrite it.
- PJR's `include/constants/species.h` has reserved numeric IDs for **13** of the 29 missing active PRL species; **16** are not yet reserved.
- **Every one of the 29** has a five-asset donor art pack in PRL: front, back, party icon, normal palette, shiny palette. PJR's selected versions of overlapping graphics must be preserved.

### Twenty-nine PRL entries to reconcile

`EDENSAUR`, `CHARAXIS`, `FORTOTOISE`, `KHANG`, `NOLAX`, `NUMEW`, `GEMLIN`, `VALKYVOIR`, `SCEPTITAN`, `SOLAZIKEN`, `SWAMPLITH`, `SKULBERUS`, `GEMIGOYLE`, `MAWYRM`, `TORKALDERA`, `CACTOMB`, `TROPISAUR`, `COELOSSUS`, `ASTRACHI`, `MILTITAN`, `SHUCKOLOSSE`, `DONPHALANX`, `FAERANIUM`, `PYROCLAST`, `FERALODON`, `DRAKEON`, `GHOULBAT`, `EEVEEON`, `NIMBEON`.

### Sixteen without reserved PJR IDs
`NUMEW`, `GEMLIN`, `VALKYVOIR`, `SCEPTITAN`, `SOLAZIKEN`, `SWAMPLITH`, `SKULBERUS`, `GEMIGOYLE`, `MAWYRM`, `TORKALDERA`, `CACTOMB`, `TROPISAUR`, `COELOSSUS`, `ASTRACHI`, `EEVEEON`, `NIMBEON`.

**Important:** PJR has assigned custom IDs 1573–1623, including trainer-only visual forms. Do not reorder those existing IDs, rename them, or reuse their numeric values. Add new species at the tail, before `SPECIES_EGG`, then audit save compatibility. No blanket text import.

## Additional source blockers — verified

Comparison of `include/constants/abilities.h` shows at least 18 PRL symbols absent from PJR:

`ABILITY_PIERCING_DRILL`, `ABILITY_DRAGONIZE`, `ABILITY_EELEVATE`, `ABILITY_314`, `ABILITY_MEGA_SOL`, `ABILITY_FIRE_MANE`, `ABILITY_317`, `ABILITY_SPICY_SPRAY`, `ABILITY_AURA_GUARD`, `ABILITY_ANCIENT_GROVE`, `ABILITY_SOLAR_DISCIPLINE`, `ABILITY_TIDAL_BASTION`, `ABILITY_ANCIENT_CORE`, `ABILITY_WISHMAKER`, `ABILITY_EDENS_CANOPY`, `ABILITY_THERMAL_WINGS`, `ABILITY_CITADEL_SHELL`, `ABILITY_STYGIAN_RUSH`.

Comparison of `include/constants/moves.h` shows at least 22 absent PRL move names or supporting aliases:
`MOVE_AMBER_BLADE`, `MOVE_SUN_RITE`, `MOVE_TECTONIC_TIDE`, `MOVE_EPOCH_CRASH`, `MOVE_RELIC_WISH`, `MOVE_EDEN_BLOOM`, `MOVE_SCORCHWING`, `MOVE_BASTION_CANNON`, `MOVE_LOVELY_BITE`, `MOVE_SHADOW_FANGS`, `MOVE_RIP_AND_TEAR`, `MOVE_EERIE_FOG`, `MOVE_SEISMIC_SLAM`, `MOVE_SOIL_DRAIN`, `MOVE_BRAVADO`, `MOVE_RAGING_SOULS`, `MOVE_IRON_FANGS`, `MOVE_BEATDOWN`, `MOVE_TAKE_FLIGHT`, `MOVE_INSECT_IMPACT`, `MOVE_EEVOBOOST`, `MOVE_RANDOM_TEACHABLE`. Not all are battle moves: distinguish aliases/sentinels from actual moves.

These are **symbol differences, not proof that 18 abilities/22 battle moves must be directly copied**. Audit which species, learnsets, trainer rules and scripts reference them, then port needed effects and data with stable IDs and no mechanics regressions.

## All-at-once actual playtest acceptance

1. Import 29 missing species data without replacing PJR's existing 22 entries or established stat/evolution choices.
2. Stage donor art with `tools/pru/import_prl_artwork.py`; register all front/back/palette/icon symbols. Resolve conflicting Kanto assets in favour of latest approved PRL while leaving PJR's Johto assets untouched.
3. Port needed learnsets, abilities, Relic move mechanics and evolution conditions. Include all pre-evolutions and any required evolutionary items; ensure a player can actually obtain each species.
4. Generate full original #001–#386 + distinct canonical Relics acquisition report. Check wild location, level, time, evolution, event and flags for every target, **including the original Elm Togepi Egg exception**. No inaccessible or gift-only species.
5. Keep all twelve early starters at original agreed pre-evolution levels; later habitats may use their evolved versions.
6. Verify Kanto donor visuals/content and Kanto/Johto storyline, rematches and PJR first League unchanged. Do not introduce Hoenn travel into PJR Ultimate.
7. Compile in fresh GitHub CI; test game on a clean save with emulator, including saving/loading, starter/rival, all additions, Pokédex, battles, evolution and Hall of Fame.
8. Release **one consolidated complete test ROM**, not repeated tiny builds. Do not falsely mark incomplete CI/source test as emulator approval.

This is an engineering checklist, not an assertion that full integration is already finished.
