"""State object used by the terminal UI."""

from dataclasses import dataclass

from maze_gen.models import MazeData
from maze_ui.constants import DEFAULT_PATTERN_COLOR, DEFAULT_WALL_COLOR


@dataclass
class UIState:
    """Keep mutable values while menu loop runs."""

    maze_params: MazeData
    maze_data: MazeData
    show_path: bool = False
    wall_color: str = DEFAULT_WALL_COLOR
    pattern_color: str = DEFAULT_PATTERN_COLOR
    status_message: str = ""
