#!/bin/bash

# 重新啟動 app container
cname="docker_deploy_v3"
docker container start ${cname}