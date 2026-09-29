# PJR Alpha Rebuild — hard rules from failed Alpha 1

This branch is a clean rebuild from frozen upstream commit `167aa6d537b109bb229c231ddce4616974c4da71`.

The previous Alpha 1 on `master` is reference-only. Do not copy its opening/starter implementation wholesale.

## Opening rules

- Keep the proven vanilla Heart & Soul Oak intro flow until any replacement text has been tested page-by-page.
- Do not change Oak task/fade/name-screen state logic merely to skip menus or speed up the intro.
- No dialogue page may exceed the normal text box width/line limits.
- Any PJR-specific Oak wording must be concise, grammatically complete, and visually tested before merging.

## Elm / starter rules

- Elm's dialogue must describe what actually happens on screen.
- The normal three-ball table interaction is the canonical PJR starter sequence for Alpha; no alternate capsule sequence is required.
- The selected starter must be created directly into party slot 0 when the party is empty.
- A starter selection is not accepted unless its front sprite, back sprite, party icon, summary screen, PC storage icon, cry, name, typing and moves all render correctly.
- Test all three starters independently from a fresh save.

## Utility / progression rules

- DexNav may be enabled during the New Bark opening as currently implemented.
- A separate Remote PC item is not required when Box Link functionality is available.
- Relic Journal progression is represented by the Alpha Ruins Lab RELICS sequence; no separate Relic Journal starter item is required.
- The starter flow must not depend on storage access.

## Asset rules

- Treat source PNGs as the source of truth.
- Do not hand-commit generated `.4bpp` / palette output for new Pokémon unless the build system explicitly requires it and it has been verified against an existing species pipeline.
- Match the existing HnS/pokeemerald-expansion species graphics conventions rather than inventing a parallel graphics path.
- Validate front/back/icon assets in game, not just by opening PNG files.

## Gate before calling anything Alpha

A candidate build must pass:
1. Oak intro through name confirmation with no overlap/stall.
2. Elm opening dialogue reads naturally and matches the actual interaction.
3. Scarabub, Skarmet and Mootiny each appear correctly in the selection preview.
4. Each selected starter lands in the party, not the PC.
5. Party menu icon is correct.
6. Summary front sprite is visible.
7. PC deposit/withdraw works normally.
8. No mystery/question-mark party entries.
9. Fresh-save smoke test repeated for all three starters.

## Overworld follower rule

- Pokémon followers are disabled in PJR.
- The follower and big-follower options are removed from the options menu.
- Custom Pokémon only require battle front/back sprites and party icons; no overworld follower sprite is required unless a future scripted event explicitly needs one.
