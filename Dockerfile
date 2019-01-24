FROM python:3.7.1

RUN mkdir -p /opt/project/laconia
RUN pip --no-cache-dir install poetry

COPY ./pyproject.toml /opt/project
COPY poetry.lock /opt/project

RUN cd /opt/project && poetry update --no-dev

COPY ./laconia /opt/project/laconia
COPY ./laconia.yml /opt/project/laconia.yml

WORKDIR /opt/project

ENTRYPOINT poetry run python -m aiohttp.web laconia.main:main