#!/bin/bash
# 把部署用資料複製入 docker app 中的 model 資料夾
dest="app/model/"
cp -r -p ../app_model_data/ ${dest}