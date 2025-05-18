FROM pwn.red/jail

COPY --from=python:slim / /srv

COPY server.py /srv/app/run

ENV JAIL_TIME=60 JAIL_MEM=20M JAIL_CONNS_PER_IP=10