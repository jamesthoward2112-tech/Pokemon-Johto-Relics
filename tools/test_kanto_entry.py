"""Regression checks for PJR's one-time Kanto initialization.

The post-League game can enter Kanto either via S.S. Aqua or Route 22/Viridian.
Both paths must use the same initializer, while existing progressed saves must not
have badges or Kanto progress reset.
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "data/scripts/pjr_kanto_init.inc"

INIT = "FLAG_EXTENDED_CONTENT_111"
VIRIDIAN_BLUE = "FLAG_HIDE_VIRIDIAN_BLUE"
DOJO_BLUE = "FLAG_HIDE_DOJO_BLUE"
BADGE16 = "FLAG_BADGE16_GET"


class InitScript:
    def __init__(self, flags=(), vars=None):
        self.flags = set(flags)
        self.vars = {
            "VAR_SSAQUA_STATE": 0,
            "VAR_NUM_BADGES": 8,
            "VAR_KANTO_ROCKET_STORY_STATE": 0,
        }
        if vars:
            self.vars.update(vars)

        self.code = []
        self.labels = {}
        for raw in SCRIPT.read_text(encoding="utf-8").splitlines():
            line = raw.split("@")[0].strip()
            if not line:
                continue
            if re.fullmatch(r"\w+::?", line):
                self.labels[line.rstrip(":")] = len(self.code)
            else:
                self.code.append(line)

    def run(self, label="Common_EventScript_PJRInitKanto"):
        pc = self.labels[label]
        for _ in range(500):
            line = self.code[pc]
            pc += 1
            cmd, _, tail = line.partition(" ")
            args = [x.strip() for x in tail.split(",") if x.strip()]

            if cmd == "return":
                return
            if cmd == "goto_if_set":
                if args[0] in self.flags:
                    pc = self.labels[args[1]]
            elif cmd == "goto_if_unset":
                if args[0] not in self.flags:
                    pc = self.labels[args[1]]
            elif cmd == "goto_if_ge":
                if self.vars.get(args[0], 0) >= int(args[1], 0):
                    pc = self.labels[args[2]]
            elif cmd == "setflag":
                self.flags.add(args[0])
            elif cmd == "clearflag":
                self.flags.discard(args[0])
            elif cmd == "setvar":
                self.vars[args[0]] = int(args[1], 0)
            else:
                raise AssertionError(f"Unhandled command: {line}")
        raise AssertionError("Kanto initializer did not terminate")


class KantoEntryRegression(unittest.TestCase):
    def test_clean_route22_entry_gets_full_kanto_defaults(self):
        s = InitScript()
        s.run()
        self.assertIn(INIT, s.flags)
        self.assertIn(VIRIDIAN_BLUE, s.flags)
        self.assertIn(DOJO_BLUE, s.flags)
        self.assertEqual(s.vars["VAR_NUM_BADGES"], 8)

    def test_existing_badge_save_is_marked_without_reset(self):
        s = InitScript([BADGE16], {"VAR_NUM_BADGES": 9})
        s.run()
        self.assertIn(INIT, s.flags)
        self.assertIn(BADGE16, s.flags)
        self.assertEqual(s.vars["VAR_NUM_BADGES"], 9)
        self.assertNotIn(VIRIDIAN_BLUE, s.flags)

    def test_existing_ferry_save_is_marked_without_reset(self):
        preserved = "FLAG_GOT_VIRIDIAN_TM_DREAM_EATER"
        s = InitScript([preserved], {"VAR_SSAQUA_STATE": 7})
        s.run()
        self.assertIn(INIT, s.flags)
        self.assertIn(preserved, s.flags)
        self.assertEqual(s.vars["VAR_SSAQUA_STATE"], 7)

    def test_both_kanto_entry_paths_call_shared_initializer(self):
        aqua = (ROOT / "data/maps/SSAqua_1F_hns/scripts.inc").read_text(encoding="utf-8")
        viridian = (ROOT / "data/maps/ViridianCity_hns/scripts.inc").read_text(encoding="utf-8")
        self.assertIn("call Common_EventScript_PJRInitKanto", aqua)
        self.assertIn("call Common_EventScript_PJRInitKanto", viridian)

    def test_initializer_does_not_strip_kanto_champion(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertNotIn("clearflag FLAG_IS_KANTO_CHAMPION", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
