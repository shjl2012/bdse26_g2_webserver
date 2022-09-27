import pandas as pd
from model.house_price_MLP import HousePriceModel

def is_return_layer_empty(layer):
    if len(layer['features']) == 0:
        return_layer = {"type": "FeatureCollection", "features": [{"id": "", "type": "Feature", "properties": {"": "", "": ""}, "geometry": {"type": "Point", "coordinates": [0, 0]}}]}
    else:
        return_layer = layer
    return return_layer

def create_df(values):
    d1 = {
            '交易標的':[int(values['target'])],
            '建物現況格局-房':[int(values['bedroom'])],
            '建物現況格局-廳':[int(values['livingroom'])],
            '建物現況格局-衛':[int(values['bathroom'])],
            '有無管理組織':[int(values['manage_org'])],
            '主建物面積':[float(values['main_area'])],
            '附屬建物面積':[float(values['sub_area'])],
            '陽台面積':[float(values['balcony'])],
            '電梯':[int(values['elevator'])],
            '屋齡':[int(values['age'])],
            '交易年份':[111],
            'floor':[int(values['floor'])],
            'total_floor':[int(values['total_floor'])],
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
    if values['parking'] == '1':
        df['車位類別_一樓平面'] = 1
    elif values['parking'] == '2':
        df['車位類別_升降平面'] = 1
    elif values['parking'] == '3':
        df['車位類別_升降機械'] = 1
    elif values['parking'] == '4':
        df['車位類別_坡道平面'] = 1
    elif values['parking'] == '5':
        df['車位類別_坡道機械'] = 1
    elif values['parking'] == '6':
        df['車位類別_塔式車位'] = 1
    elif values['parking'] == '7':
        df['車位類別_其他'] = 1

    if values['type'] == '1':
        df['建物型態-公寓'] = 1
    elif values['type'] == '2':
        df['建物型態-華廈'] = 1
    elif values['type'] == '3':
        df['建物型態-住宅大樓'] = 1
    elif values['type'] == '4':
        df['建物型態-套房'] = 1

    return df

def get_visualize_data(values, result):
    if values['county'] == '台北市':
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
        df2[values['district']] = 1
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
        house_six_ind = [(medical_facilities_indicators- ind.iloc[0,1]) / s1,
        (economic_indicators_indicators- ind.iloc[0,3]) / s2,
        (educational_resources_indicators - ind.iloc[0,5]) / s3,
        (public_safety_indicators - ind.iloc[0,7]) / s4,
        (natural_environment_indicators - ind.iloc[0,9]) / s5,
        (transportation_indicators- ind.iloc[0,11]) / s6]

        dis = pd.read_csv('./model/TPE/district_data.csv')
        testLst = dis['dist'].tolist()
        distt = 0
        i = 0
        for t in testLst:
            if t == values['district']:
                distt = i
            i = i + 1

        # 行政區六圍
        dist_six_ind = [(dis.iloc[distt,2:8].tolist()[0]- ind.iloc[0,1]) / s1,
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
        history_price = history_price.iloc[distt,2:12].tolist()

        return price, house_six_ind, dist_six_ind, residuals, history_price

    if values['county'] == '新北市':
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
        df2[values['district']] = 1
        result.drop(['idx','lon','lat','geometry','near_fuel_dist','near_market_dist'],axis=1,inplace=True)
        result = result.join(df2)
        lst = result.values.tolist()
        print(lst[0])

        NTPC_model = HousePriceModel('NTPC')
        analysis_data, price = NTPC_model.predictPrice(lst[0])
        price = price * 3.3058
        print(price)
        
    if values['county'] == '基隆市':
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
        df2[values['district']] = 1
        result.drop(['idx','lon','lat','geometry','near_fuel_dist','near_market_dist','near_hospital_dist','near_university','near_LRT_250','near_LRT_500','near_LRT_750','near_LRT_dist','near_MRT_250','near_MRT_500','near_MRT_750','near_MRT_dist'],axis=1,inplace=True)
        result = result.join(df2)
        lst = result.values.tolist()
        print(lst[0])

        KEL_model = HousePriceModel('TPE')
        price = KEL_model.predictPrice(lst[0]) * 3.3058
        print(price)