FROM python:3.11.3-alpine

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1

RUN apk add libmagic

RUN pip install "pipenv"

WORKDIR /app
COPY Pipfile ./
COPY Pipfile.lock ./
COPY main.py ./
COPY db.py ./
COPY utils.py ./
COPY clients/* ./clients/
COPY models/* ./models/

RUN pipenv install

# Set this
ENTRYPOINT ["pipenv", "run", "python", "main.py"]
