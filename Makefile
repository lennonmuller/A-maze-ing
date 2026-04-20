run:
	python3 a_maze_ing.py config.txt

install:
	pip3 install -r requirements.txt
	pip3 install -e .

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
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

.PHONY: run install debug clean lint lint-strict