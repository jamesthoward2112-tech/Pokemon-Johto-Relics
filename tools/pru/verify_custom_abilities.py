#!/usr/bin/env python3
"""Static integration gate for the nine PRL abilities absent from PJR."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

ABILITIES = (
    "ANCIENT_GROVE",
    "SOLAR_DISCIPLINE",
    "TIDAL_BASTION",
    "ANCIENT_CORE",
    "WISHMAKER",
    "EDENS_CANOPY",
    "THERMAL_WINGS",
    "CITADEL_SHELL",
    "STYGIAN_RUSH",
)


def require(path: str, *needles: str) -> None:
    text = (ROOT / path).read_text()
    missing = [needle for needle in needles if needle not in text]
    if missing:
        raise AssertionError(f"{path}: missing {', '.join(missing)}")


def main() -> None:
    constants = (ROOT / "include/constants/abilities.h").read_text()
    anchor = constants.index("ABILITY_SACRED_REBIRTH")
    positions = [constants.index(f"ABILITY_{name}", anchor) for name in ABILITIES]
    if positions != sorted(positions):
        raise AssertionError("new PRL ability IDs are not append-only after frozen PJR abilities")

    require("src/data/abilities.h", *(f"[ABILITY_{name}]" for name in ABILITIES))
    require("include/battle.h", "prlAbilityTimer[MAX_BATTLERS_COUNT]")
    require("src/battle_end_turn.c", "ABILITY_ANCIENT_GROVE", "ABILITY_WISHMAKER")
    require(
        "src/battle_util.c",
        "ABILITY_SOLAR_DISCIPLINE",
        "ABILITY_TIDAL_BASTION",
        "ABILITY_ANCIENT_CORE",
        "ABILITY_EDENS_CANOPY",
        "ABILITY_THERMAL_WINGS",
        "ABILITY_CITADEL_SHELL",
    )
    require("src/battle_main.c", "ABILITY_STYGIAN_RUSH")
    require("src/battle_script_commands.c", "ABILITY_WISHMAKER", "ABILITY_CITADEL_SHELL")
    print("PRU custom ability integration verification passed")


if __name__ == "__main__":
    main()
