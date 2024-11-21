FROM python:3.11

WORKDIR /bot

ENV PATH="${PATH}:/root/.poetry/bin"

RUN pip install poetry

COPY poetry.lock pyproject.toml /bot/

RUN poetry config virtualenvs.create false 
RUN poetry install --no-root

COPY ./ ./

ENTRYPOINT [ "python", "main.py" ]
