# Contributing to fastapi-base

> Thank you for your interest in contributing to **fastapi-base**! This document outlines the process and standards for contributing to this FastAPI backend project.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Environment](#development-environment)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Commit & PR Guidelines](#commit--pr-guidelines)
- [Code of Conduct](#code-of-conduct)
- [Contact](#contact)

## Getting Started

1. **Fork the repository** and clone your fork locally:
   ```bash
   git clone https://github.com/GabrielVGS/fastapi-base.git
   cd fastapi-base
   ```

2. **Install dependencies** (see `pyproject.toml`):
   ```bash
   cd fastapi-base
   uv sync
   ```

4. **Set up the project** (if needed):
   ```bash
   make build
   ```

## Development Environment

- Use **Python >= 3.13**.
- **Recommended tools**: `pre-commit`, `black`, `isort`, `mypy`, `ruff`, `uv`.
- Run `make precommit-run` before submiting a PR.
- Use Docker for local development (see `docker-compose.yml`).

## Coding Standards

- Follow **PEP8** and use `ruff` for formatting.
- Organize imports with `isort` or `ruff`.
- Type-check with `mypy`.
- Use descriptive commit messages.
- Write docstrings for public modules, classes, and functions.

## Testing

- Tests are located in `src/tests/`.
- **Run all tests** with:
  ```bash
  make test
  ```
- Add tests for new features and bug fixes.
- Ensure coverage does not decrease.

## Commit & PR Guidelines

1. **Create feature branches** from `main`.
```bash
git checkout -b feature/my-new-feature
2. **Ensure your code passes all checks** before opening a PR:
   ```bash
   make precommit-run
   make test
   ```
3. **Reference related issues** in your PR description.
4. **Fill out the PR template** if available.
5. **Be responsive to review feedback**.

## Code of Conduct

- Be respectful and inclusive.
- Follow the [Contributor Covenant](https://www.contributor-covenant.org/).

## Contact

- **Maintainer**: GabrielVGS (gabriel.viana.rs@gmail.com)
- For major changes, please open an issue first to discuss your proposal.
