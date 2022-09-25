#!/bin/bash
iname="johnlin/docker_deploy_v3"
cname="docker_deploy_v3"
docker build -t ${iname} .
docker container run -d -p 80:5000 --name ${cname} ${iname}

# 下一步測試
# 掛載 /app 資料夾到 webserver docker volume
# docker container run -d -v webserver:/app -p 80:5000 --name docker_test_v2 ${app}
