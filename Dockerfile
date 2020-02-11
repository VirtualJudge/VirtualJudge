FROM python:3.7-slim

MAINTAINER xudian.cn@gmail.com

ENV VJ_ENV production

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

#COPY deploy/sources.list /etc/apt/
RUN mkdir -p /public
VOLUME /public

ADD . /app
WORKDIR /app
RUN pip3 install --no-cache-dir virtualenv
RUN source /app/venv/bin/activate
RUN pip3 install --no-cache-dir -r /app/requirements.txt

CMD bash /app/deploy/entrypoint.sh
