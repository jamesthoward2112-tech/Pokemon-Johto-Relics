# PRU Work Resume Checkpoint

Updated: 2026-10-16 (recovery after interrupted Work session)

## Live recovery state — 2026-10-16T16:18:30Z
- Active local branch: `pru/complete-selective-integration-20261016`.
- Recovery base: `464fc66ed2ebe11ca1e4cda47d891dc753828499`, the CI-passing PR #11 head. It contains the seven native-move/Eerie Fog commits directly on top of PR #9.
- Last published implementation before this checkpoint: `464fc66ed2ebe11ca1e4cda47d891dc753828499` on `origin/pru/battle-port-phase1-20261016`; GitHub Actions run `38925573625` compiled the isolated ROM successfully.
- The original scratch worktree disappeared before this resumed session. Its local-only commits (`e6fb58120`, `ba603890c`) and uncommitted species/mechanics files were not present in any remote ref and could not be recovered byte-for-byte. No claim is made that those files were preserved.
- Retained evidence from the interrupted session records GREEN static checks for the 19-species ID allocation, Bleeding/Fear/Eerie Fog source integration and selective Radical Red data, but those local edits were never compiled or pushed and must be reconstructed from the pinned donors.
- Working tree at recovery was clean. This branch is the sole resumed integration branch; PR #10 remains separate.
- Immediate priorities: reconstruct the 19 species/data/assets with the ID-freeze verifier; then port remaining authentic moves/abilities/status mechanics; then implement Mewsion issue #8; finally compile in CI and emulator-test.
- Local build constraint remains: the scratch host lacks `arm-none-eabi-gcc`, `pkg-config` and libpng development headers, so GitHub Actions is the authoritative build environment.

## Purpose
A **GitHub-published recovery checkpoint** for Pokémon Relics Ultimate's consolidated integration. Update this file after each meaningful source milestone and before every expected Work-session limit. Local-only logs are insufficient; **push the checkpoint and source commits to the remote branch** so a future conversation can resume without repeating investigation.

