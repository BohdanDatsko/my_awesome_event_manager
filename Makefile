up:
	@echo "Start local up"
	docker compose -f docker-compose.local.yml up

down:
	@echo "Start local down"
	docker compose -f docker-compose.local.yml down --remove-orphans

build:
	@echo "Start local build"
	docker compose -f docker-compose.local.yml build

restart:
	@echo "Start local restart"
	docker compose -f docker-compose.local.yml down --remove-orphans
	docker compose -f docker-compose.local.yml build
	docker compose -f docker-compose.local.yml up

migrate:
	@echo "Start local migrate"
	docker compose -f docker-compose.local.yml run --rm django python manage.py migrate

makemigrations:
	@echo "Start local makemigrations"
	docker compose -f docker-compose.local.yml run --rm django python manage.py makemigrations

createsuperuser:
	@echo "Start local createsuperuser"
	docker compose -f docker-compose.local.yml run --rm django python manage.py createsuperuser

shell:
	@echo "Start local shell"
	docker compose -f docker-compose.local.yml run --rm django python manage.py shell

pytest:
	@echo "Start local pytest"
	docker compose -f docker-compose.local.yml run --rm -e DJANGO_TEST=1 django pytest

pytest_print:
	@echo "Start local pytest & return all prints"
	docker compose -f docker-compose.local.yml run --rm -e DJANGO_TEST=1 django pytest -v -s

pytest_delete_cache:
	@echo "Start local pytest_delete_cache"
	docker compose -f docker-compose.local.yml run --rm django python manage.py pytest_delete_cache
	docker compose -f docker-compose.local.yml down --remove-orphans

coverage:
	@echo "Start local coverage"
	docker compose -f docker-compose.local.yml run --rm django coverage run -m pytest
	docker compose -f docker-compose.local.yml run --rm django coverage report

docs_server:
	@echo "Start serving docs"
	docker compose -f docker-compose.docs.yml up
