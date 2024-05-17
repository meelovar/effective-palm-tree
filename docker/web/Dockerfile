FROM python:3.12-slim as base

ARG USER_ID=10001
ARG USER_NAME=py_user
ARG USER_HOME=/home/$USER_NAME

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN adduser --uid $USER_ID --home $USER_HOME --gecos "" --disabled-password $USER_NAME

USER $USER_NAME

WORKDIR $USER_HOME/app

FROM base as builder

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    PATH=$USER_HOME/.local/bin:$PATH

RUN pip install poetry

COPY --chown=$USER_NAME:$USER_NAME pyproject.toml ./

RUN poetry install --only main

FROM base as runtime

ENV VIRTUAL_ENV_PATH=$USER_HOME/app/.venv \
    PATH=$USER_HOME/app/.venv/bin:$PATH

COPY --from=builder --chown=$USER_NAME:$USER_NAME $VIRTUAL_ENV_PATH $VIRTUAL_ENV_PATH
COPY --chown=$USER_NAME:$USER_NAME --chmod=744 docker/web/entrypoint.sh $VIRTUAL_ENV_PATH/bin
COPY --chown=$USER_NAME:$USER_NAME src ./

EXPOSE 8000

ENTRYPOINT ["entrypoint.sh"]
CMD []
