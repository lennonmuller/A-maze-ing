"""Solve maze paths and export direction strings."""

from collections import deque
from typing import Deque

from maze_gen.models import Cell, Wall

Coord = tuple[int, int]
MOVE_RULES = [
    (Wall.NORTH, 0, -1),
    (Wall.EAST, 1, 0),
    (Wall.SOUTH, 0, 1),
    (Wall.WEST, -1, 0),
]

DIRECTION_BY_DELTA = {
    (0, -1): "N",
    (1, 0): "E",
    (0, 1): "S",
    (-1, 0): "W",
}


def _valid_neighbors(grid: list[list[Cell]], x: int, y: int) -> list[Coord]:
    """Return open neighbor coordinates for one cell.

    Args:
        grid: Maze grid.
        x: Cell x coordinate.
        y: Cell y coordinate.

    Returns:
        list[Coord]: Valid reachable neighbor coordinates.
    """
    height = len(grid)
    width = len(grid[0])
    cell = grid[y][x]

    neighbors: list[Coord] = []

    for wall, dx, dy in MOVE_RULES:
        nx = x + dx
        ny = y + dy
        if cell.is_closed(wall):
            continue
        if 0 <= nx < width and 0 <= ny < height:
            neighbors.append((nx, ny))

    return neighbors


def solve_shortest_path(
    grid: list[list[Cell]],
    start: Coord,
    goal: Coord
) -> list[Coord]:
    """Find shortest path between two points using BFS.

    Args:
        grid: Maze grid.
        start: Start coordinate.
        goal: Goal coordinate.

    Returns:
        list[Coord]: Ordered path from start to goal, or empty list.
    """
    if start == goal:
        return [start]

    queue: Deque[Coord] = deque([start])
    visited: set[Coord] = {start}
    parent: dict[Coord, Coord] = {}

    found = False

    while queue:
        current = queue.popleft()

        if current == goal:
            found = True
            break

        cx, cy = current
        for nxt in _valid_neighbors(grid, cx, cy):
            if nxt in visited:
                continue
            visited.add(nxt)
            parent[nxt] = current
            queue.append(nxt)

    if not found:
        return []

    path: list[Coord] = []
    node = goal
    while node != start:
        path.append(node)
        node = parent[node]
    path.append(start)
    path.reverse()
    return path


def coords_to_directions(path: list[Coord]) -> str:
    """Convert a coordinate path to ``N/E/S/W`` text.

    Args:
        path: Ordered coordinate path.

    Returns:
        str: Direction string.
    """
    if not path or len(path) < 2:
        return ""

    directions = []

    for curr, nxt in zip(path, path[1:]):

        dx = nxt[0] - curr[0]
        dy = nxt[1] - curr[1]

        step = DIRECTION_BY_DELTA.get((dx, dy))
        if step:
            directions.append(step)

    return "".join(directions)
