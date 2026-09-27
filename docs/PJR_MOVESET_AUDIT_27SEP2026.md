# PJR moveset audit — 27 Sep 2026

## Rules
- Infinity donor species use Pokémon Infinity level-up data as the authority wherever the move exists in the PJR engine.
- Eeveelutions learn their type-defining Infinity evolution move at level 0 (immediately on evolution), then follow Infinity's level progression.
- Infinity-only moves are ported rather than silently substituted.
- Pressurize has no recoverable public effect text in the available Infinity game/wiki data. PJR adapts it as Rock status, 20 PP, sharply raises Sp. Def (+2). This is explicitly a PJR adaptation.
- Alphoracle keeps the PJR identity/type but uses Oculeus's level progression. Cosmic Ray becomes Fairy in PJR because the engine has no Cosmic type.
- Future PJR-original species are banked below so their learnsets are already decided when their species data is installed.

## Implemented Infinity donor learnsets
- Champeon: Evo Reversal; then Infinity progression through Extreme Speed Lv75.
- Lepideon: Evo Signal Beam; then Infinity progression through Tail Glow Lv70.
- Guardeon: Evo Iron Defense; then Infinity progression through Destiny Bond Lv70.
- Obsideon: Evo Pressurize; then Infinity progression through Head Smash Lv75.
- Toxeon: Evo Venom Swipe; then Infinity/Scorpeon progression through Nasty Plot Lv70.
- Sphynxeon: Evo Bonemerang; then Infinity progression through Future Sight + Pain Split Lv68.
- Omeon: Evo Vanish; then Infinity progression through Phantom Force Lv72.
- Jollibird: Evo Dazzling Gleam; Infinity progression through Lv100 Happy Hour/Wish/Aura Sphere/Parting Shot.
- Grimfowl: Evo Night Daze; Infinity progression through Nasty Plot Lv66.
- Kablowfish: Evo Explosion; Infinity progression including Kablow! Lv70, Iron Head Lv73, Metal Burst Lv80.
- Mystynx: Evo Brain Freeze; Jynx/Sorcerice progression through Blizzard Lv60, with Brain Freeze again at Lv40.
- Sunflorid: Evo Incinerate; Infinity progression through Discharge + Wild Charge Lv77.
- Terathwack: Evo Bone Sweep; Infinity progression through Last Resort Lv78.
- Alphoracle: Oculeus progression: Lv1 Hidden Power/Substitute/Psystrike/Lock-On, 20 Glare, 40 Ominous Wind, 60 Future Sight, 80 Cosmic Ray, 100 Déjà-vu.

## Ported Infinity-only moves
- Pressurize — Rock status, 20 PP; PJR adaptation: +2 Sp. Def.
- Venom Swipe — Poison physical, 100 BP, 90 Acc, 10 PP.
- Vanish — Ghost status, 5 PP; +2 Evasion.
- Bone Sweep — Ground physical, 90 BP, 100 Acc, 15 PP; hits both foes.
- Brain Freeze — Psychic special, 85 BP, 100 Acc, 10 PP; 10% freeze.
- Kablow! — Steel physical, 170 BP, 100 Acc, 5 PP; user detonates. PJR uses explosion semantics plus the engine's damaging-Spikes effect. Exact dual Spikes + Toxic Spikes follow-up is a battle-effect refinement, not a learnset blocker.
- Cosmic Ray — PJR Fairy special, 95 BP, 100 Acc, 10 PP; 15% flinch; pulse move.
- Déjà-vu — Psychic special, 105 BP, never misses, 10 PP.

## Existing baby starters
Keep current PJR baby learnsets:
- Scarabub -> Heracross Lv18.
- Skarmet -> Skarmory Lv18.
- Mootiny -> Miltank Lv18.

## Banked PJR-original evolution learnsets
These are design locks for when the species are installed. Level 0 is learned on evolution.

### Heracurion — Bug/Fighting
Evo move: Titan Horn.
- 0 Titan Horn
- 1 Tackle, Leer, Horn Attack, Endure
- 19 Fury Attack
- 27 Counter
- 35 Take Down
- 44 Reversal
- 48 Brick Break
- 52 Megahorn
- 56 Bulk Up
- 60 Close Combat
- 64 Stone Edge
- 68 Superpower

Titan Horn remains the locked Fighting physical 95 BP / 100 Acc contact move with a 20% Defense drop.

### Skarmadon — Steel/Flying
Evo move: Razor Dive.
- 0 Razor Dive
- 1 Leer, Peck, Sand Attack
- 19 Swift
- 25 Agility
- 37 Fury Attack
- 44 Iron Defense
- 49 Steel Wing
- 52 Drill Peck
- 56 Iron Head
- 60 Roost
- 64 Brave Bird
- 68 Heavy Slam

Razor Dive remains Steel physical 90 BP / 100 Acc, 30% Defense drop chance, no recoil.

### Miltitan — Normal/Fighting
Evo move: Stampede.
- 0 Stampede
- 1 Tackle, Growl, Defense Curl
- 13 Stomp
- 19 Milk Drink
- 26 Bide
- 34 Rollout
- 40 Bulk Up
- 43 Body Slam
- 48 Hammer Arm
- 52 High Horsepower
- 56 Milk Drink
- 60 Double-Edge
- 64 Close Combat
- 68 Heal Bell

Stampede remains Fighting physical 95 BP / 100 Acc with 20% flinch.

