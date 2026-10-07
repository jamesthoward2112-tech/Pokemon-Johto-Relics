from __future__ import annotations
from pathlib import Path
import json, re, shutil, subprocess, sys, zipfile, os
from PIL import Image

ROOT = Path(r"C:\Users\HowardGMKtec\Documents\RelicDev\PRL-FOUNDATION-1171")
PJR = Path(r"C:\Users\HowardGMKtec\Documents\RelicDev\Pokemon-Johto-Relics")
STAGE = Path(r"C:\Users\HowardGMKtec\Documents\RelicDev\_chatgpt_prl_step10_transfer")
CANON = Path(r"C:\Users\HowardGMKtec\Documents\RelicDev\Pokemon-Relic-Legacy-Canonical\Canonical-Data\Assets")
BRANCH = "prl/step10-mass-integration"
MARK = "PRL STEP10"

def run(*args, cwd=ROOT, check=True):
    cp = subprocess.run(args, cwd=cwd, text=True, capture_output=True)
    if check and cp.returncode:
        print(cp.stdout); print(cp.stderr, file=sys.stderr); raise SystemExit(cp.returncode)
    return cp

def read(p): return Path(p).read_text(encoding="utf-8", errors="ignore")
def write(p,s):
    p=Path(p); p.parent.mkdir(parents=True, exist_ok=True); p.write_text(s, encoding="utf-8", newline="\n")

def replace_once(text, old, new, label):
    if old not in text: raise RuntimeError(f"missing marker for {label}")
    return text.replace(old, new, 1)

def c_name(name):
    special={"nuMew":"NuMew","I-Unown":"IUnownRelic","Relic Ho-Oh":"RelicHoOh"}
    if name in special: return special[name]
    return re.sub(r"[^A-Za-z0-9]", "", name)

def constify(s):
    s=s.upper().replace("É","E")
    s=s.replace("'","").replace("!","")
    s=re.sub(r"[^A-Z0-9]+","_",s).strip("_")
    aliases={"U_TURN":"U_TURN", "DEJA_VU":"DEJA_VU", "WILL_O_WISP":"WILL_O_WISP"}
    return aliases.get(s,s)

def extract_designated(text, key):
    pat=f"[{key}]"
    i=text.find(pat)
    if i<0: return None
    eq=text.find("=",i); b=text.find("{",eq)
    if b<0:return None
    depth=0; quote=None; esc=False
    for j in range(b,len(text)):
        ch=text[j]
        if quote:
            if esc: esc=False
            elif ch=='\\': esc=True
            elif ch==quote: quote=None
            continue
        if ch in "\"'": quote=ch; continue
        if ch=='{': depth+=1
        elif ch=='}':
            depth-=1
            if depth==0:
                k=j+1
                while k<len(text) and text[k].isspace(): k+=1
                if k<len(text) and text[k]==',': k+=1
                return text[i:k]
    return None

def extract_array(text, symbol):
    m=re.search(rf"static const struct LevelUpMove\s+{re.escape(symbol)}\[\]\s*=\s*\{{",text)
    if not m:return None
    b=text.find("{",m.start()); depth=0
    for j in range(b,len(text)):
        if text[j]=='{':depth+=1
        elif text[j]=='}':
            depth-=1
            if depth==0:
                k=text.find(';',j)
                return text[m.start():k+1]
    return None

def extract_u16_array(text, symbol):
    m=re.search(rf"static const u16\s+{re.escape(symbol)}\[\]\s*=\s*\{{",text)
    if not m:return None
    b=text.find("{",m.start()); depth=0
    for j in range(b,len(text)):
        if text[j]=='{':depth+=1
        elif text[j]=='}':
            depth-=1
            if depth==0:
                k=text.find(';',j); return text[m.start():k+1]
    return None

def find_species_block(species):
    key=f"[SPECIES_{species}]"
    for p in sorted((ROOT/"src/data/pokemon/species_info").glob("gen_*_families.h")):
        t=read(p); i=t.find(key)
        if i>=0:
            block=extract_designated(t,f"SPECIES_{species}")
            return p,t,block
    p=ROOT/"src/data/pokemon/species_info.h"; t=read(p)
    if key in t:return p,t,extract_designated(t,f"SPECIES_{species}")
    raise RuntimeError(f"base species not found: {species}")

def field(block, name, fallback):
    m=re.search(rf"^\s*\.{re.escape(name)}\s*=\s*(.+),\s*(?://.*)?$", block, re.M)
    return m.group(1).strip() if m else fallback

def jasc_from_png(png, out):
    im=Image.open(png)
    if im.mode!='P':
        im=im.convert('RGBA')
        bg=Image.new('RGBA', im.size,(0,0,0,0)); bg.alpha_composite(im)
        im=bg.convert('RGB').quantize(colors=15, method=Image.Quantize.MEDIANCUT)
    pal=im.getpalette() or [0]*768
    cols=[tuple(pal[i:i+3]) for i in range(0,48,3)]
    lines=["JASC-PAL","0100","16"]+[f"{r} {g} {b}" for r,g,b in cols]
    write(out,"\n".join(lines)+"\n")

def copy_sprite_set(src:Path, dest:Path, icon_fallback:Path|None=None):
    dest.mkdir(parents=True,exist_ok=True)
    for name in ("front.png","back.png"):
        q=src/name
        if not q.exists(): raise RuntimeError(f"missing {q}")
        shutil.copy2(q,dest/name)
    icon=icon_fallback if icon_fallback and icon_fallback.exists() else src/"icon.png"
    if not icon.exists(): raise RuntimeError(f"missing icon for {dest.name}: {icon}")
    shutil.copy2(icon,dest/"icon.png")
    # Preserve source palette where possible; otherwise derive exact indexed palette from front PNG.
    if (src/"normal.pal").exists(): shutil.copy2(src/"normal.pal",dest/"normal.pal")
    elif (src/"battle_palette.pal").exists(): shutil.copy2(src/"battle_palette.pal",dest/"normal.pal")
    elif (src/"front.gbapal").exists(): shutil.copy2(src/"front.gbapal",dest/"normal.gbapal")
    elif (src/"normal.gbapal").exists(): shutil.copy2(src/"normal.gbapal",dest/"normal.gbapal")
    else: jasc_from_png(dest/"front.png", dest/"normal.pal")
    if (src/"shiny.pal").exists(): shutil.copy2(src/"shiny.pal",dest/"shiny.pal")
    elif (src/"shiny.gbapal").exists(): shutil.copy2(src/"shiny.gbapal",dest/"shiny.gbapal")
    else:
        if (dest/"normal.pal").exists(): shutil.copy2(dest/"normal.pal",dest/"shiny.pal")
        else: shutil.copy2(dest/"normal.gbapal",dest/"shiny.gbapal")

