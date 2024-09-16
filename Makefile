#bin/bash
# Variables
COMPOSE_FILE = ".devcontainer/docker-compose.yaml"
DOCKER_COMPOSE =  docker compose -f $(COMPOSE_FILE)
DB_SERVICE = db
APP_SERVICE = backend



# Comandos básicos para Docker Compose
up:
	@$(DOCKER_COMPOSE) up -d
	@echo "Servicios levantados"

down:
	@$(DOCKER_COMPOSE) down
	@echo "Servicios detenidos"

restart:
	@$(DOCKER_COMPOSE) down
	@$(DOCKER_COMPOSE) up -d
	@echo "Servicios reiniciados"

logs:
	@$(DOCKER_COMPOSE) logs -f $(APP_SERVICE)

# Ejecutar migraciones Alembic
migrate:
	@$(DOCKER_COMPOSE) exec $(APP_SERVICE) alembic upgrade head
	@echo "Migraciones ejecutadas"

# Ver el estado de las migraciones
migrate-status:
	@$(DOCKER_COMPOSE) exec $(APP_SERVICE) alembic current
	@echo "Estado de las migraciones"

# Construir la imagen nuevamente
build:
	@$(DOCKER_COMPOSE) build
	@echo "Imágenes reconstruidas"

# Abrir una shell en el contenedor de la aplicación
shell-app:
	@$(DOCKER_COMPOSE) exec $(APP_SERVICE) sh

# Abrir una shell en el contenedor de la base de datos
shell-db:
	@$(DOCKER_COMPOSE) exec $(DB_SERVICE) sh

# Ver las migraciones pendientes
migrate-pending:
	@$(DOCKER_COMPOSE) exec $(APP_SERVICE) alembic history --verbose
	@echo "Migraciones pendientes"

# Eliminar todos los volúmenes y limpiar el entorno
clean:
	@$(DOCKER_COMPOSE) down -v
	@echo "Servicios y volúmenes eliminados"

# Aplicar las migraciones y levantar el servidor
start-app:
	@$(DOCKER_COMPOSE) exec $(APP_SERVICE) sh -c "alembic upgrade head && uvicorn main:app --reload --host 0.0.0.0 --port 8000"
