# PRU donor custom moves — compile-blocking integration backlog

## Updated signature effects — 16 October 2026 (post-first CI trigger)

- Lovely Bite's native `MOVE_EFFECT_PRU_INFATUATION` is now wired into `SetMoveEffect`, checking opposite gender, Oblivious, Aroma Veil and already-infatuated status. It is applied at an independently specified 10% chance on the struck Pokémon, alongside the separate 10% Bleeding chance.
- Shadow Fangs now applies `MOVE_EFFECT_PRU_CURSE` on the struck battler at an independently specified 10% chance. This sets the existing native `volatiles.cursed` effect without the user's half-HP Ghost Curse cost, alongside separate 10% Bleeding.
- Both new effects have native battle scripts/messages. New source checker `tools/pru/verify_25_donor_moves.py` asserts all 25 data entries, the two distinct chance rolls and the new one-stage Eevoboost implementation.
- **CI timing:** these additional source edits occurred *after* first complete 25-move compilation was explicitly triggered. They are committed and need the next CI build and emulator testing. Only source registration is proven until those tests pass.
- Original donor effects for Procyon/Deneb and the approved but non-identical AlteRed compatibility names remain partial (see staging notes below).


## Source staging milestone — 16 October 2026 (UNVERIFIED BUILD)

- All 25 `MOVE_*` identifiers are now explicitly appended in `include/constants/moves.h`, and 25 native battle records are present in `src/data/moves_info.h`. The original PJR moves remain unchanged; Z/Max move ID offset and saved move-ID compatibility require a separate audit.
- `EEVOBOOST`: new `EFFECT_PRU_EEVOBOOST`, one stage to all five stats, targeting user with PP 5 and priority -2, implemented as an isolated native battle script without changing the original Extreme Evoboost Z-Move +2 effect.
- `LOVELY_BITE` and `SHADOW_FANGS`: authentic type/power/accuracy/PP/contact/biting and 10% Bleeding were registered. **Missing** original independent 10% Infatuation and 10% Curse respectively; not yet complete.
- Eighteen Procyon/Deneb-reference moves: original source-listed name/type/category/power/accuracy/PP included. **Effect parity NOT verified**. `INFECTION` temporarily uses poison, `NEUROTOXIN` uses bad poison, `STINK_SPRAY` lowers accuracy, `LIFE_DRAIN` heals 50%, and several attacks use normal damage. These are documented interpretations, NOT authenticated donor scripts.
- Four AlteRed names use explicit compatibility interpretations recorded in the approved `PRU_Donor_Gaps_Resolved_2026-10-16.md`; exact original secondary effects are not implemented. `TERROR_WAVE` retains verified 110 power/85 accuracy/5 PP as a ghost move; `SPARKLINGSKY` preserves Fire/200 power/5 PP and uses PJR native 50%-max-HP recoil (not source self-KO); `SUPER_GLITCH` uses Psychic typing as a pragmatic compatibility variant. `ASSIMILATE` is a Giga-Drain-style 75-power grass recovery move. All four preserve their **original move names** and must not be described as byte-identical imports.
- Reference for the 18 moves' base metadata: [Procyon/Deneb new moves](https://pokemon-procyondeneb.fandom.com/wiki/New_Moves), [Vega/Altair moves](https://pokemon-procyondeneb.fandom.com/wiki/List_of_Moves) (community wiki; original scripts remain mandatory for exact parity).
- **Important:** This is not a fully implemented original move pack. Do not close the checklist below until secondary effects, move animations, AI, status interactions and emulator QA are verified. No clean build is asserted from these commits yet.


