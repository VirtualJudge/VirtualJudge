#!/usr/bin/env bash

APP=/app


mkdir -p /data/log

n=0
while [ $n -lt 5 ]
do
    python3 manage.py init_install && break
    n=$(($n+1))
    echo "Failed to migrate, going to retry..."
    sleep 8
done
service nginx stop
nginx -c /app/deploy/nginx/nginx.conf
exec supervisord -c /app/deploy/supervisord.conf
