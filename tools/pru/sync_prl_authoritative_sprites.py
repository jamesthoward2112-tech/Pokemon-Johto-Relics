#!/usr/bin/env python3
"""Install only active, approved PRL battle/party sprites ahead of a PRU ROM build.

The PRL commit is pinned. Original PJR graphics remain in place; active custom
species references are redirected to graphics/pokemon/prl_authoritative/.
Run before make hns. This script never edits a saved game or adds species IDs.
"""
from __future__ import annotations
import concurrent.futures
import hashlib
import json
import re
import urllib.error
import urllib.request
from pathlib import Path

PRL_SHA = "6ee9b984521ac6f2beaf995f771a726379e55c88"
ROOT = "https://raw.githubusercontent.com/jamesthoward2112-tech/Pokemon-Relic-Legacy/" + PRL_SHA
GFX_HEADERS = [Path("src/data/graphics/pjr.h"), Path("src/data/graphics/pru_pokemon.h")]
FILES = ("front.png", "back.png", "icon.png", "normal.pal", "shiny.pal")
KINDS = {
    "FrontPic": "front.4bpp.smol", "BackPic": "back.4bpp.smol",
    "Palette": "normal.gbapal", "ShinyPalette": "shiny.gbapal",
    "Icon": "icon.4bpp",
}
REQUIRED = {"noxichu", "edensaur", "charaxis", "fortotoise", "khang", "nolax", "pinsirex"}
# These icons were already converted to the GBA shared party-icon palettes.
# The donor's indexed PNGs have different palettes, so pointing their
# icon graphics at PRL-authoritative artwork made party icons look corrupt.
# Temporary Feralodon placeholder: use the complete Mega Feraligatr sprite
# already registered in this engine, without altering its species or forms.
# Donphalanx is intentionally backed by Great Tusk's exact sprites: the pinned
# PRL species data uses GreatTusk symbols, NOT the older donphalanx art folder.
# Do not overwrite approved Feralodon, Donphalanx or Tourmaline-Skarmet art on repeat builds.
PRU_VISUAL_OVERRIDES = {"feralodon", "donphalanx", "skarmet"}
NORMALIZED_EEVEE_ICONS = {
    "champeon", "lepideon", "guardeon", "obsideon", "toxeon",
    "sphynxeon", "omeon", "drakeon", "eeveeon", "nimbeon",
}
NOXICHU_BLOBS = {
    "front.png": "7e866622e368249babadc1382dea74902ddba960",
    "back.png": "3d8f20356388bc46839f4f84d43c04c8977338bd",
    "icon.png": "5bd90fbf7339e86f6f44e5697230a9b016e075d0",
}
def request(name: str) -> bytes:
    with urllib.request.urlopen(urllib.request.Request(
        ROOT + "/" + name, headers={"User-Agent": "PRU-pinned-PRL-art-import/1.0"}), timeout=40
    ) as response:
        return response.read()

def git_blob_sha(payload: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(payload)).encode() + b"\0" + payload).hexdigest()

def donor_assets(data: tuple[str, str]):
    symbol, slug = data
    paths = [f"graphics/pokemon/{slug}/{asset}" for asset in FILES]
    results = {}
    for name, path in zip(FILES, paths):
        try:
            results[name] = request(path)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return symbol, slug, None, path
            raise
    return symbol, slug, results, None

def main():
    # Canonical PRL species list, not names guessed from unrelated sprite folders.
    donor_species = request("src/data/pokemon/species_info/prl_custom.h").decode()
    names = sorted(set(re.findall(r"\[SPECIES_([A-Z0-9_]+)\]\s*=", donor_species)) | {"NOXICHU"})
    headers = {str(path): path.read_text() for path in GFX_HEADERS}
    active = []
    for name in names:
        symbol = "".join(part.capitalize() for part in name.split("_"))
        slug = name.lower()
        if name in ("NU_MEW", "NUMEW"):
            continue  # User-superseded donor; not an approved PRU species.
        if any("gMonFrontPic_" + symbol + "[]" in source for source in headers.values()):
            active.append((symbol, slug))
    print("PRL canonical species", len(names), "PRU active graphics", len(active))
    print("Active PRL sprite slugs:", sorted(slug for _, slug in active))
    assert REQUIRED.issubset({slug for _, slug in active}), "Required PRL Relic graphics symbols missing: " + repr(sorted(REQUIRED - {slug for _, slug in active}))

    manifest = []
    failures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(donor_assets, active))
    for symbol, slug, assets, missing in results:
        if assets is None:
            failures.append({"species": slug, "missing": missing})
            continue
        # No sprite recolouring: RelicDex/PRL share Valkiri's indexed art.
        # The renderer uses the same front/back pixel indices with two palettes.
        # RelicDex's green shiny palette becomes PRU's normal; the original
        # PRL blue normal palette becomes PRU's shiny. Preserve PNG bytes.
        if slug == "valkyvoir":
            green = Path("assets/pru_valkiri/normal.pal").read_bytes()
            blue = Path("assets/pru_valkiri/shiny.pal").read_bytes()
            assert green != blue
            assert b"86 160 93" in green and b"71 117 213" in blue
            assets["normal.pal"] = green
            assets["shiny.pal"] = blue
            print("VALKIRI: original indexed sprites unchanged; green normal / blue shiny palettes")
        for filename, contents in assets.items():
            if slug == "noxichu" and filename in NOXICHU_BLOBS:
                assert git_blob_sha(contents) == NOXICHU_BLOBS[filename], (
                    "PRL Noxichu donor changed: " + filename
                )
            dest = Path("graphics/pokemon/prl_authoritative") / slug / filename
            dest.parent.mkdir(parents=True, exist_ok=True)
            if not dest.exists() or dest.read_bytes() != contents:
                dest.write_bytes(contents)
        for key, source in list(headers.items()):
            if slug in PRU_VISUAL_OVERRIDES:
                continue  # Preserve all approved explicit PRU visual overrides.
            for kind, filename in KINDS.items():
                if kind == "Icon" and slug in NORMALIZED_EEVEE_ICONS:
                    # Leave the palette-compatible repository party icons intact.
                    continue
                # Only replace the exact graphics symbol of an active PRL species.
                rx = re.compile(
                    r'(const u(?:8|16|32) gMon' + kind + '_' + symbol +
                    r'\[\] = INCBIN_U(?:8|16|32)\(")' +
                    r'graphics/pokemon/[^"]+("\);)'
                )
                source = rx.sub(
                    lambda m: m.group(1) + "graphics/pokemon/prl_authoritative/" +
                    slug + "/" + filename + m.group(2), source
                )
            headers[key] = source
        manifest.append({
            "species": slug, "symbols": symbol, "source_commit": PRL_SHA,
            "asset_sha256": {name: hashlib.sha256(val).hexdigest() for name, val in assets.items()}
        })
    assert not (REQUIRED & {f["species"] for f in failures}), (
        "Missing required approved PRL art: " + str(failures)
    )
    for name, text in headers.items():
        Path(name).write_text(text)
    report = Path("PRU-QA/prl-sprite-parity.json")
    report.parent.mkdir(exist_ok=True)
    report.write_text(json.dumps({
        "pinned_prl_commit": PRL_SHA, "active_PRL_species": len(active),
        "ported": manifest, "unavailable_donor_sprites": failures
    }, indent=2) + "\n")
    print("PRL artwork imported", len(manifest), "species", "skipped", len(failures))
    if failures:
        print("DONOR GAPS", failures)

if __name__ == "__main__":
    main()
