"""Regression checks for PJR Reception Gate / Mt. Silver progression."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "data/maps/ReceptionGate_hns/scripts.inc"
HOF = ROOT / "data/maps/PokemonLeague_HallOfFame_hns/scripts.inc"
OAK = ROOT / "data/maps/PalletTown_Lab_hns/scripts.inc"

JOHTO_CHAMP = "FLAG_IS_CHAMPION"
KANTO_CHAMP = "FLAG_IS_KANTO_CHAMPION"
KANTO_GUARD = "FLAG_INDIGOJUNCTION_HIDE_KANTO_GUARD"
SILVER_GUARD = "FLAG_INDIGOJUNCTION_HIDE_SILVER_GUARD"


def parse_script(path):
    code = []
    labels = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("@", 1)[0].strip()
        if not line:
            continue
        if re.fullmatch(r"[A-Za-z0-9_]+::?", line):
            labels[line.rstrip(":")] = len(code)
        else:
            code.append(line)
    return code, labels


def run_gate(flags=()):
    code, labels = parse_script(GATE)
    flags = set(flags)
    pc = labels["ReceptionGate_OnTransition"]
    for _ in range(100):
        line = code[pc]
        pc += 1
        cmd, _, tail = line.partition(" ")
        args = [x.strip() for x in tail.split(",") if x.strip()]
        if cmd == "end":
            return flags
        if cmd == "goto_if_unset":
            if args[0] not in flags:
                pc = labels[args[1]]
        elif cmd == "goto_if_set":
            if args[0] in flags:
                pc = labels[args[1]]
        elif cmd == "setflag":
            flags.add(args[0])
        elif cmd == "clearflag":
            flags.discard(args[0])
        else:
            raise AssertionError(f"Unhandled command in gate transition: {line}")
    raise AssertionError("Gate transition did not terminate")


def block(text, label, next_label):
    m = re.search(rf"{re.escape(label)}::\n(.*?)(?={re.escape(next_label)}::)", text, re.S)
    if not m:
        raise AssertionError(f"Could not find block {label}")
    return m.group(1)


class MtSilverUnlockRegression(unittest.TestCase):
    def test_before_league_both_side_guards_are_visible(self):
        flags = run_gate([KANTO_GUARD, SILVER_GUARD])
        self.assertNotIn(KANTO_GUARD, flags)
        self.assertNotIn(SILVER_GUARD, flags)

    def test_first_league_clear_opens_kanto_but_keeps_mt_silver_locked(self):
        flags = run_gate([JOHTO_CHAMP, SILVER_GUARD])
        self.assertIn(KANTO_GUARD, flags)
        self.assertNotIn(SILVER_GUARD, flags)

    def test_second_league_clear_opens_mt_silver_and_repairs_old_save(self):
        flags = run_gate([JOHTO_CHAMP, KANTO_CHAMP])
        self.assertIn(KANTO_GUARD, flags)
        self.assertIn(SILVER_GUARD, flags)

    def test_hall_of_fame_sets_guards_at_exact_milestones(self):
        text = HOF.read_text(encoding="utf-8")
        first = block(
            text,
            "PokemonLeague_HallOfFame_EventScript_SetFirstGameClearFlags",
            "PokemonLeague_HallOfFame_EventScript_SetGameClearFlags",
        )
        second = block(
            text,
            "PokemonLeague_HallOfFame_EventScript_SetGameClearFlags",
            "PokemonLeague_HallOfFame_EventScript_SpawnAlolaMons",
        )
        self.assertIn(f"setflag {KANTO_GUARD}", first)
        self.assertNotIn(f"setflag {SILVER_GUARD}", first)
        self.assertIn(f"setflag {SILVER_GUARD}", second)
        self.assertIn(f"setflag {KANTO_CHAMP}", second)

    def test_sixteen_badges_alone_no_longer_unlock_mt_silver(self):
        text = OAK.read_text(encoding="utf-8")
        self.assertNotIn(f"setflag {SILVER_GUARD}", text)
        self.assertIn("Defeat LANCE and the ELITE FOUR", text)
        self.assertIn("FLAG_IS_KANTO_CHAMPION", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
