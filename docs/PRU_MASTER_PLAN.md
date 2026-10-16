# Pokémon Relics Ultimate — PJR donor baseline and implementation gates

Branch: `pru/ultimate-pokedex-encounters-20261016`
Donor: `pjr-rebuild` at `9e9ec181961efbbdba88055876dfa9b18fd0ae64`
Status: **development only; not playable-approved**.

## Non-negotiable scope
- **PRU is a fully standalone adventure and separate ROM**, not an extension/sequel of PKR, PHR, PJR, or PRL. It uses PJR as a technical/map/story donor only. No previous-ROM badge, Champion, money, party or save assumptions; no regional transfer/Hoenn playable chapter. The in-game title/credits/build artefact should eventually use `Pokémon Relics Ultimate` / `PRU` rather than PJR. Never overwrite the original `pjr-rebuild` release.
- Preserve PJR's Johto + Kanto maps and story, including the first Johto Elite Four, Kanto/Sinjoh continuation and existing league rematches.
- Pikachu is the **only offered first partner** at Elm's lab. The other research Poké Balls may remain for the theft storyline, but they are not obtainable by the player.
- All standard Kanto/Johto/Hoenn species (#001–#386), all nine traditional starter families, and every approved Relic/custom species are to be catchable or reachable by normal evolution. Species families may be geographically restricted by map/story access, but are not unlocked in waves.
- **Updated user decision (16 Oct 2026): NPC gifts, Pokémon Eggs, trades, prizes and fossil revivals are allowed as optional additional acquisition paths.** The opening remains Pikachu alone; preserve Elm's original Togepi Egg. Every gift species must also have an independent obtainable wild/evolution/static-encounter route in accessible PRU regions. Never make a gift the only way to complete the Pokédex.
- Retain existing PJR Elite Four and Gym rematch stories, then add the dedicated four-championship track.
- First championship: untouched PJR levels/teams/singles; second: similar party doubles approximately +10 levels; third: new teams and level cap; fourth: strongest Lv100 doubles and level cap.
- **Ancient Candy** unlocks only after **second** championship; keep Chansey training NPCs before that. Candy raises level and is reusable; avoid reverse candy by temporary battle-level adjustment for championship 3+.
- Preserve existing legendary story events. Oak unlocks additional legendary encounters after the first League; catchable encounter/battle progression must not be replaced with gift-only distribution.
- Add the **Relic Battle Hall** with five repeatable rival-pair double battles: Jessie/James; Steevee/Neevee; Green/May; Silver/Wally; Blue/Brendan.
- Add replayable Ultimate Gym partnerships; no unsupported assumptions that two opponent parties of six each work without multi-trainer engine changes.

## Current changes in this PR (scope 1)
- Elm's first selectable lab Poké Ball now awards level-5 Pikachu with existing shiny/party/PC semantics.
- Other two lab balls remain present for narrative continuity but cannot be selected. Rival-variable branch `VAR_STARTER_MON=0` retained intentionally.
- Elm opening dialogue changed to describe Pikachu instead of three choices.
- **Approved early-starter policy supersedes older locations:** all 9 traditional starter stages and 3 PJR starter stages are available no later than Route 33 / early Union Cave / Slowpoke Well, all wild at level 2–9, with no Surf requirement. Day/night variants contain the same starter where available. These remain catchable before their Lv14–18 evolutions, regardless of any optional NPC gifts.
- Chikorita Route 29 Lv2–3 (5%); Cyndaquil Route 30 Lv4 (5%); Totodile Slowpoke Well B1F Lv6–8 (5%); Bulbasaur Route 31 Lv5 (5%); Charmander Route 46 Lv2–3 (5%); Squirtle Route 32 **grass** Lv6 (5%); Treecko Route 30 Lv3–4 (4%); Torchic Route 33 Lv8–9 (5%); Mudkip Union Cave B1F Lv8 (5%).
- Scarabub Route 31 Lv5 (4%), evolves to Heracross at Lv18; Skarmet Route 46 Lv2–3 (4%), evolves to Skarmory at Lv18; Mootiny Route 29 Lv2–3 (4%), evolves to Miltank at Lv18. All three donor evolutions verified from `src/data/pokemon/species_info/pjr_families.h`.
- **Later evolved replacements:** Burned Tower Charmeleon Lv16–18; Route 41 Wartortle Lv22–25; Route 34 Grovyle Lv17–18; Route 37 Combusken Lv17–18; National Park Heracross Lv18; Route 45 Skarmory Lv37; Route 39 Miltank Lv21 (no Mootiny); deeper Slowpoke Well Croconaw Lv20–22; deeper Union Cave Marshtomp Lv21–23. Original Bulbasaur in Ilex Forest and Cyndaquil on Route 36 remain additional low-level opportunities; Totodile and Mudkip remain at their original early cave sources.
- Porygon remains catchable on Route 10 and Castform on Route 42. All inserted starter-stage encounters use existing PJR wild encounter slots. The wild catches are independent of optional NPC gift opportunities.
- Main HNS encounter baseline before targeted inserts contained 165 unique maps / 257 encounter variants; 265 of the original 386 were directly present in at least one HNS wild table. The other 121 mostly require evolution or static/legendary audits. This is **not** a claim that all 386 were already obtainable.
- **Gift policy correction committed 16 Oct:** restored original PJR Chikorita (Violet), Cyndaquil (Azalea) and Totodile (Goldenrod) optional aide gifts alongside their early wild encounters; restored Steven's choice of Treecko/Torchic/Mudkip at Silph Co. in Kanto. Elm's extra Scarabub/Skarmet/Mootiny Egg awards remain disabled for now from an earlier change; their availability and chronology are under separate review, not prohibited by gift policy.
- **Elm Togepi Egg preserved by user request:** keep `VioletCity_PokemonCenter_hns/scripts.inc`'s `giveegg SPECIES_TOGEPI`, Elm/Kimono story dialogue, `FLAG_RECEIVED_TOGEPI_EGG`, original hatching/return progression and Mr. Pokémon's separate Mystery Egg key item as PJR currently implements them. This existing Egg story remains mandatory to preserve; **do not redesign or remove the Togepi gift**.
- **Do not remove Pokémon gifts purely because species are wild.** Audit each gift, game-corner prize, restoration, trade and event endpoint, and prove a separate catch/evolution route for each species. Master all-species import is not complete.

## Standalone Relic dialogue — source audit
- Canonical chapter/timeline and source conflicts are tracked in [PRU_STANDALONE_RELIC_DIALOGUE_AUDIT.md](PRU_STANDALONE_RELIC_DIALOGUE_AUDIT.md). Treat this register as blocking until its unchecked scene-by-scene and fresh-save QA gates are closed.
- **Johto first**: Elm/Alph Resonance and PJR's radio-tower and first League plot are this player's first adventures. Kanto historical material may be adapted from PRL (most recent Kanto source), but cannot assume PKR/PRL's Kanto-first Champion, duplicate Giovanni-led Rocket or unknown golden bird after PJR's Ho-Oh reveal.
- **Other regions are world lore only**: Steven may mention Hoenn archaeology and rare species; the player has never travelled or transferred Pokémon to Hoenn in PRU.
- **Separate PKR 2.0**: PRL-to-Kanto-only conversion belongs in its own workstream/repository branch and is not a predecessor of PRU; do not strip PJR's Sinjoh/advanced legendary maps to enforce a #386 core planning index.

## Required gates BEFORE a playable declaration
1. Workflow `PJR Beta build` succeeds on this feature branch/PR.
2. Emulator fresh-save: Oak intro -> New Bark -> Elm's lab. Inspect all pages for textbox overflow.
3. Interact with each of three Poké Balls: only left ball yields Pikachu. Verify cry, battle back/front, party icon, nickname and PC deposits.
4. Finish Mr. Pokémon / Silver / police theft / Elm return; ensure visible balls and flags remain coherent, and Route 30 opens.
5. Audit optional NPC gifts, Egg awards, prizes, fossil revivals, trades and static encounters. **Retain donor gift dialogue and event flags by default**, explicitly protect Elm's Togepi Egg, and ensure gift species have separate catchable/evolvable routes. Preserve trade and gift failure/retry handling.
6. Reconcile every custom donor: distinguish species, form, shiny palette, trainer-only form, superseded design. Do not allocate final PJR species IDs without the resolved registry.
7. Audit `src/data/wild_encounters.json` (approximately 2 MB): first 14 species insertion completed by exact slot, but validate every day/night/surf/fishing table, rarity, DexNav and swarms in an emulator. Do not claim the entire National Dex is implemented.
8. Ensure all 386 base families plus approved custom families have a complete independent catch/evolution/encounter chain. Gift-only availability does not count toward this gate; gifts may coexist with the independent route.
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