### Faeranium — Grass/Fairy
Evo move: Eternal Bloom.
- 0 Eternal Bloom
- 1 Tackle, Growl, Razor Leaf, Reflect
- 23 Synthesis
- 31 Body Slam
- 41 Light Screen
- 45 Eternal Bloom
- 50 Dazzling Gleam
- 54 Synthesis
- 58 Moonblast
- 62 Giga Drain
- 66 Aromatherapy
- 70 Solar Beam
- 74 Petal Blizzard

Eternal Bloom remains Fairy special 90 BP / 100 Acc, healing 50% of damage dealt.

### Pyroclast — Fire/Ground
Evo move: Magma Rift.
- 0 Magma Rift
- 1 Tackle, Leer, Smokescreen, Ember
- 21 Quick Attack
- 31 Flame Wheel
- 45 Magma Rift
- 50 Earth Power
- 54 Lava Plume
- 58 Flamethrower
- 62 Scorching Sands
- 66 Eruption
- 70 Earthquake
- 74 Overheat

Magma Rift remains Ground special 100 BP / 100 Acc with 20% burn.

### Feralodon — Water/Dark
Evo move: Death Roll.
- 0 Death Roll
- 1 Scratch, Leer, Rage, Water Gun
- 21 Bite
- 28 Scary Face
- 38 Slash
- 45 Death Roll
- 50 Crunch
- 54 Aqua Tail
- 58 Ice Fang
- 62 Dragon Dance
- 66 Liquidation
- 70 Hydro Pump
- 74 Superpower

Death Roll remains Water physical 95 BP / 100 Acc, biting move, 20% flinch.

### Shuckolosse — Bug/Rock fortress
Evolution move: Fortress Crush.
- 0 Fortress Crush
- 1 Withdraw, Constrict, Wrap, Encore
- 23 Safeguard
- 28 Bide
- 34 Stealth Rock
- 37 Rest
- 42 Sticky Web
- 46 Iron Defense
- 50 Power Split
- 54 Guard Split
- 58 Body Press
- 62 Rock Slide
- 66 Earthquake
- 70 Shell Smash

PJR move proposal for Fortress Crush: Rock physical, 90 BP / 100 Acc / 10 PP, calculates damage from Defense like Body Press. Banked pending species implementation.

### Donphalanx — Ground war-beast
Evolution move: Siege Tusk.
- 0 Siege Tusk
- 1 Horn Attack, Growl, Defense Curl
- 17 Flail
- 25 Fury Attack
- 33 Rollout
- 41 Rapid Spin
- 45 Iron Defense
- 49 Earthquake
- 54 Heavy Slam
- 58 High Horsepower
- 62 Stone Edge
- 66 Head Smash
- 70 Body Press

PJR move proposal for Siege Tusk: Ground physical, 95 BP / 100 Acc / 10 PP; sets Stealth Rock on the opposing side after a successful hit. Banked pending species implementation.

### Sudowoodo Relic evolution — Rock/Grass, name TBD
- 0 Wood Hammer
- 1 Rock Throw, Mimic, Flail
- 19 Low Kick
- 28 Rock Slide
- 37 Feint Attack
- 40 Leech Seed
- 46 Slam
- 50 Horn Leech
- 54 Curse
- 58 Synthesis
- 62 Stone Edge
- 68 Head Smash

### Pinsir Relic evolution — name/type finalisation still TBD
No permanent new signature is invented here. Use Pinsir's physical identity:
- 0 X-Scissor
- 1 Vise Grip, Bind
- 25 Seismic Toss
- 30 Guillotine
- 36 Focus Energy
- 43 Harden
- 49 Slash
- 54 Swords Dance
- 58 Brick Break
- 62 Close Combat
- 66 Megahorn
- 70 Superpower

## Drakeon — Shining Victory donor
Use the audited Shining Victory/Wyveon data:
- 0 Dragon Claw (PJR evolution move)
- 1 Helping Hand, Tackle, Tail Whip
- 5 Sand Attack
- 9 Dragon Rage
- 13 Quick Attack
- 17 Dragon Breath
- 21 Knock Off
- 25 Dragon Dance
- 29 Dragon Claw
- 33 Crunch
- 37 Dragon Tail
- 41 Iron Head
- 45 Dragon Rush
- 50 Zen Headbutt

## Relic special forms
Relic Gengar, Crobat, Houndoom, Kingdra, Tyranitar and Scizor are forms/variants rather than new evolutions. They should keep the core parent level-up identity, with a late-game curated boss/reward set rather than an artificial extra evolution learnset:
- Relic Gengar: Shadow Ball / Sludge Bomb / Hypnosis / Dream Eater, with Nasty Plot and Destiny Bond available.
- Relic Crobat: Brave Bird / Cross Poison / Leech Life / U-turn, with Roost and Haze available.
- Relic Houndoom: Flamethrower / Dark Pulse / Crunch / Nasty Plot, with Will-O-Wisp and Destiny Bond available.
- Relic Kingdra: Hydro Pump / Dragon Pulse / Ice Beam / Rain Dance, with Draco Meteor and Agility available.
- Relic Tyranitar: Stone Edge / Crunch / Earthquake / Dragon Dance, with Iron Head and Superpower available.
- Relic Scizor: Bullet Punch / X-Scissor / Iron Head / Swords Dance, with Roost and U-turn available.

## Remaining data work after learnsets
- Exact TM/tutor compatibility pass for donor species (level-up data is the priority and is implemented first).
- Exact dual-hazard secondary effect for Kablow! if desired beyond the current explosion + Spikes engine mapping.
- Species implementation for the banked future PJR-original evolutions/forms.
