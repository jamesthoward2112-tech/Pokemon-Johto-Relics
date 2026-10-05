"""Regression checks for PJR Indigo Plateau battlefield-control move tutors."""
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "data" / "maps" / "IndigoPlateau_PokemonCenter_hns" / "scripts.inc"
MAP = ROOT / "data" / "maps" / "IndigoPlateau_PokemonCenter_hns" / "map.json"
CHOOSEBOX = ROOT / "src" / "chooseboxmon.c"
PARTY_CONSTANTS = ROOT / "include" / "constants" / "party_menu.h"
PJR_FAMILIES = ROOT / "src" / "data" / "pokemon" / "species_info" / "pjr_families.h"

HAZARD_MOVES = [
    "MOVE_STEALTH_ROCK", "MOVE_SPIKES", "MOVE_TOXIC_SPIKES", "MOVE_STICKY_WEB",
    "MOVE_STONE_AXE", "MOVE_CEASELESS_EDGE", "MOVE_SALT_CURE", "MOVE_LEECH_SEED",
    "MOVE_TOXIC", "MOVE_WILL_O_WISP", "MOVE_THUNDER_WAVE", "MOVE_TAUNT",
    "MOVE_ENCORE", "MOVE_KNOCK_OFF", "MOVE_ROAR", "MOVE_WHIRLWIND",
    "MOVE_DRAGON_TAIL", "MOVE_INFESTATION",
]

CLEANUP_MOVES = [
    "MOVE_RAPID_SPIN", "MOVE_DEFOG", "MOVE_MORTAL_SPIN", "MOVE_TIDY_UP",
    "MOVE_COURT_CHANGE", "MOVE_HAZE", "MOVE_CLEAR_SMOG", "MOVE_BRICK_BREAK",
    "MOVE_PSYCHIC_FANGS", "MOVE_ICE_SPINNER", "MOVE_HEAL_BELL",
    "MOVE_AROMATHERAPY", "MOVE_U_TURN", "MOVE_VOLT_SWITCH", "MOVE_FLIP_TURN",
    "MOVE_PARTING_SHOT", "MOVE_SNARL", "MOVE_ICY_WIND", "MOVE_BREAKING_SWIPE",
    "MOVE_CHILLING_WATER", "MOVE_ACID_SPRAY", "MOVE_NUZZLE",
]

def text() -> str:
    return SCRIPT.read_text(encoding="utf-8")

def block(label: str, next_label: str | None = None) -> str:
    source = text()
    start = source.index(label + "::")
    if next_label:
        end = source.index(next_label + "::", start)
        return source[start:end]
    return source[start:]

