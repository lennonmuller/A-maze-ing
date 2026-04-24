*This project has been created as part of the 42 curriculum by eamaral-, lmuler-f.*

# MazeGen - Reusable Maze Generator Module

Standalone Python module for generating and solving mazes.

## Package Name and Build Output

- Distribution/package name: `mazegen`
- Import name: `maze_gen`
- Standard build outputs in `dist/`:
    - `mazegen-<version>.tar.gz`
    - `mazegen-<version>-py3-none-any.whl`

## Installation

Install from a built artifact:

```bash
pip install dist/mazegen-1.0.0-py3-none-any.whl
```

Or install from source (editable):

```bash
pip install -e .
```

## Quick Start

```python
from maze_gen import MazeData, MazeGenerator
from maze_gen import solve_shortest_path, coords_to_directions

# 1) Configure generation parameters
params = MazeData(
    width=20,
    height=12,
    entry=(0, 0),
    exit=(19, 11),
    output_file="maze.txt",
    perfect=True,
    seed=123,
    algorithm="PRIM",  # "DFS" or "PRIM"
)

# 2) Instantiate and generate
generator = MazeGenerator(params)
maze = generator.get_maze()

# 3) Access generated maze structure
grid = maze.grid

# 4) Access one solution
path = solve_shortest_path(grid, maze.entry, maze.exit)
directions = coords_to_directions(path)

# 5) Optional: save maze + solution in output-file format
MazeGenerator.save_maze_to_file(maze, directions)
```

## Supported Parameters (MazeData)

- `width` (int): Maze width in cells.
- `height` (int): Maze height in cells.
- `entry` (tuple[int, int]): Entry coordinate `(x, y)`.
- `exit` (tuple[int, int]): Exit coordinate `(x, y)`.
- `output_file` (str): Output file path used by `save_maze_to_file`.
- `perfect` (bool): `False` opens extra walls (loops), `True` keeps perfect maze behavior.
- `seed` (int, optional): Random seed for reproducibility.
- `algorithm` (str, optional): `"DFS"` or `"PRIM"`.

## Accessing Structure and Solution

Generated structure is returned as `MazeData`:

- `maze.grid`: 2D list of `Cell`
- `maze.entry` / `maze.exit`
- `maze.width` / `maze.height`

Each `Cell` exposes:

- `x`, `y`
- `walls` bitmask (`NORTH=1`, `EAST=2`, `SOUTH=4`, `WEST=8`)
- `hex_value`
- `is_closed(wall)`

Solution helpers:

- `solve_shortest_path(grid, start, goal)` returns list of coordinates.
- `coords_to_directions(path)` converts to `N/E/S/W` text.

## Algorithm Notes

- `DFS`: backtracking behavior with long corridors.
- `PRIM`: randomized Prim behavior with more local branching.

## Callback Support

`get_maze(on_step=...)` accepts a callback called during generation.

```python
def on_step(maze_data):
    pass

maze = generator.get_maze(on_step=on_step)
```

## License

MIT
