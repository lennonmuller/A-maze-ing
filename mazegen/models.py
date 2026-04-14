from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class Cell:
    """
    Represents a single cell in the maze grid.

    Attributes:
        x (int): horizontal position (column)
        y (int): vertical position (row)
        walls (int): bitmask representing cell walls

    Bitmask convention:
        - 1: North
        - 2: East
        - 4: South
        - 8: West

    Default value:
        15 (1111 in binary) → all walls closed
    """
    x: int
    y: int
    walls: int = 15
    visited: bool = False


@dataclass
class MazeData:
    """
    Main data structure representing the maze.

    Attributes:
        width (int): number of columns
        height (int): number of rows
        entry (Tuple[int, int]): entry position (x, y)
        exit (Tuple[int, int]): exit position (x, y)
        output_file (str): output file name/path
        perfect (bool): indicates if maze has no cycles
        seed (int): random seed for generation
        grid (List[List[Cell]]): 2D grid of cells
        solution_path (List[Tuple[int, int]]): path from entry to exit
    """
    width: int
    height: int
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    output_file: str
    perfect: bool
    solution_path: List[Tuple[int, int]] = field(default_factory=list)
    seed: int = 42
    grid: List[List[Cell]] = field(default_factory=list)
