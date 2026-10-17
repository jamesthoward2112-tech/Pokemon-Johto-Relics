#!/usr/bin/env python3
"""Reproducible *test-only* PRU boot/title assembly.

Flow: native pokeemerald intro -> original Last Wish Scene 0 -> black fade
-> approved Noxichu cavern art -> native flashing PRESS START.
Executed by GitHub Actions before make hns; normal source branches untouched.
"""
from pathlib import Path
import base64
import hashlib
import io
import urllib.request
import ast
import subprocess
import tempfile
import zipfile
from PIL import Image

PRL_REPO = "jamesthoward2112-tech/Pokemon-Relic-Legacy"
PRL_COMMIT = "744d4c2fd3b352bbb76a917efa7b440b43730e98"
PRL_C_FILE = "src/prl_intro_trial.c"
PRL_HELPER = "tools/prl/prepare_hwl_scene0.py"
BASE = "https://raw.githubusercontent.com"
ASSET_B64 = Path("assets/pru_title/noxichu_relic_cavern_240.jpg.b64")
TITLE_DIR = Path("graphics/title_screen/pjr")

def fetch_prl(path):
    url = f"{BASE}/{PRL_REPO}/{PRL_COMMIT}/{path}"
    with urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": "PRU-title-build"}),
        timeout=65,
    ) as r:
        content = r.read()
    print("DONOR_FETCH", path, len(content),
          hashlib.sha256(content).hexdigest())
    return content

def replace_exact(path, old, new):
    target = Path(path)
    original = target.read_text()
    assert original.count(old) == 1, (
        f"Expected exactly one replacement target in {path}: {old[:90]!r}, "
        f"found {original.count(old)}"
    )
    target.write_text(original.replace(old, new))
    print("PATCH_PASS", path, old[:80].replace("\n", " "))

def install_last_wish():
    # The final PRL branch retains ORIGINAL donor Celebi/Jirachi sprites.
    code = fetch_prl(PRL_C_FILE).decode("utf-8")
    assert '#if defined(FIRERED)' in code
    assert 'graphics/intro/prl_hwl/celebi.png' in code
    assert 'graphics/intro/prl_hwl/jirachi.png' in code
    assert 'void CB2_InitPRLHwlScene0(void)' in code
    code = code.replace("#if defined(FIRERED)", "#if IS_HNS", 1)
    code = code.replace("CB2_InitPRLHwlScene0", "CB2_InitPRUHwlScene0")
    # PRU's pokeemerald-expansion fork predates PRL's INCGFX compile macro.
    # Convert donor references to ordinary INCBIN targets built by gbagfx.
    import re
    code = re.sub(r'INCGFX_U16\("([^"]+)\.png", "\.gbapal"\)',
                  r'INCBIN_U16("\1.gbapal")', code)
    code = re.sub(r'INCGFX_U32\("([^"]+)\.png", "\.4bpp\.smol"\)',
                  r'INCBIN_U32("\1.4bpp.smol")', code)
    assert "INCGFX_U16" not in code and "INCGFX_U32" not in code
    # PRU m4a wrappers take gbsEnabled as their second parameter.
    code = code.replace('m4aSongNumStart(MUS_INTRO);',
                        'm4aSongNumStart(MUS_INTRO, FALSE);')
    code = code.replace('m4aSongNumStop(MUS_INTRO);',
                        'm4aSongNumStop(MUS_INTRO, FALSE);')
    # Retain original scene cleanup and fade-out to title.
    Path("src/pru_hwl_intro.c").write_text(code)

    helper = fetch_prl(PRL_HELPER).decode("utf-8")
    assert "BLOBS =" in helper and "HOENN-S-LAST-WISH-project" in helper
    module = ast.parse(helper)
    expected = next(ast.literal_eval(n.value) for n in module.body
                    if isinstance(n, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id == "BLOBS"
                            for t in n.targets))
    # The original donor pinned commit was replaced by the author.
    # Recover the exact verified donor sources from the successful
    # 8 Oct 2026 PRL GitHub Actions export artifact, still retained.
    with tempfile.TemporaryDirectory() as temp:
        subprocess.run(["gh", "run", "download", "37778386335",
                        "--repo", PRL_REPO, "--name", "PRL-Original-Intro-Donors",
                        "--dir", temp], check=True)
        outer = Path(temp) / "Hoenns_Last_Wish_Opening_Scenes_0_to_3.zip"
        assert outer.is_file(), f"Missing original donor nested archive: {outer}"
        with zipfile.ZipFile(outer) as archive:
            prefix = "Hoenns_Last_Wish_Opening_Scenes_0_to_3/graphics/intro/scene_0/"
            dest = Path("graphics/intro/prl_hwl")
            dest.mkdir(parents=True, exist_ok=True)
            for name, sha in expected.items():
                content = archive.read(prefix + name)
                digest = hashlib.sha1(
                    b"blob " + str(len(content)).encode() + b"\0" + content
                ).hexdigest()
                assert digest == sha, f"Donor original hash mismatch: {name}"
                (dest / name).write_bytes(content)
                print("ARCHIVED_DONOR_VERIFIED", name, digest)
    assert len(expected) >= 20
    for art in ("celebi.png", "jirachi.png", "bg00.png", "moon.png"):
        assert Path("graphics/intro/prl_hwl", art).is_file()

