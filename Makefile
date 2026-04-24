PYTHON ?= python3
VENV := .venv
PY := $(VENV)/bin/python
PIP := $(PY) -m pip
MAIN := a_maze_ing.py
CONFIG := config.txt
ENV_READY := $(VENV)/.ready

help:
	@echo "Available targets:"
	@echo "  make install     Create .venv and install dependencies"
	@echo "  make run         Run a_maze_ing with config.txt"
	@echo "  make debug       Run a_maze_ing with pdb"
	@echo "  make lint        Run flake8 and mypy"
	@echo "  make lint-strict Run flake8 and strict mypy"
	@echo "  make build       Build source and wheel package"
	@echo "  make clean       Remove caches and build artifacts"
	@echo "  make fclean      Run clean and remove .venv"

run: check-venv
	@echo "Running the a_maze_ing program with the default config file..."
	$(PY) $(MAIN) $(CONFIG)


install: $(ENV_READY)
	@echo "Environment is ready."

$(PY):
	@echo "Creating virtual environment in $(VENV)..."
	$(PYTHON) -m venv $(VENV)

$(ENV_READY): requirements.txt pyproject.toml | $(PY)
	@echo "Installing project dependencies and editable package..."
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install -e .
	@touch $(ENV_READY)

check-venv:
	@test -x "$(PY)" || (echo "Virtual environment not found. Run 'make install' first." && exit 1)

debug: check-venv
	@echo "Starting the a_maze_ing program in Python debugger mode (pdb)..."
	$(PY) -m pdb $(MAIN) $(CONFIG)

clean:
	@echo "Cleaning Python caches, build artifacts, and generated output files..."
	rm -rf __pycache__ 
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf dist
	rm -rf *.egg-info
	rm -f maze.txt
	find . -type d -name "__pycache__" -exec rm -rf {} +

fclean: clean
	@echo "Removing virtual environment..."
	rm -rf $(VENV)

lint: check-venv
	@echo "Running flake8 and mypy checks with required subject flags..."
	$(PY) -m flake8 a_maze_ing.py maze_config maze_display maze_gen maze_ui
	$(PY) -m mypy a_maze_ing.py maze_config maze_display maze_gen maze_ui --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict: check-venv
	@echo "Running strict flake8 and mypy checks..."
	$(PY) -m flake8 a_maze_ing.py maze_config maze_display maze_gen maze_ui
	$(PY) -m mypy a_maze_ing.py maze_config maze_display maze_gen maze_ui --strict

build: check-venv
	@echo "Building source and wheel distributions for the project package..."
	$(PIP) install build
	$(PY) -m build

.PHONY: help run install check-venv debug clean fclean lint lint-strict build