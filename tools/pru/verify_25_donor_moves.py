#!/usr/bin/env python3
"""Verify PRU donor move names, base metadata and authentic PRL signature mechanics.

This is source regression coverage, not evidence of emulator or donor effect parity.
"""
from pathlib import Path
import re

ROOT = Path(".")
moves = (ROOT / "include/constants/moves.h").read_text()
info = (ROOT / "src/data/moves_info.h").read_text()
effects = (ROOT / "include/constants/battle_move_effects.h").read_text()
effect_table = (ROOT / "src/data/battle_move_effects.h").read_text()
battle = (ROOT / "include/constants/battle.h").read_text()
runtime = (ROOT / "src/battle_script_commands.c").read_text()
scripts = (ROOT / "data/battle_scripts_1.s").read_text()
donor = (ROOT / "tools/pru/donors/prl_custom_move_records.reference.h").read_text()

# name, type, power, accuracy, PP. Sources:
# 3: pinned PRL reference; 18: Procyon/Deneb wiki; 4: library-approved
# compatibility interpretations. The last four are NOT exact donor effect ports.
records = [
    ("EEVOBOOST", "NORMAL", 0, 0, 5),
    ("LOVELY_BITE", "FAIRY", 85, 100, 15),
    ("SHADOW_FANGS", "GHOST", 80, 100, 15),
    ("ANGRY_SWARM", "BUG", 80, 95, 15),
    ("CHROME_BALL", "STEEL", 90, 100, 10),
    ("CORNER", "DARK", 80, 100, 10),
    ("DARK_RESOLVE", "DARK", 130, 100, 5),
    ("DEADLY_TOXIN", "POISON", 120, 70, 5),
    ("GRIMEBUSTER", "POISON", 130, 90, 5),
    ("INFECTION", "POISON", 0, 100, 10),
    ("LIFE_DRAIN", "GHOST", 60, 100, 40),
    ("METAL_BLAST", "STEEL", 120, 85, 5),
    ("NEUROTOXIN", "POISON", 0, 90, 15),
    ("POSSESS", "GHOST", 120, 70, 10),
    ("QUICK_TURN", "DRAGON", 70, 100, 15),
    ("SHADOW_CLAMP", "GHOST", 90, 90, 10),
    ("SMOGSCREEN", "POISON", 65, 90, 25),
    ("SOULSHOCK", "GHOST", 65, 100, 10),
    ("STINK_SPRAY", "POISON", 0, 90, 20),
    ("VENGEANCE", "DARK", 60, 100, 10),
    ("VILE_VENOM", "POISON", 95, 90, 10),
    ("ASSIMILATE", "GRASS", 75, 100, 10),
    ("SPARKLINGSKY", "FIRE", 200, 100, 5),
    ("SUPER_GLITCH", "PSYCHIC", 250, 100, 1),
    ("TERROR_WAVE", "GHOST", 110, 85, 5),
]

def require(value: bool, reason: str) -> None:
    if not value:
        raise AssertionError(reason)

# Freeze preexisting PJR move IDs and ensure the new ones precede the movable Z/Max region.
index_start = moves.index("MOVE_IRON_FANGS,")
index_end = moves.index("MOVES_COUNT,", index_start)
custom = moves[index_start:index_end]
for suffix, typ, power, accuracy, pp in records:
    name = f"MOVE_{suffix}"
    require(len(re.findall(rf"\b{name}\b", custom)) == 1, f"enum missing/duplicated: {name}")
    match = re.search(rf"\[{name}\]\s*=\s*\{{(.*?)\n    \}},", info, re.S)
    require(match is not None, f"active data missing: {name}")
    block = match.group(1)
    for expected in (f".type = TYPE_{typ}", f".power = {power}", f".accuracy = {accuracy}", f".pp = {pp}"):
        require(expected in block, f"{name}: {expected}")
    require(".effect = EFFECT_PLACEHOLDER" not in block, f"forbidden placeholder effect: {name}")
require(len(records) == 25, "unexpected donor move count")
require(moves.index("MOVE_EEVOBOOST,") < moves.index("MOVES_COUNT,"), "Z/Max enum offset misplacement")

# Original PRL signature effects must not be accidentally downgraded.
require("EFFECT_PRU_EEVOBOOST" in effects, "separate +1 custom effect ID missing")
require("BattleScript_EffectPRUEevoboost" in effect_table, "native +1 effect mapping missing")
require("BattleScript_EffectPRUEevoboost::" in scripts, "native +1 stat script missing")
for stat in ("ATK", "DEF", "SPEED", "SPATK", "SPDEF"):
    require(f"setstatchanger STAT_{stat}, 1, FALSE" in scripts, f"PRU +1 boost missing: {stat}")
require("setstatchanger STAT_ATK, 2, FALSE" in scripts, "original +2 Z-move must remain")
for suffix, new_effect in (("LOVELY_BITE", "INFATUATION"), ("SHADOW_FANGS", "CURSE")):
    move = re.search(rf"\[MOVE_{suffix}\]\s*=\s*\{{(.*?)\n    \}},", info, re.S).group(1)
    require(f"MOVE_EFFECT_PRU_{new_effect}, .chance = 10" in move, f"{suffix}: 10% secondary missing")
    require("MOVE_EFFECT_BLEED, .chance = 10" in move, f"{suffix}: 10% Bleeding missing")
    require(f"case MOVE_EFFECT_PRU_{new_effect}:" in runtime, f"{suffix}: missing real battle handler")
    require(f"BattleScript_MoveEffectPRU{new_effect.title()}::" in scripts, f"{suffix}: narration missing")
    require(f"[MOVE_{suffix}]" in donor, f"{suffix}: pinned PRL reference missing")
print("PASS: 25 move records, append-only IDs and PRL signature status mechanics present")
print("NOTE: external donor secondary-effect parity, save migration and emulator QA remain")
