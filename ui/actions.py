"""Action handlers used by terminal menu.

This module keeps maze action logic separated from menu input flow.
"""

import random

from display.ascii_render import render_maze
from mazegen.generator import MazeGenerator
from mazegen.models import MazeData
from mazegen.solver import solve_shortest_path, coords_to_directions
from ui.state import UIState


def initialize_state(maze_params: MazeData) -> UIState:
    """Build initial UI state with first generated maze."""
    return UIState(
        maze_params=maze_params,
        maze_data=_generate_maze(maze_params),
    )


def regenerate_maze(state: UIState) -> None:
    """Generate a different maze and update state in place."""
    state.maze_params.seed = random.SystemRandom().randint(1, 10**9)
    state.maze_data = _generate_maze(state.maze_params)
    print("\nNovo labirinto gerado com sucesso.\n")


def toggle_path(state: UIState) -> None:
    """Enable or disable solved path visualization."""
    state.show_path = not state.show_path
    status = "ativado" if state.show_path else "desativado"
    print(f"\nMostrar caminho: {status}.\n")


def update_wall_color(state: UIState, color: str) -> None:
    """Save selected wall color in state."""
    state.wall_color = color


def update_pattern_color(state: UIState, color: str) -> None:
    """Save selected 42-pattern color in state."""
    state.pattern_color = color


def render_current_maze(state: UIState) -> None:
    """Print hex preview and ASCII drawing for current state."""
    path_set = _maze_path_set(state)

    print("\nPreview do Labirinto (Hexadecimal):")
    for row in state.maze_data.grid:
        print("".join(cell.hex_value for cell in row))

    print(
        "\nLegenda: 'F' sao celulas totalmente fechadas "
        "(provavelmente o '42')."
    )

    print("\nMaze generated!\n")

    print(
        render_maze(
            state.maze_data.grid,
            entry=state.maze_data.entry,
            exit=state.maze_data.exit,
            path=path_set,
            wall_color=state.wall_color,
            pattern_color=state.pattern_color,
        )
    )


def _generate_maze(maze_params: MazeData) -> MazeData:
    """Generate maze data from the current maze parameters."""
    generator = MazeGenerator(maze_params)
    data = generator.get_maze()

    path_coords = solve_shortest_path(data.grid, data.entry, data.exit)

    path_str = coords_to_directions(path_coords)

    MazeGenerator.save_maze_to_file(data, path_str)

    return data


def _maze_path_set(state: UIState) -> set[tuple[int, int]] | None:
    """Return solved path as set when path display is enabled."""
    if not state.show_path:
        return None

    path = solve_shortest_path(
        state.maze_data.grid,
        state.maze_data.entry,
        state.maze_data.exit,
    )

    if not path:
        print("\nNao existe caminho valido entre entrada e saida.\n")
        return set()

    return set(path)
