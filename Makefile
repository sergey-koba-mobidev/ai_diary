# Define variables
DOCKER = docker
DOCKER_COMPOSE = docker-compose
API_RUNNER = docker-compose run --rm langchain-api

# Containers
OLLAMA_CONTAINER_NAME = $(shell docker ps | grep ollama | rev | cut -d' ' -f1 | rev)

# Default target
all: setup

##@ General setup
.PHONY: setup
setup: ## Build Docker containers
	cp .env.example .env
	$(DOCKER_COMPOSE) build
	$(DOCKER_COMPOSE) up -d
	$(MAKE) setup-ollama

.PHONY: setup-ollama
setup-ollama: ## Install llama3 model
# Need OLLAMA_CONTAINER_NAME because container name can vary due to Docker version
	@echo "Downloading LLM model may take several minutes. Please wait..."
	@sleep 20
	$(DOCKER) exec -ti $(OLLAMA_CONTAINER_NAME) ollama pull nomic-embed-text
	$(DOCKER) exec -ti $(OLLAMA_CONTAINER_NAME) ollama pull deepseek-r1:1.5b

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

.PHONY: invoke-llm
invoke-llm:
	$(API_RUNNER) python cli.py invoke-llm "${QUERY}"

.PHONY: help
help: ## Show list of commands
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'
