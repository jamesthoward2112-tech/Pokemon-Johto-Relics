# PRU Legendary and Mythical Sprite Policy — 16 October 2026
**Latest user-approved sourcing rules. This document supersedes the earlier generic Odyssey II 21-legend sheet. No ROM assets swapped yet.**

## Locked existing custom sprites — PROTECT
- Kanto: Articuno, Zapdos, Moltres, Mewtwo.
- Johto: Raikou, Entei, Suicune, Lugia, Ho-Oh, and the established RELICS Celebi visual.
- Reuse existing approved PRL/PJR donor art. Never replace these with an alternative vanilla pose simply because it is another native-size GBA sprite.

## Overworld rule (corrected)
**Keep original vanilla overworld sprites by default.** If matching **GBA-ready alternative overworld assets are actually supplied AND approved**, they may replace the vanilla appearance. Do not resize or redraw battle sprites into overworld figures.

## Sourcing standard
Native 64×64 front and back; <=15 non-transparent colours, binary alpha and indexed GBA-compatible palettes; verify both normal and shiny, 2-frame 32×64 party icons (or retain vanilla icon until ready), positioning/animation/form pointer correctness and emulator QA. **No resize or redraw.** A donor may be visually used for the original species without introducing Mega/Primal/Bond battle mechanics unless explicitly approved. A different vanilla pose **does not count as custom art**.

## Six real alternate-form donor candidates found in existing Library assets
| Species | Proposed visuals | Native-size verified source | Open items |
|---|---|---|---|
| Latias | Mega Latias | `/Project Hoenn Relics/Sprite Resources/Elite Redux v2.65 beta2/PHR_Elite_Redux_Hoenn_Mega_Sprites_v2.65.zip` | party icon, in-game visual test |
| Latios | Mega Latios | same pack | party icon, in-game visual test; similar to Latias |
| Rayquaza | Mega Rayquaza | same pack | party icon, in-game visual test |
| Jirachi | Jirachi-Bond | `/Pokemon Sprite Libraries/TRE 2026/New Forms/TRE_2026_New_Forms_Extracted.zip`; `990_Jirachi-Bond/` | proper colored 32×64 icon and QA |
| Kyogre | Primal Kyogre | `/Pokémon Johto Relics/Sprite Resources/TRE Primal Sprite Bank/PJR_TRE_Primal_Sprite_Bank.zip`; `1034_Kyogre` | bank only has 32×32 icon frame; QA |
| Groudon | Primal Groudon | same pack; `1035_Groudon` | bank only has 32×32 icon frame; QA |

All six have transparent 64×64 front/back and normal/shiny fronts with <=15 opaque colours, verified directly against archived PNG bytes. Still **candidate only, not approved**. User must review designs; earlier approved choices (e.g. PHR donor picks) should not be overwritten until reconciled.

## Still open — find genuine distinctive, GBA-ready alternate art
- **Mew** (Xenoverse Mew Retro has oversized strips, not direct native GBA sprite).
- **Regirock, Regice, Registeel** (Odyssey II has alternate poses, not proven custom redesigns).
- **Deoxys** (PRU has Normal/Attack/Defense/Speed folders, but Odyssey II's single version is an alternate vanilla pose; locate genuine custom art and preserve form functionality).

## Sources of truth and QA
- Current PRU Notion: https://app.notion.com/p/3fb4939d431681afa46fdeb97cf8c79b
- Library visual preview: `/Pokémon Relics Ultimate/Canonical Data/PRU_Legendary_Custom_Sprite_Shortlist_2026-10-16.png`
- Library audit: `/Pokémon Relics Ultimate/Canonical Data/PRU_Legendary_Sprite_Audit_2026-10-16.md`
- No sprites were imported, overwritten or emulator-tested during this artwork audit.
