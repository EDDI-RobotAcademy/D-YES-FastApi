# -*- coding: cp949 -*-

import requests
import os
from dotenv import load_dotenv
from datetime import datetime
from weather_data import get_weather_data
from price_data import get_kamis_price_data
import random


def get_young_pumpkin_price():
    load_dotenv()

    # kamis 애호박 가격 가져오기
    days = 2
    p_itemcategorycode = '200'
    p_itemcode = '224'
    p_kindcode = '01'
    kamis_price_data = get_kamis_price_data(days, p_itemcategorycode, p_itemcode, p_kindcode)
    print(kamis_price_data)

    # 평균 기온 데이터 가져오기
    temp_start_days = 130
    temp_end_days = 114
    temp_column = '일 평균기온'
    temp_weather_data = get_weather_data(temp_start_days, temp_end_days, temp_column)
    print(temp_weather_data)

    # 강수량 데이터 가져오기
    rain_start_days = 110
    rain_end_days = 94
    rain_column = '일 강수량'
    rain_weather_data = get_weather_data(rain_start_days, rain_end_days, rain_column)
    print(rain_weather_data)

    random_number = random.choices(range(8000, 40000), k=14)
    print(random_number)

    return random_number


def send_random_number_young_pumpkin():
    random_number = get_young_pumpkin_price()
    load_dotenv()
    spring_url = os.getenv('spring')
    api_url = f"{spring_url}/farmProduce/save-young-pumpkin-price"

    data = {"date": datetime.today().strftime('%Y-%m-%d'), "farmProduceName": "youngPumpkin",
            "farmProducePrice": random_number}

    try:
        response = requests.post(api_url, json=data)

        if response.status_code == 200:
            print("스프링으로 전송 성공")
        else:
            print("스프링으로 전송 실패")
    except Exception as e:
        print(f"오류 발생: {str(e)}")
