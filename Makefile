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
	docker compose exec ciex-backend bash

# alembic
alembic-scaffold:
	@echo "scaffolding migrations folder..."
	docker compose exec ciex-backend alembic init migrations

alembic-init:
	@echo "initializing first migration...."
	docker compose exec ciex-backend alembic revision --autogenerate -m "init"

alembic-make-migrations:
	@echo "creating migration file...."
	docker compose exec ciex-backend alembic revision --autogenerate -m "add year"

alembic-migrate:
	@echo "applying migration...."
	docker compose exec ciex-backend alembic upgrade head

# lint
test:
	@echo "running pytest...."
	docker compose exec ciex-backend pytest --cov-report xml --cov=src tests/

lint:
	@echo "running ruff...."
	docker compose exec ciex-backend ruff check src

black:
	@echo "running black...."
	docker compose exec ciex-backend black .

isort:
	@echo "running isort...."
	docker compose exec ciex-backend isort .

mypy:
	@echo "running mypy...."
	docker compose exec ciex-backend mypy src/

# database
init-db: alembic-init alembic-migrate
	@echo "initializing database...."
	docker compose exec ciex-backend python3 src/db/init_db.py

# misc
check: BREW-exists
BREW-exists: ; @which brew > /dev/null

hooks: check
	@echo "installing pre-commit hooks...."
	pre-commit install
