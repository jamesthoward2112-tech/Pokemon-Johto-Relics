# PRU — Eight-Badge Polish (20 October 2026)

## Player checkpoint and scope
The current playthrough has obtained **all eight Johto badges** and is approaching Victory Road and the first Elite Four. Preserve save layout, trainer flags, progression and canonical 444-species registration; do **not** rebalance all earlier Johto routes or introduce the post-Champion systems yet.

## Already incorporated in the 20 October baseline (verified source/build, visual gameplay QA pending)
- **Skarmet:** approved Pokémon Tourmaline v1.1.1 Skarby-derived front/back/icon art, indexed in `graphics/pokemon/skarmet/`; in-game name stays Skarmet. See `docs/PRU_SKARMET_TOURMALINE_ARTWORK_20261020.md` and `CREDITS.md` for source and attribution requirements. Shiny art not separately approved.
- **Donphalanx:** approved Great Tusk front/back/icon visuals and donor-sync override. Stats, type, ID, evolution methods and other species mechanics remain Donphalanx's own.
- Carry forward previous 19 October sprite grounding (Valkiri/Swamplith), Swamplith green icon, mandatory Jessie/James encounter changes, free Blackthorn move relearning, Dragon's Den Steevee/Neevee and Route 42/Mahogany story recovery. **Do not report live player validation without actual evidence.**

## Eight-Badge change: Lum Berry / Bleeding
- `STATUS1_BLEED` is already part of `STATUS1_ANY`: ordinary Full Heal/Full Restore and the Lum Berry's full-cure logic can remove Bleeding.
- The **Lum Berry item description now explicitly says it cures Bleeding**.
- `TryCureAnyStatus()` now names **bleeding** in the BLD/Lum Berry cure text on PRU/HNS, while leaving other game variants unchanged.
- Add source-level regression `tools/pru/check_lum_berry_bleeding.py`; GitHub Actions must compile HNS, run source/ROM audits, and mGBA boot before the new direct `.gba` release.
- Do not change the 1/16-max-HP end-of-turn Bleeding tick, immunity, move procs or the BLD UI graphics.

## Final Johto checks
- Confirm Victory Road map scripts and League entry remain accessible in the user's existing eight-badge save.
- Verify Elite Four battle teams, reward/ending, saved progression flags, and first Hall-of-Fame sequence in a **live saved gameplay test**; static compilation and emulator boot alone are insufficient.
- Check BLD badge display and actual Lum Berry cure, Skarmet & Donphalanx icons/sprite grounding, and remaining custom species visuals in doubles.
- Save migration/compatibility is **not** confirmed until loading the real save.

## Deferred to after the first Hall of Fame
- Kanto wild encounter ecology rebalance and roaming Kanto legendary birds.
- Elite 20 ultimate double-battle programme and infinite Ancient Candy endgame reward.
- Michelleeby Pokémon Emerald Battle Frontier v1.1.0 facilities and major-trainer doubles, with credit and PRU systems compatibility.
- Broad exploration of all 444 encounter positions and remaining postgame legendaries.

## Build status
Source edits staged under `pru/eight-badge-polish-20261020`; see Actions/Release for the definitive CI result and direct 32 MiB GBA. Preserve existing release tags and user saves.
