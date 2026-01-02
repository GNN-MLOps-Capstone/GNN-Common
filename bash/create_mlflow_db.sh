#!/bin/bash

docker compose exec -it postgres /bin/bash -c 'psql postgresql://유저명:비밀번호@postgres/데이터베이스명 -c "CREATE DATABASE mlflow_db;"'