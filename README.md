# bdse26_g2_webserver

webserver_reference：使用 tiangolo/uwsgi-nginx-flask-docker 的測試伺服器\
webserver_test：以 ubuntu 2204 base image 建置的測試環境\
webserver_docker：以 ubutu server base image 建立的 docker 發佈版本 

※期末專題預定使用 webserver_deploy (預定發布至 Heroku)

#### 使用方式 (基於 webserver_test)
1. 把資料夾複製到 linux 虛擬機中
2. 在 app.py 寫入 flask app
3. 把要用 render_template render 的 html 檔放入 templates
4. CSS、javascript 檔案放入 static
5. (第一次啟動或有修改 Dockerfile) ./start.sh
5. docker container start [container name]
