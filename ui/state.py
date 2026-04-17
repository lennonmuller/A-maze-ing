"""State model for one interactive UI session."""

from dataclasses import dataclass

from mazegen.models import MazeData


@dataclass
class UIState:
    """Store all mutable values used while menu is running."""

    maze_params: MazeData
    maze_data: MazeData
    show_path: bool = False
    wall_color: str = "default"
    pattern_color: str = "default"
