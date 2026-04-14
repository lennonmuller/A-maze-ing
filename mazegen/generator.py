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

        if width <= 5 or height <= 5:
            raise ValueError("Maze too small")

        if width > 500 or height > 500:
            raise ValueError("Maze too big")

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

    def _get_neighbors(
        self,
        cell: Cell,
        grid: list[list[Cell]]
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

            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbor = grid[ny][nx]
                if not neighbor.visited:
                    neighbors.append((neighbor, direction))

        return neighbors

    def _generate_maze(self) -> list[list[Cell]]:
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
        grid = self._create_grid()

        stack = []
        start = grid[0][0]

        start.visited = True
        stack.append(start)

        while stack:
            current = stack[-1]

            neighbors = self._get_neighbors(current, grid)

            if neighbors:
                next_cell, direction = random.choice(neighbors)

                current.open_wall(direction)
                next_cell.open_wall(self.OPPOSITE[direction])

                next_cell.visited = True
                stack.append(next_cell)
            else:
                stack.pop()

        return grid

    def get_maze(self) -> list[list[Cell]]:
        """
        Return the generated maze.

        Returns:
            Maze grid
        """
        return self._generate_maze()
