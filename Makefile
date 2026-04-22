run:
	python3 a_maze_ing.py config.txt

install:
	python3 -m pip install -r requirements.txt
	python3 -m pip install -e .

debug:
	python3 -m pdb a_maze_ing.py config.txt

clean:
	@echo "Limpando caches e arquivos temporários..."
	rm -rf __pycache__ 
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf dist
	rm -rf *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +

lint:
	python3 -m flake8 a_maze_ing.py maze_config maze_display maze_gen maze_ui
	python3 -m mypy a_maze_ing.py maze_config maze_display maze_gen maze_ui --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	python3 -m flake8 a_maze_ing.py maze_config maze_display maze_gen maze_ui
	python3 -m mypy a_maze_ing.py maze_config maze_display maze_gen maze_ui --strict

build:
	@echo "Gerando pacote redistribuível..."
	python3 -m pip install build
	python3 -m build

.PHONY: run install debug clean lint lint-strict build