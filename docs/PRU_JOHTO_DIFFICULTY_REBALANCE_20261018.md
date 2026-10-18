# Pokémon Relics Ultimate — complete Johto difficulty rebalance (18 October 2026)

**Source branch:** `pru/johto-full-rebalance-20261018`  
**Base:** latest Valkiri/RelicDex/Throat Spray source branch `pru/prl-sprite-position-icons-tm-20261018` at `6c1275b6f453e3a2d2d10dab321da3c1709f1788`.  
**Implementation:** `src/data/trainers_hns.party` and `src/data/wild_encounters.json`; no savedata structs, species IDs, flags, or credits changed.

## Actual source changes

- Rebalanced first-battle levels for **202 individual Johto trainer parties**: Routes 30–45, 47, 26–27, Sprout Tower, Union Cave, Slowpoke Well, Ilex Forest, Goldenrod Underground, National Park, Burned Tower, Olivine Lighthouse, Mt Mortar, Lake of Rage, Rocket Hideout, Goldenrod Radio Tower and Rocket Underground, Dragon's Den and non-boss Gym trainers. **35 would-be reductions on already powerful Pokémon were rejected**; previously strong trainer parties retain their higher original levels.
- Rebalanced wild land / Surf / Rock Smash level tables on **37 distinct Johto map constants and 63 day/night encounter variants** (2050 level fields). Where these updated land encounters reached a known ordinary level-up evolution threshold, **145 encounter slots** now reference an appropriate evolved species instead of a dramatically overlevelled unevolved stage. Day/night encounter species otherwise remain geographically in place; rods are not blindly changed because different rods have different progression access.
- Preserved early Route 29–33 starter/Relic availability, original Gym Leader first battles, variable Chuck/Jasmine/Pryce challenge variants, special boss fights, rematches, Chansey training, custom evolution mechanics and PJR/PRL attribution.
- This change affects **future battles/wild encounters** on existing saves; defeated ordinary trainers do not automatically reset. It does not mutate a player's party or already-caught Pokémon.

## Progression targets

| Chapter | Ordinary trainer level progression | Nearby wild land progression |
|---|---|---|
| New Bark/Violet | Route 30: 5–8; Sprout Tower: 8–12; Violet assistants: 12–15 | Preserve early Lv2–9 catchable starters |
| Azalea | Route 32: 12–17; Union Cave: 14–25 by floor; Azalea assistants: 18–21 | Keep pre-Azalea early-source catchability |
| Goldenrod | Route 34: generally 19–24 (pre-existing stronger trainers kept); Underground: 21–25; Whitney assistants: 22–26 | Route 34: 16–22 |
| Post-Whitney | Route 35: 24–28; National Park: 25–29; Route 36: 25–29; Route 37: 28–32 | Route 35: 21–27; National Park: 22–28; Route 37: 24–29 |
| Ecruteak/Olivine | Burned Tower: 28–32; Morty assistants: 29–32; Routes 38–41 and Lighthouse: roughly 30–39 | Route 38–39: 27–33; ocean: 30–36 |
| Cianwood/Mahogany | Cianwood assistants: 34–38; Lake of Rage: 33–39; Rocket Hideout: 34–41; Mahogany assistants: 34–38 | Route 42–43: 28–37 |
| Goldenrod Rocket return | Radio Tower: 36–43; Rocket Underground: 35–42 | No unrelated encounter redirects |
| Blackthorn | Route 44: 39–45; Route 45: 43–48; Blackthorn assistants: 46–51; Dragon's Den: 48–53 | Route 44: 36–43; Ice Path: 38–46 |
| League approach | Routes 26–27: 47–53 | Routes 26–27: 44–51; Johto Victory Road 44–50 |

**User QA context:** At National Park, the older vanilla-scale trainers were level 15–20 despite Whitney being 23–27 and Morty 29–33. New National Park trainer floors are 25, and the new wild grass floor is 22.

## Engineering/verification status

- **Coded and committed** in source. Dedicated regression script: `tools/pru/check_johto_rebalance.py`.
- Full `make hns` GitHub Actions build, compiled-ROM audit and mGBA boot must pass before calling this a verified ROM.
- **Gameplay QA outstanding:** saved-playthrough battles and wild rates (especially National Park contest), Route 36 early-access gating, Surf/rod ecology, first-encounter and repeat encounters, evolution stage catchability and full Johto chapter difficulty/EXP curve.
- **Kanto deferred:** Articuno/Zapdos/Moltres roaming and level-appropriate Kanto evolved wild species are recorded separately in `docs/PRU_MASTER_PLAN.md`; no Kanto ecology was intentionally rebalanced here.
