"""Action functions used by the terminal menu."""

from collections.abc import Callable
import random

from maze_display.ascii_render import render_maze
from maze_gen.generator import MazeGenerator
from maze_gen.models import MazeData
from maze_gen.solver import solve_shortest_path, coords_to_directions
from maze_ui.constants import (
    APP_TITLE,
    FIXED_UI_WIDTH_CELLS,
    MENU_FOOTER_TEMPLATE,
    STATUS_NEW_MAZE,
    STATUS_NO_PATH,
    STATUS_PATH_OFF,
    STATUS_PATH_ON,
    STATUS_READY,
    UI_CELL_RENDER_WIDTH,
    UI_FRAME_BORDER_DISCOUNT,
    UI_FRAME_EXTRA_WIDTH,
    UI_MIN_INNER_WIDTH,
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

    next_algo = "PRIM" if state.maze_params.algorithm == "DFS" else "DFS"
    dynamic_footer = MENU_FOOTER_TEMPLATE.format(next_algo=next_algo)

    maze_text = render_maze(
        state.maze_data.grid,
        entry=state.maze_data.entry,
        exit=state.maze_data.exit,
        path=path_coords,
        wall_color=state.wall_color,
        pattern_color=state.pattern_color,
    )
    maze_lines = maze_text.splitlines()
    maze_width = (
        state.maze_data.width * UI_CELL_RENDER_WIDTH
        + UI_FRAME_EXTRA_WIDTH
    )

    print(_center_block(_render_title_box(APP_TITLE), maze_width))
    if state.status_message:
        print(state.status_message)
    if state.maze_data.pattern_warning:
        print(state.maze_data.pattern_warning)
    print()

    for line in maze_lines:
        print(line)

    print(_center_block(_render_menu_box(dynamic_footer), maze_width))


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


def _render_title_box(text: str) -> str:
    """Render the fixed-width program title box.

    Args:
        text: Title text.

    Returns:
        str: Box text with three lines.
    """
    inner_width = _fixed_inner_width()
    top = "╔" + ("═" * inner_width) + "╗"
    mid = "║" + text.center(inner_width) + "║"
    bot = "╚" + ("═" * inner_width) + "╝"
    return "\n".join([top, mid, bot])


def _render_menu_box(text: str) -> str:
    """Render a fixed-width framed text box for menu options.

    Args:
        text: Footer menu text.

    Returns:
        str: Box text with three lines.
    """
    inner_width = _fixed_inner_width()

    if len(text) > inner_width:
        text = text[:inner_width]

    top = "┌" + ("─" * inner_width) + "┐"
    mid = "│" + text.center(inner_width) + "│"
    bot = "└" + ("─" * inner_width) + "┘"
    return "\n".join([top, mid, bot])


def _fixed_inner_width() -> int:
    """Return fixed inner width used by title and menu boxes."""
    frame_width = (
        FIXED_UI_WIDTH_CELLS * UI_CELL_RENDER_WIDTH
        + UI_FRAME_EXTRA_WIDTH
    )
    return max(UI_MIN_INNER_WIDTH, frame_width - UI_FRAME_BORDER_DISCOUNT)


def _center_block(block_text: str, container_width: int) -> str:
    """Center a multi-line block inside one container width.

    Args:
        block_text: Block text with one or more lines.
        container_width: Width used as centering reference.

    Returns:
        str: Centered block text.
    """
    lines = block_text.splitlines()
    block_width = max((len(line) for line in lines), default=0)

    if container_width <= block_width:
        return block_text

    left_padding = " " * ((container_width - block_width) // 2)
    return "\n".join(left_padding + line for line in lines)


def switch_algorithm(state: UIState) -> None:
    """Switch between DFS and PRIM."""
    if state.maze_params.algorithm == "DFS":
        state.maze_params.algorithm = "PRIM"
    else:
        state.maze_params.algorithm = "DFS"

    print(f"\nAlgorithm: {state.maze_params.algorithm}")
    state.status_message = f"Algorithm: {state.maze_params.algorithm}"
