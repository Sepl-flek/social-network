FROM python:3.12-alpine3.22

RUN adduser --disabled-password appuser

COPY requirements.txt /temp/requirements.txt
COPY chatserver /chatserver

WORKDIR /chatserver
EXPOSE 8000

RUN apk add postgresql-client build-base postgresql-dev
RUN pip install -r /temp/requirements.txt

USER appuser