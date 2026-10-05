from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PARTY = ROOT / "src" / "data" / "trainers_hns.party"

BLOCKS = {
"TRAINER_WILL_2_HNS": """=== TRAINER_WILL_2_HNS ===
Name: WILL
Class: Elite Four Hns
Pic: Elite Four Will Hns
Gender: Male
Music: Hg Elite Four
Double Battle: Yes
AI: Smart Trainer / Prediction
Mugshot: Pink

Slowking Relic @ Covert Cloak
Level: 66
Ability: Regenerator
IVs: 31 HP / 0 Atk / 31 Def / 31 SpA / 31 SpD / 0 Spe
EVs: 252 HP / 0 Atk / 124 Def / 0 SpA / 132 SpD / 0 Spe
Sassy Nature
- Trick Room
- Psychic
- Scald
- Protect

Mystynx @ Light Clay
Level: 67
Ability: Snow Warning
IVs: 31 HP / 0 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe
EVs: 252 HP / 0 Atk / 0 Def / 4 SpA / 0 SpD / 252 Spe
Timid Nature
- Aurora Veil
- Blizzard
- Moonblast
- Fake Out

Exeggutor @ Sitrus Berry
Level: 67
Ability: Harvest
IVs: 31 HP / 0 Atk / 31 Def / 31 SpA / 31 SpD / 0 Spe
EVs: 252 HP / 0 Atk / 0 Def / 252 SpA / 4 SpD / 0 Spe
Quiet Nature
- Energy Ball
- Psychic
- Sleep Powder
- Protect

Grumpig @ Mental Herb
Level: 67
Ability: Own Tempo
IVs: 31 HP / 0 Atk / 31 Def / 31 SpA / 31 SpD / 0 Spe
EVs: 252 HP / 0 Atk / 4 Def / 0 SpA / 252 SpD / 0 Spe
Sassy Nature
- Imprison
- Trick Room
- Psychic
- Helping Hand

Alakazam Relic @ Life Orb
Level: 66
Ability: Magic Guard
IVs: 31 HP / 0 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe
EVs: 4 HP / 0 Atk / 0 Def / 252 SpA / 0 SpD / 252 Spe
Timid Nature
- Psychic
- Shadow Ball
- Dazzling Gleam
- Protect

Xatu @ Focus Sash
Level: 68
Ability: Magic Bounce
IVs: 31 HP / 0 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe
EVs: 4 HP / 0 Atk / 0 Def / 252 SpA / 0 SpD / 252 Spe
Timid Nature
- Tailwind
- Psychic
- Heat Wave
- Protect
""",
"TRAINER_KOGA_2_HNS": """=== TRAINER_KOGA_2_HNS ===
Name: KOGA
Class: Elite Four Hns
Pic: Elite Four Koga Hns
Gender: Male
Music: Hg Elite Four
Double Battle: Yes
AI: Smart Trainer / Prediction
Mugshot: Purple

Toxeon @ Focus Sash
Level: 67
Ability: Lightning Rod
IVs: 31 HP / 31 Atk / 31 Def / 0 SpA / 31 SpD / 31 Spe
EVs: 4 HP / 252 Atk / 0 Def / 0 SpA / 0 SpD / 252 Spe
Jolly Nature
- Toxic Spikes
- Poison Jab
- Crunch
- Protect

Crobat Relic @ Covert Cloak
Level: 68
Ability: Infiltrator
IVs: 31 HP / 31 Atk / 31 Def / 0 SpA / 31 SpD / 31 Spe
EVs: 252 HP / 4 Atk / 0 Def / 0 SpA / 0 SpD / 252 Spe
Jolly Nature
- Tailwind
- Taunt
- Cross Poison
- Super Fang

Muk @ Black Sludge
Level: 67
Ability: Poison Touch
IVs: 31 HP / 31 Atk / 31 Def / 0 SpA / 31 SpD / 31 Spe
EVs: 252 HP / 252 Atk / 0 Def / 0 SpA / 4 SpD / 0 Spe
Adamant Nature
- Gunk Shot
- Knock Off
- Venom Drench
- Protect

Tentacruel @ Assault Vest
Level: 67
Ability: Liquid Ooze
IVs: 31 HP / 0 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe
EVs: 4 HP / 0 Atk / 0 Def / 252 SpA / 0 SpD / 252 Spe
Timid Nature
- Scald
- Icy Wind
- Acid Spray
- Venoshock

Nidoking @ Life Orb
Level: 67
Ability: Sheer Force
IVs: 31 HP / 0 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe
EVs: 0 HP / 0 Atk / 4 Def / 252 SpA / 0 SpD / 252 Spe
Timid Nature
- Earth Power
- Venoshock
- Ice Beam
- Thunderbolt

Beedrill Relic @ Scope Lens
Level: 67
Ability: Sniper
IVs: 31 HP / 31 Atk / 31 Def / 0 SpA / 31 SpD / 31 Spe
EVs: 0 HP / 252 Atk / 0 Def / 0 SpA / 4 SpD / 252 Spe
Jolly Nature
- Megahorn
- Poison Jab
- Drill Run
- Protect
""",
"TRAINER_BRUNO_2_HNS": """=== TRAINER_BRUNO_2_HNS ===
Name: BRUNO
Class: Elite Four Hns
Pic: Elite Four Bruno Hns
Gender: Male
Music: Hg Elite Four
Double Battle: Yes
AI: Smart Trainer / Prediction
Mugshot: Orange

Steelix @ Smooth Rock
Level: 67
Ability: Sturdy
IVs: 31 HP / 31 Atk / 31 Def / 0 SpA / 31 SpD / 0 Spe
EVs: 252 HP / 4 Atk / 252 Def / 0 SpA / 0 SpD / 0 Spe
Impish Nature
- Sandstorm
- Stealth Rock
- Body Press
- Heavy Slam

Obsideon @ Clear Amulet
Level: 68
Ability: Sand Rush
IVs: 31 HP / 31 Atk / 31 Def / 0 SpA / 31 SpD / 31 Spe
EVs: 0 HP / 252 Atk / 0 Def / 0 SpA / 4 SpD / 252 Spe
Jolly Nature
- Rock Slide
- Head Smash
- Crunch
- Protect

Poliwrath @ Sitrus Berry
Level: 68
Ability: Water Absorb
IVs: 31 HP / 31 Atk / 31 Def / 0 SpA / 31 SpD / 31 Spe
EVs: 252 HP / 252 Atk / 0 Def / 0 SpA / 4 SpD / 0 Spe
Adamant Nature
- Wide Guard
- Drain Punch
- Liquidation
- Ice Punch

Heracurion @ Life Orb
Level: 67
Ability: Moxie
IVs: 31 HP / 31 Atk / 31 Def / 0 SpA / 31 SpD / 31 Spe
EVs: 0 HP / 252 Atk / 0 Def / 0 SpA / 4 SpD / 252 Spe
Jolly Nature
- Close Combat
- Megahorn
- Rock Slide
- Protect

Hitmonchan Relic @ Punching Glove
Level: 67
Ability: Iron Fist
IVs: 31 HP / 31 Atk / 31 Def / 0 SpA / 31 SpD / 31 Spe
EVs: 0 HP / 252 Atk / 0 Def / 0 SpA / 4 SpD / 252 Spe
Adamant Nature
- Drain Punch
- Thunder Punch
- Ice Punch
- Mach Punch

Machamp Relic @ Lum Berry
Level: 68
Ability: No Guard
IVs: 31 HP / 31 Atk / 31 Def / 0 SpA / 31 SpD / 0 Spe
EVs: 252 HP / 252 Atk / 0 Def / 0 SpA / 4 SpD / 0 Spe
Adamant Nature
- Dynamic Punch
- Rock Slide
- Knock Off
- Protect
""",
"TRAINER_KAREN_2_HNS": """=== TRAINER_KAREN_2_HNS ===
Name: KAREN
Class: Elite Four Hns
Pic: Elite Four Karen Hns
Gender: Male
Music: Hg Elite Four
Double Battle: Yes
AI: Smart Trainer / Prediction
Mugshot: Yellow

Umbreon @ Leftovers
Level: 68
Ability: Inner Focus
IVs: 31 HP / 31 Atk / 31 Def / 0 SpA / 31 SpD / 31 Spe
EVs: 252 HP / 0 Atk / 4 Def / 0 SpA / 252 SpD / 0 Spe
Careful Nature
- Snarl
- Foul Play
- Helping Hand
- Protect

Weavile @ Focus Sash
Level: 67
Ability: Pressure
IVs: 31 HP / 31 Atk / 31 Def / 0 SpA / 31 SpD / 31 Spe
EVs: 0 HP / 252 Atk / 0 Def / 0 SpA / 4 SpD / 252 Spe
Jolly Nature
- Fake Out
- Knock Off
- Triple Axel
- Ice Shard

Donphalanx @ Assault Vest
Level: 68
Ability: Intimidate
IVs: 31 HP / 31 Atk / 31 Def / 0 SpA / 31 SpD / 31 Spe
EVs: 252 HP / 252 Atk / 0 Def / 0 SpA / 4 SpD / 0 Spe
Adamant Nature
- High Horsepower
- Knock Off
- Rock Slide
- Ice Shard

Grimfowl @ Life Orb
Level: 68
Ability: No Guard
IVs: 31 HP / 0 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe
EVs: 4 HP / 0 Atk / 0 Def / 252 SpA / 0 SpD / 252 Spe
Timid Nature
- Tailwind
- Hurricane
- Night Daze
- Protect

Absol @ Scope Lens
Level: 67
Ability: Super Luck
IVs: 31 HP / 31 Atk / 31 Def / 0 SpA / 31 SpD / 31 Spe
EVs: 0 HP / 252 Atk / 0 Def / 0 SpA / 4 SpD / 252 Spe
Jolly Nature
- Sucker Punch
- Night Slash
- Psycho Cut
- Protect

Houndoom Relic @ Shuca Berry
Level: 69
Ability: Flash Fire
IVs: 31 HP / 0 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe
EVs: 4 HP / 0 Atk / 0 Def / 252 SpA / 0 SpD / 252 Spe
Timid Nature
- Heat Wave
- Dark Pulse
- Will-O-Wisp
- Protect
""",
"TRAINER_LANCE_2_HNS": """=== TRAINER_LANCE_2_HNS ===
Name: LANCE
Class: Champion Hns
Pic: Champion Lance Hns
Gender: Male
Music: Hg Champion
Double Battle: Yes
AI: Smart Trainer / Prediction
Mugshot: Blue

Drakeon @ Clear Amulet
Level: 69
Ability: Intimidate
IVs: 31 HP / 31 Atk / 31 Def / 0 SpA / 31 SpD / 31 Spe
EVs: 0 HP / 252 Atk / 0 Def / 0 SpA / 4 SpD / 252 Spe
Jolly Nature
- Dragon Claw
- Earthquake
- Rock Slide
- Protect

Skarmadon @ Covert Cloak
Level: 69
Ability: Sturdy
IVs: 31 HP / 31 Atk / 31 Def / 0 SpA / 31 SpD / 31 Spe
EVs: 252 HP / 4 Atk / 0 Def / 0 SpA / 0 SpD / 252 Spe
Jolly Nature
- Tailwind
- Brave Bird
- Iron Head
- Protect

Gyarados Relic @ Wacan Berry
Level: 69
Ability: Intimidate
IVs: 31 HP / 31 Atk / 31 Def / 0 SpA / 31 SpD / 31 Spe
EVs: 0 HP / 252 Atk / 0 Def / 0 SpA / 4 SpD / 252 Spe
Jolly Nature
- Waterfall
- Crunch
- Taunt
- Protect

Feralodon @ Life Orb
Level: 70
Ability: Tidal Roar
IVs: 31 HP / 31 Atk / 31 Def / 0 SpA / 31 SpD / 31 Spe
EVs: 0 HP / 252 Atk / 0 Def / 0 SpA / 4 SpD / 252 Spe
Adamant Nature
- Liquidation
- Dragon Claw
- Ice Fang
- Protect

Dragonite Relic @ Weakness Policy
Level: 68
Ability: Multiscale
IVs: 31 HP / 31 Atk / 31 Def / 0 SpA / 31 SpD / 31 Spe
EVs: 252 HP / 252 Atk / 0 Def / 0 SpA / 4 SpD / 0 Spe
Adamant Nature
- Dragon Dance
- Extreme Speed
- Dragon Claw
- Fire Punch

Charaxis @ Choice Band
Level: 68
Ability: Gale Wings
IVs: 31 HP / 31 Atk / 31 Def / 0 SpA / 31 SpD / 31 Spe
EVs: 0 HP / 252 Atk / 0 Def / 0 SpA / 4 SpD / 252 Spe
Jolly Nature
- Brave Bird
- Flare Blitz
- Earthquake
- Rock Slide
""",
}

raw = PARTY.read_bytes()
text = raw.decode("utf-8")
newline = "\r\n" if "\r\n" in text else "\n"

for label, block in BLOCKS.items():
    pattern = rf"^=== {re.escape(label)} ===\r?\n.*?(?=^=== |\Z)"
    replacement = block.replace("\n", newline) + newline
    text, count = re.subn(pattern, replacement, text, count=1, flags=re.M | re.S)
    if count != 1:
        raise SystemExit(f"Expected exactly one {label} block, replaced {count}")

PARTY.write_bytes(text.encode("utf-8"))
print("Updated five second-Elite-Four rematch blocks.")
