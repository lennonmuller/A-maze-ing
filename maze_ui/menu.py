"""Simple terminal menu loop for maze actions."""

from maze_gen.models import MazeData
from maze_ui.animations import (
    animate_path_reveal,
    run_with_generation_animation,
)
from maze_ui.constants import (
    COLOR_OPTIONS,
    LABEL_PATTERN_COLOR,
    LABEL_WALL_COLOR,
    PROMPT_COLOR,
    PROMPT_OPTION,
    STATUS_INVALID_COLOR,
    STATUS_INVALID_OPTION,
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
    """Run menu loop until user quits."""
    state = run_with_generation_animation(
        lambda callback: initialize_state_with_animation(
            maze_params,
            on_step=callback,
        ),
        wall_color="default",
        pattern_color="default",
    )

    while True:
        print()
        render_current_maze(state)

        choice = _menu_choice()

        if choice == "1":
            run_with_generation_animation(
                lambda callback: regenerate_maze(
                    state,
                    on_step=callback,
                ),
                wall_color=state.wall_color,
                pattern_color=state.pattern_color,
            )
        elif choice == "2":
            if state.show_path:
                toggle_path(state)
            else:
                animate_path_reveal(state)
        elif choice == "3":
            wall_color = _color_choice(LABEL_WALL_COLOR)
            update_wall_color(state, wall_color)
        elif choice == "4":
            pattern_color = _color_choice(LABEL_PATTERN_COLOR)
            update_pattern_color(state, pattern_color)
        elif choice == "5":
            break
        else:
            state.status_message = STATUS_INVALID_OPTION


def _menu_choice() -> str:
    """Read one menu option from user."""
    return input(PROMPT_OPTION).strip()


def _color_choice(title: str) -> str:
    """Read one color name or index."""
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
    return "default"
