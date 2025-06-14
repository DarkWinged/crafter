FROM python:3.12.1

RUN <<EORUN
    set -x
    groupadd -r craftsman
    useradd -r -g craftsman -d /home/craftsman -s /bin/bash craftsman
EORUN

WORKDIR /home/craftsman

RUN <<EORUN
    mkdir ./data
    chown craftsman:craftsman ./data
EORUN


ENV API_VERSION="0.0.0"
ENV APP_VERSION="0.0.0"

ENV ARCHIVE_PATH="/home/craftsman/data"
ENV SERVER_PORT="8000"
ENV SERVER_HOST="0.0.0.0"

COPY . ./crafter
RUN <<EORUN
    set -x
    pip install -U pip
    pip install --no-cache-dir -e ./crafter
EORUN

USER craftsman
ENTRYPOINT [ "server" ]
