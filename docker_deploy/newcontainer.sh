#!/bin/bash

# 建立新的 container (若已有相同名字的 container 則會停止、刪除該 container 後重啟)
app="johnlin/docker_test_v2.1"
container_name="docker_test_2"
echo "Create new container ${container_name}..."
docker container stop ${container_name} &>/dev/null
docker container rm ${container_name} &>/dev/null
docker container run -d -p 80:5000 --name ${container_name} ${app}
