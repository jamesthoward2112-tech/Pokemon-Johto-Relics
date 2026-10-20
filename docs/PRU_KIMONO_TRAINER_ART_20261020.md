# PRU — Trainer-exclusive Kimono Girl ritual artwork (20 October 2026)

## Design decision and safe implementation
**User request:** the five Ecruteak Dance Theatre Ghost Pokémon should appear customised, preferably from existing Mega Pokémon sprites, but **only in those specific trainer battles**. All other Gengar/Banette/Sableye/Misdreavus/Dusclops sprites remain normal, including the player's own.

**Technical constraint:** `P_MEGA_EVOLUTIONS FALSE` in `include/config/species_enabled.h`. Do not enable Mega mechanics, add Mega species to canonical 444, change stats/moves/abilities, or equip mega stones. Instead, reuse already present GBA-ready Mega front graphics + palettes and select them ONLY when loading those trainers' enemy front Pokémon battle sprites.

| Kimono Girl | Underlying true species | Trainer-only artwork |
|---|---|---|
| Zuki | Gengar Lv48 | Official Mega Gengar front art and matching palette (visual only) |
| Naoko | Misdreavus Lv48 | Ritual/shiny Misdreavus front palette with violet tint (not falsely claimed to be Mega) |
| Miki | Banette Lv48 | Official Mega Banette front art and matching palette (visual only) |
| Sayo | Sableye Lv48 | Official Mega Sableye front art and matching palette (visual only) |
| Kuni | Dusclops Lv48 | Ritual/shiny Dusclops front palette with blue tint (not falsely claimed to be Mega) |

Assets are already in the engine's `graphics/pokemon/<species>/mega` source directories; only three front graphics/palettes are included under `#if !P_MEGA_EVOLUTIONS` in `src/data/graphics/pjr.h`. The selector in `src/battle_gfx_sfx_util.c` validates PRU/HNS, trainer battle, opponent side, no transform form, trainer ID AND the expected species. Sprite gfx and palette are replaced in the opponent-only sprite-loading path. For Misdreavus/Dusclops, existing shiny imagery remains the base silhouette and the opponent palette is tinted. Later replace these with fully bespoke front sprite files if a GBA-compatible custom donor becomes available, without altering this mechanic.

**No new sprites appear in the player's party/back sprites/icons**; the original species are unmodified. The original Elm Master Ball dialogue, Five-Kimono challenge, Ho-Oh/Lugia route and reception-gate gating are unchanged.

## Build and gameplay QA
- `tools/pru/check_kimono_ghost_teams.py` ensures 5 non-Eeveelution Eerie Fog singles and Elm/Legendary route unchanged.
- `tools/pru/check_kimono_ritual_visuals.py` confirms art assets, exact opponent-only selector and Mega Evolution stays disabled.
- Run full `make hns`, binary 444/species audit and mGBA boot. Do not claim trainer sprite visibility based on boot alone; this requires a real Dance Theatre battle screenshot/video.
- Release a distinct direct 33,554,432-byte `.gba` with no ZIP. Keep the Ghost Kimono and Eight-Badge baseline releases intact.
- User must back up the eight-badge save, use existing Elm instruction before Dance Theatre and compare Zuki's Mega Gengar artwork and the other four appearances in actual battles. **No change to save structs or flag values.**

## Deferred
A fully custom Misdreavus and Dusclops sprite pair, and the remaining later Kimono trainers' Elite 20 rework, are post-Champion art/content unless approved earlier.
