"""ASCII renderer for maze preview in terminal.

This renderer can show start and exit points, optional shortest path,
and ANSI colors for walls and the "42" pattern.
"""

from mazegen.models import Cell, Wall


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
INNER_H_WALL = "---"
OUTER_H_WALL = "==="
INNER_V_WALL = "|"
OUTER_V_WALL = "!"


def colorize(text: str, color: str) -> str:
    """Wrap text with ANSI color code when color is supported."""
    prefix = ANSI_COLORS.get(color, "")
    if not prefix:
        return text
    return f"{prefix}{text}{ANSI_RESET}"


def render_maze(
    grid: list[list[Cell]],
    entry=None,
    exit=None,
    path: set[tuple[int, int]] | None = None,
    wall_color: str = "default",
    pattern_color: str = "default",
) -> str:
    """Render maze grid using classic ASCII borders.

    Args:
        grid: Maze matrix.
        entry: Coordinate for start marker.
        exit: Coordinate for exit marker.
        path: Optional set of cells that belong to solved path.
        wall_color: ANSI color name used for borders and walls.
        pattern_color: ANSI color name used for "42" pattern cells.

    Returns:
        Full maze drawing as a multiline string.
    """

    height = len(grid)
    width = len(grid[0])

    output = []

    # top border (always outer)
    output.append(
        colorize("+", wall_color) +
        "".join(
            colorize(f"{OUTER_H_WALL}+", wall_color)
            for _ in range(width)
        )
    )

    for y in range(height):
        line_top = colorize(OUTER_V_WALL, wall_color)
        line_bottom = colorize("+", wall_color)

        for x in range(width):
            cell = grid[y][x]

            # conteúdo da célula (CENTRO)
            if (x, y) == entry:
                content = " S "
            elif (x, y) == exit:
                content = " E "
            elif path is not None and (x, y) in path:
                content = " . "
            elif cell.walls == 15:
                content = colorize(" 4 ", pattern_color)
            else:
                content = "   "

            line_top += content

            # parede leste
            if cell.is_closed(Wall.EAST):
                east_wall = OUTER_V_WALL if x == width - 1 else INNER_V_WALL
                line_top += colorize(east_wall, wall_color)
            else:
                line_top += " "

            # parede sul
            if cell.is_closed(Wall.SOUTH):
                south_wall = OUTER_H_WALL if y == height - 1 else INNER_H_WALL
                line_bottom += (
                    colorize(south_wall, wall_color) +
                    colorize("+", wall_color)
                )
            else:
                line_bottom += "   " + colorize("+", wall_color)

        output.append(line_top)
        output.append(line_bottom)

    return "\n".join(output)
