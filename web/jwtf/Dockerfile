FROM python:3

# dependencies
RUN apt-get update
RUN apt-get upgrade -y
RUN rm -rf /var/lib/apt/lists/*
RUN pip3 install flask PyJWT

# setup unpriv user
RUN mkdir /ctf
RUN useradd -M -d /ctf ctf

# copy files
COPY server.py /ctf/server.py
COPY flag.txt /ctf/flag.txt

# file perms
RUN chown -R root:ctf /ctf 
RUN chmod -R 750 /ctf

# run
USER ctf
WORKDIR /ctf
CMD ["python3", "server.py"]
EXPOSE 1337