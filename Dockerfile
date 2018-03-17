FROM python:3.6-alpine3.6

ENV OJ_ENV production

ADD . /app
WORKDIR /app


RUN apk add --update --no-cache build-base openssl curl unzip supervisor jpeg-dev zlib-dev postgresql-dev && \
    pip install --no-cache-dir -r /app/deploy/requirements.txt && \
    apk del build-base --purge

ENTRYPOINT /app/deploy/entrypoint.sh