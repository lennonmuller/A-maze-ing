"""MazeGen - Standalone maze generation module.

Public API for the maze generator package.
"""

from maze_gen.generator import MazeGenerator
from maze_gen import constants
from maze_gen.models import MazeData, Cell, Wall
from maze_gen.solver import solve_shortest_path, coords_to_directions

__all__ = [
    "MazeGenerator",
    "MazeData",
    "Cell",
    "Wall",
    "solve_shortest_path",
    "coords_to_directions",
    "constants",
]

__version__ = "1.0.0"
__author__ = "lmuler-f, eamaral-"
