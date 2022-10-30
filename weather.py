# Reference:
# https://creepfablic.site/2021/11/14/python-weather-api/
import requests
import re
from datetime import datetime

city_code = '040010'
url = 'https://weather.tsukumijima.net/api/forecast/city/' + city_code

try:
    response = requests.get(url)
    response.raise_for_status()  # ステータスコード200番台以外は例外とする
except requests.exceptions.RequestException as e:
    print('Error:{}'.format(e))
else:
    weather_json = response.json()
    for key in weather_json.keys():
        print(key, weather_json[key])

    print(weather_json['forecasts'][0]['chanceOfRain'])  # 0:今日 1:明日 2:明後日
    # 現在の時間の降水確率を取得していく
    now_hour = datetime.now().hour
    if 0 <= now_hour < 6:
        cor = weather_json['forecasts'][0]['chanceOfRain']['T00_06']
    elif 6 <= now_hour < 12:
        cor = weather_json['forecasts'][0]['chanceOfRain']['T06_12']
    elif 12 <= now_hour < 18:
        cor = weather_json['forecasts'][0]['chanceOfRain']['T12_18']
    else:
        cor = weather_json['forecasts'][0]['chanceOfRain']['T18_24']

    print('現在の降水確率 {}'.format(cor))
