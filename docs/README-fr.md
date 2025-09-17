# Projet Base FastAPI

<p align="center">
  <a href="../README.md">🇺🇸 English</a> |
  <a href="README-pt.md">🇧🇷 Português</a> |
  <a href="README-es.md">🇪🇸 Español</a>
</p>

<p align="center">
    <a href="https://github.com/GabrielVGS/fastapi-base/actions">
        <img alt="Statut GitHub Actions" src="https://github.com/GabrielVGS/fastapi-base/actions/workflows/main.yml/badge.svg">
    </a>
    <a href="https://codecov.io/gh/GabrielVGS/fastapi-base">
     <img src="https://codecov.io/gh/GabrielVGS/fastapi-base/branch/main/graph/badge.svg?token=899NB4AK7J"/>
    </a>
    <a href="https://github.com/GabrielVGS/fastapi-base/releases">
        <img alt="Statut de Version" src="https://img.shields.io/github/v/release/GabrielVGS/fastapi-base">
    </a>
</p>

Un template backend FastAPI moderne et prêt pour la production avec des meilleures pratiques, le support Docker et des outils complets pour un développement rapide.

## 🏗️ Template du Projet

Ce projet a été créé en utilisant l'excellent template [cookiecutter-fastapi-backend](https://github.com/nickatnight/cookiecutter-fastapi-backend) par [@nickatnight](https://github.com/nickatnight), qui fournit une base solide pour les applications FastAPI avec les meilleures pratiques et des outils modernes.

## 📚 Documentation

- [Architecture](architecture.md) - Aperçu de l'architecture système
- [Guide de Développement](developing.md) - Directives de développement local
- [Guide de Contribution](../CONTRIBUTING.md) - Comment contribuer à ce projet
- [Dépannage](troubleshooting.md) - Problèmes courants et solutions

## ✨ Fonctionnalités

- **FastAPI** - Framework web moderne et rapide pour construire des APIs
- **Docker** - Développement et déploiement conteneurisés
- **PostgreSQL** - Base de données relationnelle robuste avec support asynchrone
- **Redis** - Mise en cache et gestion des sessions
- **Celery** - Traitement de tâches en arrière-plan
- **Alembic** - Gestion des migrations de base de données
- **Tests** - Suite de tests complète avec pytest
- **Qualité du Code** - Hooks pre-commit, linting et formatage
- **Sécurité des Types** - Annotations de type complètes avec validation mypy
- **Documentation** - Documentation API auto-générée avec Swagger UI

## 🚀 Démarrage Rapide

### Prérequis

