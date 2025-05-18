FROM ubuntu:22.04

# update
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y xinetd
RUN rm -rf /var/lib/apt/lists/*

# set up user
RUN mkdir /ctf
RUN useradd -M -d /ctf ctf

# import files
RUN echo "Connection blocked" > /etc/banner_fail
COPY ctf.xinetd /etc/xinetd.d/ctf
COPY ./src /ctf/
COPY flag.txt /ctf/flag.txt

# set permissions
RUN chmod +x /ctf/*
RUN chown -R root:ctf /ctf
RUN chmod -R 750 /ctf

# start
CMD ["/usr/sbin/xinetd", "-dontfork"]
EXPOSE 40000

services:
    minecraft:
      build:
        context: .
        dockerfile: Dockerfile
      ports:
        - "40000:40000"

service ctf
{
    disable = no
    socket_type = stream
    protocol    = tcp
    wait        = no
    user        = ctf
    type        = UNLISTED
    port        = 40000
    bind        = 0.0.0.0
    server      = /bin/sh
    server_args = /ctf/start.sh
    banner_fail = /etc/banner_fail
    per_source  = 10                    # the maximum instances of this service per source IP address
    rlimit_cpu  = 1                     # the maximum number of CPU seconds that the service may use
}

#!/bin/sh

cd /ctf
./minecraft