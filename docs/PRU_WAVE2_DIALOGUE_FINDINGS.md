# PRU dialogue audit — recovery wave 2 (16 October 2026)

Status: **source inspection and complete registered-HNS text inventory completed; dialogue edits / semantic sign-off still pending**.

## Recovered checkpoint

- Working PR: #6 on `pru/ultimate-pokedex-encounters-20261016`; base `pjr-rebuild`.
- Original PJR branch and PRL / PKR 2.0 work remain separate.
- GitHub Actions now executes `tools/audit_pru_standalone_dialogue.py` and uploads `PRU-Dialogue-Audit` on each PRU build.
- First actual CI scan: **545 registered HNS maps**, **662 HNS/shared .inc files**, **465 review matches** (not defects). Categories: prior-game text 0, transfer 4, starter 5, timeline 123, relic-lore 94, gift text 135, event/flag lines 104.
- 11 registered Contest Hall / Unused Contest Hall maps have no local .inc script files. These are missing **local scripts**, not evidence of missing maps or player dialogue; inspect objects/map events before marking a blocker.
- This inventory excludes unregistered FRLG/Emerald donor maps (correct for the active PJR HNS build). Shared text is reported separately because it may or may not be reachable.

## Source-confirmed grants that need policy work

The player's only approved starting gift is Pikachu. Elm's existing, story-critical **Togepi Egg is explicitly retained**. No other optional Pokémon gifts should remain, but do not remove a grant before its acquisition alternative and event flag have been checked.

| Live/map source | Current source behaviour | PRU action | Gate |
|---|---|---|---|
| `SaffronCity_SilphCo_hns/scripts.inc` | Steven offers Treecko/Torchic/Mudkip via `MULTI_HOENN_STARTERS`, sets `FLAG_GOT_HOENN_STARTER` | **Convert** to Johto/Kanto wild-location or Relic research guidance; preserve Steve(n) visit flow and one-time dialogue, retitle flag only if references safely migrated | Inspect `map.json` object flag, acquire all three in wild, no repeat/softlock |
| `CianwoodPokecenter_hns/scripts.inc` | Fisher can gift Lv25 Tentacool when player lacks Surf-capable party Pokémon | **Convert** to useful wild-location hint or non-Pokémon aid, without blocking required Surf progression | Verify HM-free Surf and fishing/wild Tentacool accessibility before removal |
| `DragonsDen_Shrine_hns/scripts.inc` | Elder gives Dratini, including `givenamedmon 4` on special quiz path | **Design replacement** for the gift that preserves Elder's approval, Dratini family access and quiz-result distinction | Test both quiz branches and flags; do not erase Dragon's Den story |
| `MtMortar_B1F_hns/scripts.inc` | Karate King gives Tyrogue after his battle | **Convert** reward/dialogue to training/clue and provide actual wild Tyrogue encounter | Check Kiyo event and `FLAG_GOT_TYROGUE` |
| `NewSinjoh_House1_hns/scripts.inc` | Elizabeth gives Paldean Wooper after being shown Celebi | **Convert** to regional-variant lead or non-Pokémon recognition, with separate capture access | Keep Celebi recognition and original Sinjoh plot intact |
| `UlaUla_House_hns/scripts.inc` | Noibat Egg is awarded during Phant event | **Review playable/registered Alola scope**; retain storyline if map accessible, but remove optional Egg only after replacement acquisition | Test transition/sidequest and Noibat acquisition |
| `data/scripts/gift_pichu.inc` | Mystery Gift event awards special Surfing Pichu Egg | **Reachability check**: not an ordinary overworld gift; do not delete a detached event merely on regex match | Confirm hook, flag and approved Mystery Gift scope |

## Explicit non-equivalences — DON'T bulk delete

