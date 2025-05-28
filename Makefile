VERSION := $(shell sed -n 's/^version = "\(.*\)"/\1/p' pyproject.toml)
IMAGE_NAME := palindrome
TAG := $(IMAGE_NAME):v$(VERSION)

install-dependencies:
	pip3 install .

build-image:
	echo "Building the Docker image based on the version from pyproject.toml."
	docker build -t $(TAG) .

setup: install-dependencies build-image

create-env-file:
	@if [ -f .env ]; then \
	    echo "Error: The file already exist."; \
	    exit 1; \
	fi
	echo "POSTGRES_USER=palindrome_user" >> .env; \
    echo "POSTGRES_PASSWORD=$$(openssl rand -hex 16)" >> .env; \
    echo "POSTGRES_DB=detections" >> .env; \
    echo "File created successfully"

up-production:
	docker compose -f docker-compose.prod.yml up -d

down-production:
	docker compose -f docker-compose.prod.yml down -v

enable-production: down-production up-production

up-test-db:
	docker compose -f ./docker-compose.test.yml up -d

down-test-db:
	docker compose -f ./docker-compose.test.yml down -v

reset-db:
	@PGPASSWORD=password psql -h localhost -p 5433 -U user -d detections -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

test:
	pytest --cov=app tests/

wait-for-db:
	@echo "Waiting availability of PostgreSQL."
	@until docker exec test-db pg_isready -U user -d detections > /dev/null 2>&1; do \
		sleep 1; \
	done
	@echo "PostgreSQL ready."

test-all: up-test-db wait-for-db reset-db test down-test-db