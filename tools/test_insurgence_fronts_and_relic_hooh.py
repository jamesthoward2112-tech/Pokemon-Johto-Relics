"""Regression coverage for the Insurgence front-fit pass and Relic Ho-Oh roof unlock."""
from pathlib import Path
import hashlib
import unittest
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]

EXPECTED = {
    "miltitan": ("837e005fcff828c97012f6c92da71f0cc3d4d44e204bfae54b15d9ef6f202854", (64, 47)),
    "sudowarden": ("afa828cdfb92ba16c95450ad2c231be54026a7fe0d1cb9211a2d918927113313", (43, 60)),
    "donphalanx": ("718ca63f5f6784544b4de40d6d931895e3092d5a56d7d8385c3cb9306f6556a9", (64, 43)),
    "faeranium": ("d8268eca5ec2378d68ee3ae21569c81443ca111745b4b4a21bdd4bc8e83c3622", (48, 60)),
    "pyroclast": ("18b72e8c9422b25a581fdb66e00fb01bc7bc32b27578c9d56ae901d3a8d11c8e", (55, 60)),
}

def ink_bbox(path):
    im = Image.open(path)
    self_pixels = im.load()
    xs, ys = [], []
    for y in range(im.height):
        for x in range(im.width):
            if self_pixels[x, y] != 0:
                xs.append(x)
                ys.append(y)
    b = (min(xs), min(ys), max(xs) + 1, max(ys) + 1)
    return b, (b[2] - b[0], b[3] - b[1])

class InsurgenceFrontFitRegression(unittest.TestCase):
    def test_fronts_are_locked_and_fit(self):
        for name, (expected_hash, expected_ink) in EXPECTED.items():
            path = ROOT / "graphics" / "pokemon" / "pjr_locked" / name / "front.png"
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), expected_hash, name)
            im = Image.open(path)
            self.assertEqual(im.size, (64, 64), name)
            self.assertEqual(ink_bbox(path)[1], expected_ink, name)
            self.assertLessEqual(len(im.getcolors(maxcolors=9999) or []), 16, name)

    def test_locked_non_insurgence_visuals_not_overwritten(self):
        script = (ROOT / "tools" / "apply_insurgence_front_fit.py").read_text(encoding="utf-8")
        self.assertNotIn('"feralodon":', script)
        self.assertNotIn('"heracurion":', script)

class RelicHoOhRoofRegression(unittest.TestCase):
    def test_roof_self_heals_stale_progress_var(self):
        text = (ROOT / "data" / "maps" / "TinTower_RoofDay_hns" / "scripts.inc").read_text(encoding="utf-8")
        self.assertIn("call TinTower_RoofDay_EventScript_SyncRelicHoOhState", text)
        for flag in (
            "FLAG_PJR_RELIC_RAIKOU", "FLAG_PJR_RELIC_ENTEI", "FLAG_PJR_RELIC_LUGIA",
            "FLAG_PJR_RELIC_UNOWN_I", "FLAG_PJR_RELIC_CELEBI", "FLAG_PJR_RELIC_SUICUNE",
            "FLAG_PJR_RELIC_ALPHORACLE", "FLAG_PJR_GOT_RAINBOW_CREST",
        ):
            self.assertIn(f"goto_if_unset {flag}, TinTower_RoofDay_EventScript_SyncRelicHoOhDone", text)
        self.assertIn("setvar VAR_COMPLETED_HO_OH, 4", text)
        self.assertIn("clearflag FLAG_HIDE_HO_OH", text)
        self.assertIn("setobjectxyperm LOCALID_HO_OH, 10, 6", text)
        self.assertIn("seteventmon SPECIES_RELIC_HO_OH, 85", text)

if __name__ == "__main__":
    unittest.main(verbosity=2)
