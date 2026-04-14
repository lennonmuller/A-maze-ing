from mazegen.models import Cell, Wall


def render_maze(
        grid: list[list[Cell]],
        entry=None,
        exit=None,
) -> str:

    """
    Render maze as ASCII.

    Returns a string with the maze drawing.
    """

    height = len(grid)
    width = len(grid[0])

    output = []

    # top border
    output.append("+" + "---+" * width)

    for y in range(height):
        line_top = "|"
        line_bottom = "+"

        for x in range(width):
            cell = grid[y][x]

            # space inside cell
            if (x, y) == entry:
                line_top += " E "
            elif (x, y) == exit:
                line_top += " X "
            else:
                line_top += "   "

            # east wall
            if cell.is_closed(Wall.EAST):
                line_top += "|"
            else:
                line_top += " "

            # south wall
            if cell.is_closed(Wall.SOUTH):
                line_bottom += "---+"
            else:
                line_bottom += "   +"

        output.append(line_top)
        output.append(line_bottom)

    return "\n".join(output)
