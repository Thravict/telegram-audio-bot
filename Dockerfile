FROM python:3.13.1-alpine3.21

ENV POETRY_VERSION=1.8.5
ENV APPLICATION_HOME=/opt/telegram-audio-bot
WORKDIR $APPLICATION_HOME
ENV POETRY_HOME=/opt/poetry

RUN set -eux; \
    python3 -m venv $POETRY_HOME; \
    $POETRY_HOME/bin/pip install poetry==$POETRY_VERSION; \
    $POETRY_HOME/bin/poetry --version

COPY ./src $APPLICATION_HOME/src
COPY ./poetry.lock $APPLICATION_HOME
COPY ./pyproject.toml $APPLICATION_HOME
COPY ./README.md $APPLICATION_HOME

RUN $POETRY_HOME/bin/poetry install

EXPOSE 8080

ENTRYPOINT [ "/bin/sh", "poetry", "run", "telegram-audio-inline-bot" ]