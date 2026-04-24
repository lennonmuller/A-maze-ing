"""Start the maze program from the command line."""

import sys
from maze_config.parser import parse_config_file
from maze_ui.menu import run_menu


def main() -> None:
    """Run the main program flow.

    Reads the config path from command-line arguments, parses the
    configuration file, and starts the interactive menu.

    Raises:
        SystemExit: If arguments are invalid or an expected runtime error
            happens during startup.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    try:
        maze_params = parse_config_file(sys.argv[1])
        run_menu(maze_params)
    except (ValueError, KeyError, FileNotFoundError, OSError) as e:
        print(f"Error: {e}")
        sys.exit(1)
    except (KeyboardInterrupt, EOFError):
        print("Error: execution interrupted by user input.")
        sys.exit(1)


if __name__ == "__main__":
    main()
