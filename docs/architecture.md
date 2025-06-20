# Architecture

## Layered Architecture

Aegis follows a strict layered architecture with **Domain-Driven Design** principles:

### Domain Layer (`aegis/domain/`)

The innermost layer with zero external dependencies. Contains:

- **Entities**: `User`, `Order`, `Product`, `OrderItem` — rich domain models with behaviour
- **Value Objects**: `Email`, `Money`, `Address`, `OrderStatus` — immutable, self-validating
- **Domain Events**: `UserCreated`, `OrderPlaced`, `OrderShipped`, etc.
- **Repository Interfaces**: Abstract contracts for data access
- **Domain Exceptions**: Typed errors for business rule violations

### Application Layer (`aegis/application/`)

Orchestrates domain operations using **CQRS**:

- **Commands**: `CreateOrderCommand`, `UpdateUserCommand`
- **Queries**: `GetUserQuery`, `GetOrdersQuery`
- **Handlers**: Process commands/queries via injected repositories
- **Mediator**: Decouples callers from handlers
- **DTOs**: Data Transfer Objects for cross-layer communication

### Infrastructure Layer (`aegis/infrastructure/`)

Concrete implementations of domain contracts:

- **Database**: Async PostgreSQL via SQLAlchemy 2.0
- **Repositories**: SQLAlchemy-backed persistence
- **Event Store**: Event sourcing audit trail
- **Unit of Work**: Transactional consistency
- **Event Bus**: In-process domain event dispatch

### API Layer (`aegis/api/`)

HTTP-facing layer:

- **Routers**: RESTful endpoints under `/v1/`
- **Schemas**: Pydantic models for request/response validation
- **Middleware**: Authentication, logging, error handling
- **Dependencies**: FastDI wiring for Mediator and services

## Data Flow

```
Client → API Router → Mediator → Handler → Repository → Database
                          ↓
                     Domain Events → Event Bus → Subscribers
```
