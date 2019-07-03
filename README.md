# Census RM Print File Service [![Build Status](https://travis-ci.com/ONSdigital/census-rm-print-file-service.svg?branch=master)](https://travis-ci.com/ONSdigital/census-rm-print-file-service)
A lighter weight service to replace the [census-rm-actionexporter-service](https://github.com/ONSdigital/census-rm-actionexporter-service)

## Dependencies
Dependencies are managed through [pipenv](https://github.com/pypa/pipenv).
Install with
```bash
make install
```

## Tests
Run unit tests with
```bash
make test
```

This will also lint and check dependency package safety

## Docker image
Test and build the docker image with
```bash
make build
```

A docker compose file is also provided to run with a rabbit service, start with
```bash
make up
```

and bring them down with
```bash
make down
```