#!/usr/bin/env python3
"""Source regression for PRU Lum Berry's Bleeding recovery/text.

This is deliberately a source-level check; actual berry activation and
healthbox presentation require an in-game playtest with an existing save.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
constants = (ROOT / "include/constants/battle.h").read_text()
holds = (ROOT / "src/battle_hold_effects.c").read_text()
items = (ROOT / "src/data/items.h").read_text()
effects = (ROOT / "src/item.c").read_text()

status_any = re.search(r"^#define STATUS1_ANY\s+([^\n]+)", constants, re.M)
assert status_any and "STATUS1_BLEED" in status_any.group(1), "Bleeding must be included in cure-all bitmask"

start = holds.index("static enum ItemEffect TryCureAnyStatus(")
end = holds.index("\nenum HealAmount", start)
cure = holds[start:end]
assert "gBattleMons[battler].status1 & STATUS1_ANY" in cure
assert "IS_HNS && (gBattleMons[battler].status1 & STATUS1_BLEED)" in cure
assert 'StringCopy(gBattleTextBuff1, COMPOUND_STRING("bleeding"));' in cure
assert cure.index("STATUS1_BLEED") < cure.index("gBattleMons[battler].status1 = 0;")
assert "gBattleMons[battler].status1 = 0;" in cure

lum_start = items.index("[ITEM_LUM_BERRY]")
lum_end = items.index("[ITEM_SITRUS_BERRY]", lum_start)
lum = items[lum_start:lum_end]
assert "Bleeding, when held." in lum, "Lum Berry's bag description must name Bleeding"
assert ".holdEffect = HOLD_EFFECT_CURE_STATUS" in lum
assert ".effect = gItemEffect_FullHeal" in lum
assert "case ITEM3_STATUS_ALL:" in effects and "return STATUS1_ANY | STATUS1_TOXIC_COUNTER;" in effects

print("PASS: PRU Lum Berry item, status cure mask and Bleeding cure message")
