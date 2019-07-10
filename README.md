# Census RM Print File Service [![Build Status](https://travis-ci.com/ONSdigital/census-rm-print-file-service.svg?branch=master)](https://travis-ci.com/ONSdigital/census-rm-print-file-service)
A lighter weight service to replace the [census-rm-actionexporter-service](https://github.com/ONSdigital/census-rm-actionexporter-service)

## Dependencies
Dependencies are managed through [pipenv](https://github.com/pypa/pipenv).
Install with
```bash
make install
```

## Configuration
The service is configured with environment variables, see [config.py](config.py).

Development defaults can be used by setting `ENVIRONMENT=DEV`.

### Logging config
The general log level is set with `LOG_LEVEL`.
There is a separate setting for pika (rabbit client library) and paramiko (sftp client library) logging, `LOG_LEVEL_PIKA` and `LOG_LEVEL_PARAMIKO` respectively which may be useful for diagnosing specific issues.

## Docker
Test and build the docker image with
```bash
make build_and_test
```
This runs the dependency install and check, linting, unit tests, builds the image then runs the integration tests against it.

Or just build with no tests with
```bash
make docker_build
```

## Run

### Locally
Run locally with dev default config with
```bash
make run
```

### Docker Compose
A docker compose file is also provided which will run the docker image along with a rabbit service and wait for the print file service to become healthy
```bash
make up
```

bring the docker compose services down with
```bash
make down
```

## Tests

### Unit tests
Run with
```bash
make unit_tests
```
Note that you may see some stray error logs in the unit test output, this is a bug with pytest not fully suppressing all output from subprocesses and can safely be ignored if the tests are passing

This will also lint and check dependency package safety

### Integration tests
Run with
```bash
make integraton_tests
```
The end to end integration tests require the app to be running with test config, the make target includes spinning up the docker-compose and waiting for start up.


## Dummy keys
This repo contains dummy keys for SSH and encryption in testing/dev. These keys *must not* be used outside development environments, unless the `ENVIRONMENT` is set to `DEV` or `TEST` the app will not use them requires configuration to specify the keys.

### Dummy Key Passphrases
| Dummy Key          | Passphrase |
| ------------------ | ---------- |
| Our dummy          | test       |
| Dummy PPO supplier | test       |
| Dummy QM supplier  | supplier   |
| Dummy RSA          | secret     |