- `RuinsOfAlph_Lab_hns/scripts.inc`: Lileep, Anorith, Omanyte, Kabuto and Aerodactyl are **fossil revivals**; those commands are part of fossil restoration, not unconditional free gifts. Determine fossil acquisition/revival policy before any change. **Never touch the Ruins' R-E-L-I-C-S / Alphoracle capture flags as collateral.**
- `GoldenrodCity_GameCorner_hns/scripts.inc`: coin-funded Pokémon prize exchanges are *purchases*, not unsolicited gifts. Keep pending specific Game Corner policy.
- `SafariZoneGate_SafariZoneEntrance_hns/scripts.inc`: `..._EventScript_Test` contains four `givemon` lines. `Route25_BillsHouse_hns/scripts.inc`: `Route25_BillsHouse_Test` contains five more. These are **test labels** and must be verified against map objects and references before being called obtainable grants.
- `data/scripts/debug.inc`: debug-only gift commands do not imply gameplay access.
- `VioletCity_PokemonCenter_hns/scripts.inc`: Elm's Togepi Egg is the intentional protected exception; do not modify it.

## Core Johto / Kanto narrative — second verification

1. `GoldenrodCity_RadioTower_5F_hns/scripts.inc`: Archer explicitly abuses Alph Resonance and describes Rocket disbanding afterwards. **Locked**: a later PRL Giovanni/Silph Rocket takeover cannot be transplanted intact. Preserve PJR's actual `TohjoFalls_GiovanniRoom_hns` event and its three-year Rocket background; distinguish this encounter from PRL's earlier Kanto episode.
2. `RuinsOfAlph_Lab_hns/scripts.inc`: first Hall of Fame flag gates the sequential six catches, then Alphoracle; failures allow later retries. `TinTower_RoofDay_hns/scripts.inc` checks all six, Alphoracle and Ancient Rainbow Crest before Ho-Oh. **Locked**: Oak's separate legendary sidequests must not duplicate or reset them.
3. `PokemonLeague_HallOfFame_hns/scripts.inc`: original first Champion and a distinct Kanto rematch flag exist. **Not yet implemented**: four complete PRU championships, level caps, tiered replay text, Ancient Candy after championship two.
4. `PalletTown_Lab_hns/scripts.inc`: Oak currently discusses Kanto badges, Mt Silver and Pokédex progress. **Needed**: a new Johto-first Relic research dialogue branch using PJR live flags; not PRL's Kanto-first opening, badges theft, or Hoenn voyage.
5. `TinTower_RoofDay_hns/scripts.inc`: text already names HO-OH and explicitly recognizes the guardian. **Locked**: never copy PRL's dialogue treating it as an unidentified golden bird.
6. Steven is a *former Hoenn Champion* in PJR; that remains world lore. NPC references to Hoenn alone are **not** evidence that the player has already played PHR.
7. Current New Bark lab still contains internal legacy label names and dormant Scarabub/Skarmet/Mootiny starter-grant branches although only the left Pikachu Poké Ball is selectable. These are a maintenance and regression risk; remove or guard only after Silver's starter/theft path is mapped. **Do not accidentally grant three starters again.**
8. `README.md` and final title/credits are still donor-branded; PRU identity is not yet production-complete.

## Next implementation order

- [ ] Check map-object reference/reachability and all call sites for each Pokémon grant; produce source-level keep/convert/dead-code decisions.
- [ ] Add alternate wild/quest acquisition *before* removing live free-gift scripts.
- [ ] Finish donor cross-reference ledger for every approved Relic species, evolution, hint and accessible Johto/Kanto location; flag superseded PRL forms.
- [ ] Finish all active HNS dialogue scene sign-off, including radio, rematches, day/night, trainer gender, optional NPCs, terminal/PC, maps and late Sinjoh.
- [ ] Implement only lore-adapted Kanto reports, Old Rocket archives, Oak legendary leads, new flags and four-championship dialogue.
- [ ] Clean build and replay a *fresh* standalone save (starter to Kanto to RELICS/Ho-Oh to Sinjoh), verify overflowing text and all capture retries.
- [ ] Separate title/game code and ROM branding from PJR without breaking donor build/saves.

**Do not mark the full dialogue audit complete or call the ROM playable-approved while any of these gates are open.**
