FROM python:slim AS app
RUN pip install --no-cache-dir pycryptodome

FROM pwn.red/jail

COPY --from=app / /srv

WORKDIR /srv/app/

COPY secrets.py .
COPY real-smooth.py run
ENV JAIL_TIME=60 JAIL_MEM=20M JAIL_CONNS_PER_IP=10