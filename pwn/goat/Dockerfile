FROM ubuntu:24.04@sha256:278628f08d4979fb9af9ead44277dbc9c92c2465922310916ad0c46ec9999295 AS app

# import into jail
FROM pwn.red/jail
COPY --from=app / /srv

# copy files over
COPY flag.txt /srv/app/flag.txt
COPY goat /srv/app/run

# setup jail
ENV JAIL_TIME=60 JAIL_MEM=20M JAIL_CONNS_PER_IP=10 JAIL_POW=12000