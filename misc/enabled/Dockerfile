FROM pwn.red/jail

COPY --from=ubuntu / /srv

WORKDIR /srv/app/

RUN mkdir /srv/flag
COPY flag.txt /srv/flag/flag.txt
COPY src/jail.sh run

ENV JAIL_TIME=60 JAIL_MEM=20M JAIL_CONNS_PER_IP=10