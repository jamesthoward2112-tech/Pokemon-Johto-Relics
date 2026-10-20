#!/usr/bin/env python3
"""Check approved PRU visual overrides without touching save data."""
from pathlib import Path
from PIL import Image
root = Path("graphics/pokemon/skarmet")
for filename, size in (("front.png",(64,64)),("back.png",(64,64)),("icon.png",(32,64))):
    im=Image.open(root/filename)
    assert im.size==size,(filename,im.size)
    assert im.mode=="P",(filename,im.mode)
    assert im.info.get("transparency")==0,(filename,im.info.get("transparency"))
    assert max(im.getdata())<16,filename
    print("SKARMET",filename,"OK indexed GBA",size)
for name in ("normal.pal","shiny.pal"):
    pal=(root/name).read_text()
    assert pal.startswith("JASC-PAL\n0100\n16\n"),name
gfx=Path("src/data/graphics/pjr.h").read_text()
for symbol in ("FrontPic","BackPic","Palette","ShinyPalette","Icon"):
    assert "gMon"+symbol+"_Skarmet[]" in gfx
    assert "graphics/pokemon/skarmet/" in gfx
assert "graphics/pokemon/prl_authoritative/skarmet/" not in gfx
for name in ("FrontPic","BackPic","Palette","ShinyPalette","Icon"):
    assert "gMon"+name+"_Donphalanx[]" in gfx
assert gfx.count("graphics/pokemon/great_tusk/") >= 5
ic=Path("src/pokemon_icon.c").read_text()
assert "sPRUSkarmetIconPalette" in ic
assert "species == SPECIES_SKARMET" in ic and "return 9;" in ic
sync=Path("tools/pru/sync_prl_authoritative_sprites.py").read_text()
assert '"skarmet"' in sync and '"donphalanx"' in sync
print("SKARMET + DONPHALANX ART OVERRIDES PASS")
