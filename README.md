*This project has been created as part of the 42 curriculum by eamaral-, lmuler-f.*

# A-Maze-ing

## Description

This project generates mazes from a config file and saves the result in a text file using hexadecimal wall values.

Goal of the project:

- Read maze settings from a config file.
- Generate a valid maze (perfect or imperfect).
- Save maze data and solution path to an output file.
- Show a visual maze in terminal.

Short overview:

- Main entry point reads one config file.
- Config parser validates all required values.
- Generator builds maze grid using DFS or PRIM.
- Solver uses BFS to get shortest path.
- Terminal UI lets user regenerate maze, show path, and change colors.

## Instructions

### Requirements

- Python 3.10+
- Virtual environment recommended

### Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
make install
```

### Run

```bash
python3 a_maze_ing.py config.txt
```

Or:

```bash
make run
```

### Debug

```bash
make debug
```

### Lint and Type Check

```bash
make lint
make lint-strict
```

### Build Package

```bash
make build
```

## Config File Format

The config file uses one `KEY=VALUE` per line.

- Empty lines are ignored.
- Lines starting with `#` are comments.

Required keys:

| Key | Value | Example |
| --- | --- | --- |
| `WIDTH` | Integer maze width in cells | `WIDTH=15` |
| `HEIGHT` | Integer maze height in cells | `HEIGHT=11` |
| `ENTRY` | Entry coordinate in `x,y` format | `ENTRY=0,0` |
| `EXIT` | Exit coordinate in `x,y` format | `EXIT=14,10` |
| `OUTPUT_FILE` | Output filename | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | Boolean (`True` or `False`) | `PERFECT=True` |

Optional keys used in this project:

- `SEED` (int, default is `42`)
- `ALGORITHM` (`DFS` or `PRIM`, default is `DFS`)

Terminal UI size limits (to keep rendering readable):

- `WIDTH <= 35`
- `HEIGHT <= 20`
- `WIDTH * HEIGHT <= 700`

Example:

```txt
WIDTH=15
HEIGHT=11
ENTRY=0,0
EXIT=14,10
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
ALGORITHM=DFS
```

## Maze Generation Algorithms

Implemented algorithms:

- Depth-First Search (DFS) with backtracking (stack-based)
- Randomized Prim (PRIM)

How DFS works:

- Start from entry cell.
- Visit one random unvisited neighbor.
- Open wall between current cell and next cell.
- Continue until dead end.
- Backtrack using stack until all cells are visited.

How PRIM works:

- Start from entry cell and mark it as visited.
- Add its unvisited neighbors to a frontier list.
- Pick a random frontier cell.
- Connect it to one random visited neighbor.
- Mark it visited and add its unvisited neighbors to frontier.
- Repeat until frontier is empty.

For imperfect mazes (`PERFECT=False`):

- The generator opens extra random walls to create loops.

How to choose during execution:

- By config: set `ALGORITHM=DFS` or `ALGORITHM=PRIM`.
- In terminal UI: option `[5]` switches between DFS and PRIM and regenerates.

## Why These Algorithms

- DFS is simple, fast, and produces long corridor-like structures.
- PRIM provides a different maze style with more local branching.
- Both are connected by construction and fit the project constraints.
- Keeping both gives visual variety and supports side-by-side comparison.

## Reusable Code

Reusable part is the maze core package (`maze_gen`):

- Data model (`MazeData`, `Cell`, `Wall`)
- Maze generator (`MazeGenerator`)
- Maze solver (`solve_shortest_path`, `coords_to_directions`)

How to reuse:

- Import from `maze_gen` in another Python project.
- Build and install package with `make build`.
- Use `MazeGenerator` and solver functions without the terminal UI.

Build artifacts:

- Package distribution name is `mazegen`.
- Running `make build` generates standard files in `dist/`:
	- `mazegen-<version>.tar.gz`
	- `mazegen-<version>-py3-none-any.whl`

Short usage example (instantiate, customize, access structure, access solution):

```python
from maze_gen import MazeData, MazeGenerator
from maze_gen import solve_shortest_path, coords_to_directions

params = MazeData(
	width=20,
	height=12,
	entry=(0, 0),
	exit=(19, 11),
	output_file="maze.txt",
	perfect=True,
	seed=123,
	algorithm="PRIM",
)

generator = MazeGenerator(params)
maze = generator.get_maze()

# Access generated structure
grid = maze.grid

# Access one shortest solution
path = solve_shortest_path(grid, maze.entry, maze.exit)
directions = coords_to_directions(path)
```

## Advanced Features Implemented

- Perfect and imperfect maze modes.
- ANSI color options for walls and 42 pattern.
- Animated generation and path reveal in terminal UI.
- Optional 42 pattern insertion with clear warning if maze is too small.

## Team and Project Management

### Team Roles

- eamaral-: [to fill]
- lmuler-f: [to fill]

### Planning (Initial vs Final)

- Initial plan: [to fill]
- Changes during project: [to fill]
- Final delivery plan: [to fill]

### What Worked Well

- [to fill]

### What Can Be Improved

- [to fill]

### Tools Used

- [to fill]

## Resources

Classic references:

- Python Docs: https://docs.python.org/3/
- dataclasses: https://docs.python.org/3/library/dataclasses.html
- enum: https://docs.python.org/3/library/enum.html
- typing: https://docs.python.org/3/library/typing.html
- `argparse` basics: https://docs.python.org/3/library/argparse.html
- DFS and BFS overview: https://en.wikipedia.org/wiki/Depth-first_search
- BFS shortest path in unweighted graph: https://en.wikipedia.org/wiki/Breadth-first_search

AI usage in this project:

- AI was used as docstring cleanup, and consistency checks.
- AI was also used to help review typing, lint issues, and README structure.
- Final design choices, code decisions, and validation were reviewed by the team.
