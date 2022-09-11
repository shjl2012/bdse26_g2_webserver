#!/bin/bash
docker volume create webserver
docker container run --name temp -v webserver:/app alpine
docker cp ./app temp:/app
docker container stop temp 
docker container rm temp