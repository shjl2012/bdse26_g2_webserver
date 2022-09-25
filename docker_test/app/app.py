from flask import Flask, render_template, request, redirect, url_for
from layer.data_preprocessing import HouseObject
from model.house_price_MLP import HousePriceModel
from global_function import *
from visDataProcess import *
import pandas as pd
import geopandas as gpd
import numpy as np
import json

# 預設地圖資料：台北市大安區復興南路一段390號(資展國際)
# 經緯度：house_lat, house_lon
# 交通運輸設施：tsp_count['total']
# 醫療設施：mdc_count['total']
# 超商：eco_count['conveniencestores']
# 學校：edu_count['schools']+edu_count['universities']
# 宮廟：sft_count['placeofworkships']
# 公園：env_count['parks']
tInput = {
    'county':'台北市', 
    'district':'大安區', 
    'street':'復興南路一段390號', 
    'target':'0', 
    'parking':'0', 
    'bedroom':'3', 
    'livingroom':'2', 
    'bathroom':'0', 
    'manage_org':'0', 
    'main_area':'60', 
    'sub_area':'0', 
    'balcony':'0', 
    'age':'10', 
    'elevator':'0', 
    'floor':'3', 
    'total_floor':'5', 
    'type':'2', 
}
tableDataProcess(tInput)
address = '台北市大安區復興南路一段390號'
house_lat, house_lon = 25.0337025, 121.5433029
price = [969067.87392507]
m20_Price, p20_Price, price = priceRange(price)
tsp_count = {'total': 66, 'parkings': 26, 'busstops': 40, 'MRTs': 9, 'TRAs': 0}
mdc_count = {'total': 216, 'hospitals': 2, 'clinics': 123, 'dentists': 70, 'pharmacies': 21}
eco_count = {'total': 37, 'conveniencestores': 36, 'fastfoods': 1}
edu_count = {'total': 11, 'libraries': 2, 'schools': 9, 'universities': 0}
sft_count = {'total': 10, 'firestations': 2, 'fuels': 1, 'markets': 2, 'polices': 2, 'placeofworkships': 3}
env_count = {'total': 24, 'cemeteries': 0, 'parks': 24, 'river_TWs': 0}
history_price = [833477.0339447, 925378.831485196, 979869.609188918, 912743.703340401, 857023.014172809, 855024.7936883, 873264.86275871, 865294.971969194, 850954.275523239, 958049.299337624]
house_six_ind = [9.7565967505099, 4.233315822475395, 5.216451566090331, 4.199755656122902, 4.270628270122547, 6.211347752246835]
dist_six_ind =  [8.066514993450667, 6.045381638868955, 5.921345331761821, 4.897790781128403, 4.3063164650807915, 5.881389971706659]
placeofworkships = {'type': 'FeatureCollection', 'features': [{'id': '2291', 'type': 'Feature', 'properties': {'full_id': 'n5110348782', 'name': '仁慈宮'}, 'geometry': {'type': 'Point', 'coordinates': [121.5457246, 25.033868700000003]}}, {'id': '2337', 'type': 'Feature', 'properties': {'full_id': 'n5699174878', 'name': '台北護靈宮'}, 'geometry': {'type': 'Point', 'coordinates': [121.5422416, 25.029478600000004]}}, {'id': '2338', 'type': 'Feature', 'properties': {'full_id': 'n5699174907', 'name': None}, 'geometry': {'type': 'Point', 'coordinates': [121.5441486, 25.029216099999996]}}]}
parks = {'type': 'FeatureCollection', 'features': [{'id': '46', 'type': 'Feature', 'properties': {'full_id': 'r6434668', 'name': '平安公園'}, 'geometry': {'type': 'Point', 'coordinates': [121.54927333479729, 25.031939604273767]}}, {'id': '105', 'type': 'Feature', 'properties': {'full_id': 'w18583895', 'name': '大安森林公園'}, 'geometry': {'type': 'Point', 'coordinates': [121.53572709082928, 25.030183875409396]}}, {'id': '113', 'type': 'Feature', 'properties': {'full_id': 'w55228247', 'name': '龍陣二號公園'}, 'geometry': {'type': 'Point', 'coordinates': [121.54253010366595, 25.02919265921805]}}, {'id': '189', 'type': 'Feature', 'properties': {'full_id': 'w197475260', 'name': '居安公園'}, 'geometry': {'type': 'Point', 'coordinates': [121.54932800767482, 25.029702034519715]}}, {'id': '341', 'type': 'Feature', 'properties': {'full_id': 'w264726963', 'name': '安祥公園'}, 'geometry': {'type': 'Point', 'coordinates': [121.54274223314731, 25.034545841508788]}}, {'id': '374', 'type': 'Feature', 'properties': {'full_id': 'w284359015', 'name': '四維公園'}, 'geometry': {'type': 'Point', 'coordinates': [121.54533069996721, 25.03063754980526]}}, {'id': '409', 'type': 'Feature', 'properties': {'full_id': 'w303275607', 'name': '新龍公園'}, 'geometry': {'type': 'Point', 'coordinates': [121.54019372354222, 25.027671371581082]}}, {'id': '410', 'type': 'Feature', 'properties': {'full_id': 'w303420866', 'name': '龍陣一號公園'}, 'geometry': {'type': 'Point', 'coordinates': [121.54254847744916, 25.027617355740823]}}, {'id': '414', 'type': 'Feature', 'properties': {'full_id': 'w303845484', 'name': '龍圖公園'}, 'geometry': {'type': 'Point', 'coordinates': [121.54165353518854, 25.03046761831683]}}, {'id': '415', 'type': 'Feature', 'properties': {'full_id': 'w303852587', 'name': '德安公園'}, 'geometry': {'type': 'Point', 'coordinates': [121.54777689075513, 25.034860049523186]}}, {'id': '421', 'type': 'Feature', 'properties': {'full_id': 'w304566637', 'name': '和安公園'}, 'geometry': {'type': 'Point', 'coordinates': [121.54451182356415, 25.034547625234303]}}, {'id': '422', 'type': 'Feature', 'properties': {'full_id': 'w304566638', 'name': '東豐公園'}, 'geometry': {'type': 'Point', 'coordinates': [121.54487450377201, 25.03581890847839]}}, {'id': '640', 'type': 'Feature', 'properties': {'full_id': 'w390780633', 'name': '台北好好看'}, 'geometry': {'type': 'Point', 'coordinates': [121.5384616803943, 25.031014210121082]}}, {'id': '646', 'type': 'Feature', 'properties': {'full_id': 'w403554086', 'name': '仁愛公園'}, 'geometry': {'type': 'Point', 'coordinates': [121.54625901087589, 25.03662467477857]}}, {'id': '647', 'type': 'Feature', 'properties': {'full_id': 'w403554087', 'name': '仁慈公園'}, 'geometry': {'type': 'Point', 'coordinates': [121.54575162562341, 25.034103635645675]}}, {'id': '648', 'type': 'Feature', 'properties': {'full_id': 'w403554088', 'name': '安東公園'}, 'geometry': {'type': 'Point', 'coordinates': [121.54482221025366, 25.028994737335147]}}, {'id': '649', 'type': 'Feature', 'properties': {'full_id': 'w403554089', 'name': '附中公園'}, 'geometry': {'type': 'Point', 'coordinates': [121.54229272200675, 25.03640387745949]}}, {'id': '798', 'type': 'Feature', 'properties': {'full_id': 'w549570624', 'name': None}, 'geometry': {'type': 'Point', 'coordinates': [121.53920956822701, 25.028929933281155]}}, {'id': '919', 'type': 'Feature', 'properties': {'full_id': 'w617310832', 'name': None}, 'geometry': {'type': 'Point', 'coordinates': [121.54890294418122, 25.030505999797732]}}, {'id': '920', 'type': 'Feature', 'properties': {'full_id': 'w617310833', 'name': None}, 'geometry': {'type': 'Point', 'coordinates': [121.54889063621611, 25.02906975872289]}}, {'id': '921', 'type': 'Feature', 'properties': {'full_id': 'w617310834', 'name': None}, 'geometry': {'type': 'Point', 'coordinates': [121.54892948877071, 25.031951271702916]}}, {'id': '922', 'type': 'Feature', 'properties': {'full_id': 'w617310835', 'name': None}, 'geometry': {'type': 'Point', 'coordinates': [121.54863313127494, 25.03206652598075]}}, {'id': '923', 'type': 'Feature', 'properties': {'full_id': 'w617310836', 'name': None}, 'geometry': {'type': 'Point', 'coordinates': [121.54861992845333, 25.03044486465368]}}, {'id': '924', 'type': 'Feature', 'properties': {'full_id': 'w617310837', 'name': None}, 'geometry': {'type': 'Point', 'coordinates': [121.548611390405, 25.028998174234708]}}]} 
schools = {'type': 'FeatureCollection', 'features': [{'id': '443', 'type': 'Feature', 'properties': {'full_id': 'r4676979', 'name': '仁愛國小'}, 'geometry': {'type': 'Point', 'coordinates': [121.55138972519298, 25.035865110321872]}}, {'id': '448', 'type': 'Feature', 'properties': {'full_id': 'r4730350', 'name': '師大附中'}, 'geometry': {'type': 'Point', 'coordinates': [121.54074096998589, 25.035258177629796]}}, {'id': '456', 'type': 'Feature', 'properties': {'full_id': 'r4774878', 'name': '大安高工'}, 'geometry': {'type': 'Point', 'coordinates': [121.54209608676811, 25.03195158954455]}}, {'id': '480', 'type': 'Feature', 'properties': {'full_id': 'r4790885', 'name': '大安國中'}, 'geometry': {'type': 'Point', 'coordinates': [121.5470283498368, 25.03040058024642]}}, {'id': '489', 'type': 'Feature', 'properties': {'full_id': 'r4790897', 'name': '私立延平中學'}, 'geometry': {'type': 'Point', 'coordinates': [121.53909419266488, 25.03652729188289]}}, {'id': '490', 'type': 'Feature', 'properties': {'full_id': 'r4790899', 'name': '建安國小'}, 'geometry': {'type': 'Point', 'coordinates': [121.54700678356096, 25.029362965711492]}}, {'id': '494', 'type': 'Feature', 'properties': {'full_id': 'r4790903', 'name': '懷生國中'}, 'geometry': {'type': 'Point', 'coordinates': [121.54111751017014, 25.040137590382276]}}, {'id': '528', 'type': 'Feature', 'properties': {'full_id': 'r4790939', 'name': '私立復興中小學'}, 'geometry': {'type': 'Point', 'coordinates': [121.54787937196922, 25.039336150598622]}}, {'id': '621', 'type': 'Feature', 'properties': {'full_id': 'r6889830', 'name': '開平餐飲學校'}, 'geometry': {'type': 'Point', 'coordinates': [121.54226047779959, 25.02866649367961]}}]}

