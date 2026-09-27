# PJR Work Mode Handoff

- Branch: `pjr-rebuild`
- Baseline: latest accepted three-starter rebuild lineage; no restart or rollback
- Build workflow: `.github/workflows/pjr-rebuild.yml`

## Completed in this integration line

- Approved PJR title screen restored with flashing `PRESS START`.
- Challenge/Nuzlocke setup removed from the opening flow.
- Oak and Elm relic-story dialogue shortened and aligned with the real three-ball sequence.
- Scarabub, Skarmet, and Mootiny remain direct level-5 party gifts.
- Player can leave Elm's lab immediately after choosing a starter.
- First aide gift changed from Potion to functional DexNav; Remote PC staged for the later Violet City aide event.
- Followers remain disabled.
- Infinity donor species, graphics, level-up learnsets, and required signature moves integrated for the queued PJR species.
- `Pressurize` verified from the supplied Infinity PBS: Rock/status, 20 PP, sharply raises the user's Special Defense.
- `Kablow!` now detonates the user and places one layer each of Spikes and Toxic Spikes.
- Normal Unown changed from Levitate to Wonder Guard and given a full Psychic/coverage level-up learnset.

## Not completed

- Full emulator-driven opening regression test for all three starter choices.
- Large-mart evolution-item stock pass, including final Drakeon availability verification.
- Any Infinity mechanic requiring broad engine recreation beyond the moves actually used by PJR species.

## Build status

- The branch push invokes the repository workflow, which installs the ARM toolchain and uploads `PJR-Three-Starters-Test.gba`.
- If CI fails, the exact compiler/workflow error from that run is the next blocker to fix.

## Next unfinished task

Verify the large-mart evolution-item inventory and Drakeon's locked Dragon Fang evolution condition after the next successful ROM has passed the opening-flow playtest.
