# PRU explicit compilation checkpoint

Checkpoint date: 2026-10-16
Branch: `pru/complete-selective-integration-20261016`

Trigger 1: compile the recovered 19-species/9-ability integration after repairing binary-corrupted species.h and duplicate AbilityHpHeal label, adding authentic PRL move records and initial Bleeding/Fear runtime wiring.

This is a **source build checkpoint only**. Do not describe it as emulator-tested or release-ready.

Outstanding: original AlteRed donor move definitions, Eevoboost and the special Lovely Bite/Shadow Fangs effects, Fear/Bleeding status presentation and all remaining integration QA.

Trigger 2: retry after binary-safe restoration of `src/pokemon.c` (source blob repaired), and full original PRL status-chance merge for 57 existing moves; capture first subsequent compiler error.

Trigger 3: verify central Pokemon source now includes the 19 species' real gfx, level-up and teachable tables; compiler should progress to source-authentic custom move requirements. Static PRL bleeding/fear percentages now imported for 57 standard moves.

Trigger 4 (2026-10-16): rebuild after fixing the exact run 38940072721 RGBA-colour-type failure for external donor PNGs. Four donor sprite packs are normalized in the temporary Actions checkout to indexed 4bpp using the pinned JASC palettes; inspect the next real compile blocker, not source-only checks. No emulator-test claim.