## Repository and authoritative inputs
- Repository: `jamesthoward2112-tech/Pokemon-Johto-Relics`
- Current verified, remotely published engineering branch: `pru/consolidated-prl-battle-import-20261016`
- Existing PR: [#9 — WIP consolidated import](https://github.com/jamesthoward2112-tech/Pokemon-Johto-Relics/pull/9)
- Verified published head at recovery: `b4b1d5f18ba52ab7af03081d25bfc82b9079b7dd`
- Stable PJR/PRU base: `pru/full-relic-import-20261016`; commit `c02ec0f209d680190f538fc224b6e440f3fc7a02` recorded as Work starting point.
- Pinned PRL/PR108 donor: `jamesthoward2112-tech/Pokemon-Relic-Legacy` commit `6ee9b984521ac6f2beaf995f771a726379e55c88`.
- External donors/canonical files: ChatGPT Library, `/Pokémon Relics Ultimate/Canonical Data/`.
- Approved encounter requirements: GitHub issue #8 (Mewsion Level 90, Cerulean Cave B2F).

## Recovery notice: published vs unpublished work
The prior **Work** session reported an isolated **local** branch `pru/complete-selective-integration-20261016`, a persistent progress ledger, and RED/GREEN compatibility-verifier checkpoints. The supplied screen recording shows reported activity on species verification, PRL mechanics, ability/graphics data, Seviian art and Mewsion logic. **This local branch is NOT present among published GitHub remote branches as of this checkpoint** and its full worktree is **not recoverable from this GitHub branch alone**. Reported local milestones are not asserted as verified commits or finished build results.

**Required first step on returning to that original Work session:** inspect its existing worktree and local branches; print `git status -sb`, `git log -n 15 --oneline --all --decorate`, and list any progress-ledger/checkpoint files; commit unfinished work safely to the existing isolated local branch, push `pru/complete-selective-integration-20261016` to `origin`, and push/update this checkpoint on the same branch. Do NOT restart the donor audit or discard existing source changes. Confirm remote SHA and include it here.

If the original Work container is irretrievable, continue on the separately published PR #9 branch from its verified commit rather than claiming local Work changes are available.

## Verified remotely published progress
- PR #9 contains canonical source requirements, pinned **37 authentic PRL custom move records**, ability descriptions, and compatibility reconciliation. This **does not prove** all battle effects are fully implemented.
- PJR source already defines 34 of PRL's 50 custom entries. The remaining 16 include superseded nuMew, so **15 genuine missing PRL species** remain.
- External donor species to import: **Adnokana, Cheauking, Frytning, Mewsion**.
- Internal PJR species IDs **1–1623 frozen**; append the 19 required imports **1624–1642** without changing existing saves.
- Standard Wooper/Quagsire must remain; preserve Paldean Wooper/Clodsire as separate forms/entries. Seviian Noibat/Noivern must reuse approved existing slots; selectively adapt Radical Red source.
- Do **not** report a consolidated ROM as compiled or emulator-tested: none is verified on the published PR #9 branch.

## Mandatory implementation
1. Port 19 species at IDs 1624–1642 with approved donor stats, typing, abilities, learned/TM/tutor/egg moves, evolution chains and cries.
2. Compare existing PJR Johto overlaps against PRL; keep approved PJR Johto gameplay and import approved latest PRL Kanto/Hoenn artwork and movesets.
3. Port **all genuine PRL custom moves and abilities** with real effects, triggers, battle text, animations and AI handling — no substituted vanilla abilities/moves.
4. **Bleeding:** PRL status bit 13, original move-specific infliction chances, 1/16 end-turn damage, healing integration, red BLD visual.
5. **Fear:** genuine two-turn volatile, 1.5× damage taken, escape restriction and related interactions.
6. **Eerie Fog:** real eight-turn weather and ability support; preserve PJR Frostbite.
7. Mewsion #425: Level 90, only after **both Mew and Mewtwo CAUGHT**, complete cave exit/re-entry, same B2F tile as Mewtwo, warning once on eligible B2F entry, retry after KO/flee, permanent dismissal on capture. Preserve Level 80 Mewtwo and Level 50 Faraway Island Mew.
8. Preserve Elm Pikachu-only starter, original Togepi Egg, early wild starter availability, PJR story, wild encounters and all existing saves.

## Build / verification gates
- Validate ID freeze, data and graphics registration, evolution access and availability of all 444 species.
- Verify original and shiny battle sprites, palette limits, both party icon frames, move tables and ability effects.
- Build actual standalone GBA ROM in GitHub CI; capture workflow URL, commit SHA, ROM filename and SHA-256.
- Emulator test clean and existing saves (mGBA if available), battles/statuses, encounters, Pokédex, graphics and gameplay progression.
- Produce final ROM, comprehensive comparison report and PR. Do not call anything tested before tests pass.

## Required live checkpoint update template
At **each meaningful code milestone or before work interruption**, overwrite this section with:
- UTC timestamp; active local and remote branch names; current local commit; last successfully pushed commit.
- What was changed and committed (specific file names/SHAs), tests run and their actual pass/fail results.
- Current build status and any available CI URL/artifact/SHA-256.
- Exact unresolved build errors, blockers, next command and priority tasks.
- Worktree dirty/untracked files and whether critical files were pushed to origin.
- Source/data provenance and unresolved donor/graphics assumptions.

**Rule: push source + checkpoint at meaningful intervals, and always before an expected usage cutoff. Never say the checkpoint is remotely recoverable until a `git ls-remote origin` check confirms it.**

## Independent acquisition follow-up — ready to cherry-pick (16 October)

The separate `pru/encounter-ecology-20261016` branch and [PR #10](https://github.com/jamesthoward2112-tech/Pokemon-Johto-Relics/pull/10) now include the completed **nine ordinary Pokémon source-audit follow-up**:
- Tyrogue Mt Mortar 1F south day/night Lv18–20 (Hitmonlee and Hitmontop); Wurmple Ilex Forest day Lv8–9 (Cascoon); Nincada Union Cave 1F Lv8–9 (Shedinja).
- Eevee Route 29 and all Water Stone, Fire Stone, friendship day/night evolution branches confirmed from species source (Vaporeon, Flareon, Espeon, Umbreon).
- Goldenrod 2F now sells Deep Sea Scale and Tooth, complementing Clamperl's existing Route 20 fishing and Gorebyss/Huntail source evolution definitions.
- `tools/pru/check_nine_acquisition.py` runs under `.github/workflows/pru-encounter-ecology.yml`. GitHub Actions passed on commit `d02fd90bfd30ec643b0e5f95c8f40b97db9a0a42`; this is **source-only QA**, not compilation or emulator testing.
- The full 444-row acquisition matrix now marks these nine `EVOLUTION_DEFINED_QA_PENDING` rather than unresolved.
- Detailed report: `docs/PRU_ENCOUNTER_ECOLOGY_20261016.md`; follow-up branch tip at time of note: `330bc40411ef8d7181e89912b4ae544dbbacd1e2`.
- **Handoff:** after recovering and pushing Work's unpublished source, selectively merge/cherry-pick PR #10 into the consolidated integration branch, resolve the `SPECIES_GEMLIN` dependency, then compile and emulator-test. Avoid source-file replacement that drops Work's newly ported species data.
