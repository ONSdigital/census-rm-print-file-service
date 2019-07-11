FROM python:3.7-slim

RUN pip install pipenv

WORKDIR /app
CMD ["python3", "run.py"]

COPY . /app
RUN pipenv install --system --deploy
