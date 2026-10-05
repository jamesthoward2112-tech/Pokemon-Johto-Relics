"""Regression checks for the Whack a Hack Scarabub front sprite."""
from pathlib import Path
import hashlib
import struct
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/pjr_whackahack/scarabub_xiros_source.png"
FRONT = ROOT / "graphics/pokemon/pjr_locked/scarabub/front.png"

SOURCE_SHA256 = "d37d5aa361fc5725d9eeb174f02f241387006b7e3a0f83b25bbb7951f5ee895b"
FRONT_SHA256 = "aa8c053ae2333f2f36197007e4b35447f4df7b51c79f4fea1857b6d6543800bd"

def png_size(path):
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise AssertionError(f"{path} is not a PNG")
    return struct.unpack(">II", data[16:24])

class ScarabubSpriteRegression(unittest.TestCase):
    def test_source_is_locked(self):
        self.assertEqual(hashlib.sha256(SOURCE.read_bytes()).hexdigest(), SOURCE_SHA256)
        self.assertEqual(png_size(SOURCE), (39, 44))

    def test_gba_front_is_locked(self):
        self.assertEqual(hashlib.sha256(FRONT.read_bytes()).hexdigest(), FRONT_SHA256)
        self.assertEqual(png_size(FRONT), (64, 64))

if __name__ == "__main__":
    unittest.main(verbosity=2)
