#!/usr/bin/env python3
"""Small in-memory tests for Kanto wild encounter overlay (no ROM required)."""
import copy
import unittest

from rebalance_kanto_wild import is_kanto, patch

class KantoEncounterRules(unittest.TestCase):
    def setUp(self):
        self.data = {
            "wild_encounter_groups": [{
                "for_maps": True,
                "encounters": [
                    {"map": "MAP_ROUTE3_HNS",
                     "land_mons": {"mons": [
                         {"min_level": 45, "max_level": 48, "species": "SPECIES_WEEDLE"},
                         {"min_level": 41, "max_level": 45, "species": "SPECIES_METAPOD"},
                         {"min_level": 50, "max_level": 52, "species": "SPECIES_HOOTHOOT"},
                         {"min_level": 22, "max_level": 23, "species": "SPECIES_PIKACHU"},
                     ]}},
                    {"map": "MAP_MT_MOON_1F_HNS",
                     "land_mons": {"mons": [
                         {"min_level": 45, "max_level": 49, "species": "SPECIES_SPINARAK"},
                         {"min_level": 61, "max_level": 61, "species": "SPECIES_URSALUNA"},
                     ]}},
                    {"map": "MAP_ROUTE30_HNS",
                     "land_mons": {"mons": [
                         {"min_level": 50, "max_level": 50, "species": "SPECIES_WEEDLE"}
                     ]}},
                ],
            }]
        }
        self.roster = {
            "SPECIES_BEEDRILL", "SPECIES_BUTTERFREE",
            "SPECIES_NOCTOWL", "SPECIES_ARIADOS", "SPECIES_URSARING",
            "SPECIES_PIKACHU",
        }

    def test_only_kanto_hns(self):
        self.assertTrue(is_kanto("MAP_ROUTE3_HNS"))
        self.assertTrue(is_kanto("MAP_MT_MOON_1F_HNS"))
        self.assertFalse(is_kanto("MAP_ROUTE30_HNS"))
        self.assertFalse(is_kanto("MAP_ROUTE3"))
        self.assertFalse(is_kanto("MAP_ROUTE37_HNS"))

    def test_evolve_and_preserve_early_encounters(self):
        _, slots, changes = patch(self.data, self.roster)
        self.assertEqual(slots, 6)
        self.assertEqual(sum(changes.values()), 5)
        mons = self.data["wild_encounter_groups"][0]["encounters"]
        self.assertEqual([s["species"] for s in mons[0]["land_mons"]["mons"]], [
            "SPECIES_BEEDRILL", "SPECIES_BUTTERFREE",
            "SPECIES_NOCTOWL", "SPECIES_PIKACHU"])
        self.assertEqual([s["species"] for s in mons[1]["land_mons"]["mons"]], [
            "SPECIES_ARIADOS", "SPECIES_URSARING"])
        self.assertEqual(mons[2]["land_mons"]["mons"][0]["species"], "SPECIES_WEEDLE")

    def test_idempotence(self):
        patch(self.data, self.roster)
        _, _, changes = patch(self.data, self.roster)
        self.assertEqual(sum(changes.values()), 0)

    def test_unknown_species_blocks_release(self):
        wrong = copy.deepcopy(self.data)
        wrong["wild_encounter_groups"][0]["encounters"][0]["land_mons"]["mons"][0]["species"] = "SPECIES_IRON_BUNDLE"
        with self.assertRaisesRegex(ValueError, "outside PRU"):
            patch(wrong, self.roster)

if __name__ == "__main__":
    unittest.main()
