# -*- coding: cp949 -*-

import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import random
from app.predict.weather_data import get_weather_data
from app.predict.price_data import get_kamis_price_data


def get_napa_cabbage_price():
    load_dotenv()

    # kamis ���� ���� ��������
    days = 2
    p_itemcategorycode = '200'
    p_itemcode = '211'
    p_kindcode = ''
    kamis_price_data = get_kamis_price_data(days, p_itemcategorycode, p_itemcode, p_kindcode)
    print(kamis_price_data)

    # ��� ��� ������ ��������
    temp_start_days = 83
    temp_end_days = 67
    temp_column = '�� ��ձ��'
    temp_weather_data = get_weather_data(temp_start_days, temp_end_days, temp_column)
    print(temp_weather_data)

    # ������ ������ ��������
    rain_start_days = 38
    rain_end_days = 22
    rain_column = '�� ������'
    rain_weather_data = get_weather_data(rain_start_days, rain_end_days, rain_column)
    print(rain_weather_data)

    random_number = random.choices(range(3500, 20000), k=14)
    print(random_number)

    return random_number


def send_random_number_napa_cabbage():
    random_number = get_napa_cabbage_price()
    load_dotenv()
    spring_url = os.getenv('spring')
    api_url = f"{spring_url}/farmProduce/save-kimchi-cabbage-price"

    data = {"date": datetime.today().strftime('%Y-%m-%d'), "farmProduceName": "kimchiCabbage",
            "farmProducePrice": random_number}

    try:
        response = requests.post(api_url, json=data)

        if response.status_code == 200:
            print("���������� ���� ����")
        else:
            print("���������� ���� ����")
    except Exception as e:
        print(f"���� �߻�: {str(e)}")