Date: 2026-10-16
Source branch: `pru/complete-selective-integration-20261016`
Compiler: [GitHub Actions run 38951072549](https://github.com/jamesthoward2112-tech/Pokemon-Johto-Relics/actions/runs/38951072549)

**STATUS:** 25 move identifiers appear in the imported 19-species learnsets but have no current constant in `include/constants/moves.h`. This is the real failure after fixing the external donor RGBA sprite-format error.

The script `tools/pru/check_custom_move_registration.py` now fails immediately on these unresolved names rather than wasting full GBA compile cycles. This is a **blocking guard**, not substitute implementation.

## Three genuine PRL moves (original reference is pinned in this repository)

- [ ] `MOVE_EEVOBOOST` — authentic enum, data, original effect/animations and AI handling required
- [ ] `MOVE_LOVELY_BITE` — authentic enum, data, original effect/animations and AI handling required
- [ ] `MOVE_SHADOW_FANGS` — authentic enum, data, original effect/animations and AI handling required

Original records in `tools/pru/donors/prl_custom_move_records.reference.h`. Eevoboost is +1 Attack, Defense, Sp.Atk, Sp.Def and Speed (PP 5); PJR's older AdditionalEffect API requires an explicit exact handler. Lovely Bite has 10% Infatuation + 10% Bleeding; Shadow Fangs has 10% Curse + 10% Bleeding. Do not misrepresent vanilla battle-script effects as genuine.

## Four AlteRed-specific moves

- [ ] `MOVE_ASSIMILATE` — authentic enum, data, original effect/animations and AI handling required
- [ ] `MOVE_SPARKLINGSKY` — authentic enum, data, original effect/animations and AI handling required
- [ ] `MOVE_SUPER_GLITCH` — authentic enum, data, original effect/animations and AI handling required
- [ ] `MOVE_TERROR_WAVE` — authentic enum, data, original effect/animations and AI handling required

Source-of-truth library `PRU_Donor_Gaps_Resolved_2026-10-16.md` documents optional **non-identical fallbacks** (Terror Wave→Shadow Ball, Sparklingsky→Mind Blown, Super Glitch→Psystrike, Assimilate→Giga Drain) for a separate compatibility build. Those approved fallbacks have NOT been applied here. If used later, they must be visibly labelled as concessions, never described as exact source behaviour.

## Eighteen other external donor names — original effects need reconciliation

- [ ] `MOVE_ANGRY_SWARM` — authentic enum, data, original effect/animations and AI handling required
- [ ] `MOVE_CHROME_BALL` — authentic enum, data, original effect/animations and AI handling required
- [ ] `MOVE_CORNER` — authentic enum, data, original effect/animations and AI handling required
- [ ] `MOVE_DARK_RESOLVE` — authentic enum, data, original effect/animations and AI handling required
- [ ] `MOVE_DEADLY_TOXIN` — authentic enum, data, original effect/animations and AI handling required
- [ ] `MOVE_GRIMEBUSTER` — authentic enum, data, original effect/animations and AI handling required
- [ ] `MOVE_INFECTION` — authentic enum, data, original effect/animations and AI handling required
- [ ] `MOVE_LIFE_DRAIN` — authentic enum, data, original effect/animations and AI handling required
- [ ] `MOVE_METAL_BLAST` — authentic enum, data, original effect/animations and AI handling required
- [ ] `MOVE_NEUROTOXIN` — authentic enum, data, original effect/animations and AI handling required
- [ ] `MOVE_POSSESS` — authentic enum, data, original effect/animations and AI handling required
- [ ] `MOVE_QUICK_TURN` — authentic enum, data, original effect/animations and AI handling required
- [ ] `MOVE_SHADOW_CLAMP` — authentic enum, data, original effect/animations and AI handling required
- [ ] `MOVE_SMOGSCREEN` — authentic enum, data, original effect/animations and AI handling required
- [ ] `MOVE_SOULSHOCK` — authentic enum, data, original effect/animations and AI handling required
- [ ] `MOVE_STINK_SPRAY` — authentic enum, data, original effect/animations and AI handling required
- [ ] `MOVE_VENGEANCE` — authentic enum, data, original effect/animations and AI handling required
- [ ] `MOVE_VILE_VENOM` — authentic enum, data, original effect/animations and AI handling required

## Mandatory acceptance before next full GBA compile

1. Freeze PJR ordinary move IDs and audit shifted Z/Max dynamic offsets and save compatibility.
2. Retrieve original donor move types, damage, PP, accuracy, priority, targets, genuine status/effect scripts and animation data.
3. Append explicit moves to `include/constants/moves.h` and register real records in `src/data/moves_info.h`; no no-op placeholders.
4. Integrate supporting engine mechanics and status messages, verify against donor records and run `python3 tools/pru/check_custom_move_registration.py`.
5. Only then change `docs/PRU_CI_TRIGGER.md` to run the expensive compiler. A green compile is not an emulator pass.
6. Follow with species evolutions, encounter completeness, Mewsion event, Rock Shop staged merge and emulator QA.

All edits to `pjr-rebuild` and temporary Rock Shop warp branches remain forbidden.
