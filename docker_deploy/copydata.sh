#!/bin/bash
# 把目前路徑的內容複製到 webserver 這個 docker volume 的 /app 資料夾用指令
# 建立一個用來存檔的中介 container temp，帶複製完資料移除
docker volume create webserver
docker container run --name temp -v webserver:/app alpine
docker cp ./app temp:/app
docker container stop temp 
docker container rm temp