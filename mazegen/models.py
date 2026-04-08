''' Classes de dados (Cell, Point, etc.) '''

from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class Cell:
    """
    Representa uma célula individual do labirinto.

    Atributos:
        x (int): Coordenada horizontal da célula na grade (coluna).
        y (int): Coordenada vertical da célula na grade (linha).
        walls (int): Máscara de bits representando as paredes da célula.

    Convenção típica para `walls` (exemplo):
        - bit 0 (1): parede ao norte
        - bit 1 (2): parede ao sul
        - bit 2 (4): parede a leste
        - bit 3 (8): parede a oeste

    Valor padrão:
        15 (binário 1111) → todas as paredes presentes.
    """
    x: int
    y: int
    walls: int = 15  # comeca todas as pareres (1111 em binario)


@dataclass
class MazeData:
    """
    Estrutura principal de dados para representar um labirinto completo.

    Atributos:
        width (int): Largura do labirinto em número de células.
        height (int): Altura do labirinto em número de células.
        entry (Tuple[int, int]): Coordenadas (x, y) da célula de entrada.
        exit (Tuple[int, int]): Coordenadas (x, y) da célula de saída.
        output_file (str): Caminho/nome do arquivo de saída para o labirinto.
        perfect (bool): Indica se o labirinto deve ser perfeito (sem ciclos).
        seed (int): Seed usada para geração pseudoaleatória do labirinto.
        grid (List[List[Cell]]): Grade bidimensional de células que compõem
        o labirinto.
        solution_path (List[Tuple[int, int]]): Lista de coordenadas (x, y) que
        formam o caminho da solução.

    Uso típico:
        - O gerador de labirinto inicializa `grid` com células e ajusta `walls`
        - O resolvedor de caminho preenche `solution_path` com a rota da
        entrada até a saída.
        - O módulo de saída usa `output_file` para salvar o labirinto e/ou a
        solução.
    """
    width: int
    height: int
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    output_file: str
    perfect: bool
    seed: int = 42
    grid: List[List[Cell]] = field(default_factory=list)
    solution_path: List[Tuple[int, int]]  # caminho curto
