PROJECT_NAME=dataVisualizer
PWD:=$(shell pwd)
PYTHONPATH=$(PWD)
OUTPUT_DIR=outputs
TEST_DIR=tests/
VENV=venv/bin
PIP=$(VENV)/pip3
PIP_FLAGS=--trusted-host=http://pypi.python.org/simple/
PYTEST=$(VENV)/py.test
PYLINT=$(VENV)/pylint
COVERAGE=$(VENV)/coverage
MYPY=$(VENV)/mypy
MYPYFLAGS=--ignore-missing-imports --follow-imports=skip
HOST_PYTHON_VER=python3.7
VENV_PYTHOM_VER=$(VENV)/python3


.PHONY: all venv clean

venv: venv/bin/activate

venv/bin/activate: requirements.txt
	test -d venv || virtualenv -p $(HOST_PYTHON_VER) venv
	$(PIP) $(PIP_FLAGS) install -Ur requirements.txt
	touch venv/bin/activate

clean:
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf .cache
	rm -rf .mypy_cache
	rm -rf __pycache__
	rm -rf $(OUTPUT_DIR)/*
	find -name '$(PROJECT_NAME).log' | xargs rm -rf
	find $(PROJECT_NAME) -name '*.pyc' | xargs rm -rf
	find $(PROJECT_NAME) -name '__pycache__' -type d | xargs rm -rf
	find $(TEST_DIR) -name '__pycache__' -type d | xargs rm -rf
