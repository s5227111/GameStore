BASE_DIR := $(shell pwd)
ENV_DIR := $(BASE_DIR)/env

hello: 
	@echo "Hello, World!"
	@echo "BASE_DIR is $(BASE_DIR)"

create-venv:
	python3 -m venv env

activate-venv: env
	@echo "Activating virtual environment..."
	@sudo -s source $(ENV_DIR)/bin/activate
	@echo "Virtual environment activated"


install-depenencies: activate-venv
	@echo "Installing dependencies..."
	@pip3 install -r requirements.txt
	@echo "Dependencies installed"

run:
	@echo "Running application..."
	@python3 app.py
	@echo "Ap