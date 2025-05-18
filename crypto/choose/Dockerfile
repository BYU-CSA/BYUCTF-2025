FROM python:3 AS app

# dependencies
RUN apt-get update
RUN apt-get upgrade -y
RUN rm -rf /var/lib/apt/lists/*
RUN pip3 install --no-cache-dir pycryptodome

# import into jail
FROM pwn.red/jail
COPY --from=app / /srv

# copy files over
COPY flag.txt /srv/app/flag.txt
COPY server.py /srv/app/run

# setup jail
ENV JAIL_TIME=60 JAIL_MEM=20M JAIL_CONNS_PER_IP=10 JAIL_CPU=500