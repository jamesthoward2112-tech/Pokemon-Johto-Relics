# PRU nine ordinary species acquisition audit (16 October 2026)

**Status:** Nine evolution chains, wild sources and the shared Goldenrod 2F evolution-item shop verified against real source files. Automated regression test committed; CI outcome and actual gameplay QA must be reported separately. **No claim of a compiled or emulator-tested ROM.**

Source baseline: `pru/encounter-ecology-20261016`, following encounter ecology PR #10. This audit stays entirely outside the interrupted Work branch and does **not** change battle engine or existing species IDs.

## Nine species and verified sources

| Target Pokémon | Base species and wild source | Code-defined evolution | Source audit |
|---|---|---|---|
| Hitmonlee | Tyrogue; Mt. Mortar 1F South (day/night), Lv18–20 | Lv20, Attack > Defence | Present |
| Hitmontop | Same wild Tyrogue | Lv20, Attack = Defence | Present |
| Vaporeon | Eevee; Route 29 (day/night), Lv2–3; also Route 34 | Eevee + Water Stone | Present |
| Flareon | Same wild Eevee | Eevee + Fire Stone | Present |
| Espeon | Same wild Eevee | High friendship and **not** nighttime, on level-up | Present |
| Umbreon | Same wild Eevee | High friendship at nighttime, on level-up | Present |
| Cascoon | Wurmple; Ilex Forest day, Lv8–9 | Lv7, personality upper-modulo-10 < 5; the opposite half produces Silcoon | Present (requires earlier-level Wurmple or offspring to experience Lv7 evolution) |
| Shedinja | Nincada; Union Cave 1F day, Lv8–9 | Nincada evolves to Ninjask at Lv20 and the split evolution creates Shedinja if party room and Poké Ball conditions pass | Present |
| Gorebyss | Clamperl; Route 20 fishing, Lv40 (also later isles) | Clamperl + Deep Sea Scale, direct item route; held-item trade route is also defined | Present |

### Source-specific details

- Tyrogue branches use `IF_ATK_GT_DEF` for Hitmonlee, `IF_ATK_EQ_DEF` for Hitmontop, and `IF_ATK_LT_DEF` for Hitmonchan. Evolving one particular Tyrogue cannot produce all three; player can catch/breed others and control stat parity by training.
- Eevee's Vaporeon/Flareon stone evolutions coexist with multiple approved custom Eevee branches. Preserve all of them. Espeon `IF_NOT_TIME, TIME_NIGHT` and Umbreon `IF_TIME, TIME_NIGHT` must remain intact.
- Wurmple source uses `IF_PID_UPPER_MODULO_10_LT, 5` for Cascoon. The Ilex Forest wild Wurmple is **already Lv8–9** and must gain an additional level to evolve; confirm evolution code applies `EVO_LEVEL, 7` when level exceeds the threshold. Wild Cascoon is not necessary.
- Shedinja's `CreateShedinja` checks party capacity and takes a standard Poké Ball from bag under `P_SHEDINJA_BALL GEN_LATEST`. Ensure player has an empty party slot and at least one Poké Ball before Lv20; don't create an ordinary wild Shedinja to bypass this.
- The Fire Stone and Water Stone item records have actual `ItemUseOutOfBattle_EvolutionStone` usage. Deep Sea Scale has `gItemEffect_EvoItem` with `EVO_HELD_ITEM_TYPE` / `EVO_HELD_ITEM_FIELD_FUNC`; actual direct item-use behaviour depends on these config macros and gameplay QA.
- All wild source paths above are entries in `src/data/wild_encounters.json` on the HNS maps, not asserted completed encounters in a compiled ROM.

## Outstanding independent QA

1. **Source item availability VERIFIED:** Goldenrod City Department Store 2F has a visible unflagged shopkeeper (`GoldenrodDeptStore2_EventScript_Clerk`) selling `ITEM_FIRE_STONE`, `ITEM_WATER_STONE`, and `ITEM_DEEP_SEA_SCALE` from one normal Poké Mart inventory. Item definitions support party-use Fire/Water Stones; `I_USE_EVO_HELD_ITEMS_FROM_BAG TRUE` is configured for the Deep Sea Scale. The automated source regression gate now checks the clerk, map and inventory. **Remaining gameplay QA:** actually reach 2F, buy/use all three items and confirm caught-Dex registration in a compiled ROM.
2. Verify friendship and daytime/nighttime clock functionality; compare Eevee's conditions against competing custom Eevee branch ordering.
3. Verify Tyrogue's exact stat-parity branch; verify Wurmple caught at Lv8–9 still evolves after its next level gain; verify Nincada with and without room/Poké Ball.
4. Catch Clamperl and evolve it directly using Deep Sea Scale; confirm it does not require a trade after all.
5. Confirm all nine caught-Dex entries unlock correctly in a built ROM and test with a fresh save and an existing PJR save.

## Regression automation

`python3 tools/pru/check_nine_acquisition_routes.py` checks original source evolution definitions, item interfaces, Shedinja's creation handler, the five required HNS wild acquisition sources, and the unflagged Goldenrod 2F clerk offering all three required evolution items. It is part of `.github/workflows/pru-encounter-ecology.yml`. **This is a source-only safety gate**, not proof of shop availability or emulator success.

## Work handoff

After Work recovers and pushes the unpublished 19-species PRL integration, selectively merge [PR #10](https://github.com/jamesthoward2112-tech/Pokemon-Johto-Relics/pull/10) into the combined branch. Re-run both ecology gates against the combined source, verify items/evolutions through actual gameplay, and update `docs/PRU_WORK_RESUME_CHECKPOINT.md` with the merged commit and CI results.

**Decision needed from user:** none. Prefer existing authentic evolution rules, accessible item placement and in-game testing. Legendary and Mythical catchability remains separate.
