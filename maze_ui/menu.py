"""Terminal menu loop for maze actions."""

from maze_gen.models import MazeData
from maze_ui.animations import (
    animate_path_reveal,
    run_with_generation_animation,
)
from maze_ui.constants import (
    CLEAR_HOME,
    COLOR_OPTIONS,
    DEFAULT_PATTERN_COLOR,
    DEFAULT_WALL_COLOR,
    LABEL_PATTERN_COLOR,
    LABEL_WALL_COLOR,
    MENU_OPTION_ALGORITHM,
    MENU_OPTION_NEW,
    MENU_OPTION_PATH,
    MENU_OPTION_PATTERN,
    MENU_OPTION_QUIT,
    MENU_OPTION_WALLS,
    PROMPT_COLOR,
    PROMPT_OPTION,
    STATUS_INVALID_COLOR,
    STATUS_INVALID_OPTION,
    STATUS_QUIT,
)
from maze_ui.actions import (
    initialize_state_with_animation,
    regenerate_maze,
    render_current_maze,
    toggle_path,
    update_pattern_color,
    update_wall_color,
)


def run_menu(maze_params: MazeData) -> None:
    """Run menu loop until user chooses quit.

    Args:
        maze_params: Maze configuration for first generation.
    """
    state = run_with_generation_animation(
        lambda callback: initialize_state_with_animation(
            maze_params,
            on_step=callback,
        ),
        wall_color=DEFAULT_WALL_COLOR,
        pattern_color=DEFAULT_PATTERN_COLOR,
    )

    while True:
        print(CLEAR_HOME, end="", flush=True)
        render_current_maze(state)

        choice = _menu_choice()

        if choice == MENU_OPTION_NEW:
            run_with_generation_animation(
                lambda callback: regenerate_maze(
                    state,
                    on_step=callback,
                ),
                wall_color=state.wall_color,
                pattern_color=state.pattern_color,
            )
        elif choice == MENU_OPTION_PATH:
            if state.show_path:
                toggle_path(state)
            else:
                animate_path_reveal(state)
        elif choice == MENU_OPTION_WALLS:
            wall_color = _color_choice(LABEL_WALL_COLOR, state.wall_color)
            update_wall_color(state, wall_color)
        elif choice == MENU_OPTION_PATTERN:
            pattern_color = _color_choice(
                LABEL_PATTERN_COLOR,
                state.pattern_color,
            )
            update_pattern_color(state, pattern_color)
        elif choice == MENU_OPTION_ALGORITHM:
            from maze_ui.actions import switch_algorithm
            switch_algorithm(state)
            run_with_generation_animation(
                lambda callback: regenerate_maze(state, on_step=callback),
                wall_color=state.wall_color,
                pattern_color=state.pattern_color,
            )
        elif choice == MENU_OPTION_QUIT:
            print(f"\n{STATUS_QUIT}")
            break
        else:
            state.status_message = STATUS_INVALID_OPTION


def _menu_choice() -> str:
    """Read one menu option from user input.

    Returns:
        str: Normalized option text.
    """
    return input(PROMPT_OPTION).strip()


def _color_choice(title: str, current_color: str) -> str:
    """Read one color by name or numeric index.

    Args:
        title: Prompt title shown before options.
        current_color: Current color kept on invalid selection.

    Returns:
        str: Selected color or current color.
    """
    options_line = "  ".join(
        f"{idx}) {color}" for idx, color in enumerate(COLOR_OPTIONS, 1)
    )
    print(f"\n{title}: {options_line}")

    selected = input(PROMPT_COLOR).strip()

    if selected.isdigit():
        index = int(selected)
        if 1 <= index <= len(COLOR_OPTIONS):
            return COLOR_OPTIONS[index - 1]

    if selected in COLOR_OPTIONS:
        return selected

    print(STATUS_INVALID_COLOR)
    return current_color
