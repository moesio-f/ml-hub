FROM python:3.10-slim-bullseye

RUN mkdir /app/
COPY ./requirements.txt /requirements.txt
RUN apt-get update && \
    apt-get install zip unzip && \
    python -m pip install -r requirements.txt

COPY ./src/ /code/
WORKDIR /code/
ENV PYTHONPATH="/code/:${PYTHONPATH}"
