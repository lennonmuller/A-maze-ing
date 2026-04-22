"""Action functions used by the terminal menu."""

from collections.abc import Callable
import random

from maze_display.ascii_render import render_maze
from maze_gen.generator import MazeGenerator
from maze_gen.models import MazeData
from maze_gen.solver import solve_shortest_path, coords_to_directions
from maze_ui.constants import (
    APP_TITLE,
    MENU_FOOTER_TEXT,
    STATUS_NEW_MAZE,
    STATUS_NO_PATH,
    STATUS_PATH_OFF,
    STATUS_PATH_ON,
    STATUS_READY,
)
from maze_ui.state import UIState


def initialize_state(maze_params: MazeData) -> UIState:
    """Create UI state and generate first maze.

    Args:
        maze_params: Base maze configuration.

    Returns:
        UIState: Initialized UI state.
    """
    state = UIState(
        maze_params=maze_params,
        maze_data=_generate_maze(maze_params),
    )
    state.status_message = STATUS_READY
    return state


def initialize_state_with_animation(
    maze_params: MazeData,
    on_step: Callable[[MazeData], None],
) -> UIState:
    """Create UI state with animated generation.

    Args:
        maze_params: Base maze configuration.
        on_step: Callback called for each generation step.

    Returns:
        UIState: Initialized UI state.
    """
    state = UIState(
        maze_params=maze_params,
        maze_data=_generate_maze(maze_params, on_step=on_step),
    )
    state.status_message = STATUS_READY
    return state


def regenerate_maze(
    state: UIState,
    on_step: Callable[[MazeData], None] | None = None,
) -> None:
    """Generate a new maze using a fresh random seed.

    Args:
        state: Mutable UI state.
        on_step: Optional callback called for generation steps.
    """
    state.maze_params.seed = random.SystemRandom().randint(1, 10**9)
    state.maze_data = _generate_maze(state.maze_params, on_step=on_step)
    state.status_message = STATUS_NEW_MAZE


def toggle_path(state: UIState) -> None:
    """Toggle shortest-path visibility.

    Args:
        state: Mutable UI state.
    """
    state.show_path = not state.show_path
    if state.show_path:
        state.status_message = STATUS_PATH_ON
    else:
        state.status_message = STATUS_PATH_OFF


def compute_shortest_path(state: UIState) -> list[tuple[int, int]]:
    """Compute shortest path for current maze.

    Args:
        state: Mutable UI state.

    Returns:
        list[tuple[int, int]]: Path coordinates.
    """
    return solve_shortest_path(
        state.maze_data.grid,
        state.maze_data.entry,
        state.maze_data.exit,
    )


def update_wall_color(state: UIState, color: str) -> None:
    """Set wall color in UI state.

    Args:
        state: Mutable UI state.
        color: New wall color name.
    """
    state.wall_color = color
    state.status_message = f"Wall color: {color}."


def update_pattern_color(state: UIState, color: str) -> None:
    """Set ``42`` pattern color in UI state.

    Args:
        state: Mutable UI state.
        color: New pattern color name.
    """
    state.pattern_color = color
    state.status_message = f"Pattern color: {color}."


def render_current_maze(
    state: UIState,
    path_override: list[tuple[int, int]] | None = None,
) -> None:
    """Render current app frame.

    Args:
        state: Mutable UI state.
        path_override: Optional path used only for current render.
    """
    path_coords = (
        path_override
        if path_override is not None
        else _maze_path_set(state)
    )

    print("╔══════════════════════════════════════════════╗")
    print(f"║{APP_TITLE:^46}║")
    print("╚══════════════════════════════════════════════╝")
    if state.status_message:
        print(state.status_message)
    if state.maze_data.pattern_warning:
        print(state.maze_data.pattern_warning)
    print()

    maze_text = render_maze(
        state.maze_data.grid,
        entry=state.maze_data.entry,
        exit=state.maze_data.exit,
        path=path_coords,
        wall_color=state.wall_color,
        pattern_color=state.pattern_color,
    )
    for line in maze_text.splitlines():
        print(line)

    print(_render_menu_box(len(state.maze_data.grid[0]), MENU_FOOTER_TEXT))


def _generate_maze(
    maze_params: MazeData,
    on_step: Callable[[MazeData], None] | None = None,
) -> MazeData:
    """Generate maze, solve path, and write output file.

    Args:
        maze_params: Maze generation parameters.
        on_step: Optional callback called during generation.

    Returns:
        MazeData: Generated maze data.
    """
    generator = MazeGenerator(maze_params)
    data = generator.get_maze(on_step=on_step)

    path_coords = solve_shortest_path(data.grid, data.entry, data.exit)

    path_str = coords_to_directions(path_coords)

    MazeGenerator.save_maze_to_file(data, path_str)

    return data


def _maze_path_set(state: UIState) -> list[tuple[int, int]] | None:
    """Return path only when path view is enabled.

    Args:
        state: Mutable UI state.

    Returns:
        list[tuple[int, int]] | None: Path, empty path, or ``None``.
    """
    if not state.show_path:
        return None

    path = compute_shortest_path(state)

    if not path:
        state.status_message = STATUS_NO_PATH
        return []

    return path


def _render_menu_box(grid_width: int, text: str) -> str:
    """Render a framed text box for menu options.

    Args:
        grid_width: Maze width used to scale box size.
        text: Footer menu text.

    Returns:
        str: Box text with three lines.
    """
    frame_width = grid_width * 4 + 1
    inner_width = max(16, frame_width - 2)

    if len(text) > inner_width:
        text = text[:inner_width]

    top = "┌" + ("─" * inner_width) + "┐"
    mid = "│" + text.center(inner_width) + "│"
    bot = "└" + ("─" * inner_width) + "┘"
    return "\n".join([top, mid, bot])
