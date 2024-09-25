FROM python:slim AS app
RUN apt update && apt install -y gcc
RUN pip install --no-cache-dir pycryptodome

FROM pwn.red/jail
COPY --from=app / /srv
COPY --chmod=555 files/server.py /srv/app/run
ENV JAIL_TIME=300 JAIL_MEM=64M JAIL_ENV_FLAG="ctf4b{1f_y0u'r3_4n_1n73rm3d1473_b3y0nd_b361nn3r,_17'5_345y!_y4y}"
