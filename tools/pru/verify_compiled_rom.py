#!/usr/bin/env python3
"""Validate the compiled PRU ROM, not merely preprocessor/source files."""
from pathlib import Path
import json, re, struct

ROM_PATH = Path("pokehns.gba")
SYMS_PATH = Path("PRU-QA-symbols.sym")
assert ROM_PATH.is_file() and SYMS_PATH.is_file(), "Missing compiled GBA or nm symbols"
rom = bytearray(ROM_PATH.read_bytes())
assert len(rom) == 32 * 1024 * 1024, "Unexpected ROM length"

# Distinct internal name/version for this QA release, without changing BPEE
# game code used to associate existing compatible save files.
rom[0xA0:0xAC] = b"PRU OCT17 V2"
rom[0xBC] = 1
rom[0xBD] = (-(sum(rom[0xA0:0xBD]) + 0x19)) & 0xFF
ROM_PATH.write_bytes(rom)
assert (sum(rom[0xA0:0xBE]) + 0x19) % 256 == 0, "GBA header complement invalid"

symbols = {}
for line in SYMS_PATH.read_text().splitlines():
    m = re.match(r"^([0-9a-fA-F]{8})\s+\w\s+(.+)$", line)
    if m:
        symbols[m.group(2)] = int(m.group(1), 16)

def addr(name):
    assert name in symbols, f"Missing ROM symbol {name}"
    a = symbols[name]
    assert 0x08000000 <= a < 0x0A000000, f"Invalid ROM symbol {name}: {a:#x}"
    return a - 0x08000000

def read32(offset):
    return struct.unpack_from("<I", rom, offset)[0]

# Verify the game actually links nurse-side Chansey objects to their
# offered trainer battles. This catches stale map data and script pointers.
maps_checked = 0
for mapfile in sorted(Path("data/maps").glob("*/map.json")):
    map_data = json.loads(mapfile.read_text())
    for index, obj in enumerate(map_data.get("object_events", [])):
        if obj.get("graphics_id") != "OBJ_EVENT_GFX_NURSE_CHANSEY_HNS":
            continue
        map_name = map_data["name"]
        if map_name == "TestMap1_hns":
            continue
        script_name = obj["script"]
        event_start = addr(map_name + "_ObjectEvents") + index * 24
        linked = read32(event_start + 16)
        wanted = symbols.get(script_name)
        assert wanted is not None, f"Missing script symbol for {map_name}: {script_name}"
        assert linked == wanted, (
            f"{map_name} object {index} points to {linked:#x}, not {script_name} at {wanted:#x}"
        )
        assert script_name.startswith("PRU_ChanseyTrainer_") or script_name == "CherryGrove_Pokecenter_Chansey"
        maps_checked += 1
assert maps_checked >= 26, f"Only {maps_checked} compiled Chansey NPC links checked"
assert b"\xbd\xc2\xbb\xc8\xcd\xbf\xd3\x00\xeb\xd5\xe2\xe8\xe7\x00\xe8\xe3\x00\xe8\xe6\xd5\xdd\xe2\xab" in rom, "Compiled Chansey prompt absent"
print(f"BINARY_PASS: {maps_checked} compiled nurse-side Chansey event pointers, battle offer present")

# Scan actual generated wild tables for Route 30 in the produced ROM.
# 261 is Gen III internal species ID for Poochyena in this HnS build.
for time in ("Day", "Night"):
    sym = f"gRoute30_hns_{time}_LandMons"
    loc = addr(sym)
    slots = [tuple(rom[loc+i*4:loc+i*4+2]) + (struct.unpack_from("<H", rom, loc+i*4+2)[0],)
             for i in range(12)]
    matches = [(low, high) for low, high, species in slots if species == 261]
    assert matches and all(3 <= low <= high <= 5 for low, high in matches), (
        f"Route 30 {time} does not contain catchable level 3-5 Poochyena: {slots}"
    )
    print(f"BINARY_PASS: Route 30 {time}, Poochyena {matches}")

# Prove the *startup itself* dispatches to Last Wish (no Emerald movie).
# Looking only at MainCB2_EndIntro had wrongly passed the previous broken build.
copyright = addr("SetUpCopyrightScreen")
last_wish_thumb = (symbols["CB2_InitPRUHwlScene0"] | 1).to_bytes(4, "little")
emerald_scene_thumb = (symbols["Task_Scene1_Load"] | 1).to_bytes(4, "little")
copyright_code = rom[copyright:copyright + 4096]
assert last_wish_thumb in copyright_code, "Startup does NOT call Last Wish directly"
assert emerald_scene_thumb not in copyright_code, "Vanilla Emerald intro still referenced by startup"
assert "gTrainerFrontPic_ChanseyTwins" in symbols, "Custom Chansey portrait not linked"
source = Path("src/intro.c").read_text()
assert "CreateTask(Task_Scene1_Load, 0);" not in source, "Vanilla Emerald movie still callable in copyright startup"
assert "SetMainCallback2(CB2_InitPRUHwlScene0);" in source, "Last Wish dispatcher not linked"
print("BINARY_PASS: short startup -> Last Wish, no vanilla Emerald movie; custom Chansey portrait linked")
print("PRU_QA_HEADER: PRU OCT17 V2; BPEE preserved; GBA complement valid")
