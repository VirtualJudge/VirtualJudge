APP=/app
DATA=/data
if [ ! -d "$DATA" ]; then
  mkdir $DATA
fi

mkdir -p $data/log

n=0
while [ $n -lt 5 ]
do
    python3 manage.py migrate && break
    n=$(($n+1))
    echo "Failed to migrate, going to retry..."
    sleep 8
done
source venv/bin/activate
exec ./manage.py runserver 0.0.0.0:8000
