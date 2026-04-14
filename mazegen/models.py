from dataclasses import dataclass, field
from typing import List, Tuple
from enum import IntEnum


class Wall(IntEnum):
    """Bit mapping (Cap IV.5)"""
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8


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

    def open_wall(self, wall: Wall) -> None:
        """Abre uma parede especifica usando operacao bitwise NOT e AND"""
        self.walls &= ~wall  # manipulando bits individuais

    def is_closed(self, wall: Wall) -> bool:
        return bool(self.walls & wall)  # verifica se a parede esta fechada

    @property
    def hex_value(self) -> str:
        """Retorna a celula em hexadecimal (0-F)"""
        return hex(self.walls)[2:].upper()  # remove "0x" e deixa maiusculo


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
    # o caminho e uma lista de coordenadas
    solution_path: List[Tuple[int, int]] = field(default_factory=list)
    seed: int = 42
    # a grade e uma matriz de objetos cell
    grid: List[List[Cell]] = field(default_factory=list)

    def __post_init__(self):
        """Inicializa o grid apos a criacao do mazedata"""
        if not self.grid:  # se o grid esta vazio
            self.grid = [
                [Cell(x, y) for x in range(self.width)]
                for y in range(self.height)
            ]
        # cria uma matriz de celulas onde cada celula recebe suas coordenadas
        # garante que grid nasca preenchida com paredes fechadas
