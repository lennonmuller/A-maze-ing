"""Core data models used by maze generation, solving, and rendering."""

from dataclasses import dataclass
from typing import Tuple
from enum import IntEnum


class Wall(IntEnum):
    """Wall direction bits used in Cell.walls bitmask.

    Each value is a power of two. This allows wall operations using
    bitwise logic.
    """
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8


@dataclass
class Cell:
    """Single maze cell with position, wall bits, and visit state.

    `walls` starts at 15, meaning all four walls are closed.
    """
    x: int
    y: int
    walls: int = 15
    visited: bool = False

    def open_wall(self, wall: Wall) -> None:
        """Open one wall by clearing its bit from the mask."""
        self.walls &= ~wall

    def is_closed(self, wall: Wall) -> bool:
        """Return True when the selected wall bit is still set."""
        return bool(self.walls & wall)

    @property
    def hex_value(self) -> str:
        """Return wall bitmask as uppercase hex text (0-F)."""
        return hex(self.walls)[2:].upper()


@dataclass
class MazeData:
    """Full maze configuration shared across project modules."""
    width: int
    height: int
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    output_file: str
    perfect: bool
    seed: int = 42