def patch_boot_flow():
    intro = Path("src/intro.c")
    source = intro.read_text()
    # Bypass only the HNS copyright/intro dispatch for this test variant;
    # fall through to the preserved vanilla Emerald copyright/startup.
    old = "#elif IS_HNS\n    return SetUpCopyrightScreenHns();\n#endif"
    assert source.count(old) == 1
    source = source.replace(
        old,
        "#elif IS_HNS\n    // PRU test: use the normal Emerald opening below.\n#endif",
    )
    # HnS has EXPANSION_INTRO enabled: that route plays the Gengar intro
    # and never calls MainCB2_EndIntro. Select native Emerald scenes 1-3
    # for this isolated PRU test, preserving the expansion path elsewhere.
    expansion_branch = ("#if EXPANSION_INTRO == TRUE\n"
                        "        SetMainCallback2(CB2_ExpansionIntro);\n"
                        "        CreateTask(Task_HandleExpansionIntro, 0);\n"
                        "#else\n"
                        "        CreateTask(Task_Scene1_Load, 0);\n"
                        "        SetMainCallback2(MainCB2_Intro);\n"
                        "#endif")
    assert source.count(expansion_branch) == 1, "Emerald/Expansion intro dispatch has changed"
    source = source.replace(expansion_branch,
                            expansion_branch.replace("#if EXPANSION_INTRO == TRUE",
                                                     "#if EXPANSION_INTRO == TRUE && !IS_HNS"))
    print("INTRO_DISPATCH_PASS PRU uses Emerald intro instead of Gengar Expansion intro")
    old = ("static void MainCB2_EndIntro(void)\n"
           "{\n"
           "    if (!UpdatePaletteFade())\n"
           "        SetMainCallback2(CB2_InitTitleScreen);\n"
           "}")
    new = ("void CB2_InitPRUHwlScene0(void);\n"
           "\n"
           "static void MainCB2_EndIntro(void)\n"
           "{\n"
           "    if (!UpdatePaletteFade())\n"
           "        SetMainCallback2(CB2_InitPRUHwlScene0);\n"
           "}")
    assert source.count(old) == 1
    intro.write_text(source.replace(old, new))
    print("BOOT_FLOW_PASS Emerald -> Last Wish -> PRU title")

def install_title_art():
    parts = sorted(ASSET_B64.parent.glob(ASSET_B64.name + '.part*'))
    assert len(parts) == 3, f"Expected three approved artwork payload parts, found {len(parts)}"
    jpg = base64.b64decode(''.join(''.join(p.read_text().split()) for p in parts), validate=True)
    assert hashlib.sha256(jpg).hexdigest() == '0ea8c588161dc79307115d06054cfbbab1ab1588bd73fbd839a13f8a00837128'
    frame = Image.open(io.BytesIO(jpg)).convert("RGB")
    assert frame.size == (240, 160), frame.size
    # GBA Mode 4: exact 240*160 8bpp indices + 256 RGB555 palette.
    indexed = frame.quantize(colors=240, method=Image.Quantize.MEDIANCUT,
                             dither=Image.Dither.NONE)
    raw = indexed.tobytes()
    assert len(raw) == 38400
    palette = indexed.getpalette()
    assert palette is not None and len(palette) >= 240 * 3
    # Pillow provides exactly the requested number of palette entries, not 256.
    palette = palette + [0] * (256 * 3 - len(palette))
    pal_bytes = bytearray()
    for i in range(256):
        r,g,b = palette[3*i:3*i+3]
        rgb555 = (r >> 3) | ((g >> 3) << 5) | ((b >> 3) << 10)
        pal_bytes += rgb555.to_bytes(2, "little")
    assert len(pal_bytes) == 512
    TITLE_DIR.mkdir(parents=True, exist_ok=True)
    (TITLE_DIR / "PJR_TitleScreen_Mode4.8bpp").write_bytes(raw)
    (TITLE_DIR / "PJR_TitleScreen_Mode4.gbapal").write_bytes(pal_bytes)
    print("TITLE_ART_PASS 240x160, 8bpp, 256 palette entries")

def patch_title():
    path = "src/title_screen.c"
    # Preserve the separately animated sprite for PRESS START.
    replace_exact(path,
        "        LoadPjrTitlePaletteBrightened();",
        "        LoadPalette(sPjrTitlePalette, BG_PLTT_ID(0), sizeof(sPjrTitlePalette));")
    replace_exact(path,
        "        CreatePressStartBanner(START_BANNER_X, 138);\n"
        "        CreateTask(Task_PjrTitleScreenInput, 0);",
        "        CreatePressStartBanner(START_BANNER_X, 138);\n"
        "        CreateTask(Task_PjrTitleScreenInput, 0);")
    # The above equality no-op intentionally checks the native blinking
    # PRESS START path is preserved. Begin black -> normal palette fade.
    replace_exact(path,
        "        SetVBlankCallback(VBlankCB);\n"
        "        SetMainCallback2(MainCB2);\n"
        "        gMain.state++;\n"
        "        break;\n"
        "    }\n"
        "}\n"
        "\n"
        "static void Task_PjrTitleScreenInput",
        "        SetVBlankCallback(VBlankCB);\n"
        "        BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);\n"
        "        SetMainCallback2(MainCB2);\n"
        "        gMain.state++;\n"
        "        break;\n"
        "    }\n"
        "}\n"
        "\n"
        "static void Task_PjrTitleScreenInput")
    print("TITLE_FLOW_PASS Last Wish black fade -> approved art with flashing sprite")

def main():
    install_last_wish()
    patch_boot_flow()
    install_title_art()
    patch_title()

if __name__ == "__main__":
    main()
