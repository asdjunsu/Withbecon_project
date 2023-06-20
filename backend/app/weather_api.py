import datetime
import json
import requests
import schedule
import time
def get_weather_info():
    '''
    ## Returns:
    ---
        uv, temperature, humidity, pm10, pm2_5
    '''

    KEY = r"RtLjsO4iuG6A8XNiSPCOwxz62ODAg2OdV3rUCpPnxujQJtIkhiSgU3qVG4iXkROeB/kNeBtZbfUU7bJBwqkQvQ=="
    UV_URL = 'http://apis.data.go.kr/1360000/LivingWthrIdxServiceV4/getUVIdxV4'
    TEMP_HUM_URL = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
    DUST_URL = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty'

    now = datetime.datetime.now()

    uv_time = now.strftime('%Y%m%d%H')
    uv_params = {
        'ServiceKey': KEY,
        'pageNo': '1',
        'numOfRows': '10',
        'dataType': 'JSON',
        'areaNo': '2700000000',
        'time': uv_time
    }
    uv_response = requests.get(UV_URL, params=uv_params)
    uv_response_json = json.loads(uv_response.content)
    uv = uv_response_json['response']['body']['items']['item'][0]['h0']
    temp_hum_hour = now.hour
    temp_hum_minute = now.minute

    if temp_hum_minute < 40:
        temp_hum_hour -= 1
        if temp_hum_hour < 0:
            temp_hum_hour = 23

    temp_hum_date = now.strftime('%Y%m%d')
    temp_hum_time = f'{temp_hum_hour:02}00'
    x_code, y_code = '89', '91'
    temp_params ={
        'serviceKey' : KEY, 
        'pageNo' : '1',
        'numOfRows' : '10',
        'dataType' : 'JSON', 
        'base_date' : temp_hum_date, 
        'base_time' : temp_hum_time, 
        'nx' : x_code, 
        'ny' : y_code 
    }
    temp_hum_response = requests.get(TEMP_HUM_URL, params=temp_params)
    temp_hum_response_json = json.loads(temp_hum_response.content)
    observe_value_list = temp_hum_response_json['response']['body']['items']['item']
    for value in observe_value_list:
        if value['category'] == 'T1H':
            temperature = value['obsrValue']
        elif value['category'] == 'REH':
            humidity = value['obsrValue']


    dust_params = {
        'serviceKey': KEY,
        'returnType': 'JSON',
        'numOfRows': '10',
        'pageNo': '1',
        'sidoName': '대구',
        'ver': '1.3'
    }

    dust_response = requests.get(DUST_URL, params=dust_params)
    dust_response_json = json.loads(dust_response.content)
    dust_value_list = dust_response_json['response']['body']['items']
    pm10_list = []
    pm2_5_list = []
    for value in dust_value_list:
        if value['pm10Value']:
            try:
                pm10_list.append(int(value['pm10Value']))
            except:
                pass
        if value['pm25Value']:
            try:
                pm2_5_list.append(int(value['pm25Value']))
            except:
                pass


    pm10 =  round(sum(pm10_list)/len(pm10_list),2)
    pm2_5 = round(sum(pm2_5_list)/len(pm2_5_list),2)

    data= {
            'uv': int(uv), 
            'temperature':float(temperature), 
            'humidity': int(humidity),
            'pm10' : pm10,
            'pm2_5' : pm2_5
            }
    return data

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

def update_weather_data():
    global weather_data
    new_data = get_weather_info()
    if new_data is not None:
        weather_data = new_data
        print(weather_data)
    return weather_data


# def update_weather_data(weather_data):
#     uv, temperature, humidity, pm10, pm2_5 = get_weather_info()
#     weather_data.update({
#         'uv': uv,
#         'temperature': temperature,
#         'humidity': humidity,
#         'pm10': pm10,
#         'pm2_5': pm2_5
#     })


# if __name__ == '__main__':
#     start_time = time.time()
#     uv, temperature, humidity, pm10, pm2_5 = get_weather_info()
#     end_time = time.time()
#     print(uv, temperature, humidity, pm10, pm2_5)
#     print('총 소요 시간:', end_time - start_time)