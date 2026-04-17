"""Interactive terminal menu controller.

This module handles menu input and delegates business actions to
`ui.actions`.
"""

from mazegen.models import MazeData
from ui.actions import (
    initialize_state,
    regenerate_maze,
    render_current_maze,
    toggle_path,
    update_pattern_color,
    update_wall_color,
)


MENU_OPTIONS = {
    "1": "Re-gerar e mostrar novo labirinto",
    "2": "Mostrar/Esconder caminho mais curto",
    "3": "Alterar cor das paredes",
    "4": "Alterar cor do padrao 42 (opcional)",
    "5": "Sair",
}

COLOR_OPTIONS = [
    "default",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
]


def run_menu(maze_params: MazeData) -> None:
    """Start the menu loop and dispatch user actions.

    Args:
        maze_params: Validated maze settings from config parser.
    """
    state = initialize_state(maze_params)

    while True:
        render_current_maze(state)

        choice = _menu_choice()

        if choice == "1":
            regenerate_maze(state)
        elif choice == "2":
            toggle_path(state)
        elif choice == "3":
            wall_color = _color_choice("Escolha a cor das paredes")
            update_wall_color(state, wall_color)
            print(f"\nCor das paredes definida para: {state.wall_color}.\n")
        elif choice == "4":
            pattern_color = _color_choice("Escolha a cor do padrao 42")
            update_pattern_color(state, pattern_color)
            print(
                f"\nCor do padrao 42 definida para: {state.pattern_color}.\n"
            )
        elif choice == "5":
            print("\nSaindo...\n")
            break
        else:
            print("\nOpcao invalida. Escolha entre 1 e 5.\n")


def _menu_choice() -> str:
    """Print available menu options and return user input."""
    print("\n==== MENU ====")
    for option, label in MENU_OPTIONS.items():
        print(f"{option}) {label}")
    return input("Escolha uma opcao: ").strip()


def _color_choice(title: str) -> str:
    """Ask user for a color name or color index.

    Args:
        title: Label shown before the color list.

    Returns:
        A valid color string from COLOR_OPTIONS.
    """
    print(f"\n{title}:")
    for idx, color in enumerate(COLOR_OPTIONS, 1):
        print(f"{idx}) {color}")

    selected = input("Escolha uma cor: ").strip()

    if selected.isdigit():
        index = int(selected)
        if 1 <= index <= len(COLOR_OPTIONS):
            return COLOR_OPTIONS[index - 1]

    if selected in COLOR_OPTIONS:
        return selected

    print("Cor invalida. Mantendo 'default'.")
    return "default"
