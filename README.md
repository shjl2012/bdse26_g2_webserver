# bdse26_g2_webserver

docker_thirdpt：使用 tiangolo/uwsgi-nginx-flask-docker image 建置的測試版\
docker_test：以 ubuntu 2204 base image 建置的測試用dockerfile，測試網站動作用\
docker_deply：最終發佈版本

※BDSE26期末專題的container部署版基於 docker_deploy

#### 使用方式 (基於 docker_deploy)
1. 把資料夾複製到 linux 虛擬機中
2. 在 app.py 寫入 flask app\
3. 把要用 render_template render 的 html 檔放入 templates\
4. CSS、javascript 檔案放入 static\
5-1. (第一次啟動或有修改 Dockerfile) ./buildnstart.sh\
5-2. (不需要更新 image，建置新的 container) ./newcontainer.sh\
5-3. (不需要更新 image，啟動以建立的 container) ./restartcontainer.sh\
