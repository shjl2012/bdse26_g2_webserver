#!/bin/bash
app="johnlin/docker_test_v2"
docker build -t ${app} .
docker container run -d -p 80:5000 --name docker_test_v2 ${app}
# docker container run -d -v webserver:/app -p 80:5000 --name docker_test_v2 ${app}
