.ONESHELL:


setup:
	rm -rf venv
	python3 -m venv venv
	. venv/bin/activate
	venv/bin/python -m pip -q install --upgrade pip
	venv/bin/python -m pip -q install -r requirements.txt

lint:
	flake8 --exclude=*.pyc,__pycache__ --max-line-length 130 lucerne_festival_crawler/
	flake8 --exclude=*.pyc,__pycache__ --max-line-length 130 tests

test:
	. venv/bin/activate
	pytest

run:
	. venv/bin/activate
	venv/bin/python main.py

clean:
	rm -rf .pytest_cache
	rm -rf venv
	rm -rf __pycache__