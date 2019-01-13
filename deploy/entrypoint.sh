#!/usr/bin/env bash

APP=/app
DATA=data
if [ ! -d "$DATA" ]; then
  mkdir $DATA
fi

if [ ! -f "$DATA/secret.key" ]; then
    echo $(cat /dev/urandom | head -1 | md5sum | head -c 32) > "$DATA/secret.key"
fi

mkdir -p $data/log

n=0
while [ $n -lt 5 ]
do
    python3 manage.py init_install && break
    n=$(($n+1))
    echo "Failed to migrate, going to retry..."
    sleep 8
done
exec supervisord -c /app/deploy/supervisord.conf
