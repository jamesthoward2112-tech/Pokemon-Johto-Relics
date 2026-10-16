# PRU donor custom moves — compile-blocking integration backlog

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
