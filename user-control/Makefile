all: down build up

build:
	@echo "Building Docker image..."
	@echo "Step 1: create fat Jar"
	mvn clean install
	@echo "Step 2: create Docker Image"
	docker build . -t ml-hub-user-control:latest --rm --compress

mariadb:
	@echo "Starting MariaDB..."
	docker-compose -f docker-compose.yaml up --no-deps mariadb

down:
	@echo "Compose down"
	docker-compose -f docker-compose.yaml down

up:
	@echo "Compose up"
	docker-compose -f docker-compose.yaml up
