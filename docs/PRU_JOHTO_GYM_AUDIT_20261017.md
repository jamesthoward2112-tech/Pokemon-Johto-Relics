# PRU Johto Gym Leader Audit & Rebalance — 17 October 2026

Active implementation: `src/data/trainers_hns.party`, branch `pru/noxichu-last-wish-title-test-20261017`.
Source base: verified PJR teams from `pjr-rebuild`. This commit rebalances the FIRST-BATTLE, conditional badge-order variants, ordinary rematches, and post-Orange-Battle-Centre rematches while retaining the Johto story and known NPC events.

## First encounters (order and exact roster)

| Leader | First fight (ordered) | Distinctive Relic / new species |
|---|---|---|
| Falkner | Hoothoot 12; Natu 13; Skarmet 14; Pidgeotto 16 | Skarmet (Steel/Flying) |
| Bugsy | Pineco 18; Ledian 19; Spinarak 19; Scarabub 20; Scyther 22 | Scarabub (Bug) |
| Whitney | Clefairy 23; Teddiursa 24; Aipom 24; Mootiny 25; **Miltank 27** | Mootiny + classic Miltank ace |
| Morty | Haunter 29; Misdreavus 30; Sableye 30; Maroghost 31; Gengar 33 | **Stantler removed**, Maroghost (Ground/Ghost) added |
| Chuck | Hitmontop 34; Primeape 35; Pinsir 36; Heracurion 37; Poliwrath 39 | Heracurion (Bug/Fighting) |
| Jasmine | Skarmory 38; Magneton 39; Scizor 40; Skarmadon 41; Steelix 43 | Skarmadon (Steel/Flying); Corsola removed |
| Pryce | Dewgong 34; Sneasel 35; Jynx 35; Jollibird 36; Piloswine 38 | Jollibird (Ice/Fairy); alternate 5/7-badge tiers gain Mystynx |
| Clair | Dragonair 47; Gyarados 48; Lapras 48; Mawyrm 49; Shelgon 50; Kingdra 52 | **Dudunsparce removed**, Mawyrm (Steel/Dragon) |

**Badge-order scaling retained:** Chuck, Jasmine, Pryce each have their explicit existing alternate battle IDs updated instead of flattening their level variants. Eight ordinary post-League rematches and seven later rematches are preserved with appropriate Relic replacements.

## Current badge reward audit — already present in map scripts

Each listed Gym already grants **10,000** bonus cash, a TM, and one special item using PJR's `FLAG_PJR_GYM_REWARD_*` guards, in addition to the badge.

| Leader | TM | Held/evolution item |
|---|---|---|
| Falkner | Roost | Sharp Beak |
| Bugsy | U-turn | Silver Powder |
| Whitney | Return | Eviolite |
| Morty | Shadow Ball | Spell Tag |
| Chuck | Focus Punch | Black Belt |
| Jasmine | Iron Tail | Metal Coat |
| Pryce | Hail | Never-Melt Ice |
| Clair | TM59 | Dragon Fang |

Clair's TM/item each have independent receipt flags. Seven other gyms give the TM in the main badge conversation and run the cash+item through a recoverable reward routine. **Open QA**: make the TM retry-safe for an entirely full bag; as currently coded, a failed initial `giveitem` may not be retried by the defeated-Leader dialogue. Keep reward flags save-stable and avoid duplicate payouts.

## Gameplay QA still required

- Compile with `make hns` and `trainerproc`; no success claim until Actions finishes.
- Start clean and check exact first-fight roster and battle difficulty/EXP compared with available encounters and repeated Chansey training.
- Check Scarbub/Skarmet/Mootiny/Maroghost/Heracurion/Skarmadon/Jollibird/Mystynx/Mawyrm have working battle graphics, cry, abilities and legal moves.
- Test badge-order variants of Chuck, Jasmine and Pryce.
- Test all 8 badge + TM + item + 10,000 rewards, including full bag and repeat interaction.
- First league rematches and later postgame teams need emulator QA; static source presence alone is not a pass.
