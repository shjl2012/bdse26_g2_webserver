ARG CODE_VERSION=22.04
FROM ubuntu:${CODE_VERSION}
LABEL maintainer='BDSE26_Group2'

# switch working directory
WORKDIR /app

# 把目前目錄下的 ./app 複製到 /app
COPY ./app /app

# 安裝必要套件 (apt-get)
RUN apt-get update && \
    apt-get install -y wget && \
    apt-get install -y python3-dev && \
    apt-get install -y gdal-bin && \
    apt-get install -y libgdal-dev && \ 
    apt-get install -y g++

RUN wget https://bootstrap.pypa.io/get-pip.py && \
    python3 get-pip.py

# 安裝必要套件 (pip3 install -r 從檔案讀取要安裝的套件以及版本)
RUN pip3 install -r requirements.txt

# 啟動 container 時直接跑 flask app
# 以下2種寫法都測試過可以使用
#ENTRYPOINT FLASK_APP=/app/app.py flask run --host=0.0.0.0
ENTRYPOINT [ "python3", "app.py" ]
