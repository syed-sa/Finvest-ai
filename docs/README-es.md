# Proyecto Base FastAPI

<p align="center">
  <a href="../README.md">🇺🇸 English</a> |
  <a href="README-pt.md">🇧🇷 Português</a> |
  <a href="README-fr.md">🇫🇷 Français</a>
</p>

<p align="center">
    <a href="https://github.com/GabrielVGS/fastapi-base/actions">
        <img alt="Estado de GitHub Actions" src="https://github.com/GabrielVGS/fastapi-base/actions/workflows/main.yml/badge.svg">
    </a>
    <a href="https://codecov.io/gh/GabrielVGS/fastapi-base">
     <img src="https://codecov.io/gh/GabrielVGS/fastapi-base/branch/main/graph/badge.svg?token=899NB4AK7J"/>
    </a>
    <a href="https://github.com/GabrielVGS/fastapi-base/releases">
        <img alt="Estado de Versión" src="https://img.shields.io/github/v/release/GabrielVGS/fastapi-base">
    </a>
</p>

Una plantilla backend FastAPI moderna y lista para producción con mejores prácticas, soporte Docker y herramientas integrales para desarrollo rápido.

## 🏗️ Plantilla del Proyecto

Este proyecto fue creado usando la excelente plantilla [cookiecutter-fastapi-backend](https://github.com/nickatnight/cookiecutter-fastapi-backend) por [@nickatnight](https://github.com/nickatnight), que proporciona una base sólida para aplicaciones FastAPI con mejores prácticas y herramientas modernas.

## 📚 Documentación

- [Arquitectura](architecture.md) - Resumen de la arquitectura del sistema
- [Guía de Desarrollo](developing.md) - Directrices de desarrollo local
- [Guía de Contribución](../CONTRIBUTING.md) - Cómo contribuir a este proyecto

## ✨ Características

- **FastAPI** - Framework web moderno y rápido para construir APIs
- **Docker** - Desarrollo y despliegue containerizado
- **PostgreSQL** - Base de datos relacional robusta con soporte asíncrono
- **Redis** - Caché y gestión de sesiones
- **Celery** - Procesamiento de tareas en segundo plano
- **Alembic** - Gestión de migraciones de base de datos
- **Pruebas** - Suite de pruebas completa con pytest
- **Calidad de Código** - Hooks pre-commit, linting y formateo
- **Seguridad de Tipos** - Anotaciones de tipo completas con validación mypy
- **Documentación** - Documentación API auto-generada con Swagger UI

## 🚀 Inicio Rápido

### Requisitos Previos

- Docker y Docker Compose
- Python 3.13+ (para desarrollo local)
- Gestor de paquetes [uv](https://docs.astral.sh/uv/)

### Ejecutar con Docker (Recomendado)

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/GabrielVGS/fastapi-base.git
   cd fastapi-base
   ```

2. **Copiar variables de entorno**:
   ```bash
   cp .env.example .env
   ```

3. **Iniciar los servicios**:
   ```bash
   make up
   ```

4. **Acceder a la aplicación**:
   - API: `http://localhost:8666/v1/`
   - Verificación de salud: `http://localhost:8666/v1/ping`
   - Documentación interactiva: `http://localhost:8666/docs`
   - Documentación alternativa: `http://localhost:8666/redoc`

## 🛠️ Desarrollo Local

### Configuración del Entorno Local

1. **Instalar uv** (si no está ya instalado):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Navegar al directorio del proyecto**:
   ```bash
   cd fastapi-base/
   ```

3. **Instalar dependencias**:
   ```bash
   uv sync
   ```

4. **Instalar hooks pre-commit**:
   ```bash
   make hooks
   ```

### Migraciones de Base de Datos

Inicializar la primera migración (el proyecto debe estar ejecutándose con `docker compose up` y no contener archivos 'version'):
```bash
make alembic-init
```

Crear nuevo archivo de migración:
```bash
make alembic-make-migrations "describe sus cambios"
```

Aplicar migraciones:
```bash
make alembic-migrate
```

### Flujo de Trabajo de Migraciones

Después de cada migración, puede crear nuevas migraciones y aplicarlas con:
```bash
make alembic-make-migrations "describe sus cambios"
make alembic-migrate
```

## 📋 Variables de Entorno

Cree un archivo `.env` basado en `.env.example`:

### Configuración de Aplicación
- `PROJECT_NAME` - Nombre del proyecto (por defecto: fastapi-base)
- `VERSION` - Versión de la API (por defecto: v1)
- `DEBUG` - Habilitar modo debug (por defecto: True)
- `SECRET_KEY` - Clave secreta para JWT y encriptación
- `ENV` - Entorno (dev/staging/production)

### Configuración de Base de Datos
- `POSTGRES_USER` - Nombre de usuario PostgreSQL
- `POSTGRES_PASSWORD` - Contraseña PostgreSQL
- `POSTGRES_DB` - Nombre de la base de datos
- `POSTGRES_HOST` - Host de la base de datos (por defecto: localhost)
- `POSTGRES_PORT` - Puerto de la base de datos (por defecto: 5432)
- `POSTGRES_URL` - URL completa de la base de datos (opcional, auto-generada si no se proporciona)

### Configuración Redis
- `REDIS_HOST` - Host Redis (por defecto: redis)
- `REDIS_PORT` - Puerto Redis (por defecto: 6379)
- `REDIS_URL` - URL completa Redis (opcional, auto-generada si no se proporciona)

### Configuraciones Opcionales
- `SENTRY_DSN` - DSN de seguimiento de errores Sentry
- `LOG_LEVEL` - Nivel de logging (por defecto: INFO)
- `CACHE_TTL` - Tiempo de vida del caché en segundos (por defecto: 60)

## 🏃 Ejecutar la Aplicación

### Usando Docker Compose (Recomendado)

```bash
# Construir e iniciar todos los servicios
make build

# Iniciar servicios (sin construcción)
make up

# Detener servicios
make down

# Acceder al bash del contenedor
make bash
```

### Desarrollo Local (sin Docker)

```bash
# Asegurar que PostgreSQL y Redis estén ejecutándose localmente
# Actualizar .env con conexiones locales de base de datos/redis

# Ejecutar la aplicación FastAPI
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## 🔧 Flujo de Trabajo de Desarrollo

Consulte el [Makefile](../Makefile) para ver todos los comandos disponibles.

### Comandos Make Disponibles

```bash
# Desarrollo
make up          # Iniciar todos los servicios con Docker Compose
make down        # Detener todos los servicios
make build       # Construir e iniciar servicios
make bash        # Acceder al shell del contenedor principal

# Base de Datos
make alembic-init              # Inicializar primera migración
make alembic-make-migrations   # Crear nueva migración
make alembic-migrate          # Aplicar migraciones
make alembic-reset            # Reiniciar base de datos
make init-db                  # Inicializar base de datos con datos de ejemplo

# Calidad de Código
make test           # Ejecutar suite de pruebas con cobertura
make lint           # Ejecutar linter ruff
make black          # Formatear código con black
make isort          # Ordenar imports
make mypy           # Verificación de tipos
make precommit-run  # Ejecutar todos los hooks pre-commit

# Mantenimiento
make hooks          # Instalar hooks pre-commit
```

### Dependencias

Por defecto, las dependencias se gestionan con [uv](https://docs.astral.sh/uv/). Por favor visite el enlace e instálelo.

Desde `./fastapi-base/` puede instalar todas las dependencias con:
```bash
uv sync
```

### Hooks Pre-commit

El proyecto usa hooks pre-commit para asegurar la calidad del código. Instálelos con:
```bash
make hooks
```

Esto instalará hooks que se ejecutan automáticamente antes de cada commit para:
- Formatear código con `black`
- Ordenar imports con `isort`
- Analizar código con `ruff`
- Verificar tipos con `mypy`
- Ejecutar pruebas

## 🧪 Pruebas

Ejecutar la suite completa de pruebas:
```bash
make test
```

Ejecutar pruebas específicas:
```bash
# Dentro del contenedor
docker compose exec fastapi-base pytest tests/test_specific.py

# Localmente (si las dependencias están instaladas)
uv run pytest tests/test_specific.py
```

## 🚀 Despliegue en Producción

El proyecto incluye configuraciones Docker listas para producción:

### Usando Dockerfile de Producción
```bash
# Construir imagen de producción
docker build -f ops/production.Dockerfile -t fastapi-base:prod .

# Ejecutar contenedor de producción
docker run -p 8000:8000 --env-file .env fastapi-base:prod
```

### Consideraciones Específicas del Entorno
- Establecer `DEBUG=False` en producción
- Usar `SECRET_KEY` apropiada
- Configurar `SENTRY_DSN` para seguimiento de errores
- Establecer credenciales apropiadas de base de datos
- Usar Redis para gestión de sesiones y caché

## 🏗️ Estructura del Proyecto

```
fastapi-base/
├── fastapi-base/              # Directorio principal de la aplicación
│   ├── src/                   # Código fuente
│   │   ├── core/              # Configuración y ajustes principales
│   │   ├── models/            # Modelos de base de datos
│   │   ├── api/               # Rutas y endpoints API
│   │   ├── db/                # Utilidades de base de datos
│   │   ├── migrations/        # Migraciones de base de datos Alembic
│   │   └── main.py            # Punto de entrada de la aplicación
│   ├── tests/                 # Suite de pruebas
│   ├── pyproject.toml         # Dependencias Python y configuración de herramientas
│   └── Dockerfile             # Imagen Docker de desarrollo
├── ops/                       # Operaciones y despliegue
│   └── production.Dockerfile  # Imagen Docker de producción
├── docs/                      # Documentación
├── docker-compose.yml         # Configuración del entorno de desarrollo
├── Makefile                   # Comandos de desarrollo
└── .env.example              # Plantilla de variables de entorno
```

## 🤝 Contribuir

¡Damos la bienvenida a las contribuciones! Por favor consulte nuestras [Directrices de Contribución](../CONTRIBUTING.md) para información detallada sobre:

- Configurar su entorno de desarrollo
- Estilo de código y estándares
- Requisitos de pruebas
- Proceso de pull request
- Código de conducta

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - vea el archivo [LICENSE](../LICENSE) para detalles.

## 🛠️ Construido Con

- [FastAPI](https://fastapi.tiangolo.com/) - Framework web moderno y rápido
- [SQLModel](https://sqlmodel.tiangolo.com/) - Bases de datos SQL en Python, diseñado para simplicidad
- [Alembic](https://alembic.sqlalchemy.org/) - Herramienta de migración de base de datos
- [Celery](https://docs.celeryproject.org/) - Cola de tareas distribuida
- [Redis](https://redis.io/) - Almacén de estructura de datos en memoria
- [PostgreSQL](https://www.postgresql.org/) - Base de datos avanzada de código abierto
- [Docker](https://www.docker.com/) - Plataforma de containerización
- [uv](https://docs.astral.sh/uv/) - Gestor de paquetes Python rápido

## 📚 Recursos Adicionales

- [Documentación FastAPI](https://fastapi.tiangolo.com/)
- [Documentación SQLModel](https://sqlmodel.tiangolo.com/)
- [Documentación Docker](https://docs.docker.com/)
- [Documentación PostgreSQL](https://www.postgresql.org/docs/)

## ⭐️ Soporte

Si encontró útil este proyecto, por favor considere:

- Darle una estrella ⭐️ en GitHub
- Compartirlo con sus colegas
- Contribuir a su desarrollo
- Reportar problemas o sugerir mejoras

---

**¡Feliz codificación!** 🚀