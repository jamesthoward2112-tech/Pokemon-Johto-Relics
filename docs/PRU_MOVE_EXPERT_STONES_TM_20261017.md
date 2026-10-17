# PRU Move Expert, unified Ancient Stone, and TM/HM naming — 17 October 2026

## Scope and provenance
Branch: `pru/move-expert-stones-tm-labels-20261017`, forked from the verified but scene-QA-pending `pru/johto-rocket-trio-fix-20261017`. Preserve its approved Last Wish → Noxichu title, Jessie/James intro, Eevee twins, Rocket scene work, and donor credits. This does not alter `pjr-rebuild`.

User-playtest findings:
- Route 34 Day-Care Move Expert produced “No more moves of this kind” even for Bulbasaur. Egg and Tutor functions were wrongly gated on global relearner unlock settings. Removed just those two access checks; species-specific move legality checks remain. Egg/Tutor move teaching needs gameplay verification.
- Goldenrod big department-store Mart lacked Moon Stone and newly imported Ancient Stone. They are now stocked.
- Seven PJR bespoke catalysts (Ancient Shell, Fossil Bark, Ancient Tusk, Frost Mirror, Ancient Horn, Ancient Plume, Ancient Bell) are no longer required for evolutions and are no longer sold in the big Mart. **The item IDs and definitions remain to avoid changing item numbering and breaking existing saves.**
- All 59 genuine TM/HM item names now display the move name (e.g. FOCUS PUNCH, DRAGON CLAW, CUT), not numeric labels; TM CASE is unchanged.

## Authoritative evolution policy
**Apply an Ancient Stone to a compatible Pokémon only at Level 45 or above.** These are item-use evolutions, NOT level-up-triggered or hold-item-triggered evolutions. `IF_MIN_LEVEL` was appended to EvolutionConditions and evaluated against `MON_DATA_LEVEL`. Eeveeon's existing Eevee → Eeveeon Ancient Stone method is deliberately unchanged, since the user's new rule applies to *Relic evolutions*, not Eeveelutions. Weezing → Frytning via ordinary Thunder Stone remains unchanged, and vanilla/other Eeveelution stones are unchanged.

| Family | Evolution |
|---|---|
| Jynx | Mystynx |
| Arbok | Adnokana |
| Weezing | Cheauking |
| Meganium | Faeranium |
| Typhlosion | Pyroclast |
| Feraligatr | Feralodon |
| Sudowoodo | Sudowarden |
| Qwilfish | Kablowfish |
| Shuckle | Shuckolosse |
| Heracross | Heracurion |
| Skarmory | Skarmadon |
| Donphan | Donphalanx |
| Miltank | Miltitan |
| Gardevoir | Valkyvoir |
| Sceptile | Sceptitan |
| Blaziken | Solaziken |
| Swampert | Swamplith |
| Mightyena | Skulberus |
| Sableye | Gemigoyle |
| Mawile | Mawyrm |
| Torkoal | Torkaldera |
| Cacturne | Cactomb |
| Tropius | Tropisaur |
| Relicanth | Coelossus |

Charaxis belongs alongside these lines as the 25th intended level-45 Ancient Stone evolution, once its approved species assets are wired into PRU. The first 13 are PJR Relic lines (including two newer merged species). The remaining 11 are PRL Hoenn donor Relic lines already represented in PRU's species table but previously lacking accessible player evolution paths.

**Charizard → Charaxis is canonical, NOT an unknown species.** Charaxis is a genuine player-obtainable PKR Kantomon (PKR regional #153, original expansion species ID 908); PRU's approved 444-entry Pokédex lists **Charaxis as entry #008** immediately after Charizard, so its import should fill an already-approved entry, not increase the target to 445. The PRU 16 October sprite-source policy records approved Charaxis normal/shiny front and back art traced to the Pokémon Mercury Gigantamax Charizard sprite archive, with the separate approved party-icon source; preserve that exact design, not the vanilla Mega X/Y variants. The former PKR mechanic was Level 50+ with Sharp Beak on level-up. **Superseding PRU requirement: use an Ancient Stone on Charizard at level 45 or above; no held item.** Charaxis is a Fire/Flying Pokémon with Gale Wings, 120 Attack / 90 Sp. Atk / 125 Speed, and established signature learnset including Aerial Ace, Flame Charge, U-turn, Roost. Preserve donor data/credit and current approved art. **Implementation blocker:** PRU's engine currently lacks `SPECIES_CHARAXIS`, its playable SpeciesInfo, full battle sprite/cry/icon registration and evolution pointer, so adding only an `EVO_ITEM` link would fail compilation. Import the exact donor species and graphical records, confirm the 444-entry register mapping and validate in emulator before reporting the evolution playable.

## Tests / release caveats
- Source regression: `python3 tools/pru/check_relic_stone_services.py`, covering all 24 evolutions, item levels, Eevee/Frytning exceptions, seven retired catalysts, Mart stock, move gating and 59 TM/HM labels.
- Branch's existing `.github/workflows/pru-battle-port.yml` was extended for this branch, with all previously pinned title and duo assets and a source regression step.
- **Not gameplay-tested** until a compiled ROM is available. Verify Egg/Tutor lists on Bulbasaur, one new Relic evolution below and above Lv45, Ancient Stone consumption, old item refusal, Moon/Ancient shop stock and receipt, TMs in Bag and Mart, plus original Eeveeon and Frytning paths. This note does not certify those behaviours.
- Separate draft PR #10 has an alternative Rock Shop inventory; do not merge that older stock list without removing bespoke catalysts and adding Moon/Ancient Stone.
