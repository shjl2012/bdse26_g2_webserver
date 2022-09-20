from flask import Flask, render_template, request, redirect, url_for
from layer.data_preprocessing import HouseObject
from model.house_price_MLP import HousePriceModel
import pandas as pd
import geopandas as gpd
import numpy as np
import json

# 預設地圖資料
house_lat, house_lon = 25.033875600120034, 121.54337981087784
price = 888,888
hospitals = {"type": "FeatureCollection", "features": [{"id": "413", "type": "Feature", "properties": {"\u6a5f\u69cb\u540d\u7a31": "\u570b\u7acb\u81fa\u7063\u5927\u5b78\u91ab\u5b78\u9662\u9644\u8a2d\u91ab\u9662\u5152\u7ae5\u91ab\u9662", "\u578b\u614b\u5225": "\u7d9c\u5408\u91ab\u9662"}, "geometry": {"type": "Point", "coordinates": [121.51858300000002, 25.044327100000004]}}]}

conveniencestores = {"type": "FeatureCollection", "features": [{"id": "10013", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u90e1\u738b\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.5103524, 25.045046300000003]}}, {"id": "10021", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u4e00\u4e00\u516d\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.510632, 25.044974699999997]}}, {"id": "10022", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u81fa\u5317\u5dff\u7b2c\uff11\uff16\uff17\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.5106688, 25.05215859999999]}}, {"id": "10041", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u516b\u56db\u4e03\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.5111993, 25.044204599999997]}}, {"id": "10061", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u516d\u4e94\u56db\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.51160630000001, 25.0443137]}}, {"id": "10063", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u516d\u516b\u4e00\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.511644, 25.043066999999997]}}, {"id": "10080", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u4e09\u4e5d\u4e03\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.5122446, 25.045916550000005]}}, {"id": "10087", "type": 
"Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u4e00\uff10\u4e94\u516b\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.51252610000002, 25.0439381]}}, {"id": "10089", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u9d3b\u555f\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.5126107, 25.047133000000002]}}, {"id": "10094", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u4e94\u56db\u4e94\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.51284099999998, 25.0424069]}}, {"id": "10105", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u516d\u4e09\u4e94\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.51335819999998, 25.0515912]}}, {"id": "10108", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u4e94\u4e5d\u516b\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.5133769, 25.053872300000002]}}, {"id": "10110", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u516d\u5341\u56db\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.51352800000001, 25.0441669]}}, {"id": "10120", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u516d\u4e00\u4e03\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.5137413, 25.0424351]}}, {"id": "10121", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u516b\u516d\u4e8c\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.51375045, 25.053885249999993]}}, {"id": "10122", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u516d\u5341\u4e8c\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.51377699999999, 25.042208]}}, {"id": "10124", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u4e00\uff10\u4e8c\u4e94\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.51384300000001, 25.045078]}}, {"id": "10129", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u4e00\uff10\u4e09\u516b\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.5140123, 25.0450619]}}, {"id": "10132", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u7b2c\u4e09\uff10\u516b\uff10\u5206\u516c\u53f8"}, "geometry": {"type": 
"Point", "coordinates": [121.51412689999998, 25.051717300000004]}}, {"id": "10134", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u4e5d\u4e5d\u4e5d\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.5142103, 25.0468959]}}, {"id": "10136", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u897f\u7ad9\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.5143012, 25.046214499999998]}}, {"id": "10139", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u4e94\u516b\u56db\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.51440490000002, 25.0450598]}}, {"id": "10151", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u4e94\u4e94\u4e09\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.51479910000002, 25.044615199999996]}}, {"id": "10153", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u56db\u516d\u516d\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.5149173, 25.054354]}}, {"id": "10159", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u516d\u516d\u4e00\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.515144, 25.050517000000003]}}, {"id": "10160", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u516b\u4e94\u4e5d\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.51515140000001, 25.044830100000002]}}, 
{"id": "10165", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u7b2c\u4e03\u516b\u4e09\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.5152652, 25.053641299999995]}}, {"id": "10182", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u4e94\u4e5d\u4e00\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.51572749999998, 25.051799899999995]}}, {"id": "10185", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u516dO\u4e5d\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.51583, 25.046222]}}, {"id": "10186", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u5bcc\u967d\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.5158335, 25.043642599999995]}}, {"id": "10194", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u4e00\uff10\u4e03\u516b\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.51610145, 25.045098649999996]}}, {"id": "10197", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u4e03\u4e00\u4e09\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.5161821, 25.045743699999996]}}, {"id": "10200", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u5357\u967d\u5206\u516c\u53f8"}, "geometry": {"type": "Point", 
"coordinates": [121.5162199, 25.044802]}}, {"id": "10201", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u516d\u56db\u516b\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.51625820000001, 25.0460991]}}, {"id": "10215", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u56db\uff10\uff10\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.5166625, 25.050424499999995]}}, {"id": "10221", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u516d\u516d\u4e94\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.51675170000001, 25.044586499999998]}}, {"id": "10222", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u4e03\u4e09\u4e09\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.5167853, 25.045417699999998]}}, {"id": "10227", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u4e09\u4e09\u4e94\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.5169215, 25.045894899999997]}}, {"id": "10244", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u4e94\u56db\u4e8c\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.5174536, 25.0456119]}}, {"id": "10247", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u516b\u516b\u56db\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.5175818, 25.049840800000002]}}, {"id": "10260", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u4e5d\u4e00\u4e5d\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.51786419999999, 25.04638459999999]}}, {"id": "10261", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u516d\u4e03\u4e5d\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.5178865, 25.046358599999998]}}, {"id": "10268", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u4e03\u516d\u4e5d\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.51809965, 25.05088235]}}, {"id": "10276", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u4e5d\u4e03\u4e5d\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.5184218, 25.049631499999993]}}, {"id": "10285", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u7b2c\u4e09\u4e94\u4e03\u25cb\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.5187842, 25.052351099999996]}}, {"id": "10296", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u516d\u56db\u4e09\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.51929170000001, 25.053094899999998]}}, {"id": "10301", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u4e94\u4e5d\u4e5d\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.51935825, 25.05015005]}}, {"id": "10305", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u516d\u5341\u516d\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.51957815, 25.0458497]}}, {"id": "10312", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u7b2c\uff13\uff10\uff18\uff18\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.51987229999999, 25.052597900000002]}}, {"id": "10314", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u798f\u5b89\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.51987620000001, 25.0501431]}}, {"id": "10318", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u4e03\u4e00\u516d\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.519961, 25.050330399999996]}}, {"id": "10367", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u516d\u4e5d\u4e5d\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.52148040000002, 25.0518507]}}, {"id": "10371", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u516d\u5341\u4e09\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.52166400000002, 25.043755999999995]}}, {"id": "10406", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u4e03\u5341\u4e00\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.52273570000001, 25.050762699999996]}}, {"id": "10415", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u4e09\u4e00\u56db\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.5228762, 25.0493891]}}, {"id": "10421", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u65e5\u6d25\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.52311310000002, 25.0501523]}}, {"id": 
"12683", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u4e03\u4e5d\u516b\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.512025990372, 25.0517741351361]}}, {"id": "12688", "type": "Feature", "properties": {"\u5206\u516c\u53f8\u540d\u7a31": "\u53f0\u5317\u5e02\u7b2c\u516d\u4e00\u4e00\u5206\u516c\u53f8"}, "geometry": {"type": "Point", "coordinates": [121.51871680663798, 25.046173978885395]}}]}

