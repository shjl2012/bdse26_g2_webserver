#!/bin/bash
app="johnlin/docker_test_v2.1"
docker build -t ${app} .
docker container run -d -p 80:5000 --name docker_test_2 ${app}

# 下一步測試
# 掛載 /app 資料夾到 webserver docker volume
# docker container run -d -v webserver:/app -p 80:5000 --name docker_test_v2 ${app}