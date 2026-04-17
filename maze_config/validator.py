"""Validation helpers for maze configuration data."""

from typing import Dict

from mazegen.models import MazeData


REQUIRED_KEYS = [
    "WIDTH",
    "HEIGHT",
    "ENTRY",
    "EXIT",
    "OUTPUT_FILE",
    "PERFECT",
]


def validate_required_keys(config: Dict[str, str]) -> None:
    """Check if all mandatory config keys are present.

    Args:
        config: Dictionary loaded from config text file.
    """
    for key in REQUIRED_KEYS:
        if key not in config:
            raise KeyError(f"Missing required key: {key}")


def validate_maze_data(data: MazeData) -> None:
    """Validate maze values after parsing.

    Rules checked here:
        - width and height must be positive
        - entry and exit must be inside bounds
        - entry and exit must be different points
    """
    if data.width <= 0 or data.height <= 0:
        raise ValueError("Width and Height must be > 0")

    if not (
        0 <= data.entry[0] < data.width and
        0 <= data.entry[1] < data.height
    ):
        raise ValueError("Entry is outside maze bounds")

    if not (
        0 <= data.exit[0] < data.width and
        0 <= data.exit[1] < data.height
    ):
        raise ValueError("Exit is outside maze bounds")

    if data.entry == data.exit:
        raise ValueError("Entry and Exit cannot be the same")
