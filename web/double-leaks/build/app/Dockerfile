FROM ubuntu:20.04

RUN mkdir /var/www
WORKDIR /var/www
COPY ./requirements.txt ./

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update --fix-missing && \
	apt-get install -y python3 python3-pip && \
	pip3 install -r requirements.txt

COPY ./ ./

RUN chmod 755 -R /var/www
RUN adduser -u 1000 double-leaks
USER double-leaks

CMD ["uwsgi", "--ini", "/var/www/uwsgi.ini"]