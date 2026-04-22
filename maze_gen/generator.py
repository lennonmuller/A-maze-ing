"""Generate maze grids from MazeData settings."""

from collections.abc import Callable
from maze_gen.models import Cell, Wall, MazeData
import random


class MazeGenerator:
    """Build a maze using DFS and optional extra openings."""

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

    DELTA_BY_DIRECTION = {
        value: key for key, value in DIRECTIONS.items()
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

    def __init__(self, data: MazeData) -> None:
        """Store settings and initialize random seed."""

        self.data = data

        self.width = data.width
        self.height = data.height
        self.pattern_cells: set[tuple[int, int]] = set()

        self.seed = data.seed
        random.seed(self.seed)

    def _create_grid(self) -> list[list[Cell]]:
        """Create a new grid with all walls closed."""

        return [
            [Cell(x, y) for x in range(self.width)]
            for y in range(self.height)
        ]

    def _insert_42_pattern(self) -> None:
        """Insert and lock the 42 pattern cells."""
        min_width = self.P_WIDTH + 4
        min_height = self.P_HEIGHT + 4

        if (
            self.data.width < min_width or
            self.data.height < min_height
        ):
            self.data.pattern_warning = (
                "Warning: maze too small for '42' pattern "
                f"({self.data.width}x{self.data.height}). "
                f"Minimum supported size: {min_width}x{min_height}."
            )
            return

        self.data.pattern_warning = ""

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

    def _center_start(self, total_size: int, part_size: int) -> int:
        """Return centered start index for a segment."""
        return (total_size - part_size) // 2

    def _get_neighbors(
        self,
        cell: Cell
    ) -> list[tuple[Cell, Wall]]:
        """Return unvisited neighbor cells with directions."""

        neighbors = []

        for (dx, dy), direction in self.DIRECTIONS.items():
            nx = cell.x + dx
            ny = cell.y + dy

            if 0 <= nx < self.data.width and 0 <= ny < self.data.height:
                neighbor = self.data.grid[ny][nx]
                if not neighbor.visited:
                    neighbors.append((neighbor, direction))

        return neighbors

    def _remove_walls(
        self,
        cell_a: Cell,
        cell_b: Cell,
        direction: Wall,
    ) -> None:
        """Open the shared wall between two cells."""
        cell_a.open_wall(direction)
        opposite_dir = self.OPPOSITE[direction]
        cell_b.open_wall(opposite_dir)

    def _imperfect_maze(
        self,
        chance: float = 0.05,
        on_step: Callable[[MazeData], None] | None = None,
    ) -> None:
        """Open random extra walls to create loops."""
        for y in range(1, self.data.height - 1):
            for x in range(1, self.data.width - 1):
                cell = self.data.grid[y][x]

                if cell.walls == 15:
                    continue

                if random.random() < chance:
                    direction = random.choice(list(self.DIRECTIONS.values()))

                    dx, dy = self.DELTA_BY_DIRECTION[direction]

                    nx, ny = x + dx, y + dy

                    if (nx, ny) in self.pattern_cells:
                        continue

                    neighbor = self.data.grid[ny][nx]
                    if cell.is_closed(direction):
                        self._remove_walls(cell, neighbor, direction)
                        if on_step is not None:
                            on_step(self.data)

    def _seal_outer_walls(self) -> None:
        """Force all outer borders to stay closed."""
        for x in range(self.width):
            self.data.grid[0][x].walls |= Wall.NORTH
            self.data.grid[self.height - 1][x].walls |= Wall.SOUTH

        for y in range(self.height):
            self.data.grid[y][0].walls |= Wall.WEST
            self.data.grid[y][self.width - 1].walls |= Wall.EAST

    def _generate_maze(
        self,
        on_step: Callable[[MazeData], None] | None = None,
    ) -> MazeData:
        """Generate maze and return updated MazeData."""
        self.data.grid = self._create_grid()
        self._insert_42_pattern()
        if on_step is not None:
            on_step(self.data)

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
                if on_step is not None:
                    on_step(self.data)
            else:
                stack.pop()

        if not self.data.perfect:
            self._imperfect_maze(on_step=on_step)

        self._seal_outer_walls()
        if on_step is not None:
            on_step(self.data)

        return self.data

    @staticmethod
    def save_maze_to_file(data: MazeData, solution_str: str) -> None:
        """Write maze hex rows and solution data to file."""
        with open(data.output_file, "w", encoding="utf-8") as file:
            for row in data.grid:
                hex_row = "".join(cell.hex_value for cell in row)
                file.write(f"{hex_row}\n")

            file.write("\n")
            file.write(f"{data.entry[0]},{data.entry[1]}\n")
            file.write(f"{data.exit[0]},{data.exit[1]}\n")
            file.write(f"{solution_str}\n")

    def get_maze(
        self,
        on_step: Callable[[MazeData], None] | None = None,
    ) -> MazeData:
        """Run generation and return the maze data object."""
        return self._generate_maze(on_step=on_step)
