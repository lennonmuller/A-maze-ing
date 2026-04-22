"""Read and parse maze config file."""

import os

from maze_gen.models import MazeData
from maze_config.validator import validate_maze_data, validate_required_keys


def parse_config_file(file_path: str) -> MazeData:
    """Load config text, parse values, validate, and return MazeData."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"'{file_path}' not found.")

    config: dict[str, str] = {}

    with open(file_path, "r", encoding="utf-8") as file:
        for line_num, line in enumerate(file, 1):
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                raise KeyError(
                    f"Error on line {line_num}: bad format. Use KEY=VALUE"
                )

            key, value = line.split("=", 1)
            config[key.strip()] = value.strip()

    validate_required_keys(config)

    maze_data = MazeData(
        width=_parse_int(config["WIDTH"], "WIDTH"),
        height=_parse_int(config["HEIGHT"], "HEIGHT"),
        entry=_parse_coord(config["ENTRY"], "ENTRY"),
        exit=_parse_coord(config["EXIT"], "EXIT"),
        output_file=config["OUTPUT_FILE"],
        perfect=_parse_bool(config["PERFECT"], "PERFECT"),
        seed=_parse_int(config.get("SEED", "42"), "SEED"),
    )

    validate_maze_data(maze_data)
    return maze_data


def _parse_coord(raw: str, label: str) -> tuple[int, int]:
    """Convert one x,y string to a tuple of integers."""
    parts = raw.split(",")
    if len(parts) != 2:
        raise ValueError(f"{label} must be in format x,y")

    return (
        _parse_int(parts[0], f"{label}.x"),
        _parse_int(parts[1], f"{label}.y"),
    )


def _parse_int(raw: str, label: str) -> int:
    """Convert string to int and show field name on error."""
    try:
        return int(raw)
    except ValueError as exc:
        raise ValueError(f"{label} must be an integer") from exc


def _parse_bool(raw: str, label: str) -> bool:
    """Convert string to bool. Only True or False is accepted."""
    value = raw.strip().lower()
    if value == "true":
        return True
    if value == "false":
        return False
    raise ValueError(f"{label} must be True or False")
