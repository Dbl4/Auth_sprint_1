include .env
WORKDIR = .

lint: 
	black -S -l 79 $(WORKDIR)
	isort $(WORKDIR)
	flake8 --inline-quotes 'double' $(WORKDIR)
	PYTHONPATH=${PYTHONPATH}:${PWD}/$(WORKDIR)
	mypy $(WORKDIR)

build:
	docker-compose down -v
	docker-compose rm -f -v
	docker-compose build


up: 
	docker-compose down
	docker-compose up --detach --build


dev:
	docker-compose down
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --detach --remove-orphans


test:
	docker-compose down
	docker-compose -f docker-compose.yml -f docker-compose.tests.yml up --detach


down: 
	docker-compose down --remove-orphans


loaddata:
	docker-compose exec postgres psql -h 127.0.0.1 -U app -d movies_database -f /var/lib/postgresql/movies_database.sql


create-superuser:
	docker-compose exec auth python commands.py ${SUPERUSER_EMAIL} ${SUPERUSER_PASSWORD}