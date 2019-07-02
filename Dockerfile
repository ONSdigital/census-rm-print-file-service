FROM python:3.7-slim

WORKDIR /app
COPY . /app
RUN pip install pipenv
RUN pipenv install --system --deploy