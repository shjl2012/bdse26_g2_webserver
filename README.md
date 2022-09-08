# bdse26_g2_webserver

v0：使用 tiangolo/uwsgi-nginx-flask-docker 的測試伺服器\
v1：使基於 ubuntu 2204 base image 建置的輕量設定包

※期末專題預定使用 v1 為基礎進行建置 (預定發布至 Heroku)

#### 使用方式 (基於 v1)
1. 把資料夾複製到 linux 虛擬機中
2. 在 app.py 寫入 flask app
3. 把要用 render_template render 的 html 檔放入 templates
4. CSS、javascript 檔案放入 static
5. 啟動 start.sh
