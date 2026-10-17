# PRU explicit compilation checkpoint

Checkpoint date: 2026-10-16
Branch: `pru/complete-selective-integration-20261016`

Trigger 1: compile the recovered 19-species/9-ability integration after repairing binary-corrupted species.h and duplicate AbilityHpHeal label, adding authentic PRL move records and initial Bleeding/Fear runtime wiring.

This is a **source build checkpoint only**. Do not describe it as emulator-tested or release-ready.

Outstanding: original AlteRed donor move definitions, Eevoboost and the special Lovely Bite/Shadow Fangs effects, Fear/Bleeding status presentation and all remaining integration QA.

Trigger 2: retry after binary-safe restoration of `src/pokemon.c` (source blob repaired), and full original PRL status-chance merge for 57 existing moves; capture first subsequent compiler error.

Trigger 3: verify central Pokemon source now includes the 19 species' real gfx, level-up and teachable tables; compiler should progress to source-authentic custom move requirements. Static PRL bleeding/fear percentages now imported for 57 standard moves.

Trigger 4 (2026-10-16): rebuild after fixing the exact run 38940072721 RGBA-colour-type failure for external donor PNGs. Four donor sprite packs are normalized in the temporary Actions checkout to indexed 4bpp using the pinned JASC palettes; inspect the next real compile blocker, not source-only checks. No emulator-test claim.

Trigger 5: run fail-fast custom move registration check plus full HnS compilation after implementing all 25 source move names and metadata, native one-stage Eevoboost, and preserving provisional external secondary-effect limitations. If compile fails, inspect first exact error. This is NOT move-effect parity or emulator QA signoff.

Trigger 6: compile the 25 native move records and separately implemented original PRL signature effects, after repairing the sole previous linker error (BattleScript_AbilityHpHeal changed from private ':' to exported '::'). Include the cheap 25-move source checker; on success preserve ROM, symbols, SHA-256 and commit. No emulator claims until actual gameplay QA.

Trigger 7: compile the complete 25 donor-move integration and late canonical Kanto Ultimate evolutions (Arbok level 40 -> Adnokana; Weezing level 40 -> Cheauking, Thunder Stone -> Frytning). Prior run 38956023183 succeeded at commit 1493c0f5 before evolution links. Capture final artifact SHA256. Build success does not imply emulator-tested or original external move-effect parity.


## Pre-test opening/dialogue source build 1 (2026-10-16)

Build branch `pru/pretest-story-services-20261016` after Elm automatic Pikachu + three fossils, Crest-state dialogue, Oak Johto-first Kanto research, source scanner and title-plan documentation. Verify exact first failure if any and save the build artifact; **do not claim emulator gameplay success**. Preserve `pjr-rebuild` and original consolidated branch.


## Pre-test first-adventure and complete active-HNS inventory build 2 (2026-10-16)

