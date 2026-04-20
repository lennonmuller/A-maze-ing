"""Render maze data as Unicode text for terminal output."""

from maze_gen.models import Cell, Wall


ANSI_COLORS = {
    "default": "",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
}
ANSI_RESET = "\033[0m"
ANSI_BG_COLORS = {
    "default": "",
    "red": "\033[41m",
    "green": "\033[42m",
    "yellow": "\033[43m",
    "blue": "\033[44m",
    "magenta": "\033[45m",
    "cyan": "\033[46m",
    "white": "\033[47m",
}
PATH_COLOR = "yellow"
CELL_WIDTH = 3

JUNCTIONS = {
    (False, False, False, False): " ",
    (False, False, False, True): "╶",
    (False, False, True, False): "╴",
    (False, False, True, True): "─",
    (False, True, False, False): "╷",
    (False, True, False, True): "┌",
    (False, True, True, False): "┐",
    (False, True, True, True): "┬",
    (True, False, False, False): "╵",
    (True, False, False, True): "└",
    (True, False, True, False): "┘",
    (True, False, True, True): "┴",
    (True, True, False, False): "│",
    (True, True, False, True): "├",
    (True, True, True, False): "┤",
    (True, True, True, True): "┼",
}

PATH_GLYPHS = dict(JUNCTIONS)
PATH_GLYPHS[(False, False, False, False)] = "•"


def colorize(text: str, color: str) -> str:
    """Apply ANSI text color when color is valid."""
    prefix = ANSI_COLORS.get(color, "")
    if not prefix:
        return text
    return f"{prefix}{text}{ANSI_RESET}"


def bg_colorize(text: str, color: str) -> str:
    """Apply ANSI background color when color is valid."""
    prefix = ANSI_BG_COLORS.get(color, "")
    if not prefix:
        return text
    return f"{prefix}{text}{ANSI_RESET}"


def render_maze(
    grid: list[list[Cell]],
    entry=None,
    exit=None,
    path: list[tuple[int, int]] | None = None,
    wall_color: str = "default",
    pattern_color: str = "default",
) -> str:
    """Return full maze drawing as one multiline string."""

    width = len(grid[0])
    height = len(grid)
    path_cells, h_edges, v_edges = _build_path_geometry(path)

    horizontal, vertical = _build_wall_maps(grid)
    output: list[str] = []

    for y in range(height + 1):
        output.append(
            _render_junction_row(
                horizontal=horizontal,
                vertical=vertical,
                y=y,
                wall_color=wall_color,
                v_edges=v_edges,
                width=width,
                height=height,
            )
        )

        if y == height:
            continue

        output.append(
            _render_cell_row(
                grid=grid,
                vertical=vertical,
                y=y,
                entry=entry,
                exit=exit,
                path_cells=path_cells,
                h_edges=h_edges,
                v_edges=v_edges,
                wall_color=wall_color,
                pattern_color=pattern_color,
                height=height,
            )
        )

    return "\n".join(output)


def _build_wall_maps(
    grid: list[list[Cell]],
) -> tuple[list[list[bool]], list[list[bool]]]:
    """Convert cell walls to horizontal and vertical segment maps."""
    height = len(grid)
    width = len(grid[0])

    horizontal = [[False] * width for _ in range(height + 1)]
    vertical = [[False] * (width + 1) for _ in range(height)]

    for y in range(height):
        for x in range(width):
            cell = grid[y][x]

            if y == 0 and cell.is_closed(Wall.NORTH):
                horizontal[0][x] = True
            if cell.is_closed(Wall.SOUTH):
                horizontal[y + 1][x] = True

            if x == 0 and cell.is_closed(Wall.WEST):
                vertical[y][0] = True
            if cell.is_closed(Wall.EAST):
                vertical[y][x + 1] = True

    return horizontal, vertical


def _render_junction_row(
    horizontal: list[list[bool]],
    vertical: list[list[bool]],
    y: int,
    wall_color: str,
    v_edges: set[tuple[int, int]],
    width: int,
    height: int,
) -> str:
    """Render one row of junctions and horizontal walls."""
    row = ""

    for x in range(width + 1):
        up = y > 0 and vertical[y - 1][x]
        down = y < len(vertical) and vertical[y][x]
        left = x > 0 and horizontal[y][x - 1]
        right = x < width and horizontal[y][x]

        row += colorize(JUNCTIONS[(up, down, left, right)], wall_color)

        if x < width:
            row += _render_horizontal_segment(
                horizontal=horizontal,
                v_edges=v_edges,
                x=x,
                y=y,
                wall_color=wall_color,
                height=height,
            )

    return row


