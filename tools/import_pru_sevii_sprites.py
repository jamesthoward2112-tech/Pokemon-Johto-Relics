#!/usr/bin/env python3
"""Install pinned Radical Red Sevii Noibat/Noivern battle sprites into PRU.

Sources are the original Radical-Red-Pokedex indexed battle sprite PNGs.
This script is a repeatable PRU-only asset derivation; it does not edit PJR.
It supplies correct front/back and shiny battle palettes. Separate 32x64
party icons and overworld/follower sprites remain art-integration gates.
"""
import hashlib
import pathlib
import shutil
import struct
import urllib.request

REVISION = "488a0918194d567b5f7b02c396118d51fb9c81ce"
EXPECTED = {
    ("noibat", "front"): "6afa35401bb397b4d52dc27b4bfaaa17a018a83895cabeba05985d1fabaf9ae1",
    ("noibat", "back"): "d61fe25075d923482733547dd1ea9e8076f8a795561db115a803f427f3403145",
    ("noibat", "front shiny"): "5d3d3535812e39eb898a9bd4d2b52356940b206baa4213e2ed6887a7928d3669",
    ("noibat", "back shiny"): "0d944d0373605bf0c830f3198310e08d707d3067090bb18f2de69cd79cf4977b",
    ("noivern", "front"): "bb383809f6b6f1bb8fb924d7b762eda239442f78ad426dba13805b1ad8ea6355",
    ("noivern", "back"): "726873522d471ec11823ae0ba8521784ba8bfbf787c7c3d78edff24e3a0ee61b",
    ("noivern", "front shiny"): "266a492f052245d391964d15896b51424f71d8c27d4b65ad0c2960108c",
    ("noivern", "back shiny"): "8e128c8ae1bb5ce654e3ff3165f56d7a5fd1006eb370ba5054607c93b4185f70",
}
DEX_IDS = {"noibat": 866, "noivern": 867}

def read_png(raw):
    assert raw[:8] == bytes((137, 80, 78, 71, 13, 10, 26, 10))
    assert struct.unpack(">II", raw[16:24]) == (64, 64), "Expected a GBA-sized single-frame sprite"
    offset = 8
    plte = None
    while offset < len(raw):
        size = struct.unpack(">I", raw[offset:offset+4])[0]
        typ = raw[offset+4:offset+8]
        chunk = raw[offset+8:offset+8+size]
        if typ == b"PLTE":
            plte = chunk
        if typ == b"IEND":
            break
        offset += 12+size
    assert plte is not None and 3 <= len(plte) <= 48 and len(plte) % 3 == 0
    colors = [list(plte[i:i+3]) for i in range(0,len(plte),3)]
    return colors + [[0, 0, 0]]*(16-len(colors))

def pal_text(colors):
    return "JASC-PAL\n0100\n16\n" + "\n".join(
        f"{r//8*8} {g//8*8} {b//8*8}" for r,g,b in colors
    ) + "\n"

def download(species, part):
    url = ("https://raw.githubusercontent.com/JwowSquared/Radical-Red-Pokedex/"
           + REVISION + "/graphics/species/"
           + part.replace(" ", "%20") + "/" + str(DEX_IDS[species]) + ".png")
    with urllib.request.urlopen(url, timeout=25) as r:
        raw = r.read()
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == EXPECTED[(species, part)], (species, part, digest)
    return raw

def main():
    for mon in ("noibat", "noivern"):
        base = pathlib.Path("graphics/pokemon") / mon
        assert base.is_dir(), base
        normal, back, shiny, shiny_back = (
            download(mon, part)
            for part in ("front", "back", "front shiny", "back shiny")
        )
        norm_pal = read_png(normal)
        shiny_pal = read_png(shiny)
        assert read_png(back) == norm_pal, "front/back palette mismatch: " + mon
        assert read_png(shiny_back) == shiny_pal, "shiny palette mismatch: " + mon
        # Source images are indexed 16-color PNGs; copy bytes without resampling.
        (base / "anim_front.png").write_bytes(normal)
        (base / "back.png").write_bytes(back)
        (base / "normal.pal").write_text(pal_text(norm_pal))
        (base / "shiny.pal").write_text(pal_text(shiny_pal))
        print("Installed pinned Radical Red Sevii", mon, "battle artwork")
    print("NOTE: PRU party icons and followers still need form-correct artwork.")

if __name__ == "__main__":
    main()
