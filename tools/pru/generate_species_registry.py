#!/usr/bin/env python3
"""Generate PRU per-Pokemon reference files from pinned PRL and live PJR sources.

This is a source/provenance inventory, NOT a claim a PRL source has been ported
or that an NPC can actually spawn the species in the current playable ROM.
"""
import argparse, csv, hashlib, json, re
from pathlib import Path

SOURCE_PRL = "6ee9b984521ac6f2beaf995f771a726379e55c88"
SPECIES_PATTERN = re.compile(r"(?m)^[ \t]*\[(SPECIES_[A-Z0-9_]+)\][ \t]*=\s*\{")
LEARN_PATTERN = re.compile(r"static\s+const\s+struct\s+LevelUpMove\s+(s\w+)\[\]\s*=\s*\{(.*?)\};", re.S)
MOVE_PATTERN = re.compile(r"LEVEL_UP_MOVE\(\s*(\d+)\s*,\s*MOVE_([A-Z0-9_]+)\s*\)")
PROPS = ("baseHP","baseAttack","baseDefense","baseSpAttack","baseSpDefense",
         "baseSpeed","types","abilities","evolutions","levelUpLearnset",
         "teachableLearnset","eggMoveLearnset","frontPic","backPic",
         "iconSprite","palette","shinyPalette","frontPicYOffset",
         "backPicYOffset","iconPalIndex")