hospitals = {'type': 'FeatureCollection', 'features': [{'id': '429', 'type': 'Feature', 'properties': {'機構名稱': '宏恩醫療財團法人宏恩綜合醫院', '型態別': '綜合醫院'}, 'geometry': {'type': 'Point', 'coordinates': [121.5466881, 25.038191599999994]}}, {'id': '433', 'type': 'Feature', 'properties': {'機構名稱': '中山醫療社團法人中山醫院', '型態別': '綜合醫院'}, 'geometry': {'type': 'Point', 'coordinates': [121.5499289, 25.036515]}}]}

conveniencestores = {'type': 'FeatureCollection', 'features': [{'id': '10789', 'type': 'Feature', 'properties': {'分公司名稱': '台北市第六O六分公司'}, 'geometry': {'type': 'Point', 'coordinates': [121.5360515, 25.034213600000005]}}, {'id': '10803', 'type': 'Feature', 'properties': {'分公司名稱': '台北市第九七一分公司'}, 'geometry': {'type': 'Point', 'coordinates': [121.5367438, 25.0327527]}}, {'id': '10813', 'type': 'Feature', 'properties': {'分公司名稱': '台北巿第３６１分公司'}, 'geometry': {'type': 'Point', 'coordinates': [121.53728920000002, 25.0363427]}}, {'id': '10836', 'type': 'Feature', 'properties': {'分公司名稱': '北市安建分公司'}, 'geometry': {'type': 'Point', 'coordinates': [121.53820649999999, 25.0348054]}}, {'id': '10859', 'type': 'Feature', 'properties': {'分公司名稱': '北市建國分公司'}, 'geometry': {'type': 'Point', 'coordinates': [121.53911400000001, 25.0294396]}}, {'id': '10862', 'type': 'Feature', 'properties': {'分公司名稱': '台北巿第１６０分公司'}, 'geometry': {'type': 'Point', 'coordinates': [121.53922110000002, 25.029078249999998]}}, {'id': '10867', 'type': 'Feature', 'properties': {'分公司名稱': '建國分公司'}, 'geometry': {'type': 'Point', 'coordinates': [121.5392682, 25.028654100000004]}}, {'id': '10869', 'type': 'Feature', 'properties': {'分公司名稱': '信美分公司'}, 'geometry': {'type': 'Point', 'coordinates': [121.53927940000001, 25.0330036]}}, {'id': '10925', 'type': 'Feature', 'properties': {'分公司名稱': '台北巿第１１０分公司'}, 'geometry': {'type': 'Point', 'coordinates': [121.54106209999999, 25.028544299999997]}}, {'id': '10956', 'type': 'Feature', 'properties': {'分公司名稱': '台北市第七九三分公司'}, 'geometry': {'type': 'Point', 'coordinates': [121.54227689999999, 25.0332039]}}, {'id': '10985', 'type': 'Feature', 'properties': {'分公司名稱': '興南分公司'}, 'geometry': {'type': 'Point', 'coordinates': [121.5432299, 25.027712299999997]}}, {'id': '10986', 'type': 'Feature', 'properties': {'分公司名稱': '台北巿第１９３分公司'}, 'geometry': {'type': 'Point', 'coordinates': [121.54326704999998, 25.030940349999998]}}, {'id': '10987', 'type': 'Feature', 'properties': {'分公司名稱': '台北市第七四八分公司'}, 'geometry': {'type': 'Point', 'coordinates': [121.543307, 25.035221]}}, {'id': '10988', 'type': 'Feature', 'properties': {'分公司名稱': '興忠分公司'}, 'geometry': {'type': 'Point', 'coordinates': [121.54344520000001, 25.039723099999996]}}, {'id': '11001', 'type': 'Feature', 'properties': {'分公司名稱': '興和分公司'}, 'geometry': {'type': 'Point', 'coordinates': [121.54378429999998, 25.028265499999993]}}, {'id': '11004', 'type': 'Feature', 'properties': {'分公司名稱': '台北市第四七九分公司'}, 'geometry': {'type': 'Point', 'coordinates': [121.54381390000002, 25.0322632]}}, {'id': '11005', 'type': 'Feature', 'properties': {'分公司名稱': '台北市第六八一分公司'}, 'geometry': {'type': 'Point', 'coordinates': [121.5439069, 25.0365515]}}, {'id': '11008', 'type': 'Feature', 'properties': {'分公司名稱': '興仁分公司'}, 'geometry': {'type': 'Point', 'coordinates': [121.54395829999999, 25.039100000000005]}}, {'id': '11009', 'type': 'Feature', 'properties': {'分公司名稱': '北市安復分公司'}, 'geometry': {'type': 'Point', 'coordinates': [121.54402605000001, 25.039935749999994]}}, {'id': '11015', 'type': 'Feature', 'properties': {'分公司名稱': '台北市第一七九分公司'}, 'geometry': {'type': 'Point', 'coordinates': [121.54412315000002, 25.039939649999997]}}, {'id': '11021', 'type': 'Feature', 'properties': {'分公司名稱': '台北巿第３６０分公司'}, 'geometry': {'type': 'Point', 'coordinates': [121.5442501, 25.036148799999996]}}, {'id': '11044', 'type': 'Feature', 'properties': {'分公司名稱': '台北市第四九五分公司'}, 'geometry': {'type': 'Point', 'coordinates': [121.54500680000001, 25.033039899999995]}}, {'id': '11052', 'type': 'Feature', 'properties': {'分公司名稱': '台北市第４１２分公司'}, 'geometry': {'type': 'Point', 'coordinates': [121.5453595, 25.038767699999998]}}, {'id': '11053', 'type': 'Feature', 'properties': {'分公司名稱': '台北巿第１８４分公司'}, 'geometry': {'type': 'Point', 'coordinates': [121.54539960000001, 25.028485300000003]}}, {'id': '11059', 'type': 'Feature', 'properties': {'分公司名稱': '台北市第五七一分公司'}, 'geometry': {'type': 'Point', 'coordinates': [121.54550720000002, 25.0361643]}}, {'id': '11062', 'type': 'Feature', 'properties': {'分公司名稱': '台北市第一０七二分公司'}, 'geometry': {'type': 'Point', 'coordinates': [121.5458156, 25.033676]}}, {'id': '11063', 'type': 'Feature', 'properties': {'分公司名稱': '台北巿第３５８分公司'}, 'geometry': {'type': 'Point', 'coordinates': [121.54585059999998, 25.030836400000002]}}, {'id': '11064', 'type': 'Feature', 'properties': {'分公司名稱': '台北巿第２５３分公司'}, 'geometry': {'type': 'Point', 'coordinates': [121.54585499999999, 25.0303178]}}, {'id': '11065', 'type': 'Feature', 'properties': {'分公司名稱': '台北市第４０１分公司'}, 'geometry': {'type': 'Point', 'coordinates': [121.54590140000002, 25.034337800000003]}}, {'id': '11097', 'type': 'Feature', 'properties': {'分公司名稱': '仁慈分公司'}, 'geometry': {'type': 'Point', 'coordinates': [121.54702750000001, 25.037108199999995]}}, {'id': '11105', 'type': 'Feature', 'properties': {'分公司名稱': '台北市第七六六分公司'}, 'geometry': {'type': 'Point', 'coordinates': [121.54742989999998, 25.0381722]}}, {'id': '11118', 'type': 'Feature', 'properties': {'分公司名稱': '第九七九分公司'}, 'geometry': {'type': 'Point', 'coordinates': [121.5480549, 25.033057199999995]}}, {'id': '11131', 'type': 'Feature', 'properties': {'分公司名稱': '台北市第六七四分公司'}, 'geometry': {'type': 'Point', 'coordinates': [121.5491721, 25.030107099999995]}}, {'id': '11142', 'type': 'Feature', 'properties': {'分公司名稱': '台北市第六０五分公司'}, 'geometry': {'type': 'Point', 'coordinates': [121.54955520000001, 25.031157099999998]}}, {'id': '11146', 'type': 'Feature', 'properties': {'分公司名稱': '敦新分公司'}, 'geometry': {'type': 'Point', 'coordinates': [121.54974230000002, 25.0369716]}}, {'id': '11156', 'type': 'Feature', 'properties': {'分公司名稱': '台北市第七二一分公司'}, 'geometry': {'type': 'Point', 'coordinates': [121.5501914, 25.0346191]}}]}

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
        df = create_df(request.values)

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

        hospitals = is_return_layer_empty(hospitals)

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

        price, house_six_ind, dist_six_ind, residuals, history_price = get_visualize_data(request.values, result)

        tInput = {
            'target':request.values['target'], 
            'parking':request.values['parking'], 
            'bedroom':request.values['bedroom'], 
            'livingroom':request.values['livingroom'], 
            'bathroom':request.values['bathroom'], 
            'manage_org':request.values['manage_org'], 
            'main_area':request.values['main_area'], 
            'sub_area':request.values['sub_area'], 
            'balcony':request.values['balcony'], 
            'age':request.values['age'], 
            'elevator':request.values['elevator'], 
            'floor':request.values['floor'], 
            'total_floor':request.values['total_floor'], 
            'type':request.values['type'], 
        }
        tableDataProcess(tInput)
        m20_Price, p20_Price, price = priceRange(price)

        return render_template('analysis.html', 
        tInput=tInput, 
        address=address,
        house_six_ind=house_six_ind, 
        dist_six_ind=dist_six_ind, 
        history_price=history_price,
        hospitals=hospitals, 
        house_lon=house_lon, 
        house_lat=house_lat, 
        conveniencestores=conveniencestores,
        parks=parks,
        schools=schools,
        placeofworkships=placeofworkships,
        price=price,
        m20_Price=m20_Price,
        p20_Price=p20_Price,
        mdc_count = mdc_count,
        eco_count = eco_count,
        edu_count = edu_count,
        sft_count = sft_count,
        env_count = env_count,
        tsp_count = tsp_count,
        )

# 數據分析頁
@app.route('/analysis')
def analysis():




    return render_template("analysis.html",
        tInput=tInput, 
        address=address,
        house_six_ind = house_six_ind, 
        dist_six_ind = dist_six_ind, 
        history_price=history_price, 
        hospitals=hospitals, 
        house_lon=house_lon, 
        house_lat=house_lat, 
        conveniencestores=conveniencestores,
        parks = parks, 
        schools=schools,
        placeofworkships = placeofworkships, 
        price=price,
        m20_Price=m20_Price,
        p20_Price=p20_Price,
        tsp_count = tsp_count, 
        mdc_count = mdc_count, 
        eco_count = eco_count, 
        edu_count = edu_count, 
        sft_count = sft_count, 
        env_count = env_count, 
        )

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
