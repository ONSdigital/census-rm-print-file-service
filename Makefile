install:
	pipenv install --dev

check:
	# TODO: 38932 - Explicitly ignore RSA decryption warning (unused by this service)
	PIPENV_PYUP_API_KEY="" pipenv check -i 38932

lint:
	pipenv run flake8

unit_tests: check lint
	pipenv run pytest test/unit_tests --cov app --cov-report term-missing

integration_tests: clean_working_files down up
	pipenv run pytest test/integration_tests
	docker-compose down

test: build_and_test

run:
	ENVIRONMENT=DEV pipenv run python run.py

docker_build:
	docker build . -t eu.gcr.io/census-rm-ci/rm/census-rm-print-file-service:latest

build_and_test: install unit_tests docker_build integration_tests

up:
	docker-compose up -d
	bash ./test/integration_tests/wait_for_print_file_service.sh

down:
	docker-compose down

clean_working_files:
	rm -rf working_files

build_and_integration_tests_no_clean: install unit_tests docker_build integration_tests_no_clean


integration_tests_no_clean: down up
	pipenv run pytest test/integration_tests
	docker-compose down