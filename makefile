BASE_DIR := $(shell pwd)
ENV_DIR := $(BASE_DIR)/env
PYTHON := $(ENV_DIR)/Scripts/python.exe
hello: 
	@echo "Hello, World!"
	@echo "BASE_DIR is $(BASE_DIR)"
	@echo "$(PYTHON)"
create-venv:
	python3 -m venv env

activate-venv: env
	@echo "Activating virtual environment..."
	@sudo -s source $(ENV_DIR)/bin/activate
	@echo "Virtual environment activated"


install-requirements:
	@echo "Installing dependencies..."
	@pip3 install -r requirements.txt --upgrade -q
	@echo "Dependencies installed"
	@echo "Updating pip..."
	@$(PYTHON) -m pip install --upgrade pip -q
	@echo "Pip updated"

run:
	@echo "Running application..."
	@$(PYTHON) app.py
	@echo "Application finished"

clean:
	@echo "Cleaning up..."
	@rm -rf $(ENV_DIR)
	@echo "Cleaned up"
	

test:
	@echo "Running tests..."
	@py -m unittest discover -s tests/ 
	@echo "Tests finished"

test-catalog:
	@echo "Running tests..."
	@$(PYTHON) -m unittest discover -v -t ./tests/ -s tests_catalog
	@echo "Tests finished"