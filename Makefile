all: black isort lint mypy

# docker
up:
	@echo "bringing up project...."
	docker compose up

down:
	@echo "bringing down project...."
	docker compose down

build:
	@echo "building project...."
	docker compose up --build

bash:
	@echo "connecting to container...."
	docker compose exec fastapi-base bash

# alembic
alembic-scaffold:
	@echo "scaffolding migrations folder..."
	docker compose exec fastapi-base alembic init migrations

alembic-init:
	@echo "initializing first migration...."
	docker compose exec fastapi-base alembic revision --autogenerate -m "init"

alembic-make-migrations:
	@read -p "Enter migration message: " comment; \
	echo "Creating migration file: $$comment"; \
	docker compose exec fastapi-base alembic revision --autogenerate -m "$$comment"

alembic-migrate:
	@echo "applying migration...."
	docker compose exec fastapi-base alembic upgrade head

alembic-reset:
	@echo "resetting database...."
	docker compose exec fastapi-base alembic downgrade base

# lint
test:
	@echo "running pytest...."
	docker compose exec fastapi-base pytest --cov-report xml --cov=src tests/

lint:
	@echo "running ruff...."
	docker compose exec fastapi-base ruff check src

black:
	@echo "running black...."
	docker compose exec fastapi-base black .

isort:
	@echo "running isort...."
	docker compose exec fastapi-base isort .

mypy:
	@echo "running mypy...."
	docker compose exec fastapi-base mypy src/

# database
init-db: alembic-init alembic-migrate
	@echo "initializing database...."
	docker compose exec fastapi-base python3 src/db/init_db.py

# misc
check: BREW-exists
BREW-exists: ; @which brew > /dev/null

hooks: check
	@echo "installing pre-commit hooks...."
	uvx pre-commit install

precommit-run:
	@echo "running pre-commit hooks...."
	uvx pre-commit run --all-files
