"""
Maze data structures.

This file contains the basic classes to build a maze.

Includes:
- Wall: direction constants (bitmask)
- Cell: represents one position in the grid
- MazeData: stores full maze configuration and grid

Other modules use this to generate and work with the maze.
"""

from dataclasses import dataclass
from typing import Tuple
from enum import IntEnum


class Wall(IntEnum):
    """
    Defines wall directions using numbers.

    Each value is a bit.
    Used to open or check walls in a cell.
    """
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8


@dataclass
class Cell:
    """
    One cell of the maze.

    Each cell has position (x, y) and walls.

    Walls use bitmask:
        1 = North
        2 = East
        4 = South
        8 = West

    Default walls = 15 (all closed)
    """
    x: int
    y: int
    walls: int = 15
    visited: bool = False

    def open_wall(self, wall: Wall) -> None:
        """
        Open one wall of the cell.

        Uses bit operation to remove the wall.
        """
        self.walls &= ~wall

    def is_closed(self, wall: Wall) -> bool:
        """
        Check if a wall is still closed.

        Returns:
            True if wall is closed
            False if wall is open
        """
        return bool(self.walls & wall)

    @property
    def hex_value(self) -> str:
        """
        Return walls value in hex (0-F).

        Useful for printing or exporting.
        """
        return hex(self.walls)[2:].upper()


@dataclass
class MazeData:
    """
    Stores all maze information.

    Includes size, entry/exit, and grid.

    Also stores solution path if needed.
    """
    width: int
    height: int
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    output_file: str
    perfect: bool
    seed: int = 42
