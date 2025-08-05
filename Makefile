.PHONY: help install test run clean

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	pip install -r requirements.txt

test: ## Run tests
	python -m pytest tests/ -v

run: ## Run the web application
	python run_app.py

run-dev: ## Run the web application in development mode
	cd web_app && python app.py

clean: ## Clean up Python cache files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

lint: ## Run linting
	flake8 web_app/ tests/ --max-line-length=100 --ignore=E501

format: ## Format code with black
	black web_app/ tests/

setup: install ## Setup the project (install dependencies)
	@echo "Setup complete!"

all: setup test ## Run setup and tests
	@echo "All tasks completed!" 