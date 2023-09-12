# -*- coding: cp949 -*-

from dotenv import load_dotenv
import requests
import random
import os
from datetime import datetime
from weather_data import get_weather_data
from price_data import get_kamis_price_data


def get_cabbage_price():
    load_dotenv()

    # kamis 양배추 가격 가져오기
    days = 2
    p_itemcategorycode = '200'
    p_itemcode = '212'
    p_kindcode = '00'
    kamis_price_data = get_kamis_price_data(days, p_itemcategorycode, p_itemcode, p_kindcode)
    print(kamis_price_data)

    # 평균 기온 데이터 가져오기
    temp_start_days = 77
    temp_end_days = 61
    temp_column = '일 평균기온'
    temp_weather_data = get_weather_data(temp_start_days, temp_end_days, temp_column)
    print(temp_weather_data)

    # 강수량 데이터 가져오기
    rain_start_days = 60
    rain_end_days = 44
    rain_column = '일 강수량'
    rain_weather_data = get_weather_data(rain_start_days, rain_end_days, rain_column)
    print(rain_weather_data)

    random_number = random.choices(range(4000, 6000), k=14)
    print(random_number)

    return random_number


def send_random_number_cabbage():
    random_number = get_cabbage_price()
    spring_url = os.getenv('spring')
    api_url = f"{spring_url}/farmProduce/save-cabbage-price"

    data = {"date": datetime.today().strftime('%Y-%m-%d'), "farmProduceName": "cabbage",
            "farmProducePrice": random_number}

    try:
        response = requests.post(api_url, json=data)

        if response.status_code == 200:
            print("스프링으로 전송 성공")
        else:
            print("스프링으로 전송 실패")
    except Exception as e:
        print(f"오류 발생: {str(e)}")
