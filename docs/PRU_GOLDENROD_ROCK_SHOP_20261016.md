# PRU — Goldenrod Department Store Rock Shop

**Implementation branch:** `pru/encounter-ecology-20261016` (encounter-only PR #10).

**Status:** Script, map NPC and directory **committed to source**. Source-only CI in progress; do not claim this as a playable or emulator-tested shop until the consolidated 19-species ROM is built and the counter has been visited.

## Design decision

The player encounters **one dedicated Rock Shop inside Goldenrod Department Store 2F**, alongside the original Trainer's Market supplies clerk. Reuse an existing floor/counter; do **not** add a standalone building, edit storyline flags, reset saves, or repurpose other shop floors.

- Existing general clerk: (14,11), `GoldenrodDeptStore2_EventScript_Clerk`, 18 ordinary trainer supplies; balls, medicine, Escape Rope, Repels.
- New Rock Shop clerk: (17,11), `GoldenrodDeptStore2_EventScript_RockShop`, 48 evolution-related items in `GoldenrodDeptStore2_RockShop`.
- 1F directory and 2F directory both show `2F MARKET / ROCK SHOP`.
- Shop entry says `Welcome to the ROCK SHOP!` and explains stones, special evolution items and Relic catalysts.
- Existing Poké Mart pricing is reused, instead of adding arbitrary per-item prices.

## Stock categories

| Stock type | Examples |
| --- | --- |
| Evolution stones (11) | Fire, Water, Thunder, Leaf, Ice, Moon, Sun, Shiny, Dusk, Dawn, Oval |
| Held/trade evolution catalysts (15) | King's Rock, Metal Coat, Dragon Scale, Up-Grade, Dubious Disc, Protector, Electirizer, Magmarizer, Prism Scale, Reaper Cloth, Razor Claw, Razor Fang, both Deep Sea items, Linking Cord |
| Regional alternative evolution items (4) | Galarica Cuff/Wreath, Black Augurite, Peat Block |
| Species-specific held evolution catalysts (11) | Expert Belt, Silver Powder, Soft Sand, Hard Stone, Poison Barb, Dragon Fang, Thick Club, Spell Tag, Miracle Seed, Charcoal, Mystic Water |
| PJR Relic catalysts (7) | Ancient Shell, Fossil Bark, Ancient Tusk, Frost Mirror, Ancient Horn, Ancient Plume, Ancient Bell |

All 48 items have source constants and item definitions; the PJR Relic catalysts use the existing `PJR_CATALYST_ITEM` data macro. **The Ancient Rainbow Crest is a story-only key item and is intentionally not sold. Ancient Candy is not a shop item and remains behind its approved late-game restrictions.**

This central counter does not substitute species-specific level, friendship, move-use, story or badge conditions: it only offers evolution items. Evolution still has to satisfy the actual species rules.

## Nine-acquisition audit impact

The Water Stone, Fire Stone and Deep Sea Scale required to produce Vaporeon, Flareon and Gorebyss now have a **single, explicit purchase endpoint** at this Rock Shop, instead of being mixed into the original supply clerk inventory. Separate Tyrogue/Eevee/Wurmple/Nincada/Clamperl wild sources remain unchanged. The nine-species checks are updated to point to the actual Rock Shop clerk.

## Static checks and gameplay gates

Run:
- `python tools/pru/check_encounter_ecology.py`
- `python tools/pru/check_nine_acquisition.py`
- `python tools/pru/check_nine_acquisition_routes.py`
- `python tools/pru/check_rock_shop.py`

CI: `.github/workflows/pru-encounter-ecology.yml`. The Rock Shop gate checks complete stock, preserved supplies, item definitions, map NPC scripts/coordinates and directory text.

**Post-merge ROM QA needed:** Counter position and collision, shop interaction, full-item list scrolling, price deduction and item delivery, stock availability from a normal save, actual item-use evolutions and in-game time/friendship rules. Any newly added PRL item constants such as **Ancient Stone** or **Ancient Emblem** (if introduced by the 19-species engine import) must be reconciled with this counter. Never sell unique progression/story keys or Ancient Candy merely to satisfy a broad item list.

## Work handoff

Do not merge PR #10 onto the interrupted local Work branch until that worktree has been safely committed and pushed. Once saved, integrate the Rock Shop and all encounter regression tests as part of the **single consolidated PRU build**. Keep PRL custom species and battle engine untouched by this shop-specific branch.
