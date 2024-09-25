FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=nointeractive
RUN apt-get -y update && apt-get -yqq install gcc make build-essential

CMD make -C /build chall
