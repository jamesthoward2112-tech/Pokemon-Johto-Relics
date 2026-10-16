# PRU consolidated donor and battle-engine port — hard requirements (16 Oct 2026)

**Status: isolated engineering branch / NOT a finished gameplay import or playable ROM.**
Base: `pru/full-relic-import-20261016` in `Pokemon-Johto-Relics`.
Primary donor: the approved latest PRL/PR108 source, `Pokemon-Relic-Legacy` commit `6ee9b984521ac6f2beaf995f771a726379e55c88`; verify it against current approved PR108 branch before importing.
External assets: PRU Canonical Data Library `PRU_AlteRed_Three_Locked_Donors_2026-10-16.zip`, `PRU_Cheauking_Adnokana_Full_Donor_20261016.zip`, donor data registry and approved art locks.

## User directive — no ability/move shortcuts

Port **PRL's custom battle moves, their original move effects, its custom abilities and their real engine triggers, and its Bleeding/Fear mechanics** together with the Pokémon. Do **not** substitute vanilla moves/abilities, merely copy names into enums, or remove the status systems to make the ROM compile. The newer PRL implementation must be adapted to PJR's battle engine rather than wholesale file replacement: PRL uses `BattleCalcValues` / `src/battle_set_effect.c` where current PJR uses a different earlier effect path.

### PRL move audit (21 battle moves + 1 support/sentinel, PJR source has none)

- `AMBER_BLADE`, `SUN_RITE`, `TECTONIC_TIDE`, `EPOCH_CRASH`, `RELIC_WISH`, `EDEN_BLOOM`, `SCORCHWING`, `BASTION_CANNON`
- `LOVELY_BITE`, `SHADOW_FANGS`, `RIP_AND_TEAR`, `EERIE_FOG`, `SEISMIC_SLAM`, `SOIL_DRAIN`, `BRAVADO`, `RAGING_SOULS`
- `IRON_FANGS`, `BEATDOWN`, `TAKE_FLIGHT`, `INSECT_IMPACT`, `EEVOBOOST`
- `RANDOM_TEACHABLE` is a supporting/sentinel symbol; validate engine usage and never pretend it is a user-selectable attack.

PRL sources: `include/constants/moves.h`, `src/data/moves_info.h`, `src/data/pokemon/level_up_learnsets/prl_custom.h`, `src/data/pokemon/teachable_learnsets/prl_custom.h`, plus animation/effect code, battle scripts, move tutor and evolution references as needed.

### PRL ability audit (16 named definitions missing from PJR)

`PIERCING_DRILL`, `DRAGONIZE`, `EELEVATE`, `MEGA_SOL`, `FIRE_MANE`, `SPICY_SPRAY`, `AURA_GUARD`, `ANCIENT_GROVE`, `SOLAR_DISCIPLINE`, `TIDAL_BASTION`, `ANCIENT_CORE`, `WISHMAKER`, `EDENS_CANOPY`, `THERMAL_WINGS`, `CITADEL_SHELL`, `STYGIAN_RUSH`.

PRL sources: `include/constants/abilities.h`, `src/data/abilities.h`, `src/battle_util.c`, and whichever other trigger paths implement the abilities (on attack, switch-in, damage, weather, end turn, healing and UI). Audit the ability triggers and immunity rules, *not just their names and descriptions*. Preserve existing PJR ability IDs and allocate new non-colliding values with save migration review. PJR and PRL may differ in `ABILITIES_COUNT` and enum layouts; do not copy numeric IDs blindly.

## Bleeding — actual PRL mechanics

Verified in the approved PRL branch:
- Nonvolatile `STATUS1_BLEED` uses bit `(1 << 13)`, included in `STATUS1_ANY` and `STATUS1_DAMAGING`.
- Move secondary effects cause Bleeding at their original per-move percentage; source has a broad range of cutting/biting/piercing moves, not only custom attacks.
- End-turn damage is **max HP / 16**, with the PRL `BattleScript_BleedTurnDmg` and matching messages. Validate minimum-1 damage and interactions with fainting, immunity, moves, cures, switching, abilities, Substitute and battle save/status serialization.
- PRL `CureBleedWithHealingMove` clears it when an appropriate healing move is used. Import effects through the correct PJR event/status handler. Ensure normal healing items and Pokémon Center have appropriate behaviour, tested in game.
- Respect the approved **red BLD battle status icon** where available. Inspect PRL art/icon assets; lack of a compiled original is a UI task, not a reason to drop the mechanic.

Relevant PRL files: `include/constants/battle.h`, `include/battle.h`, `src/battle_set_effect.c`, `src/battle_script_commands.c`, `src/battle_util.c`, `src/battle_end_turn.c`, `src/data/moves_info.h`, `src/battle_message.c`, `data/battle_scripts_1.s`, status UI/party screen and battle scripts declarations.

## Fear — actual PRL mechanics

