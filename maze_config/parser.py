"""Read and parse a maze configuration file."""

import os

from maze_gen.models import MazeData
from maze_config.validator import validate_maze_data, validate_required_keys


def parse_config_file(file_path: str) -> MazeData:
    """Parse a config file and return validated maze data.

    Args:
        file_path: Path to the config file.

    Returns:
        MazeData: Validated configuration object.

    Raises:
        FileNotFoundError: If the config file does not exist.
        KeyError: If a line has invalid format or a required key is missing.
        ValueError: If one value has invalid type or content.
    """
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
    """Convert one ``x,y`` text to integer coordinates.

    Args:
        raw: Coordinate text in ``x,y`` format.
        label: Field name used in error messages.

    Returns:
        tuple[int, int]: Parsed ``(x, y)`` coordinates.

    Raises:
        ValueError: If format or values are invalid.
    """
    parts = raw.split(",")
    if len(parts) != 2:
        raise ValueError(f"{label} must be in format x,y")

    return (
        _parse_int(parts[0], f"{label}.x"),
        _parse_int(parts[1], f"{label}.y"),
    )


def _parse_int(raw: str, label: str) -> int:
    """Convert a string to integer.

    Args:
        raw: Text value to convert.
        label: Field name used in error messages.

    Returns:
        int: Parsed integer value.

    Raises:
        ValueError: If conversion fails.
    """
    try:
        return int(raw)
    except ValueError as exc:
        raise ValueError(f"{label} must be an integer") from exc


def _parse_bool(raw: str, label: str) -> bool:
    """Convert a string to boolean.

    Args:
        raw: Text value to convert.
        label: Field name used in error messages.

    Returns:
        bool: Parsed boolean value.

    Raises:
        ValueError: If value is not ``True`` or ``False``.
    """
    value = raw.strip().lower()
    if value == "true":
        return True
    if value == "false":
        return False
    raise ValueError(f"{label} must be True or False")
