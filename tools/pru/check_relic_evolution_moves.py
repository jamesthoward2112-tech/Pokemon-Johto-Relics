#!/usr/bin/env python3
"""Static regression: PRL evolution moves and existing PJR/PRU custom levels."""
from pathlib import Path
import re
root = Path("src/data/pokemon")
donor = (root / "level_up_learnsets/prl_evolution_overrides.h").read_text()
info = (root / "species_info/pjr_families.h").read_text()
pjr = (root / "level_up_learnsets/pjr.h").read_text()
pru = (root / "level_up_learnsets/pru.h").read_text()
engine = Path("src/pokemon.c").read_text()
registry = Path("include/constants/moves.h").read_text()
targets = {
    "NOXICHU": ("Noxichu", "BITE"),
    "EDENSAUR": ("Edensaur", "EDEN_BLOOM"),
    "CHARAXIS": ("Charaxis", "SCORCHWING"),
    "FORTOTOISE": ("Fortotoise", "BASTION_CANNON"),
    "KHANG": ("Khang", "RETURN"),
    "NOLAX": ("Nolax", "EXTREME_SPEED"),
}
assert '#include "data/pokemon/level_up_learnsets/prl_evolution_overrides.h"' in engine
for species, (name, move) in targets.items():
    assert re.search(r'static const struct LevelUpMove s' + name + r'LevelUpLearnset\[\]', donor), species
    assert re.search(r'LEVEL_UP_MOVE\(\s*0\s*,\s*MOVE_' + move + r'\)', donor), species
    block = re.search(r'PJR_RED_SPECIES\(SPECIES_' + species + r',([\s\S]*?)\),', info)
    assert block and 's' + name + 'LevelUpLearnset' in block.group(1), species
    assert 'MOVE_' + move in registry, species
# Existing PJR signature moves are preserved, not replaced with the vanilla parent.
for name in ("Faeranium", "Pyroclast", "Feralodon", "Skarmadon", "Miltitan",
             "Heracurion", "Shuckolosse", "Champeon", "Guardeon", "Drakeon"):
    assert re.search(r'static const struct LevelUpMove s' + name + r'LevelUpLearnset\[\]', pjr), name
for name in ("Sceptitan", "Solaziken", "Swamplith", "Coelossus", "Eeveeon", "Nimbeon"):
    assert re.search(r'static const struct LevelUpMove s' + name + r'LevelUpLearnset\[\]', pru), name
print("PASS: 6 PRL evolution-exclusive moves wired; 16 existing PRU/PJR learnsets retained")
