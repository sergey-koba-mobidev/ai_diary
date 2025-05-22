# Define variables
DOCKER = docker
DOCKER_COMPOSE = docker-compose
API_RUNNER = docker-compose run --rm langchain-api

# Containers
API_CONTAINER_NAME = $(shell docker ps | grep api | rev | cut -d' ' -f1 | rev)

# Default target
all: setup

##@ General setup
.PHONY: setup
setup: ## Build Docker containers
	cp .env.example .env
	$(DOCKER_COMPOSE) build
	$(DOCKER_COMPOSE) up -d

.PHONY: licenses
licenses: ## Generate LICENSE-DEPENDENCIES.md file
	$(API_RUNNER) pip-licenses --format=markdown > LICENSE-DEPENDENCIES.md

##@ Everyday usage

.PHONY: start
start: ## Start all Docker containers
	$(DOCKER_COMPOSE) up -d

.PHONY: stop
stop: ## Stop all Docker containers
	$(DOCKER_COMPOSE) stop

.PHONY: restart
restart: ## Stop all Docker containers
	$(MAKE) stop
	$(MAKE) start

.PHONY: clean
clean: ## Stop and remove Docker containers
	$(DOCKER_COMPOSE) down
	$(DOCKER_COMPOSE) rm -f

##@ API related

.PHONY: pipinstall
pipinstall: ## Install python requirements
	$(API_RUNNER) pip install --no-cache-dir --upgrade -r /app/requirements.txt

.PHONY: api-console
api-console:
	$(API_RUNNER) /bin/bash

.PHONY: invoke-llm
invoke-llm:
	$(API_RUNNER) python cli.py invoke-llm "${QUERY}"

.PHONY: alembic-revision
alembic-revision:
	$(API_RUNNER) alembic revision --autogenerate -m "${M}"

.PHONY: alembic-upgrade
alembic-upgrade:
	$(API_RUNNER) alembic upgrade head

.PHONY: import-diary-file
import-diary-file:
	$(API_RUNNER) python cli.py import-diary-file "${FILE}"

.PHONY: get-llm-responses
get-llm-responses:
	$(API_RUNNER) python cli.py get-llm-responses


.PHONY: help
help: ## Show list of commands
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'
