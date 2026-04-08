''' Lógica da classe MazeGenerator '''


class MazeGenerator:
    def __init__(self, width: int, height: int) -> None:
        self._validade_input(width, height)
        self.width = width
        self.height = height
        self.maze = self._generate_maze()

    def _validate_input(self, width: int, height: int) -> None:
        if not isinstance(width, int) or not isinstance(height, int):
            raise TypeError("Width and Height must be integers")

        if width <= 0 or height <= 0:
            raise ValueError("Width and Height cannot be negative or zero")

        if width <= 5 or height <= 5:
            raise ValueError("Maze too small, for create a '42' pattern"
                             " introduce a bigger value")

        if width > 500 or height > 500:
            raise ValueError("Too big maze, please introduce a smaller value")

    def _generate_maze(self) -> list[list[int]]:
        return [[15 for _ in range(self.width)] for _ in range(self.height)]

    def get_maze(self) -> list[list[int]]:
        return self.maze


# Fase 1 escolha de algoritimo (DFS)
