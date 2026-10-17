# PRU Johto Team Rocket trio — 17 October 2026

## Scope and donor preservation

Derived from `pru/noxichu-last-wish-title-test-20261017`, without overwriting
the parallel `pru/gym-leader-overhaul-20261017` work.

The existing PRL-pinned graphics are already in the PRU tree, byte-for-byte
identical to the `prl-step10-transfer-20261007` source for these paths:

- `graphics/trainers/front_pics/james_hns.png` — existing **combined** Jessie/James 64×64 battle portrait
- `graphics/trainers/front_pics/jessie_hns.png`
- `graphics/object_events/pics/people/rockets/james_hns.png`
- `graphics/object_events/pics/people/rockets/jessie_hns.png`
- `graphics/pokemon/meowth/overworld.png` — existing Meowth walking graphics

The Rocket duo's three trainer records already use `Class: Jessie James Hns`,
`Pic: James Hns`, `Double Battle: Yes`. The class displays `JESSIE &`,
and the trainer name is `JAMES`, yielding **JESSIE & JAMES** rather than
the usual generic Rocket battle header. The combined portrait remains intact.

## Fixes

### Slowpoke Well B1F
- Keep trigger coordinates (26,15), (27,15), (28,15).
- Read player X; place James at player's X and Jessie beside him (within
  corridor X 26..28), then walk both from the north until one tile ahead.
- Add Meowth as map object 28, behind the two, moving and facing with them.
- Preserve single persistent `TRAINER_GRUNT_21_HNS` double battle, normal
  no-rematch flag `FLAG_PJR_JESSIE_JAMES_1_DEFEATED`, Kurt/Proton and legacy
  Rocket rescue logic.
- Shorten post-battle marching from six tiles to three and fade the trio away
  as a group, avoiding the prolonged backtracking sequence.

### Goldenrod Underground Switches
- Branch approach by entry side X=18 or X=24 rather than always running left.
- Jessie and James stand just across from the player on either side.
- Add animated Meowth, local object 11, offset one tile behind.
- The trio withdraws to the side they approached from after victory;
  preserve `FLAG_PJR_JESSIE_JAMES_2_DEFEATED` and the dungeon switch story.

### Goldenrod Radio Tower 4F
- Reposition the existing Meowth (local object 7) beside Jessie and James,
  then face and remove it together with the two after the double battle.
- Bind Meowth's visibility to `FLAG_PJR_JESSIE_JAMES_3_DEFEATED` to prevent
  a lingering unmatched Rocket Pokémon after the duo is gone.
- Preserve the Meowth interaction/cry script and the Proton encounter.

## Testing checklist

Automated static source checks:
`python3 tools/pru/check_johto_rocket_trio.py`.

GitHub Actions must compile `pokehns.gba` and publish
`PRU-Consolidated-WIP.gba` before any ROM link is called downloadable.

**Still requires emulator gameplay testing with appropriate Johto progress:**

1. Enter Slowpoke Well via each of the three X=26/27/28 trigger tiles and
   check walk-in placement (no side overlap or sprites passing through walls).
2. Check the three visible characters turn towards the player, remain
   until dialogue/battle, and withdraw together without backpedal artifacts.
3. Check one-Pokémon party is warned and can return for a proper double
   battle; verify two-Pokémon double battle, combined portrait and outcome.
4. Check Kurt/Proton rescue, hide flags, map reloads, old progressed saves,
   and no rematches.
5. Check Underground entrances (X=18/24, Y=3/4), synchronized movement,
   post-battle hiding, and that wall/switch story remains passable.
6. Check Radio Tower duo + Meowth appearances, battle and cleanup.

A successful source compile alone does **not** certify these in-game checks.
