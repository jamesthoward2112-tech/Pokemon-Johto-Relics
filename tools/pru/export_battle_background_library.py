#!/usr/bin/env python3
"""Archive the authentic PRL Crystal Advance Redux 38 battle backgrounds, library only.

Pinned PRL artwork bank; no changes to PRU's live battle assets or mappings.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import urllib.request, json, zlib, base64, hashlib, zipfile, struct, shutil

PRL_SHA = "93551ad482f23667bb8df46896edf796761aef6f"
URL = ("https://raw.githubusercontent.com/jamesthoward2112-tech/"
       "Pokemon-Relic-Legacy/" + PRL_SHA + "/assets/prl_crystal_presentation.json")
PREFIX = "graphics/battle_environment/crystal_redux/"
ROOT = Path("PRU-Battle-Background-Library")
OUT = ROOT / "Crystal_Redux_38"
REQUIRED = ("tiles.4bpp.lz", "tilemap.bin.lz", "entry_tiles.4bpp.lz",
            "entry_tilemap.bin.lz", "palette_48colors.gbapal")

def gba_lz77(data):
    if not data or data[0] != 0x10:
        raise ValueError("Expected GBA LZ77 format")
    size = int.from_bytes(data[1:4], "little")
    if not (0 < size < 500000):
        raise ValueError("Invalid unpacked size")
    out = bytearray()
    i = 4
    while len(out) < size:
        flags = data[i]; i += 1
        for n in range(8):
            if flags & (0x80 >> n):
                hi,lo = data[i:i+2]; i += 2
                count = (hi >> 4) + 3
                distance = (((hi & 15) << 8) | lo) + 1
                if distance > len(out):
                    raise ValueError("Bad LZ77 backreference")
                for k in range(count):
                    out.append(out[-distance])
            else:
                out.append(data[i]); i += 1
            if len(out) >= size:
                break
    return bytes(out[:size])

def render_battle(idx):
    folder = OUT / f"{idx:02d}"
    tiles = gba_lz77((folder / "tiles.4bpp.lz").read_bytes())
    tmap = gba_lz77((folder / "tilemap.bin.lz").read_bytes())
    pal = (folder / "palette_48colors.gbapal").read_bytes()
    if len(tmap) < 32*20*2 or len(pal) < 96:
        raise ValueError(f"Broken Crystal background {idx}")
    colors = []
    for i in range(0,96,2):
        n = pal[i] | pal[i+1] << 8
        colors.append(((n & 31)*255//31,((n>>5)&31)*255//31,((n>>10)&31)*255//31))
    pic = Image.new("RGB", (240, 160), (20,20,32))
    px = pic.load()
    tiles_count = len(tiles)//32
    for y in range(20):
        for x in range(30):
            entry = struct.unpack_from("<H",tmap,2*(y*32+x))[0]
            tile = entry&1023
            if tile >= tiles_count:
                continue
            hflip = bool(entry & 1024)
            vflip = bool(entry & 2048)
            bank = (entry>>12)&15
            # PRL source uses palette banks 2,3,4 for the 48-colour background.
            bankidx = bank-2 if bank>=2 else bank
            for py in range(8):
                for pxx in range(8):
                    yy = 7-py if vflip else py
                    xx = 7-pxx if hflip else pxx
                    v = tiles[tile*32+yy*4+xx//2]
                    ci = (v>>4) if xx&1 else (v&15)
                    k = bankidx*16+ci
                    if 0 <= k < len(colors):
                        px[x*8+pxx,y*8+py] = colors[k]
    return pic

def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    req = urllib.request.Request(URL,headers={"User-Agent":"PRU-Archive-Generator"})
    with urllib.request.urlopen(req,timeout=90) as fh:
        archive = json.load(fh)
    raw = zlib.decompress(base64.b64decode(archive["zlib_base64"]))
    assert hashlib.sha256(raw).hexdigest() == archive["payload_sha256"]
    records = json.loads(raw)
    count = 0
    for name, content in records.items():
        if not name.startswith(PREFIX):
            continue  # transitions are not battle background assets
        subpath = Path(name[len(PREFIX):])
        if subpath.is_absolute() or ".." in subpath.parts:
            raise ValueError("Invalid donor asset path")
        dest = OUT / subpath
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(base64.b64decode(content,validate=True))
        count += 1
    for i in range(38):
        for name in REQUIRED:
            asset = OUT / f"{i:02d}" / name
            if not asset.is_file() or asset.stat().st_size < 20:
                raise ValueError(f"Missing authentic background {asset}")
    previewdir = ROOT / "Previews"
    previewdir.mkdir(exist_ok=True)
    sheet = Image.new("RGB",(6*244,7*183),(30,32,46))
    draw = ImageDraw.Draw(sheet)
    for i in range(38):
        im = render_battle(i)
        im.save(previewdir/f"Crystal_Redux_{i:02d}.png")
        x,y=(i%6)*244,(i//6)*183
        sheet.paste(im,(x,y+20))
        draw.text((x+5,y+3),f"Battle background {i:02d}",fill="white")
    sheet.save(previewdir/"Crystal_Redux_All_38_Contact_Sheet.png")
    doc = ("# PRU Battle Background Library — 38 Crystal Advance Redux backgrounds\n\n"
           "Authentic source: PRL GitHub branch prl/restore-move-order-crystal-backgrounds-20261011\n"
           f"Pinned PRL commit: {PRL_SHA}\n"
           f"Source asset bank SHA-256 (unpacked): {archive['payload_sha256']}\n"
           "Artwork credit: Crystal Advance Redux original creators; PRL extraction and presentation.\n"
           "All 38 indices 00–37 contain original compressed GBA tiles/maps, entry overlay tiles/maps,\n"
           "and RGB555 palettes. Preview images are decoded for selection only; originals remain unchanged.\n"
           "This is an ARCHIVE ONLY: NO background has been assigned in Pokémon Relic Ultimate.\n"
           "Current working Chansey, Ralts, Unown, Poochyena and intro logic are untouched.\n"
           f"Count of archived original graphics files: {count}.\n")
    (ROOT/"README.md").write_text(doc)
    manifest={"source_url":URL,"prl_commit":PRL_SHA,"payload_sha256":archive["payload_sha256"],
              "backgrounds":38,"files":count,"live_in_pru":False,
              "files_by_background":list(REQUIRED)}
    (ROOT/"manifest.json").write_text(json.dumps(manifest,indent=2))
    with zipfile.ZipFile("PRU-Battle-Background-Library-38.zip","w",zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for f in sorted(ROOT.rglob("*")):
            if f.is_file():
                z.write(f,f.relative_to(ROOT.parent))
    print("PRU_BACKGROUND_LIBRARY_PASS",count,"source files, 38 backgrounds and indexed previews",flush=True)

if __name__=="__main__":
    main()
