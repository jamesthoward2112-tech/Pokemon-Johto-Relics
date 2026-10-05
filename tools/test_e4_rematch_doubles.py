"""Regression checks for the PJR second Elite Four Radical-style doubles rematch."""
from pathlib import Path
import hashlib
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PARTY = ROOT / "src" / "data" / "trainers_hns.party"

EXPECTED = {
    "TRAINER_WILL_2_HNS": [
        ("Slowking Relic", 66), ("Mystynx", 67), ("Exeggutor", 67),
        ("Grumpig", 67), ("Alakazam Relic", 66), ("Xatu", 68),
    ],
    "TRAINER_KOGA_2_HNS": [
        ("Toxeon", 67), ("Crobat Relic", 68), ("Muk", 67),
        ("Tentacruel", 67), ("Nidoking", 67), ("Beedrill Relic", 67),
    ],
    "TRAINER_BRUNO_2_HNS": [
        ("Steelix", 67), ("Obsideon", 68), ("Poliwrath", 68),
        ("Heracurion", 67), ("Hitmonchan Relic", 67), ("Machamp Relic", 68),
    ],
    "TRAINER_KAREN_2_HNS": [
        ("Umbreon", 68), ("Weavile", 67), ("Donphalanx", 68),
        ("Grimfowl", 68), ("Absol", 67), ("Houndoom Relic", 69),
    ],
    "TRAINER_LANCE_2_HNS": [
        ("Drakeon", 69), ("Skarmadon", 69), ("Gyarados Relic", 69),
        ("Feralodon", 70), ("Dragonite Relic", 68), ("Charaxis", 68),
    ],
}

GIMMICKS = {
    "TRAINER_WILL_2_HNS": [
        "Ability: Snow Warning", "- Trick Room", "- Aurora Veil",
        "- Imprison", "- Tailwind",
    ],
    "TRAINER_KOGA_2_HNS": [
        "- Toxic Spikes", "- Tailwind", "- Venom Drench",
        "- Icy Wind", "Ability: Lightning Rod",
    ],
    "TRAINER_BRUNO_2_HNS": [
        "Ability: Sturdy", "Ability: Sand Rush", "- Sandstorm", "- Stealth Rock",
        "- Wide Guard", "- Dynamic Punch",
    ],
    "TRAINER_KAREN_2_HNS": [
        "- Fake Out", "- Snarl", "Ability: Intimidate",
        "- Tailwind", "- Will-O-Wisp",
    ],
    "TRAINER_LANCE_2_HNS": [
        "Ability: Intimidate", "- Tailwind", "Ability: Tidal Roar",
        "@ Weakness Policy", "Ability: Gale Wings",
    ],
}

SPRITE_HASHES = {
    "graphics/pokemon/pjr_locked/skarmadon/front.png":
        "1ceaf9dd70bd3e5a0d8163adac1f4c6595eb704c5848bb4bf65f4274d83c5ad6",
    "graphics/pokemon/pjr_locked/donphalanx/front.png":
        "1f86fca8a24414ab94caaf4ff53f73e693f677e50ed695c1969d9f21b28eecd4",
}

def block(label: str) -> str:
    text = PARTY.read_text(encoding="utf-8")
    match = re.search(
        rf"^=== {re.escape(label)} ===\n(.*?)(?=^=== |\Z)",
        text,
        re.M | re.S,
    )
    if not match:
        raise AssertionError(f"Missing trainer block: {label}")
    return match.group(1)

def roster(section: str):
    lines = section.splitlines()
    mons = []
    for i, raw in enumerate(lines):
        s = raw.strip()
        if not s or ":" in s or s.startswith("-"):
            continue
        # A Pokémon header is followed by Level: before the next blank/header.
        for j in range(i + 1, min(i + 8, len(lines))):
            t = lines[j].strip()
            if t.startswith("Level:"):
                name = s.split(" @ ", 1)[0]
                mons.append((name, int(t.split(":", 1)[1].strip())))
                break
            if t and ":" not in t and not t.startswith("-"):
                break
    return mons

class TestE4RematchDoubles(unittest.TestCase):
    def test_all_rematches_are_smart_doubles(self):
        for label in EXPECTED:
            section = block(label)
            self.assertIn("Double Battle: Yes", section, label)
            self.assertIn("AI: Smart Trainer / Prediction", section, label)
            self.assertNotIn("Items: Full Restore", section, label)

    def test_rosters_and_original_levels_are_locked(self):
        for label, expected in EXPECTED.items():
            self.assertEqual(roster(block(label)), expected, label)

    def test_each_team_has_six(self):
        for label in EXPECTED:
            self.assertEqual(len(roster(block(label))), 6, label)

    def test_battle_identities_are_present(self):
        for label, markers in GIMMICKS.items():
            section = block(label)
            for marker in markers:
                self.assertIn(marker, section, f"{label}: {marker}")

    def test_corrected_skarmadon_and_donphalanx_front_sprites_are_retained(self):
        for rel, expected in SPRITE_HASHES.items():
            actual = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
            self.assertEqual(actual, expected, rel)

if __name__ == "__main__":
    unittest.main()
