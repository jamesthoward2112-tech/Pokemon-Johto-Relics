"""Regression checks for the Mt. Silver sign shortcut to Red."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "data" / "maps" / "MtSilver_Outside_hns" / "scripts.inc"
SUMMIT = ROOT / "data" / "maps" / "MtSilver_SummitDay_hns" / "map.json"

class TestMtSilverRedShortcut(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script = SCRIPT.read_text(encoding="utf-8")
        cls.summit = SUMMIT.read_text(encoding="utf-8")

    def test_sign_offers_shortcut(self):
        self.assertIn("MtSilver_Outside_EventScript_Sign::", self.script)
        self.assertIn("MSGBOX_YESNO", self.script)
        self.assertIn("case YES, MtSilver_Outside_EventScript_SummitShortcut", self.script)

    def test_shortcut_warps_near_red(self):
        self.assertIn("warp MAP_MT_SILVER_SUMMIT_DAY_HNS, 10, 8", self.script)
        self.assertIn('"x": 10', self.summit)
        self.assertIn('"y": 6', self.summit)
        self.assertIn('"script": "MtSilver_SummitDay_EventScript_Red"', self.summit)

    def test_cancel_keeps_player_outside(self):
        self.assertIn("case NO, MtSilver_Outside_EventScript_SignCancel", self.script)
        self.assertIn("case MULTI_B_PRESSED, MtSilver_Outside_EventScript_SignCancel", self.script)

if __name__ == "__main__":
    unittest.main()
