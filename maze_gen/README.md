*This project has been created as part of the 42 curriculum by eamaral-, lmuler-f*

# MazeGen - Reusable Maze Generator Module (Short Documentation)
# MazeGen - Reusable Maze Generator Module

A standalone Python module for generating and solving mazes.

## Installation

Install the `mazegen` package from the wheel distribution:

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

## Quick Start

### Basic Usage

After installation, import directly from `mazegen`:

```python
from mazegen import MazeGenerator, MazeData, solve_shortest_path, coords_to_directions

# 1. Create maze configuration
maze_config = MazeData(
    width=20,
    height=15,
    entry=(0, 0),
    exit=(19, 14),
    output_file="maze.txt",
    perfect=True,
    seed=42
)

# 2. Instantiate generator
generator = MazeGenerator(maze_config)

# 3. Generate the maze
maze_data = generator.get_maze()

# 4. Access the maze structure (grid of cells)
for row in maze_data.grid:
    hex_row = "".join(cell.hex_value for cell in row)
    print(hex_row)

# 5. Solve the maze
solution_path = solve_shortest_path(
    maze_data.grid, 
    maze_data.entry, 
    maze_data.exit
)
solution_directions = coords_to_directions(solution_path)
print(f"Solution: {solution_directions}")

# 6. Save maze and solution to file
MazeGenerator.save_maze_to_file(maze_data, solution_directions)
```

## Parameters

### MazeData Configuration

- **width** (int): Maze width in cells
- **height** (int): Maze height in cells
- **entry** (tuple[int, int]): Starting position (x, y)
- **exit** (tuple[int, int]): Goal position (x, y)
- **output_file** (str): Path to output file
- **perfect** (bool): If False, adds loops to the maze for multiple solutions
- **seed** (int, optional): Random seed for reproducible generation (default: 42)

## Accessing the Generated Maze

The `MazeData` object returned by `get_maze()` contains:

- **grid**: 2D list of `Cell` objects representing the maze structure
- **entry**: Starting coordinates
- **exit**: Goal coordinates
- **width** / **height**: Dimensions of the maze

Each `Cell` has:

- **x, y**: Cell coordinates
- **walls**: Bitmask of wall states (NORTH=1, EAST=2, SOUTH=4, WEST=8)
- **hex_value**: Walls as a single hex digit (0-F)
- **is_closed(wall)**: Check if a specific wall is closed

## Accessing the Solution

Use the `solve_shortest_path()` function to find the shortest path:

```python
from mazegen import solve_shortest_path, coords_to_directions

# Get solution as coordinate list
path = solve_shortest_path(maze_data.grid, maze_data.entry, maze_data.exit)

# Convert to direction string (N/E/S/W)
directions = coords_to_directions(path)
```

## Advanced: Custom Generation with Callbacks

Monitor maze generation progress with callbacks:

```python
def on_generation_step(maze_data):
    # Called after each generation step
    print(f"Generated {sum(1 for row in maze_data.grid for cell in row if cell.visited)} cells")

maze_data = generator.get_maze(on_step=on_generation_step)
```

## API Reference

### MazeGenerator

Main class for generating mazes.

```python
generator = MazeGenerator(data: MazeData)
```

**Methods:**
- `get_maze(on_step: Callable | None = None) -> MazeData` - Generate and return maze data
- `save_maze_to_file(data: MazeData, solution_str: str) -> None` - Save maze to file with solution

### Solver Functions

- `solve_shortest_path(grid: list[list[Cell]], start: tuple[int, int], goal: tuple[int, int]) -> list[tuple[int, int]]` - Find shortest path using BFS
- `coords_to_directions(path: list[tuple[int, int]]) -> str` - Convert path to N/E/S/W string

## License

MIT
