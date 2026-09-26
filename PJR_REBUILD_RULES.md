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
- Do not mention capsules opening unless a real capsule-opening presentation is implemented and tested.
- For the rebuild, use the normal three-ball table interaction first. Add presentation effects only after the underlying starter path is solid.
- The selected starter must be created directly into party slot 0 when the party is empty.
- A starter selection is not accepted unless its front sprite, back sprite, party icon, summary screen, PC storage icon, cry, name, typing and moves all render correctly.
- Test all three starters independently from a fresh save.

## Key-item rules

- Do not dump Relic Journal, DexNav and Remote PC/Box Link on the player immediately after choosing a starter.
- Introduce utility key items deliberately at appropriate story beats, one at a time, with each feature tested before the next is enabled.
- The starter flow must not depend on Remote PC.

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
