#!/usr/bin/env bash

APP=/app
n=0
while [ $n -lt 5 ]
do
    python manage.py init_install &&
    python manage.py migrate --no-input
    n=$(($n+1))
    echo "Failed to migrate, going to retry..."
    sleep 8
done

exec supervisord -c /app/deploy/supervisord.conf