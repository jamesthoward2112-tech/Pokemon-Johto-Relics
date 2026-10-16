# PRU — Goldenrod Department Store 2F Rock Shop

**Implementation branch:** `pru/encounter-ecology-20261016` ([PR #10](https://github.com/jamesthoward2112-tech/Pokemon-Johto-Relics/pull/10)).

**Status:** Three-tier badge-dependent inventory and dedicated clerk are committed to source. Source-only CI is the next gate. **Not yet a compiled or emulator-tested PRU ROM.**

## Design: unlock stock, not the shop

- Location: **Goldenrod Department Store 2F**. Existing supplies clerk at (14,11) remains; dedicated Rock Shop clerk at (17,11).
- The Rock Shop is always visible. It checks existing **fourth- and eighth-Johto badge flags** when spoken to, requires no new save fields, and chooses an increasingly large static Poké Mart item list.
- Branch priority: `FLAG_BADGE08_GET` first, then `FLAG_BADGE04_GET`, then arrival stock.
- Existing shops, gift scripts, pickups and story items are not rewritten. These are **shop unlock restrictions**, not global item bans.
- Shop entry communicates that more evolution items unlock with Gym Badges.

| Availability | Total stock | What is added |
| --- | ---: | --- |
| First visit to Goldenrod | **6** | Fire, Water, Thunder, Leaf, Moon and Sun Stones |
| Fourth Johto badge | **29** | Ice, Shiny, Dusk, Dawn and Oval Stones; King's Rock, Metal Coat, Dragon Scale, Up-Grade, Deep Sea Scale/Tooth, Linking Cord; 11 species-specific held evolution catalysts |
| Eighth Johto badge | **48** | Dubious Disc, Protector, Electirizer, Magmarizer, Prism Scale, Reaper Cloth, Razor Claw/Fang; Galarica Cuff/Wreath, Black Augurite, Peat Block; and 7 PJR Relic catalysts |

**Late Relic catalysts:** Ancient Shell, Fossil Bark, Ancient Tusk, Frost Mirror, Ancient Horn, Ancient Plume and Ancient Bell enter the shop only at the eighth badge. Ordinary Pokémon continue evolving through their own normal mechanics. A Relic evolution's own additional level, item, move or quest condition must also be met.

**Never sold at this Rock Shop:** story-only Ancient Rainbow Crest and Ancient Candy. Ancient Candy retains its separately approved post-League restriction.

All 48 approved items retain original PJR item IDs and current item definitions and prices. Existing Trainer's Market clerk retains its 18 original supplies. The department store directories still identify the Rock Shop.

## Nine-Pokémon acquisition impact

- Eevee -> Vaporeon/Flareon: **Water and Fire Stones at the first Rock Shop visit**.
- Clamperl -> Gorebyss: **Deep Sea Scale after fourth Johto badge**, which predates ordinary late-game Clamperl availability on Route 20.
- Tyrogue, Wurmple and Nincada evolution mechanics and wild locations unchanged.
- Eevee -> Espeon/Umbreon friendship/time-of-day mechanics remain unchanged.
- No mature evolved forms added to wild encounters purely to bypass progression.

## Source implementation and tests

- `data/maps/GoldenrodCity_DepartmentStore_2F_hns/scripts.inc`: badge-checked three-way Rock Shop dispatch; static inventories `GoldenrodDeptStore2_RockShop` (6), `GoldenrodDeptStore2_RockShopFourBadges` (29), `GoldenrodDeptStore2_RockShopEightBadges` (48).
- `data/maps/GoldenrodCity_DepartmentStore_2F_hns/map.json`: dedicated Rock Shop clerk at (17,11).
- `tools/pru/check_rock_shop.py`: exact stock/availability invariants, item-source registration, clerk coordinates and original goods retention.
- `tools/pru/check_nine_acquisition.py` and `tools/pru/check_nine_acquisition_routes.py`: check Water/Fire Stones in arrival inventory, Deep Sea items in four-badge inventory, and actual staged clerk connection.
- `.github/workflows/pru-encounter-ecology.yml`: runs source-only checks.

## ROM QA required after combining branches

1. Confirm starting with **three badges** opens 6 items; four badges gives 29; eight badges gives 48. Test ordinary saves crossing the unlock thresholds without special migration.
2. Validate actual Rock Shop clerk interaction, map collision, menu scrolling, each item cost and delivery.
3. Use Water/Fire Stones to evolve Eevee and Deep Sea Scale on Clamperl after appropriate badge progression.
4. Ensure shop does not allow Ancient Candy or quest-only crest early, and that source-gated rare Relic catalysts are not mistakenly offered early by any other new PRU store.
5. The interrupted 19-species PRL import may introduce **Ancient Stone / Ancient Emblem** or other *new* species-specific items. Reconcile those symbols and their approved story restrictions when branches are combined; do not guess their IDs or sell story keys.
6. Check correct Johto badge flag progression in emulator and ensure endgame unlocks do not rely on rematches.

**Do not merge this encounter/commerce branch into Work's unpublished worktree until its changes are safely pushed.** There is no verified complete PRU ROM from this branch.
