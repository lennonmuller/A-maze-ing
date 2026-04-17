"""Application entry point for the maze project.

This module only starts the program. It reads one config file path from
the command line, loads maze settings, and starts the interactive menu.
"""

import sys
from maze_config import parse_config_file
from ui import run_menu


def main() -> None:
    """Run the command line entry flow for the maze app.

    The function expects exactly one argument: the config file path.
    It parses this file and passes the maze settings to the UI menu.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    maze_params = parse_config_file(sys.argv[1])
    run_menu(maze_params)


if __name__ == "__main__":
    main()
