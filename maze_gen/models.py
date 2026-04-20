"""Data classes and wall flags used by the maze app."""

from dataclasses import dataclass
from enum import IntEnum


class Wall(IntEnum):
    """Bit values for cell walls."""
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8


@dataclass
class Cell:
    """One maze cell with walls and visit state."""
    x: int
    y: int
    walls: int = 15
    visited: bool = False

    def open_wall(self, wall: Wall) -> None:
        """Open one wall bit."""
        self.walls &= ~wall

    def is_closed(self, wall: Wall) -> bool:
        """Return True if a wall is still closed."""
        return bool(self.walls & wall)

    @property
    def hex_value(self) -> str:
        """Return walls as one uppercase hex digit."""
        return hex(self.walls)[2:].upper()


@dataclass
class MazeData:
    """All maze settings shared by modules."""
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int = 42
