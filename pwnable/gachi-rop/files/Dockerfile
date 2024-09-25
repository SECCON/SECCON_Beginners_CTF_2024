FROM ubuntu:22.04@sha256:2af372c1e2645779643284c7dc38775e3dbbc417b2d784a27c5a9eb784014fb8 AS base
WORKDIR /app
COPY gachi-rop run
COPY flag.txt /flag.txt
RUN mkdir ctf4b
RUN  mv /flag.txt ctf4b/flag-$(md5sum /flag.txt | awk '{print $1}').txt

FROM pwn.red/jail
COPY --from=base / /srv
RUN chmod +x /srv/app/run
ENV JAIL_TIME=60 JAIL_CPU=100 JAIL_MEM=10M