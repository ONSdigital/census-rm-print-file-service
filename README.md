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
There is a separate setting for pika (rabbit client library) logging, `LOG_LEVEL_PIKA` which may be useful for diagnosing messing issues.

## Docker
Test and build the docker image with
```bash
make build
```

## Run

### Locally
Run locally with dev default config with
```bash
make run
```

### Docker Compose
A docker compose file is also provided which will run the docker image along with a rabbit service, start with
```bash
make up
```

and bring them down with
```bash
make down
```

## Tests
Run unit tests with
```bash
make test
```

This will also lint and check dependency package safety

