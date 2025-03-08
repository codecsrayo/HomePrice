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
		mkcert 'dev.localhost' && \
		mv dev.localhost*.pem .devcontainer/configuration/tls/ && \
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
	@rm -rf .devcontainer/configuration/*
	@docker system prune -a
	@echo "Services and volumes removed"

# Start application
.PHONY: start-app

start-app:
	@$(DOCKER_COMPOSE) exec $(APP_SERVICE) sh -c "alembic upgrade head && uvicorn main:app --reload --host 0.0.0.0 --port 8000"

# Test services
.PHONY: test

test:
	@echo "\033[1;34mVerificando estado de los servicios...\033[0m"
	@if [ -z "$$(grep -oP '^DOMAIN=\K[^ ]*' .devcontainer/.env)" ]; then \
		echo "\033[1;31m❌ No se encontró la variable DOMAIN en .env\033[0m"; \
		exit 1; \
	fi
	@export DOMAIN=$$(grep -oP '^DOMAIN=\K[^ ]*' .devcontainer/.env) && \
	echo "\033[1;33mDominio configurado: $$DOMAIN\033[0m"
	@echo "\n\033[1;33m=== Servicios en ejecución ===\033[0m"
	@docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
	@echo "\n\033[1;33m=== Verificando conexión a la base de datos ===\033[0m"
	@if docker ps | grep -q $(DB_SERVICE); then \
		$(DOCKER_COMPOSE) exec $(DB_SERVICE) pg_isready -h localhost -U postgres && \
		echo "\033[1;32m✅ Base de datos operativa\033[0m"; \
	else \
		echo "\033[1;31m❌ El servicio de base de datos no está en ejecución\033[0m"; \
	fi
	@echo "\n\033[1;33m=== Verificando HTTPS ===\033[0m"
	@export DOMAIN=$$(grep -oP '^DOMAIN=\K[^ ]*' .devcontainer/.env) && \
	echo "\033[1;33mVerificando Frontend (https://$$DOMAIN/)\033[0m" && \
	if curl -s -k -I "https://$$DOMAIN/" | grep -q "HTTP/\(1.1\|2\) \(200\|301\|302\|307\|308\)"; then \
		echo "\033[1;32m✅ Frontend HTTPS operativo\033[0m"; \
	else \
		echo "\033[1;31m❌ Frontend HTTPS no responde\033[0m"; \
	fi && \
	echo "\033[1;33mVerificando API Backend (https://$$DOMAIN/api/docs)\033[0m" && \
	if curl -s -k -I "https://$$DOMAIN/api/docs" | grep -q "HTTP/\(1.1\|2\) \(200\|301\|302\|307\|308\)"; then \
		echo "\033[1;32m✅ API Backend HTTPS operativa\033[0m"; \
	else \
		echo "\033[1;31m❌ API Backend HTTPS no responde\033[0m"; \
	fi && \
	echo "\033[1;33mVerificando PGAdmin (https://$$DOMAIN/db/)\033[0m" && \
	if curl -s -k -I "https://$$DOMAIN/db/" | grep -q "HTTP/\(1.1\|2\) \(200\|301\|302\|307\|308\)"; then \
		echo "\033[1;32m✅ PGAdmin HTTPS operativo\033[0m"; \
	else \
		echo "\033[1;31m❌ PGAdmin HTTPS no responde\033[0m"; \
	fi
	@echo "\n\033[1;33m=== Verificando servicios internos ===\033[0m"
	@if docker ps | grep -q traefik; then \
		echo "\033[1;32m✅ Servicio Traefik en ejecución\033[0m"; \
	else \
		echo "\033[1;31m❌ El servicio de Traefik no está en ejecución\033[0m"; \
	fi
	@echo "\n\033[1;33m=== Resumen de servicios ===\033[0m"
	@echo "Servicios en ejecución: $$(docker ps --format "{{.Names}}" | wc -l)"
	@echo "Servicios esperados: 5 (db, backend, frontend, traefik, pgadmin)"
	@echo "\n\033[1;34mConsejo: Si utilizas certificados autofirmados, asegúrate de que estén instalados en tu navegador\033[0m"

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
	@echo "  test          - Test if services are running properly"
	@echo "  help          - Show this help message"