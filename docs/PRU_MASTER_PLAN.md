# Pokémon Relics Ultimate — PJR donor baseline and implementation gates

Branch: `pru/pretest-story-services-20261016` (supersedes old donor-plan status; original donor branch `pru/ultimate-pokedex-encounters-20261016`)
Donor: `pjr-rebuild` at `9e9ec181961efbbdba88055876dfa9b18fd0ae64`
Status: **development only; not playable-approved**.

## Non-negotiable scope
- PRU is a **fully standalone Johto-first adventure**; PJR is a technical/story/map donor, not a previous save. Never overwrite/rebrand the existing `pjr-rebuild` release.
- Preserve PJR's Johto + Kanto maps and story, including the first Johto Elite Four, Kanto/Sinjoh continuation and existing league rematches.
- Elm **hands over Level 5 Pikachu directly**, without any starter choice or Yes/No prompt. Three decorative fossil displays replace the Poké Balls on his desk. Silver's theft happens from the lab's stored research stock; the fossils cannot be taken.
- All standard Kanto/Johto/Hoenn species (#001–#386), all nine traditional starter families, and every approved Relic/custom species are to be catchable or reachable by normal evolution. Species families may be geographically restricted by map/story access, but are not unlocked in waves.
- **Optional gifts/eggs/trades are permitted**, but every gift species must also have a separate catch/evolution path within PRU. Reassess redundant traditional-starter gifts (including the Hoenn choices) in favour of rarer, progression-appropriate species. **Preserve Elm's original Togepi Egg and Mystery Egg plot without alterations.** Do not make legendary Pokémon gift-only.
- Retain existing PJR Elite Four and Gym rematch stories, then add the dedicated four-championship track.
- First championship: untouched PJR levels/teams/singles; second: similar party doubles approximately +10 levels; third: new teams and level cap; fourth: strongest Lv100 doubles and level cap.
- **Ancient Candy** unlocks only after **second** championship; keep Chansey training NPCs before that. Candy raises level and is reusable; avoid reverse candy by temporary battle-level adjustment for championship 3+.
- Preserve existing legendary story events. Oak unlocks otherwise-unavailable legendary quests after first League win; no gifts.
- Add the **Relic Battle Hall** with five repeatable rival-pair double battles: Jessie/James; Steevee/Neevee; Green/May; Silver/Wally; Blue/Brendan.
- Add replayable Ultimate Gym partnerships; no unsupported assumptions that two opponent parties of six each work without multi-trainer engine changes.

## Current changes in this PR (scope 1)
- **PRU PRE-TEST CODED, CI QA PENDING:** Elm's original three ball objects replaced by three visible fossils (Helix, Dome, Old Amber). He now gives Level 5 Pikachu automatically; no choice, no Yes/No and no overworld ball object disappears. `VAR_STARTER_MON=0` remains intentionally locked for Silver's rival team.
- Elm and first-visit Oak text integrate Resonance, fossils and Johto-first archaeological continuity; Ruins researcher responds to real Crest/Relic Ho-Oh flags. Formal live-branch audit: `docs/PRU_STANDALONE_RELIC_DIALOGUE_AUDIT.md`.
- **User-set next priority AFTER point 1:** new PRU title screen in a Relic cave featuring latest PRL Noxichu; seek donor animation, use original PRL Jirachi/Celebi sequence only if no suitable new donor; replace older Noxichu art references in all GBA asset paths.
- **Approved early-starter policy supersedes older locations:** all 9 traditional starter stages and 3 PJR starter stages are available no later than Route 33 / early Union Cave / Slowpoke Well, all wild at level 2–9, with no Surf requirement. Day/night variants contain the same starter where available. These are catchable before their Lv14–18 evolutions, not late-game gifts.
- Chikorita Route 29 Lv2–3 (5%); Cyndaquil Route 30 Lv4 (5%); Totodile Slowpoke Well B1F Lv6–8 (5%); Bulbasaur Route 31 Lv5 (5%); Charmander Route 46 Lv2–3 (5%); Squirtle Route 32 **grass** Lv6 (5%); Treecko Route 30 Lv3–4 (4%); Torchic Route 33 Lv8–9 (5%); Mudkip Union Cave B1F Lv8 (5%).
- Scarabub Route 31 Lv5 (4%), evolves to Heracross at Lv18; Skarmet Route 46 Lv2–3 (4%), evolves to Skarmory at Lv18; Mootiny Route 29 Lv2–3 (4%), evolves to Miltank at Lv18. All three donor evolutions verified from `src/data/pokemon/species_info/pjr_families.h`.
- **Later evolved replacements:** Burned Tower Charmeleon Lv16–18; Route 41 Wartortle Lv22–25; Route 34 Grovyle Lv17–18; Route 37 Combusken Lv17–18; National Park Heracross Lv18; Route 45 Skarmory Lv37; Route 39 Miltank Lv21 (no Mootiny); deeper Slowpoke Well Croconaw Lv20–22; deeper Union Cave Marshtomp Lv21–23. Original Bulbasaur in Ilex Forest and Cyndaquil on Route 36 remain additional low-level opportunities; Totodile and Mudkip remain at their original early cave sources.
- Porygon remains catchable on Route 10 and Castform on Route 42. All inserted starter-stage encounters use existing PJR wild encounter slots; no gift conversion beyond the Pikachu opening yet.
- Main HNS encounter baseline before targeted inserts contained 165 unique maps / 257 encounter variants; 265 of the original 386 were directly present in at least one HNS wild table. The other 121 mostly require evolution or static/legendary audits. This is **not** a claim that all 386 were already obtainable.
- **As currently coded in this branch:** Violet/Azalea/Goldenrod aides presently give wild-location clues rather than gifts. Elm's post-League alternative starter Eggs are presently disabled. **Current user decision supersedes these earlier no-gift assumptions**: audit all gifts and reinstate/replace gifts deliberately with rarer appropriate Pokémon, never gift-exclusive. Preserve Togepi Egg.
- **Elm Togepi Egg preserved by user request:** keep `VioletCity_PokemonCenter_hns/scripts.inc`'s `giveegg SPECIES_TOGEPI`, Elm/Kimono story dialogue, `FLAG_RECEIVED_TOGEPI_EGG`, original hatching/return progression and Mr. Pokémon's separate Mystery Egg key item as PJR currently implements them. This exception is final; **do not redesign or remove the Togepi gift**.
- **No claim yet that all gifts are removed.** Run comprehensive Pokémon-grant code search throughout other events, game corner, restoration, and trade endpoints. Master all-species import is not complete.

## Required gates BEFORE a playable declaration
1. Workflow `PJR Beta build` succeeds on this feature branch/PR.
2. Emulator fresh-save: Oak intro -> New Bark -> Elm's lab. Inspect all pages for textbox overflow.
3. Verify that Elm gifts **exactly one Pikachu**, that no offer/choice appears, and that all three fossil displays are visible but not gifts. Verify cry, battle sprites, icon, nickname and PC deposits.
4. Finish Mr. Pokémon / Silver / police theft / Elm return; ensure visible balls and flags remain coherent, and Route 30 opens.
5. Audit all gift/trade/static species awards; retain original Togepi/Mystery Egg and flags/dialogue. Gifts are permitted but redundant traditional-starter gifts should become rarer, sensible choices; separate independent obtainability required.
6. Reconcile every custom donor: distinguish species, form, shiny palette, trainer-only form, superseded design. Do not allocate final PJR species IDs without the resolved registry.
7. Audit `src/data/wild_encounters.json` (approximately 2 MB): first 14 species insertion completed by exact slot, but validate every day/night/surf/fishing table, rarity, DexNav and swarms in an emulator. Do not claim the entire National Dex is implemented.
8. Ensure all 444 approved species have an independent catch/evolution/legendary event chain, including #001–#386 originals; optional gifts are in addition to independent paths.
9. Test championship and Trainer Card progression with fresh saves; no persistent level mutation from battle cap.
10. Check final GBA ROM size, battle graphics/icon/palette pipeline, and save version/migration.

## Early and evolved encounter audit — committed; emulator pending
- Canonical map/level/location rules are the early-start policy above. No new PJR geography or Surf dependency for a starter-stage Pokémon.
- Encounter-table change `078310b5` replaces 32 variant slots. Every displaced original species remains available in at least one other slot in that same variant; this was checked before committing.
- GitHub compilation verifies source integration only. Fresh-save playtesting must check early access, wild catch rate, progression and evolved-stage availability; do not equate a successful build with in-game success.
- Any further Pokémon encounter pass must preserve this early starter availability as a regression gate.

## Deferred Kanto gameplay TODO — requested 18 October 2026

**STATUS: BACKLOG ONLY — do not implement during the current Johto-wide trainer and encounter difficulty rebalance.** Complete/verify the Johto curve first; preserve existing PRU story, sprite, evolution and credit work.

- [ ] **Kanto roaming legendary birds:** Articuno, Zapdos and Moltres should independently roam randomly throughout appropriate Kanto outdoor routes as true roaming encounters, rather than being restricted to stationary encounters. Audit the inherited roamer engine for three simultaneous active roamers and ensure roaming movement, encounter probability, Pokédex/map tracking where supported, capture/defeat persistence, re-encounter rules and any existing legendary story flags are compatible. Choose the Kanto access/unlock point during implementation; do not assume existing story encounters can be removed without a continuity audit.
- [ ] **Kanto wild encounter species should fit their levels:** audit Route 1 and all Kanto areas, replacing implausibly high-level unevolved wild Pokémon with their suitable evolutions. Example: a high-level Pidgey should generally be Pidgeot (or Pidgeotto at an appropriate lower level), and a high-level Rattata should generally be Raticate. Set stages based on evolution rules, encounter levels, location ecology and the player's post-Johto progression; retain appropriate opportunities to obtain earlier evolutionary stages elsewhere so the 444-species acquisition plan remains viable.
- [ ] Validate Kanto day/night, grass, Surf, fishing, Rock Smash, swarm and special encounters without accidentally replacing required unique species; check encounter difficulty and story progression in an actual compiled ROM and emulator. Keep Kanto work separate from the active Johto rebalance.

## Evidence
- `data/maps/NewBarkTown_Lab_hns/scripts.inc`: Elm, starter gift, Silver theft and multiple later Egg gift flows.
- `data/maps/PokemonLeague_WillsRoom_hns/scripts.inc`: original, Johto Champion rematch and post-Sinjoh rematch branches.
- `data/maps/PokemonLeague_ChampionsRoom_hns/scripts.inc`: Lance original/rematch and separate championship dialogue.
- `FEATURES.md`: 16 Gym rematches, Gen 1–9 species support, Nuzlocke-only infinite Rare Candy option and current Hoenn encounter audio system.
