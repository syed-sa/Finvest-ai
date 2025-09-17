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
   git clone https://github.com/YOUR_USERNAME/fastapi-base.git
   cd fastapi-base
   ```

2. **Copy the environment file**:
   ```bash
   cp .env.example .env
   ```

3. **Install dependencies**:
   ```bash
   cd fastapi-base
   uv sync
   ```

4. **Set up pre-commit hooks**:
   ```bash
   make hooks
   ```

5. **Build and start the project**:
   ```bash
   make build
   ```

6. **Verify the setup** by accessing:
   - API: `http://localhost:8666/v1/ping`
   - Documentation: `http://localhost:8666/docs`

## Development Environment

- Use **Python >= 3.13**.
- **Recommended tools**: `pre-commit`, `black`, `isort`, `mypy`, `ruff`, `uv`.
- Run `make precommit-run` before submitting a PR.
- Use Docker for local development (see `docker-compose.yml`).

### Development Setup

1. **Start the development environment**:
   ```bash
   make up
   ```

2. **Access the application container**:
   ```bash
   make bash
   ```

3. **Run database migrations** (first time setup):
   ```bash
   make alembic-init
   make alembic-migrate
   ```

### Available Commands

The project includes a comprehensive Makefile with useful commands:

- `make up` - Start all services
- `make down` - Stop all services
- `make build` - Build and start services
- `make test` - Run test suite
- `make lint` - Run linting checks
- `make precommit-run` - Run all pre-commit hooks
- `make bash` - Access container shell

See the [Makefile](Makefile) for the complete list of available commands.

## Coding Standards

- Follow **PEP 8** and use `ruff` for linting and formatting.
- Organize imports with `isort` (or use `ruff` for both linting and import sorting).
- Type-check with `mypy` - all new code should include proper type hints.
- Use descriptive commit messages following [Conventional Commits](https://www.conventionalcommits.org/).
- Write clear docstrings for public modules, classes, and functions.
- Keep functions and classes focused and single-purpose.
- Use meaningful variable and function names.

### Code Formatting

The project uses automated code formatting tools:

```bash
make black    # Format code with Black
make isort    # Sort imports
make lint     # Run ruff linting
make mypy     # Type checking
```

### Docstring Style

Use Google-style docstrings:

```python
def example_function(param1: str, param2: int) -> bool:
    """Brief description of the function.

    Args:
        param1: Description of param1.
        param2: Description of param2.

    Returns:
        Description of return value.

    Raises:
        ValueError: When param2 is negative.
    """
    pass
```

## Testing

- Tests are located in `src/tests/` directory.
- **Run all tests** with:
  ```bash
  make test
  ```
- Add tests for new features and bug fixes.
- Ensure test coverage does not decrease.
- Use meaningful test names that describe what is being tested.

### Test Structure

```
tests/
├── conftest.py              # Pytest configuration and fixtures
├── test_api/               # API endpoint tests
├── test_models/            # Database model tests
├── test_core/              # Core functionality tests
└── test_utils/             # Utility function tests
```

### Writing Tests

Follow these guidelines when writing tests:

1. **Use descriptive test names**:
   ```python
   def test_user_creation_with_valid_data():
       # Test implementation
   ```

2. **Use fixtures for common setup**:
   ```python
   @pytest.fixture
   def sample_user():
       return {"email": "test@example.com", "password": "testpass"}
   ```

3. **Test both success and failure cases**:
   ```python
   def test_login_success():
       # Test successful login

   def test_login_invalid_credentials():
       # Test login with wrong credentials
   ```

4. **Use appropriate assertions**:
   ```python
   assert response.status_code == 200
   assert "error" not in response.json()
   ```

## Commit & PR Guidelines

### Creating a Feature Branch

1. **Create feature branches** from `main`:
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/my-new-feature
   ```

### Before Opening a PR

2. **Ensure your code passes all checks**:
   ```bash
   make precommit-run    # Run all pre-commit hooks
   make test             # Run test suite
   ```

3. **Update documentation** if needed:
   - Update README.md for user-facing changes
   - Update docstrings for API changes
   - Add or update examples if applicable

### Pull Request Process

4. **Push your changes**:
   ```bash
   git push origin feature/my-new-feature
   ```

5. **Create a Pull Request** with:
   - A clear, descriptive title
   - A detailed description of changes made
   - Reference to related issues (e.g., "Fixes #123")
   - Screenshots for UI changes (if applicable)

6. **Fill out the PR template** if available.

7. **Be responsive to review feedback**:
   - Address all reviewer comments
   - Update your branch with requested changes
   - Re-request review when ready

### Commit Message Guidelines

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

```
type(scope): description

[optional body]

[optional footer(s)]
```

**Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

**Examples:**
```
feat(auth): add JWT token authentication
fix(api): resolve user creation validation error
docs(readme): update installation instructions
```

## Code of Conduct

- Be respectful and inclusive.
- Follow the [Contributor Covenant](https://www.contributor-covenant.org/).

## Contact

- **Maintainer**: GabrielVGS (gabriel.viana.rs@gmail.com)
- For major changes, please open an issue first to discuss your proposal.
