# Approved artwork donor: Skarmet in PRU

Pokémon Relics Ultimate's **Skarmet** (baby Skarmory) now uses the **Skarby** front/back design from Pokémon Tourmaline v1.1.1 by **tdilos**.
Source: https://www.pokecommunity.com/threads/pok%C3%A9mon-tourmaline-v1-1-1-released-02-09-2026.527425/
Tourmaline's published credits list **PTickles** for Skarby concept art and **AtecainCorp** for SpaceWorld beta Pokémon sprites. Verify authorship of the exact Skarby battle sprites and redistribution permission before publishing beyond private test builds.

The 64×64 indexed normal front/back were extracted from a locally patched copy of Tourmaline v1.1.1. The 32×64 two-frame icon is a derivative crafted from those pixels using a dedicated indexed palette. Because a unique shiny palette was not confirmed in the donor, the same palette is used for normal/shiny **temporarily**, pending verified shiny artwork. 
All files are stored under `graphics/pokemon/skarmet/` (never named Skarby for the PRU runtime). Engine species name, IDs, evolutions and stats are unchanged.

**Donphalanx** uses Great Tusk battle/icon artwork at `graphics/pokemon/great_tusk`, as locked on 20 Oct 2026. Its donor-sync override must remain enabled.

See `tools/pru/check_skarmet_tourmaline.py` for source-level audits. Live user-gameplay visual/palette tests remain outstanding.
