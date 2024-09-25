FROM dreamhackofficial/web3-base:latest@sha256:9c3f148a20a0ad309c400b3fc578a974f82692a33d49b5aa355d664ffc542032

COPY ./files/src/*.sol /app/src
COPY ./files/deploy/config.yaml /app/
COPY ./files/deploy/verifier.py /app/verifier.py
RUN printf "ctf4b{Re-3n7r4ncyyYYYyyyyYYYYyYYYyyYyYY!}" > /app/flag.txt

RUN /app/build.sh
