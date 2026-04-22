run:
	@echo "Running the maze application with the default config file..."
	python3 a_maze_ing.py config.txt

install:
	@echo "Installing project dependencies and editable package..."
	python3 -m pip install -r requirements.txt
	python3 -m pip install -e .

debug:
	@echo "Starting the maze application in Python debugger mode (pdb)..."
	python3 -m pdb a_maze_ing.py config.txt

clean:
	@echo "Cleaning Python caches, build artifacts, and generated output files..."
	rm -rf __pycache__ 
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf dist
	rm -rf *.egg-info
	rm -f maze.txt
	find . -type d -name "__pycache__" -exec rm -rf {} +

lint:
	@echo "Running flake8 and mypy checks with required subject flags..."
	python3 -m flake8 a_maze_ing.py maze_config maze_display maze_gen maze_ui
	python3 -m mypy a_maze_ing.py maze_config maze_display maze_gen maze_ui --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	@echo "Running strict flake8 and mypy checks..."
	python3 -m flake8 a_maze_ing.py maze_config maze_display maze_gen maze_ui
	python3 -m mypy a_maze_ing.py maze_config maze_display maze_gen maze_ui --strict

build:
	@echo "Building source and wheel distributions for the project package..."
	python3 -m pip install build
	python3 -m build

.PHONY: run install debug clean lint lint-strict build