"""Start the maze program from command line."""

import sys
from maze_config.parser import parse_config_file
from maze_ui.menu import run_menu


def main() -> None:
    """Read config path, load settings, and open the UI menu."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    try:
        maze_params = parse_config_file(sys.argv[1])
        run_menu(maze_params)
    except (ValueError, KeyError, FileNotFoundError) as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
