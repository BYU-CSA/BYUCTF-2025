#!/bin/bash
#start redis stack server and populate
./scripts/populate.sh &

./bin/redis-stack-server