def _render_cell_row(
    grid: list[list[Cell]],
    vertical: list[list[bool]],
    y: int,
    entry,
    exit,
    path_cells: set[tuple[int, int]],
    h_edges: set[tuple[int, int]],
    v_edges: set[tuple[int, int]],
    wall_color: str,
    pattern_color: str,
    height: int,
) -> str:
    """Render one row with vertical walls and cell content."""
    width = len(grid[0])
    row = ""

    for x in range(width + 1):
        row += _render_vertical_segment(
            vertical=vertical,
            h_edges=h_edges,
            x=x,
            y=y,
            wall_color=wall_color,
            width=width,
        )

        if x == width:
            continue

        cell = grid[y][x]

        if (x, y) == entry:
            content = " S "
        elif (x, y) == exit:
            content = " E "
        elif (x, y) in path_cells:
            content = _render_path_cell(v_edges, h_edges, x, y, width, height)
        elif cell.walls == 15:
            content = bg_colorize("   ", pattern_color)
        else:
            content = "   "

        row += content

    return row


def _render_horizontal_segment(
    horizontal: list[list[bool]],
    v_edges: set[tuple[int, int]],
    x: int,
    y: int,
    wall_color: str,
    height: int,
) -> str:
    """Render one segment between two maze rows."""
    if horizontal[y][x]:
        return colorize("─" * CELL_WIDTH, wall_color)

    if _crosses_row_boundary(v_edges, x, y, height):
        return colorize(" │ ", PATH_COLOR)

    return " " * CELL_WIDTH


def _render_vertical_segment(
    vertical: list[list[bool]],
    h_edges: set[tuple[int, int]],
    x: int,
    y: int,
    wall_color: str,
    width: int,
) -> str:
    """Render one segment between two maze columns."""
    if vertical[y][x]:
        return colorize("│", wall_color)

    if _crosses_col_boundary(h_edges, x, y, width):
        return colorize("─", PATH_COLOR)

    return " "


def _render_path_cell(
    v_edges: set[tuple[int, int]],
    h_edges: set[tuple[int, int]],
    x: int,
    y: int,
    width: int,
    height: int,
) -> str:
    """Render center glyph for one path cell."""
    glyph = _path_glyph(v_edges, h_edges, x, y, width, height)
    return colorize(f" {glyph} ", PATH_COLOR)


def _path_glyph(
    v_edges: set[tuple[int, int]],
    h_edges: set[tuple[int, int]],
    x: int,
    y: int,
    width: int,
    height: int,
) -> str:
    """Return a box glyph based on path neighbors."""
    up = y > 0 and (x, y - 1) in v_edges
    down = y + 1 < height and (x, y) in v_edges
    left = x > 0 and (x - 1, y) in h_edges
    right = x + 1 < width and (x, y) in h_edges
    return PATH_GLYPHS[(up, down, left, right)]


def _build_path_geometry(
    path: list[tuple[int, int]] | None,
) -> tuple[set[tuple[int, int]], set[tuple[int, int]], set[tuple[int, int]]]:
    """Build path cells and edges from ordered path points."""
    if not path:
        return set(), set(), set()

    path_cells = set(path)
    horizontal_edges: set[tuple[int, int]] = set()
    vertical_edges: set[tuple[int, int]] = set()

    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]

        dx = x2 - x1
        dy = y2 - y1

        if abs(dx) + abs(dy) != 1:
            continue

        if dx != 0:
            horizontal_edges.add((min(x1, x2), y1))
        else:
            vertical_edges.add((x1, min(y1, y2)))

    return path_cells, horizontal_edges, vertical_edges


def _crosses_col_boundary(
    h_edges: set[tuple[int, int]],
    x: int,
    y: int,
    width: int,
) -> bool:
    """Return True if path goes through one vertical boundary."""
    if x <= 0 or x >= width:
        return False
    return (x - 1, y) in h_edges


def _crosses_row_boundary(
    v_edges: set[tuple[int, int]],
    x: int,
    y: int,
    height: int,
) -> bool:
    """Return True if path goes through one horizontal boundary."""
    if y <= 0 or y >= height:
        return False
    return (x, y - 1) in v_edges
