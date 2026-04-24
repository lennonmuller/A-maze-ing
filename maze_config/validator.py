"""Validate parsed maze configuration data."""

from maze_gen.models import MazeData
from maze_gen.constants import SUPPORTED_ALGORITHMS
from maze_config.constants import (
    MAX_MAZE_AREA,
    MAX_MAZE_HEIGHT,
    MAX_MAZE_WIDTH,
)


REQUIRED_KEYS = [
    "WIDTH",
    "HEIGHT",
    "ENTRY",
    "EXIT",
    "OUTPUT_FILE",
    "PERFECT",
]


def validate_required_keys(config: dict[str, str]) -> None:
    """Check that all required keys are present.

    Args:
        config: Raw key/value map parsed from config file.

    Raises:
        KeyError: If one required key is missing.
    """
    for key in REQUIRED_KEYS:
        if key not in config:
            raise KeyError(f"Missing required key: {key}")


def validate_maze_data(data: MazeData) -> None:
    """Validate semantic rules for maze configuration.

    Args:
        data: Parsed maze configuration.

    Raises:
        ValueError: If one configuration rule is invalid.
    """
    if data.width <= 0 or data.height <= 0:
        raise ValueError("Width and Height must be > 0")

    if data.width > MAX_MAZE_WIDTH:
        raise ValueError(
            f"Width is too large for terminal UI (max {MAX_MAZE_WIDTH})"
        )

    if data.height > MAX_MAZE_HEIGHT:
        raise ValueError(
            f"Height is too large for terminal UI (max {MAX_MAZE_HEIGHT})"
        )

    area = data.width * data.height
    if area > MAX_MAZE_AREA:
        raise ValueError(
            f"Maze area is too large for terminal UI "
            f"(max {MAX_MAZE_AREA} cells)"
        )

    if data.algorithm not in SUPPORTED_ALGORITHMS:
        supported = ", ".join(SUPPORTED_ALGORITHMS)
        raise ValueError(
            f"Unsupported algorithm '{data.algorithm}'. "
            f"Use one of: {supported}"
        )

    if not _in_bounds(data.entry, data.width, data.height):
        raise ValueError("Entry is outside maze bounds")

    if not _in_bounds(data.exit, data.width, data.height):
        raise ValueError("Exit is outside maze bounds")

    if data.entry == data.exit:
        raise ValueError("Entry and Exit cannot be the same")

    if not data.output_file.strip():
        raise ValueError("OUTPUT_FILE cannot be empty")


def _in_bounds(coord: tuple[int, int], width: int, height: int) -> bool:
    """Check if one coordinate is inside maze bounds.

    Args:
        coord: Coordinate in ``(x, y)`` format.
        width: Maze width.
        height: Maze height.

    Returns:
        bool: ``True`` when coordinate is inside bounds.
    """
    x, y = coord
    return 0 <= x < width and 0 <= y < height
