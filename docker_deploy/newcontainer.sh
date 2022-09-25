#!/bin/bash

# 建立新的 container (若已有相同名字的 container 則會停止、刪除該 container 後重啟)
iname="johnlin/docker_deploy_v3"
cname="docker_deploy_v3"
echo "Create new container ${cname}..."
docker container stop ${cname} &>/dev/null
docker container rm ${cname} &>/dev/null
docker container run -d -p 80:5000 --name ${cname} ${iname}
