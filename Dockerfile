FROM nginx/unit:1.29.1-python3.11

WORKDIR /app

COPY pyproject.toml pyproject.toml
COPY README.md README.md
COPY quiz_api quiz_api
COPY alembic.ini alembic.ini
COPY unit-config.json /docker-entrypoint.d/config.json

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
RUN mkdir -p /config
RUN chown -R unit:unit /config

ENV CONFIG_PATH /config/config.yml

WORKDIR /config

VOLUME /config
EXPOSE 14131
