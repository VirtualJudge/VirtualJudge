FROM ubuntu:18.04

ENV OJ_ENV production

ADD . /app
WORKDIR /app

RUN apt update
RUN apt install -y python3 python3-dev postgresql supervisor  && \
    pip3 install --no-cache-dir -r /app/deploy/requirements.txt && \
    apk del build-base --purge

ENTRYPOINT /app/deploy/entrypoint.sh