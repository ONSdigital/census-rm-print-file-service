install:
	pipenv install --dev

check:
	pipenv check

lint:
	pipenv run flake8

test: check lint
	pipenv run pytest test --cov app --cov-report term-missing

build: install test
	docker build . -t eu.gcr.io/census-rm-ci/rm/census-rm-print-file-service:latest

up:
	docker-compose up -d

down:
	docker-compose down