"""Maze solving logic using breadth-first search (BFS)."""

from collections import deque
from typing import Deque

from mazegen.models import Cell, Wall

Coord = tuple[int, int]


def _valid_neighbors(grid: list[list[Cell]], x: int, y: int) -> list[Coord]:
    """Return neighbors that can be reached from one cell.

    A neighbor is valid only when the wall in that direction is open.
    """
    height = len(grid)
    width = len(grid[0])
    cell = grid[y][x]

    neighbors: list[Coord] = []

    if not cell.is_closed(Wall.NORTH) and y - 1 >= 0:
        neighbors.append((x, y - 1))
    if not cell.is_closed(Wall.EAST) and x + 1 < width:
        neighbors.append((x + 1, y))
    if not cell.is_closed(Wall.SOUTH) and y + 1 < height:
        neighbors.append((x, y + 1))
    if not cell.is_closed(Wall.WEST) and x - 1 >= 0:
        neighbors.append((x - 1, y))

    return neighbors


def solve_shortest_path(
    grid: list[list[Cell]],
    start: Coord,
    goal: Coord
) -> list[Coord]:
    """Find the shortest path from start to goal.

    The function uses BFS, so the first path to reach `goal` is the
    shortest one in number of moves.

    Args:
        grid: Maze grid.
        start: Start coordinate (x, y).
        goal: Goal coordinate (x, y).

    Returns:
        List of coordinates from start to goal.
        Returns an empty list if no path exists.
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
    """
    Translate a lis of coordinates to directions
    """
    if not path or len(path) < 2:
        return ""

    directions = []

    for i in range(len(path) - 1):
        curr = path[i]
        nxt = path[i + 1]

        dx = nxt[0] - curr[0]
        dy = nxt[1] - curr[1]

        if dy == -1:
            directions.append("N")
        elif dx == 1:
            directions.append("E")
        elif dy == 1:
            directions.append("S")
        elif dx == -1:
            directions.append("W")

    return "".join(directions)
