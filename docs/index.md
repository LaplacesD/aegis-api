# Aegis API Documentation

Welcome to the Aegis API documentation.

Aegis is a FastAPI microservice built with **Domain-Driven Design** and **CQRS** patterns. It provides a clean, layered architecture suitable for modern cloud-native deployments.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/LaplacesD/aegis-api.git
cd aegis-api

# Start the database
docker compose up -d db

# Install dependencies
pip install -e ".[dev]"

# Run migrations
alembic upgrade head

# Start the development server
uvicorn aegis.main:app --reload
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive API docs.

## Project Structure

```
aegis-api/
├── aegis/
│   ├── api/              # HTTP layer (routes, schemas, middleware)
│   ├── application/      # CQRS (commands, queries, handlers, mediator)
│   ├── domain/           # Domain model (entities, value objects, events)
│   └── infrastructure/   # Persistence, event bus, UoW
├── tests/
├── docs/
├── kubernetes/
└── .github/
```