def convert_valkyvoir(src:Path,dest:Path, icon:Path):
    dest.mkdir(parents=True,exist_ok=True)
    imgs=[]
    for fn in ("GARDEVOIR_REDUX_MEGA.png","GARDEVOIR_REDUX_MEGA_BACK.png"):
        im=Image.open(src/fn).convert('RGBA')
        if im.size!=(64,64):
            im.thumbnail((64,64), Image.Resampling.NEAREST)
            canvas=Image.new('RGBA',(64,64),(0,0,0,0)); canvas.alpha_composite(im,((64-im.width)//2,64-im.height)); im=canvas
        imgs.append(im)
    colors=[]
    for im in imgs:
        for px in im.getdata():
            if px[3] and px[:3] not in colors: colors.append(px[:3])
    if len(colors)>15:
        comb=Image.new('RGB',(128,64),(0,0,0)); comb.paste(imgs[0].convert('RGB'),(0,0)); comb.paste(imgs[1].convert('RGB'),(64,0))
        q=comb.quantize(colors=15,method=Image.Quantize.MEDIANCUT)
        pal=q.getpalette(); colors=[tuple(pal[i:i+3]) for i in range(0,45,3)]
    colors=colors[:15]
    palette=[0,0,0]+[v for c in colors for v in c]+[0]*(768-3-3*len(colors))
    def remap(im,out):
        p=Image.new('P',(64,64),0); p.putpalette(palette)
        srcpix=list(im.getdata()); op=[]
        for rgba in srcpix:
            if rgba[3]==0: op.append(0); continue
            rgb=rgba[:3]; idx=min(range(len(colors)), key=lambda i:sum((rgb[k]-colors[i][k])**2 for k in range(3))) if colors else 0
            op.append(idx+1)
        p.putdata(op); p.info['transparency']=0; p.save(out,optimize=False)
    remap(imgs[0],dest/"front.png"); remap(imgs[1],dest/"back.png")
    shutil.copy2(icon,dest/"icon.png")
    lines=["JASC-PAL","0100","16","0 0 0"]+[f"{r} {g} {b}" for r,g,b in colors]+["0 0 0"]*(15-len(colors))
    write(dest/"normal.pal","\n".join(lines)+"\n"); shutil.copy2(dest/"normal.pal",dest/"shiny.pal")

def patch_custom_enum(path, sentinel, names, first_expr=None, marker=""):
    t=read(path)
    # Idempotent: remove previous marked block.
    t=re.sub(rf"\n\s*// {re.escape(MARK)} {re.escape(marker)} BEGIN.*?// {re.escape(MARK)} {re.escape(marker)} END\n", "\n", t, flags=re.S)
    idx=t.find(sentinel)
    if idx<0: raise RuntimeError(f"sentinel {sentinel} missing in {path}")
    indent=re.match(r"\s*", t[t.rfind('\n',0,idx)+1:idx]).group(0)
    lines=[f"{indent}// {MARK} {marker} BEGIN"]
    for i,n in enumerate(names):
        if i==0 and first_expr: lines.append(f"{indent}{n} = {first_expr},")
        else: lines.append(f"{indent}{n},")
    lines.append(f"{indent}// {MARK} {marker} END")
    return t[:idx]+"\n".join(lines)+"\n"+t[idx:]

def move_from_text(desc):
    # not used for donor moves; canonical parser helper for logging only
    return desc

def make_move_entry(sym,name,typ,cat,power,acc,pp,anim,extras=""):
    accv="0" if acc is None else str(acc)
    return f'''[{sym}] =\n{{\n    .name = COMPOUND_STRING("{name.upper()}"),\n    .description = COMPOUND_STRING("PRL signature move."),\n    .effect = EFFECT_HIT,\n    .power = {power},\n    .type = TYPE_{typ},\n    .accuracy = {accv},\n    .pp = {pp},\n    .target = TARGET_SELECTED,\n    .priority = 0,\n    .category = DAMAGE_CATEGORY_{cat},\n{extras}    .battleAnimScript = gBattleAnimMove_{anim},\n}},'''

def make_ability_entry(sym,name,desc):
    safe=desc.replace('"',"'")[:95]
    return f'''[{sym}] =\n{{\n    .name = COMPOUND_STRING("{name}"),\n    .description = COMPOUND_STRING("{safe}"),\n    .aiRating = 3,\n}},'''

def append_marked_before_final(text, body, marker):
    text=re.sub(rf"\n// {re.escape(MARK)} {re.escape(marker)} BEGIN.*?// {re.escape(MARK)} {re.escape(marker)} END\n", "\n", text, flags=re.S)
    pos=text.rfind("};")
    if pos<0: raise RuntimeError(f"final initializer missing: {marker}")
    block=f"\n// {MARK} {marker} BEGIN\n{body}\n// {MARK} {marker} END\n"
    return text[:pos]+block+text[pos:]

def parse_canon_moves(s):
    out=[]
    for part in [x.strip() for x in s.split(';') if x.strip()]:
        m=re.match(r"Lv(\d+)\s+(.+)$",part, re.I)
        if not m: continue
        lv=int(m.group(1)); names=[x.strip() for x in m.group(2).split('/')]
        for n in names:
            n=re.sub(r"\s*\([^)]*\)\s*$","",n).strip()
            n=n.split(' remains ')[0].strip()
            if n: out.append((lv,n))
    return out

def level_array(symbol,moves):
    lines=[f"static const struct LevelUpMove {symbol}[] =","{"]
    for lv,n in moves: lines.append(f"    LEVEL_UP_MOVE({lv}, MOVE_{constify(n)}),")
    lines += ["    LEVEL_UP_END","};"]
    return "\n".join(lines)

def ability_expr(s):
    if s.startswith("Use normal Ho-Oh"): return None
    parts=[]
    for p in s.split('/'):
        p=p.strip(); p=re.sub(r"^Hidden:\s*","",p,flags=re.I)
        if not p: continue
        key=constify(p)
        # Project symbol names omit apostrophe and punctuation.
        parts.append("ABILITY_"+key)
    parts=(parts+["ABILITY_NONE"]*3)[:3]
    return "{ " + ", ".join(parts) + " }"

def type_expr(s):
    pts=["TYPE_"+constify(x.strip()) for x in s.split('/')]
    return "MON_TYPES("+", ".join(pts)+")"

def add_evolution(base, entries, prepend=False):
    p,t,block=find_species_block(base)
    key=f"[SPECIES_{base}]"; start=t.find(key); b=t.find('{',start)
    # find matching block closing in full text
    depth=0; end=None
    for j in range(b,len(t)):
        if t[j]=='{':depth+=1
        elif t[j]=='}':
            depth-=1
            if depth==0: end=j; break
    sub=t[start:end+1]
    evo_i=sub.find('.evolutions = EVOLUTION(')
    new_entries=",\n                                ".join(entries)
    if evo_i<0:
        insert="\n        .evolutions = EVOLUTION("+new_entries+"),\n"
        sub=sub[:-1]+insert+sub[-1:]
    else:
        epos=evo_i+len('.evolutions = EVOLUTION(')
        # match parens starting immediately before content
        openpos=sub.find('(',evo_i); d=0; close=None
        for k in range(openpos,len(sub)):
            if sub[k]=='(': d+=1
            elif sub[k]==')':
                d-=1
                if d==0: close=k; break
        current=sub[openpos+1:close].strip()
        if prepend: merged=new_entries+(",\n                                "+current if current else "")
        else: merged=current+(",\n                                "+new_entries if current else new_entries)
        sub=sub[:openpos+1]+merged+sub[close:]
    t=t[:start]+sub+t[end+1:]
    write(p,t)

def patch_field_in_species(species, replacements):
    p,t,block=find_species_block(species)
    key=f"[SPECIES_{species}]"; start=t.find(key); b=t.find('{',start); depth=0; end=None
    for j in range(b,len(t)):
        if t[j]=='{':depth+=1
        elif t[j]=='}':
            depth-=1
            if depth==0:end=j;break
    sub=t[start:end+1]
    for fname,expr in replacements.items():
        pat=rf"(^\s*\.{re.escape(fname)}\s*=\s*).+?(,\s*(?://.*)?$)"
        if re.search(pat,sub,re.M): sub=re.sub(pat,rf"\g<1>{expr}\g<2>",sub,count=1,flags=re.M)
        else: sub=sub[:-1]+f"\n        .{fname} = {expr},\n"+sub[-1:]
    write(p,t[:start]+sub+t[end+1:])

# ---- Begin ----
if not ROOT.exists() or not PJR.exists() or not (STAGE/"step9_validated_input.json").exists():
    raise SystemExit("required PRL/PJR/staging paths missing")
if run("git","status","--porcelain").stdout.strip(): raise SystemExit("PRL working tree is not clean")
branches=run("git","branch","--list",BRANCH).stdout.strip()
if branches: run("git","checkout",BRANCH)
else: run("git","checkout","-b",BRANCH)
print("BRANCH",BRANCH)

canon=json.loads(read(STAGE/"step9_validated_input.json"))
records={r["name"]:r for r in canon["species_and_forms"]}

# Extract transferred packs.
unpack=STAGE/"unpacked"; shutil.rmtree(unpack,ignore_errors=True); unpack.mkdir()
for z in ["Gemlin_PRL_GBA_Porypal.zip","Hyenadon_PRL_GBA_Original.zip","PHR_Hoennmon_PoryPal_CANONICAL_v1.zip"]:
    with zipfile.ZipFile(STAGE/z) as f: f.extractall(unpack/z.replace('.zip',''))

gfx_root=ROOT/"graphics/pokemon"; pjr_gfx=PJR/"graphics/pokemon"
# Canonical source mappings for PJR-backed sets.
pjr_map={
"Edensaur":"venusaur/mega","Charaxis":"charizard/mega_y","Fortotoise":"blastoise/mega","Khang":"khang","Nolax":"nolax",
"Scarabub":"scarabub","Skarmet":"skarmet","Mootiny":"mootiny","Heracurion":"pjr_locked/heracurion","Skarmadon":"pjr_locked/skarmadon","Miltitan":"pjr_locked/miltitan","Shuckolosse":"pjr_locked/shuckolosse","Donphalanx":"pjr_locked/donphalanx","Mystynx":"pjr_locked/mystynx","Pinsirex":"pinsir/mega","Faeranium":"pjr_locked/faeranium","Pyroclast":"pjr_locked/pyroclast","Feralodon":"pjr_locked/feralodon","Champeon":"champeon","Lepideon":"lepideon","Sphynxeon":"sphynxeon","Guardeon":"guardeon","Obsideon":"obsideon","Toxeon":"toxeon","Omeon":"omeon","Drakeon":"drakeon","Jollibird":"jollibird","Grimfowl":"grimfowl","Kablowfish":"kablowfish","Sunflorid":"sunflorid","Alphoracle":"alphoracle","Osteodian":"osteodian","Maroghost":"maroghost",
}
for name,rel in pjr_map.items():
    dest=gfx_root/re.sub(r"[^a-z0-9]+","_",name.lower()).strip('_')
    iconfb=None
    if name=="Khang": iconfb=gfx_root/"kangaskhan/mega/icon.png"
    if name=="Nolax": iconfb=gfx_root/"snorlax/icon.png"
    copy_sprite_set(pjr_gfx/rel,dest,iconfb)
# Ghoulbat audited hybrid: locate relic/crobat front if present; otherwise current donor Ghoulbat front; base Crobat back/icon.
ghsrc=pjr_gfx/"ghoulbat"
if not ghsrc.exists():
    cands=[p.parent for p in pjr_gfx.rglob("front.png") if "crobat" in str(p).lower() and "relic" in str(p).lower()]
    ghsrc=cands[0] if cands else pjr_gfx/"crobat"
ghdest=gfx_root/"ghoulbat"; ghdest.mkdir(parents=True,exist_ok=True)
shutil.copy2(ghsrc/"front.png",ghdest/"front.png")
shutil.copy2(gfx_root/"crobat/back.png",ghdest/"back.png"); shutil.copy2(gfx_root/"crobat/icon.png",ghdest/"icon.png")
if (ghsrc/"normal.pal").exists(): shutil.copy2(ghsrc/"normal.pal",ghdest/"normal.pal")
elif (ghsrc/"front.gbapal").exists(): shutil.copy2(ghsrc/"front.gbapal",ghdest/"normal.gbapal")
else:jasc_from_png(ghdest/"front.png",ghdest/"normal.pal")
if (ghdest/"normal.pal").exists():shutil.copy2(ghdest/"normal.pal",ghdest/"shiny.pal")
else:shutil.copy2(ghdest/"normal.gbapal",ghdest/"shiny.gbapal")
# Missing packs.
gemsrc=unpack/"Gemlin_PRL_GBA_Porypal"/"graphics/pokemon/gemlin"; copy_sprite_set(gemsrc,gfx_root/"gemlin")
hysrc=unpack/"Hyenadon_PRL_GBA_Original"; copy_sprite_set(hysrc,gfx_root/"hyenadon")
phr=unpack/"PHR_Hoennmon_PoryPal_CANONICAL_v1"/"PHR_Hoennmon_PoryPal_CANONICAL_v1"
for name in ["Sceptitan","Solaziken","Swamplith","Gemigoyle","Mawyrm","Torkaldera","Cactomb","Tropisaur","Coelossus","Astrachi"]:
    copy_sprite_set(phr/name,gfx_root/name.lower())
copy_sprite_set(STAGE/"numew",gfx_root/"numew")
valsrc=CANON/"Valkyvoir"; convert_valkyvoir(valsrc,gfx_root/"valkyvoir",gfx_root/"gardevoir/mega/icon.png")
# Forms.
copy_sprite_set(pjr_gfx/"unown_eye",gfx_root/"unown_eye")
copy_sprite_set(pjr_gfx/"ho_oh_relic",gfx_root/"ho_oh_relic")

# Graphics declarations for every new custom species/form except already-wired Noxichu.
gdecl=[]
for name in [r["name"] for r in canon["species_and_forms"] if r["name"] not in ("Noxichu","I-Unown")]:
    slug="ho_oh_relic" if name=="Relic Ho-Oh" else re.sub(r"[^a-z0-9]+","_",name.lower()).strip('_')
    sym=c_name(name); d=gfx_root/slug
    pal_norm=f'INCGFX_U16("graphics/pokemon/{slug}/normal.pal", ".gbapal")' if (d/"normal.pal").exists() else f'INCBIN_U16("graphics/pokemon/{slug}/normal.gbapal")'
    pal_shiny=f'INCGFX_U16("graphics/pokemon/{slug}/shiny.pal", ".gbapal")' if (d/"shiny.pal").exists() else f'INCBIN_U16("graphics/pokemon/{slug}/shiny.gbapal")'
    gdecl += [f'const u32 gMonFrontPic_{sym}[] = INCGFX_U32("graphics/pokemon/{slug}/front.png", ".4bpp.smol");',f'const u16 gMonPalette_{sym}[] = {pal_norm};',f'const u32 gMonBackPic_{sym}[] = INCGFX_U32("graphics/pokemon/{slug}/back.png", ".4bpp.smol");',f'const u16 gMonShinyPalette_{sym}[] = {pal_shiny};',f'const u8 gMonIcon_{sym}[] = INCGFX_U8("graphics/pokemon/{slug}/icon.png", ".4bpp");','']
# I-Unown dedicated graphics symbols.
d=gfx_root/"unown_eye"; norm='INCGFX_U16("graphics/pokemon/unown_eye/normal.pal", ".gbapal")' if (d/"normal.pal").exists() else 'INCBIN_U16("graphics/pokemon/unown_eye/normal.gbapal")'; shiny='INCGFX_U16("graphics/pokemon/unown_eye/shiny.pal", ".gbapal")' if (d/"shiny.pal").exists() else ('INCBIN_U16("graphics/pokemon/unown_eye/shiny.gbapal")' if (d/"shiny.gbapal").exists() else norm)
gdecl += ['const u32 gMonFrontPic_IUnownRelic[] = INCGFX_U32("graphics/pokemon/unown_eye/front.png", ".4bpp.smol");',f'const u16 gMonPalette_IUnownRelic[] = {norm};','const u32 gMonBackPic_IUnownRelic[] = INCGFX_U32("graphics/pokemon/unown_eye/back.png", ".4bpp.smol");',f'const u16 gMonShinyPalette_IUnownRelic[] = {shiny};','const u8 gMonIcon_IUnownRelic[] = INCGFX_U8("graphics/pokemon/unown_eye/icon.png", ".4bpp");']
pg=ROOT/"src/data/graphics/pokemon.h"; write(pg,append_marked_before_final(read(pg),"\n".join(gdecl),"GRAPHICS"))

# Engine species constants: preserve Noxichu's existing numeric position, then append remaining canonical identities.
sp=ROOT/"include/constants/species.h"; st=read(sp)
custom_order=["SPECIES_NOXICHU"]+["SPECIES_"+constify(r["name"]) for r in canon["species_and_forms"] if r["record_type"]=="SPECIES" and r["name"]!="Noxichu"]+["SPECIES_RELIC_HO_OH"]
# nuMew constant spelling.
custom_order=[x.replace("SPECIES_NUMEW","SPECIES_NUMEW") for x in custom_order]
m=re.search(r"\s*SPECIES_CUSTOM_START\s*=\s*SPECIES_GLIMMORA_MEGA,.*?\s*SPECIES_CUSTOM_END,",st,re.S)
if not m: raise RuntimeError("custom species enum block missing")
lines=["    SPECIES_CUSTOM_START = SPECIES_GLIMMORA_MEGA,","    // PRL engine IDs. Canonical project IDs remain PRL001..PRL049; donor numeric IDs are never reused."]+['    '+x+',' for x in custom_order]+["    SPECIES_CUSTOM_END,"]
st=st[:m.start()]+"\n"+"\n".join(lines)+st[m.end():]; write(sp,st)

# Project ID alias header.
idlines=["#ifndef GUARD_CONSTANTS_PRL_IDS_H","#define GUARD_CONSTANTS_PRL_IDS_H",""]
for r in canon["species_and_forms"]:
    eng="SPECIES_UNOWN_I" if r["name"]=="I-Unown" else ("SPECIES_RELIC_HO_OH" if r["name"]=="Relic Ho-Oh" else "SPECIES_"+constify(r["name"]))
    idlines.append(f'#define {r["canonical_symbol"]} {eng} // {r["canonical_id"]}')
for r in canon["custom_moves"]: idlines.append(f'#define {r["symbol"]} MOVE_{constify(r["name"])} // {r["canonical_id"]}')
for r in canon["custom_abilities"]: idlines.append(f'#define {r["symbol"]} ABILITY_{constify(r["name"])} // {r["canonical_id"]}')
idlines += ['#define PRL_ITEM_ANCIENT_RAINBOW_CREST ITEM_ANCIENT_RAINBOW_CREST // PRL_ITEM_009','#define PRL_ITEM_ANCIENT_STONE ITEM_ANCIENT_STONE // PRL_ITEM_010',"","#endif"]
write(ROOT/"include/constants/prl_ids.h","\n".join(idlines)+"\n")

# Moves constants before the normal-move sentinel.
move_consts=["MOVE_"+constify(r["name"]) for r in canon["custom_moves"]]
mp=ROOT/"include/constants/moves.h"; mt=read(mp)
mt=re.sub(r"\n\s*// PRL STEP10 MOVES BEGIN.*?// PRL STEP10 MOVES END\n","\n",mt,flags=re.S)
needle="    MOVES_COUNT = MOVES_COUNT_GEN9,"
if needle not in mt: raise RuntimeError("MOVES_COUNT sentinel changed")
block="    // PRL STEP10 MOVES BEGIN\n"+"\n".join([f"    {n} = MOVES_COUNT_GEN9," if i==0 else f"    {n}," for i,n in enumerate(move_consts)])+"\n    // PRL STEP10 MOVES END\n    MOVES_COUNT,"
mt=mt.replace(needle,block,1); write(mp,mt)
# Ability constants.
ap=ROOT/"include/constants/abilities.h"; at=read(ap); at=re.sub(r"\n\s*// PRL STEP10 ABILITIES BEGIN.*?// PRL STEP10 ABILITIES END\n","\n",at,flags=re.S)
needle="    ABILITIES_COUNT = ABILITIES_COUNT_GEN9,"
if needle not in at: raise RuntimeError("ability count sentinel changed")
abil_consts=["ABILITY_"+constify(r["name"]) for r in canon["custom_abilities"]]
block="    // PRL STEP10 ABILITIES BEGIN\n"+"\n".join([f"    {n} = ABILITIES_COUNT_GEN9," if i==0 else f"    {n}," for i,n in enumerate(abil_consts)])+"\n    // PRL STEP10 ABILITIES END\n    ABILITIES_COUNT,"
at=at.replace(needle,block,1); write(ap,at)
# Active item constants only; project tombstones deliberately get no live engine slots.
ip=ROOT/"include/constants/items.h"; it=read(ip); it=re.sub(r"\n\s*// PRL STEP10 ITEMS BEGIN.*?// PRL STEP10 ITEMS END\n","\n",it,flags=re.S)
idx=it.find("    ITEMS_COUNT,")
if idx<0: raise RuntimeError("ITEMS_COUNT sentinel missing")
ib="    // PRL STEP10 ITEMS BEGIN\n    ITEM_ANCIENT_RAINBOW_CREST,\n    ITEM_ANCIENT_STONE,\n    // PRL STEP10 ITEMS END\n"
it=it[:idx]+ib+it[idx:]; write(ip,it)

# Custom move data: exact PJR entries where available; generate the eight Kanto/Hoenn entries.
pjr_moves=read(PJR/"src/data/moves_info.h")
move_entries=[]
for r in canon["custom_moves"]:
    eng="MOVE_"+constify(r["name"]); donor=extract_designated(pjr_moves,eng)
    if donor: move_entries.append(donor); continue
    name=r["name"]
    specs={
      "Amber Blade":("GRASS","PHYSICAL",95,100,10,"LeafBlade","    .criticalHitStage = 1,\n    .additionalEffects = ADDITIONAL_EFFECTS({ .moveEffect = MOVE_EFFECT_DEF_MINUS_1, .chance = 20, }),\n"),
      "Sun Rite":("FIRE","PHYSICAL",95,100,10,"BlazeKick","    .additionalEffects = ADDITIONAL_EFFECTS({ .moveEffect = MOVE_EFFECT_SPD_PLUS_1, .self = TRUE, .chance = 30, }),\n"),
      "Tectonic Tide":("WATER","PHYSICAL",95,100,10,"AquaTail","    .additionalEffects = ADDITIONAL_EFFECTS({ .moveEffect = MOVE_EFFECT_DEF_MINUS_1, .chance = 30, }),\n"),
      "Epoch Crash":("ROCK","PHYSICAL",120,100,5,"StoneEdge","    .additionalEffects = ADDITIONAL_EFFECTS({ .moveEffect = MOVE_EFFECT_DEF_MINUS_1, .chance = 20, }),\n"),
      "Relic Wish":("FAIRY","SPECIAL",100,100,10,"Moonblast",""),
      "Eden Bloom":("GRASS","SPECIAL",95,100,10,"EnergyBall","    .additionalEffects = ADDITIONAL_EFFECTS({ .moveEffect = MOVE_EFFECT_POISON, .chance = 30, }),\n"),
      "Scorchwing":("FLYING","PHYSICAL",95,100,10,"BraveBird","    .makesContact = TRUE,\n    .additionalEffects = ADDITIONAL_EFFECTS({ .moveEffect = MOVE_EFFECT_BURN, .chance = 20, }),\n"),
      "Bastion Cannon":("STEEL","SPECIAL",95,100,10,"FlashCannon","    .additionalEffects = ADDITIONAL_EFFECTS({ .moveEffect = MOVE_EFFECT_DEF_PLUS_1, .self = TRUE, .chance = 30, }),\n"),
    }
    if name not in specs: raise RuntimeError(f"no move implementation source: {name}")
    move_entries.append(make_move_entry(eng,name,*specs[name]))
mip=ROOT/"src/data/moves_info.h"; write(mip,append_marked_before_final(read(mip),"\n\n".join(move_entries),"MOVE DATA"))

# Ability table entries; runtime hooks are ported in the next sub-pass, but all IDs/data are live now.
pjr_abs=read(PJR/"src/data/abilities.h"); aentries=[]
for r in canon["custom_abilities"]:
    eng="ABILITY_"+constify(r["name"]); donor=extract_designated(pjr_abs,eng)
    aentries.append(donor if donor else make_ability_entry(eng,r["name"],r["evolution_or_mechanics"]))
aip=ROOT/"src/data/abilities.h"; write(aip,append_marked_before_final(read(aip),"\n\n".join(aentries),"ABILITY DATA"))

# Clone item entries from existing evolution/key items.
items_path=ROOT/"src/data/items.h"; itemt=read(items_path)
stone=extract_designated(itemt,"ITEM_SHINY_STONE")
crest=extract_designated(itemt,"ITEM_RAINBOW_WING") or extract_designated(itemt,"ITEM_OLD_SEA_MAP")
if not stone or not crest: raise RuntimeError("could not clone item templates")
stone=stone.replace("[ITEM_SHINY_STONE]","[ITEM_ANCIENT_STONE]",1)
stone=re.sub(r'\.name\s*=\s*_\("[^"]+"\)', '.name = _("Ancient Stone")',stone,count=1)
crest=re.sub(r'^\[ITEM_[A-Z0-9_]+\]','[ITEM_ANCIENT_RAINBOW_CREST]',crest,count=1)
crest=re.sub(r'\.name\s*=\s*_\("[^"]+"\)', '.name = _("Ancient Crest")',crest,count=1)
write(items_path,append_marked_before_final(itemt,crest+"\n\n"+stone,"ITEM DATA"))

# Evolution conditions IF_MIN_LEVEL and IF_MAP_TYPE.
pp=ROOT/"include/constants/pokemon.h"; pt=read(pp)
if "IF_MIN_LEVEL" not in pt:
    pt=pt.replace("    IF_HOLD_ITEM,                       // The PokAcmon is holding a specific item.","    IF_HOLD_ITEM,                       // The PokAcmon is holding a specific item.\n    IF_MIN_LEVEL,                       // PRL: current level is at least the specified value.\n    IF_MAP_TYPE,                        // PRL: current map type matches the specified value.",1)
    write(pp,pt)
pc=ROOT/"src/pokemon.c"; pct=read(pc)
if "case IF_MIN_LEVEL:" not in pct:
    anchor="        case IF_HOLD_ITEM:\n            if (heldItem == params[i].arg1)\n            {\n                currentCondition = TRUE;\n                removeHoldItem = TRUE;\n            }\n            break;"
    repl=anchor+"\n        case IF_MIN_LEVEL:\n            if (level >= params[i].arg1)\n                currentCondition = TRUE;\n            break;\n        case IF_MAP_TYPE:\n            if (gMapHeader.mapType == params[i].arg1)\n                currentCondition = TRUE;\n            break;"
    pct=replace_once(pct,anchor,repl,"pokemon evolution conditions"); write(pc,pct)
pd=ROOT/"src/pokedex_plus_hgss.c"; pdt=read(pd)
if "case IF_MIN_LEVEL:" not in pdt:
    anchor='                case IF_HOLD_ITEM:\n                    StringAppend(gStringVar4, COMPOUND_STRING("holds "));'
    repl='                case IF_MIN_LEVEL:\n                    StringAppend(gStringVar4, COMPOUND_STRING("Lv"));\n                    ConvertIntToDecimalStringN(gStringVar2, evolutions[i].params[j].arg1, STR_CONV_MODE_LEFT_ALIGN, 3);\n                    StringAppend(gStringVar4, gStringVar2);\n                    break;\n                case IF_MAP_TYPE:\n                    StringAppend(gStringVar4, COMPOUND_STRING("specific area"));\n                    break;\n'+anchor
    pdt=replace_once(pdt,anchor,repl,"dex evolution conditions"); write(pd,pdt)

# Build learnsets: donor PJR arrays where locked; otherwise canonical text.
pjr_ls=read(PJR/"src/data/pokemon/level_up_learnsets/pjr.h")
ls_path=ROOT/"src/data/pokemon/level_up_learnsets/prl_custom.h"; existing=read(ls_path)
nox=extract_array(existing,"sNoxichuLevelUpLearnset")
arrays=[nox] if nox else []
custom_sig={"Edensaur":"Eden Bloom","Charaxis":"Scorchwing","Fortotoise":"Bastion Cannon","Khang":"Return","Nolax":"Extreme Speed","Valkyvoir":"Boomburst","Sceptitan":"Amber Blade","Solaziken":"Sun Rite","Swamplith":"Tectonic Tide","Coelossus":"Epoch Crash"}
learn_symbol={"Noxichu":"sNoxichuLevelUpLearnset"}
for name,r in records.items():
    if r["record_type"]!="SPECIES" or name=="Noxichu": continue
    sym=f"s{c_name(name)}LevelUpLearnset"
    donor=extract_array(pjr_ls,sym)
    if donor:
        arrays.append(donor); learn_symbol[name]=sym; continue
    text=r["level_up_or_form_moves"]
    if text.lower().startswith("use ") or text.lower().startswith("inherit"):
        continue
    moves=[]
    if name in custom_sig: moves.append((0,custom_sig[name]))
    # Accept "Evolution: X;" then Lv entries.
    em=re.search(r"Evolution:\s*([^;]+)",text,re.I)
    if em: moves.insert(0,(0,em.group(1).strip()))
    moves += parse_canon_moves(text)
    # Deduplicate exact level/move pairs while preserving order.
    seen=set(); moves=[x for x in moves if not (x in seen or seen.add(x))]
    if moves:
        arrays.append(level_array(sym,moves)); learn_symbol[name]=sym
# I-Unown and Relic Ho-Oh exact donor learnsets.
for sym in ["sUnownEyeLevelUpLearnset","sRelicHoOhLevelUpLearnset"]:
    a=extract_array(pjr_ls,sym)
    if not a: raise RuntimeError(f"missing donor learnset {sym}")
    arrays.append(a)
write(ls_path,"// PRL custom species level-up learnsets — Step 10 generated from locked canon / pinned donor.\n\n"+"\n\n".join(x for x in arrays if x)+"\n")

# Teachable compatibility: base species by default; preserve donor Infinity arrays and nuMew Mewtwo+Sylveon union.
pjr_teach=read(PJR/"src/data/pokemon/teachable_learnsets.h")
prl_teach=[]; teach_symbol={}
# Pull any custom teachable symbol referenced in PJR species block for matching names.
pjr_species=read(PJR/"src/data/pokemon/species_info/pjr_families.h")
for name in pjr_map.keys() | {"Ghoulbat"}:
    block=extract_designated(pjr_species,"SPECIES_"+constify(name))
    if not block: continue
    m=re.search(r"\.teachableLearnset\s*=\s*(s[A-Za-z0-9_]+)",block)
    if m and "Infinity" in m.group(1):
        arr=extract_u16_array(pjr_teach,m.group(1))
        if arr: prl_teach.append(arr); teach_symbol[name]=m.group(1)
# nuMew union from PRL standard teachables.
stdteach=read(ROOT/"src/data/pokemon/teachable_learnsets.h")
def moves_from_u16(sym):
    a=extract_u16_array(stdteach,sym)
    return re.findall(r"MOVE_[A-Z0-9_]+",a or "")
un=[]
for m in moves_from_u16("sMewtwoTeachableLearnset")+moves_from_u16("sSylveonTeachableLearnset"):
    if m not in un: un.append(m)
if un:
    arr="static const u16 sNuMewTeachableLearnset[] =\n{\n"+"\n".join(f"    {m}," for m in un)+"\n    MOVE_UNAVAILABLE,\n};"
    prl_teach.append(arr); teach_symbol["nuMew"]="sNuMewTeachableLearnset"
tp=ROOT/"src/data/pokemon/teachable_learnsets/prl_custom.h"; write(tp,"// PRL custom teachable tables — Step 10.\n\n"+"\n\n".join(prl_teach)+"\n")
# Include teachable header in pokemon.c near standard table.
pct=read(pc)
inc='#include "data/pokemon/teachable_learnsets/prl_custom.h"'
if inc not in pct:
    marker='#include "data/pokemon/teachable_learnsets.h"'
    if marker not in pct: raise RuntimeError("standard teachable include not found")
    pct=pct.replace(marker,marker+'\n'+inc,1); write(pc,pct)

# Base proxy map for metadata/teachables.
base={
"Edensaur":"VENUSAUR","Charaxis":"CHARIZARD","Fortotoise":"BLASTOISE","Khang":"KANGASKHAN","Nolax":"SNORLAX","nuMew":"MEW","Gemlin":"SABLEYE","Valkyvoir":"GARDEVOIR","Sceptitan":"SCEPTILE","Solaziken":"BLAZIKEN","Swamplith":"SWAMPERT","Hyenadon":"MIGHTYENA","Gemigoyle":"SABLEYE","Mawyrm":"MAWILE","Torkaldera":"TORKOAL","Cactomb":"CACTURNE","Tropisaur":"TROPIUS","Coelossus":"RELICANTH","Astrachi":"JIRACHI","Scarabub":"HERACROSS","Skarmet":"SKARMORY","Mootiny":"MILTANK","Heracurion":"HERACROSS","Skarmadon":"SKARMORY","Miltitan":"MILTANK","Shuckolosse":"SHUCKLE","Donphalanx":"DONPHAN","Mystynx":"JYNX","Pinsirex":"PINSIR","Faeranium":"MEGANIUM","Pyroclast":"TYPHLOSION","Feralodon":"FERALIGATR","Champeon":"EEVEE","Lepideon":"EEVEE","Sphynxeon":"EEVEE","Guardeon":"EEVEE","Obsideon":"EEVEE","Toxeon":"EEVEE","Omeon":"EEVEE","Drakeon":"EEVEE","Jollibird":"DELIBIRD","Grimfowl":"NOCTOWL","Kablowfish":"QWILFISH","Sunflorid":"SUNFLORA","Ghoulbat":"CROBAT","Alphoracle":"UNOWN","Osteodian":"MAROWAK","Maroghost":"MAROWAK","Relic Ho-Oh":"HO_OH"}
# Overrides for teachable canonical rules.
teach_base={"Nolax":"LOPUNNY"}

def base_meta(b):
    _,_,block=find_species_block(b)
    return {k:field(block,k,v) for k,v in {
      "catchRate":"45","expYield":"200","genderRatio":"PERCENT_FEMALE(50)","eggCycles":"20","friendship":"STANDARD_FRIENDSHIP","growthRate":"GROWTH_MEDIUM_FAST","eggGroups":"MON_EGG_GROUPS(EGG_GROUP_FIELD)","bodyColor":"BODY_COLOR_BROWN","cryId":"CRY_NONE","natDexNum":"NATIONAL_DEX_NONE","height":"10","weight":"300","iconPalIndex":"0","pokemonJumpType":"PKMN_JUMP_TYPE_NONE","abilities":"{ ABILITY_NONE, ABILITY_NONE, ABILITY_NONE }","levelUpLearnset":"sNoneLevelUpLearnset","teachableLearnset":"sNoneTeachableLearnset"}.items()}

species_blocks=[]
for r in canon["species_and_forms"]:
    name=r["name"]
    if r["record_type"]!="SPECIES" or name=="Noxichu": continue
    b=base[name]; meta=base_meta(b); sym=c_name(name); slug=re.sub(r"[^a-z0-9]+","_",name.lower()).strip('_')
    stats=[int(x) for x in re.findall(r"\d+",r["base_stats"])][:6]
    if len(stats)!=6: raise RuntimeError(f"bad stats {name}")
    abil=ability_expr(r["abilities"]) or meta["abilities"]
    ls=learn_symbol.get(name,meta["levelUpLearnset"])
    teach=teach_symbol.get(name)
    if not teach:
        tb=teach_base.get(name,b); teach=f"s{''.join(x.title() for x in tb.lower().split('_'))}TeachableLearnset"
        # Prefer exact expression from base metadata if using its own table.
        if tb==b: teach=meta["teachableLearnset"]
    # Custom baby evolutions live on their own species blocks.
    evo=""
    if name=="Gemlin": evo='\n    .evolutions = EVOLUTION({EVO_LEVEL, 20, SPECIES_SABLEYE, CONDITIONS({IF_TIME, TIME_NIGHT})}),' 
    elif name=="Scarabub": evo='\n    .evolutions = EVOLUTION({EVO_LEVEL, 18, SPECIES_HERACROSS}),' 
    elif name=="Skarmet": evo='\n    .evolutions = EVOLUTION({EVO_LEVEL, 18, SPECIES_SKARMORY}),' 
    elif name=="Mootiny": evo='\n    .evolutions = EVOLUTION({EVO_LEVEL, 18, SPECIES_MILTANK}),' 
    # Gemlin Hard Stone 5%.
    itemrare='\n    .itemRare = ITEM_HARD_STONE,' if name=="Gemlin" else ''
    species_name="Ho-Oh" if name=="Relic Ho-Oh" else name
    block=f'''[SPECIES_{constify(name) if name!='Relic Ho-Oh' else 'RELIC_HO_OH'}] =\n{{\n    .baseHP = {stats[0]}, .baseAttack = {stats[1]}, .baseDefense = {stats[2]},\n    .baseSpAttack = {stats[3]}, .baseSpDefense = {stats[4]}, .baseSpeed = {stats[5]},\n    .types = {type_expr(r['typing'])},\n    .catchRate = {meta['catchRate']}, .expYield = {meta['expYield']},{itemrare}\n    .genderRatio = {meta['genderRatio']}, .eggCycles = {meta['eggCycles']}, .friendship = {meta['friendship']},\n    .growthRate = {meta['growthRate']}, .eggGroups = {meta['eggGroups']},\n    .abilities = {abil}, .bodyColor = {meta['bodyColor']},\n    .speciesName = _("{species_name}"), .cryId = {meta['cryId']}, .natDexNum = {meta['natDexNum']},\n    .categoryName = _("Relic"), .height = {meta['height']}, .weight = {meta['weight']},\n    .description = COMPOUND_STRING("A Pokemon awakened by Relic Resonance.\\nIts ancient power has taken a new form."),\n    .pokemonScale = 256, .pokemonOffset = 0, .trainerScale = 256, .trainerOffset = 0,\n    .frontPic = gMonFrontPic_{sym}, .frontPicSize = MON_COORDS_SIZE(64, 64), .frontPicYOffset = 0,\n    .frontAnimFrames = sAnims_SingleFramePlaceHolder, .frontAnimId = ANIM_V_SQUISH_AND_BOUNCE,\n    .backPic = gMonBackPic_{sym}, .backPicSize = MON_COORDS_SIZE(64, 64), .backPicYOffset = 0, .backAnimId = BACK_ANIM_NONE,\n    .palette = gMonPalette_{sym}, .shinyPalette = gMonShinyPalette_{sym},\n    .iconSprite = gMonIcon_{sym}, .iconPalIndex = {meta['iconPalIndex']},\n    .pokemonJumpType = {meta['pokemonJumpType']},\n    .levelUpLearnset = {ls}, .teachableLearnset = {teach},{evo}\n}},'''
    species_blocks.append(block)
custom_species_path=ROOT/"src/data/pokemon/species_info/prl_custom.h"; write(custom_species_path,"// PRL Step 10 custom species — generated from frozen PRL canon.\n\n"+"\n\n".join(species_blocks)+"\n")
# Include inside gSpeciesInfo after existing Noxichu and before Egg.
sinfo=ROOT/"src/data/pokemon/species_info.h"; sit=read(sinfo); inc='#include "species_info/prl_custom.h"'
if inc not in sit:
    marker='    [SPECIES_EGG] ='
    if marker not in sit: raise RuntimeError("species egg marker missing")
    sit=sit.replace(marker,'    '+inc+'\n\n'+marker,1); write(sinfo,sit)

# I-Unown form exact current PRL mechanics.
patch_field_in_species("UNOWN_I",{
 "baseHP":"48","baseAttack":"72","baseDefense":"48","baseSpeed":"48","baseSpAttack":"72","baseSpDefense":"48","types":"MON_TYPES(TYPE_PSYCHIC)","abilities":"{ ABILITY_WONDER_GUARD, ABILITY_NONE, ABILITY_NONE }","speciesName":"_(\"I-Unown\")","frontPic":"gMonFrontPic_IUnownRelic","frontPicSize":"MON_COORDS_SIZE(64, 64)","backPic":"gMonBackPic_IUnownRelic","backPicSize":"MON_COORDS_SIZE(64, 64)","palette":"gMonPalette_IUnownRelic","shinyPalette":"gMonShinyPalette_IUnownRelic","iconSprite":"gMonIcon_IUnownRelic","levelUpLearnset":"sUnownEyeLevelUpLearnset"})

# Evolution wiring for non-map-script evolutions.
# Ancient Stone users.
for b,tgt,lv in [("VENUSAUR","EDENSAUR",45),("CHARIZARD","CHARAXIS",45),("BLASTOISE","FORTOTOISE",45),("HERACROSS","HERACURION",40),("SKARMORY","SKARMADON",40),("MILTANK","MILTITAN",40),("SHUCKLE","SHUCKOLOSSE",40),("DONPHAN","DONPHALANX",40),("JYNX","MYSTYNX",40),("MEGANIUM","FAERANIUM",45),("TYPHLOSION","PYROCLAST",45),("FERALIGATR","FERALODON",45)]:
    add_evolution(b,[f'{{EVO_ITEM, ITEM_ANCIENT_STONE, SPECIES_{tgt}, CONDITIONS({{IF_MIN_LEVEL, {lv}}})}}'])
add_evolution("KANGASKHAN",['{EVO_LEVEL, 0, SPECIES_KHANG, CONDITIONS({IF_MIN_FRIENDSHIP, FRIENDSHIP_EVO_THRESHOLD})}'])
add_evolution("SNORLAX",['{EVO_LEVEL, 0, SPECIES_NOLAX, CONDITIONS({IF_HOLD_ITEM, ITEM_CHESTO_BERRY})}'])
add_evolution("GARDEVOIR",['{EVO_ITEM, ITEM_SHINY_STONE, SPECIES_VALKYVOIR, CONDITIONS({IF_MIN_LEVEL, 50})}'])
add_evolution("MIGHTYENA",['{EVO_LEVEL, 0, SPECIES_HYENADON, CONDITIONS({IF_HOLD_ITEM, ITEM_HARD_STONE})}'])
add_evolution("SABLEYE",['{EVO_LEVEL, 0, SPECIES_GEMIGOYLE, CONDITIONS({IF_HOLD_ITEM, ITEM_HARD_STONE})}'])
add_evolution("MAWILE",['{EVO_LEVEL, 0, SPECIES_MAWYRM, CONDITIONS({IF_HOLD_ITEM, ITEM_DRAGON_FANG})}'])
add_evolution("TORKOAL",['{EVO_LEVEL, 0, SPECIES_TORKALDERA, CONDITIONS({IF_HOLD_ITEM, ITEM_CHARCOAL})}'])
add_evolution("CACTURNE",['{EVO_LEVEL, 0, SPECIES_CACTOMB, CONDITIONS({IF_HOLD_ITEM, ITEM_SPELL_TAG})}'])
add_evolution("TROPIUS",['{EVO_LEVEL, 0, SPECIES_TROPISAUR, CONDITIONS({IF_HOLD_ITEM, ITEM_ENIGMA_BERRY})}'])
add_evolution("PINSIR",['{EVO_LEVEL, 42, SPECIES_PINSIREX}'])
add_evolution("DELIBIRD",['{EVO_ITEM, ITEM_SHINY_STONE, SPECIES_JOLLIBIRD}'])
add_evolution("NOCTOWL",['{EVO_ITEM, ITEM_DUSK_STONE, SPECIES_GRIMFOWL}'])
add_evolution("QWILFISH",['{EVO_LEVEL, 40, SPECIES_KABLOWFISH, CONDITIONS({IF_HOLD_ITEM, ITEM_METAL_COAT})}'])
add_evolution("SUNFLORA",['{EVO_ITEM, ITEM_FIRE_STONE, SPECIES_SUNFLORID}'])
add_evolution("CROBAT",['{EVO_LEVEL, 50, SPECIES_GHOULBAT, CONDITIONS({IF_TIME, TIME_NIGHT}, {IF_MAP_TYPE, MAP_TYPE_UNDERGROUND})}'])
add_evolution("MAROWAK",['{EVO_LEVEL, 40, SPECIES_OSTEODIAN, CONDITIONS({IF_NOT_TIME, TIME_NIGHT}, {IF_HOLD_ITEM, ITEM_THICK_CLUB})}','{EVO_LEVEL, 40, SPECIES_MAROGHOST, CONDITIONS({IF_TIME, TIME_NIGHT}, {IF_HOLD_ITEM, ITEM_SPELL_TAG})}'])
# Eevee custom branches first, so Dragon Fang suppresses friendship evolutions.
eevee=[
'{EVO_LEVEL, 0, SPECIES_CHAMPEON, CONDITIONS({IF_NOT_TIME, TIME_NIGHT}, {IF_HOLD_ITEM, ITEM_EXPERT_BELT})}',
'{EVO_LEVEL, 0, SPECIES_LEPIDEON, CONDITIONS({IF_NOT_TIME, TIME_NIGHT}, {IF_HOLD_ITEM, ITEM_SILVER_POWDER})}',
'{EVO_LEVEL, 0, SPECIES_SPHYNXEON, CONDITIONS({IF_NOT_TIME, TIME_NIGHT}, {IF_HOLD_ITEM, ITEM_SOFT_SAND})}',
'{EVO_LEVEL, 0, SPECIES_GUARDEON, CONDITIONS({IF_TIME, TIME_NIGHT}, {IF_HOLD_ITEM, ITEM_METAL_COAT})}',
'{EVO_LEVEL, 0, SPECIES_OBSIDEON, CONDITIONS({IF_TIME, TIME_NIGHT}, {IF_HOLD_ITEM, ITEM_HARD_STONE})}',
'{EVO_LEVEL, 0, SPECIES_TOXEON, CONDITIONS({IF_TIME, TIME_NIGHT}, {IF_HOLD_ITEM, ITEM_POISON_BARB})}',
'{EVO_ITEM, ITEM_DUSK_STONE, SPECIES_OMEON}',
'{EVO_LEVEL, 25, SPECIES_DRAKEON, CONDITIONS({IF_HOLD_ITEM, ITEM_DRAGON_FANG})}',
]
add_evolution("EEVEE",eevee,prepend=True)

# Hoenn altar evolutions and Coelossus are deliberately map-script gates, not weakened to anywhere-item evolutions.
map_gate=ROOT/"docs/prl_step10_map_event_gates.md"; write(map_gate,"""# PRL Step 10 map/event gates\n\nThese mechanics are intentionally not encoded as ordinary anywhere evolutions:\n- Sceptile + Ancient Stone Lv45+ -> Sceptitan: Route 120 Forest Altar only.\n- Blaziken + Ancient Stone Lv45+ -> Solaziken: Route 120 Sun Altar only.\n- Swampert + Ancient Stone Lv45+ -> Swamplith: Route 120 Tide Altar only.\n- Exact returning special Kanto Shiny Relicanth -> Coelossus: Sealed Chamber First Current after all ten guardians.\n- nuMew, Astrachi, Alphoracle and Relic Ho-Oh are static scripted encounters.\n\nDo not add fallback species-table evolutions that bypass these story gates.\n""")

# Clone standard graphics globally for Mewtwo -> Mega X visual without changing mechanics.
# Use species pointer fields only; all Mega X symbols already exist in expansion.
patch_field_in_species("MEWTWO",{"frontPic":"gMonFrontPic_MewtwoMegaX","backPic":"gMonBackPic_MewtwoMegaX","palette":"gMonPalette_MewtwoMegaX","shinyPalette":"gMonShinyPalette_MewtwoMegaX","iconSprite":"gMonIcon_MewtwoMegaX"})

# Static validation manifest.
manifest={"branch":BRANCH,"species_constants":len(custom_order),"canonical_species":49,"forms":{"I-Unown":"SPECIES_UNOWN_I","Relic Ho-Oh":"SPECIES_RELIC_HO_OH"},"custom_moves":len(move_consts),"custom_abilities":len(abil_consts),"active_custom_items":["ITEM_ANCIENT_RAINBOW_CREST","ITEM_ANCIENT_STONE"],"map_script_gates":["Sceptitan","Solaziken","Swamplith","Coelossus","nuMew","Astrachi","Alphoracle","Relic Ho-Oh"],"runtime_hooks_pending":[r["name"] for r in canon["custom_abilities"] if r["name"] not in ("Ancient Bastion","Ancient Bloom","Cinder Veil","Tidal Roar")]+["Relic Wish post-hit healing"]}
write(ROOT/"docs/prl_step10_integration_manifest.json",json.dumps(manifest,indent=2))

# Ensure no accidental donor numeric IDs were introduced into project alias header.
assert "1574" not in read(ROOT/"include/constants/prl_ids.h")
# Formatting/basic sanity.
run("git","diff","--check")
print("STEP10_DATA_INTEGRATION_OK")
print(run("git","status","--short").stdout)