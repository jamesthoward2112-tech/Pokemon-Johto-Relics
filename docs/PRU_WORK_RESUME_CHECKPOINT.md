# PRU Work Resume Checkpoint

## 18 October 2026 — 444-species source registration and summary numbering audit

- **Branch:** `pru/444-species-dex-audit-20261018`, stacked on draft `pru/move-expert-stones-tm-labels-20261017` (PR #14). **Draft PR #15**: https://github.com/jamesthoward2112-tech/Pokemon-Johto-Relics/pull/15
- **Source verified:** all **444/444** entries from the approved 16 October canonical CSV have a unique `SPECIES_*` constant and a single registered SpeciesInfo record, with Castform/Deoxys aliases resolved. This is NOT a claim that all 444 have implemented encounter paths.
- **Bug/fix:** HNS summary originally used Johto Dex numbers before National unlock, giving no number for Grovyle, Mightyena and Gardevoir. Committed `src/data/pokemon/pru_dex_order.h` and an HNS-only `SpeciesToPokedexNum` 444 index with safe battle-only form fallback: **Charaxis #008, Grovyle #285, Mightyena #297, Gardevoir #318**.
- **GitHub CI:** `tools/pru/check_444_species_dex.py` added as a source assertion step to the consolidated full GitHub Actions HNS build; workflow also preserves base's Rocket/title and 25 Ancient Stone evolutions. The **new ROM is NOT yet verified compiled**.
- **Remaining blocking tasks:** native HGSS Pokédex UI and seen/caught flag schema still use inherited National/Johto IDs, so the 444 entries are not separately tracked as registered/caught; separate real Seviian Noibat/Noivern variant implementation and approved sprites missing; legendary encounter event placement pending; in-game summary and icon validation pending. Do not overclaim all 444 as playable until these gates pass.
- **Preserve:** existing `CREDITS.md`, pinned donors, #14 fixes, Rocket scenes, Last Wish/Noxichu and original playable ROM builds. Detailed audit in `docs/PRU_444_SPECIES_SOURCE_AUDIT_20261018.md`.

## 17 October 2026 — Johto Rocket trio and PRL duo integration (build in progress)

- **Working branch:** `pru/johto-rocket-trio-fix-20261017`, based on the latest usable PRU checkpoint branch `pru/noxichu-last-wish-title-test-20261017`. Pinned authoritative PRL donor remains commit `6ee9b984521ac6f2beaf995f771a726379e55c88`; approved duo-intro asset pack comes from PRL branch `prl/approved-duo-intros-jj-finale-20261011`, blob `8e13a0133d2abe1687c9eb74d2cba7366ac8dc93`.
- **Rocket scenes committed:** Slowpoke Well B1F positions Jessie, James and Meowth from player coordinates, faces the trio correctly and exits north before fade/removal. Goldenrod Underground approaches from the correct side and Radio Tower 4F keeps Meowth synchronized. Existing story flags and ordinary wild Meowth remain unchanged.
- **Jessie/James committed:** existing HNS trainer/overworld assets remain intact; approved PRL Jessie & James BG0 intro art is checksum-unpacked in Actions and routed to all four PRU Jessie/James trainer IDs. Donor credit is preserved in `docs/PRL_JESSIE_JAMES_DONOR_CREDITS.md`.
- **Steevee/Neevee finding:** these are recurring human trainer twins in PRL, not Pokémon species. Their signature species Eeveeon (`SPECIES_EEVEEON=1637`) and Nimbeon (`SPECIES_NIMBEON=1638`) already existed in PRU and are already counted in the 444-species target, so no species IDs or Pokédex count changed. Existing definitions, learnsets and art were retained; the missing Ancient Stone → Eeveeon and daytime Sharp Beak → Nimbeon Eevee evolutions were restored exactly from PRL. Four donor trainer teams were appended as HNS trainer IDs 675–678 and routed to the approved Eevee Twins intro.
- **Ancient Stone dependency:** PRL's Ancient Stone item definition was imported because PRU had no equivalent evolution stone. It retains the donor name, description, evolution-stone behavior, price and standard Shiny Stone icon/palette reference; no acquisition event was invented.
- **Verified build:** regression-first commit `24373fc` failed as expected before implementation. GitHub Actions run [39070341757](https://github.com/jamesthoward2112-tech/Pokemon-Johto-Relics/actions/runs/39070341757) completed GREEN at source commit `3237ae9b0bbef5dc53ffffdd4db02ca2e37366d2`: all static checks passed, full `make hns` linked, compiled-ROM audit passed, and the ROM was executed in mGBA for boot/title evidence. ROM artifact `PRU-Consolidated-WIP` ID `12114644869`; direct link: https://github.com/jamesthoward2112-tech/Pokemon-Johto-Relics/actions/runs/39070341757/artifacts/12114644869. Artifact ZIP digest `sha256:e7379d77a843c2dcbba0767bcbb29c709cf634059c8b67d2fbeb889c4a1087ba`.
- **Untested/outstanding:** mGBA execution proves boot/title stability only. No save-state gameplay at the three Rocket scenes, custom duo transitions, Ancient Stone evolution, or Steevee/Neevee battles has been performed. Detailed wild/special acquisition events for the twins remain intentionally deferred because none are established for Johto in the pinned donor.

## 17 October — nurse-Chansey trainers and slightly rarer NPC gift choices

**Verified build result (17 October, latest):** GitHub Actions run `39025375071` at `d5383a76bb0a42f6bac080f6e8117a43d9480697` completed GREEN: Chansey / rare gift source checks and full `make hns` ROM compilation passed. Direct `.gba` unpacked from artifact `PRU-Noxichu-LastWish-TEST` (ID `12098471245`), 33,554,432 bytes; SHA-256 `68f220ed15390bafb91491e403b1eafabac0a6ef03fee58cce02d9e6decf0e3f` verified. Runtime gameplay checks for interactions/repeated doubles, trainer-party fullness, zero payout, gift retries and reachable wild encounter geography are still outstanding.



- **26 active nurse-side Chansey overworld sprites** now dispatch to repeatable Yes/No training prompts, each a **2× Chansey double battle** with two harmless training moves (Memento and Heal Pulse). No extra training NPCs or upstairs Pokémon Centre maps. Training levels grow from 7 in Cherrygrove, 12 Violet, 20 Azalea, 26 Goldenrod, 31 Ecruteak, 37 Olivine, 40 Cianwood, 44 Mahogany, 50 Blackthorn, to 60 Indigo and regional Kanto tiers 64–90, with level 95 Mt Silver/Sinjoh and 100 Battle Frontier. Same visual Chansey NPC can be challenged repeatedly using cleartrainerflag and trainerbattle_double. Added append-only IDs 654–674 (21 trainer sets), no PJR train IDs moved. `tools/pru/check_chansey_training.py` guards all assignments.
- **Actual NPC gifts rather than misleading aide descriptions:** Violet City's Elm aide's Chikorita clue/companion is now an optional one-time Lv8 Ralts gift. For save continuity the existing FLAG_PJR_GOT_CHIKORITA guards the new Ralts handoff, and the Pokémon companion map graphic changes to Ralts. Steven at Saffron Silph now offers Treecko Lv10 / Beldum Lv10 / Bagon Lv10 with matching menu text and party+PC-full retry safety; Torchic/Mudkip are removed only from Steven's choice, not from wild availability or species records.
- `tools/pru/check_rare_gifts.py` verifies the new scene files and logs whether each gift species has an independent wild encounter on this source branch. An earlier encounter ecology PR staged Ralts Route 7, Beldum Safari Beach and Bagon Safari Cave. This build's live wild-encounter JSON contains 3 Ralts slots, 3 Treecko slots, 2 Beldum slots and 4 Bagon slots; exact accessible map locations still need verification.
- Source branch: `pru/noxichu-last-wish-title-test-20261017`, full CI run `39025297612` started at `2b21bb9cbf588b08a1248994c466cf2f65b3bdd4`. **Final verified GitHub Actions success:** run `39025297612` at exact build commit `2b21bb9cbf588b08a1248994c466cf2f65b3bdd4`; all required story/Chansey/gift static checks, donor prep, trainerproc, full `make hns`, ROM package and uploaded artifact green. Direct 32-MiB ROM SHA-256 `68f220ed15390bafb91491e403b1eafabac0a6ef03fee58cce02d9e6decf0e3f`, artifact `12097818098` (`PRU-Noxichu-LastWish-TEST`). **Emulator gameplay still not verified.** Earlier candidate runs `39024895114` and `39024900007` failed on trainerproc comment formatting and a stale QA assertion, both subsequently fixed.
- Outstanding QA: confirm Chansey double actually triggers on interaction, escape/no second viable Pokémon, rewards and repeatability; storage-full NPC retries; Ralts/Beldum/Bagon independently encounterable in this version, and animation preserving approved Last Wish + Noxichu.


## 17 October 2026 — approved title and first story-progression hardening

- **Title user-approved in Pizza Boy A:** after the startup screen, play the original Last Wish Celebi/Jirachi sequence directly, fade to approved Noxichu Relic cavern with independent flashing PRESS START. No Gengar Expansion movie and no Emerald cycling/Groudon/Rayquaza footage. Test-only branch `pru/noxichu-last-wish-title-test-20261017` was compiled at commit `c38745c6d191dd297262d705800e50b58748a19a` in successful CI run `39020672422`; user confirmed the result as **Perfect**. Keep separate from canonical PJR release.
- **Opening story source verified:** Professor Elm gives one level-5 Pikachu automatically; Helix/Dome/Old Amber are passive desk fossils; `VAR_STARTER_MON=0` selects Silver's Cyndaquil battle in Cherrygrove. The original Mystery Egg/Togepi path remains present. This is source checking, NOT a complete fresh-save run from Elm to the Pokémon League.
- **NEW source progression repair:** Hall of Fame replay can only set `FLAG_IS_KANTO_CHAMPION` on the first league victory after **ALL** `FLAG_BADGE09_GET` through `FLAG_BADGE16_GET` are owned. Earlier repeats are Johto title defenses with conditional Lance/Mary/Hall of Fame text. Only the initial qualifying Kanto championship enables the Kanto postgame unlock pass; later league clears cannot reinitialise it.
- **Legendary persistence:** removed `clearflag` of caught Mew, Entei and Raikou and no longer clear Mew/Deoxys/Jirachi event history on Hall of Fame rematches. Kanto postgame grants/roamers still need gameplay verification, as do previously caught legendary encounter object flags. This does **not** mean every legendary capture gate is QA-signed off.
- **Regression work:** `tools/pru/check_pretest_story.py` now checks all eight Kanto badge gates, rematch dialogue branches and permanent capture flags; the title-test GitHub Actions workflow now runs the story regression in addition to battle compilation. Runner `39022869046` at `1ae1cc389247a63a912e41842e00aa13fc9b25f2` passed source checks but failed on two escaped dialogue strings; these were corrected. **Final verified GREEN run `39023135810`** at `df4eb1447c738e8da3136497a47f947a3b02917d` passed full `make hns`, source checks and artifact upload (`PRU-Noxichu-LastWish-TEST`, artifact `12098065185`). SHA-256 of 32-MiB test ROM: `97fb3993591febdd39cb7194fda88fb75f9480f8e2d442f98be265102ba6ce81`. Emulator gameplay still to test. Internal header remains `POKEMON HNS`; standalone branding is separate.
- **Next:** fresh-start emulator playthrough through Mr. Pokémon, Silver's Cyndaquil battle and Togepi Egg; check that theft staging still depicts a genuine stored Pokémon, not one of Elm's fossil display objects. Continue Johto-first dialogue sweep and recurring Jessie/James and Eevee Twins integration.


## Pretest story source pass — 16 October 2026 (ongoing)

- User has **paused the current WIP ROM playthrough** until Elm's lab and the full Johto-first Relic dialogue are ready. Title screen/animation then becomes the very next priority, **ahead of Gym, gift, trainer, and shop work**.
- Safe working branch: `pru/pretest-story-services-20261016`, forked from consolidated `4501256af136729daf5e0e54824e16ccd702b6d5`. **Never alter original `pjr-rebuild`**. Current source dialogue audit `docs/PRU_STANDALONE_RELIC_DIALOGUE_AUDIT.md`; full planned work `docs/PRU_TOMORROW_MASTER_CHECKLIST_2026-10-17.md`.
- **Committed source:** Elm's desk now holds three fossil display objects, not Pokéballs; no selection or acceptance flow. Elm gifts Level 5 Pikachu directly and discusses fossil/Alph Resonance. Silver branch `VAR_STARTER_MON=0`, original Mystery Egg/Togepi path and Rocket theft retained.
- **Committed source:** Oak first Kanto lab visit discusses Johto/Alph findings. Ruins scientist differentiates missing Crest, Crest ready/Relic Ho-Oh outstanding and Relic Ho-Oh caught; unified HNS Tin Tower naming. Removed obsolete Elm starter-choice Egg claim.
- GitHub Actions workflow `.github/workflows/pru-battle-port.yml` temporarily extended for this working branch only, with new `tools/pru/check_pretest_story.py` script: verifies passive fossils, starter, original Egg, chronology and critical flags; scans all active HNS maps for exact obsolete sequel-choice expressions. Workflow run **[38963859049](https://github.com/jamesthoward2112-tech/Pokemon-Johto-Relics/actions/runs/38963859049)** source static scans **GREEN as observed**; full ROM compilation may still be underway. **Do not equate green source checks with emulator QA**. Trigger commit `112f5b6d39177333e5f4e22f0e6aa62a1f74fdd6` (later doc-only commits not part of this build, no code changes afterwards).
- **Safe flag fixes following first green build:** Tin Tower 1F's four reachable statue shortcuts no longer fabricate `FLAG_PJR_RELIC_ALPHORACLE` or `FLAG_PJR_GOT_RAINBOW_CREST` from legacy Red/Ho-Oh flags; they now require the actual Alphoracle catch flag, Crest obtained flag and Crest in bag. Regression test `tools/check_pjr_tintower_shortcut.py` updated to preserve the same four statues, rooftop Rocket battle and Ho-Oh while enforcing real progression. Red's Crest grant checks `giveitem` outcome before setting owned flag, retries on later interaction after a full-bag failure, and keeps ordinary Red rematches intact. Ho-Oh unlock now requires actual Crest owned. Latest source-check runner [38965097002](https://github.com/jamesthoward2112-tech/Pokemon-Johto-Relics/actions/runs/38965097002) at `9d6e0594...` passed the checks and is compiling the patched ROM; verify final result before claiming success.
- **Separate full active-map inventory successfully generated:** [38964424218](https://github.com/jamesthoward2112-tech/Pokemon-Johto-Relics/actions/runs/38964424218), 550 HNS script files scanned, 159 with matching story/Relic words, 663 matched dialogue lines, 0 hits from specific stale-choice/sequel regular expressions. Download `PRU-Relic-Dialogue-Audit` artifact ID `12074611093` (Markdown and CSV). This is strong lexical source coverage **not** complete manual semantic or emulator sign-off.
- **Known high-priority remaining:** old PJR Hall of Fame rematches can reset legacy caught flags / classify premature Kanto Championship; all legendary/event/roaming interactions need emulator tests; review every custom/HNS dialogue path and alternate state semantically. These are tracked, not claimed complete.
- Next title priority: newest PRL Noxichu donor asset from PRL PR108 `6ee9b984...` differs from currently installed PRU Noxichu front/back and PRU folder lacks `icon.png`. Audit every art reference before replacing, then new Relic cave title animation (search donor; fallback PRL Jirachi/Celebi intro). **Title work not implemented yet.**


## PRU binary inspection — first successful test artifact

- Downloaded and inspected artifact ID `12069724170`: ZIP contains `PRU-Consolidated-WIP.gba` (33,554,432 bytes), `.sym`, SHA-256 and commit. Independently verified ROM SHA-256 `8e8899132ca32ba41c2a5584e279efd052fc76257fc76ccc9923d0aa307a7ffd`, matching artifact manifest.
- Verified GBA header checksum matches calculated value `0xB2`; linked symbols for `BattleScript_AbilityHpHeal`, `BattleScript_EffectPRUEevoboost`, `BattleScript_MoveEffectPRUInfatuation` and `BattleScript_MoveEffectPRUCurse` exist.
- **Still WIP identity:** internal ROM title `POKEMON HNS`, game code `BPEE`, not yet branded PRU. This should be audited before the standalone release; do not mistake the WIP artifact for a final named release. Gameplay/emulator QA still required.
- Final verification source-build incorporating new Arbok/Weezing evolutions: [38956851767](https://github.com/jamesthoward2112-tech/Pokemon-Johto-Relics/actions/runs/38956851767) triggered from `73e17e535137c7b74038b816645cf694c1600def`; check actual result, do not assume success.


## 16 October 2026 — first successful consolidated ROM build

- **Verified GREEN:** GitHub Actions [38956023183](https://github.com/jamesthoward2112-tech/Pokemon-Johto-Relics/actions/runs/38956023183) built `make hns` successfully and packaged `PRU-Consolidated-WIP.gba` with `.sym`, SHA-256 and commit file. Triggering commit `1493c0f5e147a0cce179a4b257e73177e076680d`; artifact `PRU-Consolidated-WIP` GitHub ID `12069724170`. Both authentic-signature/static move QA scripts, donor art conversion, and final ELF link passed. **Not emulator-tested or ready for release.**
- A *later, uncompiled* commit `50e8948cc32dae253c292a0f67f2137a08f6dd1f` also connects approved `SPECIES_ARBOK` Level 40 → `SPECIES_ADNOKANA`, and `SPECIES_WEEZING` Level 40 → `SPECIES_CHEAUKING`, plus Thunder Stone → `SPECIES_FRYTNING`. Trigger another source build to include these evolutions before giving an up-to-date ROM.
- Remaining exactness caveat: original Procyon/Deneb/AlteRed move secondary effect parity, ROM save ID migration, all 444 obtainable species, Mewsion scripted battle, and Rock Shop branch integration/QA remain unfinished. Preserve PJR `pjr-rebuild`.


## 16 October 2026 — first complete 25-move compile reached final linking

- [CI run 38955135175](https://github.com/jamesthoward2112-tech/Pokemon-Johto-Relics/actions/runs/38955135175) reached final ELF link after compiling all 25 donor moves; **failed on a single known missing external symbol**: `BattleScript_AbilityHpHeal`. Native / 4bpp art / move registration all passed. ROM compilation was NOT successful.
- Exact root cause: prior duplicate-label repair left `data/battle_scripts_1.s` symbol `BattleScript_AbilityHpHeal:` with a single local colon, while `src/battle_util.c` references it as an external battle script. Repaired to `BattleScript_AbilityHpHeal::` so assembler exports one authoritative global symbol, without reintroducing a duplicate.
- Following first CI trigger, separately committed native real 10% Infatuation and 10% Ghost Curse status rolls for Lovely Bite and Shadow Fangs, and `tools/pru/verify_25_donor_moves.py` mandatory source assertions.
- **Next action:** explicit full CI compile incorporating exported battle script, new PRL signature secondary-effect cases, and 25-move static assertions; if green, obtain artifact hash then fresh-start emulator QA. Exact external original move-effect parity is still incomplete; document honestly.


## 16 October 2026 — Twenty-five donor moves implementation checkpoint

- **Published code:** all 25 required names appended in `include/constants/moves.h` and 25 live battle records added in `src/data/moves_info.h` (not merely reference comments).
- **Authentic PRL signatures:** `EEVOBOOST` uses its own new `EFFECT_PRU_EEVOBOOST` engine effect, shared +1 five-stat script while leaving existing Extreme Evoboost Z-Move +2 untouched. `LOVELY_BITE` inflicts 10% independent target-only Infatuation and 10% Bleeding. `SHADOW_FANGS` inflicts 10% independent target-only Ghost Curse and 10% Bleeding; it does not sacrifice the attacker’s HP. Relevant native status cases and script symbols are committed.
- **Procyon/Deneb external eighteen:** registered original documented type, category, power, accuracy, PP and names. Numeric move records are real. Native effects are *provisional* for Infection, Neurotoxin, Life Drain, Stink Spray and various status/utility effects pending direct donor code or verified reference; consult `docs/PRU_CUSTOM_MOVE_INTEGRATION_BACKLOG.md`.
- **AlteRed original four:** registered separate move records using the four approved compatibility approaches. Distinguish from exact effect ports. Type and power of Super Glitch/Assimilate are provisional compatibility and not claimed source-identical.
- **CI check:** explicit [run 38955135175](https://github.com/jamesthoward2112-tech/Pokemon-Johto-Relics/actions/runs/38955135175) is compiling source at triggering SHA `1b706b16...` after the new fail-fast move registration gate passed. Subsequent Lovely Bite/Shadow Fangs engine changes are remotely committed after the CI trigger, so require a follow-on compile. Do NOT claim a successful ROM before checking CI.
- **Unresolved:** confirm full ROM compile, test effect proc independence, Native Curses in doubles, late donor original effect parity, species evolutions/encounters, Mewsion event, Rock Shop integration, 444 Pokédex, save compatibility and emulator QA. Existing PJR release and all temp freshstart hacks remain untouched.


## 2026-10-16 20:02 BST — compile verdict and fail-fast safeguard

- **Final run verdict:** [GitHub Actions 38951072549](https://github.com/jamesthoward2112-tech/Pokemon-Johto-Relics/actions/runs/38951072549) **FAILED** after sprite-format conversion succeeded. At `build/hns/src/pokemon.o`, compiler reports 25 undeclared original custom `MOVE_*` names in `src/data/pokemon/level_up_learnsets/pru.h` and `src/data/pokemon/teachable_learnsets/pru.h`. All names and attribution/compatibility constraints are explicitly tracked in `docs/PRU_CUSTOM_MOVE_INTEGRATION_BACKLOG.md`.
- **New CI fail-fast gate:** `tools/pru/check_custom_move_registration.py` is committed and wired into the workflow before toolchain installation and full `make hns`; it lists missing genuine move constants, fails on missing entries, and warns about absent active move-table registrations without auto-stubbing. This prevents repeated ~5-minute failed builds during staged move integration. No new explicit compile requested until the real 25 move dependencies are addressed.
- **Additional committed source:** original Frytning/Mewsion icon palette indices corrected; normal Weezing Thunder Stone → Frytning evolution added. These post-trigger edits have **not** yet been compiled and must pass the next consolidated build.
- **Next phase:** implement genuine move effects/data in source (PRL reference for Eevoboost/Lovely Bite/Shadow Fangs and external donor references for remaining 22), run the cheap gate, then CI build; do not claim the GBA ROM is playable, downloaded or emulator-tested until artifact and QA exist.


## Follow-up checkpoint — 2026-10-16 20:00 BST (build running)

- Explicit GitHub Actions build [38951072549](https://github.com/jamesthoward2112-tech/Pokemon-Johto-Relics/actions/runs/38951072549) is running from trigger commit `27781e0abf52cd3c66a80ba2df05288da0c464e6`. CI **passed** the new 12-sprite RGBA→indexed 4bpp conversion step, then entered `make hns`. No finished ROM or compile result is yet verified.
- Compared imported PRU learnsets against `include/constants/moves.h`: 25 genuine custom move identifiers remain undefined (including PRL `EEVOBOOST`, `LOVELY_BITE`, `SHADOW_FANGS` and AlteRed/Procyon original donor names). Their effects are **not** declared implemented; consult canonical donor references instead of silently replacing source moves.
- Reconciled canonical AlteRed donor records: Frytning original party icon uses PJR icon palette index 0, Mewsion index 1. Corrected `src/data/pokemon/species_info/pru_custom.h` (commit `b684945f...`).
- Registered regular Weezing's approved Thunder Stone evolution to `SPECIES_FRYTNING` in `src/data/pokemon/species_info/gen_1_families.h` (commit `4de2c986...`). Galarian Weezing and other existing forms were left unchanged.
- The icon-palette and Weezing evolution commits occurred **after** the explicit CI-trigger commit; they are source-committed but **not included in that run**. Require a subsequent explicit build before declaring those changes compiled. No emulator visuals or evolution execution verified.
- Source-of-truth note: user Library `PRU_Donor_Gaps_Resolved_2026-10-16.md` documents four optional, **non-identical and explicit** AlteRed fallback moves (Terror Wave, Sparklingsky, Super Glitch and Assimilate) for a compatibility release, but authentic move effects are still preferable for the complete integration goal; do not misdescribe fallbacks as ported original effects.


## Follow-up checkpoint — 2026-10-16 19:37 BST / CI sprite-format repair

- Recovered GitHub Actions run [38940072721](https://github.com/jamesthoward2112-tech/Pokemon-Johto-Relics/actions/runs/38940072721), which failed at `graphics/pokemon/adnokana/back.4bpp`: original AlteRed PNG is RGBA (PNG colour type 6) but `gbagfx` requires indexed artwork.
- Verified all twelve external donor PNGs (front/back/icon for Adnokana, Cheauking, Frytning and Mewsion) are RGBA; PRL-sourced sprites remain separately pinned.
- Committed `tools/pru/prepare_external_donor_art.py`: deterministic conversion of these twelve PNGs to 16-index GBA-ready source in the CI checkout; preserved exact existing 16-colour JASC battle palettes for front/back, transparent index zero, and recorded colour deviation and icon-palette visual QA warnings. Does not overwrite or remove the original binary donor graphics committed to source control.
- Updated `.github/workflows/pru-battle-port.yml` to install `python3-pil` and run the conversion before `make hns`.
- **QA honest gate:** compilation not yet verified after these changes. Icons still require in-emulator palette confirmation (shared PJR `iconPalIndex`), and unresolved original donor moves may reveal subsequent compiler errors. No emulator or released ROM claimed.
- Continue fixing only genuine errors on `pru/complete-selective-integration-20261016`, keep `pjr-rebuild` and QA Rock Shop warp untouched. CI is intentionally limited to `docs/PRU_CI_TRIGGER.md` explicit pushes.


## Current GitHub-only progress — further repairs and verified CI blockers (16 October)

- **Working branch** `pru/complete-selective-integration-20261016`, all changes described here remotely committed. Latest explicit compile trigger `aa4968fa4b75ce09e7bb3a8e6bc0e53902f963b8`.
- **Repaired second binary-corrupted source**: `src/pokemon.c` was invalid non-UTF8/binary at line 1242 and produced thousands of stray-character compile errors. Reconstructed from prior verified clean source on PR #11, commit `17b8ca3fb202896b3ffbd5aaf4430365c997451f`. Note: original corrupt Work file bytes cannot be trusted; source history remains available.
- **Ported all 57 standard PRL move-specific Bleeding/Fear chances** where matching PJR moves already exist, preserving original PJR move effects (e.g. Bite flinch and 5% Bleeding). Of those, 49 Bleeding and eight Fear; commit `5faf0611a3403b7bc9d18415c7af430a032c957e`. Two other source moves, Rip and Tear and Iron Fangs, already integrate status effects. Lovely Bite and Shadow Fangs await exact PRL Infatuation/Curse effect support.
- **Fixed 19 species registration include omissions** in central `src/pokemon.c`: `#include "data/graphics/pru_pokemon.h"`, `#include "data/pokemon/level_up_learnsets/pru.h"` and `#include "data/pokemon/teachable_learnsets/pru.h"`. Commit `2ba3bdd9310534661c1803fd237ac712e7199456`. This addresses CI run `38939057476` errors where all 19 species graphics and learnsets were undeclared.
- **Compiled result so far:** GitHub Actions run `38939057476` FAILED on missing 19-species graphics/learnset registration (fixed above). Next explicit CI run triggered at `aa4968fa...`, inspect for new genuine compilation errors and capture its run ID. Do not report current ROM as successfully built or tested.
- **Outstanding before final ROM:** ~26 external donor custom moves in learnsets still not registered (from AlteRed and Procyon/Deneb). Source and moves' original effects must be obtained/ported rather than silently substituted. Eevoboost, Lovely Bite/Shadow Fangs, remaining Fear special cases, Eerie Fog end-turn stat decay, UI Red BLD, gameplay evolution/obtainability, Mewsion event #8 and full emulator QA. User's Rock Shop separate QA build remains deferred; never merge temporary new-game warp to production.
- **Efficiency and recoverability:** Only build on explicit `docs/PRU_CI_TRIGGER.md` checkpoint edits; always update GitHub checkpoints, and do not waste Work credits or recertify completed donor audits.



## GitHub-only continuation — 2026-10-16, after Work credit exhaustion

- **Verified remote branch:** `pru/complete-selective-integration-20261016`. The restored species/header and engine work described here are remotely committed, not local-only.
- **Critical repair:** Work's `include/constants/species.h` at tree blob `166404eb...` contained binary NULs and caused an unterminated preprocessor header. Reconstructed the exact frozen PJR definitions 1–1623 from PR #11 and appended approved 19 species IDs 1624–1642; repaired result `86aee386...`, commit `a5adc7d5...`.
- **Compiler fix:** Removed duplicate `BattleScript_AbilityHpHeal` label in `data/battle_scripts_1.s`, commit `ad7a2f52...`. Previous CI had failed on assembler symbol redefinition.
- **Original PRL move additions:** Native PJR move enum and move table implementations for Seismic Slam, Soil Drain, Bravado, Raging Souls, Beatdown, Take Flight, Insect Impact, Rip and Tear and Iron Fangs. Original stats/effects/probabilities retained; Soil Drain uses PJR's real `EFFECT_ABSORB` 50% semantics, unlike PRL's newer `MOVE_EFFECT_ABSORB` additional-effect API.
- **Bleeding source layer:** `STATUS1_BLEED` bit 13 and `MOVE_EFFECT_BLEED` appended (preserve frozen PJR status/effect indices); native infliction, Rock/Ghost immunity, safeguard/status gate, residual 1/16 max HP (minimum 1, Magic Guard exemption), battle scripts/messages. Source commits `33344ad...` through `aa133055...`. **Not yet emulator-tested; visual red BLD, cures/healing moves, all standard move proc chances and edge cases remain.**
- **Fear source layer:** append `VOLATILE_FEAR` / `fearTimer`, native two-turn infliction/expiry, 1.5x normal incoming damage, escape gate, scripts/messages. Source commits `58710020...` through `7f8368bb...`. **Not yet emulator-tested; Fear-inflicting standard moves and interaction QA remain.**
- **CI:** `.github/workflows/pru-battle-port.yml` now runs only on explicit `docs/PRU_CI_TRIGGER.md` changes, preventing dozens of full builds for intermediate commits. Compiler output is redirected and bounded on failures for diagnosable GitHub logs. Explicit compile checkpoint triggered by `5f3fe828...`; inspect GitHub Actions run `38938373925` for actual result. Previous attempts failed first on corrupt species.h, then duplicate script label; later donor/engine errors expected.
- **Immediate next tasks:** fix errors from latest bounded CI run; register original donor moves used in 19 species learnsets (do not substitute vanilla), complete Eevoboost, Lovely Bite, Shadow Fangs, Fear/Bleeding original proc chances and animations, complete Eerie Fog stat-drop, reconcile missing ability definitions, scripted Mewsion encounter and acquisition ecology; test saves/emulator. No consolidated playable ROM is claimed yet.
- **User requirement:** regular factual GitHub checkpoint updates and credit-efficient batch work. Do not merge QA-only Rock Shop fresh-start warp into production.



Updated: 2026-10-16 (recovery after interrupted Work session)

## Live recovery state — 2026-10-16T16:18:30Z
- Active local branch: `pru/complete-selective-integration-20261016`.
- Recovery base: `464fc66ed2ebe11ca1e4cda47d891dc753828499`, the CI-passing PR #11 head. It contains the seven native-move/Eerie Fog commits directly on top of PR #9.
- Last published implementation before this checkpoint: `464fc66ed2ebe11ca1e4cda47d891dc753828499` on `origin/pru/battle-port-phase1-20261016`; GitHub Actions run `38925573625` compiled the isolated ROM successfully.
- The original scratch worktree disappeared before this resumed session. Its local-only commits (`e6fb58120`, `ba603890c`) and uncommitted species/mechanics files were not present in any remote ref and could not be recovered byte-for-byte. No claim is made that those files were preserved.
- Retained evidence from the interrupted session records GREEN static checks for the 19-species ID allocation, Bleeding/Fear/Eerie Fog source integration and selective Radical Red data, but those local edits were never compiled or pushed and must be reconstructed from the pinned donors.
- Working tree at recovery was clean. This branch is the sole resumed integration branch; PR #10 remains separate.
- Immediate priorities: reconstruct the 19 species/data/assets with the ID-freeze verifier; then port remaining authentic moves/abilities/status mechanics; then implement Mewsion issue #8; finally compile in CI and emulator-test.
- Local build constraint remains: the scratch host lacks `arm-none-eabi-gcc`, `pkg-config` and libpng development headers, so GitHub Actions is the authoritative build environment.

## Species reconstruction checkpoint — 2026-10-16T17:02:00Z
- Active branch: `pru/complete-selective-integration-20261016`; last confirmed remote commit before this batch: `453cd93d26a40b33c78926b4f0ef1b593f4473bc`.
- Reconstructed the frozen species-ID baseline and appended the exact approved IDs 1624–1642. `tools/pru/verify_species_import.py` verifies every pre-existing ID through 1623 against `tools/pru/baselines/pjr_ids_through_1623.json` and rejects nuMew or ordinary Wooper/Quagsire replacement.
- Added pinned PRL species records and level-up/teachable learnsets for the 15 genuine imports. Added approved Kanto Ultimate/AlteRed records for Adnokana, Cheauking, Frytning index 110 and Mewsion/Mewduo index 150. Original custom move names remain in the learnsets; no vanilla fallback substitutions were made.
- Imported front, back, normal palette, shiny palette and two-frame party icon for all 19 species: 75 files are byte-identical to pinned PRL commit `6ee9b984521ac6f2beaf995f771a726379e55c88`, and 20 are byte-identical to the approved external donor pack. All 57 PNGs passed 64x64 battle-sprite / 32x64 icon dimension checks.
- Static verification: `python3 tools/pru/verify_species_import.py --donor /workspace/scratch/8f11ddff019a/prl-repo` PASS; `git diff --check` PASS.
- Build status: not yet compiled. The authentic learnsets intentionally expose the next required dependency batch: PRL ability constants/effects and original AlteRed/Procyon custom move constants/effects must be registered before compilation. This is staged source, not a playable ROM and not emulator-tested.
- Next priority: implement the missing genuine custom moves and all PRL abilities, then run the first consolidated CI compile. Evolution links, acquisition locations, issue #8 Mewsion event and egg-move reconciliation remain outstanding.

## Custom ability implementation checkpoint — 2026-10-16T17:31:00Z
- Species reconstruction is remotely published at `98cef3c5c9f5ccdf8fca6150e0ad5053979704e4` on `pru/complete-selective-integration-20261016`.
- Appended the nine PRL abilities absent from PJR after every frozen PJR ability ID: Ancient Grove, Solar Discipline, Tidal Bastion, Ancient Core, Wishmaker, Eden's Canopy, Thermal Wings, Citadel Shell and Stygian Rush. Existing Ancient Bastion/Bloom, Cinder Veil and Tidal Roar mechanics were preserved.
- Ported their original triggers: five-turn per-battler aura timers; Defense, typed-power and super-effective modifiers; Wishmaker healing/stat protection; Eden's Canopy terrain/status protection; Ancient Core hazards/stat protection; Thermal Wings recoil reduction; Citadel Shell Defense protection; and full-HP Dark priority.
- RED/GREEN gate: `tools/pru/verify_custom_abilities.py` initially failed on absent constants and now passes. `git diff --check` passes.
- Local `make -j2 hns` remains blocked before source compilation by missing host dependencies: `arm-none-eabi-gcc`, `pkg-config`, and `png.h`. No ROM or emulator result is claimed. CI compile is deferred until the authentic move/status dependency batch is registered, because current species learnsets intentionally retain unresolved original donor move names rather than substitutes.
- Next priority: append the remaining eleven PRL move records plus Eevoboost, then implement Bleeding/Fear so the native bleed-bearing moves can compile; follow with exact AlteRed moves and the approved Procyon-reference move subset.

## Purpose
A **GitHub-published recovery checkpoint** for Pokémon Relics Ultimate's consolidated integration. Update this file after each meaningful source milestone and before every expected Work-session limit. Local-only logs are insufficient; **push the checkpoint and source commits to the remote branch** so a future conversation can resume without repeating investigation.

## Repository and authoritative inputs
- Repository: `jamesthoward2112-tech/Pokemon-Johto-Relics`
- Current verified, remotely published engineering branch: `pru/consolidated-prl-battle-import-20261016`
- Existing PR: [#9 — WIP consolidated import](https://github.com/jamesthoward2112-tech/Pokemon-Johto-Relics/pull/9)
- Verified published head at recovery: `b4b1d5f18ba52ab7af03081d25bfc82b9079b7dd`
- Stable PJR/PRU base: `pru/full-relic-import-20261016`; commit `c02ec0f209d680190f538fc224b6e440f3fc7a02` recorded as Work starting point.
- Pinned PRL/PR108 donor: `jamesthoward2112-tech/Pokemon-Relic-Legacy` commit `6ee9b984521ac6f2beaf995f771a726379e55c88`.
- External donors/canonical files: ChatGPT Library, `/Pokémon Relics Ultimate/Canonical Data/`.
- Approved encounter requirements: GitHub issue #8 (Mewsion Level 90, Cerulean Cave B2F).

## Recovery notice: published vs unpublished work
The prior **Work** session reported an isolated **local** branch `pru/complete-selective-integration-20261016`, a persistent progress ledger, and RED/GREEN compatibility-verifier checkpoints. The supplied screen recording shows reported activity on species verification, PRL mechanics, ability/graphics data, Seviian art and Mewsion logic. **This local branch is NOT present among published GitHub remote branches as of this checkpoint** and its full worktree is **not recoverable from this GitHub branch alone**. Reported local milestones are not asserted as verified commits or finished build results.

**Required first step on returning to that original Work session:** inspect its existing worktree and local branches; print `git status -sb`, `git log -n 15 --oneline --all --decorate`, and list any progress-ledger/checkpoint files; commit unfinished work safely to the existing isolated local branch, push `pru/complete-selective-integration-20261016` to `origin`, and push/update this checkpoint on the same branch. Do NOT restart the donor audit or discard existing source changes. Confirm remote SHA and include it here.

If the original Work container is irretrievable, continue on the separately published PR #9 branch from its verified commit rather than claiming local Work changes are available.

## Verified remotely published progress
- PR #9 contains canonical source requirements, pinned **37 authentic PRL custom move records**, ability descriptions, and compatibility reconciliation. This **does not prove** all battle effects are fully implemented.
- PJR source already defines 34 of PRL's 50 custom entries. The remaining 16 include superseded nuMew, so **15 genuine missing PRL species** remain.
- External donor species to import: **Adnokana, Cheauking, Frytning, Mewsion**.
- Internal PJR species IDs **1–1623 frozen**; append the 19 required imports **1624–1642** without changing existing saves.
- Standard Wooper/Quagsire must remain; preserve Paldean Wooper/Clodsire as separate forms/entries. Seviian Noibat/Noivern must reuse approved existing slots; selectively adapt Radical Red source.
- Do **not** report a consolidated ROM as compiled or emulator-tested: none is verified on the published PR #9 branch.

## Mandatory implementation
1. Port 19 species at IDs 1624–1642 with approved donor stats, typing, abilities, learned/TM/tutor/egg moves, evolution chains and cries.
2. Compare existing PJR Johto overlaps against PRL; keep approved PJR Johto gameplay and import approved latest PRL Kanto/Hoenn artwork and movesets.
3. Port **all genuine PRL custom moves and abilities** with real effects, triggers, battle text, animations and AI handling — no substituted vanilla abilities/moves.
4. **Bleeding:** PRL status bit 13, original move-specific infliction chances, 1/16 end-turn damage, healing integration, red BLD visual.
5. **Fear:** genuine two-turn volatile, 1.5× damage taken, escape restriction and related interactions.
6. **Eerie Fog:** real eight-turn weather and ability support; preserve PJR Frostbite.
7. Mewsion #425: Level 90, only after **both Mew and Mewtwo CAUGHT**, complete cave exit/re-entry, same B2F tile as Mewtwo, warning once on eligible B2F entry, retry after KO/flee, permanent dismissal on capture. Preserve Level 80 Mewtwo and Level 50 Faraway Island Mew.
8. Preserve Elm Pikachu-only starter, original Togepi Egg, early wild starter availability, PJR story, wild encounters and all existing saves.

## Build / verification gates
- Validate ID freeze, data and graphics registration, evolution access and availability of all 444 species.
- Verify original and shiny battle sprites, palette limits, both party icon frames, move tables and ability effects.
- Build actual standalone GBA ROM in GitHub CI; capture workflow URL, commit SHA, ROM filename and SHA-256.
- Emulator test clean and existing saves (mGBA if available), battles/statuses, encounters, Pokédex, graphics and gameplay progression.
- Produce final ROM, comprehensive comparison report and PR. Do not call anything tested before tests pass.

## Required live checkpoint update template
At **each meaningful code milestone or before work interruption**, overwrite this section with:
- UTC timestamp; active local and remote branch names; current local commit; last successfully pushed commit.
- What was changed and committed (specific file names/SHAs), tests run and their actual pass/fail results.
- Current build status and any available CI URL/artifact/SHA-256.
- Exact unresolved build errors, blockers, next command and priority tasks.
- Worktree dirty/untracked files and whether critical files were pushed to origin.
- Source/data provenance and unresolved donor/graphics assumptions.

**Rule: push source + checkpoint at meaningful intervals, and always before an expected usage cutoff. Never say the checkpoint is remotely recoverable until a `git ls-remote origin` check confirms it.**

## Independent acquisition follow-up — ready to cherry-pick (16 October)

The separate `pru/encounter-ecology-20261016` branch and [PR #10](https://github.com/jamesthoward2112-tech/Pokemon-Johto-Relics/pull/10) now include the completed **nine ordinary Pokémon source-audit follow-up**:
- Tyrogue Mt Mortar 1F south day/night Lv18–20 (Hitmonlee and Hitmontop); Wurmple Ilex Forest day Lv8–9 (Cascoon); Nincada Union Cave 1F Lv8–9 (Shedinja).
- Eevee Route 29 and all Water Stone, Fire Stone, friendship day/night evolution branches confirmed from species source (Vaporeon, Flareon, Espeon, Umbreon).
- Goldenrod 2F now sells Deep Sea Scale and Tooth, complementing Clamperl's existing Route 20 fishing and Gorebyss/Huntail source evolution definitions.
- `tools/pru/check_nine_acquisition.py` runs under `.github/workflows/pru-encounter-ecology.yml`. GitHub Actions passed on commit `d02fd90bfd30ec643b0e5f95c8f40b97db9a0a42`; this is **source-only QA**, not compilation or emulator testing.
- The full 444-row acquisition matrix now marks these nine `EVOLUTION_DEFINED_QA_PENDING` rather than unresolved.
- Detailed report: `docs/PRU_ENCOUNTER_ECOLOGY_20261016.md`; follow-up branch tip at time of note: `330bc40411ef8d7181e89912b4ae544dbbacd1e2`.
- **Handoff:** after recovering and pushing Work's unpublished source, selectively merge/cherry-pick PR #10 into the consolidated integration branch, resolve the `SPECIES_GEMLIN` dependency, then compile and emulator-test. Avoid source-file replacement that drops Work's newly ported species data.

## 17 Oct 2026 — VERIFIED GREEN: Twin-Chansey portrait + Route 34 move specialist

- Nurse-hat twin Chansey artwork converted from the user-supplied image to a 64×64 indexed 16-colour PNG. Source: assets/pru_chansey/twins_front_64.png.b64, SHA-256 55452b964a24dc7cd5098f90ca2bba69325c1c8a9d381ddb4a5824e0e681267b. The new TRAINER_PIC_FRONT_CHANSEY_TWINS entry is loaded before compilation and assigned to all 21 Chansey-tier trainers instead of Beauty.
- Battle-message override for trainer IDs 654–674: "Chansey wants to train!" and a nonhuman Chansey send-out message, retaining repeatable two-Chansey double battles. The trainer class remains Beauty Hns internally for parser compatibility; other untested battle messages may still use it.
- Route34_DayCare_hns now has a Scientist Move Expert at (7,7), offering free Egg and Tutor moves from party/PC via existing Move Relearner engine. The original Day-Care and Odd Egg events remain. Actual NPC placement and menu behaviour need emulator QA.
- GitHub Actions run 39029758140 GREEN at build commit df4bcd1a967af04adf08b5202768867b54812e4f: full make hns, artifact 12100017409, ROM SHA256 72fab2b8623d74d03b0cec2c1ecfc071fbccd05077f51554f64efeda8707c590, 33,554,432 bytes. Direct ROM provided: PRU-Chansey-Twins-Egg-Tutor-TEST.gba. Approved Last Wish to Noxichu intro preserved. Gameplay must still be tested in Pizza Boy A.

