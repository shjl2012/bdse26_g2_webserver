from logging.config import dictConfig


def tableDataProcess(tInput:dict):
    """
    將使用者輸入房屋資訊轉換為視覺化需要資料型態
    """
    # 交易標的資料轉換
    tInput['target'] = '房子' if tInput['target']=='0' else '房子+車位'

    # 車位種類資料轉換
    parkingValue = {
    '0':'無車位', 
    '1':'一樓平面車位', 
    '2':'升降平面車位', 
    '3':'升降機械車位', 
    '4':'坡道平面車位', 
    '5':'坡道機械車位', 
    '6':'塔式車位', 
    '7':'其他'}
    for key, value in parkingValue.items():
        if tInput['parking'] == key:
            tInput['parking'] = value
        else:
            pass

    # 有無管理組職資料轉換
    tInput['manage_org'] = '有管理組職' if tInput['manage_org']=='1' else '無管理組職'

    # 電梯資料轉換
    elevatorValue = {
    '0':'無電梯', 
    '1':'有電梯',} 
    for key, value in elevatorValue.items():
        if tInput['elevator'] == key:
            tInput['elevator'] = value
        else:
            pass
    # tInput['elevator'] = '無電梯' if tInput['elevator']=='0' else '有電梯'

    # 建物型態資料轉換
    typeValue = {
    '1':'公寓', 
    '2':'華廈', 
    '3':'住宅大樓', 
    '4':'套房',}
    for key, value in typeValue.items():
        if tInput['type'] == key:
            tInput['type'] = value
        else:
            pass

    return tInput

def priceRange(price:list, history_price:list):
    """
    計算模型估價結果的±20%範圍，單位：萬元
    109年歷史平均價格，單位：萬元
    """
    m20_Price = round(float(price[0])/10000*0.8, 2)
    p20_Price = round(float(price[0])/10000*1.2, 2)
    price=round(float(price[0])/10000, 2)
    history_price_109 = round(float(history_price[8])/10000, 2)
    return m20_Price, p20_Price, price, history_price_109
