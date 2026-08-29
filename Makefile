# NovaCommerce Platform Makefile

.PHONY: all build start test clean lint docker-up docker-down help

all: build test

build:
	npm run build --workspaces --if-present

start:
	npm run start --workspaces --if-present

dev:
	npm run dev --workspaces --if-present

test:
	npm run test --workspaces --if-present

lint:
	npm run lint --workspaces --if-present

clean:
	rm -rf dist build coverage *.log

docker-up:
	docker compose -f docker/docker-compose.yaml up -d

docker-down:
	docker compose -f docker/docker-compose.yaml down

help:
	@echo "NovaCommerce Platform Commands:"
	@echo "  make build       - Build all packages and microservices"
	@echo "  make start       - Start all microservices in production mode"
	@echo "  make dev         - Start all microservices in development mode"
	@echo "  make test        - Run comprehensive test matrix"
	@echo "  make docker-up   - Launch infrastructure containers"
	@echo "  make docker-down - Stop infrastructure containers"
