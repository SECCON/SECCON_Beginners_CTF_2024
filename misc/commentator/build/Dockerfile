FROM python:slim AS app
COPY flag.txt /flag.txt
RUN mv /flag.txt /flag-$(md5sum /flag.txt | awk '{print $1}').txt

FROM pwn.red/jail
COPY --from=app / /srv
COPY commentator.py /srv/app/run
RUN chmod +x /srv/app/run
ENV JAIL_TIME=60 JAIL_MEM=20M JAIL_TMP_SIZE=1M