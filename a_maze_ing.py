import sys
import os
from typing import Dict
from mazegen.models import MazeData
from mazegen.generator import MazeGenerator


def parse_config(file_path: str) -> MazeData:
    """
    Reads config file and builds maze settings.

    This function opens a text file, reads key=value lines,
    validates required fields and converts them into usable types.

    If something is wrong, it raises errors instead of guessing.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: '{file_path}' not found.")

    config: Dict[str, str] = {}

    try:
        with open(file_path, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()

                # skip empty lines and comments
                if not line or line.startswith('#'):
                    continue

                if '=' not in line:
                    raise KeyError(
                        f"Error on line {line_num}: bad format. Use KEY=VALUE"
                    )

                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()

        # required keys (no excuses)
        required = [
            "WIDTH",
            "HEIGHT",
            "ENTRY",
            "EXIT",
            "OUTPUT_FILE",
            "PERFECT"
        ]
        for key in required:
            if key not in config:
                raise KeyError(f"Missing required key: {key}")

        # convert types
        width = int(config["WIDTH"])
        height = int(config["HEIGHT"])

        entry_raw = config["ENTRY"].split(',')
        exit_raw = config["EXIT"].split(',')

        entry = (int(entry_raw[0]), int(entry_raw[1]))
        exit_pos = (int(exit_raw[0]), int(exit_raw[1]))

        perfect = config["PERFECT"].lower() == "true"
        output_file = config["OUTPUT_FILE"]

        seed = int(config.get("SEED", 42))

        # validation rules (fuck off with chaos here)
        if width <= 0 or height <= 0:
            raise ValueError("Width and Height must be > 0")

        if not (0 <= entry[0] < width and 0 <= entry[1] < height):
            raise ValueError("Entry is outside maze bounds")

        if not (0 <= exit_pos[0] < width and 0 <= exit_pos[1] < height):
            raise ValueError("Exit is outside maze bounds")

        if entry == exit_pos:
            raise ValueError("Entry and Exit cannot be the same")

        return MazeData(
            width=width,
            height=height,
            entry=entry,
            exit=exit_pos,
            output_file=output_file,
            perfect=perfect,
            seed=seed
        )

    except ValueError as e:
        raise ValueError(f"Config value error: {e}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {e}")


def main() -> None:
    """
    Entry point of the program.

    Reads config file, generates maze, and prints result.
    """
    if len(sys.argv) != 2:
        raise ValueError("Usage: python3 a_maze_ing.py config.txt")

    maze_params = parse_config(sys.argv[1])

    generator = MazeGenerator(
        maze_params.width,
        maze_params.height,
    )

    maze = generator.get_maze()
    maze_params.grid = maze

    print("Configuration loaded successfully")
    print(f"Size: {maze_params.width}x{maze_params.height}")
    print(f"Entry: {maze_params.entry} | Exit: {maze_params.exit}")
    print("Maze generated!")

    for row in maze:
        print([cell.walls for cell in row])


if __name__ == "__main__":
    main()
