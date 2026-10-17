# PRU Gym Leader overhaul — 17 October 2026

Base source: pru/noxichu-last-wish-title-test-20261017, commit 391aedfac844bd354d929476192a3868d4507cbf.

This is a separate PRU development branch: **do not modify PJR** or overwrite the previously successful Noxichu test ROM. Trainer source is changed; gameplay has not yet been verified.

## First Gym teams

- FALKNER_1: Hoothoot Lv11, Natu Lv12, Skarmet Lv12, Pidgeotto Lv14
- BUGSY_1: Pineco Lv16, Ledian Lv17, Spinarak Lv16, Scarabub Lv17, Scyther Lv19
- WHITNEY_1: Clefairy Lv22, Teddiursa Lv22, Aipom Lv22, Mootiny Lv23, Miltank Lv24
- MORTY_1: Haunter Lv26, Gemlin Lv25, Omeon Lv27, Misdreavus Lv26, Gengar Lv28
- CHUCK_1: Hitmontop Lv33, Primeape Lv33, Heracross Lv34, Champeon Lv34, Poliwrath Lv36
- JASMINE_1: Skarmory Lv37, Guardeon Lv38, Magneton Lv37, Scizor Lv38, Steelix Lv40
- PRYCE_1: Dewgong Lv36, Sneasel Lv36, Jynx Lv37, Jollibird Lv38, Piloswine Lv40
- CLAIR_1: Dragonair Lv44, Gyarados Lv45, Altaria Lv45, Mawyrm Lv46, Dragonite Lv47, Kingdra Lv48

## PJR reward bundle — preserved without changing battle scripts

| Leader | Bonus | TM | Item |
|---|---:|---|---|
| Falkner | £10,000 | Roost | Sharp Beak |
| Bugsy | £10,000 | U-turn | Silver Powder |
| Whitney | £10,000 | Return | Eviolite |
| Morty | £10,000 | Shadow Ball | Spell Tag |
| Chuck | £10,000 | Focus Punch | Black Belt |
| Jasmine | £10,000 | Iron Tail | Metal Coat |
| Pryce | £10,000 | Hail | Never-Melt Ice |
| Clair | £10,000 | Dragon Pulse | Dragon Fang |

## Technical record

- All 30 trainer-party variants touched: 8 original, 6 badge-dependent variants, 8 first rematch, 8 post-OBC rematch.
- First gyms gain stage-appropriate Skarmet, Scarabub, Mootiny/Miltank, Ghost Omeon/Gemlin, Fighting Champeon, Steel Guardeon, Ice Jollibird and Dragon/Steel Mawyrm.
- Existing trainer IDs, gym badge scripts, battle-type flags, £10,000, TM and item reward flags untouched.
- Script sanity remaining: test full bag, reward retries, badge order, sprite assets, movesets, first/rematch flow, save compatibility; successful ROM compilation is not equivalent to gameplay approval.
