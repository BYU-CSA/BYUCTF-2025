FROM pwn.red/jail

COPY --from=python:slim / /srv

WORKDIR /srv/app/

COPY secrets.py .
COPY server.py run

ENV JAIL_TIME=60 JAIL_MEM=20M JAIL_CONNS_PER_IP=10