# Pokémon Relics Ultimate — PJR donor baseline and implementation gates

Branch: `pru/ultimate-pokedex-encounters-20261016`
Donor: `pjr-rebuild` at `9e9ec181961efbbdba88055876dfa9b18fd0ae64`
Status: **development only; not playable-approved**.

## Non-negotiable scope
- Separate PJR-based ROM. Never overwrite/rebrand the existing `pjr-rebuild` release.
- Preserve PJR's Johto + Kanto maps and story, including the first Johto Elite Four, Kanto/Sinjoh continuation and existing league rematches.
- Pikachu is the **only offered first partner** at Elm's lab. The other research Poké Balls may remain for the theft storyline, but they are not obtainable by the player.
- All standard Kanto/Johto/Hoenn species (#001–#386), all nine traditional starter families, and every approved Relic/custom species are to be catchable or reachable by normal evolution. Species families may be geographically restricted by map/story access, but are not unlocked in waves.
- No gift Pokémon or gift eggs besides the opening Pikachu. Existing story-critical egg handoffs must be redesigned with progression flags still intact; do not blindly delete scripts.
- Retain existing PJR Elite Four and Gym rematch stories, then add the dedicated four-championship track.
- First championship: untouched PJR levels/teams/singles; second: similar party doubles approximately +10 levels; third: new teams and level cap; fourth: strongest Lv100 doubles and level cap.
- **Ancient Candy** unlocks only after **second** championship; keep Chansey training NPCs before that. Candy raises level and is reusable; avoid reverse candy by temporary battle-level adjustment for championship 3+.
- Preserve existing legendary story events. Oak unlocks otherwise-unavailable legendary quests after first League win; no gifts.
- Add the **Relic Battle Hall** with five repeatable rival-pair double battles: Jessie/James; Steevee/Neevee; Green/May; Silver/Wally; Blue/Brendan.
- Add replayable Ultimate Gym partnerships; no unsupported assumptions that two opponent parties of six each work without multi-trainer engine changes.

## Current changes in this PR (scope 1)
- Elm's first selectable lab Poké Ball now awards level-5 Pikachu with existing shiny/party/PC semantics.
- Other two lab balls remain present for narrative continuity but cannot be selected. Rival-variable branch `VAR_STARTER_MON=0` retained intentionally.
- Elm opening dialogue changed to describe Pikachu instead of three choices.
- 14 Pokémon gained deliberately placed wild slots: Chikorita (Route 29), Cyndaquil (Route 36), Totodile (Slowpoke Well), Bulbasaur (Ilex Forest), Charmander (Burned Tower), Squirtle (Route 41 Surf), Treecko (Route 34), Torchic (Route 37), Mudkip (Union Cave), Scarabub (National Park), Skarmet (Route 45), Mootiny (Route 39), Porygon (Route 10), and Castform (Route 42).
- Land starter slots use 5% table positions. Squirtle/Porygon/Castform use 1% positions. Fourteen species were inserted into 24 day/night or single encounter variants. Existing displaced species retain other slots in the same variant.
- Main HNS encounter baseline before targeted inserts contained 165 unique maps / 257 encounter variants; 265 of the original 386 were directly present in at least one HNS wild table. The other 121 mostly require evolution or static/legendary audits. This is **not** a claim that all 386 were already obtainable.
- **No other gift events removed yet.** The master all-species import is not complete.

## Required gates BEFORE a playable declaration
1. Workflow `PJR Beta build` succeeds on this feature branch/PR.
2. Emulator fresh-save: Oak intro -> New Bark -> Elm's lab. Inspect all pages for textbox overflow.
3. Interact with each of three Poké Balls: only left ball yields Pikachu. Verify cry, battle back/front, party icon, nickname and PC deposits.
4. Finish Mr. Pokémon / Silver / police theft / Elm return; ensure visible balls and flags remain coherent, and Route 30 opens.
5. Audit every gift/egg/trade/static species award. Preserve Oak/Elm story logic while converting disallowed Pokémon rewards to catchable encounters; ordinary in-game trades also need an explicit policy.
6. Reconcile every custom donor: distinguish species, form, shiny palette, trainer-only form, superseded design. Do not allocate final PJR species IDs without the resolved registry.
7. Audit `src/data/wild_encounters.json` (approximately 2 MB): first 14 species insertion completed by exact slot, but validate every day/night/surf/fishing table, rarity, DexNav and swarms in an emulator. Do not claim the entire National Dex is implemented.
8. Ensure all 386 base families plus approved custom families have a complete acquisition chain: encounter, evolution item/condition, or scripted legendary battle. No inaccessible gifts.
9. Test championship and Trainer Card progression with fresh saves; no persistent level mutation from battle cap.
10. Check final GBA ROM size, battle graphics/icon/palette pipeline, and save version/migration.

## Starter habitat proposals — unimplemented
- Bulbasaur: Ilex/Viridian Forest; Chikorita: early Johto grassland; Treecko: Ilex and late forest routes.
- Charmander: Burned Tower foothills/Mt. Silver; Cyndaquil: early Johto warm/dry areas; Torchic: grassland nearer Route 37.
- Squirtle: coasts/Seafoam; Totodile: Slowpoke Well waterways; Mudkip: cave pools/Union Cave.
- All three custom PJR starter families (Scarabub, Skarmet, Mootiny) must be moved into wild encounter/evolution chains. **Do not remove their assets.**
- Replace currently scripted gifts such as PJR starter Eggs only after confirming no plot progression relies on the gift flag.

## Evidence
- `data/maps/NewBarkTown_Lab_hns/scripts.inc`: Elm, starter gift, Silver theft and multiple later Egg gift flows.
- `data/maps/PokemonLeague_WillsRoom_hns/scripts.inc`: original, Johto Champion rematch and post-Sinjoh rematch branches.
- `data/maps/PokemonLeague_ChampionsRoom_hns/scripts.inc`: Lance original/rematch and separate championship dialogue.
- `FEATURES.md`: 16 Gym rematches, Gen 1–9 species support, Nuzlocke-only infinite Rare Candy option and current Hoenn encounter audio system.
