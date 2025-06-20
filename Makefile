.PHONY: help install dev install-dev lint typecheck test coverage migrate docker-build docker-up clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
	pip install .

install-dev: ## Install development dependencies
	pip install -e ".[dev]"

lint: ## Run Ruff linter
	ruff check aegis/ tests/

typecheck: ## Run mypy type checker
	mypy aegis/

test: ## Run tests with pytest
	pytest --cov=aegis tests/ -v

coverage: ## Run tests with coverage report
	pytest --cov=aegis --cov-report=term-missing tests/

migrate: ## Run database migrations
	alembic upgrade head

docker-build: ## Build Docker image
	docker build -t aegis-api .

docker-up: ## Start all services with Docker Compose
	docker compose up -d

docker-down: ## Stop all services
	docker compose down

clean: ## Clean build artifacts
	rm -rf build/ dist/ *.egg-info .pytest_cache/ .mypy_cache/ __pycache__/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
