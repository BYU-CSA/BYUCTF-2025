FROM node:22-bookworm

# create unpriv user
RUN mkdir /ctf
WORKDIR /ctf
RUN useradd -M -d /ctf ctf
RUN chown -R root:ctf /ctf 
RUN chmod -R 750 /ctf

# install dependencies
RUN npm install --force express

# copy files
COPY server.js /ctf/server.js
COPY flag.txt /ctf/flag.txt

# run
USER ctf
CMD ["node", "/ctf/server.js"]
EXPOSE 3000