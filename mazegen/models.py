''' Classes de dados (Cell, Point, etc.) '''

from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class MazeData:
    grid: List[List[int]]  # Matriz de inteiros (0-15) seguindo o bitmask
    width: int
    height: int
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    solution_path: List[Tuple[int, int]]  # caminho curto
