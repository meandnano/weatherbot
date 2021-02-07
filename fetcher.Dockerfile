FROM alpine:3.13 as build

RUN apk update \
    && apk add py3-pip build-base \
    && pip3 install virtualenv

WORKDIR /src
COPY requirements.txt ./
RUN virtualenv venv \
    && ./venv/bin/pip3 install -r requirements.txt

FROM alpine:3.13

RUN apk add python3

WORKDIR /src

COPY --from=build /src/venv/ ./venv/
COPY fethcher.py weather.py ./

CMD ./venv/bin/python -u fethcher.py