# Contributing to Aegis API

We welcome contributions! Please follow these guidelines.

## Development Setup

```bash
git clone https://github.com/LaplacesD/aegis-api.git
cd aegis-api
pip install -e ".[dev]"
pre-commit install
```

## Code Style

- All code must pass `ruff check .` and `mypy aegis/`
- Use type hints for all function signatures
- Write docstrings for public APIs (Google-style)
- Keep functions focused and small

## Testing

- All new features must include tests
- Run `pytest tests/` before submitting
- Aim for >80% coverage on new code

## Commit Convention

We use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` — new feature
- `fix:` — bug fix
- `refactor:` — code change without feature/fix
- `docs:` — documentation only
- `test:` — test additions/fixes
- `chore:` — maintenance tasks

## Pull Request Process

1. Create a feature branch from `develop`
2. Write tests for your changes
3. Ensure CI passes (lint + test)
4. Submit a PR against `main`
5. Request review from a maintainer

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
