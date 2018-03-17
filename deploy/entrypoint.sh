#!/usr/bin/env bash

APP=/app
n=0
while [ $n -lt 5 ]
do
    python3 manage.py init_install &&
    python3 manage.py migrate && break
    n=$(($n+1))
    echo "Failed to migrate, going to retry..."
    sleep 8
done

exec supervisord -c /app/deploy/supervisord.conf