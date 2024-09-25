FROM ubuntu:22.04@sha256:2af372c1e2645779643284c7dc38775e3dbbc417b2d784a27c5a9eb784014fb8
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update --fix-missing && apt-get -y upgrade
RUN apt-get -y install xinetd qemu-system hashcash
RUN groupadd -r pwn && useradd -r -g pwn pwn

RUN echo '#!/bin/bash\n\
pushd /home/pwn\n\
  echo $FLAG > flag.txt\n\
  chmod 444 flag.txt\n\
popd\n\
unset FLAG\n\
service xinetd restart && /bin/sleep infinity' > /etc/init.sh
RUN echo 'service pwn\n\
{\n\
  type = UNLISTED\n\
  disable = no\n\
  socket_type = stream\n\
  protocol = tcp\n\
  wait = no\n\
  user = pwn\n\
  bind = 0.0.0.0\n\
  port = 9999\n\
  server = /home/pwn/run.sh\n\
}' > /etc/xinetd.d/pwn
RUN chmod 500 /etc/init.sh
RUN chmod 444 /etc/xinetd.d/pwn
RUN chmod 1733 /tmp /var/tmp /dev/shm

WORKDIR /home/pwn
ADD files/bzImage     .
ADD files/rootfs.cpio .
ADD build/run.sh      .
RUN chmod 550 run.sh

RUN chown -R root:pwn /home/pwn
RUN service xinetd restart
