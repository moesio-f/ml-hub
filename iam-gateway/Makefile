all: down build up

build:
	@echo "Building Docker image..."
	docker build . -t ml-hub-iam-gateway:latest --rm --compress

down:
	@echo "Compose down"
	docker-compose -f docker-compose.yaml down

up:
	@echo "Compose up"
	docker-compose -f docker-compose.yaml up
