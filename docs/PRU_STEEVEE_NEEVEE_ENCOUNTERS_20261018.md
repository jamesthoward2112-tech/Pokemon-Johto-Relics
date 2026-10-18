# PRU — recurring Steevee & Neevee (18 October 2026)

## Four playable PRL trainer twin encounters

| Stage | Location | Double battle team | Source trainer ID (save-stable) |
|---|---|---|---|
| 1 | Johto Route 37, replacing Ann & Anne at x13/14 y29 | Eevee 30; Eevee 30; Espeon 31; Umbreon 32 | 675 |
| 2 | Johto Route 47, two new NPCs beside the existing couple (x83/84 y29) | Vaporeon 38; Jolteon 38; Flareon 39; Omeon 40 | 676 |
| 3 | Johto Route 44, x61/62 y13 before Blackthorn | Flareon 44; Omeon 44; Espeon 45; Umbreon 45; Toxeon 46; Nimbeon 47 | 677 |
| 4 | Kanto Route 3, x33/34 y3 past Pewter | Vaporeon 61; Jolteon 61; Flareon 62; Toxeon 62; Nimbeon 63; Eeveeon 64 | 678 |

- Both NPCs trigger the same **double battle** at each location; both have independent post-battle dialogue. Separate trainer IDs mean defeating one visit does not cancel another.
- Route 37 replaces two original map-script pointers, **not** the existing trainer party ID for Ann & Anne. Already-defeated Ann & Anne do not block the new appearance when loading an old save. Other vanilla route NPCs remain intact.
- The four imported PRL trainer IDs **675–678** remain numeric-stable, with readable location aliases in `include/constants/opponents_hns.h`; `src/battle_setup.c` already routes all four to `B_TRANSITION_EEVEE_TWINS`, whose artwork is supplied through the approved `assets/prl_duo_20261011.json` import and `src/battle_transition.c`.
- Existing `OBJ_EVENT_GFX_TWIN_HNS` side-by-side overworld actors are used without importing unapproved new overworld art. Their character identities are made explicit in first-, post-, and rematch dialogue.
- A dedicated source audit `tools/pru/check_steevee_neevee_encounters.py` checks every placement, trigger, save-stable alias, team level, and custom PRL transition reference.
- Full compilation and on-device encounter/playfield collision checks are still required; source placement coordinates are chosen beside established walking-path trainers but must be checked in emulator.
- Keeps Johto wild/trainer rebalance, the original 444 species roster, all pre-existing lore, gym, Rocket, Valkiri and donor credit work.
