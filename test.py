from mazegen.models import Cell, Wall


def test_bits():
    c = Cell(0, 0)
    print(f"Inicio (todas fechadas): {c.walls} (hex: {c.hex_value})\n")

    c.open_wall(Wall.NORTH)
    print(f"abriu norte: {c.walls} (hexa: {c.hex_value})\n")

    print(f"valor em hexadecimal: {c.hex_value}\n")

    c.open_wall(Wall.SOUTH)
    print(f"Abriu sul: {c.walls} (hex: {c.hex_value})")

    if c.hex_value == 'A':
        print(" verificacao: teste open_walls executado com sucesso")


if __name__ == "__main__":
    test_bits()
