FROM ubuntu:18.04

ENV OJ_ENV production

ADD . /app
WORKDIR /app

RUN apt update
RUN apt install -y python3 python3-dev python3-pip postgresql supervisor
RUN  pip3 install -r /app/deploy/requirements.txt

ENTRYPOINT /app/deploy/entrypoint.sh