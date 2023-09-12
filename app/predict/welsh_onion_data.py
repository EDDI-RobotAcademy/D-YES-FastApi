# -*- coding: cp949 -*-

import requests
import os
from dotenv import load_dotenv
from datetime import datetime
from weather_data import get_weather_data
from price_data import get_kamis_price_data
import random


def get_welsh_onion_price():
    load_dotenv()

    # kamis ���� ���� ��������
    days = 2
    p_itemcategorycode = '200'
    p_itemcode = '246'
    p_kindcode = '00'
    kamis_price_data = get_kamis_price_data(days, p_itemcategorycode, p_itemcode, p_kindcode)
    print(kamis_price_data)

    # ��� ��� ������ ��������
    temp_start_days = 57
    temp_end_days = 41
    temp_column = '�� ��ձ��'
    temp_weather_data = get_weather_data(temp_start_days, temp_end_days, temp_column)
    print(temp_weather_data)

    # ������ ������ ��������
    rain_start_days = 21
    rain_end_days = 5
    rain_column = '�� ������'
    rain_weather_data = get_weather_data(rain_start_days, rain_end_days, rain_column)
    print(rain_weather_data)

    random_number = random.choices(range(1500, 5000), k=14)
    print(random_number)

    return random_number


def send_random_number_welsh_onion():
    random_number = get_welsh_onion_price()
    load_dotenv()
    spring_url = os.getenv('spring')
    api_url = f"{spring_url}/farmProduce/save-welsh-onion-price"

    data = {"date": datetime.today().strftime('%Y-%m-%d'), "farmProduceName": "welshOnion",
            "farmProducePrice": random_number}

    try:
        response = requests.post(api_url, json=data)

        if response.status_code == 200:
            print("���������� ���� ����")
        else:
            print("���������� ���� ����")
    except Exception as e:
        print(f"���� �߻�: {str(e)}")