RR = {
 "NOIBAT": dict(form="Seviian",types="Rock/Ghost",
    stats=[40,45,35,30,40,55],abilities=["Levitate","Rock Head","Sturdy (hidden)"],
    evolution="Lv36 -> Noivern (Sevii)",
    source="https://romhackdex.net/radical-red/pokedex/noibat-sevii/",
    moves=[(1,"Screech"),(1,"Supersonic"),(1,"Bite"),(5,"Astonish"),(11,"Rock Throw"),
           (13,"Magnitude"),(16,"Shadow Sneak"),(18,"Ominous Wind"),(23,"Rock Blast"),
           (27,"Curse"),(31,"Shadow Claw"),(35,"Rock Slide"),(40,"Phantom Force"),
           (43,"Super Fang"),(48,"Destiny Bond"),(54,"Stone Edge"),(58,"Poltergeist")]),
 "NOIVERN": dict(form="Seviian",types="Rock/Ghost",
    stats=[85,102,80,70,80,123],abilities=["Levitate","Rock Head","Sturdy (hidden)"],
    evolution="evolves from Seviian Noibat at Lv36",
    source="https://romhackdex.net/radical-red/pokedex/noivern-sevii/",
    moves=[(0,"Spirit Shackle"),(1,"Spirit Shackle"),(1,"Screech"),(1,"Moonlight"),
           (1,"Supersonic"),(1,"Bite"),(5,"Astonish"),(11,"Rock Throw"),
           (13,"Magnitude"),(16,"Shadow Sneak"),(18,"Ominous Wind"),(23,"Rock Blast"),
           (27,"Curse"),(31,"Shadow Claw"),(35,"Rock Slide"),(40,"Phantom Force"),
           (43,"Super Fang"),(48,"Destiny Bond"),(54,"Stone Edge"),
           (58,"Poltergeist"),(64,"Head Smash")]),
 "WOOPER_PALDEA": dict(form="Paldean",types="Poison/Ground",
    stats=[55,45,45,25,25,15],abilities=["Unaware","Poison Point","Water Absorb (hidden)"],
    evolution="Lv20 -> Clodsire",
    source="https://romhackdex.net/radical-red/pokedex/wooper-paldea/",
    moves=[(1,"Mud Shot"),(1,"Tail Whip"),(4,"Tackle"),(8,"Poison Tail"),
           (12,"Toxic Spikes"),(16,"Slam"),(21,"Yawn"),(24,"Poison Jab"),
           (28,"Sludge Wave"),(32,"Amnesia"),(36,"Toxic"),(40,"Earthquake")]),
 "CLODSIRE": dict(form="Paldean evolution",types="Poison/Ground",
    stats=[130,75,60,45,100,20],abilities=["Unaware","Poison Point","Water Absorb (hidden)"],
    evolution="evolves from Paldean Wooper at Lv20",
    source="https://romhackdex.net/radical-red/pokedex/clodsire/",
    moves=[(1,"Mud Shot"),(1,"Tail Whip"),(4,"Tackle"),(8,"Poison Tail"),
           (12,"Toxic Spikes"),(16,"Slam"),(21,"Yawn"),(24,"Poison Jab"),
           (30,"Sludge Wave"),(34,"Megahorn"),(40,"Toxic"),(44,"Earthquake")])
}
# Explicit overrides are reference decisions; PRU runtime mechanics still require integration.
OLD_NAMES = {"HYENADON": "RETIRED: PRL Skulberus supersedes this species"}
REQUIRED_GRAPHICS = ("front.png","back.png","icon.png","normal.pal","shiny.pal")
ROOTS = [
 ("PRL-Kanto","prl","src/data/pokemon/species_info/gen_1_families.h"),
 ("PRL-Hoenn","prl","src/data/pokemon/species_info/gen_3_families.h"),
 ("PJR-Johto","pjr","src/data/pokemon/species_info/gen_2_families.h"),
 ("PJR-custom","pjr","src/data/pokemon/species_info/pjr_families.h"),
 ("PRL-custom","prl","src/data/pokemon/species_info/prl_custom.h"),
 ("PRL-later-gen4","prl","src/data/pokemon/species_info/gen_4_families.h"),
 ("PRL-later-gen5","prl","src/data/pokemon/species_info/gen_5_families.h"),
 ("PRL-Noibat","prl","src/data/pokemon/species_info/gen_6_families.h"),
 ("PRL-later-gen7","prl","src/data/pokemon/species_info/gen_7_families.h"),
 ("PRL-later-gen8","prl","src/data/pokemon/species_info/gen_8_families.h"),
 ("PRL-later-gen9","prl","src/data/pokemon/species_info/gen_9_families.h"),
]
ALWAYS_FROM_PRL = {"NOXICHU","EEVEEON","NIMBEON","TOXEON","NOLAX","KHANG"}
CUSTOM_JOHTO_PREFER_PJR = {"SCARABUB","SKARMET","MOOTINY","ALPHORACLE",
 "HERACURION","SKARMADON","MILTITAN","SHUCKOLOSSE","DONPHALANX",
 "MYSTYNX","PINSIREX","FAERANIUM","PYROCLAST","FERALODON",
 "CHAMPEON","LEPIDEON","SPHYNXEON","GUARDEON","OBSIDEON",
 "OMEON","DRAKEON","JOLLIBIRD","GRIMFOWL","KABLOWFISH","SUNFLORID",
 "GHOULBAT","OSTEODIAN","MAROGHOST"}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def source_defs(root):
    mapping={}
    for f in (root / "src/data/pokemon/level_up_learnsets").glob("*.h"):
        try: content=f.read_text(errors="replace")
        except OSError: continue
        for match in LEARN_PATTERN.finditer(content):
            mapping[match.group(1)]={"path":str(f.relative_to(root)),
              "moves":[{"level":int(m.group(1)),"move":m.group(2)} for m in MOVE_PATTERN.finditer(match.group(2))],
              "full_source":match.group(0)}
    return mapping

def species_blocks(path):
    t=path.read_text(errors="replace")
    matches=list(SPECIES_PATTERN.finditer(t))
    for i,m in enumerate(matches):
        end=matches[i+1].start() if i+1<len(matches) else len(t)
        yield m.group(1).removeprefix("SPECIES_"), t[m.start():end]

