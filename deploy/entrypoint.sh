#!/usr/bin/env bash

APP=/app
DATA=/data

mkdir -p $DATA/log $DATA/ssl $DATA/test_case $DATA/public/upload $DATA/public/avatar $DATA/public/website
n=0
while [ $n -lt 5 ]
do
    python3 manage.py init_install &&
    python3 manage.py migrate && break
    n=$(($n+1))
    echo "Failed to migrate, going to retry..."
    sleep 8
done
service nginx stop
exec supervisord -c /app/deploy/supervisord.conf
