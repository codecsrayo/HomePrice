# Makefile for Development Environment

# Environment variables
DEVELOPMENT_ENVIRONMENT := true
COMPOSE_FILE_PROD := .devcontainer/docker-compose.yaml
COMPOSE_FILE_DEV := .devcontainer/docker-compose.dev.yaml

# Determine the environment (production or development)
ifeq ($(DEVELOPMENT_ENVIRONMENT),true)
    ENV := DEV
else
    ENV := PROD
endif

# Set the appropriate Docker Compose file
DOCKER_COMPOSE := docker compose -f $(COMPOSE_FILE_$(ENV))

# Service names
DB_SERVICE := db
APP_SERVICE := backend

# Default target
.PHONY: all
all: setup validate-certs

# Setup target
.PHONY: setup
setup:
	@echo "Setting up development environment..."
	@if [ ! -f .devcontainer/.env ]; then \
		cd .devcontainer && cp .env.example .env; \
		echo ".env file created from .env.example"; \
	else \
		echo ".env file already exists"; \
	fi


.PHONY: validate-certs
validate-certs:
	@if [ "$(ENV)" != "DEV" ]; then \
		echo "Entorno de producción saltando la generación de certificados autofirmados.."; \
		exit 1; \
	fi
	@mkdir -p .devcontainer/configuration/tls/
	@echo 'tls:\n  stores:\n    default:\n      defaultCertificate:\n        certFile: .devcontainer/configuration/tls/dev.localhost.pem\n        keyFile: .devcontainer/configuration/tls/dev.localhost-key.pem' > .devcontainer/configuration/certificates.yml
	@if [ ! -f ".devcontainer/configuration/tls/dev.localhost.pem" ]; then \
		wget https://github.com/FiloSottile/mkcert/releases/download/v1.4.4/mkcert-v1.4.4-linux-amd64 && \
		sudo mv mkcert-v1.4.4-linux-amd64 /usr/bin/mkcert && \
		sudo chmod +x /usr/bin/mkcert && \
		mkcert -install && \
		cd .devcontainer/configuration/tls/ && \
		mkcert 'dev.localhost' && \
		chmod 600 .devcontainer/configuration/tls/dev.localhost*; \
	else \
		echo "Certificados TLS ya existen. Saltando creación."; \
	fi


# Docker Compose commands
.PHONY: up down restart build logs

up:
	@$(MAKE) all
	@$(DOCKER_COMPOSE) up -d
	@echo "Services started in $(ENV)"

down:
	@$(MAKE) all
	@$(DOCKER_COMPOSE) down
	@echo "Services stopped in $(ENV)"

restart:
	@$(MAKE) all
	@$(DOCKER_COMPOSE) down
	@$(DOCKER_COMPOSE) up -d
	@echo "Services restarted in $(ENV)"

build:
	@$(MAKE) all
	@$(DOCKER_COMPOSE) build
	@echo "Images rebuilt"

logs:
	@$(MAKE) all
	@$(DOCKER_COMPOSE) logs -f $(APP_SERVICE)

# Database and migration commands
.PHONY: migrate migrate-status migrate-pending

migrate:
	@$(MAKE) all
	@$(DOCKER_COMPOSE) exec $(APP_SERVICE) alembic upgrade head
	@echo "Migrations executed"

migrate-status:
	@$(MAKE) all
	@$(DOCKER_COMPOSE) exec $(APP_SERVICE) alembic current
	@echo "Migration status"

migrate-pending:
	@$(MAKE) all
	@$(DOCKER_COMPOSE) exec $(APP_SERVICE) alembic history --verbose
	@echo "Pending migrations"

# Shell access
.PHONY: shell-app shell-db

shell-app:
	@$(MAKE) all
	@$(DOCKER_COMPOSE) exec $(APP_SERVICE) sh

shell-db:
	@$(MAKE) all
	@$(DOCKER_COMPOSE) exec $(DB_SERVICE) sh

# Clean environment
.PHONY: clean

clean:
	@$(MAKE) all
	@$(DOCKER_COMPOSE) down -v
	@echo "Services and volumes removed"

# Start application
.PHONY: start-app

start-app:
	@$(DOCKER_COMPOSE) exec $(APP_SERVICE) sh -c "alembic upgrade head && uvicorn main:app --reload --host 0.0.0.0 --port 8000"



# Help target
.PHONY: help

help:
	@echo "Available targets:"
	@echo "  setup         - Set up the development environment"
	@echo "  up            - Start the Docker containers"
	@echo "  down          - Stop the Docker containers"
	@echo "  restart       - Restart the Docker containers"
	@echo "  build         - Build the Docker images"
	@echo "  logs          - View container logs"
	@echo "  migrate       - Run database migrations"
	@echo "  migrate-status- Check the status of migrations"
	@echo "  migrate-pending- View pending migrations"
	@echo "  shell-app     - Open a shell in the app container"
	@echo "  shell-db      - Open a shell in the database container"
	@echo "  clean         - Remove all services and volumes"
	@echo "  start-app     - Apply migrations and start the server"
	@echo "  help          - Show this help message"