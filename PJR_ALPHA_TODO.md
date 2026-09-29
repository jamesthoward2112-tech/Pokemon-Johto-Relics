# PJR Alpha — To Do

## Progression / flow

- [x] Route 30 opening: remove the requirement to return home and speak to Mum before the Joey/Pidgey/Rattata roadblock clears. Once the Mr. Pokémon / Egg hand-off part of the opening is complete and the player has returned through the Elm/police sequence, Route 30 should be open automatically and the blocking NPC/Pokémon should be out of the way. Do not require a separate Mum conversation.

## Controls / battle QoL

- [x] Restore PJR's L = last-used Ball behaviour permanently. Current source has B_LAST_USED_BALL_BUTTON = L_BUTTON, but the L=A Button Mode overrides it and the battle code deliberately disables the last-ball shortcut in that mode. For PJR, L must always remain the last-ball control in battle; remove/disable the conflicting L=A mode or otherwise prevent it from stealing L. Keep R reserved for fast Run.

## Balance / gifts

- [x] Gift Cyndaquil in Azalea: reduce its gift level from Lv20 to Lv15. Lv20 is too high for the point it is obtained.

## Rocket / trainer presentation

- [ ] Jessie & James presentation/battles: every Jessie & James encounter must be a DOUBLE BATTLE, using a combined Jessie+James trainer battle sprite and a combined Jessie+James overworld sprite/event rather than two separate single-trainer objects. They should always appear and fight as a pair, never separately. Apply consistently to Slowpoke Well, Goldenrod Underground and Radio Tower (and any future Jessie & James encounters).