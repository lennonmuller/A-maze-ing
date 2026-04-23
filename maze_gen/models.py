"""Data models and wall flags used by the maze app."""

from dataclasses import dataclass, field
from enum import IntEnum


class Wall(IntEnum):
    """Bit values that represent cell walls."""
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8


@dataclass
class Cell:
    """Represent one maze cell with walls and visit state."""
    x: int
    y: int
    walls: int = 15
    visited: bool = False

    def open_wall(self, wall: Wall) -> None:
        """Open one wall for this cell.

        Args:
            wall: Wall direction to open.
        """
        self.walls &= ~wall

    def is_closed(self, wall: Wall) -> bool:
        """Check if one wall is still closed.

        Args:
            wall: Wall direction to check.

        Returns:
            bool: ``True`` if this wall is closed.
        """
        return bool(self.walls & wall)

    @property
    def hex_value(self) -> str:
        """Return wall bitmask as one uppercase hex digit.

        Returns:
            str: Hex value from ``0`` to ``F``.
        """
        return hex(self.walls)[2:].upper()


@dataclass
class MazeData:
    """Store maze configuration and generated runtime fields."""
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int = 42
    algorithm: str = "DFS"
    grid: list[list[Cell]] = field(default_factory=list)
    pattern_warning: str = ""
