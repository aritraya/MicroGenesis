.PHONY: clean clean-test clean-pyc clean-build docs help test lint
.DEFAULT_GOAL := help

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly"
	@echo "coverage - check code coverage quickly with pytest"
	@echo "docs - generate Sphinx HTML documentation"
	@echo "install - install the package to the active Python's site-packages"

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .pytest_cache/
	rm -fr .coverage
	rm -fr htmlcov/

lint:
	flake8 src tests
	black --check src tests
	isort --check src tests

test:
	pytest

coverage:
	pytest --cov=src tests/
	coverage report -m

docs:
	rm -f docs/microgenesis.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ src
	$(MAKE) -C docs clean
	$(MAKE) -C docs html

install: clean
	pip install -e .
