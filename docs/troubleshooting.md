# Troubleshooting Guide

This guide helps you resolve common issues when developing with or deploying the fastapi-base project.

## 🚨 Common Issues

### Docker and Container Issues

#### Container won't start
**Problem**: `docker compose up` fails or containers exit immediately.

**Solutions**:
1. **Check if ports are already in use**:
   ```bash
   # Check if port 8666 is already used
   lsof -i :8666
   # Check if port 5431 is already used  
   lsof -i :5431
   ```

2. **Check Docker resources**:
   ```bash
   # Clean up Docker resources
   docker system prune -f
   docker volume prune -f
   ```

3. **Check environment variables**:
   ```bash
   # Ensure .env file exists and is properly formatted
   cp .env.example .env
   ```

4. **View container logs**:
   ```bash
   docker compose logs fastapi-base
   docker compose logs db
   ```

#### Database connection issues
**Problem**: Application can't connect to PostgreSQL database.

**Solutions**:
1. **Check database container status**:
   ```bash
   docker compose ps db
   ```

2. **Check database logs**:
   ```bash
   docker compose logs db
   ```

3. **Verify environment variables**:
   ```bash
   # In .env file, ensure database settings match docker-compose.yml
   POSTGRES_HOST=db  # Not localhost when using Docker Compose
   POSTGRES_PORT=5432
   ```

4. **Test database connection**:
   ```bash
   # Connect to database directly
   docker compose exec db psql -U test -d test
   ```

### Migration Issues

#### Migration fails to create
**Problem**: `make alembic-make-migrations` fails or creates empty migration.

**Solutions**:
1. **Ensure models are imported**:
   ```python
   # In src/models/__init__.py, make sure all models are imported
   from .user import User
   from .other_model import OtherModel
   ```

2. **Check if database is running**:
   ```bash
   make up
   # Wait for database to be ready, then try again
   ```

3. **Verify model changes**:
   ```bash
   # Check that your model changes are significant enough to generate migration
   # Alembic may not detect minor changes like comment updates
   ```

#### Migration fails to apply
**Problem**: `make alembic-migrate` fails with database errors.

**Solutions**:
1. **Check migration file**:
   ```bash
   # Review the generated migration in fastapi-base/src/migrations/versions/
   ```

2. **Check database state**:
   ```bash
   # Check current migration version
   docker compose exec fastapi-base alembic current
   
   # Check migration history
   docker compose exec fastapi-base alembic history
   ```

3. **Reset database if needed** (⚠️ **Development only**):
   ```bash
   make alembic-reset
   make alembic-init
   make alembic-migrate
   ```

### Testing Issues

#### Tests fail to run
**Problem**: `make test` command fails.

**Solutions**:
1. **Ensure containers are running**:
   ```bash
   make up
   ```

2. **Check test database connection**:
   ```bash
   # Tests should use a separate test database
   # Check conftest.py for test database setup
   ```

3. **Run tests individually**:
   ```bash
   # Run specific test file to isolate issues
   docker compose exec fastapi-base pytest tests/test_api/test_users.py -v
   ```

### Code Quality Issues

#### Pre-commit hooks fail
**Problem**: `make precommit-run` fails with linting or formatting errors.

**Solutions**:
1. **Fix formatting issues**:
   ```bash
   make black    # Format code
   make isort    # Sort imports
   ```

2. **Fix linting issues**:
   ```bash
   make lint     # Check for issues
   # Review and fix the reported issues
   ```

3. **Fix type checking issues**:
   ```bash
   make mypy     # Type checking
   # Add missing type hints or fix type errors
   ```

### Performance Issues

#### Slow API responses
**Problem**: API endpoints are responding slowly.

**Solutions**:
1. **Check database queries**:
   ```bash
   # Enable query logging in development
   # In src/core/config.py, set appropriate log level
   ```

2. **Monitor Redis performance**:
   ```bash
   # Connect to Redis and check performance
   docker compose exec redis redis-cli
   > INFO stats
   ```

3. **Check resource usage**:
   ```bash
   # Monitor container resource usage
   docker stats
   ```

#### High memory usage
**Problem**: Containers consuming too much memory.

**Solutions**:
1. **Check for memory leaks**:
   ```bash
   # Monitor memory usage over time
   docker stats --no-stream
   ```

2. **Optimize database connections**:
   ```python
   # In src/core/config.py, adjust connection pool settings
   POOL_SIZE = 5  # Reduce if needed
   MAX_OVERFLOW = 10  # Reduce if needed
   ```

## 🔧 Development Environment Issues

### Local Development Setup

#### uv sync fails
**Problem**: Python dependencies can't be installed.

**Solutions**:
1. **Update uv**:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clear cache**:
   ```bash
   uv cache clean
   ```

3. **Check Python version**:
   ```bash
   python --version  # Should be 3.13+
   ```

