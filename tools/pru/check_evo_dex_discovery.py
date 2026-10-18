#!/usr/bin/env python3
"""Source regression: visible, accurate EVO page for seen Pokémon in PRU."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]

def read(path):
    return (ROOT / path).read_text(encoding="utf-8")

dex = read("src/pokedex_plus_hgss.c")
config = read("include/config/pokedex_plus_hgss.h")

assert re.search(r"#define\s+POKEDEX_PLUS_HGSS\s+TRUE\b", config)
assert re.search(r"#define\s+HGSS_HIDE_UNSEEN_EVOLUTION_NAMES\s+FALSE\b", config)
assert re.search(r"#define\s+HGSS_HIDE_UNOWNED_EVOLUTION_METHODS\s+FALSE\b", config)

# The source is shared with non-PRU variants; permit seen access for HNS only.
seen_guard = "if (!sPokedexListItem->owned && (!IS_HNS || !sPokedexListItem->seen))"
area = dex.split("static void Task_SwitchScreensFromAreaScreen(u8 taskId)\n{", 1)[1]
area = area.split("//************************************", 1)[0]
assert seen_guard in area and "gTasks[taskId].func = Task_LoadStatsScreen;" in area
stats = dex.split("static void Task_HandleStatsScreenInput(u8 taskId)\n{", 1)[1]
stats = stats.split("#define ITEM_TAG", 1)[0]
assert seen_guard in stats and "sPokedexView->selectedScreen = EVO_SCREEN;" in stats

# The EVO page must show the true method of each enabled target species.
evo = dex.split("static void PrintEvolutionTargetSpeciesAndMethod(", 2)[-1]
# Above can include the declaration; use the fully-qualified function definition.
match = re.search(r"static void PrintEvolutionTargetSpeciesAndMethod\([^;]*?\)\n\{", dex, re.S)
assert match, "missing EVO detail formatter"
evo = dex[match.end():].split("static void Task_SwitchScreensFromEvolutionScreen", 1)[0]
for token in (
    "GetSpeciesEvolutions(species)", "IsSpeciesEnabled(targetSpecies)",
    "IsPruEvoDexSpecies(targetSpecies)",
    "case EVO_ITEM:", 'COMPOUND_STRING("Use {STR_VAR_2}")',
    "case IF_MIN_LEVEL:", 'COMPOUND_STRING("Lv ")',
    "evolutions[i].params[j].arg1",
):
    assert token in evo, f"missing EVO component: {token}"

# Confirm representative displayed evolutions from the approved 444 roster.
def mon_block(path, species):
    source = read(path)
    start = re.search(r"^\s*\[SPECIES_" + species + r"\]\s*=", source, re.M)
    assert start, species
    tail = source[start.end():]
    next_mon = re.search(r"^\s*\[SPECIES_[A-Z0-9_]+\]\s*=", tail, re.M)
    return tail[:next_mon.start()] if next_mon else tail

gen1 = "src/data/pokemon/species_info/gen_1_families.h"
gen3 = "src/data/pokemon/species_info/gen_3_families.h"

charizard = mon_block(gen1, "CHARIZARD")
assert re.search(r"EVO_ITEM,\s*ITEM_ANCIENT_STONE,\s*SPECIES_CHARAXIS,\s*CONDITIONS\(\{IF_MIN_LEVEL,\s*45\}\)", charizard)
gardevoir = mon_block(gen3, "GARDEVOIR")
assert re.search(r"EVO_ITEM,\s*ITEM_ANCIENT_STONE,\s*SPECIES_VALKYVOIR,\s*CONDITIONS\(\{IF_MIN_LEVEL,\s*45\}\)", gardevoir)
pikachu = mon_block(gen1, "PIKACHU")
assert re.search(r"EVO_ITEM,\s*ITEM_MOON_STONE,\s*SPECIES_NOXICHU", pikachu)

# PRU must not expose alternate-generation or out-of-roster branches.
roster = read("src/data/pokemon/pru_dex_order.h")
approved = set(re.findall(r"^\\s*(SPECIES_[A-Z0-9_]+),\\s*//\\s*\\d+", roster, re.M))
assert len(approved) == 444, len(approved)
assert "SPECIES_RAICHU_ALOLA" not in approved
assert "SPECIES_SYLVEON" not in approved
assert "IsPruEvoDexSpecies(i)" in dex, "pre-evolutions should use canonical roster"
assert 'sPruDexSpecies[i] == species' in dex, "EVO filter must use canonical 444 array"

# The Eevee page limit must be 5, not the old truncated 10/8 display.
assert "#define PRU_EEVEE_EVOS_PER_PAGE 5" in dex
assert "#define PRU_EEVEE_EVO_PAGES 3" in dex
assert "eeveePage" in dex
assert "Task_LoadEvolutionScreen;" in dex
assert "i < sPokedexView->sEvoScreenData.eeveePage * PRU_EEVEE_EVOS_PER_PAGE" in dex
start = mon_block(gen1, "EEVEE")
pru = start.split("#if IS_HNS", 1)[1].split("#else", 1)[0]
routes = re.findall(r"\\{EVO_ITEM,\\s*ITEM_[A-Z0-9_]+,\\s*(SPECIES_[A-Z0-9_]+)\\}", pru)
assert len(routes) == len(set(routes)) == 15, (len(routes), routes)
assert all(p in approved for p in routes), routes

print("PRU_EVO_DEX_DISCOVERY_PASS: 444-only species, 15 Eevee branches in 3 pages, relic EVO access")
