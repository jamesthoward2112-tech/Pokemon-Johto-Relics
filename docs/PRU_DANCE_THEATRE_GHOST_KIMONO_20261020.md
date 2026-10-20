# PRU — Dance Theatre Ghost Kimono Teams (20 October 2026)

## Player instruction and exact scope
The user has **eight Johto badges**, was stopped at the Pokémon League reception gate with the "LEGENDARY" message, and recognised they had **forgotten to visit Professor Elm**. The existing story method is correct and MUST stay exactly as it is:
1. Return to Professor Elm in New Bark Town for his Master Ball/Kimono Girls direction.
2. Go to the Ecruteak Dance Theatre and face Zuki, Naoko, Miki, Sayo and Kuni.
3. Continue the inherited Ho-Oh or Lugia event, and re-enter reception gate when theatre progress reaches state 8.
4. Proceed through Victory Road to the Johto League.

**Do not change** the Elm script, existing theatre scene, map flags, Rocket/Silver events, the legendary branch, Ho-Oh/Lugia encounters, route guard, five-battle ordering, totem boosts, or the user's save layout. The user explicitly rescinded the earlier suggestion to bypass or auto-unlock the story after badge eight.

## Only change requested now: replace their five Eeveelution teams
Keep five independent level-48 singles (one signature Ghost each, as in the original gauntlet), with their individual intros, boosts and scripts:

| Kimono Girl | Old Eeveelution | New Ghost | Four moves |
| --- | --- | --- | --- |
| Zuki | Omeon | Gengar | Eerie Fog / Shadow Ball / Sludge Bomb / Hypnosis |
| Naoko | Lepideon | Misdreavus | Eerie Fog / Shadow Ball / Psychic / Pain Split |
| Miki | Champeon | Banette | Eerie Fog / Shadow Claw / Will-O-Wisp / Knock Off |
| Sayo | Guardeon | Sableye | Eerie Fog / Shadow Ball / Recover / Confuse Ray |
| Kuni | Drakeon | Dusclops | Eerie Fog / Night Shade / Will-O-Wisp / Pain Split |

Each uses the **already imported PRL Eerie Fog** (8 turns; 20% protection against incoming damage to Ghost/Psychic defenders) for an unmistakable ghostly ceremony. No extra species IDs. These are Kanto, Johto and Hoenn Pokémon in the approved 444 roster. Avoid Eeveelutions, reserved as Steevee & Neevee's signature group in the later Elite 20.

## Later postgame encounters and Elite 20
**Do not modify** Miharu, Youko and Shizuko's existing Sinjoh progression or teams in this pre-League patch. Their future revisited encounters can be redesigned for Elite 20 (specific number/pairings not final), subject to separate planning. The main Elite 20 and Battle Frontier remain post-Champion.

## QA and release gates
- Source regression: `tools/pru/check_kimono_ghost_teams.py` confirms five valid level-48 singles with Eerie Fog, no Eeveelution and unchanged Elm/Legendary/route milestones.
- Full `make hns`, existing 444/custom systems and sprite checks, binary audit and mGBA boot must pass in CI.
- Release a **new, uniquely tagged raw 32 MiB `.gba`**, NO ZIP. Keep the previous Eight-Badge release intact.
- User should back up existing eight-badge `.sav` and verify Elm -> Dance Theatre -> five battles -> Ho-Oh/Lugia -> reception gate. CI does **not** replace a full existing-save gameplay test.
- Potential separate fog issue: the inherited engine also has a generic fog-based accuracy reduction; review against PRL semantics in a future battle-mechanics audit rather than altering unrelated mechanics in this narrowly scoped trainer change.
