FROM node:23

# dependencies
RUN apt-get update 
RUN apt-get upgrade -y 
RUN apt-get install curl libgconf-2-4 libatk1.0-0 libatk-bridge2.0-0 libgdk-pixbuf2.0-0 libgtk-3-0 libgbm-dev libnss3-dev libxss-dev libasound2 -y

# create ctf user and directory
RUN mkdir /ctf
WORKDIR /ctf
RUN useradd -M -d /ctf ctf

# copy files
COPY secret.txt /ctf/secret.txt
COPY flag.txt /ctf/flag.txt
COPY server.js /ctf/server.js
COPY adminBot.js /ctf/adminBot.js
COPY public /ctf/public
COPY package*.json /ctf

# install dependencies
RUN npm install

# set permissions
RUN chown -R root:ctf /ctf 
RUN chmod -R 750 /ctf

CMD ["npm", "start"]

EXPOSE 3000
