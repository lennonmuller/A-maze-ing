"""Parser utilities for maze configuration files."""

from __future__ import annotations

import os
from typing import Dict

from mazegen.models import MazeData
from maze_config.validator import validate_maze_data, validate_required_keys


def parse_config_file(file_path: str) -> MazeData:
    """Read a config file, parse values, and return validated MazeData.

    Args:
        file_path: Path to text config file with KEY=VALUE lines.

    Returns:
        MazeData with typed and validated values.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: '{file_path}' not found.")

    config: Dict[str, str] = {}

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
        width=int(config["WIDTH"]),
        height=int(config["HEIGHT"]),
        entry=_parse_coord(config["ENTRY"], "ENTRY"),
        exit=_parse_coord(config["EXIT"], "EXIT"),
        output_file=config["OUTPUT_FILE"],
        perfect=config["PERFECT"].lower() == "true",
        seed=int(config.get("SEED", 42)),
    )

    validate_maze_data(maze_data)
    return maze_data


def _parse_coord(raw: str, label: str) -> tuple[int, int]:
    """Convert one coordinate string from "x,y" format to tuple.

    Args:
        raw: Raw coordinate string.
        label: Field name used in error messages.

    Returns:
        Coordinate tuple in (x, y) order.
    """
    parts = raw.split(",")
    if len(parts) != 2:
        raise ValueError(f"{label} must be in format x,y")

    return int(parts[0]), int(parts[1])
