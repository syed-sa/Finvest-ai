<p align="center">
    <a href="https://github.com/CIEX-FURG/ciex-backend/actions">
        <img alt="Status do GitHub Actions" src="https://github.com/CIEX-FURG/ciex-backend/actions/workflows/main.yml/badge.svg">
    </a>
    <a href="https://github.com/CIEX-FURG/ciex-backend/releases"><img alt="Status do Release" src="https://img.shields.io/github/v/release/CIEX-FURG/ciex-backend"></a>
</p>

## Documentação

- [Arquitetura](docs/architecture.md) - Visão geral da arquitetura do sistema
- [Desenvolvimento](docs/developing.md) - Guia de desenvolvimento local

## Uso

1. Execute `make up`
2. Acesse `http://localhost:8666/v1/ping` para o servidor uvicorn
3. Backend, API web baseada em JSON usando OpenAPI: `http://localhost:8666/v1/`
4. Documentação interativa automática com Swagger UI (do backend OpenAPI): `http://localhost:8666/docs`

## Desenvolvimento local do backend, detalhes adicionais

Inicializar a primeira migração (o projeto deve estar rodando com docker compose up e não conter arquivos de 'version')
```shell
$ make alembic-init
```

Criar novo arquivo de migração
```shell
$ docker compose exec ciex-backend alembic revision --autogenerate -m "algum comentário legal"
```

Aplicar migrações
```shell
$ make alembic-migrate
```

### Migrações

Após cada migração, você pode criar novas migrações e aplicá-las com:
```console
$ make alembic-make-migrations "comentário legal cara"
$ make alembic-migrate
```

### Fluxo de trabalho geral

Consulte o [Makefile](/Makefile) para visualizar os comandos disponíveis.

Por padrão, as dependências são gerenciadas com [uv](https://docs.astral.sh/uv/), acesse o link e instale-o.

A partir de `./ciex-backend/` você pode instalar todas as dependências com:
```console
$ uv sync
```

### Hooks do pre-commit

Se você ainda não fez isso, baixe o pacote do sistema [pre-commit](https://pre-commit.com/) e instale. Depois de concluído, instale os hooks do git com:
```console
$ pre-commit install
pre-commit installed at .git/hooks/pre-commit
```