#### Pre-commit installation fails
**Problem**: `make hooks` fails to install pre-commit hooks.

**Solutions**:
1. **Install pre-commit globally**:
   ```bash
   # Using uv
   uvx install pre-commit
   
   # Or using pip
   pip install pre-commit
   ```

2. **Install hooks manually**:
   ```bash
   cd /home/runner/work/fastapi-base/fastapi-base
   pre-commit install
   ```

### Environment Variable Issues

#### Missing environment variables
**Problem**: Application fails to start due to missing environment variables.

**Solutions**:
1. **Copy example file**:
   ```bash
   cp .env.example .env
   ```

2. **Check required variables**:
   ```bash
   # Ensure these are set in .env:
   SECRET_KEY=your-secret-key-here
   POSTGRES_USER=test
   POSTGRES_PASSWORD=test
   POSTGRES_DB=test
   ```

3. **Validate environment variables**:
   ```bash
   # Check if environment variables are loaded
   docker compose exec fastapi-base env | grep POSTGRES
   ```

## 🚀 Production Deployment Issues

### Docker Build Issues

#### Production build fails
**Problem**: `docker build -f ops/production.Dockerfile` fails.

**Solutions**:
1. **Check Docker version**:
   ```bash
   docker --version  # Ensure recent version
   ```

2. **Clear build cache**:
   ```bash
   docker builder prune -f
   ```

3. **Build with verbose output**:
   ```bash
   docker build -f ops/production.Dockerfile -t fastapi-base:prod . --no-cache --progress=plain
   ```

### Database Issues in Production

#### Connection timeouts
**Problem**: Database connections timeout in production.

**Solutions**:
1. **Check connection limits**:
   ```sql
   -- Connect to database and check current connections
   SELECT count(*) FROM pg_stat_activity;
   SHOW max_connections;
   ```

2. **Optimize connection pool**:
   ```python
   # In src/core/config.py
   POOL_SIZE = 20  # Adjust based on your needs
   MAX_OVERFLOW = 40
   ```

### SSL/TLS Issues

#### Certificate issues
**Problem**: HTTPS certificate problems in production.

**Solutions**:
1. **Check certificate validity**:
   ```bash
   openssl x509 -in your-cert.pem -text -noout
   ```

2. **Verify certificate chain**:
   ```bash
   openssl verify -CAfile ca-cert.pem your-cert.pem
   ```

## 📊 Monitoring and Debugging

### Log Analysis

#### Application logs
**Problem**: Need to analyze application behavior.

**Solutions**:
1. **View real-time logs**:
   ```bash
   # Development
   docker compose logs -f fastapi-base
   
   # Production
   docker logs -f <container-id>
   ```

2. **Search logs**:
   ```bash
   # Search for specific errors
   docker compose logs fastapi-base | grep ERROR
   
   # Search for API calls
   docker compose logs fastapi-base | grep "GET /api"
   ```

### Database Debugging

#### Query performance
**Problem**: Need to debug slow database queries.

**Solutions**:
1. **Enable query logging**:
   ```sql
   -- In PostgreSQL, enable query logging
   ALTER SYSTEM SET log_statement = 'all';
   SELECT pg_reload_conf();
   ```

2. **Analyze slow queries**:
   ```sql
   -- Check for slow queries
   SELECT query, calls, total_time, mean_time
   FROM pg_stat_statements
   ORDER BY total_time DESC
   LIMIT 10;
   ```

### API Debugging

#### Request debugging
**Problem**: Need to debug API requests and responses.

**Solutions**:
1. **Use curl for testing**:
   ```bash
   # Test API endpoints
   curl -X GET "http://localhost:8666/v1/ping" -H "accept: application/json"
   ```

2. **Use HTTPie**:
   ```bash
   # More user-friendly HTTP client
   http GET localhost:8666/v1/ping
   ```

3. **Check API documentation**:
   ```bash
   # Access interactive docs
   open http://localhost:8666/docs
   ```

## 🆘 Getting Help

If none of these solutions work:

1. **Search existing issues**: Check [GitHub Issues](https://github.com/GabrielVGS/fastapi-base/issues)
2. **Create detailed bug report**: Use our [Bug Report Template](../.github/ISSUE_TEMPLATE/bug_report.md)
3. **Join discussions**: Check [GitHub Discussions](https://github.com/GabrielVGS/fastapi-base/discussions) if available
4. **Contact maintainers**: See [CONTRIBUTING.md](../CONTRIBUTING.md) for contact information

### Information to Include in Bug Reports

When reporting issues, please include:
- Operating system and version
- Docker and Docker Compose versions
- Python version (for local development)
- Exact error messages and stack traces
- Steps to reproduce the issue
- Environment variables (remove sensitive data)
- Output of `docker compose ps` and `docker compose logs`

This will help maintainers diagnose and resolve issues more quickly.