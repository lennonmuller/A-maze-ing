''' Maze generation logic using DFS (Depth-First Search) '''

from mazegen.models import Cell
import random


class MazeGenerator:
    """
    Class responsible for generating a maze using DFS with backtracking.

    The maze is represented as a grid of Cell objects.
    Each cell starts with all walls closed (value = 15).

    The algorithm removes walls between cells to create paths,
    ensuring all cells are connected with no cycles(perfect maze).
    """

    def __init__(self, width: int, height: int) -> None:
        """
        Initialize the generator with maze dimensions.

        Args:
            width (int): number of columns
            height (int): number of rows
        """
        self._validate_input(width, height)
        self.width = width
        self.height = height
        self.maze = self._generate_maze()

    def _validate_input(self, width: int, height: int) -> None:
        """
        Validate input values for maze size.

        Raises:
            TypeError: if width or height are not integers
            ValueError: if values are out of allowed range
        """
        if not isinstance(width, int) or not isinstance(height, int):
            raise TypeError("Width and Height must be integers")

        if width <= 0 or height <= 0:
            raise ValueError("Width and Height cannot be negative or zero")

        if width <= 5 or height <= 5:
            raise ValueError("Maze too small, choose bigger values")

        if width > 500 or height > 500:
            raise ValueError("Maze too big, choose smaller values")

    def _create_grid(self) -> list[list[Cell]]:
        """
        Create a grid of cells with all walls closed.

        Returns:
            list[list[Cell]]: 2D list of Cell objects
        """
        return [
            [Cell(x, y) for x in range(self.width)]
            for y in range(self.height)
        ]

    def _remove_wall(self, current: Cell, next: Cell) -> None:
        """
        Remove walls between two adjacent cells.

        This function updates both cells to keep consistency.

        Args:
            current (Cell): current cell
            next (Cell): neighbor cell
        """
        dx = next.x - current.x
        dy = next.y - current.y

        if dx == 1:  # next is to the East
            current.walls &= ~2
            next.walls &= ~8

        elif dx == -1:  # next is to the West
            current.walls &= ~8
            next.walls &= ~2

        elif dy == 1:  # next is to the South
            current.walls &= ~4
            next.walls &= ~1

        elif dy == -1:  # next is to the North
            current.walls &= ~1
            next.walls &= ~4

    def _get_neighbors(self, cell: Cell, grid: list[list[Cell]]) -> list[Cell]:
        """
        Get all unvisited neighbors of a cell.

        Args:
            cell (Cell): current cell
            grid (list[list[Cell]]): maze grid

        Returns:
            list[Cell]: list of unvisited neighbor cells
        """
        directions = [
            (0, -1),  # North
            (1, 0),   # East
            (0, 1),   # South
            (-1, 0)   # West
        ]

        neighbors = []

        for dx, dy in directions:
            nx = cell.x + dx
            ny = cell.y + dy

            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbor = grid[ny][nx]
                if not neighbor.visited:
                    neighbors.append(neighbor)

        return neighbors

    def _generate_maze(self) -> list[list[Cell]]:
        """
        Generate the maze using DFS (Depth-First Search).

        Algorithm:
            - Start from (0,0)
            - Visit random neighbors
            - Remove walls between cells
            - Backtrack when no neighbors available

        Returns:
            list[list[Cell]]: generated maze grid
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
                next_cell = random.choice(neighbors)

                self._remove_wall(current, next_cell)

                next_cell.visited = True
                stack.append(next_cell)
            else:
                stack.pop()

        return grid

    def get_maze(self) -> list[list[Cell]]:
        """
        Get the generated maze.

        Returns:
            list[list[Cell]]: maze grid
        """
        return self.maze
