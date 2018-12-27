FROM ubuntu:18.04

MAINTAINER xudian.cn@gmail.com

ENV VJ_ENV develop


ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

#COPY deploy/sources.list /etc/apt/
RUN mkdir -p /public
RUN chown nobody /public
VOLUME /public

ADD . /app
WORKDIR /app

RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip supervisor git nginx
RUN pip3 install -r /app/requirements.txt
CMD bash /app/deploy/entrypoint.sh
