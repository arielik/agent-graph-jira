.PHONY: help install install-dev test lint format clean run docker-build docker-run

# Default target
help:
	@echo "Available commands:"
	@echo "  install      - Install production dependencies"
	@echo "  install-dev  - Install development dependencies"
	@echo "  test         - Run tests"
	@echo "  lint         - Run linting (flake8, mypy)"
	@echo "  format       - Format code (black, isort)"
	@echo "  clean        - Clean build artifacts"
	@echo "  run          - Run the application"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run   - Run Docker container"

# Installation
install:
	pip install -e .

install-dev:
	pip install -e ".[dev,docs]"
	pre-commit install

# Testing
test:
	pytest tests/ -v --cov=src --cov-report=term-missing

test-watch:
	pytest-watch tests/ src/

# Code quality
lint:
	flake8 src/ tests/
	mypy src/

format:
	black src/ tests/
	isort src/ tests/

format-check:
	black --check src/ tests/
	isort --check-only src/ tests/

# Cleanup
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Application
run:
	python -m src.main

run-example:
	python -m src.main --config examples/example-stories.yaml

# Development
dev-setup: install-dev
	cp .env.example .env
	echo "Please edit .env with your actual configuration values"

# Docker
docker-build:
	docker build -t agent-graph-jira .

docker-run:
	docker run --rm -it --env-file .env agent-graph-jira

# Documentation
docs-build:
	mkdocs build

docs-serve:
	mkdocs serve

# Data management
clean-data:
	rm -rf data/chroma_db/
	rm -rf data/faiss_index/
	rm -rf data/logs/

# Pre-commit hooks
pre-commit-all:
	pre-commit run --all-files
