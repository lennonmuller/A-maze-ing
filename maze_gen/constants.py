"""Constants shared by the reusable maze generation module."""

# Algorithm names
ALGO_DFS = "DFS"
ALGO_PRIM = "PRIM"
SUPPORTED_ALGORITHMS = (ALGO_DFS, ALGO_PRIM)
DEFAULT_ALGORITHM = ALGO_DFS

# Generation defaults
DEFAULT_SEED = 42
DEFAULT_IMPERFECT_OPEN_CHANCE = 20
CELL_ALL_WALLS_MASK = 15

# Centered 42 pattern geometry
PATTERN_42 = (
    (1, 0, 1, 0, 1, 1, 1),
    (1, 0, 1, 0, 0, 0, 1),
    (1, 1, 1, 0, 1, 1, 1),
    (0, 0, 1, 0, 1, 0, 0),
    (0, 0, 1, 0, 1, 1, 1),
)
PATTERN_42_WIDTH = 7
PATTERN_42_HEIGHT = 5
PATTERN_42_MIN_MARGIN = 4
