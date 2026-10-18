#!/usr/bin/env python3
"""Guard the user-approved Valkiri visual, move and purchasable item requirements."""
from pathlib import Path
import re

species = Path("src/data/pokemon/species_info/pru_custom.h").read_text()
block = species.split("[SPECIES_VALKYVOIR] =", 1)[1].split("[SPECIES_", 1)[0]
assert '.speciesName = _("Valkiri")' in block
assert ".levelUpLearnset = sValkiriLevelUpLearnset" in block
for t in (".frontPic = gMonFrontPic_Valkyvoir", ".backPic = gMonBackPic_Valkyvoir",
          ".palette = gMonPalette_Valkyvoir", ".shinyPalette = gMonShinyPalette_Valkyvoir"):
    assert t in block, t
levels = Path("src/data/pokemon/level_up_learnsets/pru.h").read_text()
learnset = levels.split("sValkiriLevelUpLearnset[]", 1)[1].split("LEVEL_UP_END", 1)[0]
for m in ("MOVE_ROUND", "MOVE_HYPER_VOICE", "MOVE_BOOMBURST"):
    assert m in learnset, m
assert "LEVEL_UP_MOVE( 0, MOVE_BOOMBURST)" in learnset

shop = Path("data/maps/GoldenrodCity_DepartmentStore_2F_hns/scripts.inc").read_text()
assert shop.split("GoldenrodDeptStore2_Pokemart:",1)[1].split("pokemartlistend",1)[0].count("ITEM_THROAT_SPRAY") == 1
items = Path("src/data/items.h").read_text()
assert "[ITEM_THROAT_SPRAY] =" in items
assert "HOLD_EFFECT_THROAT_SPRAY" in items

normal = Path("assets/pru_valkiri/normal.pal").read_text()
shiny = Path("assets/pru_valkiri/shiny.pal").read_text()
assert normal != shiny
assert "86 160 93" in normal and "71 117 213" in shiny
imported = Path("graphics/pokemon/prl_authoritative/valkyvoir")
if imported.exists():
    assert (imported / "normal.pal").read_text() == normal
    assert (imported / "shiny.pal").read_text() == shiny
    from PIL import Image
    for side in ("front", "back"):
        im = Image.open(imported / (side+".png")).convert("RGBA")
        colours = {rgb[:3] for rgb in im.getdata() if rgb[3]}
        assert (86,160,93) in colours, (side,"green normal missing")
        assert (71,117,213) not in colours, (side,"blue still normal")
print("PASS: Valkiri name, green normal/blue shiny, three sound moves and Goldenrod Throat Spray")
