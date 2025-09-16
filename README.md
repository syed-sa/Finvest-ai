# FastAPI Base Project

[🇧🇷 Português](docs/README-pt.md)

<p align="center">
    <a href="https://github.com/GabrielVGS/fastapi-base/actions">
        <img alt="GitHub Actions Status" src="https://github.com/GabrielVGS/fastapi-base/actions/workflows/main.yml/badge.svg">
    </a>
    <a href="https://codecov.io/gh/GabrielVGS/fastapi-base">
     <img src="https://codecov.io/gh/GabrielVGS/fastapi-base/branch/main/graph/badge.svg?token=899NB4AK7J"/>
    </a>
    <a href="https://github.com/GabrielVGS/fastapi-base/releases">
        <img alt="Release Status" src="https://img.shields.io/github/v/release/GabrielVGS/fastapi-base">
    </a>
</p>

## 🏗️ Project Template

This project was created using the excellent [cookiecutter-fastapi-backend](https://github.com/nickatnight/cookiecutter-fastapi-backend) template, which provides a solid foundation for FastAPI applications with best practices and modern tooling.

## 📚 Documentation

- [Architecture](docs/architecture.md) - System architecture overview
- [Development](docs/developing.md) - CIEX local development guide

## 🚀 Quick Start

1. Run `make up`
2. Access `http://localhost:8666/v1/ping` for the uvicorn server
3. JSON-based web API backend using OpenAPI: `http://localhost:8666/v1/`
4. Interactive automatic documentation with Swagger UI (from OpenAPI backend): `http://localhost:8666/docs`

## 🛠️ Local Backend Development

### Database Migrations

Initialize the first migration (project must be running with docker compose up and contain no 'version' files):
```shell
$ make alembic-init
```

Create new migration file:
```shell
$ docker compose exec fastapi-base alembic revision --autogenerate -m "some cool comment"
```

Apply migrations:
```shell
$ make alembic-migrate
```

### Migration Workflow

After each migration, you can create new migrations and apply them with:
```console
$ make alembic-make-migrations "even cooler comment"
$ make alembic-migrate
```

## 🔧 General Workflow

Check the [Makefile](/Makefile) to view available commands.

By default, dependencies are managed with [uv](https://docs.astral.sh/uv/). Please visit the link and install it.

From `./fastapi-base/` you can install all dependencies with:
```console
$ uv sync
```

### Pre-commit Hooks

If you haven't already, download the [pre-commit](https://pre-commit.com/) system package and install it. Once completed, install the git hooks with:
```console
$ pre-commit install
pre-commit installed at .git/hooks/pre-commit
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
