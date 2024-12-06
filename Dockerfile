FROM python:3.12-slim

RUN apt update &&  apt install -y libmariadb3 libmariadb-dev gcc git

RUN pip install poetry

RUN python -m venv /opt/.venv
ENV PATH="/opt/.venv/bin:$PATH" VIRTUAL_ENV="/opt/.venv"

RUN mkdir /app
COPY pyproject.toml poetry.lock /app/
WORKDIR /app

RUN poetry lock --no-update && poetry install --no-root

EXPOSE 5000

RUN mkdir /root/.ssh
RUN ln -s /run/secrets/ssh_key /root/.ssh/id_rsa
RUN ln -s /run/secrets/gitconfig /root/.gitconfig


ENTRYPOINT ["poetry", "run", "gunicorn", "wsgi:app", "--bind", "0.0.0.0:5000", "--workers", "4"]
# CMD tail -f /dev/null