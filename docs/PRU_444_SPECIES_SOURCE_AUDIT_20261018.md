# PRU — Full 444-Species Source Audit and Pokédex Numbering Correction

Date: 18 October 2026
Branch: `pru/444-species-dex-audit-20261018`
Base: `pru/move-expert-stones-tm-labels-20261017` (includes Rocket, Move Expert, Ancient Stone, TM label work)
Authoritative 444-species order: user Library `/Pokémon Relics Ultimate/Canonical Data/PRU_National_Pokedex_2026-10-16.csv`, copied without roster changes to `data/pru/PRU_National_Pokedex_2026-10-16.csv`.

## Findings — distinguish source existence from playable completion

- **444/444 canonical rows:** contiguous #001–#444, 444 distinct `SPECIES_*` constants, no duplicate canonical species IDs. Every constant is defined by the current engine's `include/constants/species.h`.
- **444/444 source species:** one SpeciesInfo record for each after resolving `SPECIES_CASTFORM` -> `SPECIES_CASTFORM_NORMAL` and `SPECIES_DEOXYS` -> `SPECIES_DEOXYS_NORMAL`. Records span the enabled generation family files, `pjr_families.h`, and `pru_custom.h`. These are *source registrations*, not a claim that every one is encounterable or visually finished.
- **Not a missing species:** Grovyle (`SPECIES_GROVYLE`, PRU #285), Mightyena (`SPECIES_MIGHTYENA`, #297), Gardevoir (`SPECIES_GARDEVOIR`, #318) all have stock valid species entries. `SPECIES_CHARAXIS = 1603` is already defined with donor base stats, typing, ability and graphics pointers; #008 in the canonical list, its newly added level-45 Ancient Stone evolution is in the stacked base branch.
- **Real numbering defect:** `SpeciesToPokedexNum()`, used by `src/pokemon_summary_screen.c`, used inherited *Johto* numbering before the National Dex was unlocked. Non-Johto Pokémon then returned zero and appeared as unknown. Even after the old National Dex unlock, genuine custom Relic evolutions reused the base `.natDexNum`, so a distinct PRU number was not displayed.
- **Fix now in source:** `src/data/pokemon/pru_dex_order.h` pins the approved order; `SpeciesToPokedexNum()` now uses this 444-entry mapping *only for the HNS game*. Non-PRU builds preserve their original paths. Unlisted battle-only variants inherit their base species' PRU number, preserving the 444 cap. This affects summary screen numbering; it does not alter save flags or Pokémon species IDs.

## Important unresolved issues (must not be mistaken for complete implementations)

1. **HGSS in-game Pokédex UI:** `src/pokedex_plus_hgss.c` still builds its lists using original National/Johto/Obtainable Dex IDs, and `GetSetPokedexFlag()` still stores seen/caught by inherited National Dex number. Since real custom Relic species share the National Dex ID of their ancestors, they are **not yet 444 independent tracked Pokédex entries**. A further carefully designed 444-slot Pokédex UI and save-compatibility implementation is needed. Do not simply renumber `NATIONAL_DEX_*` or change save-flag packing in an existing save.
2. **Seviian Noibat / Noivern (#418/#419):** their canonical rows currently refer to ordinary `SPECIES_NOIBAT` and `SPECIES_NOIVERN`, with corresponding base SpeciesInfo records. The sprite-source policy expressly marks exact approved Seviian artwork as unverified. Do not claim these are complete or manufacture unapproved sprite replacements.
3. **Legendary encounters:** all listed legendary/mythical *species have source records*, but unique encounter events and accessibility need an independent event/progression audit. Their locations are deliberately not invented here.
4. **Other completeness:** existence and numbers do not prove donor moveset, evolution access, shiny/front/back/party/overworld graphics, trainer teams, catchability or in-emulator behaviour. Charaxis's dedicated PKR level-up moves remain unported in the present PJR SpeciesInfo record.
5. **Build and gameplay QA:** GitHub Actions workflow now runs `python3 tools/pru/check_444_species_dex.py` and the consolidated `make hns` build. Only a successful action and in-emulator checks can certify a playable ROM. Check prior Rocket and title-screen assets remain present, and test a fresh save and an existing save.

## Regression-test gates

`python3 tools/pru/check_444_species_dex.py` validates canonical uniqueness and numbering, species constants, one SpeciesInfo record per approved species (including aliases and PJR macros), generation imports/config, PRU summary numbering and the four reported species. Existing `tools/pru/check_relic_stone_services.py` protects Charizard -> Charaxis and 24 other level-45 Ancient Stone routes.

**Credit provenance:** preserves all existing `CREDITS.md`, pinned PRL and PKR donor source records, approved Mercury-derived Charaxis art and user sprite-source policy. No artwork was replaced.
