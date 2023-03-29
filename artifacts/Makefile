all: down build up

build:
	@echo "Building Docker image..."
	@echo "Step 1: create fat Jar"
	mvn clean install
	@echo "Step 2: create Docker Image"
	docker build . -t ml-hub-artifacts:latest --rm --compress

down:
	@echo "Compose down"
	docker-compose -f docker-compose.yaml down

up:
	@echo "Compose up"
	docker-compose -f docker-compose.yaml up
