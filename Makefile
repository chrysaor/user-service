clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete

install:
	pip install -r requirements.txt

run:
	./scripts/start_server.sh

all: clean install run

user-service-dev:
	docker build -f ./build/docker/dev/Dockerfile -t user-service .

user-service-prod:
	docker build -f ./build/docker/prod/Dockerfile -t user-service .

docker-run:
	docker-compose -f build/docker-compose.yml up -d

docker-stop:
	docker-compose -f build/docker-compose.yml down
