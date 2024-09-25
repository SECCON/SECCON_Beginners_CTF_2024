#!/bin/sh
USERNAME=${BASIC_USERNAME:-user}
PASSWORD=${BASIC_PASSWORD:-password}
BACKEND_NAME=${BACKEND_NAME:-backend}

htpasswd -bc /etc/nginx/.htpasswd $USERNAME $PASSWORD

sed -i "s/app_flagalias/$BACKEND_NAME/g" /etc/nginx/nginx.conf

exec "$@"
