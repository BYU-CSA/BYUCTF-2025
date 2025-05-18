FROM redis/redis-stack-server:latest

# set PROD
ENV PROD true

# copy files
RUN mkdir /scripts
COPY ./inserts/* /scripts/
RUN chmod -R 764 /scripts

# run
CMD ["./scripts/start_and_populate.sh"]