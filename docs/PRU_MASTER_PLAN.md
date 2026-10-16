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
- **Approved early-starter policy supersedes older locations:** all 9 traditional starter stages and 3 PJR starter stages are available no later than Route 33 / early Union Cave / Slowpoke Well, all wild at level 2–9, with no Surf requirement. Day/night variants contain the same starter where available. These are catchable before their Lv14–18 evolutions, not late-game gifts.
- Chikorita Route 29 Lv2–3 (5%); Cyndaquil Route 30 Lv4 (5%); Totodile Slowpoke Well B1F Lv6–8 (5%); Bulbasaur Route 31 Lv5 (5%); Charmander Route 46 Lv2–3 (5%); Squirtle Route 32 **grass** Lv6 (5%); Treecko Route 30 Lv3–4 (4%); Torchic Route 33 Lv8–9 (5%); Mudkip Union Cave B1F Lv8 (5%).
- Scarabub Route 31 Lv5 (4%), evolves to Heracross at Lv18; Skarmet Route 46 Lv2–3 (4%), evolves to Skarmory at Lv18; Mootiny Route 29 Lv2–3 (4%), evolves to Miltank at Lv18. All three donor evolutions verified from `src/data/pokemon/species_info/pjr_families.h`.
- **Later evolved replacements:** Burned Tower Charmeleon Lv16–18; Route 41 Wartortle Lv22–25; Route 34 Grovyle Lv17–18; Route 37 Combusken Lv17–18; National Park Heracross Lv18; Route 45 Skarmory Lv37; Route 39 Miltank Lv21 (no Mootiny); deeper Slowpoke Well Croconaw Lv20–22; deeper Union Cave Marshtomp Lv21–23. Original Bulbasaur in Ilex Forest and Cyndaquil on Route 36 remain additional low-level opportunities; Totodile and Mudkip remain at their original early cave sources.
- Porygon remains catchable on Route 10 and Castform on Route 42. All inserted starter-stage encounters use existing PJR wild encounter slots; no gift conversion beyond the Pikachu opening yet.
- Main HNS encounter baseline before targeted inserts contained 165 unique maps / 257 encounter variants; 265 of the original 386 were directly present in at least one HNS wild table. The other 121 mostly require evolution or static/legendary audits. This is **not** a claim that all 386 were already obtainable.
- **Gift conversion pass 1 committed:** Elm's post-first-League starter Egg awards no longer grant eggs; original League directions and progress flags are retained. Three town aide scripts no longer give Chikorita (Violet City), Cyndaquil (Azalea Town), or Totodile (Goldenrod City); aides and their own Pokémon remain standing in towns and offer wild-location clues. The early-game starter families are already obtainable in the wild.
- **Story-critical Togepi Egg still pending.** `VioletCity_PokemonCenter_hns/scripts.inc` has `giveegg SPECIES_TOGEPI`; Elm/Kimono dialogues and `FLAG_RECEIVED_TOGEPI_EGG` are plot-linked. Do not remove until follow-up story-flag compatibility is verified. Mr. Pokémon's separate Mystery Egg key item and early plot remain untouched.
- **No claim yet that all gifts are removed.** Run comprehensive Pokémon-grant code search throughout other events, game corner, restoration, and trade endpoints. Master all-species import is not complete.

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

## Early and evolved encounter audit — committed; emulator pending
- Canonical map/level/location rules are the early-start policy above. No new PJR geography or Surf dependency for a starter-stage Pokémon.
- Encounter-table change `078310b5` replaces 32 variant slots. Every displaced original species remains available in at least one other slot in that same variant; this was checked before committing.
- GitHub compilation verifies source integration only. Fresh-save playtesting must check early access, wild catch rate, progression and evolved-stage availability; do not equate a successful build with in-game success.
- Any further Pokémon encounter pass must preserve this early starter availability as a regression gate.

## Evidence
- `data/maps/NewBarkTown_Lab_hns/scripts.inc`: Elm, starter gift, Silver theft and multiple later Egg gift flows.
- `data/maps/PokemonLeague_WillsRoom_hns/scripts.inc`: original, Johto Champion rematch and post-Sinjoh rematch branches.
- `data/maps/PokemonLeague_ChampionsRoom_hns/scripts.inc`: Lance original/rematch and separate championship dialogue.
- `FEATURES.md`: 16 Gym rematches, Gen 1–9 species support, Nuzlocke-only infinite Rare Candy option and current Hoenn encounter audio system.