Compile all latest **source changes** (fossils + Pikachu, Elm/Oak dialogue, 7-Relic/Ho-Oh flag-dependent scientist text, Bellchime no fabricated Crest/Alphoracle, Red Crest full-bag safe retry with normal Red rematches preserved), and verify expanded static gates `tools/pru/check_pretest_story.py`. Separate successful source inventory runner [38964424218](https://github.com/jamesthoward2112-tech/Pokemon-Johto-Relics/actions/runs/38964424218) enumerated 550 HNS maps and 663 keyword-matched dialogue lines with no tracked stale-wording hits; **not a full semantic or emulator audit**. Save final ROM SHA and CI errors, if any.


## Pre-test Relic story build 3 (2026-10-16)

The prior build [38964900754](https://github.com/jamesthoward2112-tech/Pokemon-Johto-Relics/actions/runs/38964900754) failed only because `tools/check_pjr_tintower_shortcut.py` still expected the old unsafe Crest/Alphoracle flag backfill from reachable TinTower 1F entrance statues. We kept the actual 4 wired statue coordinates and Rocket/Ho-Oh scenes but replaced the invalid test assertions with real-catch/real-item gates. Run complete original static checks and `make hns` again; do not confuse compilation with emulator QA.


## PRU Noxichu + Last Wish boot-title trial — 17 October 2026

Explicit GitHub Actions rebuild requested **after** the Red rematch script linking repair, commit `26fe000f22658ac25f33237bb5ff29588036533e`. Target branch: `pru/noxichu-last-wish-title-test-20261017`.

Build procedure: original Emerald intro -> PRL Last Wish Celebi/Jirachi scene -> black fade -> approved 240x160 Noxichu cavern title, separately animated flashing PRESS START. Use `tools/pru/build_noxichu_intro_trial.py` to patch the temporary runner checkout, then run `make hns`, and publish artifact `PRU-Noxichu-LastWish-TEST` with GBA and SHA-256. CI source/build green is not proof of emulator animation playback; test that separately.

This file is a configured push-path CI trigger: prior map-only Red fix did **not** match the workflow's push path filter, so this separate update forces a fresh build of the repaired head. Do not modify `pjr-rebuild`.


## 17 October — PRU Johto/Kanto title and legendary persistence compile retry

Build branch `pru/noxichu-last-wish-title-test-20261017` after source fixes for Hall of Fame/Champions Room. Source checks passed in run 39022869046 but make hns failed on incorrect doubled backslashes in newly added GBA dialogue at ChampionsRoom line 441. Corrected source in commits `b699f141` and `1f507eae`; strengthened `tools/pru/check_pretest_story.py` with literal-backslash validation and the first Silver battle. Verify build and ROM artifact, not just static checks. This is a new build of the title-approved Last Wish-only PRU test variant; no Gengar or Emerald animations. Preserve legacy `pjr-rebuild`.


## 17 Oct PRU gift inventory

Run live HNS and donor map-script gift audit for Chikorita, Torchic, Mudkip and Treecko before selecting balanced replacement NPC gifts. Print source paths/lines; follow with specific changes on this preserved title/story branch.


## 17 October — nurse-side Chansey doubles CI regression

Trigger source + full HNS ROM build after 21 two-Chansey per-centre teams were appended (levels 7–100) and nurse-side NPC interactions routed to level-specific labels. Specific fix `cc998283768519f0f1b776c7a02146ca7a859dfb`: all 21 battle entry points now use `trainerbattle_double` with built-in insufficient-usable-party handling, append-only trainer IDs 654–674, `cleartrainerflag` on each interaction to ensure rematches, and 0 prize-money payout (EXP-only). New source assertions are in `tools/pru/check_pretest_story.py`. Retain user-approved Last Wish → Noxichu title, do not re-add Emerald/Gengar. Also inspect GIFT_SPECIES_SCAN output to find live Chikorita/Torchic/Mudkip gift events; no blanket replacements until event scripts identified.


## 17 Oct PRU repeatable nurse-Chansey & rare gifts build

Explicit full runner rebuild requested after nurse-side Chansey double tiers in 26 centers, trainerproc-safe 21 trainer records, corrected `trainerbattle_double` encounter handling and source checks. Violet rare Ralts gift replaces misleading Chikorita clue; Steven now offers Treecko/Beldum/Bagon in Silph Co with full PC retry. Run `tools/pru/check_chansey_training.py` and `tools/pru/check_rare_gifts.py` before compile and report independent wild encounter coverage. Preserve approved Last Wish + Noxichu title. Deliver verified direct .gba, not GitHub link.


## 17 October — trainerproc separator repair and current rare gift + doubles build

Rebuild after `f0e8833041bfc78178268b35757e20ca0408b238`, removing the unsupported mid-file C-style comment between the last PJR trainer party and the 21 PRU Chansey doubles parties. Source tests now expect the actual `trainerbattle_double` command and usable-party checks. Include live Violet Ralts replacing former Chikorita, Saffron Steven Treecko/Beldum/Bagon gift choice, and approved Last Wish-only Noxichu title. A previous run failed while reading the additional trainer.party records; do not distribute a ROM unless new compile completes.


## 17 October — direct Chansey portrait + Breeding Centre move expert rebuild

Rebuild after restoring exact 64×64 indexed two-nurse Chansey sprite at `assets/pru_chansey/twins_front_64.png.b64` (SHA256 55452b964a24dc7cd5098f90ca2bba69325c1c8a9d381ddb4a5824e0e681267b), dedicated trainer pic, 'Chansey wants to train!' native battle intro, and Route34 Day-Care Egg/Tutor move expert. Preserve Last Wish → Noxichu title. Before claiming tested: verify successful full hns linker + emulator intro and move selection; package direct .gba.


### Retry after trainer intro source-control-character fix

CI run `39029394627` failed because the newly introduced battle message mistakenly used a doubled `\\p` escape. Corrected in commit `4ea97bdd3fa658df3002ef1bb06b41b3810e60fa` to one GBA `\p`, and the separate palette asset SHA validation has passed. Re-run all source + linker steps against this HEAD.


### Retry after fixing Day-Care text escapes

CI run `39029526816` passed PNG asset checks and battle-message compilation but failed in `Route34_DayCare_hns/scripts.inc` because new NPC text incorrectly had doubled control backslashes. Commit `1157d5eacb2f90655531372932a69a59c34dd5d9` corrected nine instances to GBA-compatible single `\n` / `\p` escapes. Rebuild the approved title+Chansey+Breeding Centre ROM now.


### Route 30 Poochyena and Chansey training regression rebuild (17 Oct)

Following user emulator QA, retain repeatable twin Chansey battles in nurse-side
Pokémon Centre NPCs. Replace orphan “Chaan! Sii!” text with the yes/no
“CHANSEY wants to train!” script; use single GBA control escapes (CI run
39032035606 had failed because of doubled escaping). Include Route 30 low-level
Poochyena (Lv3–5), applied by tools/pru/add_route30_poochyena.py before compiling.
Do not distribute until an hns build passes. Preserve Noxichu/Last Wish title,
Chansey portrait and Route 34 Egg/Tutor NPC.

### Full nurse-side Chansey map sweep (17 Oct)
GitHub Actions must scan every existing Chansey overworld object, not just the curated 26. Fail early and print any unexpected map-to-script links before running the expensive ROM compiler.