- Docker et Docker Compose
- Python 3.13+ (pour le développement local)
- Gestionnaire de paquets [uv](https://docs.astral.sh/uv/)

### Exécution avec Docker (Recommandé)

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/GabrielVGS/fastapi-base.git
   cd fastapi-base
   ```

2. **Copier les variables d'environnement** :
   ```bash
   cp .env.example .env
   ```

3. **Démarrer les services** :
   ```bash
   make up
   ```

4. **Accéder à l'application** :
   - API : `http://localhost:8666/v1/`
   - Vérification de santé : `http://localhost:8666/v1/ping`
   - Documentation interactive : `http://localhost:8666/docs`
   - Documentation alternative : `http://localhost:8666/redoc`

## 🛠️ Développement Local

### Configuration de l'Environnement Local

1. **Installer uv** (si pas déjà installé) :
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Naviguer vers le répertoire du projet** :
   ```bash
   cd fastapi-base/
   ```

3. **Installer les dépendances** :
   ```bash
   uv sync
   ```

4. **Installer les hooks pre-commit** :
   ```bash
   make hooks
   ```

### Migrations de Base de Données

Initialiser la première migration (le projet doit fonctionner avec `docker compose up` et ne contenir aucun fichier 'version') :
```bash
make alembic-init
```

Créer un nouveau fichier de migration :
```bash
make alembic-make-migrations "décrivez vos modifications"
```

Appliquer les migrations :
```bash
make alembic-migrate
```

### Flux de Travail des Migrations

Après chaque migration, vous pouvez créer de nouvelles migrations et les appliquer avec :
```bash
make alembic-make-migrations "décrivez vos modifications"
make alembic-migrate
```

## 📋 Variables d'Environnement

Créez un fichier `.env` basé sur `.env.example` :

### Paramètres d'Application
- `PROJECT_NAME` - Nom du projet (par défaut : fastapi-base)
- `VERSION` - Version de l'API (par défaut : v1)
- `DEBUG` - Activer le mode debug (par défaut : True)
- `SECRET_KEY` - Clé secrète pour JWT et chiffrement
- `ENV` - Environnement (dev/staging/production)

### Configuration de Base de Données
- `POSTGRES_USER` - Nom d'utilisateur PostgreSQL
- `POSTGRES_PASSWORD` - Mot de passe PostgreSQL
- `POSTGRES_DB` - Nom de la base de données
- `POSTGRES_HOST` - Hôte de la base de données (par défaut : localhost)
- `POSTGRES_PORT` - Port de la base de données (par défaut : 5432)
- `POSTGRES_URL` - URL complète de la base de données (optionnel, auto-généré si non fourni)

### Configuration Redis
- `REDIS_HOST` - Hôte Redis (par défaut : redis)
- `REDIS_PORT` - Port Redis (par défaut : 6379)
- `REDIS_URL` - URL complète Redis (optionnel, auto-généré si non fourni)

### Paramètres Optionnels
- `SENTRY_DSN` - DSN de suivi d'erreurs Sentry
- `LOG_LEVEL` - Niveau de log (par défaut : INFO)
- `CACHE_TTL` - Durée de vie du cache en secondes (par défaut : 60)

## 🏃 Exécution de l'Application

### Utilisation de Docker Compose (Recommandé)

```bash
# Construire et démarrer tous les services
make build

# Démarrer les services (sans construction)
make up

# Arrêter les services
make down

# Accéder au bash du conteneur
make bash
```

### Développement Local (sans Docker)

```bash
# S'assurer que PostgreSQL et Redis fonctionnent localement
# Mettre à jour .env avec les connexions locales base de données/redis

# Exécuter l'application FastAPI
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## 🔧 Flux de Travail de Développement

Consultez le [Makefile](../Makefile) pour voir toutes les commandes disponibles.

### Commandes Make Disponibles

```bash
# Développement
make up          # Démarrer tous les services avec Docker Compose
make down        # Arrêter tous les services
make build       # Construire et démarrer les services
make bash        # Accéder au shell du conteneur principal

# Base de Données
make alembic-init              # Initialiser la première migration
make alembic-make-migrations   # Créer une nouvelle migration
make alembic-migrate          # Appliquer les migrations
make alembic-reset            # Réinitialiser la base de données
make init-db                  # Initialiser la base de données avec des données d'exemple

# Qualité du Code
make test           # Exécuter la suite de tests avec couverture
make lint           # Exécuter le linter ruff
make black          # Formater le code avec black
make isort          # Trier les imports
make mypy           # Vérification des types
make precommit-run  # Exécuter tous les hooks pre-commit

# Maintenance
make hooks          # Installer les hooks pre-commit
```

### Dépendances

Par défaut, les dépendances sont gérées avec [uv](https://docs.astral.sh/uv/). Veuillez visiter le lien et l'installer.

Depuis `./fastapi-base/` vous pouvez installer toutes les dépendances avec :
```bash
uv sync
```

### Hooks Pre-commit

Le projet utilise des hooks pre-commit pour assurer la qualité du code. Installez-les avec :
```bash
make hooks
```

Cela installera des hooks qui s'exécutent automatiquement avant chaque commit pour :
- Formater le code avec `black`
- Trier les imports avec `isort`
- Analyser le code avec `ruff`
- Vérifier les types avec `mypy`
- Exécuter les tests

## 🧪 Tests

Exécuter la suite de tests complète :
```bash
make test
```

Exécuter des tests spécifiques :
```bash
# À l'intérieur du conteneur
docker compose exec fastapi-base pytest tests/test_specific.py

# Localement (si les dépendances sont installées)
uv run pytest tests/test_specific.py
```

## 🚀 Déploiement en Production

Le projet inclut des configurations Docker prêtes pour la production :

### Utilisation du Dockerfile de Production
```bash
# Construire l'image de production
docker build -f ops/production.Dockerfile -t fastapi-base:prod .

# Exécuter le conteneur de production
docker run -p 8000:8000 --env-file .env fastapi-base:prod
```

### Considérations Spécifiques à l'Environnement
- Définir `DEBUG=False` en production
- Utiliser une `SECRET_KEY` appropriée
- Configurer `SENTRY_DSN` pour le suivi d'erreurs
- Définir des identifiants de base de données appropriés
- Utiliser Redis pour la gestion des sessions et la mise en cache

## 🏗️ Structure du Projet

```
fastapi-base/
├── fastapi-base/              # Répertoire principal de l'application
│   ├── src/                   # Code source
│   │   ├── core/              # Configuration et paramètres principaux
│   │   ├── models/            # Modèles de base de données
│   │   ├── api/               # Routes et endpoints API
│   │   ├── db/                # Utilitaires de base de données
│   │   ├── migrations/        # Migrations de base de données Alembic
│   │   └── main.py            # Point d'entrée de l'application
│   ├── tests/                 # Suite de tests
│   ├── pyproject.toml         # Dépendances Python et configuration des outils
│   └── Dockerfile             # Image Docker de développement
├── ops/                       # Opérations et déploiement
│   └── production.Dockerfile  # Image Docker de production
├── docs/                      # Documentation
├── docker-compose.yml         # Configuration de l'environnement de développement
├── Makefile                   # Commandes de développement
└── .env.example              # Template des variables d'environnement
```

## 🤝 Contribution

Nous accueillons les contributions ! Veuillez consulter nos [Directives de Contribution](../CONTRIBUTING.md) pour des informations détaillées sur :

- Configuration de votre environnement de développement
- Style de code et normes
- Exigences de tests
- Processus de pull request
- Code de conduite

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](../LICENSE) pour les détails.

## 🛠️ Construit Avec

- [FastAPI](https://fastapi.tiangolo.com/) - Framework web moderne et rapide
- [SQLModel](https://sqlmodel.tiangolo.com/) - Bases de données SQL en Python, conçu pour la simplicité
- [Alembic](https://alembic.sqlalchemy.org/) - Outil de migration de base de données
- [Celery](https://docs.celeryproject.org/) - File d'attente de tâches distribuée
- [Redis](https://redis.io/) - Magasin de structure de données en mémoire
- [PostgreSQL](https://www.postgresql.org/) - Base de données open source avancée
- [Docker](https://www.docker.com/) - Plateforme de conteneurisation
- [uv](https://docs.astral.sh/uv/) - Gestionnaire de paquets Python rapide

## 📚 Ressources Supplémentaires

- [Documentation FastAPI](https://fastapi.tiangolo.com/)
- [Documentation SQLModel](https://sqlmodel.tiangolo.com/)
- [Documentation Docker](https://docs.docker.com/)
- [Documentation PostgreSQL](https://www.postgresql.org/docs/)

## ⭐️ Support

Si vous avez trouvé ce projet utile, veuillez considérer :

- Lui donner une étoile ⭐️ sur GitHub
- Le partager avec vos collègues
- Contribuer à son développement
- Signaler des problèmes ou suggérer des améliorations

---

**Bon codage !** 🚀
