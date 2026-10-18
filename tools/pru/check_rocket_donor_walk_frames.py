#!/usr/bin/env python3
"""Verify compiled Jessie and James overworld walk frames against the original donor ROM.

Run after make hns so the PNGs have been converted by gbagfx. This checks the
actual nine consecutive 256-byte 4bpp frames, not merely a nine-frame table.
"""
from hashlib import sha256
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[2]
GFX = ROOT / "graphics/object_events/pics/people/rockets"
PAL = ROOT / "graphics/object_events/palettes"
EXPECTED_SHA256 = {
    "jessie": "5a86e6a4c72324ae7cb735961238f4bf6e6eb3eba7778595ddbba6a3dc0f85af",
    "james": "561b9149542d2ce7f06c4ea1509587e2c58ee362460d85e650c4f58df8e040d6",
}
EXPECTED_PALETTE = bytes.fromhex(
    "0e535f5b1f4b5b3a0f212d5627314110da5114398a205a6b314a0829ff7f0000"
)

rules = (ROOT / "graphics_file_rules.mk").read_text()
assert "-mwidth 2 -mheight 4" in rules
graphics_info = (ROOT / "src/data/object_events/object_event_graphics_info.h").read_text()
pic_tables = (ROOT / "src/data/object_events/object_event_pic_tables.h").read_text()
anims = (ROOT / "src/data/object_events/object_event_anims.h").read_text()
assert "sAnimTable_Standard" in anims

for who, expected in EXPECTED_SHA256.items():
    source = (GFX / f"{who}_hns.png").read_bytes()
    assert source[:8] == b"\x89PNG\r\n\x1a\n", who
    width, height = struct.unpack_from(">II", source, 16)
    assert (width, height) == (16, 9 * 32), (who, width, height)
    compiled = (GFX / f"{who}_hns.4bpp").read_bytes()
    assert len(compiled) == 9 * 256, (who, len(compiled))
    actual_sha = sha256(compiled).hexdigest()
    assert actual_sha == expected, (
        f"{who}: compiled 4bpp frames differ from original Team Rocket ROM: "
        f"{actual_sha} != {expected}"
    )
    frames = [compiled[i * 256:(i + 1) * 256] for i in range(9)]
    assert len(set(frames)) == 9, who
    for a, b in ((0, 1), (0, 2), (1, 2), (3, 4), (5, 6), (7, 8)):
        assert frames[a] != frames[b], (who, a, b)
    rgb555 = (PAL / f"{who}_hns.gbapal").read_bytes()
    assert rgb555 == EXPECTED_PALETTE, (who, rgb555.hex())
    obj_name = who.capitalize() + "_hns"
    info = graphics_info.split(f"gObjectEventGraphicsInfo_{obj_name} =", 1)[1].split(";", 1)[0]
    assert "sAnimTable_Standard" in info, who
    assert f"sPicTable_{obj_name}" in info, who
    table = pic_tables.split(f"sPicTable_{obj_name}[] =", 1)[1].split("};", 1)[0]
    for index in range(9):
        assert f"overworld_frame(gObjectEventPic_{obj_name}, 2, 4, {index})" in table, (who, index)
    print(f"OK: {who}: all nine directional donor frames, GBA palette, standard animation")

print("PASS: Jessie and James compiled overworld walking frames match original Team Rocket donor ROM")
