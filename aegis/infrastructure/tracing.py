"""OpenTelemetry tracing integration for aegis-api."""

from __future__ import annotations

from functools import wraps
from typing import Any, Callable

from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)

from aegis.config import settings

tracer = trace.get_tracer("aegis-api")


def init_tracing(service_name: str = "aegis-api") -> None:
    """Initialize OpenTelemetry tracing.

    Args:
        service_name: Name of the service for span attribution.
    """
    provider = TracerProvider()
    if settings.otel_exporter == "console":
        provider.add_span_processor(
            BatchSpanProcessor(ConsoleSpanExporter())
        )
    trace.set_tracer_provider(provider)


def instrument_app(app) -> None:
    """Instrument a FastAPI app and its SQLAlchemy engine."""
    FastAPIInstrumentor.instrument_app(app)
    try:
        engine = app.state.engine
        SQLAlchemyInstrumentor().instrument(engine=engine.sync_engine)
    except AttributeError:
        pass


def traced(
    name: str | None = None,
    attributes: dict[str, str] | None = None,
) -> Callable:
    """Decorator to trace a function call."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            span_name = name or f"{func.__module__}.{func.__name__}"
            with tracer.start_as_current_span(
                span_name, attributes=attributes
            ):
                return await func(*args, **kwargs)

        return wrapper

    return decorator