class TestIndigoControlTutors(unittest.TestCase):
    def test_existing_indigo_npcs_are_reused(self):
        source = text()
        self.assertRegex(
            source,
            r"IndigoPlateau_EventScript_Cooltrainer::\s+goto IndigoPlateau_EventScript_HazardTutor",
        )
        self.assertRegex(
            source,
            r"IndigoPlateau_EventScript_ShigyNinja::\s+goto IndigoPlateau_EventScript_CleanupTutor",
        )

    def test_hazard_tutor_has_locked_move_set(self):
        section = block(
            "IndigoPlateau_EventScript_HazardTutor",
            "IndigoPlateau_EventScript_CleanupTutor",
        )
        self.assertEqual(section.count("case "), len(HAZARD_MOVES) + 2)
        source = text()
        for move in HAZARD_MOVES:
            self.assertRegex(source, rf"setvar VAR_0x8005, {move}\b")

    def test_cleanup_tutor_has_locked_move_set(self):
        section = block(
            "IndigoPlateau_EventScript_CleanupTutor",
            "IndigoPlateau_EventScript_TutorTeach_StealthRock",
        )
        self.assertEqual(section.count("case "), len(CLEANUP_MOVES) + 2)
        source = text()
        for move in CLEANUP_MOVES:
            self.assertRegex(source, rf"setvar VAR_0x8005, {move}\b")

    def test_tutors_are_free_repeatable_and_use_logical_compatibility(self):
        source = text()
        common = block(
            "IndigoPlateau_EventScript_TutorTeachMove",
            "IndigoPlateau_EventScript_TutorCancelled",
        )
        self.assertIn("chooseboxmon SELECT_PC_MON_PJR_CONTROL_TUTOR", common)
        self.assertNotRegex(common, r"removeitem|removemoney|setflag")
        self.assertNotRegex(
            block(
                "IndigoPlateau_EventScript_HazardTutor",
                "IndigoPlateau_EventScript_TutorTeach_StealthRock",
            ),
            r"checkitem|checkmoney|goto_if_set|setflag",
        )

        choosebox = CHOOSEBOX.read_text(encoding="utf-8")
        constants = PARTY_CONSTANTS.read_text(encoding="utf-8")
        self.assertIn("SELECT_PC_MON_PJR_CONTROL_TUTOR", constants)
        self.assertIn(
            "[SELECT_PC_MON_PJR_CONTROL_TUTOR] = {ChooseMonForMoveTutor, "
            "CanMonLearnPjrControlMove, MoveTutor_AfterChooseBoxMon, FALSE}",
            choosebox,
        )

        # These tutors keep normal compatibility, then add logical type-based
        # fallback only for Relic-series custom species.
        self.assertIn("if (CanLearnTeachableMove(species, move))", choosebox)
        self.assertIn(
            "if (species < SPECIES_SCARABUB || species > SPECIES_DRAGONITE_RELIC)",
            choosebox,
        )
        self.assertIn("CanSpeciesLearnPjrControlTutorMove(species, gSpecialVar_0x8005)", choosebox)
        self.assertNotIn("if (IsPjrControlTutorMove(gSpecialVar_0x8005))", choosebox)
        for move in HAZARD_MOVES + CLEANUP_MOVES:
            self.assertIn(f"case {move}:", choosebox)

        # Representative type rules: not universal, but the obvious archetypes are covered.
        self.assertRegex(
            choosebox,
            r"(?s)case MOVE_STONE_AXE:.*?TYPE_ROCK.*?TYPE_GROUND.*?TYPE_FIGHTING",
        )
        self.assertRegex(
            choosebox,
            r"(?s)case MOVE_TOXIC_SPIKES:.*?TYPE_POISON",
        )
        self.assertRegex(
            choosebox,
            r"(?s)case MOVE_DEFOG:.*?TYPE_FLYING",
        )
        self.assertRegex(
            choosebox,
            r"(?s)case MOVE_FLIP_TURN:.*?TYPE_WATER",
        )

        # Shuckoloose is Bug/Rock, so it receives the intended Rock tutor access.
        pjr_families = PJR_FAMILIES.read_text(encoding="utf-8")
        self.assertRegex(
            pjr_families,
            r"SPECIES_SHUCKOLOSSE.*?TYPE_BUG, TYPE_ROCK",
        )

        # Normal tutor/TM compatibility remains intact outside these two NPCs.
        self.assertIn(
            "CanLearnTeachableMove(GetBoxMonData(boxmon, MON_DATA_SPECIES), "
            "gSpecialVar_0x8005)",
            choosebox,
        )

    def test_cleanup_tutor_npc_is_static(self):
        data = json.loads(MAP.read_text(encoding="utf-8"))
        npc = next(
            obj for obj in data["object_events"]
            if obj.get("script") == "IndigoPlateau_EventScript_ShigyNinja"
        )
        self.assertEqual(npc["movement_type"], "MOVEMENT_TYPE_NONE")
        self.assertEqual(npc["movement_range_x"], 0)
        self.assertEqual(npc["movement_range_y"], 0)

    def test_transport_npcs_are_not_repurposed(self):
        source = text()
        self.assertIn("IndigoPlateau_EventScript_Psychic::", source)
        self.assertIn("IndigoPlateau_EventScript_Abra::", source)
        self.assertIn("warpteleport MAP_NEW_BARK_TOWN_HNS, 20, 12", source)

if __name__ == "__main__":
    unittest.main()
