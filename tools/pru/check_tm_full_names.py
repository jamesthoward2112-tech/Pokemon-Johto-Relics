#!/usr/bin/env python3
"""PRU/HNS: all active TMs and HMs must show both number and correct move.
Existing item IDs and the other game engines' item names must remain unchanged.
"""
from pathlib import Path
import re

items = Path("src/data/items.h").read_text()
defs = Path("include/constants/tms_hms.h").read_text().split("#else", 1)[0]
tm_text = defs.split("#define FOREACH_TM(F)", 1)[1].split("#define FOREACH_HM(F)", 1)[0]
hm_text = defs.split("#define FOREACH_HM(F)", 1)[1]
tm_moves = re.findall(r"\bF\(([A-Z_0-9]+)\)", tm_text)
hm_moves = re.findall(r"\bF\(([A-Z_0-9]+)\)", hm_text)
assert len(tm_moves) == 92, len(tm_moves)
assert len(hm_moves) == 8, len(hm_moves)

checked = 0
for kind, moves in (("TM", tm_moves), ("HM", hm_moves)):
    for n, move in enumerate(moves, start=1):
        key = (f"ITEM_TM_{move}" if n <= 50 else f"ITEM_TM{n}") if kind == "TM" else f"ITEM_HM_{move}"
        expected = f"{kind}{n:02d} - {move.replace('_', ' ')}"
        assert len(expected) <= 20, expected
        block = re.search(r"\[" + re.escape(key) + r"\]\s*=\s*(?://[^\n]*\n\s*)?\{", items)
        assert block, (key, "missing item")
        source = items[block.end():block.end()+300]
        assert re.search(
            r"#if IS_HNS\s+\.name = ITEM_NAME\(" + re.escape(f'"{expected}"') + r"\),"
            r"\s+#else\s+\.name = ITEM_NAME\(\"[^\"]+\"\),\s+#endif", source
        ), (key, "wrong HNS name or missing legacy preservation")
        checked += 1

assert checked == 100
# TM93-100 are inactive placeholders; do not pretend they have real moves.
for n in range(93, 101):
    assert f'[ITEM_TM{n}]' in items, ("missing placeholder", n)
    assert f'TM{n} - ' not in items, ("invented placeholder move", n)
print("PASS: all 92 valid HNS TMs and eight HMs have number + real move; legacy retained.")
