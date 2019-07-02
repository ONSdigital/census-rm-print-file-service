install:
	pipenv install --dev

check:
	pipenv check

lint:
	pipenv run flake8

test: check lint
	pipenv run pytest tests

build: install test
	docker build . -t eu.gcr.io/census-rm-ci/rm/census-rm-print-file-service:latest
