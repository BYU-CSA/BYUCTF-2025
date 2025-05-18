FROM ubuntu:18.04@sha256:152dc042452c496007f07ca9127571cb9c29697f42acbfad72324b2bb2e43c98 AS app

# import into jail
FROM pwn.red/jail
COPY --from=app / /srv

# copy files over
COPY flag.txt /srv/app/flag.txt
COPY tcl /srv/app/run

# setup jail
ENV JAIL_TIME=60 JAIL_MEM=20M JAIL_CONNS_PER_IP=10