#!/usr/bin/env python3
"""PRU Kanto: evolve late-game wild slots and enforce the canonical 444 roster.

Run after other encounter overlays and BEFORE `make hns`.
Without --write the script audits without modifying encounter files.
Only Kanto HNS encounters are affected; Johto and vanilla maps are untouched.
"""
import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path("src/data/wild_encounters.json")
DEX = Path("data/pru/PRU_National_Pokedex_2026-10-16.csv")
MIN_FINAL_LEVEL = 45

# All ordinary Gen 1-3 stage lines use their final Gen 1-3 stage; cross-gen
# evolutions (e.g. Tangrowth, Mamoswine, Ursaluna) are NEVER introduced.
# Branching evolutions choose one legal Gen 1-3 branch. PRU Relic species may
# still be directly encountered via their already-authorized separate slots.
FAMILIES = """
BULBASAUR IVYSAUR:VENUSAUR
CHARMANDER CHARMELEON:CHARIZARD
SQUIRTLE WARTORTLE:BLASTOISE
CATERPIE METAPOD:BUTTERFREE
WEEDLE KAKUNA:BEEDRILL
PIDGEY PIDGEOTTO:PIDGEOT
RATTATA:RATICATE
SPEAROW:FEAROW
EKANS:ARBOK
PICHU PIKACHU:RAICHU
SANDSHREW:SANDSLASH
NIDORAN_F NIDORINA:NIDOQUEEN
NIDORAN_M NIDORINO:NIDOKING
CLEFFA CLEFAIRY:CLEFABLE
VULPIX:NINETALES
IGGLYBUFF JIGGLYPUFF:WIGGLYTUFF
ZUBAT GOLBAT:CROBAT
ODDISH GLOOM:VILEPLUME
PARAS:PARASECT
VENONAT:VENOMOTH
DIGLETT:DUGTRIO
MEOWTH:PERSIAN
PSYDUCK:GOLDUCK
MANKEY:PRIMEAPE
GROWLITHE:ARCANINE
POLIWAG POLIWHIRL:POLIWRATH
ABRA KADABRA:ALAKAZAM
MACHOP MACHOKE:MACHAMP
BELLSPROUT WEEPINBELL:VICTREEBEL
TENTACOOL:TENTACRUEL
GEODUDE GRAVELER:GOLEM
PONYTA:RAPIDASH
SLOWPOKE:SLOWBRO
MAGNEMITE:MAGNETON
DODUO:DODRIO
SEEL:DEWGONG
GRIMER:MUK
SHELLDER:CLOYSTER
GASTLY HAUNTER:GENGAR
DROWZEE:HYPNO
KRABBY:KINGLER
VOLTORB:ELECTRODE
EXEGGCUTE:EXEGGUTOR
CUBONE:MAROWAK
KOFFING:WEEZING
RHYHORN:RHYDON
CHANSEY:BLISSEY
HORSEA SEADRA:KINGDRA
GOLDEEN:SEAKING
STARYU:STARMIE
ELEKID:ELECTABUZZ
MAGBY:MAGMAR
MAGIKARP:GYARADOS
PORYGON:PORYGON2
OMANYTE:OMASTAR
KABUTO:KABUTOPS
DRATINI DRAGONAIR:DRAGONITE
CHIKORITA BAYLEEF:MEGANIUM
CYNDAQUIL QUILAVA:TYPHLOSION
TOTODILE CROCONAW:FERALIGATR
SENTRET:FURRET
HOOTHOOT:NOCTOWL
LEDYBA:LEDIAN
SPINARAK:ARIADOS
CHINCHOU:LANTURN
TOGEPI:TOGETIC
NATU:XATU
MAREEP FLAAFFY:AMPHAROS
AZURILL MARILL:AZUMARILL
HOPPIP SKIPLOOM:JUMPLUFF
SUNKERN:SUNFLORA
WOOPER:QUAGSIRE
PINECO:FORRETRESS
SNUBBULL:GRANBULL
TEDDIURSA:URSARING
SWINUB:PILOSWINE
REMORAID:OCTILLERY
HOUNDOUR:HOUNDOOM
PHANPY:DONPHAN
SMOOCHUM:JYNX
LARVITAR PUPITAR:TYRANITAR
TREECKO GROVYLE:SCEPTILE
TORCHIC COMBUSKEN:BLAZIKEN
MUDKIP MARSHTOMP:SWAMPERT
POOCHYENA:MIGHTYENA
ZIGZAGOON:LINOONE
WURMPLE SILCOON:BEAUTIFLY
CASCOON:DUSTOX
LOTAD LOMBRE:LUDICOLO
SEEDOT NUZLEAF:SHIFTRY
TAILLOW:SWELLOW
WINGULL:PELIPPER
RALTS KIRLIA:GARDEVOIR
SURSKIT:MASQUERAIN
SHROOMISH:BRELOOM
SLAKOTH VIGOROTH:SLAKING
NINCADA:NINJASK
WHISMUR LOUDRED:EXPLOUD
MAKUHITA:HARIYAMA
NOSEPASS:NOSEPASS
SKITTY:DELCATTY
ARON LAIRON:AGGRON
MEDITITE:MEDICHAM
ELECTRIKE:MANECTRIC
GULPIN:SWALOT
CARVANHA:SHARPEDO
WAILMER:WAILORD
NUMEL:CAMERUPT
SPOINK:GRUMPIG
TRAPINCH VIBRAVA:FLYGON
CACNEA:CACTURNE
SWABLU:ALTARIA
BARBOACH:WHISCASH
CORPHISH:CRAWDAUNT
BALTOY:CLAYDOL
LILEEP:CRADILY
ANORITH:ARMALDO
FEEBAS:MILOTIC
SHUPPET:BANETTE
DUSKULL:DUSCLOPS
WYNAUT:WOBBUFFET
SNORUNT:GLALIE
SPHEAL SEALEO:WALREIN
CLAMPERL:HUNTAIL
BAGON SHELGON:SALAMENCE
BELDUM METANG:METAGROSS
"""

