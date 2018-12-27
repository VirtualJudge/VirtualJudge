FROM python:3.7-alpine

MAINTAINER xudian.cn@gmail.com

ENV VJ_ENV production


ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

#COPY deploy/sources.list /etc/apt/
RUN mkdir -p /public
VOLUME /public

ADD . /app
WORKDIR /app

RUN apk add --update --no-cache build-base nginx curl unzip supervisor postgresql-dev git libxml2-dev
RUN pip3 install --no-cache-dir -r /app/requirements.txt
RUN apk del build-base --purge

RUN curl -L  $(curl -s  https://api.github.com/repos/VirtualJudge/VirtualJudgeFE/releases/latest | grep /dist.zip | cut -d '"' -f 4) -o dist.zip && \
    unzip dist.zip && \
    rm dist.zip
CMD bash /app/deploy/entrypoint.sh
