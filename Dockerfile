FROM ubuntu:18.04

MAINTAINER xudian.cn@gmail.com

ENV VJ_ENV production


ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

#COPY deploy/sources.list /etc/apt/
RUN mkdir -p /public
VOLUME /public

ADD . /app
WORKDIR /app

RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip supervisor git nginx
RUN pip3 install -r /app/requirements.txt

RUN curl -L  $(curl -s  https://api.github.com/repos/VirtualJudge/VirtualJudgeFE/releases/latest | grep /dist.zip | cut -d '"' -f 4) -o dist.zip && \
    unzip dist.zip && \
    rm dist.zip
CMD bash /app/deploy/entrypoint.sh
