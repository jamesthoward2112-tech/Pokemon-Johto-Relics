# PRU Legendary Sprite Policy — Latest Locked Decision

## Locked art decision — 16 October 2026: Registeel option A
**APPROVED / retain:** Registeel Option A, the **Odyssey II redesign** displayed in the six-image Regi/Mew/Deoxys comparison: grey spiked armoured robot with pink/red central face/eye; matches `Registeel_front.png` and `Registeel_back.png` in `/Project Hoenn Relics/Sprite Resources/Odyssey II - Selected Hoenn/`. Both verified native 64×64 RGBA. Original project PHR selection is reaffirmed for PRU. Do **not** use Wild Indigo Option B's black shadow front; that candidate is REJECTED.
**NOT APPROVED / REJECT:** Odyssey II Deoxys image is **not a sufficiently distinctive redesign** according to the user. It may be another pose but is NOT the selected custom Deoxys. Keep current Deoxys sprite + Normal/Attack/Defense/Speed functionality pending a truly changed GBA-ready design; do not reintroduce Odyssey II Deoxys as a "custom" recommendation.
**Mew:** current Xenoverse Retro option **not chosen**. Seek a more distinctive *native GBA-ready* Mew alternative from sprite libraries, uploaded ROMs, or creator-approved source; do not assume nuMew (a separate custom species) is ordinary Mew.
**Artwork fallback:** preserve vanilla overworld appearance unless matching user-approved overworld sprites are supplied. Battle replacements need 64×64 front/back, matching party icon where possible, palette/shiny/QA; no resizing/redrawing.
**Acceptance:** approved as art direction/source lock, not a claim that the graphics have already been wired/compiled/emulator-tested in standalone PRU.

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

## Corrective follow-up audit — 16 October 2026
Earlier claim that all five Mew/Regis/Deoxys lack genuinely different art was wrong. Inspection of pixels in existing archived assets confirms:
- **Regirock, Regice, Registeel and Deoxys:** distinctive native 64×64 front/back and 32×64 menu icon in the Odyssey II bank `/Project Hoenn Relics/Sprite Resources/Odyssey II - Complete Sprite Bank/Odyssey_II_Complete_Sprite_Bank.zip`. The three Regis are also individually saved as previously user-selected PHR assets in `/Project Hoenn Relics/Sprite Resources/Odyssey II - Selected Hoenn/`. These are genuine redesigns, not mere alternate vanilla poses. Normal/shiny palette/source QA remains to be done.
- **Mew Retro (Xenoverse):** native source animation strips, front 352×85 (four 88×85 frames), back 300×75 (four 75×75 frames), Icon/IconShiny present. The opaque sprites within each front/back frame fit a 64×64 canvas *without any pixel resizing or drawing*. Native frame extraction/cropping and icon/animation reformatting are needed, so not direct-copy ready. Source: `PJR_Xenoverse_New_Donor_Bank.zip`, folder `05_Other_Xenoverse_Styles_and_Retro/Mew_Retro/`.
- **Second Registeel option:** Wild Indigo `REVIEW_ONLY_10/registeel_anim_front.png` has two 64×64 frames (64×128 sheet) showing a black shadow design. **Front only**, no matching verified back/icon. Comparison sheet shows an Odyssey II back for reference, NOT a Wild Indigo back.
- **Deoxys:** redesigned donor available for Normal form only. Attack/Defense/Speed donor variants still need checks; preserve existing functional forms.
- All candidates NOT imported/approved by the user. Vanilla overworld fallback remains; user-approved proper alternative OW sets may replace it. No scaling or redraw.
- Local review sheet: `/mnt/data/PRU_Remaining_5_Actual_Custom_Sprites_2026-10-16.png`.

## Sources of truth and QA
- Current PRU Notion: https://app.notion.com/p/3fb4939d431681afa46fdeb97cf8c79b
- Library visual preview: `/Pokémon Relics Ultimate/Canonical Data/PRU_Legendary_Custom_Sprite_Shortlist_2026-10-16.png`
- Library audit: `/Pokémon Relics Ultimate/Canonical Data/PRU_Legendary_Sprite_Audit_2026-10-16.md`
- No sprites were imported, overwritten or emulator-tested during this artwork audit.
