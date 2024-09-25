FROM python:slim AS app
RUN apt update && apt install -y gcc
RUN pip install --no-cache-dir pycryptodome

FROM pwn.red/jail
COPY --from=app / /srv
COPY --chmod=555 files/server.py /srv/app/run
ENV JAIL_TIME=300 JAIL_MEM=32M JAIL_ENV_FLAG="ctf4b{bl0ck_c1pher_is_a_fun_puzzl3}"
