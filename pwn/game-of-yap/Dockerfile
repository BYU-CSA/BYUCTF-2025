FROM ubuntu:24.04@sha256:3afff29dffbc200d202546dc6c4f614edc3b109691e7ab4aa23d02b42ba86790 AS app

# import into jail
FROM pwn.red/jail
COPY --from=app / /srv

# copy files over
COPY flag.txt /srv/app/flag.txt
COPY game-of-yap /srv/app/run

# setup jail
ENV JAIL_TIME=60 JAIL_MEM=20M JAIL_CONNS_PER_IP=10