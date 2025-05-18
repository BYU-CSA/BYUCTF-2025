#!/bin/bash
# check if prod
insert_path="/scripts/insert.redis"
if [ "$PROD" == true ]; then
    insert_path="/scripts/prod_insert.redis"
fi
# if redis is active activeRedis will contain "PONG" else nothing
activeRedis=$(redis-cli ping)

while [[ $activeRedis != "PONG" ]]; do
sleep 1;
activeRedis=$(redis-cli ping)
done

result=$(redis-cli < $insert_path);
