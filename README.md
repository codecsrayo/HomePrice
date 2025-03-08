# House Price Analysis Project

This project consists of a backend API built with FastAPI, a frontend built with Astro, and uses PostgreSQL for the database. The application uses Docker and Docker Compose for both development and production environments.

## Prerequisites

- Docker and Docker Compose
- Make

## Quick Start

```bash
# Install make if not installed
sudo apt install make

# Copy environment file
mv .devcontainer/.env.example .devcontainer/.env

# Start the application
make up
```

## Deployment

The project supports two deployment environments: development and production.

### Development Deployment

Development deployment uses self-signed certificates and is intended for local development.

```bash
# Set development environment in the Makefile
# DEVELOPMENT_ENVIRONMENT := true (default)

# Build and start containers
make build
make up

# View logs
make logs

# Stop containers
make down
```

### Production Deployment

Production deployment uses Let's Encrypt for SSL certificates and is intended for production use.

```bash
# Set production environment in the Makefile
# Edit the Makefile and set:
# DEVELOPMENT_ENVIRONMENT := false

# Build and start containers
make build
make up

# View logs
make logs

# Stop containers
make down
```

### Environment Configuration

Configure the deployment by editing `.devcontainer/.env`:

- `DOMAIN`: Set your domain (e.g., mydomain.com for production or dev.localhost for development)
  - Default for development: `dev.localhost`
- Database settings
- Other application settings

### Database Management

```bash
# Run database migrations
make migrate

# Check migration status
make migrate-status

# View pending migrations
make migrate-pending

# Access database shell
make shell-db
```

### Application Management

```bash
# Access application shell
make shell-app

# Restart services
make restart

# Clean up environment (removes volumes and containers)
make clean

# Start the application with migrations
make start-app

# Test services and HTTPS connectivity
make test
```

### Testing Services

The project includes a convenient command to test if all services are running properly and accessible via HTTPS:

```bash
make test
```

This command performs the following checks:

- Validates all running services (containers)
- Tests the database connection
- Verifies HTTPS connectivity to:
  - Frontend interface
  - Backend API
  - PGAdmin database management
- Checks the status of the Traefik proxy
- Provides a summary of running vs. expected services

The tests use the domain configured in your `.devcontainer/.env` file and include support for self-signed certificates.

## Project Structure

- `backend/`: FastAPI application
- `frontend/`: Astro frontend application
- `.devcontainer/`: Docker configuration files
  - `docker-compose.yaml`: Production Docker Compose configuration
  - `docker-compose.dev.yaml`: Development Docker Compose configuration
  - `Dockerfile.backend`: Backend container configuration
  - `Dockerfile.frontend`: Frontend container configuration

## Available Services

- Frontend: `https://{DOMAIN}/`
- Backend API: `https://{DOMAIN}/api/`
- PostgreSQL Database Management: `https://{DOMAIN}/db/`
- Traefik Dashboard (if enabled): `https://{DOMAIN}/dashboard/`