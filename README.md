*This project has been created as part of the 42 curriculum by eamaral-, lmuler-f.*

# A-Maze-ing

## Description

This project generates mazes from a config file and saves the result in a text file using hexadecimal wall values.

Goal of the project:

- Read maze settings from a config file.
- Generate a valid maze (perfect or imperfect).
- Save maze data and solution path to an output file.
- Show the maze visually in the terminal.

Project flow:

- The entry point reads one config file.
- The parser validates required values.
- The generator builds the maze with DFS or PRIM.
- The solver uses BFS to find the shortest path.
- The terminal UI allows maze regeneration, path toggle, and color changes.

## Instructions

### Requirements

- Python 3.10+
- Make

### Installation

```bash
make install
```

What this does:

- Creates `.venv` automatically (if missing)
- Installs/updates pip inside `.venv`
- Installs dependencies from `requirements.txt`
- Installs the project in editable mode (`-e .`)

### Run

```bash
make run
```

`make run` always uses the `config.txt` file from the project root.

To list all commands:

```bash
make help
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

Terminal UI size limits (for readability):

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

How to choose:

- By config: set `ALGORITHM=DFS` or `ALGORITHM=PRIM`.
- In terminal UI: option `[5]` switches between DFS and PRIM and regenerates.

## Why These Algorithms

- DFS is simple, fast, and produces long corridor-like structures.
- PRIM provides a different maze style with more local branching.
- Both are connected by construction and fit the project constraints.
- Keeping both gives visual variety and supports side-by-side comparison.

## Reusable Code

The reusable part is the maze core package (`maze_gen`):

- Data model (`MazeData`, `Cell`, `Wall`)
- Maze generator (`MazeGenerator`)
- Maze solver (`solve_shortest_path`, `coords_to_directions`)

How to reuse it:

- Import from `maze_gen` in another Python project.
- Build and install package with `make build`.
- Use `MazeGenerator` and solver functions without the terminal UI.

Build artifacts:

- Package distribution name is `mazegen`.
- Running `make build` generates standard files in `dist/`:
	- `mazegen-<version>.tar.gz`
	- `mazegen-<version>-py3-none-any.whl`

Usage example:

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

- eamaral-:
	- Organized the repository and folder structure.
	- Built the animation, terminal UI and render.
	- Helped integrate the algorithm layer with the UI.
- lmuler-f:
	- Implemented the maze generator and algorithms.
	- Structured and maintained the project Makefile.
	- Kept imports coherent across modules during integration.
	- Helped keep the package exportable and ready for build (source/wheel flow).
- Shared ownership:
	- Both collaborated in planning, review, and support across all parts of the implementation.

### Planning (Initial vs Final)

- Initial plan:
	- Split work between UI flow and maze core, then integrate everything in one CLI program.
- Changes during project:
	- Expanded the bonus scope by keeping both DFS and PRIM available at runtime.
	- Refined architecture by separating responsibilities into `maze_config`, `maze_gen`, `maze_display`, and `maze_ui`.
	- Improved terminal usability with animation and clearer status messages.
- Final delivery plan:
	- Make sure everything works smoothly end to end, from config parsing to maze generation, solving, and terminal display.
	- Keep the project setup straightforward, with simple commands to install, run, lint, and build.
	- Deliver clear documentation so anyone reviewing the project can quickly understand what we built and how we split responsibilities.

### What Worked Well

- Clear modular separation made features easier to evolve.
- Shared constants made teamwork faster: both contributors could test features and adjust values without re-reading the whole codebase.
- Using dataclasses helped a lot: less boilerplate, cleaner models, and simpler integration between parser, generator, solver, and UI.

### What Can Be Improved

- Add an optional solver visualization mode that shows explored paths before highlighting the final shortest path.
- Add a side-by-side comparison mode (DFS vs PRIM) using the same dimensions and seed.
- Display a message showing the seed number for each new maze.

### Tools Used

- Python 3.10+
- Make
- flake8
- mypy
- pytest / pytest-cov

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

- AI was used for docstring cleanup and consistency checks.
- AI was also used to review type hints and README structure.