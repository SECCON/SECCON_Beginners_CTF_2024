FROM ubuntu:24.04

RUN mkdir /var/www
WORKDIR /var/www
COPY ./requirements.txt ./

RUN apt-get update -yqq && apt-get install clamav python3 python3-pip -yqq && pip3 install -r requirements.txt --break-system-packages

COPY ./ ./

RUN chmod 755 -R /var/www
RUN adduser -u 1337 clamre
USER clamre

CMD ["uwsgi", "--ini", "/var/www/uwsgi.ini"]
