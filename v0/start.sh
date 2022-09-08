#!/bin/bash
app="johnlin/docker_test"
docker build -t ${app} .
docker run -d -p 80:80 \
  --name="docker_test" \
  -v ${PWD}:/app ${app}
