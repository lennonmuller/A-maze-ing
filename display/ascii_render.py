from mazegen.models import Cell, Wall


def render_maze(
    grid: list[list[Cell]],
    entry=None,
    exit=None,
) -> str:
    """
    Render maze in classic ASCII style (+, -, |)
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

            # conteúdo da célula (CENTRO)
            if (x, y) == entry:
                content = " S "
            elif (x, y) == exit:
                content = " E "
            elif cell.walls == 15:
                content = " 4 "
            else:
                content = "   "

            line_top += content

            # parede leste
            if cell.is_closed(Wall.EAST):
                line_top += "|"
            else:
                line_top += " "

            # parede sul
            if cell.is_closed(Wall.SOUTH):
                line_bottom += "---+"
            else:
                line_bottom += "   +"

        output.append(line_top)
        output.append(line_bottom)

    return "\n".join(output)
