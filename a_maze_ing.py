import sys
import os
from typing import Dict
from mazegen.models import MazeData


def parse_config(file_path: str) -> MazeData:
    """Read and valid the configuration archive"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: '{file_path}' not found.")

    config: Dict[str, str] = {}  # cria um dicionario vazio

    try:
        with open(file_path, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()  # <- Remobe espacos inicio/fim
                # ignora comentarios e linhas vazias
                if not line or line.startswith('#'):
                    continue

                if '=' not in line:
                    raise KeyError(f"Error on line {line_num}: Invalid format."
                          " Use KEY=VALUE")

                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
                # Divide key e value e guarda ambos no dicion s/ espacos extra

        # Validacao das chaves obrigatorias
        required = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE",
                    "PERFECT"]
        for key in required:
            if key not in config:
                raise KeyError(f"Error: The mandatory key '{key}' is missing "
                               "in config.")

        # converte os tipos para int
        width = int(config["WIDTH"])
        height = int(config["HEIGHT"])

        # converte "0,0" para tupla (0,0)
        entry_raw = config["ENTRY"].split(',')
        exit_raw = config["EXIT"].split(',')
        entry = (int(entry_raw[0]), int(entry_raw[1]))
        exit = (int(exit_raw[0]), int(exit_raw[1]))

        perfect = config["PERFECT"].lower() == "true"
        output_file = config["OUTPUT_FILE"]

        # seed (opicional)
        seed = int(config.get("SEED", 42))

        # VALIDACAO DE LIMITES regra IV.4
        if width <= 0 or height <= 0:
            raise ValueError("Width and Height cannot be negative or zero")

        if not (0 <= entry[0] < width and 0 <= entry[1] < height):
            raise ValueError("Error: Entry outside of limits")

        if not (0 <= exit[0] < width and 0 <= exit[1] < height):
            raise ValueError("Error: Exit outside of maze limits")

        if entry == exit:
            raise ValueError("Error: Entry and exit cannot be the same.")

        return MazeData(
            width=width, height=height, entry=entry,
            exit=exit, output_file=output_file, perfect=perfect,
            seed=seed
        )

    except ValueError as e:
        raise ValueError(f"Error on value of config {e}")
    except Exception as e:
        raise RuntimeError(f"Unexpected Error: {e}")


def main() -> None:
    if len(sys.argv) != 2:
        raise ValueError("Correct usage: python3 a_maze_ing.py config.txt")

    maze_params = parse_config(sys.argv[1])

    print("Configuration loaded successfully!")
    print(f"Size: {maze_params.width}x{maze_params.height}")
    print(f"Entry: {maze_params.entry} | Exit: {maze_params.exit}")


if __name__ == "__main__":
    main()
