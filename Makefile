.DEFAULT_GOAL := up

up:
	docker-compose up --build -d

down:
	docker-compose down

logs:
	docker-compose logs -f

build:
	docker-compose build

clean:
	docker-compose down -v