mdc_count = {}

app = Flask(__name__)



# 首頁：網頁使用說明
@app.route('/')
def index():
    return render_template("index.html")

# 估價模型頁
@app.route('/model', methods=['GET', 'POST'])  # type: ignore
def get_form():
    # GET 方法
    if request.method == "GET":
        return render_template('model.html')
        # return render_template('model.html', page_header="Form")
    
    # POST 方法
    elif request.method == "POST":
        print(f'req_value:{request.values}')
        d1 = {
            '交易標的':[int(request.values['target'])],
            '建物現況格局-房':[int(request.values['bedroom'])],
            '建物現況格局-廳':[int(request.values['livingroom'])],
            '建物現況格局-衛':[int(request.values['bathroom'])],
            '有無管理組織':[int(request.values['manage_org'])],
            '主建物面積':[float(request.values['main_area'])],
            '附屬建物面積':[float(request.values['sub_area'])],
            '陽台面積':[float(request.values['balcony'])],
            '電梯':[int(request.values['elevator'])],
            '屋齡':[int(request.values['age'])],
            '交易年份':[111],
            'floor':[int(request.values['floor'])],
            'total_floor':[int(request.values['total_floor'])],
            '車位類別_一樓平面':[0],
            '車位類別_其他':[0],
            '車位類別_升降平面':[0],
            '車位類別_升降機械':[0],
            '車位類別_坡道平面':[0],
            '車位類別_坡道機械':[0],
            '車位類別_塔式車位':[0],
            '建物型態-公寓':[0],
            '建物型態-華廈':[0],
            '建物型態-住宅大樓':[0],
            '建物型態-套房':[0]
        }
        df = pd.DataFrame(data=d1)
        if request.values['parking'] == '1':
            df['車位類別_一樓平面'] = 1
        elif request.values['parking'] == '2':
            df['車位類別_升降平面'] = 1
        elif request.values['parking'] == '3':
            df['車位類別_升降機械'] = 1
        elif request.values['parking'] == '4':
            df['車位類別_坡道平面'] = 1
        elif request.values['parking'] == '5':
            df['車位類別_坡道機械'] = 1
        elif request.values['parking'] == '6':
            df['車位類別_塔式車位'] = 1
        elif request.values['parking'] == '7':
            df['車位類別_其他'] = 1

        if request.values['type'] == '1':
            df['建物型態-公寓'] = 1
        elif request.values['type'] == '2':
            df['建物型態-華廈'] = 1
        elif request.values['type'] == '3':
            df['建物型態-住宅大樓'] = 1
        elif request.values['type'] == '4':
            df['建物型態-套房'] = 1

        address = request.values['county'] + \
                  request.values['district'] + \
                  request.values['street']
        
        house = HouseObject(address)
        # User輸入地址的經緯度
        house_lon, house_lat = house.get_current_location()
        # 空間資訊處理
        house.create_buffer()
        
        # 醫療設施
        target_layer = gpd.read_file('./layer/medical_facilities/hospital.geojson', encoding = 'utf-8')
        hospital = house.sjoin_point_layer(target_layer, 'near_hospital', '機構名稱', 'near')
        hospitals = json.loads(hospital)
        target_layer = gpd.read_file('./layer/medical_facilities/clinic.geojson', encoding = 'utf-8')
        clinic = house.sjoin_point_layer(target_layer, 'clinic_count', '機構名稱', 'count')
        clinics = json.loads(clinic)     
        target_layer = gpd.read_file('./layer/medical_facilities/dentist.geojson', encoding = 'utf-8')
        dentist = house.sjoin_point_layer(target_layer, 'dentist_count', '機構名稱', 'count')
        dentists = json.loads(dentist)
        target_layer = gpd.read_file('./layer/medical_facilities/pharmacy.geojson', encoding = 'utf-8')
        pharmacy = house.sjoin_point_layer(target_layer, 'pharmacy_count', '機構名稱', 'count')
        pharmacies = json.loads(pharmacy)

        mdc_count = {'total':len(hospitals['features']) + len(clinics['features']) + len(dentists['features']) + len(pharmacies['features']),
        'hospitals': len(hospitals['features']),
        'clinics': len(clinics['features']),
        'dentists': len(dentists['features']),
        'pharmacies': len(pharmacies['features'])}

        if len(hospitals['features']) == 0:
            print('hospital is null')
            hospitals = {"type": "FeatureCollection", "features": [{"id": "", "type": "Feature", "properties": {"": "", "": ""}, "geometry": {"type": "Point", "coordinates": [0, 0]}}]}

        # 經濟指標
        target_layer = gpd.read_file('./layer/economic_indicators/conveniencestore.geojson', encoding = 'utf-8')
        conveniencestore = house.sjoin_point_layer(target_layer, 'conveniencestore_count', '分公司名稱', 'count')
        conveniencestores = json.loads(conveniencestore)
        target_layer = gpd.read_file('./layer/economic_indicators/fastfood.geojson', encoding = 'utf-8')
        fastfood = house.overlay_polygon_layer(target_layer, 'fastfood_count', 'full_id', 'count')
        fastfoods = json.loads(fastfood)

        eco_count = {'total': len(conveniencestores['features']) + len(fastfoods['features']),
        'conveniencestores': len(conveniencestores['features']),
        'fastfoods': len(fastfoods['features'])}

        # 文教機構
        target_layer = gpd.read_file('./layer/educational_resources/library.geojson', encoding = 'utf-8')
        library = house.overlay_polygon_layer(target_layer, 'library_count', 'full_id', 'count')
        libraries = json.loads(library)
        target_layer = gpd.read_file('./layer/educational_resources/school.geojson', encoding = 'utf-8')
        school = house.overlay_polygon_layer(target_layer, 'near_school', 'full_id', 'near')
        schools = json.loads(school)
        target_layer = gpd.read_file('./layer/educational_resources/university.geojson', encoding = 'utf-8')
        university = house.overlay_polygon_layer(target_layer, 'near_university', 'full_id', 'near')
        universities = json.loads(university)

        edu_count = {'total': len(libraries['features']) + len(schools['features']) + + len(universities['features']),
        'libraries': len(libraries['features']),
        'schools': len(schools['features']),
        'universities': len(universities['features'])}

        # 公共安全
        target_layer = gpd.read_file('./layer/public_safety/firestation.geojson', encoding = 'utf-8')
        firestation = house.sjoin_point_layer(target_layer, 'near_firestation', '消防隊名稱', 'near')
        firestations = json.loads(firestation)
        target_layer = gpd.read_file('./layer/public_safety/fuel.geojson', encoding = 'utf-8')
        fuel = house.overlay_polygon_layer(target_layer, 'near_fuel', 'full_id', 'near')
        fuels = json.loads(fuel)
        target_layer = gpd.read_file('./layer/public_safety/market.geojson', encoding = 'utf-8')
        market = house.overlay_polygon_layer(target_layer, 'near_market', 'full_id', 'near')
        markets = json.loads(market)
        target_layer = gpd.read_file('./layer/public_safety/police.geojson', encoding = 'utf-8')
        police = house.sjoin_point_layer(target_layer, 'near_police', '中文單位名稱', 'near')
        polices = json.loads(police)
        target_layer = gpd.read_file('./layer/public_safety/placeofworkship.geojson', encoding = 'utf-8')
        placeofworkship = house.overlay_polygon_layer(target_layer, 'placeofworkship_count', 'full_id', 'count')
        placeofworkships = json.loads(placeofworkship)

        sft_count = {'total': len(firestations['features']) + len(fuels['features']) + len(markets['features']) + len(polices['features']) + len(placeofworkships['features']),
        'firestations': len(firestations['features']),
        'fuels': len(fuels['features']),
        'markets': len(markets['features']),
        'polices': len(polices['features']),
        'placeofworkships': len(placeofworkships['features'])}

        # 自然環境
        target_layer = gpd.read_file('./layer/natural_environment/cemetery.geojson', encoding = 'utf-8')
        cemetery = house.overlay_polygon_layer(target_layer, 'cemetery_area', 'full_id', 'area')
        cemeteries = json.loads(cemetery)
        target_layer = gpd.read_file('./layer/natural_environment/park.geojson', encoding = 'utf-8')
        park = house.overlay_polygon_layer(target_layer, 'park_area', 'full_id', 'area')
        parks = json.loads(park)
        target_layer = gpd.read_file('./layer/natural_environment/river_TW.geojson', encoding = 'utf-8')
        river_TW = house.overlay_polygon_layer(target_layer, 'river_TW_area', 'full_id', 'area')
        river_TWs = json.loads(river_TW)

        env_count = {'total': len(cemeteries['features']) + len(parks['features']) + len(river_TWs['features']),
        'cemeteries': len(cemeteries['features']),
        'parks': len(parks['features']),
        'river_TWs': len(river_TWs['features'])}

        # 交通運輸
        target_layer = gpd.read_file('./layer/transportation/parking.geojson', encoding = 'utf-8')
        parking = house.overlay_polygon_layer(target_layer, 'parking_area', 'full_id', 'area')
        parkings = json.loads(parking)
        target_layer = gpd.read_file('./layer/transportation/busstop.geojson', encoding = 'utf-8')
        busstop = house.sjoin_point_layer(target_layer, 'busstop_count', 'full_id', 'count')
        busstops = json.loads(busstop)
        target_layer = gpd.read_file('./layer/transportation/LRT.geojson', encoding = 'utf-8')
        LRT = house.sjoin_point_layer(target_layer, 'near_LRT', 'MARKID', 'near')
        LRTs = json.loads(LRT)
        target_layer = gpd.read_file('./layer/transportation/MRT.geojson', encoding = 'utf-8')
        MRT = house.sjoin_point_layer(target_layer, 'near_MRT', 'MARKID', 'near')
        MRTs = json.loads(MRT)
        target_layer = gpd.read_file('./layer/transportation/TRA.geojson', encoding = 'utf-8')
        TRA = house.sjoin_point_layer(target_layer, 'near_TRA', 'MARKID', 'near')
        TRAs = json.loads(TRA)

        tsp_count = {'total': len(parkings['features']) + len(busstops['features']) + len(LRTs['features']) + len(TRAs['features']),
        'parkings': len(parkings['features']),
        'busstops': len(busstops['features']),
        'MRTs': len(MRTs['features']),
        'TRAs': len(TRAs['features'])}

        result = house.return_geo_dataframe()
        result = df.join(result)

        if request.values['county'] == '台北市':
            d2 = {
                '中山區':[0],
                '中正區':[0],
                '信義區':[0],
                '內湖區':[0],
                '北投區':[0],
                '南港區':[0],
                '士林區':[0],
                '大同區':[0],
                '大安區':[0],
                '文山區':[0],
                '松山區':[0],
                '萬華區':[0]
            }
            df2 = pd.DataFrame(data=d2)
            df2[request.values['district']] = 1
            result.drop(['idx','lon','lat','geometry','near_fuel_dist','near_market_dist','near_LRT_250','near_LRT_500','near_LRT_750'],axis=1,inplace=True)
            result = result.join(df2)
            lst = result.values.tolist()

            TPE_model = HousePriceModel('TPE')
            analysis_data, price = TPE_model.predictPrice(lst[0])
            price = price * 3.3058
            analysis_data = analysis_data[0]
            medical_facilities_indicators = analysis_data[26] + analysis_data[30] + analysis_data[33] + analysis_data[36]
            economic_indicators_indicators = analysis_data[39] + analysis_data[42]
            educational_resources_indicators = analysis_data[45] + analysis_data[48] + analysis_data[52] + analysis_data[56]
            public_safety_indicators = analysis_data[60] - analysis_data[63] - analysis_data[66] + analysis_data[69]
            natural_environment_indicators = analysis_data[72] + analysis_data[75] - analysis_data[78]
            transportation_indicators = analysis_data[81] + analysis_data[84] + analysis_data[88] + analysis_data[92]

            ind = pd.read_csv('./model/TPE/Min_max_data.csv')
            s1 = (ind.iloc[0,2] - ind.iloc[0,1])/10
            s2 = (ind.iloc[0,4] - ind.iloc[0,3])/10
            s3 = (ind.iloc[0,6] - ind.iloc[0,5])/10
            s4 = (ind.iloc[0,8] - ind.iloc[0,7])/10
            s5 = (ind.iloc[0,10] - ind.iloc[0,9])/10
            s6 = (ind.iloc[0,12] - ind.iloc[0,11])/10

            # 房屋六圍
            values = [(medical_facilities_indicators- ind.iloc[0,1]) / s1,
            (economic_indicators_indicators- ind.iloc[0,3]) / s2,
            (educational_resources_indicators - ind.iloc[0,5]) / s3,
            (public_safety_indicators - ind.iloc[0,7]) / s4,
            (natural_environment_indicators - ind.iloc[0,9]) / s5,
            (transportation_indicators- ind.iloc[0,11]) / s6]

            dis = pd.read_csv('./model/TPE/district_data.csv')
            testLst = dis['dist'].tolist()
            print(testLst)
            distt = 0
            i = 0
            for t in testLst:
                if t == request.values['district']:
                    distt = i
                i = i + 1

            # 行政區六圍
            values2 = [(dis.iloc[distt,2:8].tolist()[0]- ind.iloc[0,1]) / s1,
            (dis.iloc[distt,2:8].tolist()[1]- ind.iloc[0,3]) / s2,
            (dis.iloc[distt,2:8].tolist()[2] - ind.iloc[0,5]) / s3,
            (dis.iloc[distt,2:8].tolist()[3] - ind.iloc[0,7]) / s4,
            (dis.iloc[distt,2:8].tolist()[4] - ind.iloc[0,9]) / s5,
            (dis.iloc[distt,2:8].tolist()[5]- ind.iloc[0,11]) / s6]
            # 模型精度圖
            residuals = pd.read_csv('./model/TPE/TPE_residuals.csv')
            residuals = residuals.iloc[:,1].tolist()
            # 行政區歷史成交資訊
            history_price = pd.read_csv('./model/TPE/TPE_history_price.csv')
            history_price = history_price.iloc[distt,2:11].tolist()

        if request.values['county'] == '新北市':
            d2 = {
                '三峽區':[0],
                '三芝區':[0],
                '三重區':[0],
                '中和區':[0],
                '五股區':[0],
                '八里區':[0],
                '土城區':[0],
                '新店區':[0],
                '新莊區':[0],
                '板橋區':[0],
                '林口區':[0],
                '樹林區':[0],
                '永和區':[0],
                '汐止區':[0],
                '泰山區':[0],
                '淡水區':[0],
                '深坑區':[0],
                '烏來區':[0],
                '瑞芳區':[0],
                '石碇區':[0],
                '石門區':[0],
                '萬里區':[0],
                '蘆洲區':[0],
                '貢寮區':[0],
                '金山區':[0],
                '雙溪區':[0],
                '鶯歌區':[0]
            }
            df2 = pd.DataFrame(data=d2)
            df2[request.values['district']] = 1
            result.drop(['idx','lon','lat','geometry','near_fuel_dist','near_market_dist'],axis=1,inplace=True)
            result = result.join(df2)
            lst = result.values.tolist()
            print(lst[0])

            NTPC_model = HousePriceModel('NTPC')
            analysis_data, price = NTPC_model.predictPrice(lst[0])
            price = price * 3.3058
            print(price)
            
        if request.values['county'] == '基隆市':
            d2 = {
                '七堵區':[0],
                '中山區':[0],
                '中正區':[0],
                '仁愛區':[0],
                '信義區':[0],
                '安樂區':[0],
                '暖暖區':[0]
            }
            df2 = pd.DataFrame(data=d2)
            df2[request.values['district']] = 1
            result.drop(['idx','lon','lat','geometry','near_fuel_dist','near_market_dist','near_hospital_dist','near_university','near_LRT_250','near_LRT_500','near_LRT_750','near_LRT_dist','near_MRT_250','near_MRT_500','near_MRT_750','near_MRT_dist'],axis=1,inplace=True)
            result = result.join(df2)
            lst = result.values.tolist()
            print(lst[0])

            KEL_model = HousePriceModel('TPE')
            price = KEL_model.predictPrice(lst[0]) * 3.3058
            print(price)


        # return redirect("analysis")
        return render_template('analysis.html', 
        hospital=hospitals, 
        house_lon=house_lon, 
        house_lat=house_lat, 
        conveniencestore=conveniencestores,
        price=price,
        mdc_count = mdc_count,
        eco_count = eco_count,
        edu_count = edu_count,
        sft_count = sft_count,
        env_count = env_count,
        tsp_count = tsp_count,
        values=values,
        values2=values2)

# 數據分析頁
@app.route('/analysis')
def analysis():
    return render_template("analysis.html",conveniencestore=conveniencestores, hospital=hospitals , house_lon=house_lon, house_lat=house_lat, price=price, mdc_count = mdc_count)

# 組員介紹頁
@app.route('/team')
def team():
    return render_template("team.html")




#功能測試頁：完成後需移除
@app.route('/test')  # type: ignore
def test():
    if request.method == "GET":
        return render_template('test.html')
    
    # POST 方法
    elif request.method == "POST":
        return redirect("analysis.html")



if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
