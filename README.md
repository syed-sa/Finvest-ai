# FastAPI Base Project / Projeto Base FastAPI

[🇺🇸 English](#english) | [🇧🇷 Português](#português)

---

## English

<p align="center">
    <a href="https://github.com/GabrielVGS/fastapi-base/actions">
        <img alt="GitHub Actions Status" src="https://github.com/CIEX-FURG/fastapi-base/actions/workflows/main.yml/badge.svg">
    </a>
    <a href="https://codecov.io/gh/GabrielVGS/fastapi-base">
     <img src="https://codecov.io/gh/GabrielVGS/fastapi-base/branch/main/graph/badge.svg?token=899NB4AK7J"/>
    </a>
    <a href="https://github.com/GabrielVGS/fastapi-base/releases"><img alt="Release Status" src="https://img.shields.io/github/v/release/GabrielVGS/fastapi-base"></a>
</p>

### 🏗️ Project Template

This project was created using the excellent [cookiecutter-fastapi-backend](https://github.com/nickatnight/cookiecutter-fastapi-backend) template, which provides a solid foundation for FastAPI applications with best practices and modern tooling.

### 📚 Documentation

- [Architecture](docs/architecture.md) - System architecture overview
- [Development](docs/developing.md) - CIEX local development guide

### 🚀 Quick Start

1. Run `make up`
2. Access `http://localhost:8666/v1/ping` for the uvicorn server
3. JSON-based web API backend using OpenAPI: `http://localhost:8666/v1/`
4. Interactive automatic documentation with Swagger UI (from OpenAPI backend): `http://localhost:8666/docs`

### 🛠️ Local Backend Development

#### Database Migrations

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

#### Migration Workflow

After each migration, you can create new migrations and apply them with:
```console
$ make alembic-make-migrations "even cooler comment"
$ make alembic-migrate
```

### 🔧 General Workflow

Check the [Makefile](/Makefile) to view available commands.

By default, dependencies are managed with [uv](https://docs.astral.sh/uv/). Please visit the link and install it.

From `./fastapi-base/` you can install all dependencies with:
```console
$ uv sync
```

#### Pre-commit Hooks

If you haven't already, download the [pre-commit](https://pre-commit.com/) system package and install it. Once completed, install the git hooks with:
```console
$ pre-commit install
pre-commit installed at .git/hooks/pre-commit
```

---

## Português

<p align="center">
    <a href="https://github.com/GabrielVGS/fastapi-base/actions">
        <img alt="Status do GitHub Actions" src="https://github.com/GabrielVGS/fastapi-base/actions/workflows/main.yml/badge.svg">
    </a>
    <a href="https://codecov.io/gh/GabrielVGS/fastapi-base">
     <img src="https://codecov.io/gh/GabrielVGS/fastapi-base/branch/main/graph/badge.svg?token=899NB4AK7J"/>
    </a>
    <a href="https://github.com/GabrielVGS/fastapi-base/releases"><img alt="Status do Release" src="https://img.shields.io/github/v/release/CIEX-FURG/fastapi-base"></a>
</p>

### 🏗️ Template do Projeto

Este projeto foi criado usando o excelente template [cookiecutter-fastapi-backend](https://github.com/nickatnight/cookiecutter-fastapi-backend), que fornece uma base sólida para aplicações FastAPI com melhores práticas e ferramentas modernas.

### 📚 Documentação

- [Arquitetura](docs/architecture.md) - Visão geral da arquitetura do sistema
- [Desenvolvimento](docs/developing.md) - Guia de desenvolvimento local CIEX

### 🚀 Início Rápido

1. Execute `make up`
2. Acesse `http://localhost:8666/v1/ping` para o servidor uvicorn
3. Backend, API web baseada em JSON usando OpenAPI: `http://localhost:8666/v1/`
4. Documentação interativa automática com Swagger UI (do backend OpenAPI): `http://localhost:8666/docs`

### 🛠️ Desenvolvimento Local do Backend

#### Migrações do Banco de Dados

Inicializar a primeira migração (o projeto deve estar rodando com docker compose up e não conter arquivos de 'version'):
```shell
$ make alembic-init
```

Criar novo arquivo de migração:
```shell
$ docker compose exec fastapi-base alembic revision --autogenerate -m "algum comentário legal"
```

Aplicar migrações:
```shell
$ make alembic-migrate
```

#### Fluxo de Trabalho das Migrações

Após cada migração, você pode criar novas migrações e aplicá-las com:
```console
$ make alembic-make-migrations "comentário mais legal ainda"
$ make alembic-migrate
```

### 🔧 Fluxo de Trabalho Geral

Consulte o [Makefile](/Makefile) para visualizar os comandos disponíveis.

Por padrão, as dependências são gerenciadas com [uv](https://docs.astral.sh/uv/). Acesse o link e instale-o.

A partir de `./fastapi-base/` você pode instalar todas as dependências com:
```console
$ uv sync
```

#### Hooks do Pre-commit

Se você ainda não fez isso, baixe o pacote do sistema [pre-commit](https://pre-commit.com/) e instale. Depois de concluído, instale os hooks do git com:
```console
$ pre-commit install
pre-commit installed at .git/hooks/pre-commit
```

---

### 🤝 Contributing / Contribuindo

Contributions are welcome! Please feel free to submit a Pull Request.

Contribuições são bem-vindas! Fique à vontade para enviar um Pull Request.

### 📄 License / Licença

This project is licensed under the MIT License - see the LICENSE file for details.

Este projeto está licenciado sob a Licença MIT - consulte o arquivo LICENSE para obter detalhes.