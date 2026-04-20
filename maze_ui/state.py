"""State object used by the terminal UI."""

from dataclasses import dataclass

from maze_gen.models import MazeData


@dataclass
class UIState:
    """Keep mutable values while menu loop runs."""

    maze_params: MazeData
    maze_data: MazeData
    show_path: bool = False
    wall_color: str = "default"
    pattern_color: str = "default"
    status_message: str = ""
