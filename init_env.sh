DATA=data
if [ ! -d "$DATA" ]; then
  mkdir $DATA
fi

if [ ! -f "$DATA/secret.key" ]; then
    echo $(cat /dev/urandom | head -1 | md5sum | head -c 32) > "$DATA/secret.key"
fi
