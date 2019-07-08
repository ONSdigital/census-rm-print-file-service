install:
	pipenv install --dev

check:
	pipenv check

lint:
	pipenv run flake8

unit_tests: check lint
	ENVIRONMENT=TEST pipenv run pytest test/unit_tests --cov app --cov-report term-missing

integration_tests:
	ENVIRONMENT=TEST pipenv run pytest test/integration_tests

test: unit_tests integration_tests
run:
	ENVIRONMENT=DEV pipenv run python run.py

build: install test
	docker build . -t eu.gcr.io/census-rm-ci/rm/census-rm-print-file-service:latest

up:
	docker-compose up -d

down:
	docker-compose down