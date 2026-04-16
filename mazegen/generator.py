"""
Maze generation logic.

This file implements DFS (Depth-First Search)
to create a perfect maze.

It uses Cell and Wall from models.
"""

from mazegen.models import Cell, Wall, MazeData
import random


class MazeGenerator:
    """
    Generates a maze using DFS with backtracking.

    The maze is a grid of Cell objects.
    Each cell starts with all walls closed (value = 15).

    The algorithm walks through the grid, removes walls,
    and connects all cells.

    Result: a perfect maze (no loops, all cells reachable).
    """

    DIRECTIONS = {
        (0, -1): Wall.NORTH,
        (1, 0): Wall.EAST,
        (0, 1): Wall.SOUTH,
        (-1, 0): Wall.WEST,
    }

    OPPOSITE = {
        Wall.NORTH: Wall.SOUTH,
        Wall.SOUTH: Wall.NORTH,
        Wall.EAST: Wall.WEST,
        Wall.WEST: Wall.EAST,
    }

    PATTERN_42 = [
        [1, 0, 1, 0, 1, 1, 1],
        [1, 0, 1, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1],
        [0, 0, 1, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 1, 1],
    ]

    P_WIDTH = 7
    P_HEIGHT = 5
    # GRID 5X7

    def __init__(self, data: MazeData) -> None:
        """
        Create a maze generator.

        Args:
            width: number of columns
            height: number of rows

        The maze is generated automatically on creation.
        """

        self.data = data

        self._validate_input(data.width, data.height)

        self.width = data.width
        self.height = data.height

        self.seed = data.seed
        random.seed(self.seed)

    def _validate_input(self, width: int, height: int) -> None:
        """
        Check if width and height are valid.

        Raises:
            TypeError: if values are not integers
            ValueError: if values are too small, too big, or invalid
        """
        if not isinstance(width, int) or not isinstance(height, int):
            raise TypeError("Width and Height must be integers")

        if width <= 0 or height <= 0:
            raise ValueError("Width and Height must be > 0")

    def _create_grid(self) -> list[list[Cell]]:

        """
        Create the maze grid.

        Each cell starts with all walls closed.

        Returns:
            2D list of Cell objects
        """

        return [
            [Cell(x, y) for x in range(self.width)]
            for y in range(self.height)
        ]

    def _insert_42_pattern(self) -> bool:
        """
        Try to centralize 42 pattern,
        returns True if centrilize or False if
        grid is too small"""
        if (
            self.data.width < self.P_WIDTH + 4 or
            self.data.height < self.P_HEIGHT + 4
        ):
            print("The maze size is too small to display the '42' pattern.")
            return False

        start_x = (self.data.width - self.P_WIDTH) // 2
        start_y = (self.data.height - self.P_HEIGHT) // 2

        for py in range(self.P_HEIGHT):
            for px in range(self.P_WIDTH):
                if self.PATTERN_42[py][px] == 1:
                    target_x = start_x + px
                    target_y = start_y + py

                    cell = self.data.grid[target_y][target_x]

                    cell.walls = 15

                    cell.visited = True

        return True

    def _get_neighbors(
        self,
        cell: Cell
    ) -> list[tuple[Cell, Wall]]:

        """
        Get unvisited neighbors of a cell.

        Args:
            cell: current cell
            grid: maze grid

        Returns:
            List of (neighbor, direction)
        """

        neighbors = []

        for (dx, dy), direction in self.DIRECTIONS.items():
            nx = cell.x + dx
            ny = cell.y + dy

            if 0 <= nx < self.data.width and 0 <= ny < self.data.height:
                neighbor = self.data.grid[ny][nx]
                if not neighbor.visited:
                    neighbors.append((neighbor, direction))

        return neighbors

    def _remove_walls(self, cell_a: Cell, cell_b: Cell, direction: Wall):
        """
        Remove a wall between cell_a and cell_b,
        keeping the logic of opposite walls
        """
        cell_a.open_wall(direction)
        opposite_dir = self.OPPOSITE[direction]
        cell_b.open_wall(opposite_dir)

    def _imperfect_maze(self, chance: float = 0.05):
        """
        Remove random walls
        if PErfect = False
        """
        for y in range(1, self.data.height - 1):
            for x in range(1, self.data.width - 1):
                cell = self.data.grid[y][x]

                if cell.walls == 15:
                    continue

                if random.random() < chance:
                    direction = random.choice(list(self.DIRECTIONS.values()))

                    dx, dy = 0, 0
                    for d_coord, d_bit in self.DIRECTIONS.items():
                        if d_bit == direction:
                            dx, dy = d_coord

                    nx, ny = x + dx, y + dy
                    neighbor = self.data.grid[ny][nx]
                    if cell.is_closed(direction):
                        self._remove_walls(cell, neighbor, direction)

    def _generate_maze(self) -> MazeData:
        """
        Generate the maze using DFS.

        Steps:
            - Start at (0,0)
            - Visit random neighbor
            - Remove wall
            - Continue until no options
            - Backtrack

        Returns:
            Generated maze grid
        """
        self.data.grid = self._create_grid()
        self._insert_42_pattern()

        start_x, start_y = self.data.entry
        start_cell = self.data.grid[start_y][start_x]

        stack = [start_cell]
        start_cell.visited = True

        while stack:
            current = stack[-1]

            neighbors = self._get_neighbors(current)

            if neighbors:
                next_cell, direction = random.choice(neighbors)

                current.open_wall(direction)
                next_cell.open_wall(self.OPPOSITE[direction])

                next_cell.visited = True
                stack.append(next_cell)
            else:
                stack.pop()

        if not self.data.perfect:
            self._imperfect_maze()

        return self.data

    def get_maze(self) -> list[list[Cell]]:
        """
        Return the generated maze.

        Returns:
            Maze grid
        """
        return self._generate_maze()
