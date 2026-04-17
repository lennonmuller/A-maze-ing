"""Maze generation logic.

This module builds a maze grid using depth-first search (DFS) with
backtracking. It can also add a closed "42" pattern and create extra
openings when `perfect` is disabled.
"""

from mazegen.models import Cell, Wall, MazeData
import random


class MazeGenerator:
    """Build a maze grid from the given maze settings.

    The main algorithm is DFS with backtracking. Every cell starts with
    all walls closed. During generation, walls are opened to connect cells.
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
        """Store maze settings and initialize random seed.

        Args:
            data: MazeData object with size, entry, exit, and flags.
        """

        self.data = data

        self.width = data.width
        self.height = data.height
        self.pattern_cells: set[tuple[int, int]] = set()

        self.seed = data.seed
        random.seed(self.seed)

    def _create_grid(self) -> list[list[Cell]]:
        """Create a new grid where all cells start fully closed.

        Returns:
            A matrix of Cell objects indexed as grid[y][x].
        """

        return [
            [Cell(x, y) for x in range(self.width)]
            for y in range(self.height)
        ]

    def _insert_42_pattern(self) -> bool:
        """Insert the closed "42" pattern near the center of the grid.

        Returns:
            True if the pattern was inserted.
            False if the maze is too small for the pattern.
        """
        if (
            self.data.width < self.P_WIDTH + 4 or
            self.data.height < self.P_HEIGHT + 4
        ):
            print("The maze size is too small to display the '42' pattern.")
            return False

        start_x = self._center_start(self.data.width, self.P_WIDTH)
        start_y = self._center_start(self.data.height, self.P_HEIGHT)

        self.pattern_cells.clear()

        for py in range(self.P_HEIGHT):
            for px in range(self.P_WIDTH):
                if self.PATTERN_42[py][px] == 1:
                    target_x = start_x + px
                    target_y = start_y + py

                    cell = self.data.grid[target_y][target_x]
                    self.pattern_cells.add((target_x, target_y))

                    cell.walls = 15

                    cell.visited = True

        return True

    def _center_start(self, total_size: int, part_size: int) -> int:
        """Return centered start index for a part inside a total length.

        If free space is odd, one side will naturally have one extra cell.
        """
        return (total_size - part_size) // 2

    def _get_neighbors(
        self,
        cell: Cell
    ) -> list[tuple[Cell, Wall]]:
        """Return all unvisited valid neighbors of one cell.

        Args:
            cell: Current position in the DFS walk.

        Returns:
            A list of tuples (neighbor_cell, direction_to_neighbor).
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
        """Open the wall between two adjacent cells.

        This function opens the wall in `cell_a` and also opens the
        opposite wall in `cell_b`.
        """
        cell_a.open_wall(direction)
        opposite_dir = self.OPPOSITE[direction]
        cell_b.open_wall(opposite_dir)

    def _imperfect_maze(self, chance: float = 0.05):
        """Open extra random walls to create loops.

        This step runs only when the maze is not perfect. It skips border
        cells and skips the locked cells that belong to the "42" pattern.

        Args:
            chance: Probability of trying one extra opening per cell.
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

                    if (nx, ny) in self.pattern_cells:
                        continue

                    neighbor = self.data.grid[ny][nx]
                    if cell.is_closed(direction):
                        self._remove_walls(cell, neighbor, direction)

    def _seal_outer_walls(self) -> None:
        """Force all external borders to stay closed."""
        for x in range(self.width):
            self.data.grid[0][x].walls |= Wall.NORTH
            self.data.grid[self.height - 1][x].walls |= Wall.SOUTH

        for y in range(self.height):
            self.data.grid[y][0].walls |= Wall.WEST
            self.data.grid[y][self.width - 1].walls |= Wall.EAST

    def _generate_maze(self) -> MazeData:
        """Generate one maze and return the updated MazeData object.

        Flow:
            1. Build an empty closed grid.
            2. Lock pattern cells for "42".
            3. Run DFS from the entry point.
            4. Optionally open extra walls in imperfect mode.
            5. Seal all outer borders.

        Returns:
            MazeData with `grid` filled.
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

        self._seal_outer_walls()

        return self.data

    def get_maze(self) -> list[list[Cell]]:
        """Public method to generate and return maze data."""
        return self._generate_maze()
