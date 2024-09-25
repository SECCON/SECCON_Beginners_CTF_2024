FROM ubuntu:24.04 AS base
WORKDIR /app
COPY files/chall run
RUN echo "ctf4b{0n_y0ur_m4rk}" > /app/flag.txt

FROM pwn.red/jail
COPY --from=base / /srv
RUN chmod +x /srv/app/run
ENV JAIL_TIME=120 JAIL_CPU=100 JAIL_MEM=10M
