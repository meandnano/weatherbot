FROM python:3.8-alpine

WORKDIR /src

COPY requirements.txt requirements-test.txt ./

RUN python3 -m venv venv \
    && ./venv/bin/pip3 install -r requirements-test.txt

COPY app/ ./app/
COPY tests/ ./tests/

CMD ./venv/bin/python -u -m pytest