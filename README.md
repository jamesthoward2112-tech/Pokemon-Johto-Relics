# Pokémon Johto Relics (PJR)

Pokémon Johto Relics is the Johto entry in the Relic Series, built on the Pokémon Heart & Soul / pokeemerald-expansion codebase.

## Development status

**Current stage:** Alpha 1 development  
**Active PJR branch:** `master`  
**CI ROM artifact:** `Pokemon-Johto-Relics-Alpha1.gba`

The Alpha 1 CI pipeline builds the ROM and then runs an automated mGBA opening smoke test through the trainer-name handoff. A successful workflow therefore checks both compilation and the opening transition that previously caused the game to stall.

## Building

The CI build uses:

```sh
make hns -j4 -O
```

The raw build output is `pokehns.gba`. CI packages it as `Pokemon-Johto-Relics-Alpha1.gba`.

Generated ROMs, logs, emulator captures, object files and local build output are intentionally excluded from source control.

## PJR-specific source

PJR-specific additions live alongside the inherited Heart & Soul source. Current examples include:

- `graphics/title_screen/pjr/`
- `src/data/pokemon/species_info/pjr_families.h`
- `src/data/pokemon/level_up_learnsets/pjr.h`
- Johto Relics intro, starter and opening-flow changes in the relevant map/script/source files

The repository also retains upstream Heart & Soul documentation and source assets where they remain useful for implementation, compatibility and attribution.

## CI and artifacts

The active build workflow is:

- `.github/workflows/build.yml` — builds Alpha 1, uploads the ROM artifact and runs the opening smoke test.

Temporary bootstrap/repair workflows used while establishing Alpha 1 are not part of the maintained pipeline.

## Upstream and credits

PJR is derived from Pokémon Heart & Soul / `pokemonHnS-expansion`, which itself builds on Modern Emerald, pokeemerald-expansion and pret's pokeemerald work.

Please retain the upstream credit chain. See [CREDITS.md](CREDITS.md) for the inherited project credits and attribution information.

## Repository note

This repository contains a substantial inherited branch history from the upstream Heart & Soul project. PJR development is carried on `master`; old upstream branches are retained as history unless deliberately removed later.
