"""Validate parsed maze config data."""

from maze_gen.models import MazeData


REQUIRED_KEYS = [
    "WIDTH",
    "HEIGHT",
    "ENTRY",
    "EXIT",
    "OUTPUT_FILE",
    "PERFECT",
]


def validate_required_keys(config: dict[str, str]) -> None:
    """Check that all required keys exist."""
    for key in REQUIRED_KEYS:
        if key not in config:
            raise KeyError(f"Missing required key: {key}")


def validate_maze_data(data: MazeData) -> None:
    """Check maze values like size, bounds, and output file name."""
    if data.width <= 0 or data.height <= 0:
        raise ValueError("Width and Height must be > 0")

    if not _in_bounds(data.entry, data.width, data.height):
        raise ValueError("Entry is outside maze bounds")

    if not _in_bounds(data.exit, data.width, data.height):
        raise ValueError("Exit is outside maze bounds")

    if data.entry == data.exit:
        raise ValueError("Entry and Exit cannot be the same")

    if not data.output_file.strip():
        raise ValueError("OUTPUT_FILE cannot be empty")


def _in_bounds(coord: tuple[int, int], width: int, height: int) -> bool:
    """Return True if coordinate is inside maze area."""
    x, y = coord
    return 0 <= x < width and 0 <= y < height
