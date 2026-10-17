# PRU Approved Noxichu Title + Last Wish (17 Oct 2026)

The user has approved **the specific 240 × 160, indexed 256-colour GBA title image**:
`assets/pru_title/Noxichu_Title_GBA_240x160_256colour.png`

SHA-256: `0cfdc68858e6818c771dd10e3d79b41a41658f642c0aaec7cd017b2cc60a2c64`

This file is an exact reproduction of the approved preview; no sharpening, re-quantizing, scaling, JPEG conversion, or asset swap is permitted.

The 8bpp pixel buffer is 38,400 bytes, the BGR555 palette is 512 bytes. `tools/pru/build_noxichu_intro_trial.py` embeds these into the PJR Mode 4 title bitmap at build time while preserving the **separately flashing PRESS START sprite**.

**Intro path:** native short copyright → Hoenn's Last Wish Scene 0 (Celebi + Jirachi first fly-past, then second moon fly-past) → black fade → approved Noxichu title.

Do not re-enable Emerald/Gengar intro. This branch deliberately omits donor Scene 1's Emerald montage.

## Regression evidence

GitHub Actions run #76's 90-second mGBA recording was inspected directly on 17 October and visibly shows **Celebi/Jirachi around 9 seconds and again around 17 seconds**, with title screen by roughly 30 seconds. The apparent absence of the scene was caused by inspecting only spaced frame samples. The CI workflow now exports screenshots around both encounters and after the title fades in. Full visual acceptance requires checking those screenshots and comparing the displayed title with the approved preview. A compile or running emulator process alone is not visual proof.

Library copies: `/PRU/Title Assets/Noxichu_Title_GBA_240x160_256colour.png`, `/PRU/Title Assets/Noxichu_Title_GBA_Preview_4x.png`.
