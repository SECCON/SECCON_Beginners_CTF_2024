FROM ubuntu:24.04 AS base
WORKDIR /app
COPY files/chall run
RUN echo "ctf4b{Y0u_R34lly_G0T_M3}" > /app/flag.txt

FROM pwn.red/jail
COPY --from=base / /srv
RUN chmod +x /srv/app/run
ENV JAIL_TIME=120 JAIL_CPU=100 JAIL_MEM=10M
