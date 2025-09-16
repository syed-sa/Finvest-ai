# Projeto Base FastAPI

[🇺🇸 English](README.md)

<p align="center">
    <a href="https://github.com/GabrielVGS/fastapi-base/actions">
        <img alt="Status do GitHub Actions" src="https://github.com/GabrielVGS/fastapi-base/actions/workflows/main.yml/badge.svg">
    </a>
    <a href="https://codecov.io/gh/GabrielVGS/fastapi-base">
     <img src="https://codecov.io/gh/GabrielVGS/fastapi-base/branch/main/graph/badge.svg?token=899NB4AK7J"/>
    </a>
    <a href="https://github.com/GabrielVGS/fastapi-base/releases">
        <img alt="Status do Release" src="https://img.shields.io/github/v/release/GabrielVGS/fastapi-base">
    </a>
</p>

## 🏗️ Template do Projeto

Este projeto foi criado usando o excelente template [cookiecutter-fastapi-backend](https://github.com/nickatnight/cookiecutter-fastapi-backend), que fornece uma base sólida para aplicações FastAPI com melhores práticas e ferramentas modernas.

## 📚 Documentação

- [Arquitetura](docs/architecture.md) - Visão geral da arquitetura do sistema
- [Desenvolvimento](docs/developing.md) - Guia de desenvolvimento local CIEX

## 🚀 Início Rápido

1. Execute `make up`
2. Acesse `http://localhost:8666/v1/ping` para o servidor uvicorn
3. Backend, API web baseada em JSON usando OpenAPI: `http://localhost:8666/v1/`
4. Documentação interativa automática com Swagger UI (do backend OpenAPI): `http://localhost:8666/docs`

## 🛠️ Desenvolvimento Local do Backend

### Migrações do Banco de Dados

Inicialize a primeira migração (o projeto deve estar rodando com docker compose up e não conter arquivos de 'version'):
```shell
$ make alembic-init
```

Crie um novo arquivo de migração:
```shell
$ docker compose exec fastapi-base alembic revision --autogenerate -m "algum comentário legal"
```

Aplique as migrações:
```shell
$ make alembic-migrate
```

### Fluxo de Trabalho das Migrações

Após cada migração, você pode criar novas migrações e aplicá-las com:
```console
$ make alembic-make-migrations "comentário mais legal ainda"
$ make alembic-migrate
```

## 🔧 Fluxo de Trabalho Geral

Consulte o [Makefile](/Makefile) para visualizar os comandos disponíveis.

Por padrão, as dependências são gerenciadas com [uv](https://docs.astral.sh/uv/). Acesse o link e instale-o.

A partir de `./fastapi-base/` você pode instalar todas as dependências com:
```console
$ uv sync
```

### Hooks do Pre-commit

Se você ainda não fez isso, baixe o pacote do sistema [pre-commit](https://pre-commit.com/) e instale. Depois de concluído, instale os hooks do git com:
```console
$ pre-commit install
pre-commit instalado em .git/hooks/pre-commit
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Fique à vontade para enviar um Pull Request.

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - consulte o arquivo LICENSE para obter detalhes.

## ⭐️ Apoie

Se você achou este projeto útil, por favor considere deixar uma estrela no repositório!
