FROM python:3.7-alpine

WORKDIR /app
COPY . /app
RUN pip install pipenv
RUN pipenv install --system --deploy
CMD ["python3", "run.py"]