REPLACEMENTS = {
    "SPECIES_" + baby: "SPECIES_" + evolved
    for row in FAMILIES.strip().splitlines()
    for babies, evolved in [row.split(":")]
    for baby in babies.split()
    if baby != evolved
}
# Gen 8 species and their special form must never appear in PRU.
REPLACEMENTS.update({
    "SPECIES_URSALUNA": "SPECIES_URSARING",
    "SPECIES_URSALUNA_BLOODMOON": "SPECIES_URSARING",
    "SPECIES_KLEAVOR": "SPECIES_SCIZOR",
    "SPECIES_MAGNEZONE": "SPECIES_MAGNETON",
    "SPECIES_DUDUNSPARCE_THREE_SEGMENT": "SPECIES_DUNSPARCE",
})
KANTO_AREAS = (
    "MTMOON", "VIRIDIANFOREST", "DIGLETTSCAVE", "ROCKTUNNEL",
    "POWERPLANT", "SEAFOAMISLAND", "CERULEANCAVE", "SAFARIZONE",
    "POKEMONTOWER", "VICTORYROAD", "MTEMBER", "CINNABAR",
    "PALLETTOWN", "VIRIDIANCITY", "PEWTERCITY", "CERULEANCITY",
    "VERMILIONCITY", "LAVENDERTOWN", "CELADONCITY",
    "FUCHSIACITY", "SAFFRONCITY", "SEAFOM", "ROCKTUNNEL",
)

def is_kanto(map_name):
    if not isinstance(map_name, str) or not map_name.endswith("_HNS"):
        return False
    name = map_name.removeprefix("MAP_").removesuffix("_HNS")
    route = re.match(r"^ROUTE_?0*(\d+)(?:_|$)", name)
    if route:
        return 1 <= int(route.group(1)) <= 25
    flat = re.sub(r"[^A-Z0-9]", "", name)
    return any(flat.startswith(area) for area in KANTO_AREAS)

def allowed_species():
    with DEX.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 444, f"PRU roster changed: {len(rows)} != 444"
    return {row["Species_Constant"].strip() for row in rows}

def is_allowed(name, roster):
    if name in roster:
        return True
    # Battle-only forms share a canonical entry, rather than adding a 445th.
    return any(name.startswith(x) for x in (
        "SPECIES_UNOWN_", "SPECIES_CASTFORM_", "SPECIES_DEOXYS_"
    )) and any(name.startswith(x) and x in roster for x in (
        "SPECIES_UNOWN", "SPECIES_CASTFORM", "SPECIES_DEOXYS"
    ))

def iter_encounters(value):
    if isinstance(value, dict):
        if is_kanto(value.get("map")):
            yield value
        for nested in value.values():
            yield from iter_encounters(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from iter_encounters(nested)

def patch(data, roster):
    records = list(iter_encounters(data))
    if not records:
        raise ValueError("No Kanto HNS maps found; encounter format changed")
    changes = Counter()
    banned = []
    checked = 0
    for record in records:
        for field, table in record.items():
            if not field.endswith("_mons") or not isinstance(table, dict):
                continue
            mons = table.get("mons", [])
            if not isinstance(mons, list):
                continue
            for slot in mons:
                if not isinstance(slot, dict):
                    continue
                original = slot.get("species")
                if not isinstance(original, str):
                    continue
                # SPECIES_NONE is the deliberate placeholder for disabled
                # water/fishing/grass tables and is never an encounter.
                if original == "SPECIES_NONE":
                    continue
                checked += 1
                max_level = slot.get("max_level", slot.get("min_level", 0))
                if isinstance(max_level, int) and max_level >= MIN_FINAL_LEVEL:
                    updated = REPLACEMENTS.get(original, original)
                else:
                    updated = original
                # Out-of-dex species with a safe exact replacement are
                # corrected at ANY level, since they cannot be used in PRU.
                if not is_allowed(updated, roster):
                    updated = REPLACEMENTS.get(updated, updated)
                if updated != original:
                    slot["species"] = updated
                    changes[(original, updated)] += 1
                if not is_allowed(updated, roster):
                    banned.append((record["map"], field, updated))
    if banned:
        details = "\n".join(f"{m} {kind}: {species}" for m, kind, species in sorted(set(banned))[:40])
        raise ValueError("Kanto contains species outside PRU's 444:\n" + details)
    if checked == 0:
        raise ValueError("Kanto maps have no recognizable encounter slots")
    return records, checked, changes

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write corrected encounter JSON before compiling")
    args = parser.parse_args()
    source = json.loads(ROOT.read_text(encoding="utf-8"))
    maps, count, changes = patch(source, allowed_species())
    for (before, after), total in sorted(changes.items()):
        print(f"{before} -> {after}: {total} slots")
    print(f"PRU Kanto 444/evolution audit: {len(maps)} tables, {count} slots, {sum(changes.values())} corrected")
    if args.write:
        if changes:
            ROOT.write_text(json.dumps(source, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("PASS: Kanto wild tables contain only canonical species, with mapped Lv45+ forms evolved")
    elif changes:
        raise SystemExit("Kanto still needs the corrections above; run with --write")

if __name__ == "__main__":
    main()