def prop(block,name):
    # A source declaration can contain #if expressions and runtime macros.
    m=re.search(r"\."+re.escape(name)+r"\s*=\s*(.*?)(?:,\s*(?=\.|$)|\n)",block,re.S)
    return re.sub(r"\s+"," ",m.group(1)).strip()[:500] if m else None

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--prl",type=Path,required=True)
    p.add_argument("--pjr",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    prl,pjr,out=a.prl.resolve(),a.pjr.resolve(),a.out.resolve()
    out.mkdir(parents=True,exist_ok=True)
    for root in (prl,pjr):
        if not (root/"src/data/pokemon/species_info").is_dir():
            raise SystemExit("Missing source tree: "+str(root))
    learns={"prl":source_defs(prl),"pjr":source_defs(pjr)}
    species={}
    for group,which,rel in ROOTS:
        root=prl if which=="prl" else pjr
        f=root/rel
        if not f.exists():continue
        for name,raw in species_blocks(f):
            if name in OLD_NAMES: continue
            if name in species and group=="PRL-custom" and name in CUSTOM_JOHTO_PREFER_PJR:continue
            if name in species and group=="PJR-custom" and name in ALWAYS_FROM_PRL:continue
            if name in species and group=="PRL-Noibat" and name not in RR:continue
            data={"species_constant":"SPECIES_"+name,"name":name,"source_tier":group,
                  "source_root":which,"source_file":rel,
                  "source_file_sha256":sha(f),
                  "source_commit":SOURCE_PRL if which=="prl" else "PRU branch current HEAD",
                  "source_properties":{},"graphical_assets":{},"status":"SOURCE_ONLY_NOT_PORTED",
                  "validation":["build pending","GBA animation and icon pending","catchability pending"]}
            for field in PROPS:
                v=prop(raw,field)
                if v is not None:data["source_properties"][field]=v
            learn=data["source_properties"].get("levelUpLearnset","")
            symbol=re.search(r"s[A-Za-z_0-9]+LevelUpLearnset",learn)
            if symbol and symbol.group(0) in learns[which]:
                data["level_up"]=learns[which][symbol.group(0)]
            slug=name.lower()
            chosen_root=prl if (prl/"graphics/pokemon"/slug).exists() else pjr
            if (chosen_root/"graphics/pokemon"/slug).exists():
                data["graphical_assets"]["root"]="PRL" if chosen_root==prl else "PJR"
                data["graphical_assets"]["dir"]="graphics/pokemon/"+slug+"/"
                for asset in REQUIRED_GRAPHICS:
                    f2=chosen_root/"graphics/pokemon"/slug/asset
                    if f2.is_file():data["graphical_assets"][asset]={"path":str(f2.relative_to(chosen_root)),"sha256":sha(f2)}
            species[name]=data
    # Noxichu is declared in PRL's include/constants/species.h and has
    # custom level-up/graphics; PR108 currently lacks a species-info block.
    # Make that gap visible rather than silently omitting the Pokemon.
    if "NOXICHU" not in species:
        name="NOXICHU"
        slug=name.lower()
        gfx=prl/"graphics/pokemon"/slug
        art={"root":"PRL","dir":"graphics/pokemon/"+slug+"/"}
        for asset in REQUIRED_GRAPHICS:
            f=gfx/asset
            if f.is_file():
                art[asset]={"path":str(f.relative_to(prl)),"sha256":sha(f)}
        rec={"species_constant":"SPECIES_NOXICHU","name":name,
          "source_tier":"PRL-Kanto","source_root":"prl",
          "source_file":"include/constants/species.h + src/data/pokemon/level_up_learnsets/prl_custom.h",
          "source_commit":SOURCE_PRL,
          "source_properties":{"levelUpLearnset":"sNoxichuLevelUpLearnset","baseHP":"70","baseAttack":"110","baseDefense":"70","baseSpAttack":"110","baseSpDefense":"80","baseSpeed":"125","types":"Electric/Dark","abilities":"Infiltrator","evolutions":"Moon Stone on Pikachu","teachableLearnset":"Pikachu + Umbreon compatible moves; verify actual PRL TM tables"},
          "graphical_assets":art,
          "status":"BLOCKED_PRL_SPECIES_INFO_NOT_FOUND",
          "validation":["Species enum is present, but pinned PRL species_info block missing",
                        "Design stats/typing/ability from PRL Step9 7-Oct canonical data; runtime species-info not found",
                        "Sprites/palettes hash-audited, runtime pointer and emulator QA pending"]}
        learn=learns["prl"].get("sNoxichuLevelUpLearnset")
        if learn:rec["level_up"]=learn
        species[name]=rec
    # RR species definitions must supersede ordinary inherited expansion entries.
    for name,override in RR.items():
        data=species.get(name,{"name":name,"species_constant":"SPECIES_"+name,
                               "source_properties":{},"graphical_assets":{}})
        data["priority_override"]="RADICAL_RED_REPLACEMENT"
        data["rr_design"]=override
        data["status"]="RR_LOCKED_SOURCE_PORT_AND_EMULATOR_PENDING"
        data["graphical_assets"]={"root":"Radical Red Seviian original donor" if "NOI" in name else "PRL/PJR Paldean form donor",
                                  "status":"CHECK_ASSET_PROVENANCE_AND_GBA_ICON_BEFORE_PORT"}
        species[name]=data
    for name in sorted(species):
        f=out/"species"/(name.lower()+".json")
        f.parent.mkdir(parents=True,exist_ok=True)
        f.write_text(json.dumps(species[name],indent=2,ensure_ascii=False)+"\n")
        x=species[name]
        lines=["# "+name,"","- Source tier: "+x.get("source_tier","RR"),
         "- Source: "+x.get("source_file","Radical Red override"),
         "- Status: "+x.get("status","pending"),
         "","## Source fields",""]
        lines += ["- "+k+": "+str(v) for k,v in x.get("source_properties",{}).items()]
        if "rr_design" in x:
            lines += ["","## PRU Radical Red replacement (supersedes above where conflicting)"]
            lines += ["- "+k+": "+str(v) for k,v in x["rr_design"].items()]
        lines += ["","## Level-up moves"]
        if "level_up" in x:lines += ["- Lv "+str(v["level"])+": "+v["move"] for v in x["level_up"]["moves"]]
        elif "rr_design" in x:lines += ["- Lv "+str(lvl)+": "+move for lvl,move in x["rr_design"]["moves"]]
        else:lines += ["- Not resolved in inspected level-up tables"]
        lines += ["","## Graphic source hashes","",json.dumps(x.get("graphical_assets",{}),indent=2),""]
        (out/"species"/(name.lower()+".md")).write_text("\n".join(lines))
    allrecs=sorted(species.values(),key=lambda x:x["name"])
    (out/"PRU_SPECIES_CURRENT_SOURCE.json").write_text(json.dumps(
       {"schema":"PRU SOURCE-OF-TRUTH MIRROR 2026-10-16","source_prl_sha":SOURCE_PRL,
        "note":"Source candidates and RR overrides, not gameplay integrated",
        "species":allrecs},ensure_ascii=False,indent=2)+"\n")
    with (out/"PRU_SPECIES_CURRENT_SOURCE.csv").open("w",newline="") as f:
        w=csv.writer(f);w.writerow(["species","source_tier","source_file","level_moves",
           "graphics_source","front_sha256","back_sha256","icon_sha256","status"])
        for r in allrecs:
            art=r.get("graphical_assets",{})
            w.writerow([r["name"],r.get("source_tier","Radical Red"),r.get("source_file","Radical Red"),
                 len(r.get("level_up",{}).get("moves",r.get("rr_design",{}).get("moves",[]))),
                 art.get("root",""),*(art.get(n,{}).get("sha256","") if isinstance(art.get(n),dict) else "" for n in ("front.png","back.png","icon.png")),
                 r.get("status","")])
    (out/"README.md").write_text("# PRU versioned Pokémon source files\n\n"+
       "Generated from the pinned PRL source plus PRU/PJR HNS donor and locked Radical Red overrides.\n"+
       "Source paths and SHA-256 hashes are included where actual files exist.\n"+
       "Never call these compiled or tested until code/ROM and emulator QA pass.\n"+
       "Older PRL Step 7 6–7 October sprite paths are superseded when current PRL asset exists.\n")
    print("PRU species files:",len(allrecs),"RR overrides:",len(RR))
    assert len(allrecs)>=350, "Unexpected source coverage; refuse to label complete"

if __name__=="__main__":
    main()
