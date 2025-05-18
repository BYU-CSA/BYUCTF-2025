FROM python:latest

# dependencies
RUN apt-get update
RUN apt-get upgrade -y
RUN rm -rf /var/lib/apt/lists/*
RUN pip3 install flask redis

# setup unpriv user
RUN mkdir /ctf
RUN useradd -M -d /ctf ctf

# copy files
COPY main.py /ctf/main.py
COPY templates /ctf/templates

# file perms
RUN chown -R root:ctf /ctf 
RUN chmod -R 750 /ctf

# run
USER ctf
WORKDIR /ctf
CMD ["python3", "main.py"]
EXPOSE 1337