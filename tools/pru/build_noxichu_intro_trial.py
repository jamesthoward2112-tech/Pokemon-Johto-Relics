#!/usr/bin/env python3
"""Reproducible *test-only* PRU boot/title assembly.

Flow: short native copyright/startup -> original Last Wish Scene 0 -> black fade
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
from PIL import Image, ImageEnhance, ImageFilter

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
    # Keep the native copyright/startup sequence; bypass the HnS-specific
    # Gengar copyright/intro dispatch for this test variant only.
    old = "#elif IS_HNS\n    return SetUpCopyrightScreenHns();\n#endif"
    assert source.count(old) == 1
    source = source.replace(
        old,
        "#elif IS_HNS\n    // PRU test: use the native copyright/startup below.\n#endif",
    )
    # Preserve the short native startup/copyright and go STRAIGHT into
    # the original Last Wish. Do not start Scene 1: it is the full Emerald
    # bicycle/Groudon/Kyogre/Rayquaza montage that the user rejected.
    expansion_branch = ("#if EXPANSION_INTRO == TRUE\n"
                        "        SetMainCallback2(CB2_ExpansionIntro);\n"
                        "        CreateTask(Task_HandleExpansionIntro, 0);\n"
                        "#else\n"
                        "        CreateTask(Task_Scene1_Load, 0);\n"
                        "        SetMainCallback2(MainCB2_Intro);\n"
                        "#endif")
    assert source.count(expansion_branch) == 1, "Intro dispatch has changed"
    source = source.replace(
        expansion_branch,
        "        // PRU: Last Wish plays straight after short copyright startup.\n"
        "        SetMainCallback2(CB2_InitPRUHwlScene0);")
    assert "CreateTask(Task_Scene1_Load, 0);" not in source, "Vanilla Emerald movie still reachable"
    print("INTRO_DISPATCH_PASS startup -> Last Wish (no Emerald montage)")

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
    print("BOOT_FLOW_PASS short startup -> Jirachi/Celebi -> PRU title")

def install_title_art():
    # Approved pixel-art master: user's exact 1536x1024 PNG, not an earlier JPEG.
    # A 240x160 indexed 256-colour RGB555-ready conversion is committed losslessly.
    # The full-size original is archived at /PRU/Title Assets in the user's Library.
    path = Path("assets/pru_title/noxichu_cavern_master_240x160.png")
    data = path.read_bytes()
    assert hashlib.sha256(data).hexdigest() == "0f858bbbae95e1468c2e5d89436b19c2c5e28564b77d9429b5e15cae896d0434"
    indexed = Image.open(io.BytesIO(data))
    assert indexed.size == (240, 160) and indexed.mode == "P", (indexed.size, indexed.mode)
    assert len(indexed.getcolors(maxcolors=256)) <= 256
    qa = Path("PRU-QA")
    qa.mkdir(exist_ok=True)
    indexed.save(qa / "title-new-lossless-256-palette.png")
    indexed.resize((960,640), Image.Resampling.NEAREST).save(qa / "title-new-preview-4x.png")
    raw = indexed.tobytes()
    assert len(raw) == 38400
    palette = indexed.getpalette()
    assert palette and len(palette) >= 256 * 3
    out_pal = bytearray()
    for i in range(256):
        r, g, b = palette[3*i:3*i+3]
        rgb555 = (r >> 3) | ((g >> 3) << 5) | ((b >> 3) << 10)
        out_pal.extend(rgb555.to_bytes(2, "little"))
    assert len(out_pal) == 512
    TITLE_DIR.mkdir(parents=True, exist_ok=True)
    (TITLE_DIR / "PJR_TitleScreen_Mode4.8bpp").write_bytes(raw)
    (TITLE_DIR / "PJR_TitleScreen_Mode4.gbapal").write_bytes(out_pal)
    print("TITLE_ART_PASS exact original master -> lossless indexed 240x160, 256 colours, RGB555; no JPEG or extra sharpness")

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
