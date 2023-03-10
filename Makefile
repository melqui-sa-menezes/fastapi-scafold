export PYTHONPATH=$(shell pwd)
export PYTHONDONTWRITEBYTECODE=1

.PHONY=help

help:  ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

build: ## Build project and apply migrations
	docker compose build
	docker compose up -d
	docker exec -it backend_api bash -c "alembic -x data=true upgrade head"
	docker compose stop

run: ## Up all containers and run app
	docker compose up

stop: ## Stop all containers
	docker compose stop

down: ## Remove all containers
	docker compose down

migration: ## Generate database migration
	docker compose up -d
	docker exec -it backend_api bash -c "alembic revision --autogenerate -m '${msg}'"
	docker compose stop

migrate: ## Apply alembic migrations
	docker compose up -d
	docker exec -it backend_api bash -c "alembic -x data=true upgrade head"
	docker compose stop

db:
	docker compose up db -d