#!/usr/bin/env python3
"""Trainer-only Kimono Ghost appearance checks for PRU.

Proves source selectors, donor art, story status and roster invariants. Battle
rendering still needs live gameplay visual validation on the user's saved game.
"""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[2]
visuals = (root / "src/battle_gfx_sfx_util.c").read_text()
asset_refs = (root / "src/data/graphics/pjr.h").read_text()
config = (root / "include/config/species_enabled.h").read_text()
party = (root / "src/data/trainers_hns.party").read_text()
elm = (root / "data/maps/NewBarkTown_Lab_hns/scripts.inc").read_text()
gate = (root / "data/maps/ReceptionGate_hns/scripts.inc").read_text()

assert re.search(r"#define P_MEGA_EVOLUTIONS\s+FALSE", config), "Mega forms must stay disabled"
assert "#include \"constants/opponents_hns.h\"" in visuals
assert "GetPruKimonoGhostVisual" in visuals
assert '#include "battle_setup.h"' in visuals
assert "switch (TRAINER_BATTLE_PARAM.opponentA)" in visuals
for condition in ("!IS_HNS", "BATTLE_TYPE_TRAINER", "IsOnPlayerSide(battler)",
                  "gBattleSpritesDataPtr->battlerData[battler].transformSpecies != SPECIES_NONE"):
    assert condition in visuals, f"Missing opponent-only safeguard: {condition}"

visuals_expected = {
    "ZUKI": ("GENGAR", "Gengar"),
    "NAOKO": ("MISDREAVUS", None),
    "MIKI": ("BANETTE", "Banette"),
    "SAYO": ("SABLEYE", "Sableye"),
    "KUNI": ("DUSCLOPS", None),
}
for who, (species, art) in visuals_expected.items():
    assert f"case TRAINER_{who}_HNS:" in visuals
    assert f"species == SPECIES_{species}" in visuals
    assert f"=== TRAINER_{who}_HNS ===" in party
    if art is not None:
        assert f"gMonFrontPic_{art}Mega" in visuals
        assert f"gMonPalette_{art}Mega" in visuals
        assert f'gMonFrontPic_{art}Mega[] = INCBIN_U32("graphics/pokemon/{art.lower()}/mega/front.4bpp.smol")' in asset_refs
        assert f'gMonPalette_{art}Mega[] = INCBIN_U16("graphics/pokemon/{art.lower()}/mega/normal.gbapal")' in asset_refs
        assert (root / f"graphics/pokemon/{art.lower()}/mega/front.png").exists()
        assert (root / f"graphics/pokemon/{art.lower()}/mega/normal.pal").exists()
    else:
        assert f"KIMONO_GHOST_VISUAL_{species}_RITUAL" in visuals

assert "DecompressDataWithHeaderWram(gMonFrontPic_GengarMega" in visuals
assert "DecompressDataWithHeaderWram(gMonFrontPic_BanetteMega" in visuals
assert "DecompressDataWithHeaderWram(gMonFrontPic_SableyeMega" in visuals
assert "GetMonSpritePalFromSpeciesAndPersonality(species, TRUE" in visuals
assert "setvar VAR_ECRUTEAK_CITY_THEATER, 4" in elm
assert "goto_if_lt VAR_ECRUTEAK_CITY_THEATER, 8" in (root / "data/maps/ReceptionGate_hns/scripts.inc").read_text()

print("PASS: five Kimono Ghost visuals restricted to trainer art, no Mega engine/roster change")
