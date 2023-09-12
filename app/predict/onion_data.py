# -*- coding: cp949 -*-

import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import random
from app.predict.weather_data import get_weather_data
from app.predict.price_data import get_kamis_price_data


def get_onion_price():
    load_dotenv()

    # kamis 양파 가격 가져오기
    days = 2
    p_itemcategorycode = '200'
    p_itemcode = '245'
    p_kindcode = '00'
    kamis_price_data = get_kamis_price_data(days, p_itemcategorycode, p_itemcode, p_kindcode)
    print(kamis_price_data)

    # 평균 기온 데이터 가져오기
    temp_start_days = 120
    temp_end_days = 104
    temp_column = '일 평균기온'
    temp_weather_data = get_weather_data(temp_start_days, temp_end_days, temp_column)
    print(temp_weather_data)

    # 강수량 데이터 가져오기
    rain_start_days = 83
    rain_end_days = 67
    rain_column = '일 강수량'
    rain_weather_data = get_weather_data(rain_start_days, rain_end_days, rain_column)
    print(rain_weather_data)

    random_number = random.choices(range(6000, 25000), k=14)
    print(random_number)

    return random_number


def send_random_number_onion():
    random_number = get_onion_price()
    load_dotenv()
    spring_url = os.getenv('spring')
    api_url = f"{spring_url}/farmProduce/save-onion-price"

    data = {"date": datetime.today().strftime('%Y-%m-%d'), "farmProduceName": "onion",
            "farmProducePrice": random_number}

    try:
        response = requests.post(api_url, json=data)

        if response.status_code == 200:
            print("스프링으로 전송 성공")
        else:
            print("스프링으로 전송 실패")
    except Exception as e:
        print(f"오류 발생: {str(e)}")
