run:
	python3 a_maze_ing.py config.txt

install:
	pip3 install -r requirements.txt

debug:
	python3 -m pdb

clean:
	rm -rf __pycache__ .mypy_cache dist *.egg-info

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict
