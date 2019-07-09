install:
	pipenv install --dev

check:
	pipenv check

lint:
	pipenv run flake8

unit_tests: check lint
	 pipenv run pytest test/unit_tests --cov app --cov-report term-missing

integration_tests:
	docker-compose down
	docker-compose up -d
	bash ./test/integration_tests/wait_for_print_file_service.sh
	pipenv run pytest test/integration_tests
	docker-compose down

test: unit_tests integration_tests
run:
	ENVIRONMENT=DEV pipenv run python run.py

docker_build:
	docker build . -t eu.gcr.io/census-rm-ci/rm/census-rm-print-file-service:latest

build_and_test: install unit_tests docker_build integration_tests

up:
	docker-compose up -d

down:
	docker-compose down