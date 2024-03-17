# https://www.cloudbees.com/blog/using-docker-compose-for-python-development
FROM python:3-alpine
RUN apk update && \
    apk add \
    build-base \
    postgresql \
    postgresql-dev \
    libpq
RUN python -m pip install Django
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
ENV PYTHONUNBUFFERED 1
