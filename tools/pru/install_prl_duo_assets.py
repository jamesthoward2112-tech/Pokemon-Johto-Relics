#!/usr/bin/env python3
"""Unpack approved PRL Jessie & James / Steevee & Neevee BG0 intro artwork.

Runs AFTER the unchanged, user-tested Crystal Redux presentation importer.
PRU ports PRL's approved PatternWeave task, IDs and trainer routing. The Jessie/James white palette-index bug is corrected losslessly after unpacking.
"""
import base64
import hashlib
import json
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "assets/prl_duo_20261011.json"


def restore_jessie_james_white() -> None:
    """Repair 4bpp BG0's opaque-white-as-transparent palette-index-0 error.

    The approved PRL asset has a near-white RGB555 colour (0x77BD) at index
    zero; GBA text BGs always treat nibble 0 as transparent, regardless of
    palette[0]. Fortunately indexes 14 and 15 are both exactly black.
    Merge those duplicate black entries, move WHITE into index 15, and
    replace every old 0-pixel with 15. This preserves ALL 15 distinct colours
    from the approved original without re-quantisation or altering tilemaps.
    """
    import struct

    folder = ROOT / "graphics/battle_transitions/prl"
    tile_file = folder / "jessie_james.4bpp"
    palette_file = folder / "jessie_james.gbapal"
    tiles = tile_file.read_bytes()
    palette = list(struct.unpack("<16H", palette_file.read_bytes()))

    assert len(tiles) == 16384, "Unexpected Jessie/James 512-tile 4bpp asset"
    assert palette[0] == 0x77BD, "White index changed: inspect donor before patching"
    assert palette[14] == palette[15] == 0x0000, "No redundant black slot available"

    def reindex(nibble: int) -> int:
        return 15 if nibble == 0 else 14 if nibble == 15 else nibble

    lut = bytes(((reindex(i >> 4) << 4) | reindex(i & 15))
                for i in range(256))
    fixed = tiles.translate(lut)
    assert fixed != tiles and all((b & 15) and (b >> 4) for b in fixed)
    palette[0] = 0x0000  # Reserved transparent; no pixels reference it now
    palette[15] = 0x77BD  # Original white, now fully opaque on BG0
    tile_file.write_bytes(fixed)
    palette_file.write_bytes(struct.pack("<16H", *palette))
    print("Restored PRL Jessie & James TEAM ROCKET whites: zero transparent pixels, "
          "all 15 original RGB555 colours preserved")


def unpack():
    bank = json.loads(PACK.read_text(encoding="utf-8"))
    assert bank["schema"] == "prl-duo-asset-pack-v1"
    raw = zlib.decompress(base64.b64decode(bank["zlib_base64"]))
    assert hashlib.sha256(raw).hexdigest() == bank["payload_sha256"]
    data = json.loads(raw)
    expected = {f"graphics/battle_transitions/prl/{name}.{ext}"
                for name in ("jessie_james", "eevee_twins")
                for ext in ("4bpp", "bin", "gbapal")}
    assert set(data) == expected, "Unapproved asset path in pack"
    for path, payload in data.items():
        bytes_ = base64.b64decode(payload, validate=True)
        ext = path.rsplit(".", 1)[-1]
        assert len(bytes_) == {"4bpp": 16384, "bin": 2048, "gbapal": 32}[ext]
        if ext == "bin":
            import struct
            tiles = struct.unpack("<1024H", bytes_)
            assert all(tile >> 12 == 13 and (tile & 0x3ff) < 512 for tile in tiles)
        target = ROOT / path
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists() or target.read_bytes() != bytes_:
            target.write_bytes(bytes_)
    restore_jessie_james_white()
    return expected


if __name__ == "__main__":
    unpack()