import sys
import os
from typing import Dict, Any
from mazegen.models import MazeData


def parse_config(file_path: str) -> MazeData:
    """Read and valid the configuration archive"""
    if not os.path.exists(file_path):
        print(f"Error: '{file_path}' not found.")
        sys.exit(1)

    config: Dict[str, str] = {}  # cria um dicionario vazio

    try:
        with open(file_path, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()  # <- Remobe espacos inicio/fim
                #ignora comentarios e linhas vazias
                if not line or line.startswith('#'):
                    continue

                if '=' not in line:
                    print(f"Error on line {line_num}: Invalid format. Use KEY=VALUE")
                    sys.exit(1)

                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
                #Divide key e value e guarda ambos no dicionario sem espacos extras

        # Validacao das chaves obrigatorias
        required = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
        for key in required:
            if key not in config:
                print(f"Error: The mandatory key '{key}' is missing in config.")
                sys.exit(1)

        # PAREI EM CONVERSAO DE TIPOS NO DICIONARIO

    except ValueError as e:
        print(f"Error on value of config {e}")
        sys.exit(1)


if __name__ == "__main__":
    parse_config()
