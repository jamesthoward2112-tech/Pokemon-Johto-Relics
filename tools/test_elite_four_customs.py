"""Regression audit for custom PJR Pokemon across all Elite Four tiers."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PARTIES = ROOT / "src/data/trainers_hns.party"

CUSTOM = {
    "Alakazam Relic", "Slowking Relic", "Beedrill Relic", "Crobat Relic",
    "Hitmonchan Relic", "Hitmonlee Relic", "Machamp Relic", "Houndoom Relic",
    "Gyarados Relic", "Dragonite Relic", "Heracurion", "Champeon", "Grimfowl",
    "Donphalanx", "Mystynx", "Toxeon", "Feralodon", "Drakeon", "Charaxis",
    "Skarmadon",
}

FIRST = [
    "TRAINER_WILL_1_HNS", "TRAINER_KOGA_1_HNS", "TRAINER_BRUNO_1_HNS",
    "TRAINER_KAREN_1_HNS", "TRAINER_LANCE_1_HNS",
]
REMATCH = [
    "TRAINER_WILL_2_HNS", "TRAINER_KOGA_2_HNS", "TRAINER_BRUNO_2_HNS",
    "TRAINER_KAREN_2_HNS", "TRAINER_LANCE_2_HNS",
]
POST = [
    "TRAINER_WILL_POSTOBC_HNS", "TRAINER_KOGA_POSTOBC_HNS",
    "TRAINER_BRUNO_POSTOBC_HNS", "TRAINER_KAREN_POSTOBC_HNS",
    "TRAINER_LANCE_POSTOBC_HNS",
]


def roster(label):
    text = PARTIES.read_text(encoding="utf-8")
    m = re.search(rf"^=== {re.escape(label)} ===\n(.*?)(?=^=== |\Z)", text, re.M | re.S)
    if not m:
        raise AssertionError(f"Missing trainer block: {label}")
    lines = m.group(1).splitlines()
    mons = []
    for i, line in enumerate(lines):
        s = line.strip()
        if not s or ":" in s or s.startswith("-"):
            continue
        for j in range(i + 1, min(len(lines), i + 10)):
            t = lines[j].strip()
            if not t:
                break
            if t.startswith("Level:"):
                mons.append(s.split(" @ ", 1)[0].strip())
                break
    return mons


class EliteFourCustomAudit(unittest.TestCase):
    def test_first_clear_each_member_has_custom_presence(self):
        for label in FIRST:
            with self.subTest(label=label):
                mons = roster(label)
                self.assertGreaterEqual(sum(m in CUSTOM for m in mons), 2, mons)

    def test_standard_rematch_each_member_has_at_least_three_customs(self):
        for label in REMATCH:
            with self.subTest(label=label):
                mons = roster(label)
                self.assertGreaterEqual(sum(m in CUSTOM for m in mons), 3, mons)

    def test_post_obc_each_member_has_at_least_three_customs(self):
        for label in POST:
            with self.subTest(label=label):
                mons = roster(label)
                self.assertGreaterEqual(sum(m in CUSTOM for m in mons), 3, mons)

    def test_lance_standard_rematch_is_fully_custom(self):
        mons = roster("TRAINER_LANCE_2_HNS")
        self.assertEqual(len(mons), 6, mons)
        self.assertTrue(all(m in CUSTOM for m in mons), mons)

    def test_lance_post_obc_is_fully_custom(self):
        mons = roster("TRAINER_LANCE_POSTOBC_HNS")
        self.assertEqual(len(mons), 6, mons)
        self.assertTrue(all(m in CUSTOM for m in mons), mons)


if __name__ == "__main__":
    unittest.main(verbosity=2)
