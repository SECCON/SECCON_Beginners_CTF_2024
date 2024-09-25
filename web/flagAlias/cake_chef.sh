#!/bin/bash
set -e

TIMEOUT=600
HOST="flagalias.beginners.seccon.games"
DOCKER_IMAGE_APP="ctf4b-flagalias-app"
DOCKER_IMAGE_NGINX="ctf4b-flagalias-nginx"

cat <<EOF
     .::.::.::.
    ::^^:^^:^^::  >> Cake Chef <<
    ':'':'':'':'  
    _i__i__i__i_     CTF
   (____________)    Instance
   |#o##o##o##o#|    Generator
   (____________)
We will create a new server for you.
 Please test your exploit locally.

EOF

LENGTH=10
STRENGTH=26
challenge=`dd bs=32 count=1 if=/dev/urandom 2>/dev/null | base64 | tr +/ ab | cut -c -$LENGTH`
BACKEND_NAME=`dd bs=32 count=1 if=/dev/urandom 2>/dev/null | base64 | tr +/ ab | cut -c -$LENGTH`
echo hashcash -mb$STRENGTH $challenge

# Challenge
echo "hashcash token: "
read token
if [ `expr "$token" : "^[a-zA-Z0-9\+\_\.\:\/]\{52\}$"` -eq 52 ]; then
    hashcash -cdb$STRENGTH -f /tmp/hashcash.sdb -r $challenge $token 2> /dev/null
    if [ $? -eq 0 ]; then
        echo "[+] Correct"
    else
        echo "[-] Wrong"
        exit
    fi
else
    echo "[-] Wrong"
    exit
fi

# Get random port
BASIC_USERNAME="guest"
BASIC_PASSWORD=`dd bs=32 count=1 if=/dev/urandom 2>/dev/null | base64 | tr +/ ab | cut -c -16`
read LOWERPORT UPPERPORT < /proc/sys/net/ipv4/ip_local_port_range
while :
do
    PORT="`shuf -i $LOWERPORT-$UPPERPORT -n 1`"
    ss -lpn | grep -q ":$PORT " || break
done

echo "Your server: https://${HOST}:${PORT}/"
echo "Username for basic auth: ${BASIC_USERNAME}"
echo "Password for basic auth: ${BASIC_PASSWORD}"
echo "Timeout: ${TIMEOUT}sec"
echo "It may take less than a minute to start a new instance."
echo "Please be patient. You can close this connection now."

if [ -d /path/to/directory ]; then
  cd /home/ubuntu/flagAlias
fi

docker network create "${challenge}" 2>/dev/null 1>/dev/null

# app
timeout --foreground -s9 "${TIMEOUT}" \
        docker run \
        --net="${challenge}" \
        --rm --name "${BACKEND_NAME}" "${DOCKER_IMAGE_APP}" 2>/dev/null 1>/dev/null &

# nginx
timeout --foreground -s9 "${TIMEOUT}" \
        docker run \
        --net="${challenge}" \
        -e BASIC_USERNAME="${BASIC_USERNAME}" \
        -e BASIC_PASSWORD="${BASIC_PASSWORD}" \
        -e BACKEND_NAME="${BACKEND_NAME}" \
        -v /etc/seccon/_.seccon.games.crt:/etc/nginx/certs/server.crt:ro \
        -v /etc/seccon/_.seccon.games.key:/etc/nginx/certs/server.key:ro \
        -p "${PORT}:443" \
        --rm --name "${challenge}" "${DOCKER_IMAGE_NGINX}" 2>/dev/null 1>/dev/null

docker network rm "${challenge}"

echo "Timeout!"
docker kill "${BACKEND_NAME}" 2>&1 1>/dev/null
docker kill "${challenge}" 2>&1 1>/dev/null
