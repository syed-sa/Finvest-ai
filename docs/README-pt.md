# Projeto Base FastAPI

<p align="center">
  <a href="../README.md">🇺🇸 English</a> |
  <a href="README-fr.md">🇫🇷 Français</a> |
  <a href="README-es.md">🇪🇸 Español</a>
</p>

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

Um template backend FastAPI moderno e pronto para produção com melhores práticas, suporte Docker e ferramentas abrangentes para desenvolvimento rápido.

## 🏗️ Template do Projeto

Este projeto foi criado usando o excelente template [cookiecutter-fastapi-backend](https://github.com/nickatnight/cookiecutter-fastapi-backend), que fornece uma base sólida para aplicações FastAPI com melhores práticas e ferramentas modernas.

## 📚 Documentação

- [Arquitetura](architecture.md) - Visão geral da arquitetura do sistema
- [Guia de Desenvolvimento](developing.md) - Diretrizes de desenvolvimento local
- [Guia de Contribuição](../CONTRIBUTING.md) - Como contribuir para este projeto

## ✨ Funcionalidades

- **FastAPI** - Framework web moderno e rápido para construir APIs
- **Docker** - Desenvolvimento e implantação containerizada
- **PostgreSQL** - Base de dados relacional robusta com suporte assíncrono
- **Redis** - Cache e gestão de sessões
- **Celery** - Processamento de tarefas em segundo plano
- **Alembic** - Gestão de migrações de base de dados
- **Testes** - Suite de testes abrangente com pytest
- **Qualidade de Código** - Hooks pre-commit, linting e formatação
- **Segurança de Tipos** - Anotações de tipo completas com validação mypy
- **Documentação** - Documentação API auto-gerada com Swagger UI

## 🚀 Início Rápido

### Pré-requisitos

- Docker e Docker Compose
- Python 3.13+ (para desenvolvimento local)
- Gestor de pacotes [uv](https://docs.astral.sh/uv/)

### Executar com Docker (Recomendado)

1. **Clonar o repositório**:
   ```bash
   git clone https://github.com/GabrielVGS/fastapi-base.git
   cd fastapi-base
   ```

2. **Copiar variáveis de ambiente**:
   ```bash
   cp .env.example .env
   ```

3. **Iniciar os serviços**:
   ```bash
   make up
   ```

4. **Aceder à aplicação**:
   - API: `http://localhost:8666/v1/`
   - Verificação de saúde: `http://localhost:8666/v1/ping`
   - Documentação interativa: `http://localhost:8666/docs`
   - Documentação alternativa: `http://localhost:8666/redoc`

## 🛠️ Desenvolvimento Local

### Configuração do Ambiente Local

1. **Instalar uv** (se não estiver já instalado):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Navegar para o diretório do projeto**:
   ```bash
   cd fastapi-base/
   ```

3. **Instalar dependências**:
   ```bash
   uv sync
   ```

4. **Instalar hooks pre-commit**:
   ```bash
   make hooks
   ```

### Migrações da Base de Dados

Inicializar a primeira migração (o projeto deve estar a executar com `docker compose up` e não conter arquivos 'version'):
```bash
make alembic-init
```

Criar novo arquivo de migração:
```bash
make alembic-make-migrations "descreva as suas alterações"
```

Aplicar migrações:
```bash
make alembic-migrate
```

### Fluxo de Trabalho das Migrações

Após cada migração, pode criar novas migrações e aplicá-las com:
```bash
make alembic-make-migrations "descreva as suas alterações"
make alembic-migrate
```

## 📋 Variáveis de Ambiente

Crie um arquivo `.env` baseado no `.env.example`:

### Configurações da Aplicação
- `PROJECT_NAME` - Nome do projeto (padrão: fastapi-base)
- `VERSION` - Versão da API (padrão: v1)
- `DEBUG` - Ativar modo debug (padrão: True)
- `SECRET_KEY` - Chave secreta para JWT e encriptação
- `ENV` - Ambiente (dev/staging/production)

### Configuração da Base de Dados
- `POSTGRES_USER` - Nome de utilizador PostgreSQL
- `POSTGRES_PASSWORD` - Palavra-passe PostgreSQL
- `POSTGRES_DB` - Nome da base de dados
- `POSTGRES_HOST` - Host da base de dados (padrão: localhost)
- `POSTGRES_PORT` - Porta da base de dados (padrão: 5432)
- `POSTGRES_URL` - URL completa da base de dados (opcional, auto-gerada se não fornecida)

### Configuração Redis
- `REDIS_HOST` - Host Redis (padrão: redis)
- `REDIS_PORT` - Porta Redis (padrão: 6379)
- `REDIS_URL` - URL completa Redis (opcional, auto-gerada se não fornecida)

### Configurações Opcionais
- `SENTRY_DSN` - DSN de rastreamento de erros Sentry
- `LOG_LEVEL` - Nível de logging (padrão: INFO)
- `CACHE_TTL` - Tempo de vida do cache em segundos (padrão: 60)

## 🏃 Executar a Aplicação

### Usando Docker Compose (Recomendado)

```bash
# Construir e iniciar todos os serviços
make build

# Iniciar serviços (sem construção)
make up

# Parar serviços
make down

# Aceder ao bash do contentor
make bash
```

### Desenvolvimento Local (sem Docker)

```bash
# Assegurar que PostgreSQL e Redis estão a executar localmente
# Atualizar .env com conexões locais de base de dados/redis

# Executar a aplicação FastAPI
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## 🔧 Fluxo de Trabalho de Desenvolvimento

Consulte o [Makefile](../Makefile) para ver todos os comandos disponíveis.

### Comandos Make Disponíveis

```bash
# Desenvolvimento
make up          # Iniciar todos os serviços com Docker Compose
make down        # Parar todos os serviços
make build       # Construir e iniciar serviços
make bash        # Aceder ao shell do contentor principal

# Base de Dados
make alembic-init              # Inicializar primeira migração
make alembic-make-migrations   # Criar nova migração
make alembic-migrate          # Aplicar migrações
make alembic-reset            # Reiniciar base de dados
make init-db                  # Inicializar base de dados com dados de exemplo

# Qualidade de Código
make test           # Executar suite de testes com cobertura
make lint           # Executar linter ruff
make black          # Formatar código com black
make isort          # Ordenar imports
make mypy           # Verificação de tipos
make precommit-run  # Executar todos os hooks pre-commit

# Manutenção
make hooks          # Instalar hooks pre-commit
```

### Dependências

Por padrão, as dependências são geridas com [uv](https://docs.astral.sh/uv/). Por favor visite o link e instale-o.

A partir de `./fastapi-base/` pode instalar todas as dependências com:
```bash
uv sync
```

### Hooks Pre-commit

O projeto usa hooks pre-commit para assegurar a qualidade do código. Instale-os com:
```bash
make hooks
```

Isto instalará hooks que executam automaticamente antes de cada commit para:
- Formatar código com `black`
- Ordenar imports com `isort`
- Analisar código com `ruff`
- Verificar tipos com `mypy`
- Executar testes

## 🧪 Testes

Executar a suite completa de testes:
```bash
make test
```

Executar testes específicos:
```bash
# Dentro do contentor
docker compose exec fastapi-base pytest tests/test_specific.py

# Localmente (se as dependências estiverem instaladas)
uv run pytest tests/test_specific.py
```

## 🚀 Implantação em Produção

O projeto inclui configurações Docker prontas para produção:

### Usando Dockerfile de Produção
```bash
# Construir imagem de produção
docker build -f ops/production.Dockerfile -t fastapi-base:prod .

# Executar contentor de produção
docker run -p 8000:8000 --env-file .env fastapi-base:prod
```

### Considerações Específicas do Ambiente
- Definir `DEBUG=False` em produção
- Usar `SECRET_KEY` apropriada
- Configurar `SENTRY_DSN` para rastreamento de erros
- Definir credenciais apropriadas da base de dados
- Usar Redis para gestão de sessões e cache

## 🏗️ Estrutura do Projeto

```
fastapi-base/
├── fastapi-base/              # Diretório principal da aplicação
│   ├── src/                   # Código fonte
│   │   ├── core/              # Configuração e definições principais
│   │   ├── models/            # Modelos da base de dados
│   │   ├── api/               # Rotas e endpoints API
│   │   ├── db/                # Utilitários da base de dados
│   │   ├── migrations/        # Migrações da base de dados Alembic
│   │   └── main.py            # Ponto de entrada da aplicação
│   ├── tests/                 # Suite de testes
│   ├── pyproject.toml         # Dependências Python e configuração de ferramentas
│   └── Dockerfile             # Imagem Docker de desenvolvimento
├── ops/                       # Operações e implantação
│   └── production.Dockerfile  # Imagem Docker de produção
├── docs/                      # Documentação
├── docker-compose.yml         # Configuração do ambiente de desenvolvimento
├── Makefile                   # Comandos de desenvolvimento
└── .env.example              # Template de variáveis de ambiente
```

## 🤝 Contribuir

Damos as boas-vindas às contribuições! Por favor consulte as nossas [Diretrizes de Contribuição](../CONTRIBUTING.md) para informações detalhadas sobre:

- Configurar o seu ambiente de desenvolvimento
- Estilo de código e padrões
- Requisitos de testes
- Processo de pull request
- Código de conduta

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - consulte o arquivo [LICENSE](../LICENSE) para detalhes.

## 🛠️ Construído Com

- [FastAPI](https://fastapi.tiangolo.com/) - Framework web moderno e rápido
- [SQLModel](https://sqlmodel.tiangolo.com/) - Bases de dados SQL em Python, desenhado para simplicidade
- [Alembic](https://alembic.sqlalchemy.org/) - Ferramenta de migração de base de dados
- [Celery](https://docs.celeryproject.org/) - Fila de tarefas distribuída
- [Redis](https://redis.io/) - Armazenamento de estrutura de dados em memória
- [PostgreSQL](https://www.postgresql.org/) - Base de dados avançada de código aberto
- [Docker](https://www.docker.com/) - Plataforma de containerização
- [uv](https://docs.astral.sh/uv/) - Gestor de pacotes Python rápido

## 📚 Recursos Adicionais

- [Documentação FastAPI](https://fastapi.tiangolo.com/)
- [Documentação SQLModel](https://sqlmodel.tiangolo.com/)
- [Documentação Docker](https://docs.docker.com/)
- [Documentação PostgreSQL](https://www.postgresql.org/docs/)

## ⭐️ Apoie

Se achou este projeto útil, por favor considere:

- Dar uma estrela ⭐️ no GitHub
- Partilhar com os seus colegas
- Contribuir para o seu desenvolvimento
- Reportar problemas ou sugerir melhorias

---

**Bom código!** 🚀