- Volatile state: `VOLATILE_FEAR` / `fearTimer` is a **2-bit timer**, initially set to **2** in `HandleSetEffectFear`; decreases during end-turn processing and uses `BattleScript_MoveEffectFear` for feedback.
- While Fear is active, PRL's damage calculation applies a **1.5× multiplier to incoming damage** and its escape check blocks ordinary running.
- Port every PRL Fear-inflicting move and original proc chance, including `SCARY_FACE`, `WORRY_SEED`, `NOBLE_ROAR` special handling where defined. Do not rerun their base effects or double-apply damage/statuses.
- Test prevention, cure/removal, switch-out, volatility resets, battle boundaries and messages; preserve saves.

## Eerie Fog and other linked mechanical behaviour

- Include `EERIE_FOG` as an actual PRL move and weather rather than a cosmetic text substitute. Its PRL move data uses `EFFECT_WEATHER`, weather `BATTLE_WEATHER_FOG`, eight turns, Ghost type; check additional weather interactions, abilities, overlays, duration and expiration.
- Current PJR already has generic Frostbite paths. Preserve them and reconcile PRL's differing `STATUS1_FROSTBITE` handling rather than reimporting conflicting constants. Review PRL's confusion self-hit chance and infatuation damage rules as existing project locks before final approval.
- PRL expands Bleeding secondary effects on standard moves (probabilities may be 3/5/10/15%). Port all actual data, not only moves learned by new customs.

## Pokémon integration sequencing / preservation

1. Audit **50 active PRL custom species** against the macro-defined *and* bracket-defined PJR species entries. **34 already exist**, **15 PRL species are missing**, with PRL's old `NUMEW` explicitly *superseded by new Mewsion* and **not imported**. Do not reuse any PJR numeric species ID (currently through 1623), or renumber existing saves.
2. Import 15 PRL missing species: `GEMLIN VALKYVOIR SCEPTITAN SOLAZIKEN SWAMPLITH SKULBERUS GEMIGOYLE MAWYRM TORKALDERA CACTOMB TROPISAUR COELOSSUS ASTRACHI EEVEEON NIMBEON`.
3. Import four external donors **Adnokana, Cheauking, Frytning, Mewsion** with their approved donor types, stats, authentic front/back/shiny sprites and icons. For AlteRed identity, Frytning is actual donor index 110 and Mewsion is the approved altered identity of Mewduo index 150; never copy similarly named unapproved donors.
4. Reconcile PRL's newly approved sprites/movesets/icons for existing Kanto species, Noxichu and Eeveelutions; **preserve existing PJR-exclusive Johto sprites and story**. Copy stat/move/ability differences only with an explicit per-species decision report.
5. Port approved Seviian Noibat/Noivern and Paldean Wooper/Clodsire regional variants from Radical Red (do not overwrite standard Noibat or ordinary Wooper). Preserve 444-entry Dex display order and do not treat forms or trainer-only graphics as new Dex species without approved mapping.
6. Port evolution conditions, level-up/TM/tutor/egg learnsets, cry data, menu icons and source checks; complete the encounter/evolution chain for every approved species. Preserve existing PJR first championship and early starter policy, including Elm's original Togepi Egg.
7. Add Mewsion's approved **Level 90 Cerulean Cave B2F** encounter at Mewtwo's previous tile **(8,14)**, after Mew and Mewtwo both registered CAUGHT and exit/re-entry of entire cave. Show the two-box dark-matter warning once per qualifying B2F entry. See issue #8.
8. Preserve Mew's original **Faraway Island Lv50** encounter reached with Old Sea Map; Vermilion truck is purely optional no-duplicate-Mew Easter egg.

## Required comparison and QA matrix

Produce machine-readable per-species report of: engine ID / display Dex number / source provenance / HP-Attack-Defense-SpAttack-SpDefense-Speed / primary and secondary types / all ability slots and *implemented trigger paths* / level-up-TM-tutor-egg moves and signature effects / evolution conditions and items / normal & shiny 64×64 front/back and 32×64 two-frame icon, palette indices / cries / encounters / one-save catchability.

Additional mechanic tests:
- [ ] Each of 21 real custom moves selectable, behaves as intended in battle, respects PP, targeting, animations, damage and secondary effects.
- [ ] Each of 16 custom abilities triggers as originally designed, works with opposing abilities and does not collide with PJR IDs.
- [ ] Bleeding can be inflicted by standard and custom cutting/biting attacks at source probabilities; red BLD icon, end-turn 1/16, cures, statuses, fainting/rounding tested.
- [ ] Fear 2-turn duration, 1.5× damage taken, escape prevention, stacking and cure behaviour tested in singles/doubles.
- [ ] Eerie Fog duration and overworld/battle weather rules tested; existing Frostbite intact.
- [ ] Level-40 Cheauking branch does not make Thunder Stone Frytning unavailable.
- [ ] Clean and existing-save emulator tests, event/legendary gating, Johto first league, title/intro, move relearner, storage, party and save/reload.
- [ ] One consolidated PRU build from CI, `make hns` fully passes, ROM size/graphics verified, emulator screenshots/videos or scripted runs retained.

**No completion claim** until these checks pass. This document is an implementation gate, not a claim mechanics have been ported.
