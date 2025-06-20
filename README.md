# Aegis API

[![CI](https://github.com/LaplacesD/aegis-api/actions/workflows/ci.yml/badge.svg)](https://github.com/LaplacesD/aegis-api/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

FastAPI microservice built with **Domain-Driven Design** and **CQRS** patterns.

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                     API Layer                             │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐│
│   │  Users   │  │  Orders  │  │ Products │  │Middleware│
│   └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬───┘│
└────────┼──────────────┼──────────────┼─────────────┼────┘
         │              │              │              │
┌────────┼──────────────┼──────────────┼─────────────┼────┐
│        ▼              ▼              ▼              ▼    │
│              Application Layer (CQRS)                    │
│   ┌──────────┐  ┌──────────┐  ┌───────────────────┐     │
│   │ Commands │  │  Queries  │  │    Mediator       │     │
│   └────┬─────┘  └────┬─────┘  └─────────┬─────────┘     │
└────────┼──────────────┼──────────────────┼───────────────┘
         │              │                  │
┌────────┼──────────────┼──────────────────┼───────────────┐
│        ▼              ▼                  ▼               │
│                Domain Layer                               │
│   ┌──────────┐  ┌──────────┐  ┌──────────────────┐      │
│   │ Entities │  │ Value    │  │ Domain Events &   │      │
│   │ (User,   │  │ Objects  │  │ Repository        │      │
│   │  Order,  │  │ (Money,  │  │ Interfaces        │      │
│   │  Product)│  │  Email)  │  │                   │      │
│   └──────────┘  └──────────┘  └──────────────────┘      │
└──────────────────────────────────────────────────────────┘
         │
┌────────┼──────────────────────────────────────────────────┐
│        ▼                                                  │
│           Infrastructure Layer                             │
│   ┌──────────┐  ┌────────────┐  ┌──────────────────┐     │
│   │ SQLAlchemy│  │ Event Store│  │    Unit of Work  │     │
│   │ Repos     │  │ (Sourcing) │  │                  │     │
│   └──────────┘  └────────────┘  └──────────────────┘     │
│                                                            │
│   ┌──────────────────────────────────────────────────┐    │
│   │            PostgreSQL Database                    │    │
│   └──────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────┘
```

## Quick Start

```bash
# Start dependencies
docker compose up -d db

# Install dependencies
pip install -e ".[dev]"

# Run migrations
alembic upgrade head

# Start the server
uvicorn aegis.main:app --reload
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive API documentation.

## Project Structure

```
aegis-api/
├── aegis/
│   ├── api/              # HTTP layer (routes, schemas, middleware)
│   │   └── v1/           # Version 1 API endpoints
│   ├── application/      # CQRS (commands, queries, handlers, mediator)
│   ├── domain/           # Domain model (entities, value objects, events)
│   └── infrastructure/   # Persistence, event bus, UoW
├── tests/                # Test suite
├── docs/                 # Documentation (MkDocs)
├── kubernetes/           # Kubernetes manifests
├── .github/workflows/    # CI/CD pipelines
├── docker-compose.yml    # Local dev environment
├── Dockerfile            # Container image
└── alembic/              # Database migrations
```

## Development

```bash
# Install dev dependencies
make install-dev

# Lint and type-check
make lint
make typecheck

# Run tests
make test

# Build Docker image
make docker-build
```

## Deployment

### Docker Compose

```bash
docker compose up -d
```

### Kubernetes

```bash
kubectl apply -f kubernetes/
```

## License

MIT — see [LICENSE](LICENSE).
