FROM legoclones/mips-pwn:mipsel32r5-glibc AS app

# import into jail
FROM pwn.red/jail
COPY --from=app /target/ /srv

# copy files over
COPY ctf/flag.txt /srv/app/flag.txt
COPY ctf/mips /srv/app/mips
COPY ctf/start.sh /srv/app/run

# setup jail
ENV JAIL_TIME=60 JAIL_MEM=20M JAIL_CONNS_PER_IP=10 JAIL_PIDS=10 JAIL_POW=12000