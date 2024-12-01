# Aegis API

FastAPI microservice built with Domain-Driven Design and CQRS patterns.

## Quick Start

```bash
# Start dependencies
docker compose up -d db

# Install dependencies
pip install .

# Run migrations
alembic upgrade head

# Start the server
uvicorn aegis.main:app --reload
```

Visit http://localhost:8000/docs for the interactive API documentation.
