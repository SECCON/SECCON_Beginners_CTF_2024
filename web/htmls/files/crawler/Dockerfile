FROM ubuntu:22.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install bash\
                       python3 \
                       python3-pip \
                       libdrm2 \
                       libgbm1 \
                       libnss3 \
                       libnspr4 \
                       libasound2 \
                       libgtk-3-0 \
                       libx11-xcb1

RUN mkdir -p /var/www/htmls
WORKDIR /var/www
COPY ./ ./

RUN pip3 install -r requirements.txt
ENV LANG C.UTF-8

RUN chmod 755 -R /var/www
RUN chmod 777 /var/www/htmls

RUN adduser -u 1000 htmls
USER htmls

RUN mkdir /var/www/htmls/ctf

RUN playwright install

CMD bash -c "./make_flag.sh && uwsgi --ini /var/www/uwsgi.ini"