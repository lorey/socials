.PHONY: install lint format test docs clean

install: ## Install dev dependencies
	uv sync --extra dev

lint: ## Run linting and type checking
	uv run ruff check .
	uv run mypy socials

format: ## Format code
	uv run ruff format .
	uv run ruff check --fix .

test: ## Run tests
	uv run pytest

docs: ## Serve documentation locally
	uv run mkdocs serve

clean: ## Remove build artifacts
	rm -rf build/ dist/ .eggs/ *.egg-info/
	rm -rf .pytest_cache/ .ruff_cache/ .mypy_cache/
	rm -rf htmlcov/ .coverage coverage.xml
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
